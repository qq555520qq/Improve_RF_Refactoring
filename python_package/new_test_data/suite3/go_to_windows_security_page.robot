*** Settings ***
Library     SeleniumLibrary
Resource    microsoft.txt

Test Setup    Run Keywords    Go To Microsoft
...    AND    Open Language Option
...    AND    Select English Language

*** Variables ***
@{welcomeTexts} =    Welcome    To    Taipei

*** Test Cases ***
Go To "Windows Security" Page And Log Welcome Text
    Go To Windows Page
    Open Windows 10 Menu
    Go To "Windows Security" Page
    Windows Security Page Should Be Visble
    FOR    ${var}    IN    @{welcomeTexts}
        Log Double Text    ${var}
    END
    [Teardown]    Close Browser

*** Keywords ***
Go To "Windows Security" Page
    Wait Until Page Contains Element    //*[@id='c-shellmenu_62' and normalize-space()='Windows security']    timeout=5s    error="Windows security" in menu should be visible.
    Wait Until Element Is Visible    //*[@id='c-shellmenu_62' and normalize-space()='Windows security']    timeout=5s    error="Windows security" in menu should be visible.
    Click Element    //*[@id='c-shellmenu_62' and normalize-space()='Windows security']
    Sleep    1s

Windows Security Page Should Be Visble
    Wait Until Page Contains Element    //*[normalize-space()='The most secure Windows ever']    timeout=5s    error="Windows Security" Page Should Be Visible.
    Wait Until Element Is Visible    //*[normalize-space()='The most secure Windows ever']    timeout=5s    error="Windows Security" Page Should Be Visible.
    Sleep    1s