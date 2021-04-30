from robot.api import Token
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
                                        print(lineKeyword['node'].data_tokens)
                                        break
                    elif lineKeyword['node'] == updatedArgData['lineKeyword']['node']:
                        keywordArgsTokens = lineKeyword['node'].get_tokens(Token.ARGUMENT)
                        for arg in keywordArgsTokens:
                            if str(arg.value) == str(updatedArgData['updateArg']):
                                arg.value = updatedArgData['newArg']
                                isUpdated = True
                                break
            