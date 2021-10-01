# =========================================================================================================================================
#   __script_name : CQVLDPRDEF.PY
#   __script_description : THIS SCRIPT IS USED FOR PREDEFINED VALUES IN VALUE DRIVER (GETS TRIGGERED AFTER IFLOW SCRIPT - CQTVLDRIFW.py)
#   __primary_author__ : 
#   __create_date :06-09-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
import re
import datetime
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
from SYDATABASE import SQL
Sql = SQL()

try:
    quote_record_id = Param.CPQ_Columns['Quote'] 
except:
    quote_record_id = ""
try:
    LEVEL = Param.CPQ_Columns['Level']
except:
    LEVEL = ""
try:
    TreeParam = Param.CPQ_Columns['TreeParam']   
    userId = Param.CPQ_Columns['Userid']
    quote_revision_record_id = Param.CPQ_Columns['quote_revision_record_id']
except: 
    TreeParam = ""
    userId = ""
    quote_revision_record_id = ""
	
Log.Info('predefined script started')	
def wafernode_predefinedlogic(entitlement_string, equipment_record_id):
    getwafernode_logicdetails = Sql.GetFirst(""" SELECT M.VALDRV_WAFERNODE as VALDRV_WAFERNODE , P.ENTITLEMENT_VALUE_CODE as ENTITLEMENT_VALUE_CODE FROM MAEQUP M JOIN PRENVL P ON M.VALDRV_DEVICETYPE=P.ENTITLEMENT_DISPLAY_VALUE WHERE M.EQUIPMENT_RECORD_ID='{}' """.format(str(equipment_record_id)))
    entitlement_string = re.sub('<ENTITLEMENT_DISPLAY_VALUE>[^>]*?</ENTITLEMENT_DISPLAY_VALUE>','<ENTITLEMENT_DISPLAY_VALUE>'+str(getwafernode_logicdetails.VALDRV_WAFERNODE)+'</ENTITLEMENT_DISPLAY_VALUE>',entitlement_string)
    entitlement_string = re.sub('<ENTITLEMENT_VALUE_CODE>[^>]*?</ENTITLEMENT_VALUE_CODE>','<ENTITLEMENT_VALUE_CODE>'+str(getwafernode_logicdetails.ENTITLEMENT_VALUE_CODE)+'</ENTITLEMENT_VALUE_CODE>',entitlement_string)
    return entitlement_string

def devicetype_predefinedlogic(entitlement_string, equipment_record_id):
    getdevicetype_logicdetails = Sql.GetFirst(""" SELECT M.VALDRV_DEVICETYPE as VALDRV_DEVICETYPE, P.ENTITLEMENT_VALUE_CODE as ENTITLEMENT_VALUE_CODE FROM MAEQUP M JOIN PRENVL P ON M.VALDRV_DEVICETYPE=P.ENTITLEMENT_DISPLAY_VALUE WHERE M.EQUIPMENT_RECORD_ID='{}' """.format(str(equipment_record_id)))
    entitlement_string = re.sub('<ENTITLEMENT_DISPLAY_VALUE>[^>]*?</ENTITLEMENT_DISPLAY_VALUE>','<ENTITLEMENT_DISPLAY_VALUE>'+str(getdevicetype_logicdetails.VALDRV_DEVICETYPE)+'</ENTITLEMENT_DISPLAY_VALUE>',entitlement_string)
    entitlement_string = re.sub('<ENTITLEMENT_VALUE_CODE>[^>]*?</ENTITLEMENT_VALUE_CODE>','<ENTITLEMENT_VALUE_CODE>'+str(getdevicetype_logicdetails.ENTITLEMENT_VALUE_CODE)+'</ENTITLEMENT_VALUE_CODE>',entitlement_string)
    return entitlement_string


getallequip_recid = Sql.GetList(""" SELECT EQUIPMENT_RECORD_ID FROM SAQSCE WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' """.format(str(quote_record_id), str(quote_revision_record_id)))

for equip_id in getallequip_recid:
    getxml_equip_recid = Sql.GetList(""" SELECT ENTITLEMENT_XML FROM SAQSCE WHERE EQUIPMENT_RECORD_ID='{}' QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' """ .format(str(equip_id.EQUIPMENT_RECORD_ID), str(quote_record_id), str(quote_revision_record_id)))
    
    input_xml = getxml_equip_recid.ENTITLEMENT_XML

    ref_dict = {'AGS_Z0091_VAL_WAFNOD': wafernode_predefinedlogic,'AGS_Z0091_VAL_DEVTYP': devicetype_predefinedlogic}

    entxmldict = {}
    final_xml=''
    pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
    pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')

    for m in re.finditer(pattern_tag, input_xml):
        sub_string = m.group(1)
        x=re.findall(pattern_name,sub_string)
        entxmldict[x[0]]=sub_string

    for key in ref_dict:
        if entxmldict[key]:
            entxmldict[key] = ref_dict[key](entxmldict[key],equip_id.EQUIPMENT_RECORD_ID)
            final_xml += entxmldict[key]
        else:
            final_xml += entxmldict[key]

    Sql.RunQuery( "UPDATE SAQSCE SET ENTITLEMENT_XML = ''{}'' WHERE QUOTE_RECORD_ID = '{}' AND EQUIPMENT_RECORD_ID = '{}' AND QTEREV_RECORD_ID='{}'".format(final_xml, quote_record_id, equip_id.EQUIPMENT_RECORD_ID, quote_revision_record_id) )
			


##fn call