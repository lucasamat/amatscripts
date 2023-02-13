# =========================================================================================================================================
#   __script_name : CQAPPCALWB.PY
#   __script_description : THIS SCRIPT IS USED TO 
#   __primary_author__ : 
#   __create_date :
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import System.Net
import re
import datetime
from System.Text.Encoding import UTF8
from System import Convert
import sys
from SYDATABASE import SQL
Sql = SQL()
import CQCPQC4CWB
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct() or "Sales"
try:
	contract_quote_rec_id = Quote.QuoteId
except:
	contract_quote_rec_id = ''

try:
	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
	quote_revision_record_id = ""

try:
	current_prod = Product.Name
	
except:
	current_prod = "Sales"
try:
	TabName = TestProduct.CurrentTab
except:
	TabName = "Quotes"

contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")
user_id = str(User.Id)
user_name = str(User.UserName)


contract_quote_id = Sql.GetFirst("Select QUOTE_ID FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id")))
if contract_quote_id:
    approver_insert = Sql.GetFirst("Select * FROM ACAPTX(NOLOCK) WHERE APRTRXOBJ_ID = '{}' AND ISNULL(OWNER_ID,'') = '' ".format(contract_quote_id.QUOTE_ID))
    if approver_insert:
        Trace.Write("Approver_insert")
        CQCPQC4CWB.writeback_to_c4c("approver_list",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
    else:
        Trace.Write("delete_approver")
        CQCPQC4CWB.writeback_to_c4c("delete_approver_list",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))