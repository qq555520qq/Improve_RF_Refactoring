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

builder = TestModelBuilder()
finder = KeywordFinder()
checker = FileChecker()
creator = None
lineKwsHelper = LineKeywordsHelper()
kwPrinter = KeywordPrinter()

def get_project_path_from_user(text):
    projectPath = ''
    while not(path.isdir(projectPath)):
        projectPath = input(text)
    return projectPath

def get_file_path_from_user(text):
    filePath = ''
    while not(path.isfile(filePath)):
        filePath = input(text)
    return filePath

def print_arugments_for_string_list(args):
    print('\nThe following information is new keyword\'s arguments now.')
    argsTable = PrettyTable()
    argsTable.field_names = ['Number', 'Argument']
    for index, arg in enumerate(args):
        argsTable.add_row([index + 1, arg])
    print(argsTable)

def get_arguments_of_new_keyword_from_user(lineKeywords):
    newKeywordArgs = []
    while True:
        clear_screen()
        print('According to your data we found the following information and we will wrap these keywords as a new keyword.')
        kwPrinter.print_all_lines_keywords(lineKeywords)
        if len(newKeywordArgs) == 0:
            print('\nNew keyword without arguments now.')
        else:
            print_arugments_for_string_list(newKeywordArgs)
            print('')
        arg = input('If you want to add a new argument for new keyword, please input argument content.\nIf you don\'t want to add a new argument, please input \'Exit\'.\n\nNew argument' + str(len(newKeywordArgs) + 1) + ':')
        if normalize(arg) == normalize('Exit'):
            break
        else:
            newKeywordArgs.append(arg)
    return newKeywordArgs

def is_arguemnts_changed_from_user(arg, isFirst):
    isChangeArgument = ''
    while(normalize(isChangeArgument) != normalize('Y') and normalize(isChangeArgument) != normalize('N')):
        if isFirst:
            isChangeArgument = input('\nDo you want to change keywords\' arguments with new argument \"'+ arg +'\"?(Y\\N):')
        else:
            isChangeArgument = input('Do you want to change other keywords\' arguments with new argument \"'+ arg +'\"?(Y\\N):')

    if normalize(isChangeArgument) == normalize('Y'):
        return True
    else:
        return False

def update_keywords_arguments(lineKeywords, newKeywordArgs):
    newKeywordArgsTokens = []
    for arg in newKeywordArgs:
        clear_screen()
        print_arugments_for_string_list(newKeywordArgs)
        isFirst = True
        while is_arguemnts_changed_from_user(arg, isFirst):
            clear_screen()
            kwPrinter.print_all_lines_keywords(lineKeywords)
            line = int(get_number_from_user('Please input line that you want to change.\nLine:'))
            keywordWithLine = lineKwsHelper.get_line_keyword_from_line_keywords(lineKeywords, line)
            clear_screen()
            if keywordWithLine:
                print('This is the keyword\'s information now.')
                kwPrinter.print_line_keyword(keywordWithLine['node'])
                argNum = int(get_number_from_user('Please input the argument number which you want to replace with \"' + arg + '\"\n(Ex:1)\nArgument number:'))
                lineKeywordArgs = lineKwsHelper.get_arguments_for_line_keyword(keywordWithLine)
                while not(argNum > 0 and argNum <= len(lineKeywordArgs)):
                    print('Please input correct argument number.')
                    argNum = int(get_number_from_user('Please input the argument number which you want to replace with \"' + arg + '\"\n(Ex:1)\nArgument number:'))
                updatedData = {'lineKeyword': keywordWithLine, 'updateArg': lineKeywordArgs[int(argNum) - 1], 'newArg': arg}
                lineKwsHelper.update_arguments_of_line_keyword(lineKeywords, updatedData)
                clear_screen()
            else:
                print('There is not keyword in line that you input.')
            isFirst = False

def wrap_steps_as_a_new_keyword():
    projectPath = get_project_path_from_user('Please input the folder\'s path which will be scanned.\nScanned folder path:')
    clear_screen()
    # projectPath = 'D:/Thesis Local/Thesis_For_Refactor/python_package/test_data'
    # projectPath = 'D:/Project/test_automation'
    projectbuildThread = BuildingModelThread(projectPath)
    projectbuildThread.start()

    fromFilePath = get_file_path_from_user('Please input the file\'s path which has the steps that will be wrapped as a keyword.\nFile path:')
    clear_screen()
    # fromFilePath = 'D:/Thesis Local/Thesis_For_Refactor/python_package/test_data/test_data.robot'
    # fromFilePath = 'D:/Project/test_automation/RobotTests/Feature Tests/Parts Management/TMD-18039 Edit_View Part Instance Detail Page/Keywords/TMD-18137.txt'
    fileBuildThread = BuildingModelThread(fromFilePath)
    fileBuildThread.start()

    startLine = int(get_number_from_user('Please input start line to get steps.\nStart line:'))
    clear_screen()
    endLine = int(get_number_from_user('Please input end line to get steps.\nEnd line:'))
    clear_screen()
    # startLine = 134
    # endLine = 140
    # startLine = 92
    # endLine = 98

    print('Please wait, Models building~')
    allModels = projectbuildThread.join()
    fromModel = fileBuildThread.join()
    creator = KeywordCreator(allModels)
    clear_screen()

    finder.find_keywords_by_lines(fromModel, startLine, endLine)
    lineKeywords = finder.get_lines_keywords()

    checker.find_models_with_same_keywords(allModels, lineKeywords)
    modelsWithSameKeywords = checker.get_models_with_same_keywords()

    newKeywordArgs = get_arguments_of_new_keyword_from_user(lineKeywords)
    newKeywordArgsTokens = []
    if len(newKeywordArgs) != 0:
        update_keywords_arguments(lineKeywords, newKeywordArgs)
        newKeywordArgsTokens = creator.build_tokens_of_arguments(newKeywordArgs)
    
    newKeywordsBody = lineKwsHelper.get_new_keyword_body_from_line_keywords_and_arguments_tokens(lineKeywords, newKeywordArgsTokens)
    clear_screen()
    kwPrinter.print_all_lines_keywords(lineKeywords)
    newKeywordName = input('Please input name for new keyword.\nKeyword name:')
    clear_screen()
    newKeywordPath = get_file_path_from_user('Please input the file\'s path where new keyword will insert into.\nFile path:')
    # newKeywordPath = 'D:/Thesis Local/Thesis_For_Refactor/python_package/test_data/ezScrum.txt'
    creator.create_new_keyword_for_file(newKeywordPath, newKeywordName, newKeywordsBody)

if __name__ == '__main__':

    clear_screen()
    print('Please select a mode:')
    print('1. Wrap steps as a keyword')
    mode = None
    while True:
        mode = input('Mode:')
        if(mode == '1.' or mode == '1'):
            wrap_steps_as_a_new_keyword()
            exit('Thank you for using.')
        else:
            print('Please input correct mode')
