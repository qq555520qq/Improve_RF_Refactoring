import unittest
from python_package.newRfrefactoring.builder.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywords.keywordFinder import KeywordFinder
from init import new_test_data


class KeywordFinderTest(unittest.TestCase):
    def setUp(self):
        self.builder = TestModelBuilder()
        self.finder = KeywordFinder()

    def test_find_keyword_by_keyword_name_from_file(self):
        testModel = self.builder.build(new_test_data+'/add sprint.robot')
        self.finder.visit_model_for_finding_keyword(testModel, 'Click SideBar')

        keywordCalls = self.finder.get_keyword_calls()
        keywordDefs = self.finder.get_keyword_defs()

        self.assertEqual(len(keywordCalls), 1)
        self.assertEqual(len(keywordDefs), 1)

    def test_find_keyword_by_keyword_name_from_directory(self):
        testModels = self.builder.get_all_models_in_directory(new_test_data)
        self.finder.visit_models_for_finding_keyword(testModels, 'Click SideBar')

        keywordCalls = self.finder.get_keyword_calls()
        keywordDefs = self.finder.get_keyword_defs()

        self.assertEqual(len(keywordCalls), 8)
        self.assertEqual(len(keywordDefs), 7)

    def test_find_keyword_by_lines_for_all_loops(self):
        testModel = self.builder.build(new_test_data+'/test_data.robot')
        self.finder.find_keywords_by_lines(testModel, 127, 130)
        keywords = self.finder.get_lines_keywords()
        self.assertEqual(len(keywords[0]['body']), 2)
        self.assertTrue(keywords[0]['body'][0].lineno >= 127)
        self.assertTrue(keywords[0]['body'][0].lineno <= 130)
        self.assertTrue(keywords[0]['body'][1].lineno >= 127)
        self.assertTrue(keywords[0]['body'][1].lineno <= 130)

    def test_find_keyword_by_lines_for_some_keywords_in_loops(self):
        testModel = self.builder.build(new_test_data+'/test_data.robot')
        self.finder.find_keywords_by_lines(testModel, 129, 129)
        keywords = self.finder.get_lines_keywords()

        self.assertEqual(len(keywords[0]['body']), 1)
        self.assertTrue(keywords[0]['body'][0].lineno == 129)

    def test_find_keyword_by_lines_for_all_run_keywords(self):
        testModel = self.builder.build(new_test_data+'/test_data.robot')
        self.finder.find_keywords_by_lines(testModel, 116, 117)
        keywords = self.finder.get_lines_keywords()

        self.assertEqual(len(keywords[0]['body']), 2)
        self.assertTrue(keywords[0]['body'][0]['keywordName'].lineno >= 116)
        self.assertTrue(keywords[0]['body'][0]['keywordName'].lineno <= 117)
        self.assertTrue(keywords[0]['body'][1]['keywordName'].lineno >= 116)
        self.assertTrue(keywords[0]['body'][1]['keywordName'].lineno <= 117)

    def test_find_keyword_by_lines_for_some_keywords_in_run_keywords(self):
        testModel = self.builder.build(new_test_data+'/test_data.robot')
        self.finder.find_keywords_by_lines(testModel, 7, 7)
        keywords = self.finder.get_lines_keywords()
        
        self.assertEqual(len(keywords), 1)
        self.assertTrue(keywords[0]['body'][0]['keywordName'].lineno == 7)


    def test_find_keyword_by_lines_for_not_run_keywords(self):
        testModel = self.builder.build(new_test_data+'/test_data.robot')
        self.finder.find_keywords_by_lines(testModel, 28, 28)
        keywords = self.finder.get_lines_keywords()

        self.assertEqual(len(keywords), 1)
        self.assertTrue(keywords[0]['node'].lineno == 28)