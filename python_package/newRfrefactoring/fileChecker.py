import ast
from robot.api import Token
from python_package.newRfrefactoring.utility import normalize, get_file_name_from_path, get_keywords_for_run_keywords


class FileChecker(ast.NodeVisitor):

    def __init__(self):
        self.isKeywordCalled = False
        self.isResourceImported = False
        self.checkKeywordAndResource = False
        self.checkModelsUsingSameKeywords = False
        self.checkedKeyword = None
        self.checkedResource = None
        self.currentModel = None
        self.correctModels = []
        self.copyKeywordsList = []
        self.keywordNamesList = []
        self.sameKeywords = []
        self.tempKeywords = []

    def visit_SuiteSetup(self, node):
        """
            Visit all keyword's call in suite_setup to check isKeywordUsed.
        """
        if self.checkKeywordAndResource:
            self.is_keyword_used_for_run_keywords(node)
        elif self.checkModelsUsingSameKeywords:
            self.append_same_keywords_for_run_keywords(node)

    def visit_SuiteTeardown(self, node):
        """
            Visit all keyword's call in suite_teardown to check isKeywordUsed.
        """
        if self.checkKeywordAndResource:
            self.is_keyword_used_for_run_keywords(node)
        elif self.checkModelsUsingSameKeywords:
            self.append_same_keywords_for_run_keywords(node)

    def visit_TestSetup(self, node):
        """
            Visit all keyword's call in test_setup to check isKeywordUsed.
        """
        if self.checkKeywordAndResource:
            self.is_keyword_used_for_run_keywords(node)
        elif self.checkModelsUsingSameKeywords:
            self.append_same_keywords_for_run_keywords(node)

    def visit_TestTeardown(self, node):
        """
            Visit all keyword's call in test_teardown to check isKeywordUsed.
        """
        if self.checkKeywordAndResource:
            self.is_keyword_used_for_run_keywords(node)
        elif self.checkModelsUsingSameKeywords:
            self.append_same_keywords_for_run_keywords(node)

    def visit_Setup(self, node):
        """
            Visit all keyword's call in setup to check isKeywordUsed.
        """
        if self.checkKeywordAndResource:
            self.is_keyword_used_for_run_keywords(node)
        elif self.checkModelsUsingSameKeywords:
            self.append_same_keywords_for_run_keywords(node)

    def visit_Teardown(self, node):
        """
            Visit all keyword's call in teardown to check isKeywordUsed.
        """
        if self.checkKeywordAndResource:
            self.is_keyword_used_for_run_keywords(node)
        elif self.checkModelsUsingSameKeywords:
            self.append_same_keywords_for_run_keywords(node)

    def visit_TestTemplate(self, node):
        """
            Visit all keyword's call in test_template to check isKeywordUsed.
        """
        if self.checkKeywordAndResource:
            self.is_keyword_used_for_one_keyword(node.value)

    def visit_Template(self, node):
        """
            Visit all keyword's call in template to check isKeywordUsed.
        """
        if self.checkKeywordAndResource:
            self.is_keyword_used_for_one_keyword(node.value)
    
    def visit_ForLoop(self, node):
        """
            Visit all keyword's call to check isKeywordUsed.
        """
        if self.checkKeywordAndResource:
            self.is_keyword_used_for_forloop(node.body)
        elif self.checkModelsUsingSameKeywords:
            self.append_same_keywords_for_forLoop(node)

    def visit_KeywordCall(self, node):
        """
            Visit all keyword's call to check isKeywordUsed.
        """
        if self.checkKeywordAndResource:
            self.is_keyword_used_for_one_keyword(node.keyword)
        elif self.checkModelsUsingSameKeywords:
            self.append_same_keywords_for_one_keyword(node)

    def visit_Keyword(self, node):
        """ 
            Visit keyword table to get keywordDef and keywordCalled
        """
        if self.checkKeywordAndResource:
            for keyword in node.body:
                if keyword.__class__.__name__ == 'KeywordCall':
                    self.is_keyword_used_for_one_keyword(keyword.keyword)
                elif keyword.__class__.__name__ == 'Teardown':
                    self.is_keyword_used_for_run_keywords(keyword)
                elif keyword.__class__.__name__ == 'ForLoop':
                    self.is_keyword_used_for_forloop(keyword.body)
        elif self.checkModelsUsingSameKeywords:
            for keyword in node.body:
                if keyword.__class__.__name__ == 'KeywordCall':
                    self.append_same_keywords_for_one_keyword(keyword)
                elif keyword.__class__.__name__ == 'Teardown':
                    self.append_same_keywords_for_run_keywords(keyword)
                elif keyword.__class__.__name__ == 'ForLoop':
                    self.append_same_keywords_for_forLoop(keyword)

    def visit_ResourceImport(self, node):
        """
            Visit all Resource to check isImported.
        """
        if self.checkKeywordAndResource:
            self.is_resource_imported(node.name)

    def is_keyword_used_for_one_keyword(self, keywordName):
        if(not(self.isKeywordCalled)):
            if(self.checkedKeyword == normalize(keywordName)):
                self.isKeywordCalled = True

    def is_keyword_used_for_run_keywords(self, node):
        if(not(self.isKeywordCalled)):
            keywordCalled = normalize(node.name)
            if(keywordCalled == normalize('Run Keywords')):
                for keywordToken in node.get_tokens(Token.ARGUMENT):
                    if(keywordCalled == self.checkedKeyword):
                        self.isKeywordCalled = True
                        break
            else:
                if(keywordCalled == self.checkedKeyword):
                    self.isKeywordCalled = True

    def is_keyword_used_for_forloop(self, loopBody):
        if(not(self.isKeywordCalled)):
            for loopBodyMember in loopBody:
                if loopBodyMember.__class__.__name__ == 'KeywordCall':
                    self.is_keyword_used_for_one_keyword(loopBodyMember.keyword)
                elif loopBodyMember.__class__.__name__ == 'ForLoop':
                    self.is_keyword_used_for_forloop(loopBodyMember)

    def is_resource_imported(self, resourcePath):
        if(not(self.isResourceImported)):
            if(self.checkedResource in normalize(resourcePath)):
                self.isResourceImported = True

    def visit_model_to_check_keyword_and_resource(self, testModel, keyword, resource):
        self.checkKeywordAndResource = True
        self.checkedResource = normalize(resource)
        self.checkedKeyword = normalize(keyword)
        self.visit(testModel)

        if(self.isKeywordCalled and (self.isResourceImported or (normalize(get_file_name_from_path(testModel.source)) == self.checkedResource))):
            self.correctModels.append(testModel)

        self.isKeywordCalled = False
        self.isResourceImported = False
        self.checkKeywordAndResource = False

    def visit_models_to_check_keyword_and_resource(self, testModels, keyword, resource):
        for testModel in testModels:
            if isinstance(testModel, list):
                self.visit_models_to_check_keyword_and_resource(testModel, keyword, resource)
            else:
                self.visit_model_to_check_keyword_and_resource(testModel, keyword, resource)

    def find_model_with_same_keywords(self, model, nodeDicts):

        def get_keywords_name_from_nodeDictList(nodeDictList):
            keywordNamesList = []
            for nodeDict in nodeDictList:
                if nodeDict['node'].__class__.__name__ == 'KeywordCall':
                    keywordNamesList.append(nodeDict['node'].keyword)
                elif nodeDict['node'].__class__.__name__ == 'ForLoop':
                    for loopBodyMember in nodeDict['body']:
                        keywordNamesList.append(loopBodyMember.keyword)
                else:
                    if(normalize(nodeDict['node'].name) == normalize('Run Keywords')):
                        for keywordDict in nodeDict['body']:
                            keywordNamesList.append(keywordDict['keywordName'].value)
                    else:
                        keywordNamesList.append(nodeDict['node'].name)

            return keywordNamesList
        
        self.checkModelsUsingSameKeywords = True
        self.keywordNamesList = get_keywords_name_from_nodeDictList(nodeDicts)
        self.copyKeywordNamesList = self.keywordNamesList.copy()
        self.currentModel = model
        self.visit(model)
        self.checkModelsUsingSameKeywords = False

    def find_models_with_same_keywords(self, models, nodeDictList):
        for model in models:
            if isinstance(model, list):
                self.find_models_with_same_keywords(model, nodeDictList)
            else:
                self.find_model_with_same_keywords(model, nodeDictList)
    
    def append_same_keywords_for_one_keyword(self, node):
        if self.keywordNamesList[0] == node.keyword:
            modelDict = {'model': self.currentModel, 'node': node}
            self.tempKeywords.append(modelDict)
            del(self.keywordNamesList[0])
            if(len(self.keywordNamesList) == 0):
                self.sameKeywords.append(self.tempKeywords.copy())
                self.tempKeywords = []
                self.keywordNamesList = self.copyKeywordNamesList.copy()
        elif(len(self.copyKeywordNamesList) != len(self.keywordNamesList)):
            self.tempKeywords = []
            self.keywordNamesList = self.copyKeywordNamesList.copy()
    
    def append_same_keywords_for_run_keywords(self, node):
        if(normalize(node.name) == normalize('Run Keywords')):
            keywordTokens = get_keywords_for_run_keywords(node.get_tokens(Token.ARGUMENT))
            for keywordToken in keywordTokens:
                if self.keywordNamesList[0] == keywordToken['keywordName'].value:
                    modelDict = {'model': self.currentModel, 'node': node, 'keyword': keywordToken}
                    self.tempKeywords.append(modelDict)
                    del(self.keywordNamesList[0])
                    if(len(self.keywordNamesList) == 0):
                        self.sameKeywords.append(self.tempKeywords.copy())
                        self.tempKeywords = []
                        self.keywordNamesList = self.copyKeywordNamesList.copy()
                elif(len(self.copyKeywordNamesList) != len(self.keywordNamesList)):
                    self.tempKeywords = []
                    self.keywordNamesList = self.copyKeywordNamesList.copy()
        elif self.keywordNamesList[0] == node.name:
            modelDict = {'model': self.currentModel, 'node': node}
            self.tempKeywords.append(modelDict)
            del(self.keywordNamesList[0])
            if(len(self.keywordNamesList) == 0):
                self.sameKeywords.append(self.tempKeywords.copy())
                self.tempKeywords = []
                self.keywordNamesList = self.copyKeywordNamesList.copy()
        elif(len(self.copyKeywordNamesList) != len(self.keywordNamesList)):
            self.tempKeywords = []
            self.keywordNamesList = self.copyKeywordNamesList.copy()

    def append_same_keywords_for_forLoop(self, node):
        for loopBodyMember in node.body:
            if self.keywordNamesList[0] == loopBodyMember.keyword:
                modelDict = {'model': self.currentModel, 'node': node, 'keyword': loopBodyMember}
                self.tempKeywords.append(modelDict)
                del(self.keywordNamesList[0])
                if(len(self.keywordNamesList) == 0):
                    self.sameKeywords.append(self.tempKeywords.copy())
                    self.tempKeywords = []
                    self.keywordNamesList = self.copyKeywordNamesList.copy()
            elif(len(self.copyKeywordNamesList) != len(self.keywordNamesList)):
                self.tempKeywords = []
                self.keywordNamesList = self.copyKeywordNamesList.copy()

    def get_models_with_resource_and_keyword(self):
        return self.correctModels

    def clear_models_with_resource_and_keyword(self):
        self.correctModels = []

    def get_models_with_same_keywords(self):
        return self.sameKeywords