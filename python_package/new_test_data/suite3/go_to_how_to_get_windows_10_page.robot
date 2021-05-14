*** Settings ***
Library     SeleniumLibrary
Resource    mirosoft.txt

Test Setup    Run Keywords    Go To Mircosoft
...    AND    Open Language Option
...    AND    Select English Language

*** Variables ***
@{testVariable} =    Welcome    To    Kaohsiung

*** Test Cases ***
Go To "How To Get Windows 10" Page And Log Welcome Text
    For Loop Keyword    8
    Go To Windows Page
    Open Windows 10 Menu
    Go To "How To Get Windows 10" Page
    How To Get Windows 10 Page Should Be Visble
    FOR    ${var}    IN    @{testVariable}
        Log    ${var}
    END
    [Teardown]    Close Browser

*** Keywords ***
Go To "How To Get Windows 10" Page
    Wait Until Page Contains Element    //*[@id='c-shellmenu_55' and normalize-space()='How to get Windows 10']    timeout=5s    error="How to get windows" in menu should be visible.
    Wait Until Element Is Visible    //*[@id='c-shellmenu_55' and normalize-space()='How to get Windows 10']    timeout=5s    error="How to get windows" in menu should be visible.
    Click Element    //*[@id='c-shellmenu_55' and normalize-space()='How to get Windows 10']

How To Get Windows 10 Page Should Be Visble
    Wait Until Page Contains Element    //*[normalize-space()='Want to get Windows 10?']    timeout=5s    error="How To Get Windows 10" Page Should Be Visible.
    Wait Until Element Is Visible    //*[normalize-space()='Want to get Windows 10?']    timeout=5s    error="How To Get Windows 10" Page Should Be Visible.