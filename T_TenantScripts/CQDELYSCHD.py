# =========================================================================================================================================
#   __script_name : CQDELYSCHD.PY
#   __script_description : THIS SCRIPT IS USED TO  update,delete, insert in delivery schedule based on quantiy and delivery schedule change
#   __create_date : 27/01/2022
#   Ã‚Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import sys
import System.Net
import datetime
import time
from datetime import timedelta , date

Sql = SQL()

#A055S000P01-14051 start


def delete_deliverydetails(rec_id,QuoteRecordId,rev_rec_id,Service_id):
	get_delivery_schedule_details = Sql.GetFirst("SELECT * from SAQSPD where QUOTE_RECORD_ID = '{contract_rec_id}' AND QTEREV_RECORD_ID = '{qt_rev_id}' and QTEREVSPT_RECORD_ID = '{rec_id}'".format(contract_rec_id= QuoteRecordId,qt_rev_id = rev_rec_id,rec_id=rec_id) )
	if get_delivery_schedule_details:
		delete_delivery_schedules = Sql.RunQuery("DELETE  FROM SAQSPD where QUOTE_RECORD_ID = '{contract_rec_id}' AND QTEREV_RECORD_ID = '{qt_rev_id}' and QTEREVSPT_RECORD_ID = '{rec_id}'".format(contract_rec_id= QuoteRecordId,qt_rev_id = rev_rec_id,rec_id=rec_id) )
	return 'data'

def periods_insert(contract_quote_record_id,quote_revision_record_id):
	count = Sql.GetFirst("SELECT COUNT(*) as CNT FROM SAQRDS WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
	if count.CNT==0:
		quotedetails = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'")
		getQuote_details = Sql.GetFirst("SELECT QUOTE_ID,QTEREV_ID FROM SAQTRV WHERE QUOTE_REVISION_RECORD_ID = '"+str(rev_rec_id)+"' ")
		contract_start_date = str(quotedetails.CONTRACT_VALID_FROM).split(' ')[0]
		contract_end_date = str(quotedetails.CONTRACT_VALID_TO).split(' ')[0]
		start_date = datetime.datetime.strptime(contract_start_date, '%m/%d/%Y')
		end_date = datetime.datetime.strptime(contract_end_date, '%m/%d/%Y')
		diff1 = end_date - start_date
		get_totalweeks,remainder = divmod(diff1.days,7)
		countweeks =0
		for index in range(0, get_totalweeks):
			countweeks += 1
			#Trace.Write('countweeks--'+str(countweeks))
			billing_date = start_date + datetime.timedelta(days=(7*countweeks))
			Query = "INSERT SAQRDS (QUOTE_REV_DELIVERY_SCHEDULE_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,DELIVERY_DATE,DELIVERY_PERIOD) select CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_DELIVERY_SCHEDULE_RECORD_ID,'{quote_id}' as QUOTE_ID,'{contract_rec_id}' as QUOTE_RECORD_ID,'{qt_rev_id}' as QTEREV_ID,'{qt_rev_recid}' as QTEREV_RECORD_ID,'{delivery_date}' as DELIVERY_DATE,'{delivery_period}' as DELIVERY_PERIOD ".format(quote_id=getQuote_details.QUOTE_ID,contract_rec_id= contract_quote_record_id,qt_rev_id = getQuote_details.QTEREV_ID,qt_rev_recid = quote_revision_record_id,delivery_date =billing_date,delivery_period=index+1)
			periods_insert = Sql.RunQuery(Query)

def  insert_qty_deliverydetails(rec_id,QuoteRecordId,rev_rec_id,Service_id,QTY):
	#delete_deliverydetails(rec_id,QuoteRecordId,rev_rec_id,Service_id)
	#get_delivery_schedule_details = Sql.GetFirst("SELECT * from SAQSPD where QUOTE_RECORD_ID = '{contract_rec_id}' AND QTEREV_RECORD_ID = '{qt_rev_id}' and QTEREVSPT_RECORD_ID = '{rec_id}'".format(contract_rec_id= QuoteRecordId,qt_rev_id = rev_rec_id,rec_id=rec_id) )
	#if get_delivery_schedule_details:
		#delete_delivery_schedules = Sql.RunQuery("DELETE  FROM SAQSPD where QUOTE_RECORD_ID = '{contract_rec_id}' AND QTEREV_RECORD_ID = '{qt_rev_id}' and QTEREVSPT_RECORD_ID = '{rec_id}'".format(contract_rec_id= QuoteRecordId,qt_rev_id = rev_rec_id,rec_id=rec_id))
	quotedetails = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(QuoteRecordId,rev_rec_id))
	contract_start_date = quotedetails.CONTRACT_VALID_FROM
	contract_end_date = quotedetails.CONTRACT_VALID_TO
	start_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_start_date), '%m/%d/%Y')
	end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_end_date), '%m/%d/%Y')
	diff1 = end_date - start_date
	get_totalweeks,remainder = divmod(diff1.days,7)
	count = 0
	for index in range(0, get_totalweeks):
		delivery_week_date="DATEADD(week, {weeks}, '{DeliveryDate}')".format(weeks=index, DeliveryDate=start_date.strftime('%m/%d/%Y'))
		count += 1
		Delivery = 'Delivery {}'.format(count)
		getschedule_details = Sql.RunQuery("INSERT SAQSPD  (QUOTE_REV_PO_PART_DELIVERY_SCHEDULES_RECORD_ID,DELIVERY_SCHED_CAT,DELIVERY_SCHED_DATE,PART_DESCRIPTION,PART_RECORD_ID,QUANTITY,PART_NUMBER,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREVSPT_RECORD_ID,QTEREV_RECORD_ID,CUSTOMER_PART_NUMBER_RECORD_ID,CUSTOMER_PART_NUMBER,CUSTOMER_ANNUAL_QUANTITY,DELIVERY_MODE,SCHEDULED_MODE,MATERIALSTATUS_ID,MATERIALSTATUS_RECORD_ID,SALESUOM_ID,SALESUOM_RECORD_ID,MATPRIGRP_ID,UOM_ID,DELIVERY_SCHEDULE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,UOM_RECORD_ID)  select CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_PART_DELIVERY_SCHEDULES_RECORD_ID,'{Delivery}' as DELIVERY_SCHED_CAT,{delivery_date} as DELIVERY_SCHED_DATE,PART_DESCRIPTION,PART_RECORD_ID, {value} as QUANTITY,PART_NUMBER,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QUOTE_SERVICE_PART_RECORD_ID as QTEREVSPT_RECORD_ID,QTEREV_RECORD_ID,CUSTOMER_PART_NUMBER_RECORD_ID,CUSTOMER_PART_NUMBER,CUSTOMER_ANNUAL_QUANTITY,DELIVERY_MODE,SCHEDULE_MODE as SCHEDULED_MODE,MATERIALSTATUS_ID,MATERIALSTATUS_RECORD_ID,SALESUOM_ID,SALESUOM_RECORD_ID,MATPRIGRP_ID,BASEUOM_ID as UOM_ID,'{deli_sch}' as DELIVERY_SCHEDULE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,BASEUOM_RECORD_ID as UOM_RECORD_ID FROM SAQSPT where SCHEDULE_MODE= 'SCHEDULED' and DELIVERY_MODE = 'OFFSITE' and QUOTE_RECORD_ID = '{contract_rec_id}' AND QTEREV_RECORD_ID = '{qt_rev_id}' and QUOTE_SERVICE_PART_RECORD_ID = '{rec_id}' and CUSTOMER_ANNUAL_QUANTITY > 0".format(delivery_date =delivery_week_date,contract_rec_id= QuoteRecordId,qt_rev_id = rev_rec_id,rec_id=rec_id,value=0,Delivery=Delivery,deli_sch='WEEKLY') )
		
	return 'data'


try:
	Action =Param.Action
except:
	Action = ""
try:
	rec_id =Param.rec_id
except:
	rec_id = ''
try:
	QuoteRecordId = Param.QuoteRecordId
except:
	QuoteRecordId = ''
try:
	rev_rec_id = Param.rev_rec_id
except:
	rev_rec_id = ''
try:
	Service_id = Param.Service_id
except:
	Service_id = ''
try:
	QTY = Param.QTY
except:
	QTY = ''
if Action == "INSERT":
	#insert_deliverydetails = insert_deliveryschedule_request(rec_id,QuoteRecordId,rev_rec_id,Service_id)
	insert_periods = periods_insert(QuoteRecordId,rev_rec_id)
elif Action == "DELETE":
	delete_deliverydetails = delete_deliverydetails(rec_id,QuoteRecordId,rev_rec_id,Service_id)
elif Action == "INSERT_QTY":
	insert_qty_deliverydetails = insert_qty_deliverydetails(rec_id,QuoteRecordId,rev_rec_id,Service_id,QTY)
elif Action == "INSERT_BULK_QTY":
	insert_qty_deliverydetails = insert_qty_deliverydetails(rec_id,QuoteRecordId,rev_rec_id,Service_id,QTY)