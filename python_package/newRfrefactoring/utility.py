import os

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