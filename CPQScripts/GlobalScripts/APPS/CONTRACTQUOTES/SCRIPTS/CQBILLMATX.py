# =========================================================================================================================================
#   __script_name : CQBILLMATX.PY
#   __script_description : THIS SCRIPT IS USED TO  genarte billing matrix
#   __primary_author__ : DHURGA GOPALAKRISHNAN
#   __create_date : 05/01/2022
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import re
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import datetime
import sys


Param = Param 
Sql = SQL()
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct() or "Sales"
input_data = [str(param_result.Value) for param_result in Param.CPQ_Columns]
Qt_rec_id = input_data[0]
REVISION_rec_ID = input_data[-1]

Log.Info("Billing---started-----"+str(Qt_rec_id)+"--REVISION_rec_ID---"+str(REVISION_rec_ID))
try:
	contract_quote_rec_id = input_data[0]
	#contract_quote_rec_id = Param.Quote_Record_ID
except:
	contract_quote_rec_id = ''
try:
	quote_revision_rec_id = input_data[-1]	
except:
	quote_revision_rec_id =  ""
try:
	current_prod = Product.Name	
except:
	current_prod = "Sales"
try:
	TabName = TestProduct.CurrentTab
except:
	TabName = "Quotes"
user_id = str(User.Id)
user_name = str(User.UserName)

#A055S000P01-3924-billing matrix creation start
def _insert_billing_matrix():

	Sql.RunQuery("""
			INSERT SAQRIB (
			QUOTE_BILLING_PLAN_RECORD_ID,
			BILLING_END_DATE,
			BILLING_DAY,
			BILLING_START_DATE,
			QUOTE_ID,
			QUOTE_NAME,
			QUOTE_RECORD_ID,
			QTEREV_ID,
			QTEREV_RECORD_ID,
			CPQTABLEENTRYADDEDBY,
			CPQTABLEENTRYDATEADDED,
			CpqTableEntryModifiedBy,
			CpqTableEntryDateModified,
			SALESORG_ID,
			SALESORG_NAME,
			SALESORG_RECORD_ID,
			PRDOFR_ID,
			PRDOFR_RECORD_ID
			) 
			SELECT 
			CONVERT(VARCHAR(4000),NEWID()) as QUOTE_BILLING_PLAN_RECORD_ID,
			SAQTMT.CONTRACT_VALID_TO as BILLING_END_DATE,
			30 as BILLING_DAY,
			SAQTMT.CONTRACT_VALID_FROM as BILLING_START_DATE,
			SAQTMT.QUOTE_ID,
			SAQTMT.QUOTE_NAME,
			SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID as QUOTE_RECORD_ID,
			SAQTMT.QTEREV_ID as QTEREV_ID,
			SAQTMT.QTEREV_RECORD_ID as QTEREV_RECORD_ID,
			'{UserName}' AS CPQTABLEENTRYADDEDBY,
			GETDATE() as CPQTABLEENTRYDATEADDED,
			{UserId} as CpqTableEntryModifiedBy,
			GETDATE() as CpqTableEntryDateModified,
			SAQTSV.SALESORG_ID,
			SAQTSV.SALESORG_NAME,
			SAQTSV.SALESORG_RECORD_ID,
			SAQTSV.SERVICE_ID,
			SAQTSV.SERVICE_RECORD_ID                   
			FROM SAQTMT (NOLOCK) JOIN SAQTSV on SAQTSV.QUOTE_ID = SAQTMT.QUOTE_ID
			
			WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTMT.QTEREV_RECORD_ID = '{RevisionRecordId}'
			AND SAQTSV.SERVICE_ID NOT IN ('Z0101','A6200','Z0108','Z0110') AND SAQTSV.SERVICE_ID NOT IN (SELECT PRDOFR_ID FROM SAQRIB (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}')
													
	""".format(                        
		QuoteRecordId= contract_quote_rec_id,
		RevisionRecordId=quote_revision_rec_id,
		UserId=user_id,
		UserName=user_name
	))
	#Not required right now for SAQTBP.
	#AND JQ.ENTITLEMENT_NAME IN ('FIXED_PRICE_PER_RESOU_EVENT_91','FIXED_PRICE_PER_RESOU_EVENT_92') 
	#AND JQ.ENTITLEMENT_VALUE_CODE = 'FIXED PRICE'
	#BM_line_item_start_time = time.time()
	billingmatrix_create()
	#BM_line_item_end_time = time.time()		
	return True

def insert_items_billing_plan(total_months=1, billing_date='',billing_end_date ='', amount_column='YEAR_1', entitlement_obj=None,service_id=None,get_ent_val_type =None,get_ent_billing_type_value=None,get_billling_data_dict=None):
	get_billing_cycle = get_billing_type = ''
	#Trace.Write(str(service_id)+'--get_billling_data_dict--'+str(get_billling_data_dict))
	Trace.Write(str(service_id)+'get_ent_val_type--'+str(get_ent_val_type))
	for data,val in get_billling_data_dict.items():
		if 'AGS_'+str(service_id)+'_PQB_BILCYC' in data:
			get_billing_cycle = val
		elif 'AGS_'+str(service_id)+'_PQB_BILTYP' in data:
			get_billing_type =val
	#Trace.Write('get_billing_cycle---'+str(get_billing_cycle))
	Trace.Write(str(service_id)+'----billing_type---'+str(get_billing_type)+'--CYCLE---'+str(get_billing_cycle))
	if get_billing_cycle == "Monthly":				
		get_val =12
	elif str(get_billing_cycle).upper() == "QUARTERLY":			
		get_val = 4
	elif str(get_billing_cycle).upper() == "ANNUALLY":				
		get_val = 1
	else:				
		get_val =12
	amount_column_split = amount_column.replace('_',' ')
	#amount_column = 'TOTAL_AMOUNT_INGL_CURR' # Hard Coded for Sprint 5	
	if str(get_billing_type).upper() == "FIXED" and get_billing_type != '':
		#join_condition = "JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQSCO.SERVICE_ID and SAQRIT.OBJECT_ID = SAQSCO.EQUIPMENT_ID and SAQSCO.GREENBOOK = SAQRIT.GREENBOOK"
		#object_name = 'SAQSCO'
		#divide_amt = 'SAQRIT.NET_PRICE_INGL_CURR'
		#annaul_bill_amt = 'SAQRIT.NET_PRICE_INGL_CURR'
		Trace.Write(str(service_id)+'------billing_type_value-----'+str(get_ent_billing_type_value))
		Sql.RunQuery(""" INSERT SAQIBP (

					QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,
					QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
					BILLING_DATE, BILLING_YEAR,
					EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID,
					SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
					)
					SELECT
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
					{billing_end_date} as BILLING_END_DATE,
					{BillingDate} as BILLING_START_DATE,
					{amount_column}  AS ANNUAL_BILLING_AMOUNT,
					ISNULL({amount_column}, 0) / {get_val}  as BILLING_VALUE,
					{amount_column}   as  BILLING_VALUE_INGL_CURR,
					'{billing_type}' as BILLING_TYPE,
					SAQRIT.LINE AS LINE,
					SAQSCO.QUOTE_ID,
					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
					SAQRIT.COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
					SAQRIT.ESTVAL_INGL_CURR as ESTVAL_INGL_CURR,
					SAQSCO.QUOTE_RECORD_ID,
					SAQSCO.QTEREV_ID,
					SAQSCO.QTEREV_RECORD_ID,
					{BillingDate} as BILLING_DATE,
					'{amount_column_split}' as BILLING_YEAR,
					SAQSCO.EQUIPMENT_DESCRIPTION,
					SAQSCO.EQUIPMENT_ID,
					SAQSCO.EQUIPMENT_RECORD_ID,
					'' as QTEITMCOB_RECORD_ID,
					SAQSCO.SERVICE_DESCRIPTION,
					SAQSCO.SERVICE_ID,
					SAQSCO.SERVICE_RECORD_ID,
					SAQSCO.GREENBOOK,
					SAQSCO.GREENBOOK_RECORD_ID,
					SAQSCO.SERIAL_NO AS SERIAL_NUMBER,
					SAQSCO.WARRANTY_START_DATE,
					SAQSCO.WARRANTY_END_DATE,    
					{UserId} as CPQTABLEENTRYADDEDBY,
					GETDATE() as CPQTABLEENTRYDATEADDED
					FROM SAQSCO (NOLOCK) JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQSCO.SERVICE_ID and SAQRIT.OBJECT_ID = SAQSCO.EQUIPMENT_ID and SAQSCO.GREENBOOK = SAQRIT.GREENBOOK LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
					EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_PRICE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
					WHERE SAQSCO.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCO.SERVICE_ID ='{service_id}'  and SAQRIT.NET_VALUE IS NOT NULL and ISNULL(SAQRIT.OBJECT_ID,'') <> 0 )A """.format(
					UserId=user_id, QuoteRecordId=contract_quote_rec_id,
					RevisionRecordId=quote_revision_rec_id,
					BillingDate=billing_date,billing_end_date=billing_end_date,
					get_val=get_val,
					service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split))
		Sql.RunQuery(""" INSERT SAQIBP (
					QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID,DOC_CURRENCY, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,
					QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
					BILLING_DATE, BILLING_YEAR,
					EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID,
					SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
					)
					SELECT
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
					{billing_end_date} as BILLING_END_DATE,
					{BillingDate} as BILLING_START_DATE,
					{amount_column} AS ANNUAL_BILLING_AMOUNT,
					ISNULL({amount_column}, 0) / {get_val}  as BILLING_VALUE,
					ISNULL(SAQRIT.ESTVAL_INGL_CURR, 0) / {get_val}  as  BILLING_VALUE_INGL_CURR,
					'{billing_type}' as BILLING_TYPE,
					SAQRIT.LINE AS LINE,
					SAQRIT.QUOTE_ID,
					{amount_column} AS DOC_CURRENCY,
					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
					SAQRIT.COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
					SAQRIT.ESTVAL_INGL_CURR as ESTVAL_INGL_CURR,
					SAQRIT.QUOTE_RECORD_ID,
					SAQRIT.QTEREV_ID,
					SAQRIT.QTEREV_RECORD_ID,
					{BillingDate} as BILLING_DATE,
					'{amount_column_split}' as BILLING_YEAR,
					'' as EQUIPMENT_DESCRIPTION,
					SAQRIT.OBJECT_ID as EQUIPMENT_ID,
					'' as EQUIPMENT_RECORD_ID,
					'' as QTEITMCOB_RECORD_ID,
					SAQRIT.SERVICE_DESCRIPTION,
					SAQRIT.SERVICE_ID,
					SAQRIT.SERVICE_RECORD_ID,
					SAQRIT.GREENBOOK,
					SAQRIT.GREENBOOK_RECORD_ID,
					'' AS SERIAL_NUMBER,
					'' as WARRANTY_START_DATE,
					'' as WARRANTY_END_DATE,    
					{UserId} as CPQTABLEENTRYADDEDBY,
					GETDATE() as CPQTABLEENTRYDATEADDED
					FROM SAQRIT (NOLOCK)  LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
					EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_PRICE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
					WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRIT.SERVICE_ID ='{service_id}'  and SAQRIT.NET_VALUE IS NOT NULL  and ISNULL(SAQRIT.OBJECT_ID,'') = '' )A """.format(
					UserId=user_id, QuoteRecordId=contract_quote_rec_id,
					RevisionRecordId=quote_revision_rec_id,billing_end_date=billing_end_date,
					BillingDate=billing_date,
					get_val=get_val,
					service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split))
	else:		
		Sql.RunQuery("""INSERT SAQIBP (
					
					QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID,DOC_CURRENCY, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,ESTVAL_INDT_CURR,
					QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
					BILLING_DATE, BILLING_YEAR,
					EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
					SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
				) 
				SELECT 
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
					{billing_end_date} as BILLING_END_DATE,
					{BillingDate} as BILLING_START_DATE,
					{amount_column} AS ANNUAL_BILLING_AMOUNT,
					ISNULL({amount_column}, 0) / {get_val}  as BILLING_VALUE,
					ISNULL(SAQRIT.ESTVAL_INGL_CURR, 0) / {get_val}  as  BILLING_VALUE_INGL_CURR,
					'{billing_type}' as BILLING_TYPE,
					SAQRIT.LINE AS LINE,
					SAQSCO.QUOTE_ID,
					{amount_column} AS DOC_CURRENCY,
					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,	
					SAQRIT.COMVAL_INGL_CURR	 as COMMITTED_VALUE_INGL_CURR,
					SAQRIT.ESTVAL_INGL_CURR	as 	ESTVAL_INGL_CURR,
					SAQRIT.ESTIMATED_VALUE,		
					SAQSCO.QUOTE_RECORD_ID,
					SAQSCO.QTEREV_ID,
					SAQSCO.QTEREV_RECORD_ID,
					{BillingDate} as BILLING_DATE,						
					'{amount_column_split}' as BILLING_YEAR,
					SAQSCO.EQUIPMENT_DESCRIPTION,
					SAQSCO.EQUIPMENT_ID,									
					SAQSCO.EQUIPMENT_RECORD_ID,						
					'' as QTEITMCOB_RECORD_ID,
					SAQSCO.SERVICE_DESCRIPTION,
					SAQSCO.SERVICE_ID,
					SAQSCO.SERVICE_RECORD_ID, 
					SAQSCO.GREENBOOK,
					SAQSCO.GREENBOOK_RECORD_ID,
					SAQSCO.SERIAL_NO AS SERIAL_NUMBER,
					SAQSCO.WARRANTY_START_DATE,
					SAQSCO.WARRANTY_END_DATE,    
					{UserId} as CPQTABLEENTRYADDEDBY, 
					GETDATE() as CPQTABLEENTRYDATEADDED
					FROM SAQSCO (NOLOCK) JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQSCO.SERVICE_ID and SAQRIT.OBJECT_ID = SAQSCO.EQUIPMENT_ID and SAQSCO.GREENBOOK = SAQRIT.GREENBOOK LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
					EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_PRICE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
					WHERE SAQSCO.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCO.SERVICE_ID ='{service_id}'   and SAQRIT.ESTIMATED_VALUE  IS NOT NULL  and ISNULL(SAQRIT.OBJECT_ID,'') <> 0 )A """.format(
					UserId=user_id, QuoteRecordId=contract_quote_rec_id,
					RevisionRecordId=quote_revision_rec_id,billing_end_date=billing_end_date,
					BillingDate=billing_date,
					get_val=get_val,
					service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split))
		Sql.RunQuery("""INSERT SAQIBP (					
					QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID, QTEITM_RECORD_ID, COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,DOC_CURRENCY,ESTVAL_INDT_CURR,
					QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
					BILLING_DATE, BILLING_YEAR,
					EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
					SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
				) 
				SELECT 
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,  
					{billing_end_date} as BILLING_END_DATE,
					{BillingDate} as BILLING_START_DATE,
					{amount_column} AS ANNUAL_BILLING_AMOUNT,
					ISNULL({amount_column}, 0) / {get_val}  as BILLING_VALUE,
					ISNULL(NET_PRICE_INGL_CURR, 0) / {get_val}  as  BILLING_VALUE_INGL_CURR,
					'{billing_type}' as BILLING_TYPE,
					LINE,
					QUOTE_ID,
					QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
					
					COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
					ESTVAL_INGL_CURR as ESTVAL_INGL_CURR,
					{amount_column} AS DOC_CURRENCY,
					ESTIMATED_VALUE,	
					QUOTE_RECORD_ID,
					QTEREV_ID,
					QTEREV_RECORD_ID,
					{BillingDate} as BILLING_DATE,						
					'{amount_column_split}' as BILLING_YEAR,
					'' as EQUIPMENT_DESCRIPTION,
					'' as EQUIPMENT_ID,									
					'' as EQUIPMENT_RECORD_ID,						
					'' as QTEITMCOB_RECORD_ID,
					SERVICE_DESCRIPTION,
					SERVICE_ID,
					SERVICE_RECORD_ID, 
					GREENBOOK,
					GREENBOOK_RECORD_ID,
					'' AS SERIAL_NUMBER,
					'' as WARRANTY_START_DATE,
					'' as WARRANTY_END_DATE,    
					{UserId} as CPQTABLEENTRYADDEDBY, 
					GETDATE() as CPQTABLEENTRYDATEADDED
				FROM  SAQRIT (NOLOCK) 
				WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND  ESTIMATED_VALUE IS NOT NULL AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{service_id}' AND (OBJECT_ID  IS NULL OR OBJECT_ID = '')""".format(
					UserId=user_id, QuoteRecordId=contract_quote_rec_id,
					RevisionRecordId=quote_revision_rec_id,
					BillingDate=billing_date,billing_end_date=billing_end_date,
					get_val=get_val,
					service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split))
		
		'''Sql.RunQuery("""UPDATE SAQIBP 
			SET SAQIBP.ESTVAL_INDT_CURR = ISNULL(SAQIBP.ESTVAL_INGL_CURR, 0) * SAQTRV.EXCHANGE_RATE FROM SAQIBP INNER JOIN SAQTRV ON SAQIBP.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQIBP.QTEREV_RECORD_ID = SAQTRV.QTEREV_RECORD_ID WHERE SAQIBP.QUOTE_RECORD_ID='{contract_quote_rec_id}' AND SAQIBP.QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id=quote_revision_rec_id))'''

	if service_id == 'Z0116':
		update_annual_bill_amt  = Sql.GetFirst("SELECT SUM(NET_VALUE_INGL_CURR) as YEAR1 from SAQRIT (NOLOCK) where QUOTE_RECORD_ID='{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'  and SERVICE_ID = 'Z0116' GROUP BY SERVICE_ID,GREENBOOK".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id=quote_revision_rec_id))
		if update_annual_bill_amt:
			update_credit_amt = "UPDATE SAQIBP SET ANNUAL_BILLING_AMOUNT ={amt} where QUOTE_RECORD_ID='{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'  and SERVICE_ID = 'Z0116' GROUP BY SERVICE_ID,GREENBOOK ".format(amt=update_annual_bill_amt.YEAR1,contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id=quote_revision_rec_id)
			Sql.RunQuery(update_credit_amt)
	return True

def _quote_items_greenbook_summary_insert():	
	greenbook_summary_last_line_no = 0
	quote_item_summary_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQIGS (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
	if quote_item_summary_obj:
		greenbook_summary_last_line_no = int(quote_item_summary_obj.LINE) 	
	
	Sql.RunQuery("""INSERT SAQIGS (CONTRACT_VALID_FROM, CONTRACT_VALID_TO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, QTEITMSUM_RECORD_ID, COMMITTED_VALUE_INGL_CURR, ESTVAL_INGL_CURR, NET_VALUE_INGL_CURR, DOC_CURRENCY, DOCCURR_RECORD_ID, COMMITTED_VALUE, ESTIMATED_VALUE, NET_VALUE, LINE, QUOTE_REV_ITEM_GREENBK_SUMRY_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
		SELECT IQ.*, ROW_NUMBER()OVER(ORDER BY(IQ.GREENBOOK)) + {ItemGreenbookSummaryLastLineNo} as LINE, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_GREENBK_SUMRY_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
			SELECT DISTINCT
				SAQTRV.CONTRACT_VALID_FROM,
				SAQTRV.CONTRACT_VALID_TO,
				SAQTRV.GLOBAL_CURRENCY,
				SAQTRV.GLOBAL_CURRENCY_RECORD_ID,						
				SQ.GREENBOOK,
				SQ.GREENBOOK_RECORD_ID,
				SQ.SERVICE_DESCRIPTION,
				SQ.SERVICE_ID,
				SQ.SERVICE_RECORD_ID,
				SAQTRV.QUOTE_ID,
				SAQTRV.QUOTE_RECORD_ID,
				SAQTMT.QTEREV_ID,
				SAQTMT.QTEREV_RECORD_ID,
				SQ.QTEITMSUM_RECORD_ID,
				SQ.COMMITTED_VALUE_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
				SQ.ESTVAL_INGL_CURR as ESTVAL_INGL_CURR,
				SQ.NET_VALUE_INGL_CURR as NET_VALUE_INGL_CURR,
				SQ.DOC_CURRENCY,
				SQ.DOCCURR_RECORD_ID as DOCCURR_RECORD_ID,
				SQ.COMMITTED_VALUE as COMMITTED_VALUE,
				SQ.ESTIMATED_VALUE as ESTIMATED_VALUE,
				SQ.NET_VALUE as NET_VALUE
			FROM (
					SELECT 
						SAQRIT.QUOTE_RECORD_ID, 
						SAQRIT.QTEREV_RECORD_ID,   
						SAQRIT.SERVICE_DESCRIPTION,
						SAQRIT.SERVICE_ID,
						SAQRIT.SERVICE_RECORD_ID,
						SAQRIT.GREENBOOK,
						SAQRIT.GREENBOOK_RECORD_ID,
						SAQRIT.QTEITMSUM_RECORD_ID,
						SUM(SAQRIT.COMMITTED_VALUE) as COMMITTED_VALUE_INGL_CURR,
						SUM(SAQRIT.ESTVAL_INGL_CURR) as ESTVAL_INGL_CURR,
						SUM(SAQRIT.NET_VALUE_INGL_CURR) as NET_VALUE_INGL_CURR,
						SAQRIT.DOC_CURRENCY,
						SAQRIT.DOCURR_RECORD_ID as DOCCURR_RECORD_ID,
						SUM(SAQRIT.COMMITTED_VALUE) as COMMITTED_VALUE,
						SUM(SAQRIT.ESTIMATED_VALUE) as ESTIMATED_VALUE,
						SUM(SAQRIT.NET_VALUE) as NET_VALUE
					FROM SAQRIT (NOLOCK) 
					WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' 
					GROUP BY SAQRIT.QUOTE_RECORD_ID, SAQRIT.QTEREV_RECORD_ID, SAQRIT.SERVICE_DESCRIPTION, SAQRIT.SERVICE_ID, SAQRIT.SERVICE_RECORD_ID, SAQRIT.GREENBOOK, SAQRIT.GREENBOOK_RECORD_ID, SAQRIT.QTEITMSUM_RECORD_ID, SAQRIT.DOC_CURRENCY, SAQRIT.DOCURR_RECORD_ID
				) SQ
			JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SQ.QTEREV_RECORD_ID     
			JOIN SAQTRV (NOLOCK) ON SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID			
			) IQ			
			LEFT JOIN SAQIGS (NOLOCK) ON SAQIGS.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQIGS.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQIGS.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQIGS.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID
			WHERE ISNULL(SAQIGS.GREENBOOK_RECORD_ID,'') = ''
	""".format(UserId=User.Id, UserName=User.UserName, QuoteRecordId= contract_quote_rec_id,QuoteRevisionRecordId=quote_revision_rec_id, ItemGreenbookSummaryLastLineNo=greenbook_summary_last_line_no))
	return True

def billingmatrix_create():
	#Trace.Write('4739---------------')
	_quote_items_greenbook_summary_insert()
	billing_plan_obj = Sql.GetList("SELECT DISTINCT PRDOFR_ID,BILLING_START_DATE,BILLING_END_DATE,BILLING_DAY FROM SAQRIB (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_rec_id))
	quotedetails = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_rec_id))
	get_billling_data_dict = {}
	contract_start_date = quotedetails.CONTRACT_VALID_FROM
	contract_end_date = quotedetails.CONTRACT_VALID_TO
	get_ent_val = get_ent_billing_type_value = get_ent_bill_cycle = get_billing_type = ''
	if contract_start_date and contract_end_date and billing_plan_obj:
		Sql.RunQuery("""DELETE FROM SAQIBP WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
		#Trace.Write('4739---------4744------')
		for val in billing_plan_obj:
			if billing_plan_obj:				
				contract_start_date = val.BILLING_START_DATE
				contract_end_date = val.BILLING_END_DATE				
				start_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_start_date), '%m/%d/%Y')
				#start_date = str(contract_start_date).split(' ')[0]
				billing_day = int(val.BILLING_DAY)
				get_service_val = val.PRDOFR_ID
				get_billing_cycle = Sql.GetFirst("select ENTITLEMENT_XML from SAQITE where QUOTE_RECORD_ID = '{qtid}' AND QTEREV_RECORD_ID = '{qt_rev_id}' and SERVICE_ID = '{get_service}'".format(qtid =contract_quote_rec_id,qt_rev_id=quote_revision_rec_id,get_service = str(get_service_val).strip()))
				if get_billing_cycle:
					updateentXML = get_billing_cycle.ENTITLEMENT_XML
					pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
					pattern_id = re.compile(r'<ENTITLEMENT_ID>(AGS_'+str(get_service_val)+'_PQB_BILCYC|AGS_'+str(get_service_val)+'_PQB_BILTYP)</ENTITLEMENT_ID>')
					#pattern_id_billing_type = re.compile(r'<ENTITLEMENT_ID>(AGS_'+str(get_service_val)+'_PQB_BILTYP|AGS_'+str(get_service_val)+'_PQB_BILTYP)</ENTITLEMENT_ID>')
					pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
					for m in re.finditer(pattern_tag, updateentXML):
						sub_string = m.group(1)
						get_ent_id = re.findall(pattern_id,sub_string)
						#get_ent_bill_type = re.findall(pattern_id_billing_type,sub_string)
						get_ent_val= re.findall(pattern_name,sub_string)
						if get_ent_id:
							get_ent_val = str(get_ent_val[0])
							get_billling_data_dict[get_ent_id[0]] = str(get_ent_val)
							#get_ent_bill_cycle = str(get_ent_val)
							for data,val in get_billling_data_dict.items():
								if 'AGS_'+str(get_service_val)+'_PQB_BILCYC' in data:
									get_ent_bill_cycle = val
								elif 'AGS_'+str(get_service_val)+'_PQB_BILTYP' in data:
									get_billing_type =val
							# if 	'AGS_'+str(get_service_val)+'_PQB_BILCYC' == str(get_ent_id[0]):
							# 	get_ent_val = str(get_ent_val)
							# 	Trace.Write(str(get_ent_val)+'---get_ent_name---'+str(get_ent_id[0]))
							# 	#get_ent_bill_cycle = get_ent_val
							# else:
							# 	get_ent_billing_type_value = str(get_ent_val)
				#Log.Info(str(get_billing_type)+'--475--'+str(get_ent_bill_cycle))
				billing_month_end = 0
				entitlement_obj = Sql.GetFirst("select convert(xml,replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39'),' < ',' &lt; ' ),' > ',' &gt; ' ),'_>','_&gt;'),'_<','_&lt;')) as ENTITLEMENT_XML,QUOTE_RECORD_ID,SERVICE_ID from SAQTSE (nolock) where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId =contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
				if str(get_ent_bill_cycle).upper() == "MONTHLY":
					if billing_day in (29,30,31):
						if start_date.month == 2:
							isLeap = lambda x: x % 4 == 0 and (x % 100 != 0 or x % 400 == 0)
							end_day = 29 if isLeap(start_date.year) else 28
							start_date = start_date.replace(day=end_day)
						elif start_date.month in (4, 6, 9, 11) and billing_day == 31:
							start_date = start_date.replace(day=30)
						else:
							start_date = start_date.replace(day=billing_day)
					else:
						start_date = start_date.replace(day=billing_day)
					end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_end_date), '%m/%d/%Y')
					#end_date = str(contract_end_date).split(' ')[0]
					diff1 = end_date - start_date

					avgyear = 365.2425        # pedants definition of a year length with leap years
					avgmonth = 365.2425/12.0  # even leap years have 12 months
					years, remainder = divmod(diff1.days, avgyear)
					years, months = int(years), int(remainder // avgmonth)            
					
					total_months = years * 12 + months
					for index in range(0, total_months+1):
						billing_month_end += 1
						insert_items_billing_plan(total_months=total_months, 
												billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
													Month=index, BillingDate=start_date.strftime('%m/%d/%Y')
													),billing_end_date="DATEADD(month, {Month_add}, '{BillingDate}')".format(
													Month_add=billing_month_end, BillingDate=start_date.strftime('%m/%d/%Y')
													), amount_column="YEAR_"+str((index/12) + 1),
													entitlement_obj=entitlement_obj,service_id = get_service_val,get_ent_val_type = get_ent_bill_cycle,get_ent_billing_type_value = get_ent_billing_type_value,get_billling_data_dict=get_billling_data_dict)
				elif str(get_ent_bill_cycle).upper() == "QUARTELY":
					ct_start_date =contract_start_date
					ct_end_date =contract_end_date
					if ct_start_date>ct_end_date:
						ct_start_date,ct_end_date=ct_end_date,ct_start_date
					m1=ct_start_date.Year*12+ct_start_date.Month  
					m2=ct_end_date.Year*12+ct_end_date.Month  
					months=m2-m1
					months=months/3
					for index in range(0, months):
						billing_month_end += 1
						insert_items_billing_plan(total_months=months, 
												billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
													Month=index, BillingDate=start_date.strftime('%m/%d/%Y')
													),billing_end_date="DATEADD(month, {Month_add}, '{BillingDate}')".format(
													Month_add=billing_month_end, BillingDate=start_date.strftime('%m/%d/%Y')
													),amount_column="YEAR_"+str((index/4) + 1),
													entitlement_obj=entitlement_obj,service_id = get_service_val,get_ent_val_type = get_ent_val,get_ent_billing_type_value=get_ent_billing_type_value,get_billling_data_dict=get_billling_data_dict)
				elif str(get_ent_bill_cycle).upper() == "ONE ITEM PER QUOTE":
					end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_end_date), '%m/%d/%Y')			
					diff1 = end_date - start_date
					Trace.Write('diff1--'+str(diff1))
					avgyear = 365.00    # even leap years have 12 months
					years, remainder = divmod(diff1.days, avgyear)
					years = int(years)
					
					Trace.Write('years--'+str(years))
					for index in range(1, years+1):
						billing_month_end += 1
						Trace.Write('billing_month_end--'+str(index))
						insert_items_billing_plan(total_months='',
													billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
														Month=index, BillingDate=start_date.strftime('%m/%d/%Y')
														),billing_end_date="DATEADD(month, {Month_add}, '{BillingDate}')".format(
														Month_add=billing_month_end, BillingDate=start_date.strftime('%m/%d/%Y')
														), amount_column="YEAR_"+str(index + 1),
														entitlement_obj=entitlement_obj,service_id = get_service_val,get_ent_val_type = get_ent_bill_cycle,get_ent_billing_type_value = get_ent_billing_type_value,get_billling_data_dict=get_billling_data_dict)
				else:
					Trace.Write('get_ent_val---'+str(get_ent_bill_cycle))
					if billing_day in (29,30,31):
						if start_date.month == 2:
							isLeap = lambda x: x % 4 == 0 and (x % 100 != 0 or x % 400 == 0)
							end_day = 29 if isLeap(start_date.year) else 28
							start_date = start_date.replace(day=end_day)
						elif start_date.month in (4, 6, 9, 11) and billing_day == 31:
							start_date = start_date.replace(day=30)
						else:
							start_date = start_date.replace(day=billing_day)
					else:
						start_date = start_date.replace(day=billing_day)
					end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_end_date), '%m/%d/%Y')			
					diff1 = end_date - start_date

					avgyear = 365.2425        # pedants definition of a year length with leap years
					avgmonth = 365.2425/12.0  # even leap years have 12 months
					years, remainder = divmod(diff1.days, avgyear)
					years, months = int(years), int(remainder // avgmonth)
					for index in range(0, years+1):
						billing_month_end += 1
						insert_items_billing_plan(total_months=years, 
												billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
													Month=index, BillingDate=start_date.strftime('%m/%d/%Y')
													),billing_end_date="DATEADD(month, {Month_add}, '{BillingDate}')".format(
													Month_add=billing_month_end, BillingDate=start_date.strftime('%m/%d/%Y')
													),amount_column="YEAR_"+str((index) + 1),
													entitlement_obj=entitlement_obj,service_id = get_service_val,get_ent_val_type = get_ent_val,get_ent_billing_type_value = get_ent_billing_type_value,get_billling_data_dict=get_billling_data_dict)
				#self.insert_quote_items_billing_plan()
#A055S000P01-3924-billing matrix creation end





if contract_quote_rec_id:
	ApiResponse = ApiResponseFactory.JsonResponse(_insert_billing_matrix())
	#insert_quote_billing_plan()