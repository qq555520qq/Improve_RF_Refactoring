import unittest
from init import test_data
from python_package.rfrefactoring.refactoringFacade import RefactoringFacade
from python_package.rfrefactoring.testDataVisitor import FindVisitor
from python_package.rfrefactoring.reference import Reference
from python_package.rfrefactoring.referencesMethods import get_present_method, get_replace_method
class RefactoringFacadeTest(unittest.TestCase):
    def setUp(self):
        self.facade = RefactoringFacade()
        self.root = self.facade.build(test_data)

    def test_rename_keyword_def(self):
        source = test_data+'/ezScrum.txt'
        login_ezScrum = self.facade.get_keyword_obj_from_file(self.root, 'Login EzScrum', source)
        new_kw_name = 'Login EzScrum V4'
        self.assertIsNotNone(login_ezScrum)
        self.facade.rename_keyword_def(login_ezScrum, new_kw_name)
        login_ezScrum_v4 = self.facade.get_keyword_obj_from_file(self.root, new_kw_name, source)
        self.assertIsNotNone(login_ezScrum_v4)
    
    def test_rename_variable_def(self):
        source = test_data+'/testResource.txt'
        variable = self.facade.get_variable_obj_from_file(self.root, '${resourceFileVariable}', source)
        new_var_name = 'resourceVariable'
        self.assertIsNotNone(variable)
        self.facade.rename_variable_def(variable, new_var_name)
        new_variable = self.facade.get_variable_obj_from_file(self.root, "${%s}" %new_var_name, source)
        self.assertIsNotNone(new_variable)

    def test_rename_keyword_references(self):
        source = test_data+'/ezScrum.txt'
        login_ezScrum = self.facade.get_keyword_obj_from_file(self.root, 'Login EzScrum', source)
        self.assertIsNotNone(login_ezScrum)
        references = self.facade.get_keyword_references(self.root, login_ezScrum)
        self.assertEqual(4, len(references))
        new_kw_name = 'Login EzScrum v3'
        total_references = []
        for reference in references:
            total_references.extend(reference['references'])
        self.assertEqual(6, len(total_references))
        self.facade.rename_keyword_references(total_references, login_ezScrum.name, new_kw_name)
        self.facade.rename_keyword_def(login_ezScrum, new_kw_name)
        login_ezScrum_v3 = self.facade.get_keyword_obj_from_file(self.root, new_kw_name, source)
        new_kw_references = self.facade.get_keyword_references(self.root, login_ezScrum_v3)
        self.assertEqual(4, len(new_kw_references))
        total_references_after_rename = []
        for reference in references:
            total_references_after_rename.extend(reference['references'])
        self.assertEqual(6 , len(total_references_after_rename))

    def test_rename_variable_references(self):
        source = test_data+'/testResource.txt'
        variable_name = '${resourceFileVariable}'
        new_var_name = 'newResourceVariable'
        resourceVariable = self.facade.get_variable_obj_from_file(self.root, variable_name, source)
        self.assertIsNotNone(resourceVariable)
        references = self.facade.get_variable_references(self.root, resourceVariable)
        self.assertEqual(1, len(references))
        total_references = []
        for reference in references:
            total_references.extend(reference['references'])
        self.assertEqual(4, len(total_references))
        self.facade.rename_variable_references(total_references, resourceVariable.name, new_var_name)
        self.facade.rename_variable_def(resourceVariable, new_var_name)
        newResourceVariable = self.facade.get_variable_obj_from_file(self.root, '${%s}' %new_var_name, source)
        new_kw_references = self.facade.get_variable_references(self.root, newResourceVariable)
        self.assertEqual(len(references), len(new_kw_references))
        total_references_after_rename = []
        for reference in references:
            total_references_after_rename.extend(reference['references'])
        self.assertEqual(len(total_references) , len(total_references_after_rename))