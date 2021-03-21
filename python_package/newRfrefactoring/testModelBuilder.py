import os
from robot.parsing import get_model, get_resource_model, get_init_model


class TestModelBuilder:

    def build(self, _path):

        fileName = os.path.split(_path)[1]
        extension = os.path.splitext(_path)[1]
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
            extension = os.path.splitext(file)[1]
            if os.path.isdir(testDirPath+'/'+file):
                modelsInDir = self.get_all_models_in_directory(testDirPath+'/'+file)
                if len(modelsInDir) != 0:
                    models.append(modelsInDir)
            elif (file == '__init__.robot') or (extension == '.robot') or (extension == '.txt'):
                models.append(self.build(testDirPath+'/'+file))

        return models