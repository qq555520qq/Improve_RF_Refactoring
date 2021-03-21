*** Settings ***
Force Tags    example

*** Test Cases ***
Example
    Keyword    argument

Second example
    Keyword    xxx

*** Keywords ***
Keyword
    [Arguments]    ${arg}
    Log    ${arg}