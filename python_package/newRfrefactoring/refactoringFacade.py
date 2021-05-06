import sys
from os import path
p = path.normpath(path.dirname(path.abspath(__file__))+"/../..")
sys.path.append(p)
from python_package.newRfrefactoring.builder.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywords.keywordFinder import KeywordFinder
from python_package.newRfrefactoring.checker.fileChecker import FileChecker
from python_package.newRfrefactoring.helper.lineKeywordsHelper import LineKeywordsHelper
from python_package.newRfrefactoring.keywords.keywordCreator import KeywordCreator

class RefactoringFacade:

    def __init__(self):
        self.builder = TestModelBuilder()
        self.finder = KeywordFinder()
        self.checker = FileChecker()
        self.lineKwsHelper = LineKeywordsHelper()
        self.creator = None
    
    def build_project_models(self, projectPath):
        allModels = self.builder.get_all_models_in_directory(projectPath)
        self.creator = KeywordCreator(allModels)
        return allModels
    
    def build_file_model(self, filePath):
        return self.builder.build(filePath)

    def get_steps_that_will_be_wraped(self, fromModel, startLine, endLine):
        self.finder.find_keywords_by_lines(fromModel, startLine, endLine)
        return self.finder.get_lines_keywords()

    def get_same_keywords_with_steps(self, allModels, steps):
        self.checker.find_models_with_same_keywords(allModels, steps)
        return self.checker.get_models_with_same_keywords()