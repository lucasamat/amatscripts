# =========================================================================================================================================
#   __script_name : SAPOSTCLMA.PY
#   __script_description : THIS SCRIPT IS USED FOR CPQ TO CLM INTEGRATIONS
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
from System.Net import HttpWebRequest, NetworkCredential
from System.Net import *
from System.Net import CookieContainer
from System.Net import Cookie
from System.Net import WebRequest
from System.Net import HttpWebResponse

input_data = [str(param_result.Value) for param_result in Param.CPQ_Columns]	
input_data = [input_data]
QUOTE_ID = ''
try:
	for crmifno in input_data:	
		Quote_Id = crmifno[0]
		Revision_Id = crmifno[-1]

		CLMQuery = SqlHelper.GetList("SELECT DISTINCT top 1 CASE WHEN SAQTRV.CLM_TEMPLATE_NAME ='ICMPreventiveMaintenanceSOW' THEN 'Preventive Maintenance Service SOW' else '' end as PSOW, CASE WHEN SAQTRV.CLM_TEMPLATE_NAME ='ICMStatementofWork' THEN (SELECT TOP 1 CASE WHEN SERVICE_ID='Z0091' THEN 'Managed Service SOW' WHEN SERVICE_ID='Z0092' THEN 'Standard Service SOW'  else '' end FROM SAQTSV WHERE QUOTE_ID = '"+str(Quote_Id)+"' AND QTEREV_ID = '"+str(Revision_Id)+"' ORDER BY CPQTABLEENTRYID) ELSE '' END AS SSOW, CASE WHEN SAQTRV.CLM_TEMPLATE_NAME ='ICMComprehensiveServiceAgreement' THEN (SELECT TOP 1 CASE WHEN SERVICE_ID='Z0091' THEN 'Managed Service Agreement (English)' WHEN SERVICE_ID in ('Z0108') THEN 'Forecasted Parts Management Agreement without on-site replenishment (English)' WHEN SERVICE_ID='Z0092' THEN 'Standard Service Agreement (English)' WHEN SERVICE_ID='Z0010' THEN 'Total Kit Management Service Agreement (English)' WHEN SERVICE_ID='Z0110' THEN 'Total Kit Management Agreement' WHEN SERVICE_ID='Z0108' THEN 'Forecasted Parts Management Agreement with on-site replenishment (English)'  else '' end FROM SAQTSV WHERE QUOTE_ID = '"+str(Quote_Id)+"' AND QTEREV_ID = '"+str(Revision_Id)+"' ORDER BY CPQTABLEENTRYID) ELSE '' END  AS CSOW,ISNULL(SAQTRV.CLM_TEMPLATE_NAME,'') AS StatementOfWorkType,ISNULL(CASE WHEN SAQTRV.HLV_ORG_BUN='AGS - SSC' THEN '004' ELSE NULL END,'') AS HighLevelOrg,ISNULL((SELECT REPLICATE('0',(10-LEN(ACCOUNT_ID)))+ACCOUNT_ID FROM SAQTMT(NOLOCK) WHERE QUOTE_ID = '"+str(Quote_Id)+"' AND QTEREV_ID = '"+str(Revision_Id)+"'  ),'') AS SAPOtherPartyID,ISNULL(SAQTRV.COMPANY_NAME,'') AS AppliedPartyName,ISNULL((SELECT OWNER_NAME FROM SAQTMT(NOLOCK) WHERE QUOTE_ID = '"+str(Quote_Id)+"' AND QTEREV_ID = '"+str(Revision_Id)+"'  ),'') AS CPQContractInitiator,ISNULL(SAQTRV.APPLIED_EMAIL,'') AS  AppliedSignatory1Email,ISNULL(SAQTRV.APPLIED_TITLE,'') AS AppliedSignatoryTitle,ISNULL(SAQTRV.EXTERNAL_EMAIL,'') AS ExternalSignatory1Email,ISNULL(SAQTRV.EXTERNAL_TITLE,'') AS OtherPartySignatoryTitle,ISNULL(CONVERT(VARCHAR,SAQTRV.NET_VALUE_INGL_CURR),'0') AS ExpectedValue,ISNULL(SAQTRV.GLOBAL_CURRENCY,'') AS ExpectedValueCurrency,ISNULL(SAQTRV.CUSTOMER_NOTES,'') AS Comments,ISNULL(CONVERT(VARCHAR,SAQTRV.CONTRACT_VALID_TO),'') AS ContractExpirationDate,SAQTRV.QUOTE_ID +'-'+CONVERT(VARCHAR,SAQTRV.QTEREV_ID) AS CorrelationID,'CPQ Quote#'+SAQTRV.QUOTE_ID +'-'+CONVERT(VARCHAR,SAQTRV.QTEREV_ID) AS AgreementName,ISNULL(OPPORTUNITY_ID,'') AS OpportunityNumber,CONVERT(VARCHAR(11),CONTRACT_VALID_FROM,121) AS ContractEffectiveDate,ISNULL((SELECT TOP 1 CONVERT(VARCHAR(300),MEMBER_NAME) FROM SAQDLT(NOLOCK)A WHERE QUOTE_ID = '"+str(Quote_Id)+"' AND C4C_PARTNERFUNCTION_ID = 'Sales Employee' AND QTEREV_ID = '"+str(Revision_Id)+"' AND ISNULL([PRIMARY],'FALSE')='TRUE' ),'') as SalesPerson, ISNULL((SELECT TOP 1 CONVERT(VARCHAR(300),MEMBER_NAME) FROM SAQDLT(NOLOCK)A WHERE QUOTE_ID = '"+str(Quote_Id)+"' AND C4C_PARTNERFUNCTION_ID = 'SALES MANAGER' AND QTEREV_ID = '"+str(Revision_Id)+"' ),'') as BDManager, ISNULL((SELECT TOP 1 CONVERT(VARCHAR,EMAIL) FROM SAQDLT(NOLOCK)A WHERE QUOTE_ID = '"+str(Quote_Id)+"' AND C4C_PARTNERFUNCTION_ID = 'LEGAL PERSON' AND QTEREV_ID = '"+str(Revision_Id)+"' AND ISNULL([PRIMARY],'FALSE')='TRUE' ),'') as LegalPerson  FROM SAQTRV(NOLOCK) JOIN SAOPQT (NOLOCK) on SAQTRV.QUOTE_ID = SAOPQT.QUOTE_ID WHERE SAQTRV.QTEREV_ID = '"+str(Revision_Id)+"' AND SAQTRV.QUOTE_ID = '"+str(Quote_Id)+"' AND ISNULL(SAQTRV.CLM_AGREEMENT_NUM,'')='' ")

	dt={}  

	for data in CLMQuery:
	
		dt['ContractTypeName'] = data.StatementOfWorkType
		dt['StatementOfWorkType'] = data.SSOW
		dt['ComprehensiveServiceAgreementType'] = data.CSOW
		dt['PreventiveMaintenanceSOWtype'] = data.PSOW
		dt['CorrelationID'] = data.CorrelationID
		dt['HighLevelOrg-BUID'] = data.HighLevelOrg	
		dt['AppliedPartyName'] = data.AppliedPartyName
		dt['SAPOtherPartyID'] = data.SAPOtherPartyID
		dt['CPQContractInitiator'] = data.CPQContractInitiator
		dt['QuotationNumber'] = Quote_Id
		dt['QuoteRevision'] = Revision_Id
		dt['OpportunityNumber'] = data.OpportunityNumber
		dt['AppliedSignatory1Email'] = data.AppliedSignatory1Email
		dt['AppliedSignatoryTitle'] = data.AppliedSignatoryTitle
		dt['ExternalSignatory1Email'] = data.ExternalSignatory1Email
		dt['OtherPartySignatoryTitle'] = data.OtherPartySignatoryTitle
		dt['ExpectedValue(USDonly)'] = data.ExpectedValue
		dt['ExpectedValueCurrency'] = data.ExpectedValueCurrency	
		dt['AgreementName'] = data.AgreementName
		dt['Comments'] = data.Comments
		dt['ContractExpirationDate'] = data.ContractExpirationDate
		dt['ContractEffectiveDate'] = data.ContractEffectiveDate
		dt['SalesPerson'] = data.SalesPerson
		dt['BDManager'] = data.BDManager
		dt['LegalPerson'] = data.LegalPerson #'clmadmin_AppliedMaterials@waadicm.onmicrosoft.com'
		
	Timestamp = SqlHelper.GetFirst("select Getdate() as date")
	result = {

	  "EventType": "Agreement",
	  "Action": "Create",
	  "TimeStamp": str(Timestamp.date),
	  "Data":dt}
	Result = result
	#Log.Info("22222 result --->"+str(result))
	
	LOGIN_CRE = SqlHelper.GetFirst("SELECT  URL FROM SYCONF where EXTERNAL_TABLE_NAME ='CPQ_TO_CLM'")
	Oauth_info = SqlHelper.GetFirst("SELECT  DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME ='OAUTH'")

	requestdata =Oauth_info.DOMAIN
	webclient = System.Net.WebClient()
	webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
	response = webclient.UploadString(Oauth_info.URL,str(requestdata))

	response = eval(response)
	access_token = response['access_token']

	authorization = "Bearer " + access_token
	webclient = System.Net.WebClient()
	webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
	webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;
	webclient.Headers.Add("Environment-Identifier", "T")
	clm_response = webclient.UploadString(str(LOGIN_CRE.URL),str(result))	
	Log.Info("28/12 clm_response --->"+str(clm_response))
		
	SYINPL_tableInfoData = SqlHelper.GetTable("SYINPL")
	SYINPL_DT = {}
	SYINPL_DT["INTEGRATION_NAME"] = 'CPQ to CLM Interface'
	SYINPL_DT["INTEGRATION_PAYLOAD"] = str(result)
	SYINPL_tableInfoData.AddRow(SYINPL_DT)
	sqlInfo = SqlHelper.Upsert(SYINPL_tableInfoData)
	
except:
    Log.Info("SAPOSTCLMA ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("SAPOSTCLMA ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))