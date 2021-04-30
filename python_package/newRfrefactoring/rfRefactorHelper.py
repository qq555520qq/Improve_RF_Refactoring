import sys
from os import path
p = path.normpath(path.dirname(path.abspath(__file__))+"/../..")
sys.path.append(p)
from python_package.newRfrefactoring.common.threadWithReturn import BuildingModelThread
from python_package.newRfrefactoring.builder.testModelBuilder import TestModelBuilder
from python_package.newRfrefactoring.keywords.keywordFinder import KeywordFinder
from python_package.newRfrefactoring.checker.fileChecker import FileChecker
from python_package.newRfrefactoring.keywords.keywordCreator import KeywordCreator
from python_package.newRfrefactoring.keywords.keywordPrinter import KeywordPrinter
from python_package.newRfrefactoring.helper.lineKeywordsHelper import LineKeywordsHelper
from python_package.newRfrefactoring.common.utility import *
from prettytable import PrettyTable

def print_arugments_for_string_list(args):
    print('\nThe following information is new keyword\'s arguments now.')
    argsTable = PrettyTable()
    argsTable.field_names = ['Number', 'Argument']
    for index, arg in enumerate(args):
        argsTable.add_row([index + 1, arg])
    print(argsTable)

def get_arguments_of_new_keyword_from_user():
    newKeywordArgs = []
    while True:
        if len(newKeywordArgs) == 0:
            print('\nNew keyword without arguments now.')
        else:
            print_arugments_for_string_list(newKeywordArgs)
            print('')
        arg = input('If you want to add a new argument for new keyword, please input argument content.\nIf you don\'t want to add a new argument, please input \'Exit input\'.\n\nNew argument' + str(len(newKeywordArgs) + 1) + ':')
        if normalize(arg) == normalize('Exit input'):
            break
        else:
            newKeywordArgs.append(arg)
    return newKeywordArgs

def get_arguments_for_line_keyword(keywordWithLine):
    if is_KeywordCall(keywordWithLine['belong']['node']):
        return keywordWithLine['node'].args
    elif is_ForLoop(keywordWithLine['belong']['node']):
        return keywordWithLine['node'].args
    elif is_Keyword_tag(keywordWithLine['belong']['node']):
        if len(keywordWithLine['belong']['body']) != 0:
            return keywordWithLine['node']['arguments']
        else:
            return keywordWithLine['node'].args

if __name__ == '__main__':
    builder = TestModelBuilder()
    finder = KeywordFinder()
    checker = FileChecker()
    creator = KeywordCreator()
    lineKwsHelper = LineKeywordsHelper()
    kwPrinter = KeywordPrinter()

    clear_screen()
    print('Please select a mode:')
    print('1. Wrap steps as a keyword')
    mode = None
    while True:
        mode = input('Mode:')
        if(mode == '1.' or mode == '1'):
            # projectPath = input('Please input the folder\'s path which will be scanned.\nScanned folder path:')
            projectPath = 'D:/Thesis Local/Thesis_For_Refactor/python_package/test_data'
            projectbuildThread = BuildingModelThread(projectPath)
            projectbuildThread.start()

            print('Please input the file\'s path which has the steps that will be wrapped as a keyword.')
            # fromFilePath = input('File path:')
            fromFilePath = 'D:/Thesis Local/Thesis_For_Refactor/python_package/test_data/test_data.robot'
            fileBuildThread = BuildingModelThread(fromFilePath)
            fileBuildThread.start()

            print('Please input start line and end line to get steps.')
            # startLine = int(input('Start line:'))
            # endLine = int(input('End line:'))
            startLine = 134
            endLine = 140

            print('Please wait, Models building~')
            allModels = projectbuildThread.join()
            fromModel = fileBuildThread.join()

            finder.find_keywords_by_lines(fromModel, startLine, endLine)
            lineKeywords = finder.get_lines_keywords()
            checker.find_models_with_same_keywords(allModels, lineKeywords)
            modelsWithSameKeywords = checker.get_models_with_same_keywords()
            clear_screen()

            print('According to your data we found the following information and we will wrap these keywords as a new keyword.')
            kwPrinter.print_all_lines_keywords(lineKeywords)
            newKeywordArgs = get_arguments_of_new_keyword_from_user()
            if len(newKeywordArgs) != 0:
                clear_screen()
                print_arugments_for_string_list(newKeywordArgs)
                newKeywordArgsTokens = creator.build_tokens_of_arguments(newKeywordArgs)
                for arg in newKeywordArgs:
                    isChangeArgument = input('\nDo you want to change keywords\' arguments with new argument \"'+ arg +'\"?(Y\\N):')
                    while normalize(isChangeArgument) == normalize('Y'):
                        clear_screen()
                        kwPrinter.print_all_lines_keywords(lineKeywords)
                        line = int(input('Please input line that you want to change.\nLine:'))
                        keywordWithLine = lineKwsHelper.get_line_keyword_from_line_keywords(lineKeywords, line)
                        clear_screen()
                        if keywordWithLine:
                            print('This is the keyword\'s information now.')
                            kwPrinter.print_line_keyword(keywordWithLine['node'])
                            argNum = input('Please input the argument number which you want to replace with \"' + arg + '\"\n(Ex:1)\nArgument number:')
                            lineKeywordArgs = get_arguments_for_line_keyword(keywordWithLine)
                            while not(argNum.isdigit() and int(argNum) > 0 and int(argNum) <= len(lineKeywordArgs)):
                                print('Please input correct argument number.')
                                argNum = input('Please input the argument number which you want to replace with \"' + arg + '\"\n(Ex:1)\nArgument number:')
                            updatedData = {'lineKeyword': keywordWithLine, 'updateArg': lineKeywordArgs[int(argNum) - 1], 'newArg': arg}
                            lineKwsHelper.update_arguments_of_line_keyword(lineKeywords, updatedData)
                            #完成更新參數
                        else:
                            print('There is not keyword in line that you input.')
                        isChangeArgument = input('Do you want to change other keywords\' arguments?(Y\\N):')





            # keywordsDict = creator.get_keywords_dictionary_with_args(lineKeywords)

            # self.creator.create_new_keyword_for_file(newKeywordPath, newKeywordName, lineKeywords)
            exit('Thank you for using.')
        else:
            print('Please input correct mode')
