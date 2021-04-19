from python_package.newRfrefactoring.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywordFinder import KeywordFinder
from python_package.newRfrefactoring.fileChecker import FileChecker
from python_package.newRfrefactoring.keywordMoveHelper import KeywordMoveHelper
from robot.parsing.model import Keyword, Statement
from robot.api import Token


class RefactoringFacade:

    def __init__(self):
        self.builder = TestModelBuilder()
        self.finder = KeywordFinder()
        self.checker = FileChecker()
        self.mover = KeywordMoveHelper()



    def wrap_some_keywords_as_one_keyword(self, projectPath, fromPath, startLine, endLine, newKeywordPath, newKeywordName):
        allModels = self.builder.get_all_models_in_directory(projectPath)
        fromModel = self.builder.build(fromPath)
        self.finder.find_keywords_by_lines(fromModel, startLine, endLine)
        lineKeywords = self.finder.get_lines_keywords()
        self.checker.find_models_with_same_keywords(allModels, lineKeywords.copy())
        sameKeywords = self.checker.get_models_with_same_keywords()
        self.create_new_keyword_for_file(newKeywordPath, newKeywordName, lineKeywords)
