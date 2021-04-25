import os
from prettytable import PrettyTable

def normalize(text):
    return text.lower().replace(' ', '').replace('_', '')

def recovery_models(models):
    for model in models:
        if isinstance(model, list):
            recovery_models(model)
        else:
            model.save()

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

def print_keywordCall_for_linesKeywords(keywordNode):

    keywordStr = PrettyTable()

    fields = ['Line', 'Keyword name']
    keywordData = [keywordNode.lineno, keywordNode.keyword]
    for i, arg in enumerate(keywordNode.args):
        fields.append('Argument' + str(i+1))
        keywordData.append(arg)
    keywordStr.field_names = fields
    keywordStr.add_row(keywordData)

    print(keywordStr)

def print_loop_for_linesKeywords(loopDict):

    loopStr = PrettyTable()
    
    fields = []
    loopData = []
    for i, variable in enumerate(loopDict['node'].variables):
        fields.append('Variable' + str(i+1))
        loopData.append(variable)
    fields.append('Flavor')
    loopData.append(loopDict['node'].flavor)
    for i, value in enumerate(loopDict['node'].values):
        fields.append('Values' + str(i+1))
        loopData.append(value)

    loopStr.field_names = fields
    loopStr.add_row(loopData)

    print(loopStr)
    for keyword in loopDict['body']:
        print_keywordCall_for_linesKeywords(keyword)


def print_run_keywords_for_linesKeywords(runKeywordsDict):

    keywordStr = PrettyTable()

    fields = ['Line', 'Kind', 'Keyword name']
    keywordData = []
    keywordData.append(runKeywordsDict['node'].lineno)
    keywordData.append(runKeywordsDict['node'].__class__.__name__)
    keywordData.append(runKeywordsDict['node'].name)
    if len(runKeywordsDict['body']) == 0:
        for i, arg in enumerate(runKeywordsDict['node'].args):
            fields.append('Argument' + str(i+1))
            keywordData.append(arg)
        keywordStr.field_names = fields
        keywordStr.add_row(keywordData)
        print(keywordStr)
    else:
        keywordStr.field_names = fields
        keywordStr.add_row(keywordData)
        print(keywordStr)
        for keyword in runKeywordsDict['body']:
            keywordStr.clear()
            fields = ['Line', 'Keyword name']
            keywordData = [keyword['keywordName'].lineno, keyword['keywordName'].value]
            for i, arg in enumerate(keyword['arguments']):
                fields.append('Argument' + str(i+1))
                keywordData.append(arg.value)
            keywordStr.field_names = fields
            keywordStr.add_row(keywordData)
            print(keywordStr)