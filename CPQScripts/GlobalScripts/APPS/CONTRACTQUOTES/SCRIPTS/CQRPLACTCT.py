# =========================================================================================================================================
#   __script_name : CQRPLACTCT.PY
#   __script_description : THIS SCRIPT IS USED TO REPLACE ACCOUNT AND CONTACT WHEN USER CLICKS ON REPLACE BUTTON ON A RELATED LIST RECORD.
#   __primary_author__ : WASIM ABDUL
#   __create_date : 19/10/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import datetime
from datetime import datetime
Sql = SQL()
import SYCNGEGUID as CPQID


Sql = SQL()
ScriptExecutor = ScriptExecutor
contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
#def replace_contact(repalce_values,cont_rec_id,table_name):
    #Trace.Write("repalce_values===="+str(repalce_values))
    #Trace.Write("cont_rec_id===="+str(cont_rec_id))
    #Trace.Write("table_name===="+str(table_name)) 
    #con_data_chk = Sql.GetFirst("Select * from SAQICT(NOLOCK) WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}' AND QUOTE_REV_INVOLVED_PARTY_CONTACT_ID ='{}'".format(contract_quote_record_id,quote_revision_record_id,cont_rec_id))
    #rpl_con_data_chk =Sql.GetFirst("Select * FROM SACONT(NOLOCK) WHERE CONTACT_RECORD_ID = '{}'".format(repalce_values))
    #if con_data_chk:
     #   delete_saqict = ("DELETE SAQICT WHERE QUOTE_REV_INVOLVED_PARTY_CONTACT_ID ='{}'".format(cont_rec_id))
      #  Sql.RunQuery(delete_saqict)
       # tableInfo = Sql.GetTable("SAQICT")
        #row = {}	
        #row['CITY'] = rpl_con_data_chk.CITY
        #row['CONTACT_ID'] = rpl_con_data_chk.CONTACT_ID
        #row['CONTACT_NAME'] = rpl_con_data_chk.CONTACT_NAME
        #row['CONTACT_RECORD_ID'] = rpl_con_data_chk.CONTACT_RECORD_ID
        #row['COUNTRY'] = rpl_con_data_chk.COUNTRY
        #row['COUNTRY_RECORD_ID'] = rpl_con_data_chk.COUNTRY_RECORD_ID
        #row['EMAIL'] = rpl_con_data_chk.EMAIL
        #row['PHONE'] = rpl_con_data_chk.PHONE
        #row['POSTAL_CODE'] = rpl_con_data_chk.POSTAL_CODE
        #row['QUOTE_RECORD_ID'] = contract_quote_record_id
        #row['QTEREV_RECORD_ID'] = quote_revision_record_id
        #row['QUOTE_REV_INVOLVED_PARTY_CONTACT_ID'] = cont_rec_id
        #tableInfo.AddRow(row)
        #SqlHelper.Upsert(tableInfo)
        #update_saqict="UPDATE SAQICT SET CITY = '{city}',CONTACT_ID = '{contact_id}',CONTACT_NAME = '{contact_name}',CONTACT_RECORD_ID = '{contact_rec_id}',COUNTRY ='{country}',COUNTRY_RECORD_ID ='{country_rec_id}',EMAIL = '{email}',PHONE ='{phone}',POSTAL_CODE ='{postalcode}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and QUOTE_REV_INVOLVED_PARTY_CONTACT_ID ='{cont_rec_id}'".format(city = rpl_con_data_chk.CITY,contact_id = rpl_con_data_chk.CONTACT_ID,contact_name = rpl_con_data_chk.CONTACT_NAME,contact_rec_id = rpl_con_data_chk.CONTACT_RECORD_ID,country =rpl_con_data_chk.COUNTRY,country_rec_id =rpl_con_data_chk.COUNTRY_RECORD_ID,email=rpl_con_data_chk.EMAIL,phone= rpl_con_data_chk.PHONE,postalcode =rpl_con_data_chk.POSTAL_CODE,QuoteRecordId = contract_quote_record_id,RevisionRecordId = quote_revision_record_id,cont_rec_id = cont_rec_id)
        #update_saqict = update_saqict.encode('ascii', 'ignore').decode('ascii')
        #Sql.RunQuery(update_saqict)

def add_contact(values,AllValues):
	Trace.Write("inside")
	Trace.Write("1"+str(values))
	Trace.Write("2"+str(AllValues))
	Sql.RunQuery ("""
	INSERT SAQICT (
	QUOTE_REV_INVOLVED_PARTY_CONTACT_ID,
	QUOTE_ID,
	QUOTE_RECORD_ID,
	QTEREV_ID,
	QTEREV_RECORD_ID,
	CPQTABLEENTRYADDEDBY,
	CPQTABLEENTRYDATEADDED,
	CpqTableEntryDateModified,
	CONTACT_NAME,
	CONTACT_RECORD_ID,
	CITY,
	COUNTRY,
	COUNTRY_RECORD_ID,
	STATE,
	STATE_RECORD_ID,
	EMAIL,
	PHONE,
	POSTAL_CODE

	) SELECT
	CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_INVOLVED_PARTY_CONTACT_ID,
	'{quoteid}' as QUOTE_ID,
	'{quotrecid}' as QUOTE_RECORD_ID,
	'{quoterevid}' as QTEREV_ID,
	'{quoterevrecid}' as QTEREV_RECORD_ID,
	'TEST' AS CPQTABLEENTRYADDEDBY,
	GETDATE() as CPQTABLEENTRYDATEADDED,
	GETDATE() as CpqTableEntryDateModified,
	SACONT.CONTACT_NAME,
	SACONT.CONTACT_RECORD_ID,
	SACONT.CITY,
	SACONT.COUNTRY,
	SACONT.COUNTRY_RECORD_ID,
	SACONT.STATE,
	SACONT.STATE_RECORD_ID,
	SACONT.EMAIL,
	SACONT.PHONE,
	SACONT.POSTAL_CODE
	FROM SACONT (NOLOCK)
	WHERE
	SACONT.CONTACT_RECORD_ID IN ('{val}')
	""".format(val = val,quoteid =getquotedetails.QUOTE_ID,quotrecid=getquotedetails.MASTER_TABLE_QUOTE_RECORD_ID,quoterevid = getquotedetails.QTEREV_ID,quoterevrecid =getquotedetails.QTEREV_RECORD_ID))





try:
	repalce_values = Param.repalce_values
	cont_rec_id = Param.cont_rec_id
	table_name = Param.table_name
	AllValues = Param.AllValues
	values = Param.Values
	action_type = Param.ActionType

except:
	repalce_values =''
	cont_rec_id = ''
	table_name = ''
	all_values = ''
	values = ''
	action_type = ''

Trace.Write("inside"+str(action_type))

if action_type == "ADD_CONTACTS":
	ApiResponse = ApiResponseFactory.JsonResponse(add_contact(values,AllValues))