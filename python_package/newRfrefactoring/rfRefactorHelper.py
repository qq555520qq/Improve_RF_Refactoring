import sys
from os import path
p = path.normpath(path.dirname(path.abspath(__file__))+"/../..")
sys.path.append(p)
from python_package.newRfrefactoring.threadWithReturn import BuildingModelThread
from python_package.newRfrefactoring.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywordFinder import KeywordFinder
from python_package.newRfrefactoring.fileChecker import FileChecker
from python_package.newRfrefactoring.keywordCreator import KeywordCreator
from python_package.newRfrefactoring.utility import print_keywordCall_for_linesKeywords, print_loop_for_linesKeywords, print_run_keywords_for_linesKeywords, normalize

def print_lines_keywords(liensKeywords):
    for index, keyword in enumerate(liensKeywords):
        if(keyword['node'].__class__.__name__ == 'KeywordCall'):
            print_keywordCall_for_linesKeywords(keyword['node'])
        elif(keyword['node'].__class__.__name__ == 'ForLoop'):
            print_loop_for_linesKeywords(keyword)
        elif(keyword['node'].__class__.__name__ == 'SuiteSetup' or keyword['node'].__class__.__name__ == 'SuiteTeardown' or keyword['node'].__class__.__name__ == 'TestSetup' or keyword['node'].__class__.__name__ == 'TestTeardown'or keyword['node'].__class__.__name__ == 'Setup' or keyword['node'].__class__.__name__ == 'Teardown'):
            print_run_keywords_for_linesKeywords(keyword)

def get_arguments_of_new_keyword_from_user():
    newKeywordArgs = []
    while True:
        if len(newKeywordArgs) == 0:
            print('New keyword without arguments now.')
        else:
            print('\nThe following information is new keyword\'s arguments now.')
            for index, arg in enumerate(newKeywordArgs):
                print('New argument' + str(index+1) + ':' + arg)
            print('')
        arg = input('If you want to add a new argument for new keyword, please input argument content.\nIf you don\'t want to add a new argument, please input \'Exit input\'.\n\nNew argument' + str(len(newKeywordArgs) + 1) + ':')
        if normalize(arg) == normalize('Exit input'):
            break
        else:
            newKeywordArgs.append(arg)
    return newKeywordArgs

if __name__ == '__main__':
    builder = TestModelBuilder()
    finder = KeywordFinder()
    checker = FileChecker()
    creator = KeywordCreator()

    print('Please select a mode:')
    print('1. Wrap steps as a keyword')
    mode = None
    while True:
        mode = input('Mode:')
        if(mode == '1.' or mode == '1'):
#D:\Thesis Local\Thesis_For_Refactor\python_package\test_data
            projectPath = input('Please input the folder\'s path which will be scanned.\nScanned folder path:')
            projectbuildThread = BuildingModelThread(projectPath)
            projectbuildThread.start()

#D:\Thesis Local\Thesis_For_Refactor\python_package\test_data\ezScrum.txt
            print('Please input the file\'s path which has the steps that will be wrapped as a keyword.')
            fromFilePath = input('File path:')
            fileBuildThread = BuildingModelThread(fromFilePath)
            fileBuildThread.start()
#134 138
            print('Please input start line and end line to get steps.')
            startLine = int(input('Start line:'))
            endLine = int(input('End line:'))

            print('Please wait, Models building~')
            allModels = projectbuildThread.join()
            fromModel = fileBuildThread.join()

            finder.find_keywords_by_lines(fromModel, startLine, endLine)
            lineKeywords = finder.get_lines_keywords()

            checker.find_models_with_same_keywords(allModels, lineKeywords)
            modelsWithSameKeywords = checker.get_models_with_same_keywords()

            print('According to your data we found the following information and we will wrap these keywords as a new keyword.')
            print_lines_keywords(lineKeywords)
            newKeywordArgs = get_arguments_of_new_keyword_from_user()
            argsTokens = creator.build_tokens_of_arguments(newKeywordArgs)

            isChangeArgument = input('Do you want to change keywords\' arguments?(Y\N):')
            while True:
                if normalize(isChangeArgument) == normalize('Y'):
                    print_lines_keywords(lineKeywords)
                    print('Please select keyword that you want to change arguments.')

            # for a in modelsWithSameKeywords:
            #     print(a)
            # self.checker.find_models_with_same_keywords(allModels, lineKeywords.copy())
            # modelsWithSameKeywords = self.checker.get_models_with_same_keywords()
            # keywordsDict = self.creator.get_keywords_dictionary_with_args(lineKeywords)

            # self.creator.create_new_keyword_for_file(newKeywordPath, newKeywordName, lineKeywords)
            exit('Thank you for using.')
        else:
            print('Please input correct mode')
