# =========================================================================================================================================
#   __script_name : MAPOSTTKMU.PY
#   __script_description : THIS SCRIPT IS USED TO EXTRACT KIT BOM  AND PM BOM DATA FROM SYINPL TABLE TO STAGING TABLES
#   __primary_author__ : BAJI
#   __create_date : 2020-12-28
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
from SYDATABASE import SQL
clr.AddReference("System.Net")
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage


Parameter=SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME='SELECT' ")
Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")

try :
	Status_flag = 0
	
	#Status Inprogress SYINPL by CPQ Table Entry ID
	StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL SET STATUS = ''INPROGRESS'' FROM SYINPL (NOLOCK) WHERE isnull(status,'''')='''' AND (INTEGRATION_NAME = ''SSCM_TO_CPQ_TOOL_PMKIT_DATA'' or INTEGRATION_NAME = ''SSCM_TO_CPQ_KITBOM_DATA'') ' ")	
	
	while Status_flag == 0:
		#Status Empty
		Jsonquery = SqlHelper.GetList("SELECT INTEGRATION_PAYLOAD,CpqTableEntryId from SYINPL(NOLOCK) WHERE ISNULL(STATUS,'') = 'INPROGRESS' AND (INTEGRATION_NAME = 'SSCM_TO_CPQ_KITBOM_DATA' or INTEGRATION_NAME = 'SSCM_TO_CPQ_TOOL_PMKIT_DATA') ")
		
		if len(Jsonquery) > 0:
		
			primaryQuerysession =  SqlHelper.GetFirst("SELECT NEWID() AS A")
			today = datetime.datetime.now()
			Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")
			
			for json_data in Jsonquery:
				if "Param" in str(json_data.INTEGRATION_PAYLOAD):
					splited_list = str(json_data.INTEGRATION_PAYLOAD).split("'")
					rebuilt_data = eval(str(splited_list[1]))
				else:
					splited_list = str(json_data.INTEGRATION_PAYLOAD)
					rebuilt_data = eval(splited_list)       

				if len(rebuilt_data) != 0:      

					rebuilt_data = rebuilt_data["CPQ_Columns"]
					Table_Names = rebuilt_data.keys()
					Check_flag = 0
					
					for tn in Table_Names:
						if tn in rebuilt_data:
							Check_flag = 1
							if str(tn).upper() == "MAEAPM":
								if str(type(rebuilt_data[tn])) == "<type 'dict'>":
									Tbl_data = [rebuilt_data[tn]]
								else:
									Tbl_data = rebuilt_data[tn]
									
								for record_dict in Tbl_data:
									primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " MAEAPM_INBOUND (SESSION_ID,EQUIPMENT_ID,ASSEMBLY_ID,PM_NAME,PM_FREQUENCY,KIT_ID,KIT_NUMBER,SEEDSTOCK_COST,LOGISTICS_COST,TKM_COST_PER_EVENT,cpqtableentrydatemodified,KIT_MASTER_ID)  select  ''"+ str(primaryQuerysession.A)+ "'',''"+record_dict['EQUIPMENT_ID']+ "'',''"+record_dict['ASSEMBLY_ID']+ "'',''"+record_dict['PM_NAME']+ "'',''"+record_dict['PM_FREQUENCY']+ "'',''"+record_dict['KIT_ID']+ "'',''"+record_dict['KIT_NUMBER']+ "'',''"+record_dict['SEEDSTOCK_COST']+ "'',''"+record_dict['LOGISTICS_COST']+ "'',''"+record_dict['TKM_COST_PER_EVENT']+ "'',''"+ str(Modi_date)+ "'',''"+record_dict['KIT_MASTER_ID']+ "'' ' ")
									
							elif str(tn).upper() == "MAKTPT":
								if str(type(rebuilt_data[tn])) == "<type 'dict'>":
									Tbl_data = [rebuilt_data[tn]]
								else:
									Tbl_data = rebuilt_data[tn]
									
								for record_dict in Tbl_data:
									primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " MAKTPT_INBOUND (SESSION_ID,KIT_ID,PART_NUMBER,QUANTITY,cpqtableentrydatemodified,KIT_MASTER_ID)  select  ''"+ str(primaryQuerysession.A)+ "'',''"+record_dict['KIT_ID']+ "'',''"+record_dict['PART_NUMBER']+ "'',''"+record_dict['QUANTITY']+ "'',''"+ str(Modi_date)+ "'',''"+record_dict['KIT_Master_ID']+ "'' ' ")                     
							
										
					StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL SET STATUS = ''COMPLETED''FROM SYINPL (NOLOCK)  WHERE CpqTableEntryId = ''"+str(json_data.CpqTableEntryId)+"'' ' ")
					
				else:
					StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL SET STATUS = ''COMPLETED''FROM SYINPL (NOLOCK)  WHERE CpqTableEntryId = ''"+str(json_data.CpqTableEntryId)+"'' ' ")
		else:
			Status_flag = 1	
			
	#We need to write the code for staging tables to main tables code here
	sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
	timestamp_sessionid = "'" + str(sessionid.A) + "'"	
				
	Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
	Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
	Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")

	#Staging Status Change
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAKTPT_INBOUND SET TIMESTAMP = '"+str(timestamp_sessionid)+"',PROCESS_STATUS = ''INPROGRESS'' FROM MAKTPT_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')='''' '")
	
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAEAPM_INBOUND SET TIMESTAMP = '"+str(timestamp_sessionid)+"',PROCESS_STATUS = ''INPROGRESS'' FROM MAEAPM_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')='''' '")
	
	#Part Validation
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAKTPT_INBOUND SET PROCESS_STATUS = ''ERROR'',INTEGRATION_STATUS=''SAP PART NUMBER not exists in Material Master table (MAMTRL). Please trigger the SAP PART NUMBER from ECC to CPQ to resolve this error.'' FROM MAKTPT_INBOUND (NOLOCK)  LEFT JOIN MAMTRL (NOLOCK) ON MAKTPT_INBOUND.PART_NUMBER = MAMTRL.SAP_PART_NUMBER WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND MAMTRL.SAP_PART_NUMBER IS NULL '")
	
	#Status Change
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAKTPT_INBOUND SET PROCESS_STATUS = ''READY FOR UPLOAD'' FROM MAKTPT_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')IN (''INPROGRESS'',''ERROR'') AND TIMESTAMP = '"+str(timestamp_sessionid)+"' '")
	
	#Kit Upload
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter.QUERY_CRITERIA_1)
	+ " MAMKIT(KIT_NAME,CPQTABLEENTRYADDEDBY,ADDUSR_RECORD_ID,CPQTABLEENTRYDATEADDED,KIT_RECORD_ID,KIT_ID)SELECT DISTINCT KIT_NAME,''"+ str(User.UserName)
	+ "'',''"+ str(User.Id)
	+ "'',GETDATE(),CONVERT(VARCHAR(1000),NEWID()),KIT_MASTER_ID FROM (SELECT DISTINCT MAKTPT_INBOUND.KIT_ID AS KIT_NAME,MAKTPT_INBOUND.KIT_MASTER_ID FROM MAKTPT_INBOUND (NOLOCK)  LEFT JOIN MAMKIT (NOLOCK) ON MAKTPT_INBOUND.KIT_MASTER_ID = MAMKIT.KIT_ID WHERE ISNULL(PROCESS_STATUS,'''')= (''READY FOR UPLOAD'') AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND MAMKIT.KIT_ID IS NULL)SUB_MAMKIT '")
	
	#Kit BOM Upload
	
	"""
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAKTPT SET QUANTITY = SUB_MAKTPT.QUANTITY FROM (SELECT DISTINCT MAMKIT.KIT_ID,MAMKIT.KIT_NAME,MAMKIT.KIT_RECORD_ID,SAP_DESCRIPTION,MAKTPT_INBOUND.PART_NUMBER,MATERIAL_RECORD_ID,MAKTPT_INBOUND.QUANTITY,''ACTIVE'' FROM MAKTPT_INBOUND(NOLOCK) JOIN MAMKIT (NOLOCK) ON MAKTPT_INBOUND.KIT_ID = MAMKIT.KIT_NAME LEFT JOIN MAMTRL (NOLOCK) ON MAKTPT_INBOUND.PART_NUMBER = MAMTRL.SAP_PART_NUMBER WHERE ISNULL(PROCESS_STATUS,'''')= ''READY FOR UPLOAD'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')SUB_MAKTPT JOIN MAKTPT M(NOLOCK) ON SUB_MAKTPT.KIT_ID = MAKTPT.KIT_ID AND SUB_MAKTPT.PART_NUMBER = MAKTPT.PART_NUMBER '")
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ " MAKTPT_INBOUND BOM_STATUS = ''ACTIVE'' FROM MAKTPT_INBOUND (NOLOCK) JOIN MAKTPT (NOLOCK) ON MAKTPT_INBOUND.KIT_ID = MAKTPT.KIT_ID AND MAKTPT_INBOUND.PART_NUMBER = MAKTPT.PART_NUMBER WHERE ISNULL(INTEGRATION_STATUS,'''')= '''' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  '")
"""
	
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter2.QUERY_CRITERIA_1)
	+ " MAKTPT FROM MAKTPT JOIN MAKTPT_INBOUND  ON MAKTPT.KIT_ID = MAKTPT_INBOUND.KIT_MASTER_ID WHERE ISNULL(PROCESS_STATUS,'''')= ''READY FOR UPLOAD'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  '")
	
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter.QUERY_CRITERIA_1)
	+ "  MAKTPT(KIT_ID,KIT_NAME,KIT_RECORD_ID,PART_DESCRIPTION,PART_NUMBER,PART_RECORD_ID,QUANTITY,BOM_STATUS,CPQTABLEENTRYADDEDBY,ADDUSR_RECORD_ID,CPQTABLEENTRYDATEADDED,KIT_PART_RECORD_ID) SELECT DISTINCT SUB_MAKTPT.KIT_ID,SUB_MAKTPT.KIT_NAME,SUB_MAKTPT.KIT_RECORD_ID,SUB_MAKTPT.SAP_DESCRIPTION,SUB_MAKTPT.PART_NUMBER,SUB_MAKTPT.MATERIAL_RECORD_ID,SUB_MAKTPT.QUANTITY,SUB_MAKTPT.BOM_STATUS,''"+ str(User.UserName)
	+ "'',''"+ str(User.Id)
	+ "'',GETDATE(),CONVERT(VARCHAR(1000),NEWID()) FROM (SELECT DISTINCT MAMKIT.KIT_ID,MAMKIT.KIT_NAME,MAMKIT.KIT_RECORD_ID,SAP_DESCRIPTION,MAKTPT_INBOUND.PART_NUMBER,MATERIAL_RECORD_ID,MAKTPT_INBOUND.QUANTITY,''ACTIVE'' AS BOM_STATUS FROM MAKTPT_INBOUND (NOLOCK) JOIN MAMKIT (NOLOCK) ON MAKTPT_INBOUND.KIT_MASTER_ID = MAMKIT.KIT_ID LEFT JOIN MAMTRL (NOLOCK) ON MAKTPT_INBOUND.PART_NUMBER = MAMTRL.SAP_PART_NUMBER WHERE ISNULL(PROCESS_STATUS,'''')= ''READY FOR UPLOAD'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')SUB_MAKTPT LEFT JOIN MAKTPT (NOLOCK) ON SUB_MAKTPT.KIT_ID = MAKTPT.KIT_ID AND SUB_MAKTPT.PART_NUMBER = MAKTPT.PART_NUMBER WHERE MAKTPT.PART_NUMBER IS NULL  '")
	
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ " MAKTPT set BOM_STATUS = ''ERROR - PART NOT AVAILABLE'' FROM MAKTPT_INBOUND (NOLOCK) JOIN MAKTPT (NOLOCK) ON MAKTPT_INBOUND.KIT_MASTER_ID = MAKTPT.KIT_ID AND MAKTPT_INBOUND.PART_NUMBER = MAKTPT.PART_NUMBER WHERE ISNULL(INTEGRATION_STATUS,'''')= ''ERROR'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  '")
	
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAKTPT_INBOUND SET PROCESS_STATUS = ''UPLOADED'' FROM MAKTPT_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')= ''READY FOR UPLOAD'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' '")
	
	#Preventive Maintenance Starts
	
	#Equipment Validation
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAEAPM_INBOUND SET PROCESS_STATUS = ''ERROR'',INTEGRATION_STATUS=''Equipment ID not exists in Equipment Master table (MAEQUP). Please trigger the Ibase data from ECC to CPQ to resolve this error.'' FROM MAEAPM_INBOUND (NOLOCK) LEFT JOIN MAEQUP (NOLOCK) ON MAEAPM_INBOUND.EQUIPMENT_ID = MAEQUP.EQUIPMENT_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND MAEQUP.EQUIPMENT_ID IS NULL '")
	
	#Assembly Validation
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAEAPM_INBOUND SET PROCESS_STATUS = ''ERROR'',INTEGRATION_STATUS=''Assembly ID not exists in Equipment Master table (MAEQUP). Please trigger the Ibase data from ECC to CPQ to resolve this error.'' FROM MAEAPM_INBOUND (NOLOCK) LEFT JOIN MAEQUP (NOLOCK) ON MAEAPM_INBOUND.ASSEMBLY_ID = MAEQUP.EQUIPMENT_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND MAEQUP.EQUIPMENT_ID IS NULL '")
	
	#Status Change
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAEAPM_INBOUND SET PROCESS_STATUS = ''READY FOR UPLOAD'' FROM MAEAPM_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')IN (''INPROGRESS'') AND TIMESTAMP = '"+str(timestamp_sessionid)+"' '")
	
	#PM Upload 
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter.QUERY_CRITERIA_1)
	+ " SGPMNT(ACTIVE,PM_NAME,CPQTABLEENTRYADDEDBY,ADDUSR_RECORD_ID,CPQTABLEENTRYDATEADDED,PM_RECORD_ID) SELECT SUB_SGPMNT.ACTIVE,SUB_SGPMNT.PM_NAME,''"+ str(User.UserName)
	+ "'',''"+ str(User.Id)
	+ "'',GETDATE(),CONVERT(VARCHAR(1000),NEWID()) FROM (SELECT DISTINCT ''TRUE'' AS ACTIVE,PM_NAME  FROM MAEAPM_INBOUND(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''READY FOR UPLOAD'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')SUB_SGPMNT LEFT JOIN SGPMNT (NOLOCK) ON SUB_SGPMNT.PM_NAME = SGPMNT.PM_NAME WHERE SGPMNT.PM_NAME IS NULL  '")
	
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ " SGPMNT set PM_ID = cpqtableentryid where isnull(PM_ID,'''')=''''  '")
	
	#Kit Upload
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter.QUERY_CRITERIA_1)
	+ " MAMKIT(KIT_NAME,CPQTABLEENTRYADDEDBY,ADDUSR_RECORD_ID,CPQTABLEENTRYDATEADDED,KIT_RECORD_ID,KIT_ID)SELECT DISTINCT KIT_NAME,''"+ str(User.UserName)
	+ "'',''"+ str(User.Id)
	+ "'',GETDATE(),CONVERT(VARCHAR(1000),NEWID()),KIT_MASTER_ID FROM (SELECT DISTINCT MAEAPM_INBOUND.KIT_ID AS KIT_NAME,KIT_MASTER_ID FROM MAEAPM_INBOUND (NOLOCK) LEFT JOIN MAMKIT (NOLOCK) ON MAEAPM_INBOUND.KIT_MASTER_ID = MAMKIT.KIT_ID WHERE ISNULL(PROCESS_STATUS,'''')= ''READY FOR UPLOAD'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND MAMKIT.KIT_NAME IS NULL)SUB_MAMKIT '")
	
	#Kit Number Upload
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter.QUERY_CRITERIA_1)
	+ " MATKTN(KIT_ID,KIT_NAME,KIT_NUMBER,KIT_RECORD_ID,CPQTABLEENTRYADDEDBY,ADDUSR_RECORD_ID,CPQTABLEENTRYDATEADDED,TOOL_KIT_NUMBER_RECORD_ID) SELECT MAMKIT.KIT_ID,MAMKIT.KIT_NAME,SUB_MAMKIT.KIT_NUMBER,MAMKIT.KIT_RECORD_ID,''"+ str(User.UserName)
	+ "'',''"+ str(User.Id)
	+ "'',GETDATE(),CONVERT(VARCHAR(1000),NEWID()) FROM (SELECT DISTINCT KIT_MASTER_ID as KIT_ID,KIT_NUMBER  FROM MAEAPM_INBOUND(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''READY FOR UPLOAD'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')SUB_MAMKIT  JOIN MAMKIT (NOLOCK) ON SUB_MAMKIT.KIT_ID = MAMKIT.KIT_ID LEFT JOIN MATKTN (NOLOCK)M ON SUB_MAMKIT.KIT_ID = M.KIT_ID AND SUB_MAMKIT.KIT_NUMBER = M.KIT_NUMBER WHERE M.KIT_NUMBER IS NULL AND ISNULL(SUB_MAMKIT.KIT_NUMBER,''0'')<>''0'' '")

	#Equipment PM Upload
	
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter2.QUERY_CRITERIA_1)
	+ " MAEAPK FROM MAEAPK  JOIN MAEAPM_INBOUND ON MAEAPM_INBOUND.EQUIPMENT_ID = MAEAPK.EQUIPMENT_ID WHERE ISNULL(PROCESS_STATUS,'''')= ''READY FOR UPLOAD'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(INTEGRATION_STATUS,'''')='''' '")

	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter.QUERY_CRITERIA_1)
	+ " MAEAPK (APPLICATION,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,REGION,REGION_RECORD_ID,CUSTOMER_MARKETING_NAME,DEVICE,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,KIT_ID,KIT_NAME,KIT_NUMBER,KIT_NUMBER_RECORD_ID,KIT_RECORD_ID,LOGISTICS_COST,PM_FREQUENCY,PM_ID,PM_NAME,PM_RECORD_ID,PROCESS_TYPE,SEEDSTOCK_COST,SERVICE_COMPLEXITY,TECHNOLOGY_NODE,TKM_COST_PER_EVENT,CPQTABLEENTRYADDEDBY,ADDUSR_RECORD_ID,CPQTABLEENTRYDATEADDED,EQUIPMENT_ASSEMBLY_PM_KIT_RECORD_ID) SELECT SUB_MAEAPK.*,''"+ str(User.UserName)
	+ "'',''"+ str(User.Id)
	+ "'',GETDATE(),CONVERT(VARCHAR(1000),NEWID())  FROM (SELECT DISTINCT MAEAPM_INBOUND.APPLICATION,MAEQUP.EQUIPMENT_DESCRIPTION AS ASSEMBLY_DESCRIPTION,MAEQUP.EQUIPMENT_ID AS ASSEMBLY_ID,MAEQUP.EQUIPMENT_RECORD_ID AS ASSEMBLY_RECORD_ID,MAEQUP.REGION,MAEQUP.REGION_RECORD_ID,MAEAPM_INBOUND.CUSTOMER_MARKETING_NAME,MAEAPM_INBOUND.DEVICE,MAEQUP.PAR_EQUIPMENT_DESCRIPTION AS EQUIPMENT_DESCRIPTION,MAEQUP.PAR_EQUIPMENT_ID AS EQUIPMENT_ID,MAEQUP.PAR_EQUIPMENT_RECORD_ID AS EQUIPMENT_RECORD_ID,MAMKIT.KIT_ID,MAMKIT.KIT_NAME,MATKTN.KIT_NUMBER,MATKTN.TOOL_KIT_NUMBER_RECORD_ID AS KIT_NUMBER_RECORD_ID,MAMKIT.KIT_RECORD_ID,CONVERT(FLOAT,MAEAPM_INBOUND.LOGISTICS_COST) AS LOGISTICS_COST,CONVERT(FLOAT,MAEAPM_INBOUND.PM_FREQUENCY) AS PM_FREQUENCY,SGPMNT.PM_ID,SGPMNT.PM_NAME,SGPMNT.PM_RECORD_ID,MAEAPM_INBOUND.PROCESS_TYPE,CONVERT(FLOAT,MAEAPM_INBOUND.SEEDSTOCK_COST) AS SEEDSTOCK_COST,MAEAPM_INBOUND.SERVICE_COMPLEXITY,MAEAPM_INBOUND.TECHNOLOGY_NODE,CONVERT(FLOAT,MAEAPM_INBOUND.TKM_COST_PER_EVENT) AS TKM_COST_PER_EVENT FROM MAEAPM_INBOUND (NOLOCK) JOIN MAEQUP (NOLOCK) ON MAEAPM_INBOUND.ASSEMBLY_ID = MAEQUP.EQUIPMENT_ID JOIN MAMKIT (NOLOCK) ON MAEAPM_INBOUND.KIT_master_ID = MAMKIT.KIT_ID JOIN MATKTN (NOLOCK) ON MAEAPM_INBOUND.KIT_master_ID = MATKTN.KIT_ID AND MAEAPM_INBOUND.KIT_NUMBER = MATKTN.KIT_NUMBER JOIN SGPMNT (NOLOCK) ON MAEAPM_INBOUND.PM_NAME = SGPMNT.PM_NAME WHERE ISNULL(PROCESS_STATUS,'''')= ''READY FOR UPLOAD'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(INTEGRATION_STATUS,'''')='''' AND ISNULL(MAEAPM_INBOUND.KIT_NUMBER,''0'')<>''0'' )SUB_MAEAPK LEFT JOIN MAEAPK (NOLOCK) ON SUB_MAEAPK.EQUIPMENT_ID = MAEAPK.EQUIPMENT_ID AND SUB_MAEAPK.ASSEMBLY_ID = MAEAPK.ASSEMBLY_ID AND SUB_MAEAPK.KIT_ID = MAEAPK.KIT_ID AND SUB_MAEAPK.PM_ID = MAEAPK.PM_ID WHERE MAEAPK.EQUIPMENT_ID IS NULL   '")
	
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter.QUERY_CRITERIA_1)
	+ " MAEAPK (APPLICATION,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,REGION,REGION_RECORD_ID,CUSTOMER_MARKETING_NAME,DEVICE,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID	,KIT_ID,KIT_NAME,KIT_NUMBER,KIT_NUMBER_RECORD_ID,KIT_RECORD_ID,LOGISTICS_COST,PM_FREQUENCY,PM_ID,PM_NAME,PM_RECORD_ID,PROCESS_TYPE,SEEDSTOCK_COST,SERVICE_COMPLEXITY,TECHNOLOGY_NODE,TKM_COST_PER_EVENT,CPQTABLEENTRYADDEDBY,ADDUSR_RECORD_ID,CPQTABLEENTRYDATEADDED,EQUIPMENT_ASSEMBLY_PM_KIT_RECORD_ID) SELECT SUB_MAEAPK.*,''"+ str(User.UserName)
	+ "'',''"+ str(User.Id)
	+ "'',GETDATE(),CONVERT(VARCHAR(1000),NEWID())  FROM (SELECT DISTINCT MAEAPM_INBOUND.APPLICATION,MAEQUP.EQUIPMENT_DESCRIPTION AS ASSEMBLY_DESCRIPTION,MAEQUP.EQUIPMENT_ID AS ASSEMBLY_ID,MAEQUP.EQUIPMENT_RECORD_ID AS ASSEMBLY_RECORD_ID,MAEQUP.REGION,MAEQUP.REGION_RECORD_ID,MAEAPM_INBOUND.CUSTOMER_MARKETING_NAME,MAEAPM_INBOUND.DEVICE,MAEQUP.PAR_EQUIPMENT_DESCRIPTION AS EQUIPMENT_DESCRIPTION,MAEQUP.PAR_EQUIPMENT_ID AS EQUIPMENT_ID,MAEQUP.PAR_EQUIPMENT_RECORD_ID AS EQUIPMENT_RECORD_ID,MAMKIT.KIT_ID,MAMKIT.KIT_NAME,NULL AS KIT_NUMBER,NULL AS KIT_NUMBER_RECORD_ID,MAMKIT.KIT_RECORD_ID,CONVERT(FLOAT,MAEAPM_INBOUND.LOGISTICS_COST) AS LOGISTICS_COST,CONVERT(FLOAT,MAEAPM_INBOUND.PM_FREQUENCY) AS PM_FREQUENCY,SGPMNT.PM_ID,SGPMNT.PM_NAME,SGPMNT.PM_RECORD_ID,MAEAPM_INBOUND.PROCESS_TYPE,CONVERT(FLOAT,MAEAPM_INBOUND.SEEDSTOCK_COST) AS SEEDSTOCK_COST,MAEAPM_INBOUND.SERVICE_COMPLEXITY,MAEAPM_INBOUND.TECHNOLOGY_NODE,CONVERT(FLOAT,MAEAPM_INBOUND.TKM_COST_PER_EVENT) AS TKM_COST_PER_EVENT FROM MAEAPM_INBOUND (NOLOCK) JOIN MAEQUP (NOLOCK) ON MAEAPM_INBOUND.ASSEMBLY_ID = MAEQUP.EQUIPMENT_ID JOIN MAMKIT (NOLOCK) ON MAEAPM_INBOUND.KIT_master_ID = MAMKIT.KIT_ID JOIN MAMKIT E(NOLOCK) ON MAEAPM_INBOUND.KIT_master_ID = MAMKIT.KIT_ID JOIN SGPMNT (NOLOCK) ON MAEAPM_INBOUND.PM_NAME = SGPMNT.PM_NAME WHERE ISNULL(PROCESS_STATUS,'''')= ''READY FOR UPLOAD'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(INTEGRATION_STATUS,'''')='''' AND ISNULL(MAEAPM_INBOUND.KIT_NUMBER,''0'')=''0'' )SUB_MAEAPK LEFT JOIN MAEAPK (NOLOCK) ON SUB_MAEAPK.EQUIPMENT_ID = MAEAPK.EQUIPMENT_ID AND SUB_MAEAPK.ASSEMBLY_ID = MAEAPK.ASSEMBLY_ID AND SUB_MAEAPK.KIT_ID = MAEAPK.KIT_ID AND SUB_MAEAPK.PM_ID = MAEAPK.PM_ID WHERE MAEAPK.EQUIPMENT_ID IS NULL   '")
	
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAEAPM_INBOUND SET PROCESS_STATUS = ''UPLOADED'' FROM MAEAPM_INBOUND (NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')= ''READY FOR UPLOAD'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' '")

	#Mail system
	Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #bd{color : 'black';} </style></head><body id = 'bd'>"

	Table_start = "<p>Hi Team,<br><br>KIT BOM DATA AND PM BOM DATA SUCCESSFULLY UPLOADED</p><br>"

	Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"
	Table_info = ""     

	Error_Info = Header + Table_start + Table_info + Table_End

	LOGIN_CRE = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password FROM SYCONF where Domain ='SUPPORT_MAIL'")

	# Create new SmtpClient object
	mailClient = SmtpClient()

	# Set the host and port (eg. smtp.gmail.com)
	mailClient.Host = "smtp.gmail.com"
	mailClient.Port = 587
	mailClient.EnableSsl = "true"

	# Setup NetworkCredential
	mailCred = NetworkCredential()
	mailCred.UserName = str(LOGIN_CRE.Username)
	mailCred.Password = str(LOGIN_CRE.Password)
	mailClient.Credentials = mailCred

	# Create two mail adresses, one for send from and the another for recipient
	toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
	fromEmail = MailAddress("INTEGRATION.SUPPORT@BOSTONHARBORCONSULTING.COM")

	# Create new MailMessage object
	msg = MailMessage(fromEmail, toEmail)

	# Set message subject and body
	msg.Subject = "SC KIT DATA - Notification"
	msg.IsBodyHtml = True
	msg.Body = Error_Info

	# CC Emails 	
	copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
	msg.CC.Add(copyEmail4)

	# Send the message
	mailClient.Send(msg) 
	
except:
	#Status Empty in SYINPL
	StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL SET STATUS = ''''FROM SYINPL (NOLOCK) WHERE STATUS = ''INPROGRESS'' ' ")


	Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #bd{color : 'black';} </style></head><body id = 'bd'>"

	Table_start = "<p>Hi Team,<br><br>KIT BOM script having follwing Error in Line number "+str(sys.exc_info()[-1].tb_lineno)+".<br><br>"+str(sys.exc_info()[1])+"</p><br>"
	
	Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"
	Table_info = ""     

	Error_Info = Header + Table_start + Table_info + Table_End

	LOGIN_CRE = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password FROM SYCONF where Domain ='SUPPORT_MAIL'")

	# Create new SmtpClient object
	mailClient = SmtpClient()

	# Set the host and port (eg. smtp.gmail.com)
	mailClient.Host = "smtp.gmail.com"
	mailClient.Port = 587
	mailClient.EnableSsl = "true"

	# Setup NetworkCredential
	mailCred = NetworkCredential()
	mailCred.UserName = str(LOGIN_CRE.Username)
	mailCred.Password = str(LOGIN_CRE.Password)
	mailClient.Credentials = mailCred

	# Create two mail adresses, one for send from and the another for recipient
	toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
	fromEmail = MailAddress("INTEGRATION.SUPPORT@BOSTONHARBORCONSULTING.COM")

	# Create new MailMessage object
	msg = MailMessage(fromEmail, toEmail)

	# Set message subject and body
	msg.Subject = "KIT BOM - Error Notification"
	msg.IsBodyHtml = True
	msg.Body = Error_Info

	# CC Emails 	
	copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
	msg.CC.Add(copyEmail4)
	
	# Send the message
	mailClient.Send(msg) 
	
		
	Log.Info("MAPOSTTKMU ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("MAPOSTTKMU ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})