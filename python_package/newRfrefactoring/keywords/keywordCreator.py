import ast
from robot.api import Token
from robot.parsing.model import Keyword, Statement
from python_package.newRfrefactoring.builder.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywords.keywordMoveHelper import KeywordMoveHelper
from python_package.newRfrefactoring.common.utility import save_model_and_update_old_models, normalize


class KeywordCreator(ast.NodeTransformer):

    def __init__(self, allModels=[]):
        self.allModels = allModels
        self.mover = KeywordMoveHelper(self.allModels)
        self.isRemoveNode = False

    def visit_SuiteSetup(self, node):
        """
            Visit all keyword's call in suite_setup to do somethings.
        """
        if self.isRemoveNode:
            self.is_node_equal_for_run_keywords(node, self.sameKeywordDict)

    def visit_SuiteTeardown(self, node):
        """
            Visit all keyword's call in suite_teardown to do somethings.
        """
        if self.isRemoveNode:
            self.is_node_equal_for_run_keywords(node, self.sameKeywordDict)

    def visit_TestSetup(self, node):
        """
            Visit all keyword's call in test_setup to do somethings.
        """
        if self.isRemoveNode:
            self.is_node_equal_for_run_keywords(node, self.sameKeywordDict)

    def visit_TestTeardown(self, node):
        """
            Visit all keyword's call in test_teardown to do somethings.
        """
        if self.isRemoveNode:
            self.is_node_equal_for_run_keywords(node, self.sameKeywordDict)

    def visit_Setup(self, node):
        """
            Visit all keyword's call in setup to do somethings.
        """
        if self.isRemoveNode:
            self.is_node_equal_for_run_keywords(node, self.sameKeywordDict)

    def visit_Teardown(self, node):
        """
            Visit all keyword's call in teardown to do somethings.
        """
        if self.isRemoveNode:
            self.is_node_equal_for_run_keywords(node, self.sameKeywordDict)

    def visit_TestTemplate(self, node):
        """
            Visit all keyword's call in test_template to do somethings.
        """
        if self.isRemoveNode:
            return self.is_node_equal_for_one_keyword(node, self.sameKeywordDict['node'])

    def visit_Template(self, node):
        """
            Visit all keyword's call in template to do somethings.
        """
        if self.isRemoveNode:
            return self.is_node_equal_for_one_keyword(node, self.sameKeywordDict['node'])
    
    def visit_ForLoop(self, node):
        """
            Visit all keyword's call to do somethings.
        """
        if self.isRemoveNode:
            if self.sameKeywordDict['node'] == node:
                for loopBodyMemeber in node.body.copy():
                    if loopBodyMemeber == self.sameKeywordDict['keyword']:
                        node.remove(loopBodyMemeber)
                        return self.generic_visit(node)
            return node

    def visit_KeywordCall(self, node):
        """
            Visit all keyword's call to do somethings.
        """
        if self.isRemoveNode:
            return self.is_node_equal_for_one_keyword(node, self.sameKeywordDict['node'])

    def create_new_keyword_for_file(self, _path, keywordName, keywordBody):

        targetFileModel = TestModelBuilder().build(_path)

        header = Statement.from_tokens([
            Token(Token.NAME, keywordName),
            Token(Token.EOL, '\n')
        ])

        keywordNode = Keyword(header, keywordBody)

        self.mover.insert_new_keyword_defined(targetFileModel, keywordNode)

    def build_tokens_of_arguments(self, args):
        argsTokens = [
            Token(Token.SEPARATOR, '    '),
            Token(Token.ARGUMENTS, '[Arguments]')
        ]
        for arg in args:
            argsTokens.append(Token(Token.SEPARATOR, '    '))
            argsTokens.append(Token(Token.ARGUMENT, arg))
        argsTokens.append(Token(Token.EOL, '\n'))
        
        return argsTokens

    def is_node_equal_for_one_keyword(self, node, keywordNode):
        if keywordNode == node:
            return None
        return node

    def is_node_equal_for_run_keywords(self, node, keywordDict):
        if node == keywordDict['node']:
            if normalize(node.name) == normalize('Run Keywords'):
                runKeywordsArgs = node.data_tokens
                copyRunKeywordsArgs = runKeywordsArgs.copy()
                for index, runKeywordsArg in enumerate(runKeywordsArgs.copy()):
                    if keywordDict['keywordName'] == runKeywordsArg or runKeywordsArg in keywordDict['Arguments']:
                        runKeywordsArgs.remove(runKeywordsArg)
                        if len(runKeywordsArgs) != (index + 1) and runKeywordsArgs[index + 1].value == 'AND':
                            runKeywordsArgs.remove(runKeywordsArgs[index + 1])
                if len(copyRunKeywordsArgs) != len(runKeywordsArgs):
                    return self.generic_visit(node)                
        return node

    def remove_node_for_same_keywords(self, sameKeywordDict, allModels):
        self.isRemoveNode = True
        self.removedDict = sameKeywordDict
        self.visit(sameKeywordDict['model'])
        save_model_and_update_old_models(sameKeywordDict['model'], allModels)
        self.isRemoveNode = False

    # def replace_old_steps_with_keyword_for_same_keywords(self, sameKeywords, ):
