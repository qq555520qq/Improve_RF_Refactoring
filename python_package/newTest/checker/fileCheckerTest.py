import unittest
from python_package.newRfrefactoring.builder.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.checker.fileChecker import FileChecker
from python_package.newRfrefactoring.keywords.keywordFinder import KeywordFinder
from init import new_test_data


class FileCheckerTest(unittest.TestCase):
    def setUp(self):
        self.builder = TestModelBuilder()
        self.checker = FileChecker()
        self.finder = KeywordFinder()

    def test_visit_model_to_check_keyword_and_resource_from_file(self):
        testModel = self.builder.build(new_test_data+'/add story by excel.robot')

        self.checker.visit_model_to_check_keyword_and_resource(testModel, 'Login EzScrum', 'ezScrum.txt')
        models = self.checker.get_models_with_resource_and_keyword()

        self.assertEqual(len(models), 1)

    def test_visit_models_to_check_keyword_and_resource_from_directory(self):
        testModels = self.builder.get_all_models_in_directory(new_test_data)

        self.checker.visit_models_to_check_keyword_and_resource(testModels, 'Login EzScrum', 'ezScrum.txt')
        models = self.checker.get_models_with_resource_and_keyword()
        
        self.assertEqual(len(models), 9)
    
    def test_find_model_with_same_keywords(self):
        testFromModel = self.builder.build(new_test_data+'/add sprint.robot')
        self.finder.find_keywords_by_lines(testFromModel, 10, 11)
        keywords = self.finder.get_lines_keywords()
        
        testModel = self.builder.build(new_test_data+'/add story by excel.robot')
        self.checker.find_model_with_same_keywords(testModel, keywords)
        sameKeywords = self.checker.get_models_with_same_keywords()

        self.assertEqual(len(sameKeywords), 1)
    
    def test_find_models_with_same_keywords(self):
        testFromModel = self.builder.build(new_test_data+'/add sprint.robot')
        self.finder.find_keywords_by_lines(testFromModel, 10, 11)
        keywords = self.finder.get_lines_keywords()
        
        testModels = self.builder.get_all_models_in_directory(new_test_data)
        self.checker.find_models_with_same_keywords(testModels, keywords)
        sameKeywords = self.checker.get_models_with_same_keywords()
        
        self.assertEqual(len(sameKeywords), 8)