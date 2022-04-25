#   __script_name : CQBILLEDIT.PY
#   __script_description : THIS SCRIPT IS USED TO EDIT A RECORD WHEN THE USER CLICKS ON THE GRID.
#   __primary_author__ : DHURGA
#   __create_date : 17/11/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import re

#gettotalannualamt = ""
SubTab = getdatestart = getmonthavle = getmonthavl = ""
Sql = SQL()
ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
get_total_qty =0
def remove_list(t):
	return t[3:]
get_billig_date_list = []
def BILLEDIT_SAVE(GET_DICT,totalyear,getedited_amt,TreeParam,TreeParentParam):
	Trace.Write(str(TreeParam)+'--TreeParentParam---'+str(TreeParentParam)+'---BULK EDIT SAVE BILLING MATRIX--inside function---GET_DICT----'+str(GET_DICT))
	count = 0
	for val in GET_DICT:
		count += 1
		value = val.split('-')
		getmonthavl = value[1].replace("/",'-').strip()		
		getamtval = re.findall(r"\d",str(totalyear))
		SubTab = getamtval[0]
		getannual_amt = value[3]
		getline = value[4]
		get_billig_date_list.append(value[1])
		Trace.Write('-count---'+str(count))
		#Trace.Write('edited value-----'+str(BT= value[2].replace(",","")))
		Trace.Write('getannual_amt--1111111----'+str(getannual_amt))
		#getannual_amt = getannual_amt.replace(',','')
		getannual_amt = getannual_amt.split(" ",1)[0]
		Trace.Write('getannual_amt---32----'+str(getannual_amt))
		gettotalamt_beforeupdate = Sql.GetFirst("SELECT SUM(BILLING_VALUE) as ANNUAL_BILLING_AMOUNT,SUM(ESTVAL_INGL_CURR) as ESTVAL_INGL_CURR,SERVICE_ID,BILLING_TYPE FROM SAQIBP WHERE  QUOTE_RECORD_ID ='{cq}' and SERVICE_ID = '{service_id_param}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and LINE='{getline}' and EQUIPMENT_ID = '{EID}' and BILLING_DATE NOT IN {BD} GROUP BY SERVICE_ID,BILLING_TYPE".format(cq=str(ContractRecordId),EID=value[0],service_id_param=TreeParam,getline=getline, revision_rec_id = quote_revision_record_id ,BD=str(tuple(get_billig_date_list)).replace(',)',')') ))
		gettotalamt =0
		gettotalamt_update =0
		if str(gettotalamt_beforeupdate.BILLING_TYPE).upper() == "FIXED":
			Trace.Write('40--ANNUAL_BILLING_AMOUNT---'+str(gettotalamt_beforeupdate.BILLING_TYPE))
			gettotalamt = gettotalamt_beforeupdate.ANNUAL_BILLING_AMOUNT
			if gettotalamt_beforeupdate:
				gettotalamt_update = float(gettotalamt_beforeupdate.ANNUAL_BILLING_AMOUNT)+float(value[2].replace(",",""))
		else:
			Trace.Write('45--EST_VAL_GLOBAL----'+str(gettotalamt_beforeupdate.ANNUAL_BILLING_AMOUNT))
			gettotalamt = gettotalamt_beforeupdate.ESTVAL_INGL_CURR
			if gettotalamt_beforeupdate:
				gettotalamt_update = float(gettotalamt_beforeupdate.ESTVAL_INGL_CURR)+float(value[2].replace(",",""))
		Trace.Write('gettotalamt_update-BILLING_TYPE-----'+str(gettotalamt_beforeupdate.BILLING_TYPE))
		Trace.Write("gettotalamt_updat+++++++>>>>>>>"+str(gettotalamt_update))
		Trace.Write("getannual_amt+++++++>>>>>>>"+str(getannual_amt))
		if float(gettotalamt_update) < float(getannual_amt):
			if str(gettotalamt_beforeupdate.BILLING_TYPE).upper() == "FIXED":
				edit_billmatrix = "UPDATE SAQIBP SET BILLING_VALUE = {BT} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  EQUIPMENT_ID ='{EID}' and SERVICE_ID = '{service_id_param}' and LINE='{getline}' and BILLING_DATE = '{BD}'".format(BT= value[2].replace(",",""),service_id_param=TreeParam,CT = str(ContractRecordId),EID=value[0],BD = value[1],getline=getline, revision_rec_id = quote_revision_record_id)
				Sql.RunQuery(edit_billmatrix)
			else:
				edit_billmatrix = "UPDATE SAQIBP SET ESTVAL_INGL_CURR = {BT} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  EQUIPMENT_ID ='{EID}' and SERVICE_ID = '{service_id_param}' and BILLING_DATE = '{BD}' and LINE='{getline}'".format(BT= value[2].replace(",",""),service_id_param=TreeParam,CT = str(ContractRecordId),EID=value[0],BD = value[1],getline=getline, revision_rec_id = quote_revision_record_id)
				Sql.RunQuery(edit_billmatrix)
			# getmonthvalue = Sql.GetFirst("select * from QT__Billing_Matrix_Header where QUOTE_RECORD_ID ='{CT}' and YEAR  = {BL}".format(BL =int(SubTab),CT = str(ContractRecordId)))
			# if getmonthvalue:
			# 	if getmonthvalue.MONTH_1 == getmonthavl:
			# 		getmonthavle = "MONTH_1"
			# 	elif getmonthvalue.MONTH_2 == getmonthavl:
			# 		getmonthavle = "MONTH_2"
			# 	elif getmonthvalue.MONTH_3 == getmonthavl:
			# 		getmonthavle = "MONTH_3"
			# 	elif getmonthvalue.MONTH_4 == getmonthavl:
			# 		getmonthavle = "MONTH_4"
			# 	elif getmonthvalue.MONTH_5 == getmonthavl:
			# 		getmonthavle = "MONTH_5"
			# 	elif getmonthvalue.MONTH_6 == getmonthavl:
			# 		getmonthavle = "MONTH_6"
			# 	elif getmonthvalue.MONTH_7 == getmonthavl:
			# 		getmonthavle = "MONTH_7"
			# 	elif getmonthvalue.MONTH_8 == getmonthavl:
			# 		getmonthavle = "MONTH_8"
			# 	elif getmonthvalue.MONTH_9 == getmonthavl:
			# 		getmonthavle = "MONTH_9"
			# 	elif getmonthvalue.MONTH_10 == getmonthavl:
			# 		getmonthavle = "MONTH_10"
			# 	elif getmonthvalue.MONTH_11 == getmonthavl:
			# 		getmonthavle = "MONTH_11"
			# 	else:
			# 		getmonthavle = "MONTH_12"
			#sqlforupdate = "UPDATE QT__BM_YEAR_1 SET {gmon} = {BT} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  EQUIPMENT_ID ='{EID}' and BILLING_YEAR = {BL}".format(BL =int(SubTab) ,gmon = getmonthavle,BT= value[2].replace(",",""),CT = str(ContractRecordId),EID=value[0],BD = value[1], revision_rec_id = quote_revision_record_id)
			#Sql.RunQuery(sqlforupdatePT)
			#Sql.RunQuery(sqlforupdate)
			
			#to update total amount
			
			end = int(SubTab.split(' ')[-1]) * 12
			start = end - 12 + 1
			billing_date_column = ""
			item_billing_plans_obj = Sql.GetList("""SELECT FORMAT(BILLING_DATE, 'MM-dd-yyyy') as BILLING_DATE,BILLDATE=CONVERT(VARCHAR(11),BILLING_DATE,121) FROM (SELECT ROW_NUMBER() OVER(ORDER BY BILLING_DATE)
												AS ROW, * FROM (SELECT DISTINCT BILLING_DATE
																	FROM SAQIBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID ='{}' GROUP BY EQUIPMENT_ID, BILLING_DATE) IQ) OQ WHERE OQ.ROW BETWEEN {} AND {}""".format(
																		ContractRecordId,quote_revision_record_id, start, end))
			if item_billing_plans_obj:
				billing_date_column = [item_billing_plan_obj.BILLDATE for item_billing_plan_obj in item_billing_plans_obj]
				Trace.Write(str(tuple(billing_date_column))+'billing_date_column---'+str(billing_date_column))
			pivot_columns = ",".join(['{}'.format(billing_date) for billing_date in billing_date_column])
			Trace.Write(str(tuple(billing_date_column))+'billing_date_column---'+str(pivot_columns))
			gettotalannualamt =''
			gettotalamt = Sql.GetFirst("SELECT BILLING_VALUE=SUM(BILLING_VALUE),SUM(ESTVAL_INGL_CURR) as ESTVAL_INGL_CURR FROM SAQIBP WHERE CONVERT(VARCHAR(11),BILLING_DATE,121) in {pn} and QUOTE_RECORD_ID ='{cq}' AND SERVICE_ID = '{service_id_param}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and EQUIPMENT_ID = '{EID}' and LINE='{getline}'".format(pn=tuple(billing_date_column),service_id_param=TreeParam,cq=str(ContractRecordId),EID=value[0], revision_rec_id = quote_revision_record_id,getline=getline ))
			
			if gettotalamt:
				if str(gettotalamt_beforeupdate.BILLING_TYPE).upper() == "FIXED":
					gettotalannualamt = gettotalamt.BILLING_VALUE
				else:
					gettotalannualamt = gettotalamt.ESTVAL_INGL_CURR
			Trace.Write('gettotalannualamt---'+str(gettotalannualamt))
			
			annual_sqlforupdatePTA = "UPDATE SAQIBP SET ANNUAL_BILLING_AMOUNT = {BTN} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  EQUIPMENT_ID ='{EID}' and BILLING_DATE in {BD} and LINE='{getline}' AND SERVICE_ID = '{service_id_param}' ".format(BTN= gettotalannualamt,CT = str(ContractRecordId),EID=value[0],BD = tuple(billing_date_column),service_id_param=TreeParam, revision_rec_id = quote_revision_record_id,getline=getline)
			#Sql.RunQuery(annual_sqlforupdatePTA)
			#sqlforupdate = "UPDATE QT__BM_YEAR_1 SET ANNUAL_BILLING_AMOUNT = {BTN} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  EQUIPMENT_ID ='{EID}' and BILLING_YEAR = {BL}".format(BL=int(SubTab),BTN= gettotalannualamt,CT = str(ContractRecordId),EID=value[0], revision_rec_id = quote_revision_record_id)
			
			#Sql.RunQuery(sqlforupdate)
			savebill =''
			#return 'save',savebill
		else:
			savebill = 'NOTSAVE'
	return 'not saved',savebill

try:
	GET_DICT =list(Param.billdict)
	
	#getedited_amt = Param.getedited_amt
except:
	Trace.Write('131---')
	GET_DICT = []
	#totalyear = "" 
	#getedited_amt = ""
try:
	totalyear = Param.totalyear
except:
	totalyear = ""
try:
	getedited_amt = Param.getedited_amt
except:
	getedited_amt = ""
try:
	TreeParentParam = Param.TreeParentParam
except:
	TreeParentParam = ""
try:
	TreeParam = Param.TreeParam
except:
	TreeParam = ""

ApiResponse = ApiResponseFactory.JsonResponse(BILLEDIT_SAVE(GET_DICT,totalyear,getedited_amt,TreeParam,TreeParentParam))