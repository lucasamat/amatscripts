# =========================================================================================================================================
#   __script_name : CQINSQTITM.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT QUOTE ITEMS AND ITS RELATED TABLES BASED ENTITLEMENT
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :30-09-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED -
# ==========================================================================================================================================

import Webcom.Configurator.Scripting.Test.TestProduct
import System.Net
import re
import datetime
from SYDATABASE import SQL
import CQPARTIFLW

Sql = SQL()


class ContractQuoteItem:
	def __init__(self, **kwargs):		
		self.user_id = str(User.Id)
		self.user_name = str(User.UserName)		
		self.datetime_value = datetime.datetime.now()
		self.contract_quote_record_id = kwargs.get('contract_quote_record_id')
		self.contract_quote_revision_record_id = kwargs.get('contract_quote_revision_record_id')
		self.action_type = kwargs.get('action_type')
		self.service_id = kwargs.get('service_id')
		self.greenbook_id = kwargs.get('greenbook_id')
		self.fablocation_id = kwargs.get('fablocation_id')
		self.equipment_id = kwargs.get('equipment_id') 
		self.entitlement_level_obj = kwargs.get('entitlement_level_obj')      
		self.pricing_temp_table = ''
		self.quote_line_item_temp_table = '' 
		self.quote_service_entitlement_type = ''
		self.get_billing_type_val = ""
		self.parent_service_id = ""
		self.source_object_name = ''
		self._ent_consumable = ''
		self.where_condition_string = kwargs.get('where_condition_string') 
		self.set_contract_quote_related_details()
		self._set_service_type()
		self._set_fpm_service_type()
		self._get_material_type()
		self._get_ancillary_product()
		self._get_billing_type()

	
	def set_contract_quote_related_details(self):
		contract_quote_obj = Sql.GetFirst("SELECT QUOTE_ID, QUOTE_TYPE, SALE_TYPE, C4C_QUOTE_ID, QTEREV_ID, QUOTE_CURRENCY, QUOTE_CURRENCY_RECORD_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'".format(QuoteRecordId=self.contract_quote_record_id))
		if contract_quote_obj:
			self.contract_quote_id = contract_quote_obj.QUOTE_ID      
			self.quote_type = contract_quote_obj.QUOTE_TYPE
			self.sale_type = contract_quote_obj.SALE_TYPE
			self.c4c_quote_id = contract_quote_obj.C4C_QUOTE_ID
			self.contract_quote_revision_id = contract_quote_obj.QTEREV_ID
			self.contract_currency = contract_quote_obj.QUOTE_CURRENCY
			self.contract_currency_record_id = contract_quote_obj.QUOTE_CURRENCY_RECORD_ID			
		else:
			self.contract_quote_id = ''  
			self.quote_type = ''
			self.sale_type = ''
			self.c4c_quote_id = ''
			self.contract_quote_revision_id = ''
		return True
	
	def _set_service_type(self):
		spare_parts_count_object = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQRSP (NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))			
		if spare_parts_count_object:
			self.is_spare_service = True
		else:
			self.is_spare_service = False
		return True

	def _get_consumable_val(self):
		self._ent_consumable =''
		if self.parent_service_id == 'Z0092' :
			get_consumable = Sql.GetFirst("select ENTITLEMENT_XML,SERVICE_ID from SAQTSE where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{get_service}'".format(QuoteRecordId =self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,get_service = self.parent_service_id))
			if get_consumable:
				updateentXML = get_consumable.ENTITLEMENT_XML
				pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
				pattern_id = re.compile(r'<ENTITLEMENT_ID>AGS_Z0092_TSC_CONSUM</ENTITLEMENT_ID>')
				
				pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
				for m in re.finditer(pattern_tag, updateentXML):
					sub_string = m.group(1)
					get_ent_id = re.findall(pattern_id,sub_string)
					get_ent_val= re.findall(pattern_name,sub_string)
					if get_ent_id:
						self._ent_consumable = str(get_ent_val[0])
						break
			
		return True

	def _set_fpm_service_type(self):
		fpm_spare_parts_count_object = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQSPT (NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))			
		if fpm_spare_parts_count_object:
			self.is_fpm_spare_service = True
		else:
			self.is_fpm_spare_service = False
		return True

	def _get_billing_type(self):
		self.get_billing_type_val =''
		get_billing_cycle = Sql.GetFirst("select ENTITLEMENT_XML,SERVICE_ID from SAQTSE where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{get_service}'".format(QuoteRecordId =self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,get_service = self.service_id))
		if get_billing_cycle:
			updateentXML = get_billing_cycle.ENTITLEMENT_XML
			pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
			pattern_id = re.compile(r'<ENTITLEMENT_ID>(AGS_'+str(get_billing_cycle.SERVICE_ID)+'_PQB_BILTYP)</ENTITLEMENT_ID>')
			
			pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
			for m in re.finditer(pattern_tag, updateentXML):
				sub_string = m.group(1)
				get_ent_id = re.findall(pattern_id,sub_string)
				get_ent_val= re.findall(pattern_name,sub_string)
				if get_ent_id:
					self.get_billing_type_val = str(get_ent_val[0])
					break
		return True

	def _get_material_type(self):
		get_service_config_type = Sql.GetFirst("SELECT * FROM MAMTRL (NOLOCK) WHERE SAP_PART_NUMBER = '{}' AND MATERIALCONFIG_TYPE = 'SIMPLE MATERIAL'".format(self.service_id))
		if get_service_config_type:
			self.is_simple_service = True
		else:
			self.is_simple_service = False
		return True
	
	def _get_ancillary_product(self):
		self.is_ancillary = False
		check_ancillary = Sql.GetFirst("SELECT PAR_SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' and SERVICE_ID = '{ServiceId}' AND SERVICE_ID NOT IN (SELECT ADNPRD_ID FROM SAQSAO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' )".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
		if check_ancillary:
			if check_ancillary.PAR_SERVICE_ID:
				self.is_ancillary = True
		else:
			self.is_ancillary = False
		return True

	def _quote_items_assembly_insert(self, update=True):
		# Update - Start
		#item_line_covered_object_assembly_join_string = ""	
		#item_line_covered_object_assembly_where_string = ""		
		#if update:
		item_line_covered_object_assembly_where_string = "AND ISNULL(SAQICA.ASSEMBLY_RECORD_ID,'') = '' "
		item_line_covered_object_assembly_join_string = "LEFT JOIN SAQICA (NOLOCK) ON SAQICA.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQICA.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQICA.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQICA.GREENBOOK_RECORD_ID = SAQSCE.GREENBOOK_RECORD_ID AND SAQICA.FABLOCATION_RECORD_ID = SAQSCE.FABLOCATION_RECORD_ID AND SAQICA.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND SAQICA.ASSEMBLY_RECORD_ID = IQ.ASSEMBLY_RECORD_ID"
		# Update - End
		Log.Info("===>INSERT SAQICA===> "+str("""INSERT SAQICA (EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,EQUIPMENTTYPE_ID,LINE,QTEITM_RECORD_ID,QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified) 
				SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy,GETDATE() as CpqTableEntryDateModified FROM (
					SELECT IQ.*, SAQRIO.LINE, SAQRIO.QTEITM_RECORD_ID FROM (
						SELECT 
							DISTINCT SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQSCA.GREENBOOK,SAQSCA.GREENBOOK_RECORD_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_DESCRIPTION,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQSCA.EQUIPMENTTYPE_ID
						FROM SAQTSE (NOLOCK) 
						JOIN SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCA.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID  
						WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}'
					) IQ 
					JOIN SAQSCE (NOLOCK) ON SAQSCE.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQSCE.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQSCE.EQUIPMENT_ID = IQ.EQUIPMENT_ID AND SAQSCE.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' 
					JOIN SAQRIO (NOLOCK) ON SAQRIO.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQRIO.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQRIO.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQRIO.GREENBOOK_RECORD_ID = SAQSCE.GREENBOOK_RECORD_ID AND SAQRIO.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID
					{JoinString}
					WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCE.SERVICE_ID = '{ServiceId}' {WhereString}
				)OQ""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,JoinString=item_line_covered_object_assembly_join_string, WhereString=item_line_covered_object_assembly_where_string))
				)
		Sql.RunQuery("""INSERT SAQICA (EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,EQUIPMENTTYPE_ID,LINE,QTEITM_RECORD_ID,QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified) 
				SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy,GETDATE() as CpqTableEntryDateModified FROM (
					SELECT IQ.*, SAQRIO.LINE, SAQRIO.QTEITM_RECORD_ID FROM (
						SELECT 
							DISTINCT SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQSCA.GREENBOOK,SAQSCA.GREENBOOK_RECORD_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_DESCRIPTION,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQSCA.EQUIPMENTTYPE_ID
						FROM SAQTSE (NOLOCK) 
						JOIN SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCA.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID  
						WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}'
					) IQ 
					JOIN SAQSCE (NOLOCK) ON SAQSCE.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQSCE.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQSCE.EQUIPMENT_ID = IQ.EQUIPMENT_ID AND SAQSCE.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' 
					JOIN SAQRIO (NOLOCK) ON SAQRIO.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQRIO.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQRIO.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQRIO.GREENBOOK_RECORD_ID = SAQSCE.GREENBOOK_RECORD_ID AND SAQRIO.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID
					{JoinString}
					WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCE.SERVICE_ID = '{ServiceId}' {WhereString}
				)OQ""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,JoinString=item_line_covered_object_assembly_join_string, WhereString=item_line_covered_object_assembly_where_string))
				
	def _quote_items_assembly_entitlement_insert(self, update=True):
		# Update - Start
		#item_line_covered_object_assembly_entitlement_join_string = ""	
		#item_line_covered_object_assembly_entitlement_where_string = ""		
		#if update:
		item_line_covered_object_assembly_entitlement_where_string = "AND ISNULL(SAQIAE.ASSEMBLY_RECORD_ID,'') = '' "
		item_line_covered_object_assembly_entitlement_join_string = "LEFT JOIN SAQIAE (NOLOCK) ON SAQIAE.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQIAE.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQIAE.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQIAE.FABLOCATION_RECORD_ID = SAQSCE.FABLOCATION_RECORD_ID AND SAQIAE.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND SAQIAE.ASSEMBLY_RECORD_ID = IQ.ASSEMBLY_RECORD_ID"
		# Update - End
		Log.Info("===>INSERT SAQIAE===> "+str("""INSERT SAQIAE (EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,QUOTE_ITEM_ASSEMBLY_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified) 
		SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_ASSEMBLY_ENTITLEMENT_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy,GETDATE() as CpqTableEntryDateModified FROM (
			SELECT IQ.*,SAQSCE.ENTITLEMENT_XML FROM (
				SELECT 
					DISTINCT SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID 
				FROM SAQTSE (NOLOCK) 
				JOIN SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCA.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}'
			) IQ 
			JOIN SAQSCE (NOLOCK) ON SAQSCE.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQSCE.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQSCE.EQUIPMENT_ID = IQ.EQUIPMENT_ID AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' 
			{JoinString}
			WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCE.SERVICE_ID = '{ServiceId}' {WhereString}
		)OQ""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,JoinString=item_line_covered_object_assembly_entitlement_join_string, WhereString=item_line_covered_object_assembly_entitlement_where_string))
		)
		Sql.RunQuery("""INSERT SAQIAE (EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,QUOTE_ITEM_ASSEMBLY_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified) 
		SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_ASSEMBLY_ENTITLEMENT_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy,GETDATE() as CpqTableEntryDateModified FROM (
			SELECT IQ.*,SAQSCE.ENTITLEMENT_XML FROM (
				SELECT 
					DISTINCT SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID 
				FROM SAQTSE (NOLOCK) 
				JOIN SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCA.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}'
			) IQ 
			JOIN SAQSCE (NOLOCK) ON SAQSCE.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQSCE.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQSCE.EQUIPMENT_ID = IQ.EQUIPMENT_ID AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' 
			{JoinString}
			WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCE.SERVICE_ID = '{ServiceId}' {WhereString}
		)OQ""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,JoinString=item_line_covered_object_assembly_entitlement_join_string, WhereString=item_line_covered_object_assembly_entitlement_where_string))
	
	def _quote_annualized_items_insert(self, update=False):
		if self.quote_service_entitlement_type in ('OFFERING + EQUIPMENT','OFFERING+EQUIPMENT'):
			Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION, STATUS, QUANTITY, OBJECT_ID, EQUPID, EQUIPMENT_RECORD_ID, LINE, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, KPU, SERNUM, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY, CUSTOMER_TOOL_ID, EQUCAT, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOC, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GRNBOK, GREENBOOK_RECORD_ID, GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,   OBJECT_TYPE, BLUBOK, WTYSTE, WTYEND, WTYDAY, PLTFRM, SUBSIZ, REGION, ISPOES, CSTSRC, PRCSRC, CNTYER, STADTE, ENDDTE, CNTDAY, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
					SELECT DISTINCT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
					SELECT DISTINCT IQ.*, CONTRACT_TEMP.YEAR_WISE as CNTYER, CONTRACT_TEMP.VALID_FROM as STADTE, CONTRACT_TEMP.VALID_TO as ENDDTE, DATEDIFF(day,CONTRACT_TEMP.VALID_TO, CONTRACT_TEMP.VALID_FROM) as CNTDAY FROM (
					SELECT DISTINCT					
						SAQSCO.EQUIPMENT_DESCRIPTION,
						null as STATUS,
						SAQSCO.EQUIPMENT_QUANTITY,
						SAQRIT.OBJECT_ID,
						SAQSCO.EQUIPMENT_ID as EQUPID,
						SAQSCO.EQUIPMENT_RECORD_ID,
						SAQRIT.LINE,
						SAQRIT.QUOTE_ID, 
						SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
						SAQRIT.QUOTE_RECORD_ID,
						SAQRIT.QTEREV_ID,
						SAQRIT.QTEREV_RECORD_ID,
						SAQSCO.KPU,
						SAQSCO.SERIAL_NO as SERNUM, 
						SAQRIT.SERVICE_DESCRIPTION, 
						SAQRIT.SERVICE_ID, 
						SAQRIT.SERVICE_RECORD_ID,								
						SAQSCO.TECHNOLOGY,																			
						SAQSCO.CUSTOMER_TOOL_ID, 
						SAQSCO.EQUIPMENTCATEGORY_ID as EQUCAT, 
						SAQSCO.EQUIPMENTCATEGORY_RECORD_ID, 
						SAQSCO.EQUIPMENT_STATUS,					
						SAQSCO.MNT_PLANT_ID, 
						SAQSCO.MNT_PLANT_NAME, 
						SAQSCO.MNT_PLANT_RECORD_ID,				
						SAQSCO.SALESORG_ID, 
						SAQSCO.SALESORG_NAME, 
						SAQSCO.SALESORG_RECORD_ID,  
						SAQRIT.FABLOCATION_ID as FABLOC,
						SAQRIT.FABLOCATION_NAME,
						SAQRIT.FABLOCATION_RECORD_ID,
						SAQRIT.GREENBOOK as GRNBOK, 
						SAQRIT.GREENBOOK_RECORD_ID, 			
						SAQTRV.GLOBAL_CURRENCY,
						SAQTRV.GLOBAL_CURRENCY_RECORD_ID,					
						SAQRIT.OBJECT_TYPE,
						SAQTRV.BLUEBOOK as BLUBOK,
						SAQSCO.WARRANTY_START_DATE as WTYSTE,
						SAQSCO.WARRANTY_END_DATE as WTYEND,
						DATEDIFF(day,SAQSCO.WARRANTY_END_DATE, SAQSCO.WARRANTY_START_DATE) as WTYDAY,
						SAQSCO.PLATFORM	as PLTFRM,
						SAQSCO.WAFER_SIZE as SUBSIZ,
						SAQTRV.REGION as REGION,
						SAQTMT.POES as ISPOES,
						CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'SSCM' ELSE 'CPQ' END as CSTSRC,
						CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'VALUE PRICING-SSCM' ELSE 'OFFLINE PRICING' END as PRCSRC
						
					FROM 
						SAQSCO (NOLOCK)					 
						JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCE.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCE.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
						AND SAQSCE.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
						JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
						JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
						JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
												AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
												AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
												AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID
												AND SAQRIT.OBJECT_ID = SAQSCO.EQUIPMENT_ID
						LEFT JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID					
					WHERE 
						SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE'
					) IQ
					LEFT JOIN (
							SELECT QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_RECORD_ID, FABLOCATION_RECORD_ID, GREENBOOK_RECORD_ID, OBJECT_ID as EQUIPMENT_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, CONCAT('YEAR ',YEAR_NUM) as YEAR_WISE, CASE WHEN YEAR_NUM = YEAR THEN CONTRACT_VALID_TO ELSE DATEADD(yy,YEAR_NUM,DATEADD(dd,-1,CONTRACT_VALID_FROM)) END as VALID_TO, DATEADD(yy,YEAR_NUM-1,CONTRACT_VALID_FROM) as VALID_FROM
							FROM (
								SELECT DISTINCT CEILING(DATEDIFF(mm,CONTRACT_VALID_FROM,CONTRACT_VALID_TO)/12.0) as YEAR, QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_RECORD_ID, FABLOCATION_RECORD_ID, GREENBOOK_RECORD_ID, OBJECT_ID,CONTRACT_VALID_FROM,CONTRACT_VALID_TO 
								FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'
							) IQ_SAQRIT CROSS JOIN (SELECT 1 as YEAR_NUM UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) CJQ where YEAR>=YEAR_NUM
						) CONTRACT_TEMP ON  CONTRACT_TEMP.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND CONTRACT_TEMP.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND CONTRACT_TEMP.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND CONTRACT_TEMP.FABLOCATION_RECORD_ID = IQ.FABLOCATION_RECORD_ID AND CONTRACT_TEMP.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID AND CONTRACT_TEMP.EQUIPMENT_ID = IQ.EQUPID									
					) OQ
					LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = OQ.SERVICE_RECORD_ID AND SAQICO.GREENBOOK_RECORD_ID = OQ.GREENBOOK_RECORD_ID AND ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = ISNULL(OQ.FABLOCATION_RECORD_ID,'') AND SAQICO.EQUIPMENT_RECORD_ID = OQ.EQUIPMENT_RECORD_ID
					WHERE ISNULL(SAQICO.EQUIPMENT_RECORD_ID,'') = ''
					""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id)
			)	
		else:
			Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION, STATUS, QUANTITY, OBJECT_ID, EQUPID, EQUIPMENT_RECORD_ID, LINE, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID,QTEREV_RECORD_ID, KPU, SERNUM, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY,CUSTOMER_TOOL_ID, EQUCAT, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID,  FABLOC, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GRNBOK, GREENBOOK_RECORD_ID, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, OBJECT_TYPE, BLUBOK, WTYSTE, WTYEND, WTYDAY, PLTFRM, SUBSIZ, REGION, ISPOES, CSTSRC, PRCSRC, CNTYER, STADTE, ENDDTE, CNTDAY, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
					SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
					SELECT IQ.*, CONTRACT_TEMP.YEAR_WISE, CONTRACT_TEMP.VALID_FROM as STADTE, CONTRACT_TEMP.VALID_TO as ENDDTE, DATEDIFF(day,CONTRACT_TEMP.VALID_TO, CONTRACT_TEMP.VALID_FROM) as CNTDAY FROM (
						SELECT DISTINCT					
							null as EQUIPMENT_DESCRIPTION,
							null as STATUS,
							null as EQUIPMENT_QUANTITY,
							SAQRIT.OBJECT_ID,
							null as EQUIPMENT_ID as EQUPID,
							null as EQUIPMENT_RECORD_ID,
							SAQRIT.LINE,
							SAQRIT.QUOTE_ID, 
							SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
							SAQRIT.QUOTE_RECORD_ID,
							SAQRIT.QTEREV_ID,
							SAQRIT.QTEREV_RECORD_ID,
							null as KPU,
							null as SERIAL_NO as SERNUM, 
							SAQRIT.SERVICE_DESCRIPTION, 
							SAQRIT.SERVICE_ID, 
							SAQRIT.SERVICE_RECORD_ID,								
							null as TECHNOLOGY,																			
							null as CUSTOMER_TOOL_ID, 
							null as EQUIPMENTCATEGORY_ID as EQUCAT, 
							null as EQUIPMENTCATEGORY_RECORD_ID, 
							null as EQUIPMENT_STATUS,					
							null as MNT_PLANT_ID, 
							null as MNT_PLANT_NAME, 
							null as MNT_PLANT_RECORD_ID,			
							SAQTRV.SALESORG_ID, 
							SAQTRV.SALESORG_NAME, 
							SAQTRV.SALESORG_RECORD_ID, 
							SAQRIT.FABLOCATION_ID as FABLOC,
							SAQRIT.FABLOCATION_NAME,
							SAQRIT.FABLOCATION_RECORD_ID,
							SAQRIT.GREENBOOK as GRNBOK, 
							SAQRIT.GREENBOOK_RECORD_ID, 			
							SAQTRV.GLOBAL_CURRENCY,
							SAQTRV.GLOBAL_CURRENCY_RECORD_ID,					
							SAQRIT.OBJECT_TYPE,
							SAQTRV.BLUEBOOK as BLUBOK,
							null as WTYSTE,
							null as WTYEND,
							null as WTYDAY,
							null as PLTFRM,
							null as SUBSIZ,
							SAQTRV.REGION as REGION,
							SAQTMT.POES as ISPOES,
							CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'SSCM' ELSE 'CPQ' END as CSTSRC,
							CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'VALUE PRICING-SSCM' ELSE 'OFFLINE PRICING' END as PRCSRC				
						FROM 
							SAQRIT 
							JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID         
							JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
							JOIN SAQSGE (NOLOCK) ON SAQSGE.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQSGE.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQSGE.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQSGE.GREENBOOK = SAQRIT.GREENBOOK
							LEFT JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_RECORD_ID = SAQRIT.SERVICE_RECORD_ID	
											
						WHERE 
							SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSGE.CONFIGURATION_STATUS,'') = 'COMPLETE'
					) IQ
					LEFT JOIN (
							SELECT QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_RECORD_ID, FABLOCATION_RECORD_ID, GREENBOOK_RECORD_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, CONCAT('YEAR ',YEAR_NUM) as YEAR_WISE, CASE WHEN YEAR_NUM = YEAR THEN CONTRACT_VALID_TO ELSE DATEADD(yy,YEAR_NUM,DATEADD(dd,-1,CONTRACT_VALID_FROM)) END as VALID_TO, DATEADD(yy,YEAR_NUM-1,CONTRACT_VALID_FROM) as VALID_FROM
							FROM (
								SELECT DISTINCT CEILING(DATEDIFF(mm,CONTRACT_VALID_FROM,CONTRACT_VALID_TO)/12.0) as YEAR, QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_RECORD_ID, FABLOCATION_RECORD_ID, GREENBOOK_RECORD_ID, CONTRACT_VALID_FROM,CONTRACT_VALID_TO							
								FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'
							) IQ_SAQRIT CROSS JOIN (SELECT 1 as YEAR_NUM UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) CJQ where YEAR>=YEAR_NUM
						) CONTRACT_TEMP ON  CONTRACT_TEMP.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND CONTRACT_TEMP.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND CONTRACT_TEMP.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND ISNULL(CONTRACT_TEMP.FABLOCATION_RECORD_ID,'') = ISNULL(IQ.FABLOCATION_RECORD_ID,'') AND CONTRACT_TEMP.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID
					) OQ
					LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = OQ.SERVICE_RECORD_ID AND ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = ISNULL(OQ.FABLOCATION_RECORD_ID,'') AND SAQICO.GREENBOOK_RECORD_ID = OQ.GREENBOOK_RECORD_ID 
					WHERE ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = '' AND ISNULL(SAQICO.GREENBOOK_RECORD_ID,'') = ''
					""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id)
			)
		Sql.RunQuery("""UPDATE SAQTRV SET REVISION_STATUS = 'ACQUIRING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))

		# Target (Sales) Price Discount %
		Sql.RunQuery("""UPDATE SAQICO
						SET SADSPC = PRCFVA.FACTOR_PCTVAR		
							FROM SAQICO (NOLOCK)
							JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID
							WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(PRCFVA.FACTOR_NAME,'') = 'Sales Discount'
							""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		
		# Target Price Min Margin %
		Sql.RunQuery("""UPDATE SAQICO
						SET TAPMMP = PRCFVA.FACTOR_PCTVAR		
							FROM SAQICO (NOLOCK)
							JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID
							WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(PRCFVA.FACTOR_NAME,'') = 'Target Margin'
							""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))

		# BD Price Discount %
		Sql.RunQuery("""UPDATE SAQICO
						SET BDDSPC = PRCFVA.FACTOR_PCTVAR		
							FROM SAQICO (NOLOCK)
							JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID
							WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(PRCFVA.FACTOR_NAME,'') = 'BD Discount'
							""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		
		# BD Price Min Margin %
		Sql.RunQuery("""UPDATE SAQICO
						SET BDPMMP = PRCFVA.FACTOR_PCTVAR		
							FROM SAQICO (NOLOCK)
							JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID
							WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(PRCFVA.FACTOR_NAME,'') = 'BD Margin'
							""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		
		# Ceiling Price Uplift %
		Sql.RunQuery("""UPDATE SAQICO
						SET CEPRUP = PRCFVA.FACTOR_PCTVAR		
							FROM SAQICO (NOLOCK)
							JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID
							WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(PRCFVA.FACTOR_NAME,'') = 'Ceiling Margin'
							""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		
		# Entitlement Columns Insert
		datetime_string = self.datetime_value.strftime("%d%m%Y%H%M%S")
		SAQICO_BKP = "SAQICO_BKP_{}_{}".format(self.contract_quote_id, datetime_string)
		SAQITE_BKP = "SAQITE_BKP_{}_{}".format(self.contract_quote_id, datetime_string)
		
		Log.Info(str(self.contract_quote_id)+"===SAQICO_BKP==>> "+str(SAQICO_BKP))
		Log.Info(str(self.contract_quote_id)+"===SAQITE_BKP==>> "+str(SAQITE_BKP))
		entitlement_details = [{
								"field":["INTCPV","Intercept","AGS_{}_VAL_INTCPT".format(self.service_id)],						"coeff":["INTCPC","Intercept Coefficient","AGS_{}_VAL_INTCCO".format(self.service_id)]
								},
								{
								"field":["OSSVDV","Total Cost without Seedstock","AGS_{}_VAL_TBCOST".format(self.service_id)],	"coeff":["LTCOSS","Total Cost w/o Seedstock Coeff","AGS_{}_VAL_TBCOCO".format(self.service_id)]
								},
								{
								"field":["POFVDV","Product Offering","AGS_{}_VAL_POFFER".format(self.service_id)],	
								"coeff":["POFVDC","Product Offering Coefficient","AGS_{}_VAL_POFFCO".format(self.service_id)]
								},
								{
								"field":["GBKVDV","Greenbook","AGS_{}_VAL_GRNBKV".format(self.service_id)],	
								"coeff":["GBKVDC","Greenbook Coefficient","AGS_{}_VAL_GRNBCO".format(self.service_id)]
								},
								{
								"field":["UIMVDV","Uptime Improvement","AGS_{}_VAL_UPIMPV".format(self.service_id)],	
								"coeff":["UIMVDC","Uptime Improvement Coefficient","AGS_{}_VAL_UPIMCO".format(self.service_id)]
								},
								{
								"field":["CAVVDV","Capital Avoidance","AGS_{}_VAL_CAPAVD".format(self.service_id)],	
								"coeff":["CAVVDC","Capital Avoidance Coefficient","AGS_{}_VAL_CAPACO".format(self.service_id)]
								},
								{
								"field":["WNDVDV","Wafer Node","AGS_{}_VAL_WAFNOD".format(self.service_id)],	
								"coeff":["WNDVDC","Wafer Node Coefficient","AGS_{}_VAL_WAFNCO".format(self.service_id)]
								},
								{
								"field":["CCRTMV","Contract Coverage & Response Time","AGS_{}_VAL_CCRTME".format(self.service_id)],	
								"coeff":["CCRTMC","Contract Coverage & Response Time Coefficient","AGS_{}_VAL_CCRTCO".format(self.service_id)]
								},
								{
								"field":["SCMVDV","Service Complexity","AGS_{}_VAL_SCCCDF".format(self.service_id)],
								"coeff":["SCMVDC", "Service Complexity Coefficient", "AGS_{}_VAL_SCCCCO".format(self.service_id)]
								},
								{
								"field":["CCDFFV","Cleaning Coating Differentiation","AGS_{}_VAL_CCDVAL".format(self.service_id)],
								"coeff":["CCDFFC", "Cleaning Coating Diff coeff.", "AGS_{}_VAL_CCDVCO".format(self.service_id)]
								},
								{
								"field":["NPIVDV","NPI","AGS_{}_VAL_NPIREC".format(self.service_id)],
								"coeff":["NPIVDC", "NPI Coefficient", "AGS_{}_VAL_NPICOF".format(self.service_id)]
								},	
								{
								"field":["DTPVDV","Device Type","AGS_{}_VAL_DEVTYP".format(self.service_id)],
								"coeff":["DTPVDC", "Device Type Coefficient", "AGS_{}_VAL_DEVTCO".format(self.service_id)]
								},	
								{
								"field":["CSTVDV","# CSA Tools per Fab","AGS_{}_VAL_TLSFAB".format(self.service_id)],
								"coeff":["CSTVDC", "# CSA Tools per Fab Coefficient", "AGS_{}_VAL_TLSFCO".format(self.service_id)]
								},	
								{
								"field":["CSGVDV","Customer Segment","AGS_{}_VAL_CSTSEG".format(self.service_id)],
								"coeff":["CSGVDC", "Customer Segment Coefficent", "AGS_{}_VAL_CSSGCO".format(self.service_id)]
								},	
								{
								"field":["QRQVDV","Quality Required","AGS_{}_VAL_QLYREQ".format(self.service_id)],
								"coeff":["QRQVDC", "Quality Required Coefficient", "AGS_{}_VAL_QLYRCO".format(self.service_id)]
								},	
								{
								"field":["SVCVDV","Service Competition","AGS_{}_VAL_SVCCMP".format(self.service_id)],
								"coeff":["SVCVDC", "Service Competition Coefficient", "AGS_{}_VAL_SVCCCO".format(self.service_id)]
								},
								{
								"field":["RKFVDV","Risk Factor","AGS_{}_VAL_RSKFVD".format(self.service_id)],
								"coeff":["RKFVDC", "Risk Factor Coefficient", "AGS_{}_VAL_RSKFCO".format(self.service_id)]
								},
								{
								"field":["PBPVDV","PDC Base Price","AGS_{}_VAL_PDCBSE".format(self.service_id)],
								"coeff":["PBPVDC", "PDC Base Price Coefficient", "AGS_{}_VAL_PDCBCO".format(self.service_id)]
								},
								{
								"field":["CMLAB_ENT","Corrective Maintenance Labor","AGS_{}_NET_CRMALB".format(self.service_id)]
								},		
								{
								"field":["CNSMBL_ENT","Consumable","AGS_{}_TSC_CONSUM".format(self.service_id)]
								},
								{
								"field":["CNTCVG_ENT","Contract Coverage","AGS_{}_CVR_CNTCOV".format(self.service_id)]
								},	
								{
								"field":["NCNSMB_ENT","Non-Consumable","AGS_{}_TSC_NONCNS".format(self.service_id)]
								},	
								{
								"field":["PMEVNT_ENT","PM Events","AGS_{}_STT_PMEVNT".format(self.service_id)]
								},		
								{
								"field":["PMLAB_ENT","Preventive Maintenance Labor","AGS_{}_NET_PRMALB".format(self.service_id)]
								},	
								{
								"field":["PRMKPI_ENT","Primary KPI. Perf Guarantee","AGS_{}_KPI_PRPFGT".format(self.service_id)]
								},
								{
								"field":["OFRING","Product Offering","AGS_{}_VAL_POFFER".format(self.service_id)]
								},	
								{
								"field":["QTETYP","Quote Type","AGS_{}_PQB_QTETYP".format(self.service_id)]
								},	
								{
								"field":["BILTYP","Billing Type","AGS_{}_PQB_BILTYP".format(self.service_id)]
								},	
									
							]
		start_count = 1
		end_count = 500

		exit_flag = 1
		while exit_flag == 1:
			quote_items_obj = SqlHelper.GetFirst(
						"SELECT DISTINCT QTEITM_RECORD_ID FROM (SELECT DISTINCT QTEITM_RECORD_ID, ROW_NUMBER()OVER(ORDER BY QTEITM_RECORD_ID) AS SNO FROM (SELECT DISTINCT QTEITM_RECORD_ID FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.contract_quote_revision_record_id)+"' AND SERVICE_ID = '"+str(self.service_id)+"' )A) A WHERE SNO>= "+str(start_count)+" AND SNO<="+str(end_count)+""
					)
			
			SAQICO_BKP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str		(SAQICO_BKP)+"'' ) BEGIN DROP TABLE "+str(SAQICO_BKP)+" END  ' ")
					
			SAQITE_BKP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQITE_BKP)+"'' ) BEGIN DROP TABLE "+str(SAQITE_BKP)+" END  ' ")
			
			table_insert = SqlHelper.GetFirst(
				"sp_executesql @T=N'SELECT * INTO "+str(SAQICO_BKP)+" FROM (SELECT DISTINCT QTEITM_RECORD_ID FROM (SELECT DISTINCT QTEITM_RECORD_ID, ROW_NUMBER()OVER(ORDER BY QTEITM_RECORD_ID) AS SNO FROM (SELECT DISTINCT QTEITM_RECORD_ID FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = ''"+str(self.contract_quote_record_id)+"'' AND QTEREV_RECORD_ID = ''"+str(self.contract_quote_revision_record_id)+"'' AND SERVICE_ID = ''"+str(self.service_id)+"'' )A) A WHERE SNO>= "+str(start_count)+" AND SNO<="+str(end_count)+") OQ'"
					)
			
			table_insert = SqlHelper.GetFirst(
				"sp_executesql @T=N'SELECT SAQITE.* INTO "+str(SAQITE_BKP)+" FROM SAQITE (NOLOCK) JOIN "+str(SAQICO_BKP)+" SAQICO_BKP ON SAQITE.QTEITM_RECORD_ID = SAQICO_BKP.QTEITM_RECORD_ID  WHERE QUOTE_ID = ''"+str(self.contract_quote_id)+"'' AND QTEREV_ID = ''"+str(self.contract_quote_revision_id)+"'' '")
			
			start_count = start_count + 500
			end_count = end_count + 500

			if str(quote_items_obj) != "None":				
				for entitlement_detail in entitlement_details:					
					try:
						S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET "+str(entitlement_detail.get('field')[0])+" = ISNULL(ENTITLEMENT_DISPLAY_VALUE,'''') FROM SAQICO A(NOLOCK) JOIN (SELECT distinct QUOTE_ID, QTEREV_ID, SERVICE_ID, QTEITM_RECORD_ID, replace(X.Y.value(''(ENTITLEMENT_DISPLAY_VALUE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_DISPLAY_VALUE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT A.QUOTE_ID, A.QTEREV_ID, A.SERVICE_ID, A.QTEITM_RECORD_ID, CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>"+str(entitlement_detail.get('field')[2])+"'',entitlement_xml),charindex (''"+str(entitlement_detail.get('field')[1])+"</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>"+str(entitlement_detail.get('field')[2])+"'',entitlement_xml)+len(''"+str(entitlement_detail.get('field')[1])+"</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM "+str(SAQITE_BKP)+" (nolock)a JOIN "+str(SAQICO_BKP)+" C ON A.QTEITM_RECORD_ID = C.QTEITM_RECORD_ID WHERE QUOTE_ID = ''"+str(self.contract_quote_id)+"'' AND QTEREV_ID = ''"+str(self.contract_quote_revision_id)+"'' AND SERVICE_ID = ''"+str(self.service_id)+"'' AND charindex (''"+str(entitlement_detail.get('field')[1])+"</ENTITLEMENT_NAME>'',entitlement_xml) > 0) e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEITM_RECORD_ID = B.QTEITM_RECORD_ID  WHERE B.ENTITLEMENT_NAME=''"+str(entitlement_detail.get('field')[1])+"'' AND ISNULL(ENTITLEMENT_DISPLAY_VALUE,'''') <>''''  '")		
						if entitlement_detail.get('coeff'):			
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET "+str(entitlement_detail.get('coeff')[0])+" = ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO A(NOLOCK) JOIN (SELECT distinct QUOTE_ID, QTEREV_ID, SERVICE_ID, QTEITM_RECORD_ID, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT A.QUOTE_ID, A.QTEREV_ID, A.SERVICE_ID, A.QTEITM_RECORD_ID, CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>"+str(entitlement_detail.get('coeff')[2])+"'',entitlement_xml),charindex (''"+str(entitlement_detail.get('coeff')[1])+"</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>"+str(entitlement_detail.get('coeff')[2])+"'',entitlement_xml)+len(''"+str(entitlement_detail.get('coeff')[1])+"</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM "+str(SAQITE_BKP)+" (nolock)a JOIN "+str(SAQICO_BKP)+" C ON A.QTEITM_RECORD_ID = C.QTEITM_RECORD_ID WHERE QUOTE_ID = ''"+str(self.contract_quote_id)+"'' AND QTEREV_ID = ''"+str(self.contract_quote_revision_id)+"'' AND SERVICE_ID = ''"+str(self.service_id)+"'' AND charindex (''"+str(entitlement_detail.get('coeff')[1])+"</ENTITLEMENT_NAME>'',entitlement_xml) > 0) e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEITM_RECORD_ID = B.QTEITM_RECORD_ID  WHERE B.ENTITLEMENT_NAME=''"+str(entitlement_detail.get('coeff')[1])+"'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
					except Exception:
						Log.Info("===>>>>>NNN "+str("sp_executesql @T=N'UPDATE A SET "+str(entitlement_detail.get('field')[0])+" = ISNULL(ENTITLEMENT_DISPLAY_VALUE,'''') FROM SAQICO A(NOLOCK) JOIN (SELECT distinct QUOTE_ID, QTEREV_ID, SERVICE_ID, QTEITM_RECORD_ID, replace(X.Y.value(''(ENTITLEMENT_DISPLAY_VALUE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_DISPLAY_VALUE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT A.QUOTE_ID, A.QTEREV_ID, A.SERVICE_ID, A.QTEITM_RECORD_ID, CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>"+str(entitlement_detail.get('field')[2])+"'',entitlement_xml),charindex (''"+str(entitlement_detail.get('field')[1])+"</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>"+str(entitlement_detail.get('field')[2])+"'',entitlement_xml)+len(''"+str(entitlement_detail.get('field')[1])+"</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM "+str(SAQITE_BKP)+" (nolock)a JOIN "+str(SAQICO_BKP)+" C ON A.QTEITM_RECORD_ID = C.QTEITM_RECORD_ID WHERE QUOTE_ID = ''"+str(self.contract_quote_id)+"'' AND QTEREV_ID = ''"+str(self.contract_quote_revision_id)+"'' AND SERVICE_ID = ''"+str(self.service_id)+"'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEITM_RECORD_ID = B.QTEITM_RECORD_ID  WHERE B.ENTITLEMENT_NAME=''"+str(entitlement_detail.get('field')[1])+"'' AND ISNULL(ENTITLEMENT_DISPLAY_VALUE,'''') <>''''  '"))
						Log.Info("SAQICO Entitlement Update Issue {}-{}".format(entitlement_detail.get('field')[1],entitlement_detail.get('field')[2]))
						if entitlement_detail.get('coeff'):
							Log.Info("SAQICO Entitlement Update Issue {}-{}".format(entitlement_detail.get('coeff')[1],entitlement_detail.get('coeff')[2]))
			else:
				exit_flag = 0
			
			SAQICO_BKP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str		(SAQICO_BKP)+"'' ) BEGIN DROP TABLE "+str(SAQICO_BKP)+" END  ' ")
					
			SAQITE_BKP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQITE_BKP)+"'' ) BEGIN DROP TABLE "+str(SAQITE_BKP)+" END  ' ")
		return True

	def _quote_annualized_items_insert_old(self, update=False):			
		dynamic_col_names = ""	
		if self.is_ancillary == True or self.service_id == 'Z0116':
			dynamic_value_for_status = "'ACQUIRED' AS STATUS,'0' AS NET_PRICE_INGL_CURR, "
			dynamic_col_names = " NET_PRICE_INGL_CURR,"
			if self.service_id == 'Z0046' and self.get_billing_type_val.upper() == 'VARIABLE':
				dynamic_value_for_status += " '0' AS ESTVAL_INGL_CURR,  '0' AS DISCOUNT_AMOUNT_INGL_CURR,"
				dynamic_col_names += "ESTVAL_INGL_CURR, DISCOUNT_AMOUNT_INGL_CURR,"
		else:
			dynamic_value_for_status = "null AS STATUS, "
		if self.quote_service_entitlement_type in ('OFFERING + EQUIPMENT','OFFERING+EQUIPMENT'):			
			Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION, STATUS,{DynamicColNames} QUANTITY,OBJECT_ID,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, LINE, QUOTE_ID, QTEITM_RECORD_ID,  QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,KPU, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY,CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,   OBJECT_TYPE, YEAR, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
				SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT IQ.*, CONTRACT_TEMP.YEAR_WISE, CONTRACT_TEMP.VALID_FROM, CONTRACT_TEMP.VALID_TO FROM (
				SELECT DISTINCT					
					SAQSCO.EQUIPMENT_DESCRIPTION,
					{DynamicValueForStatus}
					SAQSCO.EQUIPMENT_QUANTITY,
					SAQRIT.OBJECT_ID,
					SAQSCO.EQUIPMENT_ID,
					SAQSCO.EQUIPMENT_RECORD_ID,
					SAQRIT.LINE,
					SAQRIT.QUOTE_ID, 
					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
					SAQRIT.QUOTE_RECORD_ID,
					SAQRIT.QTEREV_ID,
					SAQRIT.QTEREV_RECORD_ID,
					SAQSCO.KPU,
					SAQSCO.SERIAL_NO, 
					SAQRIT.SERVICE_DESCRIPTION, 
					SAQRIT.SERVICE_ID, 
					SAQRIT.SERVICE_RECORD_ID,								
					SAQSCO.TECHNOLOGY,																			
					SAQSCO.CUSTOMER_TOOL_ID, 
					SAQSCO.EQUIPMENTCATEGORY_ID, 
					SAQSCO.EQUIPMENTCATEGORY_RECORD_ID, 
					SAQSCO.EQUIPMENT_STATUS,					
					SAQSCO.MNT_PLANT_ID, 
					SAQSCO.MNT_PLANT_NAME, 
					SAQSCO.MNT_PLANT_RECORD_ID,				
					SAQSCO.SALESORG_ID, 
					SAQSCO.SALESORG_NAME, 
					SAQSCO.SALESORG_RECORD_ID,  
					SAQRIT.FABLOCATION_ID,
					SAQRIT.FABLOCATION_NAME,
					SAQRIT.FABLOCATION_RECORD_ID,
					SAQRIT.GREENBOOK, 
					SAQRIT.GREENBOOK_RECORD_ID, 			
					SAQTRV.GLOBAL_CURRENCY,
					SAQTRV.GLOBAL_CURRENCY_RECORD_ID,					
					SAQRIT.OBJECT_TYPE				
				FROM 
					SAQSCO (NOLOCK)					 
					JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCE.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCE.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
					AND SAQSCE.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
					JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
					JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
											AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
											AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
											AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID
											AND SAQRIT.OBJECT_ID = SAQSCO.EQUIPMENT_ID				
					LEFT JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQRIT.SERVICE_ID AND PRCFVA.FACTOR_ID = 'YOYDIS'
					
				WHERE 
					SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE'
				) IQ
				LEFT JOIN (
						SELECT QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_RECORD_ID, FABLOCATION_RECORD_ID, GREENBOOK_RECORD_ID, OBJECT_ID as EQUIPMENT_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, CONCAT('YEAR ',YEAR_NUM) as YEAR_WISE, CASE WHEN YEAR_NUM = YEAR THEN CONTRACT_VALID_TO ELSE DATEADD(yy,YEAR_NUM,DATEADD(dd,-1,CONTRACT_VALID_FROM)) END as VALID_TO, DATEADD(yy,YEAR_NUM-1,CONTRACT_VALID_FROM) as VALID_FROM
						FROM (
							SELECT DISTINCT CEILING(DATEDIFF(mm,CONTRACT_VALID_FROM,CONTRACT_VALID_TO)/12.0) as YEAR, QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_RECORD_ID, FABLOCATION_RECORD_ID, GREENBOOK_RECORD_ID, OBJECT_ID,CONTRACT_VALID_FROM,CONTRACT_VALID_TO 
							FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'
						) IQ_SAQRIT CROSS JOIN (SELECT 1 as YEAR_NUM UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) CJQ where YEAR>=YEAR_NUM
					) CONTRACT_TEMP ON  CONTRACT_TEMP.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND CONTRACT_TEMP.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND CONTRACT_TEMP.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND CONTRACT_TEMP.FABLOCATION_RECORD_ID = IQ.FABLOCATION_RECORD_ID AND CONTRACT_TEMP.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID AND CONTRACT_TEMP.EQUIPMENT_ID = IQ.EQUIPMENT_ID									
				) OQ
				LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = OQ.SERVICE_RECORD_ID AND SAQICO.GREENBOOK_RECORD_ID = OQ.GREENBOOK_RECORD_ID AND ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = ISNULL(OQ.FABLOCATION_RECORD_ID,'') AND SAQICO.EQUIPMENT_RECORD_ID = OQ.EQUIPMENT_RECORD_ID
				WHERE ISNULL(SAQICO.EQUIPMENT_RECORD_ID,'') = ''
				""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, DynamicValueForStatus = dynamic_value_for_status,DynamicColNames = dynamic_col_names)
			)		

			Sql.RunQuery("""UPDATE SAQTRV SET REVISION_STATUS = 'ACQUIRING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QTEREV_RECORD_ID}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
		else:
			if self.service_id in ('Z0110','Z0108'):
				self._simple_quote_annualized_items_insert()
			else:				
				Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION, STATUS,{DynamicColNames} QUANTITY,OBJECT_ID,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, LINE, QUOTE_ID, QTEITM_RECORD_ID,  QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,KPU, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY,CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID,  FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,  OBJECT_TYPE, YEAR, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
					SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
					SELECT IQ.*, CONTRACT_TEMP.YEAR_WISE, CONTRACT_TEMP.VALID_FROM, CONTRACT_TEMP.VALID_TO FROM (
						SELECT DISTINCT					
							null as EQUIPMENT_DESCRIPTION,
							{DynamicValueForStatus}
							null as EQUIPMENT_QUANTITY,
							SAQRIT.OBJECT_ID,
							null as EQUIPMENT_ID,
							null as EQUIPMENT_RECORD_ID,
							SAQRIT.LINE,
							SAQRIT.QUOTE_ID, 
							SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
							SAQRIT.QUOTE_RECORD_ID,
							SAQRIT.QTEREV_ID,
							SAQRIT.QTEREV_RECORD_ID,
							null as KPU,
							null as SERIAL_NO, 
							SAQRIT.SERVICE_DESCRIPTION, 
							SAQRIT.SERVICE_ID, 
							SAQRIT.SERVICE_RECORD_ID,								
							null as TECHNOLOGY,																			
							null as CUSTOMER_TOOL_ID, 
							null as EQUIPMENTCATEGORY_ID, 
							null as EQUIPMENTCATEGORY_RECORD_ID, 
							null as EQUIPMENT_STATUS,					
							null as MNT_PLANT_ID, 
							null as MNT_PLANT_NAME, 
							null as MNT_PLANT_RECORD_ID,			
							SAQTRV.SALESORG_ID, 
							SAQTRV.SALESORG_NAME, 
							SAQTRV.SALESORG_RECORD_ID, 
							SAQRIT.FABLOCATION_ID,
							SAQRIT.FABLOCATION_NAME,
							SAQRIT.FABLOCATION_RECORD_ID,
							SAQRIT.GREENBOOK, 
							SAQRIT.GREENBOOK_RECORD_ID, 			
							SAQTRV.GLOBAL_CURRENCY,
							SAQTRV.GLOBAL_CURRENCY_RECORD_ID,					
							SAQRIT.OBJECT_TYPE				
						FROM 
							SAQRIT 
							JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID         
							JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
							JOIN SAQSGE (NOLOCK) ON SAQSGE.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQSGE.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQSGE.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQSGE.GREENBOOK = SAQRIT.GREENBOOK
							LEFT JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQRIT.SERVICE_ID AND PRCFVA.FACTOR_ID = 'YOYDIS'
											
						WHERE 
							SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSGE.CONFIGURATION_STATUS,'') = 'COMPLETE'
					) IQ
					LEFT JOIN (
							SELECT QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_RECORD_ID, FABLOCATION_RECORD_ID, GREENBOOK_RECORD_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, CONCAT('YEAR ',YEAR_NUM) as YEAR_WISE, CASE WHEN YEAR_NUM = YEAR THEN CONTRACT_VALID_TO ELSE DATEADD(yy,YEAR_NUM,DATEADD(dd,-1,CONTRACT_VALID_FROM)) END as VALID_TO, DATEADD(yy,YEAR_NUM-1,CONTRACT_VALID_FROM) as VALID_FROM
							FROM (
								SELECT DISTINCT CEILING(DATEDIFF(mm,CONTRACT_VALID_FROM,CONTRACT_VALID_TO)/12.0) as YEAR, QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_RECORD_ID, FABLOCATION_RECORD_ID, GREENBOOK_RECORD_ID, CONTRACT_VALID_FROM,CONTRACT_VALID_TO							
								FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'
							) IQ_SAQRIT CROSS JOIN (SELECT 1 as YEAR_NUM UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) CJQ where YEAR>=YEAR_NUM
						) CONTRACT_TEMP ON  CONTRACT_TEMP.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND CONTRACT_TEMP.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND CONTRACT_TEMP.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND ISNULL(CONTRACT_TEMP.FABLOCATION_RECORD_ID,'') = ISNULL(IQ.FABLOCATION_RECORD_ID,'') AND CONTRACT_TEMP.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID
					) OQ
					LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = OQ.SERVICE_RECORD_ID AND ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = ISNULL(OQ.FABLOCATION_RECORD_ID,'') AND SAQICO.GREENBOOK_RECORD_ID = OQ.GREENBOOK_RECORD_ID 
					WHERE ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = '' AND ISNULL(SAQICO.GREENBOOK_RECORD_ID,'') = ''
					""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, DynamicValueForStatus = dynamic_value_for_status,DynamicColNames = dynamic_col_names)
				)

				Sql.RunQuery("""UPDATE SAQTRV SET REVISION_STATUS = 'ACQUIRING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QTEREV_RECORD_ID}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
	def _quote_item_line_entitlement_insert(self, update=False):
		# Update - Start
		#item_line_covered_object_entitlement_join_string = ""	
		#item_line_covered_object_entitlement_where_string = ""		
		#if update:
		##deleteing SAQIEN record
		Sql.RunQuery("DELETE SAQIEN FROM SAQIEN (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		item_line_covered_object_entitlement_where_string = " AND ISNULL(SAQIEN.EQUIPMENT_RECORD_ID,'') = '' "
		item_line_covered_object_entitlement_join_string = "LEFT JOIN SAQIEN (NOLOCK) ON SAQIEN.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQIEN.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQIEN.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQIEN.FABLOCATION_RECORD_ID = SAQSCE.FABLOCATION_RECORD_ID AND SAQIEN.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID"
		# Update - End
		item_line_covered_object_entitlement_query = """INSERT SAQIEN (QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,QTESRVENT_RECORD_ID,SERVICE_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION,SERIAL_NO,ENTITLEMENT_XML,CPS_CONFIGURATION_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,LINE,CPS_MATCH_ID,QTEITMCOB_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QTEITM_RECORD_ID) 
		(
			SELECT 
				DISTINCT CONVERT(VARCHAR(4000), NEWID()) AS QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID, SAQSCE.QUOTE_ID,SAQSCE.QUOTE_RECORD_ID,SAQSCE.QTEREV_ID,SAQSCE.QTEREV_RECORD_ID,SAQSCE.QTESRVENT_RECORD_ID,SAQSCE.SERVICE_RECORD_ID,SAQSCE.SERVICE_ID,SAQSCE.SERVICE_DESCRIPTION,SAQICO.SERIAL_NO,SAQSCE.ENTITLEMENT_XML,SAQSCE.CPS_CONFIGURATION_ID,SAQSCE.FABLOCATION_ID,SAQSCE.FABLOCATION_NAME,SAQSCE.FABLOCATION_RECORD_ID,SAQICO.LINE,SAQSCE.CPS_MATCH_ID,SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID as QTEITMCOB_RECORD_ID,SAQICO.EQUIPMENT_ID,SAQICO.EQUIPMENT_RECORD_ID,SAQSCE.SALESORG_ID,SAQSCE.SALESORG_NAME,SAQSCE.SALESORG_RECORD_ID,SAQICO.QTEITM_RECORD_ID 
			FROM SAQSCE (NOLOCK) 
			JOIN SAQICO ON SAQICO.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQICO.SERVICE_ID = SAQSCE.SERVICE_ID AND SAQICO.						QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQICO.FABLOCATION_ID = SAQSCE.FABLOCATION_ID 
							AND SAQICO.GREENBOOK = SAQSCE.GREENBOOK AND SAQICO.EQUIPMENT_ID = SAQSCE.EQUIPMENT_ID 
			
			{JoinString}
			WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCE.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' {WhereString}
		)""".format(
		QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,
		JoinString=item_line_covered_object_entitlement_join_string, WhereString=item_line_covered_object_entitlement_where_string)
		Log.Info("===>INSERT SAQIEN===> "+str(item_line_covered_object_entitlement_query))
		Sql.RunQuery(item_line_covered_object_entitlement_query)

		# temp_equipment_entitlement_table = "ITEM_INSERT_SAQSCE_BKP_{}".format(self.contract_quote_id)
		# try:
		# 	Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(temp_equipment_entitlement_table)+"'' ) BEGIN DROP TABLE "+str(temp_equipment_entitlement_table)+" END  ' ")
		# 	where_condition = "QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id)
		# 	where_condition = where_condition.replace("'","''")

		# 	Sql.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><QTEREV_RECORD_ID>''+QTEREV_RECORD_ID+''</QTEREV_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><FABLOCATION_ID>''+FABLOCATION_ID+''</FABLOCATION_ID><GREENBOOK>''+GREENBOOK+''</GREENBOOK><EQUIPMENT_ID>''+equipment_id+''</EQUIPMENT_ID>'' AS sml,replace(replace(replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,''&'','';#38''),'''','';#39''),'' < '','' &lt; '' ),'' > '','' &gt; '' ),''_>'',''_&gt;''),''_<'',''_&lt;''),''&'','';#38''),''<10%'',''&lt;10%'') as entitlement_xml FROM SAQSCE (NOLOCK) WHERE "+str(where_condition)+" )A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,EQUIPMENT_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,FABLOCATION_ID,GREENBOOK,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_PRICE_IMPACT,IS_DEFAULT,ENTITLEMENT_TYPE,ENTITLEMENT_DESCRIPTION,PRICE_METHOD,CALCULATION_FACTOR INTO "+str(temp_equipment_entitlement_table)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',QTEREV_RECORD_ID VARCHAR(100) ''QTEREV_RECORD_ID'',EQUIPMENT_ID VARCHAR(100) ''EQUIPMENT_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',FABLOCATION_ID VARCHAR(100) ''FABLOCATION_ID'',GREENBOOK VARCHAR(100) ''GREENBOOK'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_DESCRIPTION VARCHAR(100) ''ENTITLEMENT_DESCRIPTION'',PRICE_METHOD VARCHAR(100) ''PRICE_METHOD'',CALCULATION_FACTOR VARCHAR(100) ''CALCULATION_FACTOR'') ; exec sys.sp_xml_removedocument @H; '")
		# 	Log.Info("====> Insert SAQIAC ==> "+str("""INSERT SAQIAC (ASSEMBLY_ID,ASSEMBLY_RECORD_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,KIT_NAME,KIT_NUMBER,KITNUMBER_RECORD_ID,KIT_RECORD_ID,LINE,PM_ID,PM_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUOTE_ID,QTEITMCOB_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERIAL_NUMBER,YEAR,QUOTE_REV_ITM_ANNUAL_COMP_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
		# 		SELECT IQ.*, 
		# 			CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITM_ANNUAL_COMP_RECORD_ID, 
		# 			'{UserName}' AS CPQTABLEENTRYADDEDBY,
		# 			GETDATE() as CPQTABLEENTRYDATEADDED,
		# 			{UserId} as CpqTableEntryModifiedBy,
		# 			GETDATE() as CpqTableEntryDateModified FROM (
		# 				SELECT 
		# 					SAQICO.ASSEMBLY_ID,
		# 					SAQICO.ASSEMBLY_RECORD_ID,
		# 					SAQICO.EQUIPMENT_DESCRIPTION,
		# 					SAQICO.EQUIPMENT_ID,
		# 					SAQICO.EQUIPMENT_RECORD_ID,
		# 					SAQICO.KIT_NAME,
		# 					SAQICO.KIT_NUMBER,
		# 					null as KITNUMBER_RECORD_ID,
		# 					null as KIT_RECORD_ID,
		# 					SAQICO.LINE,
		# 					SAQICO.PM_ID,
		# 					SAQICO.PM_RECORD_ID,
		# 					SAQICO.SERVICE_DESCRIPTION,
		# 					SAQICO.SERVICE_ID,
		# 					SAQICO.SERVICE_RECORD_ID,
		# 					SAQICO.QUOTE_ID,
		# 					SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID as QTEITMCOB_RECORD_ID,
		# 					SAQICO.QTEITM_RECORD_ID,
		# 					SAQICO.QUOTE_RECORD_ID,
		# 					SAQICO.QTEREV_ID,
		# 					SAQICO.QTEREV_RECORD_ID,
		# 					SAQICO.SERIAL_NO as SERIAL_NUMBER,
		# 				FROM SAQICO (NOLOCK)
		# 				JOIN {TempEquipmentEntitlementTable} TEQENT ON TEQENT.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND TEQENT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND TEQENT.SERVICE_ID = SAQICO.SERVICE_ID AND TEQENT.FABLOCATION_ID = SAQICO.FABLOCATION_ID AND TEQENT.GREENBOOK = SAQICO.GREENBOOK AND TEQENT.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID
		# 				LEFT JOIN PRENTL (NOLOCK) ON PRENTL.SERVICE_ID = TEQENT.SERVICE_ID AND PRENTL.ENTITLEMENT_ID = TEQENT.ENTITLEMENT_ID AND PRENTL.ACTIVE = 1
		# 				WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}
		# 			)IQ
		# 			LEFT JOIN SAQIAC (NOLOCK) WHERE SAQIAC.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQIAC.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQIAC.SERVICE_ID = IQ.SERVICE_ID AND SAQIAC.FABLOCATION_ID = IQ.FABLOCATION_ID AND SAQIAC.GREENBOOK = IQ.GREENBOOK AND SAQIAC.EQUIPMENT_ID = IQ.EQUIPMENT_ID 
		# 	""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id)))
		# 	Sql.RunQuery("""INSERT SAQIAC (ASSEMBLY_ID,ASSEMBLY_RECORD_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,KIT_NAME,KIT_NUMBER,KITNUMBER_RECORD_ID,KIT_RECORD_ID,LINE,PM_ID,PM_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUOTE_ID,QTEITMCOB_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERIAL_NUMBER,YEAR,QUOTE_REV_ITM_ANNUAL_COMP_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
		# 		SELECT IQ.*, 
		# 			CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITM_ANNUAL_COMP_RECORD_ID, 
		# 			'{UserName}' AS CPQTABLEENTRYADDEDBY,
		# 			GETDATE() as CPQTABLEENTRYDATEADDED,
		# 			{UserId} as CpqTableEntryModifiedBy,
		# 			GETDATE() as CpqTableEntryDateModified FROM (
		# 				SELECT 
		# 					SAQICO.ASSEMBLY_ID,
		# 					SAQICO.ASSEMBLY_RECORD_ID,
		# 					SAQICO.EQUIPMENT_DESCRIPTION,
		# 					SAQICO.EQUIPMENT_ID,
		# 					SAQICO.EQUIPMENT_RECORD_ID,
		# 					SAQICO.KIT_NAME,
		# 					SAQICO.KIT_NUMBER,
		# 					null as KITNUMBER_RECORD_ID,
		# 					null as KIT_RECORD_ID,
		# 					SAQICO.LINE,
		# 					SAQICO.PM_ID,
		# 					SAQICO.PM_RECORD_ID,
		# 					SAQICO.SERVICE_DESCRIPTION,
		# 					SAQICO.SERVICE_ID,
		# 					SAQICO.SERVICE_RECORD_ID,
		# 					SAQICO.QUOTE_ID,
		# 					SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID as QTEITMCOB_RECORD_ID,
		# 					SAQICO.QTEITM_RECORD_ID,
		# 					SAQICO.QUOTE_RECORD_ID,
		# 					SAQICO.QTEREV_ID,
		# 					SAQICO.QTEREV_RECORD_ID,
		# 					SAQICO.SERIAL_NO as SERIAL_NUMBER,
		# 				FROM SAQICO (NOLOCK)
		# 				JOIN {TempEquipmentEntitlementTable} TEQENT ON TEQENT.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND TEQENT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND TEQENT.SERVICE_ID = SAQICO.SERVICE_ID AND TEQENT.FABLOCATION_ID = SAQICO.FABLOCATION_ID AND TEQENT.GREENBOOK = SAQICO.GREENBOOK AND TEQENT.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID
		# 				LEFT JOIN PRENTL (NOLOCK) ON PRENTL.SERVICE_ID = TEQENT.SERVICE_ID AND PRENTL.ENTITLEMENT_ID = TEQENT.ENTITLEMENT_ID AND PRENTL.ACTIVE = 1
		# 				WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}
		# 			)IQ
		# 			LEFT JOIN SAQIAC (NOLOCK) WHERE SAQIAC.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQIAC.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQIAC.SERVICE_ID = IQ.SERVICE_ID AND SAQIAC.FABLOCATION_ID = IQ.FABLOCATION_ID AND SAQIAC.GREENBOOK = IQ.GREENBOOK AND SAQIAC.EQUIPMENT_ID = IQ.EQUIPMENT_ID
		# 	""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		# except Exception:
		# 	Log.Info("Error in SAQIAC insert")
		# finally:
		# 	Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(temp_equipment_entitlement_table)+"'' ) BEGIN DROP TABLE "+str(temp_equipment_entitlement_table)+" END  ' ")
	
	def _quote_items_object_insert(self, update=False):
		join_condition_string = ""
		#item_object_where_string = ""
		#item_object_join_string = ""
		if self.quote_service_entitlement_type in ('OFFERING + EQUIPMENT','OFFERING+EQUIPMENT'):
			join_condition_string = ' AND SAQRIT.OBJECT_ID = SAQSCO.EQUIPMENT_ID'
		#if update:
		item_object_where_string = "AND ISNULL(SAQRIO.EQUIPMENT_RECORD_ID,'') = '' "
		item_object_join_string = "LEFT JOIN SAQRIO (NOLOCK) ON SAQRIO.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQRIO.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQRIO.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQRIO.GREENBOOK_RECORD_ID = SAQSCE.GREENBOOK_RECORD_ID AND SAQRIO.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID"
		if self.quote_service_entitlement_type in ("OFFERING + PM EVENT","OFFERING + SCH. MAIN. EVENT"):
			Sql.RunQuery("""INSERT SAQRIO (CUSTOMER_TOOL_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, KPU, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, SERIAL_NUMBER, TECHNOLOGY, TOOL_CONFIGURATION, WAFER_SIZE, QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
					SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
					SELECT DISTINCT
						null as CUSTOMER_TOOL_ID,
						IQ.EQUIPMENT_DESCRIPTION,					
						IQ.EQUIPMENT_ID,
						IQ.EQUIPMENT_RECORD_ID,                        
						IQ.GREENBOOK, 
						IQ.GREENBOOK_RECORD_ID,
						null as KPU,
						SAQRIT.LINE as LINE,
						IQ.SERVICE_DESCRIPTION, 
						IQ.SERVICE_ID, 
						IQ.SERVICE_RECORD_ID, 
						SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
						SAQTRV.QUOTE_ID,
						SAQTRV.QUOTE_RECORD_ID,
						SAQTRV.QTEREV_ID,
						SAQTRV.QTEREV_RECORD_ID,
						null as SERIAL_NUMBER, 
						null as TECHNOLOGY, 
						--PRPRBM.TOOL_CONFIGURATION,
						null as TOOL_CONFIGURATION,
						null as WAFER_SIZE					
					FROM 
						(
							SELECT DISTINCT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PM_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.EQUIPMENT_ID,SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION,SAQGPA.GREENBOOK_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_RECORD_ID,PROCESS_TYPE,TECHNOLOGY_NODE
								FROM SAQGPA (NOLOCK) INNER JOIN MAEQUP (NOLOCK) ON SAQGPA.ASSEMBLY_ID = MAEQUP.EQUIPMENT_ID  AND SAQGPA.FABLOCATION_ID = MAEQUP.FABLOCATION_ID AND MAEQUP.GOT_CODE = SAQGPA.GOT_CODE AND MAEQUP.PAR_EQUIPMENT_ID = SAQGPA.EQUIPMENT_ID
								WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' 
						) IQ
						
						JOIN SAQGPE (NOLOCK) ON SAQGPE.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID  AND SAQGPE.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID  AND IQ.GREENBOOK = SAQGPE.GREENBOOK AND IQ.GOT_CODE = SAQGPE.GOT_CODE AND IQ.PM_ID = SAQGPE.PM_ID AND IQ.SERVICE_ID = SAQGPE.SERVICE_ID
						JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID         
						JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
						JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
												AND SAQRIT.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID
												AND SAQRIT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID
												AND SAQRIT.FABLOCATION_ID = IQ.FABLOCATION_ID
												AND SAQRIT.GREENBOOK = IQ.GREENBOOK
												AND SAQRIT.OBJECT_ID = IQ.PM_ID
												AND SAQRIT.GOT_CODE = IQ.GOT_CODE
						-- LEFT JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.EQUIPMENT_RECORD_ID = IQ.EQUIPMENT_RECORD_ID AND PRPRBM.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID		
						LEFT JOIN SAQRIO (NOLOCK) ON SAQRIO.QUOTE_RECORD_ID = SAQGPE.QUOTE_RECORD_ID AND SAQRIO.QTEREV_RECORD_ID = SAQGPE.QTEREV_RECORD_ID AND SAQRIO.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQRIO.GREENBOOK_RECORD_ID = SAQGPE.GREENBOOK_RECORD_ID AND SAQRIO.EQUIPMENT_RECORD_ID = IQ.EQUIPMENT_RECORD_ID	
						WHERE 
							IQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND IQ.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND IQ.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQGPE.CONFIGURATION_STATUS,'') = 'COMPLETE' AND ISNULL(SAQRIO.EQUIPMENT_RECORD_ID,'') = ''
						) IQ
					""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,
					JoinString=item_object_join_string, JoinConditionString=join_condition_string, WhereConditionString=item_object_where_string)
				)
		
		else:
			Log.Info("====>INSERT SAQRIO===> "+str("""INSERT SAQRIO (CUSTOMER_TOOL_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, KPU, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, SERIAL_NUMBER, TECHNOLOGY, TOOL_CONFIGURATION, WAFER_SIZE, QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
					SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
					SELECT DISTINCT
						SAQSCO.CUSTOMER_TOOL_ID,
						SAQSCO.EQUIPMENT_DESCRIPTION,					
						SAQSCO.EQUIPMENT_ID,
						SAQSCO.EQUIPMENT_RECORD_ID,                        
						SAQSCO.GREENBOOK, 
						SAQSCO.GREENBOOK_RECORD_ID,
						SAQSCO.KPU,
						SAQRIT.LINE as LINE,
						SAQSCO.SERVICE_DESCRIPTION, 
						SAQSCO.SERVICE_ID, 
						SAQSCO.SERVICE_RECORD_ID, 
						SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
						SAQSCO.QUOTE_ID,
						SAQSCO.QUOTE_RECORD_ID,
						SAQSCO.QTEREV_ID,
						SAQSCO.QTEREV_RECORD_ID,
						SAQSCO.SERIAL_NO as SERIAL_NUMBER, 
						SAQSCO.TECHNOLOGY, 
						--PRPRBM.TOOL_CONFIGURATION,
						null as TOOL_CONFIGURATION,
						SAQSCO.WAFER_SIZE					
					FROM 
						SAQSCO (NOLOCK)					 
						JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCE.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCE.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
						AND SAQSCE.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
						JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
						JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
						JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
												AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
												AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
												AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID
												{JoinConditionString}
						--LEFT JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND PRPRBM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID		
						{JoinString}					
					WHERE 
						SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' {WhereConditionString}
					) IQ
					""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,
					JoinString=item_object_join_string, JoinConditionString=join_condition_string, WhereConditionString=item_object_where_string)
				))
			Sql.RunQuery("""INSERT SAQRIO (CUSTOMER_TOOL_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, KPU, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, SERIAL_NUMBER, TECHNOLOGY, TOOL_CONFIGURATION, WAFER_SIZE, QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
					SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
					SELECT DISTINCT
						SAQSCO.CUSTOMER_TOOL_ID,
						SAQSCO.EQUIPMENT_DESCRIPTION,					
						SAQSCO.EQUIPMENT_ID,
						SAQSCO.EQUIPMENT_RECORD_ID,                        
						SAQSCO.GREENBOOK, 
						SAQSCO.GREENBOOK_RECORD_ID,
						SAQSCO.KPU,
						SAQRIT.LINE as LINE,
						SAQSCO.SERVICE_DESCRIPTION, 
						SAQSCO.SERVICE_ID, 
						SAQSCO.SERVICE_RECORD_ID, 
						SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
						SAQSCO.QUOTE_ID,
						SAQSCO.QUOTE_RECORD_ID,
						SAQSCO.QTEREV_ID,
						SAQSCO.QTEREV_RECORD_ID,
						SAQSCO.SERIAL_NO as SERIAL_NUMBER, 
						SAQSCO.TECHNOLOGY, 
						--PRPRBM.TOOL_CONFIGURATION,
						null as TOOL_CONFIGURATION,
						SAQSCO.WAFER_SIZE					
					FROM 
						SAQSCO (NOLOCK)					 
						JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCE.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCE.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
						AND SAQSCE.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
						JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
						JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
						JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
												AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
												AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
												AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID
												{JoinConditionString}
						--LEFT JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND PRPRBM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID		
						{JoinString}					
					WHERE 
						SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' {WhereConditionString}
					) IQ
					""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,
					JoinString=item_object_join_string, JoinConditionString=join_condition_string, WhereConditionString=item_object_where_string)
				)

		##update quantity in SAQRIT
		if self.quote_service_entitlement_type not in ('OFFERING + EQUIPMENT','OFFERING+EQUIPMENT'):
			self._quote_item_qty_update()

	def _quote_items_entitlement_insert(self, update=False):		
		join_condition_string = ''
		dynamic_group_id_value = 'null as ENTITLEMENT_GROUP_ID'
		dynamic_is_changed_value = 'null as IS_CHANGED'
		if self.quote_service_entitlement_type in ('OFFERING + EQUIPMENT','OFFERING+EQUIPMENT'):
			join_condition_string = ' AND SAQRIT.FABLOCATION_RECORD_ID = {ObjectName}.FABLOCATION_RECORD_ID AND SAQRIT.OBJECT_ID = {ObjectName}.EQUIPMENT_ID'.format(ObjectName=self.source_object_name)
			dynamic_group_id_value = '{ObjectName}.ENTITLEMENT_GROUP_ID'.format(ObjectName=self.source_object_name)
			dynamic_is_changed_value = '{ObjectName}.IS_CHANGED'.format(ObjectName=self.source_object_name)
		#if update: # need to verify one more time
		Sql.RunQuery("DELETE SAQITE FROM SAQITE WHERE SAQITE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQITE.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		Log.Info("===> INSERT SAQITE ===> "+str("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID)
					SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified,
						{ObjectName}.CPS_CONFIGURATION_ID,
						{ObjectName}.CPS_MATCH_ID,
						null as ENTITLEMENT_COST_IMPACT,
						{dynamic_group_id_value},
						null as ENTITLEMENT_GROUP_XML,
						null as ENTITLEMENT_PRICE_IMPACT,
						{ObjectName}.ENTITLEMENT_XML,
						{dynamic_is_changed_value},
						SAQRIT.LINE,						
						SAQRIT.SERVICE_DESCRIPTION,
						SAQRIT.SERVICE_ID,
						SAQRIT.SERVICE_RECORD_ID,
						SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
						SAQRIT.QUOTE_ID,
						SAQRIT.QUOTE_RECORD_ID,
						SAQRIT.QTEREV_ID,
						SAQRIT.QTEREV_RECORD_ID,						
						SAQRIT.GREENBOOK,
						SAQRIT.GREENBOOK_RECORD_ID
					FROM {ObjectName} (NOLOCK) 
					JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID
												AND SAQRIT.SERVICE_RECORD_ID = {ObjectName}.SERVICE_RECORD_ID
												AND SAQRIT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID
												AND SAQRIT.FABLOCATION_RECORD_ID = {ObjectName}.FABLOCATION_RECORD_ID
												AND SAQRIT.GREENBOOK_RECORD_ID = {ObjectName}.GREENBOOK_RECORD_ID		
												{JoinConditionString}			
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE'			
				""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinConditionString=join_condition_string, dynamic_is_changed_value = dynamic_is_changed_value, dynamic_group_id_value = dynamic_group_id_value)))
		Sql.RunQuery("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID)
					SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified,
						{ObjectName}.CPS_CONFIGURATION_ID,
						{ObjectName}.CPS_MATCH_ID,
						null as ENTITLEMENT_COST_IMPACT,
						{dynamic_group_id_value},
						null as ENTITLEMENT_GROUP_XML,
						null as ENTITLEMENT_PRICE_IMPACT,
						{ObjectName}.ENTITLEMENT_XML,
						{dynamic_is_changed_value},
						SAQRIT.LINE,						
						SAQRIT.SERVICE_DESCRIPTION,
						SAQRIT.SERVICE_ID,
						SAQRIT.SERVICE_RECORD_ID,
						SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
						SAQRIT.QUOTE_ID,
						SAQRIT.QUOTE_RECORD_ID,
						SAQRIT.QTEREV_ID,
						SAQRIT.QTEREV_RECORD_ID,						
						SAQRIT.GREENBOOK,
						SAQRIT.GREENBOOK_RECORD_ID
					FROM {ObjectName} (NOLOCK) 
					JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID
												AND SAQRIT.SERVICE_RECORD_ID = {ObjectName}.SERVICE_RECORD_ID
												AND SAQRIT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID	
												AND ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ISNULL({ObjectName}.GREENBOOK_RECORD_ID,'')
												{JoinConditionString}			
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE'			
				""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinConditionString=join_condition_string, dynamic_is_changed_value = dynamic_is_changed_value, dynamic_group_id_value = dynamic_group_id_value))
		return True

	def _quote_items_fpm_entitlement_insert(self, update=False):		
		join_condition_string = ''
		dynamic_group_id_value = 'null as ENTITLEMENT_GROUP_ID'
		dynamic_is_changed_value = 'null as IS_CHANGED'
		# if self.quote_service_entitlement_type in ('OFFERING + EQUIPMENT','OFFERING+EQUIPMENT'):
		# 	join_condition_string = ' AND SAQRIT.FABLOCATION_RECORD_ID = {ObjectName}.FABLOCATION_RECORD_ID AND SAQRIT.OBJECT_ID = {ObjectName}.EQUIPMENT_ID'.format(ObjectName=self.source_object_name)
		# 	dynamic_group_id_value = '{ObjectName}.ENTITLEMENT_GROUP_ID'.format(ObjectName=self.source_object_name)
		# 	dynamic_is_changed_value = '{ObjectName}.IS_CHANGED'.format(ObjectName=self.source_object_name)
		#if update: # need to verify one more time
		Sql.RunQuery("DELETE SAQITE FROM SAQITE WHERE SAQITE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQITE.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		Log.Info("===> INSERT SAQITE ===> "+str("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID)
					SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified,
						{ObjectName}.CPS_CONFIGURATION_ID,
						{ObjectName}.CPS_MATCH_ID,
						null as ENTITLEMENT_COST_IMPACT,
						{dynamic_group_id_value},
						null as ENTITLEMENT_GROUP_XML,
						null as ENTITLEMENT_PRICE_IMPACT,
						{ObjectName}.ENTITLEMENT_XML,
						{dynamic_is_changed_value},
						SAQRIT.LINE,						
						SAQRIT.SERVICE_DESCRIPTION,
						SAQRIT.SERVICE_ID,
						SAQRIT.SERVICE_RECORD_ID,
						SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
						SAQRIT.QUOTE_ID,
						SAQRIT.QUOTE_RECORD_ID,
						SAQRIT.QTEREV_ID,
						SAQRIT.QTEREV_RECORD_ID						
					FROM {ObjectName} (NOLOCK) 
					JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID
												AND SAQRIT.SERVICE_ID = {ObjectName}.SERVICE_ID
												AND SAQRIT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID		
												{JoinConditionString}			
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE'			
				""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinConditionString=join_condition_string, dynamic_is_changed_value = dynamic_is_changed_value, dynamic_group_id_value = dynamic_group_id_value)))
		Sql.RunQuery("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID)
					SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified,
						{ObjectName}.CPS_CONFIGURATION_ID,
						{ObjectName}.CPS_MATCH_ID,
						null as ENTITLEMENT_COST_IMPACT,
						{dynamic_group_id_value},
						null as ENTITLEMENT_GROUP_XML,
						null as ENTITLEMENT_PRICE_IMPACT,
						{ObjectName}.ENTITLEMENT_XML,
						{dynamic_is_changed_value},
						SAQRIT.LINE,						
						SAQRIT.SERVICE_DESCRIPTION,
						SAQRIT.SERVICE_ID,
						SAQRIT.SERVICE_RECORD_ID,
						SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
						SAQRIT.QUOTE_ID,
						SAQRIT.QUOTE_RECORD_ID,
						SAQRIT.QTEREV_ID,
						SAQRIT.QTEREV_RECORD_ID
					FROM {ObjectName} (NOLOCK) 
					JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID
												AND SAQRIT.SERVICE_ID = {ObjectName}.SERVICE_ID
												AND SAQRIT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID	
												{JoinConditionString}			
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE'			
				""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinConditionString=join_condition_string, dynamic_is_changed_value = dynamic_is_changed_value, dynamic_group_id_value = dynamic_group_id_value))
		return True

	def _ordering_item_line_no(self):
		doctype_obj = Sql.GetFirst("SELECT ITEM_NUMBER_INCREMENT FROM SAQTRV LEFT JOIN SADOTY ON SADOTY.DOCTYPE_ID=SAQTRV.DOCTYP_ID WHERE SAQTRV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTRV.QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
		if doctype_obj:
			item_number_inc = int(doctype_obj.ITEM_NUMBER_INCREMENT)
			
		check_saqrit_record = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
		if check_saqrit_record:
			Sql.RunQuery("""UPDATE SAQRIT SET LINE  = IQ.line_order from SAQRIT (NOLOCK) INNER JOIN (SELECT CpqTableEntryId,ROW_NUMBER()OVER(ORDER BY(CpqTableEntryId)) * {itemnumberinc} as line_order FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ) IQ on IQ.CpqTableEntryId = SAQRIT.CpqTableEntryId  WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,itemnumberinc=item_number_inc))
			for obj in ['SAQICO','SAQRIO','SAQITE','SAQRIP','SAQIFP','SAQIBP']:
				Sql.RunQuery("""UPDATE {obj} SET LINE  = SAQRIT.LINE from {obj} (NOLOCK) INNER JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = {obj}.QUOTE_RECORD_ID AND {obj}.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND QTEITM_RECORD_ID = QUOTE_REVISION_CONTRACT_ITEM_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, obj=obj))

	def _set_quote_service_entitlement_type(self):
		##chk ancillary offering
		check_ancillary = Sql.GetFirst("SELECT PAR_SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' and SERVICE_ID = '{ServiceId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
		if check_ancillary:
			if check_ancillary.PAR_SERVICE_ID:
				self.parent_service_id = check_ancillary.PAR_SERVICE_ID

		Log.Info("_quote_items_insert ===> 1")
		# service_entitlement_obj = Sql.GetFirst("""SELECT ENTITLEMENT_ID,ENTITLEMENT_DISPLAY_VALUE FROM 
		# 								(
		# 									SELECT DISTINCT 
		# 											IQ.QUOTE_RECORD_ID,
		# 											IQ.QTEREV_RECORD_ID, 
		# 											replace(X.Y.value('(ENTITLEMENT_ID)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_ID,
		# 											replace(replace(replace(replace(X.Y.value('(ENTITLEMENT_DISPLAY_VALUE)[1]', 'VARCHAR(128)'),';#38','&'),';#39',''''),'_&lt;','_<' ),'_&gt;','_>') as ENTITLEMENT_DISPLAY_VALUE 
		# 									FROM (
		# 										SELECT QUOTE_RECORD_ID,QTEREV_RECORD_ID,CONVERT(xml,replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39'),' < ',' &lt; ' ),' > ',' &gt; ' ),'_>','_&gt;'),'_<','_&lt;'))  as ENTITLEMENT_XML  
		# 										FROM SAQTSE (NOLOCK) 
		# 										WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' and SERVICE_ID = '{ServiceId}' 
		# 										) IQ 
		# 									OUTER APPLY IQ.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) 
		# 								) as OQ 
		# 								WHERE ENTITLEMENT_ID LIKE '{EntitlementAttrId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id if not self.parent_service_id else self.parent_service_id,EntitlementAttrId='AGS_'+str(self.service_id)+'_PQB_QTITST'))
		#if service_entitlement_obj:
		# if self.action_type == 'UPDATE_LINE_ITEMS' and self.entitlement_level_obj != 'SAQTSE' and self.parent_service_id:
		# 	where_str = self.where_condition_string.replace('SRC.','').replace(self.service_id,self.parent_service_id).replace('WHERE','')
		# else:
		where_str = " QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' and SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id)
		service_entitlement_obj = Sql.GetFirst("""SELECT SERVICE_ID, ENTITLEMENT_XML FROM  {obj_name} (NOLOCK) WHERE {where_str}""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id, obj_name = self.entitlement_level_obj, where_str = where_str))
		if service_entitlement_obj:
			quote_item_tag_pattern = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
			entitlement_id_tag_pattern = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(self.service_id)+'_PQB_QTITST</ENTITLEMENT_ID>')

			entitlement_display_value_tag_pattern = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
			for quote_item_tag in re.finditer(quote_item_tag_pattern, service_entitlement_obj.ENTITLEMENT_XML):
				quote_item_tag_content = quote_item_tag.group(1)
				entitlement_id_tag_match = re.findall(entitlement_id_tag_pattern,quote_item_tag_content)	
				
				if entitlement_id_tag_match:
					entitlement_display_value_tag_match = re.findall(entitlement_display_value_tag_pattern,quote_item_tag_content)
					if entitlement_display_value_tag_match:
						self.quote_service_entitlement_type = entitlement_display_value_tag_match[0].upper()
						Trace.Write("---self.quote_service_entitlement_type"+str(self.quote_service_entitlement_type))
						if self.quote_service_entitlement_type in ('OFFERING + EQUIPMENT','OFFERING+EQUIPMENT'):
							Trace.Write("---===self.quote_service_entitlement_type"+str(self.quote_service_entitlement_type))
							self.source_object_name = 'SAQSCE'
						elif self.quote_service_entitlement_type in ('OFFERING + FAB + GREENBOOK + GROUP OF EQUIPMENT', 'OFFERING + GREENBOOK + GR EQUI', 'OFFERING + CHILD GROUP OF PART','OFFERING+FAB+GREENBOOK+CREDIT','OFFERING+GREENBOOK+TOOLS GROUP', 'OFFER. + FAB + GRNBK + CHILD','OFFERING + FAB + GREENBOOK'):
							self.source_object_name = 'SAQSGE'
						elif self.quote_service_entitlement_type in ('OFFERING+CONSIGNED+ON REQUEST','OFFERING'):
							self.source_object_name = 'SAQTSE'
						elif self.quote_service_entitlement_type in ('OFFERING + PM EVENT','OFFERING + SCH. MAIN. EVENT'):
							self.source_object_name = 'SAQGPE'
						break
				
				else:
					continue
			# if self.service_id == 'Z0101':
			# 	self.quote_service_entitlement_type = 'OFFERING + GREENBOOK + GR EQUI'
			Log.Info(str(self.contract_quote_id)+"_set_quote_service_entitlement_type ===> 2"+str(self.quote_service_entitlement_type))

	def _quote_items_summary_insert(self, update=False):
		if self.source_object_name:	
			item_summary_where_string = " AND ISNULL(SAQRIS.SERVICE_RECORD_ID,'') = '' "
			item_summary_join_string = "LEFT JOIN SAQRIS (NOLOCK) ON SAQRIS.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQRIS.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQRIS.SERVICE_RECORD_ID = {ObjectName}.SERVICE_RECORD_ID".format(ObjectName=self.source_object_name)	
			summary_last_line_no = 0
			quote_item_summary_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIS (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
			if quote_item_summary_obj:
				summary_last_line_no = int(quote_item_summary_obj.LINE) 	
			Trace.Write('###--->Inside Quote items summary insert function###')
			Log.Info("===> INSERT SAQRIS ===> "+str("""INSERT SAQRIS (CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DIVISION_ID, DIVISION_RECORD_ID, DOC_CURRENCY, DOCCURR_RECORD_ID, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, PLANT_ID, PLANT_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, LINE, QUOTE_REV_ITEM_SUMMARY_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
				SELECT IQ.*, ROW_NUMBER()OVER(ORDER BY(IQ.SERVICE_ID)) + {ItemSummaryLastLineNo} as LINE, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_SUMMARY_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
					SELECT DISTINCT
						SAQTRV.CONTRACT_VALID_FROM,
						SAQTRV.CONTRACT_VALID_TO,
						SAQTRV.DIVISION_ID,
						SAQTRV.DIVISION_RECORD_ID,
						SAQTRV.DOC_CURRENCY,
						SAQTRV.DOCCURR_RECORD_ID,
						SAQTRV.GLOBAL_CURRENCY,
						SAQTRV.GLOBAL_CURRENCY_RECORD_ID,						
						MAMSOP.PLANT_ID,
						MAMSOP.PLANT_RECORD_ID,
						{ObjectName}.SERVICE_DESCRIPTION,
						{ObjectName}.SERVICE_ID,
						{ObjectName}.SERVICE_RECORD_ID,						
						1 as QUANTITY,
						SAQTRV.QUOTE_ID,
						SAQTRV.QUOTE_RECORD_ID,
						SAQTMT.QTEREV_ID,
						SAQTMT.QTEREV_RECORD_ID
					FROM {ObjectName} (NOLOCK) 
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
					JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
					LEFT JOIN MAMSOP (NOLOCK) ON MAMSOP.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID AND MAMSOP.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSOP.DISTRIBUTIONCHANNEL_ID = SAQTRV.DISTRIBUTIONCHANNEL_ID			
					{JoinString}
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' {WhereConditionString}) IQ			
			""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, ItemSummaryLastLineNo=summary_last_line_no, WhereConditionString=item_summary_where_string, JoinString=item_summary_join_string)))
			Sql.RunQuery("""INSERT SAQRIS (CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DIVISION_ID, DIVISION_RECORD_ID, DOC_CURRENCY, DOCCURR_RECORD_ID, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, PLANT_ID, PLANT_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, LINE, QUOTE_REV_ITEM_SUMMARY_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
				SELECT IQ.*, ROW_NUMBER()OVER(ORDER BY(IQ.SERVICE_ID)) + {ItemSummaryLastLineNo} as LINE, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_SUMMARY_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
					SELECT DISTINCT
						SAQTRV.CONTRACT_VALID_FROM,
						SAQTRV.CONTRACT_VALID_TO,
						SAQTRV.DIVISION_ID,
						SAQTRV.DIVISION_RECORD_ID,
						SAQTRV.DOC_CURRENCY,
						SAQTRV.DOCCURR_RECORD_ID,
						SAQTRV.GLOBAL_CURRENCY,
						SAQTRV.GLOBAL_CURRENCY_RECORD_ID,						
						MAMSOP.PLANT_ID,
						MAMSOP.PLANT_RECORD_ID,
						{ObjectName}.SERVICE_DESCRIPTION,
						{ObjectName}.SERVICE_ID,
						{ObjectName}.SERVICE_RECORD_ID,						
						1 as QUANTITY,
						SAQTRV.QUOTE_ID,
						SAQTRV.QUOTE_RECORD_ID,
						SAQTMT.QTEREV_ID,
						SAQTMT.QTEREV_RECORD_ID
					FROM {ObjectName} (NOLOCK) 
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
					JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
					LEFT JOIN MAMSOP (NOLOCK) ON MAMSOP.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID AND MAMSOP.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSOP.DISTRIBUTIONCHANNEL_ID = SAQTRV.DISTRIBUTIONCHANNEL_ID			
					{JoinString}
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' {WhereConditionString}) IQ			
			""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, ItemSummaryLastLineNo=summary_last_line_no, WhereConditionString=item_summary_where_string, JoinString=item_summary_join_string))
			#self.getting_cps_tax(self.service_id)
			ScriptExecutor.ExecuteGlobal('CQCPSTAXRE',{'service_id':self.service_id, 'Fun_type':'CPQ_TO_ECC'})
		return True		
	
	def _pmsa_quote_items_entitlement_insert(self,update=False):
		#if update: # need to verify one more time
		Sql.RunQuery("DELETE SAQITE FROM SAQITE WHERE SAQITE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQITE.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		Sql.RunQuery("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID)
					SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified,OQ.* FROM ( SELECT DISTINCT 
						{ObjectName}.CPS_CONFIGURATION_ID,
						{ObjectName}.CPS_MATCH_ID,
						null as ENTITLEMENT_COST_IMPACT,
						null as ENTITLEMENT_GROUP_ID,
						null as ENTITLEMENT_GROUP_XML,
						null as ENTITLEMENT_PRICE_IMPACT,
						{ObjectName}.ENTITLEMENT_XML,
						null as IS_CHANGED,
						SAQRIT.LINE,						
						SAQRIT.SERVICE_DESCRIPTION,
						SAQRIT.SERVICE_ID,
						SAQRIT.SERVICE_RECORD_ID,
						SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
						SAQRIT.QUOTE_ID,
						SAQRIT.QUOTE_RECORD_ID,
						SAQRIT.QTEREV_ID,
						SAQRIT.QTEREV_RECORD_ID,						
						IQ.GREENBOOK,
						IQ.GREENBOOK_RECORD_ID
						FROM (
							SELECT DISTINCT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PM_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION,SAQGPA.SERVICE_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID,PROCESS_TYPE,TECHNOLOGY_NODE
								FROM SAQGPA (NOLOCK) 
									INNER JOIN MAEQUP (NOLOCK) ON SAQGPA.ASSEMBLY_ID = MAEQUP.EQUIPMENT_ID  AND SAQGPA.FABLOCATION_ID = MAEQUP.FABLOCATION_ID AND MAEQUP.GOT_CODE = SAQGPA.GOT_CODE AND MAEQUP.PAR_EQUIPMENT_ID = SAQGPA.EQUIPMENT_ID
								WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' 
								
						) IQ
						JOIN {ObjectName} (NOLOCK) ON {ObjectName}.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND {ObjectName}.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND {ObjectName}.GREENBOOK = IQ.GREENBOOK AND {ObjectName}.GOT_CODE = IQ.GOT_CODE AND {ObjectName}.PM_ID = IQ.PM_ID AND IQ.SERVICE_ID = SAQGPE.SERVICE_ID
						JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID
												AND SAQRIT.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID
												AND SAQRIT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID
												AND SAQRIT.GREENBOOK = IQ.GREENBOOK
												AND SAQRIT.FABLOCATION_ID = IQ.FABLOCATION_ID
												AND SAQRIT.OBJECT_ID = IQ.PM_ID
												AND SAQRIT.GOT_CODE = IQ.GOT_CODE
															
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND IQ.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' ) OQ			
				""".format(UserId=self.user_id, UserName=self.user_name, ObjectName='SAQGPE', QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		return True

	def _quote_items_insert(self, update=False):
		Log.Info("====>>> _quote_items_insert")
		#Log.Info("Checking_source_object_name"+str(source_object_name))
		Trace.Write("====>>> _quote_items_insert"+str(self.quote_service_entitlement_type))

		# dynamic_select_columns = ""
		# item_where_string = ""
		# item_join_string = ""
		# if self.quote_service_entitlement_type == 'OFFERING + EQUIPMENT':			
		# 	dynamic_select_columns = "SAQSCE.EQUIPMENT_ID as OBJECT_ID, 'EQUIPMENT' as OBJECT_TYPE, SAQSCE.FABLOCATION_ID as FABLOCATION_ID, SAQSCE.FABLOCATION_NAME as FABLOCATION_NAME, SAQSCE.FABLOCATION_RECORD_ID as FABLOCATION_RECORD_ID, "			
		# 	#if update:
		# 	item_where_string += "WHERE ISNULL(SAQRIT.OBJECT_ID,'') = '' "
		# 	item_join_string += "LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQRIT.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID AND ISNULL(SAQRIT.OBJECT_ID,'') = IQ.OBJECT_ID"
		# elif self.quote_service_entitlement_type in ('OFFERING + FAB + GREENBOOK + GROUP OF EQUIPMENT', 'OFFERING + GREENBOOK + GR EQUI', 'OFFERING + CHILD GROUP OF PART'):			
		# 	dynamic_select_columns = "null as OBJECT_ID, 'GREENBOOK' as OBJECT_TYPE, null as FABLOCATION_ID, null as FABLOCATION_NAME, null as FABLOCATION_RECORD_ID,"			
		# 	#if update:
		# 	item_where_string += "WHERE ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ''"
		# 	item_join_string += "LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID  AND SAQRIT.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID"	
		# else:
		# 	return False
		dynamic_global_curr_columns = ""
		dynamic_columns = get_billing_type = ""
		if self.is_ancillary == True:
			dynamic_global_curr_columns = " '0' AS NET_VALUE_INGL_CURR, '0' AS NET_PRICE_INGL_CURR,"
			dynamic_columns = "NET_VALUE_INGL_CURR, NET_PRICE_INGL_CURR,"
			if self.service_id == 'Z0046' and self.get_billing_type_val.upper() == 'VARIABLE':
				dynamic_global_curr_columns += " '0' AS ESTVAL_INGL_CURR,  '0' AS COMVAL_INGL_CURR,"
				dynamic_columns += "ESTVAL_INGL_CURR, COMVAL_INGL_CURR,"
		
		
		if self.source_object_name:		
			equipments_count = 0
			quote_item_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
			if quote_item_obj:
				equipments_count = int(quote_item_obj.LINE)
					
			if self.quote_service_entitlement_type in ('OFFERING + EQUIPMENT','OFFERING+EQUIPMENT'):
				#get billing type start
				
				Log.Info("===> INSERT SAQRIT ===> "+str("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE,{DynamicColumnNames} GREENBOOK, GREENBOOK_RECORD_ID, QTEITMSUM_RECORD_ID)
					SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified, 
						IQ.* FROM (
					SELECT
						DISTINCT
						SAQTRV.CONTRACT_VALID_FROM,
						SAQTRV.CONTRACT_VALID_TO,
						SAQTRV.DOC_CURRENCY,
						SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
						ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
						SAQTRV.EXCHANGE_RATE_DATE,
						SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
						null as GL_ACCOUNT_NO,
						SAQTRV.GLOBAL_CURRENCY,
						SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
						ROW_NUMBER()OVER(ORDER BY({ObjectName}.CpqTableEntryId)) + {EquipmentsCount} as LINE,
						SAQSCE.EQUIPMENT_ID as OBJECT_ID,
						'EQUIPMENT' as OBJECT_TYPE,
						SAQSCE.FABLOCATION_ID as FABLOCATION_ID,
						SAQSCE.FABLOCATION_NAME as FABLOCATION_NAME,
						SAQSCE.FABLOCATION_RECORD_ID as FABLOCATION_RECORD_ID,			
						{ObjectName}.SERVICE_DESCRIPTION,
						{ObjectName}.SERVICE_ID,
						{ObjectName}.SERVICE_RECORD_ID,
						null as PROFIT_CENTER,
						1 as QUANTITY,
						SAQTRV.QUOTE_ID,
						SAQTRV.QUOTE_RECORD_ID,
						SAQTMT.QTEREV_ID,
						SAQTMT.QTEREV_RECORD_ID,
						null as REF_SALESORDER,
						'ACQUIRING' as STATUS,
						MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
						MAMSCT.TAXCLASSIFICATION_ID,
						MAMSCT.TAXCLASSIFICATION_RECORD_ID,
						SAQRIS.TAX_PERCENTAGE,
						{DynamicNetValues}					
						{ObjectName}.GREENBOOK,
						{ObjectName}.GREENBOOK_RECORD_ID,
						SAQRIS.QUOTE_REV_ITEM_SUMMARY_RECORD_ID as QTEITMSUM_RECORD_ID
					FROM {ObjectName} (NOLOCK) 
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
					JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
					JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = {ObjectName}.SERVICE_ID
					JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID 
					LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.DIVISION_ID = SAQTRV.DIVISION_ID AND MAMSCT.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' 
					) IQ
					LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQRIT.FABLOCATION_RECORD_ID = IQ. FABLOCATION_RECORD_ID AND ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ISNULL(IQ.GREENBOOK_RECORD_ID,'') AND ISNULL(SAQRIT.OBJECT_ID,'') = IQ.OBJECT_ID
					WHERE ISNULL(SAQRIT.OBJECT_ID,'') = ''			
				""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count, DynamicNetValues=dynamic_global_curr_columns,DynamicColumnNames=dynamic_columns)))
				Log.Info("SAQRIT=== 1")
				Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE,{DynamicColumnNames} GREENBOOK,BILLING_TYPE,GREENBOOK_RECORD_ID, QTEITMSUM_RECORD_ID)
					SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified, 
						IQ.* FROM (
					SELECT
						DISTINCT
						SAQTRV.CONTRACT_VALID_FROM,
						SAQTRV.CONTRACT_VALID_TO,
						SAQTRV.DOC_CURRENCY,
						SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
						ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
						SAQTRV.EXCHANGE_RATE_DATE,
						SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
						null as GL_ACCOUNT_NO,
						SAQTRV.GLOBAL_CURRENCY,
						SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
						ROW_NUMBER()OVER(ORDER BY({ObjectName}.CpqTableEntryId)) + {EquipmentsCount} as LINE,
						SAQSCE.EQUIPMENT_ID as OBJECT_ID,
						'EQUIPMENT' as OBJECT_TYPE,
						SAQSCE.FABLOCATION_ID as FABLOCATION_ID,
						SAQSCE.FABLOCATION_NAME as FABLOCATION_NAME,
						SAQSCE.FABLOCATION_RECORD_ID as FABLOCATION_RECORD_ID,			
						{ObjectName}.SERVICE_DESCRIPTION,
						{ObjectName}.SERVICE_ID,
						{ObjectName}.SERVICE_RECORD_ID,
						null as PROFIT_CENTER,
						1 as QUANTITY,
						SAQTRV.QUOTE_ID,
						SAQTRV.QUOTE_RECORD_ID,
						SAQTMT.QTEREV_ID,
						SAQTMT.QTEREV_RECORD_ID,
						null as REF_SALESORDER,
						null as STATUS,
						MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
						MAMSCT.TAXCLASSIFICATION_ID,
						MAMSCT.TAXCLASSIFICATION_RECORD_ID,
						SAQRIS.TAX_PERCENTAGE,
						{DynamicNetValues}					
						{ObjectName}.GREENBOOK,
						'{billing_type}' as BILLING_TYPE,
						{ObjectName}.GREENBOOK_RECORD_ID,
						SAQRIS.QUOTE_REV_ITEM_SUMMARY_RECORD_ID as QTEITMSUM_RECORD_ID
					FROM {ObjectName} (NOLOCK) 
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
					JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
					JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = {ObjectName}.SERVICE_ID
					JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID 
					LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.DIVISION_ID = SAQTRV.DIVISION_ID AND MAMSCT.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' 
					) IQ
					LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQRIT.FABLOCATION_RECORD_ID = IQ. FABLOCATION_RECORD_ID AND ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ISNULL(IQ.GREENBOOK_RECORD_ID,'') AND ISNULL(SAQRIT.OBJECT_ID,'') = IQ.OBJECT_ID
					WHERE ISNULL(SAQRIT.OBJECT_ID,'') = ''			
				""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count, DynamicNetValues=dynamic_global_curr_columns,billing_type=self.get_billing_type_val,DynamicColumnNames=dynamic_columns))
			elif self.quote_service_entitlement_type in ('OFFERING + FAB + GREENBOOK + GROUP OF EQUIPMENT', 'OFFERING + GREENBOOK + GR EQUI', 'OFFERING + CHILD GROUP OF PART','OFFERING+GREENBOOK+TOOLS GROUP','OFFER. + FAB + GRNBK + CHILD','OFFERING + FAB + GREENBOOK'):
				Log.Info("===> INSERT SAQRIT 111111 ===> "+str("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE,{DynamicColumnNames} GREENBOOK, GREENBOOK_RECORD_ID, QTEITMSUM_RECORD_ID)
					SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified, 
						OQ.* 
					FROM (
						SELECT 
							DISTINCT
							SAQTRV.CONTRACT_VALID_FROM,
							SAQTRV.CONTRACT_VALID_TO,
							SAQTRV.DOC_CURRENCY,
							SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
							ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
							SAQTRV.EXCHANGE_RATE_DATE,
							SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
							null as GL_ACCOUNT_NO,
							SAQTRV.GLOBAL_CURRENCY,
							SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
							ROW_NUMBER()OVER(ORDER BY({ObjectName}.CpqTableEntryId)) + {EquipmentsCount} as LINE,
							null as OBJECT_ID,
							'EQUIPMENT' as OBJECT_TYPE,
							IQ.FABLOCATION_ID as FABLOCATION_ID,
							IQ.FABLOCATION_NAME as FABLOCATION_NAME,
							IQ.FABLOCATION_RECORD_ID as FABLOCATION_RECORD_ID,			
							{ObjectName}.SERVICE_DESCRIPTION,
							{ObjectName}.SERVICE_ID,
							{ObjectName}.SERVICE_RECORD_ID,
							null as PROFIT_CENTER,
							1 as QUANTITY,
							SAQTRV.QUOTE_ID,
							SAQTRV.QUOTE_RECORD_ID,
							SAQTMT.QTEREV_ID,
							SAQTMT.QTEREV_RECORD_ID,
							null as REF_SALESORDER,
							'ACQUIRING' as STATUS,
							MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
							MAMSCT.TAXCLASSIFICATION_ID,
							MAMSCT.TAXCLASSIFICATION_RECORD_ID,
							SAQRIS.TAX_PERCENTAGE,
							{DynamicNetValues}					
							{ObjectName}.GREENBOOK,
							{ObjectName}.GREENBOOK_RECORD_ID,
							SAQRIS.QUOTE_REV_ITEM_SUMMARY_RECORD_ID as QTEITMSUM_RECORD_ID
						FROM (
							SELECT 
								QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID 
							FROM SAQSCO (NOLOCK)
							WHERE SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' 
							GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID
						) IQ
						JOIN {ObjectName} (NOLOCK) ON {ObjectName}.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND {ObjectName}.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND {ObjectName}.SERVICE_ID = IQ.SERVICE_ID AND {ObjectName}.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID
						JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
						JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
						JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = {ObjectName}.SERVICE_ID
						JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID 
						LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.DIVISION_ID = SAQTRV.DIVISION_ID AND MAMSCT.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER
						WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' 
					) OQ
					LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = OQ.SERVICE_RECORD_ID  AND SAQRIT.GREENBOOK_RECORD_ID = OQ.GREENBOOK_RECORD_ID
					WHERE ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ''
				""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count, DynamicNetValues=dynamic_global_curr_columns,DynamicColumnNames=dynamic_columns)))
				Log.Info("SAQRIT=== 2")
				Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE,{DynamicColumnNames} GREENBOOK,BILLING_TYPE,GREENBOOK_RECORD_ID, QTEITMSUM_RECORD_ID)
					SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified, 
						OQ.* 
					FROM (
						SELECT 
							DISTINCT
							SAQTRV.CONTRACT_VALID_FROM,
							SAQTRV.CONTRACT_VALID_TO,
							SAQTRV.DOC_CURRENCY,
							SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
							ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
							SAQTRV.EXCHANGE_RATE_DATE,
							SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
							null as GL_ACCOUNT_NO,
							SAQTRV.GLOBAL_CURRENCY,
							SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
							--ROW_NUMBER()OVER(ORDER BY({ObjectName}.CpqTableEntryId)) + {EquipmentsCount} as LINE,
							null  as LINE,
							null as OBJECT_ID,
							'GREENBOOK' as OBJECT_TYPE,
							IQ.FABLOCATION_ID as FABLOCATION_ID,
							IQ.FABLOCATION_NAME as FABLOCATION_NAME,
							IQ.FABLOCATION_RECORD_ID as FABLOCATION_RECORD_ID,			
							{ObjectName}.SERVICE_DESCRIPTION,
							{ObjectName}.SERVICE_ID,
							{ObjectName}.SERVICE_RECORD_ID,
							null as PROFIT_CENTER,
							1 as QUANTITY,
							SAQTRV.QUOTE_ID,
							SAQTRV.QUOTE_RECORD_ID,
							SAQTMT.QTEREV_ID,
							SAQTMT.QTEREV_RECORD_ID,
							null as REF_SALESORDER,
							CASE WHEN {ObjectName}.SERVICE_ID = 'Z0101' THEN 'ACQUIRED' ELSE 'ACQUIRING' END AS STATUS,
							MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
							MAMSCT.TAXCLASSIFICATION_ID,
							MAMSCT.TAXCLASSIFICATION_RECORD_ID,
							SAQRIS.TAX_PERCENTAGE,
							{DynamicNetValues}					
							{ObjectName}.GREENBOOK,
							'{billing_type}' as BILLING_TYPE,
							{ObjectName}.GREENBOOK_RECORD_ID,
							SAQRIS.QUOTE_REV_ITEM_SUMMARY_RECORD_ID as QTEITMSUM_RECORD_ID
						FROM (
							SELECT 
								QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID 
							FROM SAQSCO (NOLOCK)
							WHERE SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' 
							GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID
						) IQ
						JOIN {ObjectName} (NOLOCK) ON {ObjectName}.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND {ObjectName}.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND {ObjectName}.SERVICE_ID = IQ.SERVICE_ID AND {ObjectName}.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID
						JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
						JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
						JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = {ObjectName}.SERVICE_ID
						JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID 
						LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.DIVISION_ID = SAQTRV.DIVISION_ID AND MAMSCT.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER
						WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' 
					) OQ
					LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = OQ.SERVICE_RECORD_ID  AND SAQRIT.GREENBOOK_RECORD_ID = OQ.GREENBOOK_RECORD_ID
					WHERE ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ''
				""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count,billing_type=self.get_billing_type_val, DynamicNetValues=dynamic_global_curr_columns,DynamicColumnNames=dynamic_columns))
			elif self.quote_service_entitlement_type in ("OFFERING + PM EVENT","OFFERING + SCH. MAIN. EVENT"):
				Log.Info("SAQRIT=== 3")
				Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE,PM_ID,PM_RECORD_ID,GOTCODE_RECORD_ID,GOT_CODE,PM_LEVEL, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE,{DynamicColumnNames} GREENBOOK,BILLING_TYPE,GREENBOOK_RECORD_ID, QTEITMSUM_RECORD_ID)
					SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified, 
						OQ.* 
					FROM (
						SELECT 
							DISTINCT
							SAQTRV.CONTRACT_VALID_FROM,
							SAQTRV.CONTRACT_VALID_TO,
							SAQTRV.DOC_CURRENCY,
							SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
							ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
							SAQTRV.EXCHANGE_RATE_DATE,
							SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
							null as GL_ACCOUNT_NO,
							SAQTRV.GLOBAL_CURRENCY,
							SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
							--ROW_NUMBER()OVER(ORDER BY(IQ.PM_ID)) + {EquipmentsCount} as LINE,
							null as LINE,
							IQ.PM_ID as OBJECT_ID,
							'EVENT' as OBJECT_TYPE,
							IQ.PM_ID,
							IQ.PM_RECORD_ID, 
							IQ.GOTCODE_RECORD_ID,
							IQ.GOT_CODE,
							IQ.PM_LEVEL,
							IQ.FABLOCATION_ID as FABLOCATION_ID,
							IQ.FABLOCATION_NAME as FABLOCATION_NAME,
							IQ.FABLOCATION_RECORD_ID as FABLOCATION_RECORD_ID,			
							IQ.SERVICE_DESCRIPTION,
							IQ.SERVICE_ID,
							IQ.SERVICE_RECORD_ID,
							null as PROFIT_CENTER,
							1 as QUANTITY,
							SAQTRV.QUOTE_ID,
							SAQTRV.QUOTE_RECORD_ID,
							SAQTMT.QTEREV_ID,
							SAQTMT.QTEREV_RECORD_ID,
							null as REF_SALESORDER,
							'ACQUIRING' as STATUS,
							MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
							MAMSCT.TAXCLASSIFICATION_ID,
							MAMSCT.TAXCLASSIFICATION_RECORD_ID,
							SAQRIS.TAX_PERCENTAGE,
							{DynamicNetValues}					
							IQ.GREENBOOK,
							'{billing_type}' as BILLING_TYPE,
							IQ.GREENBOOK_RECORD_ID,
							SAQRIS.QUOTE_REV_ITEM_SUMMARY_RECORD_ID as QTEITMSUM_RECORD_ID
						FROM (
							SELECT DISTINCT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PM_RECORD_ID, SAQGPA.GOTCODE_RECORD_ID, SAQGPA.PM_LEVEL,SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, PROCESS_TYPE, TECHNOLOGY_NODE
								FROM SAQGPA (NOLOCK)  INNER JOIN MAEQUP (NOLOCK) ON SAQGPA.ASSEMBLY_ID = MAEQUP.EQUIPMENT_ID  AND SAQGPA.FABLOCATION_ID = MAEQUP.FABLOCATION_ID AND MAEQUP.GOT_CODE = SAQGPA.GOT_CODE AND MAEQUP.PAR_EQUIPMENT_ID = SAQGPA.EQUIPMENT_ID
								WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' 
								
						) IQ
						JOIN {ObjectName} (NOLOCK) ON {ObjectName}.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND {ObjectName}.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND {ObjectName}.GREENBOOK = IQ.GREENBOOK AND {ObjectName}.GOT_CODE = IQ.GOT_CODE AND {ObjectName}.PM_ID = IQ.PM_ID AND IQ.SERVICE_ID = SAQGPE.SERVICE_ID
						JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
						JOIN SAQTRV (NOLOCK) ON SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
						JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = IQ.SERVICE_ID
						JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = IQ.SERVICE_ID 
						LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.DIVISION_ID = SAQTRV.DIVISION_ID AND MAMSCT.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER
						WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND IQ.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' 
					) OQ
					LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = OQ.SERVICE_RECORD_ID  AND SAQRIT.OBJECT_ID = OQ.OBJECT_ID AND SAQRIT.FABLOCATION_ID = OQ.FABLOCATION_ID AND SAQRIT.GREENBOOK = OQ.GREENBOOK AND SAQRIT.GOT_CODE = OQ.GOT_CODE
					WHERE ISNULL(SAQRIT.OBJECT_ID,'') = ''
				""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count,billing_type=self.get_billing_type_val, DynamicNetValues=dynamic_global_curr_columns,DynamicColumnNames=dynamic_columns))
			
			elif self.quote_service_entitlement_type == 'OFFERING+FAB+GREENBOOK+CREDIT':
				Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE,NET_VALUE_INGL_CURR, NET_PRICE_INGL_CURR,NET_PRICE,YEAR_1_INGL_CURR,YEAR_1,COMVAL_INGL_CURR,ESTVAL_INGL_CURR,COMMITTED_VALUE,ESTIMATED_VALUE, GREENBOOK,BILLING_TYPE,GREENBOOK_RECORD_ID, QTEITMSUM_RECORD_ID)
					SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified, 
						OQ.* 
					FROM (
						SELECT 
							DISTINCT
							SAQTRV.CONTRACT_VALID_FROM,
							SAQTRV.CONTRACT_VALID_TO,
							SAQTRV.DOC_CURRENCY,
							SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
							ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
							SAQTRV.EXCHANGE_RATE_DATE,
							SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
							IQ.GL_ACCOUNT_NO as GL_ACCOUNT_NO,
							SAQTRV.GLOBAL_CURRENCY,
							SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
							ROW_NUMBER()OVER(ORDER BY({ObjectName}.CpqTableEntryId)) + {EquipmentsCount} as LINE,
							null as OBJECT_ID,
							'GREENBOOK' as OBJECT_TYPE,
							null as FABLOCATION_ID,
							null as FABLOCATION_NAME,
							null as FABLOCATION_RECORD_ID,			
							{ObjectName}.SERVICE_DESCRIPTION,
							{ObjectName}.SERVICE_ID,
							{ObjectName}.SERVICE_RECORD_ID,
							null as PROFIT_CENTER,
							1 as QUANTITY,
							SAQTRV.QUOTE_ID,
							SAQTRV.QUOTE_RECORD_ID,
							SAQTMT.QTEREV_ID,
							SAQTMT.QTEREV_RECORD_ID,
							IQ.SALESORDER_NO as REF_SALESORDER,
							'ACQUIRED' AS STATUS,
							MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
							MAMSCT.TAXCLASSIFICATION_ID,
							MAMSCT.TAXCLASSIFICATION_RECORD_ID,
							SAQRIS.TAX_PERCENTAGE,
							'0' AS NET_VALUE_INGL_CURR, 
							-- CONCAT('-',IQ.CREDIT_APPLIED_INGL_CURR) AS NET_PRICE_INGL_CURR,
							-- CONCAT('-',IQ.CREDIT_APPLIED_INGL_CURR) AS NET_PRICE,
							IQ.CREDIT_APPLIED_INGL_CURR AS NET_PRICE_INGL_CURR,
							IQ.CREDIT_APPLIED_INGL_CURR AS NET_PRICE,
							IQ.CREDIT_APPLIED_INGL_CURR AS YEAR_1_INGL_CURR,
							IQ.CREDIT_APPLIED_INGL_CURR AS YEAR_1,
							'0' AS COMVAL_INGL_CURR ,
							'0' AS ESTVAL_INGL_CURR,
							'0' AS COMMITTED_VALUE,
							'0' AS ESTIMATED_VALUE,
							{ObjectName}.GREENBOOK,
							'{billing_type}' as BILLING_TYPE,
							{ObjectName}.GREENBOOK_RECORD_ID,
							SAQRIS.QUOTE_REV_ITEM_SUMMARY_RECORD_ID as QTEITMSUM_RECORD_ID
						FROM (
							SELECT 
								QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, GREENBOOK, GREENBOOK_RECORD_ID,CREDITVOUCHER_RECORD_ID,CREDIT_APPLIED_INGL_CURR,GL_ACCOUNT_NO,QUOTE_REV_CREDIT_VOUCHER_RECORD_ID,SALESORDER_NO 
							FROM SAQRCV (NOLOCK)
							WHERE SAQRCV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRCV.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRCV.SERVICE_ID = '{ServiceId}' 
							GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, GREENBOOK, GREENBOOK_RECORD_ID,CREDITVOUCHER_RECORD_ID,CREDIT_APPLIED_INGL_CURR,GL_ACCOUNT_NO,QUOTE_REV_CREDIT_VOUCHER_RECORD_ID,SALESORDER_NO
						) IQ
						JOIN {ObjectName} (NOLOCK) ON {ObjectName}.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND {ObjectName}.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND {ObjectName}.SERVICE_ID = IQ.SERVICE_ID AND {ObjectName}.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID
						JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
						JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
						JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = {ObjectName}.SERVICE_ID
						JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID 
						LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.DIVISION_ID = SAQTRV.DIVISION_ID AND MAMSCT.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER
						WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' 
					) OQ
					LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = OQ.SERVICE_RECORD_ID  AND SAQRIT.GREENBOOK_RECORD_ID = OQ.GREENBOOK_RECORD_ID
					WHERE ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ''
				""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count,billing_type=self.get_billing_type_val))
				
				
				Sql.RunQuery("""UPDATE SAQRIT 
								SET NET_VALUE_INGL_CURR = NET_PRICE_INGL_CURR + ISNULL(TAX_AMOUNT, 0),
								NET_VALUE = NET_PRICE + ISNULL(TAX_AMOUNT, 0)  
								FROM SAQRIT (NOLOCK)
									WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' """.format(QuoteRecordId=self.contract_quote_record_id ,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
				###calling script for saqris,saqtrv insert
				CallingCQIFWUDQTM = ScriptExecutor.ExecuteGlobal("CQIFWUDQTM",{"QT_REC_ID":self.contract_quote_id})	

			##ordering line field in saqrit
			self._ordering_item_line_no()

			# Item Level entitlement Insert
			if self.service_id == 'Z0101' or self.quote_service_entitlement_type in ('OFFERING+CONSIGNED+ON REQUEST','OFFERING'):
				self._service_based_quote_items_entitlement_insert(update=update)  
			elif self.quote_service_entitlement_type in ('OFFERING + PM EVENT','OFFERING + SCH. MAIN. EVENT'):
				self._pmsa_quote_items_entitlement_insert(update=update)  
			else:
				self._quote_items_entitlement_insert(update=update)
		return True		
	
	def _simple_quote_items_insert(self):
		equipments_count = 0
		item_number_inc = 0
		validate_axcliary = Sql.GetFirst("SELECT COUNT(SERVICE_ID) AS AXCLIARY_PRODUCT_FLAG from SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID='{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
		if validate_axcliary.AXCLIARY_PRODUCT_FLAG:
			quote_item_obj = Sql.GetFirst("SELECT COUNT(LINE) as LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
			equipments_count = int(quote_item_obj.LINE)
				
		#quote_line_item_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
		#quote_item_obj = Sql.GetFirst("SELECT COUNT(LINE) as LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
		#if quote_line_item_obj:
		#	if quote_line_item_obj.LINE:
		#		equipments_count = int(quote_line_item_obj.LINE) 

		doctype_obj = Sql.GetFirst("SELECT ITEM_NUMBER_INCREMENT FROM SAQTRV LEFT JOIN SADOTY ON SADOTY.DOCTYPE_ID=SAQTRV.DOCTYP_ID WHERE SAQTRV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTRV.QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
		if doctype_obj:
			item_number_inc = int(doctype_obj.ITEM_NUMBER_INCREMENT)
			
		Log.Info("SAQRIT=== 4")
		Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE, GREENBOOK, GREENBOOK_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID,NET_VALUE_INGL_CURR, NET_PRICE_INGL_CURR, QTEITMSUM_RECORD_ID) 
			SELECT
				CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
				'{UserName}' AS CPQTABLEENTRYADDEDBY,
				GETDATE() as CPQTABLEENTRYDATEADDED,
				{UserId} as CpqTableEntryModifiedBy,
				GETDATE() as CpqTableEntryDateModified,
				SAQTRV.CONTRACT_VALID_FROM,
				SAQTRV.CONTRACT_VALID_TO,
				SAQTRV.DOC_CURRENCY,
				SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
				ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
				SAQTRV.EXCHANGE_RATE_DATE,
				SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
				null as GL_ACCOUNT_NO,
				SAQTRV.GLOBAL_CURRENCY,
				SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
				ROW_NUMBER()OVER(ORDER BY(OQ.GREENBOOK)) + {EquipmentsCount} as LINE,
				null as OBJECT_ID,
				'GREENBOOK' as OBJECT_TYPE,
				OQ.SERVICE_DESCRIPTION,
				OQ.SERVICE_ID,
				OQ.SERVICE_RECORD_ID,
				null as PROFIT_CENTER,
				1 as QUANTITY,
				SAQTRV.QUOTE_ID,
				SAQTRV.QUOTE_RECORD_ID,
				SAQTMT.QTEREV_ID,
				SAQTMT.QTEREV_RECORD_ID,
				null as REF_SALESORDER,
				null as STATUS,
				MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
				MAMSCT.TAXCLASSIFICATION_ID,
				MAMSCT.TAXCLASSIFICATION_RECORD_ID,
				SAQRIS.TAX_PERCENTAGE,
				OQ.GREENBOOK,
				OQ.GREENBOOK_RECORD_ID,
				OQ.FABLOCATION_ID as FABLOCATION_ID,
				OQ.FABLOCATION_NAME as FABLOCATION_NAME,
				OQ.FABLOCATION_RECORD_ID as FABLOCATION_RECORD_ID,
				'0' AS NET_VALUE_INGL_CURR,
				'0' AS NET_PRICE_INGL_CURR,
				SAQRIS.QUOTE_REV_ITEM_SUMMARY_RECORD_ID as QTEITMSUM_RECORD_ID
			FROM (
					SELECT 
						QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERVICE_RECORD_ID, SERVICE_DESCRIPTION 
					FROM SAQSCO (NOLOCK)
					WHERE SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' 
					GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERVICE_RECORD_ID,SERVICE_DESCRIPTION
				) OQ 

			JOIN (
				SELECT DISTINCT SAQSGE.QUOTE_RECORD_ID,SAQSGE.QTEREV_RECORD_ID, SAQTSV.SERVICE_ID,SAQSGE.GREENBOOK,SAQSGE.SALESORG_RECORD_ID FROM SAQSGE (NOLOCK) INNER JOIN SAQTSV ON SAQSGE.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID  AND SAQSGE.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQSGE.SERVICE_ID = SAQTSV.PAR_SERVICE_ID 
				WHERE SAQSGE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSGE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(CONFIGURATION_STATUS, '') = 'COMPLETE' AND SAQTSV.SERVICE_ID ='{ServiceId}'
				
			) AS IQ ON IQ.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND IQ.SERVICE_ID = OQ.SERVICE_ID	AND IQ.SERVICE_ID = '{ServiceId}' AND IQ.GREENBOOK = OQ.GREENBOOK AND IQ.SERVICE_ID = '{ServiceId}'

			JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID     
			JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = IQ.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
			JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = OQ.SERVICE_ID
			JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = OQ.SERVICE_ID 
			LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.DIVISION_ID = SAQTRV.DIVISION_ID AND MAMSCT.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER
			LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = OQ.SERVICE_RECORD_ID AND ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ISNULL(OQ.GREENBOOK_RECORD_ID,'')
			WHERE OQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND OQ.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND OQ.SERVICE_ID = '{ServiceId}'  AND  ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ''""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count))
		
		##ordering line field in saqrit
		self._ordering_item_line_no()
	
	def _simple_fpm_quote_items_insert(self):
		equipments_count = 0
		Sql.RunQuery("DELETE FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID LIKE '{ServiceId}%'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
		
		quote_line_item_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
		if quote_line_item_obj:
			equipments_count = int(quote_line_item_obj.LINE)
		
		Log.Info("SAQRIT=== 5")
		Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE, GREENBOOK, GREENBOOK_RECORD_ID,NET_VALUE_INGL_CURR, NET_PRICE_INGL_CURR) 
		SELECT
			CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
			'{UserName}' AS CPQTABLEENTRYADDEDBY,
			GETDATE() as CPQTABLEENTRYDATEADDED,
			{UserId} as CpqTableEntryModifiedBy,
			GETDATE() as CpqTableEntryDateModified,
			SAQTRV.CONTRACT_VALID_FROM,
			SAQTRV.CONTRACT_VALID_TO,
			SAQTRV.DOC_CURRENCY,
			SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
			ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
			SAQTRV.EXCHANGE_RATE_DATE,
			SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
			null as GL_ACCOUNT_NO,
			SAQTRV.GLOBAL_CURRENCY,
			SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
			ROW_NUMBER()OVER(ORDER BY(SAQSPT.CpqTableEntryId)) + {EquipmentsCount} as LINE,
			null as OBJECT_ID,
			null as OBJECT_TYPE,
			SAQSPT.SERVICE_DESCRIPTION,
			SAQSPT.SERVICE_ID,
			SAQSPT.SERVICE_RECORD_ID,
			null as PROFIT_CENTER,
			1 as QUANTITY,
			SAQTRV.QUOTE_ID,
			SAQTRV.QUOTE_RECORD_ID,
			SAQTMT.QTEREV_ID,
			SAQTMT.QTEREV_RECORD_ID,
			null as REF_SALESORDER,
			null as STATUS,
			MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
			MAMSCT.TAXCLASSIFICATION_ID,
			MAMSCT.TAXCLASSIFICATION_RECORD_ID,
			SAQSPT.TAX_PERCENTAGE,
			null as GREENBOOK,
			null as GREENBOOK_RECORD_ID,
			'0' AS NET_VALUE_INGL_CURR,
			'0' AS NET_PRICE_INGL_CURR
		FROM SAQSPT (NOLOCK) 
		JOIN (
			SELECT SAQSPT.QUOTE_RECORD_ID, SAQSPT.SERVICE_ID, MAX(CpqTableEntryId) as CpqTableEntryId, CAST(ROW_NUMBER()OVER(ORDER BY SAQSPT.SERVICE_ID) + {EquipmentsCount} AS DECIMAL(5,1)) AS LINE_ITEM_ID FROM SAQSPT (NOLOCK) 
			WHERE SAQSPT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSPT.QTEREV_RECORD_ID ='{QuoteRevisionRecordId}'
			AND SAQSPT.CUSTOMER_ANNUAL_QUANTITY > 0
			GROUP BY SAQSPT.QUOTE_RECORD_ID, SAQSPT.SERVICE_ID
		) AS IQ ON IQ.CpqTableEntryId = SAQSPT.CpqTableEntryId
		JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID  AND SAQTMT.QTEREV_RECORD_ID = SAQSPT.QTEREV_RECORD_ID            
		JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQSPT.SERVICE_ID 
		JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = SAQSPT.SALESORG_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID
		LEFT JOIN MAMSCT (NOLOCK) ON SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID = MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID AND SAQTRV.COUNTRY_RECORD_ID = MAMSCT.COUNTRY_RECORD_ID AND SAQTRV.DIVISION_ID = MAMSCT.DIVISION_ID  
		LEFT JOIN MAMSOP (NOLOCK) ON MAMSOP.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER AND MAMSOP.SALESORG_ID = SAQSPT.SALESORG_ID		
		--LEFT JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQSPT.SERVICE_ID AND PRCFVA.FACTOR_ID = 'YOYDIS'
		WHERE SAQSPT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSPT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSPT.SERVICE_ID = '{ServiceId}' """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count))

		##ordering line field in saqrit
		self._ordering_item_line_no()

	def _simple_items_object_insert(self):
		Sql.RunQuery("""INSERT SAQRIO (CUSTOMER_TOOL_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, KPU, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, SERIAL_NUMBER, TECHNOLOGY, TOOL_CONFIGURATION, WAFER_SIZE, QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
				SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT DISTINCT
					SAQSCO.CUSTOMER_TOOL_ID,
					SAQSCO.EQUIPMENT_DESCRIPTION,					
					SAQSCO.EQUIPMENT_ID,
					SAQSCO.EQUIPMENT_RECORD_ID,                        
					SAQSCO.GREENBOOK, 
					SAQSCO.GREENBOOK_RECORD_ID,
					SAQSCO.KPU,
					SAQRIT.LINE as LINE,
					SAQSCO.SERVICE_DESCRIPTION, 
					SAQSCO.SERVICE_ID, 
					SAQSCO.SERVICE_RECORD_ID, 
					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
					SAQSCO.QUOTE_ID,
					SAQSCO.QUOTE_RECORD_ID,
					SAQSCO.QTEREV_ID,
					SAQSCO.QTEREV_RECORD_ID,
					SAQSCO.SERIAL_NO as SERIAL_NUMBER, 
					SAQSCO.TECHNOLOGY, 
					--PRPRBM.TOOL_CONFIGURATION,
					null as TOOL_CONFIGURATION,
					SAQSCO.WAFER_SIZE					
				FROM 
					SAQSCO (NOLOCK)					 
					JOIN (
						SELECT SAQSCE.QUOTE_RECORD_ID,SAQSCE.QTEREV_RECORD_ID, SAQTSV.SERVICE_ID,SAQSCE.EQUIPMENT_ID FROM SAQSCE (NOLOCK) INNER JOIN SAQTSV ON SAQSCE.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID  AND SAQSCE.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQSCE.SERVICE_ID = SAQTSV.PAR_SERVICE_ID 
						WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(CONFIGURATION_STATUS, '') = 'COMPLETE' AND SAQTSV.SERVICE_ID ='{ServiceId}'
						
					) AS IQ ON IQ.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQSCO.SERVICE_ID	AND IQ.EQUIPMENT_ID	 = SAQSCO.EQUIPMENT_ID	AND IQ.SERVICE_ID = '{ServiceId}'
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
					JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
					JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
											AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
											AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
											AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID
					--LEFT JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND PRPRBM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID		
					LEFT JOIN SAQRIO (NOLOCK) ON SAQRIO.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQRIO.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND SAQRIO.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID AND SAQRIO.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID AND SAQRIO.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID			
				WHERE 
					SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}'  AND ISNULL(SAQRIO.EQUIPMENT_RECORD_ID,'') = '' 
				) OQ
				""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,
				)
			)

		##update quantity in SAQRIT
		self._quote_item_qty_update()

	def _simple_quote_annualized_items_insert(self):
		Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION,STATUS,QUANTITY,OBJECT_ID,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO,LINE, QUOTE_ID, QTEITM_RECORD_ID,  QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,KPU, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY,CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,OBJECT_TYPE, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT DISTINCT					
					null as EQUIPMENT_DESCRIPTION,
					'ACQUIRED' AS STATUS,
					null as QUANTITY,
					SAQRIT.OBJECT_ID,
					null as EQUIPMENT_ID,
					null as EQUIPMENT_RECORD_ID,                        
					SAQRIT.CONTRACT_VALID_FROM,
					SAQRIT.CONTRACT_VALID_TO,
					SAQRIT.LINE,
					SAQRIT.QUOTE_ID, 
					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
					SAQRIT.QUOTE_RECORD_ID,
					SAQRIT.QTEREV_ID,
					SAQRIT.QTEREV_RECORD_ID,
					null as KPU,
					null as SERIAL_NO, 
					SAQRIT.SERVICE_DESCRIPTION, 
					SAQRIT.SERVICE_ID, 
					SAQRIT.SERVICE_RECORD_ID,								
					null as TECHNOLOGY,																			
					null as CUSTOMER_TOOL_ID, 
					null as EQUIPMENTCATEGORY_ID, 
					null as EQUIPMENTCATEGORY_RECORD_ID, 
					null as EQUIPMENT_STATUS,					
					null as MNT_PLANT_ID, 
					null as MNT_PLANT_NAME, 
					null as MNT_PLANT_RECORD_ID,					
					SAQTRV.SALESORG_ID, 
					SAQTRV.SALESORG_NAME, 
					SAQTRV.SALESORG_RECORD_ID, 
					SAQRIT.FABLOCATION_ID,
					SAQRIT.FABLOCATION_NAME,
					SAQRIT.FABLOCATION_RECORD_ID,
					SAQRIT.GREENBOOK, 
					SAQRIT.GREENBOOK_RECORD_ID, 			
					SAQTRV.GLOBAL_CURRENCY,
					SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
					SAQRIT.OBJECT_TYPE				
				FROM 
					SAQRIT (NOLOCK)					 
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID         
					JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
					LEFT JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQRIT.SERVICE_ID AND PRCFVA.FACTOR_ID = 'YOYDIS'
					LEFT JOIN (
						SELECT DATEADD(year,1,CONTRACT_VALID_FROM) as date_year,'YEAR 1' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' 
						UNION ALL  
						SELECT DATEADD(year,2,CONTRACT_VALID_FROM) as date_year,'YEAR 2' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) > 12 then 1 else 0 end )
						UNION ALL  
						SELECT DATEADD(year,3,CONTRACT_VALID_FROM) as date_year,'YEAR 3' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) > 24 then 1 else 0 end )
						UNION ALL  
						SELECT DATEADD(year,4,CONTRACT_VALID_FROM) as date_year,'YEAR 4' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) > 36  then 1 else 0 end )
						UNION ALL  
						SELECT DATEADD(year,5,CONTRACT_VALID_FROM) as date_year,'YEAR 5' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) > 48  then 1 else 0 end )
					) CONTRACT_TEMP ON  CONTRACT_TEMP.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND CONTRACT_TEMP.SERVICE_ID = SAQRIT.SERVICE_ID AND CONTRACT_TEMP.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND CONTRACT_TEMP.FABLOCATION_ID = SAQRIT.FABLOCATION_ID AND CONTRACT_TEMP.GREENBOOK = SAQRIT.GREENBOOK					
				WHERE 
					SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'
				) IQ
				
				LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = ISNULL(IQ.FABLOCATION_RECORD_ID,'') AND SAQICO.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID 
				WHERE ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = '' AND ISNULL(SAQICO.GREENBOOK_RECORD_ID,'') = ''
				""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id)
			)
	
		Sql.RunQuery("""UPDATE SAQTRV SET REVISION_STATUS = 'ACQUIRING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QTEREV_RECORD_ID}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
	def _simple_fpm_quote_annualized_items_insert(self):
		Trace.Write('FPM_ANNUALIZED_ITEM_INSERT')
		Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION,STATUS,QUANTITY,OBJECT_ID,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO,LINE, QUOTE_ID, QTEITM_RECORD_ID,  QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,KPU, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY,CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,OBJECT_TYPE, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
			SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
			SELECT DISTINCT					
				null as EQUIPMENT_DESCRIPTION,
				'ACQUIRED' AS STATUS,
				null as QUANTITY,
				SAQRIT.OBJECT_ID,
				null as EQUIPMENT_ID,
				null as EQUIPMENT_RECORD_ID,                        
				SAQRIT.CONTRACT_VALID_FROM,
				SAQRIT.CONTRACT_VALID_TO,
				SAQRIT.LINE,
				SAQRIT.QUOTE_ID, 
				SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
				SAQRIT.QUOTE_RECORD_ID,
				SAQRIT.QTEREV_ID,
				SAQRIT.QTEREV_RECORD_ID,
				null as KPU,
				null as SERIAL_NO, 
				SAQRIT.SERVICE_DESCRIPTION, 
				SAQRIT.SERVICE_ID, 
				SAQRIT.SERVICE_RECORD_ID,								
				null as TECHNOLOGY,																			
				null as CUSTOMER_TOOL_ID, 
				null as EQUIPMENTCATEGORY_ID, 
				null as EQUIPMENTCATEGORY_RECORD_ID, 
				null as EQUIPMENT_STATUS,					
				null as MNT_PLANT_ID, 
				null as MNT_PLANT_NAME, 
				null as MNT_PLANT_RECORD_ID,			
				SAQTRV.SALESORG_ID, 
				SAQTRV.SALESORG_NAME, 
				SAQTRV.SALESORG_RECORD_ID, 
				SAQRIT.FABLOCATION_ID,
				SAQRIT.FABLOCATION_NAME,
				SAQRIT.FABLOCATION_RECORD_ID,
				SAQRIT.GREENBOOK, 
				SAQRIT.GREENBOOK_RECORD_ID, 			
				SAQTRV.GLOBAL_CURRENCY,
				SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
				SAQRIT.OBJECT_TYPE				
			FROM 
				SAQRIT (NOLOCK)					 
				JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID         
				JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
				LEFT JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQRIT.SERVICE_ID AND PRCFVA.FACTOR_ID = 'YOYDIS'
				LEFT JOIN (
					SELECT DATEADD(year,1,CONTRACT_VALID_FROM) as date_year,'YEAR 1' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' 
					UNION ALL  
					SELECT DATEADD(year,2,CONTRACT_VALID_FROM) as date_year,'YEAR 2' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) > 12 then 1 else 0 end )
					UNION ALL  
					SELECT DATEADD(year,3,CONTRACT_VALID_FROM) as date_year,'YEAR 3' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) > 24 then 1 else 0 end )
					UNION ALL  
					SELECT DATEADD(year,4,CONTRACT_VALID_FROM) as date_year,'YEAR 4' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) > 36  then 1 else 0 end )
					UNION ALL  
					SELECT DATEADD(year,5,CONTRACT_VALID_FROM) as date_year,'YEAR 5' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) > 48  then 1 else 0 end )
				) CONTRACT_TEMP ON  CONTRACT_TEMP.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND CONTRACT_TEMP.SERVICE_ID = SAQRIT.SERVICE_ID AND CONTRACT_TEMP.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND CONTRACT_TEMP.FABLOCATION_ID = SAQRIT.FABLOCATION_ID AND CONTRACT_TEMP.GREENBOOK = SAQRIT.GREENBOOK					
			WHERE 
				SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'
			) IQ
			
			LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = ISNULL(IQ.FABLOCATION_RECORD_ID,'') AND SAQICO.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID 
			WHERE ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = '' AND ISNULL(SAQICO.GREENBOOK_RECORD_ID,'') = '' AND NOT EXISTS (SELECT SERVICE_ID FROM SAQICO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}')
			""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id)
		)

		Sql.RunQuery("""UPDATE SAQTRV SET REVISION_STATUS = 'ACQUIRING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
	def _insert_quote_item_forecast_parts(self):
		Trace.Write("_ent_consumable---"+str(self._ent_consumable)+"par_Service_id---"+str(self.parent_service_id) )
			
		if self.service_id == 'Z0101' and self._ent_consumable.upper() == 'SOME INCLUSIONS' : 
			Sql.RunQuery("""INSERT SAQRIP (QUOTE_REVISION_ITEM_PRODUCT_LIST_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified, PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QUANTITY, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, LINE, NEW_PART ) 
			SELECT 
				CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_PRODUCT_LIST_RECORD_ID,
				'{UserName}' AS CPQTABLEENTRYADDEDBY,
				GETDATE() as CPQTABLEENTRYDATEADDED,
				{UserId} as CpqTableEntryModifiedBy,
				GETDATE() as CpqTableEntryDateModified,
				IQ.PART_DESCRIPTION,
				IQ.PART_NUMBER,
				IQ.PART_RECORD_ID,
				SAQRIT.SERVICE_DESCRIPTION,
				SAQRIT.SERVICE_ID,
				SAQRIT.SERVICE_RECORD_ID,
				SAQRIT.QUANTITY,
				IQ.QUOTE_ID,
				SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
				SAQRIT.QUOTE_RECORD_ID,
				SAQRIT.QTEREV_ID,
				SAQRIT.QTEREV_RECORD_ID,
				SAQRIT.LINE,
				IQ.NEW_PART 
			FROM (SELECT SAQSCO.FABLOCATION_ID, SAQSCO.SERVICE_ID, SAQSCO.QUOTE_ID, SAQSCO.GREENBOOK, PART_NUMBER, PART_DESCRIPTION, 	PART_RECORD_ID,SAQRSP.QUANTITY,SAQRSP.NEW_PART,SAQRSP.QUOTE_RECORD_ID,SAQRSP.QTEREV_RECORD_ID 
				FROM SAQSCO INNER JOIN SAQRSP ON SAQSCO.QUOTE_RECORD_ID = SAQRSP.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQRSP.QTEREV_RECORD_ID AND SAQSCO.SERVICE_ID = SAQRSP.SERVICE_ID 
			WHERE SAQRSP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRSP.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRSP.SERVICE_ID = '{ServiceId}' AND SAQRSP.QUANTITY > 0 
			GROUP BY SAQSCO.FABLOCATION_ID, SAQSCO.SERVICE_ID, SAQSCO.QUOTE_ID, SAQSCO.GREENBOOK, PART_NUMBER, PART_DESCRIPTION, PART_RECORD_ID,SAQRSP.QUANTITY,SAQRSP.NEW_PART,SAQRSP.QUOTE_RECORD_ID,SAQRSP.QTEREV_RECORD_ID ) IQ 
			INNER JOIN SAQRIT ON IQ.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQRIT.GREENBOOK = IQ.GREENBOOK AND SAQRIT.FABLOCATION_ID = IQ.FABLOCATION_ID 
			LEFT JOIN SAQRIP (NOLOCK) ON SAQRIP.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQRIP.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQRIP.SERVICE_RECORD_ID = SAQRIT.SERVICE_RECORD_ID AND SAQRIP.PART_RECORD_ID = IQ.PART_RECORD_ID 
			WHERE IQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND IQ.QTEREV_RECORD_ID = '{RevisionRecordId}' AND IQ.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQRIP.PART_RECORD_ID,'') = '' """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
			
			
			##calling the iflow for pricing..
			try:
				# if action_type == 'UPDATE_LINE_ITEMS':
				Log.Info("PART PRICING IFLOW STARTED!")
				CQPARTIFLW.iflow_pricing_call(str(self.user_name),str(self.contract_quote_id),str(self.contract_quote_revision_record_id))
			except:
				Log.Info("PART PRICING IFLOW ERROR!")
		elif not (self.service_id == 'Z0100' and self._ent_consumable.upper() == 'SOME INCLUSIONS' and self.parent_service_id == 'Z0092'):
			Sql.RunQuery("""INSERT SAQRIP (QUOTE_REVISION_ITEM_PRODUCT_LIST_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified, PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QUANTITY, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, LINE, NEW_PART ) 
				SELECT 
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_PRODUCT_LIST_RECORD_ID,
					'{UserName}' AS CPQTABLEENTRYADDEDBY,
					GETDATE() as CPQTABLEENTRYDATEADDED,
					{UserId} as CpqTableEntryModifiedBy,
					GETDATE() as CpqTableEntryDateModified,
					SAQRSP.PART_DESCRIPTION,
					SAQRSP.PART_NUMBER,
					SAQRSP.PART_RECORD_ID,
					SAQRSP.SERVICE_DESCRIPTION,
					SAQRSP.SERVICE_ID,
					SAQRSP.SERVICE_RECORD_ID,
					SAQRSP.QUANTITY,
					SAQRSP.QUOTE_ID,
					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
					SAQRSP.QUOTE_RECORD_ID,
					SAQRSP.QTEREV_ID,
					SAQRSP.QTEREV_RECORD_ID,
					SAQRIT.LINE,
					SAQRSP.NEW_PART
				FROM SAQRSP (NOLOCK) 
				JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQRSP.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQRSP.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = SAQRSP.SERVICE_RECORD_ID AND SAQRIT.GREENBOOK_RECORD_ID = SAQRSP.GREENBOOK_RECORD_ID AND SAQRIT.FABLOCATION_RECORD_ID = SAQRSP.FABLOCATION_RECORD_ID 
				LEFT JOIN SAQRIP (NOLOCK) ON SAQRIP.QUOTE_RECORD_ID = SAQRSP.QUOTE_RECORD_ID AND SAQRIP.QTEREV_RECORD_ID = SAQRSP.QTEREV_RECORD_ID AND SAQRIP.SERVICE_RECORD_ID = SAQRSP.SERVICE_RECORD_ID AND SAQRIP.PART_RECORD_ID = SAQRSP.PART_RECORD_ID 

				WHERE SAQRSP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRSP.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRSP.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQRIP.PART_RECORD_ID,'') = '' """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
				
	def _insert_quote_item_fpm_forecast_parts(self):
			
		Sql.RunQuery("DELETE FROM SAQIFP WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(
					QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
		
		Sql.RunQuery("""INSERT SAQIFP (QUOTE_ITEM_FORECAST_PART_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified, PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, ANNUAL_QUANTITY, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID,BASEUOM_ID,BASEUOM_RECORD_ID,MATPRIGRP_ID,MATPRIGRP_NAME,MATPRIGRP_RECORD_ID, LINE, GLOBALCURRENCY_RECORD_ID,GLOBAL_CURRENCY,DOCURR_RECORD_ID,DOC_CURRENCY,PRICING_STATUS ) 
			SELECT 
				CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_FORECAST_PART_RECORD_ID,
				'{UserName}' AS CPQTABLEENTRYADDEDBY,
				GETDATE() as CPQTABLEENTRYDATEADDED,
				{UserId} as CpqTableEntryModifiedBy,
				GETDATE() as CpqTableEntryDateModified,
				SAQSPT.PART_DESCRIPTION,
				SAQSPT.PART_NUMBER,
				SAQSPT.PART_RECORD_ID,
				SAQSPT.SERVICE_DESCRIPTION,
				SAQSPT.SERVICE_ID,
				SAQSPT.SERVICE_RECORD_ID,
				SAQSPT.CUSTOMER_ANNUAL_QUANTITY,
				SAQSPT.QUOTE_ID,
				SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
				SAQSPT.QUOTE_RECORD_ID,
				SAQSPT.QTEREV_ID,
				SAQSPT.QTEREV_RECORD_ID,
				SAQSPT.BASEUOM_ID,
				SAQSPT.BASEUOM_RECORD_ID,
				SAQSPT.MATPRIGRP_ID,
				SAQSPT.MATPRIGRP_NAME,
				SAQSPT.MATPRIGRP_RECORD_ID,
				SAQRIT.LINE,
				SAQRIT.GLOBAL_CURRENCY_RECORD_ID,
				SAQRIT.GLOBAL_CURRENCY,
				SAQRIT.DOCURR_RECORD_ID,
				SAQRIT.DOC_CURRENCY,
				'ACQUIRING...' AS PRICING_STATUS
			FROM SAQSPT (NOLOCK) 
			JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQSPT.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = SAQSPT.SERVICE_RECORD_ID 
			LEFT JOIN SAQIFP (NOLOCK) ON SAQIFP.QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID AND SAQIFP.QTEREV_RECORD_ID = SAQSPT.QTEREV_RECORD_ID AND SAQIFP.SERVICE_RECORD_ID = SAQSPT.SERVICE_RECORD_ID AND SAQIFP.PART_RECORD_ID = SAQSPT.PART_RECORD_ID 
			WHERE SAQSPT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSPT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSPT.SERVICE_ID = '{ServiceId}' AND SAQSPT.CUSTOMER_ANNUAL_QUANTITY > 0 AND ISNULL(SAQIFP.PART_RECORD_ID,'') = '' """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		
		##calling the iflow for pricing..
		try:
			Log.Info("PART PRICING IFLOW STARTED!")
			CQPARTIFLW.iflow_pricing_call(str(self.user_name),str(self.contract_quote_id),str(self.contract_quote_revision_record_id))
		except:
			Log.Info("PART PRICING IFLOW ERROR!")

		##User story 4432 ends..
	#A055S000P01-15550 start
	def _insert_item_level_delivery_schedule(self):
		try:
			Sql.RunQuery("DELETE FROM SAQIPD WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(
						QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
			Log.Info('2089----')
			insert_item_level_delivery_schedule = "INSERT SAQIPD (QUOTE_REV_ITEM_PART_DELIVERY_RECORD_ID,DELIVERY_SCHED_CAT,DELIVERY_SCHED_DATE,LINE,PART_DESCRIPTION,PART_NUMBER,PART_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUANTITY,QUOTE_ID,QTEITMPRT_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREVSPT_RECORD_ID,QTEREV_RECORD_ID) select CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_PART_DELIVERY_RECORD_ID,DS.DELIVERY_SCHED_CAT,DS.DELIVERY_SCHED_DATE,FP.LINE,DS.PART_DESCRIPTION,DS.PART_NUMBER,DS.PART_RECORD_ID,DS.SERVICE_DESCRIPTION,DS.SERVICE_ID,DS.SERVICE_RECORD_ID,DS.QUANTITY,DS.QUOTE_ID,FP.QUOTE_ITEM_FORECAST_PART_RECORD_ID as QTEITMPRT_RECORD_ID,FP.QTEITM_RECORD_ID,FP.QUOTE_RECORD_ID,FP.QTEREV_ID,DS.QTEREVSPT_RECORD_ID,DS.QTEREV_RECORD_ID FROM SAQSPD DS JOIN SAQIFP FP ON FP.PART_RECORD_ID = DS.PART_RECORD_ID and FP.QUOTE_RECORD_ID= DS.QUOTE_RECORD_ID and FP.QTEREV_ID= DS.QTEREV_ID where FP.QUOTE_ID = '{QuoteRecordId}' and FP.QTEREV_RECORD_ID= '{rev_rec_id}'".format(QuoteRecordId=self.contract_quote_id,rev_rec_id=self.contract_quote_revision_record_id)
			Log.Info('insert_item_level_delivery_schedule==='+str(insert_item_level_delivery_schedule))
			Sql.RunQuery(insert_item_level_delivery_schedule)
		except:
			pass
	#A055S000P01-15550 end
	
	def _delete_item_related_table_records(self):
		for delete_object in ['SAQIAE','SAQICA','SAQRIO','SAQICO']:
			delete_statement = "DELETE DT FROM " +str(delete_object)+" DT (NOLOCK) JOIN SAQSCE (NOLOCK) ON DT.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND DT.SERVICE_ID=SAQSCE.SERVICE_ID AND DT.QUOTE_RECORD_ID=SAQSCE.QUOTE_RECORD_ID AND DT.QTEREV_RECORD_ID=SAQSCE.QTEREV_RECORD_ID WHERE DT.QUOTE_RECORD_ID='{}' AND DT.QTEREV_RECORD_ID='{}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS, '')='INCOMPLETE' AND DT.SERVICE_ID='{}' ".format(self.contract_quote_record_id, self.contract_quote_revision_record_id, self.service_id)
			if delete_object == "SAQICO" and self.service_id in ('Z0110','Z0108'):
				delete_statement = "DELETE DT FROM " +str(delete_object)+" DT (NOLOCK) WHERE DT.QUOTE_RECORD_ID='{}' AND DT.QTEREV_RECORD_ID='{}' AND DT.SERVICE_ID='{}' ".format(self.contract_quote_record_id, self.contract_quote_revision_record_id, self.service_id)			
			Sql.RunQuery(delete_statement)
	
		join_condition_string = ''
		if self.quote_service_entitlement_type in ('OFFERING + EQUIPMENT','OFFERING+EQUIPMENT'):
			join_condition_string = """AND ISNULL(SAQRIT.OBJECT_ID, '') = SAQSCE.EQUIPMENT_ID"""
		# item entitlement delete
		quote_item_entitlement_delete_statement = """
				DELETE SAQITE 
					FROM SAQITE (NOLOCK) 
					JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID = SAQITE.QTEITM_RECORD_ID 
					JOIN SAQSCE ON SAQSCE.QUOTE_RECORD_ID=SAQRIT.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID=SAQRIT.QTEREV_RECORD_ID AND SAQSCE.SERVICE_ID=SAQRIT.SERVICE_ID AND SAQSCE.FABLOCATION_RECORD_ID = SAQRIT.FABLOCATION_RECORD_ID AND SAQSCE.GREENBOOK_RECORD_ID = SAQRIT.GREENBOOK_RECORD_ID {JoinCondition}
					WHERE SAQITE.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQITE.QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS, '')='INCOMPLETE' AND SAQITE.SERVICE_ID='{ServiceId}' """.format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinCondition=join_condition_string)	
		Sql.RunQuery(quote_item_entitlement_delete_statement)
		# item delete
		quote_item_delete_statement = """
				DELETE SAQRIT 
					FROM SAQRIT (NOLOCK) 
					JOIN SAQSCE ON SAQSCE.QUOTE_RECORD_ID=SAQRIT.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID=SAQRIT.QTEREV_RECORD_ID AND SAQSCE.SERVICE_ID=SAQRIT.SERVICE_ID AND SAQSCE.FABLOCATION_RECORD_ID = SAQRIT.FABLOCATION_RECORD_ID AND SAQSCE.GREENBOOK_RECORD_ID = SAQRIT.GREENBOOK_RECORD_ID {JoinCondition}
					WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS, '') ='INCOMPLETE' AND SAQRIT.SERVICE_ID='{ServiceId}' """.format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinCondition=join_condition_string)	
		Sql.RunQuery(quote_item_delete_statement)

	def _delete_z0046_quote_items(self):
		if self.service_id == 'Z0046':
			deleting_tables_list = ['SAQRIT','SAQRIO','SAQITE','SAQICO']
			for obj in deleting_tables_list:
				Sql.RunQuery("DELETE {obj} FROM {obj} (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, obj = obj))

	def _service_based_quote_items_entitlement_insert(self, update=False):		
		#if update: # need to verify one more time
		Sql.RunQuery("DELETE SAQITE FROM SAQITE WHERE SAQITE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQITE.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		Sql.RunQuery("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID)
					SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified,
						{ObjectName}.CPS_CONFIGURATION_ID,
						{ObjectName}.CPS_MATCH_ID,
						null as ENTITLEMENT_COST_IMPACT,
						null as ENTITLEMENT_GROUP_ID,
						null as ENTITLEMENT_GROUP_XML,
						null as ENTITLEMENT_PRICE_IMPACT,
						{ObjectName}.ENTITLEMENT_XML,
						null as IS_CHANGED,
						SAQRIT.LINE,						
						SAQRIT.SERVICE_DESCRIPTION,
						SAQRIT.SERVICE_ID,
						SAQRIT.SERVICE_RECORD_ID,
						SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
						SAQRIT.QUOTE_ID,
						SAQRIT.QUOTE_RECORD_ID,
						SAQRIT.QTEREV_ID,
						SAQRIT.QTEREV_RECORD_ID,						
						null as GREENBOOK,
						null as GREENBOOK_RECORD_ID
					FROM {ObjectName} (NOLOCK) 
					JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID
												AND SAQRIT.SERVICE_RECORD_ID = {ObjectName}.SERVICE_RECORD_ID
												AND SAQRIT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID
															
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE'			
				""".format(UserId=self.user_id, UserName=self.user_name, ObjectName='SAQTSE', QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		return True

	def _simple_delete_item_related_table_records(self):
		for delete_object in ['SAQRIO','SAQICO']:
			delete_statement = "DELETE DT FROM " +str(delete_object)+" DT (NOLOCK) JOIN SAQSCO ON DT.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND DT.SERVICE_ID=SAQSCO.SERVICE_ID  AND DT.QUOTE_RECORD_ID=SAQSCO.QUOTE_RECORD_ID AND DT.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID JOIN SAQSCE (NOLOCK) ON DT.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND SAQSCO.PAR_SERVICE_ID=SAQSCE.SERVICE_ID AND DT.QUOTE_RECORD_ID=SAQSCE.QUOTE_RECORD_ID AND DT.QTEREV_RECORD_ID=SAQSCE.QTEREV_RECORD_ID WHERE DT.QUOTE_RECORD_ID='{}' AND DT.QTEREV_RECORD_ID='{}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS, '')='INCOMPLETE' AND DT.SERVICE_ID='{}' ".format(self.contract_quote_record_id, self.contract_quote_revision_record_id, self.service_id)			
			Sql.RunQuery(delete_statement)
		
		# item delete
		quote_item_delete_statement = """
				DELETE SAQRIT 
					FROM SAQRIT (NOLOCK) 
					JOIN SAQSCO (NOLOCK) ON SAQRIT.SERVICE_ID=SAQSCO.SERVICE_ID  AND SAQRIT.QUOTE_RECORD_ID=SAQSCO.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID=SAQRIT.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID=SAQRIT.QTEREV_RECORD_ID AND SAQSCE.SERVICE_ID=SAQSCO.PAR_SERVICE_ID AND SAQSCE.FABLOCATION_RECORD_ID = SAQRIT.FABLOCATION_RECORD_ID AND SAQSCE.GREENBOOK_RECORD_ID = SAQRIT.GREENBOOK_RECORD_ID 
					WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS, '') ='INCOMPLETE' AND SAQRIT.SERVICE_ID='{ServiceId}' """.format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id)	
		Sql.RunQuery(quote_item_delete_statement)

	def _quote_item_qty_update(self):
		if self.quote_service_entitlement_type in ("OFFERING + PM EVENT","OFFERING + SCH. MAIN. EVENT"):
			Sql.RunQuery(""" UPDATE SAQRIT SET QUANTITY = IQ.QUANTITY FROM SAQRIT (NOLOCK) INNER JOIN (SELECT DISTINCT SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,COUNT(DISTINCT SAQGPA.EQUIPMENT_ID) AS QUANTITY
								FROM SAQGPA (NOLOCK) INNER JOIN MAEQUP (NOLOCK) ON SAQGPA.ASSEMBLY_ID = MAEQUP.EQUIPMENT_ID  AND SAQGPA.FABLOCATION_ID = MAEQUP.FABLOCATION_ID AND MAEQUP.GOT_CODE = SAQGPA.GOT_CODE AND MAEQUP.PAR_EQUIPMENT_ID = SAQGPA.EQUIPMENT_ID
								WHERE SAQGPA.QUOTE_RECORD_ID= '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}'  GROUP BY SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,PM_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,TECHNOLOGY_NODE,PROCESS_TYPE ) IQ ON IQ.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQRIT.OBJECT_ID = IQ.PM_ID AND SAQRIT.FABLOCATION_ID = IQ.FABLOCATION_ID WHERE 
					SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
		else:
			Sql.RunQuery(""" UPDATE SAQRIT SET QUANTITY = IQ.QUANTITY FROM SAQRIT (NOLOCK) INNER JOIN (SELECT COUNT(*) AS QUANTITY,QTEREV_RECORD_ID, QUOTE_RECORD_ID, SERVICE_ID,GREENBOOK,LINE FROM SAQRIO (NOLOCK) WHERE 
					QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' GROUP BY QTEREV_RECORD_ID, QUOTE_RECORD_ID, SERVICE_ID,GREENBOOK,LINE ) IQ ON IQ.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQRIT.GREENBOOK = IQ.GREENBOOK AND IQ.LINE = SAQRIT.LINE WHERE 
					SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))

	def _simple_quote_items_summary_insert(self):	
		if self.quote_service_entitlement_type in ("OFFERING + PM EVENT","OFFERING + SCH. MAIN. EVENT"):
			condition_str = ' AND SAQTSE.SERVICE_ID = SAQTSV.SERVICE_ID '
		else:
			condition_str = ' AND SAQTSE.SERVICE_ID = SAQTSV.PAR_SERVICE_ID '	
		summary_last_line_no = 0
		quote_item_summary_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIS (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
		if quote_item_summary_obj:
			summary_last_line_no = int(quote_item_summary_obj.LINE) 		
		Sql.RunQuery("""INSERT SAQRIS (CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DIVISION_ID, DIVISION_RECORD_ID, DOC_CURRENCY, DOCCURR_RECORD_ID, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, PLANT_ID, PLANT_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, LINE, QUOTE_REV_ITEM_SUMMARY_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
			SELECT IQ.*, ROW_NUMBER()OVER(ORDER BY(IQ.SERVICE_ID)) + {ItemSummaryLastLineNo} as LINE, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_SUMMARY_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT DISTINCT
					SAQTRV.CONTRACT_VALID_FROM,
					SAQTRV.CONTRACT_VALID_TO,
					SAQTRV.DIVISION_ID,
					SAQTRV.DIVISION_RECORD_ID,
					SAQTRV.DOC_CURRENCY,
					SAQTRV.DOCCURR_RECORD_ID,
					SAQTRV.GLOBAL_CURRENCY,
					SAQTRV.GLOBAL_CURRENCY_RECORD_ID,						
					MAMSOP.PLANT_ID,
					MAMSOP.PLANT_RECORD_ID,
					SAQTSV.SERVICE_DESCRIPTION,
					SAQTSV.SERVICE_ID,
					SAQTSV.SERVICE_RECORD_ID,					
					1 as QUANTITY,
					SAQTRV.QUOTE_ID,
					SAQTRV.QUOTE_RECORD_ID,
					SAQTMT.QTEREV_ID,
					SAQTMT.QTEREV_RECORD_ID
				FROM SAQTSV (NOLOCK) 
				JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID  
				JOIN (
				SELECT DISTINCT SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID, SAQTSV.SERVICE_ID,SAQTSE.SALESORG_RECORD_ID FROM SAQTSE (NOLOCK) INNER JOIN SAQTSV ON SAQTSE.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID  AND SAQTSE.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID {condition_str}
				WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(CONFIGURATION_STATUS, '') = 'COMPLETE' AND SAQTSV.SERVICE_ID ='{ServiceId}'			
				) AS IQ ON IQ.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQTSV.SERVICE_ID	AND IQ.SERVICE_ID = '{ServiceId}' 
				JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = SAQTSV.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
				LEFT JOIN MAMSOP (NOLOCK) ON MAMSOP.SAP_PART_NUMBER = SAQTSV.SERVICE_ID AND MAMSOP.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSOP.DISTRIBUTIONCHANNEL_ID = SAQTRV.DISTRIBUTIONCHANNEL_ID			
				LEFT JOIN SAQRIS (NOLOCK) ON SAQRIS.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID AND SAQRIS.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQRIS.SERVICE_RECORD_ID = SAQTSV.SERVICE_RECORD_ID
				WHERE SAQTSV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSV.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQTSV.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQRIS.SERVICE_RECORD_ID,'') = '') IQ			
		""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, ItemSummaryLastLineNo=summary_last_line_no, condition_str = condition_str) 
		)
		#self.getting_cps_tax(self.service_id)
		ScriptExecutor.ExecuteGlobal('CQCPSTAXRE',{'service_id':self.service_id, 'Fun_type':'CPQ_TO_ECC'})
		return True		

	def _do_opertion(self):		
		self._set_quote_service_entitlement_type()
		self._get_consumable_val()
		Log.Info("===> _do_opertion 0000")
		if self.action_type == "INSERT_LINE_ITEMS":		
			Log.Info("===> _do_opertion 1111")	
			if self.is_spare_service == True and self.service_id in ('Z0101','Z0100'):				
				# Spare Parts Insert/Update
				self._quote_items_summary_insert()
				self._quote_items_insert()
				self._quote_items_object_insert()	
				self._quote_annualized_items_insert()
				self._insert_quote_item_forecast_parts()
			elif self.is_fpm_spare_service == True:				
				# Spare Parts Insert/Update (Z0108)...
				Log.Info("===> _do_opertion z0108 z0110 for testing")
				Log.Info("QID ==>"+str(self.contract_quote_id))
				saqspt_have_qty = Sql.GetFirst("SELECT COUNT(*) AS CNT FROM SAQSPT (NOLOCK) WHERE QUOTE_ID = '{}' AND CUSTOMER_ANNUAL_QUANTITY IS NOT NULL".format(self.contract_quote_id))
				if saqspt_have_qty.CNT>0:              
					self._quote_items_summary_insert()
					self._simple_fpm_quote_items_insert()
					self._insert_quote_item_fpm_forecast_parts()
					self._insert_item_level_delivery_schedule()
					self._simple_fpm_quote_annualized_items_insert()
					self._quote_items_fpm_entitlement_insert()
			elif self.is_simple_service == True:
				self._simple_quote_items_summary_insert()
				self._simple_quote_items_insert()
				self._simple_items_object_insert()
				self._simple_quote_annualized_items_insert()
			else:	
				if self.quote_service_entitlement_type in ("OFFERING + PM EVENT","OFFERING + SCH. MAIN. EVENT"):
					self._simple_quote_items_summary_insert()
				else:
					self._quote_items_summary_insert()
				self._quote_items_insert()		
				self._quote_items_object_insert()	
				self._quote_annualized_items_insert()	
				self._quote_item_line_entitlement_insert()
				self._quote_items_assembly_insert()
				self._quote_items_assembly_entitlement_insert()
		else:
			##deleting Z0046 SAQRIT records
			self._delete_z0046_quote_items()
			quote_revision_item_obj = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
			if not quote_revision_item_obj:
				Log.Info("===> _do_opertion 2222")
				if self.is_spare_service == True and self.service_id in ('Z0101','Z0100'):		
					# Spare Parts Insert/Update
					self._quote_items_summary_insert()
					self._quote_items_insert()
					self._quote_items_object_insert()	
					self._quote_annualized_items_insert()
					self._insert_quote_item_forecast_parts()

				##simple product quote item insert
				elif self.is_simple_service == True:
					Log.Info("===> _do_opertion 3333")
					self._simple_quote_items_summary_insert()
					self._simple_quote_items_insert()
					self._simple_items_object_insert()
					self._simple_quote_annualized_items_insert()
				elif self.is_fpm_spare_service == True:				
					# Spare Parts Insert/Update (Z0108)...
					Log.Info("===>2 _do_opertion z0108 z0110 for testing")
					saqspt_have_qty = Sql.GetFirst("SELECT COUNT(*) AS CNT FROM SAQSPT (NOLOCK) WHERE QUOTE_ID = '{}' AND CUSTOMER_ANNUAL_QUANTITY IS NOT NULL".format(self.contract_quote_id))
					if saqspt_have_qty.CNT>0:              
						self._quote_items_summary_insert()
						self._simple_fpm_quote_items_insert()
						self._insert_quote_item_fpm_forecast_parts()
						self.self._insert_item_level_delivery_schedule()
						self._simple_fpm_quote_annualized_items_insert()
						self._quote_items_fpm_entitlement_insert()
				else:
					Log.Info("===> _do_opertion 4444")
					self._quote_items_summary_insert()
					self._quote_items_insert()		
					self._quote_items_object_insert()	
					#self.cqent()
					self._quote_annualized_items_insert()
					self._quote_item_line_entitlement_insert()
					self._quote_items_assembly_insert()
					self._quote_items_assembly_entitlement_insert()
			else:
				self._delete_item_related_table_records()
				
				if self.is_spare_service == True and self.service_id in ('Z0101','Z0100'):	
					# Spare Parts Insert/Update
					self._quote_items_summary_insert()
					self._quote_items_insert()
					self._quote_items_object_insert()
					self._quote_annualized_items_insert()
					self._insert_quote_item_forecast_parts()
						
				elif self.is_simple_service == True:
					self._simple_delete_item_related_table_records()
					self._simple_quote_items_summary_insert()
					self._simple_quote_items_insert()
					self._simple_items_object_insert()
					self._simple_quote_annualized_items_insert()
				else:
					self._quote_items_summary_insert()
					self._quote_items_insert(update=True)		
					self._quote_items_object_insert(update=True)	
					self._quote_annualized_items_insert(update=True)
					self._quote_item_line_entitlement_insert(update=True)
					self._quote_items_assembly_insert(update=True)
					self._quote_items_assembly_entitlement_insert(update=True)
		
		if self.service_id == 'Z0117':
			CallingCQIFWUDQTM = ScriptExecutor.ExecuteGlobal("CQIFWUDQTM",{"QT_REC_ID":str(self.contract_quote_id),"Operation":"VOUCHER_UPDATE"})
			
		# Pricing Calculation - Start
		# quote_line_item_obj = Sql.GetFirst("SELECT LINE FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND ISNULL(STATUS,'') = ''".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		# #added condition to restrict email trigger thrice
		# if quote_line_item_obj and self.action_type == "UPDATE_LINE_ITEMS":
		# 	Log.Info("====> QTPOSTACRM called from ==> "+str(self.contract_quote_id)+'--'+str(self.service_id))
		# 	ScriptExecutor.ExecuteGlobal('QTPOSTACRM',{'QUOTE_ID':self.contract_quote_id,'REVISION_ID':self.contract_quote_revision_id, 'Fun_type':'cpq_to_sscm'})
		# 	SqlHelper.GetFirst("sp_executesql @T=N'update A SET A.STATUS = (CASE WHEN A.STATUS =''ERROR'' THEN ''ERROR'' WHEN A.STATUS =''PARTIALLY PRICED'' THEN ''ERROR'' END) from SAQRIT A inner join ( select SERVICE_ID,LINE,SAQICO.QUOTE_ID from SAQICO WHERE SAQICO.QUOTE_ID = ''"+str(self.contract_quote_id)+"'' group by SERVICE_ID,LINE,SAQICO.QUOTE_ID Having count(*) > 1 ) as od on od.LINE = A.LINE AND od.SERVICE_ID = A.SERVICE_ID '")
		# 	SqlHelper.GetFirst("sp_executesql @T=N'update A SET A.STATUS = (CASE WHEN A.STATUS =''ACQUIRING'' THEN ''ACQUIRING'' WHEN A.STATUS =''ERROR'' THEN ''ERROR'' END) from SAQRIT A inner join ( select SERVICE_ID,LINE,SAQICO.QUOTE_ID from SAQICO WHERE SAQICO.QUOTE_ID = ''"+str(self.contract_quote_id)+"'' group by SERVICE_ID,LINE,SAQICO.QUOTE_ID Having count(*) > 1 ) as od on od.LINE = A.LINE AND od.SERVICE_ID = A.SERVICE_ID '")
		# 	SqlHelper.GetFirst("sp_executesql @T=N'update A SET A.STATUS = (CASE WHEN A.STATUS =''ACQUIRING'' THEN ''PARTIALLY PRICING'' WHEN A.STATUS =''PARTIALLY PRICING'' THEN ''PARTIALLY PRICING'' END) from SAQRIT A inner join ( select SERVICE_ID,LINE,SAQICO.QUOTE_ID from SAQICO WHERE SAQICO.QUOTE_ID = ''"+str(self.contract_quote_id)+"'' group by SERVICE_ID,LINE,SAQICO.QUOTE_ID Having count(*) > 1 ) as od on od.LINE = A.LINE AND od.SERVICE_ID = A.SERVICE_ID '")
		# Pricing Calculation - End
		return True

try:
	where_condition_string = Param.WhereString
except:
	where_condition_string = ''
action_type = Param.ActionType
try:
	entitlement_level_obj = Param.EntitlementLevel
except:
	entitlement_level_obj = "SAQTSE"
parameters = {}
keysofparameters = {
	"QUOTE_RECORD_ID" : "contract_quote_record_id",
	"QTEREV_RECORD_ID" : "contract_quote_revision_record_id",
	"SERVICE_ID" : "service_id",
	"GREENBOOK" : "greenbook_id",
	"FABLOCATION_ID" : "fablocation_id",
	"EQUIPMENT_ID" : "equipment_id",
}
parameters['action_type']=str(action_type)
parameters['entitlement_level_obj'] = str(entitlement_level_obj)
if where_condition_string:
	parameters['where_condition_string'] = str(where_condition_string)
if action_type == "UPDATE_LINE_ITEMS":
	for key in keysofparameters.keys():
		if str(key) in where_condition_string:
			pattern = re.compile(r''+str(key)+'\s*\=\s*\'([^>]*?)\'')
			result = re.search(pattern, where_condition_string).group(1)
			parameters[keysofparameters[key]]=str(result)	
else:
	parameters[keysofparameters['QUOTE_RECORD_ID']]=str(Param.ContractQuoteRecordId)
	parameters[keysofparameters['QTEREV_RECORD_ID']]=str(Param.ContractQuoteRevisionRecordId)
	parameters[keysofparameters['SERVICE_ID']]=str(Param.ServiceId)
	
contract_quote_item_obj = ContractQuoteItem(**parameters)
contract_quote_item_obj._do_opertion()