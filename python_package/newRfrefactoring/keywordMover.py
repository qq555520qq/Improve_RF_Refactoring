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

        def get_models_without_import(allModels, modelsWithImport):
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

        self.finder.visit_model_for_finding_keyword(fromFileModel, movedKeywordName)
        self.movedKeywordNode = self.finder.get_keyword_defs()[0]['keywordNode']

        self.removeOldKeywordDefined = True
        self.visit(fromFileModel)
        fromFileModel.save()
        update_model(fromFileModel, self.modelsInDir)
        self.removeOldKeywordDefined = False

        self.insertKeywordDefined = True
        self.visit(targetFileModel)
        targetFileModel.save()
        update_model(targetFileModel, self.modelsInDir)
        self.insertKeywordDefined = False

        fromFileName = get_file_name_from_path(fromFileModel.source)
        self.checker.visit_models_to_check_keyword_and_resource(self.modelsInDir, movedKeywordName, fromFileName)
        modelsUsingKeyword = self.checker.get_models_with_resource_and_keyword()
        self.checker.clear_models_with_resource_and_keyword()

        targetFileName = get_file_name_from_path(targetFileModel.source)
        self.checker.visit_models_to_check_keyword_and_resource(modelsUsingKeyword, movedKeywordName, targetFileName)
        modelsWithImport = self.checker.get_models_with_resource_and_keyword()
        modelsWithoutImport = get_models_without_import(modelsUsingKeyword, modelsWithImport)

        self.importResource = True
        for model in modelsWithoutImport:
            self.visit(model)
            model.save()
        self.importResource = False