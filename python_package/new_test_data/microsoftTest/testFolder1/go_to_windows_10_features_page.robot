*** Settings ***
Library     SeleniumLibrary
Resource    ../microsoft.txt

Test Setup    Run Keywords    Go To Microsoft
...    AND    Open Language Option
...    AND    Select English Language

*** Variables ***
@{welcomeTainan} =    Welcome    To    Tainan

*** Test Cases ***
Go To "Windows 10 features" Page And Log Welcome Text
    Go To Windows Page
    Open Windows 10 Menu
    Go To "Windows 10 features" Page
    "Windows 10 features" Page Should Be Visible
    FOR    ${var}    IN    @{welcomeTainan}
        Log Double Text    ${var}
    END
    [Teardown]    Close Browser

*** Keywords ***
Go To "Windows 10 features" Page
    Wait Until Page Contains Element    //*[@id='c-shellmenu_60' and normalize-space()='Windows 10 features']    timeout=5s    error="Windows 10 features" in menu should be visible.
    Wait Until Element Is Visible    //*[@id='c-shellmenu_60' and normalize-space()='Windows 10 features']    timeout=5s    error="Windows 10 features" in menu should be visible.
    Click Element    //*[@id='c-shellmenu_60' and normalize-space()='Windows 10 features']
    Sleep    2s

"Windows 10 features" Page Should Be Visible
    Wait Until Page Contains Element    //*[normalize-space()='Do great things with Windows']    timeout=5s    error="Windows 10 features" Page Should Be Visible.
    Wait Until Element Is Visible    //*[normalize-space()='Do great things with Windows']    timeout=5s    error="Windows 10 features" Page Should Be Visible.
    Sleep    2s