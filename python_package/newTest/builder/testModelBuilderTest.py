import unittest
from python_package.newRfrefactoring.builder.testModelBuilder import TestModelBuilder
from init import new_test_data


class TestModelBuilderTest(unittest.TestCase):
    def setUp(self):
        self.builder = TestModelBuilder()

    def test_build(self):
        testModel = self.builder.build(new_test_data+'/add sprint.robot')
        self.assertIsNotNone(testModel)

    def test_get_all_models(self):
        models = self.builder.get_all_models_in_directory(new_test_data)
        self.assertIsNotNone(models)
