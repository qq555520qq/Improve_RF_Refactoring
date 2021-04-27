import sys
from os import path
p = path.normpath(path.dirname(path.abspath(__file__))+"/../..")
sys.path.append(p)
from python_package.newRfrefactoring.threadWithReturn import BuildingModelThread
from python_package.newRfrefactoring.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywordFinder import KeywordFinder
from python_package.newRfrefactoring.fileChecker import FileChecker
from python_package.newRfrefactoring.keywordCreator import KeywordCreator
from python_package.newRfrefactoring.utility import print_keywordCall_for_linesKeywords, print_loop_for_linesKeywords, print_run_keywords_for_linesKeywords, normalize, clear_screen

def print_all_lines_keywords(liensKeywords):
    for index, keyword in enumerate(liensKeywords):
        if(keyword['node'].__class__.__name__ == 'KeywordCall'):
            print_keywordCall_for_linesKeywords(keyword['node'])
        elif(keyword['node'].__class__.__name__ == 'ForLoop'):
            print_loop_for_linesKeywords(keyword)
        elif(keyword['node'].__class__.__name__ == 'SuiteSetup' or keyword['node'].__class__.__name__ == 'SuiteTeardown' or keyword['node'].__class__.__name__ == 'TestSetup' or keyword['node'].__class__.__name__ == 'TestTeardown'or keyword['node'].__class__.__name__ == 'Setup' or keyword['node'].__class__.__name__ == 'Teardown'):
            print_run_keywords_for_linesKeywords(keyword)

def print_line_keyword(lineKeywords, line):
    for lineKeyword in lineKeywords:
        if(lineKeyword['node'].__class__.__name__ == 'KeywordCall'):
            print_keywordCall_for_linesKeywords(lineKeyword['node'], line)
        elif(lineKeyword['node'].__class__.__name__ == 'ForLoop'):
            print_loop_for_linesKeywords(lineKeyword, line)
        elif(lineKeyword['node'].__class__.__name__ == 'SuiteSetup' or lineKeyword['node'].__class__.__name__ == 'SuiteTeardown' or lineKeyword['node'].__class__.__name__ == 'TestSetup' or lineKeyword['node'].__class__.__name__ == 'TestTeardown'or lineKeyword['node'].__class__.__name__ == 'Setup' or lineKeyword['node'].__class__.__name__ == 'Teardown'):
            print_run_keywords_for_linesKeywords(lineKeyword, line)

def get_arguments_of_new_keyword_from_user():
    newKeywordArgs = []
    while True:
        if len(newKeywordArgs) == 0:
            print('\nNew keyword without arguments now.')
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

def get_arguments_of_the_keyword_from_user():
    newKeywordArgs = []
    while True:
        if len(newKeywordArgs) == 0:
            print('The keyword without arguments now.')
        else:
            print('\nThe following information is the keyword\'s arguments now.')
            for index, arg in enumerate(newKeywordArgs):
                print('New argument' + str(index+1) + ':' + arg)
            print('')
        arg = input('If you want to add a new argument for the keyword, please input argument content.\nIf you don\'t want to add a new argument, please input \'Exit input\'.\n\nNew argument' + str(len(newKeywordArgs) + 1) + ':')
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

            clear_screen()
            print('According to your data we found the following information and we will wrap these keywords as a new keyword.')
            print_all_lines_keywords(lineKeywords)
            newKeywordArgs = get_arguments_of_new_keyword_from_user()
            if len(newKeywordArgs) != 0:
                argsTokens = creator.build_tokens_of_arguments(newKeywordArgs)

            isChangeArgument = input('Do you want to change keywords\' arguments?(Y\\N):')
            while normalize(isChangeArgument) == normalize('Y'):
                clear_screen()
                print('Please select keyword that you want to change arguments.')
                print_all_lines_keywords(lineKeywords)
                line = int(input('Please input line that you want to change.\nLine:'))
                clear_screen()
                print('This is the keyword\'s information now.')
                print_line_keyword(lineKeywords, line)
                keywordArgs = get_arguments_of_the_keyword_from_user()
                # 更新Lines keywords
                clear_screen()
            # keywordsDict = creator.get_keywords_dictionary_with_args(lineKeywords)

            # self.creator.create_new_keyword_for_file(newKeywordPath, newKeywordName, lineKeywords)
            exit('Thank you for using.')
        else:
            print('Please input correct mode')
