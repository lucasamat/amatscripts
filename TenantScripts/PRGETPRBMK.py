# =========================================================================================================================================
#   __script_name : PRGETPRBMK.PY
#   __script_description : THIS SCRIPT IS USED TO CONNECTING HANA DB ,FETCHING PRICEBENCHMARK DATA AND STORED IN PRPRBM.
#   __primary_author__ : BAJI
#   __create_date :02/03/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

try:
    import clr
    import System.Net
    from System.Text.Encoding import UTF8
    from System import Convert
    import sys
    
    Log.Info("PRGETPRBMK Started")
    Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
    Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
    Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")

    LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME='HANA_CONNECTION'")	
    
    OAUTH_CREDENTIALS = SqlHelper.GetFirst("SELECT DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME='HANA_OAUTH'")
    
    if LOGIN_CREDENTIALS is not None:

        oauthURL = str(OAUTH_CREDENTIALS.URL)
        requestdata = str(OAUTH_CREDENTIALS.DOMAIN)
        webclient = System.Net.WebClient()
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
        response = webclient.UploadString(str(oauthURL),str(requestdata))
        response = eval(response)       
              
        
        
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response['access_token'])
        
        #staging_tableInfo = SqlHelper.GetTable("PRPRBM_INBOUND")
        PRPRBM_tableInfoData = SqlHelper.GetTable("PRPRBM")

        #PRPRBM
        start =1
        end = 500
        check_flag = 1
        start_flag = 1
        while check_flag == 1:

            req_input = '{"query":"select * from (select  *,row_number () over (order by GEN_ROW_NUM) as sno from cds_pl_pricebenchmark_vw  )a where sno>='+str(start)+' and sno<='+str(end)+'"}'

            response2 = webclient.UploadString(str(LOGIN_CREDENTIALS.URL), str(req_input)) 
            
            start = start + 500
            end = end + 500
                
            response = eval(response2.replace("'","@@@"))
            if str(type(response)) == "<type 'dict'>":
                response = [response]

            if len(response) > 0:			

                for record_dict in response:						
                            
                    str_joint ="""''{TOTALSTDCOSPARTS}'',''{CUSTMINFAB}'',''{CONTRACT_END_FISCAL_MONTH}'',''{TOTALNETREVENUE}'',''{PROCESSPARTSKITSCLEANRECY}'',''{GEN_ROW_NUM}'',''{TOTAL_COST}'',''{SERVICE_PRODUCT_NAME}'',''{CUSTMINANNUAL_BKNG_PRICE}'',''{CONTRACT_END_DATE}'',''{TECHFORCE}'',''{CONTRACT_BOOKING_FISCAL_QURT}'',''{FABVANTAGE}'',''{CONTRACT_BOOKING_DATE}'',''{ANNUALIZED_BOOKING_PRICE}'',''{CONTRACT_END_FISCAL_YEAR}'',''{SALES_DOCUMENT_ITEM}'',''{FNCNLLOCDESC}'',''{GLOBALMAXCNTRENDDATE}'',''{SWAPKITSAMATPROVIDED}'',''{PROCESSAPPENGINEERING}'',''{TOTALGROSSMARGINDLR}'',''{CMLABOR}'',''{CUSTMAXANNUAL_BKNG_PRICE}'',''{CUSTMAXCNTRENDDATE}'',''{TOTALGROSSREVENUE}'',''{CONTRACT_CONTRACTCOVERAGE}'',''{CONTRACT}'',''{PLATFORM}'',''{FNCNLLOC}'',''{TOTALSTDCOSLABOR}'',''{RESPONSETIME}'',''{GLBLMAXANNUAL_BKNG_PRICE}'',''{GLBLMINANNUAL_BKNG_PRICE}'',''{TOTALSTDCOST}'',''{BOOKING_PER_TOOL}'',''{EQUIPMENT_NUMBER}'',''{CONSUMABLE}'',''{NODE}'',''{TOTALNEWORDERS}''""".format(TOTALSTDCOSPARTS = record_dict['TOTALSTDCOSPARTS'], CUSTMINFAB = record_dict['CUSTMINFAB'], CONTRACT_END_FISCAL_MONTH = record_dict['CONTRACT_END_FISCAL_MONTH'], TOTALNETREVENUE = record_dict['TOTALNETREVENUE'], PROCESSPARTSKITSCLEANRECY=record_dict['PROCESSPARTSKITSCLEANRECY'], GEN_ROW_NUM = record_dict['GEN_ROW_NUM'], TOTAL_COST = record_dict['TOTAL_COST'], SERVICE_PRODUCT_NAME = record_dict['SERVICE_PRODUCT_NAME'], CUSTMINANNUAL_BKNG_PRICE = record_dict['CUSTMINANNUAL_BKNG_PRICE'], CONTRACT_END_DATE = record_dict['CONTRACT_END_DATE'], TECHFORCE = record_dict['TECHFORCE'], CONTRACT_BOOKING_FISCAL_QURT = record_dict['CONTRACT_BOOKING_FISCAL_QURT'], FABVANTAGE = record_dict['FABVANTAGE'], CONTRACT_BOOKING_DATE = record_dict['CONTRACT_BOOKING_DATE'], ANNUALIZED_BOOKING_PRICE = record_dict['ANNUALIZED_BOOKING_PRICE'], CONTRACT_END_FISCAL_YEAR = record_dict['CONTRACT_END_FISCAL_YEAR'], SALES_DOCUMENT_ITEM =record_dict['SALES_DOCUMENT_ITEM'], FNCNLLOCDESC = record_dict['FNCNLLOCDESC'], GLOBALMAXCNTRENDDATE = record_dict['GLOBALMAXCNTRENDDATE'], SWAPKITSAMATPROVIDED = record_dict['SWAPKITSAMATPROVIDED'], PROCESSAPPENGINEERING = record_dict['PROCESSAPPENGINEERING'], TOTALGROSSMARGINDLR = record_dict['TOTALGROSSMARGINDLR'], CMLABOR = record_dict['CMLABOR'], CUSTMAXANNUAL_BKNG_PRICE = record_dict['CUSTMAXANNUAL_BKNG_PRICE'], CUSTMAXCNTRENDDATE = record_dict['CUSTMAXCNTRENDDATE'], TOTALGROSSREVENUE = record_dict['TOTALGROSSREVENUE'], CONTRACT_CONTRACTCOVERAGE = record_dict['CONTRACT_CONTRACTCOVERAGE'], CONTRACT = record_dict['CONTRACT'], PLATFORM = record_dict['PLATFORM'], FNCNLLOC = record_dict['FNCNLLOC'], TOTALSTDCOSLABOR = record_dict['TOTALSTDCOSLABOR'], RESPONSETIME = record_dict['RESPONSETIME'], GLBLMAXANNUAL_BKNG_PRICE = record_dict['GLBLMAXANNUAL_BKNG_PRICE'], GLBLMINANNUAL_BKNG_PRICE = record_dict['GLBLMINANNUAL_BKNG_PRICE'], TOTALSTDCOST = record_dict['TOTALSTDCOST'], BOOKING_PER_TOOL = record_dict['BOOKING_PER_TOOL'], EQUIPMENT_NUMBER = record_dict['EQUIPMENT_NUMBER'], CONSUMABLE =record_dict['CONSUMABLE'], NODE = record_dict['NODE'], TOTALNEWORDERS = record_dict['TOTALNEWORDERS'])
                
                
                    str_joint1 = """,''{BLUEBOOK}'',''{SERVICE_PRODUCT_DESC}'',''{DAYSCOUNT}'',''{WAFERSIZE}'',''{SRVCTECHVITA}'',''{ONCALLOUTSIDECONTRCOVERAGE}'',''{TOTALNETBOOKINGS}'',''{STDGROSSMARGINDLR}'',''{CNTRDESC}'',''{BLACKBOOK}'',''{GLOBALMINCUSTSHRTNAME}'',''{CONTRACT_END_FISCAL_QUARTER}'',''{CONTRACT_START_FISCAL_MONTH}'',''{SRVCTECHPDCSERVER}'',''{CONTRACT_START_FISCAL_YEAR}'',''{PMLABOR}'',''{CONTRACT_START_FISCAL_QUARTER}'',''{RENEWALFLAG}'',''{TOOLCONFG}'',''{CUSTMINCNTRENDDATE}'',''{GLOBALMAXFAB}'',''{STDCOSLABOR}'',''{GLOBALMAXCUSTSHRTNAME}'',''{CUSTSHRTNAMEMKTG}'',''{STD_COS_PO_ITEM}'',''{SIMILARTOOL}'',''{DIFF_MONTHS}'',''{STDCOSPARTS}'',''{CUSTNAME}'',''{RFPCONTRACTMATCH}'',''{GLOBALMINFAB}'',''{GREENBOOK}'',''{CONTRACT_START_DATE}'',''{RFPNUM}'',''{NONCONSUMABLE}'',''{SERIAL_NUMBER}'',''{CUSTMAXFAB}'',''{RFPSYSID}'',''{GLOBALMINCNTRENDDATE}'',''{WETCLEANSLABOR}'',''{CONTRACT_BOOKING_FISCAL_YEAR}''""".format( BLUEBOOK = record_dict['BLUEBOOK'], SERVICE_PRODUCT_DESC = record_dict['SERVICE_PRODUCT_DESC'], DAYSCOUNT =record_dict['DAYSCOUNT'], WAFERSIZE = record_dict['WAFERSIZE'], SRVCTECHVITA = record_dict['SRVCTECHVITA'], ONCALLOUTSIDECONTRCOVERAGE = record_dict['ONCALLOUTSIDECONTRCOVERAGE'], TOTALNETBOOKINGS = record_dict['TOTALNETBOOKINGS'], STDGROSSMARGINDLR = record_dict['STDGROSSMARGINDLR'], CNTRDESC = record_dict['CNTRDESC'], BLACKBOOK = record_dict['BLACKBOOK'], GLOBALMINCUSTSHRTNAME = record_dict['GLOBALMINCUSTSHRTNAME'], CONTRACT_END_FISCAL_QUARTER = record_dict['CONTRACT_END_FISCAL_QUARTER'], CONTRACT_START_FISCAL_MONTH = record_dict['CONTRACT_START_FISCAL_MONTH'], SRVCTECHPDCSERVER = record_dict['SRVCTECHPDCSERVER'], CONTRACT_START_FISCAL_YEAR = record_dict['CONTRACT_START_FISCAL_YEAR'], PMLABOR =record_dict['PMLABOR'], CONTRACT_START_FISCAL_QUARTER = record_dict['CONTRACT_START_FISCAL_QUARTER'], RENEWALFLAG = record_dict['RENEWALFLAG'], TOOLCONFG = record_dict['TOOLCONFG'], CUSTMINCNTRENDDATE =record_dict['CUSTMINCNTRENDDATE'], GLOBALMAXFAB =record_dict['GLOBALMAXFAB'], STDCOSLABOR = record_dict['STDCOSLABOR'], GLOBALMAXCUSTSHRTNAME =record_dict['GLOBALMAXCUSTSHRTNAME'], CUSTSHRTNAMEMKTG =record_dict['CUSTSHRTNAMEMKTG'], STD_COS_PO_ITEM =record_dict['STD_COS_PO_ITEM'], SIMILARTOOL = record_dict['SIMILARTOOL'], DIFF_MONTHS =record_dict['DIFF_MONTHS'], STDCOSPARTS =record_dict['STDCOSPARTS'], CUSTNAME =record_dict['CUSTNAME'], RFPCONTRACTMATCH =record_dict['RFPCONTRACTMATCH'], GLOBALMINFAB =record_dict['GLOBALMINFAB'], GREENBOOK =record_dict['GREENBOOK'], CONTRACT_START_DATE =record_dict['CONTRACT_START_DATE'], RFPNUM = record_dict['RFPNUM'], NONCONSUMABLE = record_dict['NONCONSUMABLE'], SERIAL_NUMBER =record_dict['SERIAL_NUMBER'], CUSTMAXFAB = record_dict['CUSTMAXFAB'], RFPSYSID =record_dict['RFPSYSID'], GLOBALMINCNTRENDDATE = record_dict['GLOBALMINCNTRENDDATE'], WETCLEANSLABOR = record_dict['WETCLEANSLABOR'], CONTRACT_BOOKING_FISCAL_YEAR =record_dict['CONTRACT_BOOKING_FISCAL_YEAR'])
    
                    primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " PRPRBM_INBOUND (TOTALSTDCOSPARTS, CUSTMINFAB, CONTRACT_END_FISCAL_MONTH, TOTALNETREVENUE, PROCESSPARTSKITSCLEANRECY, GEN_ROW_NUM, TOTAL_COST, SERVICE_PRODUCT_NAME, CUSTMINANNUAL_BKNG_PRICE, CONTRACT_END_DATE, TECHFORCE, CONTRACT_BOOKING_FISCAL_QURT, FABVANTAGE, CONTRACT_BOOKING_DATE, ANNUALIZED_BOOKING_PRICE, CONTRACT_END_FISCAL_YEAR, SALES_DOCUMENT_ITEM, FNCNLLOCDESC, GLOBALMAXCNTRENDDATE, SWAPKITSAMATPROVIDED, PROCESSAPPENGINEERING, TOTALGROSSMARGINDLR, CMLABOR, CUSTMAXANNUAL_BKNG_PRICE, CUSTMAXCNTRENDDATE, TOTALGROSSREVENUE, CONTRACT_CONTRACTCOVERAGE, CONTRACT, PLATFORM, FNCNLLOC, TOTALSTDCOSLABOR, RESPONSETIME, GLBLMAXANNUAL_BKNG_PRICE, GLBLMINANNUAL_BKNG_PRICE, TOTALSTDCOST, BOOKING_PER_TOOL, EQUIPMENT_NUMBER, CONSUMABLE, NODE, TOTALNEWORDERS, BLUEBOOK, SERVICE_PRODUCT_DESC, DAYSCOUNT, WAFERSIZE, SRVCTECHVITA, ONCALLOUTSIDECONTRCOVERAGE, TOTALNETBOOKINGS, STDGROSSMARGINDLR, CNTRDESC, BLACKBOOK, GLOBALMINCUSTSHRTNAME, CONTRACT_END_FISCAL_QUARTER, CONTRACT_START_FISCAL_MONTH, SRVCTECHPDCSERVER, CONTRACT_START_FISCAL_YEAR, PMLABOR, CONTRACT_START_FISCAL_QUARTER, RENEWALFLAG, TOOLCONFG, CUSTMINCNTRENDDATE, GLOBALMAXFAB, STDCOSLABOR, GLOBALMAXCUSTSHRTNAME, CUSTSHRTNAMEMKTG, STD_COS_PO_ITEM, SIMILARTOOL, DIFF_MONTHS, STDCOSPARTS, CUSTNAME, RFPCONTRACTMATCH, GLOBALMINFAB, GREENBOOK, CONTRACT_START_DATE, RFPNUM, NONCONSUMABLE, SERIAL_NUMBER, CUSTMAXFAB, RFPSYSID, GLOBALMINCNTRENDDATE, WETCLEANSLABOR, CONTRACT_BOOKING_FISCAL_YEAR)  select  "+str_joint+ ""+str_joint1+ " ' ")					

                

            else:
                check_flag = 0	
        
        
        s = SqlHelper.GetFirst("sp_executesql @T=N'update prprbm_inbound set TOTALSTDCOST= NULL where isnull(TOTALSTDCOST,'''')=''''  '")
        s = SqlHelper.GetFirst("sp_executesql @T=N'update prprbm_inbound set TOTALNETREVENUE= NULL where isnull(TOTALNETREVENUE,'''')=''''  '")
        s = SqlHelper.GetFirst("sp_executesql @T=N'update prprbm_inbound set TOTALGROSSREVENUE= NULL where isnull(TOTALGROSSREVENUE,'''')=''''  '")
        s = SqlHelper.GetFirst("sp_executesql @T=N'update prprbm_inbound set TOTAL_COST= NULL where isnull(TOTAL_COST,'''')=''''  '")
        s = SqlHelper.GetFirst("sp_executesql @T=N'update prprbm_inbound set GLBLMINANNUAL_BKNG_PRICE= NULL where isnull(GLBLMINANNUAL_BKNG_PRICE,'''')=''''  '")
        s = SqlHelper.GetFirst("sp_executesql @T=N'update prprbm_inbound set GLBLMAXANNUAL_BKNG_PRICE= NULL where isnull(GLBLMAXANNUAL_BKNG_PRICE,'''')=''''  '")
        s = SqlHelper.GetFirst("sp_executesql @T=N'update prprbm_inbound set CUSTMINANNUAL_BKNG_PRICE= NULL where isnull(CUSTMINANNUAL_BKNG_PRICE,'''')=''''  '")
        s = SqlHelper.GetFirst("sp_executesql @T=N'update prprbm_inbound set CUSTMAXANNUAL_BKNG_PRICE= NULL where isnull(CUSTMAXANNUAL_BKNG_PRICE,'''')=''''  '")
        s = SqlHelper.GetFirst("sp_executesql @T=N'update prprbm_inbound set ANNUALIZED_BOOKING_PRICE= NULL where isnull(ANNUALIZED_BOOKING_PRICE,'''')=''''  '")
        
        s = SqlHelper.GetFirst("sp_executesql @T=N'INSERT PRPRBM(ANNUALIZED_BOOKING_PRICE,	BLACKBOOK,	BLUEBOOK,	BOOKING_PER_TOOL,	CMLABOR,	CONSUMABLE,	CONTRACT_BOOKING_DATE,	CONTRACT_BOOKING_FISCAL_QURT,	CONTRACT_BOOKING_FISCAL_YEAR,	CONTRACT_CONTRACTCOVERAGE,	CNTRDESC,	CONTRACT_END_DATE,	CONTRACT_END_FISCAL_MONTH,	CONTRACT_END_FISCAL_QUARTER,	CONTRACT_END_FISCAL_YEAR,	CONTRACT,	CONTRACT_START_DATE,	CONTRACT_START_FISCAL_MONTH,	CONTRACT_START_FISCAL_QUARTER,	CONTRACT_START_FISCAL_YEAR,	CUSTMAXANNUAL_BKNG_PRICE,	CUSTMAXCNTRENDDATE,	CUSTMAXFAB,	CUSTMINANNUAL_BKNG_PRICE,	CUSTMINCNTRENDDATE,	CUSTMINFAB,	CUSTNAME,	CUSTSHRTNAMEMKTG,	DAYSCOUNT,	NODE,	DIFF_MONTHS,	EQUIPMENT_NUMBER,	FNCNLLOC,	FNCNLLOCDESC,	FABVANTAGE,	GLBLMAXANNUAL_BKNG_PRICE,	GLOBALMAXCNTRENDDATE,	GLOBALMAXCUSTSHRTNAME,	GLOBALMAXFAB,	GLBLMINANNUAL_BKNG_PRICE,	GLOBALMINCNTRENDDATE,	GLOBALMINCUSTSHRTNAME,	GLOBALMINFAB,	GREENBOOK,	NONCONSUMABLE,	ONCALLOUTSIDECONTRCOVERAGE,	PLATFORM,	PMLABOR,	PROCESSAPPENGINEERING,	PROCESSPARTSKITSCLEANRECY,	SERVICE_PRODUCT_DESC,	SERVICE_PRODUCT_NAME,	RENEWALFLAG,	RESPONSETIME,	RFPCONTRACTMATCH,	RFPNUM,	RFPSYSID,	GEN_ROW_NUM,	SALES_DOCUMENT_ITEM,	SERIAL_NUMBER,	SRVCTECHVITA,	SIMILARTOOL,	SRVCTECHPDCSERVER,	STDCOSPARTS,	STD_COS_PO_ITEM,	STDCOSLABOR,	STDGROSSMARGINDLR,	SWAPKITSAMATPROVIDED,	TECHFORCE,	TOOLCONFG,	TOTAL_COST,	TOTALGROSSMARGINDLR,	TOTALGROSSREVENUE,	TOTALNETBOOKINGS,	TOTALNETREVENUE,	TOTALNEWORDERS,	TOTALSTDCOST,	TOTALSTDCOSPARTS,	TOTALSTDCOSLABOR,	WAFERSIZE,	WETCLEANSLABOR,PRICE_BENCHMARK_RECORD_ID,	CPQTABLEENTRYDATEADDED,		CpqTableEntryDateModified )SELECT A.*,CONVERT(VARCHAR(100),NEWID()),GETDATE(),GETDATE() FROM(  SELECT PRPRBM_INBOUND.ANNUALIZED_BOOKING_PRICE,	PRPRBM_INBOUND.BLACKBOOK,	PRPRBM_INBOUND.BLUEBOOK,	PRPRBM_INBOUND.BOOKING_PER_TOOL,	PRPRBM_INBOUND.CMLABOR,	PRPRBM_INBOUND.CONSUMABLE,	PRPRBM_INBOUND.CONTRACT_BOOKING_DATE,	PRPRBM_INBOUND.CONTRACT_BOOKING_FISCAL_QURT,	PRPRBM_INBOUND.CONTRACT_BOOKING_FISCAL_YEAR,	PRPRBM_INBOUND.CONTRACT_CONTRACTCOVERAGE,	PRPRBM_INBOUND.CNTRDESC,	PRPRBM_INBOUND.CONTRACT_END_DATE,	PRPRBM_INBOUND.CONTRACT_END_FISCAL_MONTH,	PRPRBM_INBOUND.CONTRACT_END_FISCAL_QUARTER,	PRPRBM_INBOUND.CONTRACT_END_FISCAL_YEAR,	PRPRBM_INBOUND.CONTRACT,	PRPRBM_INBOUND.CONTRACT_START_DATE,	PRPRBM_INBOUND.CONTRACT_START_FISCAL_MONTH,	PRPRBM_INBOUND.CONTRACT_START_FISCAL_QUARTER,	PRPRBM_INBOUND.CONTRACT_START_FISCAL_YEAR,	PRPRBM_INBOUND.CUSTMAXANNUAL_BKNG_PRICE,	PRPRBM_INBOUND.CUSTMAXCNTRENDDATE,	PRPRBM_INBOUND.CUSTMAXFAB,	PRPRBM_INBOUND.CUSTMINANNUAL_BKNG_PRICE,	PRPRBM_INBOUND.CUSTMINCNTRENDDATE,	PRPRBM_INBOUND.CUSTMINFAB,	PRPRBM_INBOUND.CUSTNAME,	PRPRBM_INBOUND.CUSTSHRTNAMEMKTG,	PRPRBM_INBOUND.DAYSCOUNT,	PRPRBM_INBOUND.NODE,	PRPRBM_INBOUND.DIFF_MONTHS,	PRPRBM_INBOUND.EQUIPMENT_NUMBER,	PRPRBM_INBOUND.FNCNLLOC,	PRPRBM_INBOUND.FNCNLLOCDESC,	PRPRBM_INBOUND.FABVANTAGE,	PRPRBM_INBOUND.GLBLMAXANNUAL_BKNG_PRICE,	PRPRBM_INBOUND.GLOBALMAXCNTRENDDATE,	PRPRBM_INBOUND.GLOBALMAXCUSTSHRTNAME,	PRPRBM_INBOUND.GLOBALMAXFAB,	PRPRBM_INBOUND.GLBLMINANNUAL_BKNG_PRICE,	PRPRBM_INBOUND.GLOBALMINCNTRENDDATE,	PRPRBM_INBOUND.GLOBALMINCUSTSHRTNAME,	PRPRBM_INBOUND.GLOBALMINFAB,	PRPRBM_INBOUND.GREENBOOK,	PRPRBM_INBOUND.NONCONSUMABLE,	PRPRBM_INBOUND.ONCALLOUTSIDECONTRCOVERAGE,	PRPRBM_INBOUND.PLATFORM,	PRPRBM_INBOUND.PMLABOR,	PRPRBM_INBOUND.PROCESSAPPENGINEERING,	PRPRBM_INBOUND.PROCESSPARTSKITSCLEANRECY,	PRPRBM_INBOUND.SERVICE_PRODUCT_DESC,	PRPRBM_INBOUND.SERVICE_PRODUCT_NAME,	PRPRBM_INBOUND.RENEWALFLAG,	PRPRBM_INBOUND.RESPONSETIME,	PRPRBM_INBOUND.RFPCONTRACTMATCH,	PRPRBM_INBOUND.RFPNUM,	PRPRBM_INBOUND.RFPSYSID,	PRPRBM_INBOUND.GEN_ROW_NUM,	PRPRBM_INBOUND.SALES_DOCUMENT_ITEM,	PRPRBM_INBOUND.SERIAL_NUMBER,	PRPRBM_INBOUND.SRVCTECHVITA,	PRPRBM_INBOUND.SIMILARTOOL,	PRPRBM_INBOUND.SRVCTECHPDCSERVER,	PRPRBM_INBOUND.STDCOSPARTS,	PRPRBM_INBOUND.STD_COS_PO_ITEM,	PRPRBM_INBOUND.STDCOSLABOR,	PRPRBM_INBOUND.STDGROSSMARGINDLR,	PRPRBM_INBOUND.SWAPKITSAMATPROVIDED,	PRPRBM_INBOUND.TECHFORCE,	PRPRBM_INBOUND.TOOLCONFG,	PRPRBM_INBOUND.TOTAL_COST,	PRPRBM_INBOUND.TOTALGROSSMARGINDLR,	PRPRBM_INBOUND.TOTALGROSSREVENUE,	PRPRBM_INBOUND.TOTALNETBOOKINGS,	PRPRBM_INBOUND.TOTALNETREVENUE,	PRPRBM_INBOUND.TOTALNEWORDERS,	PRPRBM_INBOUND.TOTALSTDCOST,	PRPRBM_INBOUND.TOTALSTDCOSPARTS,	PRPRBM_INBOUND.TOTALSTDCOSLABOR,	PRPRBM_INBOUND.WAFERSIZE,	PRPRBM_INBOUND.WETCLEANSLABOR FROM PRPRBM_INBOUND (NOLOCK) LEFT JOIN PRPRBM (NOLOCK) ON PRPRBM_INBOUND.GEN_ROW_NUM = PRPRBM.GEN_ROW_NUM WHERE PRPRBM.GEN_ROW_NUM IS NULL )A '")
        
        s = SqlHelper.GetFirst("sp_executesql @T=N'delete from prprbm_inbound '")

        ApiResponse = ApiResponseFactory.JsonResponse(
            {
                "Response": [
                    {
                        "Status": "200",
                        "Message": "Pricebenchmark Data Successfully Uploaded ."
                    }
                ]
            }
        )
                
except:     
    Log.Info("PRGETPRBMK ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("PRGETPRBMK ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
    ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]}) 