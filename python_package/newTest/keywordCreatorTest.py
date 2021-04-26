import unittest
from python_package.newRfrefactoring.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywordFinder import KeywordFinder
from python_package.newRfrefactoring.keywordCreator import KeywordCreator
from python_package.newRfrefactoring.utility import recovery_models
from robot.api import Token
from init import test_data


class KeywordCreatorTest(unittest.TestCase):

    def setUp(self):
        self.builder = TestModelBuilder()
        self.creator = KeywordCreator()
        self.finder = KeywordFinder()

    def test_create_new_keyword_for_file(self):
        tearDownModel = self.builder.build(test_data+'/ezScrum.txt')

        keywordBody = [
            Token(Token.SEPARATOR, '    '),
            Token(Token.ARGUMENTS, '[Arguments]'),
            Token(Token.SEPARATOR, '    '),
            Token(Token.ARGUMENT, '${test}'),
            Token(Token.EOL, '\n'),
            Token(Token.SEPARATOR, '    '),
            Token(Token.KEYWORD, 'Login EzScrum'),
            Token(Token.EOL, '\n')
        ]

        self.creator.create_new_keyword_for_file(test_data+'/ezScrum.txt', 'New Created Keyword', keywordBody)
        
        newModel = self.builder.build(test_data+'/ezScrum.txt')
        self.finder.visit_model_for_finding_keyword(newModel, 'New Created Keyword')
        keywords = self.finder.get_keyword_defs()
        self.assertEqual(len(keywords), 1)

        recovery_models([tearDownModel])

    # def test_wrap_some_keywords_as_one_keyword(self):
    #     tearDownModel = self.builder.build(test_data+'/ezScrum.txt')
        # RefactoringFacade().wrap_some_keywords_as_one_keyword(test_data, test_data+'/add sprint.robot', 10, 11, test_data+'/ezScrum.txt', 'Choose File And Click Side')
        # RefactoringFacade().wrap_some_keywords_as_one_keyword(test_data, test_data+'/test_data.robot', 116, 121, test_data+'/ezScrum.txt', 'Choose File And Click Side')
        # newModel = self.builder.build(test_data+'/ezScrum.txt')
        # self.finder.visit_model_for_finding_keyword(newModel, 'Choose File And Click Side')
        # keywords = self.finder.get_keyword_defs()
        # self.assertEqual(len(keywords), 1)

        # recovery_models([tearDownModel])