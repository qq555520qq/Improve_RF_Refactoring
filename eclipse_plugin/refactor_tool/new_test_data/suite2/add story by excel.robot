*** Setting ***
Test Setup        Login EzScrum
Test Teardown     Close Browser
Library           SeleniumLibrary
Resource          ezScrum.txt

*** Variables ***
${StoryPath}      C:\\Users\\lab1321\\Documents\\workspace\\thesis\\refactor_tool\\lib\\python\\test_data\\suite2/Story.xls

*** Test Cases ***
Add story to project
    Choose Project    One
    Click SideBar    Product Backlog
    Import Story    ${StoryPath}
    Verify Story Is Imported

*** Keywords ***
Choose Project
    [Arguments]    ${project_name}
    Wait Until Page Contains Element    xpath://div[text()='${project_name}']    timeout=3s
    Wait Until Element Is Visible    xpath://div[text()='${project_name}']    timeout=3s
    Click Element    xpath://div[text()='${project_name}']
    Wait Until Element Is Visible    xpath://*[@id='ProjectNameInfo' and contains(text(),'${project_name}')]    timeout=1.5s

Click SideBar
    [Arguments]    ${title}
    Wait Until Page Contains Element    xpath://span[text()='${title}']
    Wait Until Element Is Visible    xpath://span[text()='${title}']
    Click Element    xpath://span[text()='${title}']
    Run Keyword If    "${title}"=="Sprint Plan"    Wait Until Element Is Visible    xpath://span[text()='Sprint Plan List']
    Run Keyword If    "${title}"=="Product Backlog"    Wait Until Element Is Visible    xpath://span[text()='Product Backlog']
    Wait Until Page Does Not Contain Element    xpath://*[text()='loading info...']    timeout=3s

Import Story
    [Arguments]    ${path}
    Click Import / Export Story Button
    Click Import Story Button
    Choose File    //*[text()='Import Stories:']/..//input[(@name)]    ${path}
    Wait Until Page Contains Element    xpath://*[contains(@class,'x-window') and contains(@style,'visibility: visible')]//table[contains(@class,'x-btn') and not(contains(@class,'disabled'))]//*[text()='Submit']    timeout=5s    error=Submit Button is not enable
    Click Button    xpath://*[contains(@class,'x-window') and contains(@style,'visibility: visible')]//table[contains(@class,'x-btn') and not(contains(@class,'disabled'))]//*[text()='Submit']

Verify Story Is Imported
    Wait Until Page Does Not Contain Element    xpath://div[contains(text(),'Please')]    timeout=3s
    Wait Until Page Does Not Contain Element    xpath://*[text()='loading info...']    timeout=3s

Verify Each Project Can Be Imported Stories
    [Arguments]    ${project_name}
    Login EzScrum
    Choose Project    ${project_name}
    Import Story    ${StoryPath}
    Verify Story Is Imported
    [Teardown]    Close Browser

Add stories to project
    Login EzScrum
    Choose Project    One
    Import Story    ${StoryPath}
    Verify Story Is Imported
    [Teardown]    Close Browser

Click Import Story Button
    Click Element    xpath://*[contains(@class,'x-menu') and contains(@style,'visibility: visible')]//*[text()='Import Story']
    Wait Until Page Contains Element    //*[contains(@class,'x-window') and contains(@style,'visibility: visible')]
    Wait Until Element Is Visible    //*[contains(@class,'x-window') and contains(@style,'visibility: visible')]

Click Import / Export Story Button
    Click Button    xpath://*[@id='productBacklogMasterPanel']//button[text()='Import / Export Story' and not(@disabled)]
    Wait Until Page Contains Element    //*[contains(@class,'x-menu') and contains(@style,'visibility: visible')]
    Wait Until Element Is Visible    //*[contains(@class,'x-menu') and contains(@style,'visibility: visible')]

Click Submit Button
    Wait Until Page Contains Element    xpath://*[contains(@class,'x-window') and contains(@style,'visibility: visible')]//table[contains(@class,'x-btn') and not(contains(@class,'disabled'))]//*[text()='Submit']    timeout=1s    error=Submit Button is not enable
    Click Button    xpath://*[contains(@class,'x-window') and contains(@style,'visibility: visible')]//table[contains(@class,'x-btn') and not(contains(@class,'disabled'))]//*[text()='Submit']
