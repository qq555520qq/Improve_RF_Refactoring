*** Settings ***
Library     SeleniumLibrary
Resource    ../../microsoft.txt
Resource    ../../common.txt

Test Setup    Run Keywords    Go To Microsoft
...    AND    Open Language Option
...    AND    Select English Language

*** Variables ***
@{welcomeTaichung} =    Welcome    To    Taichung

*** Test Cases ***
Go To "Remote resources & tips" Page And Log Welcome Text
    Go To Windows Page
    Open Windows 10 Menu
    Go To "Remote resources & tips" Page
    "Remote resources & tips" Page Should Be Visible
    FOR    ${var}    IN    @{welcomeTaichung}
        Log Double Text    ${var}
    END
    Log Triple Text    Welcome to Taichung very much
    [Teardown]    Close Browser

*** Keywords ***
Go To "Remote resources & tips" Page
    Wait Until Page Contains Element    //*[@id='c-shellmenu_58' and normalize-space()='Remote resources & tips']    timeout=5s    error="Remote resources & tips" in menu should be visible.
    Wait Until Element Is Visible    //*[@id='c-shellmenu_58' and normalize-space()='Remote resources & tips']    timeout=5s    error="Remote resources & tips" in menu should be visible.
    Click Element    //*[@id='c-shellmenu_58' and normalize-space()='Remote resources & tips']
    Sleep    2s

"Remote resources & tips" Page Should Be Visible
    Wait Until Page Contains Element    //*[normalize-space()='Tips and ideas to stay productive and connected at home']    timeout=5s    error="Remote resources & tips" Page Should Be Visible.
    Wait Until Element Is Visible    //*[normalize-space()='Tips and ideas to stay productive and connected at home']    timeout=5s    error="Remote resources & tips" Page Should Be Visible.
    Sleep    2s