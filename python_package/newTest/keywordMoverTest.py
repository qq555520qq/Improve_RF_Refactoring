import unittest
from python_package.newRfrefactoring.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywordMover import KeywordMover
from init import test_data


class KeywordMoverTest(unittest.TestCase):
    def setUp(self):
        self.builder = TestModelBuilder()
        modelsInDir = self.builder.get_all_models_in_directory(test_data)
        self.mover = KeywordMover(modelsInDir)

    def test_move_keyword_defined_to_file(self):

        fromFileModel = self.builder.build(test_data + '/ezScrum.txt')
        targetFileModel = self.builder.build(test_data + '/testResource.txt')
        self.mover.move_keyword_defined_to_file('Login EzScrum', fromFileModel, targetFileModel)