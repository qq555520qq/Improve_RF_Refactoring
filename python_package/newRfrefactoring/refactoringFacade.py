from python_package.newRfrefactoring.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywordMoveHelper import KeywordMoveHelper
from robot.parsing.model import Keyword, Statement
from robot.api import Token

class RefactoringFacade:

    def __init__(self):
        self.builder = TestModelBuilder()


    def create_new_keyword_for_file(self, _path, keywordName, keywordBody):

        targetFileModel = self.builder.build(_path)
        mover = KeywordMoveHelper()

        header = Statement.from_tokens([
            Token(Token.NAME, keywordName),
            Token(Token.EOL, '\n')
        ])
        keywordNode = Keyword(header, keywordBody)

        mover.insert_new_keyword_defined(targetFileModel, keywordNode)