import os
import platform

def normalize(text):
    return text.lower().replace(' ', '').replace('_', '')

def recovery_models(models):
    for model in models:
        if isinstance(model, list):
            recovery_models(model)
        else:
            model.save()

def is_KeywordCall(node):
    return node.__class__.__name__ == 'KeywordCall'

def is_ForLoop(node):
    return node.__class__.__name__ == 'ForLoop'

def is_Keyword_tag(node):
    return node.__class__.__name__ == 'SuiteSetup' or node.__class__.__name__ == 'SuiteTeardown' or node.__class__.__name__ == 'TestSetup' or node.__class__.__name__ == 'TestTeardown'or node.__class__.__name__ == 'Setup' or node.__class__.__name__ == 'Teardown'

def get_file_name_from_path(_path):
    return os.path.split(_path)[1]

def get_file_extension_from_path(_path):
    return os.path.splitext(_path)[1]

def get_keywords_for_run_keywords(tokens):
    lineList = []
    keywordTokens = []
    keywordDict = {'keywordName': None, 'arguments': []}
    for token in tokens:
        if not(token.lineno in lineList or token.value == 'AND'):
            if keywordDict['keywordName']:
                keywordTokens.append(keywordDict)
                keywordDict = {'keywordName': token, 'arguments': []}
            else:
                keywordDict['keywordName'] = token
            lineList.append(token.lineno)
        elif(token.value != 'AND'):
            keywordDict['arguments'].append(token)

    if keywordDict['keywordName']:
        keywordTokens.append(keywordDict)
    return keywordTokens

def clear_screen():
    """ 
    Clear the terminal screen. 
    """
    command = 'cls' if platform.system().lower() == 'windows' else 'clear'
    os.system(command)