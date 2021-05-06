*** Settings ***
Documentation     ${settingVariable} document
Suite Setup       Open Browser    ${settingVariable}
Suite Teardown    Close Browser    ${settingVariable}
Test Setup        Login EzScrum
Test Teardown     Run Keywords    Delete Sprint    stress_tests    ${testVariable}_1
...               AND    Close Browser    ${testVariable}
Force Tags        ${settingVariable} test data    ${settingVariable}_5
Library           SeleniumLibrary    ${settingVariable}
Resource          testResource.txt
Resource          ezScrum.txt

*** Variable ***
${settingVariable}    chrome
${testVariable}    test variable

*** Test Cases ***
Add a sprint to project
    Choose Project    One
    Click SideBar    Sprint Plan
    Add Sprint    sprint_goal=stress_tests    start_date=2019/08/15    interval=1    team_size=5    hours_to_commit=5    focus_factor=100
    Sprint Should Exist    stress_tests

test temp
    [Documentation]    ${testVariable}
    [Tags]    ${testVariable}
    [Setup]    Choose Project    ${testVariable}
    [Template]    Choose Project
    [Timeout]    50${testVariable}
    project_name=${testVariable}_1
    project_name=${testVariable}_2
    project_name=${testVariable}_3

test variable assign in step
    [Tags]    ${testVariable}
    [Setup]    Choose Project    ${testVariable}
    [Timeout]    50${testVariable}
    Choose Project    ${testVariable}_9
    ${testVariable} =    Set Variable    duplicate variable name
    Should Be Equal    ${testVariable}    duplicate variable name
    [Teardown]    Log    teardown ${testVariable}

*** Keywords ***
Choose Project
    [Arguments]    ${project_name}
    Wait Until Page Contains Element    xpath://div[text()='${project_name}']    timeout=3s
    Wait Until Element Is Visible    xpath://div[text()='${project_name}']    timeout=3s
    Click Element    xpath://div[text()='${project_name}']
    Wait Until Element Is Visible    xpath://*[@id='ProjectNameInfo' and contains(text(),'${project_name}')]    timeout=3s

Click SideBar
    [Arguments]    ${title}=5
    Wait Until Page Contains Element    xpath://span[text()='${title}']
    Wait Until Element Is Visible    xpath://span[text()='${title}']
    Click Element    xpath://span[text()='${title}']
    Run Keyword If    "${title}"=="Sprint Plan"    Wait Until Element Is Visible    xpath://span[text()='Sprint Plan List']
    Run Keyword If    "${title}"=="Sprint Backlog"    Wait Until Element Is Visible    xpath://span[text()='Story & Task List']
    Wait Until Page Does Not Contain Element    xpath://*[text()='loading info...']    timeout=1s

Add Sprint
    [Arguments]    ${sprint_goal}    ${start_date}    ${interval}    ${team_size}    ${hours_to_commit}    ${focus_factor}
    Click Add Sprint Button
    Input Information    ${sprint_goal}    ${start_date}    ${interval}    ${team_size}    ${hours_to_commit}    ${focus_factor}
    Click Submit Button

Sprint Should Exist
    [Arguments]    ${sprint_goal}
    Wait Until Page Contains Element    xpath://*[contains(@class,' x-grid-panel')]//*[text()='${sprint_goal}']
    Wait Until Element Is Visible    xpath://*[contains(@class,' x-grid-panel')]//*[text()='${sprint_goal}']

Click Submit Button
    Wait Until Page Contains Element    xpath://*[contains(@class,'x-window') and contains(@style,'visibility: visible')]//table[contains(@class,'x-btn') and not(contains(@class,'disabled'))]//*[text()='Submit']    timeout=1s    error=Submit Button is not enable
    Click Button    xpath://*[contains(@class,'x-window') and contains(@style,'visibility: visible')]//table[contains(@class,'x-btn') and not(contains(@class,'disabled'))]//*[text()='Submit']
    Wait Until Element Is Not Visible    xpath://*[contains(@class,'x-window') and contains(@style,'visibility: visible')]//*[text()='Add New Sprint']

Click Add Sprint Button
    Click Button    xpath://*[@id='SprintPlan_Page']//button[text()='New Sprint' and not(@disabled)]
    Wait Until Element Is Visible    xpath://*[contains(@class,'x-window') and contains(@style,'visibility: visible')]

Delete Sprint
    [Arguments]    ${sprint_name}
    Click Element    xpath://*[text()='${sprint_name}']
    Wait Until Page Contains Element    xpath://table[contains(@class,'x-btn') and not(contains(@class,'disabled'))]//*[text()='Delete Sprint']
    Click Element    xpath://table[contains(@class,'x-btn') and not(contains(@class,'disabled'))]//*[text()='Delete Sprint']
    Wait Until Element Is Visible    xpath://*[contains(@class,'x-window') and contains(@style,'visibility: visible')]//table[contains(@class,'x-btn') and not(contains(@class,'disabled'))]//*[text()='Delete']
    Click Element    xpath://*[contains(@class,'x-window') and contains(@style,'visibility: visible')]//table[contains(@class,'x-btn') and not(contains(@class,'disabled'))]//*[text()='Delete']

Input Information
    [Arguments]    ${sprint_goal}    ${start_date}    ${interval}    ${team_size}    ${hours_to_commit}    ${focus_factor}
    Input Field    Sprint Goal    ${sprint_goal}
    Input Field    Start Date    ${start_date}
    Input Field    Interval (weeks)    ${interval}
    Input Field    Team size    ${team_size}
    Input Field    Hours to Commit    ${hours_to_commit}
    Input Field    Focus Factor    ${focus_factor}

Input Field
    [Arguments]    ${field_name}    ${text}
    Input Text    xpath://*[contains(@class,'x-window') and contains(@style,'visibility: visible')]//*[@class='x-form-item ' and .//label[contains(normalize-space(),'${field_name}')]]//*[self::input or self::textarea]    ${text}

Test Keyword
    Log    ${testVariable}
    Log    321
    [Teardown]    Run Keywords    Log    ${testVariable}123
    ...    AND    Log    321

Duplicate Variable Keyword
    Log    ${testVariable}
    Log    321
    ${testVariable} =    Set Variable    duplicate variable test data
    [Teardown]    Run Keywords    Log    ${testVariable}123
    ...    AND    Log    321

For Loop Keyword
    [Arguments]    ${times}
    :FOR    ${var}    IN    @{testVariable}
    \    Log    ${times}
    \    test    ${testVariable}

Difference Kinds of Variable Keyword
    Log    &{testVariable}
    Log    7&{testVariable}['data']
    Log    ${testVariable['data']}
    Log    ${testVariable["data"]}5
    Log    67@{testVariable}[5]8
    Log    123{testVariable}567

Default argument Keyword
    [Arguments]    ${test}=${testVariable}
    Log    msg=${testVariable}
