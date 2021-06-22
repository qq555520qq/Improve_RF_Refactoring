*** Settings ***
Library     SeleniumLibrary
Resource    ../microsoft.txt

Test Setup    Run Keywords    Go To Microsoft
...    AND    Open Language Option
...    AND    Select English Language

*** Variables ***
@{welcomeKaohsiung} =    Welcome    To    Kaohsiung

*** Test Cases ***
Go To "How To Get Windows 10" Page And Log Welcome Text
    Go To Windows Page
    Open Windows 10 Menu
    Go To "How To Get Windows 10" Page
    "How To Get Windows 10" Page Should Be Visible
    FOR    ${var}    IN    @{welcomeKaohsiung}
        Log Double Text    ${var}
    END
    [Teardown]    Close Browser

*** Keywords ***
Go To "How To Get Windows 10" Page
    Wait Until Page Contains Element    //*[@id='c-shellmenu_55' and normalize-space()='How to get Windows 10']    timeout=5s    error="How to get windows" in menu should be visible.
    Wait Until Element Is Visible    //*[@id='c-shellmenu_55' and normalize-space()='How to get Windows 10']    timeout=5s    error="How to get windows" in menu should be visible.
    Click Element    //*[@id='c-shellmenu_55' and normalize-space()='How to get Windows 10']
    Sleep    2s

"How To Get Windows 10" Page Should Be Visible
    Wait Until Page Contains Element    //*[normalize-space()='Want to get Windows 10?']    timeout=5s    error="How To Get Windows 10" Page Should Be Visible.
    Wait Until Element Is Visible    //*[normalize-space()='Want to get Windows 10?']    timeout=5s    error="How To Get Windows 10" Page Should Be Visible.
    Sleep    2s