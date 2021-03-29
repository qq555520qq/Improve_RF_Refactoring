import unittest
from python_package.newRfrefactoring.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywordFinder import KeywordFinder
from python_package.newRfrefactoring.keywordRenamer import KeywordRenamer
from init import test_data


class KeywordRenamerTest(unittest.TestCase):
    def setUp(self):
        self.builder = TestModelBuilder()
        self.finder = KeywordFinder()
        self.renamer = KeywordRenamer()

    def test_rename_keyword_for_file(self):
        testModel = self.builder.build(test_data+'/add sprint.robot')
        self.finder.visit_model_for_finding_keyword(testModel, 'Click SideBar')

        keywordCalls = self.finder.get_keyword_calls()
        keywordDefs = self.finder.get_keyword_defs()

        self.assertEqual(len(keywordCalls), 1)
        self.assertEqual(len(keywordDefs), 1)
        self.finder.clear_keyword_calls()
        self.finder.clear_keyword_defs()

        self.renamer.rename_keyword_for_nodes(keywordCalls, 'Test Rename Keyword')
        self.renamer.rename_keyword_for_nodes(keywordDefs, 'Test Rename Keyword')
        
        self.finder.visit_model_for_finding_keyword(testModel, 'Test Rename Keyword')

        keywordCalls = self.finder.get_keyword_calls()
        keywordDefs = self.finder.get_keyword_defs()

        self.assertEqual(len(keywordCalls), 1)
        self.assertEqual(len(keywordDefs), 1)

        self.renamer.rename_keyword_for_nodes(keywordCalls, 'Click SideBar')
        self.renamer.rename_keyword_for_nodes(keywordDefs, 'Click SideBar')

    def test_rename_keyword_for_nodes(self):
        testModels = self.builder.get_all_models_in_directory(test_data)
        self.finder.visit_models_for_finding_keyword(testModels, 'Click SideBar')

        keywordCalls = self.finder.get_keyword_calls()
        keywordDefs = self.finder.get_keyword_defs()

        self.assertEqual(len(keywordCalls), 7)
        self.assertEqual(len(keywordDefs), 7)
        self.finder.clear_keyword_calls()
        self.finder.clear_keyword_defs()

        self.renamer.rename_keyword_for_nodes(keywordCalls, 'Test Rename Keyword')
        self.renamer.rename_keyword_for_nodes(keywordDefs, 'Test Rename Keyword')

        self.finder.visit_models_for_finding_keyword(testModels, 'Test Rename Keyword')

        keywordCalls = self.finder.get_keyword_calls()
        keywordDefs = self.finder.get_keyword_defs()

        self.assertEqual(len(keywordCalls), 7)
        self.assertEqual(len(keywordDefs), 7)

        self.renamer.rename_keyword_for_nodes(keywordCalls, 'Click SideBar')
        self.renamer.rename_keyword_for_nodes(keywordDefs, 'Click SideBar')