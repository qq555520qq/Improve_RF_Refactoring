from python_package.newRfrefactoring.builder.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywords.keywordMoveHelper import KeywordMoveHelper
from robot.parsing.model import Keyword, Statement
from robot.api import Token


class KeywordCreator:

    def __init__(self, allModels=[]):
        self.allModels = allModels
        self.mover = KeywordMoveHelper(self.allModels)

    def create_new_keyword_for_file(self, _path, keywordName, keywordBody):

        targetFileModel = TestModelBuilder().build(_path)

        header = Statement.from_tokens([
            Token(Token.NAME, keywordName),
            Token(Token.EOL, '\n')
        ])

        keywordNode = Keyword(header, keywordBody)

        self.mover.insert_new_keyword_defined(targetFileModel, keywordNode)

    def build_tokens_of_arguments(self, args):
        argsTokens = [
            Token(Token.SEPARATOR, '    '),
            Token(Token.ARGUMENTS, '[Arguments]')
        ]
        for arg in args:
            argsTokens.append(Token(Token.SEPARATOR, '    '))
            argsTokens.append(Token(Token.ARGUMENT, arg))
        argsTokens.append(Token(Token.EOL, '\n'))
        
        return argsTokens