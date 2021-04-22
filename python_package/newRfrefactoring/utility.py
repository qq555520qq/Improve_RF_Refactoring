import os
from prettytable import PrettyTable

def normalize(text):
    return text.lower().replace(' ', '').replace('_', '')

def get_file_name_from_path(_path):
    return os.path.split(_path)[1]

def get_file_extension_from_path(_path):
    return os.path.splitext(_path)[1]

def get_keywords_for_run_keywords(tokens):
    lineList = []
    keywordTokens = []
    for token in tokens:
        if not(token.lineno in lineList or token.value == 'AND'):
            lineList.append(token.lineno)
            keywordTokens.append(token)
    return keywordTokens

def recovery_models(models):
    for model in models:
        if isinstance(model, list):
            recovery_models(model)
        else:
            model.save()

def is_keyword_name_equal(node, keywordName):
    if(node.__class__.__name__ == 'KeywordCall'):
        return node.keyword == keywordName
    elif(node.__class__.__name__ == 'TestTemplate' or node.__class__.__name__ == 'SuiteTeardown' or node.__class__.__name__ == 'TestSetup' or node.__class__.__name__ == 'TestTeardown'or node.__class__.__name__ == 'Setup' or node.__class__.__name__ == 'Teardown'):
        return node.name == keywordName
    elif(node.__class__.__name__ == 'TestTemplate' or node.__class__.__name__ == 'Template'):
        return node.value == keywordName

def print_keyword(keywordNode):

    keywordStr = PrettyTable()

    fields = ['Keyword name']
    for i in range(len(keywordNode.args)):
        fields.append('Argument' + str(i+1))
    keywordStr.field_names = fields

    keywordData = [keywordNode.keyword]
    for arg in keywordNode.args:
        keywordData.append(arg)
    keywordStr.add_row(keywordData)

    print(keywordStr)

def print_Teardown(teardownNode):

    keywordStr = PrettyTable()

    fields = ['Kind',]
    for i in range(len(keywordNode.args)):
        fields.append('Argument' + str(i+1))
    keywordStr.field_names = fields

    keywordData = [keywordNode.keyword]
    for arg in keywordNode.args:
        keywordData.append(arg)
    keywordStr.add_row(keywordData)

    print(keywordStr)

def print_loop(loopNode):

    loopStr = PrettyTable()
    
    fields = []
    for i in range(len(loopNode.variables)):
        fields.append('Variable' + str(i+1))
    fields.append('Flavor')
    for i in range(len(loopNode.values)):
        fields.append('Values' + str(i+1))
    loopStr.field_names = fields
    
    loopData = []
    for variable in loopNode.variables:
        loopData.append(variable)
    loopData.append(loopNode.flavor)
    for values in loopNode.values:
        loopData.append(values)
    loopStr.add_row(loopData)

    print(loopStr)