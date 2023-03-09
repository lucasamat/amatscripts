# =========================================================================================================================================
#   __script_name : CQCRUDOPTN.PY
#   __script_description : THIS SCRIPT IS USED TO ADD, UPDATE, DELETE RECORDS IN THE SALES AND RELATED TABLES
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN, Suriya (BitBucket deployment issue fixed)
#   __create_date :23-09-2020
# ==========================================================================================================================================
import datetime
import sys
import re
import System.Net
import SYCNGEGUID as CPQID
import CQADDONPRD
import CQVLDRIFLW
from SYDATABASE import SQL

Sql = SQL()
ScriptExecutor = ScriptExecutor
webclient = System.Net.WebClient()


try:
    current_prod = Product.Name
    Trace.Write('27---inside try--')
except:
    current_prod = "SALES"
    Trace.Write('27----inside catch----')

import time
class ContractQuoteCrudOpertion:
    def __init__(self, **kwargs):
        self.trigger_from = kwargs.get('trigger_from')
        if self.trigger_from:
            self.tree_param = kwargs.get('tree_param')
            self.tree_parent_level_0 = kwargs.get('tree_parent_level_0')
            self.tree_parent_level_1 = kwargs.get('tree_parent_level_1')
            self.contract_quote_record_id = kwargs.get('contract_quote_record_id')
        else:
            self.tree_param = Product.GetGlobal("TreeParam")
            self.tree_parent_level_0 = Product.GetGlobal("TreeParentLevel0")
            self.tree_parent_level_1 = Product.GetGlobal("TreeParentLevel1")
            self.tree_parent_level_2 = Product.GetGlobal("TreeParentLevel2")
            self.tree_parent_level_3 = Product.GetGlobal("TreeParentLevel3")
            self.tree_parent_level_4 = Product.GetGlobal("TreeParentLevel4")
            self.tree_parent_level_5 = Product.GetGlobal("TreeParentLevel5")
            self.tree_parent_level_6 = Product.GetGlobal("TreeParentLevel6")
            self.tree_parent_level_7 = Product.GetGlobal("TreeParentLevel7")
            self.tree_parent_level_8 = Product.GetGlobal("TreeParentLevel8")
        self.user_id = str(User.Id) #ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID")
        self.user_name = str(User.UserName) #ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERNAME")
        #self.sale_type = None
        
        self.datetime_value = datetime.datetime.now()
        self.set_contract_quote_related_details()

    def set_contract_quote_related_details(
        self, columns=["*"], table_name=None, where_condition="", table_joins="", single_record=False
    ):
        # Set - Contract Quote Details
        if not self.trigger_from == "IntegrationScript":
            try:
                self.contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
            except:
                self.contract_quote_record_id = ''	
            try:
                self.quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
            except:
                self.quote_revision_record_id = ''
            #Trace.Write("quote---"+str(self.contract_quote_record_id))
        GetToolReloc = Sql.GetList("SELECT CpqTableEntryId FROM SAQTIP WHERE (CPQ_PARTNER_FUNCTION = 'RECEIVING ACCOUNT' OR CPQ_PARTNER_FUNCTION = 'SENDING ACCOUNT') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id))
        #Trace.Write("count--"+str(list(GetToolReloc)))
        self.sale_type = None
        if GetToolReloc:
            GetToolReloc = list(GetToolReloc)
            if len(GetToolReloc) == 2:
                self.sale_type = "TOOL RELOCATION"
                
        #Trace.Write("SALE TYPE = "+str(self.sale_type))
        contract_quote_record_obj = self._get_record_obj(
            columns=[
                "QUOTE_ID",
                "QUOTE_NAME",
                "QUOTE_TYPE",
                #"SALESORG_ID",
                #"SALESORG_NAME",
                #"SALESORG_RECORD_ID",
                "ACCOUNT_ID",
                "ACCOUNT_NAME",
                "ACCOUNT_RECORD_ID",
                "CONTRACT_VALID_FROM",
                "CONTRACT_VALID_TO",
                "QUOTE_CURRENCY",
                "QUOTE_CURRENCY_RECORD_ID",
                "C4C_QUOTE_ID",
                "SOURCE_CONTRACT_ID",
                "SALE_TYPE",
                "QTEREV_ID",
                "QTEREV_RECORD_ID"
            ],
            table_name="SAQTMT",
            where_condition="MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id),
            single_record=True,
        )
        salesorg_obj = self._get_record_obj(
            columns=[
                #"QUOTE_ID",
                #"QUOTE_NAME",
                "SALESORG_ID",
                "SALESORG_NAME",
                "SALESORG_RECORD_ID"
                #"ACCOUNT_ID",
                #"ACCOUNT_NAME",
                #"ACCOUNT_RECORD_ID",
                #"CONTRACT_VALID_FROM",
                #"CONTRACT_VALID_TO",
                #"QUOTE_CURRENCY",
                #"QUOTE_CURRENCY_RECORD_ID",
                #"C4C_QUOTE_ID",
                #"SOURCE_CONTRACT_ID"
            ],
            table_name="SAQTRV",
            where_condition="QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id),
            single_record=True,
        )		
        #INC08671239,INC08847888 - START - M
        if contract_quote_record_obj and salesorg_obj:
            self.contract_quote_id = contract_quote_record_obj.QUOTE_ID
            self.contract_quote_name = contract_quote_record_obj.QUOTE_NAME
            self.quote_type = contract_quote_record_obj.QUOTE_TYPE
            self.quote_revision_id = contract_quote_record_obj.QTEREV_ID
            self.quote_revision_record_id = contract_quote_record_obj.QTEREV_RECORD_ID
            self.salesorg_id = salesorg_obj.SALESORG_ID
            self.salesorg_name = salesorg_obj.SALESORG_NAME
            self.salesorg_record_id = salesorg_obj.SALESORG_RECORD_ID
            self.account_id = contract_quote_record_obj.ACCOUNT_ID
            self.account_name = contract_quote_record_obj.ACCOUNT_NAME
            self.account_record_id = contract_quote_record_obj.ACCOUNT_RECORD_ID
            self.contract_start_date = contract_quote_record_obj.CONTRACT_VALID_FROM
            self.contract_end_date = contract_quote_record_obj.CONTRACT_VALID_TO
            self.contract_currency = contract_quote_record_obj.QUOTE_CURRENCY
            self.contract_currency_record_id = contract_quote_record_obj.QUOTE_CURRENCY_RECORD_ID
            self.c4c_quote_id = contract_quote_record_obj.C4C_QUOTE_ID
            self.source_contract_id = contract_quote_record_obj.SOURCE_CONTRACT_ID
            #self.sale_type = contract_quote_record_obj.SALE_TYPE
            #INC08797912 A
            self.account_name = re.sub(r"â","''",self.account_name)
            self.account_name = re.sub(r"ï¼","+",self.account_name)
            self.contract_quote_name=re.sub(r"â","''",self.contract_quote_name)
            self.contract_quote_name=re.sub(r"ï¼","+",self.contract_quote_name)
            #INC08797912 A
            #INC08671239,INC08847888 - END - M
        else:
            self.contract_quote_id = None
            self.contract_quote_name = None
            self.salesorg_id = None
            self.salesorg_name = None
            self.salesorg_record_id = None
            self.account_id = None
            self.account_record_id = None
            self.account_name = None
            self.contract_start_date = None
            self.contract_end_date = None
            self.contract_currency = None
            self.contract_currency_record_id = None
            self.c4c_quote_id = None
            self.source_contract_id = None
            #self.sale_type = None
        return True

    def _get_record_obj(self, columns=["*"], table_name=None, where_condition="", table_joins="", single_record=False,notin_condition = ""):	
        if table_name and self.tree_param != 'Approval Chain Steps' and str(current_prod).upper() not in ("SYSTEM ADMIN","APPROVAL CENTER"):
            
            if where_condition:
                where_condition = "WHERE {}".format(where_condition)			
                if notin_condition!="":
                    where_condition += notin_condition
            Trace.Write('###230 -->'+str(where_condition))
            if single_record:
                return Sql.GetFirst("SELECT {Columns} FROM {ObjectName} (NOLOCK) {Joins} {WhereCondition}".format(
                        Columns=",".join(columns), ObjectName=table_name, Joins=table_joins, WhereCondition=where_condition
                    ))
            else:				
                return Sql.GetList(
                    "SELECT {Columns} FROM {ObjectName} (NOLOCK) {Joins} {WhereCondition}".format(
                        Columns=",".join(columns), ObjectName=table_name, Joins=table_joins, WhereCondition=where_condition
                    )
                )
        return None

    def _process_query(self, query_string):
        try:
            Sql.RunQuery(query_string)
        except Exception:
            Log.Info("_process_query---->:" + str(sys.exc_info()[1]))
        return True

    def _add_record(
        self, master_object_name=None, columns=[], table_name=None, condition_column=None, values=[], where_condition=""
    ):
        if self.action_type == "ADD_OFFERING" and self.all_values:
            if self.tree_param=="Product Offerings":
                product_type=" PRODUCT_TYPE IS NOT NULL AND PRODUCT_TYPE <> '' AND PRODUCT_TYPE != 'Add-On Products' "
            elif self.tree_param!="Product Offerings" and self.tree_param!="Add-On Products":
                product_type=" PRODUCT_TYPE = '{TreeParam}' ".format(TreeParam=self.tree_param)
            qury_str=""
            if A_Keys!="" and A_Values!="":
                for key,val in zip(A_Keys,A_Values):
                    if(val!=""):
                        if key=="MATERIAL_RECORD_ID":
                            key="CpqTableEntryId"
                            val = ''.join(re.findall(r'\d+', val)) if not val.isdigit() else val
                        qury_str+=" MAMTRL."+key+" LIKE '%"+val+"%' AND "
                get_sales_org = SqlHelper.GetFirst("SELECT * FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id))
                sales_org=""
                if get_sales_org :
                    sales_org=get_sales_org.SALESORG_ID
                # INC08593801 - Start - M
                query_string="select MAMTRL.MATERIAL_RECORD_ID, MAMTRL.SAP_PART_NUMBER, SAP_DESCRIPTION, PRODUCT_TYPE from MAMTRL (NOLOCK)  INNER JOIN MAMSOP (NOLOCK) ON MAMTRL.MATERIAL_RECORD_ID = MAMSOP.MATERIAL_RECORD_ID  WHERE {product_type} AND {Qury_Str} MAMTRL.SAP_PART_NUMBER NOT IN (SELECT SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' )  AND SALESORG_ID='{sales_org}'  ".format(product_type=product_type,Qury_Str=qury_str,contract_quote_record_id = self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,sales_org=sales_org)
                # INC08593801 - End - M
                result=SqlHelper.GetList(query_string)
                if result is not None:
                    record_ids = [data.MATERIAL_RECORD_ID for data in result]
        else:
            record_ids = [
                CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
                if value.strip() != "" and master_object_name in value
                else value
                for value in values
            ]
        
        if record_ids:
            if len(record_ids) == 1:
                where_conditon = "%s = '%s'" % (condition_column, record_ids[0],)
            else:
                where_conditon = "%s in %s" % (condition_column, tuple(record_ids),)
            notin_condition = " AND  NOT EXISTS (SELECT ADNPRD_ID FROM SAQSAO WHERE SERVICE_ID = '"+str(self.tree_parent_level_1)+"' AND QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND ADNPRD_RECORD_ID IN "+str(tuple(record_ids)).replace(",)",')')+" ) "  if table_name == "SAQSAO" and self.action_type == "ADD_ON_PRODUCTS" else ""
            records_obj = self._get_record_obj(columns=columns, table_name=master_object_name, where_condition=where_conditon,notin_condition = notin_condition)
            if records_obj:
                auto_number_column_name_obj = self._get_record_obj(
                    columns=["API_NAME"],
                    table_name="SYOBJD",
                    where_condition="OBJECT_NAME = '{}' AND DATA_TYPE='AUTO NUMBER'".format(table_name),
                    single_record=True,
                )
                auto_number_column_name = auto_number_column_name_obj.API_NAME

                common_row_values = {
                    "QUOTE_RECORD_ID": self.contract_quote_record_id,
                    "QUOTE_ID": self.contract_quote_id,
                    "QTEREV_RECORD_ID" : self.quote_revision_record_id,
                    "QTEREV_ID" : self.quote_revision_id
                }
                for record_obj in records_obj:
                    row = {data.Key: data.Value for data in record_obj}
                    row[auto_number_column_name] = str(Guid.NewGuid()).upper()
                    row.update(common_row_values)				
                    yield dict(row)
        ##A055S000P01-8740 code ends...
        #ScriptExecutor.ExecuteGlobal('CQDOCUTYPE',{'QUOTE_RECORD_ID':self.contract_quote_record_id,'QTEREV_RECORD_ID':self.quote_revision_record_id})
        ##A055S000P01-8740 code ends...
    
    def _create(self):
        pass

    def _update(self):
        pass

    def _delete(self):
        pass
        
class ContractQuoteOfferingsModel(ContractQuoteCrudOpertion):
    def __init__(self, **kwargs):
        ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'), 
                                            tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
        self.opertion = kwargs.get('opertion')
        self.action_type = kwargs.get('action_type')
        self.values = kwargs.get('values')
        self.table_name = kwargs.get('table_name')
        self.all_values = kwargs.get('all_values')
        self.new_part = kwargs.get('new_part')
        self.tool_type = kwargs.get('tool_type')
        self.node_id = ""
        self.inclusion = kwargs.get('inclusion')
    
    # def _insert_quote_line_items(self, cart_id, cart_user_id):
    # 	Bundle_Query = ''
        
    # 	if self.tree_parent_level_0 == 'Comprehensive Services':			
    # 		Bundle_Query = Sql.GetFirst("SELECT ADNPRD_ID FROM SAQSAO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id, self.tree_param,self.quote_revision_record_id))
    # 	elif self.tree_parent_level_0 == 'Add-On Products':			
    # 		Bundle_Query = Sql.GetFirst("SELECT SERVICE_ID,SERVICE_DESCRIPTION FROM SAQSAO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND ADNPRD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id, self.tree_param,self.quote_revision_record_id))
    # 		Bundle_Query_addon = Sql.GetFirst("SELECT ADNPRD_ID,ADNPRD_DESCRIPTION FROM SAQSAO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND ADNPRD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id, self.tree_param,self.quote_revision_record_id))
        
    # 	if Bundle_Query:			
    # 		if Bundle_Query and self.tree_parent_level_0 == 'Add-On Products':
    # 			bundleser = Bundle_Query.SERVICE_ID + " - BUNDLE"
    # 			if Bundle_Query_addon:
    # 				bundledes =Bundle_Query.SERVICE_DESCRIPTION+ " WITH " + Bundle_Query_addon.ADNPRD_DESCRIPTION
    # 			else:
    # 				bundledes = ''
    # 		else:
    # 			bundleser = self.tree_param + " - BUNDLE"
    # 			bundledes = ''
            
            # self._process_query("""INSERT QT__SAQITM (
            # 			ITEM_LINE_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTY_OF_TOOLS, CURRENCY, UNIT_PRICE, EXTENDED_UNIT_PRICE,
            # 			QUANTITY, FORECAST_VALUE, ONSITE_PURCHASE_COMMIT, QUOTE_ID, QUOTE_RECORD_ID, TAX_PERCENTAGE, TAX,  ownerId, cartId
            # 		) 
            # 		SELECT 
            # 			SAQITM.LINE_ITEM_ID as ITEM_LINE_ID,
            # 			'{bundledescription}' as SERVICE_DESCRIPTION,
            # 			REPLACE(SAQITM.SERVICE_ID , '- BUNDLE', '') as SERVICE_ID,
            # 			SAQITM.SERVICE_RECORD_ID,					
            # 			0 AS QTY_OF_TOOLS,
            # 			SAQITM.CURRENCY,
            # 			(SAQITM.NET_VALUE-SAQITM.TAX) as UNIT_PRICE,
            # 			SAQITM.NET_VALUE as EXTENDED_UNIT_PRICE,
            # 			SAQITM.QUANTITY,
            # 			0 AS FORECAST_VALUE,
            # 			SAQITM.ONSITE_PURCHASE_COMMIT,
            # 			SAQITM.QUOTE_ID,
            # 			SAQITM.QUOTE_RECORD_ID,
            # 			SAQITM.TAX_PERCENTAGE,
            # 			SAQITM.TAX,
            # 			{UserId} as ownerId,
            # 			{CartId} as cartId
            # 		FROM SAQITM (NOLOCK) 
            # 		JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = SAQITM.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQITM.QTEREV_RECORD_ID               
            # 		WHERE SAQITM.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQITM.SERVICE_ID = '{ServiceId}' """.format(
            # 			CartId=cart_id, UserId=cart_user_id, QuoteRecordId=self.contract_quote_record_id,
            # 			RevisionRecordId=self.quote_revision_record_id,
            # 			ServiceId=bundleser,bundledescription = bundledes,))
            # Sql.RunQuery("""INSERT QT__SAQITM (
            # 			ITEM_LINE_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTY_OF_TOOLS, CURRENCY, UNIT_PRICE, EXTENDED_UNIT_PRICE,
            # 			QUANTITY, FORECAST_VALUE, ONSITE_PURCHASE_COMMIT, QUOTE_ID, QUOTE_RECORD_ID, TAX_PERCENTAGE, TAX,  ownerId, cartId
            # 		) 
            # 		SELECT 
            # 			SAQITM.LINE_ITEM_ID as ITEM_LINE_ID,
            # 			SAQITM.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
            # 			SUBSTRING(SAQITM.SERVICE_ID , 9, 13) as SERVICE_ID,
            # 			SAQITM.SERVICE_RECORD_ID,					
            # 			0 AS QTY_OF_TOOLS,
            # 			SAQITM.CURRENCY,
            # 			(SAQITM.NET_VALUE-SAQITM.TAX) as UNIT_PRICE,
            # 			SAQITM.NET_VALUE as EXTENDED_UNIT_PRICE,
            # 			SAQITM.QUANTITY,
            # 			0 AS FORECAST_VALUE,
            # 			SAQITM.ONSITE_PURCHASE_COMMIT,
            # 			SAQITM.QUOTE_ID,
            # 			SAQITM.QUOTE_RECORD_ID,
            # 			SAQITM.TAX_PERCENTAGE,
            # 			SAQITM.TAX,
            # 			{UserId} as ownerId,
            # 			{CartId} as cartId
            # 		FROM SAQITM (NOLOCK)                 
            # 		WHERE SAQITM.QUOTE_RECORD_ID='{QuoteRecordId}'  AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQITM.SERVICE_ID LIKE '%ADDON%' """.format(
            # 			CartId=cart_id, UserId=cart_user_id, QuoteRecordId=self.contract_quote_record_id,
            # 			RevisionRecordId=self.quote_revision_record_id,
            # 			ServiceId=bundleser,bundledescription = bundledes))			
        # else:
            # self._process_query("""INSERT QT__SAQITM (
            # 			ITEM_LINE_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTY_OF_TOOLS, CURRENCY, UNIT_PRICE, EXTENDED_UNIT_PRICE,
            # 			QUANTITY, FORECAST_VALUE, ONSITE_PURCHASE_COMMIT, QUOTE_ID, QUOTE_RECORD_ID, TAX_PERCENTAGE, TAX,  ownerId, cartId
            # 		) 
            # 		SELECT 
            # 			SAQITM.LINE_ITEM_ID as ITEM_LINE_ID,
            # 			SAQITM.SERVICE_DESCRIPTION,
            # 			REPLACE(SAQITM.SERVICE_ID , '- BASE', '') as SERVICE_ID,
            # 			SAQITM.SERVICE_RECORD_ID,					
            # 			0 AS QTY_OF_TOOLS,
            # 			SAQITM.CURRENCY,
            # 			(SAQITM.NET_VALUE-SAQITM.TAX) as UNIT_PRICE,
            # 			SAQITM.NET_VALUE as EXTENDED_UNIT_PRICE,
            # 			SAQITM.QUANTITY,
            # 			0 AS FORECAST_VALUE,
            # 			SAQITM.ONSITE_PURCHASE_COMMIT,
            # 			SAQITM.QUOTE_ID,
            # 			SAQITM.QUOTE_RECORD_ID,
            # 			SAQITM.TAX_PERCENTAGE,
            # 			SAQITM.TAX,
            # 			{UserId} as ownerId,
            # 			{CartId} as cartId
            # 		FROM SAQITM (NOLOCK) 
            # 		JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = SAQITM.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID  AND SAQTSV.QTEREV_RECORD_ID = SAQITM.QTEREV_RECORD_ID              
            # 		WHERE SAQITM.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID = '{ServiceId}' """.format(
            # 			CartId=cart_id, UserId=cart_user_id, QuoteRecordId=self.contract_quote_record_id,
            # 			RevisionRecordId=self.quote_revision_record_id,
            # 			ServiceId=self.tree_param,))
        # if self.tree_param == 'Z0068' and self.tree_parent_level_0 == 'Add-On Products':
            # self._process_query("""UPDATE A SET A.TARGET_PRICE = B.TARGET_PRICE,A.SALES_PRICE = B.SALES_PRICE,A.CEILING_PRICE = B.CEILING_PRICE,A.TOTAL_COST = B.TOTAL_COST,A.EXTENDED_PRICE = B.EXTENDED_PRICE,A.TAX = B.TAX,A.PRICING_STATUS = 'ACQUIRED' FROM QT__SAQITM A(NOLOCK) JOIN (SELECT SUM(TARGET_PRICE) AS TARGET_PRICE,SUM(SALES_PRICE) AS SALES_PRICE,SUM(CEILING_PRICE) AS CEILING_PRICE,SUM(TOTAL_COST) AS TOTAL_COST,SUM(EXTENDED_PRICE) AS EXTENDED_PRICE,SUM(TAX) AS TAX,QUOTE_RECORD_ID,SERVICE_RECORD_ID from QT__SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID='{Service_id}' GROUP BY QUOTE_RECORD_ID,SERVICE_RECORD_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID  AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID
            # AND A.SERVICE_RECORD_ID=B.SERVICE_RECORD_ID """.format(			
            # QuoteRecordId=self.contract_quote_record_id,
            # RevisionRecordId=self.quote_revision_record_id,
            # Service_id =self.tree_param))				
        # """ if Quote is not None:
        # 	Quote.QuoteTables["SAQITM"].Save()
        # 	Quote.QuoteTables["SAQICO"].Save()
        # 	Quote.QuoteTables["SAQIFP"].Save()
        # 	Quote.Save() """
        # return True

    # def _delete_quote_line_items(self, cart_id, cart_user_id):
    # 	self._process_query("""DELETE QT__SAQITM FROM QT__SAQITM 
    # 							JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = QT__SAQITM.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = QT__SAQITM.QUOTE_RECORD_ID  AND SAQTSV.QTEREV_RECORD_ID = QT__SAQITM.QTEREV_RECORD_ID
    # 							WHERE QT__SAQITM.cartId = '{CartId}' AND ownerId = {UserId} AND QT__SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND QT__SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_DESCRIPTION = '{ServiceId}'""".format(
    # 								CartId=cart_id, UserId=cart_user_id, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, ServiceId=self.tree_param))
    # 	return True
    
    # def _insert_quote_spare_parts(self, cart_id, cart_user_id):		
    # 	self._process_query("""INSERT QT__SAQIFP (
    # 				QUOTE_ITEM_FORECAST_PART_RECORD_ID, ANNUAL_QUANTITY, BASEUOM_RECORD_ID, CUSTOMER_PART_NUMBER, 
    # 				CUSTOMER_PART_NUMBER_RECORD_ID, DELIVERY_MODE, EXTENDED_UNIT_PRICE, ITEM_LINE_ID, PART_DESCRIPTION, PART_NUMBER, 
    # 				PART_RECORD_ID, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID,
    # 				SALESUOM_CONVERSION_FACTOR, SCHEDULE_MODE, SERVICE_DESCRIPTION, SERVICE_ID,
    # 				SERVICE_RECORD_ID, UNIT_PRICE, VALID_FROM_DATE, VALID_TO_DATE, MATPRIGRP_ID, MATPRIGRP_NAME, MATPRIGRP_RECORD_ID, PART_LINE_ID, ownerId, cartId
    # 			) 
    # 			SELECT 
    # 				CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_FORECAST_PART_RECORD_ID,  
    # 				SAQIFP.ANNUAL_QUANTITY,
    # 				SAQIFP.BASEUOM_RECORD_ID,
    # 				SAQIFP.PART_NUMBER AS CUSTOMER_PART_NUMBER,
    # 				SAQIFP.PART_RECORD_ID AS CUSTOMER_PART_NUMBER_RECORD_ID,
    # 				SAQIFP.DELIVERY_MODE,
    # 				SAQIFP.EXTENDED_PRICE,
    # 				SAQIFP.LINE as ITEM_LINE_ID,
    # 				SAQIFP.PART_DESCRIPTION,
    # 				SAQIFP.PART_NUMBER,
    # 				SAQIFP.PART_RECORD_ID,
    # 				SAQIFP.QUOTE_ID,
    # 				SAQIFP.QTEITM_RECORD_ID,
    # 				SAQIFP.QUOTE_NAME,
    # 				SAQIFP.QUOTE_RECORD_ID,
    # 				SAQIFP.SALESORG_ID,
    # 				SAQIFP.SALESORG_NAME,
    # 				SAQIFP.SALESORG_RECORD_ID,
    # 				0 AS SALESUOM_CONVERSION_FACTOR,					
    # 				SAQIFP.SCHEDULE_MODE,
    # 				SAQIFP.SERVICE_DESCRIPTION,
    # 				SAQTSV.SERVICE_ID,
    # 				SAQIFP.SERVICE_RECORD_ID,
    # 				SAQIFP.UNIT_PRICE,
    # 				SAQIFP.VALID_FROM_DATE,
    # 				SAQIFP.VALID_TO_DATE,
    # 				SAQIFP.MATPRIGRP_ID,
    # 				SAQIFP.MATPRIGRP_NAME,
    # 				SAQIFP.MATPRIGRP_RECORD_ID,
    # 				SAQIFP.PART_LINE_ID,
    # 				{UserId} as ownerId,
    # 				{CartId} as cartId
    # 			FROM SAQIFP (NOLOCK) 
    # 			JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = SAQIFP.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQIFP.QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQIFP.QTEREV_RECORD_ID                
    # 			WHERE SAQIFP.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQIFP.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID = '{ServiceId}'""".format(
    # 				CartId=cart_id, UserId=cart_user_id, QuoteRecordId=self.contract_quote_record_id,
    # 				RevisionRecordId=self.quote_revision_record_id,
    # 				ServiceId=self.tree_param))
    # 	if Quote is not None:
    # 		Quote.QuoteTables["SAQITM"].Save()
    # 		Quote.QuoteTables["SAQICO"].Save()
    # 		Quote.QuoteTables["SAQIFP"].Save()
    # 		Quote.Save() 
    # 	return True
    
    # def _delete_quote_spare_parts(self, cart_id, cart_user_id):
    # 	self._process_query("""DELETE QT__SAQIFP 
    # 							FROM QT__SAQIFP 
    # 							JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = QT__SAQIFP.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = QT__SAQIFP.QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = QT__SAQIFP.QTEREV_RECORD_ID
    # 							WHERE QT__SAQIFP.cartId = '{CartId}' AND ownerId = {UserId} AND QT__SAQIFP.QUOTE_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID = '{ServiceId}'""".format(
    # 								CartId=cart_id, UserId=cart_user_id, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, ServiceId=self.tree_param))
    # 	return True

    def _create(self):		
        row_values = {}
        if self.action_type == "ADD_OFFERING":
            master_object_name = "MAMTRL"
            columns = [
                "SAP_PART_NUMBER AS SERVICE_ID",
                "SAP_DESCRIPTION AS SERVICE_DESCRIPTION",
                "MATERIAL_RECORD_ID AS SERVICE_RECORD_ID",
                "PRODUCT_TYPE AS SERVICE_TYPE",
                "UNIT_OF_MEASURE AS UOM_ID",
                "UOM_RECORD_ID AS UOM_RECORD_ID",
            ]
            table_name = "SAQTSV"
            condition_column = "MATERIAL_RECORD_ID"
            row_values = {"QUOTE_NAME": self.contract_quote_name,
                "SALESORG_ID": self.salesorg_id,
                "SALESORG_NAME": self.salesorg_name,
                "SALESORG_RECORD_ID": self.salesorg_record_id,
                "QTEREV_RECORD_ID": self.quote_revision_record_id,
                "QTEREV_ID":self.quote_revision_id,
                "CONTRACT_VALID_FROM":self.contract_start_date,
                "CONTRACT_VALID_TO":self.contract_end_date,
                "OBJECT_QUANTITY": "1" }

            offering_table_info = Sql.GetTable(table_name)
            existing_offering_ids = []
            Trace.Write('@@Values-->'+str(list(values)))
            for row_detail in self._add_record(
                master_object_name=master_object_name,
                columns=columns,
                table_name=table_name,
                condition_column=condition_column,
                values=self.values,
            ):
                check_existing_offerings_obj = self._get_record_obj(
                    columns=["SERVICE_ID"],
                    table_name=table_name,
                    where_condition="QUOTE_SERVICE_RECORD_ID = '{}'".format(row_detail.get("QUOTE_SERVICE_RECORD_ID")),
                    single_record=False,
                )
                if check_existing_offerings_obj:
                    existing_offering_ids.extend(
                        [
                            check_existing_offering_obj.SERVICE_ID
                            for check_existing_offering_obj in check_existing_offerings_obj
                        ]
                    )
                    if row_detail.get("SERVICE_ID") in existing_offering_ids:
                        continue
                    else:
                        existing_offering_ids.append(row_detail.get("SERVICE_ID"))
                Trace.Write('Row_Values--->'+str(row_values))
                row_detail.update(row_values)
                ###A055S000P01-9650 START
                Trace.Write('###Row_details----> '+str(row_detail))
                getservice_count = Sql.GetFirst("Select count(CpqTableEntryId) as COUNT FROM SAQTSV(NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
                get_poes = Sql.GetFirst("Select POES FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
                # for count in getservice_count:
                if getservice_count.COUNT == 0:
                    service_id = row_detail.get("SERVICE_ID")
                    document_type_obj = Sql.GetFirst("select DOCTYP_ID,DOCTYP_RECORD_ID from MAMADT(NOLOCK) where SAP_PART_NUMBER = '{}' AND POES ='{}'".format(service_id,get_poes.POES))
                    if document_type_obj:
                        row_values_doctyp = {"DOCTYP_ID": document_type_obj.DOCTYP_ID,"DOCTYP_RECORD_ID": document_type_obj.DOCTYP_RECORD_ID}
                        Trace.Write("row_detail -------------->"+str(row_detail))
                        row_detail.update(row_values_doctyp)
                        offering_table_info.AddRow(row_detail)
                        Sql.Upsert(offering_table_info)
                        Sql.RunQuery("UPDATE SAQTRV SET DOCTYP_ID = '{DocumentType}',DOCTYP_RECORD_ID = '{DocumentTypeRecordId}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(DocumentType = document_type_obj.DOCTYP_ID,DocumentTypeRecordId = document_type_obj.DOCTYP_RECORD_ID,QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
                # elif count.COUNT <= 1:
                # 	mamtrl_record = Sql.GetFirst("SELECT CLM_CONTRACT_TYPE,CLM_TEMPLATE_NAME FROM MAMTRL (NOLOCK) WHERE SAP_PART_NUMBER = '"+str(getservice_count.SERVICE_ID)+"'")

                # 	sow_update_query= "UPDATE SAQTRV SET CLM_CONTRACT_TYPE = '"+str(mamtrl_record.CLM_CONTRACT_TYPE)+"', CLM_TEMPLATE_NAME = '"+str(mamtrl_record.CLM_TEMPLATE_NAME)+"' WHERE QUOTE_RECORD_ID = '" + str(Quote) + "' "
                # 	Sql.RunQuery(sow_update_query)
                else:
                    get_first_service_id = Sql.GetFirst("SELECT SERVICE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY CpqTableEntryId ASC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
                    service_id = row_detail.get("SERVICE_ID")
                    service_maadpr = Sql.GetFirst(" SELECT COMP_PRDOFR_DOCTYP_RECORD_ID,COMP_PRDOFR_DOCTYP FROM MAADPR WHERE POES = '{}' and PRDOFR_ID = '{}' AND COMP_PRDOFR_ID ='{service_id}' ".format(get_poes.POES,get_first_service_id.SERVICE_ID,service_id = service_id))
                    if service_maadpr:
                        row_values_doctyp = {"DOCTYP_ID": service_maadpr.COMP_PRDOFR_DOCTYP,"DOCTYP_RECORD_ID": service_maadpr.COMP_PRDOFR_DOCTYP_RECORD_ID}
                        row_detail.update(row_values_doctyp)
                        Trace.Write('row_detail-->'+str(row_detail))
                        offering_table_info.AddRow(row_detail)
                        Trace.Write('offering_table_info-->'+str(offering_table_info))
                        Sql.Upsert(offering_table_info)

                

                product_offering = Sql.GetList("SELECT SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
                if len(product_offering) > 1:
                    #INC08971850 - Start - M
                    get_service_obj = Sql.GetFirst("SELECT TOP 1 SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY CpqTableEntryId ASC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
                   
                    mamtrl_record = Sql.GetFirst("SELECT CLM_CONTRACT_TYPE,CLM_TEMPLATE_NAME FROM MAMTRL (NOLOCK) WHERE SAP_PART_NUMBER = '"+str(get_service_obj.SERVICE_ID)+"'")
                    sow_update_query= "UPDATE SAQTRV SET CLM_CONTRACT_TYPE = '"+str(mamtrl_record.CLM_CONTRACT_TYPE)+"', CLM_TEMPLATE_NAME = '"+str(mamtrl_record.CLM_TEMPLATE_NAME)+"' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id)
                    #INC08971850 - End - M
                    Trace.Write("sow_update_query_1 "+str(sow_update_query))
                    Sql.RunQuery(sow_update_query)
                elif len(product_offering) <= 1:
                    for count in product_offering:
                        mamtrl_record = Sql.GetFirst("SELECT CLM_CONTRACT_TYPE,CLM_TEMPLATE_NAME FROM MAMTRL (NOLOCK) WHERE SAP_PART_NUMBER = '"+str(count.SERVICE_ID)+"'")

                    sow_update_query= "UPDATE SAQTRV SET CLM_CONTRACT_TYPE = '"+str(mamtrl_record.CLM_CONTRACT_TYPE)+"', CLM_TEMPLATE_NAME = '"+str(mamtrl_record.CLM_TEMPLATE_NAME)+"' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id)
                    Trace.Write("sow_update_query_2 "+str(sow_update_query))
                    Sql.RunQuery(sow_update_query)

                service_id = row_detail.get("SERVICE_ID")
                if service_id != "Z0108" and service_id != "Z0110":
                    MainObjUpdateQuery = """UPDATE SAQTRV SET
                        INCOTERM_ID = 'NA',INCOTERM_NAME = 'Not Applicable',INCOTERM_LOCATION = 'Not Applicable',INCOTERM_RECORD_ID = ''
                        WHERE QUOTE_REVISION_RECORD_ID = '{}' """.format(Quote.GetGlobal("quote_revision_record_id"))
                    Sql.RunQuery(MainObjUpdateQuery)
                #A055S000P01-9650 ENDS
                #offering_table_info.AddRow(row_detail)
                #Sql.Upsert(offering_table_info)
                #service_obj  = Sql.GetFirst("select COUNT(SERVICE_ID) as count,SERVICE_ID from SAQTSV where QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id))
                #if service_obj.count == 1:
                #	document_type_obj = Sql.GetFirst("select DOCTYP_ID from MAMADT where SAP_PART_NUMBER = '{}'".format(service_obj.SERVICE_ID))
                #	if document_type_obj is not None:
                #		self._process_query("UPDATE SAQTMT SET DOCUMENT_TYPE = '{}' WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(document_type_obj.DOCTYP_ID,self.contract_quote_record_id))
                Trace.Write("row_detail__JJ "+str(row_detail))
                self.CreateEntitlements(row_detail)
                
            ##A055S000P01-8740 code starts...
            #ScriptExecutor.ExecuteGlobal('CQDOCUTYPE',{'QUOTE_RECORD_ID':self.contract_quote_record_id,'QTEREV_RECORD_ID':self.quote_revision_record_id})
            ##A055S000P01-8740 code ends...
            # ADD VD TO THE OFFERINGS
            #QTSID = str(row_detail["SERVICE_ID"])
            #Trace.Write("service_ID"+str(QTSID))
            #self._process_query(""" INSERT SAQSAO (QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID,ADNPRD_DESCRIPTION,ADNPRD_ID,ADNPRDOFR_RECORD_ID,ADNPRD_RECORD_ID,ADN_TYPE,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTESRV_RECORD_ID,SALESORG_ID,SALESORG_NAME,ACTIVE,SALESORG_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified) SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID,MAADPR.ADNPRDOFR_NAME,MAADPR.ADNPRDOFR_ID,MAADPR.ADNPRDOFR_RECORD_ID,MAADPR.ADD_ON_PRODUCT_RECORD_ID,MAADPR.ADN_TYPE,SAQTSV.QUOTE_ID,SAQTSV.QUOTE_NAME,SAQTSV.QUOTE_RECORD_ID,SAQTSV.QUOTE_SERVICE_RECORD_ID,SAQTSV.SALESORG_ID,SAQTSV.SALESORG_NAME,'FALSE' as ACTIVE,SAQTSV.SALESORG_RECORD_ID,SAQTSV.SERVICE_DESCRIPTION,SAQTSV.SERVICE_ID,SAQTSV.SERVICE_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM MAADPR (NOLOCK) INNER JOIN  SAQTSV ON MAADPR.PRDOFR_ID = SAQTSV.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND SERVICE_ID ='{ServiceIds}' """.format(UserId=self.user_id,UserName=self.user_name,QuoteRecordId=self.contract_quote_record_id,ServiceIds=str(QTSID)))
        elif self.action_type == "ADD_SPARE_PARTS" or self.action_type == "ADD_PARTS":
            if self.values:
                batch_group_record_id = str(Guid.NewGuid()).upper()
                #spare_parts_obj = re.finditer(r'([a-zA-Z0-9_\-.\(\)]*\s?[a-zA-Z0-9\-]?)\t+(\d*)', self.values[0])                         
                #spare_parts_details = [(str(Guid.NewGuid()).upper(), spare_part_obj.group(1), spare_part_obj.group(2), 'IN PROGRESS', self.contract_quote_id, self.contract_quote_record_id, batch_group_record_id) for spare_part_obj in spare_parts_obj]

                spare_parts_details = [(str(Guid.NewGuid()).upper(), spare_part, 1, 'IN PROGRESS', self.contract_quote_id, self.contract_quote_record_id, batch_group_record_id,self.quote_revision_record_id) for spare_part in self.values[0].splitlines()]
                
                spare_parts_details_joined = ', '.join(map(str, spare_parts_details))
                self._process_query("""INSERT INTO SYSPBT(BATCH_RECORD_ID, SAP_PART_NUMBER, QUANTITY, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,QTEREV_RECORD_ID) 
                                        SELECT * FROM (VALUES {}) QS (BATCH_RECORD_ID, SAP_PART_NUMBER, QUANTITY, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,QTEREV_RECORD_ID)""".format(spare_parts_details_joined))
                self._process_query("""DELETE SYSPBT FROM SYSPBT JOIN SAQSPT ON SYSPBT.SAP_PART_NUMBER = SAQSPT.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID AND  SYSPBT.QTEREV_RECORD_ID = SAQSPT.QTEREV_RECORD_ID WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
                
                if self.action_type == "ADD_PARTS":
                    self._process_query("""DELETE SYSPBT FROM SYSPBT JOIN SAQRSP ON SYSPBT.SAP_PART_NUMBER = SAQRSP.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQRSP.QUOTE_RECORD_ID AND  SYSPBT.QTEREV_RECORD_ID = SAQRSP.QTEREV_RECORD_ID WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
                    
                    parts_value = 0
                    Service_Id = self.tree_param
                    entitlement_obj = Sql.GetFirst("select ENTITLEMENT_XML from SAQTSE (nolock) where QUOTE_RECORD_ID  = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
                    entitlement_xml = entitlement_obj.ENTITLEMENT_XML
                    quote_item_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
                    entitlement_value_str = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(Service_Id)+'[^>]*?_TSC_SCPT</ENTITLEMENT_ID>')
                    value = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
                    for m in re.finditer(quote_item_tag, entitlement_xml):
                        sub_string = m.group(1)
                        scheduled_parts =re.findall(entitlement_value_str,sub_string)
                        scheduled_value =re.findall(value,sub_string)
                        if scheduled_parts and scheduled_value:
                            parts_value = scheduled_value[0]
                            break
                    if self.tree_param == 'Z0108':
                        delivery_mode = "OFFSITE"
                        schedule_mode= "SCHEDULED" if int(parts_value) > 9 else "UNSCHEDULED"
                    elif self.tree_param == 'Z0110':
                        delivery_mode = " "
                        schedule_mode= " "
                    if self.tree_param in ('Z0108','Z0110'):
                        part_numbers=''
                        part_numbers= str([spare_part for spare_part in self.values[0].splitlines()])
                        part_numbers=part_numbers.replace("'",'"')
                        ScriptExecutor.ExecuteGlobal('CQPARTSINS',{"CPQ_Columns":{"Action": "LoadParts","Part_number":part_numbers,"QuoteID":self.contract_quote_id}})
                elif self.action_type == "ADD_SPARE_PARTS":
                    #HPQC 1210 & 2099 start
                    for spare_part in self.values[0].splitlines():                        
                        #Log.Info('spare_part ==> ' + str(spare_part))
                        #exclusion bulk add parts
                        if self.inclusion == 0 and self.new_part == 0:
                            #Log.Info('exclusion condition')
                            self._process_query("""DELETE SYSPBT FROM SYSPBT JOIN SAQRSP ON SYSPBT.SAP_PART_NUMBER = SAQRSP.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQRSP.QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQRSP.QTEREV_RECORD_ID WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRSP.NEW_PART='False' AND (SAQRSP.INCLUDED = 'True' OR SAQRSP.INCLUDED = 'False') AND SAQRSP.PART_NUMBER = '{part_no}' AND SAQRSP.PAR_SERVICE_ID = '{service_id}'""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, part_no = spare_part, service_id = self.tree_parent_level_0))
                        #inclusion bulk add parts
                        elif self.inclusion == 1 and self.new_part == 0:
                            #Log.Info('inclusion condition')
                            self._process_query("""DELETE SYSPBT FROM SYSPBT JOIN SAQRSP ON SYSPBT.SAP_PART_NUMBER = SAQRSP.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQRSP.QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQRSP.QTEREV_RECORD_ID WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND (SAQRSP.INCLUDED = 'True' OR (SAQRSP.INCLUDED = 'False' AND SAQRSP.NEW_PART='False')) AND SAQRSP.PART_NUMBER = '{part_no}' AND SAQRSP.PAR_SERVICE_ID = '{service_id}'""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, part_no = spare_part, service_id = self.tree_parent_level_0))
                        #newparts bulk add parts
                        elif self.inclusion == 0 and self.new_part == 1:
                            #Log.Info('new part condition')
                            self._process_query("""DELETE SYSPBT FROM SYSPBT JOIN SAQRSP ON SYSPBT.SAP_PART_NUMBER = SAQRSP.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQRSP.QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQRSP.QTEREV_RECORD_ID WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRSP.NEW_PART='True' AND SAQRSP.PART_NUMBER = '{part_no}' AND SAQRSP.PAR_SERVICE_ID = '{service_id}'""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, part_no = spare_part, service_id = self.tree_parent_level_0))
                    #HPQC 1210 & 2099 end
                            
                    ent_table =""
                    parent_based_condition = ""
                    if self.tree_param in ("Z0091","Z0092","Z0004","Z0006","Z0007","Z0035","Z0009","Z0090") or  self.tree_parent_level_0 in ("Z0091","Z0092","Z0004","Z0006","Z0007","Z0035","Z0009","Z0090"):
                        parent_based_condition = " AND SAQTSV.SERVICE_ID = 'Z0101'"		
                    # if self.tree_parent_level_0 == 'Z0009' and self.inclusion == 1:
                    # 	parent_based_condition = " AND SAQTSV.SERVICE_ID = 'Z0100'"	
                    # if self.tree_param in ("Z0091","Z0092","Z0004","Z0006","Z0007","Z0035","Z0009"):
                    # 	ent_table = "SAQTSE"
                    if self.tree_parent_level_0 in ("Z0091","Z0092","Z0004","Z0006","Z0007","Z0035","Z0009"):
                        ent_table = "SAQSGE"
                    if self.tree_parent_level_0 == 'Z0092':
                        get_entitlement_xml =Sql.GetFirst("""select ENTITLEMENT_XML from {ent_table} (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}'""".format(QuoteRecordId = self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, service_id = self.tree_parent_level_0, ent_table = ent_table,greenbook =  self.tree_param ))
                        if get_entitlement_xml :
                            pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
                            pattern_id = re.compile(r'<ENTITLEMENT_ID>AGS_[^>]*?_TSC_CONSUM</ENTITLEMENT_ID>')
                            pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>Some Inclusions</ENTITLEMENT_DISPLAY_VALUE>')
                            updateentXML = get_entitlement_xml.ENTITLEMENT_XML
                            flag_excluse=0
                            
                            for m in re.finditer(pattern_tag, updateentXML):
                                sub_string = m.group(1)
                                get_ent_id =re.findall(pattern_id,sub_string)
                                get_ent_name=re.findall(pattern_name,sub_string)
                                if get_ent_id and get_ent_name:
                                    flag_excluse=1
                                    break
                            if flag_excluse==1 and self.inclusion == 1:
                                parent_based_condition = " AND SAQTSV.SERVICE_ID in ('Z0100','Z0101')"		

                    #fab_count = SqlHelper.GetList("SELECT COUNT(FABLOCATION_ID) AS COUNT from SAQSCO WHERE GREENBOOK = '"+str(self.tree_param)"' AND 	SERVICE_ID = '"+str(self.treeparentparam)+"' AND QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' GROUP BY FABLOCATION_ID")
                    fab_count = Sql.GetFirst("SELECT COUNT(DISTINCT FABLOCATION_ID) AS COUNT from SAQSCO WHERE GREENBOOK = '{}' AND 	SERVICE_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' GROUP BY FABLOCATION_ID".format(self.tree_param,self.tree_parent_level_0,self.contract_quote_record_id, self.quote_revision_record_id ))
                    if ('Z0101' in parent_based_condition or'Z0100' in parent_based_condition ) and self.tree_parent_level_0 in ("Z0091","Z0092","Z0004","Z0006","Z0007","Z0035","Z0009","Z0090"):
                        for i in range(fab_count.COUNT):
                            # INC08593801 - Start - M
                            # INC08733295 - Start - M
                            self._process_query("""
                                                INSERT SAQRSP (QUOTE_REV_PO_PRODUCT_LIST_ID, BASEUOM_ID, BASEUOM_RECORD_ID,SALESUOM_CONVERSION_FACTOR, SALESUOM_ID, SALESUOM_RECORD_ID,PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID,QUANTITY, QUOTE_ID, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,NEW_PART,INCLUDED)
                                                SELECT DISTINCT
                                                    CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_PRODUCT_LIST_ID,
                                                    BASEUOM_ID,
                                                    BASEUOM_RECORD_ID,
                                                    SALESUOM_CONVERSION_FACTOR, 
                                                    SALESUOM_ID,
                                                    SALESUOM_RECORD_ID,
                                                    PART_DESCRIPTION,
                                                    PART_NUMBER,
                                                    PART_RECORD_ID,
                                                    QUANTITY,
                                                    QUOTE_ID,
                                                    QUOTE_RECORD_ID,
                                                    QTEREV_ID,
                                                    QTEREV_RECORD_ID,
                                                    SERVICE_DESCRIPTION,
                                                    SERVICE_ID,
                                                    SERVICE_RECORD_ID,
                                                    PAR_SERVICE_DESCRIPTION,
                                                    PAR_SERVICE_ID,
                                                    PAR_SERVICE_RECORD_ID,
                                                    GREENBOOK,
                                                    GREENBOOK_RECORD_ID,
                                                    FABLOCATION_ID,
                                                    FABLOCATION_NAME,
                                                    FABLOCATION_RECORD_ID,
                                                    {UserId} as CPQTABLEENTRYADDEDBY, 
                                                    GETDATE() as CPQTABLEENTRYDATEADDED,
                                                    {new_part} as NEW_PART,
                                                    {included} as INCLUDED
                                                FROM (
                                                SELECT 
                                                    DISTINCT
                                                    MAMTRL.UNIT_OF_MEASURE as BASEUOM_ID,
                                                    MAMTRL.UOM_RECORD_ID as BASEUOM_RECORD_ID,
                                                    1.00 as SALESUOM_CONVERSION_FACTOR,
                                                    CASE WHEN MAMSOP.SALESUOM_ID<>'' THEN MAMSOP.SALESUOM_ID ELSE MAMTRL.UNIT_OF_MEASURE END as SALESUOM_ID,
                                                    CASE WHEN MAMSOP.SALESUOM_RECORD_ID<>'' THEN MAMSOP.SALESUOM_RECORD_ID ELSE MAMTRL.UOM_RECORD_ID END as SALESUOM_RECORD_ID,
                                                    MAMTRL.SAP_DESCRIPTION as PART_DESCRIPTION,
                                                    MAMTRL.SAP_PART_NUMBER as PART_NUMBER,
                                                    MAMTRL.MATERIAL_RECORD_ID as PART_RECORD_ID,
                                                    0 as QUANTITY,
                                                    SAQTMT.QUOTE_ID as QUOTE_ID,
                                                    SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID as QUOTE_RECORD_ID,
                                                    SAQTMT.QTEREV_ID as QTEREV_ID,
                                                    SAQTMT.QTEREV_RECORD_ID as QTEREV_RECORD_ID,
                                                    SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
                                                    SAQTSV.SERVICE_ID as SERVICE_ID,
                                                    SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
                                                    SAQTSV.PAR_SERVICE_DESCRIPTION as PAR_SERVICE_DESCRIPTION,
                                                    SAQTSV.PAR_SERVICE_ID as PAR_SERVICE_ID,
                                                    SAQTSV.PAR_SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID,
                                                    '{green_book}' as GREENBOOK,
                                                    SAQSCO.GREENBOOK_RECORD_ID as GREENBOOK_RECORD_ID,
                                                    SAQSCO.FABLOCATION_ID as FABLOCATION_ID,
                                                    SAQSCO.FABLOCATION_NAME as FABLOCATION_NAME,
                                                    SAQSCO.FABLOCATION_RECORD_ID as FABLOCATION_RECORD_ID
                                                FROM SYSPBT (NOLOCK)
                                                JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SYSPBT.SAP_PART_NUMBER
                                                JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID
                                            JOIN SAQTSV (NOLOCK) ON SAQTSV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQTSV.PAR_SERVICE_ID = '{service_id}'
                                            JOIN SAQSCO (NOLOCK) ON SAQSCO.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQSCO.GREENBOOK = '{green_book}'
                                                JOIN MAMSOP (NOLOCK) ON MAMSOP.MATERIAL_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID AND MAMSOP.SALESORG_RECORD_ID = SAQTSV.SALESORG_RECORD_ID
                                                WHERE SYSPBT.BATCH_STATUS = 'IN PROGRESS' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND MAMTRL.PRODUCT_TYPE IS NULL {ParentBasedCondition}) IQ
                                                """.format(
                                    green_book =self.tree_param,
                                    service_id = self.tree_parent_level_0 if self.tree_parent_level_0 in ("Z0091","Z0092","Z0004","Z0006","Z0007","Z0035","Z0009","Z0090") else self.tree_param,
                                    BatchGroupRecordId=batch_group_record_id,
                                    QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,
                                    UserId=self.user_id,
                                    ParentBasedCondition=parent_based_condition,
                                    new_part= self.new_part if self.new_part else 0,
                                    included = self.inclusion
                                )
                            )
                    # INC08593801 - End - M
                    # INC08733295 - End - M
                    
                    # elif 'Z0100' in parent_based_condition :
                    # 	Trace.Write("z0100---11")
                    # 	#for i in range(fab_count.COUNT):
                    # 	self._process_query("""INSERT SAQRSP (QUOTE_REV_PO_PRODUCT_LIST_ID,PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID,PROD_INSP_MEMO,QUANTITY, QUOTE_ID, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,NEW_PART,INCLUDED,UNIT_PRICE,EXTENDED_PRICE,UNIT_PRICE_INGL_CURR,EXTENDED_PRICE_INGL_CURR)
                    # 			SELECT DISTINCT
                    # 				CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_PRODUCT_LIST_ID,
                    # 				PART_DESCRIPTION,
                    # 				PART_NUMBER,
                    # 				PART_RECORD_ID,
                    # 				PROD_INSP_MEMO,
                    # 				QUANTITY,
                    # 				QUOTE_ID,
                    # 				QUOTE_RECORD_ID,
                    # 				QTEREV_ID,
                    # 				QTEREV_RECORD_ID,
                    # 				SERVICE_DESCRIPTION,
                    # 				SERVICE_ID,
                    # 				SERVICE_RECORD_ID,
                    # 				PAR_SERVICE_DESCRIPTION,
                    # 				PAR_SERVICE_ID,
                    # 				PAR_SERVICE_RECORD_ID,
                    # 				GREENBOOK,
                    # 				GREENBOOK_RECORD_ID,
                    # 				FABLOCATION_ID,
                    # 				FABLOCATION_NAME,
                    # 				FABLOCATION_RECORD_ID,
                    # 				{UserId} as CPQTABLEENTRYADDEDBY, 
                    # 				GETDATE() as CPQTABLEENTRYDATEADDED,
                    # 				{new_part} as NEW_PART,
                    # 				1 as INCLUDED,
                    # 				CASE WHEN SERVICE_ID = 'Z0101' THEN '0' ELSE null END AS UNIT_PRICE,
                    # 				CASE WHEN SERVICE_ID = 'Z0101' THEN '0' ELSE null END AS EXTENDED_PRICE,
                    # 				CASE WHEN SERVICE_ID = 'Z0101' THEN '0' ELSE null END AS UNIT_PRICE_INGL_CURR,
                    # 				CASE WHEN SERVICE_ID = 'Z0101' THEN '0' ELSE null END AS EXTENDED_PRICE_INGL_CURR
                    # 			FROM (
                    # 			SELECT 
                    # 				DISTINCT
                    # 				MAMTRL.SAP_DESCRIPTION as PART_DESCRIPTION,
                    # 				MAMTRL.SAP_PART_NUMBER as PART_NUMBER,
                    # 				MAMTRL.MATERIAL_RECORD_ID as PART_RECORD_ID,
                    # 				MAMTRL.PROD_INSP_MEMO as PROD_INSP_MEMO,
                    # 				0 as QUANTITY,
                    # 				SAQTMT.QUOTE_ID as QUOTE_ID,
                    # 				SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID as QUOTE_RECORD_ID,
                    # 				SAQTMT.QTEREV_ID as QTEREV_ID,
                    # 				SAQTMT.QTEREV_RECORD_ID as QTEREV_RECORD_ID,
                    # 				SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
                    # 				SAQTSV.SERVICE_ID as SERVICE_ID,
                    # 				SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
                    # 				SAQTSV.PAR_SERVICE_DESCRIPTION as PAR_SERVICE_DESCRIPTION,
                    # 				SAQTSV.PAR_SERVICE_ID as PAR_SERVICE_ID,
                    # 				SAQTSV.PAR_SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID,
                    # 				null as GREENBOOK,
                    # 				null as GREENBOOK_RECORD_ID,
                    # 				null as FABLOCATION_ID,
                    # 				null as FABLOCATION_NAME,
                    # 				null as FABLOCATION_RECORD_ID
                    # 			FROM SYSPBT (NOLOCK)
                    # 			JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SYSPBT.SAP_PART_NUMBER
                    # 			JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID
                    # 			JOIN SAQTSV (NOLOCK) ON SAQTSV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQTSV.PAR_SERVICE_ID = '{service_id}' 
                    # 			JOIN SAQSCO (NOLOCK) ON SAQSCO.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQSCO.PAR_SERVICE_ID = SAQTSV.PAR_SERVICE_ID AND SAQSCO.SERVICE_ID = SAQTSV.SERVICE_ID  
                    # 			JOIN MAMSOP (NOLOCK) ON MAMSOP.MATERIAL_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID AND MAMSOP.SALESORG_RECORD_ID = SAQTSV.SALESORG_RECORD_ID
                    # 			WHERE SYSPBT.BATCH_STATUS = 'IN PROGRESS' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND MAMTRL.PRODUCT_TYPE IS NULL AND MAMTRL.IS_SPARE_PART = 1 {ParentBasedCondition}) IQ
                    # 			""".format(fab_location_id = '',
                    # 				service_id = self.tree_param,
                    # 				BatchGroupRecordId=batch_group_record_id,
                    # 				QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,
                    # 				UserId=self.user_id,
                    # 				ParentBasedCondition=parent_based_condition,
                    # 				new_part= self.new_part if self.new_part else 0
                    # 			)
                    # 	)
            

                    # get_child_service_id = Sql.GetFirst("""SELECT SAQTSV.SERVICE_ID FROM SAQTSV (NOLOCK) JOIN SAQRSP (NOLOCK) ON SAQRSP.SERVICE_ID = SAQTSV.SERVICE_ID AND SAQRSP.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID AND SAQRSP.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID WHERE SAQTSV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSV.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.PAR_SERVICE_ID = '{service_id}'""".format(QuoteRecordId = self.contract_quote_record_id,RevisionRecordId = self.quote_revision_record_id,service_id = self.tree_parent_level_0 if self.tree_parent_level_0 in ("Z0091","Z0092","Z0004","Z0006","Z0007","Z0035","Z0009") else self.tree_param))
                    # if get_child_service_id:
                    # 	if get_child_service_id.SERVICE_ID == 'Z0101':
                    # 		spareparts_config_status_count = Sql.GetFirst(""" SELECT COUNT(CONFIGURATION_STATUS) AS COUNT FROM SAQTSE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND CONFIGURATION_STATUS='COMPLETE' """.format(self.contract_quote_record_id,self.quote_revision_record_id,get_child_service_id.SERVICE_ID))
                    # 		if spareparts_config_status_count.COUNT > 0:
                    # 			data = ScriptExecutor.ExecuteGlobal("CQINSQTITM",{"ContractQuoteRecordId":self.contract_quote_record_id, "ContractQuoteRevisionRecordId":self.quote_revision_record_id, "ServiceId":get_child_service_id.SERVICE_ID, "ActionType":'INSERT_LINE_ITEMS'})

                        
                self._process_query(
                    """DELETE FROM SYSPBT WHERE SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'  and SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' and SYSPBT.BATCH_STATUS = 'IN PROGRESS'""".format(
                        BatchGroupRecordId=batch_group_record_id,RevisionRecordId=self.quote_revision_record_id
                    )
                )
                #INC08733295 - Start - A
                Sql.RunQuery(
                    """UPDATE SAQRSP SET SAQRSP.SALESUOM_CONVERSION_FACTOR =   CASE WHEN M.BASE_QUANTITY=0.00 THEN 1.00 ELSE M.BASE_QUANTITY END FROM SAQRSP S INNER JOIN MAMUOC M ON S.PART_NUMBER= M.SAP_PART_NUMBER WHERE S.BASEUOM_ID=M.BASEUOM_ID AND  S.SALESUOM_ID=M.CONVERSIONUOM_ID AND S.QUOTE_RECORD_ID = '{QuoteRecordId}' AND S.QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(QuoteRecordId = self.contract_quote_record_id ,RevisionRecordId =self.quote_revision_record_id)
                )
                #INC08733295 - END - A
        return True

    def _update(self):
        pass

    def _delete(self):
        pass
    ##A055S000P01-14047 start 
    # def getschedule_delivery_insert(self,billing_date= ''):
    # 	Trace.Write('23---'+str(billing_date))
    # 	getschedule_details = Sql.RunQuery("INSERT SAQSPD  (QUOTE_REV_PO_PART_DELIVERY_SCHEDULES_RECORD_ID,DELIVERY_SCHED_CAT,PART_DESCRIPTION,PART_NUMBER,PART_RECORD_ID,QUANTITY,CUSTOMER_ANNUAL_QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,DELIVERY_MODE,QTEREVSPT_RECORD_ID,QTEREV_RECORD_ID)  select CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_PART_DELIVERY_SCHEDULES_RECORD_ID,null as DELIVERY_SCHED_CAT,{delivery_date} as DELIVERY_SCHED_DATE,PART_DESCRIPTION,PART_NUMBER,PART_RECORD_ID, CUSTOMER_ANNUAL_QUANTITY as QUANTITY,CUSTOMER_ANNUAL_QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,DELIVERY_MODE,QUOTE_SERVICE_PART_RECORD_ID as QTEREVSPT_RECORD_ID,QTEREV_RECORD_ID FROM SAQSPT where SCHEDULE_MODE= 'SCHEDULED' and DELIVERY_MODE = 'OFFSITE' and QUOTE_RECORD_ID = '{contract_rec_id}' AND QTEREV_RECORD_ID = '{qt_rev_id}' and CUSTOMER_ANNUAL_QUANTITY >0".format(delivery_date =billing_date,contract_rec_id= self.contract_quote_record_id,qt_rev_id = self.quote_revision_record_id) )
    #A055S000P01-14047 end

    def periods_insert(self,contract_quote_record_id,quote_revision_record_id):
        count = Sql.GetFirst("SELECT COUNT(*) as CNT FROM SAQRDS WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
        if count.CNT==0:
            quotedetails = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'")
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
                Query = "INSERT SAQRDS (QUOTE_REV_DELIVERY_SCHEDULE_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,DELIVERY_DATE,DELIVERY_PERIOD) select CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_DELIVERY_SCHEDULE_RECORD_ID,'{quote_id}' as QUOTE_ID,'{contract_rec_id}' as QUOTE_RECORD_ID,'{qt_rev_id}' as QTEREV_ID,'{qt_rev_recid}' as QTEREV_RECORD_ID,'{delivery_date}' as DELIVERY_DATE,'{delivery_period}' as DELIVERY_PERIOD ".format(quote_id=self.contract_quote_id,contract_rec_id= self.contract_quote_record_id,qt_rev_id = self.quote_revision_id,qt_rev_recid = self.quote_revision_record_id,delivery_date =billing_date,delivery_period=index+1)
                periods_query = Sql.RunQuery(Query)

    def CreateEntitlements(self,OfferingRow_detail):		
        Request_URL="https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"
                
        Fullresponse = ScriptExecutor.ExecuteGlobal("CQENTLNVAL", {'action':'GET_RESPONSE','partnumber':OfferingRow_detail.get("SERVICE_ID"),'request_url':Request_URL,'request_type':"New"})
        Fullresponse=str(Fullresponse).replace(": true",": \"true\"").replace(": false",": \"false\"")
        Fullresponse= eval(Fullresponse)
        ##getting configuration_status status
        if Fullresponse['complete'] == 'true' and Fullresponse['consistent'] == 'true' :
            configuration_status = 'COMPLETE'
        elif Fullresponse['complete'] == 'false':
            configuration_status = 'INCOMPLETE'
                                                                                            
                                        
        else:
            configuration_status = 'ERROR'
        attributesdisallowedlst=[]
        attributeReadonlylst=[]
        attributesallowedlst=[]
        attributedefaultvalue = []
        overall_att_list_sub =[]
        overallattributeslist =[]
        attributevalues={}
        get_toolptip= ''
        #getquote_sales_val = AttributeID_Pass = ''
        for rootattribute, rootvalue in Fullresponse.items():
            if rootattribute=="rootItem":
                for Productattribute, Productvalue in rootvalue.items():
                    if Productattribute=="characteristics":
                        for prdvalue in Productvalue:
                            overallattributeslist.append(prdvalue['id'])
                            if prdvalue['id'].startswith('AGS_Z0046_'):
                                overall_att_list_sub.append(prdvalue['id'])
                            if prdvalue['visible'] =='false':
                                attributesdisallowedlst.append(prdvalue['id'])
                            else:								
                                attributesallowedlst.append(prdvalue['id'])
                            if prdvalue['readOnly'] =='true':
                                attributeReadonlylst.append(prdvalue['id'])
                            for attribute in prdvalue['values']:								
                                attributevalues[str(prdvalue['id'])]=attribute['value']
                                if attribute["author"] in ('Default','System'):
                                    #Trace.Write('prdvalue---1554-----'+str(prdvalue['id']))
                                    attributedefaultvalue.append(prdvalue["id"])
        attributesallowedlst = list(set(attributesallowedlst))
        overallattributeslist = list(set(overallattributeslist))		
        HasDefaultvalue=False
        ProductVersionObj=Sql.GetFirst("Select product_id from product_versions(nolock) where SAPKBId = '"+str(Fullresponse['kbId'])+"' AND SAPKBVersion='"+str(Fullresponse['kbKey']['version'])+"'")
        is_default = ent_val_code = ''
        Attributeid_list = {}
        get_toolptip = ""
        if ProductVersionObj:
            insertservice = ""
            tbrow={}	
            for attrs in overallattributeslist:
                
                if attrs in attributevalues:					
                    HasDefaultvalue=True					
                    STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}' ".format(attrs))
                    ent_disp_val = attributevalues[attrs]
                    ent_val_code = attributevalues[attrs]
                    #Trace.Write("ent_disp_val----"+str(ent_disp_val))
                else:					
                    HasDefaultvalue=False
                    ent_disp_val = ""
                    ent_val_code = ""
                    STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs))
                    
                ATTRIBUTE_DEFN=Sql.GetFirst("SELECT * FROM ATTRIBUTE_DEFN (NOLOCK) WHERE SYSTEM_ID='{}'".format(attrs))
                PRODUCT_ATTRIBUTES=Sql.GetFirst("SELECT A.ATT_DISPLAY_DESC,P.ATTRDESC FROM ATT_DISPLAY_DEFN (NOLOCK) A INNER JOIN PRODUCT_ATTRIBUTES (NOLOCK) P ON A.ATT_DISPLAY=P.ATT_DISPLAY WHERE P.PRODUCT_ID={} AND P.STANDARD_ATTRIBUTE_CODE={}".format(ProductVersionObj.product_id,STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE))
                if PRODUCT_ATTRIBUTES:
                    if PRODUCT_ATTRIBUTES.ATTRDESC:
                        get_toolptip = PRODUCT_ATTRIBUTES.ATTRDESC
                    if PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC:
                        if PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC in ('Drop Down','Check Box') and ent_disp_val:
                            get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
                            ent_disp_val = get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL 
                
                getslaes_value  = Sql.GetFirst("SELECT SALESORG_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '"+str(OfferingRow_detail.get("QUOTE_RECORD_ID"))+"'")
                if getslaes_value:
                    getquote_sales_val = getslaes_value.SALESORG_ID
                get_il_sales = Sql.GetList("select SALESORG_ID from SASORG where country = 'IL'")
                get_il_sales_list = [val.SALESORG_ID for val in get_il_sales]
                if str(attrs) == 'AGS_REL_STDATE' and 'Z0007' in OfferingRow_detail.get("SERVICE_ID"):
                    try:						
                        QuoteStartDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteStartDate').Content, '%Y-%m-%d').date()
                        ent_disp_val = 	str(QuoteStartDate)
                        ent_val_code = ''					
                    except:						
                        ent_disp_val = ent_disp_val
                        ent_val_code = ''
                else:
                    ent_disp_val = ent_disp_val
                    ent_val_code = ent_val_code
                if ATTRIBUTE_DEFN:
                    if ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME.upper() == "FAB LOCATION":
                        Trace.Write(str(attrs)+'--attrs---1118----'+str(ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME))
                        Trace.Write(str(getquote_sales_val)+'-getquote_sales_val---'+str(get_il_sales_list))
                        #AttributeID_Pass = attrs
                        if getquote_sales_val in get_il_sales_list:
                            Attributeid_list[attrs] = "Israel"
                        else:
                            Attributeid_list[attrs] = 'ROW'

                    #NewValue = 'ROW'
                    #NewValue = ''
                Trace.Write("attrs---"+str(attrs))
                # if str(attrs) == 'AGS_{}_CVR_CNTCOV'.format(OfferingRow_detail.get("SERVICE_ID")):
                # 	Trace.Write("attrs-1111--"+str(attrs))
                # 	Attributeid_list[attrs] = "5x8"
                if str(attrs) == 'AGS_CON_DAY' and 'Z0016' in OfferingRow_detail.get("SERVICE_ID"): 
                    try:						
                        QuoteEndDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteExpirationDate').Content, '%Y-%m-%d').date()
                        QuoteStartDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteStartDate').Content, '%Y-%m-%d').date()
                        contract_days = (QuoteEndDate - QuoteStartDate).days
                        ent_disp_val = 	str(contract_days)
                    except:						
                        ent_disp_val = ent_disp_val	
                else:
                    ent_disp_val = ent_disp_val	
                #A055S000P01-7401 START
                if str(attrs) in ('AGS_POA_PROD_TYPE','AGS_{}_GEN_POAPDT'.format(OfferingRow_detail.get("SERVICE_ID")) ) and ent_disp_val != '':
                    val = ""
                    if str(ent_disp_val) == 'Comprehensive':
                        val = "COMPREHENSIVE SERVICES"
                    elif str(ent_disp_val) == 'Complementary':
                        val = "COMPLEMENTARY PRODUCTS"
                    Sql.RunQuery("UPDATE SAQTSV SET SERVICE_TYPE = '{}' WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(str(val),self.contract_quote_record_id,self.quote_revision_record_id,OfferingRow_detail.get("SERVICE_ID")))
                    #Log.Info('ent_disp_val---'+str(ent_disp_val)+'--val-----'+str(val))
                #A055S000P01-7401 END
                DTypeset={"Drop Down":"DropDown","Free Input, no Matching":"FreeInputNoMatching","Check Box":"CheckBox"}
                insertservice += """<QUOTE_ITEM_ENTITLEMENT>
                    <ENTITLEMENT_ID>{ent_name}</ENTITLEMENT_ID>
                    <ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
                    <ENTITLEMENT_DESCRIPTION>{tool_desc}</ENTITLEMENT_DESCRIPTION>
                    <ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
                    <ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
                    <ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
                    <ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
                    <IS_DEFAULT>{is_default}</IS_DEFAULT>
                    <PRICE_METHOD>{pm}</PRICE_METHOD>
                    <CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
                    <ENTITLEMENT_NAME>{ent_desc}</ENTITLEMENT_NAME>
                    </QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrs),
                        ent_val_code = ent_val_code,
                        ent_type = DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC] if PRODUCT_ATTRIBUTES else  '',
                        ent_desc = ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME.replace("&",";#38").replace(">","&gt;").replace("<","&lt;"),
                        ent_disp_val = ent_disp_val.replace("&",";#38").replace(">","&gt;").replace("<","&lt;")  if HasDefaultvalue==True else '',
                        ct = '',pi = '',
                        is_default = '1' if str(attrs) in attributedefaultvalue else '0',
                        pm = '',cf = '',
                        tool_desc = get_toolptip.replace("'","''").replace("&",";#38").replace(">","&gt;").replace("<","&lt;") 
                    )
            insertservice = insertservice.encode('ascii', 'ignore').decode('ascii')
            
            tbrow["QUOTE_SERVICE_ENTITLEMENT_RECORD_ID"]=str(Guid.NewGuid()).upper()
            tbrow["QUOTE_ID"]=OfferingRow_detail.get("QUOTE_ID")
            tbrow["ENTITLEMENT_XML"]=insertservice
            tbrow["QUOTE_NAME"]=str(OfferingRow_detail.get("QUOTE_NAME")).replace("'","''")#INC08658971
            tbrow["QUOTE_RECORD_ID"]=OfferingRow_detail.get("QUOTE_RECORD_ID")
            tbrow["QTESRV_RECORD_ID"]=OfferingRow_detail.get("QUOTE_SERVICE_RECORD_ID")
            tbrow["SERVICE_RECORD_ID"]=OfferingRow_detail.get("SERVICE_RECORD_ID")
            tbrow["SERVICE_ID"]=OfferingRow_detail.get("SERVICE_ID")
            tbrow["SERVICE_DESCRIPTION"]=OfferingRow_detail.get("SERVICE_DESCRIPTION").replace("'","''")
            tbrow["CPS_CONFIGURATION_ID"]=Fullresponse['id']
            tbrow["SALESORG_RECORD_ID"]=OfferingRow_detail.get("SALESORG_RECORD_ID")
            tbrow["SALESORG_ID"]=OfferingRow_detail.get("SALESORG_ID")
            tbrow["SALESORG_NAME"]=OfferingRow_detail.get("SALESORG_NAME")
            tbrow["CPS_MATCH_ID"] = 1
            tbrow["CPQTABLEENTRYADDEDBY"] = self.user_id
            tbrow["CPQTABLEENTRYDATEADDED"] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")  
            tbrow["QTEREV_RECORD_ID"] = self.quote_revision_record_id
            tbrow["QTEREV_ID"] = self.quote_revision_id
            tbrow["CONFIGURATION_STATUS"] = configuration_status
            #tbrow["IS_DEFAULT"] = '1'

            columns = ', '.join("" + str(x) + "" for x in tbrow.keys())
            values = ', '.join("'" + str(x) + "'" for x in tbrow.values())
            insert_qtqtse_query = "INSERT INTO SAQTSE ( %s ) VALUES ( %s );" % (columns, values)
                                                                
            Sql.RunQuery(insert_qtqtse_query)
            if Attributeid_list:
                Trace.Write('1406---AttributeID_Pass---'+str(Attributeid_list))
                try:
                    for attr_key,attr_value in Attributeid_list.items():
                        Trace.Write('1408--NewValue----'+str(Attributeid_list))					
                        add_where =''
                        ServiceId = OfferingRow_detail.get("SERVICE_ID")
                        whereReq = "QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(OfferingRow_detail.get("QUOTE_RECORD_ID"),OfferingRow_detail.get("SERVICE_ID"),self.quote_revision_record_id)
                        ent_params_list = str(whereReq)+"||"+str(add_where)+"||"+str(attr_key)+"||"+str(attr_value)+"||"+str(ServiceId) + "||" + 'SAQTSE'
                        result = ScriptExecutor.ExecuteGlobal("CQASSMEDIT", {"ACTION": 'UPDATE_ENTITLEMENT', 'ent_params_list':ent_params_list})
                except:
                    #Log.Info('1408------error--')
                    Trace.Write('error--296')
            try:
                if OfferingRow_detail.get("SERVICE_ID") == 'Z0016':
                    try:
                        QuoteEndDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteExpirationDate').Content, '%Y-%m-%d').date()
                        QuoteStartDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteStartDate').Content, '%Y-%m-%d').date()
                        contract_days = (QuoteEndDate - QuoteStartDate).days
                        ent_disp_val = 	str(contract_days)
                    except:						
                        ent_disp_val = ent_disp_val					

                    # try:
                    # 	AttributeID = 'AGS_CON_DAY'
                    # 	NewValue = ent_disp_val
                    # 	add_where =''
                    # 	ServiceId = OfferingRow_detail.get("SERVICE_ID")
                    # 	whereReq = "QUOTE_RECORD_ID = '"+str(OfferingRow_detail.get('QUOTE_RECORD_ID'))+"' and SERVICE_ID like '%Z0016%' and QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' "

                    # 	ent_params_list = str(whereReq)+"||"+str(add_where)+"||"+str(AttributeID)+"||"+str(ent_disp_val)+"||"+str(ServiceId) + "||" + 'SAQTSE'
                    # 	result = ScriptExecutor.ExecuteGlobal("CQASSMEDIT", {"ACTION": 'UPDATE_ENTITLEMENT', 'ent_params_list':ent_params_list})
                    # except:
                    # 	pass
        
            except:
                pass
            #calling pre-logic valuedriver script
            try:
                Trace.Write("PREDEFINED WAFER DRIVER IFLOW")
                where_condition = " WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND SERVICE_ID = '{}' ".format(self.contract_quote_record_id, self.quote_revision_record_id, OfferingRow_detail.get("SERVICE_ID"))
                # CQTVLDRIFW.valuedriver_predefined(self.contract_quote_record_id,"SERVICE_LEVEL",OfferingRow_detail.get("SERVICE_ID"),self.user_id,self.quote_revision_record_id, where_condition)
                
                predefined = ScriptExecutor.ExecuteGlobal("CQVLDPRDEF",{"where_condition": where_condition,"quote_rec_id": self.contract_quote_record_id ,"level":"SERVICE_LEVEL", "treeparam": OfferingRow_detail.get("SERVICE_ID"),"user_id": self.user_id, "quote_rev_id":self.quote_revision_record_id})

            except:
                Trace.Write("EXCEPT---PREDEFINED DRIVER IFLOW")
            ##HPQC DEFECT 544 CODE STARTS..
            try:
                where_condition = " WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND SERVICE_ID = '{}' ".format(self.contract_quote_record_id, self.quote_revision_record_id, OfferingRow_detail.get("SERVICE_ID"))
                ##SAQTSE ent columns update
                ScriptExecutor.ExecuteGlobal("CQENTLNVAL", {'action':'ENTITLEMENT_COLUMN_UPDATE',
                                                                    'partnumber':OfferingRow_detail.get("SERVICE_ID"),
                                                                    'where_cond' :where_condition, 
                                                                    'ent_level_table': "SAQTSE"
                                                                    })
            except:
                Log.Info("SAQTSE UPDATE ERROR")
            ##HPQC DEFECT 544 CODE ENDS..
            if OfferingRow_detail.get("SERVICE_ID") in ['Z0108','Z0110']:
                try:

                    #A055S000P01-13524 start(UPDATE SAQSPT)
                    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                    quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
                    if OfferingRow_detail.get("SERVICE_ID") == "Z0108":
                        Trace.Write('###Periods insert for Z0108')
                        self.periods_insert(contract_quote_record_id,quote_revision_record_id)
                    get_party_role = Sql.GetList("SELECT CPQ_PARTNER_FUNCTION, PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' and CPQ_PARTNER_FUNCTION in ('SOLD TO')")
                    account_info = {}
                    for keyobj in get_party_role:
                        account_info[keyobj.CPQ_PARTNER_FUNCTION] = keyobj.PARTY_ID
                        
                    get_party_role = Sql.GetList("SELECT CPQ_PARTNER_FUNCTION, PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' and CPQ_PARTNER_FUNCTION in ('SHIP TO')")
                    shipto_list=[]
                    for keyobj in get_party_role:
                        shipto_list.append('00'+str(keyobj.PARTY_ID))
                    shiptostr=str(shipto_list)
                    shiptostr=re.sub(r"'",'"',shiptostr)
                    account_info['SHIP TO']=shiptostr
    
                    #get info from revision table start
                    sales_id = sales_rec =qt_rev_id = qt_id=''
                    get_rev_sales_ifo = Sql.GetFirst("select QUOTE_ID,SALESORG_ID,SALESORG_RECORD_ID,QTEREV_ID,CONTRACT_VALID_FROM,CONTRACT_VALID_TO from SAQTRV where QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QUOTE_REVISION_RECORD_ID = '"+str(quote_revision_record_id)+"'")
                    if get_rev_sales_ifo:
                        sales_id = get_rev_sales_ifo.SALESORG_ID
                        sales_rec = get_rev_sales_ifo.SALESORG_RECORD_ID
                        qt_rev_id = get_rev_sales_ifo.QTEREV_ID
                        qt_id = get_rev_sales_ifo.QUOTE_ID
                    #get info from revision table end
                    parts_value = 0
                    Service_Id = OfferingRow_detail.get("SERVICE_ID")
                    entitlement_obj = Sql.GetFirst("select ENTITLEMENT_XML from SAQTSE (nolock) where QUOTE_RECORD_ID  = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
                    entitlement_xml = entitlement_obj.ENTITLEMENT_XML
                    quote_item_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
                    entitlement_value_str = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(Service_Id)+'[^>]*?_TSC_SCPT</ENTITLEMENT_ID>')
                    value = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
                    for m in re.finditer(quote_item_tag, entitlement_xml):
                        sub_string = m.group(1)
                        scheduled_parts =re.findall(entitlement_value_str,sub_string)
                        scheduled_value =re.findall(value,sub_string)
                        if scheduled_parts and scheduled_value:
                            parts_value = scheduled_value[0]
                            break
                        Trace.Write("Chkng_param "+str(OfferingRow_detail.get("SERVICE_ID")))
                    ScriptExecutor.ExecuteGlobal('CQPARTSINS',{"CPQ_Columns":{"Action": "LoadParts","QuoteID":self.contract_quote_id}})
                    #A055S000P01-14047 start
                    if OfferingRow_detail.get("SERVICE_ID") == "Z0108":
                        quotedetails = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QUOTE_REVISION_RECORD_ID = '"+str(quote_revision_record_id)+"'")
                        contract_start_date = quotedetails.CONTRACT_VALID_FROM
                        contract_end_date = quotedetails.CONTRACT_VALID_TO
                        start_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_start_date), '%m/%d/%Y')
                        end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_end_date), '%m/%d/%Y')

                        diff1 = end_date - start_date
                        get_totalweeks,remainder = divmod(diff1.days,7)
                        countweeks =0
                        Trace.Write('8--'+str(get_totalweeks))
                        for index in range(0, get_totalweeks):
                            countweeks += 1
                            #Trace.Write('countweeks--'+str(countweeks))
                            billing_date="DATEADD(week, {weeks}, '{BillingDate}')".format(weeks=index, BillingDate=start_date.strftime('%m/%d/%Y'))
                            Trace.Write('billing_date--'+str(billing_date))
                            #getschedule_delivery_insert(billing_date)
                    #A055S000P01-14047 end
                except Exception as e:
                    Trace.Write("EXCEPT----PREDEFINED DRIVER IFLOW"+str(e))

class PartsListModel(ContractQuoteCrudOpertion):
    def __init__(self, **kwargs):		
        ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'), 
                                            tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'),tree_parent_level_1=kwargs.get('tree_parent_level_1'))
        self.opertion = kwargs.get('opertion')
        self.action_type = kwargs.get('action_type')
        self.values = kwargs.get('values')
        self.table_name = kwargs.get('table_name')
        self.all_values = kwargs.get('all_values')		
        self.node_id = ""
        self.new_part = kwargs.get('new_part')
        self.inclusion = kwargs.get('inclusion')
    
    def _create(self):
        if self.action_type == "ADD_PART" or self.action_type == "ADD_SPARE_PART":
            self._add_parts_list()
    
    def _add_parts_list(self):
        master_object_name = "MAMTRL"
        if self.values:
            record_ids = []
            if self.all_values:
                qury_str = ""
                if A_Keys!="" and A_Values!="":
                    for key,val in zip(A_Keys,A_Values):
                        if(val!=""):
                            if key=="MATERIAL_RECORD_ID":
                                key="CpqTableEntryId"
                                val = ''.join(re.findall(r'\d+', val)) if not val.isdigit() else val
                            qury_str+=" MAMTRL."+key+" LIKE '%"+val+"%' AND "
                # INC08593801 - Start - M
                query_str="""SELECT MATERIAL_RECORD_ID,SAP_PART_NUMBER,SAP_DESCRIPTION,PRODUCT_TYPE FROM MAMTRL WHERE SAP_PART_NUMBER NOT IN (SELECT PART_NUMBER FROM {} (NOLOCK) WHERE {} QUOTE_RECORD_ID = '{}' AND  QTEREV_RECORD_ID ='{}')""".format("SAQSPT" if self.action_type == "ADD_SPARE_PART" else "SAQRSP",qury_str,self.contract_quote_record_id,self.quote_revision_record_id)
                query_string=SqlHelper.GetList(query_str)
                # INC08593801 - End - M
                if query_string is not None:
                    record_ids = [data.MATERIAL_RECORD_ID for data in query_string]

                query_string_for_count = "SELECT COUNT(*) as count FROM ({Query_String})OQ".format(
                    Query_String=query_str
                )
                table_count_data = Sql.GetFirst(query_string_for_count)
                if table_count_data is not None:
                    table_total_rows = table_count_data.count
            else:                    
                record_ids = [
                    CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
                    if value.strip() != "" and master_object_name in value
                    else value
                    for value in self.values
                ]
            batch_group_record_id = str(Guid.NewGuid()).upper()
            record_ids = str(str(record_ids)[1:-1].replace("'",""))
            parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")			
            primaryQueryItems = SqlHelper.GetFirst(""+str(parameter.QUERY_CRITERIA_1)+" SYSPBT(BATCH_RECORD_ID,SAP_PART_NUMBER, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,QTEREV_RECORD_ID) SELECT MAMTRL.MATERIAL_RECORD_ID as BATCH_RECORD_ID,MAMTRL.SAP_PART_NUMBER, ''IN PROGRESS'' as BATCH_STATUS, ''"+str(self.contract_quote_id)+"'' as QUOTE_ID, ''"+str(self.contract_quote_record_id)+"'' as QUOTE_RECORD_ID, ''"+str(batch_group_record_id)+"'' as BATCH_GROUP_RECORD_ID,''"+str(self.quote_revision_record_id)+"'' as QTEREV_RECORD_ID FROM MAMTRL (NOLOCK) JOIN splitstring(''"+record_ids+"'') ON ltrim(rtrim(NAME)) = MAMTRL.MATERIAL_RECORD_ID'")
            Trace.Write('##action type '+str(self.action_type))
            if self.tree_param == 'Z0108' or self.tree_param == 'Z0110':
                part_nos =[]
                for val in self.values:
                    val  = val.split('-')[1].lstrip("0")
                    get_part = Sql.GetFirst("SELECT SAP_PART_NUMBER FROM MAMTRL WHERE CpqTableEntryId = '"+str(val)+"' ")
                    part_nos.append(get_part.SAP_PART_NUMBER)
                Trace.Write('###PART_NOS-->'+str(part_nos))
                Trace.Write('###values-->'+str(self.values))
                #calling CQPARTSINS
                #ScriptExecutor.ExecuteGlobal('CQPARTSINS',{"Action": "AddParts","partno":part_nos})
            if self.action_type == "ADD_SPARE_PART":
                parts_value = 0
                Service_Id = self.tree_param
                entitlement_obj = Sql.GetFirst("select ENTITLEMENT_XML from SAQTSE (nolock) where QUOTE_RECORD_ID  = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
                entitlement_xml = entitlement_obj.ENTITLEMENT_XML
                quote_item_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
                entitlement_value_str = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(Service_Id)+'[^>]*?_TSC_SCPT</ENTITLEMENT_ID>')
                value = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
                for m in re.finditer(quote_item_tag, entitlement_xml):
                    sub_string = m.group(1)
                    scheduled_parts =re.findall(entitlement_value_str,sub_string)
                    scheduled_value =re.findall(value,sub_string)
                    if scheduled_parts and scheduled_value:
                        parts_value = scheduled_value[0]
                        break
                if self.tree_param == 'Z0108':
                    delivery_mode = "OFFSITE"
                    schedule_mode= "SCHEDULED" if int(parts_value) > 9 else "UNSCHEDULED"
                elif self.tree_param == 'Z0110':
                    delivery_mode = " "
                    schedule_mode= " "
                part_numbers=''
                part_numbers=str(part_nos)
                part_numbers=part_numbers.replace("'",'"')
                ScriptExecutor.ExecuteGlobal('CQPARTSINS',{"CPQ_Columns":{"Action": "LoadParts","Part_number":part_numbers,"QuoteID":self.contract_quote_id}})
            elif self.action_type == "ADD_PART":
                ent_table =""
                parent_based_condition = ""
                if self.tree_param in ("Z0091","Z0092","Z0004","Z0006","Z0007","Z0035","Z0009","Z0090") or  self.tree_parent_level_0 in ("Z0091","Z0092","Z0004","Z0006","Z0007","Z0035","Z0009","Z0090"):
                    parent_based_condition = " AND SAQTSV.SERVICE_ID = 'Z0101'"		
                # if self.tree_parent_level_0 == 'Z0009' and self.inclusion == 1:
                # 	parent_based_condition = " AND SAQTSV.SERVICE_ID = 'Z0100'"	
                # if self.tree_param in ("Z0091","Z0092","Z0004","Z0006","Z0007","Z0035","Z0009"):
                # 	ent_table = "SAQTSE"
                if self.tree_parent_level_0 in ("Z0091","Z0092","Z0004","Z0006","Z0007","Z0035","Z0009"):
                    ent_table = "SAQSGE"
                if self.tree_parent_level_0 == 'Z0092' and self.inclusion == 1:
                    get_entitlement_xml =Sql.GetFirst("""select ENTITLEMENT_XML from {ent_table} (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}'""".format(QuoteRecordId = self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, service_id = self.tree_parent_level_0, ent_table = ent_table,greenbook =  self.tree_param ))
                    if get_entitlement_xml :
                        pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
                        pattern_id = re.compile(r'<ENTITLEMENT_ID>AGS_[^>]*?_TSC_CONSUM</ENTITLEMENT_ID>')
                        pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>Some Inclusions</ENTITLEMENT_DISPLAY_VALUE>')
                        updateentXML = get_entitlement_xml.ENTITLEMENT_XML
                        flag_excluse=0
                        
                        for m in re.finditer(pattern_tag, updateentXML):
                            sub_string = m.group(1)
                            get_ent_id =re.findall(pattern_id,sub_string)
                            get_ent_name=re.findall(pattern_name,sub_string)
                            if get_ent_id and get_ent_name:
                                flag_excluse=1
                                break
                        if flag_excluse==1 and self.inclusion == 1:
                            parent_based_condition = " AND SAQTSV.SERVICE_ID in ('Z0100','Z0101')"			


                #fab_count = SqlHelper.GetList("SELECT COUNT(FABLOCATION_ID) AS COUNT from SAQSCO WHERE GREENBOOK = '"+str(self.tree_param)"' AND 	SERVICE_ID = '"+str(self.treeparentparam)+"' AND QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' GROUP BY FABLOCATION_ID")
                fab_count = Sql.GetFirst("SELECT COUNT(DISTINCT FABLOCATION_ID) AS COUNT from SAQSCO WHERE GREENBOOK = '{}' AND 	SERVICE_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' GROUP BY FABLOCATION_ID".format(self.tree_param,self.tree_parent_level_0,self.contract_quote_record_id, self.quote_revision_record_id ))
                if ('Z0101' in parent_based_condition or'Z0100' in parent_based_condition ) and self.tree_parent_level_0 in ("Z0091","Z0092","Z0004","Z0006","Z0007","Z0035","Z0009","Z0090"):
                    for i in range(fab_count.COUNT):
                        # INC08593801 - Start - M
                        # INC08733295 - Start - M
                        self._process_query("""
                                                INSERT SAQRSP (QUOTE_REV_PO_PRODUCT_LIST_ID,BASEUOM_ID, BASEUOM_RECORD_ID,SALESUOM_CONVERSION_FACTOR, SALESUOM_ID, SALESUOM_RECORD_ID,PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID,PROD_INSP_MEMO,QUANTITY, QUOTE_ID, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,NEW_PART,INCLUDED)
                                                SELECT DISTINCT
                                                    CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_PRODUCT_LIST_ID,
                                                    BASEUOM_ID,
                                                    BASEUOM_RECORD_ID,
                                                    SALESUOM_CONVERSION_FACTOR, 
                                                    SALESUOM_ID,
                                                    SALESUOM_RECORD_ID,
                                                    PART_DESCRIPTION,
                                                    PART_NUMBER,
                                                    PART_RECORD_ID,
                                                    PROD_INSP_MEMO,
                                                    QUANTITY,
                                                    QUOTE_ID,
                                                    QUOTE_RECORD_ID,
                                                    QTEREV_ID,
                                                    QTEREV_RECORD_ID,
                                                    SERVICE_DESCRIPTION,
                                                    SERVICE_ID,
                                                    SERVICE_RECORD_ID,
                                                    PAR_SERVICE_DESCRIPTION,
                                                    PAR_SERVICE_ID,
                                                    PAR_SERVICE_RECORD_ID,
                                                    GREENBOOK,
                                                    GREENBOOK_RECORD_ID,
                                                    FABLOCATION_ID,
                                                    FABLOCATION_NAME,
                                                    FABLOCATION_RECORD_ID,
                                                    {UserId} as CPQTABLEENTRYADDEDBY, 
                                                    GETDATE() as CPQTABLEENTRYDATEADDED,
                                                    {new_part} as NEW_PART,
                                                    {included} as INCLUDED
                                                FROM (
                                                SELECT 
                                                    DISTINCT
                                                    MAMTRL.UNIT_OF_MEASURE as BASEUOM_ID,
                                                    MAMTRL.UOM_RECORD_ID as BASEUOM_RECORD_ID,
                                                    1.00 as SALESUOM_CONVERSION_FACTOR,
                                                    CASE WHEN MAMSOP.SALESUOM_ID<>'' THEN MAMSOP.SALESUOM_ID ELSE MAMTRL.UNIT_OF_MEASURE END as SALESUOM_ID,
                                                    CASE WHEN MAMSOP.SALESUOM_RECORD_ID<>'' THEN MAMSOP.SALESUOM_RECORD_ID ELSE MAMTRL.UOM_RECORD_ID END as SALESUOM_RECORD_ID,
                                                    MAMTRL.SAP_DESCRIPTION as PART_DESCRIPTION,
                                                    MAMTRL.SAP_PART_NUMBER as PART_NUMBER,
                                                    MAMTRL.MATERIAL_RECORD_ID as PART_RECORD_ID,
                                                    MAMTRL.PROD_INSP_MEMO as PROD_INSP_MEMO,
                                                    0 as QUANTITY,
                                                    SAQTMT.QUOTE_ID as QUOTE_ID,
                                                    SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID as QUOTE_RECORD_ID,
                                                    SAQTMT.QTEREV_ID as QTEREV_ID,
                                                    SAQTMT.QTEREV_RECORD_ID as QTEREV_RECORD_ID,
                                                    SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
                                                    SAQTSV.SERVICE_ID as SERVICE_ID,
                                                    SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
                                                    SAQTSV.PAR_SERVICE_DESCRIPTION as PAR_SERVICE_DESCRIPTION,
                                                    SAQTSV.PAR_SERVICE_ID as PAR_SERVICE_ID,
                                                    SAQTSV.PAR_SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID,
                                                    '{green_book}' as GREENBOOK,
                                                    SAQSCO.GREENBOOK_RECORD_ID as GREENBOOK_RECORD_ID,
                                                    SAQSCO.FABLOCATION_ID as FABLOCATION_ID,
                                                    SAQSCO.FABLOCATION_NAME as FABLOCATION_NAME,
                                                    SAQSCO.FABLOCATION_RECORD_ID as FABLOCATION_RECORD_ID
                                                FROM SYSPBT (NOLOCK)
                                                JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SYSPBT.SAP_PART_NUMBER
                                                JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID
                                            JOIN SAQTSV (NOLOCK) ON SAQTSV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQTSV.PAR_SERVICE_ID = '{service_id}'
                                            JOIN SAQSCO (NOLOCK) ON SAQSCO.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQSCO.GREENBOOK = '{green_book}' 
                                                JOIN MAMSOP (NOLOCK) ON MAMSOP.MATERIAL_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID AND MAMSOP.SALESORG_RECORD_ID = SAQTSV.SALESORG_RECORD_ID
                                                WHERE SYSPBT.BATCH_STATUS = 'IN PROGRESS' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND MAMTRL.PRODUCT_TYPE IS NULL {ParentBasedCondition}) IQ
                                                """.format(
                                                green_book =self.tree_param ,
                                                fab_location_id = '',
                                                service_id = self.tree_parent_level_0 if self.tree_parent_level_0 in ("Z0091","Z0092","Z0004","Z0006","Z0007","Z0035","Z0009","Z0090") else self.tree_param,
                                                BatchGroupRecordId=batch_group_record_id,
                                                QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,
                                                UserId=self.user_id,
                                                ParentBasedCondition=parent_based_condition,
                                                new_part= self.new_part if self.new_part else 0,
                                                included = self.inclusion
                                            )
                                        )
                                        # INC08593801 - End - M
                                        # INC08733295 - End - M                            
                # elif 'Z0100' in parent_based_condition :
                # 	Trace.Write("z0100---2211")
                # 	self._process_query("""INSERT SAQRSP (QUOTE_REV_PO_PRODUCT_LIST_ID,PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID,PROD_INSP_MEMO,QUANTITY, QUOTE_ID, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,NEW_PART,INCLUDED,UNIT_PRICE,EXTENDED_PRICE,UNIT_PRICE_INGL_CURR,EXTENDED_PRICE_INGL_CURR)
                # 			SELECT DISTINCT
                # 				CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_PRODUCT_LIST_ID,
                # 				PART_DESCRIPTION,
                # 				PART_NUMBER,
                # 				PART_RECORD_ID,
                # 				PROD_INSP_MEMO,
                # 				QUANTITY,
                # 				QUOTE_ID,
                # 				QUOTE_RECORD_ID,
                # 				QTEREV_ID,
                # 				QTEREV_RECORD_ID,
                # 				SERVICE_DESCRIPTION,
                # 				SERVICE_ID,
                # 				SERVICE_RECORD_ID,
                # 				PAR_SERVICE_DESCRIPTION,
                # 				PAR_SERVICE_ID,
                # 				PAR_SERVICE_RECORD_ID,
                # 				GREENBOOK,
                # 				GREENBOOK_RECORD_ID,
                # 				FABLOCATION_ID,
                # 				FABLOCATION_NAME,
                # 				FABLOCATION_RECORD_ID,
                # 				{UserId} as CPQTABLEENTRYADDEDBY, 
                # 				GETDATE() as CPQTABLEENTRYDATEADDED,
                # 				{new_part} as NEW_PART,
                # 				1 as INCLUDED,
                # 				CASE WHEN SERVICE_ID = 'Z0101' THEN '0' ELSE null END AS UNIT_PRICE,
                # 				CASE WHEN SERVICE_ID = 'Z0101' THEN '0' ELSE null END AS EXTENDED_PRICE,
                # 				CASE WHEN SERVICE_ID = 'Z0101' THEN '0' ELSE null END AS UNIT_PRICE_INGL_CURR,
                # 				CASE WHEN SERVICE_ID = 'Z0101' THEN '0' ELSE null END AS EXTENDED_PRICE_INGL_CURR
                # 			FROM (
                # 			SELECT 
                # 				DISTINCT
                # 				MAMTRL.SAP_DESCRIPTION as PART_DESCRIPTION,
                # 				MAMTRL.SAP_PART_NUMBER as PART_NUMBER,
                # 				MAMTRL.MATERIAL_RECORD_ID as PART_RECORD_ID,
                # 				MAMTRL.PROD_INSP_MEMO as PROD_INSP_MEMO,
                # 				0 as QUANTITY,
                # 				SAQTMT.QUOTE_ID as QUOTE_ID,
                # 				SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID as QUOTE_RECORD_ID,
                # 				SAQTMT.QTEREV_ID as QTEREV_ID,
                # 				SAQTMT.QTEREV_RECORD_ID as QTEREV_RECORD_ID,
                # 				SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
                # 				SAQTSV.SERVICE_ID as SERVICE_ID,
                # 				SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
                # 				SAQTSV.PAR_SERVICE_DESCRIPTION as PAR_SERVICE_DESCRIPTION,
                # 				SAQTSV.PAR_SERVICE_ID as PAR_SERVICE_ID,
                # 				SAQTSV.PAR_SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID,
                # 				null as GREENBOOK,
                # 				null as GREENBOOK_RECORD_ID,
                # 				null as FABLOCATION_ID,
                # 				null as FABLOCATION_NAME,
                # 				null as FABLOCATION_RECORD_ID
                # 			FROM SYSPBT (NOLOCK)
                # 			JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SYSPBT.SAP_PART_NUMBER
                # 			JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID
                # 			JOIN SAQTSV (NOLOCK) ON SAQTSV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQTSV.PAR_SERVICE_ID = '{service_id}'
                # 			JOIN SAQSCO (NOLOCK) ON SAQSCO.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQSCO.PAR_SERVICE_ID = SAQTSV.PAR_SERVICE_ID AND SAQSCO.SERVICE_ID = SAQTSV.SERVICE_ID 
                # 			JOIN MAMSOP (NOLOCK) ON MAMSOP.MATERIAL_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID AND MAMSOP.SALESORG_RECORD_ID = SAQTSV.SALESORG_RECORD_ID
                # 			WHERE SYSPBT.BATCH_STATUS = 'IN PROGRESS' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND MAMTRL.PRODUCT_TYPE IS NULL AND MAMTRL.IS_SPARE_PART = 1 {ParentBasedCondition}) IQ
                # 			""".format(fab_location_id = '',
                # 				service_id = self.tree_param,
                # 				BatchGroupRecordId=batch_group_record_id,
                # 				QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,
                # 				UserId=self.user_id,
                # 				ParentBasedCondition=parent_based_condition,
                # 				new_part= self.new_part if self.new_part else 0
                # 			)
                # 	)
                
                
                get_child_service_id = Sql.GetFirst("""SELECT SAQTSV.SERVICE_ID FROM SAQTSV (NOLOCK) JOIN SAQRSP (NOLOCK) ON SAQRSP.SERVICE_ID = SAQTSV.SERVICE_ID AND SAQRSP.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID AND SAQRSP.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID WHERE SAQTSV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSV.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.PAR_SERVICE_ID = '{service_id}'""".format(QuoteRecordId = self.contract_quote_record_id,RevisionRecordId = self.quote_revision_record_id,service_id = self.tree_parent_level_0 if self.tree_parent_level_0 in ("Z0091","Z0092","Z0004","Z0006","Z0007","Z0035","Z0009") else self.tree_param))
                #INC08733295 - Start - A
                Sql.RunQuery(
                    """UPDATE SAQRSP SET SAQRSP.SALESUOM_CONVERSION_FACTOR =   CASE WHEN M.BASE_QUANTITY=0.00 THEN 1.00 ELSE M.BASE_QUANTITY END FROM SAQRSP S INNER JOIN MAMUOC M ON S.PART_NUMBER= M.SAP_PART_NUMBER WHERE S.BASEUOM_ID=M.BASEUOM_ID AND  S.SALESUOM_ID=M.CONVERSIONUOM_ID AND S.QUOTE_RECORD_ID = '{QuoteRecordId}' AND S.QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(QuoteRecordId = self.contract_quote_record_id ,RevisionRecordId =self.quote_revision_record_id)
                )
                #INC08733295 - END - A
                # if get_child_service_id:
                # 	if get_child_service_id.SERVICE_ID == 'Z0101':
                # 		spareparts_config_status_count = Sql.GetFirst(""" SELECT COUNT(CONFIGURATION_STATUS) AS COUNT FROM SAQTSE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND CONFIGURATION_STATUS='COMPLETE' """.format(self.contract_quote_record_id,self.quote_revision_record_id,get_child_service_id.SERVICE_ID))
                # 		if spareparts_config_status_count.COUNT > 0:
                # 			data = ScriptExecutor.ExecuteGlobal("CQINSQTITM",{"ContractQuoteRecordId":self.contract_quote_record_id, "ContractQuoteRevisionRecordId":self.quote_revision_record_id, "ServiceId":get_child_service_id.SERVICE_ID, "ActionType":'INSERT_LINE_ITEMS'})
            self._process_query(
                        """DELETE FROM SYSPBT WHERE SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' and SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' and SYSPBT.BATCH_STATUS = 'IN PROGRESS'""".format(
                            BatchGroupRecordId=batch_group_record_id,RevisionRecordId=self.quote_revision_record_id
                        )
                    )

class ToolRelocationModel(ContractQuoteCrudOpertion):
    def __init__(self, **kwargs):
        ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'),
                                            tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
        self.opertion = kwargs.get('opertion')
        self.action_type = kwargs.get('action_type')
        self.values = kwargs.get('values')
        self.table_name = kwargs.get('table_name')
        self.all_values = kwargs.get('all_values')		
        self.node_id = ""	

    def _create(self):
        #userName = str(self.user_name)
        if self.action_type == "ADD_TOOL_RELOCATION_EQUIPMENTS":
            self._add_quote_source_tool_relocation()

    def _add_quote_source_tool_relocation(self):
        master_object_name = "MAEQUP"
        if self.values:
            record_ids = []
            if self.all_values:               
                # query_string = "select MAEQUP.EQUIPMENT_RECORD_ID from MAEQUP (NOLOCK) inner join SAQSCF (NOLOCK) on MAEQUP.FABLOCATION_RECORD_ID = SAQSCF.SRCFBL_RECORD_ID and MAEQUP.ACCOUNT_RECORD_ID = SAQSCF.SRCACC_RECORD_ID and MAEQUP.FABLOCATION_ID = SAQSCF.SRCFBL_ID inner join  MAFBLC (nolock) on MAFBLC.FAB_LOCATION_ID = SAQSCF.SRCFBL_ID AND MAFBLC.ACCOUNT_ID = SAQSCF.SRCACC_ID AND isnull(MAEQUP.PAR_EQUIPMENT_ID,'') = '' AND SAQSCF.QUOTE_RECORD_ID = '{}' where MAEQUP.GREENBOOK_RECORD_ID != '' AND MAEQUP.GREENBOOK_RECORD_ID is not null AND NOT EXISTS (SELECT EQUIPMENT_ID FROM SAQSTE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}') ".format(
                # self.contract_quote_record_id,
                # self.contract_quote_record_id
                # )
                query_string = "select MAEQUP.EQUIPMENT_RECORD_ID from MAEQUP (NOLOCK) inner join SAQSCF (NOLOCK) on MAEQUP.FABLOCATION_RECORD_ID = SAQSCF.SRCFBL_RECORD_ID and MAEQUP.ACCOUNT_RECORD_ID = SAQSCF.SRCACC_RECORD_ID and MAEQUP.FABLOCATION_ID = SAQSCF.SRCFBL_ID inner join  MAFBLC (nolock) on MAFBLC.FAB_LOCATION_ID = SAQSCF.SRCFBL_ID AND MAFBLC.ACCOUNT_ID = SAQSCF.SRCACC_ID AND isnull(MAEQUP.PAR_EQUIPMENT_ID,'') = '' AND SAQSCF.QUOTE_RECORD_ID = '{}' AND SAQSCF.QTEREV_RECORD_ID = '{}' where MAEQUP.GREENBOOK_RECORD_ID != '' AND MAEQUP.GREENBOOK_RECORD_ID is not null AND MAEQUP.EQUIPMENT_ID not in (SELECT EQUIPMENT_ID FROM SAQSTE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SAQSCF.QTEREV_RECORD_ID = '{}') ".format(
                self.contract_quote_record_id,
                self.quote_revision_record_id,
                self.contract_quote_record_id,
                self.quote_revision_record_id
                )
                query_string_for_count = "SELECT COUNT(*) as count FROM ({Query_String})OQ".format(
                    Query_String=query_string
                )
                table_count_data = Sql.GetFirst(query_string_for_count)
                if table_count_data is not None:
                    table_total_rows = table_count_data.count
                if table_total_rows:
                    record_ids = [data for data in self.get_res(query_string, table_total_rows)]                    
            else:                    
                record_ids = [
                    CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
                    if value.strip() != "" and master_object_name in value
                    else value
                    for value in self.values
                ]
            batch_group_record_id = str(Guid.NewGuid()).upper()
            record_ids = str(str(record_ids)[1:-1].replace("'",""))
            parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")			
            primaryQueryItems = SqlHelper.GetFirst(""+str(parameter.QUERY_CRITERIA_1)+" SYSPBT(BATCH_RECORD_ID, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,QTEREV_RECORD_ID) SELECT MAEQUP.EQUIPMENT_RECORD_ID as BATCH_RECORD_ID, ''IN PROGRESS'' as BATCH_STATUS, ''"+str(self.contract_quote_id)+"'' as QUOTE_ID, ''"+str(self.contract_quote_record_id)+"'' as QUOTE_RECORD_ID, ''"+str(batch_group_record_id)+"'' as BATCH_GROUP_RECORD_ID,''"+str(self.quote_revision_record_id)+"'' as QTEREV_RECORD_ID FROM MAEQUP (NOLOCK) JOIN splitstring(''"+record_ids+"'') ON ltrim(rtrim(NAME)) = MAEQUP.EQUIPMENT_RECORD_ID'")
            self._process_query(
                            """
                                INSERT SAQSTE (
                                    QUOTE_SOURCE_TARGET_FAB_LOC_EQUIP_RECORD_ID,
                                    EQUIPMENT_ID,
                                    EQUIPMENT_RECORD_ID,
                                    EQUIPMENT_DESCRIPTION,   
                                    SRCACC_ID,
                                    SRCACC_NAME,
                                    SRCACC_RECORD_ID,
                                    SRCFBL_ID,
                                    SRCFBL_NAME,
                                    SRCFBL_RECORD_ID,
                                    FABLOCATION_ID,
                                    FABLOCATION_NAME,
                                    FABLOCATION_RECORD_ID,
                                    QUOTE_RECORD_ID,
                                    QUOTE_ID,
                                    QUOTE_NAME,
                                    QTEREV_ID,
                                    QTEREV_RECORD_ID,
                                    PLATFORM,
                                    EQUIPMENTCATEGORY_RECORD_ID,
                                    EQUIPMENTCATEGORY_ID,
                                    EQUIPMENTCATEGORY_DESCRIPTION,
                                    EQUIPMENT_STATUS,
                                    GREENBOOK,
                                    GREENBOOK_RECORD_ID,
                                    MNT_PLANT_RECORD_ID,
                                    MNT_PLANT_ID,
                                    MNT_PLANT_NAME,
                                    CPQTABLEENTRYADDEDBY,
                                    CPQTABLEENTRYDATEADDED,
                                    CpqTableEntryModifiedBy,
                                    CpqTableEntryDateModified
                                    ) SELECT
                                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SOURCE_TARGET_FAB_LOC_EQUIP_RECORD_ID,
                                        MAEQUP.EQUIPMENT_ID,
                                        MAEQUP.EQUIPMENT_RECORD_ID,
                                        MAEQUP.EQUIPMENT_DESCRIPTION,
                                        SAQSCF.SRCACC_ID,  
                                        SAQSCF.SRCACC_NAME,
                                        SAQSCF.SRCACC_RECORD_ID,
                                        SAQSCF.SRCFBL_ID,
                                        SAQSCF.SRCFBL_NAME,
                                        SAQSCF.SRCFBL_RECORD_ID,
                                        '' as FABLOCATION_ID,
                                        '' as FABLOCATION_NAME,
                                        '' as FABLOCATION_RECORD_ID,
                                        '{QuoteRecId}' as QUOTE_RECORD_ID,
                                        '{QuoteId}' as QUOTE_ID,
                                        '{QuoteName}' as QUOTE_NAME,
                                        '{RevisionId}' as QTEREV_ID,
                                        '{RevisionRecordId}' as QTEREV_RECORD_ID,
                                        MAEQUP.PLATFORM,
                                        MAEQUP.EQUIPMENTCATEGORY_RECORD_ID,
                                        MAEQUP.EQUIPMENTCATEGORY_ID,
                                        MAEQUP.EQUIPMENTCATEGORY_DESCRIPTION,
                                        MAEQUP.EQUIPMENT_STATUS,
                                        MAEQUP.GREENBOOK,
                                        MAEQUP.GREENBOOK_RECORD_ID,
                                        MAEQUP.MNT_PLANT_RECORD_ID,
                                        MAEQUP.MNT_PLANT_ID,
                                        MAEQUP.MNT_PLANT_NAME,
                                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                                        GETDATE() as CPQTABLEENTRYDATEADDED,
                                        {UserId} as CpqTableEntryModifiedBy,
                                        GETDATE() as CpqTableEntryDateModified
                                        FROM SYSPBT (NOLOCK)
                                        JOIN MAEQUP (NOLOCK) ON SYSPBT.BATCH_RECORD_ID = MAEQUP.EQUIPMENT_RECORD_ID JOIN SAQSCF(NOLOCK) ON SAQSCF.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQSCF.QTEREV_RECORD_ID = SYSPBT.QTEREV_RECORD_ID AND MAEQUP.FABLOCATION_ID = SAQSCF.SRCFBL_ID  WHERE 
                                        SYSPBT.QUOTE_RECORD_ID = '{QuoteRecId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'
                                        AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'                        
                                """.format(
                                QuoteId=self.contract_quote_id,
                                BatchGroupRecordId=batch_group_record_id,
                                UserName=self.user_name,
                                UserId=self.user_id,
                                QuoteRecId=self.contract_quote_record_id,
                                RevisionId=self.quote_revision_id,
                                RevisionRecordId=self.quote_revision_record_id,
                                QuoteName=str(self.contract_quote_name).replace("'","''")
                            )
                        )	

        self._process_query(
                    """DELETE FROM SYSPBT WHERE SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' and SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' and SYSPBT.BATCH_STATUS = 'IN PROGRESS'""".format(
                        BatchGroupRecordId=batch_group_record_id,RevisionRecordId=self.quote_revision_record_id
                    )
                )

    def get_res(self, query_string, table_total_rows):
        for offset_skip_count in range(0, table_total_rows+1, 1000):
            pagination_condition = "WHERE SNO>={Skip_Count} AND SNO<={Fetch_Count}".format(Skip_Count=offset_skip_count+1, Fetch_Count=offset_skip_count+1000)
            query_string_with_pagination = 'SELECT * FROM (SELECT *, ROW_NUMBER()OVER(ORDER BY EQUIPMENT_RECORD_ID) AS SNO FROM ({Query_String}) IQ)OQ {Pagination_Condition}'.format(
                                            Query_String=query_string, Pagination_Condition=pagination_condition)
            table_data = Sql.GetList(query_string_with_pagination)
            if table_data is not None:
                for row_data in table_data:
                    yield row_data.EQUIPMENT_RECORD_ID


class ContractQuoteFabModel(ContractQuoteCrudOpertion):
    def __init__(self, **kwargs):
        ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'), 
                                            tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
        self.opertion = kwargs.get('opertion')
        self.action_type = kwargs.get('action_type')
        self.values = kwargs.get('values')
        self.table_name = kwargs.get('table_name')
        self.all_values = kwargs.get('all_values')		
        self.tool_type = kwargs.get('tool_type')
        self.node_id = ""	

    def _create(self):
        #userName = self.user_name
        error_msg= ''
        mylist = []
        row_values = {}
        if self.action_type == "ADD_FAB":
            master_object_name = "MAFBLC"
            columns = [
                "FAB_LOCATION_ID AS FABLOCATION_ID",
                "FAB_LOCATION_NAME AS FABLOCATION_NAME",
                "FAB_LOCATION_RECORD_ID AS FABLOCATION_RECORD_ID",
                "COUNTRY",
                "COUNTRY_RECORD_ID",
                "MNT_PLANT_ID",
                "MNT_PLANT_NAME",
                "MNT_PLANT_RECORD_ID",
                "STATUS AS FABLOCATION_STATUS"
                
            ]
            table_name = "SAQFBL"
            condition_column = "FAB_LOCATION_RECORD_ID"
            if self.sale_type != "TOOL RELOCATION":
                contract_quote_record_obj = self._get_record_obj(
                columns=[
                    "ACCOUNT_ID",
                    "ACCOUNT_NAME",
                    "ACCOUNT_RECORD_ID"
                ],
                table_name="SAQTMT",
                where_condition="MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id),
                single_record=True,
                )
                account_id = contract_quote_record_obj.ACCOUNT_ID
                account_name = contract_quote_record_obj.ACCOUNT_NAME
                account_rec_id = contract_quote_record_obj.ACCOUNT_RECORD_ID
            else:
                account_id = self.tree_param.split(' - ')
                account_id = account_id[len(account_id)-1]
                account_table  = Sql.GetFirst("SELECT ACCOUNT_NAME,ACCOUNT_RECORD_ID FROM SAACNT(NOLOCK) WHERE ACCOUNT_ID = '"+str(account_id)+"'") 
                if account_table:
                    account_name = account_table.ACCOUNT_NAME
                    account_rec_id = account_table.ACCOUNT_RECORD_ID
            row_values = {
                "QUOTE_NAME": self.contract_quote_name,
                "SALESORG_ID": self.salesorg_id,
                "SALESORG_NAME": self.salesorg_name,
                "SALESORG_RECORD_ID": self.salesorg_record_id,
                # "CPQTABLEENTRYADDEDBY": self.userName,
                "RELOCATION_FAB_TYPE" : "SENDING FAB" if "Sending Account -" in self.tree_param else "RECEIVING FAB" if "Receiving Account -" in self.tree_param else "",
                "ACCOUNT_ID" : account_id,
                "ACCOUNT_NAME" : account_name,
                "ACCOUNT_RECORD_ID" : account_rec_id,
                "QTEREV_RECORD_ID":self.quote_revision_record_id,
                "QTEREV_ID" : self.quote_revision_id,
            }

            fab_table_info = Sql.GetTable(table_name)
            if self.all_values:
                qury_str=""
                if A_Keys!="" and A_Values!="":
                    for key,val in zip(A_Keys,A_Values):
                        if(val!=""):
                            if key=="FAB_LOCATION_RECORD_ID":
                                key="CpqTableEntryId"
                                val = ''.join(re.findall(r'\d+', val)) if not val.isdigit() else val
                            qury_str+=" "+key+" LIKE '%"+val+"%' AND "
                master_fab_obj = self._get_record_obj(
                    columns=["FAB_LOCATION_RECORD_ID"],
                    table_name=master_object_name,
                    table_joins="JOIN SAQTMT (NOLOCK) ON MAFBLC.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID",
                    where_condition=""" SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND {} NOT EXISTS (SELECT FABLOCATION_ID FROM SAQFBL (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}')""".format(
                        self.contract_quote_record_id, qury_str, self.contract_quote_record_id,self.quote_revision_record_id, single_record=False,
                    ),
                )
                if master_fab_obj:
                    self.values = [fab_obj.FAB_LOCATION_RECORD_ID for fab_obj in master_fab_obj]
            
            for row_detail in self._add_record(
                master_object_name=master_object_name,
                columns=columns,
                table_name=table_name,
                condition_column=condition_column,
                values=self.values,
            ):
                row_detail.update(row_values)				
                mylist.append(row_detail)				
                fab_table_info.AddRow(row_detail)

            Sql.Upsert(fab_table_info)
            if ("Sending Account -" in self.tree_param or "Receiving Account -" in self.tree_param) and self.tree_parent_level_0 == 'Fab Locations':
                auto_equp_insert = "true"
                #Trace.Write("auto equp add"+str(self.tree_parent_level_0)+'--'+str(mylist))
                self._add_equipment(auto_equp_insert,mylist)
            
        elif self.action_type == "ADD_ON_PRODUCTS":			
            where_condition=""
            master_object_name = "MAADPR"
            GETPARENTSERVICE= Sql.GetFirst("SELECT QUOTE_SERVICE_RECORD_ID,CONTRACT_VALID_FROM, CONTRACT_VALID_TO FROM SAQTSV(NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' ".format(self.contract_quote_record_id,self.quote_revision_record_id,self.tree_parent_level_1)) #A055S000P01-20834, CR704 - M
            columns = [
                "COMP_PRDOFR_NAME AS ADNPRD_DESCRIPTION",
                "COMP_PRDOFR_ID AS ADNPRD_ID",
                "COMP_PRDOFR_RECORD_ID AS ADNPRDOFR_RECORD_ID",
                "PO_COMP_RECORD_ID AS ADNPRD_RECORD_ID",
                "COMP_PRDOFR_TYPE AS ADN_TYPE",
                #"GETPARENTSERVICE.QUOTE_SERVICE_RECORD_ID AS QTESRV_RECORD_ID",
                "'TRUE' AS ACTIVE",
                "PRDOFR_NAME AS SERVICE_DESCRIPTION",
                "PRDOFR_ID AS SERVICE_ID",
                "PRDOFR_RECORD_ID AS SERVICE_RECORD_ID",
                # "MNT_PLANT_RECORD_ID",
                # "STATUS AS FABLOCATION_STATUS" 
            ]
            columns1 = [
                "COMP_PRDOFR_NAME AS SERVICE_DESCRIPTION",
                "COMP_PRDOFR_ID AS SERVICE_ID",
                "COMP_PRDOFR_RECORD_ID AS SERVICE_RECORD_ID",
                #"GETPARENTSERVICE.QUOTE_SERVICE_RECORD_ID AS QTESRV_RECORD_ID",
                "PRDOFR_NAME AS PAR_SERVICE_DESCRIPTION",
                "PRDOFR_ID AS PAR_SERVICE_ID",
                "PRDOFR_RECORD_ID AS PAR_SERVICE_RECORD_ID",
            ]
            table_name = "SAQSAO"
            condition_column = "PO_COMP_RECORD_ID"
            row_values = {
                "QUOTE_NAME": self.contract_quote_name,
                "SALESORG_ID": self.salesorg_id,
                "SALESORG_NAME": self.salesorg_name,
                "SALESORG_RECORD_ID": self.salesorg_record_id,
                "QTEREV_ID" : self.quote_revision_id,
                # "CPQTABLEENTRYADDEDBY": self.userName,
            }
            get_greenbook = Sql.GetFirst("SELECT BUSINESS_UNITS_RECORD_ID FROM SABUUN WHERE BUSINESSUNIT_ID = '"+str(self.tree_parent_level_0)+"' ")
            greenbook_values = {
                "GREENBOOK": self.tree_parent_level_0,
                "GREENBOOK_RECORD_ID": get_greenbook.BUSINESS_UNITS_RECORD_ID,
                "CONTRACT_VALID_FROM": GETPARENTSERVICE.CONTRACT_VALID_FROM, #A055S000P01-20834, CR704 - M
                "CONTRACT_VALID_TO": GETPARENTSERVICE.CONTRACT_VALID_TO #A055S000P01-20834, CR704 - M
            }

            fab_table_info = Sql.GetTable(table_name)
            greenbook_table_info = Sql.GetTable("SAQSGB")
            if self.all_values:
                qury_str=""
                if A_Keys!="" and A_Values!="":
                    for key,val in zip(A_Keys,A_Values):
                        if(val!=""):
                            if key=="PO_COMP_RECORD_ID":
                                key="CpqTableEntryId"
                                val = ''.join(re.findall(r'\d+', val)) if not val.isdigit() else val
                            qury_str+=" "+key+" LIKE '%"+val+"%' AND "
                document_Type = Sql.GetFirst("SELECT DOCTYP_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id))
                doc_type = str(document_Type.DOCTYP_ID)
                master_fab_obj = self._get_record_obj(
                    columns=["PO_COMP_RECORD_ID"],
                    table_name=master_object_name,
                    table_joins="JOIN SAQTSV (NOLOCK) ON MAADPR.PRDOFR_ID = SAQTSV.SERVICE_ID",
                    where_condition=""" {} SAQTSV.QUOTE_RECORD_ID = '{}'  AND SAQTSV.SERVICE_ID = '{}' AND COMP_PRDOFR_DOCTYP = '{}' AND QTEREV_RECORD_ID = '{}'AND NOT EXISTS (SELECT ADNPRD_ID FROM SAQSAO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}')""".format(qury_str,
                        self.contract_quote_record_id,self.tree_parent_level_1,doc_type,self.quote_revision_record_id, self.contract_quote_record_id,self.quote_revision_record_id,self.tree_parent_level_1, single_record=False,
                    ),
                )

                if master_fab_obj:
                    self.values = [fab_obj.PO_COMP_RECORD_ID for fab_obj in master_fab_obj]
            for row_detail in self._add_record(
                master_object_name=master_object_name,
                columns=columns,
                table_name=table_name,
                condition_column=condition_column,
                values=self.values,
            ):

                row_detail.update(row_values)				
                mylist.append(row_detail)
                fab_table_info.AddRow(row_detail)
            Sql.Upsert(fab_table_info)
            #to insert in SAQSGB
            for row_detail in self._add_record(
                master_object_name=master_object_name,
                columns=columns1,
                table_name="SAQSGB",
                condition_column=condition_column,
                values=self.values,
            ):
                row_detail.update(row_values)	
                row_detail.update(greenbook_values)				
                greenbook_table_info.AddRow(row_detail)
            Sql.Upsert(greenbook_table_info)

            QueryStatement ="""UPDATE SAQSAO SET QTESRV_RECORD_ID ='{id}' WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}'  """.format(self.contract_quote_record_id,self.quote_revision_record_id,self.tree_parent_level_1,id = str(GETPARENTSERVICE.QUOTE_SERVICE_RECORD_ID) )
            Sql.RunQuery(QueryStatement)
            #for id in self.values:
            
            #	QueryStatement ="""UPDATE SAQSAO SET ACTIVE ='TRUE' WHERE QUOTE_RECORD_ID = '{quote_record_id}' AND SERVICE_ID ='{treeparam}' AND ADNPRD_ID = '{id}' """.format(quote_record_id=self.contract_quote_record_id,treeparam = self.tree_param,id = str(id) )
            #	Sql.RunQuery(QueryStatement)
            #QuoteEndDate = self.contract_start_date
            
            #QuoteStartDate = self.contract_end_date
            # INC08847658 - Starts - M
            #A055S000P01-20834, CR704 - Starts - M
            Sql.RunQuery(""" INSERT SAQTSV(QUOTE_SERVICE_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION,SERVICE_RECORD_ID,UOM_ID,UOM_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,QTEPARSRV_RECORD_ID,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_RECORD_ID,SAQSGB.QUOTE_ID,SAQSGB.QUOTE_NAME,SAQSGB.QUOTE_RECORD_ID,SAQSGB.QTEREV_ID,SAQSGB.QTEREV_RECORD_ID,SAQSGB.SERVICE_ID,SAQSGB.SERVICE_DESCRIPTION,SAQSGB.SERVICE_RECORD_ID,MAMTRL.UNIT_OF_MEASURE,MAMTRL.UOM_RECORD_ID,SAQSGB.SALESORG_ID,SAQSGB.SALESORG_NAME,SAQSGB.SALESORG_RECORD_ID,SAQSGB.PAR_SERVICE_DESCRIPTION,SAQSGB.PAR_SERVICE_ID,SAQSGB.PAR_SERVICE_RECORD_ID,SAQSGB.QTESRV_RECORD_ID,SAQSGB.CONTRACT_VALID_FROM,SAQSGB.CONTRACT_VALID_TO,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM SAQSGB INNER JOIN MAMTRL ON SAQSGB.SERVICE_ID = MAMTRL.SAP_PART_NUMBER Where QUOTE_RECORD_ID ='{quote_record_id}' and QTEREV_RECORD_ID = '{RevisionRecordId}' AND GREENBOOK ='{treeparentparam}'AND NOT EXISTS (SELECT SERVICE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='{quote_record_id}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID=SAQSGB.SERVICE_ID) """.format(quote_record_id=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,UserId=self.user_id,UserName=self.user_name,startdate = self.contract_start_date,enddate = self.contract_end_date, treeparentparam = self.tree_parent_level_0 ))
            #A055S000P01-20834, CR704 - Ends - M
            # INC08847658 - Ends - M

            #CR666-INC08864593 - START - M
            Sql.RunQuery(""" INSERT SAQTSV(QUOTE_SERVICE_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION,SERVICE_RECORD_ID,UOM_ID,UOM_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,QTEPARSRV_RECORD_ID,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_RECORD_ID,SAQSGB.QUOTE_ID,SAQSGB.QUOTE_NAME,SAQSGB.QUOTE_RECORD_ID,SAQSGB.QTEREV_ID,SAQSGB.QTEREV_RECORD_ID,SAQSGB.SERVICE_ID,SAQSGB.SERVICE_DESCRIPTION,SAQSGB.SERVICE_RECORD_ID,MAMTRL.UNIT_OF_MEASURE,MAMTRL.UOM_RECORD_ID,SAQSGB.SALESORG_ID,SAQSGB.SALESORG_NAME,SAQSGB.SALESORG_RECORD_ID,SAQSGB.PAR_SERVICE_DESCRIPTION,SAQSGB.PAR_SERVICE_ID,SAQSGB.PAR_SERVICE_RECORD_ID,SAQSGB.QTESRV_RECORD_ID,'{startdate}' as CONTRACT_VALID_FROM,'{enddate}' as CONTRACT_VALID_TO,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM SAQSGB INNER JOIN MAMTRL ON SAQSGB.SERVICE_ID = MAMTRL.SAP_PART_NUMBER Where QUOTE_RECORD_ID ='{quote_record_id}' and QTEREV_RECORD_ID = '{RevisionRecordId}' AND GREENBOOK ='{treeparentparam}' AND SAQSGB.SERVICE_ID='Z0123' AND NOT EXISTS (SELECT SERVICE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='{quote_record_id}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID=SAQSGB.SERVICE_ID AND SAQTSV.PAR_SERVICE_ID=SAQSGB.PAR_SERVICE_ID) """.format(quote_record_id=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,UserId=self.user_id,UserName=self.user_name,startdate = self.contract_start_date,enddate = self.contract_end_date, treeparentparam = self.tree_parent_level_0 ))
            #CR666-INC08864593 - END - M

            

            #insert in Greenbook table
            # Sql.RunQuery(""" INSERT SAQSGB(
            # QUOTE_SERVICE_GREENBOOK_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION,SERVICE_RECORD_ID,UOM_ID,UOM_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,GREENBOOK,GREENBOOK_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
            # SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_RECORD_ID,SAQSAO.QUOTE_ID,SAQSAO.QUOTE_NAME,SAQSAO.QUOTE_RECORD_ID,SAQSAO.QTEREV_ID,SAQSAO.QTEREV_RECORD_ID,SAQSAO.ADNPRD_ID,SAQSAO.ADNPRD_DESCRIPTION,SAQSAO.ADNPRDOFR_RECORD_ID,MAMTRL.UNIT_OF_MEASURE,MAMTRL.UOM_RECORD_ID,SAQSAO.SALESORG_ID,SAQSAO.SALESORG_NAME,SAQSAO.SALESORG_RECORD_ID,SAQSAO.SERVICE_DESCRIPTION,SAQSAO.SERVICE_ID,SAQSAO.SERVICE_RECORD_ID,'6/14/2022 12:00:00 AM' as CONTRACT_VALID_FROM,'12/24/2020 12:00:00 AM' as CONTRACT_VALID_TO,SABUUN.BUSINESSUNIT_ID as GREENBOOK,SABUUN.BUSINESS_UNITS_RECORD_ID as GREENBOOK_RECORD_ID,'X0116961' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, 133 as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM SAQSAO
            # INNER JOIN MAMTRL ON SAQSAO.ADNPRD_ID = MAMTRL.SAP_PART_NUMBER INNER JOIN SABUUN ON SABUUN.BUSINESSUNIT_ID = '{greenbook}' Where QUOTE_RECORD_ID ='{quote_record_id}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparam}' AND SAQSAO.ACTIVE ='TRUE' AND NOT EXISTS (SELECT SERVICE_ID FROM SAQSGB WHERE QUOTE_RECORD_ID ='{quote_record_id}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSGB.SERVICE_ID=SAQSAO.ADNPRD_ID) """.format(quote_record_id=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,treeparam = self.tree_parent_level_1,greenbook=self.tree_parent_level_0,UserId=self.user_id,UserName=self.user_name,startdate = self.contract_start_date,enddate = self.contract_end_date ))
            #insert in entitlement table based on add on products
            service_addon_object =Sql.GetList("Select SAQSAO.*,SAQTSV.QUOTE_SERVICE_RECORD_ID from SAQSAO (nolock) inner join SAQTSV on SAQTSV.QUOTE_RECORD_ID=SAQSAO.QUOTE_RECORD_ID and SAQTSV.QTEREV_RECORD_ID=SAQSAO.QTEREV_RECORD_ID and SAQTSV.SERVICE_ID = SAQSAO.ADNPRD_ID where SAQSAO.QUOTE_RECORD_ID= '{QuoteRecordId}' AND SAQSAO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSAO.ACTIVE ='TRUE' AND SAQSAO.SERVICE_ID = '{service_id}' AND SAQSAO.SERVICE_ID NOT IN (SELECT SERVICE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{service_id}' AND SAQTSV.SERVICE_ID=SAQSAO.ADNPRD_ID)".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, service_id =self.tree_parent_level_1 ))
            #tableInfo = SqlHelper.GetTable("SAQTSE")
            x = datetime.datetime.today()
            x= str(x)
            y = x.split(" ")
            for OfferingRow_detail in service_addon_object:
                # addon_entitlement_object = Sql.GetFirst("select SAQTSE.PAR_SERVICE_ID from SAQTSE(nolock) inner join SAQSAO on SAQTSE.SERVICE_ID = SAQSAO.ADNPRD_ID AND SAQTSE.PAR_SERVICE_ID = SAQSAO.SERVICE_ID AND SAQTSE.QUOTE_RECORD_ID = SAQSAO.QUOTE_RECORD_ID and SAQTSE.QTEREV_RECORD_ID = SAQSAO.QTEREV_RECORD_ID WHERE SAQTSE.PAR_SERVICE_ID = '{}' AND SAQSAO.QUOTE_RECORD_ID = '{}' and SAQSAO.QTEREV_RECORD_ID = '{}'".format(self.tree_parent_level_1,self.contract_quote_record_id,self.quote_revision_record_id))
                # if addon_entitlement_object is None:
                # 	CQADDONPRD.addon_service_level_entitlement(OfferingRow_detail,self.tree_parent_level_0)
                #try:
                #Trace.Write("OfferingRow_detail--"+str(OfferingRow_detail))
                CQADDONPRD.addon_operations(OfferingRow_detail,self.tree_parent_level_0)
                # except:
                # 	pass
                
        # INC08795842 - Starts - M
        elif self.action_type == "ADD_CREDIT":			
            where_condition=""
            credit_applicable = ""
            master_object_name = "SACRVC"
            try:
                APPLIED_CREDITS = Param.APPLIED_CREDITS
            except:
                APPLIED_CREDITS = ''
            try:
                CREDIT_APPLIED = Param.CREDIT_APPLIED
            except:
                CREDIT_APPLIED = ''
            try:
                CREDIT_AMOUNTS = Param.CREDIT_AMOUNTS
            except:
                CREDIT_AMOUNTS = ''
            try:
                CREDIT_NOTE = Param.CREDIT_NOTE
            except:
                CREDIT_NOTE = ''
            for key,val in enumerate(list(self.values)):
                val = re.sub("[^0-9]","",val)
                id = val.lstrip("0")
                key = int(key)
                credit_details = Sql.GetFirst("SELECT * FROM SACRVC WHERE CpqTableEntryId = '"+str(id)+"' ")
                if credit_details.CRTAPP_INGL_CURR:
                    credit_applied = credit_details.CRTAPP_INGL_CURR
                else:
                    credit_applied = 0
                if APPLIED_CREDITS:
                    total_credits_used = float(str(APPLIED_CREDITS[key]).replace(",","")) + float(str(credit_applied).replace(",",""))
                    Trace.Write("Credits_va2"+str(total_credits_used))
                else:
                    Trace.Write("editwithoutAPPLIED_CREDITS")
                    total_credits_used = float(str(credit_applied).replace(",",""))
                #total_credits_used = str(total_credits_used)
                total_amount_available = str(credit_details.ZGBAL_AMT)
                Trace.Write("total_credits_used--- "+str(total_credits_used))
                if float(total_credits_used) > float(total_amount_available):
                    Trace.Write("Credit Limit Exceeded !!!")
                    credit_applicable = "No"
                    error_msg = 'ERROR : CREDIT VOCHER LIMIT EXCEEDED !!!'
                else:
                    if APPLIED_CREDITS!='':
                        Trace.Write("crdit amt-"+str(APPLIED_CREDITS[key]))
                        # if '-' not in APPLIED_CREDITS[key] :
                        # 	APPLIED_CREDITS[key] = '-'+str(APPLIED_CREDITS[key])

                        # try:
                        if int(credit_details.UNBL_INGL_CURR)== 0 or int(credit_details.UNBL_INGL_CURR)=='':
                            Trace.Write("credit1")
                            unapplied = float(str(credit_details.WRBTR).replace(",",""))-float(str(APPLIED_CREDITS[key]).replace(",","")) if APPLIED_CREDITS[key]!='' else float(str(credit_details.WRBTR).replace(",",""))
                        else:
                            Trace.Write("credit2")
                            unapplied = float(str(credit_details.UNBL_INGL_CURR).replace(",",""))-float(str(APPLIED_CREDITS[key]).replace(",","")) if APPLIED_CREDITS[key]!='' else float(str(credit_details.UNBL_INGL_CURR).replace(",",""))
                        if str(credit_details.CRTAPP_INGL_CURR) == "":
                            Trace.Write("credit3")
                            credit_details.CRTAPP_INGL_CURR = 0
                        Trace.Write("credit4")
                        # Sql.RunQuery("UPDATE SACRVC SET CRTAPP_INGL_CURR = '{}', UNBL_INGL_CURR = '{}' WHERE CpqTableEntryId = '{}'".format(float(credit_details.CRTAPP_INGL_CURR.replace(",",""))+ float(APPLIED_CREDITS[key].replace(",","")), unapplied, id))
                        Sql.RunQuery("UPDATE SACRVC SET CRTAPP_INGL_CURR = '{}', UNBL_INGL_CURR = '{}' WHERE CpqTableEntryId = '{}'".format(float(str(credit_details.CRTAPP_INGL_CURR).replace(",",""))+ float(str(APPLIED_CREDITS[key].replace(",",""))), unapplied, id))
                        # except Exception as e:
                        # 	Trace.Write('EXCEPTION: '+str(e))
                        # 	Trace.Write('APPLIED_CREDITS'+str(APPLIED_CREDITS))
                        # 	Trace.Write('CREDIT_AMOUNTS'+str(CREDIT_AMOUNTS))
                    else:
                        Trace.Write('###---No Credits Applied')
                if credit_applicable != "No":
                    GETPARENTSERVICE= Sql.GetFirst("SELECT QUOTE_SERVICE_RECORD_ID FROM SAQTSV(NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' ".format(self.contract_quote_record_id,self.quote_revision_record_id,self.tree_parent_level_1))
                    columns = [
                        "CREDITVOUCHER_RECORD_ID"
                    ]
                    table_name = "SAQRCV"
                    condition_column = "CREDITVOUCHER_RECORD_ID"
                    get_greenbook = Sql.GetFirst("SELECT BUSINESS_UNITS_RECORD_ID FROM SABUUN WHERE BUSINESSUNIT_ID = '"+str(self.tree_parent_level_0)+"' ")
                    # INC08699134 - Starts - M
                    get_addon = Sql.GetFirst("SELECT SERVICE_DESCRIPTION,SERVICE_RECORD_ID,SERVICE_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID FROM SAQSGB WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}'".format(self.contract_quote_record_id,self.quote_revision_record_id,self.tree_parent_level_1))
                    #2124 start
                    get_div_rec = Sql.GetFirst("SELECT DIVISION_RECORD_ID FROM SADIVN where DIVISION_ID='{}'".format(credit_details.SPART))
                    row_values = {
                        "GREENBOOK": self.tree_parent_level_0,
                        "GREENBOOK_RECORD_ID": get_greenbook.BUSINESS_UNITS_RECORD_ID,
                        "SERVICE_DESCRIPTION":get_addon.SERVICE_DESCRIPTION,
                        "SERVICE_ID":ADDON_PRD_ID,
                        "SERVICE_RECORD_ID": get_addon.SERVICE_RECORD_ID,
                        "GL_ACCOUNT_NO": credit_details.HKONT if credit_details.HKONT else '',
                        "SALESORDER_NO": credit_details.ZUONR if credit_details.ZUONR else '',
                        "CRDVCH_NOTE": CREDIT_NOTE,
                        "DIVISION_ID":credit_details.SPART if credit_details.SPART else '',
                        "DIVISION_RECORD_ID": get_div_rec.DIVISION_RECORD_ID if get_div_rec  else '',
                        "PAR_SERVICE_DESCRIPTION":get_addon.SERVICE_DESCRIPTION if get_addon.SERVICE_DESCRIPTION else "",
                        "PAR_SERVICE_ID": get_addon.SERVICE_ID if get_addon.SERVICE_ID else "",
                        "PAR_SERVICE_RECORD_ID": get_addon.SERVICE_RECORD_ID if get_addon.SERVICE_RECORD_ID else "",
                        "QUOTE_RECORD_ID": self.contract_quote_record_id,
                        "QUOTE_ID": self.contract_quote_id,
                        "QTEREV_RECORD_ID" : self.quote_revision_record_id,
                        "QTEREV_ID" : self.quote_revision_id,
                        "CREDITVOUCHER_RECORD_ID" : credit_details.CREDITVOUCHER_RECORD_ID if credit_details.CREDITVOUCHER_RECORD_ID else '',
                        "QUOTE_REV_CREDIT_VOUCHER_RECORD_ID" : str(Guid.NewGuid()).upper()
                    }

                    # INC08699134 - Ends - M
                    # row_detail.update(row_values)

                    credit_table_info = Sql.GetTable(table_name)
                    saqrcv_ids = []
                    if self.all_values:
                        qury_str=""
                        if A_Keys!="" and A_Values!="":
                            for key,val in zip(A_Keys,A_Values):
                                if(val!=""):
                                    if key=="CREDITVOUCHER_RECORD_ID":
                                        key="CpqTableEntryId"
                                        val = ''.join(re.findall(r'\d+', val)) if not val.isdigit() else val
                                    qury_str+=" "+key+" LIKE '%"+val+"%' AND "
                        master_credit_obj = self._get_record_obj(
                            columns=["CREDITVOUCHER_RECORD_ID"],
                            table_name=master_object_name,
                            table_joins="",
                            where_condition=""" {} REPLACE(LTRIM(REPLACE(KUNAG,'0',' ')),' ','0') = '{}' """.format(qury_str,Quote.GetCustomField('STPAccountID').Content,single_record=False)
                        )

                        if master_credit_obj:
                            self.values = [credit_obj.CREDITVOUCHER_RECORD_ID for credit_obj in master_credit_obj]
                    credit_table_info.AddRow(row_values)
                    saqrcv_ids.append(row_values["QUOTE_REV_CREDIT_VOUCHER_RECORD_ID"])
                    Sql.Upsert(credit_table_info)
                    credit_applied = dict(CREDIT_APPLIED)
                    for key,value in credit_applied.items():
                        for credit in saqrcv_ids:
                            Sql.RunQuery(" UPDATE SAQRCV SET CREDIT_APPLIED_INGL_CURR = {},CREDIT_APPLIED_INVC_CURR = {} FROM SAQRCV JOIN SACRVC ON SACRVC.ZUONR = SAQRCV.SALESORDER_NO AND SACRVC.CREDITVOUCHER_RECORD_ID = SAQRCV.CREDITVOUCHER_RECORD_ID WHERE QUOTE_REV_CREDIT_VOUCHER_RECORD_ID = '{}' AND SACRVC.CpqTableEntryId = '{}'".format(float(value),float(value),credit,str(key).split('-')[1]))
        # INC08795842 - Ends - M

        elif self.action_type == "ADD_SOURCE_FAB":			
            master_object_name = "MAFBLC"
            columns = [
                "FAB_LOCATION_ID AS SRCFBL_ID",
                "FAB_LOCATION_NAME AS SRCFBL_NAME",
                "FAB_LOCATION_RECORD_ID AS SRCFBL_RECORD_ID",
                "ACCOUNT_ID AS SRCACC_ID",
                "ACCOUNT_NAME AS SRCACC_NAME",
                "ACCOUNT_RECORD_ID AS SRCACC_RECORD_ID",
                # "COUNTRY",
                # "COUNTRY_RECORD_ID",
                # "MNT_PLANT_ID",
                # "MNT_PLANT_NAME",
                # "MNT_PLANT_RECORD_ID",
                # "STATUS AS FABLOCATION_STATUS" 
            ]
            table_name = "SAQSCF"
            condition_column = "FAB_LOCATION_RECORD_ID"
            row_values = {
                "QUOTE_NAME": self.contract_quote_name,
                # "SALESORG_ID": self.salesorg_id,
                # "SALESORG_NAME": self.salesorg_name,
                # "SALESORG_RECORD_ID": self.salesorg_record_id,
                # "CPQTABLEENTRYADDEDBY": self.userName,
            }

            fab_table_info = Sql.GetTable(table_name)
            if self.all_values:
                master_fab_obj = self._get_record_obj(
                    columns=["FAB_LOCATION_RECORD_ID"],
                    table_name=master_object_name,
                    table_joins="JOIN SAQTMT (NOLOCK) ON MAFBLC.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID",
                    where_condition=""" SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND NOT EXISTS (SELECT SRCFBL_ID FROM SAQSCF (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}')""".format(
                        self.contract_quote_record_id, self.contract_quote_record_id,self.quote_revision_record_id, single_record=False,
                    ),
                )

                if master_fab_obj:
                    self.values = [fab_obj.FAB_LOCATION_RECORD_ID for fab_obj in master_fab_obj]

            for row_detail in self._add_record(
                master_object_name=master_object_name,
                columns=columns,
                table_name=table_name,
                condition_column=condition_column,
                values=self.values,
            ):
                row_detail.update(row_values)				
                mylist.append(row_detail)				
                fab_table_info.AddRow(row_detail)
            Sql.Upsert(fab_table_info)
            
        elif self.action_type == "ADD_EQUIPMENTS":
            self._add_equipment()
        
        elif self.action_type == "ADD_UNMAPPED_EQUIPMENTS":
            # SAQFBL INSERT FOR UNMAPPED EQUIPMENTS STARTS
            #Trace.Write("Unmapped_chk_j "+str(list(self.values)))
            #Trace.Write("self.contract_quote_id "+str(self.contract_quote_id))
            
            master_fab = Sql.GetFirst("SELECT * FROM MAFBLC (NOLOCK) WHERE FAB_LOCATION_ID = 'UNMAPPED' AND FAB_LOCATION_ID NOT IN (SELECT FABLOCATION_ID FROM SAQFBL (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"')  ")
            acunt_info = Sql.GetFirst("SELECT ACCOUNT_ID, ACCOUNT_NAME, ACCOUNT_RECORD_ID FROM SAACNT (NOLOCK) WHERE ACCOUNT_ID = '"+str(self.tree_param).split('-')[1].strip()+"'")
            if master_fab:

                unmapped_fab_table_info = SqlHelper.GetTable("SAQFBL")
                fab_table ={
                    "QUOTE_FABLOCATION_RECORD_ID": str(Guid.NewGuid()).upper(),
                    "FABLOCATION_ID": str(master_fab.FAB_LOCATION_ID),
                    "FABLOCATION_NAME": str(master_fab.FAB_LOCATION_NAME),
                    "FABLOCATION_RECORD_ID": str(master_fab.FAB_LOCATION_RECORD_ID),
                    "QUOTE_ID": str(self.contract_quote_id),
                    "QUOTE_NAME": str(self.contract_quote_name).replace("'","''"),
                    "QUOTE_RECORD_ID": str(self.contract_quote_record_id),
                    "COUNTRY": str(master_fab.COUNTRY),
                    "COUNTRY_RECORD_ID": str(master_fab.COUNTRY_RECORD_ID),
                    "MNT_PLANT_ID": str(master_fab.MNT_PLANT_ID),
                    "MNT_PLANT_NAME": str(master_fab.MNT_PLANT_NAME),
                    "MNT_PLANT_RECORD_ID": str(master_fab.MNT_PLANT_RECORD_ID),
                    "SALESORG_ID": str(master_fab.SALESORG_ID),
                    "SALESORG_NAME": str(master_fab.SALESORG_NAME),
                    "SALESORG_RECORD_ID": str(master_fab.SALESORG_RECORD_ID),
                    "FABLOCATION_STATUS": "",
                    "ADDRESS_1": str(master_fab.ADDRESS_1),
                    "ADDRESS_2": str(master_fab.ADDRESS_2),
                    "CITY": str(master_fab.CITY),
                    "STATE": str(master_fab.STATE),
                    "STATE_RECORD_ID": str(master_fab.STATE_RECORD_ID),
                    "RELOCATION_FAB_TYPE": "SENDING FAB",
                    "ACCOUNT_ID": str(acunt_info.ACCOUNT_ID),
                    "ACCOUNT_NAME": str(acunt_info.ACCOUNT_NAME),
                    "ACCOUNT_RECORD_ID": str(acunt_info.ACCOUNT_RECORD_ID),
                    "QTEREV_RECORD_ID": str(self.quote_revision_record_id)

                }
                unmapped_fab_table_info.AddRow(fab_table)
                Sql.Upsert(unmapped_fab_table_info)


            # SAQFBL INSERT FOR UNMAPPED EQUIPMENTS ENDS

            master_object_name = "MAEQUP"
            if self.values:
                record_ids = [value for value in self.values]
                #Trace.Write("record_ids_chk_j "+str(record_ids))
                for rec in record_ids:
                    obj = rec.split('-')[0]
                    cpq_entry = rec.split('-')[1].lstrip('0')
                    Trace.Write("cpq_entry_Chk_J"+str(cpq_entry))
                    # maequp_data = Sql.GetFirst("SELECT * FROM MAEQUP (NOLOCK) WHERE CpqTableEntryId = '"+str(cpq_entry)+"'")
                    #INC08704188 - Start - M
                    self._process_query(
                        """
                            INSERT SAQFEQ (
                                QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
                                EQUIPMENT_ID,
                                EQUIPMENT_RECORD_ID,
                                EQUIPMENT_DESCRIPTION,                            
                                FABLOCATION_ID,
                                FABLOCATION_NAME,
                                FABLOCATION_RECORD_ID,
                                SERIAL_NUMBER,
                                QUOTE_RECORD_ID,
                                QUOTE_ID,
                                QUOTE_NAME,
                                QTEREV_ID,
                                QTEREV_RECORD_ID,
                                KPU,
                                PLATFORM,
                                EQUIPMENTCATEGORY_RECORD_ID,
                                EQUIPMENTCATEGORY_ID,
                                EQUIPMENTCATEGORY_DESCRIPTION,
                                EQUIPMENT_STATUS,
                                PBG,
                                GREENBOOK,
                                GREENBOOK_RECORD_ID,
                                MNT_PLANT_RECORD_ID,
                                MNT_PLANT_ID,
                                MNT_PLANT_NAME,
                                WARRANTY_START_DATE,
                                WARRANTY_END_DATE,
                                SALESORG_ID,
                                SALESORG_NAME,
                                SALESORG_RECORD_ID,
                                CUSTOMER_TOOL_ID,
                                CPQTABLEENTRYADDEDBY,
                                CPQTABLEENTRYDATEADDED,
                                CpqTableEntryModifiedBy,
                                CpqTableEntryDateModified,
                                RELOCATION_FAB_TYPE,
                                RELOCATION_EQUIPMENT_TYPE,WAFER_SIZE,
                                TECHNOLOGY,
                                DEVICE_NODE,
                                DEVICE_TYPE,
                                PROCESS_TYPE,
                                WAFER_SIZE_GROUP,
                                GENERATION,
                                END_PRODUCT_TECHNOLOGY,
                                SUBSTRATE_SIZE_GROUP
                                ) SELECT
                                    CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
                                    MAEQUP.EQUIPMENT_ID,
                                    MAEQUP.EQUIPMENT_RECORD_ID,
                                    MAEQUP.EQUIPMENT_DESCRIPTION,                                
                                    MAEQUP.FABLOCATION_ID,
                                    MAEQUP.FABLOCATION_NAME,
                                    MAEQUP.FABLOCATION_RECORD_ID,
                                    MAEQUP.SERIAL_NO,
                                    '{QuoteRecId}' as QUOTE_RECORD_ID,
                                    '{QuoteId}' as QUOTE_ID,
                                    '{QuoteName}' as QUOTE_NAME,
                                    '{RevisionId}' as QTEREV_ID,
                                    '{RevisionRecordId}' as QTEREV_RECORD_ID,
                                    MAEQUP.KPU,
                                    MAEQUP.PLATFORM,
                                    MAEQUP.EQUIPMENTCATEGORY_RECORD_ID,
                                    MAEQUP.EQUIPMENTCATEGORY_ID,
                                    MAEQUP.EQUIPMENTCATEGORY_DESCRIPTION,
                                    MAEQUP.EQUIPMENT_STATUS,
                                    MAEQUP.PBG,
                                    MAEQUP.GREENBOOK,
                                    MAEQUP.GREENBOOK_RECORD_ID,
                                    MAEQUP.MNT_PLANT_RECORD_ID,
                                    MAEQUP.MNT_PLANT_ID,
                                    MAEQUP.MNT_PLANT_NAME,
                                    MAEQUP.WARRANTY_START_DATE,
                                    MAEQUP.WARRANTY_END_DATE,
                                    MAEQUP.SALESORG_ID,
                                    MAEQUP.SALESORG_NAME,
                                    MAEQUP.SALESORG_RECORD_ID,
                                    MAEQUP.CUSTOMER_TOOL_ID,
                                    '{UserName}' AS CPQTABLEENTRYADDEDBY,
                                    GETDATE() as CPQTABLEENTRYDATEADDED,
                                    {UserId} as CpqTableEntryModifiedBy,
                                    GETDATE() as CpqTableEntryDateModified,
                                    '{relocation_fab_type}' AS RELOCATION_FAB_TYPE,
                                    '{relocation_equp_type}' AS RELOCATION_EQUIPMENT_TYPE,
                                    MAEQUP.SUBSTRATE_SIZE,
                                    MAEQUP.TECHNOLOGY,
                                    MAEQUP.DEVICE_NODE,
                                    MAEQUP.DEVICE_TYPE,
                                    MAEQUP.PROCESS_TYPE,
                                    MAEQUP.WAFER_SIZE_GROUP,
                                    MAEQUP.GENERATION,
                                    MAEQUP.END_PRODUCT_TECHNOLOGY,
                                    MAEQUP.SUBSTRATE_SIZE_GROUP
                                    FROM MAEQUP (NOLOCK) WHERE CpqTableEntryId = '{cpq_entry}'
                        """.format(
                                treeparam=self.tree_param,
                                treeparentparam=self.tree_parent_level_0,
                                QuoteId=self.contract_quote_id,
                                UserName=self.user_name,
                                UserId=self.user_id,
                                cpq_entry=cpq_entry,
                                QuoteRecId=self.contract_quote_record_id,
                                # INC08617554 Starts - M
                                QuoteName= str(self.contract_quote_name).replace("'","''"),
                                # INC08617554 Ends - M
                                RevisionId=self.quote_revision_id,
                                RevisionRecordId=self.quote_revision_record_id,
                                # warranty_end = " NULL AS WARRANTY_END_DATE" if self.tool_type=="TEMP_TOOL" else " MAEQUP.WARRANTY_END_DATE ",
                                relocation_fab_type = "SENDING FAB" if "Sending Account -" in self.tree_param else "RECEIVING FAB" if "Receiving Account -" in self.tree_param else "",
                                relocation_equp_type = "SENDING EQUIPMENT" if "Sending Account -" in self.tree_param else "RECEIVING EQUIPMENT" if "Receiving Account -" in self.tree_param else "",
                        )
                    )
                    #INC08704188 - End - M
                    #ibase attributes update Query optimisation
                    Sql.RunQuery("UPDATE SAQFEQ SET IBASE_ATTSTS = 'INCOMPLETE' WHERE (ISNULL(PLATFORM, '') = '' OR ISNULL(DEVICE_TYPE, '') = '' OR ISNULL(DEVICE_NODE, '') = '' OR ISNULL(SUBSTRATE_SIZE_GROUP, '')= '') AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'" .format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
                    Sql.RunQuery("UPDATE SAQFEQ SET IBASE_ATTSTS = 'COMPLETE' WHERE ISNULL(PLATFORM, '') != '' AND ISNULL(DEVICE_TYPE, '') != '' AND ISNULL(DEVICE_NODE, '') != '' AND ISNULL(SUBSTRATE_SIZE_GROUP, '') != '' AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'" .format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
                    Sql.RunQuery("UPDATE SAQFEQ SET IBASE_ATTSTS = 'INCOMPLETE' WHERE (ISNULL(TECHNOLOGY, '') = '' OR ISNULL(GENERATION, '') = '' OR ISNULL(END_PRODUCT_TECHNOLOGY, '')= '') AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'AND GREENBOOK = 'DISPLAY'" .format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
                    Sql.RunQuery("UPDATE SAQFEQ SET IBASE_ATTSTS = 'COMPLETE' WHERE ISNULL(TECHNOLOGY, '') != '' AND ISNULL(GENERATION, '') != '' AND ISNULL(END_PRODUCT_TECHNOLOGY, '') != '' AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'AND GREENBOOK = 'DISPLAY'" .format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
                    ##unmapped fab's greenbook insert
                    self._process_query(
                        """INSERT SAQFGB(
                            FABLOCATION_ID,
                            FABLOCATION_NAME,
                            FABLOCATION_RECORD_ID,
                            GREENBOOK,
                            GREENBOOK_RECORD_ID,
                            QUOTE_ID,
                            QUOTE_NAME,
                            QUOTE_RECORD_ID,
                            QTEREV_ID,
                            QTEREV_RECORD_ID,
                            SALESORG_ID,
                            SALESORG_NAME,
                            SALESORG_RECORD_ID,						
                            CpqTableEntryModifiedBy,
                            CpqTableEntryDateModified,
                            QUOTE_FAB_LOC_GB_RECORD_ID,
                            CPQTABLEENTRYADDEDBY,
                            CPQTABLEENTRYDATEADDED
                            ) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOC_GB_RECORD_ID,
                            '{UserName}' AS CPQTABLEENTRYADDEDBY,
                            GETDATE() as CPQTABLEENTRYDATEADDED FROM (
                            SELECT DISTINCT
                            SAQFEQ.FABLOCATION_ID,
                            SAQFEQ.FABLOCATION_NAME,
                            SAQFEQ.FABLOCATION_RECORD_ID,
                            SAQFEQ.GREENBOOK,
                            SAQFEQ.GREENBOOK_RECORD_ID,
                            SAQFEQ.QUOTE_ID,
                            SAQFEQ.QUOTE_NAME,
                            SAQFEQ.QUOTE_RECORD_ID,
                            SAQFEQ.QTEREV_ID,
                            SAQFEQ.QTEREV_RECORD_ID,
                            SAQFEQ.SALESORG_ID,
                            SAQFEQ.SALESORG_NAME,
                            SAQFEQ.SALESORG_RECORD_ID,
                            {UserId} as CpqTableEntryModifiedBy,
                            GETDATE() as CpqTableEntryDateModified
                            FROM SAQFEQ (NOLOCK)
                            JOIN MAEQUP (NOLOCK) ON MAEQUP.SALESORG_ID = SAQFEQ.SALESORG_ID AND MAEQUP.EQUIPMENT_RECORD_ID = SAQFEQ.EQUIPMENT_RECORD_ID AND MAEQUP.FABLOCATION_ID = SAQFEQ.FABLOCATION_ID
                            
                            WHERE SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQFEQ.QTEREV_RECORD_ID = '{RevisionRecordId}' AND MAEQUP.CpqTableEntryId = '{cpq_entry}' AND SAQFEQ.GREENBOOK NOT IN (SELECT GREENBOOK FROM SAQFGB WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND FABLOCATION_ID ='UNMAPPED')
                            ) FB""".format(
                                            treeparam=self.tree_param,
                                            QuoteRecordId=self.contract_quote_record_id,
                                            RevisionRecordId=self.quote_revision_record_id,
                                            UserId=self.user_id,
                                            UserName=self.user_name,
                                            cpq_entry = cpq_entry,
                                        )
                        )	


        elif self.action_type == "ADD_NSO":
            master_object_name = "PRLPBE"
            if self.values:
                record_ids = [value for value in self.values]
                #Trace.Write("record_ids_chk_j "+str(record_ids))
                for rec in record_ids:
                    obj = rec.split('-')[0]
                    cpq_entry = rec.split('-')[1].lstrip('0')
                    Trace.Write("cpq_entry_Chk_J"+str(cpq_entry))
                    nso_master_table = Sql.GetList("SELECT BUSINESS_UNIT,DIVISION_ID,DIVISION_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,SAP_PART_NUMBER,PRODUCT_ID,POSS_NSO_DESCRIPTION,POSS_COST,POSS_PRICE,POSS_NSO_PART_ID FROM PRLPBE (NOLOCK) WHERE CpqTableEntryId = '{cpq_entry}'".format(cpq_entry = cpq_entry))
                    for nso_data in nso_master_table:
                        #CR666-INC08864593 - START - M
                        nso_equipment_list = Sql.GetList("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,EQUIPMENT_STATUS,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QTESRVGBK_RECORD_ID,QTESRV_RECORD_ID,SERIAL_NO,TEMP_TOOL,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = 'Z0123' AND GREENBOOK = '{}' AND PAR_SERVICE_ID = '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id,self.tree_parent_level_0,self.tree_parent_level_1))
                        #CR666-INC08864593 - END - M
                        for eqp in nso_equipment_list:
                            Trace.Write("CHK_POSS_ "+str(nso_data))
                            nso_table_info = SqlHelper.GetTable("SAQSCN")
                            if nso_data.POSS_COST:
                                poss_cost = nso_data.POSS_COST
                            else:
                                poss_cost = 0
                            if nso_data.POSS_PRICE:
                                poss_price = nso_data.POSS_PRICE
                            else:
                                poss_price = 0
                            # Trace.Write("poss_price "+str(poss_price)+" poss_cost "+str(poss_cost))
                            nso_table = {
                                "QUOTE_REV_PO_EQUIPMENT_PARTS_RECORD_ID": str(Guid.NewGuid()).upper(),
                                "BUSINESS_UNIT": nso_data.BUSINESS_UNIT,
                                "CONTRACT_VALID_FROM": eqp.CONTRACT_VALID_FROM,
                                "CONTRACT_VALID_TO": eqp.CONTRACT_VALID_TO,
                                "DIVISION_ID": nso_data.DIVISION_ID,
                                "DIVISION_RECORD_ID": nso_data.DIVISION_RECORD_ID,
                                "EQUIPMENT_DESCRIPTION": eqp.EQUIPMENT_DESCRIPTION,
                                "EQUIPMENT_ID": eqp.EQUIPMENT_ID,
                                "EQUIPMENT_RECORD_ID": eqp.EQUIPMENT_RECORD_ID,
                                "EQUIPMENT_STATUS": eqp.EQUIPMENT_STATUS,
                                "FABLOCATION_ID": eqp.FABLOCATION_ID,
                                "FABLOCATION_NAME": eqp.FABLOCATION_NAME,
                                "FABLOCATION_RECORD_ID": eqp.FABLOCATION_RECORD_ID,
                                "GREENBOOK": nso_data.GREENBOOK,
                                "GREENBOOK_RECORD_ID": nso_data.GREENBOOK_RECORD_ID,
                                "POSS_NSO_DESCRIPTION": nso_data.POSS_NSO_DESCRIPTION,
                                "POSS_NSO_PART_ID": nso_data.POSS_NSO_PART_ID, #A055S000P01-18196
                                "SERVICE_DESCRIPTION": eqp.SERVICE_DESCRIPTION,
                                "SERVICE_ID": eqp.SERVICE_ID,
                                "SERVICE_RECORD_ID": eqp.SERVICE_RECORD_ID,
                                "QUANTITY": 1,
                                "QUOTE_ID": str(self.contract_quote_id),
                                "QUOTE_RECORD_ID": str(self.contract_quote_record_id),
                                "QTEREV_ID": str(self.quote_revision_id),
                                "QTEREV_RECORD_ID": str(self.quote_revision_record_id),
                                "QTESRVGBK_RECORD_ID": eqp.QTESRVGBK_RECORD_ID,
                                "QTESRV_RECORD_ID": eqp.QTESRV_RECORD_ID,
                                "SAP_PART_NUMBER": nso_data.SAP_PART_NUMBER,
                                "SERIAL_NO": eqp.SERIAL_NO,
                                "TEMP_TOOL": eqp.TEMP_TOOL,
                                "POSS_COST": nso_data.POSS_COST,
                                "POSS_PRICE": nso_data.POSS_PRICE,
                                "EXTENDED_POSS_COST": float(poss_cost) * 1,
                                "EXTENDED_POSS_PRICE": float(poss_price) * 1,
                                "INCLUDED": "TRUE",
                                #CR666-INC08864593 - START - M
                                "PAR_SERVICE_DESCRIPTION": eqp.PAR_SERVICE_DESCRIPTION,
                                "PAR_SERVICE_ID": eqp.PAR_SERVICE_ID,
                                "PAR_SERVICE_RECORD_ID": eqp.PAR_SERVICE_RECORD_ID
                                #CR666-INC08864593 - END - M
                            } 
                            nso_table_info.AddRow(nso_table)
                            Sql.Upsert(nso_table_info)
        
        return error_msg

    def _add_equipment(self,auto_equp_insert = None,fab_list= None):
        #EquipList=[]
        master_object_name = "MAEQUP"
        if self.values:
            record_ids = []
            if self.all_values and auto_equp_insert is None:	     
                qury_str=""
                if A_Keys!="" and A_Values!="":
                    for key,val in zip(A_Keys,A_Values):
                        if(val!=""):
                            if key=="EQUIPMENT_RECORD_ID":
                                key="CpqTableEntryId"
                                val = ''.join(re.findall(r'\d+', val)) if not val.isdigit() else val
                            qury_str+=" "+key+" LIKE '%"+val+"%' AND "
                if self.tool_type=="TEMP_TOOL": 
                    query_string = "SELECT EQUIPMENT_RECORD_ID FROM MAEQUP (NOLOCK) WHERE {Query_str} ISNULL(SERIAL_NO, '') <> '' AND ISNULL(GREENBOOK, '') <> '' ".format(
                            Query_str= qury_str,
                            fab=self.tree_param,
                            QuoteRecordId=self.contract_quote_record_id,
                            RevisionRecordId=self.quote_revision_record_id
                        )			
                else:
                    #INC08896962 - Start - M
                    # INC08977656 - Starts - M
                    query_string = "SELECT EQUIPMENT_RECORD_ID FROM MAEQUP (NOLOCK) WHERE {Query_str} ISNULL(SERIAL_NO, '') <> '' AND ISNULL(GREENBOOK, '') <> '' AND ACCOUNT_RECORD_ID IN (SELECT ACCOUNT_RECORD_ID FROM SAACNT WHERE PAR_ACCOUNT_RECORD_ID = ( SELECT PAR_ACCOUNT_RECORD_ID FROM SAOPQT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' ) ) AND FABLOCATION_ID = '{fab}' AND EQUIPMENT_RECORD_ID NOT IN  (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND FABLOCATION_ID = '{fab}' AND ISNULL (SERIAL_NUMBER, '') <> '' )".format(
                            Query_str= qury_str,
                            acc=self.account_record_id,
                            fab=self.tree_param,
                            salesorgid = self.salesorg_id,
                            salesorgrecid=self.salesorg_record_id,
                            QuoteRecordId=self.contract_quote_record_id,
                            RevisionRecordId=self.quote_revision_record_id
                        )		
                    #INC08896962 - End - M
                    # INC08977656 - Ends - M
                query_string_for_count = "SELECT COUNT(*) as count FROM ({Query_String})OQ".format(
                    Query_String=query_string
                )
                #Trace.Write("query_string_for_count"+str(query_string))
                get_fab = "('"+str(self.tree_param)+"')"
                table_count_data = Sql.GetFirst(query_string_for_count)
                if table_count_data is not None:
                    table_total_rows = table_count_data.count
                if table_total_rows:
                    record_ids = [data for data in self.get_res(query_string, table_total_rows)]   
            ##equipment auto insert for sending equipment
            elif auto_equp_insert == "true": 
                #Trace.Write('ifff1--')       
                account_id = self.tree_param.split(' - ')
                account_id = account_id[len(account_id)-1]
                fab_type = 'SENDING FAB' if "Sending Account -" in self.tree_param else 'RECEIVING FAB' if "Receiving Account -" in self.tree_param else ""
                get_fab_query = Sql.GetList("SELECT FABLOCATION_ID FROM SAQFBL WHERE QUOTE_RECORD_ID = '{}' and QTEREV_RECORD_ID = '{}' and ACCOUNT_ID = '{}' and RELOCATION_FAB_TYPE = '{}' ".format(self.contract_quote_record_id,self.quote_revision_record_id,account_id,fab_type) )
                if get_fab_query:
                    get_fab = str(tuple([fab['FABLOCATION_ID'] for fab in fab_list])).replace(",)",')')
                else:
                    get_fab = ""
                query_string = "SELECT EQUIPMENT_RECORD_ID FROM MAEQUP (NOLOCK) WHERE ACCOUNT_ID = '{acc}' AND FABLOCATION_ID in {fab} AND  ISNULL(SERIAL_NO, '') <> '' AND ISNULL(GREENBOOK, '') <> '' AND NOT EXISTS (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND FABLOCATION_ID in {fab} and RELOCATION_EQUIPMENT_TYPE = '{equp_type}' )".format(
                            acc=account_id,
                            fab=get_fab,
                            QuoteRecordId=self.contract_quote_record_id,
                            RevisionRecordId=self.quote_revision_record_id,
                            equp_type = "SENDING EQUIPMENT" if "Sending Account -" in self.tree_param else "RECEIVING EQUIPMENT" if "Receiving Account -" in self.tree_param else "" )
                query_string_for_count = "SELECT COUNT(*) as count FROM ({Query_String})OQ".format(
                    Query_String=query_string
                )
                table_count_data = Sql.GetFirst(query_string_for_count)
                if table_count_data is not None:
                    table_total_rows = table_count_data.count
                if table_total_rows:
                    record_ids = [data for data in self.get_res(query_string, table_total_rows)]                  
            else:
                get_fab = "('"+str(self.tree_param)+"')"
                record_ids = [
                    CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
                    if value.strip() != "" and master_object_name in value
                    else value
                    for value in self.values
                ]
            batch_group_record_id = str(Guid.NewGuid()).upper()
            record_ids = str(str(record_ids)[1:-1].replace("'",""))
            parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
            SqlHelper.GetFirst(""+str(parameter.QUERY_CRITERIA_1)+" SYSPBT(BATCH_RECORD_ID, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,QTEREV_RECORD_ID) SELECT MAEQUP.EQUIPMENT_RECORD_ID as BATCH_RECORD_ID, ''IN PROGRESS'' as BATCH_STATUS, ''"+str(self.contract_quote_id)+"'' as QUOTE_ID, ''"+str(self.contract_quote_record_id)+"'' as QUOTE_RECORD_ID, ''"+str(batch_group_record_id)+"'' as BATCH_GROUP_RECORD_ID,''"+str(self.quote_revision_record_id)+"'' as QTEREV_RECORD_ID FROM MAEQUP (NOLOCK) JOIN splitstring(''"+record_ids+"'') ON ltrim(rtrim(NAME)) = MAEQUP.EQUIPMENT_RECORD_ID'")
            # INC08764519 - Start - M
            get_fab_details = Sql.GetFirst("SELECT FAB_LOCATION_RECORD_ID,FAB_LOCATION_ID,FAB_LOCATION_NAME from MAFBLC WHERE FAB_LOCATION_ID = '"+str(self.tree_param)+"' ")
            # INC08764519 - End - M
            get_salesorg= Sql.GetFirst("SELECT SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '{QuoteRecId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,))
            #INC08704188 - Start - M
            self._process_query(
                            """
                                INSERT SAQFEQ (
                                    QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
                                    EQUIPMENT_ID,
                                    EQUIPMENT_RECORD_ID,
                                    EQUIPMENT_DESCRIPTION,                            
                                    FABLOCATION_ID,
                                    FABLOCATION_NAME,
                                    FABLOCATION_RECORD_ID,
                                    SERIAL_NUMBER,
                                    QUOTE_RECORD_ID,
                                    QUOTE_ID,
                                    QUOTE_NAME,
                                    QTEREV_ID,
                                    QTEREV_RECORD_ID,
                                    KPU,
                                    PLATFORM,
                                    EQUIPMENTCATEGORY_RECORD_ID,
                                    EQUIPMENTCATEGORY_ID,
                                    EQUIPMENTCATEGORY_DESCRIPTION,
                                    EQUIPMENT_STATUS,
                                    PBG,
                                    GREENBOOK,
                                    GREENBOOK_RECORD_ID,
                                    MNT_PLANT_RECORD_ID,
                                    MNT_PLANT_ID,
                                    MNT_PLANT_NAME,
                                    WARRANTY_START_DATE,
                                    WARRANTY_END_DATE,
                                    SALESORG_ID,
                                    SALESORG_NAME,
                                    SALESORG_RECORD_ID,
                                    CUSTOMER_TOOL_ID,
                                    CPQTABLEENTRYADDEDBY,
                                    CPQTABLEENTRYDATEADDED,
                                    CpqTableEntryModifiedBy,
                                    CpqTableEntryDateModified,
                                    RELOCATION_FAB_TYPE,
                                    RELOCATION_EQUIPMENT_TYPE,WAFER_SIZE,
                                    TECHNOLOGY,
                                    TEMP_TOOL,
                                    DEVICE_NODE,
                                    DEVICE_TYPE,
                                    PROCESS_TYPE,
                                    WAFER_SIZE_GROUP,
                                    GENERATION,
                                    END_PRODUCT_TECHNOLOGY,
                                    SUBSTRATE_SIZE_GROUP
                                    ) SELECT
                                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
                                        MAEQUP.EQUIPMENT_ID,
                                        MAEQUP.EQUIPMENT_RECORD_ID,
                                        MAEQUP.EQUIPMENT_DESCRIPTION,  
                                        {fab_id},{fab_name},{fab_recid},                    
                                        MAEQUP.SERIAL_NO,
                                        '{QuoteRecId}' as QUOTE_RECORD_ID,
                                        '{QuoteId}' as QUOTE_ID,
                                        '{QuoteName}' as QUOTE_NAME,
                                        '{RevisionId}' as QTEREV_ID,
                                        '{RevisionRecordId}' as QTEREV_RECORD_ID,
                                        MAEQUP.KPU,
                                        MAEQUP.PLATFORM,
                                        MAEQUP.EQUIPMENTCATEGORY_RECORD_ID,
                                        MAEQUP.EQUIPMENTCATEGORY_ID,
                                        MAEQCT.EQUIPMENTCATEGORY_DESCRIPTION,
                                        MAEQUP.EQUIPMENT_STATUS,
                                        MAEQUP.PBG,
                                        MAEQUP.GREENBOOK,
                                        MAEQUP.GREENBOOK_RECORD_ID,
                                        MAEQUP.MNT_PLANT_RECORD_ID,
                                        MAEQUP.MNT_PLANT_ID,
                                        MAEQUP.MNT_PLANT_NAME,
                                        {warranty_start},{warranty_end},{salesorg_id},{salesorg_name},{salesorg_recid},
                                        MAEQUP.CUSTOMER_TOOL_ID,
                                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                                        GETDATE() as CPQTABLEENTRYDATEADDED,
                                        {UserId} as CpqTableEntryModifiedBy,
                                        GETDATE() as CpqTableEntryDateModified,
                                        '{relocation_fab_type}' AS RELOCATION_FAB_TYPE,
                                        '{relocation_equp_type}' AS RELOCATION_EQUIPMENT_TYPE,
                                        MAEQUP.SUBSTRATE_SIZE,
                                        MAEQUP.TECHNOLOGY,
                                        '{is_temptool}' AS TEMP_TOOL,
                                        MAEQUP.DEVICE_NODE,
                                        MAEQUP.DEVICE_TYPE,
                                        MAEQUP.PROCESS_TYPE,
                                        MAEQUP.WAFER_SIZE_GROUP,
                                        MAEQUP.GENERATION,
                                        MAEQUP.END_PRODUCT_TECHNOLOGY,
                                        MAEQUP.SUBSTRATE_SIZE_GROUP 
                                        FROM MAEQUP (NOLOCK)
                                        JOIN SYSPBT (NOLOCK) ON SYSPBT.BATCH_RECORD_ID = MAEQUP.EQUIPMENT_RECORD_ID JOIN MAEQCT(NOLOCK)
                                        ON MAEQUP.EQUIPMENTCATEGORY_ID = MAEQCT.EQUIPMENTCATEGORY_ID
                                        WHERE 
                                        SYSPBT.QUOTE_RECORD_ID = '{QuoteRecId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'
                                        AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'                        
                                """.format(
                                fab_id=" '"+str(get_fab_details.FAB_LOCATION_ID)+"' AS FABLOCATION_ID" if self.tool_type=="TEMP_TOOL" else " MAEQUP.FABLOCATION_ID ",
                                fab_name=" '"+str(get_fab_details.FAB_LOCATION_NAME)+"' AS FABLOCATION_NAME" if self.tool_type=="TEMP_TOOL" else " MAEQUP.FABLOCATION_NAME ",
                                fab_recid = " '"+str(get_fab_details.FAB_LOCATION_RECORD_ID)+"' AS FABLOCATION_RECORD_ID" if self.tool_type=="TEMP_TOOL" else " MAEQUP.FABLOCATION_RECORD_ID ",
                                salesorg_id = " '"+str(get_salesorg.SALESORG_ID)+"' AS SALESORG_ID" if self.tool_type=="TEMP_TOOL" else " MAEQUP.SALESORG_ID ",
                                salesorg_name = " '"+str(get_salesorg.SALESORG_NAME)+"' AS SALESORG_NAME" if self.tool_type=="TEMP_TOOL" else " MAEQUP.SALESORG_NAME ",
                                salesorg_recid = " '"+str(get_salesorg.SALESORG_RECORD_ID)+"' AS SALESORG_RECORD_ID" if self.tool_type=="TEMP_TOOL" else " MAEQUP.SALESORG_RECORD_ID ",
                                warranty_start = " NULL AS WARRANTY_START_DATE" if self.tool_type=="TEMP_TOOL" else " MAEQUP.WARRANTY_START_DATE ",
                                warranty_end = " NULL AS WARRANTY_END_DATE" if self.tool_type=="TEMP_TOOL" else " MAEQUP.WARRANTY_END_DATE ",
                                is_temptool = "TRUE" if self.tool_type=="TEMP_TOOL" else "",
                                treeparam=self.tree_param,
                                treeparentparam=self.tree_parent_level_0,
                                QuoteId=self.contract_quote_id,
                                BatchGroupRecordId=batch_group_record_id,
                                UserName=self.user_name,
                                UserId=self.user_id,
                                QuoteRecId=self.contract_quote_record_id,
                                RevisionId=self.quote_revision_id,
                                RevisionRecordId=self.quote_revision_record_id,
                                # INC08617554 Starts - M
                                QuoteName= str(self.contract_quote_name).replace("'","''"),
                                # INC08617554 Ends - M
                                relocation_fab_type = "SENDING FAB" if "Sending Account -" in self.tree_param else "RECEIVING FAB" if "Receiving Account -" in self.tree_param else "",
                                relocation_equp_type = "SENDING EQUIPMENT" if "Sending Account -" in self.tree_param else "RECEIVING EQUIPMENT" if "Receiving Account -" in self.tree_param else "",
                            )
                        )
            #INC08704188 - End - M
            #ibase attributes update Query optimisation
            Sql.RunQuery("UPDATE SAQFEQ SET IBASE_ATTSTS = 'INCOMPLETE' WHERE (ISNULL(PLATFORM, '') = '' OR ISNULL(DEVICE_TYPE, '') = '' OR ISNULL(DEVICE_NODE, '') = '' OR ISNULL(SUBSTRATE_SIZE_GROUP, '')= '') AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'" .format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
            Sql.RunQuery("UPDATE SAQFEQ SET IBASE_ATTSTS = 'COMPLETE' WHERE ISNULL(PLATFORM, '') != '' AND ISNULL(DEVICE_TYPE, '') != '' AND ISNULL(DEVICE_NODE, '') != '' AND ISNULL(SUBSTRATE_SIZE_GROUP, '') != '' AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'" .format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
            Sql.RunQuery("UPDATE SAQFEQ SET IBASE_ATTSTS = 'INCOMPLETE' WHERE (ISNULL(TECHNOLOGY, '') = '' OR ISNULL(GENERATION, '') = '' OR ISNULL(END_PRODUCT_TECHNOLOGY, '')= '') AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'AND GREENBOOK = 'DISPLAY'" .format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
            Sql.RunQuery("UPDATE SAQFEQ SET IBASE_ATTSTS = 'COMPLETE' WHERE ISNULL(TECHNOLOGY, '') != '' AND ISNULL(GENERATION, '') != '' AND ISNULL(END_PRODUCT_TECHNOLOGY, '') != '' AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'AND GREENBOOK = 'DISPLAY'" .format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
            self._process_query(
                    """INSERT SAQFGB(
                        FABLOCATION_ID,
                        FABLOCATION_NAME,
                        FABLOCATION_RECORD_ID,
                        GREENBOOK,
                        GREENBOOK_RECORD_ID,
                        QUOTE_ID,
                        QUOTE_NAME,
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        SALESORG_ID,
                        SALESORG_NAME,
                        SALESORG_RECORD_ID,						
                        CpqTableEntryModifiedBy,
                        CpqTableEntryDateModified,
                        QUOTE_FAB_LOC_GB_RECORD_ID,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED
                        ) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOC_GB_RECORD_ID,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED FROM (
                        SELECT DISTINCT
                        SAQFEQ.FABLOCATION_ID,
                        SAQFEQ.FABLOCATION_NAME,
                        SAQFEQ.FABLOCATION_RECORD_ID,
                        SAQFEQ.GREENBOOK,
                        SAQFEQ.GREENBOOK_RECORD_ID,
                        SAQFEQ.QUOTE_ID,
                        SAQFEQ.QUOTE_NAME,
                        SAQFEQ.QUOTE_RECORD_ID,
                        SAQFEQ.QTEREV_ID,
                        SAQFEQ.QTEREV_RECORD_ID,
                        SAQFEQ.SALESORG_ID,
                        SAQFEQ.SALESORG_NAME,
                        SAQFEQ.SALESORG_RECORD_ID,
                        {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified
                        FROM SAQFEQ (NOLOCK)
                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID
                        JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQFEQ.EQUIPMENT_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID WHERE SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQFEQ.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'  AND NOT EXISTS (SELECT * FROM SAQFGB B WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQFEQ.GREENBOOK = B.GREENBOOK AND FABLOCATION_ID IN {fab})
                        ) FB""".format(
                                        treeparam=self.tree_param,
                                        QuoteRecordId=self.contract_quote_record_id,
                                        RevisionRecordId=self.quote_revision_record_id,
                                        BatchGroupRecordId=batch_group_record_id,
                                        UserId=self.user_id,
                                        UserName=self.user_name,
                                        fab = get_fab,
                                    )
                    )		
            # INC08694276 - Start - M AND INC08701856
            #INC08700058 - Start - M 
            # INC08737391 - Starts - M
            self._process_query(
                    """
                        INSERT SAQFEA (
                            QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,
                            EQUIPMENT_ID,
                            EQUIPMENT_RECORD_ID,
                            EQUIPMENT_DESCRIPTION,
                            ASSEMBLY_ID,
                            ASSEMBLY_STATUS,
                            ASSEMBLY_DESCRIPTION,
                            ASSEMBLY_RECORD_ID,                           
                            FABLOCATION_ID,
                            FABLOCATION_NAME,
                            FABLOCATION_RECORD_ID,
                            SERIAL_NUMBER,
                            QUOTE_RECORD_ID,
                            QUOTE_ID,
                            QUOTE_NAME,
                            QTEREV_ID,
                            QTEREV_RECORD_ID,
                            EQUIPMENTCATEGORY_RECORD_ID,
                            EQUIPMENTCATEGORY_ID,
                            EQUIPMENTCATEGORY_DESCRIPTION,
                            EQUIPMENTTYPE_ID,
                            EQUIPMENTTYPE_DESCRIPTION,
                            EQUIPMENTTYPE_RECORD_ID,
                            GOT_CODE,
                            MNT_PLANT_RECORD_ID,
                            MNT_PLANT_ID,
                            WARRANTY_START_DATE,
                            WARRANTY_END_DATE,
                            SALESORG_ID,
                            SALESORG_NAME,
                            SALESORG_RECORD_ID,
                            GREENBOOK,
                            GREENBOOK_RECORD_ID,
                            QTEREVFEQ_RECORD_ID,
                            CPQTABLEENTRYADDEDBY,
                            CPQTABLEENTRYDATEADDED,
                            CpqTableEntryModifiedBy,
                            CpqTableEntryDateModified
                            ) SELECT
                                CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
                                MAEQUP.PAR_EQUIPMENT_ID,
                                MAEQUP.PAR_EQUIPMENT_RECORD_ID,
                                MAEQUP.PAR_EQUIPMENT_DESCRIPTION,
                                MAEQUP.EQUIPMENT_ID,
                                MAEQUP.EQUIPMENT_STATUS,
                                MAEQUP.EQUIPMENT_DESCRIPTION,
                                MAEQUP.EQUIPMENT_RECORD_ID,                 
                                SAQFEQ.FABLOCATION_ID,
                                SAQFEQ.FABLOCATION_NAME,
                                SAQFEQ.FABLOCATION_RECORD_ID,
                                MAEQUP.SERIAL_NO,
                                '{QuoteRecId}' as QUOTE_RECORD_ID,
                                '{QuoteId}' as QUOTE_ID,
                                '{QuoteName}' as QUOTE_NAME,
                                '{RevisionId}' as QTEREV_ID,
                                '{RevisionRecordId}' as QTEREV_RECORD_ID,
                                MAEQUP.EQUIPMENTCATEGORY_RECORD_ID,
                                MAEQUP.EQUIPMENTCATEGORY_ID,
                                MAEQCT.EQUIPMENTCATEGORY_DESCRIPTION,
                                MAEQUP.EQUIPMENTTYPE_ID,
                                MAEQTY.EQUIPMENT_TYPE_DESCRIPTION,
                                MAEQUP.EQUIPMENTTYPE_RECORD_ID,
                                MAEQUP.GOT_CODE,
                                MAEQUP.MNT_PLANT_RECORD_ID,
                                MAEQUP.MNT_PLANT_ID,
                                MAEQUP.WARRANTY_START_DATE,
                                MAEQUP.WARRANTY_END_DATE,
                                MAEQUP.SALESORG_ID,
                                MAEQUP.SALESORG_NAME,
                                MAEQUP.SALESORG_RECORD_ID,
                                SAQFEQ.GREENBOOK,
                                SAQFEQ.GREENBOOK_RECORD_ID,
                                SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID AS QTEREVFEQ_RECORD_ID,
                                '{UserName}' AS CPQTABLEENTRYADDEDBY,
                                GETDATE() as CPQTABLEENTRYDATEADDED,
                                {UserId} as CpqTableEntryModifiedBy,
                                GETDATE() as CpqTableEntryDateModified
                                FROM MAEQUP (NOLOCK)
                                JOIN SYSPBT (NOLOCK)
                                ON SYSPBT.BATCH_RECORD_ID = MAEQUP.PAR_EQUIPMENT_RECORD_ID LEFT JOIN MAEQCT(NOLOCK)
                                ON MAEQUP.EQUIPMENTCATEGORY_ID = MAEQCT.EQUIPMENTCATEGORY_ID LEFT JOIN MAEQTY (NOLOCK)
                                ON MAEQTY.EQUIPMENT_TYPE_ID = MAEQUP.EQUIPMENTTYPE_ID
                                JOIN SAQFEQ (NOLOCK) ON SAQFEQ.EQUIPMENT_RECORD_ID = SYSPBT.BATCH_RECORD_ID AND SAQFEQ.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQFEQ.QTEREV_RECORD_ID = SYSPBT.QTEREV_RECORD_ID
                                WHERE 
                                SYSPBT.QUOTE_RECORD_ID = '{QuoteRecId}'
                                AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'                        
                        """.format(
                        treeparam=self.tree_param,
                        treeparentparam=self.tree_parent_level_0,
                        QuoteId=self.contract_quote_id,
                        BatchGroupRecordId=batch_group_record_id,
                        UserName=self.user_name,
                        UserId=self.user_id,
                        QuoteRecId=self.contract_quote_record_id,
                        RevisionId=self.quote_revision_id,
                        RevisionRecordId=self.quote_revision_record_id,
                        QuoteName=str(self.contract_quote_name).replace("'","''")
                    )
                )
            # INC08737391 - Ends - M
            #INC08700058 - End - M 
            # INC08694276 - End - M INC08701856 M
            #INC08730324 A
            self._process_query("""UPDATE A SET A.IBASE_ATTSTS ='NO ASSEMBLY' FROM SAQFEQ A(NOLOCK) LEFT OUTER JOIN SAQFEA B(NOLOCK) on A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID WHERE A.QUOTE_RECORD_ID = '{QuoteRecId}' AND A.QTEREV_RECORD_ID ='{RevisionRecordId}' AND B.EQUIPMENT_ID IS NULL""".format(QuoteRecId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
            #INC08730324 A
            self._process_query(
                                """DELETE FROM SYSPBT WHERE SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' and SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' and SYSPBT.BATCH_STATUS = 'IN PROGRESS'""".format(
                                    BatchGroupRecordId=batch_group_record_id,RevisionRecordId=self.quote_revision_record_id
                                )
                            )
        return True

    def _update(self):
        pass

    def _delete(self):
        pass
    
    def get_res(self, query_string, table_total_rows):
        for offset_skip_count in range(0, table_total_rows+1, 1000):
            pagination_condition = "WHERE SNO>={Skip_Count} AND SNO<={Fetch_Count}".format(Skip_Count=offset_skip_count+1, Fetch_Count=offset_skip_count+1000)
            query_string_with_pagination = 'SELECT * FROM (SELECT *, ROW_NUMBER()OVER(ORDER BY EQUIPMENT_RECORD_ID) AS SNO FROM ({Query_String}) IQ)OQ {Pagination_Condition}'.format(
                                            Query_String=query_string, Pagination_Condition=pagination_condition)
            table_data = Sql.GetList(query_string_with_pagination)
            if table_data is not None:
                for row_data in table_data:
                    yield row_data.EQUIPMENT_RECORD_ID


class ContractQuoteCoveredObjModel(ContractQuoteCrudOpertion):
    def __init__(self, **kwargs):
        ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'), 
                                            tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'),tree_parent_level_1=kwargs.get('tree_parent_level_1'))
        self.opertion = kwargs.get('opertion')
        self.action_type = kwargs.get('action_type')
        self.values = kwargs.get('values')
        self.table_name = kwargs.get('table_name')
        self.all_values = kwargs.get('all_values')
        self.applied_preventive_maintainence_quote_type_changed = kwargs.get('applied_preventive_maintainence_quote_type_changed')
        self.tools_from_ui = kwargs.get('tools_from_ui')
        self.entitlement_level_value = kwargs.get('entitlement_level_value')
        self.entitlement_level = kwargs.get('entitlement_level')
        self.entitlement_value = kwargs.get('entitlement_value')
        self.pmevents_changes_insert =  kwargs.get('pmevents_changes_insert')
        self.pm_entlmnt_val = kwargs.get('pm_entlmnt_val')
        self.ent_quote_type = kwargs.get('ent_quote_type')#INC08621345 - A 
        self.tool_type = kwargs.get('tool_type')
        self.new_revision = kwargs.get('new_revision')
        self.quote_type_value = kwargs.get('quote_type_value') ####A055S000P01-19173 code starts..ends..
        self.real_time_integration_service = kwargs.get('real_time_integration_service')
        self.node_id = ""

    def get_results(self, query_string, table_total_rows):
        for offset_skip_count in range(0, table_total_rows+1, 1000):
            pagination_condition = "WHERE SNO>={Skip_Count} AND SNO<={Fetch_Count}".format(Skip_Count=offset_skip_count+1, Fetch_Count=offset_skip_count+1000)
            if Product.GetGlobal("addon_service_id") == "Z0123":
                query_string_with_pagination = 'SELECT * FROM (SELECT *, ROW_NUMBER()OVER(ORDER BY QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) AS SNO FROM ({Query_String}) IQ)OQ {Pagination_Condition}'.format(
                                                Query_String=query_string, Pagination_Condition=pagination_condition)
            else:
                query_string_with_pagination = 'SELECT * FROM (SELECT *, ROW_NUMBER()OVER(ORDER BY QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID) AS SNO FROM ({Query_String}) IQ)OQ {Pagination_Condition}'.format(
                                                Query_String=query_string, Pagination_Condition=pagination_condition)
            table_data = Sql.GetList(query_string_with_pagination)
            if table_data is not None:
                for row_data in table_data:
                    if Product.GetGlobal("addon_service_id") == "Z0123":
                        yield row_data.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID
                    else:
                        yield  row_data.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID

    def _insert_quote_service_covered_object(self,record_ids='', **kwargs):		
        Trace.Write("self.trigger_from ---->"+str(self.trigger_from)+" - "+str(record_ids))
        Trace.Write("@@batch record id in function-->"+str(kwargs.get('batch_group_record_id')))
        #INC09226624 start
        eqp_where = ""
        if self.tree_param in ("Z0004","Z0004W"):
            eqp_where = "AND MAEQUP.EQUIPMENTCATEGORY_ID = 'Y'"
        #INC09226624 end
        if self.tree_param.endswith("W"):
            #Log.Info("self.tree_param"+str(self.tree_param))
            self._process_query(
            """
                INSERT SAQSCO (
                    QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
                    EQUIPMENT_ID,
                    EQUIPMENT_RECORD_ID,
                    EQUIPMENT_DESCRIPTION,
                    FABLOCATION_ID,
                    FABLOCATION_NAME,
                    FABLOCATION_RECORD_ID,
                    WAFER_SIZE,
                    SALESORG_ID,
                    SALESORG_NAME,
                    SALESORG_RECORD_ID,
                    SERIAL_NO,
                    QUOTE_RECORD_ID,
                    QUOTE_ID,
                    QUOTE_NAME,
                    ACCOUNT_ID,
                    ACCOUNT_NAME,
                    ACCOUNT_RECORD_ID,
                    QTEREV_ID,
                    QTEREV_RECORD_ID,
                    KPU,
                    RELOCATION_EQUIPMENT_TYPE,
                    SERVICE_ID,
                    SERVICE_TYPE,
                    SERVICE_DESCRIPTION,
                    SERVICE_RECORD_ID,
                    EQUIPMENT_STATUS,
                    EQUIPMENTCATEGORY_ID,
                    EQUIPMENTCATEGORY_DESCRIPTION,
                    EQUIPMENTCATEGORY_RECORD_ID,
                    PLATFORM,
                    GREENBOOK,
                    GREENBOOK_RECORD_ID,
                    MNT_PLANT_RECORD_ID,
                    MNT_PLANT_NAME,
                    MNT_PLANT_ID,
                    WARRANTY_START_DATE,
                    WARRANTY_END_DATE,
                    CUSTOMER_TOOL_ID,
                    PAR_SERVICE_DESCRIPTION,
                    PAR_SERVICE_ID,
                    PAR_SERVICE_RECORD_ID,
                    TECHNOLOGY,
                    CONTRACT_VALID_FROM,
                    CONTRACT_VALID_TO,
                    TEMP_TOOL,
                    QTEREVFEQ_RECORD_ID,
                    TOOL_CONFIG,
                    IBASE_ATTSTS,
                    DEVICE_NODE,
                    CPQTABLEENTRYADDEDBY,
                    CPQTABLEENTRYDATEADDED,
                    CpqTableEntryModifiedBy,
                    CpqTableEntryDateModified					
                    ) SELECT CONVERT(VARCHAR(100),NEWID()) AS QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,A.*  FROM (SELECT
                        DISTINCT
                        SAQFEQ.EQUIPMENT_ID,
                        SAQFEQ.EQUIPMENT_RECORD_ID,
                        SAQFEQ.EQUIPMENT_DESCRIPTION,                                
                        SAQFEQ.FABLOCATION_ID,
                        SAQFEQ.FABLOCATION_NAME,
                        SAQFEQ.FABLOCATION_RECORD_ID,
                        SAQFEQ.WAFER_SIZE,
                        SAQFEQ.SALESORG_ID,
                        SAQFEQ.SALESORG_NAME,
                        SAQFEQ.SALESORG_RECORD_ID,
                        SERIAL_NUMBER,
                        SAQFEQ.QUOTE_RECORD_ID,
                        SAQFEQ.QUOTE_ID,
                        SAQFEQ.QUOTE_NAME,
                        '{account_id}' as ACCOUNT_ID,
                        '{account_name}' as ACCOUNT_NAME,
                        '{account_record_id}' as ACCOUNT_RECORD_ID,
                        SAQFEQ.QTEREV_ID,
                        SAQFEQ.QTEREV_RECORD_ID,
                        SAQFEQ.KPU,
                        '{RelocationEqType}' AS RELOCATION_EQUIPMENT_TYPE,
                        '{TreeParam}' as SERVICE_ID,
                        '{TreeParentParam}' as SERVICE_TYPE,
                        SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
                        SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
                        SAQFEQ.EQUIPMENT_STATUS,
                        SAQFEQ.EQUIPMENTCATEGORY_ID,
                        SAQFEQ.EQUIPMENTCATEGORY_DESCRIPTION,
                        SAQFEQ.EQUIPMENTCATEGORY_RECORD_ID,
                        SAQFEQ.PLATFORM,
                        SAQFEQ.GREENBOOK,
                        SAQFEQ.GREENBOOK_RECORD_ID,
                        SAQFEQ.MNT_PLANT_RECORD_ID,
                        SAQFEQ.MNT_PLANT_NAME,
                        SAQFEQ.MNT_PLANT_ID,
                        SAQFEQ.WARRANTY_START_DATE,
                        SAQFEQ.WARRANTY_END_DATE,
                        SAQFEQ.CUSTOMER_TOOL_ID,
                        SAQTSV.PAR_SERVICE_DESCRIPTION,
                        SAQTSV.PAR_SERVICE_ID,
                        SAQTSV.PAR_SERVICE_RECORD_ID,
                        SAQFEQ.TECHNOLOGY,
                        SAQTSV.CONTRACT_VALID_FROM as CONTRACT_VALID_FROM,
                        SAQTSV.CONTRACT_VALID_TO as CONTRACT_VALID_TO,
                        SAQFEQ.TEMP_TOOL,
                        SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID as QTEREVFEQ_RECORD_ID,
                        MAEQUP.TOOL_CONFIGURATION as TOOL_CONFIG,
                        SAQFEQ.IBASE_ATTSTS,
                        SAQFEQ.DEVICE_NODE,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified						
                        FROM SAQFEQ (NOLOCK) JOIN SAQTSV (NOLOCK) ON
                        SAQFEQ.QUOTE_ID = SAQTSV.QUOTE_ID AND
                        SAQTSV.SERVICE_ID = '{TreeParam}' AND
                        SAQTSV.SERVICE_TYPE = '{TreeParentParam}'
                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID=SAQFEQ.QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID
                        JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQFEQ.EQUIPMENT_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID  AND SYSPBT.QTEREV_RECORD_ID=SAQTSV.QTEREV_RECORD_ID AND SYSPBT.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID = SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID
                        JOIN MAEQUP (NOLOCK) ON MAEQUP.EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID {eqp_where}
                        WHERE 
                        SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQFEQ.QTEREV_RECORD_ID = '{RevisionRecordId}'
                        AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND  (SAQFEQ.TEMP_TOOL = 'False' or SAQFEQ.TEMP_TOOL IS NULL) )A                       
                """.format(
                        TreeParam=self.tree_param,
                        TreeParentParam=self.tree_parent_level_0,
                        QuoteRecordId=self.contract_quote_record_id,
                        RevisionRecordId=self.quote_revision_record_id,
                        BatchGroupRecordId=kwargs.get('batch_group_record_id'),
                        UserName=self.user_name,
                        UserId=self.user_id,
                        eqp_where = eqp_where,
                        account_id=self.account_id,
                        account_name=self.account_name,
                        account_record_id=self.account_record_id,
                        RelocationEqType=self.tree_param if self.tree_parent_level_1 == 'Complementary Products' else ''
                    )
            )
        elif self.tree_param == "Add-On Products":
            service_addon_object =Sql.GetList("Select SAQSAO.*,SAQTSV.QUOTE_SERVICE_RECORD_ID from SAQSAO (nolock) inner join SAQTSV on SAQTSV.QUOTE_RECORD_ID=SAQSAO.QUOTE_RECORD_ID and SAQTSV.QTEREV_RECORD_ID=SAQSAO.QTEREV_RECORD_ID and SAQTSV.SERVICE_ID = SAQSAO.ADNPRD_ID where SAQSAO.QUOTE_RECORD_ID= '{QuoteRecordId}' AND SAQSAO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSAO.ACTIVE ='TRUE' AND SAQSAO.SERVICE_ID = '{service_id}' AND SAQSAO.SERVICE_ID NOT IN (SELECT SERVICE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{service_id}' AND SAQTSV.SERVICE_ID=SAQSAO.ADNPRD_ID)".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, service_id =self.tree_parent_level_1 ))
            #tableInfo = SqlHelper.GetTable("SAQTSE")
                                                            
            x = datetime.datetime.today()
            x= str(x)
            y = x.split(" ")
            #CR666-INC08864593 - START - M
            for OfferingRow_detail in service_addon_object:
                CQADDONPRD._addon_equipment_insert(OfferingRow_detail,self.tree_parent_level_0,record_ids,self.tree_parent_level_1)
            #CR666-INC08864593 - END - M
        else:
            #Log.Info("self.tree_param_else"+str(self.tree_param))
            self._process_query(
                """
                    INSERT SAQSCO (
                        QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
                        EQUIPMENT_ID,
                        EQUIPMENT_RECORD_ID,
                        EQUIPMENT_DESCRIPTION,
                        FABLOCATION_ID,
                        FABLOCATION_NAME,
                        FABLOCATION_RECORD_ID,
                        WAFER_SIZE,
                        SALESORG_ID,
                        SALESORG_NAME,
                        SALESORG_RECORD_ID,
                        SERIAL_NO,
                        QUOTE_RECORD_ID,
                        QUOTE_ID,
                        QUOTE_NAME,
                        ACCOUNT_ID,
                        ACCOUNT_NAME,
                        ACCOUNT_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        KPU,
                        RELOCATION_EQUIPMENT_TYPE,
                        SERVICE_ID,
                        SERVICE_TYPE,
                        SERVICE_DESCRIPTION,
                        SERVICE_RECORD_ID,
                        EQUIPMENT_STATUS,
                        EQUIPMENTCATEGORY_ID,
                        EQUIPMENTCATEGORY_DESCRIPTION,
                        EQUIPMENTCATEGORY_RECORD_ID,
                        PLATFORM,
                        GREENBOOK,
                        GREENBOOK_RECORD_ID,
                        MNT_PLANT_RECORD_ID,
                        MNT_PLANT_NAME,
                        MNT_PLANT_ID,
                        WARRANTY_START_DATE,
                        WARRANTY_END_DATE,
                        CUSTOMER_TOOL_ID,
                        PAR_SERVICE_DESCRIPTION,
                        PAR_SERVICE_ID,
                        PAR_SERVICE_RECORD_ID,
                        TECHNOLOGY,
                        CONTRACT_VALID_FROM,
                        CONTRACT_VALID_TO,
                        TEMP_TOOL,
                        QTEREVFEQ_RECORD_ID,
                        TOOL_CONFIG,
                        IBASE_ATTSTS,
                        DEVICE_NODE,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED,
                        CpqTableEntryModifiedBy,
                        CpqTableEntryDateModified
                        ) SELECT CONVERT(VARCHAR(100),NEWID()) AS QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,A.*  FROM (SELECT
                            DISTINCT
                            SAQFEQ.EQUIPMENT_ID,
                            SAQFEQ.EQUIPMENT_RECORD_ID,
                            SAQFEQ.EQUIPMENT_DESCRIPTION,                                
                            SAQFEQ.FABLOCATION_ID,
                            SAQFEQ.FABLOCATION_NAME,
                            SAQFEQ.FABLOCATION_RECORD_ID,
                            SAQFEQ.WAFER_SIZE,
                            SAQFEQ.SALESORG_ID,
                            SAQFEQ.SALESORG_NAME,
                            SAQFEQ.SALESORG_RECORD_ID,
                            SERIAL_NUMBER,
                            SAQFEQ.QUOTE_RECORD_ID,
                            SAQFEQ.QUOTE_ID,
                            SAQFEQ.QUOTE_NAME,
                            '{account_id}' as ACCOUNT_ID,
                            '{account_name}' as ACCOUNT_NAME,
                            '{account_record_id}' as ACCOUNT_RECORD_ID,
                            SAQFEQ.QTEREV_ID,
                            SAQFEQ.QTEREV_RECORD_ID,
                            SAQFEQ.KPU,
                            '{RelocationEqType}' AS RELOCATION_EQUIPMENT_TYPE,
                            '{TreeParam}' as SERVICE_ID,
                            '{TreeParentParam}' as SERVICE_TYPE,
                            SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
                            SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
                            SAQFEQ.EQUIPMENT_STATUS,
                            SAQFEQ.EQUIPMENTCATEGORY_ID,
                            SAQFEQ.EQUIPMENTCATEGORY_DESCRIPTION,
                            SAQFEQ.EQUIPMENTCATEGORY_RECORD_ID,
                            SAQFEQ.PLATFORM,
                            SAQFEQ.GREENBOOK,
                            SAQFEQ.GREENBOOK_RECORD_ID,
                            SAQFEQ.MNT_PLANT_RECORD_ID,
                            SAQFEQ.MNT_PLANT_NAME,
                            SAQFEQ.MNT_PLANT_ID,
                            SAQFEQ.WARRANTY_START_DATE,
                            SAQFEQ.WARRANTY_END_DATE,
                            SAQFEQ.CUSTOMER_TOOL_ID,
                            SAQTSV.PAR_SERVICE_DESCRIPTION,
                            SAQTSV.PAR_SERVICE_ID,
                            SAQTSV.PAR_SERVICE_RECORD_ID,
                            SAQFEQ.TECHNOLOGY,
                            SAQTSV.CONTRACT_VALID_FROM as CONTRACT_VALID_FROM,
                            SAQTSV.CONTRACT_VALID_TO as CONTRACT_VALID_TO,
                            SAQFEQ.TEMP_TOOL,
                            SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID as QTEREVFEQ_RECORD_ID,
                            MAEQUP.TOOL_CONFIGURATION as TOOL_CONFIG,
                            SAQFEQ.IBASE_ATTSTS,
                            SAQFEQ.DEVICE_NODE,
                            '{UserName}' AS CPQTABLEENTRYADDEDBY,
                            GETDATE() as CPQTABLEENTRYDATEADDED,
                            {UserId} as CpqTableEntryModifiedBy,
                            GETDATE() as CpqTableEntryDateModified
                            FROM SAQFEQ (NOLOCK) JOIN SAQTSV (NOLOCK) ON
                            SAQFEQ.QUOTE_ID = SAQTSV.QUOTE_ID AND
                            SAQTSV.SERVICE_ID = '{TreeParam}' AND
                            SAQTSV.SERVICE_TYPE = '{TreeParentParam}'
                            LEFT JOIN SAQSCO(NOLOCK) ON SAQSCO.EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID AND SAQSCO.TEMP_TOOL = SAQFEQ.TEMP_TOOL AND SAQSCO.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID AND SAQSCO.QUOTE_RECORD_ID=SAQFEQ.QUOTE_RECORD_ID AND SAQSCO.QTEREVFEQ_RECORD_ID = SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID AND SAQSCO.TEMP_TOOL = 'False' AND SAQSCO.SERVICE_ID ='{TreeParam}'
                            JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID=SAQFEQ.QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID
                            JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQFEQ.EQUIPMENT_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID  AND SYSPBT.QTEREV_RECORD_ID=SAQTSV.QTEREV_RECORD_ID AND SYSPBT.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID = SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID
                            JOIN MAEQUP (NOLOCK) ON MAEQUP.EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID {eqp_where}
                            WHERE 
                            SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQFEQ.QTEREV_RECORD_ID = '{RevisionRecordId}'
                            AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND  (SAQFEQ.TEMP_TOOL = 'False' or SAQFEQ.TEMP_TOOL IS NULL) AND ISNULL(SAQSCO.EQUIPMENT_RECORD_ID,'')='')A                       
                    """.format(
                            TreeParam=self.tree_param,
                            TreeParentParam=self.tree_parent_level_0,
                            QuoteRecordId=self.contract_quote_record_id,
                            RevisionRecordId=self.quote_revision_record_id,
                            BatchGroupRecordId=kwargs.get('batch_group_record_id'),
                            UserName=self.user_name,
                            eqp_where = eqp_where,
                            UserId=self.user_id,
                            account_id=self.account_id,
                            account_name=self.account_name,
                            account_record_id=self.account_record_id,
                            RelocationEqType=self.tree_param if self.tree_parent_level_1 == 'Complementary Products' else ''
                        )
                )
                
            #INC08761336 M
            #INC08834775 - Start - M
            self._process_query(
            """
                INSERT SAQSCO (
                    QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
                    EQUIPMENT_ID,
                    EQUIPMENT_RECORD_ID,
                    EQUIPMENT_DESCRIPTION,
                    FABLOCATION_ID,
                    FABLOCATION_NAME,
                    FABLOCATION_RECORD_ID,
                    WAFER_SIZE,
                    SALESORG_ID,
                    SALESORG_NAME,
                    SALESORG_RECORD_ID,
                    SERIAL_NO,
                    QUOTE_RECORD_ID,
                    QUOTE_ID,
                    QUOTE_NAME,
                    ACCOUNT_ID,
                    ACCOUNT_NAME,
                    ACCOUNT_RECORD_ID,
                    QTEREV_ID,
                    QTEREV_RECORD_ID,
                    KPU,
                    RELOCATION_EQUIPMENT_TYPE,
                    SERVICE_ID,
                    SERVICE_TYPE,
                    SERVICE_DESCRIPTION,
                    SERVICE_RECORD_ID,
                    EQUIPMENT_STATUS,
                    EQUIPMENTCATEGORY_ID,
                    EQUIPMENTCATEGORY_DESCRIPTION,
                    EQUIPMENTCATEGORY_RECORD_ID,
                    PLATFORM,
                    GREENBOOK,
                    GREENBOOK_RECORD_ID,
                    MNT_PLANT_RECORD_ID,
                    MNT_PLANT_NAME,
                    MNT_PLANT_ID,
                    WARRANTY_START_DATE,
                    WARRANTY_END_DATE,
                    CUSTOMER_TOOL_ID,
                    PAR_SERVICE_DESCRIPTION,
                    PAR_SERVICE_ID,
                    PAR_SERVICE_RECORD_ID,
                    TECHNOLOGY,
                    CONTRACT_VALID_FROM,
                    CONTRACT_VALID_TO,
                    TEMP_TOOL,
                    QTEREVFEQ_RECORD_ID,
                    TOOL_CONFIG,
                    IBASE_ATTSTS,
                    DEVICE_NODE,
                    CPQTABLEENTRYADDEDBY,
                    CPQTABLEENTRYDATEADDED,
                    CpqTableEntryModifiedBy,
                    CpqTableEntryDateModified
                    ) SELECT CONVERT(VARCHAR(100),NEWID()) AS QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,A.*  FROM (SELECT
                        DISTINCT
                        SAQFEQ.EQUIPMENT_ID,
                        SAQFEQ.EQUIPMENT_RECORD_ID,
                        SAQFEQ.EQUIPMENT_DESCRIPTION,                                
                        SAQFEQ.FABLOCATION_ID,
                        SAQFEQ.FABLOCATION_NAME,
                        SAQFEQ.FABLOCATION_RECORD_ID,
                        SAQFEQ.WAFER_SIZE,
                        SAQFEQ.SALESORG_ID,
                        SAQFEQ.SALESORG_NAME,
                        SAQFEQ.SALESORG_RECORD_ID,
                        SERIAL_NUMBER,
                        SAQFEQ.QUOTE_RECORD_ID,
                        SAQFEQ.QUOTE_ID,
                        SAQFEQ.QUOTE_NAME,
                        '{account_id}' as ACCOUNT_ID,
                        '{account_name}' as ACCOUNT_NAME,
                        '{account_record_id}' as ACCOUNT_RECORD_ID,
                        SAQFEQ.QTEREV_ID,
                        SAQFEQ.QTEREV_RECORD_ID,
                        SAQFEQ.KPU,
                        '{RelocationEqType}' AS RELOCATION_EQUIPMENT_TYPE,
                        '{TreeParam}' as SERVICE_ID,
                        '{TreeParentParam}' as SERVICE_TYPE,
                        SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
                        SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
                        SAQFEQ.EQUIPMENT_STATUS,
                        SAQFEQ.EQUIPMENTCATEGORY_ID,
                        SAQFEQ.EQUIPMENTCATEGORY_DESCRIPTION,
                        SAQFEQ.EQUIPMENTCATEGORY_RECORD_ID,
                        SAQFEQ.PLATFORM,
                        SAQFEQ.GREENBOOK,
                        SAQFEQ.GREENBOOK_RECORD_ID,
                        SAQFEQ.MNT_PLANT_RECORD_ID,
                        SAQFEQ.MNT_PLANT_NAME,
                        SAQFEQ.MNT_PLANT_ID,
                        CONVERT(varchar, SAQFEQ.WARRANTY_START_DATE) as WARRANTY_START_DATE,
                        CONVERT(varchar, SAQFEQ.WARRANTY_END_DATE) as WARRANTY_END_DATE,
                        SAQFEQ.CUSTOMER_TOOL_ID,
                        SAQTSV.PAR_SERVICE_DESCRIPTION,
                        SAQTSV.PAR_SERVICE_ID,
                        SAQTSV.PAR_SERVICE_RECORD_ID,
                        SAQFEQ.TECHNOLOGY,
                        SAQTSV.CONTRACT_VALID_FROM as CONTRACT_VALID_FROM,
                        SAQTSV.CONTRACT_VALID_TO as CONTRACT_VALID_TO,
                        SAQFEQ.TEMP_TOOL,
                        SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID as QTEREVFEQ_RECORD_ID,
                        MAEQUP.TOOL_CONFIGURATION as TOOL_CONFIG,
                        SAQFEQ.IBASE_ATTSTS,
                        SAQFEQ.DEVICE_NODE,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified
                        FROM SAQFEQ (NOLOCK) 
                        {join_cndtn}
                        JOIN SAQTSV (NOLOCK) ON
                        SAQFEQ.QUOTE_ID = SAQTSV.QUOTE_ID AND
                        SAQTSV.SERVICE_ID = '{TreeParam}' AND
                        SAQTSV.SERVICE_TYPE = '{TreeParentParam}' 
                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID=SAQFEQ.QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID
                        JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQFEQ.EQUIPMENT_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID  AND SYSPBT.QTEREV_RECORD_ID=SAQTSV.QTEREV_RECORD_ID AND SYSPBT.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID = SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID AND SAQTSV.SERVICE_ID = SYSPBT.SAP_PART_NUMBER
                        JOIN MAEQUP (NOLOCK) ON MAEQUP.EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID {eqp_where}
                        WHERE 
                        SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQFEQ.QTEREV_RECORD_ID = '{RevisionRecordId}'
                        AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SAQFEQ.TEMP_TOOL = 'True' {and_cndtn})A    
                """.format(
                        TreeParam=self.tree_param,
                        TreeParentParam=self.tree_parent_level_0,
                        QuoteRecordId=self.contract_quote_record_id,
                        RevisionRecordId=self.quote_revision_record_id,
                        BatchGroupRecordId=kwargs.get('batch_group_record_id'),
                        UserName=self.user_name,
                        eqp_where = eqp_where,
                        UserId=self.user_id,
                        account_id=self.account_id,
                        account_name=self.account_name,
                        account_record_id=self.account_record_id,
                        RelocationEqType=self.tree_param if self.tree_parent_level_1 == 'Complementary Products' else '',
						join_cndtn = " INNER JOIN SAQFEQ_INBOUND (NOLOCK) ON SAQFEQ_INBOUND.EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID AND SAQFEQ_INBOUND.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID AND SAQFEQ_INBOUND.QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SAQFEQ_INBOUND.TMPTOL_SEQ  = SAQFEQ.TMPTOL_SEQ AND SAQFEQ_INBOUND.SERVICE_ID = '{}' ".format(self.tree_param) if self.trigger_from == 'python_script' else '',
						and_cndtn = " AND SAQFEQ_INBOUND.SERVICE_ID ='{}' ".format(self.tree_param) if self.trigger_from == 'python_script' else ''
                    )
            )
            #INC08834775 - End - M
            self._process_query("""DELETE FROM SAQFEQ_INBOUND WHERE QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{TreeParam}'""".format(contract_quote_record_id = self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam = self.tree_param))
            #INC08761336 M
        #A055S000P01-20807 M 
        getToolIdling = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQTDA (NOLOCK) WHERE TOOLIDLING_DISPLAY_VALUE ='Yes' AND TOOLIDLING_ID = 'Idling Allowed' and QUOTE_RECORD_ID = '{}' and QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id))
        #INC08942741 M
        getToolIdlingValue = Sql.GetFirst("SELECT ISNULL(IDLING_ALLOWED,'No') AS IDLING_ALLOWED FROM SAQTSE(NOLOCK) WHERE QUOTE_RECORD_ID = '{}' and QTEREV_RECORD_ID = '{}' AND ISNULL(IDLING_ALLOWED,'No') = 'Yes'".format(self.contract_quote_record_id,self.quote_revision_record_id))
        #INC08942741 M
        toolIdlingVal = ""
        if getToolIdlingValue:
            toolIdlingVal = getToolIdlingValue.IDLING_ALLOWED


        if getToolIdling is None and toolIdlingVal == "Yes":

            getPRTIAV = Sql.GetList("SELECT PRTIDA.TOOLIDLING_ID,PRTIDA.DISPLAY_ORDER,PRTIAV.TOOLIDLING_NAME,PRTIAV.TOOLIDLING_VALUE_CODE,PRTIAV.TOOLIDLING_DISPLAY_VALUE FROM PRTIAV (NOLOCK) JOIN PRTIDA (NOLOCK) ON PRTIAV.TOOLIDLING_ID = PRTIDA.TOOLIDLING_ID WHERE PRTIDA.TOOLIDLING_ID != 'Idling Allowed' AND [DEFAULT] = 1 AND PRTIDA.DISPLAY_ORDER%5 =0")
            VALUES = {}
            VALUES["Idling Allowed"] = "Yes"
            for x in getPRTIAV:
                VALUES[x.TOOLIDLING_ID] = x.TOOLIDLING_VALUE_CODE
            for x,y in VALUES.items():

                Sql.RunQuery(""" INSERT SAQTDA(
                    QUOTE_REV_TOOL_IDLING_ATTR_VAL_RECORD_ID,
                    QUOTE_ID,
                    QUOTE_RECORD_ID,
                    QTEREV_ID,
                    QTEREV_RECORD_ID,
                    TOLIDLVAL_RECORD_ID,
                    TOOLIDLING_DISPLAY_VALUE,
                    TOOLIDLING_ID,
                    TOOLIDLING_NAME,
                    TOOLIDLING_RECORD_ID,
                    TOOLIDLING_VALUE_CODE,
                    CPQTABLEENTRYADDEDBY,
                    CPQTABLEENTRYDATEADDED
                    ) SELECT 
                    CONVERT(VARCHAR(4000),NEWID()),
                    '{}' AS QUOTE_ID,
                    '{}' AS QUOTE_RECORD_ID,
                    '{}' AS QTEREV_ID,
                    '{}' AS QTEREV_RECORD_ID,
                    PRTIAV.TOLIDLATTVAL_RECORD_ID,
                    PRTIAV.TOOLIDLING_DISPLAY_VALUE,
                    PRTIAV.TOOLIDLING_ID,
                    PRTIAV.TOOLIDLING_NAME,
                    PRTIAV.TOOLIDLING_RECORD_ID,
                    PRTIAV.TOOLIDLING_VALUE_CODE,
                    '{}' AS CPQTABLEENTRYADDEDBY,
                    GETDATE() AS CPQTABLEENTRYDATEADDED
                    FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_VALUE_CODE = '{}' AND TOOLIDLING_ID = '{}'
                    """.format(self.contract_quote_id,self.contract_quote_record_id,self.quote_revision_id,self.quote_revision_record_id,User.UserName,y,x))       
        #A055S000P01-20807 M 




        getdate = Sql.GetFirst("select CONTRACT_VALID_FROM,CONTRACT_VALID_TO from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"'")
        #get_warrent_dates= SqlHelper.GetList("select QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,WARRANTY_END_DATE_ALERT,WARRANTY_START_DATE,WARRANTY_END_DATE from SAQSCO where QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' ")
        update_warranty_enddate_alert = ''
        warrant_enddat_alert_update = SqlHelper.GetFirst("sp_executesql @T=N'update B SET B.WARRANTY_END_DATE_ALERT = (CASE WHEN B.WARRANTY_END_DATE >= A.CONTRACT_VALID_FROM AND B.WARRANTY_END_DATE <=A.CONTRACT_VALID_TO THEN 1 ELSE 0 END) FROM SAQTMT A JOIN SAQSCO B ON A.MASTER_TABLE_QUOTE_RECORD_ID=B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID=B.QTEREV_RECORD_ID WHERE A.MASTER_TABLE_QUOTE_RECORD_ID = ''"+str(self.contract_quote_record_id)+"'' AND A.QTEREV_RECORD_ID = ''"+str(self.quote_revision_record_id)+"'' AND B.WARRANTY_END_DATE >= A.CONTRACT_VALID_FROM and B.WARRANTY_END_DATE <=A.CONTRACT_VALID_TO '")
            # get_warrent_dates= SqlHelper.GetList("SELECT B.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,B.WARRANTY_END_DATE_ALERT,B.WARRANTY_END_DATE FROM SAQTMT A JOIN SAQSCO B ON A.MASTER_TABLE_QUOTE_RECORD_ID=B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID=B.QTEREV_RECORD_ID WHERE A.MASTER_TABLE_QUOTE_RECORD_ID =  '"+str(self.contract_quote_record_id)+"' AND A.QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND B.WARRANTY_END_DATE >= A.CONTRACT_VALID_FROM and B.WARRANTY_END_DATE <=A.CONTRACT_VALID_TO")
            # for val in get_warrent_dates:
            # 	update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 1 where QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' and QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
            # 	Sql.RunQuery(update_warranty_enddate_alert)
            # for val in get_warrent_dates:
            # 	if val.WARRANTY_END_DATE:
            # 		WARRANTY_val = datetime.datetime.strptime(str(val.WARRANTY_END_DATE), "%Y-%m-%d")
            # 		get_con_date = str(getdate.CONTRACT_VALID_FROM).split(" ")[0]
            # 		get_con_date = datetime.datetime.strptime(str(get_con_date), "%m/%d/%Y")
            # 		if WARRANTY_val > get_con_date:
            # 			update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 1 where QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' and QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
            # 		else:
            # 			update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 0 where QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' and  QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
            # 		Sql.RunQuery(update_warranty_enddate_alert)
            # 	else:
            # 		if WARRANTY_val > get_con_end_date:
            # 			update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 1 where QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' and QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
            # 		else:
            # 			update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 0 where QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' and QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
                #Sql.RunQuery(update_warranty_enddate_alert)
                #4393 end
                # if val.WARRANTY_START_DATE:
                # 	if val.WARRANTY_END_DATE >= get_contract_date.CONTRACT_VALID_FROM:
                # 		if val.WARRANTY_END_DATE:
                # 			if val.WARRANTY_END_DATE >= get_contract_date.CONTRACT_VALID_TO:
                # 				Trace.Write('QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID---'+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID))
                # 				update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 1 where QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
                # 		else:
                # 			update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 0 where QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
                # 			Trace.Write('no end date--')
                # 		Sql.RunQuery(update_warranty_enddate_alert)
        
    
    def _insert_quote_service_covered_assembly(self, **kwargs):
        #INC08701856 M
        self._process_query(
            """
                INSERT SAQSCA (
                    QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,
                    CPQTABLEENTRYADDEDBY,
                    CPQTABLEENTRYDATEADDED,
                    CpqTableEntryModifiedBy,
                    CpqTableEntryDateModified,
                    ASSEMBLY_ID,
                    ASSEMBLY_DESCRIPTION,
                    ASSEMBLY_RECORD_ID,
                    EQUIPMENT_ID,
                    EQUIPMENT_DESCRIPTION,
                    EQUIPMENT_RECORD_ID,
                    SERIAL_NUMBER,
                    INCLUDED,
                    GOT_CODE,
                    EQUIPMENTCATEGORY_ID,
                    EQUIPMENTCATEGORY_DESCRIPTION,
                    EQUIPMENTCATEGORY_RECORD_ID,
                    ASSEMBLY_STATUS,
                    WARRANTY_START_DATE,
                    WARRANTY_END_DATE,
                    EQUIPMENTTYPE_ID,
                    EQUIPMENTTYPE_DESCRIPTION,
                    EQUIPMENTTYPE_RECORD_ID,
                    QUOTE_ID,
                    QUOTE_NAME,
                    QUOTE_RECORD_ID,
                    QTEREV_ID,
                    QTEREV_RECORD_ID,
                    SERVICE_ID,
                    SERVICE_DESCRIPTION,
                    SERVICE_RECORD_ID,
                    FABLOCATION_ID,
                    FABLOCATION_RECORD_ID,
                    FABLOCATION_NAME,
                    SALESORG_ID,
                    SALESORG_NAME,
                    SALESORG_RECORD_ID,
                    MNT_PLANT_ID,
                    MNT_PLANT_RECORD_ID,
                    GREENBOOK,
                    GREENBOOK_RECORD_ID,
                    PAR_SERVICE_DESCRIPTION,
                    PAR_SERVICE_ID,
                    PAR_SERVICE_RECORD_ID,
                    CONTRACT_VALID_FROM,
                    CONTRACT_VALID_TO,
                    QTESRVCOB_RECORD_ID
                    ) SELECT
                    CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,
                    '{UserName}' AS CPQTABLEENTRYADDEDBY,
                    GETDATE() as CPQTABLEENTRYDATEADDED,
                    {UserId} as CpqTableEntryModifiedBy,
                    GETDATE() as CpqTableEntryDateModified,
                    SAQFEA.ASSEMBLY_ID,
                    SAQFEA.ASSEMBLY_DESCRIPTION,
                    SAQFEA.ASSEMBLY_RECORD_ID,
                    SAQFEA.EQUIPMENT_ID,
                    SAQFEA.EQUIPMENT_DESCRIPTION,
                    SAQFEA.EQUIPMENT_RECORD_ID,
                    SAQFEA.SERIAL_NUMBER,
                    SAQFEA.INCLUDED,
                    SAQFEA.GOT_CODE,
                    SAQFEA.EQUIPMENTCATEGORY_ID,
                    SAQFEA.EQUIPMENTCATEGORY_DESCRIPTION,
                    SAQFEA.EQUIPMENTCATEGORY_RECORD_ID,
                    SAQFEA.ASSEMBLY_STATUS,
                    SAQFEA.WARRANTY_START_DATE,
                    SAQFEA.WARRANTY_END_DATE,
                    SAQFEA.EQUIPMENTTYPE_ID,
                    SAQFEA.EQUIPMENTTYPE_DESCRIPTION,
                    SAQFEA.EQUIPMENTTYPE_RECORD_ID,
                    SAQFEA.QUOTE_ID,
                    SAQFEA.QUOTE_NAME,
                    SAQFEA.QUOTE_RECORD_ID,
                    SAQFEA.QTEREV_ID,
                    SAQFEA.QTEREV_RECORD_ID,
                    '{TreeParam}' as SERVICE_ID,
                    SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
                    SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
                    SAQFEA.FABLOCATION_ID,
                    SAQFEA.FABLOCATION_RECORD_ID,
                    SAQFEA.FABLOCATION_NAME,
                    SAQFEA.SALESORG_ID,
                    SAQFEA.SALESORG_NAME,
                    SAQFEA.SALESORG_RECORD_ID,
                    SAQFEA.MNT_PLANT_ID,
                    SAQFEA.MNT_PLANT_RECORD_ID,
                    SAQSCO.GREENBOOK,
                    SAQSCO.GREENBOOK_RECORD_ID,
                    SAQTSV.PAR_SERVICE_DESCRIPTION,
                    SAQTSV.PAR_SERVICE_ID,
                    SAQTSV.PAR_SERVICE_RECORD_ID,
                    SAQSCO.CONTRACT_VALID_FROM,
                    SAQSCO.CONTRACT_VALID_TO,
                    SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID
                    FROM SYSPBT (NOLOCK)
                    JOIN (select SAQFEA.*,SYSPBT.BATCH_GROUP_RECORD_ID,SYSPBT.CpqTableEntryId as cpqid from SAQFEA(nolock) join SYSPBT (nolock) on SAQFEA.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID and SAQFEA.QTEREV_RECORD_ID = SYSPBT.QTEREV_RECORD_ID and SAQFEA.EQUIPMENT_RECORD_ID = SYSPBT.BATCH_RECORD_ID AND SAQFEA.QTEREVFEQ_RECORD_ID = SYSPBT.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID where  SAQFEA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQFEA.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' ) SAQFEA ON SAQFEA.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQFEA.EQUIPMENT_RECORD_ID = SYSPBT.BATCH_RECORD_ID AND SAQFEA.QTEREV_RECORD_ID = SYSPBT.QTEREV_RECORD_ID AND SAQFEA.cpqid = SYSPBT.CpqTableEntryId
                    JOIN SAQTSV (NOLOCK) ON SAQFEA.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID  AND SAQFEA.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID
                    JOIN SAQSCO (NOLOCK) ON SAQFEA.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQFEA.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID AND SAQFEA.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND SAQTSV.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQFEA.GREENBOOK = SAQSCO.GREENBOOK AND SAQFEA.QTEREVFEQ_RECORD_ID = SAQSCO.QTEREVFEQ_RECORD_ID
                    WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND  SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID = '{TreeParam}' AND SAQTSV.SERVICE_TYPE = '{TreeParentParam}'
                """.format( 
                UserId=self.user_id,
                UserName=self.user_name,
                TreeParam=self.tree_param,
                TreeParentParam=self.tree_parent_level_0,
                QuoteRecordId=self.contract_quote_record_id,
                RevisionRecordId=self.quote_revision_record_id,
                BatchGroupRecordId=kwargs.get('batch_group_record_id'),
                included = 1 if self.tree_param  == 'Sending Equipment' else "''"
            )
        )
        #INC08701856 M
        #if self.tree_param in ("Z0009","Z0010","Z0128") and kwargs.get('quotetype_value_for_offering').upper() != "TOOL BASED":
        #INC08621345 - Start - M
        # if self.tree_param:##A055S000P01-18658 code starts... calling the script to receive and update Real Time Event/KIT for the quote..
        #     self.entitlement_level = self.entitlement_level if self.entitlement_level else "OFFERING LEVEL"
        #     self.entitlement_level_value = self.entitlement_level_value if self.entitlement_level_value else self.tree_param
        #     ScriptExecutor.ExecuteGlobal('QTPOSTPKIT',{'QUOTE_ID':str(self.contract_quote_id),'REVISION_ID':str(self.quote_revision_id),'LEVEL':str(kwargs.get('entitlement_level')),'VALUE': str(kwargs.get('entitlement_level_value'))})
        #     #INC08621140,INC08638619 - Start - A
        #     Sql.RunQuery("""UPDATE MAEAPM_INBOUND SET PM_LEVEL = 'Scheduled Maintenance' where QUOTE_ID = '{}' AND QTEREV_ID ='{}' and PM_LEVEL = 'Sched Maint'""".format(self.contract_quote_id, self.quote_revision_id))
        #     #INC08621140,INC08638619 - End - A
        ##A055S000P01-18658 code ends...
        #INC08621345 - End - M
        if self.sale_type == 'TOOL RELOCATION' and self.tree_param == "Sending Equipment":			
            self._process_query(
                """
                    INSERT SAQSSA (
                        QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED,
                        CpqTableEntryModifiedBy,
                        CpqTableEntryDateModified,
                        SND_ASSEMBLY_ID,
                        SND_ASSEMBLY_DESCRIPTION,
                        SND_ASSEMBLY_RECORD_ID,
                        SND_EQUIPMENT_ID,
                        SND_EQUIPMENT_DESCRIPTION,
                        SND_EQUIPMENT_RECORD_ID,
                        GOT_CODE,
                        EQUIPMENTCATEGORY_ID,
                        EQUIPMENTCATEGORY_DESCRIPTION,
                        EQUIPMENTCATEGORY_RECORD_ID,
                        ASSEMBLY_STATUS,
                        EQUIPMENTTYPE_ID,
                        EQUIPMENTTYPE_DESCRIPTION,
                        EQUIPMENTTYPE_RECORD_ID,
                        QUOTE_ID,
                        QUOTE_NAME,
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        SERVICE_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_RECORD_ID,
                        SNDFBL_ID,
                        SNDFBL_NAME,
                        SNDFBL_RECORD_ID,
                        ADDUSR_RECORD_ID,
                        QTESRV_RECORD_ID,
                        SNDACC_ID,
                        SNDACC_NAME,
                        SNDACC_RECORD_ID,
                        MODUSR_RECORD_ID,
                        QTESNDEQP_RECORD_ID,
                        GREENBOOK,
                        GREENBOOK_RECORD_ID,
                        INCLUDED
                        ) SELECT
                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified,
                        SAQFEA.ASSEMBLY_ID,
                        SAQFEA.ASSEMBLY_DESCRIPTION,
                        SAQFEA.ASSEMBLY_RECORD_ID,
                        SAQFEA.EQUIPMENT_ID,
                        SAQFEA.EQUIPMENT_DESCRIPTION,
                        SAQFEA.EQUIPMENT_RECORD_ID,
                        
                        SAQFEA.GOT_CODE,
                        SAQFEA.EQUIPMENTCATEGORY_ID,
                        SAQFEA.EQUIPMENTCATEGORY_DESCRIPTION,
                        SAQFEA.EQUIPMENTCATEGORY_RECORD_ID,
                        SAQFEA.ASSEMBLY_STATUS,
                        
                        SAQFEA.EQUIPMENTTYPE_ID,
                        SAQFEA.EQUIPMENTTYPE_DESCRIPTION,
                        SAQFEA.EQUIPMENTTYPE_RECORD_ID,
                        SAQFEA.QUOTE_ID,
                        SAQFEA.QUOTE_NAME,
                        SAQFEA.QUOTE_RECORD_ID,
                        SAQFEA.QTEREV_ID,
                        SAQFEA.QTEREV_RECORD_ID,
                        SAQSSE.SERVICE_ID,
                        SAQSSE.SERVICE_DESCRIPTION,
                        SAQSSE.SERVICE_RECORD_ID,
                        SAQSSE.SNDFBL_ID as FABLOCATION_ID,
                        SAQSSE.SNDFBL_NAME as FABLOCATION_NAME,
                        SAQSSE.SNDFBL_RECORD_ID as FABLOCATION_RECORD_ID,
                        SAQFEA.ADDUSR_RECORD_ID,
                        SAQSSE.QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID,
                        SAQFEA.SRCACC_ID,
                        SAQFEA.SRCACC_NAME,
                        SAQFEA.SRCACC_RECORD_ID,
                        '' as MODUSR_RECORD_ID,
                        '' as QTESNDEQP_RECORD_ID,
                        '' as GREENBOOK,
                        '' as GREENBOOK_RECORD_ID,
                        1
                        FROM SAQFEA (NOLOCK)
                        JOIN SAQSSE (NOLOCK) ON SAQFEA.QUOTE_RECORD_ID = SAQSSE.QUOTE_RECORD_ID AND SAQFEA.EQUIPMENT_ID = SAQSSE.SND_EQUIPMENT_ID AND SAQFEA.QTEREV_RECORD_ID = SAQSSE.QTEREV_RECORD_ID
                        WHERE  SAQSSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSSE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSSE.SERVICE_ID = '{TreeParentParam}'
                    """.format(
                    UserId=self.user_id,
                    UserName=self.user_name,
                    TreeParentParam=self.tree_parent_level_0,
                    QuoteRecordId=self.contract_quote_record_id,
                    RevisionRecordId=self.quote_revision_record_id
                    
                )
            )
            # self._process_query(
            # 	"""
            # 		INSERT SAQSSA (
            # 			QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,
            # 			CPQTABLEENTRYADDEDBY,
            # 			CPQTABLEENTRYDATEADDED,
            # 			CpqTableEntryModifiedBy,
            # 			CpqTableEntryDateModified,
            # 			SND_ASSEMBLY_ID,
            # 			SND_ASSEMBLY_DESCRIPTION,
            # 			SND_ASSEMBLY_RECORD_ID,
            # 			SND_EQUIPMENT_ID,
            # 			SND_EQUIPMENT_DESCRIPTION,
            # 			SND_EQUIPMENT_RECORD_ID,
            # 			GOT_CODE,
            # 			EQUIPMENTCATEGORY_ID,
            # 			EQUIPMENTCATEGORY_DESCRIPTION,
            # 			EQUIPMENTCATEGORY_RECORD_ID,
            # 			ASSEMBLY_STATUS,
            # 			EQUIPMENTTYPE_ID,
            # 			EQUIPMENTTYPE_DESCRIPTION,
            # 			EQUIPMENTTYPE_RECORD_ID,
            # 			QUOTE_ID,
            # 			QUOTE_NAME,
            # 			QUOTE_RECORD_ID,
            # 			SERVICE_ID,
            # 			SERVICE_DESCRIPTION,
            # 			SERVICE_RECORD_ID,
            # 			SNDFBL_ID,
            # 			SNDFBL_NAME,
            # 			SNDFBL_RECORD_ID,
            # 			ADDUSR_RECORD_ID,
            # 			QTESRV_RECORD_ID,
            # 			SNDACC_ID,
            # 			SNDACC_NAME,
            # 			SNDACC_RECORD_ID,
            # 			MODUSR_RECORD_ID,
            # 			QTESNDEQP_RECORD_ID,
            # 			GREENBOOK,
            # 			GREENBOOK_RECORD_ID
            # 			) SELECT
            # 			CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,
            # 			'{UserName}' AS CPQTABLEENTRYADDEDBY,
            # 			GETDATE() as CPQTABLEENTRYDATEADDED,
            # 			{UserId} as CpqTableEntryModifiedBy,
            # 			GETDATE() as CpqTableEntryDateModified,
            # 			SAQSCA.ASSEMBLY_ID,
            # 			SAQSCA.ASSEMBLY_DESCRIPTION,
            # 			SAQSCA.ASSEMBLY_RECORD_ID,
            # 			SAQSCA.EQUIPMENT_ID,
            # 			SAQSCA.EQUIPMENT_DESCRIPTION,
            # 			SAQSCA.EQUIPMENT_RECORD_ID,
            # 			SAQSCA.GOT_CODE,
            # 			SAQSCA.EQUIPMENTCATEGORY_ID,
            # 			SAQSCA.EQUIPMENTCATEGORY_DESCRIPTION,
            # 			SAQSCA.EQUIPMENTCATEGORY_RECORD_ID,
            # 			SAQSCA.ASSEMBLY_STATUS,
            # 			SAQSCA.EQUIPMENTTYPE_ID,
            # 			SAQSCA.EQUIPMENTTYPE_DESCRIPTION,
            # 			SAQSCA.EQUIPMENTTYPE_RECORD_ID,
            # 			SAQSCA.QUOTE_ID,
            # 			SAQSCA.QUOTE_NAME,
            # 			SAQSCA.QUOTE_RECORD_ID,
            # 			SAQSCA.SERVICE_ID,
            # 			SAQSCA.SERVICE_DESCRIPTION,
            # 			SAQSCA.SERVICE_RECORD_ID,
            # 			SAQSCA.FABLOCATION_ID,
            # 			SAQSCA.FABLOCATION_NAME,
            # 			SAQSCA.FABLOCATION_RECORD_ID,
            # 			SAQSCA.ADDUSR_RECORD_ID,
            # 			SAQSCO.QTESRV_RECORD_ID,
            # 			SAQSCO.SNDACC_ID,
            # 			SAQSCO.SNDACC_NAME,
            # 			SAQSCO.SNDACC_RECORD_ID,
            # 			'' as MODUSR_RECORD_ID,
            # 			'' as QTESNDEQP_RECORD_ID,
            # 			SAQSCA.GREENBOOK,
            # 			SAQSCA.GREENBOOK_RECORD_ID
            # 			FROM SYSPBT (NOLOCK)
            # 			JOIN (select SAQSCA.* from SAQSCA(nolock) join SYSPBT (nolock) on SAQSCA.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID and SAQSCA.EQUIPMENT_RECORD_ID = SYSPBT.BATCH_RECORD_ID where  SAQSCA.QUOTE_RECORD_ID = '{QuoteRecordId}' ) SAQSCA ON SAQSCA.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQSCA.EQUIPMENT_RECORD_ID = SYSPBT.BATCH_RECORD_ID
            # 			JOIN SAQSCO (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCA.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID
            # 			WHERE SAQSCO.RELOCATION_EQUIPMENT_TYPE ='Receiving Equipment' AND SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SAQSCA.SERVICE_ID = '{TreeParam}' AND SAQSCO.SERVICE_TYPE = '{TreeParentParam}'
            # 		""".format(
            # 		UserId=self.user_id,
            # 		UserName=self.user_name,
            # 		TreeParam=self.tree_param if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_0,
            # 		TreeParentParam=self.tree_parent_level_0 if self.tree_parent_level_0 == 'Comprehensive Services' else self.tree_parent_level_1,
            # 		QuoteRecordId=self.contract_quote_record_id,
            # 		BatchGroupRecordId=kwargs.get('batch_group_record_id')
            # 	)
            # )
            # self._process_query(
            # 	"""
            # 		INSERT SAQSSA (
            # 			QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,
            # 			CPQTABLEENTRYADDEDBY,
            # 			CPQTABLEENTRYDATEADDED,
            # 			CpqTableEntryModifiedBy,
            # 			CpqTableEntryDateModified,
            # 			SND_ASSEMBLY_ID,
            # 			SND_ASSEMBLY_DESCRIPTION,
            # 			SND_ASSEMBLY_RECORD_ID,
            # 			SND_EQUIPMENT_ID,
            # 			SND_EQUIPMENT_DESCRIPTION,
            # 			SND_EQUIPMENT_RECORD_ID,
            # 			GOT_CODE,
            # 			EQUIPMENTCATEGORY_ID,
            # 			EQUIPMENTCATEGORY_DESCRIPTION,
            # 			EQUIPMENTCATEGORY_RECORD_ID,
            # 			ASSEMBLY_STATUS,
            # 			EQUIPMENTTYPE_ID,
            # 			EQUIPMENTTYPE_DESCRIPTION,
            # 			EQUIPMENTTYPE_RECORD_ID,
            # 			QUOTE_ID,
            # 			QUOTE_NAME,
            # 			QUOTE_RECORD_ID,
            # 			SERVICE_ID,
            # 			SERVICE_DESCRIPTION,
            # 			SERVICE_RECORD_ID,
            # 			SNDFBL_ID,
            # 			SNDFBL_NAME,
            # 			SNDFBL_RECORD_ID,
            # 			ADDUSR_RECORD_ID,
            # 			QTESRV_RECORD_ID,
            # 			SNDACC_ID,
            # 			SNDACC_NAME,
            # 			SNDACC_RECORD_ID,
            # 			MODUSR_RECORD_ID,
            # 			QTESNDEQP_RECORD_ID,
            # 			GREENBOOK,
            # 			GREENBOOK_RECORD_ID
            # 			) SELECT
            # 			CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,
            # 			'{UserName}' AS CPQTABLEENTRYADDEDBY,
            # 			GETDATE() as CPQTABLEENTRYDATEADDED,
            # 			{UserId} as CpqTableEntryModifiedBy,
            # 			GETDATE() as CpqTableEntryDateModified,
            # 			SAQSCA.ASSEMBLY_ID,
            # 			SAQSCA.ASSEMBLY_DESCRIPTION,
            # 			SAQSCA.ASSEMBLY_RECORD_ID,
            # 			SAQSCA.EQUIPMENT_ID,
            # 			SAQSCA.EQUIPMENT_DESCRIPTION,
            # 			SAQSCA.EQUIPMENT_RECORD_ID,
            # 			SAQSCA.GOT_CODE,
            # 			SAQSCA.EQUIPMENTCATEGORY_ID,
            # 			SAQSCA.EQUIPMENTCATEGORY_DESCRIPTION,
            # 			SAQSCA.EQUIPMENTCATEGORY_RECORD_ID,
            # 			SAQSCA.ASSEMBLY_STATUS,
            # 			SAQSCA.EQUIPMENTTYPE_ID,
            # 			SAQSCA.EQUIPMENTTYPE_DESCRIPTION,
            # 			SAQSCA.EQUIPMENTTYPE_RECORD_ID,
            # 			SAQSCA.QUOTE_ID,
            # 			SAQSCA.QUOTE_NAME,
            # 			SAQSCA.QUOTE_RECORD_ID,
            # 			SAQSCA.SERVICE_ID,
            # 			SAQSCA.SERVICE_DESCRIPTION,
            # 			SAQSCA.SERVICE_RECORD_ID,
            # 			SAQSCA.FABLOCATION_ID,
            # 			SAQSCA.FABLOCATION_NAME,
            # 			SAQSCA.FABLOCATION_RECORD_ID,
            # 			SAQSCA.ADDUSR_RECORD_ID,
            # 			SAQSCO.QTESRV_RECORD_ID,
            # 			SAQSCO.SNDACC_ID,
            # 			SAQSCO.SNDACC_NAME,
            # 			SAQSCO.SNDACC_RECORD_ID,
            # 			'' as MODUSR_RECORD_ID,
            # 			'' as QTESNDEQP_RECORD_ID,
            # 			SAQSCA.GREENBOOK,
            # 			SAQSCA.GREENBOOK_RECORD_ID
            # 			FROM SAQSCA (NOLOCK)
            # 			JOIN SAQSCO (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCA.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID
            # 			WHERE SAQSCO.RELOCATION_EQUIPMENT_TYPE ='SENDING EQUIPMENT' AND SAQSCA.QUOTE_RECORD_ID = '{QuoteRecordId}'  AND SAQSCA.SERVICE_ID = '{TreeParam}' AND SAQSCO.SERVICE_TYPE = '{TreeParentParam}'
            # 		""".format(
            # 		UserId=self.user_id,
            # 		UserName=self.user_name,
            # 		TreeParam=self.tree_param if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_0,
            # 		TreeParentParam=self.tree_parent_level_0 if self.tree_parent_level_0 == 'Comprehensive Services' else self.tree_parent_level_1,
            # 		QuoteRecordId=self.contract_quote_record_id
                    
            # 	)
            # )

    def _insert_quote_service_fab_location(self, **kwargs):
        if self.sale_type == "TOOL RELOCATION" and self.tree_param == "Sending Equipment":
            # self._process_query(
            # 	"""INSERT SAQSFB(
            # 		FABLOCATION_ID,
            # 		FABLOCATION_NAME,
            # 		FABLOCATION_RECORD_ID,
            # 		SERVICE_ID,
            # 		SERVICE_TYPE,
            # 		SERVICE_DESCRIPTION,
            # 		SERVICE_RECORD_ID,
            # 		FABLOCATION_STATUS,
            # 		QUOTE_ID,
            # 		QUOTE_NAME,
            # 		QUOTE_RECORD_ID,
            # 		MNT_PLANT_ID,
            # 		MNT_PLANT_NAME,
            # 		MNT_PLANT_RECORD_ID,
            # 		ADDRESS_1,
            # 		ADDRESS_2,
            # 		CITY,
            # 		COUNTRY,
            # 		COUNTRY_RECORD_ID,
            # 		SALESORG_ID,
            # 		SALESORG_NAME,
            # 		SALESORG_RECORD_ID,
            # 		PAR_SERVICE_DESCRIPTION,
            # 		PAR_SERVICE_ID,
            # 		PAR_SERVICE_RECORD_ID,
            # 		QUOTE_SERVICE_FAB_LOCATION_RECORD_ID,
            # 		CPQTABLEENTRYADDEDBY,
            # 		CPQTABLEENTRYDATEADDED,
            # 		CpqTableEntryModifiedBy,
            # 		CpqTableEntryDateModified
            # 		) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_FAB_LOCATION_RECORD_ID,
            # 		'{UserName}' AS CPQTABLEENTRYADDEDBY,
            # 		GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy,
            # 		GETDATE() as CpqTableEntryDateModified FROM (
            # 		SELECT DISTINCT
            # 		SAQSCO.SNDFBL_ID,
            # 		SAQSCO.SNDFBL_NAME,
            # 		SAQSCO.SNDFBL_RECORD_ID,
            # 		SAQSCO.SERVICE_ID,
            # 		SAQSCO.SERVICE_TYPE,
            # 		SAQSCO.SERVICE_DESCRIPTION,
            # 		SAQSCO.SERVICE_RECORD_ID,
            # 		MAFBLC.STATUS,
            # 		SAQSCO.QUOTE_ID,
            # 		SAQSCO.QUOTE_NAME,
            # 		SAQSCO.QUOTE_RECORD_ID,
            # 		SAQSCO.MNT_PLANT_ID,
            # 		SAQSCO.MNT_PLANT_NAME,
            # 		SAQSCO.MNT_PLANT_RECORD_ID,
            # 		MAFBLC.ADDRESS_1,
            # 		MAFBLC.ADDRESS_2,
            # 		MAFBLC.CITY,
            # 		MAFBLC.COUNTRY,
            # 		MAFBLC.COUNTRY_RECORD_ID,
            # 		SAQSCO.SALESORG_ID,
            # 		SAQSCO.SALESORG_NAME,
            # 		SAQSCO.SALESORG_RECORD_ID,
            # 		SAQSCO.PAR_SERVICE_DESCRIPTION,
            # 		SAQSCO.PAR_SERVICE_ID,
            # 		SAQSCO.PAR_SERVICE_RECORD_ID
            # 		FROM SAQSCO (NOLOCK)
            # 		JOIN MAFBLC (NOLOCK) ON SAQSCO.SNDFBL_ID = MAFBLC.FAB_LOCATION_ID 
            # 		JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID
            # 		JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
            # 		WHERE SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND
            # 		SAQSCO.SERVICE_ID = '{TreeParam}' AND SAQSCO.SERVICE_TYPE = '{TreeParentParam}' AND NOT EXISTS(SELECT FABLOCATION_ID FROM SAQSFB WHERE SERVICE_ID = '{TreeParam}' AND QUOTE_RECORD_ID = '{QuoteRecordId}')
            # 		) FB""".format(
            # 						TreeParam=self.tree_param if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_0,
            # 						TreeParentParam=self.tree_parent_level_0 if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_1,
            # 						QuoteRecordId=self.contract_quote_record_id,
            # 						BatchGroupRecordId=kwargs.get('batch_group_record_id'),
            # 						UserId=self.user_id,
            # 						UserName=self.user_name,
            # 					)
            # 	)
            if self.tree_param == "Sending Equipment" and self.sale_type == "TOOL RELOCATION":
                self._process_query(
                    """INSERT SAQSSF(
                        SNDFBL_ID,
                        SNDFBL_NAME,
                        SNDACC_ID,
                        SNDACC_NAME,
                        SNDACC_RECORD_ID,
                        SNDFBL_RECORD_ID,
                        SERVICE_ID,					
                        SERVICE_DESCRIPTION,
                        SERVICE_RECORD_ID,
                        SNDFBL_STATUS,
                        QUOTE_ID,
                        QUOTE_NAME,
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        MNT_PLANT_ID,
                        MNT_PLANT_NAME,
                        MNT_PLANT_RECORD_ID,
                        ADDRESS_1,
                        ADDRESS_2,
                        CITY,
                        COUNTRY,
                        COUNTRY_RECORD_ID,
                        SALESORG_ID,
                        SALESORG_NAME,
                        SALESORG_RECORD_ID,					
                        QUOTE_SERVICE_SENDING_FAB_LOC_ID,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED,
                        CpqTableEntryModifiedBy,
                        CpqTableEntryDateModified
                        ) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_SENDING_FAB_LOC_ID,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified FROM (
                        SELECT DISTINCT
                        SAQSSE.SNDFBL_ID,
                        SAQSSE.SNDFBL_NAME,
                        SAQSSE.SNDACC_ID,
                        SAQSSE.SNDACC_NAME,
                        SAQSSE.SNDACC_RECORD_ID,
                        SAQSSE.SNDFBL_RECORD_ID,
                        SAQSSE.SERVICE_ID,					
                        SAQSSE.SERVICE_DESCRIPTION,
                        SAQSSE.SERVICE_RECORD_ID,
                        MAFBLC.STATUS,
                        SAQSSE.QUOTE_ID,
                        SAQSSE.QUOTE_NAME,
                        SAQSSE.QUOTE_RECORD_ID,
                        SAQSSE.QTEREV_ID,
                        SAQSSE.QTEREV_RECORD_ID,
                        SAQSSE.MNT_PLANT_ID,
                        SAQSSE.MNT_PLANT_NAME,
                        SAQSSE.MNT_PLANT_RECORD_ID,
                        MAFBLC.ADDRESS_1,
                        MAFBLC.ADDRESS_2,
                        MAFBLC.CITY,
                        MAFBLC.COUNTRY,
                        MAFBLC.COUNTRY_RECORD_ID,
                        SAQSSE.SALESORG_ID,
                        SAQSSE.SALESORG_NAME,
                        SAQSSE.SALESORG_RECORD_ID					
                        FROM SAQSSE (NOLOCK)
                        JOIN MAFBLC (NOLOCK) ON SAQSSE.SNDFBL_ID = MAFBLC.FAB_LOCATION_ID 
                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSSE.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSSE.QTEREV_RECORD_ID
                        JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQSSE.SND_EQUIPMENT_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQSSE.QTEREV_RECORD_ID
                        WHERE SAQSSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSSE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND
                        SAQSSE.SERVICE_ID = '{TreeParentParam}' AND SAQSSE.SNDFBL_ID NOT IN(SELECT SNDFBL_ID FROM SAQSSF (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{TreeParentParam}')
                        ) FB""".format(
                                        TreeParam=self.tree_param if (self.tree_parent_level_1 == 'Complementary Products') and self.sale_type == 'TOOL RELOCATION' else self.tree_parent_level_1,
                                        TreeParentParam=self.tree_parent_level_0 if (self.tree_parent_level_1 == 'Complementary Products') and self.sale_type == 'TOOL RELOCATION' else self.tree_parent_level_1,
                                        TreeSuperParentParam = self.tree_parent_level_1,
                                        QuoteRecordId=self.contract_quote_record_id,
                                        RevisionRecordId=self.quote_revision_record_id,
                                        BatchGroupRecordId=kwargs.get('batch_group_record_id'),
                                        UserId=self.user_id,
                                        UserName=self.user_name,
                                    )
                    )			
    
        else:
            Trace.Write("FAB REMOVAL -> SAQSFB NO INSERT")
            '''
            self._process_query(
                """INSERT SAQSFB(
                    FABLOCATION_ID,
                    FABLOCATION_NAME,
                    FABLOCATION_RECORD_ID,
                    SERVICE_ID,
                    SERVICE_TYPE,
                    SERVICE_DESCRIPTION,
                    SERVICE_RECORD_ID,
                    FABLOCATION_STATUS,
                    QUOTE_ID,
                    QUOTE_NAME,
                    QUOTE_RECORD_ID,
                    QTEREV_ID,
                    QTEREV_RECORD_ID,
                    MNT_PLANT_ID,
                    MNT_PLANT_NAME,
                    MNT_PLANT_RECORD_ID,
                    ADDRESS_1,
                    ADDRESS_2,
                    CITY,
                    COUNTRY,
                    COUNTRY_RECORD_ID,
                    SALESORG_ID,
                    SALESORG_NAME,
                    SALESORG_RECORD_ID,
                    CONTRACT_VALID_FROM,
                    CONTRACT_VALID_TO,
                    PAR_SERVICE_DESCRIPTION,
                    PAR_SERVICE_ID,
                    PAR_SERVICE_RECORD_ID,
                    QUOTE_SERVICE_FAB_LOCATION_RECORD_ID,
                    CPQTABLEENTRYADDEDBY,
                    CPQTABLEENTRYDATEADDED,
                    CpqTableEntryModifiedBy,
                    CpqTableEntryDateModified
                    ) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_FAB_LOCATION_RECORD_ID,
                    '{UserName}' AS CPQTABLEENTRYADDEDBY,
                    GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy,
                    GETDATE() as CpqTableEntryDateModified FROM (
                    SELECT DISTINCT
                    SAQSCO.FABLOCATION_ID,
                    SAQSCO.FABLOCATION_NAME,
                    SAQSCO.FABLOCATION_RECORD_ID,
                    SAQSCO.SERVICE_ID,
                    SAQSCO.SERVICE_TYPE,
                    SAQSCO.SERVICE_DESCRIPTION,
                    SAQSCO.SERVICE_RECORD_ID,
                    MAFBLC.STATUS,
                    SAQSCO.QUOTE_ID,
                    SAQSCO.QUOTE_NAME,
                    SAQSCO.QUOTE_RECORD_ID,
                    SAQSCO.QTEREV_ID,
                    SAQSCO.QTEREV_RECORD_ID,
                    SAQSCO.MNT_PLANT_ID,
                    SAQSCO.MNT_PLANT_NAME,
                    SAQSCO.MNT_PLANT_RECORD_ID,
                    MAFBLC.ADDRESS_1,
                    MAFBLC.ADDRESS_2,
                    MAFBLC.CITY,
                    MAFBLC.COUNTRY,
                    MAFBLC.COUNTRY_RECORD_ID,
                    SAQSCO.SALESORG_ID,
                    SAQSCO.SALESORG_NAME,
                    SAQSCO.SALESORG_RECORD_ID,
                    SAQTMT.CONTRACT_VALID_FROM,
                    SAQTMT.CONTRACT_VALID_TO,
                    SAQSCO.PAR_SERVICE_DESCRIPTION,
                    SAQSCO.PAR_SERVICE_ID,
                    SAQSCO.PAR_SERVICE_RECORD_ID
                    FROM SAQSCO (NOLOCK)
                    JOIN MAFBLC (NOLOCK) ON SAQSCO.FABLOCATION_ID = MAFBLC.FAB_LOCATION_ID 
                    JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
                    JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
                    WHERE SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}'  AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND
                    SAQSCO.SERVICE_ID = '{TreeParam}' AND SAQSCO.SERVICE_TYPE = '{TreeParentParam}' AND FABLOCATION_ID NOT IN (SELECT FABLOCATION_ID FROM SAQSFB WHERE SERVICE_ID = '{TreeParam}' AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}')
                    ) FB""".format(
                                    TreeParam=self.tree_param if (self.tree_parent_level_0.upper() == 'COMPREHENSIVE SERVICES' or self.tree_parent_level_0.upper() == 'COMPLEMENTARY PRODUCTS') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_0,
                                    TreeParentParam=self.tree_parent_level_0 if (self.tree_parent_level_0.upper() == 'COMPREHENSIVE SERVICES' or self.tree_parent_level_0.upper() == 'COMPLEMENTARY PRODUCTS') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_1,
                                    QuoteRecordId=self.contract_quote_record_id,
                                    RevisionRecordId=self.quote_revision_record_id,
                                    BatchGroupRecordId=kwargs.get('batch_group_record_id'),
                                    UserId=self.user_id,
                                    UserName=self.user_name,
                                )
                )
                '''
        
    def _insert_quote_service_greenbook(self, **kwargs):
        if self.sale_type == "TOOL RELOCATION":
            #INC08700058 - Start - M
                self._process_query(
                """
                    INSERT SAQSGB (
                        QUOTE_SERVICE_GREENBOOK_RECORD_ID,
                        GREENBOOK,
                        GREENBOOK_RECORD_ID,
                        QUOTE_ID,
                        QUOTE_NAME,
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        SALESORG_ID,
                        SALESORG_NAME,
                        SALESORG_RECORD_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_ID,
                        SERVICE_RECORD_ID,
                        EQUIPMENT_QUANTITY,
                        CONTRACT_VALID_FROM,
                        CONTRACT_VALID_TO,
                        UOM_ID,
                        PAR_SERVICE_DESCRIPTION,
                        PAR_SERVICE_ID,
                        PAR_SERVICE_RECORD_ID,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED,
                        CpqTableEntryModifiedBy,
                        CpqTableEntryDateModified
                        ) SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_RECORD_ID,A.* from (SELECT DISTINCT
                            SAQSCO.GREENBOOK,
                            SAQSCO.GREENBOOK_RECORD_ID,
                            SAQSCO.QUOTE_ID,
                            SAQSCO.QUOTE_NAME,
                            SAQSCO.QUOTE_RECORD_ID,
                            SAQSCO.QTEREV_ID,
                            SAQSCO.QTEREV_RECORD_ID,
                            SAQSCO.SALESORG_ID,
                            SAQSCO.SALESORG_NAME,
                            SAQSCO.SALESORG_RECORD_ID,
                            SAQSCO.SERVICE_DESCRIPTION,
                            SAQSCO.SERVICE_ID,
                            SAQSCO.SERVICE_RECORD_ID,
                            SAQSCO.EQUIPMENT_QUANTITY,								
                            SAQTMT.CONTRACT_VALID_FROM,
                            SAQTMT.CONTRACT_VALID_TO,
                            SAQTSV.UOM_ID,
                            SAQTSV.PAR_SERVICE_DESCRIPTION,
                            SAQTSV.PAR_SERVICE_ID,
                            SAQTSV.PAR_SERVICE_RECORD_ID,
                            '{UserName}' AS CPQTABLEENTRYADDEDBY,
                            GETDATE() as CPQTABLEENTRYDATEADDED,
                            {UserId} as CpqTableEntryModifiedBy,
                            GETDATE() as CpqTableEntryDateModified
                            FROM SAQSCO (NOLOCK) JOIN SAQTSV (NOLOCK) ON
                            SAQSCO.QUOTE_ID = SAQTSV.QUOTE_ID AND
                            SAQTSV.SERVICE_ID = '{TreeParam}' AND
                            SAQTSV.SERVICE_TYPE = '{TreeParentParam}'
                            JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
                            JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID
                            WHERE 
                            SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}'
                            AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}')A LEFT JOIN SAQSGB (NOLOCK) AS M ON A.QUOTE_RECORD_ID = M.QUOTE_RECORD_ID AND M.QTEREV_RECORD_ID = A.QTEREV_RECORD_ID AND M.SERVICE_ID = A.SERVICE_ID AND M.GREENBOOK = A.GREENBOOK WHERE M.QUOTE_RECORD_ID is null                  
                    """.format(
                            TreeParam=self.tree_param if (self.tree_parent_level_0.upper() == 'COMPREHENSIVE SERVICES' or self.tree_parent_level_0.upper() == 'COMPLEMENTARY PRODUCTS') and self.sale_type == 'TOOL RELOCATION' else self.tree_parent_level_0,
                            TreeParentParam=self.tree_parent_level_0 if (self.tree_parent_level_0.upper() == 'COMPREHENSIVE SERVICES' or self.tree_parent_level_0.upper() == 'COMPLEMENTARY PRODUCTS') and self.sale_type == 'TOOL RELOCATION' else self.tree_parent_level_1,
                            QuoteRecordId=self.contract_quote_record_id,
                            RevisionRecordId=self.quote_revision_record_id,
                            BatchGroupRecordId=kwargs.get('batch_group_record_id'),
                            UserName=self.user_name,
                            UserId=self.user_id
                        )
            )
                #INC08700058 - End - M
        else:
            #INC08700058,INC08778358  - Start - M
            self._process_query(
                """
                    INSERT SAQSGB (
                        QUOTE_SERVICE_GREENBOOK_RECORD_ID,
                        GREENBOOK,
                        GREENBOOK_RECORD_ID,
                        QUOTE_ID,
                        QUOTE_NAME,
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        SALESORG_ID,
                        SALESORG_NAME,
                        SALESORG_RECORD_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_ID,
                        SERVICE_RECORD_ID,
                        EQUIPMENT_QUANTITY,
                        CONTRACT_VALID_FROM,
                        CONTRACT_VALID_TO,
                        PAR_SERVICE_DESCRIPTION,
                        PAR_SERVICE_ID,
                        PAR_SERVICE_RECORD_ID,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED,
                        CpqTableEntryModifiedBy,
                        CpqTableEntryDateModified
                        ) SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_RECORD_ID,A.* from (SELECT DISTINCT
                            SAQSCO.GREENBOOK,
                            SAQSCO.GREENBOOK_RECORD_ID,
                            SAQSCO.QUOTE_ID,
                            SAQSCO.QUOTE_NAME,
                            SAQSCO.QUOTE_RECORD_ID,
                            SAQSCO.QTEREV_ID,
                            SAQSCO.QTEREV_RECORD_ID,
                            SAQSCO.SALESORG_ID,
                            SAQSCO.SALESORG_NAME,
                            SAQSCO.SALESORG_RECORD_ID,
                            SAQSCO.SERVICE_DESCRIPTION,
                            SAQSCO.SERVICE_ID,
                            SAQSCO.SERVICE_RECORD_ID,
                            SAQSCO.EQUIPMENT_QUANTITY,								
                            SAQTMT.CONTRACT_VALID_FROM,
                            SAQTMT.CONTRACT_VALID_TO,
                            SAQTSV.PAR_SERVICE_DESCRIPTION,
                            ISNULL(SAQTSV.PAR_SERVICE_ID,'') as PAR_SERVICE_ID,
                            ISNULL(SAQTSV.PAR_SERVICE_RECORD_ID,'') as PAR_SERVICE_RECORD_ID,
                            '{UserName}' AS CPQTABLEENTRYADDEDBY,
                            GETDATE() as CPQTABLEENTRYDATEADDED,
                            {UserId} as CpqTableEntryModifiedBy,
                            GETDATE() as CpqTableEntryDateModified
                            FROM SAQSCO (NOLOCK) JOIN SAQTSV (NOLOCK) ON
                            SAQSCO.QUOTE_ID = SAQTSV.QUOTE_ID AND
                            SAQTSV.SERVICE_ID = '{TreeParam}' AND
                            SAQSCO.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND  
                            SAQSCO.SERVICE_ID = SAQTSV.SERVICE_ID AND
                            SAQTSV.SERVICE_TYPE = '{TreeParentParam}'
                            JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
                            JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID
                            WHERE 
                            SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}'
                            AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}')A LEFT JOIN SAQSGB (NOLOCK) AS M ON A.QUOTE_RECORD_ID = M.QUOTE_RECORD_ID AND M.QTEREV_RECORD_ID = A.QTEREV_RECORD_ID AND M.SERVICE_ID = A.SERVICE_ID AND M.GREENBOOK = A.GREENBOOK WHERE M.QUOTE_RECORD_ID is null                  
                    """.format(
                            TreeParam=self.tree_param if (self.tree_parent_level_0.upper() == 'COMPREHENSIVE SERVICES' or self.tree_parent_level_0.upper() == 'COMPLEMENTARY PRODUCTS') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_0,
                            TreeParentParam=self.tree_parent_level_0 if (self.tree_parent_level_0.upper() == 'COMPREHENSIVE SERVICES' or self.tree_parent_level_0.upper() == 'COMPLEMENTARY PRODUCTS') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_1,
                            QuoteRecordId=self.contract_quote_record_id,
                            RevisionRecordId=self.quote_revision_record_id,
                            BatchGroupRecordId=kwargs.get('batch_group_record_id'),
                            UserName=self.user_name,
                            UserId=self.user_id
                        )
            )
            #INC08700058,INC08778358  - End - M

    #A055S000P01-20610,A055S000P01-20609,CR681 - Start - A
    def real_time_status_update(self, **kwargs):
        service_id = kwargs.get('service_id')
        get_assembly_count = Sql.GetFirst("select count(*) as cnt FROM SAQSCA (NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID ='{RevisionRecordId}' AND SERVICE_ID ='{service_id}'".format(QuoteRecordId = self.contract_quote_record_id,RevisionRecordId = self.quote_revision_record_id,service_id = service_id )) 
        #CR681 - A055S000P01-20700 - Start - A
        for assembly_table in ["SAQGPA","SAQSCA","SAQSCO"]: 
            Sql.RunQuery("""UPDATE {obj_name} SET ENTINT_STATUS = '', ENTINT_STATUS_DESC = '' WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID ='{RevisionRecordId}' AND SERVICE_ID ='{service_id}' """.format(QuoteRecordId = self.contract_quote_record_id,RevisionRecordId = self.quote_revision_record_id,service_id = service_id, obj_name= assembly_table )) 
        Sql.RunQuery("""UPDATE SAQSCO SET IBASE_ATTSTS = 'COMPLETE' WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID ='{RevisionRecordId}' AND SERVICE_ID ='{service_id}' AND IBASE_ATTSTS = 'REQUIRED EVENT IS MISSING'""".format(QuoteRecordId = self.contract_quote_record_id,RevisionRecordId = self.quote_revision_record_id,service_id = service_id ))    
        #CR681 - A055S000P01-20700 - End - A
        get_total_count,remainder = divmod(get_assembly_count.cnt,1000)
        get_total_count = get_total_count + (1 if remainder > 0 else 0)
        cnt = 1
        fetch_count = 0
        end_count = 1000
        QueryResult = "begin transaction;"
        equipment_status_dict = {}
        while cnt <= get_total_count:
            get_assembly_record = Sql.GetList("""SELECT * from SAQSCA (NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID ='{RevisionRecordId}' AND SERVICE_ID ='{service_id}' ORDER BY CpqTableEntryId ASC OFFSET {fetch_count} ROWS FETCH NEXT {end_count} ROWS ONLY """.format(QuoteRecordId = self.contract_quote_record_id,RevisionRecordId = self.quote_revision_record_id, service_id = service_id, fetch_count=fetch_count, end_count=end_count))
            for i in get_assembly_record:
                if kwargs.get('quote_type').upper() != 'TOOL':
                    obj_name = "SAQGPA"
                    where_cond = " QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID ='{RevisionRecordId}' AND SERVICE_ID ='{service_id}' AND ASSEMBLY_ID ='{assmbly_id}' AND EQUIPMENT_ID ='{equp_id}' ".format(QuoteRecordId = self.contract_quote_record_id,RevisionRecordId = self.quote_revision_record_id, service_id = service_id,assmbly_id=i.ASSEMBLY_ID, equp_id=i.EQUIPMENT_ID)
                else:
                    obj_name = "SAQSCA"
                    where_cond = " QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID = '{}'".format(i.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID)
                assembly_status =[]
                assembly_status_desc =[]
                get_event_details = Sql.GetList("select * from MAEAPM_INBOUND (NOLOCK) WHERE QUOTE_ID ='{QuoteId}' AND QTEREV_ID ='{RevisionId}' AND SERVICE_ID ='{service_id}' AND ASSEMBLY_ID ='{assmbly_id}' AND EQUIPMENT_ID ='{equp_id}'".format(assmbly_id=i.ASSEMBLY_ID, equp_id=i.EQUIPMENT_ID, RevisionId = self.quote_revision_id, QuoteId =self.contract_quote_id,service_id = service_id))
                if get_event_details:
                    assembly_status = [event.STATUS for event in get_event_details if event.STATUS]
                    assembly_status_desc = [event.STATUS_DESCRIPTION  for event in get_event_details if event.STATUS_DESCRIPTION and event.STATUS == 'ERROR' ]
                    assembly_status_desc = list(set(assembly_status_desc))
                    assembly_status_desc = str(assembly_status_desc).replace("'","")[1:-1]
                    #Trace.Write("assembly_status--"+str(assembly_status))
                    if i.EQUIPMENT_ID in equipment_status_dict.keys() and 'ERROR' in assembly_status:
                        #Trace.Write("iffff--"+str(assembly_status))
                        equipment_status_dict[i.EQUIPMENT_ID] = [equipment_status_dict[i.EQUIPMENT_ID][0]+','+str(i.ASSEMBLY_ID)+' - ERROR',equipment_status_dict[i.EQUIPMENT_ID][1]+','+ str(i.ASSEMBLY_ID)+' - '+ assembly_status_desc]
                    elif 'ERROR' in assembly_status:
                        #Trace.Write("elseeee--"+str(assembly_status))
                        equipment_status_dict[i.EQUIPMENT_ID] =  [str(i.ASSEMBLY_ID)+' - ERROR', str(i.ASSEMBLY_ID)+' - '+ assembly_status_desc]
                    
                    update_query = "UPDATE {obj_name} SET ENTINT_STATUS = '{status}', ENTINT_STATUS_DESC = '{desc}' WHERE {where_cond} ".format(status= 'ERROR' if 'ERROR' in assembly_status else 'SUCCESS' , desc = assembly_status_desc , obj_name =obj_name, where_cond =where_cond )
                    QueryResult += update_query +';'
            cnt += 1
            fetch_count +=1000
            end_count += 1000
        QueryResult += "commit;"
        Sql.RunQuery(QueryResult)
        Log.Info("equipment_status_dict--"+str(equipment_status_dict)+'-'+str(where_cond))
        #Trace.Write("equipment_status_dict--"+str(equipment_status_dict)+'-'+str(where_cond))
        #SAQSCO status update starts
        saqsco_qry = "begin transaction;"
        saqsco_ibase_qry = "begin transaction;"
        for key,value in equipment_status_dict.items():
            saqsco_update_query = """UPDATE SAQSCO SET IBASE_ATTSTS = 'REQUIRED EVENT IS MISSING', ENTINT_STATUS = '{status}', ENTINT_STATUS_DESC = '{status_desc}' WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID ='{RevisionRecordId}' AND SERVICE_ID ='{service_id}' AND EQUIPMENT_ID = '{equp_id}' AND IBASE_ATTSTS ='COMPLETE'""".format(QuoteRecordId=self.contract_quote_record_id, RevisionRecordId = self.quote_revision_record_id, service_id = service_id, equp_id= key, status=value[0],status_desc = value[1] )
            saqsco_ibase_update_query = """UPDATE SAQSCO SET ENTINT_STATUS = '{status}', ENTINT_STATUS_DESC = '{status_desc}' WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID ='{RevisionRecordId}' AND SERVICE_ID ='{service_id}' AND EQUIPMENT_ID = '{equp_id}'""".format(QuoteRecordId=self.contract_quote_record_id, RevisionRecordId = self.quote_revision_record_id, service_id = service_id, equp_id= key, status=value[0],status_desc = value[1] )

            #Trace.Write("saqsco_update_query--"+str(saqsco_update_query))
            saqsco_qry += saqsco_update_query +';'
            saqsco_ibase_qry += saqsco_ibase_update_query +';'
        saqsco_qry += "commit;"
        saqsco_ibase_qry += "commit;"
        #Trace.Write("saqsco_qry--"+str(saqsco_qry))
        Sql.RunQuery(saqsco_qry)
        Sql.RunQuery(saqsco_ibase_qry)
        #SAQSCO status update ends
        return True
    #A055S000P01-20610,A055S000P01-20609 - End - A

    def _insert_quote_service_preventive_maintenance_kit_parts(self, **kwargs):##function to insert events and kit records for tool based quote...
        # Sql.RunQuery("""DELETE FROM SAQSAP WHERE QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(contract_quote_record_id = self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
        # Sql.RunQuery("""DELETE FROM SAQSKP WHERE QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(contract_quote_record_id = self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
        #TKM_start_time = time.time()
        #INC08621140,INC08638619 - Start - A
        #INC08621345 - Start - A 
        service_id = self.tree_param
        if self.entitlement_level in ("GREENBOOK LEVEL","EQUIPMENT LEVEL"):
            service_id = self.tree_parent_level_0
        if self.new_revision == "YES" :
            service_id = self.real_time_integration_service
        #INC08621345 - End - A 
        self.entitlement_level = self.entitlement_level if self.entitlement_level else "OFFERING LEVEL"
        self.entitlement_level_value = self.entitlement_level_value if self.entitlement_level_value else self.tree_param
        if self.new_revision == "YES" :
            self.entitlement_level_value = self.real_time_integration_service
        Log.Info("SAQSAP INSERT-"+str(self.contract_quote_record_id)+'-'+str(self.quote_revision_id)+'-'+str(self.entitlement_level)+'-'+str(self.entitlement_level_value))
        ScriptExecutor.ExecuteGlobal('QTPOSTPKIT',{'QUOTE_ID':str(self.contract_quote_id),'REVISION_ID':str(self.quote_revision_id),'LEVEL':str(self.entitlement_level),'VALUE':str(self.entitlement_level_value)})
        Sql.RunQuery("""UPDATE MAEAPM_INBOUND SET PM_LEVEL = 'Scheduled Maintenance' where QUOTE_ID = '{}' AND QTEREV_ID ='{}' and PM_LEVEL = 'Sched Maint'""".format(self.contract_quote_id, self.quote_revision_id))
        #INC08621140,INC08638619 - End - A
        try:
            #Suresh Added
            CRMQT = SqlHelper.GetFirst("select convert(varchar(100),c4c_quote_id) as c4c_quote_id,MASTER_TABLE_QUOTE_RECORD_ID AS QUOTE_RECORD_ID from SAQTMT(nolock) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(contract_quote_record_id = self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id)) 
            SAQSCA = "SAQSCA_BKP_"+str(CRMQT.c4c_quote_id)
            #INC08786125 - M
            SAQSCA_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS (NOLOCK) WHERE NAME= ''"+str(SAQSCA)+"'' ) BEGIN DROP TABLE "+str(SAQSCA)+" END  ' ")
            sure0090 = SqlHelper.GetFirst("sp_executesql @T=N'SELECT * INTO "+str(SAQSCA)+" FROM SAQSCA(NOLOCK) WHERE QUOTE_RECORD_ID = ''"+str(CRMQT.QUOTE_RECORD_ID)+"'' AND QTEREV_RECORD_ID = ''"+str(self.quote_revision_record_id)+"''  ' ")
            #Suresh Ended
            #INC08621140,INC08638619 - M
            #INC08621345 - M 
            if self.pmevents_changes_insert == "Yes" or self.new_revision == "YES":
                ##A055S000P01-18658 code starts...
                ##calling the script to receive and update Real Time Event/KIT for the quote..
                self._process_query("""INSERT SAQSAP (
                        ASSEMBLY_ID,
                        ASSEMBLY_DESCRIPTION,
                        ASSEMBLY_RECORD_ID,
                        EQUIPMENT_ID,
                        EQUIPMENT_DESCRIPTION,
                        EQUIPMENT_RECORD_ID,
                        GOT_CODE,
                        KIT_ID,
                        KIT_NAME, 
                        KIT_NUMBER,
                        KIT_NUMBER_RECORD_ID,
                        KIT_RECORD_ID,
                        PM_ID,
                        PM_NAME,
                        MNTEVT_LEVEL,
                        PM_RECORD_ID,
                        QUOTE_ID,
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        SERIAL_NO,
                        SERVICE_DESCRIPTION,
                        SERVICE_ID,
                        SALESORG_ID,
                        SALESORG_RECORD_ID,
                        PM_FREQUENCY,
                        SSCM_PM_FREQUENCY,
                        QTESRVCOA_RECORD_ID,
                        PAR_SERVICE_DESCRIPTION,
                        PAR_SERVICE_ID,
                        PAR_SERVICE_RECORD_ID,
                        PM_FREQUENCY_EDITABLE,
                        QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED
                        ) SELECT PM.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
                        SELECT DISTINCT  
                        MAEAPM_INBOUND.ASSEMBLY_ID,
                        SAQSCA.ASSEMBLY_DESCRIPTION,
                        SAQSCA.ASSEMBLY_RECORD_ID,
                        MAEAPM_INBOUND.EQUIPMENT_ID,
                        SAQSCA.EQUIPMENT_DESCRIPTION,
                        SAQSCA.EQUIPMENT_RECORD_ID,
                        SAQSCA.GOT_CODE,
                        MAEAPM_INBOUND.KIT_ID,
                        MAMKIT.KIT_NAME,
                        MAEAPM_INBOUND.KIT_NUMBER,
                        MATKTN.TOOL_KIT_NUMBER_RECORD_ID AS KIT_NUMBER_RECORD_ID,
                        MAMKIT.KIT_RECORD_ID,
                        MAPMEV.PM_ID,
                        MAEAPM_INBOUND.PM_NAME,
                        MAPMEV.MNTEVT_LEVEL,
                        MAPMEV.PM_RECORD_ID AS PM_RECORD_ID,
                        '{QuoteId}' as QUOTE_ID,
                        '{QuoteRecordId}' as QUOTE_RECORD_ID,
                        '{RevisionId}' as QTEREV_ID,
                        '{RevisionRecordId}' as QTEREV_RECORD_ID,
                        SAQSCA.SERIAL_NUMBER,
                        SAQSCA.SERVICE_DESCRIPTION,
                        SAQSCA.SERVICE_ID,
                        SAQTRV.SALESORG_ID,
                        SAQTRV.SALESORG_RECORD_ID,
                        CAST(round(MAEAPM_INBOUND.PM_FREQUENCY,2) AS decimal(18,2)) as PM_FREQUENCY,
                        CAST(round(MAEAPM_INBOUND.PM_FREQUENCY,2) AS decimal(18,2)) as SSCM_PM_FREQUENCY,
                        SAQSCA.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID AS QTESRVCOA_RECORD_ID,
                        SAQSCA.PAR_SERVICE_DESCRIPTION,
                        SAQSCA.PAR_SERVICE_ID,
                        SAQSCA.PAR_SERVICE_RECORD_ID,
                        MAEAPM_INBOUND.RFP_EDIT as PM_FREQUENCY_EDITABLE
                        FROM SAQFEQ (NOLOCK) 
                        JOIN {SAQSCA} SAQSCA(NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID  AND SAQSCA.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID
                        JOIN SAQSCO (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID  AND SAQSCA.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND SAQSCO.SERVICE_ID = SAQSCA.SERVICE_ID AND SAQSCA.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
                        JOIN MAEAPM_INBOUND(NOLOCK) ON MAEAPM_INBOUND.QUOTE_ID = SAQSCO.QUOTE_ID AND MAEAPM_INBOUND.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID AND MAEAPM_INBOUND.QTEREV_ID = SAQSCO.QTEREV_ID AND MAEAPM_INBOUND.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCA.ASSEMBLY_ID = MAEAPM_INBOUND.ASSEMBLY_ID
                        LEFT JOIN MAMKIT(NOLOCK) ON MAMKIT.KIT_ID =  MAEAPM_INBOUND.KIT_ID 
                        LEFT JOIN MATKTN(NOLOCK) ON MATKTN.KIT_ID = MAEAPM_INBOUND.KIT_ID AND MATKTN.KIT_NUMBER = MAEAPM_INBOUND.KIT_NUMBER
                        JOIN MAPMEV(NOLOCK) ON MAPMEV.PM_NAME = MAEAPM_INBOUND.PM_NAME AND MAPMEV.MNTEVT_LEVEL = MAEAPM_INBOUND.PM_LEVEL
                        JOIN SAQTRV(NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID 
                        WHERE SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQFEQ.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCA.SERVICE_ID = '{TreeParam}' ) PM """.format(
                        UserName=self.user_name,
                        TreeParam=self.real_time_integration_service if self.real_time_integration_service else service_id,
                        QuoteId = self.contract_quote_id,
                        QuoteRecordId=self.contract_quote_record_id,
                        RevisionId=self.quote_revision_id,
                        RevisionRecordId=self.quote_revision_record_id,
                        BatchGroupRecordId=kwargs.get('batch_group_record_id'),
                        SAQSCA = str(SAQSCA),
                        additional_where = kwargs.get('additional_where')
                        )
                    )
                self._process_query("""INSERT SAQSKP (
                        ASSEMBLY_ID,
                        ASSEMBLY_DESCRIPTION,
                        ASSEMBLY_RECORD_ID,
                        EQUIPMENT_ID,
                        EQUIPMENT_DESCRIPTION,
                        EQUIPMENT_RECORD_ID,
                        KIT_ID,
                        KIT_NAME,
                        KIT_NUMBER,
                        KIT_NUMBER_RECORD_ID,
                        KIT_RECORD_ID,
                        PART_NUMBER,
                        PART_DESCRIPTION,
                        PART_RECORD_ID,
                        QUANTITY,
                        PM_ID,
                        PM_NAME,
                        PM_RECORD_ID,
                        TKM_FLAG,
                        QUOTE_ID,
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_ID,
                        SERVICE_RECORD_ID,
                        QTESRVMASY_RECORD_ID,
                        PAR_SERVICE_DESCRIPTION,
                        PAR_SERVICE_ID,
                        PAR_SERVICE_RECORD_ID,
                        QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED
                        ) 
                        SELECT KP.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
                        SELECT DISTINCT
                        SAQSAP.ASSEMBLY_ID,
                        SAQSCA.ASSEMBLY_DESCRIPTION,
                        SAQSCA.ASSEMBLY_RECORD_ID,
                        SAQSAP.EQUIPMENT_ID,
                        SAQSCA.EQUIPMENT_DESCRIPTION,
                        SAQSCA.EQUIPMENT_RECORD_ID,
                        SAQSAP.KIT_ID,
                        MAMKIT.KIT_NAME,
                        SAQSAP.KIT_NUMBER,
                        MATKTN.TOOL_KIT_NUMBER_RECORD_ID AS KIT_NUMBER_RECORD_ID,
                        MAMKIT.KIT_RECORD_ID,
                        MAMTRL.SAP_PART_NUMBER,
                        MAMTRL.SAP_DESCRIPTION,
                        MAMTRL.MATERIAL_RECORD_ID,
                        MAKTPT.QUANTITY,
                        MAPMEV.PM_ID,
                        SAQSAP.PM_NAME,
                        MAPMEV.PM_RECORD_ID AS PM_RECORD_ID,
                        1 as TKM_FLAG,
                        '{QuoteId}' as QUOTE_ID,
                        '{QuoteRecordId}' as QUOTE_RECORD_ID,
                        '{RevisionId}' as QTEREV_ID,
                        '{RevisionRecordId}' as QTEREV_RECORD_ID,
                        SAQSCA.SERVICE_DESCRIPTION,
                        SAQSCA.SERVICE_ID,
                        SAQSCA.SERVICE_RECORD_ID,
                        SAQSCA.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID AS QTESRVMASY_RECORD_ID,
                        SAQSCA.PAR_SERVICE_DESCRIPTION,
                        SAQSCA.PAR_SERVICE_ID,
                        SAQSCA.PAR_SERVICE_RECORD_ID
                        FROM SAQFEQ (NOLOCK)
                        JOIN {SAQSCA} SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID
                        JOIN SAQSAP (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQSAP.QUOTE_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQSAP.QTEREV_RECORD_ID
                        AND SAQSAP.ASSEMBLY_ID = SAQSCA.ASSEMBLY_ID AND SAQSAP.EQUIPMENT_ID =  SAQSCA.EQUIPMENT_ID 		AND SAQSAP.QTEREV_RECORD_ID =  SAQSCA.QTEREV_RECORD_ID		
                        INNER JOIN MAMKIT(NOLOCK) ON MAMKIT.KIT_ID =  SAQSAP.KIT_ID 
                        INNER JOIN MATKTN(NOLOCK) ON MATKTN.KIT_ID = SAQSAP.KIT_ID AND ISNULL(MATKTN.KIT_NUMBER ,'')= ISNULL(SAQSAP.KIT_NUMBER,ISNULL(MATKTN.KIT_NUMBER ,''))
                        JOIN MAPMEV(NOLOCK) ON MAPMEV.PM_NAME = SAQSAP.PM_NAME 
                        JOIN MAKTPT(NOLOCK) ON MAKTPT.KIT_ID = SAQSAP.KIT_ID
                        JOIN MAKTPT_INBOUND(NOLOCK) ON MAKTPT_INBOUND.KIT_ID = SAQSAP.KIT_ID AND MAKTPT_INBOUND.QUOTE_ID = SAQSAP.QUOTE_ID AND MAKTPT_INBOUND.QTEREV_ID = SAQSAP.QTEREV_ID AND MAKTPT_INBOUND.SERVICE_ID = SAQSAP.SERVICE_ID AND MAKTPT_INBOUND.PART_NUMBER = MAKTPT.PART_NUMBER
                        JOIN MAMTRL(NOLOCK) ON MAMTRL.SAP_PART_NUMBER = MAKTPT.PART_NUMBER
                        WHERE SAQFEQ.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCA.SERVICE_ID = '{TreeParam}') KP """.format(
                        UserName=self.user_name,
                        TreeParam=self.real_time_integration_service if self.real_time_integration_service else service_id,
                        QuoteId = self.contract_quote_id,
                        QuoteRecordId=self.contract_quote_record_id,
                        RevisionId=self.quote_revision_id,
                        RevisionRecordId=self.quote_revision_record_id,
                        BatchGroupRecordId=kwargs.get('batch_group_record_id'),
                        SAQSCA = str(SAQSCA)
                        ))
                        #INC08621140,INC08638619 - M
            #INC08621345 - M 
            else:
                self._process_query("""INSERT SAQSAP (
                        ASSEMBLY_ID,
                        ASSEMBLY_DESCRIPTION,
                        ASSEMBLY_RECORD_ID,
                        EQUIPMENT_ID,
                        EQUIPMENT_DESCRIPTION,
                        EQUIPMENT_RECORD_ID,
                        GOT_CODE,
                        KIT_ID,
                        KIT_NAME, 
                        KIT_NUMBER,
                        KIT_NUMBER_RECORD_ID,
                        KIT_RECORD_ID,
                        PM_ID,
                        PM_NAME,
                        MNTEVT_LEVEL,
                        PM_RECORD_ID,
                        QUOTE_ID,
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        SERIAL_NO,
                        SERVICE_DESCRIPTION,
                        SERVICE_ID,
                        SALESORG_ID,
                        SALESORG_RECORD_ID,
                        PM_FREQUENCY,
                        SSCM_PM_FREQUENCY,
                        QTESRVCOA_RECORD_ID,
                        PAR_SERVICE_DESCRIPTION,
                        PAR_SERVICE_ID,
                        PAR_SERVICE_RECORD_ID,
                        PM_FREQUENCY_EDITABLE,
                        QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED
                        ) SELECT PM.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
                        SELECT DISTINCT  
                        MAEAPM_INBOUND.ASSEMBLY_ID,
                        SAQSCA.ASSEMBLY_DESCRIPTION,
                        SAQSCA.ASSEMBLY_RECORD_ID,
                        MAEAPM_INBOUND.EQUIPMENT_ID,
                        SAQSCA.EQUIPMENT_DESCRIPTION,
                        SAQSCA.EQUIPMENT_RECORD_ID,
                        SAQSCA.GOT_CODE,
                        MAEAPM_INBOUND.KIT_ID,
                        MAMKIT.KIT_NAME,
                        MAEAPM_INBOUND.KIT_NUMBER,
                        MATKTN.TOOL_KIT_NUMBER_RECORD_ID AS KIT_NUMBER_RECORD_ID,
                        MAMKIT.KIT_RECORD_ID,
                        MAPMEV.PM_ID,
                        MAEAPM_INBOUND.PM_NAME,
                        MAPMEV.MNTEVT_LEVEL,
                        MAPMEV.PM_RECORD_ID AS PM_RECORD_ID,
                        '{QuoteId}' as QUOTE_ID,
                        '{QuoteRecordId}' as QUOTE_RECORD_ID,
                        '{RevisionId}' as QTEREV_ID,
                        '{RevisionRecordId}' as QTEREV_RECORD_ID,
                        SAQSCA.SERIAL_NUMBER,
                        SAQSCA.SERVICE_DESCRIPTION,
                        SAQSCA.SERVICE_ID,
                        SAQTRV.SALESORG_ID,
                        SAQTRV.SALESORG_RECORD_ID,
                        CAST(round(MAEAPM_INBOUND.PM_FREQUENCY,2) AS decimal(18,2)) as PM_FREQUENCY,
                        CAST(round(MAEAPM_INBOUND.PM_FREQUENCY,2) AS decimal(18,2)) as SSCM_PM_FREQUENCY,
                        SAQSCA.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID AS QTESRVCOA_RECORD_ID,
                        SAQSCA.PAR_SERVICE_DESCRIPTION,
                        SAQSCA.PAR_SERVICE_ID,
                        SAQSCA.PAR_SERVICE_RECORD_ID,
                        MAEAPM_INBOUND.RFP_EDIT as PM_FREQUENCY_EDITABLE 
                        FROM SYSPBT (NOLOCK) 
                        JOIN {SAQSCA} SAQSCA(NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQSCA.EQUIPMENT_RECORD_ID = SYSPBT.BATCH_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SYSPBT.QTEREV_RECORD_ID
                        JOIN MAEAPM_INBOUND(NOLOCK) ON MAEAPM_INBOUND.QUOTE_ID = SAQSCA.QUOTE_ID AND MAEAPM_INBOUND.EQUIPMENT_ID = SAQSCA.EQUIPMENT_ID AND MAEAPM_INBOUND.QTEREV_ID = SAQSCA.QTEREV_ID AND MAEAPM_INBOUND.SERVICE_ID = SAQSCA.SERVICE_ID AND SAQSCA.ASSEMBLY_ID = MAEAPM_INBOUND.ASSEMBLY_ID
                        LEFT JOIN MAMKIT(NOLOCK) ON MAMKIT.KIT_ID =  MAEAPM_INBOUND.KIT_ID 
                        LEFT JOIN MATKTN(NOLOCK) ON MATKTN.KIT_ID = MAEAPM_INBOUND.KIT_ID AND MATKTN.KIT_NUMBER = MAEAPM_INBOUND.KIT_NUMBER
                        JOIN MAPMEV(NOLOCK) ON MAPMEV.PM_NAME = MAEAPM_INBOUND.PM_NAME AND MAPMEV.MNTEVT_LEVEL = MAEAPM_INBOUND.PM_LEVEL
                        JOIN SAQTRV(NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID 
                        WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCA.SERVICE_ID = '{TreeParam}' ) PM """.format(
                        UserName=self.user_name,
                        TreeParam=self.real_time_integration_service if self.real_time_integration_service else self.tree_param,
                        QuoteId = self.contract_quote_id,
                        QuoteRecordId=self.contract_quote_record_id,
                        RevisionId=self.quote_revision_id,
                        RevisionRecordId=self.quote_revision_record_id,
                        BatchGroupRecordId=kwargs.get('batch_group_record_id'),
                        SAQSCA = str(SAQSCA),
                        additional_where = kwargs.get('additional_where')
                        )
                    )
                ##A055S000P01-18658 code ends...
                self._process_query("""INSERT SAQSKP (
                        ASSEMBLY_ID,
                        ASSEMBLY_DESCRIPTION,
                        ASSEMBLY_RECORD_ID,
                        EQUIPMENT_ID,
                        EQUIPMENT_DESCRIPTION,
                        EQUIPMENT_RECORD_ID,
                        KIT_ID,
                        KIT_NAME,
                        KIT_NUMBER,
                        KIT_NUMBER_RECORD_ID,
                        KIT_RECORD_ID,
                        PART_NUMBER,
                        PART_DESCRIPTION,
                        PART_RECORD_ID,
                        QUANTITY,
                        PM_ID,
                        PM_NAME,
                        PM_RECORD_ID,
                        TKM_FLAG,
                        QUOTE_ID,
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_ID,
                        SERVICE_RECORD_ID,
                        QTESRVMASY_RECORD_ID,
                        PAR_SERVICE_DESCRIPTION,
                        PAR_SERVICE_ID,
                        PAR_SERVICE_RECORD_ID,
                        QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED
                        ) 
                        SELECT KP.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
                        SELECT DISTINCT
                        SAQSAP.ASSEMBLY_ID,
                        SAQSCA.ASSEMBLY_DESCRIPTION,
                        SAQSCA.ASSEMBLY_RECORD_ID,
                        SAQSAP.EQUIPMENT_ID,
                        SAQSCA.EQUIPMENT_DESCRIPTION,
                        SAQSCA.EQUIPMENT_RECORD_ID,
                        SAQSAP.KIT_ID,
                        MAMKIT.KIT_NAME,
                        SAQSAP.KIT_NUMBER,
                        MATKTN.TOOL_KIT_NUMBER_RECORD_ID AS KIT_NUMBER_RECORD_ID,
                        MAMKIT.KIT_RECORD_ID,
                        MAMTRL.SAP_PART_NUMBER,
                        MAMTRL.SAP_DESCRIPTION,
                        MAMTRL.MATERIAL_RECORD_ID,
                        MAKTPT.QUANTITY,
                        MAPMEV.PM_ID,
                        SAQSAP.PM_NAME,
                        MAPMEV.PM_RECORD_ID AS PM_RECORD_ID,
                        1 as TKM_FLAG,
                        '{QuoteId}' as QUOTE_ID,
                        '{QuoteRecordId}' as QUOTE_RECORD_ID,
                        '{RevisionId}' as QTEREV_ID,
                        '{RevisionRecordId}' as QTEREV_RECORD_ID,
                        SAQSCA.SERVICE_DESCRIPTION,
                        SAQSCA.SERVICE_ID,
                        SAQSCA.SERVICE_RECORD_ID,
                        SAQSCA.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID AS QTESRVMASY_RECORD_ID,
                        SAQSCA.PAR_SERVICE_DESCRIPTION,
                        SAQSCA.PAR_SERVICE_ID,
                        SAQSCA.PAR_SERVICE_RECORD_ID
                        FROM SYSPBT (NOLOCK)
                        JOIN {SAQSCA} SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQSCA.EQUIPMENT_RECORD_ID = SYSPBT.BATCH_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SYSPBT.QTEREV_RECORD_ID
                        JOIN SAQSAP (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQSAP.QUOTE_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQSAP.QTEREV_RECORD_ID
                        AND SAQSAP.ASSEMBLY_ID = SAQSCA.ASSEMBLY_ID AND SAQSAP.EQUIPMENT_ID =  SAQSCA.EQUIPMENT_ID 		AND SAQSAP.QTEREV_RECORD_ID =  SAQSCA.QTEREV_RECORD_ID		
                        INNER JOIN MAMKIT(NOLOCK) ON MAMKIT.KIT_ID =  SAQSAP.KIT_ID 
                        INNER JOIN MATKTN(NOLOCK) ON MATKTN.KIT_ID = SAQSAP.KIT_ID AND ISNULL(MATKTN.KIT_NUMBER ,'')= ISNULL(SAQSAP.KIT_NUMBER,ISNULL(MATKTN.KIT_NUMBER ,''))
                        JOIN MAPMEV(NOLOCK) ON MAPMEV.PM_NAME = SAQSAP.PM_NAME 
                        JOIN MAKTPT(NOLOCK) ON MAKTPT.KIT_ID = SAQSAP.KIT_ID
                        JOIN MAKTPT_INBOUND(NOLOCK) ON MAKTPT_INBOUND.KIT_ID = SAQSAP.KIT_ID AND MAKTPT_INBOUND.QUOTE_ID = SAQSAP.QUOTE_ID AND MAKTPT_INBOUND.QTEREV_ID = SAQSAP.QTEREV_ID AND MAKTPT_INBOUND.SERVICE_ID = SAQSAP.SERVICE_ID AND MAKTPT_INBOUND.PART_NUMBER = MAKTPT.PART_NUMBER
                        JOIN MAMTRL(NOLOCK) ON MAMTRL.SAP_PART_NUMBER = MAKTPT.PART_NUMBER
                        WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCA.SERVICE_ID = '{TreeParam}') KP """.format(
                        UserName=self.user_name,
                        TreeParam=self.tree_param,
                        QuoteId = self.contract_quote_id,
                        QuoteRecordId=self.contract_quote_record_id,
                        RevisionId=self.quote_revision_id,
                        RevisionRecordId=self.quote_revision_record_id,
                        BatchGroupRecordId=kwargs.get('batch_group_record_id'),
                        SAQSCA = str(SAQSCA)
                        ))
            #A055S000P01-20610,A055S000P01-20609,CR681 - Start - A
            self.real_time_status_update(service_id= service_id, quote_type = 'TOOL')
            #A055S000P01-20610,A055S000P01-20609,CR681 - End - A
            ##A055S000P01-18658 code starts...
            ##Deleting the inbound tables after inserting the events ant kit...
            delete_obj_list = ["MAEAPM_INBOUND","MAKTPT_INBOUND"]
            for object in delete_obj_list:
                Sql.RunQuery("DELETE FROM {} WHERE QUOTE_ID='{}' AND QTEREV_ID = '{}' ".format(object,self.contract_quote_id,self.quote_revision_id))
            #A055S000P01-18658 code ends...
                    
            ##UPDATING THE TKM COLUMN VALUE STARTS..
            Sql.RunQuery("""UPDATE SAQSAP SET TKM_FLAG = 1 from SAQSAP join (Select count(QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID) as cnt,EQUIPMENT_ID,ASSEMBLY_ID,PM_ID,QUOTE_RECORD_ID
                from SAQSKP(NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' group by EQUIPMENT_ID,ASSEMBLY_ID,PM_ID,QUOTE_RECORD_ID) as parts on 
                SAQSAP.EQUIPMENT_ID = parts.EQUIPMENT_ID  AND parts.ASSEMBLY_ID = SAQSAP.ASSEMBLY_ID AND parts.PM_ID = SAQSAP.PM_ID AND parts.QUOTE_RECORD_ID = SAQSAP.QUOTE_RECORD_ID WHERE SAQSAP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSAP.QTEREV_RECORD_ID = '{RevisionRecordId}' and parts.cnt > 0""".format(QuoteRecordId = self.contract_quote_record_id,RevisionRecordId= self.quote_revision_record_id ))
            ##UPDATING THE TKM COLUMN VALU ENDS.
            #INC08786125 - M
            SAQSCA_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS (NOLOCK) WHERE NAME= ''"+str(SAQSCA)+"'' ) BEGIN DROP TABLE "+str(SAQSCA)+" END  ' ")
            return True
        except:
            #INC08786125 - M
            SAQSCA_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS (NOLOCK) WHERE NAME= ''"+str(SAQSCA)+"'' ) BEGIN DROP TABLE "+str(SAQSCA)+" END  ' ")

    
    def applied_preventive_maintainence(self, **kwargs):##function to insert got code ,events and child tables for event based and flex event based quote type...
        ###Deleting the SAQSCA,SAQSAP and SAQSKP TABLE records when the user is changing the quote type from Tool Based to other values...
        #Log.Info("INSIDE FUNCTION TO CHECK FOR REVISION")
        #INC08621345 - Start - M
        service_id = self.tree_param 
        if self.entitlement_level in ("GREENBOOK LEVEL","EQUIPMENT LEVEL"):
            service_id = self.tree_parent_level_0
        if self.new_revision == "YES" :
            service_id = self.real_time_integration_service
        #INC08696637 - Start - A
        ScriptExecutor.ExecuteGlobal('QTPOSTPKIT',{'QUOTE_ID':str(self.contract_quote_id),'REVISION_ID':str(self.quote_revision_id),'LEVEL':str(self.entitlement_level),'VALUE':str(self.entitlement_level_value)})
        #INC08621140,INC08638619 - Start - A
        Sql.RunQuery("""UPDATE MAEAPM_INBOUND SET PM_LEVEL = 'Scheduled Maintenance' where QUOTE_ID = '{}' AND QTEREV_ID ='{}' and PM_LEVEL = 'Sched Maint'""".format(self.contract_quote_id, self.quote_revision_id))
        #INC08696637 - End - A
        if(kwargs.get('applied_preventive_maintainence_quote_type_changed') == "Yes" or  kwargs.get('pmevents_changes_insert') == "Yes")and self.tools_from_ui != "Yes":
        
            #Log.Info("INSIDE IF TO CHECK FOR REVISION")
            self.entitlement_level = self.entitlement_level if self.entitlement_level else "OFFERING LEVEL"
            self.entitlement_level_value = self.entitlement_level_value if self.entitlement_level_value else service_id
            Log.Info("SAQRGG INSERT-"+str(self.contract_quote_record_id)+'-'+str(self.real_time_integration_service)) 
            if self.new_revision == "YES":
                self.tree_param = self.entitlement_level_value = service_id = self.real_time_integration_service
            #INC08621140,INC08638619 - End - A
            delete_obj_list = ["SAQSAP","SAQSKP"]
            for object in delete_obj_list:
                Sql.RunQuery("DELETE FROM {} WHERE QUOTE_RECORD_ID='{}' and SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(object,self.contract_quote_record_id, service_id,self.quote_revision_record_id ))
            self._process_query("""INSERT SAQRGG (
                    GOT_CODE,
                    GOTCODE_RECORD_ID,
                    GREENBOOK,
                    GREENBOOK_RECORD_ID,
                    SERVICE_ID,
                    SERVICE_DESCRIPTION,
                    SERVICE_RECORD_ID,
                    QUOTE_ID,
                    QUOTE_RECORD_ID,
                    QTEREV_ID,
                    QTEREV_RECORD_ID,
                    QTESRV_RECORD_ID,
                    QTESRVGBK_RECORD_ID,
                    QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID,
                    CPQTABLEENTRYADDEDBY,
                    CPQTABLEENTRYDATEADDED
                    )SELECT gotcode.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(
                    SELECT DISTINCT  
                    MAEQUP.GOT_CODE,
                    SAGTCD.GOT_CODES_RECORD_ID,
                    SAQSCO.GREENBOOK,
                    SAQSCO.GREENBOOK_RECORD_ID,
                    SAQSCO.SERVICE_ID,
                    SAQSCO.SERVICE_DESCRIPTION,
                    SAQSCO.SERVICE_RECORD_ID,
                    '{QuoteId}' as QUOTE_ID,
                    '{QuoteRecordId}' as QUOTE_RECORD_ID,
                    '{RevisionId}' as QTEREV_ID,
                    '{RevisionRecordId}' as QTEREV_RECORD_ID,
                    SAQTSV.QUOTE_SERVICE_RECORD_ID as QTESRV_RECORD_ID,
                    SAQSGB.QUOTE_SERVICE_GREENBOOK_RECORD_ID as QTESRVGBK_RECORD_ID
                    FROM SAQSCO (NOLOCK)
                    JOIN MAEQUP(NOLOCK) ON MAEQUP.PAR_EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID
                    JOIN SAQTSV(NOLOCK) ON SAQTSV.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQSCO.SERVICE_RECORD_ID = SAQTSV.SERVICE_RECORD_ID
                    JOIN SAQSGB(NOLOCK) ON SAQSGB.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQSGB.QTEREV_RECORD_ID AND SAQSCO.SERVICE_RECORD_ID = SAQSGB.SERVICE_RECORD_ID AND SAQSCO.GREENBOOK_RECORD_ID = SAQSGB.GREENBOOK_RECORD_ID
                    JOIN SAGTCD(NOLOCK) ON MAEQUP.GOT_CODE = SAGTCD.GOT_CODE
                    JOIN SAQTRV(NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID 
                    WHERE SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCO.SERVICE_ID = '{TreeParam}' ) gotcode LEFT JOIN SAQRGG (nolock) as pmsa_gotcode on  gotcode.QUOTE_RECORD_ID = pmsa_gotcode.QUOTE_RECORD_ID and gotcode.QTEREV_RECORD_ID = pmsa_gotcode.QTEREV_RECORD_ID and gotcode.SERVICE_RECORD_ID = pmsa_gotcode.SERVICE_RECORD_ID and gotcode.GREENBOOK_RECORD_ID = pmsa_gotcode.GREENBOOK_RECORD_ID and gotcode.GOT_CODES_RECORD_ID = pmsa_gotcode.GOTCODE_RECORD_ID WHERE ISNULL(pmsa_gotcode.GOTCODE_RECORD_ID,'') = '' """.format(
                    UserName=self.user_name,
                    TreeParam=service_id,
                    QuoteId = self.contract_quote_id,
                    QuoteRecordId=self.contract_quote_record_id,
                    RevisionId=self.quote_revision_id,
                    RevisionRecordId=self.quote_revision_record_id
                    )
                )
            ##A055S000P01-17959 inserting the device node and process type as null by default...##HPQC DEFECT 471 Events not inserting issue , changed the join condition for saqgpm table insert...
            #INC08664376,INC08696637,INC08709720 - Start - M
            self._process_query("""INSERT SAQGPM(CHAMBER_QUANTITY,
                    GOT_CODE,
                    GOTCODE_RECORD_ID,
                    GREENBOOK,
                    GREENBOOK_RECORD_ID,
                    PM_ID,
                    PM_NAME,
                    PM_RECORD_ID,
                    MNTEVT_LEVEL,
                    KIT_ID,
                    KIT_NAME,
                    KIT_RECORD_ID,
                    SERVICE_ID,
                    SERVICE_DESCRIPTION,
                    SERVICE_RECORD_ID,
                    PM_FREQUENCY_EDITABLE,
                    PROCESS_TYPE,
                    DEVICE_NODE,
                    QUOTE_ID,
                    QUOTE_RECORD_ID,
                    QTEREV_ID,
                    QTEREV_RECORD_ID,
                    QTESRV_RECORD_ID,
                    QTESRVGBK_RECORD_ID,
                    QTEREVGOT_RECORD_ID,
                    TKM_FLAG,
                    QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID,
                    CPQTABLEENTRYADDEDBY,
                    CPQTABLEENTRYDATEADDED
                    )SELECT DISTINCT pmsa_pmevents.CHAMBER_QUANTITY,
                    pmsa_pmevents.GOT_CODE,
                    pmsa_pmevents.GOTCODE_RECORD_ID,
                    pmsa_pmevents.GREENBOOK,
                    pmsa_pmevents.GREENBOOK_RECORD_ID,
                    pmsa_pmevents.PM_ID,
                    pmsa_pmevents.PM_NAME,
                    pmsa_pmevents.PM_RECORD_ID,
                    pmsa_pmevents.PM_LEVEL,
                    pmsa_pmevents.KIT_ID,
                    pmsa_pmevents.KIT_NAME,
                    pmsa_pmevents.KIT_RECORD_ID,
                    pmsa_pmevents.SERVICE_ID,
                    pmsa_pmevents.SERVICE_DESCRIPTION,
                    pmsa_pmevents.SERVICE_RECORD_ID,
                    pmsa_pmevents.PM_FREQUENCY_EDITABLE,
                    pmsa_pmevents.PROCESS_TYPE,
                    pmsa_pmevents.DEVICE_NODE,
                    pmsa_pmevents.QUOTE_ID,
                    pmsa_pmevents.QUOTE_RECORD_ID,
                    pmsa_pmevents.QTEREV_ID,
                    pmsa_pmevents.QTEREV_RECORD_ID,
                    pmsa_pmevents.QTESRV_RECORD_ID,
                    pmsa_pmevents.QTESRVGBK_RECORD_ID,
                    pmsa_pmevents.QTEREVGOT_RECORD_ID,pmsa_pmevents.TKM_FLAG,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(
                    SELECT DISTINCT
                    0 as CHAMBER_QUANTITY,
                    SAQRGG.GOT_CODE,
                    SAQRGG.GOTCODE_RECORD_ID,
                    SAQRGG.GREENBOOK,
                    SAQRGG.GREENBOOK_RECORD_ID,
                    MAPMEV.PM_ID,
                    MAEAPM_INBOUND.PM_NAME,
                    MAPMEV.PM_RECORD_ID,
                    CASE WHEN MAEAPM_INBOUND.PM_LEVEL ='Sched Maint' THEN 'Scheduled Maintenance' ELSE MAEAPM_INBOUND.PM_LEVEL END AS PM_LEVEL ,
                    MAEAPM_INBOUND.KIT_ID,
                    MAMKIT.KIT_NAME,
                    MAMKIT.KIT_RECORD_ID,
                    SAQRGG.SERVICE_ID,
                    SAQRGG.SERVICE_DESCRIPTION,
                    SAQRGG.SERVICE_RECORD_ID,
                    MAEAPM_INBOUND.RFP_EDIT as PM_FREQUENCY_EDITABLE,
                    ISNULL(MAEQUP.PROCESS_TYPE,'') AS PROCESS_TYPE,
                    ISNULL(MAEQUP.DEVICE_NODE,'') AS DEVICE_NODE,
                    '{QuoteId}' as QUOTE_ID,
                    '{QuoteRecordId}' as QUOTE_RECORD_ID,
                    '{RevisionId}' as QTEREV_ID,
                    '{RevisionRecordId}' as QTEREV_RECORD_ID,
                    SAQRGG.QTESRV_RECORD_ID as QTESRV_RECORD_ID,
                    SAQRGG.QTESRVGBK_RECORD_ID as QTESRVGBK_RECORD_ID,
                    SAQRGG.QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID as QTEREVGOT_RECORD_ID,
                    {tkm_flag} as TKM_FLAG
                    FROM SAQRGG (NOLOCK) 
                    JOIN SAQSCA(NOLOCK) ON SAQRGG.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQRGG.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID AND SAQRGG.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID AND SAQRGG.GREENBOOK_RECORD_ID = SAQSCA.GREENBOOK_RECORD_ID
                    JOIN MAEQUP(NOLOCK) ON MAEQUP.PAR_EQUIPMENT_ID = SAQSCA.EQUIPMENT_ID AND MAEQUP.EQUIPMENT_ID = SAQSCA.ASSEMBLY_ID AND SAQRGG.GOT_CODE = MAEQUP.GOT_CODE
                    JOIN MAEAPM_INBOUND(NOLOCK) ON MAEAPM_INBOUND.QUOTE_ID = SAQSCA.QUOTE_ID AND MAEAPM_INBOUND.EQUIPMENT_ID = SAQSCA.EQUIPMENT_ID AND MAEAPM_INBOUND.QTEREV_ID = SAQSCA.QTEREV_ID AND MAEAPM_INBOUND.SERVICE_ID = SAQSCA.SERVICE_ID AND MAEQUP.EQUIPMENT_ID = MAEAPM_INBOUND.ASSEMBLY_ID
                    JOIN MAPMEV ON MAPMEV.PM_NAME = MAEAPM_INBOUND.PM_NAME AND MAPMEV.MNTEVT_LEVEL = MAEAPM_INBOUND.PM_LEVEL
                    {JoinString} MAMKIT ON MAMKIT.KIT_ID = MAEAPM_INBOUND.KIT_ID
                    WHERE SAQRGG.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRGG.
                    QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRGG.SERVICE_ID = '{TreeParam}' AND  MAEAPM_INBOUND.PM_LEVEL IN {pm_level_value}) pmsa_pmevents  LEFT JOIN SAQGPM (NOLOCK) AS pm on pmsa_pmevents.QUOTE_RECORD_ID = pm.QUOTE_RECORD_ID AND pmsa_pmevents.QTEREV_RECORD_ID = pm.QTEREV_RECORD_ID AND pmsa_pmevents.SERVICE_RECORD_ID = pm.SERVICE_RECORD_ID AND pmsa_pmevents.GREENBOOK_RECORD_ID = pm.GREENBOOK_RECORD_ID and pmsa_pmevents.GOTCODE_RECORD_ID = pm.GOTCODE_RECORD_ID and pmsa_pmevents.PM_RECORD_ID = pm.PM_RECORD_ID and isnull(pmsa_pmevents.PROCESS_TYPE,'') = isnull(pm.PROCESS_TYPE,'') and isnull(pmsa_pmevents.DEVICE_NODE,'') = isnull(pm.DEVICE_NODE,'') AND ISNULL(pmsa_pmevents.KIT_ID,'') = ISNULL(pm.KIT_ID,'')
                    WHERE ISNULL(pm.PM_RECORD_ID,'') = '' """.format(
                    UserName=self.user_name,
                    TreeParam=self.real_time_integration_service if self.real_time_integration_service else self.tree_param,
                    QuoteId = self.contract_quote_id,
                    QuoteRecordId=self.contract_quote_record_id,
                    RevisionId=self.quote_revision_id,
                    RevisionRecordId=self.quote_revision_record_id,
                    pm_level_value = ('Scheduled Maintenance','Sched Maint','Chamber / Module PM') if(kwargs.get('quote_type_attribute_value').upper() != "TOOL BASED") else ('Scheduled Maintenance','Chamber / Module PM','Corrective Maintenance'),
                    tkm_flag = (1 if (str(self.tree_param) == "Z0010" or str(self.real_time_integration_service) == "Z0010"  ) else 0),
                    JoinString = 'JOIN' if str(self.tree_param) == "Z0010" else 'LEFT JOIN'
                    )
                )
            Log.Info("revision_service"+str(self.real_time_integration_service))
            Log.Info("paramsent_from_script"+str(self.tree_param))
            Log.Info("""INSERT SAQGPM(CHAMBER_QUANTITY,
                    GOT_CODE,
                    GOTCODE_RECORD_ID,
                    GREENBOOK,
                    GREENBOOK_RECORD_ID,
                    PM_ID,
                    PM_NAME,
                    PM_RECORD_ID,
                    MNTEVT_LEVEL,
                    KIT_ID,
                    KIT_NAME,
                    KIT_RECORD_ID,
                    SERVICE_ID,
                    SERVICE_DESCRIPTION,
                    SERVICE_RECORD_ID,
                    PM_FREQUENCY_EDITABLE,
                    PROCESS_TYPE,
                    DEVICE_NODE,
                    QUOTE_ID,
                    QUOTE_RECORD_ID,
                    QTEREV_ID,
                    QTEREV_RECORD_ID,
                    QTESRV_RECORD_ID,
                    QTESRVGBK_RECORD_ID,
                    QTEREVGOT_RECORD_ID,
                    TKM_FLAG,
                    QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID,
                    CPQTABLEENTRYADDEDBY,
                    CPQTABLEENTRYDATEADDED
                    )SELECT DISTINCT pmsa_pmevents.CHAMBER_QUANTITY,
                    pmsa_pmevents.GOT_CODE,
                    pmsa_pmevents.GOTCODE_RECORD_ID,
                    pmsa_pmevents.GREENBOOK,
                    pmsa_pmevents.GREENBOOK_RECORD_ID,
                    pmsa_pmevents.PM_ID,
                    pmsa_pmevents.PM_NAME,
                    pmsa_pmevents.PM_RECORD_ID,
                    pmsa_pmevents.PM_LEVEL,
                    pmsa_pmevents.KIT_ID,
                    pmsa_pmevents.KIT_NAME,
                    pmsa_pmevents.KIT_RECORD_ID,
                    pmsa_pmevents.SERVICE_ID,
                    pmsa_pmevents.SERVICE_DESCRIPTION,
                    pmsa_pmevents.SERVICE_RECORD_ID,
                    pmsa_pmevents.PM_FREQUENCY_EDITABLE,
                    pmsa_pmevents.PROCESS_TYPE,
                    pmsa_pmevents.DEVICE_NODE,
                    pmsa_pmevents.QUOTE_ID,
                    pmsa_pmevents.QUOTE_RECORD_ID,
                    pmsa_pmevents.QTEREV_ID,
                    pmsa_pmevents.QTEREV_RECORD_ID,
                    pmsa_pmevents.QTESRV_RECORD_ID,
                    pmsa_pmevents.QTESRVGBK_RECORD_ID,
                    pmsa_pmevents.QTEREVGOT_RECORD_ID,pmsa_pmevents.TKM_FLAG,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(
                    SELECT DISTINCT
                    0 as CHAMBER_QUANTITY,
                    SAQRGG.GOT_CODE,
                    SAQRGG.GOTCODE_RECORD_ID,
                    SAQRGG.GREENBOOK,
                    SAQRGG.GREENBOOK_RECORD_ID,
                    MAPMEV.PM_ID,
                    MAEAPM_INBOUND.PM_NAME,
                    MAPMEV.PM_RECORD_ID,
                    CASE WHEN MAEAPM_INBOUND.PM_LEVEL ='Sched Maint' THEN 'Scheduled Maintenance' ELSE MAEAPM_INBOUND.PM_LEVEL END AS PM_LEVEL ,
                    MAEAPM_INBOUND.KIT_ID,
                    MAMKIT.KIT_NAME,
                    MAMKIT.KIT_RECORD_ID,
                    SAQRGG.SERVICE_ID,
                    SAQRGG.SERVICE_DESCRIPTION,
                    SAQRGG.SERVICE_RECORD_ID,
                    MAEAPM_INBOUND.RFP_EDIT as PM_FREQUENCY_EDITABLE,
                    ISNULL(MAEQUP.PROCESS_TYPE,'') AS PROCESS_TYPE,
                    ISNULL(MAEQUP.DEVICE_NODE,'') AS DEVICE_NODE,
                    '{QuoteId}' as QUOTE_ID,
                    '{QuoteRecordId}' as QUOTE_RECORD_ID,
                    '{RevisionId}' as QTEREV_ID,
                    '{RevisionRecordId}' as QTEREV_RECORD_ID,
                    SAQRGG.QTESRV_RECORD_ID as QTESRV_RECORD_ID,
                    SAQRGG.QTESRVGBK_RECORD_ID as QTESRVGBK_RECORD_ID,
                    SAQRGG.QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID as QTEREVGOT_RECORD_ID,
                    {tkm_flag} as TKM_FLAG
                    FROM SAQRGG (NOLOCK) 
                    JOIN SAQSCA(NOLOCK) ON SAQRGG.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQRGG.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID AND SAQRGG.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID AND SAQRGG.GREENBOOK_RECORD_ID = SAQSCA.GREENBOOK_RECORD_ID
                    JOIN MAEQUP(NOLOCK) ON MAEQUP.PAR_EQUIPMENT_ID = SAQSCA.EQUIPMENT_ID AND MAEQUP.EQUIPMENT_ID = SAQSCA.ASSEMBLY_ID AND SAQRGG.GOT_CODE = MAEQUP.GOT_CODE
                    JOIN MAEAPM_INBOUND(NOLOCK) ON MAEAPM_INBOUND.QUOTE_ID = SAQSCA.QUOTE_ID AND MAEAPM_INBOUND.EQUIPMENT_ID = SAQSCA.EQUIPMENT_ID AND MAEAPM_INBOUND.QTEREV_ID = SAQSCA.QTEREV_ID AND MAEAPM_INBOUND.SERVICE_ID = SAQSCA.SERVICE_ID AND MAEQUP.EQUIPMENT_ID = MAEAPM_INBOUND.ASSEMBLY_ID
                    JOIN MAPMEV ON MAPMEV.PM_NAME = MAEAPM_INBOUND.PM_NAME AND MAPMEV.MNTEVT_LEVEL = MAEAPM_INBOUND.PM_LEVEL
                    {JoinString} MAMKIT ON MAMKIT.KIT_ID = MAEAPM_INBOUND.KIT_ID
                    WHERE SAQRGG.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRGG.
                    QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRGG.SERVICE_ID = '{TreeParam}' AND  MAEAPM_INBOUND.PM_LEVEL IN {pm_level_value}) pmsa_pmevents  LEFT JOIN SAQGPM (NOLOCK) AS pm on pmsa_pmevents.QUOTE_RECORD_ID = pm.QUOTE_RECORD_ID AND pmsa_pmevents.QTEREV_RECORD_ID = pm.QTEREV_RECORD_ID AND pmsa_pmevents.SERVICE_RECORD_ID = pm.SERVICE_RECORD_ID AND pmsa_pmevents.GREENBOOK_RECORD_ID = pm.GREENBOOK_RECORD_ID and pmsa_pmevents.GOTCODE_RECORD_ID = pm.GOTCODE_RECORD_ID and pmsa_pmevents.PM_RECORD_ID = pm.PM_RECORD_ID and isnull(pmsa_pmevents.PROCESS_TYPE,'') = isnull(pm.PROCESS_TYPE,'') and isnull(pmsa_pmevents.DEVICE_NODE,'') = isnull(pm.DEVICE_NODE,'') AND ISNULL(pmsa_pmevents.KIT_ID,'') = ISNULL(pm.KIT_ID,'')
                    WHERE ISNULL(pm.PM_RECORD_ID,'') = '' """.format(
                    UserName=self.user_name,
                    TreeParam=self.real_time_integration_service if self.real_time_integration_service else self.tree_param,
                    QuoteId = self.contract_quote_id,
                    QuoteRecordId=self.contract_quote_record_id,
                    RevisionId=self.quote_revision_id,
                    RevisionRecordId=self.quote_revision_record_id,
                    pm_level_value = ('Scheduled Maintenance','Sched Maint','Chamber / Module PM') if(kwargs.get('quote_type_attribute_value').upper() != "TOOL BASED") else ('Scheduled Maintenance','Chamber / Module PM','Corrective Maintenance'),
                    tkm_flag = (1 if (str(self.tree_param) == "Z0010" or str(self.real_time_integration_service) == "Z0010"  ) else 0),
                    JoinString = 'JOIN' if str(self.tree_param) == "Z0010" else 'LEFT JOIN'
                    )
                )
                # additional_where = kwargs.get('additional_where')
            #INC08664376,INC08696637,INC08709720 - End - M
            Sql.RunQuery("""UPDATE SAQGPM
                        SET
                        SAQGPM.CHAMBER_QUANTITY = assembly.cnt
                        FROM SAQGPM (NOLOCK)
                        INNER JOIN (select DISTINCT count(SAQGPA.QTEREVPME_RECORD_ID) as cnt,SAQGPA.QTEREVPME_RECORD_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID FROM saqgpa WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' and SAQGPA.QTEREV_RECORD_ID = '{RevisionRecordId}' GROUP BY SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.QTEREVPME_RECORD_ID) assembly ON SAQGPM.QUOTE_RECORD_ID = assembly.QUOTE_RECORD_ID AND SAQGPM.QTEREV_RECORD_ID = assembly.QTEREV_RECORD_ID AND SAQGPM.QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID = assembly.QTEREVPME_RECORD_ID WHERE SAQGPM.QUOTE_RECORD_ID = '{QuoteRecordId}' and SAQGPM.QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
            
            ##Creating backup table for saqgpa table insert... 
            saqgpm_backup_table = "saqgpm_backup_table_{}".format(self.contract_quote_id) 
            #INC08786125 - M
            drop_saqgpm_backup_table = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS (NOLOCK) WHERE NAME= ''"+str(saqgpm_backup_table)+"'' ) BEGIN DROP TABLE "+str(saqgpm_backup_table)+" END  ' ")


            saqgpm_temp_table_insert = SqlHelper.GetFirst("sp_executesql @T=N'SELECT SAQGPM.GOT_CODE,SAQGPM.GOTCODE_RECORD_ID,SAQGPM.GREENBOOK,SAQGPM.GREENBOOK_RECORD_ID,SAQGPM.PM_ID,SAQGPM.PM_NAME,SAQGPM.PM_RECORD_ID,SAQGPM.TKM_FLAG,SAQGPM.MNTEVT_LEVEL,SAQGPM.SERVICE_ID,SAQGPM.SERVICE_DESCRIPTION,SAQGPM.SERVICE_RECORD_ID,SAQGPM.PM_FREQUENCY,SAQGPM.SSCM_PM_FREQUENCY,SAQGPM.PM_FREQUENCY_EDITABLE,SAQGPM.PROCESS_TYPE,SAQGPM.DEVICE_NODE,SAQGPM.QUOTE_ID,SAQGPM.QUOTE_RECORD_ID,SAQGPM.QTEREV_ID,SAQGPM.QTEREV_RECORD_ID,SAQGPM.QTESRV_RECORD_ID,SAQGPM.QTESRVGBK_RECORD_ID,SAQGPM.KIT_ID,SAQGPM.KIT_NAME,SAQGPM.KIT_NUMBER,SAQGPM.KITNUMBER_RECORD_ID,SAQGPM.KIT_RECORD_ID,SAQGPM.QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID as QTEREVPME_RECORD_ID INTO "+str(saqgpm_backup_table)+" FROM SAQGPM (NOLOCK) WHERE SAQGPM.QUOTE_RECORD_ID = ''{}'' AND SAQGPM.QTEREV_RECORD_ID = ''{}'' AND  SAQGPM.SERVICE_ID = ''{}'' '".format(self.contract_quote_record_id,self.quote_revision_record_id,self.real_time_integration_service if self.real_time_integration_service else service_id))


            saqsco_backup_table = "saqsco_backup_table_{}".format(self.contract_quote_id) 
            #INC08786125 - M
            drop_saqsco_backup_table = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS (NOLOCK) WHERE NAME= ''"+str(saqsco_backup_table)+"'' ) BEGIN DROP TABLE "+str(saqsco_backup_table)+" END  ' ")
            ##HPQC DEFECT 630 code starts...
            #HPQC DEFECT 1917 - ADDED GREENBOOK AND GREENBOOK_RECORD_ID to insert and backup query
            #INC08865716,INC08871703 - Start - M
            saqsco_temp_table_insert = SqlHelper.GetFirst("sp_executesql @T=N'SELECT SAQSCO.QUOTE_RECORD_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQSCO.QTEREV_RECORD_ID,SAQSCO.QUOTE_ID,SAQSCO.QTEREV_ID,SAQSCO.SERVICE_RECORD_ID,SAQSCO.SERVICE_ID,SAQSCO.EQUIPMENT_ID,SAQSCO.EQUIPMENT_DESCRIPTION,SAQSCO.EQUIPMENT_RECORD_ID,SAQSCO.FABLOCATION_ID,SAQSCO.FABLOCATION_NAME,SAQSCO.FABLOCATION_RECORD_ID INTO "+str(saqsco_backup_table)+" FROM SAQSCO(NOLOCK) WHERE SAQSCO.QUOTE_RECORD_ID = ''{}'' AND SAQSCO.QTEREV_RECORD_ID = ''{}'' AND  SAQSCO.SERVICE_ID = ''{}'' '".format(self.contract_quote_record_id,self.quote_revision_record_id,self.real_time_integration_service if self.real_time_integration_service else service_id))
            #INC08865716,INC08871703 - End - M
            ##HPQC DEFECT 630 code ends...
            ##HPQC DEFECT 471 code starts...
            #INC08664376,INC08782102  - Start - M  
            #INC08664376,INC08709720,INC08782102,INC08865716,INC08871703 - Start - M                               
            self._process_query(
                """INSERT SAQGPA (
                        ASSEMBLY_ID,
                        ASSEMBLY_DESCRIPTION,
                        ASSEMBLY_RECORD_ID,
                        ASSEMBLY_STATUS,
                        EQUIPMENT_ID,
                        EQUIPMENT_DESCRIPTION,
                        EQUIPMENT_RECORD_ID,
                        EQUIPMENTTYPE_ID,
                        EQUIPMENTTYPE_RECORD_ID,
                        GOT_CODE,
                        GOTCODE_RECORD_ID,
                        GREENBOOK,
                        GREENBOOK_RECORD_ID,
                        FABLOCATION_ID,
                        FABLOCATION_NAME,
                        FABLOCATION_RECORD_ID,
                        PM_ID,
                        PM_NAME,
                        PM_RECORD_ID,
                        MNTEVT_LEVEL,
                        SERVICE_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_RECORD_ID,
                        PM_FREQUENCY,
                        SSCM_PM_FREQUENCY,
                        CLEAN_COAT_DIFF,
                        PM_FREQUENCY_EDITABLE,
                        PROCESS_TYPE,
                        DEVICE_NODE,
                        KIT_ID,
                        KIT_NAME,
                        KIT_NUMBER,
                        KITNUMBER_RECORD_ID,
                        KIT_RECORD_ID,
                        QUOTE_ID,
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        QTESRV_RECORD_ID,
                        QTESRVGBK_RECORD_ID,
                        QTEREVPME_RECORD_ID,
                        QTESRVCOB_RECORD_ID,
                        TKM_FLAG,
                        INCLUDED,
                        QUOTE_REV_PO_GRNBK_PM_EVEN_ASSEMBLIES_RECORD_ID,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED,
                        ADDUSR_RECORD_ID)
                        SELECT PM_EVENT_ASSEMBLY.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_GRNBK_PM_EVEN_ASSEMBLIES_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED ,{UserId} as ADDUSR_RECORD_ID FROM (SELECT DISTINCT 
                        MAEQUP.EQUIPMENT_ID AS ASSEMBLY_ID,
                        MAEQUP.EQUIPMENT_DESCRIPTION AS ASSEMBLY_DESCRIPTION,
                        MAEQUP.EQUIPMENT_RECORD_ID AS ASSEMBLY_RECORD_ID,
                        MAEQUP.EQUIPMENT_STATUS AS ASSEMBLY_STATUS,
                        saqsco_backup_table.EQUIPMENT_ID,
                        saqsco_backup_table.EQUIPMENT_DESCRIPTION,
                        saqsco_backup_table.EQUIPMENT_RECORD_ID,
                        MAEQUP.EQUIPMENTTYPE_ID,
                        MAEQUP.EQUIPMENTTYPE_RECORD_ID,
                        saqgpm_backup_table.GOT_CODE,
                        saqgpm_backup_table.GOTCODE_RECORD_ID,
                        saqgpm_backup_table.GREENBOOK,
                        saqgpm_backup_table.GREENBOOK_RECORD_ID,
                        saqsco_backup_table.FABLOCATION_ID,
                        saqsco_backup_table.FABLOCATION_NAME,
                        saqsco_backup_table.FABLOCATION_RECORD_ID,
                        saqgpm_backup_table.PM_ID,
                        saqgpm_backup_table.PM_NAME,
                        saqgpm_backup_table.PM_RECORD_ID,
                        saqgpm_backup_table.MNTEVT_LEVEL,
                        saqgpm_backup_table.SERVICE_ID,
                        saqgpm_backup_table.SERVICE_DESCRIPTION,
                        saqgpm_backup_table.SERVICE_RECORD_ID,
                        MAEAPM_INBOUND.PM_FREQUENCY,
                        MAEAPM_INBOUND.PM_FREQUENCY AS SSCM_PM_FREQUENCY,
                        MAEAPM_INBOUND.CLEAN_COATING AS CLEAN_COATING,
                        saqgpm_backup_table.PM_FREQUENCY_EDITABLE,
                        saqgpm_backup_table.PROCESS_TYPE,
                        saqgpm_backup_table.DEVICE_NODE,
                        saqgpm_backup_table.KIT_ID,
                        saqgpm_backup_table.KIT_NAME,
                        MAEAPM_INBOUND.KIT_NUMBER,
                        MATKTN.TOOL_KIT_NUMBER_RECORD_ID,
                        saqgpm_backup_table.KIT_RECORD_ID,
                        saqgpm_backup_table.QUOTE_ID,
                        saqgpm_backup_table.QUOTE_RECORD_ID,
                        saqgpm_backup_table.QTEREV_ID,
                        saqgpm_backup_table.QTEREV_RECORD_ID,
                        saqgpm_backup_table.QTESRV_RECORD_ID,
                        saqgpm_backup_table.QTESRVGBK_RECORD_ID,
                        saqgpm_backup_table.QTEREVPME_RECORD_ID,
                        saqsco_backup_table.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID as QTESRVCOB_RECORD_ID,
                        saqgpm_backup_table.TKM_FLAG as TKM_FLAG,
                        1 AS INCLUDED
                        FROM {saqgpm_backup_table} (NOLOCK)  saqgpm_backup_table
                    JOIN {saqsco_backup_table} (NOLOCK)  saqsco_backup_table ON saqgpm_backup_table.QUOTE_RECORD_ID = saqsco_backup_table.QUOTE_RECORD_ID AND saqgpm_backup_table.QTEREV_RECORD_ID = saqsco_backup_table.QTEREV_RECORD_ID AND saqgpm_backup_table.SERVICE_RECORD_ID = saqsco_backup_table.SERVICE_RECORD_ID and saqgpm_backup_table.GREENBOOK = saqsco_backup_table.GREENBOOK
                    JOIN MAEQUP(NOLOCK) ON MAEQUP.PAR_EQUIPMENT_RECORD_ID = saqsco_backup_table.EQUIPMENT_RECORD_ID AND MAEQUP.GOT_CODE = saqgpm_backup_table.GOT_CODE and isnull(MAEQUP.PROCESS_TYPE,'') = isnull(saqgpm_backup_table.PROCESS_TYPE,'') and isnull(MAEQUP.DEVICE_NODE,'') = isnull(saqgpm_backup_table.DEVICE_NODE,'')
                    JOIN MAEAPM_INBOUND(NOLOCK) ON MAEAPM_INBOUND.EQUIPMENT_ID = saqsco_backup_table.EQUIPMENT_ID AND MAEAPM_INBOUND.ASSEMBLY_ID = MAEQUP.EQUIPMENT_ID AND MAEAPM_INBOUND.PM_NAME = saqgpm_backup_table.PM_NAME AND MAEAPM_INBOUND.KIT_ID = saqgpm_backup_table.KIT_ID AND MAEAPM_INBOUND.QUOTE_ID = saqsco_backup_table.QUOTE_ID AND MAEAPM_INBOUND.QTEREV_ID = saqsco_backup_table.QTEREV_ID AND MAEAPM_INBOUND.SERVICE_ID = saqsco_backup_table.SERVICE_ID 
                    LEFT JOIN MATKTN ON MATKTN.KIT_NUMBER = MAEAPM_INBOUND.KIT_NUMBER AND MAEAPM_INBOUND.KIT_ID = MATKTN.KIT_ID
                    WHERE saqgpm_backup_table.QUOTE_RECORD_ID = '{QuoteRecordId}' AND 
                    saqgpm_backup_table.QTEREV_RECORD_ID = '{RevisionRecordId}' AND saqgpm_backup_table.QUOTE_RECORD_ID = '{QuoteRecordId}' AND saqgpm_backup_table.SERVICE_ID = '{TreeParam}' ) PM_EVENT_ASSEMBLY  LEFT JOIN SAQGPA (NOLOCK) AS ASSEMBLY ON PM_EVENT_ASSEMBLY.QUOTE_RECORD_ID = ASSEMBLY.QUOTE_RECORD_ID AND ASSEMBLY.QTEREV_RECORD_ID = PM_EVENT_ASSEMBLY.QTEREV_RECORD_ID AND ASSEMBLY.SERVICE_RECORD_ID = PM_EVENT_ASSEMBLY.SERVICE_RECORD_ID AND ASSEMBLY.GREENBOOK_RECORD_ID = PM_EVENT_ASSEMBLY.GREENBOOK_RECORD_ID AND ASSEMBLY.GOTCODE_RECORD_ID = PM_EVENT_ASSEMBLY.GOTCODE_RECORD_ID AND  ASSEMBLY.ASSEMBLY_RECORD_ID = PM_EVENT_ASSEMBLY.ASSEMBLY_RECORD_ID AND ASSEMBLY.EQUIPMENT_RECORD_ID = PM_EVENT_ASSEMBLY.EQUIPMENT_RECORD_ID AND  ASSEMBLY.PM_RECORD_ID = PM_EVENT_ASSEMBLY.PM_RECORD_ID AND PM_EVENT_ASSEMBLY.QTESRVCOB_RECORD_ID = ASSEMBLY.QTESRVCOB_RECORD_ID WHERE ISNULL(ASSEMBLY.ASSEMBLY_RECORD_ID,'') = '' """.format(
                    UserId=self.user_id,
                    UserName=self.user_name,
                    TreeParam=self.real_time_integration_service if self.real_time_integration_service else service_id,
                    QuoteId = self.contract_quote_id,
                    QuoteRecordId=self.contract_quote_record_id,
                    RevisionId=self.quote_revision_id,
                    saqgpm_backup_table = str(saqgpm_backup_table),
                    saqsco_backup_table = str(saqsco_backup_table),
                    RevisionRecordId=self.quote_revision_record_id
                    )
                )
            #INC08782102 - End - M
            #INC08696637 - Start - A
            Log.Info(
                """INSERT SAQGPA (
                        ASSEMBLY_ID,
                        ASSEMBLY_DESCRIPTION,
                        ASSEMBLY_RECORD_ID,
                        ASSEMBLY_STATUS,
                        EQUIPMENT_ID,
                        EQUIPMENT_DESCRIPTION,
                        EQUIPMENT_RECORD_ID,
                        EQUIPMENTTYPE_ID,
                        EQUIPMENTTYPE_RECORD_ID,
                        GOT_CODE,
                        GOTCODE_RECORD_ID,
                        GREENBOOK,
                        GREENBOOK_RECORD_ID,
                        PM_ID,
                        PM_NAME,
                        PM_RECORD_ID,
                        MNTEVT_LEVEL,
                        SERVICE_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_RECORD_ID,
                        PM_FREQUENCY,
                        SSCM_PM_FREQUENCY,
                        CLEAN_COAT_DIFF,
                        PM_FREQUENCY_EDITABLE,
                        PROCESS_TYPE,
                        DEVICE_NODE,
                        KIT_ID,
                        KIT_NAME,
                        KIT_NUMBER,
                        KITNUMBER_RECORD_ID,
                        KIT_RECORD_ID,
                        QUOTE_ID,
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        QTESRV_RECORD_ID,
                        QTESRVGBK_RECORD_ID,
                        QTEREVPME_RECORD_ID,
                        QTESRVCOB_RECORD_ID,
                        TKM_FLAG,
                        INCLUDED,
                        QUOTE_REV_PO_GRNBK_PM_EVEN_ASSEMBLIES_RECORD_ID,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED,
                        ADDUSR_RECORD_ID)
                        SELECT PM_EVENT_ASSEMBLY.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_GRNBK_PM_EVEN_ASSEMBLIES_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED ,{UserId} as ADDUSR_RECORD_ID FROM (SELECT DISTINCT 
                        MAEQUP.EQUIPMENT_ID AS ASSEMBLY_ID,
                        MAEQUP.EQUIPMENT_DESCRIPTION AS ASSEMBLY_DESCRIPTION,
                        MAEQUP.EQUIPMENT_RECORD_ID AS ASSEMBLY_RECORD_ID,
                        MAEQUP.EQUIPMENT_STATUS AS ASSEMBLY_STATUS,
                        saqsco_backup_table.EQUIPMENT_ID,
                        saqsco_backup_table.EQUIPMENT_DESCRIPTION,
                        saqsco_backup_table.EQUIPMENT_RECORD_ID,
                        MAEQUP.EQUIPMENTTYPE_ID,
                        MAEQUP.EQUIPMENTTYPE_RECORD_ID,
                        saqgpm_backup_table.GOT_CODE,
                        saqgpm_backup_table.GOTCODE_RECORD_ID,
                        saqgpm_backup_table.GREENBOOK,
                        saqgpm_backup_table.GREENBOOK_RECORD_ID,
                        saqgpm_backup_table.PM_ID,
                        saqgpm_backup_table.PM_NAME,
                        saqgpm_backup_table.PM_RECORD_ID,
                        saqgpm_backup_table.MNTEVT_LEVEL,
                        saqgpm_backup_table.SERVICE_ID,
                        saqgpm_backup_table.SERVICE_DESCRIPTION,
                        saqgpm_backup_table.SERVICE_RECORD_ID,
                        MAEAPM_INBOUND.PM_FREQUENCY,
                        MAEAPM_INBOUND.PM_FREQUENCY AS SSCM_PM_FREQUENCY,
                        MAEAPM_INBOUND.CLEAN_COATING AS CLEAN_COATING,
                        saqgpm_backup_table.PM_FREQUENCY_EDITABLE,
                        saqgpm_backup_table.PROCESS_TYPE,
                        saqgpm_backup_table.DEVICE_NODE,
                        saqgpm_backup_table.KIT_ID,
                        saqgpm_backup_table.KIT_NAME,
                        MAEAPM_INBOUND.KIT_NUMBER,
                        MATKTN.TOOL_KIT_NUMBER_RECORD_ID,
                        saqgpm_backup_table.KIT_RECORD_ID,
                        saqgpm_backup_table.QUOTE_ID,
                        saqgpm_backup_table.QUOTE_RECORD_ID,
                        saqgpm_backup_table.QTEREV_ID,
                        saqgpm_backup_table.QTEREV_RECORD_ID,
                        saqgpm_backup_table.QTESRV_RECORD_ID,
                        saqgpm_backup_table.QTESRVGBK_RECORD_ID,
                        saqgpm_backup_table.QTEREVPME_RECORD_ID,
                        saqsco_backup_table.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID as QTESRVCOB_RECORD_ID,
                        saqgpm_backup_table.TKM_FLAG as TKM_FLAG,
                        1 AS INCLUDED
                        FROM {saqgpm_backup_table} (NOLOCK)  saqgpm_backup_table
                    JOIN {saqsco_backup_table} (NOLOCK)  saqsco_backup_table ON saqgpm_backup_table.QUOTE_RECORD_ID = saqsco_backup_table.QUOTE_RECORD_ID AND saqgpm_backup_table.QTEREV_RECORD_ID = saqsco_backup_table.QTEREV_RECORD_ID AND saqgpm_backup_table.SERVICE_RECORD_ID = saqsco_backup_table.SERVICE_RECORD_ID and saqgpm_backup_table.GREENBOOK = saqsco_backup_table.GREENBOOK
                    JOIN MAEQUP(NOLOCK) ON MAEQUP.PAR_EQUIPMENT_RECORD_ID = saqsco_backup_table.EQUIPMENT_RECORD_ID AND MAEQUP.GOT_CODE = saqgpm_backup_table.GOT_CODE and isnull(MAEQUP.PROCESS_TYPE,'') = isnull(saqgpm_backup_table.PROCESS_TYPE,'') and isnull(MAEQUP.DEVICE_NODE,'') = isnull(saqgpm_backup_table.DEVICE_NODE,'')
                    JOIN MAEAPM_INBOUND(NOLOCK) ON MAEAPM_INBOUND.EQUIPMENT_ID = saqsco_backup_table.EQUIPMENT_ID AND MAEAPM_INBOUND.ASSEMBLY_ID = MAEQUP.EQUIPMENT_ID AND MAEAPM_INBOUND.PM_NAME = saqgpm_backup_table.PM_NAME AND MAEAPM_INBOUND.KIT_ID = saqgpm_backup_table.KIT_ID AND MAEAPM_INBOUND.QUOTE_ID = saqsco_backup_table.QUOTE_ID AND MAEAPM_INBOUND.QTEREV_ID = saqsco_backup_table.QTEREV_ID AND MAEAPM_INBOUND.SERVICE_ID = saqsco_backup_table.SERVICE_ID 
                    LEFT JOIN MATKTN ON MATKTN.KIT_NUMBER = MAEAPM_INBOUND.KIT_NUMBER AND MAEAPM_INBOUND.KIT_ID = MATKTN.KIT_ID
                    WHERE saqgpm_backup_table.QUOTE_RECORD_ID = '{QuoteRecordId}' AND 
                    saqgpm_backup_table.QTEREV_RECORD_ID = '{RevisionRecordId}' AND saqgpm_backup_table.QUOTE_RECORD_ID = '{QuoteRecordId}' AND saqgpm_backup_table.SERVICE_ID = '{TreeParam}' ) PM_EVENT_ASSEMBLY  LEFT JOIN SAQGPA (NOLOCK) AS ASSEMBLY ON PM_EVENT_ASSEMBLY.QUOTE_RECORD_ID = ASSEMBLY.QUOTE_RECORD_ID AND ASSEMBLY.QTEREV_RECORD_ID = PM_EVENT_ASSEMBLY.QTEREV_RECORD_ID AND ASSEMBLY.SERVICE_RECORD_ID = PM_EVENT_ASSEMBLY.SERVICE_RECORD_ID AND ASSEMBLY.GREENBOOK_RECORD_ID = PM_EVENT_ASSEMBLY.GREENBOOK_RECORD_ID AND ASSEMBLY.GOTCODE_RECORD_ID = PM_EVENT_ASSEMBLY.GOTCODE_RECORD_ID AND  ASSEMBLY.ASSEMBLY_RECORD_ID = PM_EVENT_ASSEMBLY.ASSEMBLY_RECORD_ID AND ASSEMBLY.EQUIPMENT_RECORD_ID = PM_EVENT_ASSEMBLY.EQUIPMENT_RECORD_ID AND  ASSEMBLY.PM_RECORD_ID = PM_EVENT_ASSEMBLY.PM_RECORD_ID WHERE ISNULL(ASSEMBLY.ASSEMBLY_RECORD_ID,'') = '' """.format(
                    UserId=self.user_id,
                    UserName=self.user_name,
                    TreeParam=self.real_time_integration_service if self.real_time_integration_service else service_id,
                    QuoteId = self.contract_quote_id,
                    QuoteRecordId=self.contract_quote_record_id,
                    RevisionId=self.quote_revision_id,
                    saqgpm_backup_table = str(saqgpm_backup_table),
                    saqsco_backup_table = str(saqsco_backup_table),
                    RevisionRecordId=self.quote_revision_record_id
                    )
                )
            #INC08696637 - End - A
            #INC08664376 - End - M
            ##HPQC DEFECT 471 code ends...
            #INC08743915 - Start M Replace maequp/saqgpa equipment join condition
            # Sql.RunQuery("""UPDATE SAQGPA SET FABLOCATION_ID = MAEQUP.FABLOCATION_ID,
            #                 FABLOCATION_NAME = MAEQUP.FABLOCATION_NAME,
            #                 FABLOCATION_RECORD_ID = MAEQUP.FABLOCATION_RECORD_ID		
            #                 FROM SAQGPA(NOLOCK) JOIN MAEQUP(NOLOCK) ON MAEQUP.EQUIPMENT_RECORD_ID = SAQGPA.EQUIPMENT_RECORD_ID WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPA.SERVICE_ID = '{TreeParam}' AND ISNULL(SAQGPA.FABLOCATION_RECORD_ID,'') = '' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam=self.real_time_integration_service if self.real_time_integration_service else service_id))
            #INC08743915 - End M
            #INC08638619 - Start - M
            #INC08664376 - Start - M
            # Sql.RunQuery("""UPDATE SAQGPA
            #     SET PROCESS_TYPE = MAEQUP.PROCESS_TYPE,
            #         DEVICE_NODE = MAEQUP.DEVICE_NODE		
            #         FROM SAQGPA (NOLOCK) JOIN MAEQUP (NOLOCK) ON MAEQUP.PAR_EQUIPMENT_RECORD_ID = SAQGPA.EQUIPMENT_RECORD_ID AND 
            #         MAEQUP.EQUIPMENT_ID = SAQGPA.ASSEMBLY_ID WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPA.SERVICE_ID = '{TreeParam}'  """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam=self.tree_param))
            #INC08664376 - End - M
            #INC08638619 - End - M
            #drop_saqgpm_backup_table = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(saqgpm_backup_table)+"'' ) BEGIN DROP TABLE "+str(saqgpm_backup_table)+" END  ' ")

            #drop_saqsco_backup_table = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(saqsco_backup_table)+"'' ) BEGIN DROP TABLE "+str(saqsco_backup_table)+" END  ' ")
            ##HPQC 526 code starts...
            #INC08664376 - Start - M
            # Sql.RunQuery("""UPDATE SAQGPM
            #             SET
            #             DEVICE_NODE = assembly.DEVICE_NODE
            #             FROM SAQGPM (NOLOCK)
            #             INNER JOIN (select QTEREVPME_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_RECORD_ID,GOTCODE_RECORD_ID,PM_RECORD_ID,DEVICE_NODE,PROCESS_TYPE FROM SAQGPA where SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' and SAQGPA.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPA.SERVICE_ID = '{TreeParam}' GROUP BY QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_RECORD_ID,GOTCODE_RECORD_ID,PM_RECORD_ID,DEVICE_NODE,PROCESS_TYPE,QTEREVPME_RECORD_ID) assembly ON SAQGPM.QUOTE_RECORD_ID = assembly.QUOTE_RECORD_ID AND SAQGPM.QTEREV_RECORD_ID = assembly.QTEREV_RECORD_ID  AND  SAQGPM.QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID = assembly.QTEREVPME_RECORD_ID WHERE SAQGPM.QUOTE_RECORD_ID = '{QuoteRecordId}' and SAQGPM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPM.SERVICE_ID = '{TreeParam}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam=self.real_time_integration_service if self.real_time_integration_service else self.tree_param, pm_level_value = ('Scheduled Maintenance','Sched Maint','Chamber / Module PM') if(kwargs.get('quote_type_attribute_value').upper() != "TOOL BASED") else ('Scheduled Maintenance','Chamber / Module PM','Corrective Maintenance')))
            #INC08664376 - End - M
            ##HPQC 526  code ends...
            ##query to update the sscm frequency and pm frequency after inserting the saqgpa table
            Sql.RunQuery("""UPDATE SAQGPM
                        SET
                        PM_FREQUENCY = assembly.PM_FREQUENCY,
                        SSCM_PM_FREQUENCY = assembly.SSCM_PM_FREQUENCY
                        FROM SAQGPM (NOLOCK)
                        INNER JOIN (select SAQGPA.QTEREVPME_RECORD_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.SERVICE_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.PM_RECORD_ID,ISNULL(SAQGPA.DEVICE_NODE,'') AS DEVICE_NODE,ISNULL(SAQGPA.PROCESS_TYPE,'') AS PROCESS_TYPE,SUM(ISNULL(SAQGPA.PM_FREQUENCY, 0)) as PM_FREQUENCY,SUM(ISNULL(SAQGPA.SSCM_PM_FREQUENCY, 0)) as SSCM_PM_FREQUENCY FROM SAQGPA where SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' and SAQGPA.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPA.SERVICE_ID = '{TreeParam}' GROUP BY QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_RECORD_ID,GOTCODE_RECORD_ID,PM_RECORD_ID,ISNULL(SAQGPA.DEVICE_NODE,''),ISNULL(SAQGPA.PROCESS_TYPE,''),GREENBOOK_RECORD_ID,QTEREVPME_RECORD_ID) assembly ON SAQGPM.QUOTE_RECORD_ID = assembly.QUOTE_RECORD_ID AND SAQGPM.QTEREV_RECORD_ID = assembly.QTEREV_RECORD_ID  AND SAQGPM.QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID = assembly.QTEREVPME_RECORD_ID WHERE SAQGPM.QUOTE_RECORD_ID = '{QuoteRecordId}' and SAQGPM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPM.SERVICE_ID = '{TreeParam}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam=self.real_time_integration_service if self.real_time_integration_service else service_id))

            self._process_query(
                """INSERT SAQSKP (
                        ASSEMBLY_ID,
                        ASSEMBLY_DESCRIPTION,
                        ASSEMBLY_RECORD_ID,
                        EQUIPMENT_ID,
                        EQUIPMENT_DESCRIPTION,
                        EQUIPMENT_RECORD_ID,
                        PART_NUMBER,
                        PART_DESCRIPTION,
                        PART_RECORD_ID,
                        QUANTITY,
                        PM_ID,
                        PM_NAME,
                        PM_RECORD_ID,
                        KIT_ID,
                        KIT_RECORD_ID,
                        KIT_NUMBER,
                        KIT_NUMBER_RECORD_ID,
                        QUOTE_ID,
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_ID,
                        SERVICE_RECORD_ID,
                        QTEGBKPME_RECORD_ID,
                        QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED
                    ) 
                    SELECT KP.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
                        SELECT DISTINCT
                        SAQGPA.ASSEMBLY_ID,
                        SAQGPA.ASSEMBLY_DESCRIPTION,
                        SAQGPA.ASSEMBLY_RECORD_ID,
                        SAQGPA.EQUIPMENT_ID,
                        SAQGPA.EQUIPMENT_DESCRIPTION,
                        SAQGPA.EQUIPMENT_RECORD_ID,
                        MAKTPT_INBOUND.PART_NUMBER,
                        MAMTRL.SAP_DESCRIPTION,
                        MAMTRL.MATERIAL_RECORD_ID,
                        MAKTPT_INBOUND.QUANTITY,
                        SAQGPA.PM_ID,
                        SAQGPA.PM_NAME,
                        SAQGPA.PM_RECORD_ID AS PM_RECORD_ID,
                        SAQGPA.KIT_ID,
                        SAQGPA.KIT_RECORD_ID,
                        SAQGPA.KIT_NUMBER,
                        SAQGPA.KITNUMBER_RECORD_ID,
                        '{QuoteId}' as QUOTE_ID,
                        '{QuoteRecordId}' as QUOTE_RECORD_ID,
                        '{RevisionId}' as QTEREV_ID,
                        '{RevisionRecordId}' as QTEREV_RECORD_ID,
                        SAQGPA.SERVICE_DESCRIPTION,
                        SAQGPA.SERVICE_ID,
                        SAQGPA.SERVICE_RECORD_ID,
                        SAQGPA.QTEREVPME_RECORD_ID
                        FROM
                        SAQGPA(NOLOCK)
                        JOIN MAKTPT(NOLOCK) ON MAKTPT.KIT_ID = SAQGPA.KIT_ID
                        JOIN MAKTPT_INBOUND(NOLOCK) ON MAKTPT_INBOUND.KIT_ID = SAQGPA.KIT_ID AND MAKTPT_INBOUND.QUOTE_ID = SAQGPA.QUOTE_ID AND MAKTPT_INBOUND.QTEREV_ID = SAQGPA.QTEREV_ID AND MAKTPT_INBOUND.SERVICE_ID = SAQGPA.SERVICE_ID AND MAKTPT_INBOUND.PART_NUMBER = MAKTPT.PART_NUMBER
                        JOIN MAMTRL(NOLOCK) ON MAMTRL.SAP_PART_NUMBER = MAKTPT.PART_NUMBER
                    WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPA.SERVICE_ID = '{TreeParam}') KP LEFT JOIN SAQSKP (NOLOCK) AS KIT ON 
                    KP.QUOTE_RECORD_ID =KIT.QUOTE_RECORD_ID AND KP.QTEREV_RECORD_ID =KIT.QTEREV_RECORD_ID AND KP.SERVICE_RECORD_ID =KIT.SERVICE_RECORD_ID AND KP.SERVICE_RECORD_ID =KIT.SERVICE_RECORD_ID AND KP.EQUIPMENT_RECORD_ID =KIT.EQUIPMENT_RECORD_ID  AND KP.ASSEMBLY_RECORD_ID =KIT.ASSEMBLY_RECORD_ID AND KP.PM_RECORD_ID =KIT.PM_RECORD_ID AND KP.KIT_RECORD_ID =KIT.KIT_RECORD_ID  AND KP.KITNUMBER_RECORD_ID =KIT.KIT_NUMBER_RECORD_ID WHERE ISNULL(KIT.KIT_RECORD_ID,'') = '' """.format(
                    UserName=self.user_name,
                    TreeParam=self.real_time_integration_service if self.real_time_integration_service else service_id,
                    QuoteId = self.contract_quote_id,
                    QuoteRecordId=self.contract_quote_record_id,
                    RevisionId=self.quote_revision_id,
                    RevisionRecordId=self.quote_revision_record_id
                    ))
            #INC08709720 - Start - M
            self._process_query("""INSERT SAQGPE (
                    CPS_CONFIGURATION_ID,
                    CPS_MATCH_ID,
                    --ENTITLEMENT_XML,
                    SERVICE_ID,
                    SERVICE_RECORD_ID,
                    GOT_CODE,
                    GOTCODE_RECORD_ID,
                    GREENBOOK,
                    GREENBOOK_RECORD_ID,
                    KB_VERSION,
                    PM_ID,
                    KIT_ID,
                    KIT_NUMBER,
                    KITNUMBER_RECORD_ID,
                    KIT_RECORD_ID,
                    PM_RECORD_ID,
                    QUOTE_ID,
                    QUOTE_RECORD_ID,
                    QTEREV_ID,
                    QTEREV_RECORD_ID,
                    QTEGBKENT_RECORD_ID,
                    QTEGGTPME_RECORD_ID,
                    QUOTE_REV_GOT_CD_PM_EVNT_ENTITLEMENTS_RECORD_ID,
                    CPQTABLEENTRYADDEDBY,
                    CPQTABLEENTRYDATEADDED
                    ) 
                    SELECT pm_entitlement.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_GOT_CD_PM_EVNT_ENTITLEMENTS_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(SELECT DISTINCT 
                    SAQSGE.CPS_CONFIGURATION_ID,
                    SAQSGE.CPS_MATCH_ID,
                    --SAQSGE.ENTITLEMENT_XML,
                    SAQGPM.SERVICE_ID,
                    SAQGPM.SERVICE_RECORD_ID,
                    SAQGPM.GOT_CODE,
                    SAQGPM.GOTCODE_RECORD_ID,
                    SAQGPM.GREENBOOK,
                    SAQGPM.GREENBOOK_RECORD_ID,
                    SAQSGE.KB_VERSION,
                    SAQGPM.PM_ID,
                    SAQGPM.KIT_ID,
                    SAQGPM.KIT_NUMBER,
                    SAQGPM.KITNUMBER_RECORD_ID,
                    SAQGPM.KIT_RECORD_ID,
                    SAQGPM.PM_RECORD_ID,
                    SAQGPM.QUOTE_ID,
                    SAQGPM.QUOTE_RECORD_ID,
                    SAQGPM.QTEREV_ID,
                    SAQGPM.QTEREV_RECORD_ID,
                    SAQSGE.QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID as QTEGBKENT_RECORD_ID,
                    SAQGPM.QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID as QTEGGTPME_RECORD_ID
                    FROM SAQSGE (NOLOCK)
                    JOIN SAQGPM(NOLOCK) ON SAQGPM.QUOTE_RECORD_ID = SAQSGE.QUOTE_RECORD_ID AND SAQGPM.QTEREV_RECORD_ID = SAQSGE.QTEREV_RECORD_ID 
                    AND SAQGPM.SERVICE_RECORD_ID = SAQSGE.SERVICE_RECORD_ID AND SAQGPM.GREENBOOK_RECORD_ID = SAQSGE.GREENBOOK_RECORD_ID
                    WHERE SAQSGE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSGE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPM.SERVICE_ID = '{TreeParam}' )pm_entitlement LEFT JOIN SAQGPE (NOLOCK) AS EVENT_ENTITLEMENT ON pm_entitlement.QUOTE_RECORD_ID = EVENT_ENTITLEMENT.QUOTE_RECORD_ID  AND pm_entitlement.QTEREV_RECORD_ID = EVENT_ENTITLEMENT.QTEREV_RECORD_ID AND pm_entitlement.GREENBOOK_RECORD_ID = EVENT_ENTITLEMENT.GREENBOOK_RECORD_ID AND pm_entitlement.GOTCODE_RECORD_ID = EVENT_ENTITLEMENT.GOTCODE_RECORD_ID AND pm_entitlement.PM_RECORD_ID = EVENT_ENTITLEMENT.PM_RECORD_ID AND pm_entitlement.QTEGGTPME_RECORD_ID = EVENT_ENTITLEMENT.QTEGGTPME_RECORD_ID WHERE ISNULL(EVENT_ENTITLEMENT.QTEGGTPME_RECORD_ID,'') = '' """.format(
                    UserName=self.user_name,
                    TreeParam=self.real_time_integration_service if self.real_time_integration_service else service_id,
                    QuoteId = self.contract_quote_id,
                    QuoteRecordId=self.contract_quote_record_id,
                    RevisionId=self.quote_revision_id,
                    RevisionRecordId=self.quote_revision_record_id)
                    )
            #INC08709720 - End - M
            #creating backup table for saqgpe table insert...
            saqsge_backup_table = "saqsge_backup_table_{}".format(self.contract_quote_id)  
            #INC08786125 - M
            drop_saqsge_backup_table = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS (NOLOCK) WHERE NAME= ''"+str(saqsge_backup_table)+"'' ) BEGIN DROP TABLE "+str(saqsge_backup_table)+" END  ' ")


            saqsge_temp_table_insert = SqlHelper.GetFirst("sp_executesql @T=N'SELECT SAQSGE.GREENBOOK,SAQSGE.GREENBOOK_RECORD_ID,SAQSGE.SERVICE_RECORD_ID,SAQSGE.QUOTE_RECORD_ID,SAQSGE.QTEREV_RECORD_ID,SAQSGE.QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,SAQSGE.ENTITLEMENT_XML,SAQSGE.CONFIGURATION_STATUS INTO "+str(saqsge_backup_table)+" FROM SAQSGE (NOLOCK) WHERE SAQSGE.QUOTE_RECORD_ID = ''{}'' AND SAQSGE.QTEREV_RECORD_ID = ''{}'' AND SAQSGE.SERVICE_ID = ''{}'' '".format(self.contract_quote_record_id,self.quote_revision_record_id,self.real_time_integration_service if self.real_time_integration_service else service_id))

            Sql.RunQuery("""UPDATE SAQGPE SET ENTITLEMENT_XML = saqsge_backup_table.ENTITLEMENT_XML,CONFIGURATION_STATUS = saqsge_backup_table.CONFIGURATION_STATUS FROM  {saqsge_backup_table} (NOLOCK)  saqsge_backup_table JOIN SAQGPE ON saqsge_backup_table.QUOTE_RECORD_ID = SAQGPE.QUOTE_RECORD_ID AND saqsge_backup_table.QTEREV_RECORD_ID = SAQGPE.QTEREV_RECORD_ID AND saqsge_backup_table.SERVICE_RECORD_ID = SAQGPE.SERVICE_RECORD_ID AND saqsge_backup_table.GREENBOOK_RECORD_ID = SAQGPE.GREENBOOK_RECORD_ID WHERE SAQGPE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPE.SERVICE_ID = '{TreeParam}' AND ISNULL(SAQGPE.ENTITLEMENT_XML,'') = '' """.format(saqsge_backup_table = str(saqsge_backup_table),QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam=self.real_time_integration_service if self.real_time_integration_service else service_id))
            #INC08786125 - M
            drop_saqsge_backup_table = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS (NOLOCK) WHERE NAME= ''"+str(saqsge_backup_table)+"'' ) BEGIN DROP TABLE "+str(saqsge_backup_table)+" END  ' ")
            #SAQGPE Entitlement col update
            if self.real_time_integration_service:
                try:
                    where_condition = " WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND SERVICE_ID = '{}' ".format(self.contract_quote_record_id, self.quote_revision_record_id,self.real_time_integration_service)
                    ##SAQGPE ent columns update
                    ScriptExecutor.ExecuteGlobal("CQENTLNVAL", {'action':'ENTITLEMENT_COLUMN_UPDATE',
                                                                        'partnumber':self.real_time_integration_service,
                                                                        'where_cond' :where_condition, 
                                                                        'ent_level_table': "SAQGPE"
                                                                        })
                except:
                    Log.Info("SAQGPE UPDATE ERROR")
        else:
            #Log.Info("INSIDE ELSE TO CHECK FOR REVISION")
            #INC08696637 - Start - M
            self._process_query("""INSERT SAQRGG (
                    GOT_CODE,
                    GOTCODE_RECORD_ID,
                    GREENBOOK,
                    GREENBOOK_RECORD_ID,
                    SERVICE_ID,
                    SERVICE_DESCRIPTION,
                    SERVICE_RECORD_ID,
                    QUOTE_ID,
                    QUOTE_RECORD_ID,
                    QTEREV_ID,
                    QTEREV_RECORD_ID,
                    QTESRV_RECORD_ID,
                    QTESRVGBK_RECORD_ID,
                    QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID,
                    CPQTABLEENTRYADDEDBY,
                    CPQTABLEENTRYDATEADDED
                    )SELECT gotcode.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(
                    SELECT DISTINCT  
                    MAEQUP.GOT_CODE,
                    SAGTCD.GOT_CODES_RECORD_ID,
                    SAQSCO.GREENBOOK,
                    SAQSCO.GREENBOOK_RECORD_ID,
                    SAQSCO.SERVICE_ID,
                    SAQSCO.SERVICE_DESCRIPTION,
                    SAQSCO.SERVICE_RECORD_ID,
                    '{QuoteId}' as QUOTE_ID,
                    '{QuoteRecordId}' as QUOTE_RECORD_ID,
                    '{RevisionId}' as QTEREV_ID,
                    '{RevisionRecordId}' as QTEREV_RECORD_ID,
                    SAQTSV.QUOTE_SERVICE_RECORD_ID as QTESRV_RECORD_ID,
                    SAQSGB.QUOTE_SERVICE_GREENBOOK_RECORD_ID as QTESRVGBK_RECORD_ID
                    FROM SYSPBT (NOLOCK) 
                    JOIN SAQSCO(NOLOCK) ON SAQSCO.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQSCO.EQUIPMENT_RECORD_ID = SYSPBT.BATCH_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SYSPBT.QTEREV_RECORD_ID
                    JOIN MAEQUP(NOLOCK) ON MAEQUP.PAR_EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID
                    JOIN SAQTSV(NOLOCK) ON SAQTSV.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQSCO.SERVICE_RECORD_ID = SAQTSV.SERVICE_RECORD_ID
                    JOIN SAQSGB(NOLOCK) ON SAQSGB.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQSGB.QTEREV_RECORD_ID AND SAQSCO.GREENBOOK_RECORD_ID = SAQSGB.GREENBOOK_RECORD_ID AND SAQSCO.SERVICE_RECORD_ID = SAQSGB.SERVICE_RECORD_ID
                    JOIN SAGTCD(NOLOCK) ON MAEQUP.GOT_CODE = SAGTCD.GOT_CODE
                    JOIN SAQTRV(NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID 
                    WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCO.SERVICE_ID = '{TreeParam}' ) gotcode LEFT JOIN SAQRGG (nolock) as pmsa_gotcode on  gotcode.QUOTE_RECORD_ID = pmsa_gotcode.QUOTE_RECORD_ID and gotcode.QTEREV_RECORD_ID = pmsa_gotcode.QTEREV_RECORD_ID and gotcode.SERVICE_RECORD_ID = pmsa_gotcode.SERVICE_RECORD_ID and gotcode.GREENBOOK_RECORD_ID = pmsa_gotcode.GREENBOOK_RECORD_ID and gotcode.GOT_CODES_RECORD_ID = pmsa_gotcode.GOTCODE_RECORD_ID WHERE ISNULL(pmsa_gotcode.GOTCODE_RECORD_ID,'') = '' """.format(
                    UserName=self.user_name,
                    TreeParam=service_id,
                    QuoteId = self.contract_quote_id,
                    QuoteRecordId=self.contract_quote_record_id,
                    RevisionId=self.quote_revision_id,
                    RevisionRecordId=self.quote_revision_record_id,
                    BatchGroupRecordId=kwargs.get('batch_group_record_id')
                    )
                )
            #INC08696637 - End - M
            ##A055S000P01-17959 inserting the device node and process type as null by default...##HPQC DEFECT 471 Events not inserting issue , changed the join condition for saqgpm table insert...
            #INC08664376,INC08696637 - Start - M
            self._process_query("""INSERT SAQGPM(CHAMBER_QUANTITY,
                    GOT_CODE,
                    GOTCODE_RECORD_ID,
                    GREENBOOK,
                    GREENBOOK_RECORD_ID,
                    PM_ID,
                    PM_NAME,
                    PM_RECORD_ID,
                    MNTEVT_LEVEL,
                    KIT_ID,
                    KIT_NAME,
                    KIT_RECORD_ID,
                    SERVICE_ID,
                    SERVICE_DESCRIPTION,
                    SERVICE_RECORD_ID,
                    PM_FREQUENCY_EDITABLE,
                    PROCESS_TYPE,
                    DEVICE_NODE,
                    QUOTE_ID,
                    QUOTE_RECORD_ID,
                    QTEREV_ID,
                    QTEREV_RECORD_ID,
                    QTESRV_RECORD_ID,
                    QTESRVGBK_RECORD_ID,
                    QTEREVGOT_RECORD_ID,
                    TKM_FLAG,
                    QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID,
                    CPQTABLEENTRYADDEDBY,
                    CPQTABLEENTRYDATEADDED
                    )SELECT DISTINCT pmsa_pmevents.CHAMBER_QUANTITY,
                    pmsa_pmevents.GOT_CODE,
                    pmsa_pmevents.GOTCODE_RECORD_ID,
                    pmsa_pmevents.GREENBOOK,
                    pmsa_pmevents.GREENBOOK_RECORD_ID,
                    pmsa_pmevents.PM_ID,
                    pmsa_pmevents.PM_NAME,
                    pmsa_pmevents.PM_RECORD_ID,
                    pmsa_pmevents.PM_LEVEL,
                    pmsa_pmevents.KIT_ID,
                    pmsa_pmevents.KIT_NAME,
                    pmsa_pmevents.KIT_RECORD_ID,
                    pmsa_pmevents.SERVICE_ID,
                    pmsa_pmevents.SERVICE_DESCRIPTION,
                    pmsa_pmevents.SERVICE_RECORD_ID,
                    pmsa_pmevents.PM_FREQUENCY_EDITABLE,
                    pmsa_pmevents.PROCESS_TYPE,
                    pmsa_pmevents.DEVICE_NODE,
                    pmsa_pmevents.QUOTE_ID,
                    pmsa_pmevents.QUOTE_RECORD_ID,
                    pmsa_pmevents.QTEREV_ID,
                    pmsa_pmevents.QTEREV_RECORD_ID,
                    pmsa_pmevents.QTESRV_RECORD_ID,
                    pmsa_pmevents.QTESRVGBK_RECORD_ID,
                    pmsa_pmevents.QTEREVGOT_RECORD_ID,pmsa_pmevents.TKM_FLAG,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(
                    SELECT DISTINCT
                    0 as CHAMBER_QUANTITY,
                    SAQRGG.GOT_CODE,
                    SAQRGG.GOTCODE_RECORD_ID,
                    SAQRGG.GREENBOOK,
                    SAQRGG.GREENBOOK_RECORD_ID,
                    MAPMEV.PM_ID,
                    MAEAPM_INBOUND.PM_NAME,
                    MAPMEV.PM_RECORD_ID,
                    CASE WHEN MAEAPM_INBOUND.PM_LEVEL ='Sched Maint' THEN 'Scheduled Maintenance' ELSE MAEAPM_INBOUND.PM_LEVEL END AS PM_LEVEL ,
                    MAEAPM_INBOUND.KIT_ID,
                    MAMKIT.KIT_NAME,
                    MAMKIT.KIT_RECORD_ID,
                    SAQRGG.SERVICE_ID,
                    SAQRGG.SERVICE_DESCRIPTION,
                    SAQRGG.SERVICE_RECORD_ID,
                    MAEAPM_INBOUND.RFP_EDIT as PM_FREQUENCY_EDITABLE,
                    ISNULL(MAEQUP.PROCESS_TYPE,'') AS PROCESS_TYPE,
                    ISNULL(MAEQUP.DEVICE_NODE,'') AS DEVICE_NODE,
                    '{QuoteId}' as QUOTE_ID,
                    '{QuoteRecordId}' as QUOTE_RECORD_ID,
                    '{RevisionId}' as QTEREV_ID,
                    '{RevisionRecordId}' as QTEREV_RECORD_ID,
                    SAQRGG.QTESRV_RECORD_ID as QTESRV_RECORD_ID,
                    SAQRGG.QTESRVGBK_RECORD_ID as QTESRVGBK_RECORD_ID,
                    SAQRGG.QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID as QTEREVGOT_RECORD_ID,
                    {tkm_flag} as TKM_FLAG
                    FROM SYSPBT (NOLOCK) 
                    JOIN SAQRGG(NOLOCK) ON SAQRGG.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQRGG.QTEREV_RECORD_ID = SYSPBT.QTEREV_RECORD_ID
                    JOIN SAQSCA(NOLOCK) ON SAQRGG.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQRGG.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID
                    AND SAQRGG.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID AND SAQRGG.GREENBOOK_RECORD_ID = SAQSCA.GREENBOOK_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQSCA.EQUIPMENT_RECORD_ID
                    JOIN MAEQUP(NOLOCK) ON MAEQUP.PAR_EQUIPMENT_ID = SAQSCA.EQUIPMENT_ID AND MAEQUP.EQUIPMENT_ID = SAQSCA.ASSEMBLY_ID AND SAQRGG.GOT_CODE = MAEQUP.GOT_CODE
                    JOIN MAEAPM_INBOUND(NOLOCK) ON MAEAPM_INBOUND.QUOTE_ID = SAQSCA.QUOTE_ID AND MAEAPM_INBOUND.EQUIPMENT_ID = SAQSCA.EQUIPMENT_ID AND MAEAPM_INBOUND.QTEREV_ID = SAQSCA.QTEREV_ID AND MAEAPM_INBOUND.SERVICE_ID = SAQSCA.SERVICE_ID AND MAEQUP.EQUIPMENT_ID = MAEAPM_INBOUND.ASSEMBLY_ID
                    JOIN MAPMEV ON MAPMEV.PM_NAME = MAEAPM_INBOUND.PM_NAME AND MAPMEV.MNTEVT_LEVEL = MAEAPM_INBOUND.PM_LEVEL
                    {JoinString} MAMKIT ON MAMKIT.KIT_ID = MAEAPM_INBOUND.KIT_ID
                    WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.
                    QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRGG.SERVICE_ID = '{TreeParam}' AND  MAEAPM_INBOUND.PM_LEVEL IN {pm_level_value}) pmsa_pmevents  LEFT JOIN SAQGPM (NOLOCK) AS pm on pmsa_pmevents.QUOTE_RECORD_ID = pm.QUOTE_RECORD_ID AND pmsa_pmevents.QTEREV_RECORD_ID = pm.QTEREV_RECORD_ID AND pmsa_pmevents.SERVICE_RECORD_ID = pm.SERVICE_RECORD_ID AND pmsa_pmevents.GREENBOOK_RECORD_ID = pm.GREENBOOK_RECORD_ID and pmsa_pmevents.GOTCODE_RECORD_ID = pm.GOTCODE_RECORD_ID and pmsa_pmevents.PM_RECORD_ID = pm.PM_RECORD_ID and isnull(pmsa_pmevents.PROCESS_TYPE,'') = isnull(pm.PROCESS_TYPE,'') and isnull(pmsa_pmevents.DEVICE_NODE,'') = isnull(pm.DEVICE_NODE,'') AND ISNULL(pmsa_pmevents.KIT_ID,'') = ISNULL(pm.KIT_ID,'')
                    WHERE ISNULL(pm.PM_RECORD_ID,'') = '' """.format(
                    UserName=self.user_name,
                    TreeParam=self.real_time_integration_service if self.real_time_integration_service else service_id,
                    QuoteId = self.contract_quote_id,
                    QuoteRecordId=self.contract_quote_record_id,
                    RevisionId=self.quote_revision_id,
                    RevisionRecordId=self.quote_revision_record_id,
                    BatchGroupRecordId=kwargs.get('batch_group_record_id'),
                    pm_level_value = ('Scheduled Maintenance','Sched Maint','Chamber / Module PM') if(kwargs.get('quote_type_attribute_value').upper() != "TOOL BASED") else ('Scheduled Maintenance','Chamber / Module PM','Corrective Maintenance'),
                    tkm_flag = (1 if (str(service_id) == "Z0010" or str(self.real_time_integration_service) == "Z0010"  ) else 0),
                    JoinString = 'JOIN' if str(service_id) == "Z0010" else 'LEFT JOIN'
                    )
                )
            #INC08664376,INC08696637 - End - M
            ##Creating backup table for saqgpa table insert... 
            saqgpm_backup_table = "saqgpm_backup_table_{}".format(self.contract_quote_id) 
            #INC08786125 - M
            drop_saqgpm_backup_table = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS (NOLOCK) WHERE NAME= ''"+str(saqgpm_backup_table)+"'' ) BEGIN DROP TABLE "+str(saqgpm_backup_table)+" END  ' ")


            saqgpm_temp_table_insert = SqlHelper.GetFirst("sp_executesql @T=N'SELECT SAQGPM.GOT_CODE,SAQGPM.GOTCODE_RECORD_ID,SAQGPM.GREENBOOK,SAQGPM.GREENBOOK_RECORD_ID,SAQGPM.PM_ID,SAQGPM.PM_NAME,SAQGPM.PM_RECORD_ID,SAQGPM.TKM_FLAG,SAQGPM.MNTEVT_LEVEL,SAQGPM.SERVICE_ID,SAQGPM.SERVICE_DESCRIPTION,SAQGPM.SERVICE_RECORD_ID,SAQGPM.PM_FREQUENCY,SAQGPM.SSCM_PM_FREQUENCY,SAQGPM.PM_FREQUENCY_EDITABLE,SAQGPM.PROCESS_TYPE,SAQGPM.DEVICE_NODE,SAQGPM.QUOTE_ID,SAQGPM.QUOTE_RECORD_ID,SAQGPM.QTEREV_ID,SAQGPM.QTEREV_RECORD_ID,SAQGPM.QTESRV_RECORD_ID,SAQGPM.QTESRVGBK_RECORD_ID,SAQGPM.KIT_ID,SAQGPM.KIT_NAME,SAQGPM.KIT_NUMBER,SAQGPM.KITNUMBER_RECORD_ID,SAQGPM.KIT_RECORD_ID,SAQGPM.QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID as QTEREVPME_RECORD_ID INTO "+str(saqgpm_backup_table)+" FROM SAQGPM (NOLOCK) WHERE SAQGPM.QUOTE_RECORD_ID = ''{}'' AND SAQGPM.QTEREV_RECORD_ID = ''{}'' AND  SAQGPM.SERVICE_ID = ''{}'' '".format(self.contract_quote_record_id,self.quote_revision_record_id,self.real_time_integration_service if self.real_time_integration_service else service_id))


            saqsco_backup_table = "saqsco_backup_table_{}".format(self.contract_quote_id) 
            #INC08786125 - M
            drop_saqsco_backup_table = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS (NOLOCK) WHERE NAME= ''"+str(saqsco_backup_table)+"'' ) BEGIN DROP TABLE "+str(saqsco_backup_table)+" END  ' ")
            ##HPQC DEFECT 630 code starts...
            #HPQC 1917 -- added GREENBOOK AND GREENBOOK_RECORD_ID to insert and backup query
            saqsco_temp_table_insert = SqlHelper.GetFirst("sp_executesql @T=N'SELECT SAQSCO.QUOTE_RECORD_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQSCO.QTEREV_RECORD_ID,SAQSCO.QUOTE_ID,SAQSCO.QTEREV_ID,SAQSCO.SERVICE_RECORD_ID,SAQSCO.SERVICE_ID,SAQSCO.EQUIPMENT_ID,SAQSCO.EQUIPMENT_DESCRIPTION,SAQSCO.EQUIPMENT_RECORD_ID INTO "+str(saqsco_backup_table)+" FROM SAQSCO(NOLOCK) WHERE SAQSCO.QUOTE_RECORD_ID = ''{}'' AND SAQSCO.QTEREV_RECORD_ID = ''{}'' AND  SAQSCO.SERVICE_ID = ''{}'' '".format(self.contract_quote_record_id,self.quote_revision_record_id,self.real_time_integration_service if self.real_time_integration_service else service_id))
            ##HPQC DEFECT 630 code ends...
            ##HPQC DEFECT 471 and 630 code starts...
            #INC08664376,INC08709720,INC08782102,INC08865716,INC08871703 - Start - M  
            self._process_query(
                """INSERT SAQGPA (
                        ASSEMBLY_ID,
                        ASSEMBLY_DESCRIPTION,
                        ASSEMBLY_RECORD_ID,
                        ASSEMBLY_STATUS,
                        EQUIPMENT_ID,
                        EQUIPMENT_DESCRIPTION,
                        EQUIPMENT_RECORD_ID,
                        EQUIPMENTTYPE_ID,
                        EQUIPMENTTYPE_RECORD_ID,
                        GOT_CODE,
                        GOTCODE_RECORD_ID,
                        GREENBOOK,
                        GREENBOOK_RECORD_ID,
                        FABLOCATION_ID,
                        FABLOCATION_NAME,
                        FABLOCATION_RECORD_ID,
                        PM_ID,
                        PM_NAME,
                        PM_RECORD_ID,
                        MNTEVT_LEVEL,
                        SERVICE_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_RECORD_ID,
                        PM_FREQUENCY,
                        SSCM_PM_FREQUENCY,
                        CLEAN_COAT_DIFF,
                        PM_FREQUENCY_EDITABLE,
                        PROCESS_TYPE,
                        DEVICE_NODE,
                        KIT_ID,
                        KIT_NAME,
                        KIT_NUMBER,
                        KITNUMBER_RECORD_ID,
                        KIT_RECORD_ID,
                        QUOTE_ID,
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        QTESRV_RECORD_ID,
                        QTESRVGBK_RECORD_ID,
                        QTEREVPME_RECORD_ID,
                        QTESRVCOB_RECORD_ID,
                        TKM_FLAG,
                        INCLUDED,
                        QUOTE_REV_PO_GRNBK_PM_EVEN_ASSEMBLIES_RECORD_ID,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED,
                        ADDUSR_RECORD_ID)
                        SELECT PM_EVENT_ASSEMBLY.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_GRNBK_PM_EVEN_ASSEMBLIES_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED ,{UserId} as ADDUSR_RECORD_ID FROM (SELECT DISTINCT 
                        MAEQUP.EQUIPMENT_ID AS ASSEMBLY_ID,
                        MAEQUP.EQUIPMENT_DESCRIPTION AS ASSEMBLY_DESCRIPTION,
                        MAEQUP.EQUIPMENT_RECORD_ID AS ASSEMBLY_RECORD_ID,
                        MAEQUP.EQUIPMENT_STATUS AS ASSEMBLY_STATUS,
                        saqsco_backup_table.EQUIPMENT_ID,
                        saqsco_backup_table.EQUIPMENT_DESCRIPTION,
                        saqsco_backup_table.EQUIPMENT_RECORD_ID,
                        MAEQUP.EQUIPMENTTYPE_ID,
                        MAEQUP.EQUIPMENTTYPE_RECORD_ID,
                        saqgpm_backup_table.GOT_CODE,
                        saqgpm_backup_table.GOTCODE_RECORD_ID,
                        saqgpm_backup_table.GREENBOOK,
                        saqgpm_backup_table.GREENBOOK_RECORD_ID,
                        saqsco_backup_table.FABLOCATION_ID,
                        saqsco_backup_table.FABLOCATION_NAME,
                        saqsco_backup_table.FABLOCATION_RECORD_ID,
                        saqgpm_backup_table.PM_ID,
                        saqgpm_backup_table.PM_NAME,
                        saqgpm_backup_table.PM_RECORD_ID,
                        saqgpm_backup_table.MNTEVT_LEVEL,
                        saqgpm_backup_table.SERVICE_ID,
                        saqgpm_backup_table.SERVICE_DESCRIPTION,
                        saqgpm_backup_table.SERVICE_RECORD_ID,
                        MAEAPM_INBOUND.PM_FREQUENCY,
                        MAEAPM_INBOUND.PM_FREQUENCY AS SSCM_PM_FREQUENCY,
                        MAEAPM_INBOUND.CLEAN_COATING AS CLEAN_COATING,
                        saqgpm_backup_table.PM_FREQUENCY_EDITABLE,
                        saqgpm_backup_table.PROCESS_TYPE,
                        saqgpm_backup_table.DEVICE_NODE,
                        saqgpm_backup_table.KIT_ID,
                        saqgpm_backup_table.KIT_NAME,
                        MAEAPM_INBOUND.KIT_NUMBER,
                        MATKTN.TOOL_KIT_NUMBER_RECORD_ID,
                        saqgpm_backup_table.KIT_RECORD_ID,
                        saqgpm_backup_table.QUOTE_ID,
                        saqgpm_backup_table.QUOTE_RECORD_ID,
                        saqgpm_backup_table.QTEREV_ID,
                        saqgpm_backup_table.QTEREV_RECORD_ID,
                        saqgpm_backup_table.QTESRV_RECORD_ID,
                        saqgpm_backup_table.QTESRVGBK_RECORD_ID,
                        saqgpm_backup_table.QTEREVPME_RECORD_ID,
                        saqsco_backup_table.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID as QTESRVCOB_RECORD_ID,
                        saqgpm_backup_table.TKM_FLAG as TKM_FLAG,
                        1 AS INCLUDED
                        FROM SYSPBT(NOLOCK)
                    JOIN {saqgpm_backup_table} (NOLOCK)  saqgpm_backup_table ON SYSPBT.QUOTE_RECORD_ID = saqgpm_backup_table.QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = saqgpm_backup_table.QTEREV_RECORD_ID
                    JOIN {saqsco_backup_table} (NOLOCK)  saqsco_backup_table ON saqgpm_backup_table.QUOTE_RECORD_ID = saqsco_backup_table.QUOTE_RECORD_ID AND saqgpm_backup_table.QTEREV_RECORD_ID = saqsco_backup_table.QTEREV_RECORD_ID AND saqgpm_backup_table.SERVICE_RECORD_ID = saqsco_backup_table.SERVICE_RECORD_ID AND saqgpm_backup_table.GREENBOOK = saqsco_backup_table.GREENBOOK AND SYSPBT.BATCH_RECORD_ID = saqsco_backup_table.EQUIPMENT_RECORD_ID
                    JOIN MAEQUP(NOLOCK) ON MAEQUP.PAR_EQUIPMENT_RECORD_ID = saqsco_backup_table.EQUIPMENT_RECORD_ID AND MAEQUP.GOT_CODE = saqgpm_backup_table.GOT_CODE and isnull(MAEQUP.PROCESS_TYPE,'') = isnull(saqgpm_backup_table.PROCESS_TYPE,'') and isnull(MAEQUP.DEVICE_NODE,'') = isnull(saqgpm_backup_table.DEVICE_NODE,'')
                    JOIN MAEAPM_INBOUND(NOLOCK) ON MAEAPM_INBOUND.EQUIPMENT_ID = saqsco_backup_table.EQUIPMENT_ID AND MAEAPM_INBOUND.ASSEMBLY_ID = MAEQUP.EQUIPMENT_ID AND MAEAPM_INBOUND.PM_NAME = saqgpm_backup_table.PM_NAME AND MAEAPM_INBOUND.KIT_ID = saqgpm_backup_table.KIT_ID  AND MAEAPM_INBOUND.QUOTE_ID = saqsco_backup_table.QUOTE_ID AND MAEAPM_INBOUND.QTEREV_ID = saqsco_backup_table.QTEREV_ID AND MAEAPM_INBOUND.SERVICE_ID = saqsco_backup_table.SERVICE_ID
                    LEFT JOIN MATKTN ON MATKTN.KIT_NUMBER = MAEAPM_INBOUND.KIT_NUMBER AND MAEAPM_INBOUND.KIT_ID = MATKTN.KIT_ID
                    WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.
                    QTEREV_RECORD_ID = '{RevisionRecordId}' AND saqsco_backup_table.SERVICE_ID = '{TreeParam}') PM_EVENT_ASSEMBLY  
                LEFT JOIN SAQGPA (NOLOCK) AS ASSEMBLY ON PM_EVENT_ASSEMBLY.QUOTE_RECORD_ID = ASSEMBLY.QUOTE_RECORD_ID AND ASSEMBLY.QTEREV_RECORD_ID = PM_EVENT_ASSEMBLY.QTEREV_RECORD_ID AND ASSEMBLY.SERVICE_RECORD_ID = PM_EVENT_ASSEMBLY.SERVICE_RECORD_ID AND ASSEMBLY.GREENBOOK_RECORD_ID = PM_EVENT_ASSEMBLY.GREENBOOK_RECORD_ID AND ASSEMBLY.GOTCODE_RECORD_ID = PM_EVENT_ASSEMBLY.GOTCODE_RECORD_ID AND  ASSEMBLY.ASSEMBLY_RECORD_ID = PM_EVENT_ASSEMBLY.ASSEMBLY_RECORD_ID AND ASSEMBLY.EQUIPMENT_RECORD_ID = PM_EVENT_ASSEMBLY.EQUIPMENT_RECORD_ID AND  ASSEMBLY.PM_RECORD_ID = PM_EVENT_ASSEMBLY.PM_RECORD_ID AND PM_EVENT_ASSEMBLY.QTESRVCOB_RECORD_ID = ASSEMBLY.QTESRVCOB_RECORD_ID WHERE ISNULL(ASSEMBLY.ASSEMBLY_RECORD_ID,'') = '' """.format(
                    UserId=self.user_id,
                    UserName=self.user_name,
                    TreeParam=self.real_time_integration_service if self.real_time_integration_service else service_id,
                    QuoteId = self.contract_quote_id,
                    QuoteRecordId=self.contract_quote_record_id,
                    RevisionId=self.quote_revision_id,
                    RevisionRecordId=self.quote_revision_record_id,
                    saqgpm_backup_table = str(saqgpm_backup_table),
                    saqsco_backup_table = str(saqsco_backup_table),
                    BatchGroupRecordId=kwargs.get('batch_group_record_id')
                    )
                )
            #INC08782102 - End -M
            #INC08696637 - Start - A
            Log.Info(
                """INSERT SAQGPA (
                        ASSEMBLY_ID,
                        ASSEMBLY_DESCRIPTION,
                        ASSEMBLY_RECORD_ID,
                        ASSEMBLY_STATUS,
                        EQUIPMENT_ID,
                        EQUIPMENT_DESCRIPTION,
                        EQUIPMENT_RECORD_ID,
                        EQUIPMENTTYPE_ID,
                        EQUIPMENTTYPE_RECORD_ID,
                        GOT_CODE,
                        GOTCODE_RECORD_ID,
                        GREENBOOK,
                        GREENBOOK_RECORD_ID,
                        PM_ID,
                        PM_NAME,
                        PM_RECORD_ID,
                        MNTEVT_LEVEL,
                        SERVICE_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_RECORD_ID,
                        PM_FREQUENCY,
                        SSCM_PM_FREQUENCY,
                        CLEAN_COAT_DIFF,
                        PM_FREQUENCY_EDITABLE,
                        PROCESS_TYPE,
                        DEVICE_NODE,
                        KIT_ID,
                        KIT_NAME,
                        KIT_NUMBER,
                        KITNUMBER_RECORD_ID,
                        KIT_RECORD_ID,
                        QUOTE_ID,
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        QTESRV_RECORD_ID,
                        QTESRVGBK_RECORD_ID,
                        QTEREVPME_RECORD_ID,
                        QTESRVCOB_RECORD_ID,
                        TKM_FLAG,
                        INCLUDED,
                        QUOTE_REV_PO_GRNBK_PM_EVEN_ASSEMBLIES_RECORD_ID,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED,
                        ADDUSR_RECORD_ID)
                        SELECT PM_EVENT_ASSEMBLY.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_GRNBK_PM_EVEN_ASSEMBLIES_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED ,{UserId} as ADDUSR_RECORD_ID FROM (SELECT DISTINCT 
                        MAEQUP.EQUIPMENT_ID AS ASSEMBLY_ID,
                        MAEQUP.EQUIPMENT_DESCRIPTION AS ASSEMBLY_DESCRIPTION,
                        MAEQUP.EQUIPMENT_RECORD_ID AS ASSEMBLY_RECORD_ID,
                        MAEQUP.EQUIPMENT_STATUS AS ASSEMBLY_STATUS,
                        saqsco_backup_table.EQUIPMENT_ID,
                        saqsco_backup_table.EQUIPMENT_DESCRIPTION,
                        saqsco_backup_table.EQUIPMENT_RECORD_ID,
                        MAEQUP.EQUIPMENTTYPE_ID,
                        MAEQUP.EQUIPMENTTYPE_RECORD_ID,
                        saqgpm_backup_table.GOT_CODE,
                        saqgpm_backup_table.GOTCODE_RECORD_ID,
                        saqgpm_backup_table.GREENBOOK,
                        saqgpm_backup_table.GREENBOOK_RECORD_ID,
                        saqgpm_backup_table.PM_ID,
                        saqgpm_backup_table.PM_NAME,
                        saqgpm_backup_table.PM_RECORD_ID,
                        saqgpm_backup_table.MNTEVT_LEVEL,
                        saqgpm_backup_table.SERVICE_ID,
                        saqgpm_backup_table.SERVICE_DESCRIPTION,
                        saqgpm_backup_table.SERVICE_RECORD_ID,
                        MAEAPM_INBOUND.PM_FREQUENCY,
                        MAEAPM_INBOUND.PM_FREQUENCY AS SSCM_PM_FREQUENCY,
                        MAEAPM_INBOUND.CLEAN_COATING AS CLEAN_COATING,
                        saqgpm_backup_table.PM_FREQUENCY_EDITABLE,
                        saqgpm_backup_table.PROCESS_TYPE,
                        saqgpm_backup_table.DEVICE_NODE,
                        saqgpm_backup_table.KIT_ID,
                        saqgpm_backup_table.KIT_NAME,
                        MAEAPM_INBOUND.KIT_NUMBER,
                        MATKTN.TOOL_KIT_NUMBER_RECORD_ID,
                        saqgpm_backup_table.KIT_RECORD_ID,
                        saqgpm_backup_table.QUOTE_ID,
                        saqgpm_backup_table.QUOTE_RECORD_ID,
                        saqgpm_backup_table.QTEREV_ID,
                        saqgpm_backup_table.QTEREV_RECORD_ID,
                        saqgpm_backup_table.QTESRV_RECORD_ID,
                        saqgpm_backup_table.QTESRVGBK_RECORD_ID,
                        saqgpm_backup_table.QTEREVPME_RECORD_ID,
                        saqsco_backup_table.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID as QTESRVCOB_RECORD_ID,
                        saqgpm_backup_table.TKM_FLAG as TKM_FLAG,
                        1 AS INCLUDED
                        FROM SYSPBT(NOLOCK)
                    JOIN {saqgpm_backup_table} (NOLOCK)  saqgpm_backup_table ON SYSPBT.QUOTE_RECORD_ID = saqgpm_backup_table.QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = saqgpm_backup_table.QTEREV_RECORD_ID
                    JOIN {saqsco_backup_table} (NOLOCK)  saqsco_backup_table ON saqgpm_backup_table.QUOTE_RECORD_ID = saqsco_backup_table.QUOTE_RECORD_ID AND saqgpm_backup_table.QTEREV_RECORD_ID = saqsco_backup_table.QTEREV_RECORD_ID AND saqgpm_backup_table.SERVICE_RECORD_ID = saqsco_backup_table.SERVICE_RECORD_ID AND saqgpm_backup_table.GREENBOOK = saqsco_backup_table.GREENBOOK AND SYSPBT.BATCH_RECORD_ID = saqsco_backup_table.EQUIPMENT_RECORD_ID
                    JOIN MAEQUP(NOLOCK) ON MAEQUP.PAR_EQUIPMENT_RECORD_ID = saqsco_backup_table.EQUIPMENT_RECORD_ID AND MAEQUP.GOT_CODE = saqgpm_backup_table.GOT_CODE and isnull(MAEQUP.PROCESS_TYPE,'') = isnull(saqgpm_backup_table.PROCESS_TYPE,'') and isnull(MAEQUP.DEVICE_NODE,'') = isnull(saqgpm_backup_table.DEVICE_NODE,'')
                    JOIN MAEAPM_INBOUND(NOLOCK) ON MAEAPM_INBOUND.EQUIPMENT_ID = saqsco_backup_table.EQUIPMENT_ID AND MAEAPM_INBOUND.ASSEMBLY_ID = MAEQUP.EQUIPMENT_ID AND MAEAPM_INBOUND.PM_NAME = saqgpm_backup_table.PM_NAME AND MAEAPM_INBOUND.KIT_ID = saqgpm_backup_table.KIT_ID  AND MAEAPM_INBOUND.QUOTE_ID = saqsco_backup_table.QUOTE_ID AND MAEAPM_INBOUND.QTEREV_ID = saqsco_backup_table.QTEREV_ID AND MAEAPM_INBOUND.SERVICE_ID = saqsco_backup_table.SERVICE_ID
                    LEFT JOIN MATKTN ON MATKTN.KIT_NUMBER = MAEAPM_INBOUND.KIT_NUMBER AND MAEAPM_INBOUND.KIT_ID = MATKTN.KIT_ID
                    WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.
                    QTEREV_RECORD_ID = '{RevisionRecordId}' AND saqsco_backup_table.SERVICE_ID = '{TreeParam}') PM_EVENT_ASSEMBLY  
                LEFT JOIN SAQGPA (NOLOCK) AS ASSEMBLY ON PM_EVENT_ASSEMBLY.QUOTE_RECORD_ID = ASSEMBLY.QUOTE_RECORD_ID AND ASSEMBLY.QTEREV_RECORD_ID = PM_EVENT_ASSEMBLY.QTEREV_RECORD_ID AND ASSEMBLY.SERVICE_RECORD_ID = PM_EVENT_ASSEMBLY.SERVICE_RECORD_ID AND ASSEMBLY.GREENBOOK_RECORD_ID = PM_EVENT_ASSEMBLY.GREENBOOK_RECORD_ID AND ASSEMBLY.GOTCODE_RECORD_ID = PM_EVENT_ASSEMBLY.GOTCODE_RECORD_ID AND  ASSEMBLY.ASSEMBLY_RECORD_ID = PM_EVENT_ASSEMBLY.ASSEMBLY_RECORD_ID AND ASSEMBLY.EQUIPMENT_RECORD_ID = PM_EVENT_ASSEMBLY.EQUIPMENT_RECORD_ID AND  ASSEMBLY.PM_RECORD_ID = PM_EVENT_ASSEMBLY.PM_RECORD_ID WHERE ISNULL(ASSEMBLY.ASSEMBLY_RECORD_ID,'') = '' """.format(
                    UserId=self.user_id,
                    UserName=self.user_name,
                    TreeParam=self.real_time_integration_service if self.real_time_integration_service else service_id,
                    QuoteId = self.contract_quote_id,
                    QuoteRecordId=self.contract_quote_record_id,
                    RevisionId=self.quote_revision_id,
                    RevisionRecordId=self.quote_revision_record_id,
                    saqgpm_backup_table = str(saqgpm_backup_table),
                    saqsco_backup_table = str(saqsco_backup_table),
                    BatchGroupRecordId=kwargs.get('batch_group_record_id')
                    )
                )
            #INC08696637,INC08709720 - End - A
            #INC08664376 - End - M
            ##HPQC DEFECT 471 code ends...
            #INC08743915 - Start M Replace maequp/saqgpa equipment join condition
            Sql.RunQuery("""UPDATE SAQGPA SET FABLOCATION_ID = MAEQUP.FABLOCATION_ID,
                            FABLOCATION_NAME = MAEQUP.FABLOCATION_NAME,
                            FABLOCATION_RECORD_ID = MAEQUP.FABLOCATION_RECORD_ID		
                            FROM SAQGPA(NOLOCK) JOIN MAEQUP(NOLOCK) ON MAEQUP.EQUIPMENT_RECORD_ID = SAQGPA.EQUIPMENT_RECORD_ID WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPA.SERVICE_ID = '{TreeParam}' AND ISNULL(SAQGPA.FABLOCATION_RECORD_ID,'') = '' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam=self.real_time_integration_service if self.real_time_integration_service else self.tree_param))
            #INC08743915 - End M
            #INC08664376 - Start - M
            # Sql.RunQuery("""UPDATE SAQGPA
            #     SET PROCESS_TYPE = MAEQUP.PROCESS_TYPE,
            #         DEVICE_NODE = MAEQUP.DEVICE_NODE		
            #         FROM SAQGPA (NOLOCK) 
            #         JOIN MAEQUP (NOLOCK) ON MAEQUP.PAR_EQUIPMENT_RECORD_ID = SAQGPA.EQUIPMENT_RECORD_ID AND 
            #         MAEQUP.EQUIPMENT_ID = SAQGPA.ASSEMBLY_ID
            #         JOIN SYSPBT (NOLOCK) ON SYSPBT.QTEREV_RECORD_ID = SAQGPA.QTEREV_RECORD_ID AND 
            #         SYSPBT.QUOTE_RECORD_ID = SAQGPA.QUOTE_RECORD_ID
            #         WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPA.SERVICE_ID = '{TreeParam}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam=self.real_time_integration_service if self.tree_param in ('Revisions' or 'Quote Information') else self.tree_param,BatchGroupRecordId =kwargs.get('batch_group_record_id')))
            #INC08664376 - End - M
            ##query to update the sscm frequency and pm frequency after inserting the saqgpa table
            Sql.RunQuery("""UPDATE SAQGPM
                            SET
                            PM_FREQUENCY = assembly.PM_FREQUENCY,
                            SSCM_PM_FREQUENCY = assembly.SSCM_PM_FREQUENCY
                            FROM SAQGPM (NOLOCK)
                            INNER JOIN (select SAQGPA.QTEREVPME_RECORD_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.SERVICE_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.PM_RECORD_ID,ISNULL(SAQGPA.DEVICE_NODE,'') AS DEVICE_NODE,ISNULL(SAQGPA.PROCESS_TYPE,'') AS PROCESS_TYPE,SUM(ISNULL(SAQGPA.PM_FREQUENCY, 0)) as PM_FREQUENCY,SUM(ISNULL(SAQGPA.SSCM_PM_FREQUENCY, 0)) as SSCM_PM_FREQUENCY FROM SAQGPA where SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' and SAQGPA.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPA.SERVICE_ID = '{TreeParam}' GROUP BY QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_RECORD_ID,GOTCODE_RECORD_ID,PM_RECORD_ID,ISNULL(DEVICE_NODE,''),ISNULL(PROCESS_TYPE,''),GREENBOOK_RECORD_ID,QTEREVPME_RECORD_ID) assembly ON SAQGPM.QUOTE_RECORD_ID = assembly.QUOTE_RECORD_ID AND SAQGPM.QTEREV_RECORD_ID = assembly.QTEREV_RECORD_ID AND SAQGPM.QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID = assembly.QTEREVPME_RECORD_ID
                            JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQGPM.QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQGPM.QTEREV_RECORD_ID 
                            WHERE SAQGPM.QUOTE_RECORD_ID = '{QuoteRecordId}' and SAQGPM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPM.SERVICE_ID = '{TreeParam}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam=self.real_time_integration_service if self.real_time_integration_service else service_id,BatchGroupRecordId =kwargs.get('batch_group_record_id')))

            Sql.RunQuery("""UPDATE SAQGPM
                        SET
                        SAQGPM.CHAMBER_QUANTITY = assembly.cnt
                        FROM SAQGPM (NOLOCK)
                        INNER JOIN (select DISTINCT count(SAQGPA.QTEREVPME_RECORD_ID) as cnt,SAQGPA.QTEREVPME_RECORD_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID FROM saqgpa WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' and SAQGPA.QTEREV_RECORD_ID = '{RevisionRecordId}' GROUP BY SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.QTEREVPME_RECORD_ID) assembly ON SAQGPM.QUOTE_RECORD_ID = assembly.QUOTE_RECORD_ID AND SAQGPM.QTEREV_RECORD_ID = assembly.QTEREV_RECORD_ID AND SAQGPM.QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID = assembly.QTEREVPME_RECORD_ID WHERE SAQGPM.QUOTE_RECORD_ID = '{QuoteRecordId}' and SAQGPM.QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
            #INC08786125 - M
            drop_saqgpm_backup_table = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS (NOLOCK) WHERE NAME= ''"+str(saqgpm_backup_table)+"'' ) BEGIN DROP TABLE "+str(saqgpm_backup_table)+" END  ' ")
            #INC08786125 - M
            drop_saqsco_backup_table = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS (NOLOCK) WHERE NAME= ''"+str(saqsco_backup_table)+"'' ) BEGIN DROP TABLE "+str(saqsco_backup_table)+" END  ' ")
            ##HPQC 526 code starts..
            #INC08664376 - Start - M
            # Sql.RunQuery("""UPDATE SAQGPM
            #             SET
            #             DEVICE_NODE = assembly.DEVICE_NODE
            #             FROM SAQGPM (NOLOCK)
            #             INNER JOIN (select QTEREVPME_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_RECORD_ID,GOTCODE_RECORD_ID,PM_RECORD_ID,DEVICE_NODE,PROCESS_TYPE FROM SAQGPA where SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' and SAQGPA.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPA.SERVICE_ID = '{TreeParam}' GROUP BY QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_RECORD_ID,GOTCODE_RECORD_ID,PM_RECORD_ID,DEVICE_NODE,PROCESS_TYPE,QTEREVPME_RECORD_ID) assembly ON SAQGPM.QUOTE_RECORD_ID = assembly.QUOTE_RECORD_ID AND SAQGPM.QTEREV_RECORD_ID = assembly.QTEREV_RECORD_ID  AND  SAQGPM.QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID = assembly.QTEREVPME_RECORD_ID
            #             JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQGPM.QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQGPM.QTEREV_RECORD_ID
            #             WHERE SAQGPM.QUOTE_RECORD_ID = '{QuoteRecordId}' and SAQGPM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPM.SERVICE_ID = '{TreeParam}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam=self.real_time_integration_service if self.real_time_integration_service else self.tree_param,BatchGroupRecordId =kwargs.get('batch_group_record_id'), pm_level_value = ('Scheduled Maintenance','Sched Maint','Chamber / Module PM') if(kwargs.get('quote_type_attribute_value').upper() != "TOOL BASED") else ('Scheduled Maintenance','Chamber / Module PM','Corrective Maintenance')))
            #INC08664376 - End - M
            ##HPQC 526 code ends..
            self._process_query(
                """INSERT SAQSKP (
                        ASSEMBLY_ID,
                        ASSEMBLY_DESCRIPTION,
                        ASSEMBLY_RECORD_ID,
                        EQUIPMENT_ID,
                        EQUIPMENT_DESCRIPTION,
                        EQUIPMENT_RECORD_ID,
                        PART_NUMBER,
                        PART_DESCRIPTION,
                        PART_RECORD_ID,
                        QUANTITY,
                        PM_ID,
                        PM_NAME,
                        PM_RECORD_ID,
                        KIT_ID,
                        KIT_NAME,
                        KIT_RECORD_ID,
                        KIT_NUMBER,
                        KIT_NUMBER_RECORD_ID,
                        QUOTE_ID,
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_ID,
                        SERVICE_RECORD_ID,
                        QTEGBKPME_RECORD_ID,
                        QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED
                    ) 
                    SELECT KP.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
                        SELECT DISTINCT
                        SAQGPA.ASSEMBLY_ID,
                        SAQGPA.ASSEMBLY_DESCRIPTION,
                        SAQGPA.ASSEMBLY_RECORD_ID,
                        SAQGPA.EQUIPMENT_ID,
                        SAQGPA.EQUIPMENT_DESCRIPTION,
                        SAQGPA.EQUIPMENT_RECORD_ID,
                        MAKTPT_INBOUND.PART_NUMBER,
                        MAMTRL.SAP_DESCRIPTION,
                        MAMTRL.MATERIAL_RECORD_ID,
                        MAKTPT_INBOUND.QUANTITY,
                        SAQGPA.PM_ID,
                        SAQGPA.PM_NAME,
                        SAQGPA.PM_RECORD_ID AS PM_RECORD_ID,
                        SAQGPA.KIT_ID,
                        SAQGPA.KIT_NAME,
                        SAQGPA.KIT_RECORD_ID,
                        SAQGPA.KIT_NUMBER,
                        SAQGPA.KITNUMBER_RECORD_ID,
                        '{QuoteId}' as QUOTE_ID,
                        '{QuoteRecordId}' as QUOTE_RECORD_ID,
                        '{RevisionId}' as QTEREV_ID,
                        '{RevisionRecordId}' as QTEREV_RECORD_ID,
                        SAQGPA.SERVICE_DESCRIPTION,
                        SAQGPA.SERVICE_ID,
                        SAQGPA.SERVICE_RECORD_ID,
                        SAQGPA.QTEREVPME_RECORD_ID
                        FROM SYSPBT(NOLOCK)
                        JOIN SAQGPA(NOLOCK) ON SAQGPA.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQGPA.EQUIPMENT_RECORD_ID = SYSPBT.BATCH_RECORD_ID AND SAQGPA.QTEREV_RECORD_ID = SYSPBT.QTEREV_RECORD_ID
                        JOIN MAKTPT(NOLOCK) ON MAKTPT.KIT_ID = SAQGPA.KIT_ID
                        JOIN MAKTPT_INBOUND(NOLOCK) ON MAKTPT_INBOUND.KIT_ID = SAQGPA.KIT_ID AND MAKTPT_INBOUND.QUOTE_ID = SAQGPA.QUOTE_ID AND MAKTPT_INBOUND.QTEREV_ID = SAQGPA.QTEREV_ID AND MAKTPT_INBOUND.SERVICE_ID = SAQGPA.SERVICE_ID AND MAKTPT_INBOUND.PART_NUMBER = MAKTPT.PART_NUMBER
                        JOIN MAMTRL(NOLOCK) ON MAMTRL.SAP_PART_NUMBER = MAKTPT.PART_NUMBER
                    WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPA.SERVICE_ID = '{TreeParam}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}') KP LEFT JOIN SAQSKP (NOLOCK) AS KIT ON 
                    KP.QUOTE_RECORD_ID =KIT.QUOTE_RECORD_ID AND KP.QTEREV_RECORD_ID =KIT.QTEREV_RECORD_ID AND KP.SERVICE_RECORD_ID =KIT.SERVICE_RECORD_ID AND KP.EQUIPMENT_RECORD_ID =KIT.EQUIPMENT_RECORD_ID  AND KP.ASSEMBLY_RECORD_ID =KIT.ASSEMBLY_RECORD_ID AND KP.PM_RECORD_ID =KIT.PM_RECORD_ID AND KP.KIT_RECORD_ID =KIT.KIT_RECORD_ID  AND KP.KITNUMBER_RECORD_ID =KIT.KIT_NUMBER_RECORD_ID WHERE ISNULL(KIT.KIT_RECORD_ID,'') = '' """.format(
                    UserName=self.user_name,
                    TreeParam=self.real_time_integration_service if self.real_time_integration_service else service_id,
                    QuoteId = self.contract_quote_id,
                    QuoteRecordId=self.contract_quote_record_id,
                    RevisionId=self.quote_revision_id,
                    RevisionRecordId=self.quote_revision_record_id,
                    BatchGroupRecordId=kwargs.get('batch_group_record_id')
                    ))
        
        Sql.RunQuery("""UPDATE SAQGPA SET QTEREVPME_RECORD_ID = SAQGPM.QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID from SAQGPA JOIN SAQGPM ON SAQGPA.GOT_CODE = SAQGPM.GOT_CODE AND SAQGPA.PM_ID = SAQGPM.PM_ID AND SAQGPA.KIT_ID = SAQGPM.KIT_ID AND SAQGPA.KIT_NUMBER = SAQGPM.KIT_NUMBER AND SAQGPA.QUOTE_RECORD_ID = SAQGPM.QUOTE_RECORD_ID AND SAQGPA.QTEREV_RECORD_ID = SAQGPM.QTEREV_RECORD_ID WHERE SAQGPA.QUOTE_RECORD_ID = '{}' AND SAQGPA.QTEREV_RECORD_ID = '{}' AND SAQGPA.SERVICE_ID = '{}'""".format(self.contract_quote_record_id,self.quote_revision_record_id,self.real_time_integration_service if self.real_time_integration_service else service_id)
            )
            
        Sql.RunQuery("""UPDATE SAQSKP SET QTEGBKPME_RECORD_ID = SAQGPM.QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID from SAQSKP JOIN SAQGPM ON SAQSKP.PM_ID = SAQGPM.PM_ID AND SAQSKP.KIT_ID = SAQGPM.KIT_ID AND SAQSKP.KIT_NUMBER = SAQGPM.KIT_NUMBER AND SAQSKP.QUOTE_RECORD_ID = SAQGPM.QUOTE_RECORD_ID AND SAQSKP.QTEREV_RECORD_ID = SAQGPM.QTEREV_RECORD_ID WHERE SAQSKP.QUOTE_RECORD_ID = '{}' AND SAQSKP.QTEREV_RECORD_ID = '{}' AND SAQSKP.SERVICE_ID = '{}'""".format(self.contract_quote_record_id,self.quote_revision_record_id,self.real_time_integration_service if self.real_time_integration_service else service_id)
            )
        
        
        ###A055S000P01-19603 Starts
        TreeParam=self.real_time_integration_service if self.real_time_integration_service else service_id
        #INC08621345 - End - M
        if str(TreeParam) in ("Z0009","Z0010","Z0128"):
            check_assembly = True
            if str(TreeParam) == "Z0009":
                check_assembly = False
                get_quote_type = Sql.GetFirst("SELECT QUOTE_TYPE FROM SAQTSE WHERE QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = 'Z0009'")
                if get_quote_type.QUOTE_TYPE!="Tool based":
                    check_assembly = True
            if check_assembly:
                #CR357B
                Sql.RunQuery("UPDATE SAQSCO SET IBASE_ATTSTS = 'INCOMPLETE' FROM (SELECT DISTINCT A.EQUIPMENT_ID FROM SAQSCA A JOIN MAEQUP B ON  B.PAR_EQUIPMENT_ID = A.EQUIPMENT_ID AND B.EQUIPMENT_ID = A.ASSEMBLY_ID WHERE A.QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND A.QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND A.SERVICE_ID = '"+str(TreeParam)+"' AND B.EQUIPMENTTYPE_DESCRIPTION = 'CHAMBER' AND A.GREENBOOK IN ('EPI','ETCH','ALD','DSM','FEP','MDP','PPC','SRP','MPKG','DISPLAY') AND ISNULL(B.PROCESS_TYPE,'') = '') equp WHERE QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '"+str(TreeParam)+"' AND SAQSCO.EQUIPMENT_ID = equp.EQUIPMENT_ID  AND SAQSCO.IBASE_ATTSTS = 'COMPLETE'")
                Sql.RunQuery("UPDATE SAQSCO SET IBASE_ATTSTS = 'INCOMPLETE' FROM (SELECT DISTINCT A.EQUIPMENT_ID FROM SAQSCA A JOIN MAEQUP B ON  B.PAR_EQUIPMENT_ID = A.EQUIPMENT_ID AND B.EQUIPMENT_ID = A.ASSEMBLY_ID WHERE A.QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND A.QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND A.SERVICE_ID = '"+str(TreeParam)+"' AND B.EQUIPMENTTYPE_DESCRIPTION = 'POLISHER' AND A.GREENBOOK IN ('CMP') AND ISNULL(B.PROCESS_TYPE,'') = '') equp WHERE QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '"+str(TreeParam)+"' AND SAQSCO.EQUIPMENT_ID = equp.EQUIPMENT_ID  AND SAQSCO.IBASE_ATTSTS = 'COMPLETE'")
                Sql.RunQuery("UPDATE SAQSCO SET IBASE_ATTSTS = 'INCOMPLETE' FROM (SELECT DISTINCT A.EQUIPMENT_ID FROM SAQSCO A JOIN MAEQUP B ON A.EQUIPMENT_ID = B.EQUIPMENT_ID WHERE A.QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND A.QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND A.SERVICE_ID = '"+str(TreeParam)+"' AND ISNULL(B.DEVICE_NODE,'') = '') equp WHERE QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '"+str(TreeParam)+"' AND SAQSCO.EQUIPMENT_ID = equp.EQUIPMENT_ID  AND SAQSCO.IBASE_ATTSTS = 'COMPLETE'")
                #CR357B
        ###A055S000P01-19603 Ends
        #A055S000P01-20610,A055S000P01-20609,CR681 - Start - A
        self.real_time_status_update(service_id= service_id, quote_type = 'EVENT')
        #A055S000P01-20610,A055S000P01-20609,CR681 - End - A
        delete_obj_list = ["MAEAPM_INBOUND","MAKTPT_INBOUND"]
        for object in delete_obj_list:
            Sql.RunQuery("DELETE FROM {} WHERE QUOTE_ID='{}' AND QTEREV_ID = '{}' ".format(object,self.contract_quote_id,self.quote_revision_id))
            # self._process_query("""INSERT SAQGPE (
            # 		CPS_CONFIGURATION_ID,
            # 		CPS_MATCH_ID,
            # 		--ENTITLEMENT_XML,
            # 		SERVICE_ID,
            # 		SERVICE_RECORD_ID,
            # 		GOT_CODE,
            # 		GOTCODE_RECORD_ID,
            # 		GREENBOOK,
            # 		GREENBOOK_RECORD_ID,
            # 		KB_VERSION,
            # 		PM_ID,
            # 		PM_RECORD_ID,
            # 		QUOTE_ID,
            # 		QUOTE_RECORD_ID,
            # 		QTEREV_ID,
            # 		QTEREV_RECORD_ID,
            # 		QTEGBKENT_RECORD_ID,
            # 		QTEGGTPME_RECORD_ID,
            # 		QUOTE_REV_GOT_CD_PM_EVNT_ENTITLEMENTS_RECORD_ID,
            # 		CPQTABLEENTRYADDEDBY,
            # 		CPQTABLEENTRYDATEADDED
            # 		) 
            # 		SELECT pm_entitlement.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_GOT_CD_PM_EVNT_ENTITLEMENTS_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(SELECT DISTINCT 
            # 		SAQSGE.CPS_CONFIGURATION_ID,
            # 		SAQSGE.CPS_MATCH_ID,
            # 		--SAQSGE.ENTITLEMENT_XML,
            # 		SAQGPM.SERVICE_ID,
            # 		SAQGPM.SERVICE_RECORD_ID,
            # 		SAQGPM.GOT_CODE,
            # 		SAQGPM.GOTCODE_RECORD_ID,
            # 		SAQGPM.GREENBOOK,
            # 		SAQGPM.GREENBOOK_RECORD_ID,
            # 		SAQSGE.KB_VERSION,
            # 		SAQGPM.PM_ID,
            # 		SAQGPM.PM_RECORD_ID,
            # 		SAQGPM.QUOTE_ID,
            # 		SAQGPM.QUOTE_RECORD_ID,
            # 		SAQGPM.QTEREV_ID,
            # 		SAQGPM.QTEREV_RECORD_ID,
            # 		SAQSGE.QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID as QTEGBKENT_RECORD_ID,
            # 		SAQGPM.QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID as QTEGGTPME_RECORD_ID
            # 		FROM SYSPBT (NOLOCK) 
            # 		JOIN SAQSGE(NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQSGE.QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQSGE.QTEREV_RECORD_ID
            # 		JOIN SAQGPM(NOLOCK) ON SAQGPM.QUOTE_RECORD_ID = SAQSGE.QUOTE_RECORD_ID AND SAQGPM.QTEREV_RECORD_ID = SAQSGE.QTEREV_RECORD_ID 
            # 		AND SAQGPM.SERVICE_RECORD_ID = SAQSGE.SERVICE_RECORD_ID AND SAQGPM.GREENBOOK_RECORD_ID = SAQSGE.GREENBOOK_RECORD_ID
            # 		WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}'  AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SAQGPM.SERVICE_ID = '{TreeParam}' )pm_entitlement LEFT JOIN SAQGPE (NOLOCK) AS EVENT_ENTITLEMENT ON pm_entitlement.QUOTE_RECORD_ID = EVENT_ENTITLEMENT.QUOTE_RECORD_ID  AND pm_entitlement.QTEREV_RECORD_ID = EVENT_ENTITLEMENT.QTEREV_RECORD_ID AND pm_entitlement.GREENBOOK_RECORD_ID = EVENT_ENTITLEMENT.GREENBOOK_RECORD_ID AND pm_entitlement.GOTCODE_RECORD_ID = EVENT_ENTITLEMENT.GOTCODE_RECORD_ID AND pm_entitlement.PM_RECORD_ID = EVENT_ENTITLEMENT.PM_RECORD_ID AND pm_entitlement.QTEGGTPME_RECORD_ID = EVENT_ENTITLEMENT.QTEGGTPME_RECORD_ID AND ISNULL(EVENT_ENTITLEMENT.QTEGGTPME_RECORD_ID,'') = '' """.format(
            # 		UserName=self.user_name,
            # 		TreeParam=self.tree_param,
            # 		QuoteId = self.contract_quote_id,
            # 		QuoteRecordId=self.contract_quote_record_id,
            # 		RevisionId=self.quote_revision_id,
            # 		RevisionRecordId=self.quote_revision_record_id,
            # 		BatchGroupRecordId=kwargs.get('batch_group_record_id'))
            # 		)
            
            # #creating backup table for saqgpe table insert...
            # saqsge_backup_table = "saqsge_backup_table_{}".format(self.contract_quote_id) 

            # drop_saqsge_backup_table = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(saqsge_backup_table)+"'' ) BEGIN DROP TABLE "+str(saqsge_backup_table)+" END  ' ")


            # saqsge_temp_table_insert = SqlHelper.GetFirst("sp_executesql @T=N'SELECT SAQSGE.GREENBOOK,SAQSGE.GREENBOOK_RECORD_ID,SAQSGE.SERVICE_RECORD_ID,SAQSGE.QUOTE_RECORD_ID,SAQSGE.QTEREV_RECORD_ID,SAQSGE.QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,SAQSGE.ENTITLEMENT_XML,SAQSGE.CONFIGURATION_STATUS INTO "+str(saqsge_backup_table)+" FROM SAQSGE (NOLOCK) WHERE SAQSGE.QUOTE_RECORD_ID = ''{}'' AND SAQSGE.QTEREV_RECORD_ID = ''{}'' AND SAQSGE.SERVICE_ID = ''{}'' '".format(self.contract_quote_record_id,self.quote_revision_record_id,self.tree_param))

            # Sql.RunQuery("""UPDATE SAQGPE SET ENTITLEMENT_XML = saqsge_backup_table.ENTITLEMENT_XML,CONFIGURATION_STATUS = saqsge_backup_table.CONFIGURATION_STATUS FROM  {saqsge_backup_table} (NOLOCK)  saqsge_backup_table JOIN SAQGPE ON saqsge_backup_table.QUOTE_RECORD_ID = SAQGPE.QUOTE_RECORD_ID AND saqsge_backup_table.QTEREV_RECORD_ID = SAQGPE.QTEREV_RECORD_ID AND saqsge_backup_table.SERVICE_RECORD_ID = SAQGPE.SERVICE_RECORD_ID AND saqsge_backup_table.GREENBOOK_RECORD_ID = SAQGPE.GREENBOOK_RECORD_ID WHERE SAQGPE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPE.SERVICE_ID = '{TreeParam}' AND ISNULL(SAQGPE.ENTITLEMENT_XML,'') = '' """.format(saqsge_backup_table = str(saqsge_backup_table),QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam=self.tree_param))

            # drop_saqsge_backup_table = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(saqsge_backup_table)+"'' ) BEGIN DROP TABLE "+str(saqsge_backup_table)+" END  ' ")
                
            # Sql.RunQuery("""UPDATE SAQGPE
            # 			SET ENTITLEMENT_XML = IQ.ENTITLEMENT_XML,
            # 			CONFIGURATION_STATUS = IQ.CONFIGURATION_STATUS
            # 				FROM SAQGPE (NOLOCK)
            # 				INNER JOIN (SELECT SAQSGE.ENTITLEMENT_XML,SAQSGE.QUOTE_RECORD_ID,SAQSGE.QTEREV_RECORD_ID,SAQSGE.CONFIGURATION_STATUS
            # 							FROM SAQGPE (NOLOCK) 
            # 							JOIN SAQSGE (NOLOCK) ON SAQSGE.QUOTE_RECORD_ID = SAQGPE.QUOTE_RECORD_ID AND SAQSGE.QTEREV_RECORD_ID = SAQGPE.QTEREV_RECORD_ID AND SAQSGE.GREENBOOK_RECORD_ID = SAQGPE.GREENBOOK_RECORD_ID
            # 							JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQGPE.QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQGPE.QTEREV_RECORD_ID
            # 							WHERE SAQGPE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSGE.SERVICE_ID = '{TreeParam}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'
            # 							)IQ ON SAQGPE.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQGPE.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam=self.tree_param,BatchGroupRecordId = kwargs.get('batch_group_record_id') ))

    
    def _create(self):
        Trace.Write("inside create"+str(self.action_type))
        if self.action_type == "ADD_COVERED_OBJ":
            quotetype_value_for_offering = ''
            Trace.Write("add covered object")
            covered_start_time = time.time()
            master_object_name = "SAQFEQ"
            if self.values:
                record_ids = []
                if self.all_values:        
                    qury_str=""
                    if A_Keys!="" and A_Values!="":
                        for key,val in zip(A_Keys,A_Values):
                            if(val!=""):
                                if key=="QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID":
                                    key="CpqTableEntryId"
                                    val = ''.join(re.findall(r'\d+', val)) if not val.isdigit() else val
                                qury_str+=" "+key+" LIKE '%"+val+"%' AND "
                    if self.tree_param != '' and self.tree_parent_level_0 == 'Add-On Products' : 
                    #modified for temp tool same multiple equipment need to check for temp
                    #ADDED FOR ADD ON PRODUCT SCENARIO
                        query_string ="select SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID, SAQFEQ.EQUIPMENT_ID, SAQFEQ.SERIAL_NUMBER, SAQFEQ.PBG, SAQFEQ.PLATFORM, SAQFEQ.FABLOCATION_ID, SAQFEQ.FABLOCATION_NAME from  SAQFEQ(NOLOCK) JOIN SAQSCO ON SAQSCO.QUOTE_ID = SAQFEQ.QUOTE_ID  AND SAQSCO.EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID AND SAQSCO.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID  WHERE SAQFEQ.QUOTE_RECORD_ID = '{quo_rec_id}' AND SAQFEQ.QTEREV_RECORD_ID = '{RevisionRecordId}' AND {Qury_Str} NOT EXISTS(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{quo_rec_id}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID ='{TreeParam}' ) ".format(quo_rec_id=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam = self.tree_param,Qury_Str=qury_str)
                    elif self.tree_param == "Add-On Products":
                        #1736
                        Trace.Write("Qury_Str_chk--- "+str(qury_str))
                        query_string ="select QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID, EQUIPMENT_ID, FABLOCATION_ID, FABLOCATION_NAME from  SAQSCO(NOLOCK)  WHERE QUOTE_RECORD_ID = '{quo_rec_id}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND GREENBOOK = '{TreeParentParam}' AND {Qury_Str} SERVICE_ID = '{service_id}' AND NOT EXISTS(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{quo_rec_id}' and QTEREV_RECORD_ID = '{RevisionRecordId}' AND {Qury_Str} SERVICE_ID ='{addon_service_id}' ) ".format(quo_rec_id=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParentParam = self.tree_parent_level_0 ,addon_service_id = Product.GetGlobal("addon_service_id"),service_id= self.tree_parent_level_1 ,Qury_Str=qury_str)
                            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
                    elif self.tree_param == 'Z0004':
                        #INC09226624 start
                        query_string = "SELECT QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID NOT IN(SELECT QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID FROM SAQFEQ (NOLOCK) LEFT OUTER JOIN SAQSCO(NOLOCK) ON SAQSCO.EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID AND SAQSCO.QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID AND SAQSCO.TEMP_TOOL = SAQFEQ.TEMP_TOOL WHERE SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCO.EQUIPMENTCATEGORY_ID = 'Y' AND {Qury_Str} SAQSCO.SERVICE_ID ='{TreeParam}') AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam = self.tree_param,Qury_Str=qury_str)
                        #INC09226624 end
                    else:
                        if self.tree_param == "Sending Equipment" or self.tree_param == "Receiving Equipment":
                            query_string = "SELECT QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND RELOCATION_EQUIPMENT_TYPE = '{tree_param}' AND {Qury_Str} EQUIPMENT_ID NOT IN(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{TreeParam}'  AND RELOCATION_EQUIPMENT_TYPE = '{tree_param}')".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam = self.tree_param if self.tree_parent_level_0 == 'Comprehensive Services' else self.tree_parent_level_0,Qury_Str=qury_str,tree_param=str(self.tree_param).upper())
                        else:
                            query_string = "SELECT QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND {Qury_Str} QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID NOT IN (SELECT QTEREVFEQ_RECORD_ID FROM SAQSCO WHERE  QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{TreeParam}') ".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam = self.tree_param,Qury_Str=qury_str)
                    query_string_for_count = "SELECT COUNT(*) as count FROM ({Query_String})OQ".format(
                        Query_String=query_string
                    )
                    table_count_data = Sql.GetFirst(query_string_for_count)
                                                                    
                    if table_count_data is not None:
                        table_total_rows = table_count_data.count
                    if table_total_rows:
                        record_ids = [data for data in self.get_results(query_string, table_total_rows)]    
                        Trace.Write("record_ids_yield--- "+str(record_ids))                
                else:
                    record_ids = [
                        CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
                        if value.strip() != "" and master_object_name in value
                        else value
                        for value in self.values
                    ]
                batch_group_record_id = str(Guid.NewGuid()).upper()
                Trace.Write('@@@Batch Group Record ID --->'+str(batch_group_record_id))
                record_ids = str(str(record_ids)[1:-1].replace("'",""))
                parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
                Trace.Write("record_ids--->"+str(record_ids))
                primaryQueryItems = SqlHelper.GetFirst(""+str(parameter.QUERY_CRITERIA_1)+" SYSPBT(BATCH_RECORD_ID, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,QTEREV_RECORD_ID,QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,SAP_PART_NUMBER) SELECT SAQFEQ.EQUIPMENT_RECORD_ID as BATCH_RECORD_ID, ''IN PROGRESS'' as BATCH_STATUS, SAQFEQ.QUOTE_ID, SAQFEQ.QUOTE_RECORD_ID, ''"+str(batch_group_record_id)+"'' as BATCH_GROUP_RECORD_ID,''"+str(self.quote_revision_record_id)+"'' as QTEREV_RECORD_ID,SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,''"+str(self.tree_param)+"'' as SAP_PART_NUMBER FROM SAQFEQ (NOLOCK) JOIN splitstring(''"+record_ids+"'') ON ltrim(rtrim(NAME)) = SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID'")

                Trace.Write(""+str(parameter.QUERY_CRITERIA_1)+" SYSPBT(BATCH_RECORD_ID, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,QTEREV_RECORD_ID,QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,SAP_PART_NUMBER) SELECT SAQFEQ.EQUIPMENT_RECORD_ID as BATCH_RECORD_ID, ''IN PROGRESS'' as BATCH_STATUS, SAQFEQ.QUOTE_ID, SAQFEQ.QUOTE_RECORD_ID, ''"+str(batch_group_record_id)+"'' as BATCH_GROUP_RECORD_ID,''"+str(self.quote_revision_record_id)+"'' as QTEREV_RECORD_ID,SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,''"+str(self.tree_param)+"'' as SAP_PART_NUMBER FROM SAQFEQ (NOLOCK) JOIN splitstring(''"+record_ids+"'') ON ltrim(rtrim(NAME)) = SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID'")
                #SAQSCO_start_time = time.time()
                self._insert_quote_service_covered_object(batch_group_record_id=batch_group_record_id,record_ids = record_ids)
                #SAQSCO_end_time = time.time()
                
                #SAQSCA_start_time = time.time()
                # Trace.Write("@4546-5576--------"+str(record_ids))
                #import re -INC08621345 
                service_entitlement_object =Sql.GetFirst("""select ENTITLEMENT_XML from SAQTSE (nolock) where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{service_id}' """.format(QuoteRecordId = self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,service_id = self.real_time_integration_service if self.real_time_integration_service else self.tree_param))
                #quotetype_value_for_offering = ''
                if service_entitlement_object is not None:
                    pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
                    quote_type_attribute = re.compile(r'<ENTITLEMENT_ID>AGS_[^>]*?_PQB_QTETYP</ENTITLEMENT_ID>')
                    quote_type_attribute_value = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
                    XML = service_entitlement_object.ENTITLEMENT_XML
                    for values in re.finditer(pattern_tag, XML):
                        sub_string = values.group(1)
                        quotetype_id =re.findall(quote_type_attribute,sub_string)
                        if quotetype_id:
                            quotetype_value =re.findall(quote_type_attribute_value,sub_string)
                            quotetype_value_for_offering = str(quotetype_value[0]).upper()
                ####A055S000P01-16862 code starts...
                self._insert_quote_service_covered_assembly(entitlement_level_value = self.entitlement_level_value,entitlement_level = self.entitlement_level,batch_group_record_id=batch_group_record_id,quotetype_value_for_offering= quotetype_value_for_offering) ####A055S000P01-16862 code ends...
                self._insert_quote_service_fab_location(batch_group_record_id=batch_group_record_id)
                #SAQSCA_end_time = time.time()
                
                #SAQSGB_start_time = time.time()
                self._insert_quote_service_greenbook(batch_group_record_id=batch_group_record_id)
                #A055S000P01-20813,CR704 - Start - M
                Sql.RunQuery("UPDATE A SET A.CONTRACT_VALID_FROM = B.MIN,A.CONTRACT_VALID_TO = B.MAX FROM SAQSGB (NOLOCK) A JOIN (SELECT MIN(CONTRACT_VALID_FROM) as MIN,MAX(CONTRACT_VALID_TO) as MAX,SERVICE_ID,GREENBOOK FROM SAQSCO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' GROUP BY SERVICE_ID,GREENBOOK) B ON A.GREENBOOK = B.GREENBOOK AND A.SERVICE_ID = B.SERVICE_ID WHERE A.QUOTE_RECORD_ID = '{QuoteRecordId}' AND A.QTEREV_RECORD_ID = '{RevisionRecordId}'  ".format(QuoteRecordId = self.contract_quote_record_id,RevisionRecordId = self.quote_revision_record_id))
                #A055S000P01-20813,CR704 - End - M
                #SAQSGB_end_time = time.time()	
                ##To check the PM events Attribute value...
                ##A055S000P01-12518 code starts...
                #import re
                #INC08621345 - Start - M
                service_entitlement_obj =Sql.GetFirst("""select PMLAB_ENT, CMLAB_ENT,QUOTE_TYPE from SAQTSE (nolock) where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{service_id}' """.format(QuoteRecordId = self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,service_id = self.tree_param))
                quote_type_attribute_value = ""
                pm_event_attribute_value = ""
                cm_labor = ''
                additional_where =""
                if service_entitlement_obj is not None:
                    # pm_event_flag=0
                    # qte_type_flag=0
                    if service_entitlement_obj.PMLAB_ENT:
                        pm_event_attribute_value = service_entitlement_obj.PMLAB_ENT
                    if service_entitlement_obj.CMLAB_ENT:
                        cm_labor = service_entitlement_obj.CMLAB_ENT
                    if service_entitlement_obj.QUOTE_TYPE:
                        quote_type_attribute_value = service_entitlement_obj.QUOTE_TYPE
                    Trace.Write("service_id---"+str(cm_labor)+'-'+str(quote_type_attribute_value)+'-'+str(pm_event_attribute_value))
                    # updateentXML = service_entitlement_obj.ENTITLEMENT_XML
                    # pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
                    # pattern_id = re.compile(r'<ENTITLEMENT_ID>AGS_[^>]*?_NET_PRMALB</ENTITLEMENT_ID>')
                    # pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
                    # quote_type_id = re.compile(r'<ENTITLEMENT_ID>AGS_[^>]*?_PQB_QTETYP</ENTITLEMENT_ID>')
                    # for value in re.finditer(pattern_tag, updateentXML):
                    #     sub_string = value.group(1)
                    #     pm_event_attribute_id =re.findall(pattern_id,sub_string)
                    #     quote_type_attribute_id =re.findall(quote_type_id,sub_string)
                    #     additional_where = ""
                    # if quote_type_attribute_id:
                    #     quote_type_attribute_value =re.findall(pattern_name,sub_string)
                    #     quote_type_attribute_value = quote_type_attribute_value[0]
                    # if pm_event_attribute_id:
                    #     pm_event_attribute_value = re.findall(pattern_name,sub_string)
                    if (pm_event_attribute_value or cm_labor) and self.tree_param not in ('Z0009','Z0010') and quote_type_attribute_value:
                        # pm_event_attribute_value = re.findall(pattern_name,sub_string)
                        # pm_event_attribute_value == "PMSA Flex" or pm_event_attribute_value == "Event based")
                        #Trace.Write("555 "+str(self.tree_param)+" 555 "+str(pm_event_attribute_value))
                        if pm_event_attribute_value == "Included - All PM" :
                            additional_where = " (ISNULL(MAEAPK.MNTEVT_LEVEL,'') IN ('Chamber / Module PM' ,'Scheduled Maintenance' )) AND"
                            #Trace.Write("additional_where_chk_1 "+str(additional_where))
                        if  cm_labor == "Included":
                            additional_where = " (ISNULL(MAEAPK.MNTEVT_LEVEL,'') IN ('Corrective Maintenance' ) AND MAEAPK.MNTEVT_LEVEL != '') AND "
                        elif "Included - Monthly and Above" in pm_event_attribute_value:
                            additional_where = " (MAEAPK.MNTEVT_LEVEL = 'Chamber / Module PM' OR MAEAPK.MNTEVT_LEVEL = 'Scheduled Maintenance') AND (MAEAPK.PM_ID = 'Monthly' OR MAEAPK.PM_ID = 'Quarterly' OR MAEAPK.PM_ID = 'Semi-Annual' OR MAEAPK.PM_ID = 'Annual' OR MAEAPK.PM_ID = '24 Month') AND"
                        elif ("Included - Quarterly and Above" in pm_event_attribute_value or "Included - Qtrly and Above" in pm_event_attribute_value):
                            additional_where = " (MAEAPK.MNTEVT_LEVEL = 'Chamber / Module PM' OR MAEAPK.MNTEVT_LEVEL = 'Scheduled Maintenance') AND (MAEAPK.PM_ID = 'Quarterly' OR MAEAPK.PM_ID = 'Semi-Annual' OR MAEAPK.PM_ID = 'Annual') AND"
                        # elif (self.tree_param in ("Z0099") and ("Included - Monthly and Above" in pm_event_attribute_value)):
                        #     additional_where = " (MAEAPK.MNTEVT_LEVEL = 'Chamber / Module PM' OR MAEAPK.MNTEVT_LEVEL = 'Scheduled Maintenance') AND (MAEAPK.PM_ID = 'Monthly' OR MAEAPK.PM_ID = 'Quarterly' OR MAEAPK.PM_ID = 'Semi-Annual' OR MAEAPK.PM_ID = 'Annual') AND"
                        if(pm_event_attribute_value != "Excluded" or cm_labor != "Excluded"):
                            # if self.tree_param == "Z0099" and "Included - All PM" not in pm_event_attribute_value:
                            #     Trace.Write("Insert Restricted")
                            # else:
                            self._insert_quote_service_preventive_maintenance_kit_parts(entitlement_level_value = self.entitlement_level_value,entitlement_level = self.entitlement_level,batch_group_record_id=batch_group_record_id,quotetype_value_for_offering= quotetype_value_for_offering,additional_where = additional_where)
                            # pm_event_flag=1
                    if self.tree_param in ('Z0009','Z0128','Z0010') and quote_type_attribute_value and ((pm_event_attribute_value or cm_labor) or self.tree_param in ('Z0128','Z0010')):
                        # quote_type_attribute_value =re.findall(pattern_name,sub_string)
                        if quote_type_attribute_value.upper() != 'TOOL BASED':##Checking the Quote type before calling the events insert....
                            additional_where = ""
                            if self.tree_param == 'Z0010' or self.tree_param == 'Z0128':
                                self.tools_from_ui = "No"
                                
                                self.applied_preventive_maintainence_quote_type_changed = "Yes"
                                # self.applied_preventive_maintainence(entitlement_level_value = self.entitlement_level_value,entitlement_level = self.entitlement_level,batch_group_record_id=batch_group_record_id,quote_type_attribute_value = quote_type_attribute_value,applied_preventive_maintainence_quote_type_changed = self.applied_preventive_maintainence_quote_type_changed,pmevents_changes_insert = self.pmevents_changes_insert,additional_where=additional_where)
                                # qte_type_flag=1
                            if self.tree_param in ("Z0009") and (pm_event_attribute_value == "Included - All PM" ):
                                additional_where = " AND ((MAEAPK.MNTEVT_LEVEL = 'Chamber / Module PM' OR MAEAPK.MNTEVT_LEVEL = 'Scheduled Maintenance') AND MAEAPK.MNTEVT_LEVEL != '') "
                                # if pm_event_attribute_value != "":
                                #     self.applied_preventive_maintainence(entitlement_level_value = self.entitlement_level_value,entitlement_level = self.entitlement_level,batch_group_record_id=batch_group_record_id,quote_type_attribute_value = quote_type_attribute_value,applied_preventive_maintainence_quote_type_changed = self.applied_preventive_maintainence_quote_type_changed,pmevents_changes_insert = self.pmevents_changes_insert,additional_where=additional_where)
                                    # qte_type_flag=1
                            if  cm_labor == "Included":
                                additional_where = " AND ((MAEAPK.MNTEVT_LEVEL = 'Corrective Maintenance') AND MAEAPK.MNTEVT_LEVEL != '') "
                            if (self.tree_param in ("Z0009") and "Included - < Quarterly" in pm_event_attribute_value):
                                additional_where = " AND (MAEAPK.MNTEVT_LEVEL = 'Chamber / Module PM' OR MAEAPK.MNTEVT_LEVEL = 'Scheduled Maintenance') AND (MAEAPK.PM_ID = 'Monthly' OR MAEAPK.PM_ID = 'Quarterly')"
                                # if pm_event_attribute_value != "":
                                #     self.applied_preventive_maintainence(entitlement_level_value = self.entitlement_level_value,entitlement_level = self.entitlement_level,batch_group_record_id=batch_group_record_id,quote_type_attribute_value = quote_type_attribute_value,applied_preventive_maintainence_quote_type_changed = self.applied_preventive_maintainence_quote_type_changed,pmevents_changes_insert = self.pmevents_changes_insert,additional_where=additional_where)
                                #     qte_type_flag=1
                            self.applied_preventive_maintainence(entitlement_level_value = self.entitlement_level_value,entitlement_level = self.entitlement_level,batch_group_record_id=batch_group_record_id,quote_type_attribute_value = quote_type_attribute_value,applied_preventive_maintainence_quote_type_changed = self.applied_preventive_maintainence_quote_type_changed,pmevents_changes_insert = self.pmevents_changes_insert,additional_where=additional_where)
                        else:
                            # pm_event_attribute_value = re.findall(pattern_name,sub_string)
                            
                            if(quote_type_attribute_value.upper() == "TOOL BASED" and (pm_event_attribute_value != "Excluded" and cm_labor != "Excluded")):
                                Trace.Write("self.tree_param_chk "+str(self.tree_param)+" - "+"pm_event_attribute_value_chk "+str(pm_event_attribute_value))
                                if self.tree_param in ("Z0009") and (pm_event_attribute_value == "Included - All PM" ):
                                    additional_where = " ((MAEAPK.MNTEVT_LEVEL = 'Chamber / Module PM' OR MAEAPK.MNTEVT_LEVEL = 'Scheduled Maintenance') AND MAEAPK.MNTEVT_LEVEL != '') AND"
                                    Trace.Write("additional_where_chk_1 "+str(additional_where))
                                    #if pm_event_attribute_value != "":
                                    # self._insert_quote_service_preventive_maintenance_kit_parts(entitlement_level_value = self.entitlement_level_value,entitlement_level = self.entitlement_level,batch_group_record_id=batch_group_record_id,quotetype_value_for_offering= quotetype_value_for_offering,additional_where = additional_where)
                                    # qte_type_flag=1
                                if cm_labor ==  "Included" : 
                                    additional_where = " ((MAEAPK.MNTEVT_LEVEL = 'Corrective Maintenance') AND MAEAPK.MNTEVT_LEVEL != '') AND"
                                if (self.tree_param in ("Z0009") and "Included - < Quarterly" in pm_event_attribute_value):
                                    additional_where = " (MAEAPK.MNTEVT_LEVEL = 'Chamber / Module PM' OR MAEAPK.MNTEVT_LEVEL = 'Scheduled Maintenance') AND (MAEAPK.PM_ID = 'Monthly' OR MAEAPK.PM_ID = 'Quarterly') AND"
                                    #if pm_event_attribute_value != "":
                                self._insert_quote_service_preventive_maintenance_kit_parts(entitlement_level_value = self.entitlement_level_value,entitlement_level = self.entitlement_level,batch_group_record_id=batch_group_record_id,quotetype_value_for_offering= quotetype_value_for_offering,additional_where = additional_where)
                                    # qte_type_flag=1
                    # if (self.tree_param == 'Z0009' or self.tree_param == 'Z0010' or self.tree_param == 'Z0128') and qte_type_flag == 1:
                    #     break
                    # else:
                    #     if pm_event_flag == 1:
                    #         break
                ##A055S000P01-12518 code ends...
                #ENTITLEMENT SV TO CE
                Entitlement_start_time = time.time()
                if self.trigger_from == 'PythonScript':
                    contracts_obj = Sql.GetList("SELECT DISTINCT SERVICE_ID FROM CTCSCE (NOLOCK) WHERE CONTRACT_ID = '{ContractId}'".format(ContractId=self.source_contract_id))
                    if contracts_obj:
                        product_list = [(contract_obj.SERVICE_ID).strip() for contract_obj in contracts_obj]
                        product_list=','.join(map(str, product_list))					
                    try:
                        level = "COV OBJ RENEWAL ONE="+product_list+"="+self.contract_quote_record_id+"="+str(self.quote_revision_record_id)			
                        CQVLDRIFLW.iflow_valuedriver_rolldown(self.source_contract_id,level)
                    except:						
                        Log.Info("except renewal one SAQSCE")
                else:
                    #ENTITLEMENT SV TO CE AND GB
                    ancillary_dict =  ""
                    try: 
                        if Quote.GetCustomField('ANCILLARY_DICT').Content:
                            ancillary_dict = eval(Quote.GetCustomField('ANCILLARY_DICT').Content)
                            ancillary_dict = str(ancillary_dict[self.tree_param])
                        # if ancillary_dict:
                        # 	ancillary_dict_val_serv = (re.sub(r'^{|}$','',ancillary_dict)).split(':')[0]
                        # 	ancillary_dict_val = (re.sub(r'^{|"}$','',ancillary_dict)).split(': "')[1]
                        # 	ancillary_dict ={}
                        # 	ancillary_dict = eval(ancillary_dict_val)
                        ancillary_dict = ancillary_dict.replace("'",";39;").replace('{',"_;").replace("}","$;").replace(":","=")
                        #Quote.SetGlobal("ancillary_object_dict","")
                    except:
                        ancillary_dict = ""
                    
                    #Trace.Write("---ancillary_dict--"+str(ancillary_dict))
                    try:
                        #quote_ent_roll = self.contract_quote_record_id+"=="+str(ancillary_dict)
                        #and str(self.tree_param) == ancillary_dict_val
                        service_id = self.tree_param
                        if self.tree_param not in ('Receiving Equipment','Add-On Products') :
                            level = "COV OBJ ENTITLEMENT,"+str(service_id)+","+str(self.tree_parent_level_0)+","+str(self.user_id)+","+str(self.quote_revision_record_id)
                            CQVLDRIFLW.iflow_valuedriver_rolldown(self.contract_quote_record_id,level,ancillary_dict)
                            #CQVLDRIFLW.iflow_valuedriver_rolldown(quote_ent_roll,level,str(ancillary_dict))						
                    except:
                        Trace.Write("EXCEPT----COV OBJ ENTITLEMENT IFLOW")
                Entitlement_end_time = time.time()
                #Log.Info("Entitlement end==> "+str(Entitlement_end_time - Entitlement_start_time)
                #Commented to check the inforamtion
                # self._process_query(
                # 	"""DELETE FROM SYSPBT WHERE SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' and SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' and SYSPBT.BATCH_STATUS = 'IN PROGRESS'""".format(
                # 		BatchGroupRecordId=batch_group_record_id,RevisionRecordId=self.quote_revision_record_id
                # 	))
                covered_end_time = time.time()
                #Log.Info("ADD_COVERED_OBJ end==> "+str(covered_end_time - covered_start_time) +" QUOTE ID----"+str(self.contract_quote_id))
                d2 = Sql.GetFirst("""SELECT QTEREV_ID,GREENBOOK FROM SAQSGB WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND GREENBOOK='CMP' """.format(str(self.contract_quote_record_id),self.quote_revision_record_id))
                # try:
                # 	Trace.Write("PREDEFINED WAFER DRIVER IFLOW")
                # 	CQTVLDRIFW.valuedriver_predefined(self.contract_quote_record_id,"PREDEFINED DRIVER",self.tree_param, self.tree_parent_level_0, self.tree_parent_level_1, self.tree_parent_level_2,self.user_id,self.user_name,self.quote_revision_record_id)
                # except:
                # 	Trace.Write("EXCEPT----PREDEFINED DRIVER IFLOW")
    
            ##To write the below condition to call the function when the user is changing the quote type or preventive maintainence labor attribute in the service level entitlement when the tools are added before...
            #INC08621345 - Start - M
            if self.tools_from_ui != "Yes":
                additional_where = ""
                if self.applied_preventive_maintainence_quote_type_changed == "Yes" and self.tree_param in ("Z0009"):
                    quote_type_attribute_value = self.entitlement_value
                    batch_group_record_id = ""
                    self.applied_preventive_maintainence(entitlement_level_value = self.entitlement_level_value,entitlement_level = self.entitlement_level,batch_group_record_id=batch_group_record_id,quote_type_attribute_value = quote_type_attribute_value,applied_preventive_maintainence_quote_type_changed = self.applied_preventive_maintainence_quote_type_changed,pmevents_changes_insert = self.pmevents_changes_insert,additional_where=additional_where)
                if self.pmevents_changes_insert == "Yes":
                    batch_group_record_id = str(Guid.NewGuid()).upper()
                    equipment_record_ids = []
                    parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
                    service_equipment_query = Sql.GetList("SELECT QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{service_id}' """.format(QuoteRecordId = self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,service_id = self.tree_param))
                    for service_equipment in service_equipment_query:
                        equipment_record_ids.append(service_equipment.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)

                    record_ids = str(equipment_record_ids).replace("'","").replace("[","").replace("]","")
                    # service_entitlement_obj =Sql.GetFirst("""select ENTITLEMENT_XML from SAQTSE (nolock) where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{service_id}' """.format(QuoteRecordId = self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,service_id = self.tree_param))
                    Trace.Write("quote_type_attribute_value-"+str(self.ent_quote_type)+'-'+str(self.pm_entlmnt_val))
                    quote_type_attribute_value = self.ent_quote_type
                    service_id = ""
                    pm_event_attribute_value = ""
                    cm_labor = ""
                    if len(self.pm_entlmnt_val.split("||")) == 2:
                        pm_event_attribute_value = self.pm_entlmnt_val.split("||")[0]
                        cm_labor = self.pm_entlmnt_val.split("||")[1]
                    if quote_type_attribute_value and pm_event_attribute_value:
                        service_id = self.tree_param
                        if self.entitlement_level in ("GREENBOOK LEVEL","EQUIPMENT LEVEL"):
                            service_id = self.tree_parent_level_0

                        Trace.Write("service_id---"+str(service_id)+'-'+str(quote_type_attribute_value))
                        if pm_event_attribute_value and service_id not in ('Z0009','Z0010','Z0128'):
                            # pm_event_attribute_value = str(pm_entlmnt_val)
                            # pm_event_attribute_value == "PMSA Flex" or pm_event_attribute_value == "Event based")
                            additional_where = ''

                            Trace.Write("555 "+str(self.tree_param)+" 555 "+str(pm_event_attribute_value))
                            if pm_event_attribute_value== "Included - All PM" :
                                additional_where = " (ISNULL(MAEAPK.MNTEVT_LEVEL,'') IN ('Chamber / Module PM' ,'Scheduled Maintenance' )) AND"
                            elif pm_event_attribute_value == "Included - Monthly and Above" :
                                additional_where = " (MAEAPK.MNTEVT_LEVEL = 'Chamber / Module PM' OR MAEAPK.MNTEVT_LEVEL = 'Scheduled Maintenance') AND (MAEAPK.PM_ID = 'Monthly' OR MAEAPK.PM_ID = 'Quarterly' OR MAEAPK.PM_ID = 'Semi-Annual' OR MAEAPK.PM_ID = 'Annual') AND"
                            elif pm_event_attribute_value in ("Included - Quarterly and Above","Included - Qtrly and Above") :
                                additional_where = " (MAEAPK.MNTEVT_LEVEL = 'Chamber / Module PM' OR MAEAPK.MNTEVT_LEVEL = 'Scheduled Maintenance') AND (MAEAPK.PM_ID = 'Quarterly' OR MAEAPK.PM_ID = 'Semi-Annual' OR MAEAPK.PM_ID = 'Annual') AND"
                            elif cm_labor == "Included":
                                additional_where += " (ISNULL(MAEAPK.MNTEVT_LEVEL,'') IN ('Corrective Maintenance' ) AND MAEAPK.MNTEVT_LEVEL != '') AND "
                            # elif (self.tree_param in ("Z0099") and ("Included - Monthly and Above" in pm_event_attribute_value)):
                            #     additional_where = " (MAEAPK.MNTEVT_LEVEL = 'Chamber / Module PM' OR MAEAPK.MNTEVT_LEVEL = 'Scheduled Maintenance') AND (MAEAPK.PM_ID = 'Monthly' OR MAEAPK.PM_ID = 'Quarterly' OR MAEAPK.PM_ID = 'Semi-Annual' OR MAEAPK.PM_ID = 'Annual') AND"
                            if quote_type_attribute_value.upper() == "TOOL BASED" and (pm_event_attribute_value != "Excluded" or cm_labor == "Included"):
                                # if self.tree_param == "Z0099" and "Included - All PM" not in pm_event_attribute_value:
                                #     Trace.Write("Insert Restricted")
                                # else:
                                self._insert_quote_service_preventive_maintenance_kit_parts(entitlement_level_value = self.entitlement_level_value,entitlement_level = self.entitlement_level,batch_group_record_id=batch_group_record_id,quotetype_value_for_offering= quotetype_value_for_offering,additional_where = additional_where)
                                # pm_event_flag=1
                        if service_id in ('Z0009','Z0010','Z0128') :
                            # quote_type_attribute_value =re.findall(pattern_name,sub_string)
                            # Trace.Write("quote_type_attribute_value_chk "+str(quote_type_attribute_value))
                            if quote_type_attribute_value.upper() != 'TOOL BASED' :##Checking the Quote type before calling the events insert....
                                self.applied_preventive_maintainence_quote_type_changed = "Yes"
                                additional_where = ""
                                if service_id in ("Z0009") and pm_event_attribute_value == "Included - All PM":
                                    additional_where = " AND ((MAEAPK.MNTEVT_LEVEL = 'Chamber / Module PM' OR MAEAPK.MNTEVT_LEVEL = 'Scheduled Maintenance') AND MAEAPK.MNTEVT_LEVEL != '') "
                                    Trace.Write("additional_where_chk_1 "+str(additional_where))
                                    # if pm_event_attribute_value != "":
                                        
                                    #     qte_type_flag=1
                                if service_id in ("Z0009") and cm_labor == "Included":
                                    additional_where = " AND ((MAEAPK.MNTEVT_LEVEL = 'Corrective Maintenance') AND MAEAPK.MNTEVT_LEVEL != '') "
                                if service_id in ("Z0009") and pm_event_attribute_value == "Included - < Quarterly":
                                    additional_where = " AND (MAEAPK.MNTEVT_LEVEL = 'Chamber / Module PM' OR MAEAPK.MNTEVT_LEVEL = 'Scheduled Maintenance') AND (MAEAPK.PM_ID = 'Monthly' OR MAEAPK.PM_ID = 'Quarterly')"
                                    # if pm_event_attribute_value != "":
                                    #     self.applied_preventive_maintainence(entitlement_level_value = self.entitlement_level_value,entitlement_level = self.entitlement_level,batch_group_record_id=batch_group_record_id,quote_type_attribute_value = quote_type_attribute_value,applied_preventive_maintainence_quote_type_changed = self.applied_preventive_maintainence_quote_type_changed,pmevents_changes_insert = self.pmevents_changes_insert,additional_where=additional_where)
                                    #     qte_type_flag=1
                                self.applied_preventive_maintainence(entitlement_level_value = self.entitlement_level_value,entitlement_level = self.entitlement_level,batch_group_record_id=batch_group_record_id,quote_type_attribute_value = quote_type_attribute_value,applied_preventive_maintainence_quote_type_changed = self.applied_preventive_maintainence_quote_type_changed,pmevents_changes_insert = self.pmevents_changes_insert,additional_where=additional_where)
                            else:
                                # pm_event_attribute_value = re.findall(pattern_name,sub_string)
                                
                                if quote_type_attribute_value.upper() == "TOOL BASED" and (pm_event_attribute_value != "Excluded" or cm_labor == "Included"):
                                    Trace.Write("self.tree_param_chk "+str(self.tree_param)+" - "+"pm_event_attribute_value_chk "+str(pm_event_attribute_value))
                                    if service_id in ("Z0009") and pm_event_attribute_value == "Included - All PM":
                                        additional_where = " ((MAEAPK.MNTEVT_LEVEL = 'Chamber / Module PM' OR MAEAPK.MNTEVT_LEVEL = 'Scheduled Maintenance') AND MAEAPK.MNTEVT_LEVEL != '') AND"
                                        Trace.Write("additional_where_chk_1 "+str(additional_where))
                                        # if pm_event_attribute_value != "":
                                            
                                        #     qte_type_flag=1
                                    if service_id in ("Z0009") and cm_labor == "Included":
                                        additional_where += " ((MAEAPK.MNTEVT_LEVEL = 'Corrective Maintenance') AND MAEAPK.MNTEVT_LEVEL != '') AND"
                                    if service_id in ("Z0009") and pm_event_attribute_value == "Included - < Quarterly":
                                        additional_where = " (MAEAPK.MNTEVT_LEVEL = 'Chamber / Module PM' OR MAEAPK.MNTEVT_LEVEL = 'Scheduled Maintenance') AND (MAEAPK.PM_ID = 'Monthly' OR MAEAPK.PM_ID = 'Quarterly') AND"
                                        # if pm_event_attribute_value != "":
                                        #     self._insert_quote_service_preventive_maintenance_kit_parts(entitlement_level_value = self.entitlement_level_value,entitlement_level = self.entitlement_level,batch_group_record_id=batch_group_record_id,quotetype_value_for_offering= quotetype_value_for_offering,additional_where = additional_where)
                                        #     qte_type_flag=1
                                    self._insert_quote_service_preventive_maintenance_kit_parts(entitlement_level_value = self.entitlement_level_value,entitlement_level = self.entitlement_level,batch_group_record_id=batch_group_record_id,quotetype_value_for_offering= quotetype_value_for_offering,additional_where = additional_where)
                        # if (self.tree_param == 'Z0009' or self.tree_param == 'Z0010' or self.tree_param == 'Z0128') and qte_type_flag == 1:
                        #     break
                        # else:
                        #     if pm_event_flag == 1:
                        #         break
                #INC08621345 - End - M
        elif self.new_revision == "YES": ####A055S000P01-19173 code starts.. 
            self.tools_from_ui = "No"
            Log.Info("Revision NODE-"+str(self.quote_type_value)) #INC08621140,INC08638619
            quote_type_attribute_value = self.quote_type_value 
            self.applied_preventive_maintainence_quote_type_changed = "Yes"
            if quote_type_attribute_value.upper() == "TOOL BASED": #INC08621140,INC08638619
                self._insert_quote_service_preventive_maintenance_kit_parts()				
            else:
                self.applied_preventive_maintainence(applied_preventive_maintainence_quote_type_changed = self.applied_preventive_maintainence_quote_type_changed,quote_type_attribute_value = quote_type_attribute_value)
            ##A055S000P01-19173 code ends..
        return True
    
    def _update(self):
        pass

    def _delete(self):
        pass
    
class QuoteItemsCalculation(ContractQuoteCrudOpertion):
    def __init__(self, **kwargs):
        ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'), 
                                            tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
        self.opertion = kwargs.get('opertion')
        self.action_type = kwargs.get('action_type')
        self.values = kwargs.get('values')
        self.table_name = kwargs.get('table_name')
        self.all_values = kwargs.get('all_values')

    def _calculate(self):
        #contract_quote_obj = Sql.GetFirst(
        #			"""SELECT QUOTE_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' """.format(
        #				QuoteRecordId= self.contract_quote_record_id
        #			)
        #		)
        #QuoteID = contract_quote_obj.QUOTE_ID
        #Trace.Write("QuoteID--> "+str(self.contract_quote_id))
        Log.Info("===> QTPOSTACRM called from CQCRUDOPTN - QuoteItemsCalculation")
        ScriptExecutor.ExecuteGlobal('QTPOSTACRM',{'QUOTE_ID':self.contract_quote_id,'QTEREV_ID':self.quote_revision_id, 'Fun_type':'cpq_to_sscm'})
        
        # Approval Trigger - Start		
        #import ACVIORULES
        #violationruleInsert = ACVIORULES.ViolationConditions()
        #header_obj = Sql.GetFirst("SELECT RECORD_ID FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = 'SAQTRV'")
        #if header_obj:			
        ''' violationruleInsert.InsertAction(
                                            header_obj.RECORD_ID, self.quote_revision_record_id, "SAQTRV"
                                            ) '''
        # Approval Trigger - End
        return None


class ContractQuoteNoficationApprovalModel(ContractQuoteCrudOpertion):

    def __init__(self, **kwargs):
        ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'),tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
        self.opertion = kwargs.get('opertion')
        self.action_type = kwargs.get('action_type')
        self.values = kwargs.get('values')
        self.table_name = kwargs.get('table_name')
        self.all_values = kwargs.get('all_values')		
        self.node_id = ""

    def _get(self):
        gettransactionmessage = ""		
        get_approvaltxn_steps = Sql.GetList("select distinct ACAPCH.APRCHN_NAME,ACAPCH.APRCHN_ID,ACAPCH.APRCHN_DESCRIPTION from ACAPTX inner JOIN ACAPCH ON ACAPTX.APRCHN_RECORD_ID=ACAPCH.APPROVAL_CHAIN_RECORD_ID   where ACAPTX.APRTRXOBJ_ID = '{}' and  ACAPTX.APPROVALSTATUS NOT IN ('APPROVED')".format(self.contract_quote_id))		
        if get_approvaltxn_steps and str(current_prod).upper() == 'SALES':
            gettransactionmessage = 'This quote requires approval due to the following:'
            for val in get_approvaltxn_steps:				
                gettransactionmessage += ('<div class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-warning"><label> <img src="/mt/APPLIEDMATERIALS_DEV/Additionalfiles/warning1.svg" alt="Warning"> '+val.APRCHN_ID +' | Description : ' +val.APRCHN_DESCRIPTION+'</label></div></div>')
        return gettransactionmessage


class ContractQuoteNoficationModel(ContractQuoteCrudOpertion):
    def __init__(self, **kwargs):
        ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'),tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
                
        self.opertion = kwargs.get('opertion')
        self.action_type = kwargs.get('action_type')
        self.values = kwargs.get('values')
        self.table_name = kwargs.get('table_name')
        self.all_values = kwargs.get('all_values')		
        self.node_id = ""
        ##getting apr current rec id
        self.apr_current_record_id = kwargs.get('apr_current_record_id')

    def _get(self):
        quote_notif_obj = self._get_record_obj(
                    columns=["CPQTABLEENTRYDATEADDED", "CPQTABLEENTRYADDEDBY"],
                    table_name="SAQICO",
                    where_condition="QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND STATUS = 'APPROVAL REQUIRED'".format(self.contract_quote_record_id,self.quote_revision_record_id),
                    single_record=True,
                )
        # commented for time being performance need to rework
        #obj_list = ['SAQTSE','SAQSFE','SAQSGE','SAQSCE','SAQIEN']
        #obj_list = ['SAQIEN']
        # gettransactionmessage = ""		
        # get_approvaltxn_steps = Sql.GetList("select distinct ACAPCH.APRCHN_NAME,ACAPCH.APRCHN_ID,ACAPCH.APRCHN_DESCRIPTION from ACAPTX inner JOIN ACAPCH ON ACAPTX.APRCHN_RECORD_ID=ACAPCH.APPROVAL_CHAIN_RECORD_ID   where ACAPTX.APRTRXOBJ_ID = '{}' and  ACAPTX.APPROVALSTATUS NOT IN ('APPROVED')".format(self.contract_quote_id))		
        # if get_approvaltxn_steps and str(current_prod).upper() == 'SALES':
        # 	gettransactionmessage = 'This quote requires approval due to the following:'
        # 	for val in get_approvaltxn_steps:				
        # 		gettransactionmessage += ('<div class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-warning"><label> <img src="/mt/APPLIEDMATERIALS_DEV/Additionalfiles/warning1.svg" alt="Warning"> '+val.APRCHN_ID +' | Description : ' +val.APRCHN_DESCRIPTION+'</label></div></div>')
        quote_config_change = ""
        ent_message_query = Sql.GetFirst("SELECT MESSAGE_TEXT, RECORD_ID, OBJECT_RECORD_ID, MESSAGE_CODE, MESSAGE_LEVEL,MESSAGE_TYPE, OBJECT_RECORD_ID FROM SYMSGS (NOLOCK) WHERE RECORD_ID ='864BA37C-7523-4C7D-A586-6CEF1CABD682' and MESSAGE_LEVEL = 'WARNING'")
        ent_msg_txt = msg_txt = getostfactor = msg_app_txt = getpricefactor = ent_msg_gen_txt =""
        # AllParams = Param.AllParams
        #TreeParam = Product.GetGlobal("TreeParam")
        #notification banner start for add on product
        adoprod_table_value = Sql.GetFirst("SELECT MESSAGE_TEXT, RECORD_ID, OBJECT_RECORD_ID, MESSAGE_CODE, MESSAGE_LEVEL,MESSAGE_TYPE, OBJECT_RECORD_ID FROM SYMSGS (NOLOCK) WHERE OBJECT_RECORD_ID ='SYOBJ-01039' and MESSAGE_LEVEL = 'INFORMATION'")
        adoprod_message_query = check_active_query= ''
        #adoprod_message_query=Sql.GetList("SELECT distinct SAQSAO.QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID,SAQSAO.QUOTE_RECORD_ID,ACTIVE from SAQSAO inner join SAQSCO on SAQSCO.QUOTE_RECORD_ID = SAQSAO.QUOTE_RECORD_ID WHERE SAQSCO.QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id))
        
        #adoprod_message_query=Sql.GetList("SELECT distinct QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID from SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id))
        #check_active_query = Sql.GetList("SELECT distinct SAQSAO.QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID,SAQSAO.QUOTE_RECORD_ID,ACTIVE from SAQSAO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id))
        
        #check_active = [i for i in check_active_query if i.ACTIVE == True]	
        if adoprod_message_query and not check_active_query and str(current_prod).upper() == 'SALES':			
            msg_app_txt = (
                    '<div  class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-info"><label> <img src="/mt/APPLIEDMATERIALS_DEV/Additionalfiles/infor_icon_green.svg" alt="Warning">'
                    + str(adoprod_table_value.MESSAGE_LEVEL)
                    + " : "
                    + str(adoprod_table_value.MESSAGE_CODE)
                    + " : "
                    + str(adoprod_table_value.MESSAGE_TEXT)
                    + "</label></div></div>"
                )
        elif adoprod_message_query and check_active_query:			
            msg_app_txt =""
        ##notification banner ends
        
        #Approval Chain Steps notification banner starts
        if self.tree_param == "Approval Chain Steps" and str(current_prod).upper() == 'APPROVAL CENTER':
            
            # ent_msg_txt = (
            # 	'<div class="row modulesecbnr brdr" onclick="call_vertical_scrl()" data-toggle="collapse" data-target="#alertnotify" aria-expanded="true">NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div>'
            # )
            acapch_query =  Sql.GetList("SELECT * from ACAPCH (nolock) where APPROVAL_CHAIN_RECORD_ID  ='{}'".format(self.apr_current_record_id))
            acacst_query =  Sql.GetList("SELECT distinct APRCHN_RECORD_ID from ACACST WHERE APRCHN_RECORD_ID = '{}'".format(self.apr_current_record_id))
            
            if acapch_query and not acacst_query:
                
                msg_app_txt = (
                    '<div  class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-info"><label> <img src="/mt/APPLIEDMATERIALS_DEV/Additionalfiles/infor_icon_green.svg" alt="Warning">'
                    + ""
                    + "Please enter atleast one Approval Chain Step to associate with the Approval chains"
                    + "</label></div></div>"
                )
            elif acapch_query and acacst_query:
                
                msg_app_txt = ""
        #Approval Chain Steps notification banner ends	
        gettransactionmessage = ""
        #quoterecid = 'SAQTMT-'+self.contract_quote_record_id
        #getqtrec = Sql.GetFirst("select QUOTE_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"'")
        #get_approvaltxn_steps = Sql.GetList("select distinct ACAPCH.APRCHN_ID,ACAPCH.APRCHN_DESCRIPTION from ACAPMA (NOLOCK) JOIN ACAPCH ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID where ACAPMA.APRTRXOBJ_RECORD_ID = '"+str(self.contract_quote_record_id)+"' and ACAPMA.APRSTAMAP_APPROVALSTATUS NOT IN ('APPROVED')")
        #get_approvaltxn_steps = Sql.GetList("select DISTINCT ACAPCH.APRCHN_ID,ACAPCH.APRCHN_DESCRIPTION, APRCHN_RECORD_ID from ACAPMA (NOLOCK) JOIN ACAPCH ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID where ACAPMA.APRTRXOBJ_RECORD_ID = '"+str(self.contract_quote_record_id)+"' and NOT EXISTS (SELECT DISTINCT ACAPCH.APRCHN_ID from ACAPMA (NOLOCK) JOIN ACAPCH ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID where ACAPMA.APRTRXOBJ_RECORD_ID ='" +str(self.contract_quote_record_id)+"' and ACAPMA.APRSTAMAP_APPROVALSTATUS IN ('APPROVED')) ")
        get_quote_id  = Sql.GetFirst("select QUOTE_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id))
        
        if get_quote_id:

            get_approvaltxn_steps = Sql.GetList("select distinct ACAPCH.APRCHN_NAME,ACAPCH.APRCHN_ID,ACAPCH.APRCHN_DESCRIPTION from ACAPTX inner JOIN ACAPCH ON ACAPTX.APRCHN_RECORD_ID=ACAPCH.APPROVAL_CHAIN_RECORD_ID   where ACAPTX.APRTRXOBJ_ID = '{}' and  ACAPTX.APPROVALSTATUS NOT IN ('APPROVED')".format(get_quote_id.QUOTE_ID))
            Trace.Write('6571---'+str(current_prod))
            if get_approvaltxn_steps and str(current_prod).upper() == 'SALES':
                gettransactionmessage = 'This quote requires approval due to the following:'
                for val in get_approvaltxn_steps:
                    Trace.Write('6571--desc----'+str(val.APRCHN_DESCRIPTION))
                    #gettransactionmessage = '<p>This quote has to be approved for the following : </p>'
                    gettransactionmessage += ('<div class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-warning"><label> <img src="/mt/APPLIEDMATERIALS_DEV/Additionalfiles/warning1.svg" alt="Warning"> '+val.APRCHN_ID +' | Description : ' +str(val.APRCHN_DESCRIPTION).upper()+'</label></div></div>')
            if self.tree_param == "Fab Locations" and str(current_prod).upper() == 'SALES':
                Trace.Write("fab_delete===========")
                fab_location_msg_notification = Sql.GetFirst("SELECT MESSAGE_TEXT, RECORD_ID, OBJECT_RECORD_ID, MESSAGE_CODE, MESSAGE_LEVEL,MESSAGE_TYPE, OBJECT_RECORD_ID FROM SYMSGS (NOLOCK) WHERE RECORD_ID ='429E4C2B-F380-45E6-A364-D65429357461' and MESSAGE_LEVEL = 'INFORMATION'")

                fab_location_data = Sql.GetList(" SELECT * FROM SAQFBL (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId= self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
                if fab_location_data:
                    quote_config_change = (
                        '<div  class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-info"><label> <img src="/mt/APPLIEDMATERIALS_DEV/Additionalfiles/infor_icon_green.svg" alt="Warning">'
                        + str(fab_location_msg_notification.MESSAGE_LEVEL)
                        + " : "
                        + str(fab_location_msg_notification.MESSAGE_TEXT)
                        + "</label></div></div>"
                    )
            getStatus = Sql.GetFirst("SELECT REVISION_STATUS,MODVRS_DIRTY_FLAG FROM SAQTRV (NOLOCK) WHERE QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(get_quote_id.QUOTE_ID,self.quote_revision_record_id))
            getFlag = Sql.GetFirst("SELECT MODVRS_DIRTY_FLAG FROM SAQICO (NOLOCK) WHERE QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(get_quote_id.QUOTE_ID,self.quote_revision_record_id))
            getItemFlag = Sql.GetFirst("SELECT MODVRS_DIRTY_FLAG FROM SAQRIT (NOLOCK) WHERE QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(get_quote_id.QUOTE_ID,self.quote_revision_record_id))
            edit_config_notification_query = Sql.GetFirst("SELECT DIRTY_FLAG FROM SAQTRV (NOLOCK) WHERE QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(get_quote_id.QUOTE_ID,self.quote_revision_record_id))
            if edit_config_notification_query:
                if str(edit_config_notification_query.DIRTY_FLAG) == "True":
                    gettransactionmessage += ('<div class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-warning"><label> <img src="/mt/APPLIEDMATERIALS_DEV/Additionalfiles/warning1.svg" alt="Warning"> The quote configuration has changed. Please click on the complete stage button to regenerate the quote items.</label></div></div>')
            if getStatus.REVISION_STATUS == "APPROVED":
                gettransactionmessage = ""
            if getStatus:
                if getStatus.MODVRS_DIRTY_FLAG == 1:
                    gettransactionmessage += 'This Quote has the following notifications:'
                    gettransactionmessage += ('<div class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-warning"><label> <img src="/mt/APPLIEDMATERIALS_DEV/Additionalfiles/warning1.svg" alt="Warning"> 99999 | NEW COST MODEL VERSIONS AVAILABLE | There are new cost model versions available from SSCM. In order to update the costs and prices, please revision the quote.</label></div></div>')
            elif getItemFlag:
                if getItemFlag.MODVRS_DIRTY_FLAG == 1:
                    gettransactionmessage += 'This Quote has the following notifications:'
                    gettransactionmessage += ('<div class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-warning"><label> <img src="/mt/APPLIEDMATERIALS_DEV/Additionalfiles/warning1.svg" alt="Warning"> 99999 | NEW COST MODEL VERSIONS AVAILABLE | There are new cost model versions available from SSCM. In order to update the costs and prices, please revision the quote.</label></div></div>')
            elif getFlag:
                if getFlag.MODVRS_DIRTY_FLAG == 1:
                    gettransactionmessage += 'This Quote has the following notifications:'
                    gettransactionmessage += ('<div class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-warning"><label> <img src="/mt/APPLIEDMATERIALS_DEV/Additionalfiles/warning1.svg" alt="Warning"> 99999 | NEW COST MODEL VERSIONS AVAILABLE | There are new cost model versions available from SSCM. In order to update the costs and prices, please revision the quote.</label></div></div>')
            # saqrit_status = []
            # saqico_status = []
            # get_tkm_status = Sql.GetList("SELECT SAQRIT.STATUS AS SAQRIT_STATUS,SAQICO.STATUS AS SAQICO_STATUS FROM SAQRIT (NOLOCK) INNER JOIN SAQICO (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID  WHERE SAQRIT.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQRIT.QTEREV_RECORD_ID = '{quote_rev_rec_id}'".format(quote_rec_id = self.contract_quote_record_id,quote_rev_rec_id = self.quote_revision_record_id))
            # for status in get_tkm_status:
            # 	saqrit_status.append(status.SAQRIT_STATUS)
            # 	saqico_status.append(status.SAQICO_STATUS)
            # get_revision_status = Sql.GetFirst("SELECT REVISION_STATUS FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_rev_rec_id}'")
            # if get_revision_status.REVISION_STATUS == "CFG-ON HOLD TKM":
            # 	gettransactionmessage += '<div class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-warning"><label> <img src="/mt/APPLIEDMATERIALS_DEV/Additionalfiles/warning1.svg" alt="Warning">The quote revision is on hold due to missing TKM Kit IDs. Your quote will automatically transition out of the hold status once all TKM Kit IDs are available in SSCM.</label></div></div>'
        #Trace.Write('gettransactionmessage---'+str(gettransactionmessage))
        # if ent_message_query:
        # 	#for val in obj_list:
        # 	tablename = 'SAQTSE'
        # 	#check_fabvantage_messgae_query = Sql.GetFirst("SELECT ENTITLEMENT_COST_IMPACT,ENTITLEMENT_PRICE_IMPACT from {} where QUOTE_RECORD_ID = '{}'  and PRICE_METHOD = 'MANUAL PRICE' and ENTITLEMENT_NAME  = 'ADDL_PERF_GUARANTEE_91_1'".format(val,self.contract_quote_record_id))
        # 	#commented on 31 maarch start
        # 	#check_fabvantage_messgae_query = Sql.GetList("select ENTITLEMENT_COST_IMPACT,ENTITLEMENT_PRICE_IMPACT from (SELECT distinct e.QUOTE_RECORD_ID, replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(IS_DEFAULT)[1]', 'VARCHAR(128)'),';#38','&') as IS_DEFAULT,replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT,replace(X.Y.value('(ENTITLEMENT_TYPE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_TYPE,replace(X.Y.value('(PRICE_METHOD)[1]', 'VARCHAR(128)'),';#38','&') as PRICE_METHOD,replace(X.Y.value('(ENTITLEMENT_VALUE_CODE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value('(ENTITLEMENT_DESCRIPTION)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_DESCRIPTION,replace(X.Y.value('(ENTITLEMENT_DISPLAY_VALUE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_DISPLAY_VALUE FROM (select QUOTE_RECORD_ID,convert(xml,replace(ENTITLEMENT_XML,'&',';#38')) as ENTITLEMENT_XML from {} (nolock) where QUOTE_RECORD_ID = '{}') e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) ) as m where PRICE_METHOD ='MANUAL PRICE'".format(val,self.contract_quote_record_id))
        # 	#end 31 march
        # 	if str(self.contract_quote_record_id):
        # 		#getinnercon  = Sql.GetFirst("select QUOTE_RECORD_ID,convert(xml,replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML from SAQTSE (nolock)  where  QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"'")
        # 		entitlement_obj  = Sql.GetFirst("SELECT ENTITLEMENT_XML FROM SAQTSE (NOLOCK) WHERE QUOTE_RECORD_ID= '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
        # 		if entitlement_obj:
        # 			#check_fabvantage_messgae_query = Sql.GetList("SELECT distinct e.QUOTE_RECORD_ID, replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(PRICE_METHOD)[1]', 'VARCHAR(128)'),';#38','&') as PRICE_METHOD,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT FROM (select '"+str(getinnercon.QUOTE_RECORD_ID)+"' as QUOTE_RECORD_ID,convert(xml,'"+str(getinnercon.ENTITLEMENT_XML)+"') as ENTITLEMENT_XML ) e  OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y)  ")
        # 			#if check_fabvantage_messgae_query:
        # 			#for val in check_fabvantage_messgae_query:
        # 			entitlement_xml = entitlement_obj.ENTITLEMENT_XML
        # 			quote_item_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
        # 			pattern_pricemethod = re.compile(r'<PRICE_METHOD>([^>]*?)</PRICE_METHOD>')
        # 			pattern_costimpact = re.compile(r'<ENTITLEMENT_COST_IMPACT>([^>]*?)</ENTITLEMENT_COST_IMPACT>')
        # 			pattern_priceimpact = re.compile(r'<ENTITLEMENT_PRICE_IMPACT>([^>]*?)</ENTITLEMENT_PRICE_IMPACT>')
        # 			for m in re.finditer(quote_item_tag, entitlement_xml):
        # 				sub_string = m.group(1)
        # 				pricemethod_match = re.findall(pattern_pricemethod,sub_string)
        # 				if pricemethod_match == 'MANUAL PRICE':
        # 					cost_impact = re.findall(pattern_costimpact,sub_string)
        # 					price_impact = re.findall(pattern_priceimpact,sub_string)
        # 					getostfactor = cost_impact
        # 					getpricefactor = price_impact 
        # 					#if val.PRICE_METHOD == 'MANUAL PRICE':
        # 					#getostfactor = val.ENTITLEMENT_COST_IMPACT
        # 					#getpricefactor = val.ENTITLEMENT_PRICE_IMPACT								
        # 					if str(getostfactor).strip != "" and  str(getpricefactor).strip() != "":									
        # 						ent_msg_txt = ""									
        # 					else:									
        # 						errorLogDeleteQuery = "DELETE SYELOG FROM SYELOG (NOLOCK) INNER JOIN SYMSGS (NOLOCK) ON SYMSGS.RECORD_ID = SYELOG.ERRORMESSAGE_RECORD_ID AND SYMSGS.TRACK_HISTORY = 0 WHERE SYMSGS.MESSAGE_CODE = '000001' AND SYELOG.OBJECT_RECORD_ID = 'E5504B40-36E7-4EA6-9774-EA686705A63F'  AND SYELOG.OBJECT_VALUE = '{}' AND SYELOG.OBJECT_VALUE_REC_ID = '{}'".format(self.contract_quote_record_id, self.contract_quote_record_id)
        # 						Sql.RunQuery(errorLogDeleteQuery)
        # 						insertErrLogWarnQuery = """INSERT SYELOG (ERROR_LOGS_RECORD_ID, ERRORMESSAGE_RECORD_ID, ERRORMESSAGE_DESCRIPTION, OBJECT_NAME, OBJECT_TYPE, OBJECT_RECORD_ID, OBJECT_VALUE_REC_ID, OBJECT_VALUE, ACTIVE, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
        # 							select
        # 							CONVERT(VARCHAR(4000),NEWID()) as ERROR_LOGS_RECORD_ID, 
        # 							SAPCPQ_ATTRIBUTE_NAME as ERRORMESSAGE_RECORD_ID,
        # 							MESSAGE_TEXT as ERRORMESSAGE_DESCRIPTION,
        # 							'{table_name}' as OBJECT_NAME,
        # 							MESSAGE_TYPE as OBJECT_TYPE,
        # 							OBJECT_RECORD_ID as OBJECT_RECORD_ID,
        # 							'{quoteId}' as OBJECT_VALUE_REC_ID,
        # 							'{quoteId}' as OBJECT_VALUE,
        # 							1 as ACTIVE,
        # 							'{Get_UserID}' as CPQTABLEENTRYADDEDBY, 
        # 							convert(varchar(10), '{datetime_value}', 101) as CPQTABLEENTRYDATEADDED, 
        # 							'{Get_UserID}' as CpqTableEntryModifiedBy, 
        # 							convert(varchar(10), '{datetime_value}', 101) as CpqTableEntryDateModified
        # 							from SYMSGS (nolock)
        # 							where  OBJECT_RECORD_ID = '87896663-6F9D-4D6E-B1C1-6DA146B56815' and MESSAGE_LEVEL = 'WARNING' and MESSAGE_CODE = '000001'
        # 						""".format(
        # 							quoteId=self.contract_quote_record_id,
        # 							Get_UserID=self.user_id,
        # 							datetime_value=self.datetime_value,
        # 							table_name = tablename
        # 						)
        # 						Sql.RunQuery(insertErrLogWarnQuery)
        # 						ent_msg_txt = (
        # 							'<div class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-warning"><label> <img src="/mt/APPLIEDMATERIALS_DEV/Additionalfiles/warning1.svg" alt="Warning"> '
        # 							+ str(ent_message_query.MESSAGE_LEVEL)
        # 							+ " : "
        # 							+ str(ent_message_query.MESSAGE_CODE)
        # 							+ " : "
        # 							+ str(ent_message_query.MESSAGE_TEXT)
        # 							+ "</label></div></div>"
        # 						)
        # 				else:
        # 					ent_msg_txt = ""
        # 	else:
        # 		ent_msg_txt = ""
        # 	if quote_notif_obj:
        # 		info_message_obj = Sql.GetFirst("SELECT MESSAGE_TEXT, RECORD_ID, OBJECT_RECORD_ID, MESSAGE_CODE, MESSAGE_LEVEL,MESSAGE_TYPE, OBJECT_RECORD_ID FROM SYMSGS (NOLOCK) WHERE RECORD_ID ='9A7602EE-46D9-4891-BCD9-BBCB4B3E313E' and MESSAGE_LEVEL = 'WARNING'")
                
        # 		if info_message_obj:
        # 			errorLogDeleteQuery = "DELETE SYELOG FROM SYELOG (NOLOCK) INNER JOIN SYMSGS (NOLOCK) ON SYMSGS.SAPCPQ_ATTRIBUTE_NAME = SYELOG.ERRORMESSAGE_RECORD_ID AND SYMSGS.TRACK_HISTORY = 0 WHERE SYMSGS.MESSAGE_CODE = '000006' AND SYELOG.OBJECT_RECORD_ID = 'E5504B40-36E7-4EA6-9774-EA686705A63F' AND SYELOG.OBJECT_NAME = 'SAQICO' AND SYELOG.OBJECT_VALUE = '{}' AND SYELOG.OBJECT_VALUE_REC_ID = '{}'".format(self.contract_quote_record_id, self.contract_quote_record_id)
        # 			Sql.RunQuery(errorLogDeleteQuery)
        # 			insertErrLogWarnQuery = """INSERT SYELOG (ERROR_LOGS_RECORD_ID, ERRORMESSAGE_RECORD_ID, ERRORMESSAGE_DESCRIPTION, OBJECT_NAME, OBJECT_TYPE, OBJECT_RECORD_ID, OBJECT_VALUE_REC_ID, OBJECT_VALUE, ACTIVE, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
        # 				select
        # 				CONVERT(VARCHAR(4000),NEWID()) as ERROR_LOGS_RECORD_ID, 
        # 				SAPCPQ_ATTRIBUTE_NAME as ERRORMESSAGE_RECORD_ID,
        # 				MESSAGE_TEXT as ERRORMESSAGE_DESCRIPTION,
        # 				OBJECT_APINAME as OBJECT_NAME,
        # 				MESSAGE_TYPE as OBJECT_TYPE,
        # 				OBJECT_RECORD_ID as OBJECT_RECORD_ID,
        # 				'{quoteId}' as OBJECT_VALUE_REC_ID,
        # 				'{quoteId}' as OBJECT_VALUE,
        # 				1 as ACTIVE,
        # 				'{Get_UserID}' as CPQTABLEENTRYADDEDBY, 
        # 				convert(varchar(10), '{datetime_value}', 101) as CPQTABLEENTRYDATEADDED, 
        # 				'{Get_UserID}' as CpqTableEntryModifiedBy, 
        # 				convert(varchar(10), '{datetime_value}', 101) as CpqTableEntryDateModified
        # 				from SYMSGS (nolock)
        # 				where OBJECT_APINAME = 'SAQICO' and OBJECT_RECORD_ID = 'E5504B40-36E7-4EA6-9774-EA686705A63F' and MESSAGE_LEVEL = 'WARNING' and MESSAGE_CODE = '000006'
        # 			""".format(
        # 				quoteId=self.contract_quote_record_id,
        # 				Get_UserID=self.user_id,
        # 				datetime_value=self.datetime_value,
        # 			)
                
                
        # Is Changed Information Notification - Start
        #equip_level_entitlement_obj = Sql.GetFirst("SELECT QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID FROM SAQSCE (NOLOCK) WHERE IS_CHANGED = 1 AND QUOTE_RECORD_ID= '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
        #if equip_level_entitlement_obj:
            # log_message_obj = Sql.GetFirst(
            # 		"SELECT TOP 1000 SYMSGS.MESSAGE_TEXT, SYMSGS.MESSAGE_TYPE, SYMSGS.MESSAGE_CODE, SYMSGS.MESSAGE_LEVEL FROM SYMSGS (nolock) INNER JOIN SYELOG (NOLOCK) ON SYELOG.ERRORMESSAGE_RECORD_ID = SYMSGS.RECORD_ID WHERE SYMSGS.MESSAGE_CODE = '200112' AND SYMSGS.MESSAGE_LEVEL = 'INFORMATION' AND SYELOG.OBJECT_VALUE = '{QuoteId}' AND SYELOG.OBJECT_VALUE_REC_ID = '{QuoteRecordId}' ORDER BY abs(SYMSGS.MESSAGE_CODE)".format(
            # 			QuoteId=self.contract_quote_id,
            # 			QuoteRecordId=self.contract_quote_record_id
            # 		)
            # 	)
            # if log_message_obj:
            # 	ent_msg_txt += (
            # 		'<div class="col-md-12" id="entitlement-info"><div class="col-md-12 alert-info"><label> <img src="/mt/APPLIEDMATERIALS_DEV/Additionalfiles/infocircle1.svg" alt="Info"> '
            # 		+ str(log_message_obj.MESSAGE_LEVEL)
            # 		+ " : "
            # 		+ str(log_message_obj.MESSAGE_CODE)
            # 		+ " : "
            # 		+ str(log_message_obj.MESSAGE_TEXT)
            # 		+ "</label></div></div>"
            # 	)
        # Is Changed Information Notification
        return ent_msg_txt,msg_app_txt,gettransactionmessage,ent_msg_gen_txt,quote_config_change

class ContractQuoteApprovalModel(ContractQuoteCrudOpertion):
    def __init__(self, **kwargs):
        ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'), 
                                            tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
        #self.opertion = kwargs.get('opertion')
        #self.action_type = kwargs.get('action_type')
    def _update(self):		
        if self.trigger_from == "APPROVED":
            Sql.RunQuery("UPDATE SAQTMT SET QUOTE_STATUS = 'APPROVED' WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id))
            Log.Info("===> QTPOSTACRM called from CQCRUDOPTN - ContractQuoteApprovalModel")
            result = ScriptExecutor.ExecuteGlobal("QTPOSTACRM", {"QUOTE_ID": self.contract_quote_id, 'Fun_type':'cpq_to_crm'})
        elif self.trigger_from == "SUBMIT FOR APPROVAL":
            Sql.RunQuery("UPDATE SAQTMT SET QUOTE_STATUS = 'APPROVAL REQUIRED' WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id))
        """ ScriptExecutor.ExecuteGlobal(
            "SYALLTABOP",
            {"Primary_Data": str(self.contract_quote_record_id), "TabNAME": "Quote", "ACTION": "VIEW", "RELATED": ""},
        ) """
class ContractQuoteBillingMatrixModel(ContractQuoteCrudOpertion):
    def __init__(self, **kwargs):
        ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'),
                                            tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
        self.opertion = kwargs.get('opertion')
        self.action_type = kwargs.get('action_type')
        self.values = kwargs.get('values')
        self.table_name = kwargs.get('table_name')
        self.all_values = kwargs.get('all_values')		
        self.node_id = ""
    def _update(self):		
        result = {}
        for array_val in self.values:            
            for data in array_val:
                result[data.Key] = data.Value

        # Sql.RunQuery("""UPDATE SAQIBP
        # 			SET BILLING_DATE = '{NewBillingDate}'                    
        # 			WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND BILLING_DATE = '{OldBillingDate}' AND SERVICE_ID = '{ServiceId}'""".format(
        # 			NewBillingDate=result.get('modified_date'), QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, 
        # 			OldBillingDate=result.get('billing_date'),ServiceId =result.get('service_id')
        # ))
                
        return True	

class QuoteAccountModel(ContractQuoteCrudOpertion):
    def __init__(self, **kwargs):
        ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'),tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
        self.opertion = kwargs.get('opertion')
        self.action_type = kwargs.get('action_type')
        self.values = kwargs.get('values')
        self.replace_contact = kwargs.get('replace_contact')
    def _create(self):
        import CQCPQC4CWB
        if self.action_type == "REPLACE_ACCOUNT":
            get_obj_id = Sql.GetFirst("SELECT OBJECT_ID FROM SAQTIP WHERE CpqTableEntryId = '{}' ".format(self.replace_contact.split('-')[1].lstrip('0')))
            if get_obj_id.OBJECT_ID is None or get_obj_id.OBJECT_ID =="":
                input_data = {"ACTION":"GET_OBJECTID"}
                CQCPQC4CWB.writeback_to_c4c("involved_parties", self.contract_quote_record_id, self.quote_revision_record_id,input_data)
                get_obj_id = Sql.GetFirst("SELECT OBJECT_ID FROM SAQTIP WHERE CpqTableEntryId = '{}' ".format(self.replace_contact.split('-')[1].lstrip('0')))
                Trace.Write('First time updated object id-->'+str(get_obj_id.OBJECT_ID))
            Sql.RunQuery("DELETE FROM SAQTIP WHERE CpqTableEntryId = '{}' ".format(self.replace_contact.split('-')[1].lstrip('0')))
            get_account_details = Sql.GetFirst("SELECT a.*,B.ADDRESS_1 from SAACPF A JOIN SAACNT B ON B.ACCOUNT_ID = A.PARTNER_ID WHERE A.CpqTableEntryId = '{}' ".format(self.values[0].split('-')[1].lstrip('0')))
            account_table_info = SqlHelper.GetTable("SAQTIP")
            partner_function = function_id = get_account_details.PARTNERFUNCTION_ID
            if partner_function == "SH":
                partner_function = "SHIP TO"
                role_code = "1005"
            elif partner_function == "BP":
                partner_function = "BILL TO"
                role_code = "10"
            elif partner_function == "PY":
                partner_function = "PAYER"	
                role_code = "8"
            account_table = {
                "QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
                "QUOTE_ID": self.contract_quote_id,
                "QUOTE_NAME": str(self.contract_quote_name).replace("'","''"),
                "QUOTE_RECORD_ID": self.contract_quote_record_id,
                "QTEREV_ID": self.quote_revision_id,
                "QTEREV_RECORD_ID": self.quote_revision_record_id,
                "IS_MAIN": 'TRUE',
                "PRIMARY": 'TRUE',
                "PARTNERFUNCTION_ID" : function_id,
                "PARTY_ID": get_account_details.PARTNER_ID,
                "PARTY_NAME": get_account_details.PARTNER_NAME,
                "CPQ_PARTNER_FUNCTION":partner_function,
                "ADDRESS":get_account_details.ADDRESS_1,
                "OBJECT_ID":get_obj_id.OBJECT_ID
            } 
            account_table_info.AddRow(account_table)
            Sql.Upsert(account_table_info)
            try:
                input_data = {"PARTY_ID":get_account_details.PARTNER_ID,"ROLE_CODE":role_code,"OBJECT_ID":get_obj_id.OBJECT_ID,"ACTION":"UPDATE_C4C"}
                CQCPQC4CWB.writeback_to_c4c("involved_parties", self.contract_quote_record_id, self.quote_revision_record_id,input_data)
            except Exception as e:
                Log.Info('Writeback to C4C of Involved Parties Failed due to '+str(e))

def Factory(node=None):
    """Factory Method"""
    models = {
        "OFFERINGS MODEL": ContractQuoteOfferingsModel,
        
        "FAB MODEL": ContractQuoteFabModel,
        "TOOL RELOCATION MODEL":ToolRelocationModel,
        "COVERED OBJ MODEL": ContractQuoteCoveredObjModel,		
        "QUOTE ITEM CALCULATION": QuoteItemsCalculation,
        "QUOTE LEVEL NOTIFICATION": ContractQuoteNoficationModel,
        "QUOTE APPROVAL LEVEL NOTIFICATION":ContractQuoteNoficationApprovalModel,
        "QUOTE APPROVAL MODEL":ContractQuoteApprovalModel,
        "BILLING MATRIX MODEL": ContractQuoteBillingMatrixModel,
        #"QUOTE ITEMS MODEL":ContractQuoteItemsModel,
        "PARTS MODEL": PartsListModel,
        "ACCOUNT MODEL":QuoteAccountModel
    }
    return models[node]

if hasattr(Param, 'CPQ_Columns'):
    Trace.Write("Started Here...>")
    Trace.Write(Param.CPQ_Columns)
    integration_param_objects = Param.CPQ_Columns
    integration_param = {}
    for integration_param_object in integration_param_objects: 
        integration_param[str(integration_param_object.Key)] = str(integration_param_object.Value)		
    opertion = integration_param.get('Opertion')
    node_type = integration_param.get('NodeType')
    try:
        values = integration_param.get('Values')
    except Exception:
        values = []

    try:
        all_values = integration_param.get('AllValues')
    except Exception:
        all_values = False
    try:
        table_name = integration_param.get('ObjectName')
    except Exception:
        table_name = None
    try:
        action_type = integration_param.get('ActionType')
    except Exception:
        action_type = None
    try:
        trigger_from = integration_param.get('TriggerFrom')
    except Exception:
        trigger_from = None
    try:
        service_id = integration_param.get('service_id')
    except Exception:
        service_id = None
    try:
        service_type = integration_param.get('service_type')
    except Exception:
        service_type = None             
    try:
        get_response = integration_param.get('GetResponse')
    except Exception:
        get_response = False
    try:
        contract_quote_record_id = integration_param.get('ContractQuoteRecordId')	
    except Exception:
        contract_quote_record_id = False
    try:
        objname = integration_param.get('OBJECTNAME')	
    except Exception:
        objname = False
    try:
        bmtreeparam = integration_param.get('TREEPARAM')	
    except Exception:
        bmtreeparam = False
    try:
        currrecordid = integration_param.get('CurrentRecordId')	
    except Exception:
        currrecordid = False
    
    # Integration call to update billing matrix - End
else:
    try:
        opertion = Param.Opertion
        node_type = Param.NodeType
        try:
            values = Param.Values
        except Exception:
            values = []
        try:
            A_Keys = Param.A_Keys
            A_Values = Param.A_Values
        except:
            A_Keys = ""
            A_Values = ""
        try:
            ADDON_PRD_ID = Param.ADDON_PRD_ID
        except:
            ADDON_PRD_ID = ""
        try:
            all_values = Param.AllValues
        except Exception:
            all_values = False
        try:
            table_name = Param.ObjectName
        except Exception:
            table_name = None
        try:
            action_type = Param.ActionType
        except Exception:
            action_type = None
        try:
            trigger_from = Param.TriggerFrom
        except Exception:
            trigger_from = None
        try:
            service_id = Param.ServiceId
        except Exception:
            service_id = None
        try:
            real_time_integration_service = Param.RealTimeIntegrationService
        except Exception:
            real_time_integration_service = None
        try:
            service_type = Param.ServiceType
        except Exception:
            service_type = None  
        try:
            tree_parent_level_1 = Param.tree_parent_level_1
        except Exception:
            tree_parent_level_1 = None	           
        try:
            get_response = Param.GetResponse
        except Exception:
            get_response = False
        try:
            apr_current_record_id = Param.CurrentRecordId
        except Exception:
            apr_current_record_id = None
        try:
            objname = Param.OBJECTNAME
        except Exception:
            objname = None
        try:
            bmtreeparam = Param.TREEPARAM
        except Exception:
            bmtreeparam = None
        try:
            contract_quote_record_id = Param.ContractQuoteRecordId	
        except Exception:
            contract_quote_record_id = False
        try:
            new_part = Param.new_part
        except:
            Trace.Write("new_part Exception")
            new_part = 0
        try:
            inclusion = Param.inclusion
        except:
            Trace.Write("inclusion Exception")
            inclusion = 0
        try:
            tools_from_ui = Param.tools_from_ui
        except:
            tools_from_ui = "No"
        try:
            entitlement_level = Param.entitlement_level
        except:
            entitlement_level = "OFFERING LEVEL"
        try:
            entitlement_level_value = Param.entitlement_level_value
        except:
            entitlement_level_value = "No"
        try:
            tool_type = Param.TOOL_TYPE
        except:
            tool_type = ""
        ##Added the param to insert the pmsa related child tables when the user is changing the quote type from tool based to event based or flex based...
        try:
            applied_preventive_maintainence_quote_type_changed = Param.applied_preventive_maintainence_quote_type_changed
        except:
            applied_preventive_maintainence_quote_type_changed = "No"
        try:
            entitlement_value = Param.entitlement_value
        except:
            entitlement_value = ""
        try:
            pmevents_changes_insert = Param.pmevents_changes_insert
        except:
            pmevents_changes_insert = "No"
        try:
            pm_entlmnt_val = Param.pm_entlmnt_val
        except:
            pm_entlmnt_val = ""
        #INC08621345 - Start - A
        try:
            ent_quote_type = Param.ent_quote_type
        except:
            ent_quote_type = ""
        #INC08621345 - End - A
        ##A055S000P01-19173 code starts..
        ##Added the below param to receive the value from the CQREVISION script while creating new revision...
        try:
            new_revision = Param.NewRevision
        except:
            new_revision = "NO"
        try:
            quote_type_value = Param.QuoteTypeValue
        except:
            quote_type_value = "NO"
        ##A055S000P01-19173 code starts..
        try:
            tool_type = Param.TOOL_TYPE
        except:
            tool_type = ""
        try:
            replace_contact = Param.ReplaceContact
        except:
            replace_contact = ""
    except Exception as e:
        Trace.Write('error-'+str(e))
        pass	

node_object = Factory(node_type)(
    opertion=opertion, action_type=action_type, table_name=table_name, values=values, 
    all_values=all_values, trigger_from=trigger_from, contract_quote_record_id=contract_quote_record_id, 
    tree_param=service_id, tree_parent_level_0=service_type,tree_parent_level_1 = tree_parent_level_1,apr_current_record_id= apr_current_record_id,new_part=new_part,tool_type=tool_type,inclusion = inclusion,applied_preventive_maintainence_quote_type_changed = applied_preventive_maintainence_quote_type_changed,pmevents_changes_insert= pmevents_changes_insert,pm_entlmnt_val=pm_entlmnt_val,ent_quote_type = ent_quote_type, entitlement_value = entitlement_value,tools_from_ui = tools_from_ui,entitlement_level = entitlement_level,entitlement_level_value = entitlement_level_value,new_revision = new_revision,quote_type_value = quote_type_value,real_time_integration_service = real_time_integration_service,replace_contact = replace_contact
)#INC08621345 - ent_quote_type added
##A055S000P01-19173 ... added the new_revision as new param...

if opertion == "ADD":
    node_object._create()
elif opertion == "UPDATE":
    node_object._update()
elif opertion == "DELETE":
    response = node_object._delete()
    if get_response:
        ApiResponse = ApiResponseFactory.JsonResponse(response)
elif opertion == "GET":
    ApiResponse = ApiResponseFactory.JsonResponse(node_object._get())
elif opertion == "CALCULATE":
    node_object._calculate()
