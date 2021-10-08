# =========================================================================================================================================
#   __script_name : CQENTRLDWN.PY
#   __script_description : THIS SCRIPT IS USED FOR ENTITLEMENT ROLLDOWN 
#   __primary_author__ : ASHA LYSANDAR
#   __create_date : 12-11-2020
#   � BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
import datetime
import re
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
from SYDATABASE import SQL
Sql = SQL()
userId = str(User.Id)
userName = str(User.UserName)


try:
	objs = Param.CPQ_Columns['objectName']    
	wherecon = Param.CPQ_Columns['where']
except:
	objectName = Param.objectName
	wherecon = Param.where
wherecon = wherecon.replace("&#39;","'")
objItems = objs.split('=')
where = wherecon.split(",")[0]
SAQITMWhere = wherecon.split(",")[1]
sectionid = wherecon.split(",")[2]
objectName = objItems[0]
quote = objItems[2].split(",")[1]
revision =  objItems[2].split(",")[2]
Log.Info("QUOTE--------->"+str(quote)+'---'+str(revision))
userid = objItems[2].split(",")[0]
ancillary_flag = objItems[2].split(",")[3]
try: 
	attributeList = objItems[1].split(",")
except:
	attributeList = ""
get_serviceid = SAQITMWhere.split('SERVICE_ID = ')
get_serviceid = get_serviceid[len(get_serviceid)-1].replace("'","")
Log.Info("script called..40-----"+str(objectName)+" - "+str(where)+" - "+str(SAQITMWhere)+"------ "+str(attributeList)+'--'+str(get_serviceid))

def sendEmail(level):
	Log.Info('284-----entitlement email started-----')
	getQuoteId = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(quote))
	getEmail = Sql.GetFirst("SELECT email from users where id={}".format(userid))
	Log.Info("SELECT email from users where id='{}'".format(userid))
	userEmail = ""
	userEmail = str(getEmail.email)
	Header = "<!DOCTYPE html><html><head><style>h4{font-weight:normal; font-family:sans-serif;} table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #grey{background: rgb(245,245,245);} #bd{color : 'black';}</style> </head> <body><h4>Hi, <br> <br>The Entitlement settings have been applied to the equipment in the following quote:</br></h4>"

	Table_start ="<table class='table table-bordered'><tr><th id = 'grey'>Quote ID</th><th id = 'grey'>Rolldown Level</th><th id = 'grey'>Rolldown Status</th></tr><tr><td >"+str(getQuoteId.QUOTE_ID)+"</td><td>"+str(level)+"</td><td>Completed</td></tr></table> <br> <br>Note: Please do not reply to this email.</body></html>"

	Error_Info = Header + Table_start

	LOGIN_CRE = Sql.GetFirst("SELECT User_name,Password FROM SYCONF where Domain ='SUPPORT_MAIL'")

	# Create new SmtpClient object
	mailClient = SmtpClient()

	# Set the host and port (eg. smtp.gmail.com)
	mailClient.Host = "smtp.gmail.com"
	mailClient.Port = 587
	mailClient.EnableSsl = "true"

	# Setup NetworkCredential
	mailCred = NetworkCredential()
	mailCred.UserName = str(LOGIN_CRE.User_name)
	mailCred.Password = str(LOGIN_CRE.Password)
	mailClient.Credentials = mailCred
	to_email = ''
	to_email += str(userEmail)
	#Log.Info()
	from_email = ''
	from_email += str(userEmail)
	# Create two mail adresses, one for send from and the another for recipient
	toEmail = MailAddress(to_email)
	fromEmail = MailAddress(from_email)

	# Create new MailMessage object
	msg = MailMessage(fromEmail, toEmail)

	# Set message subject and body
	msg.Subject = str(level)+" Rolldown"
	msg.IsBodyHtml = True
	msg.Body = Error_Info
	copyEmail1 = MailAddress("sathyabama.akhala@bostonharborconsulting.com")
	#copyEmail2 = MailAddress("mayura.priya@bostonharborconsulting.com")
	#copyEmail3 = MailAddress("dhurga.gopalakrishnan@bostonharborconsulting.com")
	copyEmail4 = MailAddress("ranjani.parkavi@bostonharborconsulting.com")
	copyEmail5 = MailAddress("ashish.gandotra@bostonharborconsulting.com")
	#copyEmail6 = MailAddress("aditya.shivkumar@bostonharborconsulting.com")
	msg.Bcc.Add(copyEmail1)
	#msg.Bcc.Add(copyEmail2)
	#msg.Bcc.Add(copyEmail3)
	msg.Bcc.Add(copyEmail4)
	msg.Bcc.Add(copyEmail5)
	#msg.Bcc.Add(copyEmail6)
	# CC Emails
	# Send the message
	mailClient.Send(msg)

	return True
datetimenow = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")  
gettodaydate = datetime.datetime.now().strftime("%Y-%m-%d")
obj_list = []

def Request_access_token():
	webclient = System.Net.WebClient()
	webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
	webclient.Headers[
		System.Net.HttpRequestHeader.Authorization
	] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0="
	response = webclient.DownloadString(
		"https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials"
	)
	return eval(response)
def get_config_id():
	newConfigurationid  =""
	response = Request_access_token()
	webclient = System.Net.WebClient()		
	Request_URL="https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"
	webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])    

	ProductPartnumber = get_serviceid
	try:        
		requestdata = '{"productKey":"'+ ProductPartnumber+ '","date":"'+gettodaydate+'","context":[{"name":"VBAP-MATNR","value":"'+ ProductPartnumber+ '"}]}'
		response1 = webclient.UploadString(Request_URL, str(requestdata))        
		response1 = str(response1).replace(": true", ': "true"').replace(": false", ': "false"')
		Fullresponse = eval(response1)
		newConfigurationid = Fullresponse["id"]	
	except:
		pass
	return newConfigurationid
	
def ChildEntRequest(config_id,tableName,where):	
	#attribute_id,value_code,attr_type,display_name,config_id,cpsmatchID,isdefault	
	ent_child_temp = "ENT_SAVE_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)
	cpsmatchID = 11
	try:
		if tableName :
			#ent_child_temp = "ENT_SAVE_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)
			ent_child_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_child_temp)+"'' ) BEGIN DROP TABLE "+str(ent_child_temp)+" END  ' ")
			where_cond = where.replace("'","''")
			Sql.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID>'' AS sml,replace(replace(replace(replace(entitlement_xml,''&'','';#38''),'''','';#39''),'' < '','' &lt; ''),'' > '','' &gt; '')  as entitlement_xml from "+str(tableName)+"(nolock) "+str(where_cond)+" )A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_COST_IMPACT,ENTITLEMENT_TYPE,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,IS_DEFAULT INTO "+str(ent_child_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'') ; exec sys.sp_xml_removedocument @H; '")

			Parentgetdata=Sql.GetList("SELECT * FROM {} ".format(ent_child_temp))
			Log.Info("where------ "+str(where))
			if Parentgetdata:					
				response = Request_access_token()					
				Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(config_id)+"/items/1"
				#webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
				cpsmatchID=11
				
				for row in Parentgetdata:
					webclient = System.Net.WebClient()
					
					webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
						
					#webclient.Headers.Add("If-Match", "111")
					webclient.Headers.Add("If-Match", "1"+str(cpsmatchID))	
					get_ent_type = Sql.GetFirst("select ENTITLEMENT_TYPE from PRENTL where ENTITLEMENT_ID = '"+str(row.ENTITLEMENT_ID)+"' and SERVICE_ID = '"+str(get_serviceid)+"'")	
					if row.ENTITLEMENT_VALUE_CODE and row.ENTITLEMENT_VALUE_CODE not in ('undefined','None') and   row.ENTITLEMENT_ID !='undefined' and row.ENTITLEMENT_DISPLAY_VALUE !='select' and row.IS_DEFAULT =='0' and str(get_ent_type.ENTITLEMENT_TYPE).upper() not in ["VALUE DRIVER","VALUE DRIVER COEFFICIENT"]:
						try:
							requestdata = '{"characteristics":['
							
							requestdata +='{"id":"'+ str(row.ENTITLEMENT_ID) + '","values":[' 
							if row.ENTITLEMENT_TYPE in ('Check Box','CheckBox'):
								Log.Info('ENTITLEMENT_VALUE_CODE----'+str(row.ENTITLEMENT_VALUE_CODE)+'---'+str(eval(row.ENTITLEMENT_VALUE_CODE)))
								for code in eval(row.ENTITLEMENT_VALUE_CODE):
									requestdata += '{"value":"' + str(code) + '","selected":true}'
									requestdata +=','
								requestdata +=']},'	
							else:
								requestdata+= '{"value":"' +str(row.ENTITLEMENT_VALUE_CODE) + '","selected":true}]},'
							requestdata += ']}'
							requestdata = requestdata.replace('},]','}]')
							Log.Info("requestdata--child-- " + str(requestdata))
							response1 = webclient.UploadString(Request_URL, "PATCH", str(requestdata))
							cpsmatchID = cpsmatchID + 10			
							
						except Exception:
							Log.Info("Patch Error-1-"+str(sys.exc_info()[1]))
							cpsmatchID = cpsmatchID


		
		
		
		
		# if attribute_id !="":
		# 	response = Request_access_token()	
		# 	Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(config_id)+"/items/1"
		# 	webclient = System.Net.WebClient()
		# 	webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
		# 	if value_code and value_code not in ('undefined','None') and attribute_id !='undefined' and display_name !='select' and isdefault =='0':	
		# 		webclient.Headers.Add("If-Match", "1"+str(cpsmatchID))	
		# 		try:
		# 			requestdata = '{"characteristics":['
		# 			requestdata +='{"id":"'+ str(attribute_id) + '","values":[' 
		# 			if attr_type in ('Check Box','CheckBox'):
		# 				for code in eval(value_code):
		# 					requestdata += '{"value":"' + code + '","selected":true}'
		# 					requestdata +=','
		# 				requestdata +=']},'	
		# 			else:
		# 				requestdata+= '{"value":"' +str(value_code) + '","selected":true}]},'
		# 			requestdata += ']}'
		# 			requestdata = requestdata.replace('},]','}]')
		# 			#Log.Info("requestdata--child-- " + str(requestdata))
		# 			response1 = webclient.UploadString(Request_URL, "PATCH", str(requestdata))
		# 			cpsmatchID +=10
		# 		except Exception:
		# 			Log.Info("Patch Error-1-"+str(sys.exc_info()[1]))
			
	except Exception:
		Log.Info("Patch Error-2-"+str(sys.exc_info()[1]))        
	ent_child_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_child_temp)+"'' ) BEGIN DROP TABLE "+str(ent_child_temp)+" END  ' ")
	return cpsmatchID

##Pricing rollup
def entitlement_price_rollup(objectname,ent_temp):
	datetimenow = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p") 
	where_condition = SAQITMWhere.replace('A.','')
	update_fields = " CPS_CONFIGURATION_ID = '{}', CpqTableEntryModifiedBy = {}, CpqTableEntryDateModified = '{}'".format(getinnercon.CPS_CONFIGURATION_ID,userid,datetimenow)

	Log.Info('price rollup'+str(ent_roll_temp))
	if objectname == 'SAQSFE':
		obj_list = ['SAQTSE']
	elif objectname == 'SAQSGE':
		obj_list = ['SAQSFE','SAQTSE']
	elif objectname == 'SAQSCE':
		obj_list = ['SAQSGE','SAQSFE','SAQTSE']
	for obj in obj_list:
		##Z0016 ROLLUP
		if obj == 'SAQTSE' and GetXMLsecField:
			#newConfigurationid	= get_config_id()
			where_condition = SAQITMWhere.replace('A.','')
			GetXMLsec = Sql.GetList("select distinct ENTITLEMENT_ID,IS_DEFAULT,case when ENTITLEMENT_TYPE in ('Check Box','CheckBox') then 'Check Box' else ENTITLEMENT_TYPE end as ENTITLEMENT_TYPE,ENTITLEMENT_NAME,PRICE_METHOD,CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE null END as ENTITLEMENT_COST_IMPACT from {} {} AND ENTITLEMENT_ID like '%AGS_LAB_OPT%'".format(ent_temp,where_condition))
			get_ser_xml = Sql.GetFirst("""Select ENTITLEMENT_XML FROM SAQTSE (NOLOCK) {where_condition}""".format(where_condition = where_condition))
			flag = False
			if GetXMLsec:
				
				updateentXML = get_ser_xml.ENTITLEMENT_XML
				get_val_list =re.findall(r'AGS_LAB_OPT[\w\W]*?<',updateentXML)
				#if len(get_val_list) == len(GetXMLsec):
				
				for value in GetXMLsec:
					where_condtn = SAQITMWhere.replace('A.','')
					where_condtn += " AND ENTITLEMENT_ID = '{}'".format(value.ENTITLEMENT_ID) 
					get_cost_impact = value.ENTITLEMENT_COST_IMPACT
					get_currency = value.PRICE_METHOD
					GetXML = Sql.GetFirst("SELECT * from {} where ENTITLEMENT_ID = '{}' ".format(ent_temp,value.ENTITLEMENT_ID))
					if GetXML:
						get_value = GetXML.ENTITLEMENT_DISPLAY_VALUE
						get_calc_factor = GetXML.CALCULATION_FACTOR 
						get_price_impact = GetXML.ENTITLEMENT_PRICE_IMPACT
						get_code = GetXML.ENTITLEMENT_VALUE_CODE
					
					if value.ENTITLEMENT_TYPE == 'FreeInputNoMatching':
						get_value_qry = Sql.GetFirst("select SUM(CASE WHEN Isnumeric(ENTITLEMENT_DISPLAY_VALUE) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_DISPLAY_VALUE) ELSE 0 END) AS ENTITLEMENT_DISPLAY_VALUE from {pricetemp} {where_condition} ".format(pricetemp = ent_temp,where_condition = where_condtn))
						if get_value_qry:
							get_calc_factor = get_value = int(round(float(get_value_qry.ENTITLEMENT_DISPLAY_VALUE) ) )
							if value.ENTITLEMENT_COST_IMPACT and get_value:
								get_price_impact = get_value * float(value.ENTITLEMENT_COST_IMPACT)
							else:
								get_price_impact = 0.00
								
					elif value.ENTITLEMENT_TYPE in ('Check Box','CheckBox'):
						get_value_qry = Sql.GetList("select ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_VALUE_CODE from {pricetemp} where ENTITLEMENT_ID = '{ent_name}' ".format(pricetemp = ent_temp,ent_name = value.ENTITLEMENT_ID))
						getvalue = []
						getcode = []
						for val in get_value_qry:
							if val.ENTITLEMENT_VALUE_CODE and val.ENTITLEMENT_VALUE_CODE != 'undefined':
								getcode.extend(eval(val.ENTITLEMENT_VALUE_CODE) )
								
							if val.ENTITLEMENT_DISPLAY_VALUE and val.ENTITLEMENT_DISPLAY_VALUE != 'undefined':
								getvalue.extend(eval(val.ENTITLEMENT_DISPLAY_VALUE) )
						get_val = list(set(getvalue) )
						get_cod = list(set(getcode))
						get_value = str(get_val).replace("'", '"')
						get_code = str(get_cod).replace("'", '"')
					get_desc = value.ENTITLEMENT_DESCRIPTION
					assign_xml = """
						<ENTITLEMENT_ID>{ent_name}</ENTITLEMENT_ID>
						<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
						<ENTITLEMENT_DESCRIPTION>{tool_desc}</ENTITLEMENT_DESCRIPTION>
						<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
						<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
						<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
						<IS_DEFAULT>{is_default}</IS_DEFAULT>
						<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
						<PRICE_METHOD>{pm}</PRICE_METHOD>
						<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
						<ENTITLEMENT_NAME>{ent_desc}</ENTITLEMENT_NAME>
						""".format(ent_name = value.ENTITLEMENT_ID,ent_val_code = get_code.replace("'","''") if  "'" in str(get_code) and value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' else get_code, ent_disp_val = get_value.replace("'","''") if  "'" in str(get_value) else get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_NAME ,pm = get_currency ,cf= get_calc_factor, ent_type = value.ENTITLEMENT_TYPE, tool_desc = get_desc.replace("'","''") if "'" in get_desc else get_desc) 
					if value.ENTITLEMENT_ID+'<' in get_val_list:
						updateentXML = re.sub(r'<ENTITLEMENT_ID>'+str(value.ENTITLEMENT_ID)+'<[\w\W]*?</CALCULATION_FACTOR>', assign_xml, updateentXML )
					else:
						flag = True
						updateentXML += "<QUOTE_ITEM_ENTITLEMENT>"+assign_xml+"</QUOTE_ITEM_ENTITLEMENT>"
						
			if updateentXML:
				Log.Info('updateentXML--ser-'+str(updateentXML))
				where_condition = SAQITMWhere.replace('A.','')
				UpdateEntitlement = " UPDATE SAQTSE SET ENTITLEMENT_XML= '{}', {} {} ".format(updateentXML,update_fields,where_condition)
			
				Sql.RunQuery(UpdateEntitlement)
				if flag == True:
					newConfigurationid	= get_config_id()
					cpsmatchID = ChildEntRequest(newConfigurationid,obj,where_condition)
					Log.Info('cpsconfig---ser-'+str(newConfigurationid)+'cpsmatchID-'+str(cpsmatchID))
					Sql.RunQuery("UPDATE {} SET CPS_CONFIGURATION_ID = '{}',CPS_MATCH_ID={}  {} ".format(obj,newConfigurationid,cpsmatchID,where_condition))

		elif obj == 'SAQSFE' and GetXMLsecField:
			where_condition = SAQITMWhere.replace('A.','')
			fab_val = where_cond.split('AND ')
			where_condition += ' AND {}'.format( fab_val[len(fab_val)-1] )
			
			get_ser_xml = Sql.GetFirst("""Select ENTITLEMENT_XML FROM {obj} (NOLOCK) {where_condition}""".format(obj =obj ,where_condition = where_condition))
			updateentXML = ""
			GetXMLsec = Sql.GetList("select distinct ENTITLEMENT_ID,IS_DEFAULT,case when ENTITLEMENT_TYPE in ('Check Box','CheckBox') then 'Check Box' else ENTITLEMENT_TYPE end as ENTITLEMENT_TYPE,ENTITLEMENT_NAME,PRICE_METHOD,CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE null END as ENTITLEMENT_COST_IMPACT from {} {} AND ENTITLEMENT_ID like '%AGS_LAB_OPT%'".format(ent_temp,where_condition))
			if GetXMLsec:

				updateentXML = get_ser_xml.ENTITLEMENT_XML
				get_val_list =re.findall(r'AGS_LAB_OPT[\w\W]*?<',updateentXML)
				flag = False
				for value in GetXMLsec:
					where_condtn = SAQITMWhere.replace('A.','')
					where_condtn += " AND {} AND ENTITLEMENT_ID = '{}'".format(fab_val[len(fab_val)-1],value.ENTITLEMENT_ID) 
					get_cost_impact = value.ENTITLEMENT_COST_IMPACT
					get_currency = value.PRICE_METHOD
					GetXML = Sql.GetFirst("SELECT * from {} where ENTITLEMENT_ID = '{}' ".format(ent_roll_temp,value.ENTITLEMENT_ID))
					if GetXML:
						get_value = GetXML.ENTITLEMENT_DISPLAY_VALUE
						get_calc_factor = GetXML.CALCULATION_FACTOR 
						get_price_impact = GetXML.ENTITLEMENT_PRICE_IMPACT
						get_code = GetXML.ENTITLEMENT_VALUE_CODE

					if value.ENTITLEMENT_TYPE == 'FreeInputNoMatching':

						get_value_qry = Sql.GetFirst("select SUM(CASE WHEN Isnumeric(ENTITLEMENT_DISPLAY_VALUE) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_DISPLAY_VALUE) ELSE 0 END) AS ENTITLEMENT_DISPLAY_VALUE from {pricetemp}  {where_condition} ".format(pricetemp = ent_temp,where_condition = where_condtn))

						if get_value_qry:
							
							get_calc_factor = get_value = round(float(get_value_qry.ENTITLEMENT_DISPLAY_VALUE),2 )
							if value.ENTITLEMENT_COST_IMPACT and get_value:
								get_price_impact = get_value * float(value.ENTITLEMENT_COST_IMPACT)
							else:
								get_price_impact = 0.00
							
					elif value.ENTITLEMENT_TYPE in ('Check Box','CheckBox') :
						get_value_qry = Sql.GetList("select ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_VALUE_CODE from {pricetemp} where ENTITLEMENT_ID = '{ent_name}' ".format(pricetemp = ent_temp,ent_name = value.ENTITLEMENT_ID))
						getvalue = []
						getcode = []
						for val in get_value_qry:
							if val.ENTITLEMENT_VALUE_CODE and val.ENTITLEMENT_VALUE_CODE != 'undefined':
								getcode.extend(eval(val.ENTITLEMENT_VALUE_CODE) )
								
							if val.ENTITLEMENT_DISPLAY_VALUE and val.ENTITLEMENT_DISPLAY_VALUE != 'undefined':
								getvalue.extend(eval(val.ENTITLEMENT_DISPLAY_VALUE) )
						get_val = list(set(getvalue) )
						get_cod = list(set(getcode))
						get_value = str(get_val).replace("'", '"')
						get_code = str(get_cod).replace("'", '"')
					get_desc = value.ENTITLEMENT_DESCRIPTION
					assign_xml = """
						<ENTITLEMENT_ID>{ent_name}</ENTITLEMENT_ID>
						<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
						<ENTITLEMENT_DESCRIPTION>{tool_desc}</ENTITLEMENT_DESCRIPTION>
						<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
						<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
						<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
						<IS_DEFAULT>{is_default}</IS_DEFAULT>
						<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
						<PRICE_METHOD>{pm}</PRICE_METHOD>
						<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
						<ENTITLEMENT_NAME>{ent_desc}</ENTITLEMENT_NAME>
						""".format(ent_name = value.ENTITLEMENT_ID,ent_val_code = get_code.replace("'","''") if  "'" in str(get_code) and value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' else get_code, ent_disp_val = get_value.replace("'","''") if  "'" in str(get_value) else get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_NAME ,pm = get_currency ,cf= get_calc_factor, ent_type = value.ENTITLEMENT_TYPE, tool_desc =  get_desc.replace("'","''") if "'" in get_desc else get_desc) 
					if value.ENTITLEMENT_ID+'<' in get_val_list:
						updateentXML = re.sub(r'<ENTITLEMENT_ID>'+str(value.ENTITLEMENT_ID)+'<[\w\W]*?</CALCULATION_FACTOR>', assign_xml, updateentXML )
					else:
						updateentXML += "<QUOTE_ITEM_ENTITLEMENT>"+assign_xml+"</QUOTE_ITEM_ENTITLEMENT>"
						flag = True
						

					
			if updateentXML:
				UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
							
				Sql.RunQuery(UpdateEntitlement)
				if flag == True:
					newConfigurationid	= get_config_id()
					cpsmatchID = ChildEntRequest(newConfigurationid,obj,where_condition)
					Log.Info('cpsconfig---fab-'+str(newConfigurationid)+'cpsmatchID-'+str(cpsmatchID))
					Sql.RunQuery("UPDATE {} SET CPS_CONFIGURATION_ID = '{}',CPS_MATCH_ID={}  {} ".format(obj,newConfigurationid,cpsmatchID,where_condition))

		elif obj == 'SAQSGE' and GetXMLsecField:
			where_condition = SAQITMWhere.replace('A.','')
			fab_val = where_cond.split('AND ')
			where_condition += ' AND {} AND {} '.format( fab_val[len(fab_val)-1], fab_val[len(fab_val)-2]  )
			
			updateentXML = ""
		
			GetXMLsec = Sql.GetList("select distinct ENTITLEMENT_ID,IS_DEFAULT,case when ENTITLEMENT_TYPE in ('Check Box','CheckBox') then 'Check Box' else ENTITLEMENT_TYPE end as ENTITLEMENT_TYPE,ENTITLEMENT_NAME,PRICE_METHOD,CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE null END as ENTITLEMENT_COST_IMPACT from {} {} AND ENTITLEMENT_ID like '%AGS_LAB_OPT%'".format(ent_temp,where_condition))
			get_ser_xml = Sql.GetFirst("""Select ENTITLEMENT_XML FROM {obj} (NOLOCK) {where_condition}""".format(obj=obj,where_condition = where_condition))
			if GetXMLsec:
				flag = False
				#foo = [i.ENTITLEMENT_NAME for i in GetXMLsec]
				updateentXML = get_ser_xml.ENTITLEMENT_XML
				get_val_list =re.findall(r'AGS_LAB_OPT[\w\W]*?<',updateentXML)
				#new_list = list(set(foo).difference(get_val_list))
				for value in GetXMLsec:
					where_condtn = SAQITMWhere.replace('A.','')
					where_condtn += " AND {} and {} AND ENTITLEMENT_ID = '{}'".format(fab_val[len(fab_val)-1], fab_val[len(fab_val)-2],value.ENTITLEMENT_ID) 
					get_cost_impact = value.ENTITLEMENT_COST_IMPACT
					get_currency = value.PRICE_METHOD
					GetXML = Sql.GetFirst("SELECT * from {} where ENTITLEMENT_ID = '{}' ".format(ent_temp,value.ENTITLEMENT_ID))
					if GetXML:
						get_value = GetXML.ENTITLEMENT_DISPLAY_VALUE
						get_calc_factor = GetXML.CALCULATION_FACTOR 
						get_price_impact = GetXML.ENTITLEMENT_PRICE_IMPACT
						get_code = GetXML.ENTITLEMENT_VALUE_CODE
				
				
					if value.ENTITLEMENT_TYPE == 'FreeInputNoMatching':

						get_value_qry = Sql.GetFirst("select SUM(CASE WHEN Isnumeric(ENTITLEMENT_DISPLAY_VALUE) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_DISPLAY_VALUE) ELSE 0 END) AS ENTITLEMENT_DISPLAY_VALUE from {pricetemp}  {where_condition} ".format(pricetemp = ent_temp,where_condition = where_condtn))

						if get_value_qry:
							get_calc_factor = get_value = int(round(float(get_value_qry.ENTITLEMENT_DISPLAY_VALUE) ) )
							if value.ENTITLEMENT_COST_IMPACT and get_value:
								get_price_impact = get_value * float(value.ENTITLEMENT_COST_IMPACT)
							else:
								get_price_impact = 0.00
							
						
					elif value.ENTITLEMENT_TYPE in ('Check Box','CheckBox') :
						get_value_qry = Sql.GetList("select ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_VALUE_CODE from {pricetemp} where ENTITLEMENT_ID = '{ent_name}' ".format(pricetemp = ent_temp,ent_name = value.ENTITLEMENT_ID))
						getvalue = []
						getcode = []
						for val in get_value_qry:
							if val.ENTITLEMENT_VALUE_CODE and val.ENTITLEMENT_VALUE_CODE != 'undefined':
								getcode.extend(eval(val.ENTITLEMENT_VALUE_CODE) )
								
							if val.ENTITLEMENT_DISPLAY_VALUE and val.ENTITLEMENT_DISPLAY_VALUE != 'undefined':
								getvalue.extend(eval(val.ENTITLEMENT_DISPLAY_VALUE) )
						get_val = list(set(getvalue) )
						get_cod = list(set(getcode))
						get_value = str(get_val).replace("'", '"')
						get_code = str(get_cod).replace("'", '"')
					get_desc = value.ENTITLEMENT_DESCRIPTION
					assign_xml = """
						<ENTITLEMENT_ID>{ent_name}</ENTITLEMENT_ID>
						<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
						<ENTITLEMENT_DESCRIPTION>{tool_desc}</ENTITLEMENT_DESCRIPTION>
						<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
						<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
						<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
						<IS_DEFAULT>{is_default}</IS_DEFAULT>
						<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
						<PRICE_METHOD>{pm}</PRICE_METHOD>
						<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
						<ENTITLEMENT_NAME>{ent_desc}</ENTITLEMENT_NAME>
						""".format(ent_name = value.ENTITLEMENT_ID, ent_val_code = get_code.replace("'","''") if  "'" in str(get_code) and value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' else get_code, ent_disp_val = get_value.replace("'","''") if  "'" in str(get_value) else get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,tool_desc=  get_desc.replace("'","''") if "'" in get_desc else get_desc  ,pm = get_currency ,cf= get_calc_factor, ent_type = value.ENTITLEMENT_TYPE, ent_desc= value.ENTITLEMENT_NAME) 
					if value.ENTITLEMENT_ID+'<' in get_val_list:
						updateentXML = re.sub(r'<ENTITLEMENT_ID>'+str(value.ENTITLEMENT_ID)+'<[\w\W]*?</CALCULATION_FACTOR>', assign_xml, updateentXML )
					else:
						updateentXML += "<QUOTE_ITEM_ENTITLEMENT>"+assign_xml+"</QUOTE_ITEM_ENTITLEMENT>"
						flag = False

			if updateentXML:
				UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
							
				Sql.RunQuery(UpdateEntitlement)
				if flag == True:
					newConfigurationid	= get_config_id()
					cpsmatchID = ChildEntRequest(newConfigurationid,obj,where_condition)
					Log.Info('cpsconfig---grn-'+str(newConfigurationid)+'cpsmatchID-'+str(cpsmatchID))
					Sql.RunQuery("UPDATE {} SET CPS_CONFIGURATION_ID = '{}',CPS_MATCH_ID={}  {} ".format(obj,newConfigurationid,cpsmatchID,where_condition))

##z0046 insert
def ancillary_service_Z0046(get_serviceid):
	Log.Info('136----')
	try:
	#if get_serviceid == "Z0091":
		Log.Info('Z0091-1-Z0046---')
		where_condition = where.replace('SRC.','')
		get_ancillaryservice = Sql.GetFirst("select * from SAQTSE {where_condition}""".format(where_condition= SAQITMWhere.replace('A.','')))
		if get_ancillaryservice :
			Log.Info('Z0091--Z0046---')
			#if 
			get_ancillary_fab = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQSFE {where_condition}""".format(where_condition=where_condition ))
			if get_ancillary_fab:
				if get_ancillary_fab.cnt == 0:
					SAQSFE_ancillary_query="""
						INSERT SAQSFE (ENTITLEMENT_XML,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
						CPS_CONFIGURATION_ID, CPS_MATCH_ID,QTESRVENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,QTESRVFBL_RECORD_ID,CONFIGURATION_STATUS,QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID, CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)
						SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
						SELECT 
							DISTINCT	
							SAQTSE.ENTITLEMENT_XML,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSFB.FABLOCATION_ID, SAQSFB.FABLOCATION_NAME, SAQSFB.FABLOCATION_RECORD_ID, SAQSFB.QUOTE_SERVICE_FAB_LOCATION_RECORD_ID as QTESRVFBL_RECORD_ID,SAQTSE.CONFIGURATION_STATUS
						FROM
						SAQTSE (NOLOCK)
						JOIN SAQSFB ON SAQSFB.SERVICE_ID = 'Z0091' AND SAQSFB.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSFB.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID
						WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ""".format(UserId=userid, QuoteRecordId=quote, ServiceId='Z0046', revision_rec_id = revision)
					Log.Info('SAQSFE_ancillary_query--148----ROLL DOWN----'+str(SAQSFE_ancillary_query))
					Sql.RunQuery(SAQSFE_ancillary_query)
					
			
			get_ancillary_grn = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQSGE {where_condition}""".format(where_condition=where_condition ))
			if get_ancillary_grn:
				if get_ancillary_grn.cnt == 0: 
					qtqtse_query_anc="""
						INSERT SAQSGE (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
						CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,QTSFBLENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED )
						SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT IQ.*,M.ENTITLEMENT_XML,M.CONFIGURATION_STATUS FROM(
						SELECT 
							DISTINCT	
							SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSFE.QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID as QTSFBLENT_RECORD_ID,SAQSFE.FABLOCATION_ID,SAQSFE.FABLOCATION_NAME,SAQSFE.FABLOCATION_RECORD_ID
						FROM
						SAQTSE (NOLOCK)
						JOIN SAQSCO  (NOLOCK) ON SAQSCO.SERVICE_ID = 'Z0091' AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID JOIN SAQSFE ON SAQSFE.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSFE.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSFE.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID 
						WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}'  AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ JOIN SAQSFE (NOLOCK) M ON IQ.QTSFBLENT_RECORD_ID = QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID )OQ""".format(UserId=userid, QuoteRecordId=quote, ServiceId='Z0046', revision_rec_id = revision)
					Log.Info("qtqtse_query_anc---163------"+str(qtqtse_query_anc))
					Sql.RunQuery(qtqtse_query_anc)
			
			get_ancillary_equp = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQSCE {where_condition}""".format(where_condition=where_condition ))
			if get_ancillary_equp:
				if get_ancillary_equp.cnt == 0: 
					qtqsce_anc_query="""
						INSERT SAQSCE
						(KB_VERSION,ENTITLEMENT_XML,CONFIGURATION_STATUS,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,QTESRVCOB_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
						SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
						SELECT 
						SAQTSE.KB_VERSION,SAQTSE.ENTITLEMENT_XML,SAQTSE.CONFIGURATION_STATUS,SAQSCO.EQUIPMENT_ID,SAQSCO.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID as QTESRVCOB_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSCO.SERIAL_NO,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQSCO.FABLOCATION_ID,SAQSCO.FABLOCATION_NAME,SAQSCO.FABLOCATION_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID
						FROM	
						SAQTSE (NOLOCK)
						JOIN SAQSCO (NOLOCK) ON SAQSCO.SERVICE_ID = 'Z0091' AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID 
						WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}' AND SAQSCO.EQUIPMENT_ID not in (SELECT EQUIPMENT_ID FROM SAQSCE (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'   AND QTEREV_RECORD_ID = '{revision_rec_id}' AND SERVICE_ID = '{ServiceId}')) IQ""".format(UserId=userid, QuoteRecordId=quote, ServiceId='Z0046', revision_rec_id = revision)
					Log.Info('@qtqsce_anc_query-renewal----179=---Qt_rec_id--'+str(qtqsce_anc_query))
					Sql.RunQuery(qtqsce_anc_query)
			
			# get_SAQSCO = Sql.GetFirst("""SELECT count(*) as cnt FROM SAQSCO (NOLOCK) WHERE SAQSCO.QUOTE_RECORD_ID = '{ContractId}' AND QTEREV_RECORD_ID = '{revision_rec_id}'""".format(ContractId=Qt_rec_id,revision_rec_id = rev_rec_id))
			# Log.Info("get_SAQSCO---> "+ str(get_SAQSCO.cnt))
			
			# get_SAQSCE = Sql.GetFirst("""SELECT count(*) as cnt FROM SAQSCE (NOLOCK) WHERE SAQSCE.QUOTE_RECORD_ID = '{ContractId}' AND QTEREV_RECORD_ID = '{revision_rec_id}'""".format(ContractId=Qt_rec_id,revision_rec_id = rev_rec_id))
			# Log.Info("get_SAQSCE---> "+ str(get_SAQSCE.cnt))

			# Duplicate records removed from assembly level entitlement in offering - Start
			Sql.RunQuery("""DELETE FROM SAQSAE WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}'""".format(UserId=userid, QuoteRecordId=quote, ServiceId='Z0046', revision_rec_id = revision))
			# Duplicate records removed from assembly level entitlement in offering - End
			SAQSAE_ent_anc_renewal = """INSERT SAQSAE (KB_VERSION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,QTESRVCOA_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS,QTESRVCOE_RECORD_ID,QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(SELECT IQ.*,M.ENTITLEMENT_XML,M.CONFIGURATION_STATUS,M.QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID as QTESRVCOE_RECORD_ID FROM ( SELECT DISTINCT SAQTSE.KB_VERSION,SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.GREENBOOK,SAQSCA.GREENBOOK_RECORD_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_DESCRIPTION,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQSCA.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID as QTESRVCOA_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID FROM SAQTSE (NOLOCK) JOIN (SELECT * FROM SAQSCA (NOLOCK) WHERE SAQSCA.QUOTE_RECORD_ID = '{ContractId}' AND SAQSCA.QTEREV_RECORD_ID = '{revision_rec_id}' ) SAQSCA ON SAQTSE.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQTSE.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID AND SAQTSE.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{ContractId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{serviceId}') IQ JOIN SAQSCE (NOLOCK) M ON M.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND M.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND M.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND M.EQUIPMENT_ID = IQ.EQUIPMENT_ID )IQ""".format(UserId=userid, QuoteRecordId=quote, ServiceId='Z0046', revision_rec_id = revision)
			Log.Info('SAQSAE_ent_anc_renewal--393--renewal-1881-----'+str(SAQSAE_ent_anc_renewal))

	except Exception as e:
		Log.Info("error on ancillary--"+str(e)+'--'+str(str(sys.exc_info()[-1].tb_lineno)))


## Entitlement rolldown fn
def entitlement_rolldown(objectName,get_serviceid,where,ent_temp):
	is_changed = False
	if 'Z0007' in get_serviceid:
		objectName = 'SAQSCE'
		obj_list = ['SAQTSE','SAQSFE','SAQSGE','SAQIEN','SAQSAE']
	if objectName == 'SAQTSE':
		obj_list = ['SAQSCE','SAQSFE','SAQSGE','SAQIEN','SAQSAE']
	elif objectName == 'SAQSFE':
		obj_list = ['SAQSCE','SAQSGE','SAQIEN','SAQSAE']
		is_changed = True
	elif objectName == 'SAQSGE':
		obj_list = ['SAQSCE','SAQIEN','SAQSAE']
		is_changed = True
	elif objectName == 'SAQSCE' and 'Z0007' not in get_serviceid:
		obj_list = ['SAQIEN','SAQSAE']
		is_changed = True
	datetimenow = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p") 
	
	fab_dict = {}
	grnbk_dict = {}
	try:
		for obj in obj_list:
			join =""
			update_fields = " CPS_CONFIGURATION_ID = '{}', CpqTableEntryModifiedBy = {}, CpqTableEntryDateModified = '{}',CONFIGURATION_STATUS = '{}'".format(getinnercon.CPS_CONFIGURATION_ID,userid,datetimenow,getinnercon.CONFIGURATION_STATUS)
			if objectName == 'SAQSGE' and obj == 'SAQIEN':
				join = " JOIN SAQICO ON SAQICO.QUOTE_RECORD_ID = SRC.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SRC.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SRC.SERVICE_ID AND SAQICO.FABLOCATION_ID = SRC.FABLOCATION_ID AND SAQICO.GREENBOOK = SRC.GREENBOOK AND TGT.QTEITMCOB_RECORD_ID = SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID "
			
			elif obj in ('SAQSAE','SAQIEN') and objectName == 'SAQSCE':
				join = " AND SRC.GREENBOOK =TGT.GREENBOOK AND SRC.FABLOCATION_ID = TGT.FABLOCATION_ID AND SRC.EQUIPMENT_ID = TGT.EQUIPMENT_ID  "
			elif obj in ('SAQSAE','SAQIEN') and objectName == 'SAQSGE':
				join = " AND SRC.GREENBOOK =TGT.GREENBOOK AND SRC.FABLOCATION_ID = TGT.FABLOCATION_ID  "
			elif obj in ('SAQSAE','SAQIEN') and objectName == 'SAQSFE':
				join = "  AND SRC.FABLOCATION_ID = TGT.FABLOCATION_ID  "
			
			
			if is_changed and obj == "SAQSCE":
				update_fields += ",IS_CHANGED = 1"
			
			###roll down for all levels starts
			
			if obj == 'SAQTSE'  and GetXMLsecField and 'Z0007' in get_serviceid:
				where_condition = SAQITMWhere.replace('A.','')
				updateentXML = ""
				for value in GetXMLsecField:
					get_value = value.ENTITLEMENT_DISPLAY_VALUE
					get_calc_factor = value.CALCULATION_FACTOR 
					get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
					get_cost_impact = value.ENTITLEMENT_COST_IMPACT
					#try:
					get_currency = value.PRICE_METHOD
					#except:
					#get_currency = ""
					#Log.Info('ENTITLEMENT_COST_IMPACT-----'+str(value.ENTITLEMENT_COST_IMPACT))
								
					if (value.ENTITLEMENT_TYPE in ('Drop Down','DropDown') and value.ENTITLEMENT_COST_IMPACT):
						
						GetXMLfab = Sql.GetFirst("select SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS ENTITLEMENT_COST_IMPACT from (SELECT * FROM {pricetemp} {where_condition} AND ENTITLEMENT_ID = '{ent_name}') IQ ".format(pricetemp = ent_temp,where_condition = where_condition,ent_name = value.ENTITLEMENT_ID))

						if GetXMLfab:
							get_cost_impact = GetXMLfab.ENTITLEMENT_COST_IMPACT
						#Log.Info("get_calc_factor---"+str(get_calc_factor))
					get_desc = value.ENTITLEMENT_DESCRIPTION
					get_code = value.ENTITLEMENT_VALUE_CODE
					updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
						<ENTITLEMENT_ID>{ent_name}</ENTITLEMENT_ID>
						<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
						<ENTITLEMENT_DESCRIPTION>{tool_desc}</ENTITLEMENT_DESCRIPTION>
						<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
						<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
						<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
						<IS_DEFAULT>{is_default}</IS_DEFAULT>
						<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
						<PRICE_METHOD>{pm}</PRICE_METHOD>
						<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
						<ENTITLEMENT_NAME>{ent_desc}</ENTITLEMENT_NAME>
						</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_ID,ent_val_code = get_code.replace("'","''") if  "'" in str(get_code) and value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' else get_code, ent_disp_val = get_value.replace("'","''") if  "'" in str(get_value) else get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_NAME ,pm = value.PRICE_METHOD ,cf= get_calc_factor, ent_type = value.ENTITLEMENT_TYPE,tool_desc= get_desc.replace("'","''") if "'" in get_desc else get_desc) 
					
				#Log.Info('updateentXML--ser-'+str(updateentXML))
				where_condition = SAQITMWhere.replace('A.','')
				UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
				#Log.Info('UpdateEntitlement--'+str(" UPDATE {} SET ENTITLEMENT_XML= '', {} {} ".format(obj, update_fields,where_condition)))
					

			elif obj == 'SAQSFE' and GetXMLsecField:
				if 'Z0007' in get_serviceid and objectName == 'SAQSCE': 
					where_condition = SAQITMWhere.replace('A.','')
					
					get_value_query = Sql.GetList("select QUOTE_RECORD_ID,QTEREV_RECORD_ID ,FABLOCATION_RECORD_ID, FABLOCATION_ID from SAQSFB {} ".format(where_condition) )
					
					for fab in get_value_query:
						where_condition = SAQITMWhere.replace('A.','')
						updateentXML = ""
						where_condition += " AND FABLOCATION_ID = '{}'".format(fab.FABLOCATION_ID )
						for value in GetXMLsecField:
							get_value = value.ENTITLEMENT_DISPLAY_VALUE
							get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
							get_calc_factor = value.CALCULATION_FACTOR 
							get_cost_impact = value.ENTITLEMENT_COST_IMPACT
							
							if (value.ENTITLEMENT_TYPE in ('Drop Down','DropDown')  and value.ENTITLEMENT_COST_IMPACT):
								
								GetXMLfab = Sql.GetFirst("select SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS ENTITLEMENT_COST_IMPACT from (SELECT * FROM {pricetemp} {where_condition} AND ENTITLEMENT_ID = '{ent_name}') IQ ".format(pricetemp = ent_temp,where_condition = where_condition,ent_name = value.ENTITLEMENT_ID))
								if GetXMLfab:
									get_cost_impact = GetXMLfab.ENTITLEMENT_COST_IMPACT
							get_desc = value.ENTITLEMENT_DESCRIPTION
							get_code = value.ENTITLEMENT_VALUE_CODE
							updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
								<ENTITLEMENT_ID>{ent_name}</ENTITLEMENT_ID>
								<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
								<ENTITLEMENT_DESCRIPTION>{tool_desc}</ENTITLEMENT_DESCRIPTION>
								<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
								<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
								<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
								<IS_DEFAULT>{is_default}</IS_DEFAULT>
								<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
								<PRICE_METHOD>{pm}</PRICE_METHOD>
								<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
								<ENTITLEMENT_NAME>{ent_desc}</ENTITLEMENT_NAME>
								</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_ID,ent_val_code = get_code.replace("'","''") if  "'" in str(get_code) and value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' else get_code, ent_disp_val = get_value.replace("'","''") if  "'" in str(get_value) else get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_NAME ,pm = value.PRICE_METHOD ,cf= get_calc_factor , ent_type = value.ENTITLEMENT_TYPE,tool_desc= get_desc.replace("'","''") if "'" in get_desc else get_desc) 
						
					
						UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
									
						Sql.RunQuery(UpdateEntitlement)
				else:
					get_value_query = Sql.GetList("select distinct FABLOCATION_ID from SAQSFB {} ".format(where_cond))
					##value driver
					val_list = []
					val_coeff = []
					get_valuedriver_ids = Sql.GetList("SELECT PRENTL.ENTITLEMENT_ID,PRENTL.ENTITLEMENT_DESCRIPTION from PRENTL (NOLOCK) INNER JOIN PRENLI (NOLOCK) ON PRENTL.ENTITLEMENT_ID = PRENLI.ENTITLEMENT_ID WHERE SERVICE_ID = '{}' AND ENTITLEMENT_TYPE = 'VALUE DRIVER' AND PRENTL.ENTITLEMENT_ID NOT IN ('AGS_Z0091_VAL_UPIMPV', 'AGS_Z0091_VAL_CSTSEG', 'AGS_Z0091_VAL_SVCCMP', 'AGS_Z0091_VAL_QLYREQ') AND ENTITLEMENTLEVEL_NAME = 'OFFERING FAB LEVEL' AND PRENTL.ENTITLEMENT_ID NOT IN (SELECT ENTITLEMENT_ID from PRENLI (NOLOCK) WHERE ENTITLEMENTLEVEL_NAME IN ('OFFERING LEVEL')) ".format(get_serviceid) )
					val_list = [i.ENTITLEMENT_ID for i in get_valuedriver_ids]
					if get_valuedriver_ids:
						lst = str(tuple([i.ENTITLEMENT_ID for i in get_valuedriver_ids])).replace(",)",')')
						get_coeffi = Sql.GetList("SELECT ENTITLEMENT_ID from PRENTL (NOLOCK) where SERVICE_ID = '{}' AND PAR_ENPAR_ENTITLEMENT_ID in {} ".format(get_serviceid ,lst) )
						val_coeff = [i.ENTITLEMENT_ID for i in get_coeffi]
						val_list.extend(val_coeff)
					Log.Info("val_list--fab-"+str(val_list))
					for fab in get_value_query:
						where_condition = where_cond + " AND FABLOCATION_ID = '{}' ".format(fab.FABLOCATION_ID)
						get_equipment_count = Sql.GetFirst("select count(*) as cnt from SAQSCO {}".format(where_condition))
						updateentXML = ""
						####value driver
						get_previous_xml = Sql.GetFirst("SELECT ENTITLEMENT_XML FROM {} {}".format(obj, where_condition))
						
						for value in GetXMLsecField:
							get_value = value.ENTITLEMENT_DISPLAY_VALUE
							get_cost_impact = value.ENTITLEMENT_COST_IMPACT
							get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
							get_currency = value.PRICE_METHOD
							get_calc_factor = value.CALCULATION_FACTOR 
							if value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' and 'AGS_LAB_OPT' in value.ENTITLEMENT_ID and 'Z0016' in get_serviceid:
								if get_value_query and value.ENTITLEMENT_DISPLAY_VALUE and value.ENTITLEMENT_ID in grnbk_dict.keys() :
								
									get_calc_factor = get_value = round(float(grnbk_dict[value.ENTITLEMENT_ID]) *	float(get_equipment_count.cnt),2)
									if value.ENTITLEMENT_COST_IMPACT and get_value:
										get_price_impact = get_value * float(value.ENTITLEMENT_COST_IMPACT)
									else:
										get_price_impact = 0.00
							get_desc = value.ENTITLEMENT_DESCRIPTION	
							get_code = value.ENTITLEMENT_VALUE_CODE
							###updating exisitng value for non editable value drivers
							if val_list and get_previous_xml and  value.ENTITLEMENT_ID in val_list:
								get_val_list =re.findall(r''+str(value.ENTITLEMENT_ID)+'<[\w\W]*?</ENTITLEMENT_DISPLAY_VALUE>',get_previous_xml.ENTITLEMENT_XML)
								
								get_code = re.findall( re.compile(r'<ENTITLEMENT_VALUE_CODE>([^>]*?)</ENTITLEMENT_VALUE_CODE>'), get_val_list[0] )[0]
								get_value = re.findall( re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>'), get_val_list[0] )[0]
								#Log.Info("value driver-fab-"+str(get_value)+str(value.ENTITLEMENT_ID))

							updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
									<ENTITLEMENT_ID>{ent_name}</ENTITLEMENT_ID>
									<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
									<ENTITLEMENT_DESCRIPTION>{tool_desc}</ENTITLEMENT_DESCRIPTION>
									<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
									<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
									<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
									<IS_DEFAULT>{is_default}</IS_DEFAULT>
									<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
									<PRICE_METHOD>{pm}</PRICE_METHOD>
									<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
									<ENTITLEMENT_NAME>{ent_desc}</ENTITLEMENT_NAME>
									</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_ID,ent_val_code = get_code.replace("'","''") if  "'" in str(get_code) and value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' else get_code, ent_disp_val = get_value.replace("'","''") if  "'" in str(get_value) else get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_NAME ,pm = value.PRICE_METHOD ,cf= get_calc_factor , ent_type = value.ENTITLEMENT_TYPE,tool_desc= get_desc.replace("'","''") if "'" in get_desc else get_desc)  
						UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
						
						
						Sql.RunQuery(UpdateEntitlement)
				
				
			elif obj == 'SAQSGE' and GetXMLsecField:
				if 'Z0007' in get_serviceid and objectName == 'SAQSCE':
					where_condition = SAQITMWhere.replace('A.','')
					#fab_val = where_cond.split('AND ')
					#where_condition += ' AND {}'.format( fab_val[len(fab_val)-1] )
					#Log.Info('where_condition-----1307--'+str(where_condition))	
					
					get_value_query = Sql.GetList("select FABLOCATION_ID,GREENBOOK,count(*) as cnt from SAQSCO {} group by FABLOCATION_ID,GREENBOOK ".format(where_cond ))
					for fab in get_value_query:
						updateentXML = ""
						where_condition = SAQITMWhere.replace('A.','')
						where_condition += " AND FABLOCATION_ID = '{}' and GREENBOOK = '{}'".format(fab.FABLOCATION_ID,fab.GREENBOOK )
						for value in GetXMLsecField:
							get_value = value.ENTITLEMENT_DISPLAY_VALUE
							get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
							get_calc_factor = value.CALCULATION_FACTOR 
							get_cost_impact = value.ENTITLEMENT_COST_IMPACT
							
							if (value.ENTITLEMENT_TYPE in ('Drop Down','DropDown') and value.ENTITLEMENT_COST_IMPACT):
								#GetXMLfab = Sql.GetFirst("select SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS ENTITLEMENT_COST_IMPACT,FABLOCATION_ID,GREENBOOK from (SELECT distinct e.QUOTE_RECORD_ID, e.FABLOCATION_RECORD_ID, e.FABLOCATION_ID,e.GREENBOOK,e.EQUIPMENT_ID ,replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT FROM (select SAQSCE.EQUIPMENT_ID,SAQSCE.QUOTE_RECORD_ID as QUOTE_RECORD_ID, SAQSCE.FABLOCATION_RECORD_ID, SAQSCE.FABLOCATION_ID,SAQSCE.GREENBOOK, CONVERT(xml, replace(cast(SAQSCE.ENTITLEMENT_XML as varchar(max)),'&','&amp;'), 2) as ENTITLEMENT_XML FROM SAQSCE (NOLOCK) {}) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) ) IQ where ENTITLEMENT_NAME =  '{}' GROUP BY QUOTE_RECORD_ID, FABLOCATION_ID, FABLOCATION_RECORD_ID, GREENBOOK ".format(where_condition,value.ENTITLEMENT_NAME))
								GetXMLfab = Sql.GetFirst("select SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS ENTITLEMENT_COST_IMPACT from (SELECT * FROM {pricetemp} {where_condition} AND ENTITLEMENT_ID = '{ent_name}') IQ ".format(pricetemp = ent_temp,where_condition = where_condition,ent_name = value.ENTITLEMENT_ID))
								if GetXMLfab:
									get_cost_impact = GetXMLfab.ENTITLEMENT_COST_IMPACT
								#Log.Info("get_calc_factor---"+str(get_calc_factor))
							get_desc = value.ENTITLEMENT_DESCRIPTION
							get_code = value.ENTITLEMENT_VALUE_CODE
							updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
								<ENTITLEMENT_ID>{ent_name}</ENTITLEMENT_ID>
								<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
								<ENTITLEMENT_DESCRIPTION>{tool_desc}</ENTITLEMENT_DESCRIPTION>
								<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
								<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
								<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
								<IS_DEFAULT>{is_default}</IS_DEFAULT>
								<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
								<PRICE_METHOD>{pm}</PRICE_METHOD>
								<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
								<ENTITLEMENT_NAME>{ent_desc}</ENTITLEMENT_NAME>
								</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_ID,ent_val_code = get_code.replace("'","''") if  "'" in str(get_code) and value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' else get_code, ent_disp_val = get_value.replace("'","''") if  "'" in str(get_value) else get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_NAME ,pm = value.PRICE_METHOD ,cf= get_calc_factor , ent_type = value.ENTITLEMENT_TYPE,tool_desc= get_desc.replace("'","''") if "'" in get_desc else get_desc) 
						
						#Log.Info('updateentXML--fab2-'+str(updateentXML))
					
						UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
									
						Sql.RunQuery(UpdateEntitlement)
					
				else:
					get_value_query = Sql.GetList("select FABLOCATION_ID,GREENBOOK,count(*) as cnt from SAQSCO {} group by FABLOCATION_ID,GREENBOOK ".format(where_cond ))			
					##value driver
					val_list = []
					val_coeff = []
					get_valuedriver_ids = Sql.GetList("SELECT PRENTL.ENTITLEMENT_ID,PRENTL.ENTITLEMENT_DESCRIPTION from PRENTL (NOLOCK) INNER JOIN PRENLI (NOLOCK) ON PRENTL.ENTITLEMENT_ID = PRENLI.ENTITLEMENT_ID WHERE SERVICE_ID = '{}' AND ENTITLEMENT_TYPE = 'VALUE DRIVER' AND PRENTL.ENTITLEMENT_ID NOT IN ('AGS_Z0091_VAL_UPIMPV', 'AGS_Z0091_VAL_CSTSEG', 'AGS_Z0091_VAL_SVCCMP', 'AGS_Z0091_VAL_QLYREQ') AND ENTITLEMENTLEVEL_NAME = 'OFFERING FAB GREENBOOK LEVEL' AND PRENTL.ENTITLEMENT_ID NOT IN (SELECT ENTITLEMENT_ID from PRENLI (NOLOCK) WHERE ENTITLEMENTLEVEL_NAME IN ('OFFERING LEVEL')) ".format(get_serviceid) )
					val_list = [i.ENTITLEMENT_ID for i in get_valuedriver_ids]
					if get_valuedriver_ids:
						lst = str(tuple([i.ENTITLEMENT_ID for i in get_valuedriver_ids])).replace(",)",')')
						get_coeffi = Sql.GetList("SELECT ENTITLEMENT_ID from PRENTL (NOLOCK) where SERVICE_ID = '{}' AND PAR_ENPAR_ENTITLEMENT_ID in {} ".format(get_serviceid ,lst) )
						val_coeff = [i.ENTITLEMENT_ID for i in get_coeffi]
						val_list.extend(val_coeff)
					Log.Info("val_list--grn-"+str(val_list))
					for grnbk in get_value_query:
						where_condition = where_cond + "AND FABLOCATION_ID = '{}' AND GREENBOOK = '{}' ".format(grnbk.FABLOCATION_ID,grnbk.GREENBOOK)
						updateentXML = ""
						for value in GetXMLsecField:
							####value driver
							get_previous_xml = Sql.GetFirst("SELECT ENTITLEMENT_XML FROM {} {}".format(obj, where_condition))

							get_value = value.ENTITLEMENT_DISPLAY_VALUE
							get_cost_impact = value.ENTITLEMENT_COST_IMPACT
							get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
							get_calc_factor = value.CALCULATION_FACTOR
							get_currency = value.PRICE_METHOD
							if value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' and 'AGS_LAB_OPT' in value.ENTITLEMENT_ID and 'Z0016' in get_serviceid:
								
								if get_value_query and value.ENTITLEMENT_DISPLAY_VALUE and value.ENTITLEMENT_ID in grnbk_dict.keys() :
									get_val = float(grnbk_dict[value.ENTITLEMENT_ID]) * float(grnbk.cnt)
									if value.ENTITLEMENT_COST_IMPACT and get_val:
										get_price_impact = get_val * float(value.ENTITLEMENT_COST_IMPACT)
									else:
										get_price_impact = 0.00
									get_calc_factor = get_value = round(get_val,2)
							
							get_desc = value.ENTITLEMENT_DESCRIPTION
							get_code = value.ENTITLEMENT_VALUE_CODE
							###updating exisitng value for non editable value drivers
							if val_list and get_previous_xml and  value.ENTITLEMENT_ID in val_list:
								#Log.Info("value driver--"+str(value.ENTITLEMENT_ID))
								get_val_list =re.findall(r''+str(value.ENTITLEMENT_ID)+'<[\w\W]*?</ENTITLEMENT_DISPLAY_VALUE>',get_previous_xml.ENTITLEMENT_XML)
								
								get_code = re.findall( re.compile(r'<ENTITLEMENT_VALUE_CODE>([^>]*?)</ENTITLEMENT_VALUE_CODE>'), get_val_list[0] )[0]
								get_value = re.findall( re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>'), get_val_list[0] )[0]
							updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
								<ENTITLEMENT_ID>{ent_name}</ENTITLEMENT_ID>
								<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
								<ENTITLEMENT_DESCRIPTION>{tool_desc}</ENTITLEMENT_DESCRIPTION>
								<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
								<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
								<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
								<IS_DEFAULT>{is_default}</IS_DEFAULT>
								<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
								<PRICE_METHOD>{pm}</PRICE_METHOD>
								<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
								<ENTITLEMENT_NAME>{ent_desc}</ENTITLEMENT_NAME>
								</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_ID,ent_val_code = get_code.replace("'","''") if  "'" in str(get_code) and value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' else get_code, ent_disp_val = get_value.replace("'","''") if  "'" in str(get_value) else get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_NAME ,pm = value.PRICE_METHOD ,cf= get_calc_factor , ent_type = value.ENTITLEMENT_TYPE,tool_desc= get_desc.replace("'","''") if "'" in get_desc else get_desc)  
						
						UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
							
						Sql.RunQuery(UpdateEntitlement)

			elif obj == 'SAQSCE' and GetXMLsecField:
			
				get_value_query = Sql.GetFirst("select count(*) as cnt from SAQSCO  {}   ".format(where_cond))
			
				where_condition = where_cond
				updateentXML = ""
				##value driver
				val_list = []
				val_coeff = []
				get_valuedriver_ids = Sql.GetList("SELECT PRENTL.ENTITLEMENT_ID,PRENTL.ENTITLEMENT_DESCRIPTION from PRENTL (NOLOCK) INNER JOIN PRENLI (NOLOCK) ON PRENTL.ENTITLEMENT_ID = PRENLI.ENTITLEMENT_ID WHERE SERVICE_ID = '{}' AND ENTITLEMENT_TYPE = 'VALUE DRIVER' AND PRENTL.ENTITLEMENT_ID NOT IN ('AGS_Z0091_VAL_UPIMPV', 'AGS_Z0091_VAL_CSTSEG', 'AGS_Z0091_VAL_SVCCMP', 'AGS_Z0091_VAL_QLYREQ') AND ENTITLEMENTLEVEL_NAME = 'OFFERING FAB GREENBOOK TOOL LEVEL' AND PRENTL.ENTITLEMENT_ID NOT IN (SELECT ENTITLEMENT_ID from PRENLI (NOLOCK) WHERE ENTITLEMENTLEVEL_NAME IN ('OFFERING LEVEL')) ".format(get_serviceid) )
				val_list = [i.ENTITLEMENT_ID for i in get_valuedriver_ids]
				if get_valuedriver_ids:
					lst = str(tuple([i.ENTITLEMENT_ID for i in get_valuedriver_ids])).replace(",)",')')
					get_coeffi = Sql.GetList("SELECT ENTITLEMENT_ID from PRENTL (NOLOCK) where SERVICE_ID = '{}' AND PAR_ENPAR_ENTITLEMENT_ID in {} ".format(get_serviceid ,lst) )
					val_coeff = [i.ENTITLEMENT_ID for i in get_coeffi]
					val_list.extend(val_coeff)
				Log.Info("val_list--equp-"+str(val_list))
				for value in GetXMLsecField:
					get_value = value.ENTITLEMENT_DISPLAY_VALUE
					get_cost_impact = value.ENTITLEMENT_COST_IMPACT
					get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
					get_calc_factor = value.CALCULATION_FACTOR
					get_currency = value.PRICE_METHOD
					####value driver
					get_previous_xml = Sql.GetFirst("SELECT ENTITLEMENT_XML FROM {} {}".format(obj, where_condition))
						
					if value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' and 'AGS_LAB_OPT' in value.ENTITLEMENT_ID and 'Z0016' in get_serviceid:
						if get_value_query and value.ENTITLEMENT_DISPLAY_VALUE:
							get_val = float(value.ENTITLEMENT_DISPLAY_VALUE) / float(get_value_query.cnt)
							grnbk_dict[value.ENTITLEMENT_ID] = get_val
							if value.ENTITLEMENT_COST_IMPACT and get_val:
								get_price_impact = get_val * float(value.ENTITLEMENT_COST_IMPACT)
							else:
								get_price_impact = 0.00
							get_calc_factor = get_value = round(get_val,2)
					get_desc = value.ENTITLEMENT_DESCRIPTION
					get_code = value.ENTITLEMENT_VALUE_CODE
					###updating exisitng value for non editable value drivers
					if val_list and get_previous_xml and  value.ENTITLEMENT_ID in val_list:
						get_val_list =re.findall(r''+str(value.ENTITLEMENT_ID)+'<[\w\W]*?</ENTITLEMENT_DISPLAY_VALUE>',get_previous_xml.ENTITLEMENT_XML)
						
						get_code = re.findall( re.compile(r'<ENTITLEMENT_VALUE_CODE>([^>]*?)</ENTITLEMENT_VALUE_CODE>'), get_val_list[0] )[0]
						get_value = re.findall( re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>'), get_val_list[0] )[0]
					updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
						<ENTITLEMENT_ID>{ent_name}</ENTITLEMENT_ID>
						<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
						<ENTITLEMENT_DESCRIPTION>{tool_desc}</ENTITLEMENT_DESCRIPTION>
						<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
						<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
						<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
						<IS_DEFAULT>{is_default}</IS_DEFAULT>
						<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
						<PRICE_METHOD>{pm}</PRICE_METHOD>
						<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
						<ENTITLEMENT_NAME>{ent_desc}</ENTITLEMENT_NAME>
						</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_ID,ent_val_code = get_code.replace("'","''") if  "'" in str(get_code) and value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' else get_code, ent_disp_val = get_value.replace("'","''") if  "'" in str(get_value) else get_value,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_NAME ,pm = value.PRICE_METHOD ,cf= get_calc_factor , ent_type = value.ENTITLEMENT_TYPE,tool_desc= get_desc.replace("'","''") if "'" in get_desc else get_desc) 
				UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
				Sql.RunQuery(UpdateEntitlement)

				##temp table creation for z0016
				if 'Z0016' in get_serviceid:
					where_condition = SAQITMWhere.replace('A.','').replace("'","''")
				
					ent_temp = "SAQSCE_ENT1_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)
					ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
					Sql.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><QTEREV_RECORD_ID>''+QTEREV_RECORD_ID+''</QTEREV_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><FABLOCATION_ID>''+FABLOCATION_ID+''</FABLOCATION_ID><GREENBOOK>''+GREENBOOK+''</GREENBOOK><EQUIPMENT_ID>''+equipment_id+''</EQUIPMENT_ID>'' AS sml,replace(replace(replace(replace(entitlement_xml,''&'','';#38''),'''','';#39''),'' < '','' &lt; ''),'' > '','' &gt; '')  as entitlement_xml from SAQSCE(nolock) "+str(where_condition)+" )A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,EQUIPMENT_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,FABLOCATION_ID,GREENBOOK,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_PRICE_IMPACT,IS_DEFAULT,ENTITLEMENT_TYPE,ENTITLEMENT_DESCRIPTION,PRICE_METHOD,CALCULATION_FACTOR INTO "+str(ent_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',QTEREV_RECORD_ID VARCHAR(100) ''QTEREV_RECORD_ID'',EQUIPMENT_ID VARCHAR(100) ''EQUIPMENT_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',FABLOCATION_ID VARCHAR(100) ''FABLOCATION_ID'',GREENBOOK VARCHAR(100) ''GREENBOOK'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_DESCRIPTION VARCHAR(100) ''ENTITLEMENT_DESCRIPTION'',PRICE_METHOD VARCHAR(100) ''PRICE_METHOD'',CALCULATION_FACTOR VARCHAR(100) ''CALCULATION_FACTOR'') ; exec sys.sp_xml_removedocument @H; '")



			else:
				Log.Info('else part roll down'+str(objectName)+'--'+str(obj)+'--'+str(join)+'--'+str(where))
				update_field_str = ""
				if obj == 'SAQSAE':
					update_query = """ UPDATE TGT 
					SET TGT.ENTITLEMENT_XML = SRC.ENTITLEMENT_XML,
					TGT.CPS_MATCH_ID = SRC.CPS_MATCH_ID,
					TGT.CPS_CONFIGURATION_ID = SRC.CPS_CONFIGURATION_ID,
					TGT.CpqTableEntryModifiedBy = {},
					TGT.CpqTableEntryDateModified = '{}',
					TGT.CONFIGURATION_STATUS = '{}'
					FROM {} (NOLOCK) SRC JOIN {} (NOLOCK) TGT 
					ON  TGT.QUOTE_RECORD_ID = SRC.QUOTE_RECORD_ID AND TGT.QTEREV_RECORD_ID = SRC.QTEREV_RECORD_ID AND TGT.SERVICE_ID = SRC.SERVICE_ID {} {} """.format(userid,datetimenow,getinnercon.CONFIGURATION_STATUS,'SAQSCE',obj,join,where)
					Log.Info('update_query--863----'+str(update_query))
					Sql.RunQuery(update_query)
				else:
					update_query = """ UPDATE TGT 
					SET TGT.ENTITLEMENT_XML = SRC.ENTITLEMENT_XML,
					TGT.CPS_MATCH_ID = SRC.CPS_MATCH_ID,
					TGT.CPS_CONFIGURATION_ID = SRC.CPS_CONFIGURATION_ID,
					TGT.CpqTableEntryModifiedBy = {},
					TGT.CpqTableEntryDateModified = '{}'
					{}
					FROM {} (NOLOCK) SRC JOIN {} (NOLOCK) TGT 
					ON  TGT.QUOTE_RECORD_ID = SRC.QUOTE_RECORD_ID AND TGT.QTEREV_RECORD_ID = SRC.QTEREV_RECORD_ID AND TGT.SERVICE_ID = SRC.SERVICE_ID {} {} """.format(userid,datetimenow,update_field_str,objectName,obj,join,where)
					Sql.RunQuery(update_query)

					

			##roll down and up for all levels ends

			if (obj == "SAQSCE" or objectName == "SAQSCE"):            
				where_string_splitted = ''
				where_str = where.split('AND')
				if where_str:
					where_string_splitted = 'AND'.join(where_str[0:2])
				Log.Info("""UPDATE SAQSCE
									SET
									ENTITLEMENT_GROUP_ID = OQ.RowNo                            
									FROM SAQSCE (NOLOCK)
									INNER JOIN (
										SELECT *, ROW_NUMBER()OVER(ORDER BY IQ.QUOTE_RECORD_ID) AS RowNo  FROM (
										SELECT DISTINCT SRC.QUOTE_RECORD_ID,SRC.QTEREV_RECORD_ID, SRC.SERVICE_ID, SRC.ENTITLEMENT_XML
										FROM SAQSCE (NOLOCK) SRC
										JOIN MAMTRL ON MAMTRL.SAP_PART_NUMBER = SRC.SERVICE_ID AND MAMTRL.SERVICE_TYPE = 'NON TOOL BASED'
										{WhereString} )AS IQ
									)AS OQ
									ON OQ.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND OQ.SERVICE_ID = SAQSCE.SERVICE_ID AND OQ.ENTITLEMENT_XML = SAQSCE.ENTITLEMENT_XML AND OQ.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID""".format(WhereString=where_string_splitted))
				Sql.RunQuery("""UPDATE SAQSCE
									SET
									ENTITLEMENT_GROUP_ID = OQ.RowNo
									FROM SAQSCE (NOLOCK)
									INNER JOIN (
										SELECT *, ROW_NUMBER()OVER(ORDER BY IQ.QUOTE_RECORD_ID) AS RowNo  FROM (
										SELECT DISTINCT SRC.QUOTE_RECORD_ID,SRC.QTEREV_RECORD_ID, SRC.SERVICE_ID, SRC.ENTITLEMENT_XML
										FROM SAQSCE (NOLOCK) SRC
										JOIN MAMTRL ON MAMTRL.SAP_PART_NUMBER = SRC.SERVICE_ID AND MAMTRL.SERVICE_TYPE = 'NON TOOL BASED'
										{WhereString} )AS IQ
									)AS OQ
									ON OQ.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND OQ.SERVICE_ID = SAQSCE.SERVICE_ID AND OQ.ENTITLEMENT_XML = SAQSCE.ENTITLEMENT_XML AND OQ.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID""".format(WhereString=where_string_splitted))
				Sql.RunQuery("""UPDATE SAQSCE
									SET								
									IS_CHANGED = 1                            
									FROM SAQSCE (NOLOCK) SRC
									{WhereString}								
									""".format(WhereString=where_string_splitted))
				# Is Changed Information Notification - Start
				quote_item_obj = Sql.GetFirst("SELECT QUOTE_ITEM_RECORD_ID FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID= '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{revision_id}'".format(QuoteRecordId=getinnercon.QUOTE_RECORD_ID,revision_id = getinnercon.QTEREV_RECORD_ID))		
				if quote_item_obj:
					Sql.RunQuery("DELETE SYELOG FROM SYELOG (NOLOCK) INNER JOIN SYMSGS (NOLOCK) ON SYMSGS.RECORD_ID = SYELOG.ERRORMESSAGE_RECORD_ID AND SYMSGS.TRACK_HISTORY = 0 WHERE SYMSGS.MESSAGE_CODE = '200112' AND SYMSGS.OBJECT_APINAME = 'SAQSCE' AND SYMSGS.MESSAGE_LEVEL = 'INFORMATION' AND SYELOG.OBJECT_VALUE_REC_ID = '{}'".format(getinnercon.QUOTE_RECORD_ID))

					Sql.RunQuery("""INSERT SYELOG (ERROR_LOGS_RECORD_ID, ERRORMESSAGE_RECORD_ID, ERRORMESSAGE_DESCRIPTION, OBJECT_NAME, OBJECT_TYPE, OBJECT_RECORD_ID, OBJECT_VALUE_REC_ID, OBJECT_VALUE, ACTIVE, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
									SELECT
										CONVERT(VARCHAR(4000),NEWID()) as ERROR_LOGS_RECORD_ID, 
										RECORD_ID as ERRORMESSAGE_RECORD_ID,
										MESSAGE_TEXT as ERRORMESSAGE_DESCRIPTION,
										OBJECT_APINAME as OBJECT_NAME,
										MESSAGE_TYPE as OBJECT_TYPE,
										OBJECT_RECORD_ID as OBJECT_RECORD_ID,
										'{QuoteRecordId}' as OBJECT_VALUE_REC_ID,
										'{QuoteId}' as OBJECT_VALUE,
										1 as ACTIVE,
										'{UserId}' as CPQTABLEENTRYADDEDBY, 
										'{DateTimeValue}' as CPQTABLEENTRYDATEADDED, 
										'{UserId}' as CpqTableEntryModifiedBy, 
										'{DateTimeValue}' as CpqTableEntryDateModified
									FROM SYMSGS (nolock)
									WHERE OBJECT_APINAME = 'SAQSCE' AND MESSAGE_LEVEL = 'INFORMATION' AND MESSAGE_CODE = '200112'
								""".format(
									QuoteRecordId=getinnercon.QUOTE_RECORD_ID,
									QuoteId=getinnercon.QUOTE_ID,
									UserId=userId,
									DateTimeValue=datetimenow
								))
				# Is Changed Information Notification - End

			
			
		
		##rollup for pricing
		if 'Z0016' in get_serviceid and objectName != 'SAQTSE':
			entitlement_price_rollup(objectName, ent_temp)
		##ancillary_service insert
		if 'Z0091' in get_serviceid and ancillary_flag == 'YES':
			ancillary_service_Z0046(get_serviceid)
		sendEmail(level)

	except Exception as e:
		Log.Info("error on roll down--"+str(e)+'--'+str(str(sys.exc_info()[-1].tb_lineno)))
		ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")	
		ent_temp_drop1 = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_roll_temp)+"'' ) BEGIN DROP TABLE "+str(ent_roll_temp)+" END  ' ")	
	
	try:
		pattern = re.compile(r'QUOTE_RECORD_ID\s*\=\s*\'([^>]*?)\'')
		result = re.search(pattern, where).group(1)
		quote_obj = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(result))
		if quote_obj:
			Quote = QuoteHelper.Edit(quote_obj.QUOTE_ID)	
	except Exception:
		Log.Info("Exception in Quote Edit") 

	try:
		data = ScriptExecutor.ExecuteGlobal("CQINSQTITM",{"WhereString":where, "ActionType":'UPDATE_LINE_ITEMS'})
	except Exception:
		Log.Info("Exception in Quote Item insert") 



level = ""
if objectName == 'SAQTSE':
	level = "Offering Entitlement "
elif objectName == 'SAQSFE':
	level = "Fab Location Entitlement "
elif objectName == 'SAQSGE':
	level = "Greenbook Entitlement "
elif objectName == "SAQSCE":
	level = "Equipment Entitlement "
elif objectName == "SAQSAE":
	level = "Assembly Entitlement "
Log.Info("level1---"+str(level))
where_cond = where.replace('SRC.','')
getinnercon  = Sql.GetFirst("select QUOTE_RECORD_ID,QTEREV_RECORD_ID,QUOTE_ID,CPS_MATCH_ID,CPS_CONFIGURATION_ID,CONFIGURATION_STATUS from "+str(objectName)+" (nolock) "+str(where_cond)+"")

##get c4c quote id
get_c4c_quote_id = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(getinnercon.QUOTE_RECORD_ID,getinnercon.QTEREV_RECORD_ID))
###SAQSCE temp table
ent_temp = ""
if 'Z0007' in get_serviceid or ('Z0016' in get_serviceid and objectName == 'SAQSCE'):
	where_condition = SAQITMWhere.replace('A.','').replace("'","''")

	ent_temp = "SAQSCE_ENT_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)
	ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
	Sql.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><QTEREV_RECORD_ID>''+QTEREV_RECORD_ID+''</QTEREV_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><FABLOCATION_ID>''+FABLOCATION_ID+''</FABLOCATION_ID><GREENBOOK>''+GREENBOOK+''</GREENBOOK><EQUIPMENT_ID>''+equipment_id+''</EQUIPMENT_ID>'' AS sml,replace(replace(replace(replace(entitlement_xml,''&'','';#38''),'''','';#39''),'' < '','' &lt; ''),'' > '','' &gt; '')  as entitlement_xml from SAQSCE(nolock) "+str(where_condition)+" )A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,EQUIPMENT_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,FABLOCATION_ID,GREENBOOK,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_PRICE_IMPACT,IS_DEFAULT,ENTITLEMENT_TYPE,ENTITLEMENT_DESCRIPTION,PRICE_METHOD,CALCULATION_FACTOR INTO "+str(ent_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',QTEREV_RECORD_ID VARCHAR(100) ''QTEREV_RECORD_ID'',EQUIPMENT_ID VARCHAR(100) ''EQUIPMENT_ID'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',FABLOCATION_ID VARCHAR(100) ''FABLOCATION_ID'',GREENBOOK VARCHAR(100) ''GREENBOOK'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_DESCRIPTION VARCHAR(100) ''ENTITLEMENT_DESCRIPTION'',PRICE_METHOD VARCHAR(100) ''PRICE_METHOD'',CALCULATION_FACTOR VARCHAR(100) ''CALCULATION_FACTOR'') ; exec sys.sp_xml_removedocument @H; '")



where_conditn = where_cond.replace("'","''")
ent_roll_temp = "ENT_ROLL_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)
ent_temp_drop1 = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_roll_temp)+"'' ) BEGIN DROP TABLE "+str(ent_roll_temp)+" END  ' ")
Sql.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select distinct ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><QTEREV_RECORD_ID>''+QTEREV_RECORD_ID+''</QTEREV_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID>'' AS sml,replace(replace(replace(replace(entitlement_xml,''&'','';#38''),'''','';#39''),'' < '','' &lt; ''),'' > '','' &gt; '')  as entitlement_xml from "+str(objectName)+"(nolock) "+str(where_conditn)+" )A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_PRICE_IMPACT,IS_DEFAULT,ENTITLEMENT_TYPE,ENTITLEMENT_DESCRIPTION,PRICE_METHOD,CALCULATION_FACTOR INTO "+str(ent_roll_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',QTEREV_RECORD_ID VARCHAR(100) ''QTEREV_RECORD_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_DESCRIPTION VARCHAR(100) ''ENTITLEMENT_DESCRIPTION'',PRICE_METHOD VARCHAR(100) ''PRICE_METHOD'',CALCULATION_FACTOR VARCHAR(100) ''CALCULATION_FACTOR'') ; exec sys.sp_xml_removedocument @H; '")

GetXMLsecField = Sql.GetList("SELECT * from {} ".format(ent_roll_temp))

#calling rolldown

entitlement_rolldown(objectName,get_serviceid,where,ent_temp)

if ent_temp:
	ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
if ent_roll_temp:
	ent_temp_drop1 = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_roll_temp)+"'' ) BEGIN DROP TABLE "+str(ent_roll_temp)+" END  ' ")

