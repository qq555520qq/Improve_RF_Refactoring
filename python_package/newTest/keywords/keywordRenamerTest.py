import unittest
from python_package.newRfrefactoring.builder.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywords.keywordFinder import KeywordFinder
from python_package.newRfrefactoring.keywords.keywordRenamer import KeywordRenamer
from init import new_test_data


class KeywordRenamerTest(unittest.TestCase):
    def setUp(self):
        self.builder = TestModelBuilder()
        self.finder = KeywordFinder()
        self.renamer = KeywordRenamer()

    def test_rename_keyword_for_file(self):
        testModel = self.builder.build(new_test_data+'/add sprint.robot')
        self.finder.visit_model_for_finding_keyword(testModel, 'Click SideBar')

        keywordCalls = self.finder.get_keyword_calls()
        keywordDefs = self.finder.get_keyword_defs()

        self.assertEqual(len(keywordCalls), 1)
        self.assertEqual(len(keywordDefs), 1)
        self.finder.clear_keyword_calls()
        self.finder.clear_keyword_defs()
        
        self.renamer.rename_keyword_for_nodes('Test Rename Keyword', keywordDefs, keywordCalls)
        
        self.finder.visit_model_for_finding_keyword(testModel, 'Test Rename Keyword')

        keywordCalls = self.finder.get_keyword_calls()
        keywordDefs = self.finder.get_keyword_defs()

        self.assertEqual(len(keywordCalls), 1)
        self.assertEqual(len(keywordDefs), 1)
        self.renamer.rename_keyword_for_nodes('Click SideBar', keywordDefs, keywordCalls)

    def test_rename_keyword_for_nodes(self):
        testModels = self.builder.get_all_models_in_directory(new_test_data)
        self.finder.visit_models_for_finding_keyword(testModels, 'Click SideBar')

        keywordCalls = self.finder.get_keyword_calls()
        keywordDefs = self.finder.get_keyword_defs()

        self.assertEqual(len(keywordCalls), 8)
        self.assertEqual(len(keywordDefs), 7)
        self.finder.clear_keyword_calls()
        self.finder.clear_keyword_defs()

        self.renamer.rename_keyword_for_nodes('Test Rename Keyword', keywordDefs, keywordCalls)

        self.finder.visit_models_for_finding_keyword(testModels, 'Test Rename Keyword')

        keywordCalls = self.finder.get_keyword_calls()
        keywordDefs = self.finder.get_keyword_defs()

        self.assertEqual(len(keywordCalls), 8)
        self.assertEqual(len(keywordDefs), 7)

        self.renamer.rename_keyword_for_nodes('Click SideBar', keywordDefs, keywordCalls)
        self.renamer.rename_keyword_for_nodes('Click SideBar', keywordDefs, keywordCalls)