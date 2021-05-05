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
    keywordToken = []
    KeywordsToken = []
    keywordsList = []

    for token in tokens:
        if token.value != 'AND':
            keywordToken.append(token)
        else:
            KeywordsToken.append(keywordToken.copy())
            keywordToken = []

    if keywordToken != []:
        KeywordsToken.append(keywordToken.copy())
        keywordToken = []

    for keywordTokenList in KeywordsToken:
        keywordDict = {'keywordName': None, 'arguments': []}
        for index, keyword in enumerate(keywordTokenList):
            if index == 0:
                keywordDict['keywordName'] = keyword
            else:
                keywordDict['arguments'].append(keyword)
        keywordsList.append(keywordDict)

    return keywordsList

    # lineList = []
    # keywordTokens = []
    # for token in tokens:
    #     if not(token.lineno in lineList or token.value == 'AND'):
    #         if keywordDict['keywordName']:
    #             keywordTokens.append(keywordDict)
    #             keywordDict = {'keywordName': token, 'arguments': []}
    #         else:
    #             keywordDict['keywordName'] = token
    #         lineList.append(token.lineno)
    #     elif(token.value != 'AND'):
    #         keywordDict['arguments'].append(token)

    # if keywordDict['keywordName']:
    #     keywordTokens.append(keywordDict)
    # return keywordTokens

def clear_screen():
    """ 
    Clear the terminal screen. 
    """
    command = 'cls' if platform.system().lower() == 'windows' else 'clear'
    os.system(command)

def get_number_from_user(text):
    number = ''
    while not(number.isdigit()):
        number = input(text)
    return number

def get_folder_path_from_user(text):
    projectPath = ''
    while not(os.path.isdir(projectPath)):
        clear_screen()
        projectPath = input(text)
    return projectPath

def get_file_path_from_user(text):
    filePath = ''
    while not(os.path.isfile(filePath)):
        filePath = input(text)
    return filePath

def save_model_and_update_old_models(model, oldModels):

    def update_model(model, allModels):
        for index, oldModel in enumerate(allModels):
            if isinstance(oldModel, list):
                update_model(model, oldModel)
            elif(model.source == oldModel.source):
                allModels[index] = model

    model.save()
    update_model(model, oldModels)