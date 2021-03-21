import ast
from robot.api import get_model, Token
from python_package.newRfrefactoring.utilty import normalize


class KeywordRenamer(ast.NodeVisitor):

    def __init__(self):
        self.new_name = None
        self.node = None

    def visit_SuiteSetup(self, node):
        """
            Visit all keyword's call in suite_setup to do something.
        """
        if(self.node == node):
            token = node.get_token(Token.KEYWORD)
            token.value = self.new_name

    def visit_SuiteTeardown(self, node):
        """
            Visit all keyword's call in suite_teardown to do something.
        """
        if(self.node == node):
            token = node.get_token(Token.KEYWORD)
            token.value = self.new_name

    def visit_TestSetup(self, node):
        """
            Visit all keyword's call in test_setup to do something.
        """
        if(self.node == node):
            token = node.get_token(Token.KEYWORD)
            token.value = self.new_name

    def visit_TestTeardown(self, node):
        """
            Visit all keyword's call in test_teardown to do something.
        """
        if(self.node == node):
            token = node.get_token(Token.KEYWORD)
            token.value = self.new_name

    def visit_Setup(self, node):
        """
            Visit all keyword's call in setup to do something.
        """
        if(self.node == node):
            token = node.get_token(Token.KEYWORD)
            token.value = self.new_name

    def visit_Teardown(self, node):
        """
            Visit all keyword's call in teardown to do something.
        """
        if(self.node == node):
            token = node.get_token(Token.KEYWORD)
            token.value = self.new_name

    def visit_TestTemplate(self, node):
        """
            Visit all keyword's call in test_template to do something.
        """
        if(self.node == node):
            token = node.get_token(Token.KEYWORD)
            token.value = self.new_name

    def visit_Template(self, node):
        """
            Visit all keyword's call in template to do something.
        """
        if(self.node == node):
            token = node.get_token(Token.KEYWORD)
            token.value = self.new_name

    def visit_KeywordCall(self, node):
        """
            Visit all keyword's call to do something.
        """
        if(self.node == node):
            token = node.get_token(Token.KEYWORD)
            token.value = self.new_name

    def visit_KeywordName(self, node):
        """
            Visit all keyword's define to do something.
        """
        if(self.node == node):
            token = node.get_token(Token.KEYWORD_NAME)
            token.value = self.new_name

    def rename_keyword_for_nodes(self, nodeDicts, new_name):
        self.new_name = new_name

        for nodeDict in nodeDicts:
            self.node = nodeDict['node']
            self.visit(nodeDict['model'])
            nodeDict['model'].save()
