import os

def normalize(text):
    return text.lower().replace(' ', '').replace('_', '')

def get_file_name_from_path(_path):
    return os.path.split(_path)[1]

def get_file_extension_from_path(_path):
    return os.path.splitext(_path)[1]