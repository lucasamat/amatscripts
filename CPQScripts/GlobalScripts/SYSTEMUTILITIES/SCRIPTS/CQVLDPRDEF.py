# =========================================================================================================================================
#   __script_name : CQVLDRLDWN.PY
#   __script_description : THIS SCRIPT IS USED FOR PREDEFINED VALUES IN VALUE DRIVER (GETS TRIGGERED AFTER IFLOW SCRIPT - CQTVLDRIFW.py)
#   __primary_author__ : 
#   __create_date :06-09-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
import datetime
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
from SYDATABASE import SQL

Sql = SQL()

Log.Info('Predefined Iflow')

def PreDefinedWaferNode():
    Log.Info('check def')
    #GREENBOOK != DISPLAY AND PPC
    quer_statement_17 = """ INSERT SAQSCD (QUOTE_SERVICE_COVERED_OBJ_TOOL_DRIVER_RECORD_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,SERIAL_NUMBER,QTESRVCOB_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,VALUEDRIVER_ID,VALUEDRIVER_RECORD_ID,VALUEDRIVER_TYPE,VALUEDRIVER_NAME,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,QTESRVFBL_RECORD_ID,QTESRVGBK_VDR_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,QTEREV_ID,QTEREV_RECORD_ID)
    SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_TOOL_DRIVER_RECORD_ID,SAQSCO.EQUIPMENT_DESCRIPTION,SAQSCO.EQUIPMENT_ID,SAQSCO.EQUIPMENT_RECORD_ID,SAQSCO.QUOTE_ID,SAQSCO.QUOTE_NAME,SAQSCO.QUOTE_RECORD_ID,SAQSCO.SERIAL_NO as SERIAL_NUMBER,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,SAQSCO.SERVICE_DESCRIPTION,SAQSCO.SERVICE_ID,SAQSCO.SERVICE_RECORD_ID,PRSVDR.VALUEDRIVER_ID,PRSVDR.VALUEDRIVER_RECORD_ID,PRSVDR.VALUEDRIVER_TYPE,PRSVDR.VALUEDRIVER_NAME,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQSCO.FABLOCATION_ID,SAQSCO.FABLOCATION_NAME,SAQSCO.FABLOCATION_RECORD_ID,'' as QTESRVFBL_RECORD_ID,'' as QTESRVGBK_VDR_RECORD_ID,'{username}' as CPQTABLEENTRYADDEDBY ,'{datetimenow}' as CPQTABLEENTRYDATEADDED ,'' as QTEREV_ID,SAQSCO.QTEREV_RECORD_ID from MAEQUP INNER JOIN SAQSCO (NOLOCK) ON MAEQUP.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID and MAEQUP.GREENBOOK = SAQSCO.GREENBOOK INNER JOIN PRSVDR ON SAQSCO.SERVICE_ID = PRSVDR.SERVICE_ID  WHERE MAEQUP.GREENBOOK = 'DISPLAY' AND SAQSCO.QUOTE_RECORD_ID ='{rec}' AND SAQSCO.QTEREV_RECORD_ID = '{qurev_rec_id}' AND SAQSCO.SERVICE_ID ='{treeparam}' AND PRSVDR.VALUEDRIVER_ID = 'Wafer-Node' AND (MAEQUP.SUBSTRATE_SIZE IN ('300MM') AND (MAEQUP.TECHNOLOGY_NODE IN ('NOR','EQUIP/MATL','MPS','PACKAGING','WFR MFG','SOLAR','PCM','OTHER') OR MAEQUP.TECHNOLOGY_NODE >= '28NM' OR MAEQUP.TECHNOLOGY_NODE >= '4X')) AND MAEQUP.EQUIPMENT_ID NOT IN (SELECT EQUIPMENT_ID FROM SAQSCD WHERE QTEREV_RECORD_ID = '{qurev_rec_id}' AND SERVICE_ID ='{treeparam}' AND QUOTE_RECORD_ID ='{rec}' )""".format(rec=Qt_rec_id, datetimenow=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"), userid=userId, username=userName,treeparam=TreeParam,qurev_rec_id=quote_revision_record_id)
    Sql.RunQuery(quer_statement_17)
    quer_statement_18 = """ INSERT SAQSCV (QUOTE_SERVICE_COVERED_OBJ_TOOL_DRIVER_VALUE_RECORD_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTESRVCOB_RECORD_ID,QTESRVCOB_VDR_RECORD_ID,SERIAL_NUMBER,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,TOOL_VALUEDRIVER_ID,TOOL_VALUEDRIVER_RECORD_ID,TOOL_VALUEDRIVER_VALUE_CODE,TOOL_VALUEDRIVER_VALUE_DESCRIPTION,GREENBOOK,GREENBOOK_RECORD_ID,TOOL_VALUEDRIVER_VALUE_RECORD_ID,VALUEDRIVER_COEFFICIENT,VALUEDRIVER_COEFFICIENT_RECORD_ID,FABLOCATION_ID,CPQTABLEENTRYADDEDBY,ADDUSR_RECORD_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,CPQTABLEENTRYDATEADDED,QTESRVFBL_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID)
    SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_TOOL_DRIVER_VALUE_RECORD_ID,SAQSCO.EQUIPMENT_DESCRIPTION,SAQSCO.EQUIPMENT_ID,SAQSCO.EQUIPMENT_RECORD_ID,SAQSCO.QUOTE_ID,SAQSCO.QUOTE_NAME,SAQSCO.QUOTE_RECORD_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,SAQSCD.QUOTE_SERVICE_COVERED_OBJ_TOOL_DRIVER_RECORD_ID as QTESRVCOB_VDR_RECORD_ID,SAQSCO.SERIAL_NO as SERIAL_NUMBER,SAQSCO.SERVICE_DESCRIPTION,SAQSCO.SERVICE_ID,SAQSCO.SERVICE_RECORD_ID,PRSDVL.VALUEDRIVER_ID,PRSDVL.VALUEDRIVER_RECORD_ID,PRSDVL.VALUEDRIVER_VALUE_CODE,PRSDVL.VALUEDRIVER_VALUE_DESCRIPTION,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,PRSDVL.VALUEDRIVER_VALUE_RECORD_ID,PRSDVL.VALUEDRIVER_COEFFICIENT,PRSDVL.SRVDRVAL_RECORD_ID as VALUEDRIVER_COEFFICIENT_RECORD_ID,SAQSCO.FABLOCATION_ID,'{username}' as CPQTABLEENTRYADDEDBY,'{userid}' as ADDUSR_RECORD_ID,SAQSCO.FABLOCATION_NAME,SAQSCO.FABLOCATION_RECORD_ID,'{datetimenow}' as CPQTABLEENTRYDATEADDED,'' as QTESRVFBL_RECORD_ID,'' as QTEREV_ID,SAQSCO.QTEREV_RECORD_ID from MAEQUP INNER JOIN SAQSCO (NOLOCK) ON MAEQUP.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID and MAEQUP.GREENBOOK = SAQSCO.GREENBOOK INNER JOIN PRSDVL ON SAQSCO.SERVICE_ID = PRSDVL.SERVICE_ID INNER JOIN SAQSCD ON SAQSCO.SERVICE_ID = SAQSCD.SERVICE_ID AND SAQSCO.QTEREV_RECORD_ID = SAQSCD.QTEREV_RECORD_ID AND SAQSCO.EQUIPMENT_ID = SAQSCD.EQUIPMENT_ID WHERE MAEQUP.GREENBOOK = 'DISPLAY' AND SAQSCO.QUOTE_RECORD_ID ='{rec}' AND SAQSCO.QTEREV_RECORD_ID = '{qurev_rec_id}' AND SAQSCO.SERVICE_ID ='{treeparam}' AND PRSDVL.VALUEDRIVER_ID = 'Wafer-Node' AND PRSDVL.VALUEDRIVER_VALUE_DESCRIPTION ='Legacy' AND (MAEQUP.SUBSTRATE_SIZE IN ('300MM') AND (MAEQUP.TECHNOLOGY_NODE IN ('NOR','EQUIP/MATL','MPS','PACKAGING','WFR MFG','SOLAR','PCM','OTHER') OR MAEQUP.TECHNOLOGY_NODE >= '28NM' OR MAEQUP.TECHNOLOGY_NODE >= '4X')) AND MAEQUP.EQUIPMENT_ID NOT IN (SELECT EQUIPMENT_ID FROM SAQSCV WHERE QTEREV_RECORD_ID = '{qurev_rec_id}' AND SERVICE_ID ='{treeparam}' AND QUOTE_RECORD_ID ='{rec}' )""".format(rec=Qt_rec_id, datetimenow=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"), userid=userId, username=userName,treeparam=TreeParam,qurev_rec_id=quote_revision_record_id)
    Sql.RunQuery(quer_statement_18)
    Log.Info("quer_statement 17->"+str(quer_statement_17))
    Log.Info("quer_statement_18 ->"+str(quer_statement_18))




try:
    Qt_rec_id = Param.CPQ_Columns['Quote'] 
except:
    Qt_rec_id = ""

#Log.Info("Qt_rec_id ->"+str(Qt_rec_id))
try:
    LEVEL = Param.CPQ_Columns['Level']
except:
    LEVEL = ""

try:
    TreeParam = Param.CPQ_Columns['TreeParam']
    TreeParentParam = Param.CPQ_Columns['TreeParentParam']
    TreeSuperParentParam = Param.CPQ_Columns['TreeSuperParentParam']
    TreeTopSuperParentParam = Param.CPQ_Columns['TreeTopSuperParentParam']
    userId = Param.CPQ_Columns['Userid']
    userName = Param.CPQ_Columns['Username']
    quote_revision_record_id = Param.CPQ_Columns['quote_revision_record_id']
except: 
    TreeParam = ""
    TreeParentParam = ""
    TreeSuperParentParam = ""
    TreeTopSuperParentParam = ""
    userId = ""
    userName = ""
    quote_revision_record_id = ""

if LEVEL == 'PREDEFINED WAFER DRIVER':
    ApiResponse = ApiResponseFactory.JsonResponse(PreDefinedWaferNode())