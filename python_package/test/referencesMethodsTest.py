import unittest
from robot304.parsing.model import TestData
from init import test_data,get_instance_from_testData
from python_package.rfrefactoring.reference import Reference
from python_package.rfrefactoring.referencesMethods import get_variable_match_result, get_for_loop_object_present_method, get_for_loop_object_replace_method, get_setting_object_present_method, get_setting_object_replace_method, get_step_object_present_method, get_step_object_replace_method, get_variable_replace_str, get_present_method
class ReferencesMethodsTest(unittest.TestCase):
    def setUp(self):
        self.suite = TestData(source=test_data+"/test_data.robot")
        self.setting = next((setting for setting in self.suite.setting_table),None)
        keyword = get_instance_from_testData("Duplicate Variable Keyword", self.suite.keyword_table)
        self.step = get_instance_from_testData("Log", keyword.steps)
        for_loop_keyword = get_instance_from_testData("For Loop Keyword",self.suite.keyword_table)
        self.for_loop = for_loop_keyword.steps[0]

    def test_with_get_variable_match_result(self):
        variable_name = "matchVariable"
        variable = "${%s}" %variable_name
        variables_should_be_match = [variable, '${%s[5]}' %variable_name, '@{%s}' %variable_name, '&{%s}' %variable_name,\
        '${%s["name123"]}' %variable_name, "@{%s['${variable}']}" %variable_name, '${%s}[5]' %variable_name, '${%s[59]}' %variable_name,\
        '${%s}abc34' %variable_name, "XPATH://DIV[TEXT()='%s'" %variable, '%s' %variable.upper()]
        variables_should_not_be_match = ['${match}', '#{%s}' %variable_name, '${matchVariable_5}']
        for var in variables_should_be_match:
            self.assertGreater(len(get_variable_match_result(variable, var)) ,0, "'%s' value should be matched" %var)
        for var in variables_should_not_be_match:
            self.assertEquals(len(get_variable_match_result(variable, var)), 0, "'%s' value should not be matched" %var)

    def test_get_replace_str(self):
        def test_with_case_insensitive():
            variable_name = '${test123}'
            new_var_name = 'test456'
            target_str = "${admin['${TeSt123}']}"
            self.assertEquals("${admin['${test456}']}" , get_variable_replace_str(target_str, variable_name, new_var_name))
        
        def test_with_case_equal():
            variable_name = '${test123}'
            new_var_name = 'test456'
            target_str = "${admin['${test123}']}"
            self.assertEquals("${admin['${test456}']}" , get_variable_replace_str(target_str, variable_name, new_var_name))
        test_with_case_equal()
        test_with_case_insensitive()

    def test_setting_object_present_method(self):
        self.assertIsNotNone(self.setting)
        present = get_setting_object_present_method()
        present_str = present(self.setting)
        self.assertEqual("Documentation    ${settingVariable} document", present_str)
    
    def test_setting_object_replace_method(self):
        self.assertIsNotNone(self.setting)
        variable_name = "${settingVariable}"
        new_variable_name = "varialbeSetting"
        present = get_setting_object_present_method()
        replace = get_setting_object_replace_method('variable')
        replace(self.setting, variable_name, new_variable_name)
        self.assertEqual("Documentation    ${varialbeSetting} document", present(self.setting).strip())
    
    def test_step_object_present_method(self):
        self.assertIsNotNone(self.step)
        present = get_step_object_present_method()
        self.assertEqual("Log    ${testvariable}    ${testVariable}",present(self.step))
    
    def test_step_object_replace_method(self):
        self.assertIsNotNone(self.step)
        variable_name = "${testVariable}"
        new_name = "test123"
        present = get_step_object_present_method()
        replace = get_step_object_replace_method('variable')
        replace(self.step, variable_name, new_name)
        self.assertEqual("Log    ${%s}    ${%s}" %(new_name, new_name), present(self.step))
    
    def test_for_loop_object_present_method(self):
        self.assertIsNotNone(self.for_loop)
        present = get_for_loop_object_present_method()
        self.assertEquals(": FOR    ${var}    IN    @{testVariable}\n\\    Log    ${times}\n\\    test    ${testVariable}",present(self.for_loop))
    
    def test_for_loop_object_replace_method(self):
        self.assertIsNotNone(self.for_loop)
        present = get_present_method(self.for_loop)
        replace = get_for_loop_object_replace_method('variable')
        variable_name = "${testVariable}"
        new_name = "for_loop_variable"
        replace(self.for_loop, variable_name, new_name)
        self.assertEquals(": FOR    ${var}    IN    @{for_loop_variable}\n\\    Log    ${times}\n\\    test    ${for_loop_variable}", present(self.for_loop))
    
    def test_present_and_replace_with_step_reference(self):
        reference = Reference(self.step, get_step_object_present_method(), get_step_object_replace_method('variable'))
        self.assertEquals("Log    ${testvariable}    ${testVariable}" , reference.get_present_value())
        var_name = "${testVariable}"
        new_name = "newTestVariable"
        reference.replace(var_name, new_name)
        self.assertEquals("Log    ${%s}    ${%s}" %(new_name, new_name), reference.get_present_value())