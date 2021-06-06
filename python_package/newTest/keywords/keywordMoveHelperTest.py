import unittest
from python_package.newRfrefactoring.builder.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywords.keywordMoveHelper import KeywordMoveHelper
from python_package.newRfrefactoring.checker.fileChecker import FileChecker
from python_package.newRfrefactoring.common.utility import recovery_models
from init import new_test_data
from robot.parsing.model import Keyword, Statement
from robot.api import Token


class KeywordMoveHelperTest(unittest.TestCase):

    def setUp(self):
        self.builder = TestModelBuilder()
        self.teardownModels = self.builder.get_all_models_in_directory(new_test_data)
        modelsInDir = self.builder.get_all_models_in_directory(new_test_data)
        self.mover = KeywordMoveHelper(modelsInDir)
        self.checker = FileChecker()

    def test_move_keyword_defined_to_file(self):

        fromFileModel = self.builder.build(new_test_data + '/ezScrum.txt')
        targetFileModel = self.builder.build(new_test_data + '/testResource.txt')
        self.mover.move_keyword_defined_to_file('Login EzScrum', fromFileModel, targetFileModel, 5, 'testResource.txt')

        allModels = self.mover.get_models_after_moving()
        self.checker.visit_models_to_check_keyword_and_resource(allModels, 'Login EzScrum', 'testResource.txt')
        modelsUsingKeyword = self.checker.get_models_with_resource_and_keyword()

        self.assertEqual(len(modelsUsingKeyword), 9)

        recovery_models(self.teardownModels)

