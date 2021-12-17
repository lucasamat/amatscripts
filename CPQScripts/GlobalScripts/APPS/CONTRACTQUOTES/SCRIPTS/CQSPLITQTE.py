# =========================================================================================================================================
#   __script_name : CQSPLITQTE.PY
#   __script_description : THIS SCRIPT IS USED TO SPLIT THE ITEMS BY PRODUCT OFFERINGS
#   __primary_author__ : WASIM.ABDUL
#   __create_date :12-13-2021
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

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct() or "Sales"
try:
    contract_quote_record_id = Quote.QuoteId
except:
    contract_quote_record_id = ''

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

def splitserviceinsert():
    splitservice_object = 'Z0105'
    material_obj = Sql.GetFirst("SELECT MATERIAL_RECORD_ID,SAP_DESCRIPTION,MATERIALCONFIG_TYPE FROM MAMTRL WHERE SAP_PART_NUMBER = '{}'".format(splitservice_object))
    service_list=[]
    #NEED TO change Query for SAQRIT
    get_existing_record = Sql.GetList("SELECT SERVICE_ID FROM SAQRIT WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SPLIT = 'YES'".format(contract_quote_rec_id,quote_revision_rec_id))
    for i in get_existing_record:
        service_list.append(i.SERVICE_ID)
    parservice_values=tuple(service_list)
    parservice_values=re.sub('\,\)',')',str(parservice_values))
    if get_existing_record:
        description = material_obj.SAP_DESCRIPTION
        material_record_id = material_obj.MATERIAL_RECORD_ID

        Sql.RunQuery("""INSERT SAQTSV (QTEREV_RECORD_ID,QTEREV_ID,QUOTE_ID, QUOTE_NAME,UOM_ID,UOM_RECORD_ID, QUOTE_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, PAR_SERVICE_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_RECORD_ID,SERVICE_RECORD_ID, SERVICE_TYPE, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, QUOTE_SERVICE_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
                        SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                        SELECT DISTINCT QTEREV_RECORD_ID, QTEREV_ID,QUOTE_ID, QUOTE_NAME,UOM_ID,UOM_RECORD_ID, QUOTE_RECORD_ID, '{description}' AS SERVICE_DESCRIPTION, '{splitservice_object}' AS SERVICE_ID,SERVICE_ID as PAR_SERVICE_ID,SERVICE_DESCRIPTION AS PAR_SERVICE_DESCRIPTION,QUOTE_SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID, '{material_record_id}' AS SERVICE_RECORD_ID, '' AS SERVICE_TYPE, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, SALESORG_ID, SALESORG_NAME,SALESORG_RECORD_ID FROM SAQTSV (NOLOCK)
                        WHERE SERVICE_ID IN {service_id} AND QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' 
                        ) A""".format(description=description, service_id = parservice_values, material_record_id = material_record_id,contract_quote_rec_id = contract_quote_rec_id , quote_revision_rec_id = quote_revision_rec_id ,UserName = user_name, UserId = user_id,splitservice_object = splitservice_object ))
    
    ###split the items with new insert and updation:
    split_service =Sql.GetFirst("Select * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='Z0105'".format(contract_quote_rec_id,quote_revision_rec_id))
    splitservice_id = split_service.SERVICE_ID
    splitservice_name = split_service.SERVICE_DESCRIPTION
    splitservice_recid = split_service.SERVICE_RECORD_ID
    # SPLIT SAQRIS 
    equipmentservice_count = 0
    quote_item_obj_service = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIS (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
    if quote_item_obj_service:
	    equipmentservice_count = int(quote_item_obj_service.LINE)
    QueryStatement ="""MERGE SAQRIS SRC USING (SELECT 	
    QUOTE_REV_ITEM_SUMMARY_RECORD_ID,COMMITTED_VALUE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DIVISION_ID,DIVISION_RECORD_ID,DOC_CURRENCY,DOCCURR_RECORD_ID,ESTIMATED_VALUE,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,ROW_NUMBER()OVER(ORDER BY(SAQRIS.CpqTableEntryId)) + {equipmentservice_count} as LINE,NET_PRICE,NET_PRICE_INGL_CURR,NET_VALUE,NET_VALUE_INGL_CURR,PLANT_ID,PLANT_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR  FROM SAQRIS where QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID  = '{quote_revision_rec_id}'  )
    TGT ON (SRC.QUOTE_RECORD_ID = TGT.QUOTE_RECORD_ID AND SRC.QTEREV_RECORD_ID = TGT.QTEREV_RECORD_ID AND SRC.SERVICE_ID = 'Z0105')
    WHEN NOT MATCHED BY TARGET
    THEN INSERT(QUOTE_REV_ITEM_SUMMARY_RECORD_ID,COMMITTED_VALUE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DIVISION_ID,DIVISION_RECORD_ID,DOC_CURRENCY,DOCCURR_RECORD_ID,ESTIMATED_VALUE,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,LINE,NET_PRICE,NET_PRICE_INGL_CURR,NET_VALUE,NET_VALUE_INGL_CURR,PLANT_ID,PLANT_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR)
    VALUES (NEWID(),COMMITTED_VALUE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DIVISION_ID,DIVISION_RECORD_ID,DOC_CURRENCY,DOCCURR_RECORD_ID,ESTIMATED_VALUE,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,LINE,NET_PRICE,NET_PRICE_INGL_CURR,NET_VALUE,NET_VALUE_INGL_CURR,PLANT_ID,PLANT_RECORD_ID,'{splitservice_name}', '{splitservice_id}','{splitservice_recid}',QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR);""".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_recid = splitservice_recid,splitservice_id=splitservice_id,splitservice_name = splitservice_name,equipmentservice_count =equipmentservice_count )
    Sql.RunQuery(QueryStatement)
    #split In saqrit
    equipments_count = 0
    quote_item_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
    if quote_item_obj:
	    equipments_count = int(quote_item_obj.LINE)
    QueryStatement ="""MERGE SAQRIT SRC USING (SELECT QUOTE_REVISION_CONTRACT_ITEM_ID,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DOC_CURRENCY,DOCURR_RECORD_ID,EXCHANGE_RATE,EXCHANGE_RATE_DATE,EXCHANGE_RATE_RECORD_ID,GL_ACCOUNT_NO,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,ROW_NUMBER()OVER(ORDER BY(SAQRIT.CpqTableEntryId)) + {equipments_count} as LINE2,LINE,OBJECT_ID,OBJECT_TYPE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,PROFIT_CENTER,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,REF_SALESORDER,STATUS,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,TAXCLASSIFICATION_DESCRIPTION,TAXCLASSIFICATION_ID,TAXCLASSIFICATION_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,NET_PRICE,NET_PRICE_INGL_CURR,PLANT_ID,PLANT_NAME,PLANT_RECORD_ID,COMVAL_INGL_CURR,ESTVAL_INGL_CURR,NET_VALUE,NET_VALUE_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR,YEAR_1,YEAR_1_INGL_CURR,YEAR_2,YEAR_2_INGL_CURR,YEAR_3,YEAR_3_INGL_CURR,YEAR_4,YEAR_4_INGL_CURR,YEAR_5,YEAR_5_INGL_CURR,QTEITMSUM_RECORD_ID,MODULE_ID,MODULE_NAME,MODULE_RECORD_ID,PARQTEITM_LINE,PARQTEITM_LINE_RECORD_ID,BILLING_TYPE,COMMITTED_VALUE,ESTIMATED_VALUE FROM SAQRIT where QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID  = '{quote_revision_rec_id}')
    TGT ON (SRC.QUOTE_RECORD_ID = TGT.QUOTE_RECORD_ID AND SRC.QTEREV_RECORD_ID = TGT.QTEREV_RECORD_ID AND SRC.SERVICE_ID = 'Z0105')
    WHEN NOT MATCHED BY TARGET
    THEN INSERT(QUOTE_REVISION_CONTRACT_ITEM_ID,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DOC_CURRENCY,DOCURR_RECORD_ID,EXCHANGE_RATE,EXCHANGE_RATE_DATE,EXCHANGE_RATE_RECORD_ID,GL_ACCOUNT_NO,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,LINE,OBJECT_ID,OBJECT_TYPE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,PROFIT_CENTER,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,REF_SALESORDER,STATUS,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,TAXCLASSIFICATION_DESCRIPTION,TAXCLASSIFICATION_ID,TAXCLASSIFICATION_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,NET_PRICE,NET_PRICE_INGL_CURR,PLANT_ID,PLANT_NAME,PLANT_RECORD_ID,COMVAL_INGL_CURR,ESTVAL_INGL_CURR,NET_VALUE,NET_VALUE_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR,YEAR_1,YEAR_1_INGL_CURR,YEAR_2,YEAR_2_INGL_CURR,YEAR_3,YEAR_3_INGL_CURR,YEAR_4,YEAR_4_INGL_CURR,YEAR_5,YEAR_5_INGL_CURR,QTEITMSUM_RECORD_ID,MODULE_ID,MODULE_NAME,MODULE_RECORD_ID,PARQTEITM_LINE,PARQTEITM_LINE_RECORD_ID,BILLING_TYPE,COMMITTED_VALUE,ESTIMATED_VALUE)
    VALUES (NEWID(),CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DOC_CURRENCY,DOCURR_RECORD_ID,EXCHANGE_RATE,EXCHANGE_RATE_DATE,EXCHANGE_RATE_RECORD_ID,GL_ACCOUNT_NO,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,LINE2,OBJECT_ID,OBJECT_TYPE,'{splitservice_name}','{splitservice_id}','{splitservice_recid}',PROFIT_CENTER,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,REF_SALESORDER,STATUS,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,TAXCLASSIFICATION_DESCRIPTION,TAXCLASSIFICATION_ID,TAXCLASSIFICATION_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,NET_PRICE,NET_PRICE_INGL_CURR,PLANT_ID,PLANT_NAME,PLANT_RECORD_ID,COMVAL_INGL_CURR,ESTVAL_INGL_CURR,NET_VALUE,NET_VALUE_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR,YEAR_1,YEAR_1_INGL_CURR,YEAR_2,YEAR_2_INGL_CURR,YEAR_3,YEAR_3_INGL_CURR,YEAR_4,YEAR_4_INGL_CURR,YEAR_5,YEAR_5_INGL_CURR,QTEITMSUM_RECORD_ID,MODULE_ID,MODULE_NAME,MODULE_RECORD_ID,LINE,QUOTE_REVISION_CONTRACT_ITEM_ID,BILLING_TYPE,COMMITTED_VALUE,ESTIMATED_VALUE);""".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_recid = splitservice_recid,splitservice_id=splitservice_id,splitservice_name = splitservice_name,equipments_count =equipments_count )
    Sql.RunQuery(QueryStatement)


    ##insert for saqico from SAQICO WITH SAQRIT
    QueryStatement ="""MERGE SAQICO SRC USING (Select A.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,A.EQUIPMENT_DESCRIPTION,A.EQUIPMENT_RECORD_ID,A.FABLOCATION_ID,A.FABLOCATION_NAME,A.FABLOCATION_RECORD_ID,A.PLATFORM,A.QUOTE_ID,B.QUOTE_REVISION_CONTRACT_ITEM_ID,A.QUOTE_RECORD_ID,A.SERIAL_NO,B.SERVICE_DESCRIPTION,B.SERVICE_ID,B.SERVICE_RECORD_ID,A.TECHNOLOGY,A.CEILING_PRICE_MARGIN,A.DISCOUNT,A.YEAR_OVER_YEAR,A.BD_DISCOUNT,A.BD_DISCOUNT_RECORD_ID,A.BD_PRICE_MARGIN,A.BD_PRICE_MARGIN_RECORD_ID,A.CLEANING_COST,A.CUSTOMER_TOOL_ID,A.EQUIPMENTCATEGORY_ID,A.EQUIPMENTCATEGORY_RECORD_ID,A.EQUIPMENT_STATUS,A.KPI_COST,A.LABOR_COST,A.MNT_PLANT_ID,A.MNT_PLANT_NAME,A.MNT_PLANT_RECORD_ID,A.PM_PART_COST,A.SALESORG_ID,A.SALESORG_NAME,A.SALESORG_RECORD_ID,A.TARGET_PRICE_MARGIN,A.TARGET_PRICE_MARGIN_RECORD_ID,A.WARRANTY_END_DATE,A.WARRANTY_START_DATE,A.GREENBOOK,A.EQUIPMENT_ID,A.GREENBOOK_RECORD_ID,A.EQUIPMENTCATEGORY_DESCRIPTION,A.DOCURR_RECORD_ID,A.ANNUAL_BENCHMARK_BOOKING_PRICE,A.BENCHMARKING_THRESHOLD,A.CONTRACT_ID,A.CONTRACT_NAME,A.CONTRACT_RECORD_ID,A.PRICEBENCHMARK_RECORD_ID,A.PRICE_BENCHMARK_TYPE,A.TOOL_CONFIGURATION,A.GLOBAL_CURRENCY,B.LINE,A.GLOBAL_CURRENCY_RECORD_ID,A.CONTRACT_VALID_FROM,A.CONTRACT_VALID_TO,A.QTEITMGBK_RECORD_ID,A.ENTITLEMENT_COST_IMPACT,A.QTEREV_ID,A.QTEREV_RECORD_ID,A.GREATER_THAN_QTLY_PM_COST,A.LESS_THAN_QTLY_PM_COST,A.METROLOGY_COST,A.RECOATING_COST,A.REFURB_COST,A.SLSDIS_PRICE_MARGIN,A.SLSDIS_PRICE_MARGIN_RECORD_ID,A.SEEDSTOCK_COST,A.TOTAL_COST_WOSEEDSTOCK,A.TOTAL_COST_WSEEDSTOCK,A.ASSEMBLY_ID,A.ASSEMBLY_RECORD_ID,A.CEILING_PRICE_MARGIN_RECORD_ID,A.SALDIS_PERCENT,A.BD_PRICE_INGL_CURR,A.CEILING_PRICE_INGL_CURR,A.DISCOUNT_AMOUNT_INGL_CURR,A.ENTPRCIMP_INGL_CURR,A.KPU,A.MODEL_PRICE_INGL_CURR,A.NET_PRICE_INGL_CURR,A.SLSDIS_PRICE_INGL_CURR,A.SALDIS_RECORD_ID,A.TARGET_PRICE_INGL_CURR,A.STATUS,A.HEAD_REBUILD_QTY,A.SALES_PRICE_INGL_CURR,A.YEAR,A.ADD_COST_IMPACT,A.ANNUAL_PMSA_COST,A.ADD_PRICE_IMPACT,A.ANNUAL_PMSA_PRICE,A.BILLING_TYPE,A.CNTPRI_INGL_CURR,A.CNTCST_INGL_CURR,A.ESTVAL_INGL_CURR,A.FAILURE_COST,A.GOT_CODE,A.WARRANTY_PERIOD,A.KIT_NAME,A.KIT_NUMBER,A.NUMBER_OF_DAYS,A.OBJECT_ID,A.OBJECT_TYPE,A.OUTSOURCE_COST,A.PER_EVENT_PMSA_COST,A.PER_EVENT_PMSA_PRICE,A.PM_COUNT_YEAR,A.PM_ID,A.PM_LABOR_LEVEL,A.PM_RECORD_ID,A.LOGISTICS_COST,A.QUANTITY,A.REPLACE_COST,A.ADJ_PM_FREQUENCY,A.SSCM_PM_FREQUENCY,A.TKM_RECORD_ID,A.MODULE_ID,A.MODULE_NAME,A.MODULE_RECORD_ID FROM SAQICO(NOLOCK) A JOIN SAQRIT (NOLOCK) B ON A.QUOTE_RECORD_ID  = B.QUOTE_RECORD_ID AND A.LINE = B.PARQTEITM_LINE where B.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND B.QTEREV_RECORD_ID  = '{quote_revision_rec_id}' AND B.SERVICE_ID = 'Z0105')
    TGT ON (SRC.QUOTE_RECORD_ID = TGT.QUOTE_RECORD_ID AND SRC.QTEREV_RECORD_ID = TGT.QTEREV_RECORD_ID AND SRC.SERVICE_ID = 'Z0105')
    WHEN NOT MATCHED BY TARGET
    THEN INSERT(QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,PLATFORM,QUOTE_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,TECHNOLOGY,CEILING_PRICE_MARGIN,DISCOUNT,YEAR_OVER_YEAR,BD_DISCOUNT,BD_DISCOUNT_RECORD_ID,BD_PRICE_MARGIN,BD_PRICE_MARGIN_RECORD_ID,CLEANING_COST,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_ID,EQUIPMENTCATEGORY_RECORD_ID,EQUIPMENT_STATUS,KPI_COST,LABOR_COST,MNT_PLANT_ID,MNT_PLANT_NAME,MNT_PLANT_RECORD_ID,PM_PART_COST,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,TARGET_PRICE_MARGIN,TARGET_PRICE_MARGIN_RECORD_ID,WARRANTY_END_DATE,WARRANTY_START_DATE,GREENBOOK,EQUIPMENT_ID,GREENBOOK_RECORD_ID,EQUIPMENTCATEGORY_DESCRIPTION,DOCURR_RECORD_ID,ANNUAL_BENCHMARK_BOOKING_PRICE,BENCHMARKING_THRESHOLD,CONTRACT_ID,CONTRACT_NAME,CONTRACT_RECORD_ID,PRICEBENCHMARK_RECORD_ID,PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,GLOBAL_CURRENCY,LINE,GLOBAL_CURRENCY_RECORD_ID,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,QTEITMGBK_RECORD_ID,ENTITLEMENT_COST_IMPACT,QTEREV_ID,QTEREV_RECORD_ID,GREATER_THAN_QTLY_PM_COST,LESS_THAN_QTLY_PM_COST,METROLOGY_COST,RECOATING_COST,REFURB_COST,SLSDIS_PRICE_MARGIN,SLSDIS_PRICE_MARGIN_RECORD_ID,SEEDSTOCK_COST,TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,CEILING_PRICE_MARGIN_RECORD_ID,SALDIS_PERCENT,BD_PRICE_INGL_CURR,CEILING_PRICE_INGL_CURR,DISCOUNT_AMOUNT_INGL_CURR,ENTPRCIMP_INGL_CURR,KPU,MODEL_PRICE_INGL_CURR,NET_PRICE_INGL_CURR,SLSDIS_PRICE_INGL_CURR,SALDIS_RECORD_ID,TARGET_PRICE_INGL_CURR,STATUS,HEAD_REBUILD_QTY,SALES_PRICE_INGL_CURR,YEAR,ADD_COST_IMPACT,ANNUAL_PMSA_COST,ADD_PRICE_IMPACT,ANNUAL_PMSA_PRICE,BILLING_TYPE,CNTPRI_INGL_CURR,CNTCST_INGL_CURR,ESTVAL_INGL_CURR,FAILURE_COST,GOT_CODE,WARRANTY_PERIOD,KIT_NAME,KIT_NUMBER,NUMBER_OF_DAYS,OBJECT_ID,OBJECT_TYPE,OUTSOURCE_COST,PER_EVENT_PMSA_COST,PER_EVENT_PMSA_PRICE,PM_COUNT_YEAR,PM_ID,PM_LABOR_LEVEL,PM_RECORD_ID,LOGISTICS_COST,QUANTITY,REPLACE_COST,ADJ_PM_FREQUENCY,SSCM_PM_FREQUENCY,TKM_RECORD_ID,MODULE_ID,MODULE_NAME,MODULE_RECORD_ID)
    VALUES (NEWID(),EQUIPMENT_DESCRIPTION,EQUIPMENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,PLATFORM,QUOTE_ID,QUOTE_REVISION_CONTRACT_ITEM_ID,QUOTE_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,TECHNOLOGY,CEILING_PRICE_MARGIN,DISCOUNT,YEAR_OVER_YEAR,BD_DISCOUNT,BD_DISCOUNT_RECORD_ID,BD_PRICE_MARGIN,BD_PRICE_MARGIN_RECORD_ID,CLEANING_COST,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_ID,EQUIPMENTCATEGORY_RECORD_ID,EQUIPMENT_STATUS,KPI_COST,LABOR_COST,MNT_PLANT_ID,MNT_PLANT_NAME,MNT_PLANT_RECORD_ID,PM_PART_COST,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,TARGET_PRICE_MARGIN,TARGET_PRICE_MARGIN_RECORD_ID,WARRANTY_END_DATE,WARRANTY_START_DATE,GREENBOOK,EQUIPMENT_ID,GREENBOOK_RECORD_ID,EQUIPMENTCATEGORY_DESCRIPTION,DOCURR_RECORD_ID,ANNUAL_BENCHMARK_BOOKING_PRICE,BENCHMARKING_THRESHOLD,CONTRACT_ID,CONTRACT_NAME,CONTRACT_RECORD_ID,PRICEBENCHMARK_RECORD_ID,PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,GLOBAL_CURRENCY,LINE,GLOBAL_CURRENCY_RECORD_ID,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,QTEITMGBK_RECORD_ID,ENTITLEMENT_COST_IMPACT,QTEREV_ID,QTEREV_RECORD_ID,GREATER_THAN_QTLY_PM_COST,LESS_THAN_QTLY_PM_COST,METROLOGY_COST,RECOATING_COST,REFURB_COST,SLSDIS_PRICE_MARGIN,SLSDIS_PRICE_MARGIN_RECORD_ID,SEEDSTOCK_COST,TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,CEILING_PRICE_MARGIN_RECORD_ID,SALDIS_PERCENT,BD_PRICE_INGL_CURR,CEILING_PRICE_INGL_CURR,DISCOUNT_AMOUNT_INGL_CURR,ENTPRCIMP_INGL_CURR,KPU,MODEL_PRICE_INGL_CURR,NET_PRICE_INGL_CURR,SLSDIS_PRICE_INGL_CURR,SALDIS_RECORD_ID,TARGET_PRICE_INGL_CURR,STATUS,HEAD_REBUILD_QTY,SALES_PRICE_INGL_CURR,YEAR,ADD_COST_IMPACT,ANNUAL_PMSA_COST,ADD_PRICE_IMPACT,ANNUAL_PMSA_PRICE,BILLING_TYPE,CNTPRI_INGL_CURR,CNTCST_INGL_CURR,ESTVAL_INGL_CURR,FAILURE_COST,GOT_CODE,WARRANTY_PERIOD,KIT_NAME,KIT_NUMBER,NUMBER_OF_DAYS,OBJECT_ID,OBJECT_TYPE,OUTSOURCE_COST,PER_EVENT_PMSA_COST,PER_EVENT_PMSA_PRICE,PM_COUNT_YEAR,PM_ID,PM_LABOR_LEVEL,PM_RECORD_ID,LOGISTICS_COST,QUANTITY,REPLACE_COST,ADJ_PM_FREQUENCY,SSCM_PM_FREQUENCY,TKM_RECORD_ID,MODULE_ID,MODULE_NAME,MODULE_RECORD_ID );""".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id )
    Sql.RunQuery(QueryStatement)   

splitserviceinsert()
