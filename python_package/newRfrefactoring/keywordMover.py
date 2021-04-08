import ast
from robot.parsing.model import Statement
from robot.api import Token
from python_package.newRfrefactoring.utility import normalize, get_file_name_from_path
from python_package.newRfrefactoring.fileChecker import FileChecker
from python_package.newRfrefactoring.keywordFinder import KeywordFinder


class KeywordMover(ast.NodeTransformer):

    def __init__(self, modelsInDir):
        self.finder = KeywordFinder()
        self.checker = FileChecker()
        self.modelsInDir = modelsInDir
        self.movedKeywordNode = None
        self.removeOldKeywordDefined = False
        self.insertKeywordDefined = False
        self.importResource = False

    def visit_SettingSection(self, node):
        if(self.importResource):
            newResource = Statement.from_tokens([
                Token(Token.RESOURCE, 'Resource'),
                Token(Token.SEPARATOR, '    '),
                Token(Token.NAME, 'testResource.txt'),
                Token(Token.EOL, '\n')
            ])
            node.body.insert(0, newResource)
        return node

    def visit_Keyword(self, node):
        if(self.removeOldKeywordDefined):
            if(node == self.movedKeywordNode):
                return None
        return node

    def visit_KeywordSection(self, node):
        """
            Visit all keyword's define to do something.
        """
        if(self.insertKeywordDefined):
            empty_line = Statement.from_tokens([Token(Token.EOL, '\n')])
            node.body.append(empty_line)
            node.body.append(self.movedKeywordNode)

        return self.generic_visit(node)

    def move_keyword_defined_to_file(self, movedKeywordName, fromFileModel, targetFileModel):

        def split_models_without_import(allModels, modelsWithImport):
            for model in modelsWithImport:
                if(model in allModels):
                    allModels.remove(model)
            return allModels
        
        def update_model(model, allModels):
            for index, oldModel in enumerate(allModels):
                if isinstance(oldModel, list):
                    update_model(model, oldModel)
                elif(model.source == oldModel.source):
                    allModels[index] = model

        def find_moved_keyword_node(fromFileModel, movedKeywordName):
            self.finder.visit_model_for_finding_keyword(fromFileModel, movedKeywordName)
            return self.finder.get_keyword_defs()[0]['keywordNode']

        def save_model_and_update_old_models(model, oldModels):
            model.save()
            update_model(model, oldModels)

        def remove_old_keyword_defined(model):
            self.removeOldKeywordDefined = True
            self.visit(model)
            save_model_and_update_old_models(model, self.modelsInDir)
            self.removeOldKeywordDefined = False

        def insert_new_keyword_defined(model):
            self.insertKeywordDefined = True
            self.visit(model)
            save_model_and_update_old_models(model, self.modelsInDir)
            self.insertKeywordDefined = False

        def get_models_without_import_new_resource(movedKeywordName, oldImportedResource, newImportedResource):
            oldImportedResourceName = get_file_name_from_path(oldImportedResource.source)
            self.checker.visit_models_to_check_keyword_and_resource(self.modelsInDir, movedKeywordName, oldImportedResourceName)
            modelsUsingKeyword = self.checker.get_models_with_resource_and_keyword()
            self.checker.clear_models_with_resource_and_keyword()
            newImportedResourceName = get_file_name_from_path(newImportedResource.source)
            self.checker.visit_models_to_check_keyword_and_resource(modelsUsingKeyword, movedKeywordName, newImportedResourceName)
            modelsWithImport = self.checker.get_models_with_resource_and_keyword()
            return split_models_without_import(modelsUsingKeyword, modelsWithImport)

        def import_new_resource_for_models(modelsWithoutImport):
            self.importResource = True
            for model in modelsWithoutImport:
                self.visit(model)
                save_model_and_update_old_models(model, self.modelsInDir)
            self.importResource = False

        self.movedKeywordNode = find_moved_keyword_node(fromFileModel, movedKeywordName)
        remove_old_keyword_defined(fromFileModel)
        insert_new_keyword_defined(targetFileModel)
        modelsWithoutImport = get_models_without_import_new_resource(movedKeywordName, fromFileModel, targetFileModel)
        import_new_resource_for_models(modelsWithoutImport)

    def get_models_after_moving(self):
        return self.modelsInDir