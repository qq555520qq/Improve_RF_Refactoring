import ast
from robot.api import get_model, Token
from python_package.newRfrefactoring.utility import normalize


class KeywordFinder(ast.NodeVisitor):

    def __init__(self):
        self.keywordCallList = []
        self.keywordDefList = []
        self.model = None
        self.keyword = None

    # def visit_SuiteSetup(self, node):
    #     """
    #         Visit all keyword's call in suite_setup to do something.
    #     """
    #     self.append_keywordCall_into_list(node, node.name)

    # def visit_SuiteTeardown(self, node):
    #     """
    #         Visit all keyword's call in suite_teardown to do something.
    #     """
    #     self.append_keywordCall_into_list(node, node.name)

    # def visit_TestSetup(self, node):
    #     """
    #         Visit all keyword's call in test_setup to do something.
    #     """
    #     self.append_keywordCall_into_list(node, node.name)

    # def visit_TestTeardown(self, node):
    #     """
    #         Visit all keyword's call in test_teardown to do something.
    #     """
    #     self.append_keywordCall_into_list(node, node.name)

    # def visit_Setup(self, node):
    #     """
    #         Visit all keyword's call in setup to do something.
    #     """
    #     self.append_keywordCall_into_list(node, node.name)

    # def visit_Teardown(self, node):
    #     """
    #         Visit all keyword's call in teardown to do something.
    #     """
    #     self.append_keywordCall_into_list(node, node.name)

    # def visit_TestTemplate(self, node):
    #     """
    #         Visit all keyword's call in test_template to do something.
    #     """
    #     self.append_keywordCall_into_list(node, node.name)

    # def visit_Template(self, node):
    #     """
    #         Visit all keyword's call in template to do something.
    #     """
    #     self.append_keywordCall_into_list(node, node.value)

    # def visit_KeywordCall(self, node):
    #     """
    #         Visit all keyword's call to do something.
    #     """
    #     self.append_keywordCall_into_list(node, node.keyword)

    def visit_Keyword(self, node):
        """ 
            Visit every keyword to get keywordDef and keywordCalled
        """
        keywordDef = node.header.get_value(Token.KEYWORD_NAME)
        self.append_keywordDef_into_list(node, keywordDef)

        for token in node.body:
            if(token.__class__.__name__ == 'keywordCall'):
                self.append_keywordCall_into_list(node, token.get_value(Token.KEYWORD))
            elif(token.__class__.__name__ == 'Teardown'):
                self.append_keywordCall_into_list(node, token.get_value(Token.NAME))
                for keyword in token.get_values(Token.ARGUMENT):
                    self.append_keywordCall_into_list(node, keyword)

    def visit_model_for_finding_keyword(self, model, keyword):
        """ 
            Start visiting model.
        """
        self.keyword = normalize(keyword)
        self.model = model
        self.visit(model)

    def visit_models_for_finding_keyword(self, models, keyword):
        """ 
            Start visiting every models.
        """
        for model in models:
            if isinstance(model, list):
                self.visit_models_for_finding_keyword(model, keyword)
            else:
                self.visit_model_for_finding_keyword(model, keyword)

    def append_keywordCall_into_list(self, node, keywordCall):
        if normalize(keywordCall) == self.keyword:
            nodeDict = {'model': self.model, 'node': node}
            self.keywordCallList.append(nodeDict)

    def append_keywordDef_into_list(self, node, keywordDef):
        if normalize(keywordDef) == self.keyword:
            nodeDict = {'model': self.model, 'node': node}
            self.keywordDefList.append(nodeDict)

    def clear_keyword_calls(self):
        self.keywordCallList = []

    def clear_keyword_defs(self):
        self.keywordDefList = []

    def get_keyword_calls(self):
        return self.keywordCallList

    def get_keyword_defs(self):
        return self.keywordDefList
