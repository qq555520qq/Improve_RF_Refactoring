import unittest
from python_package.newRfrefactoring.builder.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywords.keywordFinder import KeywordFinder
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

    def test_find_keyword_by_lines_for_all_loops(self):
        testModel = self.builder.build(test_data+'/test_data.robot')
        self.finder.find_keywords_by_lines(testModel, 116, 119)
        keywords = self.finder.get_lines_keywords()

        self.assertEqual(len(keywords[0]['body']), 2)
        self.assertTrue(keywords[0]['body'][0].lineno >= 116)
        self.assertTrue(keywords[0]['body'][0].lineno <= 119)
        self.assertTrue(keywords[0]['body'][1].lineno >= 116)
        self.assertTrue(keywords[0]['body'][1].lineno <= 119)

    def test_find_keyword_by_lines_for_some_keywords_in_loops(self):
        testModel = self.builder.build(test_data+'/test_data.robot')
        self.finder.find_keywords_by_lines(testModel, 117, 117)
        keywords = self.finder.get_lines_keywords()

        self.assertEqual(len(keywords[0]['body']), 1)
        self.assertTrue(keywords[0]['body'][0].lineno == 117)

    def test_find_keyword_by_lines_for_all_run_keywords(self):
        testModel = self.builder.build(test_data+'/test_data.robot')
        self.finder.find_keywords_by_lines(testModel, 111, 112)
        keywords = self.finder.get_lines_keywords()

        self.assertEqual(len(keywords[0]['body']), 2)
        self.assertTrue(keywords[0]['body'][0]['keywordName'].lineno >= 111)
        self.assertTrue(keywords[0]['body'][0]['keywordName'].lineno <= 112)
        self.assertTrue(keywords[0]['body'][1]['keywordName'].lineno >= 111)
        self.assertTrue(keywords[0]['body'][1]['keywordName'].lineno <= 112)

    def test_find_keyword_by_lines_for_some_keywords_in_run_keywords(self):
        testModel = self.builder.build(test_data+'/test_data.robot')
        self.finder.find_keywords_by_lines(testModel, 7, 7)
        keywords = self.finder.get_lines_keywords()
        
        self.assertEqual(len(keywords), 1)
        self.assertTrue(keywords[0]['body'][0]['keywordName'].lineno == 7)


    def test_find_keyword_by_lines_for_not_run_keywords(self):
        testModel = self.builder.build(test_data+'/test_data.robot')
        self.finder.find_keywords_by_lines(testModel, 27, 27)
        keywords = self.finder.get_lines_keywords()

        self.assertEqual(len(keywords), 1)
        self.assertTrue(keywords[0]['node'].lineno == 27)