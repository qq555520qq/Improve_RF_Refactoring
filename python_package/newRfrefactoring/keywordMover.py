import ast
from python_package.newRfrefactoring.utility import normalize, get_file_name_from_path
from python_package.newRfrefactoring.fileChecker import FileChecker
from python_package.newRfrefactoring.keywordFinder import KeywordFinder


class KeywordMover(ast.NodeTransformer):

    def __init__(self, modelsInDir):
        self.checker = FileChecker()
        self.modelsInDir = modelsInDir
        self.finder = KeywordFinder()

    def visit_KeywordName(self, node):
        """
            Visit all keyword's define to do something.
        """
        if(self.node == node):
            token = node.get_token(Token.KEYWORD_NAME)
            token.value = self.new_name

    def move_keyword_to_file(self, movedKeyword, fromFileModel, targetFileModel):

        self.finder.visit_model_for_finding_keyword(fromFileModel, movedKeyword)
        self.finder.get_keyword_defs()

        fromFileName = get_file_name_from_path(fromFileModel.source)



        self.checker.visit_models_to_check_keyword_and_resource(self.modelsInDir, movedKeyword, fromFileName)
        modelsUsingKeyword = self.checker.get_models_with_resource_and_keyword()


        

