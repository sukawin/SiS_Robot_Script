*** Settings ***
Library    SeleniumLibrary
Library    BuiltIn
library    DateTime

*** Variables ***
${URL}          https://vrm.homepro.co.th/user/logon.aspx
${USER_ID}      V3096
${PASSWORD}     sisthai@123

*** Test Cases ***
Login And Process Data
    Open Browser And Login
    Accept TOS
    Select Menu Sales
    Export Sales Report
    Select Menu Stock
    Export Stock Report
    Export Stock Report Pivot
    [Teardown]    Close Browser
    
*** Keywords ***
Open Browser And Login
    Open Browser    ${URL}    chrome
    Maximize Browser Window
    Sleep    2s
    Wait Until Element Is Visible   xpath=//*[@id="form1"]    10s    
    Sleep    2s
    Input Text    xpath=//*[@id="TBO_UserID"]    ${USER_ID}    #enter user id
    Sleep    2s
    Input Text    xpath=//*[@id="TBO_Password"]    ${PASSWORD}    #enter password
    Sleep    2s
    Click Button    xpath=//*[@id="BTN_SUBMIT"]    #submit
    Sleep    2s

Accept TOS
    Click Button    xpath=//*[@id="ContentPlaceHolder3_BTN_ACCEPT"]    #Accept
    Sleep    5s

Select Menu Sales
    Click Element    xpath=//*[@id="menu-wrap"]/div/nav/ul/li[7]/a    #select operation
    Sleep    2s
    Click Element    xpath=//*[@id="menu-wrap"]/div/nav/ul/li[7]/ul/li[2]/a    #Select Sales Report
    Sleep    5s

Export Sales Report
    Click Element    xpath=//*[@id="ContentPlaceHolder1_radioDate"]
    Sleep    2s
    ${DATE}=    Get Current Date    UTC    result_format=%d/%m/%Y    increment=-1 day
    Sleep    2s
    Input Text    xpath=//*[@id="ContentPlaceHolder1_TBO_DateStart"]    ${DATE}
    Click Element    xpath=//*[@id="ContentPlaceHolder1_rdEXType_CSV"]
    Sleep    2s
    Click Button    xpath=//*[@id="ContentPlaceHolder1_btnExportExcelArtConsolidate"]
    Sleep    8s

Select Menu Stock
    Click Element    xpath=//*[@id="menu-wrap"]/div/nav/ul/li[9]/a    #select Export
    Sleep    2s
    Click Element    xpath=//*[@id="menu-wrap"]/div/nav/ul/li[9]/ul/li[2]/a    #Select Export Data
    Sleep    5s

Export Stock Report
    Click Element    xpath=//*[@id="tabs"]/ul/li[3]
    Sleep    2s
    Click Button    xpath=//*[@id="ContentPlaceHolder1_btnDownload_Inv"]
    Sleep    8s

Export Stock Report Pivot
    Click Element    xpath=//*[@id="ContentPlaceHolder1_chkPivot"]
    Sleep    2s
    Click Button    xpath=//*[@id="ContentPlaceHolder1_btnDownload_Inv"]
    Sleep    8s
