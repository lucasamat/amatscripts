# =========================================================================================================================================
#   __script_name : CQVLDPRDEF.PY
#   __script_description : THIS SCRIPT IS USED FOR PREDEFINED VALUES IN VALUE DRIVER (GETS TRIGGERED AFTER IFLOW SCRIPT - CQTVLDRIFW.py)
#   __primary_author__ : 
#   __create_date :06-09-2021
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
import re
from SYDATABASE import SQL

Sql = SQL()

try:
    quote_record_id = Param.quote_rec_id
except:
    quote_record_id = ""	
try:
    get_selected_value = dict(Param.get_selected_value)
    Trace.Write('get_selected_value--try--'+str(get_selected_value))
except:
    get_selected_value = ""
    Trace.Write('get_selected_value--try--except--')
try:
    LEVEL = Param.level
except:
    LEVEL = ""
try:
    TreeParam = Param.treeparam
    
except: 
    TreeParam = ""
try:
    quote_revision_record_id = Param.quote_rev_id
except:
    quote_revision_record_id = ""
try:
    where_condition =  Param.where_condition
except:
    where_condition =  ""	
try:
    uptime_list = list(Param.uptime_list)
except:
    uptime_list = ""
try:
    get_ent_type_val = Param.get_ent_type_val
except:
    get_ent_type_val = ""
try:
    serviceId =Param.serviceId
except:
    serviceId = ""

def equipment_predefined():	
    get_valuedriver_ids = Sql.GetList("SELECT PRENTL.ENTITLEMENT_ID,PRENTL.ENTITLEMENT_DESCRIPTION from PRENTL (NOLOCK)  WHERE SERVICE_ID = '{}' AND ENTITLEMENT_TYPE ='VALUE DRIVER'   ".format(TreeParam) )
    getall_recid = Sql.GetList(""" SELECT EQUIPMENT_ID,ENTITLEMENT_XML,GREENBOOK_RECORD_ID,FABLOCATION_RECORD_ID FROM SAQSCE (NOLOCK) {}""".format(str(where_condition) ))
    QueryResult = ""
    QueryResult += "begin transaction;"
    for rec in getall_recid:
        entxmldict = {}
        pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
        pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')
        entitlement_display_value_tag_pattern = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
        display_val_dict = {}
        updateentXML = rec.ENTITLEMENT_XML
        for m in re.finditer(pattern_tag, updateentXML):
            sub_string = m.group(1)
            x=re.findall(pattern_name,sub_string)
            if x:
                entitlement_display_value_tag_match = re.findall(entitlement_display_value_tag_pattern,sub_string)
                if entitlement_display_value_tag_match:
                    display_val_dict[x[0]] = entitlement_display_value_tag_match[0].upper()
            entxmldict[x[0]]=sub_string
        for val in get_valuedriver_ids:
            Trace.Write("vallls"+str(val.ENTITLEMENT_ID.upper()))
            if 'WAFER NODE' in val.ENTITLEMENT_DESCRIPTION.upper():
                get_val = Sql.GetFirst(""" SELECT M.VALDRV_WAFERNODE as VALDRV_WAFERNODE FROM MAEQUP (NOLOCK) M WHERE M.EQUIPMENT_ID='{}' """.format(str(rec.EQUIPMENT_ID)))
                if get_val:
                    updateentXML = updating_xml(entxmldict,updateentXML,val.ENTITLEMENT_ID,get_val.VALDRV_WAFERNODE,TreeParam)
            elif 'DEVICE TYPE' in val.ENTITLEMENT_DESCRIPTION.upper():
                get_val = Sql.GetFirst(""" SELECT M.VALDRV_DEVICETYPE as VALDRV_DEVICETYPE FROM MAEQUP (NOLOCK) M WHERE M.EQUIPMENT_ID='{}' """.format(str(rec.EQUIPMENT_ID)))
                if get_val:
                    updateentXML = updating_xml(entxmldict,updateentXML,val.ENTITLEMENT_ID,get_val.VALDRV_DEVICETYPE,TreeParam)
            elif  val.ENTITLEMENT_DESCRIPTION.upper() in ('CONTRACT COVERAGE & RESPONSE TIME','CONTRACT COVERAGE & RESP TIME'):		
                response_time = ""
                coverage_time = ""
                if "AGS_"+str(TreeParam)+"_CVR_CNTCOV" in display_val_dict.keys():
                    coverage_time = display_val_dict["AGS_"+str(TreeParam)+"_CVR_CNTCOV"]
                if "AGS_"+str(TreeParam)+"_CVR_RSPTIM" in display_val_dict.keys():
                    response_time = display_val_dict["AGS_"+str(TreeParam)+"_CVR_RSPTIM"]
                if coverage_time and response_time:
                    #COVERAGE 7X12 / RESPONSE 8
                    ent_value = "COVERAGE {} / RESPONSE {}".format(coverage_time.replace("X","x"),response_time.split(' ')[0] )
                    if ent_value:
                        Trace.Write("inside11")
                        updateentXML = updating_xml(entxmldict,updateentXML,val.ENTITLEMENT_ID,ent_value,TreeParam)
                    Trace.Write("contract cov-"+str(coverage_time)+'---'+str(response_time)+'--'+str(ent_value))
            elif val.ENTITLEMENT_ID in ('AGS_{}_VAL_CTFNBB'.format(TreeParam),'AGS_{}_VAL_TLSFAB'.format(TreeParam)):
                try:
                    #AGS_Z0010_VAL_CTFNBB
                    Trace.Write("csa")
                    ent_value = ""
                    account_id_query = Sql.GetFirst("SELECT BLUEBOOK FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(quote_record_id,quote_revision_record_id ))
                    # account_id_query = Sql.GetFirst("SELECT ACCOUNT_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(quote_record_id)+"'")
                    # account_bluebook_query = Sql.GetFirst("SELECT BLUEBOOK FROM SAACNT (NOLOCK) WHERE ACCOUNT_ID = '"+str(account_id_query.ACCOUNT_ID)+"'")
                    tools_count_query = Sql.GetFirst("SELECT COUNT(EQUIPMENT_ID) AS COUNT FROM SAQSCO (NOLOCK) {} ".format(where_condition))
                    if account_id_query.BLUEBOOK != "DES" and val.ENTITLEMENT_ID == 'AGS_{}_VAL_CTFNBB'.format(TreeParam):
                        if tools_count_query.COUNT < 10:
                            ent_value = '<10'
                        elif tools_count_query.COUNT in range(10,51):
                            ent_value = '>10 to <=50'
                        elif tools_count_query.COUNT > 50:
                            ent_value = '>50'
                    elif account_id_query.BLUEBOOK == "DES" and val.ENTITLEMENT_ID == 'AGS_{}_VAL_TLSFAB'.format(TreeParam):
                        if tools_count_query.COUNT > 7:
                            ent_value = '>7'
                        elif tools_count_query.COUNT in range(3,8):
                            ent_value = '>=3 to <=7'
                        elif tools_count_query.COUNT < 3:
                            ent_value = '<3'
                    if ent_value:
                        updateentXML = updating_xml(entxmldict,updateentXML,val.ENTITLEMENT_ID,ent_value,TreeParam)
                except Exception as e:
                    Log.Info("equipment--"+str(e))
        ##total seed coefficent update
        # try:
        # 	Trace.Write("try"+str(TreeParam))
        # 	ent_value = ''
        # 	#ent_code = '001' 
        # 	entitlement_id = 'AGS_{}_VAL_TBCOST'.format(TreeParam)
        # 	if entitlement_id in updateentXML:
        # 		Trace.Write("try")
        # 		get_value_qry = Sql.GetFirst("SELECT ENTITLEMENT_DISPLAY_VALUE FROM PRENVL WHERE ENTITLEMENT_ID ='{}' AND SERVICE_ID ='{} ' ".format(entitlement_id,TreeParam))
        # 		if get_value_qry:
        # 			if get_value_qry.ENTITLEMENT_DISPLAY_VALUE:
        # 				ent_value = get_value_qry.ENTITLEMENT_DISPLAY_VALUE
        # 				updateentXML = updating_xml(entxmldict,updateentXML,entitlement_id,ent_value,TreeParam)
        # except Exception as e:
        # 	Trace.Write("exceptt"+str(e))
        # 	pass
        for roll_obj in ['SAQSCE','SAQSAE']:
            QueryResult += "UPDATE {} SET ENTITLEMENT_XML = '{}' {} AND FABLOCATION_RECORD_ID = '{}' AND GREENBOOK_RECORD_ID ='{}' AND EQUIPMENT_ID ='{}' ;".format(roll_obj, updateentXML.replace("'","''") ,where_condition,rec.FABLOCATION_RECORD_ID, rec.GREENBOOK_RECORD_ID, rec.EQUIPMENT_ID)
    QueryResult += "commit;"
    Sql.RunQuery(QueryResult)
    #Product.SetGlobal("QueryResult-equp-",QueryResult)
    
def greenbook_predefined():
    getxml_query = Sql.GetList(""" SELECT GREENBOOK,ENTITLEMENT_XML,GREENBOOK_RECORD_ID FROM SAQSGE (NOLOCK) {}""".format(str(where_condition)))	
    #get_valuedriver_ids = Sql.GetList("SELECT PRENTL.ENTITLEMENT_ID,PRENTL.ENTITLEMENT_DESCRIPTION from PRENTL (NOLOCK) INNER JOIN PRENLI (NOLOCK) ON PRENTL.ENTITLEMENT_ID = PRENLI.ENTITLEMENT_ID WHERE SERVICE_ID = '{}' AND ENTITLEMENT_TYPE ='VALUE DRIVER' AND PRENLI.ENTITLEMENTLEVEL_NAME = 'OFFERING FAB GREENBOOK LEVEL' AND PRENTL.ENTITLEMENT_ID NOT IN (SELECT ENTITLEMENT_ID from PRENLI (NOLOCK) WHERE ENTITLEMENTLEVEL_NAME IN ('OFFERING FAB LEVEL','OFFERING LEVEL')) ".format(TreeParam) )
    QueryResult = ""
    QueryResult += "begin transaction;"
    for rec in getxml_query:
        entxmldict = {}
        pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
        pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')
        updateentXML = rec.ENTITLEMENT_XML
        for m in re.finditer(pattern_tag, updateentXML):
            sub_string = m.group(1)
            x=re.findall(pattern_name,sub_string)
            entxmldict[x[0]]=sub_string
        #for val in get_valuedriver_ids:
        #if 'GREENBOOK' in val.ENTITLEMENT_DESCRIPTION.upper():
        ent_value = rec.GREENBOOK
        updateentXML = updating_xml(entxmldict,updateentXML,"AGS_{}_VAL_GRNBKV".format(TreeParam),ent_value,TreeParam)
        
        ##total seed coefficent update
        # try:
        # 	Trace.Write("try"+str(TreeParam))
        # 	ent_value = ''
        # 	#ent_code = '001' 
        # 	entitlement_id = 'AGS_{}_VAL_TBCOST'.format(TreeParam)
        # 	if entitlement_id in updateentXML:
        # 		Trace.Write("try")
        # 		get_value_qry = Sql.GetFirst("SELECT ENTITLEMENT_DISPLAY_VALUE FROM PRENVL WHERE ENTITLEMENT_ID ='{}' AND SERVICE_ID ='{} ' ".format(entitlement_id,TreeParam))
        # 		if get_value_qry:
        # 			if get_value_qry.ENTITLEMENT_DISPLAY_VALUE:
        # 				ent_value = get_value_qry.ENTITLEMENT_DISPLAY_VALUE
        # 				updateentXML = updating_xml(entxmldict,updateentXML,entitlement_id,ent_value,TreeParam)
        # except Exception as e:
        # 	Trace.Write("exceptt"+str(e))
        # 	pass		
        #Sql.RunQuery( "UPDATE SAQSGE SET ENTITLEMENT_XML = '{}' {} AND FABLOCATION_RECORD_ID = '{}' AND GREENBOOK_RECORD_ID ='{}'".format(updateentXML.replace("'","''") ,where_condition,rec.FABLOCATION_RECORD_ID, rec.GREENBOOK_RECORD_ID   ) )
        ##rolldown
        for roll_obj in ['SAQSGE','SAQSCE','SAQSAE']:
            QueryResult += "UPDATE {} SET ENTITLEMENT_XML = '{}' {}  AND GREENBOOK_RECORD_ID ='{}'; ".format(roll_obj, updateentXML.replace("'","''") ,where_condition, rec.GREENBOOK_RECORD_ID)
    QueryResult += "commit;"
    Sql.RunQuery(QueryResult)

# def fab_predefined():
# 	getxml_query = Sql.GetList("""SELECT ENTITLEMENT_XML,FABLOCATION_RECORD_ID FROM SAQSFE {}""".format(str(where_condition) ))
    
# 	get_valuedriver_ids = Sql.GetList("SELECT PRENTL.ENTITLEMENT_ID,PRENTL.ENTITLEMENT_DESCRIPTION from PRENTL (NOLOCK) INNER JOIN PRENLI (NOLOCK) ON PRENTL.ENTITLEMENT_ID = PRENLI.ENTITLEMENT_ID WHERE SERVICE_ID = '{}' AND ENTITLEMENT_TYPE ='VALUE DRIVER' AND PRENLI.ENTITLEMENTLEVEL_NAME = 'OFFERING FAB LEVEL' AND PRENTL.ENTITLEMENT_ID NOT IN (SELECT ENTITLEMENT_ID from PRENLI (NOLOCK) WHERE ENTITLEMENTLEVEL_NAME IN ('OFFERING LEVEL')) ".format(TreeParam) )
# 	for rec in getxml_query:
# 		entxmldict = {}
# 		pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
# 		pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')
# 		updateentXML = rec.ENTITLEMENT_XML
# 		#Log.Info('updateentXML---'+str(updateentXML))
# 		for m in re.finditer(pattern_tag, updateentXML):
# 			sub_string = m.group(1)
# 			#Log.Info('sub_string---'+str(sub_string))
# 			x=re.findall(pattern_name,sub_string)
# 			#Log.Info('x---'+str(x))
# 			entxmldict[x[0]]=sub_string
# 		for val in get_valuedriver_ids:
# 			if 'CSA TOOLS PER FAB' in val.ENTITLEMENT_DESCRIPTION.upper():
# 				ent_value = ""
# 				account_id_query = Sql.GetFirst("SELECT ACCOUNT_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(quote_record_id)+"'")
# 				account_bluebook_query = Sql.GetFirst("SELECT BLUEBOOK FROM SAACNT (NOLOCK) WHERE ACCOUNT_ID = '"+str(account_id_query.ACCOUNT_ID)+"'")
# 				tools_count_query = Sql.GetFirst("SELECT COUNT(GREENBOOK) AS COUNT FROM SAQSCO (NOLOCK) {} AND FABLOCATION_RECORD_ID = '{}' GROUP BY FABLOCATION_NAME".format(where_condition, rec.FABLOCATION_RECORD_ID))
# 				if account_bluebook_query.BLUEBOOK != "DISPLAY":
# 					if tools_count_query.COUNT > 50:
# 						ent_value = '# CSA tools in Fab_>50'
# 					elif tools_count_query.COUNT in range(10,51):
# 						ent_value = '# CSA tools in Fab_10-50'
# 					elif tools_count_query.COUNT < 10:
# 						ent_value = '# CSA tools in Fab_<10'
# 				elif account_bluebook_query.BLUEBOOK == "DISPLAY":
# 					if tools_count_query.COUNT > 7:
# 						ent_value = '# CSA tools in Fab_<7'
# 					elif tools_count_query.COUNT in range(3,8):
# 						ent_value = '# CSA tools in Fab_3-7'
# 					elif tools_count_query.COUNT < 3:
# 						ent_value = '# CSA tools in Fab_<3'
# 				if ent_value:
# 					updateentXML = updating_xml(entxmldict,updateentXML,val.ENTITLEMENT_ID,ent_value)
        
# 		#Sql.RunQuery( "UPDATE SAQSGE SET ENTITLEMENT_XML = '{}' {} AND FABLOCATION_RECORD_ID = '{}' AND GREENBOOK_RECORD_ID ='{}'".format(updateentXML.replace("'","''") ,where_condition,rec.FABLOCATION_RECORD_ID, rec.GREENBOOK_RECORD_ID   ) )

# 		##rolldown
# 		for roll_obj in ['SAQSGE','SAQSCE','SAQSAE']:
# 			Sql.RunQuery( "UPDATE {} SET ENTITLEMENT_XML = '{}' {} AND FABLOCATION_RECORD_ID = '{}' ".format(roll_obj, updateentXML.replace("'","''") ,where_condition,rec.FABLOCATION_RECORD_ID   ) )
            

##service level
def service_level_predefined(): 
    getxml_query = Sql.GetFirst(""" SELECT ENTITLEMENT_XML FROM SAQTSE (NOLOCK) {} """.format(str(where_condition)))
    entxmldict = {}
    pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
    pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')
    updateentXML = getxml_query.ENTITLEMENT_XML
    for m in re.finditer(pattern_tag, updateentXML):
        sub_string = m.group(1)
        #Log.Info('sub_string---'+str(sub_string))
        x=re.findall(pattern_name,sub_string)
        #Log.Info('x---'+str(x))
        entxmldict[x[0]]=sub_string

    get_valuedriver_ids = Sql.GetList("SELECT PRENTL.ENTITLEMENT_ID,PRENTL.ENTITLEMENT_DESCRIPTION from PRENTL (NOLOCK) WHERE SERVICE_ID = '{service_id}' AND ENTITLEMENT_TYPE = 'VALUE DRIVER' AND PRENTL.ENTITLEMENT_ID IN ('AGS_{service_id}_VAL_POFFER','AGS_{service_id}_VAL_INTCPT','AGS_{service_id}_VAL_CSTSEG') ".format(service_id = TreeParam))

    for val in get_valuedriver_ids:
        if 'PRODUCT OFFERING' in val.ENTITLEMENT_DESCRIPTION.upper() or 'INTERCEPT' in val.ENTITLEMENT_DESCRIPTION.upper():
            ent_value = ""
            updateentXML = updating_xml(entxmldict,updateentXML,val.ENTITLEMENT_ID,ent_value,TreeParam )
        elif 'CUSTOMER SEGMENT' in val.ENTITLEMENT_DESCRIPTION.upper():
            try:
                get_customer_segment =Sql.GetFirst("SELECT CUSTOMER_SEGMENT FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID='{}' AND CPQ_PARTNER_FUNCTION = 'SOLD TO' ".format(quote_record_id,quote_revision_record_id))
                
            except:
                get_customer_segment =''
            if get_customer_segment :
                updateentXML = updating_xml(entxmldict,updateentXML,val.ENTITLEMENT_ID,get_customer_segment.CUSTOMER_SEGMENT,TreeParam)
    #Product.SetGlobal("updateentXML",updateentXML)
    Sql.RunQuery( "UPDATE SAQTSE SET ENTITLEMENT_XML = '{}' WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID='{}'".format(updateentXML.replace("'","''") , quote_record_id,TreeParam, quote_revision_record_id) )
    ##rolldown
    # for roll_obj in ['SAQSFE','SAQSGE','SAQSCE','SAQSAE']:
    # 	Sql.RunQuery( "UPDATE {} SET ENTITLEMENT_XML = '{}' {} ".format(roll_obj, updateentXML.replace("'","''") ,where_condition   ) )
        
def updating_xml(entxmldict, input_xml, ent_id, ent_value,service_id):	
    where =""
    check_valuedriver = Sql.GetFirst("SELECT count(*) as cnt FROM PREGBV (NOLOCK) WHERE ENTITLEMENT_ID = '{}' AND PREGBV.ACTIVE = 1".format(ent_id) )
    if ent_value and check_valuedriver.cnt > 0:
        get_value_code = Sql.GetFirst("SELECT ENTITLEMENT_VALUE_CODE FROM PREGBV (NOLOCK) WHERE ENTITLEMENT_ID ='{}' AND SERVICE_ID = '{}' AND ENTITLEMENT_DISPLAY_VALUE = '{}'".format(ent_id, service_id, ent_value) )
        value_ent_code = ''
        if get_value_code:
            if get_value_code.ENTITLEMENT_VALUE_CODE:
                value_ent_code = get_value_code.ENTITLEMENT_VALUE_CODE
        entitlement_string = entxmldict[ent_id]
        entitlement_string = re.sub('<ENTITLEMENT_DISPLAY_VALUE>[^>]*?</ENTITLEMENT_DISPLAY_VALUE>','<ENTITLEMENT_DISPLAY_VALUE>'+str(ent_value.replace("'","''").replace("&",";#38").replace(">","&gt;").replace("<","&lt;"))+'</ENTITLEMENT_DISPLAY_VALUE>',entitlement_string)
        entitlement_string = re.sub('<ENTITLEMENT_VALUE_CODE>[^>]*?</ENTITLEMENT_VALUE_CODE>','<ENTITLEMENT_VALUE_CODE>'+str(value_ent_code)+'</ENTITLEMENT_VALUE_CODE>',entitlement_string)
        where = " AND PRENVL.ENTITLEMENT_DISPLAY_VALUE = '{}'".format(ent_value)
        input_xml = re.sub(r'<QUOTE_ITEM_ENTITLEMENT>\s*<ENTITLEMENT_ID>'+str(ent_id)+'[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>', entitlement_string, input_xml )
        Trace.Write("input_xml--"+str(input_xml))
        # re.sub(r'<ENTITLEMENT_ID>'+str(ent_id)+'<[\w\W]*?</CALCULATION_FACTOR>', entitlement_string, input_xml )
        #Log.Info("EID11->{}, {} ".format(str(ent_id),str(entitlement_string)) )

    # get_coefficient_val = Sql.GetFirst("SELECT ENTITLEMENT_COEFFICIENT, PRENTL.ENTITLEMENT_ID FROM PRENVL (NOLOCK) INNER JOIN PRENTL (NOLOCK) ON PAR_ENPAR_ENTITLEMENT_ID = PRENVL.ENTITLEMENT_ID AND PRENVL.SERVICE_ID = PRENTL.SERVICE_ID WHERE PRENVL.ENTITLEMENT_ID = '{}' AND PRENVL.SERVICE_ID = '{}' {}".format(ent_id, service_id, where))
    # if get_coefficient_val.ENTITLEMENT_ID in entxmldict.keys():
    # 	entitlement_string2 = entxmldict[get_coefficient_val.ENTITLEMENT_ID]
    # 	entitlement_string2 = re.sub('<ENTITLEMENT_DISPLAY_VALUE>[^>]*?</ENTITLEMENT_DISPLAY_VALUE>','<ENTITLEMENT_DISPLAY_VALUE>'+str(get_coefficient_val.ENTITLEMENT_COEFFICIENT)+'</ENTITLEMENT_DISPLAY_VALUE>',entitlement_string2)

    # 	entitlement_string2 = re.sub('<ENTITLEMENT_VALUE_CODE>[^>]*?</ENTITLEMENT_VALUE_CODE>','<ENTITLEMENT_VALUE_CODE>'+str(get_coefficient_val.ENTITLEMENT_COEFFICIENT)+'</ENTITLEMENT_VALUE_CODE>',entitlement_string2)
    # 	input_xml = re.sub(r'<QUOTE_ITEM_ENTITLEMENT>\s*<ENTITLEMENT_ID>'+str(get_coefficient_val.ENTITLEMENT_ID)+'[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>', entitlement_string2, input_xml )
        #Log.Info("EID->{}, {} ".format(str(ent_id),str(entitlement_string2)) )
    return input_xml

def valuedriver_onchage():
    Trace.Write("onchange")
    entxmldict = {}	
    querystring =''
    uptime=''	
    entitlement_display_value_tag_pattern = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
    display_val_dict = {}
    getxml_query = Sql.GetFirst(""" SELECT ENTITLEMENT_XML FROM {objname} (NOLOCK) {where}""".format(objname=TreeParam,where=str(where_condition)))
    updateentXML =''
    #for rec in getxml_query:
    if getxml_query:
        if getxml_query.ENTITLEMENT_XML:
            updateentXML = getxml_query.ENTITLEMENT_XML
            pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
            pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')
            for m in re.finditer(pattern_tag, updateentXML):
                sub_string = m.group(1)
                x=re.findall(pattern_name,sub_string)
                if x:
                    entitlement_display_value_tag_match = re.findall(entitlement_display_value_tag_pattern,sub_string)
                    if entitlement_display_value_tag_match:
                        display_val_dict[x[0]] = entitlement_display_value_tag_match[0].upper()
                entxmldict[x[0]]=sub_string
    #if str(get_ent_type_val).upper() in ["VALUE DRIVER","VALUE DRIVER COEFFICIENT"]:
    obj =re.match(r".*SERVICE_ID\s*\=\s*\'([^>]*?)\'",where_condition)
    dynamic_service = obj.group(1)
    try:
        
        if uptime_list:
            base_percent = uptime_list[0]
            target_percent = uptime_list[1]
            uptime_key = uptime_list[2]
            uptime_coeff = uptime_list[3]
            obj =re.match(r".*SERVICE_ID\s*\=\s*\'([^>]*?)\'",where_condition)
            dynamic_service = obj.group(1)
            check_valuedriver = Sql.GetFirst("SELECT count(*) as cnt FROM PREGBV (NOLOCK) WHERE ENTITLEMENT_ID = '{}' AND PREGBV.ACTIVE = 1".format(uptime_key) )
            if base_percent and target_percent in entxmldict.keys() and check_valuedriver.cnt > 0:
                base= entxmldict[base_percent]
                base_price=re.search(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>',base)
                base_price_value =str(base_price.group(1))
                target= entxmldict[target_percent]
                target_price=re.search(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>',target)
                target_price_value=str(target_price.group(1))
                uptime=float(target_price_value)-float(base_price_value)
                # if uptime >= 10:
                # 	uptime = 10
                if uptime == 0:
                    uptime = '0%'
                elif uptime > 0 and uptime <= 1:
                    uptime = '> 0% AND <=1%'
                elif uptime > 1 and uptime <= 2:
                    uptime = '> 1% AND <=2%'
                elif uptime > 2:
                    uptime = '> 2%'
                update=Sql.GetFirst("Select ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_VALUE_CODE FROM PREGBV (NOLOCK) WHERE ENTITLEMENT_DISPLAY_VALUE = '{uptime}' AND ENTITLEMENT_ID = '{uptime_key}' AND SERVICE_ID = '{dynamic_service}'".format(uptime=uptime,dynamic_service=dynamic_service, uptime_key =uptime_key))
                for key in entxmldict.keys():
                    # if uptime_coeff == key:
                    # 	entxmldict[uptime_coeff] = re.sub('<ENTITLEMENT_DISPLAY_VALUE>[^>]*?</ENTITLEMENT_DISPLAY_VALUE>','<ENTITLEMENT_DISPLAY_VALUE>'+str(update.ENTITLEMENT_COEFFICIENT)+'</ENTITLEMENT_DISPLAY_VALUE>',entxmldict[uptime_coeff])
                    # 	entxmldict[uptime_coeff] = re.sub('<ENTITLEMENT_VALUE_CODE>[^>]*?</ENTITLEMENT_VALUE_CODE>','<ENTITLEMENT_VALUE_CODE>'+str(update.ENTITLEMENT_COEFFICIENT)+'</ENTITLEMENT_VALUE_CODE>',entxmldict[uptime_coeff])
                    # 	querystring = querystring + entxmldict[uptime_coeff]
                    if uptime_key == key:
                        Trace.Write("value--"+str(update.ENTITLEMENT_DISPLAY_VALUE))
                        entxmldict[uptime_key] = re.sub('<ENTITLEMENT_DISPLAY_VALUE>[^>]*?</ENTITLEMENT_DISPLAY_VALUE>','<ENTITLEMENT_DISPLAY_VALUE>'+str(update.ENTITLEMENT_DISPLAY_VALUE).replace("'","''").replace("&",";#38").replace(">","&gt;").replace("<","&lt;")+'</ENTITLEMENT_DISPLAY_VALUE>',entxmldict[uptime_key])
                        entxmldict[uptime_key] = re.sub('<ENTITLEMENT_VALUE_CODE>[^>]*?</ENTITLEMENT_VALUE_CODE>','<ENTITLEMENT_VALUE_CODE>'+str(update.ENTITLEMENT_VALUE_CODE)+'</ENTITLEMENT_VALUE_CODE>',entxmldict[uptime_key])
                        querystring = querystring + entxmldict[uptime_key]
                    else:
                        querystring = querystring + entxmldict[key]
                updateentXML = querystring
                Update_xml_uptime = ("UPDATE {TreeParam} SET ENTITLEMENT_XML = '{querystring}' {where_condition}".format(TreeParam=TreeParam,querystring=querystring,where_condition=where_condition))
                Sql.RunQuery(Update_xml_uptime)
    except Exception as e:
        Log.Info('323--error--'+str(e))
    ##contract & covergae onchange update
    try:
        check_valuedriver = Sql.GetFirst("SELECT count(*) as cnt FROM PREGBV (NOLOCK) WHERE ENTITLEMENT_ID = '{}' AND PREGBV.ACTIVE = 1".format(uptime_key) )
        if updateentXML and check_valuedriver.cnt > 0:
            ent_id = "AGS_"+str(dynamic_service)+"_VAL_CCRTME"
            response_time = ""
            coverage_time = ""
            
            if "AGS_"+str(dynamic_service)+"_CVR_CNTCOV" in display_val_dict.keys():
                coverage_time = display_val_dict["AGS_"+str(dynamic_service)+"_CVR_CNTCOV"]
            if "AGS_"+str(dynamic_service)+"_CVR_RSPTIM" in display_val_dict.keys():
                response_time = display_val_dict["AGS_"+str(dynamic_service)+"_CVR_RSPTIM"]
            if coverage_time and response_time:
                #COVERAGE 7X12 / RESPONSE 8
                ent_value = "COVERAGE {} / RESPONSE {}".format(coverage_time.replace("X","x"),response_time.split(' ')[0] )
                if ent_value:
                    updateentXML = updating_xml(entxmldict,updateentXML,ent_id,ent_value,dynamic_service)
                
                    Update_xml_cov = ("UPDATE {TreeParam} SET ENTITLEMENT_XML = '{querystring}' {where_condition}".format(TreeParam=TreeParam,querystring=updateentXML,where_condition=where_condition))
                    Sql.RunQuery(Update_xml_cov)
    except Exception as e:
        Log.Info("cov onchange error-"+str(e))

    ##coefficient
    for key,val in get_selected_value.items():
        get_coefficient_val = Sql.GetFirst("SELECT ENTITLEMENT_COEFFICIENT, PRENTL.ENTITLEMENT_ID FROM PRENVL (NOLOCK) INNER JOIN PRENTL (NOLOCK) ON PAR_ENPAR_ENTITLEMENT_ID = PRENVL.ENTITLEMENT_ID AND PRENVL.SERVICE_ID = PRENTL.SERVICE_ID WHERE PRENVL.ENTITLEMENT_ID = '{}' AND PRENVL.SERVICE_ID = '{}' and PRENVL.ENTITLEMENT_DISPLAY_VALUE='{}'".format(str(key), serviceId,val))
        if get_coefficient_val:
            if get_coefficient_val.ENTITLEMENT_ID in entxmldict.keys():
                entitlement_string2 = entxmldict[get_coefficient_val.ENTITLEMENT_ID]
                entitlement_string2 = re.sub('<ENTITLEMENT_DISPLAY_VALUE>[^>]*?</ENTITLEMENT_DISPLAY_VALUE>','<ENTITLEMENT_DISPLAY_VALUE>'+str(get_coefficient_val.ENTITLEMENT_COEFFICIENT)+'</ENTITLEMENT_DISPLAY_VALUE>',entitlement_string2)
                Trace.Write(str(get_coefficient_val.ENTITLEMENT_COEFFICIENT)+"---entitlement_string2---"+str(entitlement_string2))
                entitlement_string2 = re.sub('<ENTITLEMENT_VALUE_CODE>[^>]*?</ENTITLEMENT_VALUE_CODE>','<ENTITLEMENT_VALUE_CODE>'+str(get_coefficient_val.ENTITLEMENT_COEFFICIENT)+'</ENTITLEMENT_VALUE_CODE>',entitlement_string2)
                updateentXML = re.sub(r'<QUOTE_ITEM_ENTITLEMENT>\s*<ENTITLEMENT_ID>'+str(get_coefficient_val.ENTITLEMENT_ID)+'[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>', entitlement_string2, updateentXML )
                Trace.Write("entxmldict---entitlement_string2--"+str(entitlement_string2))
                Sql.RunQuery( "UPDATE {objname} SET ENTITLEMENT_XML = '{xml_data}'  {where}".format(xml_data=updateentXML.replace("'","''") ,objname=TreeParam,where=str(where_condition)) )
        #return inputXML


try:
    if LEVEL == 'SERVICE_LEVEL':
        service_level_predefined()
    elif LEVEL == 'ONCHNGAE_DRIVERS':
        valuedriver_onchage()
    else:
        obj_list = ['SAQSGE','SAQSCE']
        for obj in obj_list:
            # if obj == "SAQSFE":
            # 	fab_predefined()
            if obj == "SAQSGE":
                greenbook_predefined()
            elif obj == "SAQSCE":
                equipment_predefined()
except Exception as e:
    Log.Info('error--'+str(e)+str(sys.exc_info()[1]))