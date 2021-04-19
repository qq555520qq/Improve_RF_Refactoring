from python_package.newRfrefactoring.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywordMoveHelper import KeywordMoveHelper
from robot.parsing.model import Keyword, Statement
from robot.api import Token


class KeywordCreator:

    def create_new_keyword_for_file(self, _path, keywordName, keywordBody):

        targetFileModel = TestModelBuilder().build(_path)

        header = Statement.from_tokens([
            Token(Token.NAME, keywordName),
            Token(Token.EOL, '\n')
        ])

        keywordNode = Keyword(header, keywordBody)

        KeywordMoveHelper().insert_new_keyword_defined(targetFileModel, keywordNode)

    def get_keywords_Dictionary_With_Args(self, keywords):
        keywordsWithArgs = []
        for keyword in keywords:
            if(keyword.__class__.__name__ == 'KeywordCall'):
                args = keyword.get_tokens(Token.ARGUMENT)
                keywordDict = {'loop': False, 'node': keyword, 'keywordName': keyword.name, 'arguments': args}
                keywordsWithArgs.append(keywordDict)
            elif(keyword.__class__.__name__ == 'ForLoop'):
                loopValuesList = keyword.header.values
                loopDict = {'loop': True, 'node': keyword, 'loopValues': loopValuesList}
                keywordsWithArgs.append(loopDict)

        return keywordsWithArgs
