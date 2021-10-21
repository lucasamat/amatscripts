# =========================================================================================================================================
#   __script_name : CQPRTPRCUP.py
#   __script_description : THIS SCRIPT IS USED FOR CPS PART PRICING 
#   __primary_author__ : 
#   __create_date :23-10-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
#clr.AddReference("System.Net")
clr.AddReference("IronPython")
clr.AddReference("Microsoft.Scripting")
from System.Net import WebRequest
from System.Net import HttpWebResponse
from Microsoft.Scripting import SourceCodeKind
from IronPython.Hosting import Python
from IronPython import Compiler
#import Webcom.Configurator.Scripting.Test.TestProduct
import System.Net
import sys
import datetime
from System.Text.Encoding import UTF8
from System import Convert
from SYDATABASE import SQL
import time
import datetime 



Sql = SQL()
QUOTE = Param.CPQ_Columns['Entries']
revision = Param.CPQ_Columns['Revision']
script_start_time = time.time()
Log.Info("QUOTE ID---> "+str(QUOTE)+"CPS Price Script Started")
Log.Info("------->CPI Hitting  2021")
webclient = System.Net.WebClient()
webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0=";
response = webclient.DownloadString("https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials")
response = eval(response)
Request_URL="https://cpservices-pricing.cfapps.us10.hana.ondemand.com/api/v1/statelesspricing"
webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response['access_token'])

Log.Info("654 response['access_token'] --->"+str(response['access_token']))


x = datetime.datetime.today()
x= str(x)
y = x.split(" ")
#partids = []
all_count = 0
loop_count = 0
#GET PRICING PROCEDURE
contract_quote_record_id = None
account_info={}
SAQTIP_INFO = SqlHelper.GetList(""" SELECT PARTY_ROLE, PARTY_ID FROM SAQTIP (NOLOCK) WHERE QUOTE_ID='{}' AND QTEREV_RECORD_ID='{}' AND PARTY_ROLE IN ('SOLD TO','SHIP TO') """.format(QUOTE,revision))
for keyobj in SAQTIP_INFO:
    account_info[keyobj.PARTY_ROLE] = keyobj.PARTY_ID

GetPricingProcedure = Sql.GetFirst("SELECT DIVISION_ID, DISTRIBUTIONCHANNEL_ID, SALESORG_ID, DOC_CURRENCY, PRICINGPROCEDURE_ID, QUOTE_RECORD_ID,EXCHANGE_RATE_TYPE, GLOBAL_CURRENCY FROM SAQTRV (NOLOCK) WHERE QUOTE_ID = '{}' AND QTEREV_RECORD_ID='{}' ".format(QUOTE,revision))
if GetPricingProcedure is not None:
    PricingProcedure = GetPricingProcedure.PRICINGPROCEDURE_ID
    curr = GetPricingProcedure.DOC_CURRENCY
    glb_curr =  GetPricingProcedure.GLOBAL_CURRENCY
    dis = GetPricingProcedure.DISTRIBUTIONCHANNEL_ID
    salesorg = GetPricingProcedure.SALESORG_ID
    div = GetPricingProcedure.DIVISION_ID
    exch = GetPricingProcedure.EXCHANGE_RATE_TYPE
    contract_quote_record_id = GetPricingProcedure.QUOTE_RECORD_ID
    #taxk1 = GetPricingProcedure.CUSTAXCLA_ID
    taxk1 = "1"
#else:
#PricingProcedure = 'ZZNA05'
#curr = 'USD'
#dis = '01'
#salesorg = '2034'
#div = '98'

#UPDATE PRICING PROCEDURE TO SAQITM


update_SAQITM = "UPDATE SAQITM SET PRICINGPROCEDURE_ID = '{prc}' WHERE SAQITM.QUOTE_ID = '{quote}' AND SAQITM.QTEREV_RECORD_ID='{revision_rec_id}'".format(prc=str(PricingProcedure), quote=QUOTE, revision_rec_id = revision)
Sql.RunQuery(update_SAQITM)
update_SAQIFP = "UPDATE SAQIFP SET PRICINGPROCEDURE_ID = '{prc}' WHERE SAQIFP.QUOTE_ID = '{quote}'".format(prc=str(PricingProcedure), quote=QUOTE)
Sql.RunQuery(update_SAQIFP)

today = datetime.datetime.now()
Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")


start = 1
end = 1000
L = 1

Taxm1Qurey=Sql.GetFirst("SELECT ISNULL(SRVTAXCLA_ID,1) as SRVTAXCLA_ID FROM SAQITM (NOLOCK) WHERE QUOTE_ID ='{quote}' AND QTEREV_RECORD_ID='{revision_rec_id}'".format(quote=QUOTE, revision_rec_id = revision))
part_query = SqlHelper.GetList("SELECT PART_NUMBER, ANNUAL_QUANTITY FROM (SELECT PART_NUMBER, ANNUAL_QUANTITY,ROW_NUMBER() OVER(ORDER BY PART_NUMBER) AS SNO FROM SAQIFP (NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE)+"' AND QTEREV_RECORD_ID = '"+str(revision)+"' AND PRICING_STATUS = 'ACQUIRING...' )A WHERE SNO>="+str(start)+" AND SNO<="+str(end)+"  ")
if part_query:

    while L == 1:
        #Log.Info("Looping Count ==> "+str(n))
        itemid = ''
        part_query = SqlHelper.GetList("SELECT PART_NUMBER, ANNUAL_QUANTITY FROM (SELECT PART_NUMBER, ANNUAL_QUANTITY,ROW_NUMBER() OVER(ORDER BY PART_NUMBER) AS SNO FROM SAQIFP (NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE)+"' AND QTEREV_RECORD_ID = '"+str(revision)+"' AND PRICING_STATUS = 'ACQUIRING...' )A WHERE SNO>="+str(start)+" AND SNO<="+str(end)+"  ")
        partids = quantity = li = []
        s = ""
        if part_query:      
            partids = [p.PART_NUMBER for p in part_query]
            quantity = [float(q.ANNUAL_QUANTITY) for q in part_query]  
            start = start + 1000
            end = end + 1000
            
            if len(partids) == 1:
                Log.Info("**Single-Partids**")
                itemid = str(partids[0])+";"+str(QUOTE)+";"+str(quantity[0])
                #item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(quantity[0])+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(partids[0])+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["CN"]},{"name":"KOMK-ALAND","values":["CN"]},{"name":"KOMK-REGIO","values":["TX"]},{"name":"KOMK-KUNNR","values":["'+stp_account_id+'"]},{"name":"KOMK-KUNWE","values":["'+stp_account_id+'"]},{"name":"KOMP-TAXM1","values":["'+str(Taxm1Qurey.SRVTAXCLA_ID)+'"]},{"name":"KOMK-TAXK1","values":["'+str(taxk1)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(div)+'"]},{"name":"KOMP-PMATN","values":["'+str(partids[0])+'"]},{"name":"KOMK-WAERK","values":["'+str(curr)+'"]},{"name":"KOMK-HWAER","values":["'+str(curr)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]},{"name":"KOMP-KPOSN","values":["0"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMP-ZZEXE","values":["true"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(y[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(y[0])+'"}],"variantConditions":[],"statistical":true,"subItems":[]}'
                #item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(quantity[0])+',"unit":"EA"},"exchRateType":"M","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(partids[0])+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["US"]},{"name":"KOMP-KPOSN","values":["10"]},{"name":"KOMV-KSCHL","values":[""]},{"name":"KOMP-ZZEXE","values":[""]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMK-KUNNR","values":["0010010977"]},{"name":"KOMK-KUNWE","values":["0010010977"]},{"name":"KOMK-SPART","values":["98"]},{"name":"KOMP-SPART","values":["98"]},{"name":"KOMP-PMATN","values":["0041-29874"]},{"name":"KOMP-ZZPSTR_COUNTER","values":["1"]},{"name":"KOMK-WAERK","values":["USD"]},{"name":"KOMK-ZZSPART","values":["22"]},{"name":"KOMV-KDUPL","values":[""]},{"name":"KOMP-ZZPRREASON","values":[""]},{"name":"KOMK-AUART","values":["ZQT1"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMP-FAREG","values":[""]},{"name":"KOMP-EVRWR","values":["X"]},{"name":"KOMK-KURST","values":["M"]},{"name":"KOMP-MGAME","values":["1.00"]},{"name":"KOMK-BUKRS","values":["0001"]},{"name":"KOMV-KKURS","values":["1.00"]},{"name":"KOMK-AUART_SD","values":["ZQT1"]},{"name":"KOMP-WERKS","values":["5252"]},{"name":"KOMP-MWSBP","values":["0.00"]},{"name":"KOMP-PRSOK","values":["X"]},{"name":"KOMP-PSTYV","values":["ZAGN"]},{"name":"KOMV-KNTYP","values":["G"]},{"name":"KOMK-VTWEG","values":["01"]},{"name":"KOMP-BRTWR","values":["0.0"]},{"name":"KOMP-MGLME","values":["1.0"]},{"name":"KOMV-KPEIN","values":["1.0"]},{"name":"KOMK-FKART","values":[""]},{"name":"KOMK-ERDAT","values":["20211004"]},{"name":"KOMV-KNUMV","values":[""]},{"name":"KOMK-VBTYP","values":["B"]},{"name":"KOMK-VKORG","values":["2000"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"2021-10-01"},{"name":"KOMK-FBUDA","value":"2021-10-01"}],"variantConditions":[],"statistical":true,"subItems":[]}'
                item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(quantity[0])+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(partids[0])+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["CN"]},{"name":"KOMP-KPOSN","values":["10"]},{"name":"KOMV-KSCHL","values":[""]},{"name":"KOMP-ZZEXE","values":[""]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMK-KUNNR","values":["'+account_info['SOLD TO']+'"]},{"name":"KOMK-KUNWE","values":["'+account_info['SHIP TO']+'"]},{"name":"KOMK-SPART","values":["22"]},{"name":"KOMP-SPART","values":["98"]},{"name":"KOMP-PMATN","values":["'+str(partids[0])+'"]},{"name":"KOMP-ZZPSTR_COUNTER","values":["1"]},{"name":"KOMK-WAERK","values":["USD"]},{"name":"KOMK-ZZSPART","values":["'+str(div)+'"]},{"name":"KOMV-KDUPL","values":[""]},{"name":"KONV-KOAID","values":["A"]},{"name":"KOMP-ZZPRREASON","values":[""]},{"name":"KOMK-AUART","values":["ZQT1"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-ZZWFSTATUS","values":[""]},{"name":"KOMP-UEPOS","values":["0000"]},{"name":"KOMP-FAREG","values":[""]},{"name":"KOMP-EVRWR","values":["X"]},{"name":"KOMK-KURST","values":["M"]},{"name":"KOMP-MGAME","values":["1.00"]},{"name":"KOMP-TAXM1","values":["1"]},{"name":"KOMK-ZZKTOKD","values":["KUNA"]},{"name":"KOMK-BUKRS","values":["0028"]},{"name":"KOMV-KKURS","values":["1.00"]},{"name":"KONP-KNTYP","values":["L"]},{"name":"KOMK-ZTERM","values":["1.00"]},{"name":"KOMK-INCO1","values":["DAP"]},{"name":"KOMK-AUART_SD","values":["ZQT1"]},{"name":"KOMK-ALAND","values":["AG"]},{"name":"KOMP-WERKS","values":["8639"]},{"name":"KOMP-MWSBP","values":["0.00"]},{"name":"KOMP-PRSOK","values":["X"]},{"name":"KOMP-PSTYV","values":["ZAGN"]},{"name":"KOMP-SKTOF","values":["X"]},{"name":"KOMK-PLTYP","values":["TS"]},{"name":"KOMP-ZZMTLSEGMCODE","values":["A01-000"]},{"name":"KOMP-KONDM","values":["N"]},{"name":"KOMV-KNTYP","values":["G"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMP-BRTWR","values":["0.0"]},{"name":"KOMP-MGLME","values":["1.0"]},{"name":"KOMV-KPEIN","values":["1.0"]},{"name":"KOMK-FKART","values":[""]},{"name":"KOMK-ERDAT","values":["20211004"]},{"name":"KOMV-KNUMV","values":[""]},{"name":"KOMK-VBTYP","values":["B"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"2021-10-01"},{"name":"KOMK-FBUDA","value":"2021-10-01"}],"variantConditions":[],"statistical":true,"subItems":[]}'
                    

                requestdata = '<?xml version=\"1.0\" encoding=\"UTF-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\">  <soapenv:Body> <cpq_columns><root> {"docCurrency":"'+curr+'","locCurrency":"'+curr+'","pricingProcedure":"'+PricingProcedure+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+str(item_string)+']} </root> <CPSToken>'+str(response['access_token'])+'</CPSToken></cpq_columns> </soapenv:Body></soapenv:Envelope>'
            else:
                Log.Info("**Multiple-Partids**")
                for p,q in zip(partids,quantity):
                    itemid = str(p)+";"+str(QUOTE)+";"+str(q)
                    #item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(q)+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(p)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["CN"]},{"name":"KOMK-ALAND","values":["CN"]},{"name":"KOMK-REGIO","values":["TX"]},{"name":"KOMK-KUNNR","values":["'+stp_account_id+'"]},{"name":"KOMK-KUNWE","values":["'+stp_account_id+'"]},{"name":"KOMP-TAXM1","values":["'+str(Taxm1Qurey.SRVTAXCLA_ID)+'"]},{"name":"KOMK-TAXK1","values":["'+str(taxk1)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(div)+'"]},{"name":"KOMP-PMATN","values":["'+str(p)+'"]},{"name":"KOMK-WAERK","values":["'+str(curr)+'"]},{"name":"KOMK-HWAER","values":["'+str(curr)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]},{"name":"KOMP-KPOSN","values":["0"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMP-ZZEXE","values":["true"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(y[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(y[0])+'"}],"variantConditions":[],"statistical":true,"subItems":[]}'
                    #item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(q)+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(p)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["US"]},{"name":"KOMP-KPOSN","values":["10"]},{"name":"KOMV-KSCHL","values":[""]},{"name":"KOMP-ZZEXE","values":[""]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMK-KUNNR","values":["0010010977"]},{"name":"KOMK-KUNWE","values":["0010010977"]},{"name":"KOMK-SPART","values":["98"]},{"name":"KOMP-SPART","values":["98"]},{"name":"KOMP-PMATN","values":["0041-29874"]},{"name":"KOMP-ZZPSTR_COUNTER","values":["1"]},{"name":"KOMK-WAERK","values":["USD"]},{"name":"KOMK-ZZSPART","values":["22"]},{"name":"KOMV-KDUPL","values":[""]},{"name":"KOMP-ZZPRREASON","values":[""]},{"name":"KOMK-AUART","values":["ZQT1"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMP-FAREG","values":[""]},{"name":"KOMP-EVRWR","values":["X"]},{"name":"KOMK-KURST","values":["M"]},{"name":"KOMP-MGAME","values":["1.00"]},{"name":"KOMK-BUKRS","values":["0001"]},{"name":"KOMV-KKURS","values":["1.00"]},{"name":"KOMK-AUART_SD","values":["ZQT1"]},{"name":"KOMP-WERKS","values":["5252"]},{"name":"KOMP-MWSBP","values":["0.00"]},{"name":"KOMP-PRSOK","values":["X"]},{"name":"KOMP-PSTYV","values":["ZAGN"]},{"name":"KOMV-KNTYP","values":["G"]},{"name":"KOMK-VTWEG","values":["01"]},{"name":"KOMP-BRTWR","values":["0.0"]},{"name":"KOMP-MGLME","values":["1.0"]},{"name":"KOMV-KPEIN","values":["1.0"]},{"name":"KOMK-FKART","values":[""]},{"name":"KOMK-ERDAT","values":["20211004"]},{"name":"KOMV-KNUMV","values":[""]},{"name":"KOMK-VBTYP","values":["B"]},{"name":"KOMK-VKORG","values":["2000"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"2021-10-01"},{"name":"KOMK-FBUDA","value":"2021-10-01"}],"variantConditions":[],"statistical":true,"subItems":[]}'
                    item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(q)+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(p)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["CN"]},{"name":"KOMP-KPOSN","values":["10"]},{"name":"KOMV-KSCHL","values":[""]},{"name":"KOMP-ZZEXE","values":[""]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMK-KUNNR","values":["'+account_info['SOLD TO']+'"]},{"name":"KOMK-KUNWE","values":["'+account_info['SHIP TO']+'"]},{"name":"KOMK-SPART","values":["22"]},{"name":"KOMP-SPART","values":["98"]},{"name":"KOMP-PMATN","values":["'+str(p)+'"]},{"name":"KOMP-ZZPSTR_COUNTER","values":["1"]},{"name":"KOMK-WAERK","values":["USD"]},{"name":"KOMK-ZZSPART","values":["'+str(div)+'"]},{"name":"KOMV-KDUPL","values":[""]},{"name":"KONV-KOAID","values":["A"]},{"name":"KOMP-ZZPRREASON","values":[""]},{"name":"KOMK-AUART","values":["ZQT1"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-ZZWFSTATUS","values":[""]},{"name":"KOMP-UEPOS","values":["0000"]},{"name":"KOMP-FAREG","values":[""]},{"name":"KOMP-EVRWR","values":["X"]},{"name":"KOMK-KURST","values":["M"]},{"name":"KOMP-MGAME","values":["1.00"]},{"name":"KOMP-TAXM1","values":["1"]},{"name":"KOMK-ZZKTOKD","values":["KUNA"]},{"name":"KOMK-BUKRS","values":["0028"]},{"name":"KOMV-KKURS","values":["1.00"]},{"name":"KONP-KNTYP","values":["L"]},{"name":"KOMK-ZTERM","values":["1.00"]},{"name":"KOMK-INCO1","values":["DAP"]},{"name":"KOMK-AUART_SD","values":["ZQT1"]},{"name":"KOMK-ALAND","values":["AG"]},{"name":"KOMP-WERKS","values":["8639"]},{"name":"KOMP-MWSBP","values":["0.00"]},{"name":"KOMP-PRSOK","values":["X"]},{"name":"KOMP-PSTYV","values":["ZAGN"]},{"name":"KOMP-SKTOF","values":["X"]},{"name":"KOMK-PLTYP","values":["TS"]},{"name":"KOMP-ZZMTLSEGMCODE","values":["A01-000"]},{"name":"KOMP-KONDM","values":["N"]},{"name":"KOMV-KNTYP","values":["G"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMP-BRTWR","values":["0.0"]},{"name":"KOMP-MGLME","values":["1.0"]},{"name":"KOMV-KPEIN","values":["1.0"]},{"name":"KOMK-FKART","values":[""]},{"name":"KOMK-ERDAT","values":["20211004"]},{"name":"KOMV-KNUMV","values":[""]},{"name":"KOMK-VBTYP","values":["B"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"2021-10-01"},{"name":"KOMK-FBUDA","value":"2021-10-01"}],"variantConditions":[],"statistical":true,"subItems":[]}'
                    li.append(item_string)
                s = ','.join(li)
                
                start_time = time.time()
                #requestdata = '<?xml version=\"1.0\" encoding=\"UTF-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\">  <soapenv:Body> <cpq_columns><root>  {"docCurrency":"'+curr+'","locCurrency":"'+curr+'","pricingProcedure":"'+PricingProcedure+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+str(s)+']} </root> <CPSToken>'+str(response['access_token'])+'</CPSToken></cpq_columns> </soapenv:Body></soapenv:Envelope>'
                requestdata = '<?xml version=\"1.0\" encoding=\"UTF-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\">  <soapenv:Body> <cpq_columns><root>  {"docCurrency":"null","locCurrency":"'+curr+'","pricingProcedure":"'+PricingProcedure+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+str(s)+']} </root> <CPSToken>'+str(response['access_token'])+'</CPSToken></cpq_columns> </soapenv:Body></soapenv:Envelope>'
            Log.Info("requestdata==>"+str(requestdata))
            #response1 = webclient.UploadString(Request_URL,str(requestdata))
            
            LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password,Domain FROM SYCONF where Domain='AMAT_TST'")
            Login_Username = str(LOGIN_CREDENTIALS.Username)
            Login_Password = str(LOGIN_CREDENTIALS.Password)
            authorization = Login_Username + ":" + Login_Password
            binaryAuthorization = UTF8.GetBytes(authorization)
            authorization = Convert.ToBase64String(binaryAuthorization)
            authorization = "Basic " + authorization
            webclient = System.Net.WebClient()
            webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
            webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization
            #Log.Info("Looping Count ==> ")
            
            response1 = webclient.UploadString("https://e250404-iflmap.hcisbt.us3.hana.ondemand.com/cxf/CPQ_CPS",str(requestdata))
            Log.Info(response1)
            end_time = time.time()
            #Log.Info("QUOTE ID---> "+str(QUOTE)+"loop---"+str(loop_count)+ "---time"+str(end_time - start_time))
        else:
            L=0
else:
    Log.Info('150----to call pricing here---quote table insert----')
    price = []
    #QUOTE = ''
    account_obj = Sql.GetFirst("SELECT ACCOUNT_ID FROM SAOPQT (NOLOCK) WHERE QUOTE_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{revision_rec_id}'".format(QuoteRecordId=QUOTE,revision_rec_id = revision))
    stp_account_id = ""
    service_obj = Sql.GetFirst("SELECT SERVICE_ID FROM SAQTSE (NOLOCK) WHERE QUOTE_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{revision_rec_id}'".format(QuoteRecordId=QUOTE,revision_rec_id = revision))
    serviceId = ""
    if account_obj:
        stp_account_id = str(account_obj.ACCOUNT_ID)
    if service_obj:
        serviceId = str(service_obj.SERVICE_ID)
    salesorg_obj = Sql.GetFirst("SELECT DIVISION_ID, DISTRIBUTIONCHANNEL_ID, SALESORG_ID, DOC_CURRENCY, PRICINGPROCEDURE_ID,EXCHANGE_RATE_TYPE FROM SAQTRV (NOLOCK) WHERE QUOTE_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{revision_rec_id}'".format(QuoteRecordId=QUOTE,revision_rec_id = revision))
    item_string = ''
    if salesorg_obj:
        Trace.Write("serviceId--22--"+str(serviceId))			
        
        exchange_rate_type = salesorg_obj.EXCHANGE_RATE_TYPE if salesorg_obj.EXCHANGE_RATE_TYPE else 'M'
        pricing_procedure_id = salesorg_obj.PRICINGPROCEDURE_ID if salesorg_obj.PRICINGPROCEDURE_ID else 'ZZNA05'
        item_string = '{"itemId":"1","externalId":null,"quantity":{"value":'+str(1)+',"unit":"EA"},"exchRateType":"'+exchange_rate_type+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(serviceId)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-ALAND","values":["US"]},{"name":"KOMK-REGIO","values":["TX"]},{"name":"KOMK-KUNNR","values":["'+stp_account_id+'"]},{"name":"KOMK-KUNWE","values":["'+stp_account_id+'"]},{"name":"KOMK-SPART","values":["'+str(salesorg_obj.DIVISION_ID)+'"]},{"name":"KOMP-SPART","values":["'+str(salesorg_obj.DIVISION_ID)+'"]},{"name":"KOMP-PMATN","values":["'+str(serviceId)+'"]},{"name":"KOMK-WAERK","values":["'+str(salesorg_obj.DOC_CURRENCY)+'"]},{"name":"KOMK-HWAER","values":["'+str(salesorg_obj.DOC_CURRENCY)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-VTWEG","values":["'+str(salesorg_obj.DISTRIBUTIONCHANNEL_ID)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg_obj.SALESORG_ID)+'"]},{"name":"KOMP-KPOSN","values":["0"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMP-ZZEXE","values":["true"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(y[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(y[0])+'"}],"variantConditions":[{"factor":1.0,"key":"AGS_LAB_OPT6"},{"factor":13.0,"key":"AGS_LAB_OPT8"}],"statistical":true,"subItems":[]}'

    requestdata = '{"docCurrency":"'+salesorg_obj.DOC_CURRENCY+'","locCurrency":"'+salesorg_obj.DOC_CURRENCY+'","pricingProcedure":"'+pricing_procedure_id+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+item_string+']}'
    #Log.Info("requestdata--171---"+str(requestdata))
    response1 = webclient.UploadString(Request_URL,str(requestdata))
    #Log.Info("res--173-------"+str(response1))
    response1 = str(response1).replace(": true", ': "true"').replace(": false", ': "false"').replace(": null",': " None"')
    response1 = eval(response1)
    #Log.Info("res--176------"+str(response1))
    for root, value in response1.items():
        if root == "items":
            #Log.Info("6666 i[u] --->"+str(list(root1[inv])))
            price = value[:]			 
            break
   
    #Log.Info("type condition--->")
    #price = [price]
    #Log.Info("456789 type(price) --->"+str(type(price)))
    #for i in price[0]['conditions']:		
        #Itemidinfo = str(i["itemId"])
        #Log.Info("456 Itemidinfo --->"+str(Itemidinfo))
        #QUOTE = str(Itemidinfo[1])	
    contract_quote_record_id = None		
    getuomrec_val = ''
    getservicerecord = Sql.GetFirst("select QUOTE_RECORD_ID,QUOTE_NAME,SERVICE_DESCRIPTION,SERVICE_ID,	SERVICE_RECORD_ID from SAQTSE (NOLOCK) where QUOTE_ID = '{}' AND QTEREV_RECORD_ID='{}'".format(QUOTE,revision))
    #QuoteItemList = Quote.QuoteTables["SAQICD"]
    for cond_info in price[0]['conditions']:
        #Log.Info("333 cond_info['conditionType'] --->"+str(cond_info['conditionType']))
        getuomrec = Sql.GetFirst("select UOM_RECORD_ID from MAMTRL where UNIT_OF_MEASURE = '"+str(cond_info['conditionUnit'])+"'")
        if getuomrec:
            getuomrec_val = getuomrec.UOM_RECORD_ID
        else:
            getuomrec_val = 'EA'
        #Log.Info("query start")
        #Log.Info("sp_executesql @T=N'INSERT QT__SAQICD (CONDITION_COUNTER,CONDITION_DATA_TYPE,CONDITION_RATE,CONDITION_TYPE,CONDITIONTYPE_NAME,CONDITIONTYPE_RECORD_ID,UOM,CONDITION_VALUE,UOM_RECORD_ID,LINE,QUOTE_ID,QTEITM_RECORD_ID,QUOTE_NAME,SERVICE_DESCRIPTION,SERVICE_ID,STEP_NUMBER,SERVICE_RECORD_ID,QUOTE_RECORD_ID,CONDITION_CURRENCY,CONDITION_BASE) values (''"+str(cond_info['conditionCounter'])+"'',''"+str(cond_info['calculationType'])+"'',''"+str(cond_info['conditionRate'].strip())+"'',''"+str(cond_info['conditionType'])+ "'',''"+ str(cond_info['conditionTypeDescription'].strip())+ "'' , ''"+ str(cond_info['conditionUnitValue'])+ "'',''"+ str(cond_info['conditionUnit'])+ "'',''"+ str(cond_info['conditionValue'])+ "'',''"+ str(getuomrec_val)+ "'','''',''"+ str(getservicerecord.QUOTE_RECORD_ID)+ "'','''',''"+ str(getservicerecord.QUOTE_NAME)+ "'',''"+ str(getservicerecord.SERVICE_DESCRIPTION)+ "'',''"+ str(getservicerecord.SERVICE_ID)+ "'',''"+ str(cond_info['stepNo'])+ "'',''"+ str(getservicerecord.SERVICE_RECORD_ID)+ "'',''"+ str(QUOTE)+ "'',''"+str(cond_info['conditionCurrency'])+"'',''"+str(cond_info['conditionBase'])+"'')'")
        '''
        saqicd_insert = SqlHelper.GetFirst("sp_executesql @T=N'INSERT QT__SAQICD (CONDITION_COUNTER,CONDITION_DATA_TYPE,CONDITION_RATE,CONDITION_TYPE,CONDITIONTYPE_NAME,CONDITIONTYPE_RECORD_ID,UOM,CONDITION_VALUE,UOM_RECORD_ID,LINE,QUOTE_ID,QTEITM_RECORD_ID,QUOTE_NAME,SERVICE_DESCRIPTION,SERVICE_ID,STEP_NUMBER,SERVICE_RECORD_ID,QUOTE_RECORD_ID,CONDITION_CURRENCY,CONDITION_BASE) values (''"+str(cond_info['conditionCounter'])+"'',''"+str(cond_info['calculationType'])+"'',''"+str(cond_info['conditionRate'].strip())+"'',''"+str(cond_info['conditionType'])+ "'',''"+ str(cond_info['conditionTypeDescription'].strip())+ "'' , ''"+ str(cond_info['conditionUnitValue'])+ "'',''"+ str(cond_info['conditionUnit'])+ "'',''"+ str(cond_info['conditionValue'])+ "'',''"+ str(getuomrec_val)+ "'','''',''"+ str(QUOTE)+ "'','''',''"+ str(getservicerecord.QUOTE_NAME)+ "'',''"+ str(getservicerecord.SERVICE_DESCRIPTION)+ "'',''"+ str(getservicerecord.SERVICE_ID)+ "'',''"+ str(cond_info['stepNo'])+ "'',''"+ str(getservicerecord.SERVICE_RECORD_ID)+ "'',''"+ str(getservicerecord.QUOTE_RECORD_ID)+ "'',''"+str(cond_info['conditionCurrency'])+"'',''"+str(cond_info['conditionBase'])+"'')'")
        newRow = QuoteItemList.AddNewRow()
        newRow['CONDITION_COUNTER'] = cond_info['conditionCounter']
        newRow['CONDITION_DATA_TYPE'] =  cond_info['conditionType']
        newRow['CONDITION_RATE'] = cond_info['conditionRate'].strip()
        newRow['CONDITION_TYPE'] = cond_info['conditionType']
        newRow['CONDITIONTYPE_NAME'] = cond_info['conditionTypeDescription'].strip()
        newRow['UOM'] =  cond_info['conditionUnit']
        newRow['CONDITIONTYPE_RECORD_ID'] = ''
        newRow['CONDITION_VALUE'] = cond_info['conditionValue']
        newRow['UOM_RECORD_ID'] = getuomrec.UOM_RECORD_ID
        newRow['LINE'] = ''
        newRow['QTEITM_RECORD_ID'] = ''
        newRow['QUOTE_NAME'] = getservicerecord.QUOTE_NAME
        newRow['SERVICE_DESCRIPTION'] = getservicerecord.SERVICE_DESCRIPTION
        newRow['SERVICE_ID'] = getservicerecord.SERVICE_ID
        newRow['STEP_NUMBER'] = cond_info['stepNo']
        newRow['SERVICE_RECORD_ID'] = getservicerecord.SERVICE_RECORD_ID
        newRow['QUOTE_RECORD_ID'] = contract_quote_record_id
        newRow['QUOTE_ID'] = QUOTE
        QuoteItemList.Save()'''		                
today = datetime.datetime.now()
Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")

#Log.Info("CQPRTPRCUP  end time ---->"+str(Modi_date))
