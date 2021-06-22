*** Settings ***
Library     SeleniumLibrary
Resource    ../microsoft.txt

Test Setup    Run Keywords    Go To Microsoft
...    AND    Open Language Option
...    AND    Select English Language

*** Variables ***
@{welcomeTaipei} =    Welcome    To    Taipei

*** Test Cases ***
Go To "Windows Security" Page And Log Welcome Text
    Go To Windows Page
    Open Windows 10 Menu
    Go To "Windows Security" Page
    "Windows Security" Page Should Be Visible
    FOR    ${var}    IN    @{welcomeTaipei}
        Log Double Text    ${var}
    END
    [Teardown]    Close Browser

*** Keywords ***
Go To "Windows Security" Page
    Wait Until Page Contains Element    //*[@id='c-shellmenu_62' and normalize-space()='Windows security']    timeout=5s    error="Windows security" in menu should be visible.
    Wait Until Element Is Visible    //*[@id='c-shellmenu_62' and normalize-space()='Windows security']    timeout=5s    error="Windows security" in menu should be visible.
    Click Element    //*[@id='c-shellmenu_62' and normalize-space()='Windows security']
    Sleep    2s

"Windows Security" Page Should Be Visible
    Wait Until Page Contains Element    //*[normalize-space()='Protect your data and devices with Windows Security']    timeout=5s    error="Windows Security" Page Should Be Visible.
    Wait Until Element Is Visible    //*[normalize-space()='Protect your data and devices with Windows Security']    timeout=5s    error="Windows Security" Page Should Be Visible.
    Sleep    2s