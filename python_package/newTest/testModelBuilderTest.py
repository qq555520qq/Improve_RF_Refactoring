import unittest
from python_package.newRfrefactoring.testModelBuilder import TestModelBuilder
from init import test_data


class TestModelBuilderTest(unittest.TestCase):
    def setUp(self):
        self.builder = TestModelBuilder()

    def test_build(self):
        testModel = self.builder.build(test_data+'/add sprint.robot')
        self.assertIsNotNone(testModel)

    def test_get_all_models(self):
        models = self.builder.get_all_models_in_directory(test_data)
        self.assertIsNotNone(models)
