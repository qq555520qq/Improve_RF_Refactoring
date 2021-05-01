from robot.api import Token
from robot.parsing.model import Statement
from python_package.newRfrefactoring.common.utility import is_ForLoop, is_Keyword_tag, is_KeywordCall

class LineKeywordsHelper():

    def get_line_keyword_from_line_keywords(self, lineKeywords, line):
        for lineKeyword in lineKeywords:
            if is_KeywordCall(lineKeyword['node']):
                if lineKeyword['node'].lineno == line:
                    return {'belong': lineKeyword, 'node': lineKeyword['node']}
            elif is_ForLoop(lineKeyword['node']):
                for loopBodyMember in lineKeyword['body']:
                    if loopBodyMember.lineno == line:
                        return {'belong': lineKeyword, 'node': loopBodyMember}
            elif is_Keyword_tag(lineKeyword['node']):
                if len(lineKeyword['body']) != 0:
                    for keyword in lineKeyword['body']:
                        if keyword['keywordName'].lineno == line:
                            return {'belong': lineKeyword, 'node': keyword}
                elif lineKeyword['node'].lineno == line:
                    return {'belong': lineKeyword, 'node': lineKeyword['node']}
        return None

    def get_arguments_for_line_keyword(self, keywordWithLine):
        if is_KeywordCall(keywordWithLine['belong']['node']):
            return keywordWithLine['node'].args
        elif is_ForLoop(keywordWithLine['belong']['node']):
            return keywordWithLine['node'].args
        elif is_Keyword_tag(keywordWithLine['belong']['node']):
            if len(keywordWithLine['belong']['body']) != 0:
                return keywordWithLine['node']['arguments']
            else:
                return keywordWithLine['node'].args

    def update_arguments_of_line_keyword(self, lineKeywordsList, updatedArgData):
        isUpdated = False

        for lineKeyword in lineKeywordsList:
            if isUpdated:
                break
            if lineKeyword == updatedArgData['lineKeyword']['belong']:
                if(is_KeywordCall(lineKeyword['node']) and lineKeyword['node'] == updatedArgData['lineKeyword']['node']):
                    keywordArgsTokens = lineKeyword['node'].get_tokens(Token.ARGUMENT)
                    for arg in keywordArgsTokens:
                        if str(arg.value) == str(updatedArgData['updateArg']):
                            arg.value = updatedArgData['newArg']
                            isUpdated = True
                            break
                elif is_ForLoop(lineKeyword['node']):
                    for member in lineKeyword['body']:
                        if member == updatedArgData['lineKeyword']['node']:
                            keywordArgsTokens = member.get_tokens(Token.ARGUMENT)
                            for arg in keywordArgsTokens:
                                if str(arg.value) == str(updatedArgData['updateArg']):
                                    arg.value = updatedArgData['newArg']
                                    isUpdated = True
                                    break
                elif is_Keyword_tag(lineKeyword['node']):
                    if len(lineKeyword['body']) != 0:
                        for keyword in lineKeyword['body']:
                            if keyword == updatedArgData['lineKeyword']['node']:
                                for arg in keyword['arguments']:
                                    if str(arg.value) == str(updatedArgData['updateArg']):
                                        arg.value = updatedArgData['newArg']
                                        isUpdated = True
                                        break
                    elif lineKeyword['node'] == updatedArgData['lineKeyword']['node']:
                        keywordArgsTokens = lineKeyword['node'].get_tokens(Token.ARGUMENT)
                        for arg in keywordArgsTokens:
                            if str(arg.value) == str(updatedArgData['updateArg']):
                                arg.value = updatedArgData['newArg']
                                isUpdated = True
                                break

    def get_new_keyword_body_from_line_keywords_and_arguments_tokens(self, lineKeywords, argsTokens):
        keywordsBody = []
        if len(argsTokens) != 0:
            arguments = Statement.from_tokens(argsTokens)
            keywordsBody.append(arguments)
        for lineKeyword in lineKeywords:
            keywordsBody.append(lineKeyword['node'])
        return keywordsBody