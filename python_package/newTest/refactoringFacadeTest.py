import unittest
from python_package.newRfrefactoring.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywordFinder import KeywordFinder
from python_package.newRfrefactoring.refactoringFacade import RefactoringFacade
from python_package.newRfrefactoring.utility import recovery_models
from robot.parsing.model import Keyword, Statement
from robot.api import Token
from init import test_data


class RefactoringFacadeTest(unittest.TestCase):

    def setUp(self):
        self.builder = TestModelBuilder()
        self.refactor = RefactoringFacade()
        self.finder = KeywordFinder()

    def test_create_new_keyword_for_file(self):
        tearDownModel = self.builder.build(test_data+'/ezScrum.txt')

        keywordBody = Statement.from_tokens([
            Token(Token.SEPARATOR, '    '),
            Token(Token.KEYWORD, 'Login EzScrum'),
            Token(Token.EOL, '\n')
        ])

        self.refactor.create_new_keyword_for_file(test_data+'/ezScrum.txt', 'New Created Keyword', keywordBody)
        
        newModel = self.builder.build(test_data+'/ezScrum.txt')
        self.finder.visit_model_for_finding_keyword(newModel, 'New Created Keyword')
        keywords = self.finder.get_keyword_defs()
        self.assertEqual(len(keywords), 1)

        recovery_models([tearDownModel])