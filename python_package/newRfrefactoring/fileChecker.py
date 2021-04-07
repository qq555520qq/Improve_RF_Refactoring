import ast
from robot.api import Token
from python_package.newRfrefactoring.utility import normalize, get_file_name_from_path


class FileChecker(ast.NodeVisitor):

    def __init__(self):
        self.isKeywordCalled = False
        self.isResourceImported = False
        self.checkedKeyword = None
        self.checkedResource = None
        self.correctModels = []

    def visit_SuiteSetup(self, node):
        """
            Visit all keyword's call in suite_setup to check isKeywordUsed.
        """
        self.is_keyword_used_for_multiple_keyword(node)

    def visit_SuiteTeardown(self, node):
        """
            Visit all keyword's call in suite_teardown to check isKeywordUsed.
        """
        self.is_keyword_used_for_multiple_keyword(node)

    def visit_TestSetup(self, node):
        """
            Visit all keyword's call in test_setup to check isKeywordUsed.
        """
        self.is_keyword_used_for_multiple_keyword(node)

    def visit_TestTeardown(self, node):
        """
            Visit all keyword's call in test_teardown to check isKeywordUsed.
        """
        self.is_keyword_used_for_multiple_keyword(node)

    def visit_Setup(self, node):
        """
            Visit all keyword's call in setup to check isKeywordUsed.
        """
        self.is_keyword_used_for_multiple_keyword(node)

    def visit_Teardown(self, node):
        """
            Visit all keyword's call in teardown to check isKeywordUsed.
        """
        self.is_keyword_used_for_multiple_keyword(node)

    def visit_TestTemplate(self, node):
        """
            Visit all keyword's call in test_template to check isKeywordUsed.
        """
        self.is_keyword_used_for_one_keyword(node.value)

    def visit_Template(self, node):
        """
            Visit all keyword's call in template to check isKeywordUsed.
        """
        self.is_keyword_used_for_one_keyword(node.value)

    def visit_KeywordCall(self, node):
        """
            Visit all keyword's call to check isKeywordUsed.
        """
        self.is_keyword_used_for_one_keyword(node.keyword)

    def visit_ResourceImport(self, node):
        """
            Visit all Resource to check isImported.
        """
        self.is_resource_imported(node.name)

    def is_keyword_used_for_multiple_keyword(self, node):
        keywordCalled = normalize(node.name)
        if(keywordCalled == normalize('Run Keywords')):
            for keywordToken in node.get_tokens(Token.ARGUMENT):
                if(keywordCalled == self.checkedKeyword):
                    self.isKeywordCalled = True
                    break
        else:
            if(keywordCalled == self.checkedKeyword):
                self.isKeywordCalled = True

    def is_keyword_used_for_one_keyword(self, keywordName):
        if(not(self.isKeywordCalled)):
            if(self.checkedKeyword in normalize(keywordName)):
                self.isKeywordCalled = True

    def is_resource_imported(self, resourcePath):
        if(not(self.isResourceImported)):
            if(self.checkedResource in normalize(resourcePath)):
                self.isResourceImported = True

    def visit_model_to_check_keyword_and_resource(self, testModel, keyword, resource):
        self.checkedResource = normalize(resource)
        self.checkedKeyword = normalize(keyword)
        self.visit(testModel)

        if(self.isKeywordCalled and (self.isResourceImported or (normalize(get_file_name_from_path(testModel.source)) == self.checkedResource))):
            self.correctModels.append(testModel)

        self.isKeywordCalled = False
        self.isResourceImported = False

    def visit_models_to_check_keyword_and_resource(self, testModels, keyword, resource):
        for testModel in testModels:
            if isinstance(testModel, list):
                self.visit_models_to_check_keyword_and_resource(testModel, keyword, resource)
            else:
                self.visit_model_to_check_keyword_and_resource(testModel, keyword, resource)

    def get_models_with_resource_and_keyword(self):
        return self.correctModels

    def clear_models_with_resource_and_keyword(self):
        self.correctModels = []