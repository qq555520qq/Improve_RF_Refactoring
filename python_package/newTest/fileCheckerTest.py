import unittest
from python_package.newRfrefactoring.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.fileChecker import FileChecker
from init import test_data


class FileCheckerTest(unittest.TestCase):
    def setUp(self):
        self.builder = TestModelBuilder()
        self.checker = FileChecker()

    def test_visit_model_to_check_keyword_and_resource_from_file(self):
        testModel = self.builder.build(test_data+'/add story by excel.robot')

        self.checker.visit_model_to_check_keyword_and_resource(testModel, 'Login EzScrum', 'ezScrum.txt')
        models = self.checker.get_models_with_resource_and_keyword()

        self.assertEqual(len(models), 1)

    def test_visit_models_to_check_keyword_and_resource_from_directory(self):
        testModels = self.builder.get_all_models_in_directory(test_data)

        self.checker.visit_models_to_check_keyword_and_resource(testModels, 'Login EzScrum', 'ezScrum.txt')
        models = self.checker.get_models_with_resource_and_keyword()
        
        self.assertEqual(len(models), 8)