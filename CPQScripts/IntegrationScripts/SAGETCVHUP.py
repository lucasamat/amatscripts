# =========================================================================================================================================
#   __script_name : SAGETCVHUP.PY
#   __script_description : THIS SCRIPT IS USED TO CONNECTING HANA DB AND FETCHING DATA
#   __primary_author__ : BAJI
#   __create_date :
#   Ã‚Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

try:
	import clr
	import System.Net
	from System.Text.Encoding import UTF8
	from System import Convert
	import sys
	
	Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
	Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
	Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")

	LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME,Password,URL FROM SYCONF where EXTERNAL_TABLE_NAME='HANA_CONNECTION'")
	if LOGIN_CREDENTIALS is not None:

		Login_Username = str(LOGIN_CREDENTIALS.USER_NAME)
		Login_Password = str(LOGIN_CREDENTIALS.Password)
		authorization = Login_Username+":"+Login_Password
		binaryAuthorization = UTF8.GetBytes(authorization)
		authorization = Convert.ToBase64String(binaryAuthorization)
		authorization = "Basic " + authorization


		webclient = System.Net.WebClient()
		webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
		webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;

		#SACRVC

		Table_Name = 'SACRVC_INBOUND'

		TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name)+"'' ) BEGIN DROP TABLE "+str(Table_Name)+" END CREATE TABLE "+str(Table_Name)+" (MANDT VARCHAR(250) ,BUKRS VARCHAR(250) ,HKONT VARCHAR(250) ,ZUONR VARCHAR(250) ,GJAHR VARCHAR(250) ,BELNR VARCHAR(250) ,	BUZEI VARCHAR(250) ,BUDAT VARCHAR(250) ,ZAFTYPE VARCHAR(250) ,ZAFSP VARCHAR(250) ,KUNAG	VARCHAR(250) ,SPART VARCHAR(250) ,	WRBTR VARCHAR(250) ,WAERS VARCHAR(250) ,ZAFGBOOK VARCHAR(250) ,	ZAFKPU	VARCHAR(250) ,ZAFPLATFORM VARCHAR(250) ,ZAFTECHNO VARCHAR(250) ,ZAFWAFER VARCHAR(250) ,	ZAFTOOL_ID VARCHAR(250) ,ZAFSHIP_DATE VARCHAR(250) ,ZAFEXPIRY_DATE VARCHAR(250) ,	ZAF_UDATE VARCHAR(250) ,ZAF_UTIME VARCHAR(250),ZDOC_AMT VARCHAR(250) ,ZGBAL_AMT VARCHAR(250), ZDOC_AMT_KEY VARCHAR(250),ZGBAL_AMT_KEY VARCHAR(250) )'")	

		start =1
		end = 5000
		check_flag1 = 1
		while check_flag1 == 1:

			req_input = '{"query":"select * from (select *,row_number () over (order by hkont) as sno from zaf0470)a where sno>='+str(start)+' and sno<='+str(end)+'"}'

			response2 = webclient.UploadString(str(LOGIN_CREDENTIALS.URL), str(req_input))

			response = eval(response2)
			if str(type(response)) == "<type 'dict'>":
				response = [response]

			if len(response) > 0:			

				for record_dict in response:
					
					splt_info = """ ''{ZAFPLATFORM}'',''{ZAF_UDATE}'',''{ZAFTOOL_ID}'',''{ZAFWAFER}'',''{ZAFSHIP_DATE}'',''{GJAHR}'',''{ZAFKPU}'',''{ZAFTYPE}'',''{ZAF_UTIME}'',''{BUDAT}'',''{ZAFSP}'',''{ZAFTECHNO}'',''{BUZEI}'',''{ZAFEXPIRY_DATE}'',''{BELNR}'',''{BUKRS}'',''{ZAFGBOOK}'',''{SPART}'',''{ZUONR}'',''{KUNAG}'',''{MANDT}'',''{ZDOC_AMT}'',''{ZGBAL_AMT}'',''{ZDOC_AMT_KEY}'',''{ZGBAL_AMT_KEY}'' """.format(ZAFPLATFORM = record_dict['ZAFPLATFORM'],ZAF_UDATE = str(record_dict['ZAF_UDATE']),ZAFTOOL_ID = str(record_dict['ZAFTOOL_ID']),ZAFWAFER = record_dict['ZAFWAFER'],ZAFSHIP_DATE= str(record_dict['ZAFSHIP_DATE']),GJAHR = str(record_dict['GJAHR']),ZAFKPU = str(record_dict['ZAFKPU']),ZAFTYPE = str(record_dict['ZAFTYPE']),ZAF_UTIME = str(record_dict['ZAF_UTIME']),BUDAT = str(record_dict['BUDAT']),ZAFSP= record_dict['ZAFSP'],ZAFTECHNO = record_dict['ZAFTECHNO'],BUZEI = str(record_dict['BUZEI']),ZAFEXPIRY_DATE = str(record_dict['ZAFEXPIRY_DATE']),BELNR = str(record_dict['BELNR']),BUKRS= str(record_dict['BUKRS']),ZAFGBOOK = str(record_dict['ZAFGBOOK']),SPART = str(record_dict['SPART']),ZUONR = str(record_dict['ZUONR']),KUNAG = str(record_dict['KUNAG']),MANDT = str(record_dict['MANDT']), ZDOC_AMT= str(record_dict['ZDOC_AMT']),ZGBAL_AMT = str(record_dict['ZGBAL_AMT']),ZDOC_AMT_KEY = str(record_dict['ZDOC_AMT_KEY']),ZGBAL_AMT_KEY = str(record_dict['ZGBAL_AMT_KEY']) )

					Stagingquery = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " "+str(Table_Name)+" (HKONT, ZAFPLATFORM, ZAF_UDATE, ZAFTOOL_ID, ZAFWAFER, ZAFSHIP_DATE, GJAHR, ZAFKPU, ZAFTYPE, ZAF_UTIME, BUDAT, ZAFSP, ZAFTECHNO, BUZEI, ZAFEXPIRY_DATE,  BELNR, BUKRS, ZAFGBOOK, SPART, ZUONR, KUNAG, MANDT,ZDOC_AMT, ZGBAL_AMT, ZDOC_AMT_KEY ,ZGBAL_AMT_KEY)  select  N''"+str(record_dict['HKONT'])+ "'',"+str(splt_info)+ "  ' ")

				start = start + 5000
				end = end + 5000

			else:
				check_flag1 = 0


		#SACVNT

		Table_Name = 'SACVNT_INBOUND' 

		TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name)+"'' ) BEGIN DROP TABLE "+str(Table_Name)+" END CREATE TABLE "+str(Table_Name)+" (HKONT VARCHAR(250), ZAF_UDATE VARCHAR(250), MANDT VARCHAR(250), ZAF_UTIME VARCHAR(250), ZAFNOTE VARCHAR(250), ZUONR VARCHAR(250), GJAHR VARCHAR(250), BUZEI VARCHAR(250), ZAFNOTE_ID VARCHAR(250), BELNR VARCHAR(250), BUKRS VARCHAR(250))'")	


		start =1
		end = 5000
		check_flag2 = 1
		while check_flag2 == 1:
			req_input = '{"query":"select * from (select *,row_number () over (order by hkont) as sno from zaf0471)a where sno>='+str(start)+' and sno<='+str(end)+'"}'

			response2 = webclient.UploadString(str(LOGIN_CREDENTIALS.URL), str(req_input))

			response = eval(response2)
			if str(type(response)) == "<type 'dict'>":
				response = [response]

			if len(response) > 0:			

				for record_dict in response:

					Stagingquery = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " "+str(Table_Name)+" (HKONT, ZAF_UDATE, MANDT, ZAF_UTIME, ZAFNOTE, ZUONR, GJAHR, BUZEI, ZAFNOTE_ID, BELNR, BUKRS)  select  N''"+str(record_dict['HKONT'])+ "'',''"+str(record_dict['ZAF_UDATE'])+ "'',''"+str(record_dict['MANDT'])+ "'',''"+str(record_dict['ZAF_UTIME'])+ "'',''"+record_dict['ZAFNOTE']+ "'',''"+str(record_dict['ZUONR'])+ "'',''"+str(record_dict['GJAHR'])+ "'',''"+str(record_dict['BUZEI'])+ "'',''"+str(record_dict['ZAFNOTE_ID'])+ "'',''"+str(record_dict['BELNR'])+ "'',''"+str(record_dict['BUKRS'])+ "'' ' ")

				start = start + 5000
				end = end + 5000

			else:

				check_flag2 = 0
		
		
		#SACRVC Insert Query  
		
		primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SACRVC_INBOUND SET ZAFSHIP_DATE = null FROM SACRVC_INBOUND(NOLOCK) where ZAFSHIP_DATE = ''00000000''    '") 

		primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SACRVC_INBOUND SET ZAF_UDATE = null FROM SACRVC_INBOUND(NOLOCK) where ZAF_UDATE = ''00000000''    '") 
		
		primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SACRVC_INBOUND SET BUDAT = null FROM SACRVC_INBOUND(NOLOCK) where BUDAT = ''00000000''    '") 
		
		primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SACRVC_INBOUND SET ZAFEXPIRY_DATE = null FROM SACRVC_INBOUND(NOLOCK) where ZAFEXPIRY_DATE = ''00000000''    '") 
		
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter.QUERY_CRITERIA_1)
			+ " SACRVC (SPART,ZAF_UTIME ,HKONT, ZAFPLATFORM, ZAFTOOL_ID, ZAFWAFER, GJAHR, ZAFKPU, ZAFTYPE, ZAFSP, ZAFTECHNO, BUZEI,   BELNR, BUKRS, ZAFGBOOK,ZUONR, KUNAG,ZAF_UDATE,ZAFSHIP_DATE ,BUDAT,ZAFEXPIRY_DATE,MANDT,ZDOC_AMT,ZGBAL_AMT ,ZDOC_AMT_KEY,ZGBAL_AMT_KEY,CREDITVOUCHER_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)SELECT SUB_SACRVC.*, CONVERT(VARCHAR(4000),NEWID()),''"+ str(User.UserName)+ "'',GETDATE() FROM (SELECT DISTINCT SPART,''19000101 ''+CONCAT(SUBSTRING(ZAF_UTIME, 1, 2), '':'', SUBSTRING(ZAF_UTIME, 3, 2), '':'', SUBSTRING(ZAF_UTIME, 5, 2)) AS ZAF_UTIME ,HKONT, ZAFPLATFORM,  ZAFTOOL_ID, ZAFWAFER,  CONVERT(VARCHAR,GJAHR) AS GJAHR , ZAFKPU, ZAFTYPE, ZAFSP, ZAFTECHNO, CONVERT(VARCHAR,BUZEI) AS BUZEI , BELNR, BUKRS, ZAFGBOOK, ZUONR, KUNAG, convert(date,ZAF_UDATE) as ZAF_UDATE,convert(date,ZAFSHIP_DATE) as ZAFSHIP_DATE,convert(date,BUDAT) as BUDAT,convert(date,ZAFEXPIRY_DATE) as ZAFEXPIRY_DATE,MANDT,ZDOC_AMT,ZGBAL_AMT ,ZDOC_AMT_KEY,ZGBAL_AMT_KEY FROM SACRVC_INBOUND(NOLOCK) )SUB_SACRVC LEFT JOIN SACRVC(NOLOCK)  ON SUB_SACRVC.BUKRS = SACRVC.BUKRS AND SUB_SACRVC.HKONT = SACRVC.HKONT AND SUB_SACRVC.BELNR = SACRVC.BELNR AND SUB_SACRVC.ZUONR = SACRVC.ZUONR AND SUB_SACRVC.GJAHR = SACRVC.GJAHR AND SUB_SACRVC.BUZEI = SACRVC.BUZEI AND SUB_SACRVC.MANDT = SACRVC.MANDT WHERE SACRVC.BUKRS IS NULL '"	)
        
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ " SACRVC SET ZAFEXPIRY_DATE = convert(date,SACRVC_INBOUND.ZAFEXPIRY_DATE)   FROM SACRVC_INBOUND (NOLOCK) JOIN SACRVC(NOLOCK)  ON SACRVC_INBOUND.BUKRS = SACRVC.BUKRS AND SACRVC_INBOUND.HKONT = SACRVC.HKONT AND SACRVC_INBOUND.BELNR = SACRVC.BELNR AND SACRVC_INBOUND.ZUONR = SACRVC.ZUONR AND SACRVC_INBOUND.GJAHR = SACRVC.GJAHR AND SACRVC_INBOUND.BUZEI = SACRVC.BUZEI AND SACRVC_INBOUND.MANDT = SACRVC.MANDT '"	)
		
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ " SACRVC SET CRTAPP_INGL_CURR = CREDIT_APPLIED_INGL_CURR FROM SACRVC (NOLOCK) JOIN (SELECT CREDITVOUCHER_RECORD_ID,SUM(CREDIT_APPLIED_INGL_CURR) AS CREDIT_APPLIED_INGL_CURR FROM SAQRCV (NOLOCK) GROUP BY CREDITVOUCHER_RECORD_ID)SAQRCV ON SACRVC.CREDITVOUCHER_RECORD_ID = SAQRCV.CREDITVOUCHER_RECORD_ID '"	)
		
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ " SACRVC SET UNBL_INGL_CURR = ISNULL(ZGBAL_AMT,0) - ISNULL(CRTAPP_INGL_CURR,0) FROM SACRVC (NOLOCK)  '"	)
			
		#SACVNT Insert Query		
		
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter.QUERY_CRITERIA_1)
			+ " SACVNT (HKONT, ZAF_UDATE, MANDT, ZAF_UTIME, ZAFNOTE, ZUONR, GJAHR, BUZEI, ZAFNOTE_ID, BELNR, BUKRS ,CRDVCH_NOTE_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)SELECT SUB_SACVNT.*,CONVERT(VARCHAR(4000),NEWID()),''"+ str(User.UserName)+ "'',GETDATE() FROM (SELECT DISTINCT HKONT, ZAF_UDATE, MANDT, ZAF_UTIME, ZAFNOTE, ZUONR, GJAHR, BUZEI, ZAFNOTE_ID, BELNR, BUKRS FROM SACVNT_INBOUND(NOLOCK))SUB_SACVNT LEFT JOIN SACVNT(NOLOCK)  ON SUB_SACVNT.BUKRS = SACVNT.BUKRS AND SUB_SACVNT.HKONT = SACVNT.HKONT AND SUB_SACVNT.BELNR = SACVNT.BELNR AND SUB_SACVNT.ZUONR = SACVNT.ZUONR AND SUB_SACVNT.GJAHR = SACVNT.GJAHR AND SUB_SACVNT.BUZEI = SACVNT.BUZEI AND SUB_SACVNT.MANDT = SACVNT.MANDT WHERE SACVNT.BUKRS IS NULL '"	)
		
		
		
		Tbl = 'SACRVC_INBOUND'
		TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Tbl)+"'' ) BEGIN DROP TABLE "+str(Tbl)+" END'")

		Tbl = 'SACVNT_INBOUND'
		TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Tbl)+"'' ) BEGIN DROP TABLE "+str(Tbl)+" END'")

		ApiResponse = ApiResponseFactory.JsonResponse(
			{
				"Response": [
					{
						"Status": "200",
						"Message": "Data Successfully Uploaded ."
					}
				]
			}
		)

except:     
	Log.Info("SAGETCVHUP ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("SAGETCVHUP ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})