import unittest
from python_package.newRfrefactoring.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywordMoveHelper import KeywordMoveHelper
from python_package.newRfrefactoring.fileChecker import FileChecker
from init import test_data


class KeywordMoveHelperTest(unittest.TestCase):
    def setUp(self):
        self.builder = TestModelBuilder()
        self.teardownModels = self.builder.get_all_models_in_directory(test_data)
        modelsInDir = self.builder.get_all_models_in_directory(test_data)
        self.mover = KeywordMoveHelper(modelsInDir)
        self.checker = FileChecker()

    def test_move_keyword_defined_to_file(self):

        fromFileModel = self.builder.build(test_data + '/ezScrum.txt')
        targetFileModel = self.builder.build(test_data + '/testResource.txt')
        self.mover.move_keyword_defined_to_file('Login EzScrum', fromFileModel, targetFileModel, 'testResource.txt')

        allModels = self.mover.get_models_after_moving()
        self.checker.visit_models_to_check_keyword_and_resource(allModels, 'Login EzScrum', 'testResource.txt')
        modelsUsingKeyword = self.checker.get_models_with_resource_and_keyword()

        self.assertEqual(len(modelsUsingKeyword), 8)

        def recovery_models(models):
            for model in models:
                if isinstance(model, list):
                    recovery_models(model)
                else:
                    model.save()

        recovery_models(self.teardownModels)



