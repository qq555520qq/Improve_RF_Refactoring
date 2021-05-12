import unittest
import re
from os import path
from robot304.api import TestData
from init import test_data, get_instance_from_testData
from python_package.rfrefactoring.referencesFinder import *
from robot304.parsing.model import ResourceFile

class KeywordReferenceFinderTest(unittest.TestCase):
    def setUp(self):
        source_path = test_data+'/add sprint.robot'
        self.suite = TestData(source=source_path)
        self.finder = KeywordReferenceFinder()

    def test_find_kw_usage_from_keyword(self):        
        source_keyword = get_instance_from_testData('Test Keyword',self.suite.keyword_table)
        self.assertIsNotNone(source_keyword)
        usages = self.finder.find_references_from_keyword('Log',source_keyword)
        self.assertEqual(len(usages),3)
    
    def test_find_kw_usage_from_setting(self):
        setting_table = self.suite.setting_table
        usages = self.finder.find_references_from_settings('Login EzScrum',setting_table)
        self.assertEqual(1,len(usages))

    def test_find_kw_usage_from_testcase(self):
        testcase = get_instance_from_testData('test temp', self.suite.testcase_table)
        self.assertIsNotNone(testcase)
        usages = self.finder.find_references_from_testcase('123', testcase)
        self.assertEqual(1, len(usages))

    def test_find_kw_usage_from_testdataFile(self):
        usages = self.finder.find_references_from_testdataFile('Input Field',self.suite)
        self.assertEqual(6, len(usages['references']))
        self.assertEqual(self.suite.name, usages['testdata'].name)
    
    def test_find_kw_usage_from_resource(self):
        source_path = test_data+'/ezScrum.txt'
        ezScrum_resource = ResourceFile(source=source_path).populate()
        usages = self.finder.find_references_from_testdataFile('Find Usage Test Keyword1',ezScrum_resource)
        self.assertEqual(ezScrum_resource, usages['testdata'])
        self.assertEqual(3, len(usages['references']))

class VariableReferenceFinderTest(unittest.TestCase):
    def setUp(self):
        self.variable_finder = VariableReferenceFinder()
        self.suite = TestData(source=test_data+"/test_data.robot")
        
    def test_find_glob_var_usage_from_keyword(self):
        def get_variable_usage_from_keyword(variableName, keywordName):
            keyword = get_instance_from_testData(keywordName, self.suite.keyword_table)
            self.assertIsNotNone(keyword)
            return self.variable_finder.find_global_variable_references_from_keyword(variableName, keyword)
            
        def test_with_normal_case():
            keyword_name = 'Test Keyword'
            variable_name = '${testVariable}'
            usages = get_variable_usage_from_keyword(variable_name, keyword_name)
            self.assertEqual(2, len(usages))
        
        def test_with_duplicate_name_in_keyword_args():
            keyword_name = 'Click SideBar'
            variable_name = '${title}'
            usages = get_variable_usage_from_keyword(variable_name, keyword_name)
            self.assertEqual(0, len(usages))
        
        def test_with_duplicate_name_in_step():
            keyword_name = 'Duplicate Variable Keyword'
            variable_name = '${testVariable}'
            usages = get_variable_usage_from_keyword(variable_name, keyword_name)
            self.assertEqual(1, len(usages))

        def test_with_default_argument():
            keyword_name = "Default argument Keyword"
            variable_name = '${testVariable}'
            usages = get_variable_usage_from_keyword(variable_name, keyword_name)
            self.assertEquals(2, len(usages))
        test_with_default_argument()
        test_with_normal_case()
        test_with_duplicate_name_in_step()
        test_with_duplicate_name_in_keyword_args()
    
    def test_find_glob_var_usage_in_testcase(self):
        def get_variable_usage_from_testcase(variableName, testcaseName):
            testcase = get_instance_from_testData(testcaseName, self.suite.testcase_table)
            self.assertIsNotNone(testcase)
            return self.variable_finder.find_global_variable_references_from_testcase_obj(variableName, testcase)
            
        def test_with_normal_case():
            variable_name = '${testVariable}'
            test_case_name = 'test temp'
            usages = get_variable_usage_from_testcase(variable_name, test_case_name)
            self.assertEqual(7, len(usages))
        
        def test_with_duplicate_name_assign_in_step():
            variable_name = '${testVariable}'
            test_case_name = 'test variable assign in step'
            usages = get_variable_usage_from_testcase(variable_name, test_case_name)
            self.assertEqual(4, len(usages))

        test_with_normal_case()
        test_with_duplicate_name_assign_in_step()
    
    def test_find_glob_var_usage_from_setting_table(self):
        def get_usage_from_setting_table(variable, table):
            return self.variable_finder.find_global_variable_references_from_setting(variable, table)

        def test_with_resource_file():
            resource_file = ResourceFile(source=test_data+'/testResource.txt').populate()
            variable_name = '${resourceFileVariable}'
            usages = get_usage_from_setting_table(variable_name, resource_file.setting_table)
            self.assertEqual(2, len(usages))

        def test_with_testcase_file():
            variable_name = '${settingVariable}'
            usages = get_usage_from_setting_table(variable_name, self.suite.setting_table)
            self.assertEqual(5, len(usages))
        test_with_testcase_file()
        test_with_resource_file()
    
    def test_find_glob_var_usage_from_testdata_file(self):
        def test_with_testcase():
            variable_name = '${testVariable}'
            variable = get_instance_from_testData(variable_name, self.suite.variable_table)
            self.assertIsNotNone(variable)
            usages = self.variable_finder.find_global_variable_references_from_testdata_file(variable, self.suite)
            self.assertEqual(23, len(usages['references']))
            self.assertEqual(self.suite, usages['testdata'])
        def test_with_resource_file():
            resource_file = ResourceFile(source=test_data+'/testResource.txt').populate()
            variable_name = '${resourceFileVariable}'
            variable = get_instance_from_testData(variable_name, resource_file.variable_table)
            self.assertIsNotNone(variable)
            usages = self.variable_finder.find_global_variable_references_from_testdata_file(variable, resource_file)
            self.assertEqual(4, len(usages['references']))
            self.assertEqual(resource_file, usages['testdata'])
        
        test_with_testcase()
        test_with_resource_file()
    
    def test_find_local_var_usage_from_testcase_obj(self):
        def test_with_keyword():
            keyword = get_instance_from_testData('Choose Project', self.suite.keyword_table)
            variable_name = '${project_name}'
            self.assertIsNotNone(keyword)
            usages = self.variable_finder.find_local_variable_references_from_test_case_obj(variable_name, keyword)
            self.assertEqual(4, len(usages))

        def test_with_testcase():
            testcase = get_instance_from_testData('test temp', self.suite.testcase_table)
            variable_name = '${testVariable}'
            self.assertIsNotNone(testcase)
            usages = self.variable_finder.find_local_variable_references_from_test_case_obj(variable_name, testcase)
            self.assertEqual(7, len(usages))
        test_with_keyword()
        # test_with_testcase()
