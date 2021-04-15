import unittest
from python_package.newRfrefactoring.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywordFinder import KeywordFinder
from init import test_data


class KeywordFinderTest(unittest.TestCase):
    def setUp(self):
        self.builder = TestModelBuilder()
        self.finder = KeywordFinder()

    def test_find_keyword_by_keyword_name_from_file(self):
        testModel = self.builder.build(test_data+'/add sprint.robot')
        self.finder.visit_model_for_finding_keyword(testModel, 'Click SideBar')

        keywordCalls = self.finder.get_keyword_calls()
        keywordDefs = self.finder.get_keyword_defs()

        self.assertEqual(len(keywordCalls), 1)
        self.assertEqual(len(keywordDefs), 1)

    def test_find_keyword_by_keyword_name_from_directory(self):
        testModels = self.builder.get_all_models_in_directory(test_data)
        self.finder.visit_models_for_finding_keyword(testModels, 'Click SideBar')

        keywordCalls = self.finder.get_keyword_calls()
        keywordDefs = self.finder.get_keyword_defs()

        self.assertEqual(len(keywordCalls), 7)
        self.assertEqual(len(keywordDefs), 7)

    def test_find_keyword_by_lines_from_file(self):
        testModel = self.builder.build(test_data+'/add sprint.robot')
        self.finder.find_keywords_by_lines(testModel, 11, 13)
        keywords = self.finder.get_lines_keywords()

        self.assertEqual(len(keywords), 3)