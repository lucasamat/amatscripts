# =========================================================================================================================================
#   __script_name :SYPOSAVEAL.PY
#   __script_description : THIS SCRIPT IS USED WHEN SAVING A RELATED LIST RECORD.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
# GS_POPUP_SAVE_ALL

import SYTABACTIN as Table
import SYCNGEGUID as CPQID
from SYDATABASE import SQL

Sql = SQL()
#import PRCTPRFPBE

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
#import PRIFLWTRGR
#import PRGRPRBKEN

#from PAUPDDRYFG import DirtyFlag
import datetime




def Calcfctrs(TreeParam, Treeparent, TreesuperParent, TopParentparam, query_result, old_query_result, TABLE_ID):
    Flag = 1
    final_levels = ""

    Pricing_levels = {
        "Price Classes": "PRICE MODEL CLASS|MODCLS_RECORD_ID|FACTOR_VAROBJREC_RECORD_ID",
        "Price Model Classes": "PRICE MODEL CLASS|MODCLS_RECORD_ID|FACTOR_VAROBJREC_RECORD_ID",
        "Pricebooks": "PRICEBOOK|LIST_PRICEBOOK_RECORD_ID|FACTOR_VAROBJREC_RECORD_ID",
        "Price Methods": "PRICEBOOK MATERIAL|PRICEBOOK_MATERIAL_RECORD_ID|FACTOR_VAROBJREC_RECORD_ID",
        "Pricebook Entry Information": "PRICEBOOK ENTRY|LIST_PRICEBOOK_ENTRY_RECORD_ID|FACTOR_VAROBJREC_RECORD_ID",
        "Price Class Information": "PRICE CLASS|PRICECLASS_ID|FACTOR_VAROBJREC_ID",
    }

    Ideal_rolldown = [
        "CALCULATION FACTOR",
        "PRICE CLASS",
        "PRICE MODEL CLASS",
        "PRICEBOOK MATERIAL",
        "SALES ORG PRICE CLASS",
        "PRICEBOOK",
        "PRICEBOOK ENTRY",
        "SEGMENT_REVISION_PRODUCT",
    ]

    


    TreesuperParent = "Price Model Classes" if TreesuperParent == "Price Classes" else TreesuperParent
    Treeparent = "Price Methods" if Treeparent == "Materials In Pricing Procedure" else Treeparent


    value = (
        str(query_result.get("FACTOR_NUMVAR"))
        if str(query_result.get("FACTOR_DATATYPE")) == "NUMBER"
        else (
            str(query_result.get("FACTOR_PCTVAR"))
            if str(query_result.get("FACTOR_DATATYPE")) == "PERCENT"
            else str(query_result.get("FACTOR_CURVAR"))
        )
    )
    
    valueget = value
    old_value = (
        str(old_query_result.get("FACTOR_NUMVAR"))
        if str(old_query_result.get("FACTOR_DATATYPE")) == "NUMBER"
        else (
            str(old_query_result.get("FACTOR_PCTVAR"))
            if str(old_query_result.get("FACTOR_DATATYPE")) == "PERCENT"
            else str(old_query_result.get("FACTOR_CURVAR"))
        )
    )


    if float(value) != float(old_value):
        Flag = 0
        query_result.update({"FACTOR_STATUS": "TRUE"})
        table_PRCFVA = SqlHelper.GetTable("PRCFVA")
        table_PRCFVA.AddRow(query_result)
        SqlHelper.Upsert(table_PRCFVA)

    if Flag == 0:
        if TopParentparam in Pricing_levels.keys():
            level = str(Pricing_levels.get(TopParentparam)).split("|")[0]
            apiname = str(Pricing_levels.get(TopParentparam)).split("|")[1]
            value = str(query_result.get(str(Pricing_levels.get(TopParentparam)).split("|")[2]))

        elif TreesuperParent in Pricing_levels.keys():
            level = str(Pricing_levels.get(TreesuperParent)).split("|")[0]
            apiname = str(Pricing_levels.get(TreesuperParent)).split("|")[1]
            value = str(query_result.get(str(Pricing_levels.get(TreesuperParent)).split("|")[2]))

        elif Treeparent in Pricing_levels.keys():
            level = str(Pricing_levels.get(Treeparent)).split("|")[0]
            apiname = str(Pricing_levels.get(Treeparent)).split("|")[1]
            value = str(query_result.get(str(Pricing_levels.get(Treeparent)).split("|")[2]))

        elif TreeParam in Pricing_levels.keys():
            level = str(Pricing_levels.get(TreeParam)).split("|")[0]
            apiname = str(Pricing_levels.get(TreeParam)).split("|")[1]
            value = str(query_result.get(str(Pricing_levels.get(TreeParam)).split("|")[2]))

        else:
            level = ""
            apiname = ""
            value = ""

        if level in Levels:
            del Ideal_rolldown[: int(Ideal_rolldown.index(level)) + 1]

        final_levels = ",".join([lvl for lvl in Ideal_rolldown if lvl in Levels])
        


    return ""


'''@DirtyFlag(
    access_from="ADD_PLANT",
    revision_id=Product.GetGlobal("segmentRevisionId"),
    segment_record_id=Product.GetGlobal("segment_rec_id"),
)'''
def do_process(TABLEID, LABLE, VALUE):
    
    # Trace.Write("VALUE------------" + str(VALUE))
    # Trace.Write("TABLEID------------" + str(TABLEID))
    # Trace.Write("LABLE------------" + str(LABLE))

    if len(VALUE) > 0:
        if VALUE[0] != "":
            OBJNAME = VALUE[0].split("-")
            VALUE[0] = CPQID.KeyCPQId.GetKEYId(str(OBJNAME[0]), str(VALUE[0]))

    CONT_VALUE = ""
    CONT_TABLEID = ""
    RECORDID = ""
    try:
        CONT_LABLE = list(Param.CONT_LABLE)
    except:
        Trace.Write("err")
    try:
        CONT_VALUE = list(Param.CONT_VALUE)
    except:
        Trace.Write("err")
    try:
        CONT_TABLEID = Param.CONT_TABLEID
    except:
        Trace.Write("err")
    try:
        RECORDID = Param.RECORDID
    except:
        Trace.Write("err")
    try:
        RECORDFEILD = Param.RECORDFEILD
    except:
        Trace.Write("err")
    try:
        COUNTRIES = list(Param.Countries)
    except:
        Trace.Write("errorr")
    try:
        Treeparam = Param.TreeParam
        Treeparentparam = Param.TreeParentParam
        Treesuperparentparam = Param.TreeSuperParentParam
        treetopparentparam = Param.TopSuperParentParam
    except:
        Treeparam = ""
        Treeparentparam = ""
        Treesuperparentparam = ""
        treetopparentparam = ""


    FIXED_FACTOR_ISCHNAGED = 0
    MARKUP_FACTOR_ISCHNAGED = 0
    LOWPRCADJ_FACTOR_ISCHNAGED = 0
    LIST_PRICE_ISCHNAGED = 0
    GPA_FACTOR_ISCHNAGED = 0
    SPA_FACTOR_ISCHNAGED = 0
    err_msg = ""
    err_display=""
    Flag_unique = "True"

    Recodrid = ""
    if len(VALUE) > 0:
        Recodrid = VALUE[0]
    val_code = ""

    if len(VALUE) > 0:
        oper = VALUE[0]
    new_val = ""
    result = ""
    next_id = ""
    flag = 0
    validation = ""
    Req_Flag = 0
    
    req_obj = Sql.GetList(
        "select API_NAME,DATA_TYPE,LENGTH,REQUIRED from  SYOBJD(NOLOCK) where OBJECT_NAME = '" + str(TABLEID) + "' "
    )
    if req_obj is not None and len(req_obj) > 0:
        required_val = [str(i.API_NAME) for i in req_obj if str(i.REQUIRED).lower()=="true"]
        err_display+="$('.err_msgs').text('');"
        for data, datas in zip(LABLE, VALUE):
            if data in required_val and (datas == "" or datas is None or datas == '..Select') and TABLEID != "MAMAFC" and TABLEID != "CMQTCL":
                Req_Flag = 1
                err_display+="$('#"+str(data)+"_err').html('<span style=\"color:red\">Required Field</span>'); "
            for i in req_obj:
                if i.API_NAME==data and i.LENGTH and len(datas)>i.LENGTH:
                    err_display+="$('#"+str(data)+"_err').html('<span style=\"color:red\">Length exceeded "+str(i.LENGTH)+"</span>'); "
                elif datas!="" and i.API_NAME==data and i.DATA_TYPE=='NUMBER' and not datas.isdigit():
                    err_display+="$('#"+str(data)+"_err').html('<span style=\"color:red\">No Alphabets or Special Characters</span>'); "
        if Req_Flag==1:
            err_msg = '<div class="col-md-12" id="PageAlert" ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert_notifcatio6" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert_notifcatio6" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"  ><label ><img src="/mt/OCTANNER_DEV/Additionalfiles/stopicon1.svg" alt="Error"> ERROR : You will not be able to save your data until all required fields are populated </label></div></div></div>'
        else:
            err_msg = ""
    Chkctry = ""
    for tab in Product.Tabs:
        if tab.Name == "Country" and Product.Tabs.GetByName(tab.Name).IsSelected:
            Chkctry = "true"
    if flag == 0 and len(VALUE) >= 0:
        
        if VALUE[0] is None or VALUE[0] == "":
            
            CONT_LABLE = []
            CONT_VALUE = []
            next_id = Sql.GetFirst("SELECT CONVERT(VARCHAR(4000),NEWID()) AS REC_ID")
            new_val = str(next_id.REC_ID)
            Lable_obj = Sql.GetFirst("SELECT FIELD_LABEL FROM  SYOBJD(NOLOCK) WHERE API_NAME='" + str(LABLE[0]) + "'")
            Trace.Write("SELECT FIELD_LABEL FROM  SYOBJD(NOLOCK) WHERE API_NAME='" + str(LABLE[0]) + "'")
            if Lable_obj is not None:
                lable = eval(str("Lable_obj.FIELD_LABEL"))
                VALUE[0] = new_val
                CONT_TABLEID = CONT_TABLEID.split("__")
                
                CONT_TABLEID = CONT_TABLEID[1]
                CONT_VALUE.insert(1, new_val)
                CONT_VALUE.insert(2, new_val)
                CONT_LABLE.insert(1, lable)
                CONT_LABLE.insert(2, lable)



            
            row = dict(zip(LABLE, VALUE))
            ##auto populate SAPCPQ_ATTRIBUTE_NAME starts
            
            if str(TABLEID) == "SYSECT":
                
                primary_obj_rec=Sql.GetFirst("SELECT RECORD_ID from SYOBJH where OBJECT_NAME = '"+str(row["PRIMARY_OBJECT_NAME"])+"'")
                row["PRIMARY_OBJECT_RECORD_ID"]=str(primary_obj_rec.RECORD_ID)
                page_rec_id=Sql.GetFirst("SELECT RECORD_ID from SYPAGE where PAGE_NAME = '"+str(row["PAGE_NAME"])+"'")
                row["PAGE_RECORD_ID"]=str(page_rec_id.RECORD_ID)
            #Trace.Write("------1904----" + str(TABLEID)+str(row))
            try:
                
                if ("SAPCPQ_ATTRIBUTE_NAME") in row and str(TABLEID) == "SYPSAC":
                    if str(row.get("TAB_RECORD_ID")) != "":
                        sytabs_app_id = Sql.GetFirst("SELECT APP_ID FROM SYPSAC (NOLOCK) WHERE TAB_RECORD_ID = '{}'".format(str(row.get("TAB_RECORD_ID"))))
                        APP_ID = "SYPSAC-{}-".format(sytabs_app_id.APP_ID)
                        cpq_attr_name = Sql.GetFirst("SELECT max(SAPCPQ_ATTRIBUTE_NAME) AS SAPCPQ_ATTRIBUTE_NAME FROM SYPSAC (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME like '{}%'".format(str(APP_ID)))
                        if sytabs_app_id is not None and cpq_attr_name is not None:
                            x = cpq_attr_name.SAPCPQ_ATTRIBUTE_NAME.split("-")
                            length = len(x[len(x)-1])
                            row["SAPCPQ_ATTRIBUTE_NAME"] = str(APP_ID)+ str(int(x[len(x)-1])+1).zfill(length)
                elif ("SAPCPQ_ATTRIBUTE_NAME" in row) and str(TABLEID) == "SYTABS":
                    if (str(row["APP_ID"]) != ""):
                        APP_ID = str(TABLEID)+"-"+str(row["APP_ID"])+"-"
                        cpq_attr_name = Sql.GetFirst("SELECT max(SAPCPQ_ATTRIBUTE_NAME) AS SAPCPQ_ATTRIBUTE_NAME FROM SYTABS (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME like '{}%'".format(str(APP_ID)))
                        x = cpq_attr_name.SAPCPQ_ATTRIBUTE_NAME.split("-")
                        length = len(x[len(x)-1])
                        row["SAPCPQ_ATTRIBUTE_NAME"] = str(APP_ID)+ str(int(x[len(x)-1])+1).zfill(length)
                        
                elif ("SAPCPQ_ATTRIBUTE_NAME" in row) and str(TABLEID) == "SYOBJD":
                    cpq_attr_name = Sql.GetFirst("SELECT max(SAPCPQ_ATTRIBUTE_NAME) AS SAPCPQ_ATTRIBUTE_NAME FROM SYOBJD (NOLOCK)")
                    x = cpq_attr_name.SAPCPQ_ATTRIBUTE_NAME.split("-")
                    length = len(x[len(x)-1])
                    row["SAPCPQ_ATTRIBUTE_NAME"] = "SYOBJD-"+ str(int(x[len(x)-1])+1).zfill(length)
                
                elif ("SAPCPQ_ATTRIBUTE_NAME" in row) and str(TABLEID) == "SYSECT":
                    if str(row.get("PAGE_RECORD_ID")) != "":
                        sypage_app_id = Sql.GetFirst("SELECT APP_ID FROM SYPAGE (NOLOCK) INNER JOIN SYTABS (NOLOCK) ON SYTABS.RECORD_ID = SYPAGE.TAB_RECORD_ID WHERE SYPAGE.RECORD_ID = '{}'".format(str(row.get("PAGE_RECORD_ID"))))
                        APP_ID = "SYSECT-{}-".format(sypage_app_id.APP_ID)
                        cpq_attr_name = Sql.GetFirst("SELECT max(SAPCPQ_ATTRIBUTE_NAME) AS SAPCPQ_ATTRIBUTE_NAME FROM SYSECT (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME like '{}%'".format(str(APP_ID)))
                        if sypage_app_id is not None and cpq_attr_name is not None:
                            x = cpq_attr_name.SAPCPQ_ATTRIBUTE_NAME.split("-")
                            length = len(x[len(x)-1])
                            row["SAPCPQ_ATTRIBUTE_NAME"] = str(APP_ID)+ str(int(x[len(x)-1])+1).zfill(length)
                elif ("SAPCPQ_ATTRIBUTE_NAME") in row and str(TABLEID) == "SYPGAC":
                    if str(row.get("TAB_RECORD_ID")) != "":
                        sytabs_app_id = Sql.GetFirst("SELECT APP_ID FROM SYPGAC (NOLOCK) WHERE TAB_RECORD_ID = '{}'".format(str(row.get("TAB_RECORD_ID"))))
                        APP_ID = "SYPGAC-{}-".format(sytabs_app_id.APP_ID)
                        cpq_attr_name = Sql.GetFirst("SELECT max(SAPCPQ_ATTRIBUTE_NAME) AS SAPCPQ_ATTRIBUTE_NAME FROM SYPGAC (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME like '{}%'".format(str(APP_ID)))
                        if sytabs_app_id is not None and cpq_attr_name is not None:
                            x = cpq_attr_name.SAPCPQ_ATTRIBUTE_NAME.split("-")
                            length = len(x[len(x)-1])
                            row["SAPCPQ_ATTRIBUTE_NAME"] = str(APP_ID)+ str(int(x[len(x)-1])+1).zfill(length)
                elif ("SAPCPQ_ATTRIBUTE_NAME" in row) and str(TABLEID) == "SYSEFL":
                    sysefl_app_id = Product.Attributes.GetByName('QSTN_SYSEFL_SY_00153').GetValue()   
                    if sysefl_app_id != "":
                        APP_ID = "SYSEFL-{}-".format(sysefl_app_id)
                        
                        cpq_attr_name = Sql.GetFirst("SELECT max(SAPCPQ_ATTRIBUTE_NAME) AS SAPCPQ_ATTRIBUTE_NAME FROM SYSEFL (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME like '{}%'".format(str(APP_ID)))
                        
                        if sysefl_app_id is not None and cpq_attr_name is not None:
                            x = cpq_attr_name.SAPCPQ_ATTRIBUTE_NAME.split("-")
                            length = len(x[len(x)-1])
                            row["SAPCPQ_ATTRIBUTE_NAME"] = str(APP_ID)+ str(int(x[len(x)-1])+1).zfill(length)
                            Trace.Write("APP_ID---->" + str(row["SAPCPQ_ATTRIBUTE_NAME"]))
            except:
                Trace.Write("Table--"+str(TABLEID))
                Trace.Write("exept cpq")
            
            ##auto populate SAPCPQ_ATTRIBUTE_NAME ends
            if str(TABLEID) == "SYTRND":
                if ("NODE_NAME" in row):
                    row["NODE_NAME"] = row["NODE_NAME"].title()
            elif str(TABLEID) == "SYPGAC":
                if ("ACTION_NAME" in row):
                    row["ACTION_NAME"] = row["ACTION_NAME"].title()

                 


        Trace.Write("row-=======> " + str(row))
        
        if oper is None or oper == "" and Req_Flag == 0:

            if str(TABLEID).strip() == "SYROUS":
                userid = ""
                ROLE_ID = row["ROLE_ID"]
                role_rec_val = Sql.GetFirst("SELECT ROLE_RECORD_ID FROM  SYROMA(NOLOCK) WHERE ROLE_ID='" + ROLE_ID + "'")
                userid_obj = Sql.GetFirst("SELECT ID FROM USERS WHERE NAME = '{}'".format(row["USER_NAME"]))
                if userid_obj:
                    userid = userid_obj.ID
                else:
                    userid = ""
                row["ROLE_USER_RECORD_ID"] = str(Guid.NewGuid()).upper()
                row["USER_RECORD_ID"] = userid
                if role_rec_val:
                    row["ROLE_RECORD_ID"] = role_rec_val.ROLE_RECORD_ID
                Trace.Write("Row-SYROUS----->" + str(row))

            if str(TABLEID).strip() == "SYOBJC":
                row["OBJECT_CONSTRAINT_RECORD_ID"] = str(Guid.NewGuid()).upper()
                
            if Flag_unique == "True":

                if "CpqTableEntryModifiedBy" in row.keys() and "CpqTableEntryDateModified" in row.keys():
                    if TABLEID == 'SAQTIP':
                        ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
                        # quote_val=Sql.GetFirst("SELECT MASTER_TABLE_QUOTE_RECORD_ID,QUOTE_NAME FROM SAQTMT WHERE QUOTE_ID = '"+row["QUOTE_ID"]+"'")
                        quote_val=Sql.GetFirst("SELECT MASTER_TABLE_QUOTE_RECORD_ID,QUOTE_NAME FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(ContractRecordId)+"'")
                        row["QUOTE_RECORD_ID"]=quote_val.MASTER_TABLE_QUOTE_RECORD_ID
                        row["QUOTE_NAME"]=quote_val.QUOTE_NAME
                        if row["PARTY_ROLE"] != "..Select":
                            Table.TableActions.Create(TABLEID, row)
                        if row["PARTY_ROLE"] == "RECEIVING ACCOUNT":
                            contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                            sales_org_details = Sql.GetFirst("SELECT SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID FROM SAQTSO (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
                            account_details = Sql.GetFirst("SELECT ACCOUNT_RECORD_ID,CITY,COUNTRY,COUNTRY_RECORD_ID FROM SAACNT (NOLOCK) WHERE ACCOUNT_ID = '"+str(row["PARTY_ID"])+"'")
                            receiving_account_row ={
                                "ACCOUNT_ID": row["PARTY_ID"],
                                "ACCOUNT_NAME": row["PARTY_NAME"],
                                "ACCOUNT_RECORD_ID": account_details.ACCOUNT_RECORD_ID,
                                "QUOTE_ID": row["QUOTE_ID"],
                                "QUOTE_NAME": row["QUOTE_NAME"],
                                "QUOTE_RECORD_ID": str(contract_quote_record_id),
                                "RELOCATION_TYPE": "RECEIVING ACCOUNT",
                                "SALESORG_ID": sales_org_details.SALESORG_ID,
                                "SALESORG_NAME": sales_org_details.SALESORG_NAME,
                                "SALESORG_RECORD_ID": sales_org_details.SALESORG_RECORD_ID,
                                "QUOTE_SENDING_RECEIVING_ACCOUNT": str(Guid.NewGuid()).upper(),
                                "ADDRESS_1": row["ADDRESS"],
                                "ADDRESS_2": "",
                                "CITY": account_details.CITY,
                                "COUNTRY": account_details.COUNTRY,
                                "COUNTRY_RECORD_ID": account_details.COUNTRY_RECORD_ID,
                                "EMAIL": row["EMAIL"],
                                "PHONE": row["PHONE"],
                                "POSTAL_CODE": "",
                                "STATE": "",
                                "STATE_RECORD_ID": ""
                            }
                            Table.TableActions.Create("SAQSRA", receiving_account_row)
                        elif row["PARTY_ROLE"] == "SENDING ACCOUNT":
                            contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                            sales_org_details = Sql.GetFirst("SELECT SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID FROM SAQTSO (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
                            account_details = Sql.GetFirst("SELECT ACCOUNT_RECORD_ID,CITY,COUNTRY,COUNTRY_RECORD_ID FROM SAACNT (NOLOCK) WHERE ACCOUNT_ID = '"+str(row["PARTY_ID"])+"'")
                            receiving_account_row ={
                                "ACCOUNT_ID": row["PARTY_ID"],
                                "ACCOUNT_NAME": row["PARTY_NAME"],
                                "ACCOUNT_RECORD_ID": account_details.ACCOUNT_RECORD_ID,
                                "QUOTE_ID": row["QUOTE_ID"],
                                "QUOTE_NAME": row["QUOTE_NAME"],
                                "QUOTE_RECORD_ID": str(contract_quote_record_id),
                                "RELOCATION_TYPE": "SENDING ACCOUNT",
                                "SALESORG_ID": sales_org_details.SALESORG_ID,
                                "SALESORG_NAME": sales_org_details.SALESORG_NAME,
                                "SALESORG_RECORD_ID": sales_org_details.SALESORG_RECORD_ID,
                                "QUOTE_SENDING_RECEIVING_ACCOUNT": str(Guid.NewGuid()).upper(),
                                "ADDRESS_1": row["ADDRESS"],
                                "ADDRESS_2": "",
                                "CITY": account_details.CITY,
                                "COUNTRY": account_details.COUNTRY,
                                "COUNTRY_RECORD_ID": account_details.COUNTRY_RECORD_ID,
                                "EMAIL": row["EMAIL"],
                                "PHONE": row["PHONE"],
                                "POSTAL_CODE": "",
                                "STATE": "",
                                "STATE_RECORD_ID": ""
                            }
                            Table.TableActions.Create("SAQSRA", receiving_account_row)
                    else:    
                        
                        if TABLEID == "SYTREE":
                            newTableInfo = SqlHelper.GetTable('SYTREE')
                            #Trace.Write("TRACE_TESTZ--inside sytree--save---" + str(row))
                            row["CPQTABLEENTRYADDEDBY"] = User.Id
                            row["CPQTABLEENTRYDATEADDED"] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
                            #Trace.Write("TRACE_TESTZ--inside sytree--save-311-----" + str(row))
                            newTableInfo.AddRow(row)
                            sqlInfo = SqlHelper.Upsert(newTableInfo)
                        else:
                            
                            Table.TableActions.Create(TABLEID, row)

                else:
                    Trace.Write("row lastttttt-=======> " + str(row))

        


    if str(new_val) is not None and str(new_val) != "":
        new_val = row.get(str(LABLE[0]))
        result = ScriptExecutor.ExecuteGlobal(
            "SYPARCEFMA", {"Object": str(TABLEID), "API_Name": LABLE[0], "API_Value": str(new_val)},
        )
        new_value_dict = {API_Names["API_NAME"]: API_Names["FORMULA_RESULT"] for API_Names in result}
        
        if new_value_dict is not None:
            
            if row.get("FACTOR_PCTVAR"):
                
                row["FACTOR_PCTVAR"] = row.get("FACTOR_PCTVAR").strip("%")
            elif row.get("FACTOR_DATATYPE") == "PERCENT":
                row["FACTOR_TXTVAR"] = row.get("FACTOR_PCTVAR")
            elif row.get("APPROVER_SELECTION_METHOD") and str(TABLEID) == 'ACACSA':            
                if row.get("APPROVER_SELECTION_METHOD") == "INDIVIDUAL USERS":                    
                    row["APRCHNSTP_APPROVER_ID"] = "USR-"+str(row.get("USERNAME"))                    
                elif row.get("APPROVER_SELECTION_METHOD").strip() == "GROUP OF USERS" and row.get("PROFILE_ID"):           
                    row["APRCHNSTP_APPROVER_ID"] = "PRO-"+str(row.get("PROFILE_ID"))
                                        
                elif row.get("APPROVER_SELECTION_METHOD").strip() == "GROUP OF USERS" and row.get("ROLE_ID"):               
                    row["APRCHNSTP_APPROVER_ID"] = "ROL-"+str(row.get("ROLE_ID"))
                                       

            elif row.get("APRCHNSTP_NAME"):
                row["APRCHNSTP_NAME"] = row.get("APRCHNSTP_NAME").upper()
            if str(Req_Flag) == "0" and Flag_unique == "True":
            
                
                sql_sgs = Sql.GetFirst(
                    "SELECT API_NAME FROM  SYOBJD(NOLOCK) WHERE DATA_TYPE='AUTO NUMBER' AND OBJECT_NAME = '"
                    + str(TABLEID)
                    + "'"
                )
                autoNo = sql_sgs.API_NAME
                sql_cpq = Sql.GetFirst("SELECT * FROM " + str(TABLEID) + " WHERE " + str(autoNo) + "='" + str(new_val) + "'")
                dictc = {}
                if sql_cpq is not None:
                    dictc = {"CpqTableEntryId": str(sql_cpq.CpqTableEntryId)}
                    row.update(dictc)
                    if "CPQTABLEENTRYMODIFIEDBY" in row.keys() and "CPQTABLEENTRYDATEMODIFIED" in row.keys():
                        row.pop("CPQTABLEENTRYMODIFIEDBY")
                        row.pop("CPQTABLEENTRYDATEMODIFIED")
                    
                    Table.TableActions.Update(TABLEID, LABLE[0], row)
                    
        #for single record index save
        # check indexname exist Start
        if str(TABLEID).strip() == "SYOBJX":
            getindexobj = row.get("OBJECT_APINAME")
            
            # check index query start
            getobjectrec = ""
            try:
                
                DROP_INDEX = Sql.GetList(
                    "SELECT C.NAME AS INDEX_N  FROM sys.index_columns A JOIN SYS.COLUMNS B ON A.COLUMN_ID = B.COLUMN_ID AND A.OBJECT_ID = B.OBJECT_ID JOIN SYS.INDEXES C ON A.INDEX_ID = C.INDEX_ID AND A.OBJECT_ID = C.OBJECT_ID WHERE OBJECT_NAME(A.OBJECT_ID)='"
                    + getindexobj
                    + "'   "
                )
                if len(DROP_INDEX) > 1:
                    for inse in DROP_INDEX:
                        if "PK_" not in inse.INDEX_N:
                            QueryStatement = "DROP INDEX {Index_Name} on {Obj_Name}".format(
                                Index_Name=inse.INDEX_N, Obj_Name=getindexobj
                            )
                            a = Sql.RunQuery(QueryStatement)
            except:
                Trace.Write("DELETE EXISTING INDEX IN EXCEPT")
            # check indexname exist End
            #create index :
            indexquey = Sql.GetList("SELECT top 1000 * FROM  SYOBJX (Nolock) WHERE OBJECT_APINAME ='" + str(getindexobj) + "'")
            if indexquey:
                for val in indexquey:
                    if val.INDEX_EXPRESSION:
                        INDEX_EXPRESSION = val.INDEX_EXPRESSION
                        INDEX_NAME = val.INDEX_NAME
                        QueryStatement = "CREATE INDEX {Index_Name} on {Obj_Name}({Col_Name})".format(
                            Index_Name=INDEX_NAME, Obj_Name=val.OBJECT_APINAME, Col_Name=INDEX_EXPRESSION
                        )
                        try:
                            
                            a = Sql.RunQuery(QueryStatement)
                        except:
                            Trace.Write("Already index Created")
            # create index query end
        #for single record constrainst start-Dhurga
        if str(TABLEID).strip() == "SYOBJC":
            getobjectname = row.get("OBJECT_APINAME")
            getconst_type = row.get("CONSTRAINT_TYPE")
            getrec_id = row.get("OBJECT_CONSTRAINT_RECORD_ID")
            getconst_type = Sql.GetFirst("select CONSTRAINT_TYPE from SYOBJC where OBJECT_CONSTRAINT_RECORD_ID = '"+str(getrec_id)+"'")
            try:
                
                # CREATE NOT NULL Constraint
                if getconst_type == "NOT NULL":
                    try:
                        query_result = Sql.GetFirst(
                            "SELECT OBJECT_APINAME, OBJECTFIELD_APINAME FROM SYOBJC(NOLOCK) CON INNER JOIN [INFORMATION_SCHEMA].[COLUMNS] SCHCON ON SCHCON.TABLE_NAME = CON.OBJECT_APINAME AND SCHCON.COLUMN_NAME = CON.OBJECTFIELD_APINAME AND SCHCON.IS_NULLABLE='YES' WHERE CONSTRAINT_TYPE ='NOT NULL' AND OBJECT_APINAME='"
                            + str(getobjectname)
                            + "' and OBJECT_CONSTRAINT_RECORD_ID = '"+str(getrec_id)+"'"
                        )
                        result = Sql.GetFirst(
                            "sp_executesql @T=N'ALTER TABLE "
                            + query_result.OBJECT_APINAME
                            + " ALTER COLUMN "
                            + query_result.OBJECTFIELD_APINAME
                            + " NVARCHAR(250) NOT NULL'"
                        )
                    except:
                        Trace.Write('not null throwing error')

                

                # CREATE UNIQUE Constraint
                elif getconst_type == "UNIQUE":
                    
                    try:
                        query_result = Sql.GetFirst(
                            "SELECT OBJECT_APINAME, OBJECTFIELD_APINAME FROM SYOBJC(NOLOCK) WHERE CONSTRAINT_TYPE='UNIQUE' AND OBJECT_APINAME='"
                            + str(getobjectname)
                            + "' and OBJECT_CONSTRAINT_RECORD_ID = '"+str(getrec_id)+"'"
                        )
                        
                        result = Sql.GetFirst(
                            "sp_executesql @T=N'ALTER TABLE "
                            + query_result.OBJECT_APINAME
                            + " ADD CONSTRAINT UQ_"
                            + query_result.OBJECT_APINAME
                            + "_"
                            + query_result.OBJECTFIELD_APINAME
                            + " UNIQUE("
                            + query_result.OBJECTFIELD_APINAME
                            + ")'  "
                        )
                    except:
                        Trace.Write('unique const throwing error')

                # CREATE FOREIGN KEY Constraint
                query_result = Sql.GetFirst(
                    "SELECT TABLE_NAME=OBJECT_APINAME,COLUMN_NAME=OBJECTFIELD_APINAME,REFERENCETABLE=REFOBJECT_APINAME,REFERENCECOLUMN=REFOBJECTFIELD_APINAME FROM SYOBJC WHERE CONSTRAINT_TYPE='FOREIGN KEY' AND OBJECT_APINAME = '"
                    + str(getobjectname)
                    + "' and OBJECT_CONSTRAINT_RECORD_ID = '"+str(getrec_id)+"'  "
                )

                #for loop in query_result:
                result = Sql.GetFirst(
                    "sp_executesql @T=N'ALTER TABLE "
                    + query_result.TABLE_NAME
                    + " ADD CONSTRAINT FK_"
                    + query_result.TABLE_NAME
                    + "_"
                    + query_result.COLUMN_NAME
                    + " FOREIGN KEY ("
                    + query_result.COLUMN_NAME
                    + ") REFERENCES "
                    + query_result.REFERENCETABLE
                    + " ("
                    + query_result.REFERENCECOLUMN
                    + ")' "
                )

                # CREATE FOREIGN KEY Reference
                query_result = Sql.GetFirst(
                    "SELECT TABLE_NAME=OBJECT_APINAME,COLUMN_NAME=OBJECTFIELD_APINAME,REFERENCETABLE=REFOBJECT_APINAME,REFERENCECOLUMN=REFOBJECTFIELD_APINAME FROM SYOBJC WHERE CONSTRAINT_TYPE='FOREIGN KEY' AND REFOBJECT_APINAME='"
                    + str(getobjectname)
                    + "' and OBJECT_CONSTRAINT_RECORD_ID = '"+str(getrec_id)+"'"
                )

                #for loop in query_result:
                result = Sql.GetFirst(
                    "sp_executesql @T=N'ALTER TABLE "
                    + query_result.TABLE_NAME
                    + " ADD CONSTRAINT FK_"
                    + query_result.TABLE_NAME
                    + "_"
                    + query_result.COLUMN_NAME
                    + " FOREIGN KEY ("
                    + query_result.COLUMN_NAME
                    + ") REFERENCES "
                    + query_result.REFERENCETABLE
                    + " ("
                    + query_result.REFERENCECOLUMN
                    + ")' "
                )

                result_update = "UPDATE SYOBJH SET HAS_CONSTRAINTS = 1 WHERE OBJECT_NAME='" + str(getobjectname) + "'"
                query_result = Sql.RunQuery(str(result_update))
            except Exception, e:
                exceptMessage = "SYDRPCONST : recreateConstraint : EXCEPTION : UNABLE TO CREATE CONSTRAINTS: " + str(e)
                Trace.Write(exceptMessage)
        
    rel_name = ""
    related_id = ""
    if CONT_TABLEID is not None and len(CONT_TABLEID) > 0 and str(CONT_TABLEID) != "":
        CONT_TABLEID = CONT_TABLEID.split("_")
        related_id = CONT_TABLEID[0] + "-" + CONT_TABLEID[1]
        related_name_obj = Sql.GetFirst(
            "SELECT top 1 NAME FROM SYOBJR(NOLOCK) WHERE RECORD_ID='" + str(related_id) + "' ORDER BY CpqTableEntryId DESC "
        )
        if related_name_obj is not None:
            related_org_name = str(related_name_obj.NAME)
            rel_name = "div_CTR_" + str(related_org_name).replace(" ", "_")
        '''QueryStatement = "update PRPBMA set AVAILABLE_FORUSE='False'"
        a = Sql.RunQuery(QueryStatement)
        QueryStatement = "update PRPBMA set AVAILABLE_FORUSE='True' where PRICEBOOK_MATERIAL_RECORD_ID in (select pb.PRICEBOOK_MATERIAL_RECORD_ID  FROM PRPBMA pb INNER JOIN MAMTRL (nolock) a on a.MATERIAL_RECORD_ID =pb.MATERIAL_RECORD_ID inner join MAMAFC (nolock) b on a.SAP_PART_NUMBER=b.SAP_PART_NUMBER inner join CACTPR (nolock) c on a.SAP_PART_NUMBER=c.SAP_PART_NUMBER inner join PRLPBE (nolock) d on a.SAP_PART_NUMBER=d.SAP_PART_NUMBER inner join PRPRCL (nolock) e on d.PRICECLASS_ID=e.PRICECLASS_ID inner join MALGMA (nolock) f on a.SAP_PART_NUMBER=f.SAP_PART_NUMBER inner join CAMAIM (nolock) g on a.SAP_PART_NUMBER=g.SAP_PART_NUMBER where d.LIST_PRICE > 0 and f.LANGUAGE_ID='en_US' and pb.PROCEDURE_ID=d.PROCEDURE_ID and f.LNGMAT_WEBSHORTDESC!='' and f.LNGMAT_LONGDESC!='')"
        a = Sql.RunQuery(QueryStatement)'''

    val = []
    val.insert(1, CONT_LABLE)
    val.insert(2, CONT_VALUE)
    val.insert(3, CONT_TABLEID)
    val.insert(4, result)
    val.insert(5, RECORDID)
    val.insert(6, RECORDFEILD)
    val.insert(7, related_id)
    val.insert(8, rel_name)
    val.insert(9, err_msg)
    val.insert(10,err_display)
    return val


LABLE = list(Param.LABLE)
Trace.Write("LABLE-------->" + str(LABLE))
VALUE = list(Param.VALUE)
Trace.Write("Value-------->" + str(VALUE))
TABLEID = (Param.TABLEID).strip()
Trace.Write("table_idididid------>" + str(TABLEID))
ApiResponse = ApiResponseFactory.JsonResponse(do_process(TABLEID, LABLE, VALUE))
