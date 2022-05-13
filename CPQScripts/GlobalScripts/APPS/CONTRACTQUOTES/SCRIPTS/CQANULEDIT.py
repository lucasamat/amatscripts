# =========================================================================================================================================
#   __script_name : CQANULEDIT.PY
#   __script_description : THIS SCRIPT IS USED TO EDIT THE ANNUAL GRID BASED ON ENTITLEMENT PRICING
#   __primary_author__ : WASIM ABDUL 
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import datetime
from datetime import datetime
Sql = SQL()
import SYCNGEGUID as CPQID

contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")
user_id = str(User.Id)
user_name = str(User.UserName) 
def constructcat4editablity(Quote_rec_id,MODE,values):
	#Trace.Write("Quote_rec_id"+str(Quote_rec_id))
	#Trace.Write("valuesvaluesvalues"+str(list(values)))
	get_all_lines =Sql.GetList("Select * from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_rec_id}' and QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND CpqTableEntryId IN ({values})".format(contract_quote_rec_id = contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,values=",".join(values).replace("SAQICO-","")))
	annual_dict={}
	for line_values in get_all_lines:
		record_list=[]
		if line_values:
			#allvalue_edit1="CAVVCI"
			#allvalue_edit2="CAVVPI"
			#allvalue_edit3="ADDCOF"
			#record_list.append(allvalue_edit1)
			#record_list.append(allvalue_edit2)
			#record_list.append(allvalue_edit3)	
			#nonstandard consuamble logic is pending
			Trace.Write("BPTTKPBPTTKPBPTTKP"+str(type(line_values.AMNCPE)))
			if (line_values.BPTTKP == 'Yes'):
				Trace.Write("ifff")
				editvalue1 ="BPTKCI"
				editvalue2 ="BPTKPI"
				record_list.append(editvalue1)
				record_list.append(editvalue2)
			if(line_values.ATGKEY != 'Excluded' and line_values.ATGKEY != 'Exception' and str(line_values.ATGKEY) != ''):
				editvalue3 = "ATGKEC"
				editvalue4 = "ATGKEP"
				record_list.append(editvalue3)
				record_list.append(editvalue4)
			if(line_values.NWPTON == 'Yes'):
				editvalue5 = "NWPTOC"
				editvalue6 = "NWPTOP"
				record_list.append(editvalue5)
				record_list.append(editvalue6)
			if(line_values.CNSMBL_ENT == 'Some Inclusions'):
				editvalue7 = "CONSCP"
				editvalue8 = "CONSPI"
				record_list.append(editvalue7)
				record_list.append(editvalue8)
			if(line_values.NCNSMB_ENT == 'Some Inclusions' or line_values.NCNSMB_ENT == 'Some Exclusions'):
				editvalue9 = "NONCCI"
				editvalue10 = "NONCPI"
				record_list.append(editvalue9)
				record_list.append(editvalue10)
			if(line_values.TGKPNS != 'Excluded' and str(line_values.TGKPNS) != ''):
				editvalue11 = "ATKNCI"
				editvalue12 = "ATKNPI"
				record_list.append(editvalue11)
				record_list.append(editvalue12)
			if(line_values.AMNCPE == "1"):
				editvalue13="AMNCCI"
				editvalue14="AMNPPI"
				record_list.append(editvalue13)
				record_list.append(editvalue14)
		annual_dict[str(line_values.LINE)] = record_list
	Trace.Write("dictdictdict"+str(annual_dict)) 
	return str(annual_dict)



def constructpricingsummary(Quote_rec_id,MODE,values):
	get_all_lines =Sql.GetList("Select * from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_rec_id}' and QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND CpqTableEntryId IN ({values})".format(contract_quote_rec_id = contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,values=",".join(values).replace("SAQICO-","")))
	annual_dict_pricing={}
	for line_values in get_all_lines:
		record_list=[]
		if line_values:
			if (line_values.BPTTKP == 'Yes'):
				Trace.Write("ifff")
				editvalue1 ="BPTKCI"
				editvalue2 ="BPTKPI"
				record_list.append(editvalue1)
				record_list.append(editvalue2)
			allvalue_edit1="TGADJP"
			allvalue_edit2="YOYPCT"
			allvalue_edit3="USRPRC"
			record_list.append(allvalue_edit1)
			record_list.append(allvalue_edit2)
			record_list.append(allvalue_edit3)
		annual_dict_pricing[str(line_values.LINE)] = record_list
	Trace.Write("dictdictdict"+str(annual_dict_pricing)) 
	return str(annual_dict_pricing)

ACTION = Param.ACTION
try:
	values = Param.values
except:
	values = ""


if ACTION == 'CAT4_ENTITLMENT':
    MODE="EDIT"
    Quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
    ApiResponse = ApiResponseFactory.JsonResponse(constructcat4editablity(Quote_rec_id,MODE,values))
elif ACTION == 'PRICING_SUMMARY':
    MODE="EDIT"
    Quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
    ApiResponse = ApiResponseFactory.JsonResponse(constructpricingsummary(Quote_rec_id,MODE,values))