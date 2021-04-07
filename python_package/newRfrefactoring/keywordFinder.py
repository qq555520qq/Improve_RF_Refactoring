import ast
from robot.api import Token
from python_package.newRfrefactoring.utility import normalize


class KeywordFinder(ast.NodeVisitor):

    def __init__(self):
        self.keywordCallList = []
        self.keywordDefList = []
        self.model = None
        self.targetKeyword = None

    def visit_SuiteSetup(self, node):
        """
            Visit all keyword's call in suite_setup to do something.
        """
        self.append_keywordCall_of_multiple_keywords_into_list(node)

    def visit_SuiteTeardown(self, node):
        """
            Visit all keyword's call in suite_teardown to do something.
        """
        self.append_keywordCall_of_multiple_keywords_into_list(node)

    def visit_TestSetup(self, node):
        """
            Visit all keyword's call in test_setup to do something.
        """
        self.append_keywordCall_of_multiple_keywords_into_list(node)

    def visit_TestTeardown(self, node):
        """
            Visit all keyword's call in test_teardown to do something.
        """
        self.append_keywordCall_of_multiple_keywords_into_list(node)

    def visit_Setup(self, node):
        """
            Visit keyword calls in test cases to get keywordDef and keywordCalled
        """
        self.append_keywordCall_of_multiple_keywords_into_list(node)

    def visit_Teardown(self, node):
        """
            Visit keyword calls in test cases to get keywordDef and keywordCalled
        """
        self.append_keywordCall_of_multiple_keywords_into_list(node)

    def visit_TestTemplate(self, node):
        """
            Visit all keyword's call in test_template to get keywordDef and keywordCalled
        """
        self.append_keywordCall_into_list(node.value, node.get_token(Token.NAME))

    def visit_Template(self, node):
        """
            Visit keyword calls in test cases to get keywordDef and keywordCalled
        """
        self.append_keywordCall_into_list(node.value, node.get_token(Token.NAME))

    def visit_KeywordCall(self, node):
        """
            Visit keyword calls in test cases to get keywordDef and keywordCalled
        """
        self.append_keywordCall_into_list(node.keyword, node.get_token(Token.KEYWORD))

    def visit_Keyword(self, node):
        """ 
            Visit keyword table to get keywordDef and keywordCalled
        """
        keywordDef = node.header.get_value(Token.KEYWORD_NAME)
        self.append_keywordDef_into_list(keywordDef, node)
        
        for token in node.body:
            if(token.__class__.__name__ == 'KeywordCall'):
                self.append_keywordCall_into_list(token.get_value(Token.KEYWORD), token.get_token(Token.KEYWORD))
            elif(token.__class__.__name__ == 'Teardown'):
                self.append_keywordCall_of_multiple_keywords_into_list(token)

    def visit_model_for_finding_keyword(self, model, keyword):
        """ 
            Start visiting model.
        """
        self.targetKeyword = normalize(keyword)
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

    def append_keywordCall_into_list(self, actualKeywordName, keywordToken, nodes=[]):
        if normalize(actualKeywordName) == self.targetKeyword:
            nodeDict = {'model': self.model, 'nodes': nodes, 'token': keywordToken}
            self.keywordCallList.append(nodeDict)

    def append_keywordDef_into_list(self, actualKeywordName, keywordNode):
        if normalize(actualKeywordName) == self.targetKeyword:
            nodeDict = {'model': self.model, 'keywordNode': keywordNode}
            self.keywordDefList.append(nodeDict)

    def append_keywordCall_of_multiple_keywords_into_list(self, node):
        keywordCall = normalize(node.get_value(Token.NAME))
        if(keywordCall == normalize('Run Keywords')):
            for keywordToken in node.get_tokens(Token.ARGUMENT):
                self.append_keywordCall_into_list(keywordToken.value, keywordToken, node)
        else:
            self.append_keywordCall_into_list(keywordCall, node.get_token(Token.NAME))
            

    def clear_keyword_calls(self):
        self.keywordCallList = []

    def clear_keyword_defs(self):
        self.keywordDefList = []

    def get_keyword_calls(self):
        return self.keywordCallList

    def get_keyword_defs(self):
        return self.keywordDefList