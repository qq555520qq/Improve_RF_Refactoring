import ast
from python_package.newRfrefactoring.utility import normalize


class FileChecker(ast.NodeVisitor):

    def __init__(self):
        self.isKeywordCalled = False
        self.isResourceImported = False
        self.checkedKeyword = None
        self.checkedResource = None
        self.correctModels = []

    def visit_SuiteSetup(self, node):
        """
            Visit all keyword's call in suite_setup to do something.
        """
        if(not(self.isKeywordCalled)):
            self.is_keyword_equal(node.name)

    def visit_SuiteTeardown(self, node):
        """
            Visit all keyword's call in suite_teardown to do something.
        """
        if(not(self.isKeywordCalled)):
            self.is_keyword_equal(node.name)

    def visit_TestSetup(self, node):
        """
            Visit all keyword's call in test_setup to do something.
        """
        if(not(self.isKeywordCalled)):
            self.is_keyword_equal(node.name)

    def visit_TestTeardown(self, node):
        """
            Visit all keyword's call in test_teardown to do something.
        """
        if(not(self.isKeywordCalled)):
            self.is_keyword_equal(node.name)

    def visit_Setup(self, node):
        """
            Visit all keyword's call in setup to do something.
        """
        if(not(self.isKeywordCalled)):
            self.is_keyword_equal(node.name)

    def visit_Teardown(self, node):
        """
            Visit all keyword's call in teardown to do something.
        """
        if(not(self.isKeywordCalled)):
            self.is_keyword_equal(node.name)

    def visit_TestTemplate(self, node):
        """
            Visit all keyword's call in test_template to do something.
        """
        if(not(self.isKeywordCalled)):
            self.is_keyword_equal(node.name)

    def visit_Template(self, node):
        """
            Visit all keyword's call in template to do something.
        """
        if(not(self.isKeywordCalled)):
            self.is_keyword_equal(node.value)

    def visit_KeywordCall(self, node):
        """
            Visit all keyword's call to do something.
        """
        if(not(self.isKeywordCalled)):
            self.is_keyword_equal(node.keyword)

    def visit_ResourceImport(self, node):
        """
            Visit all Resource to do something.
        """
        if(not(self.isResourceImported)):
            self.is_resource_equal(node.name)

    def is_keyword_equal(self, keywordName):
        if(normalize(keywordName) == normalize(self.checkedKeyword)):
            self.isKeywordCalled = True

    def is_resource_equal(self, resource):
        if(self.checkedResource in resource):
            self.isResourceImported = True

    def visit_model_to_check_keyword_and_resource(self, testModel, keyword, resource):
        self.checkedResource = resource
        self.checkedKeyword = keyword
        self.visit(testModel)

        if(self.isKeywordCalled and self.isResourceImported):
            self.isKeywordCalled = False
            self.is_resource_equal = False
            self.correctModels.append(testModel)
        else:
            self.isKeywordCalled = False
            self.is_resource_equal = False

    def visit_models_to_check_keyword_and_resource(self, testModels, keyword, resource):
        for testModel in testModels:
            if isinstance(testModel, list):
                self.visit_models_to_check_keyword_and_resource(testModel, keyword, resource)
            else:
                self.visit_model_to_check_keyword_and_resource(testModel, keyword, resource)

    def get_models_with_resource_and_keyword(self):
        return self.correctModels
