 # ====================================================================================================================
#   __script_name : CQDOCUTYPE.PY
#   __script_description : THIS SCRIPT IS USED TO DETERMINE THE DOCUMENT TYPE BASED ON THE SERVICE OFFERING
#   __primary_author__ : GAYATHRI AMARESAN
#   __create_date :
#   Ã‚Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ====================================================================================================================
import clr
import System.Net
import sys
from SYDATABASE import SQL

Sql = SQL()

def update_document_type(QuoteRecordId,RevisionRecordId,ServicerecordId):
    service_obj  = Sql.GetFirst("select SERVICE_ID from SAQTSV(NOLOCK) where QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServicerecordId}'".format(QuoteRecordId = QuoteRecordId,RevisionRecordId = RevisionRecordId,ServicerecordId = ServicerecordId))
    document_type_obj = None    
    Quote_obj = Sql.GetFirst("SELECT POES FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId = QuoteRecordId,RevisionRecordId = RevisionRecordId))
    if service_obj:
        #Log.Info("INSIDE_SERVICE")
        #Log.Info("service_obj" + str(service_obj.SERVICE_ID))
        #Log.Info("Quote_obj" + str(Quote_obj.POES))
        document_type_obj = Sql.GetFirst("select DOCTYP_ID,DOCTYP_RECORD_ID from MAMADT(NOLOCK) where SAP_PART_NUMBER = '{}' AND POES ='{}'".format(service_obj.SERVICE_ID,Quote_obj.POES))
        Sql.RunQuery("UPDATE SAQTSV SET DOCTYP_ID = '{DocumentType}',DOCTYP_RECORD_ID = '{DocumentTypeRecordId}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'".format(DocumentType = document_type_obj.DOCTYP_ID,DocumentTypeRecordId = document_type_obj.DOCTYP_RECORD_ID,QuoteRecordId = QuoteRecordId,RevisionRecordId = RevisionRecordId,ServicerecordId = ServicerecordId))
    else:
        Log.Info('26---')
        if Quote_obj is not None:
            if str(Quote_obj.POES).upper() =="TRUE":
                document_type_obj = Sql.GetFirst("select DOCTYP_ID,DOCTYP_RECORD_ID from MAMADT where DOCTYP_ID ='ZSWC'")
            else:
                Log.Info('26--inside condt-')
                document_type_obj = Sql.GetFirst("select DOCTYP_ID,DOCTYP_RECORD_ID from MAMADT where DOCTYP_ID ='ZTBC'")    
        
    if document_type_obj:
        Log.Info('26--update---'+str(document_type_obj.DOCTYP_ID))
        Sql.RunQuery("UPDATE SAQTRV SET DOCTYP_ID = '{DocumentType}',DOCTYP_RECORD_ID = '{DocumentTypeRecordId}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(DocumentType = document_type_obj.DOCTYP_ID,DocumentTypeRecordId = document_type_obj.DOCTYP_RECORD_ID,QuoteRecordId = QuoteRecordId,RevisionRecordId = RevisionRecordId)) 
    
try:
    QuoteRecordId = Param.QUOTE_RECORD_ID
    RevisionRecordId = Param.QTEREV_RECORD_ID
    ServicerecordId = Param.SERVICE_ID
except:
    QuoteRecordId = ""
    RevisionRecordId = "" 
    ServicerecordId = ""
#Log.Info("CQDOCUTYPE called for Quote Record ID--->"+str(QuoteRecordId))   
#Log.Info("CQDOCUTYPE called for ServicerecordId--->"+str(ServicerecordId))
Log.Info("CQDOCUTYPE called for RevisionRecordId-->"+str(RevisionRecordId))
update_document_type(QuoteRecordId,RevisionRecordId,ServicerecordId)