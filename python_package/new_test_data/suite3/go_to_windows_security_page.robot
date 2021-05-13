*** Settings ***
Library     SeleniumLibrary
Resource    mirosoft.txt

*** Test Cases ***
Go To "Windows Security" Page And Log Welcome Text
    Go To Mircosoft
    Open Language Option
    Select English Language
    For Loop Keyword    3
    Go To Windows Page
    Open Windows 10 Menu
    Go To "Windows Security" Page
    Windows Security Page Should Be Visble
    [Teardown]    Close Browser

*** Keywords ***
Go To "Windows Security" Page
    Wait Until Page Contains Element    //*[@id='c-shellmenu_62' and normalize-space()='Windows security']    timeout=5s    error="How to get windows" in menu should be visible.
    Wait Until Element Is Visible    //*[@id='c-shellmenu_62' and normalize-space()='Windows security']    timeout=5s    error="How to get windows" in menu should be visible.
    Click Element    //*[@id='c-shellmenu_62' and normalize-space()='Windows security']

Windows Security Page Should Be Visble
    Wait Until Page Contains Element    //*[normalize-space()='The most secure Windows ever']    timeout=5s    error="Windows Security" Page Should Be Visible.
    Wait Until Element Is Visible    //*[normalize-space()='The most secure Windows ever']    timeout=5s    error="Windows Security" Page Should Be Visible.