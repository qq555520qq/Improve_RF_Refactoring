import ast
from robot.api import Token
from robot.parsing.model import Keyword, Statement
from python_package.newRfrefactoring.builder.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywords.keywordMoveHelper import KeywordMoveHelper
from python_package.newRfrefactoring.common.utility import save_model_and_update_old_models, normalize, get_keywords_for_run_keywords, is_Keyword_tag


class KeywordCreator(ast.NodeTransformer):

    def __init__(self, allModels=[]):
        self.allModels = allModels
        self.mover = KeywordMoveHelper(self.allModels)
        self.removedDict = None
        self.isRemoveNode = False

    def visit_SuiteSetup(self, node):
        """
            Visit all keyword's call in suite_setup to do somethings.
        """
        if self.isRemoveNode:
            return self.is_node_equal_for_run_keywords(node, self.removedDict)

    def visit_SuiteTeardown(self, node):
        """
            Visit all keyword's call in suite_teardown to do somethings.
        """
        if self.isRemoveNode:
            return self.is_node_equal_for_run_keywords(node, self.removedDict)

    def visit_TestSetup(self, node):
        """
            Visit all keyword's call in test_setup to do somethings.
        """
        if self.isRemoveNode:
            return self.is_node_equal_for_run_keywords(node, self.removedDict)

    def visit_TestTeardown(self, node):
        """
            Visit all keyword's call in test_teardown to do somethings.
        """
        if self.isRemoveNode:
            return self.is_node_equal_for_run_keywords(node, self.removedDict)

    def visit_Setup(self, node):
        """
            Visit all keyword's call in setup to do somethings.
        """
        if self.isRemoveNode:
            return self.is_node_equal_for_run_keywords(node, self.removedDict)

    def visit_Teardown(self, node):
        """
            Visit all keyword's call in teardown to do somethings.
        """
        if self.isRemoveNode:
            return self.is_node_equal_for_run_keywords(node, self.removedDict)

    def visit_TestTemplate(self, node):
        """
            Visit all keyword's call in test_template to do somethings.
        """
        if self.isRemoveNode:
            return self.is_node_equal_for_one_keyword(node, self.removedDict['node'])

    def visit_Template(self, node):
        """
            Visit all keyword's call in template to do somethings.
        """
        if self.isRemoveNode:
            return self.is_node_equal_for_one_keyword(node, self.removedDict['node'])

    def visit_ForLoop(self, node):
        """
            Visit all keyword's call to do somethings.
        """
        if self.isRemoveNode:
            if self.removedDict['node'] == node:
                for loopBodyMemeber in node.body.copy():
                    if loopBodyMemeber == self.removedDict['keyword']:
                        node.body.remove(loopBodyMemeber)
                        if len(node.body) == 0:
                            return None
                        else:
                            return self.generic_visit(node)
            return node

    def visit_KeywordCall(self, node):
        """
            Visit all keyword's call to do somethings.
        """
        if self.isRemoveNode:
            return self.is_node_equal_for_one_keyword(node, self.removedDict['node'])

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

    def is_node_equal_for_run_keywords(self, node, removedDict):
        def get_arguments_value_from_arguments_tokens(argsTokens):
            argsValues = []
            for argToken in argsTokens:
                argsValues.append(argToken.value)
            return argsValues

            removedDict['keyword']['arguments']
        
        if node == removedDict['node']:
            if normalize(node.name) == normalize('Run Keywords'):
                runKeywordsArgs = node.get_tokens(Token.ARGUMENT)
                copyRunKeywordsArgs = runKeywordsArgs.copy()
                for index, runKeywordsArg in enumerate(copyRunKeywordsArgs):
                    removedArgsValues = get_arguments_value_from_arguments_tokens(removedDict['keyword']['arguments'])
                    if runKeywordsArg.value == removedDict['keyword']['keywordName'].value or runKeywordsArg.value in removedArgsValues:
                        removedIndex = runKeywordsArgs.index(runKeywordsArg)
                        del(runKeywordsArgs[removedIndex])
                        if runKeywordsArg.value in removedArgsValues:
                            removedArgsValues.remove(runKeywordsArg.value)
                        if len(runKeywordsArgs) != removedIndex and runKeywordsArgs[removedIndex].value == 'AND':
                            del(runKeywordsArgs[removedIndex])
                        if len(removedArgsValues) == 0:
                            break
                if len(copyRunKeywordsArgs) != len(runKeywordsArgs):
                    if len(runKeywordsArgs) != 0:
                        runKeywordsDict = get_keywords_for_run_keywords(runKeywordsArgs)
                        runKeywordsNode = self.build_tag_keywords_for_run_keywords(node.__class__.__name__, runKeywordsDict)
                        self.removedDict['node'] = runKeywordsNode
                        return self.generic_visit(runKeywordsNode)
                    else:
                        return None
        return node

    def build_tag_keywords_for_run_keywords(self, tagClass, keywords):
        def build_tokens_of_run_keywords(keywordsTokens, keywords):
            isFirst = True
            for keyword in keywords:
                if isFirst:
                    keywordsTokens.append(Token(Token.ARGUMENT, keyword['keywordName'].value))
                    isFirst = False
                else:
                    keywordsTokens.append(Token(Token.EOL, '\n'))
                    keywordsTokens.append(Token(Token.SEPARATOR, '    '))
                    keywordsTokens.append(Token(Token.CONTINUATION, '...'))
                    keywordsTokens.append(Token(Token.SEPARATOR, '                    '))
                    keywordsTokens.append(Token(Token.ARGUMENT, 'AND'))
                    keywordsTokens.append(Token(Token.SEPARATOR, '    '))
                    keywordsTokens.append(Token(Token.ARGUMENT, keyword['keywordName'].value))
                for arg in keyword['arguments']:
                    keywordsTokens.append(Token(Token.SEPARATOR, '    '))
                    keywordsTokens.append(Token(Token.ARGUMENT, arg.value))
        tagToken = None
        if tagClass == 'SuiteSetup':
            tagToken = Token.SUITE_SETUP
        elif tagClass == 'SuiteTeardown':
            tagToken = Token.SUITE_TEARDOWN
        elif tagClass == 'TestSetup':
            tagToken = Token.TEST_SETUP
        elif tagClass == 'TestTeardown':
            tagToken = Token.TEST_TEARDOWN
        elif tagClass == 'Setup':
            tagToken = Token.SETUP
        elif tagClass == 'Teardown':
            tagToken = Token.TEARDOWN
            
        keywordsTokens = [
            Token(Token.SEPARATOR, '    '),
            Token(tagToken, '['+tagClass+']'),
            Token(Token.SEPARATOR, '    '),
            Token(Token.NAME, 'Run Keywords'),
            Token(Token.SEPARATOR, '    ')
        ]
        build_tokens_of_run_keywords(keywordsTokens, keywords)
        return Statement.from_tokens(keywordsTokens)

    def remove_node_for_same_keywords(self, sameKeywordDict, allModels):
        self.isRemoveNode = True
        self.removedDict = sameKeywordDict
        self.visit(sameKeywordDict['model'])
        save_model_and_update_old_models(sameKeywordDict['model'], allModels)
        self.isRemoveNode = False

    def replace_old_steps_with_keyword_for_same_keywords(self, sameKeywords, allModels):
        tagKeywords = []
        updatedNode = None
        for sameKeyword in sameKeywords:
            if is_Keyword_tag(sameKeyword['node']):
                if not(sameKeyword['node'] in tagKeywords):
                    tagKeywords.append(sameKeyword['node'])
                else:
                    sameKeyword['node'] = updatedNode
            self.remove_node_for_same_keywords(sameKeyword, allModels)
            if is_Keyword_tag(sameKeyword['node']):
                updatedNode = sameKeyword['node']
            
