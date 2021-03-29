import os
from python_package.newRfrefactoring.utility import normalize, get_file_name_from_path, get_file_extension_from_path
from robot.parsing import get_model, get_resource_model, get_init_model


class TestModelBuilder:

    def build(self, _path):

        fileName = get_file_name_from_path(_path)
        extension = get_file_extension_from_path(_path)
        if fileName == '__init__.robot':
            return get_init_model(_path)
        elif extension == '.robot':
            return get_model(_path)
        elif extension == '.txt':
            return get_resource_model(_path)

        return None

    def get_all_models_in_directory(self, testDirPath):
        files = os.listdir(testDirPath)
        models = []
        for file in files:
            extension = get_file_extension_from_path(file)
            if os.path.isdir(testDirPath+'/'+file):
                modelsInDir = self.get_all_models_in_directory(testDirPath+'/'+file)
                if len(modelsInDir) != 0:
                    models.append(modelsInDir)
            elif (file == '__init__.robot') or (extension == '.robot') or (extension == '.txt'):
                models.append(self.build(testDirPath+'/'+file))

        return models