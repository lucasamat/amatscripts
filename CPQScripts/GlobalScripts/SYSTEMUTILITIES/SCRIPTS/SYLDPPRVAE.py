# =========================================================================================================================================
#   __script_name : SYLDPPRVAE.PY
#   __script_description : THIS SCRIPT IS USED TO OPEN THE POPUP TO VIEW OR EDIT A RELATED LIST RECORD.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import SYCNGEGUID as CPQID
from SYDATABASE import SQL

Sql = SQL()


def POPUPLISTVALUE(LABLE, VALUE, TABLEID, OPERATION, RECORDID, RECORDFEILD, RETURN, NEWVAL):
    if OPERATION == "EDIT":
        btn1 = "SAVE"
        func1 = '<button type="button" class="btnconfig" onclick="popup_cont_VIEW();">CANCEL</button>'
        func2 = "popup_cont_SAVE(this)"
        func3 = ""
        func4 = ""
        btn3 = ""
    else:
        btn1 = "EDIT"
        func1 = (
            '<button type="button" onclick="viewedit_popup_close()" class="btnconfig" data-dismiss="modal">CANCEL</button>'
        )
        func2 = "popup_cont_EDIT()"
        func4 = "popup_cont_EDIT()"
        btn3 = "DELETE"
        func3 = "popup_cont_DELETE(this)"
    if RETURN == "EDIT":
        func1 = (
            '<button type="button" onclick="viewedit_popup_close()" class="btnconfig" data-dismiss="modal">CANCEL</button>'
        )
    # Variable needed.
    flag_val = ""
    Question_obj = ""
    new_value_dict = {}
    sec_str = ""
    NewID = ""
    texts = ""
    col = ""
    tot_names = ""
    Chkctry = ""
    edit_field = []
    date_field = []
    canedit = "False"
    candelete = "False"
    # Variable based Argument and calculations.
    primary_value = RECORDID
    
    primary_field = RECORDFEILD
    
    custom_table = ""
    popup_lable_id = ""
    popup_lable_obj = ""
    record_field = ""
    popup_name = ""
    OBJ_REC_ID = ""
    table = valueslist = ""
    if RECORDID is not None:
        RECORDID = RECORDID.split("-")
        custom_table = RECORDID[0]
    if RECORDFEILD is not None:
        RECORDFEILD = RECORDFEILD.split("_")
        if str(TABLEID) != "SYOBJR_93122_MMOBJ_00265":
            RECORDFEILD = RECORDFEILD[1] + "-" + RECORDFEILD[2] + "-" + RECORDFEILD[3]
            # RECORDFEILD = RECORDFEILD[1] + "-" + RECORDFEILD[2]
    if (
        str(TABLEID) == "MATERIALS_IN_PRICE_METHODS"
        or str(TABLEID) == "MATERIALS_IN_PRICE_CLASSES"
        or str(TABLEID) == "LIST_PRICEBOOKS_IN_PRICEBOOK_SET"
    ):
        canedit = "TRUE"
    if TABLEID is not None:
        TABLEID = TABLEID.split("_")
        table = TABLEID[2] + "-" + TABLEID[3] if TABLEID[0] != "PRICEFACTOR" else TABLEID[0]
        popup_lable_id = TABLEID[0] + "-" + TABLEID[1]
        
    if popup_lable_id is not None:
        popup_lable_obj = Sql.GetFirst(
            "SELECT CAN_EDIT, OBJ_REC_ID, CAN_DELETE, NAME FROM SYOBJR (nolock) WHERE SAPCPQ_ATTRIBUTE_NAME='"
            + str(popup_lable_id)
            + "'"
        )
        canedit = str(popup_lable_obj.CAN_EDIT)
        candelete = str(popup_lable_obj.CAN_DELETE)
        popup_name = str(popup_lable_obj.NAME)

        OBJ_REC_ID = str(popup_lable_obj.OBJ_REC_ID)
        table = OBJ_REC_ID

    lable = list(LABLE)[1]
    value = ""
    input_val = ""
    record_value = ""
    MATE_FULFILLMENT_COUNTRY_REC_ID = ""

    Question_obj = Sql.GetFirst("SELECT OBJECT_NAME, LABEL FROM SYOBJH (nolock) WHERE RECORD_ID='" + str(OBJ_REC_ID) + "'")
    Trace.Write("SELECT OBJECT_NAME, LABEL FROM SYOBJH (nolock) WHERE RECORD_ID='" + str(OBJ_REC_ID) + "'")
    ObjectName = ""
    if Question_obj: 
        ObjectName = Question_obj.OBJECT_NAME
        
    try:
        value = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(value))
    except:
        value = value
    ###code ends
    
    getcurrencyval = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(list(VALUE)[1]))
    rec_field = Sql.GetFirst(
        "SELECT API_FIELD_NAME,API_NAME FROM SYSEFL (nolock) WHERE SAPCPQ_ATTRIBUTE_NAME='"
        + str(RECORDFEILD)
        + "'"
    )
    if rec_field is not None and rec_field != "":
        if rec_field.API_FIELD_NAME != "" and rec_field.API_FIELD_NAME is not None:
            record_field = str(eval("rec_field.API_FIELD_NAME"))
        if rec_field.API_NAME != "" and rec_field.API_NAME is not None:
            record_value = str(eval("rec_field.API_NAME"))
    api_obj = Sql.GetList(
        "select DATA_TYPE,API_NAME from  SYOBJD (nolock) WHERE OBJECT_NAME='" + str(record_value).strip() + "'"
    )
    api_list = [inn.API_NAME for inn in api_obj]
    for tab in Product.Tabs:
        if tab.IsSelected == True:
            if tab.Name == "Country":
                Chkctry = "true"
    Flag_value = Product.GetGlobal("Flag_value")
    # Date calculation changing date-time field to date field.
    api_date_list = [
        "EFFECTIVEDATE_END",
        "EFFECTIVEDATE_BEG",
        "PROMO_BEGDATE",
        "PROMO_ENDDATE",
        "EXCHANGE_RATE_DATE",
    ]
    for text in api_list:
        s = Sql.GetList(
            "select DATA_TYPE,API_NAME,LENGTH,DECIMALS from  SYOBJD (nolock) WHERE API_NAME='"
            + str(text)
            + "' and OBJECT_NAME='"
            + str(record_value).strip()
            + "'"
        )
        for ins in s:
            if ins.DATA_TYPE == "DATE" or ins.API_NAME in api_date_list:
                if texts != "":
                    text = "CONVERT(VARCHAR(10)," + str(text) + ",101) AS [" + str(text) + "]"
                    texts = texts + "," + str(text)
                else:
                    text = "CONVERT(VARCHAR(10)," + str(text) + ",101) AS [" + str(text) + "]"
                    texts = str(text)
            else:
                if col != "":
                    col = col + "," + "[" + str(text) + "]"
                else:  #####   JIRA-10602 Starts #####
                    if str(text) != "FACTOR_VAROBJREC_RECORD_ID":
                        col = "[" + str(text) + "]"
                #####   JIRA-10602 Ends #####
    if texts != "":
        col = col + "," + texts
    tot_names = col
    
    header_obj = Sql.GetFirst(
        "SELECT "
        + str(tot_names)
        + " FROM "
        + str(record_value)
        + " (NOLOCK) WHERE "
        + str(record_field)
        + "='"
        + str(primary_value)
        + "'"
    )
    # If object is not empty will proceed further.
    if Question_obj is not None:
        texts1 = ""
        tot_names1 = ""
        col1 = ""
        pricbk_lock = ""
        pricbkst_lock = ""
        attr_chk = ""
        lock_val = "FALSE"  # 7108 starts..ends..
        ObjectName = Question_obj.OBJECT_NAME

        Qstr1 = (
            "SELECT API_NAME FROM  SYOBJD (nolock) WHERE FIELD_LABEL='"
            + str(lable)
            + "' AND PARENT_OBJECT_RECORD_ID ='"
            + str(table)
            + "'"
        )
        Lable_obj = Sql.GetFirst(Qstr1)
        lable = eval(str("Lable_obj.API_NAME"))
        Qstr2 = "select DATA_TYPE,API_NAME from  SYOBJD (nolock) WHERE OBJECT_NAME='" + str(ObjectName).strip() + "'"
        api_obj1 = Sql.GetList(Qstr2)
        api_list1 = [inn.API_NAME for inn in api_obj1]
        for text1 in api_list1:
            s1 = Sql.GetList(
                "select DATA_TYPE,LENGTH,API_NAME,DECIMALS from  SYOBJD (nolock) WHERE API_NAME='"
                + str(text1)
                + "' and OBJECT_NAME='"
                + str(ObjectName).strip()
                + "'"
            )
            for ins in s1:
                if ins.DATA_TYPE == "DATE" or ins.API_NAME in api_date_list:
                    if texts1 != "":
                        if ins.API_NAME == "PROMO_BEGDATE":
                            text1 = "CONVERT(VARCHAR(8)," + str(text1) + ",101) AS [" + str(text1) + "]"
                        else:
                            text1 = "CONVERT(VARCHAR(10)," + str(text1) + ",101) AS [" + str(text1) + "]"
                        texts1 = texts1 + "," + str(text1)
                    else:
                        if ins.API_NAME == "PROMO_BEGDATE":
                            text1 = "CONVERT(VARCHAR(8)," + str(text1) + ",101) AS [" + str(text1) + "]"
                        else:
                            text1 = "CONVERT(VARCHAR(10)," + str(text1) + ",101) AS [" + str(text1) + "]"
                        texts1 = str(text1)
                else:
                    if col1 != "":
                        col1 = col1 + "," + "[" + str(text1) + "]"
                    else:
                        col1 = "[" + str(text1) + "]"
        if texts1 != "":
            col1 = col1 + "," + texts1
        tot_names1 = col1
        new_value_dict = {}
        if NEWVAL != "":
            if str(RETURN) == "CLEAR SELECTION":
                attrval_obj = Sql.GetFirst(
                    "SELECT API_NAME FROM  SYOBJD (nolock) WHERE OBJECT_NAME='"
                    + str(ObjectName)
                    + "' AND LOOKUP_OBJECT='"
                    + str(NEWVAL)
                    + "'"
                )
                api_name = attrval_obj.API_NAME.strip()
                TABLE_OBJS = Sql.GetList(
                    "select OBJECT_NAME,API_NAME,DATA_TYPE,LOOKUP_OBJECT,FORMULA_LOGIC FROM  SYOBJD (nolock) where OBJECT_NAME ='"
                    + str(ObjectName)
                    + "' and FORMULA_LOGIC like '%"
                    + str(api_name)
                    + "%'"
                )
                if TABLE_OBJS is not None:
                    for TABLE_OBJ in TABLE_OBJS:
                        # Tarce.Write("Parse Formula")
                        if TABLE_OBJ.DATA_TYPE != "":
                            DATA_TYPE = str(TABLE_OBJ.DATA_TYPE)
                            if api_name in str(TABLE_OBJ.FORMULA_LOGIC):
                                new_value_dict[str(TABLE_OBJ.API_NAME)] = ""
                                new_value_dict[str(api_name)] = ""
        script = (
            "SELECT "
            + str(tot_names1)
            + " FROM "
            + str(ObjectName)
            + " (NOLOCK) WHERE "
            + str(lable)
            + " = '"
            + str(value)
            + "'"
        )
        Custom_obj = Sql.GetFirst(script)
        #Trace.Write("elseelseelseelse")
        
        if ObjectName == "PRCFVA":
            # Trace.Write("objectobjectobjectobject")
            # Trace.Write(
            #     "SELECT DISTINCT TOP 1000 API_NAME, DATA_TYPE, FORMULA_DATA_TYPE, LOOKUP_OBJECT, PERMISSION, REQUIRED, ABS(DISPLAY_ORDER) as DISPLAY_ORDER, LOOKUP_API_NAME, FIELD_LABEL, SOURCE_DATA SYOBJD (NOLOCK)  WHERE  OBJECT_NAME='"
            #     + str(ObjectName)
            #     + "' AND API_NAME <> 'FACTOR_VAROBJREC_RECORD_ID' ORDER BY ABS(DISPLAY_ORDER)"
            # )
            Qstr3 = (
                "SELECT DISTINCT TOP 1000 API_NAME, DATA_TYPE, FORMULA_DATA_TYPE, LOOKUP_OBJECT, DECIMALS, PERMISSION, REQUIRED, ABS(DISPLAY_ORDER) as DISPLAY_ORDER, LOOKUP_API_NAME, FIELD_LABEL, SOURCE_DATA FROM  SYOBJD (NOLOCK)  WHERE  OBJECT_NAME='"
                + str(ObjectName)
                + "' and  API_NAME <> 'FACTOR_VAROBJREC_RECORD_ID' ORDER BY ABS(DISPLAY_ORDER)"
            )
        else:
            Qstr3 = (
                "SELECT DISTINCT TOP 1000 API_NAME, DATA_TYPE, FORMULA_DATA_TYPE, LOOKUP_OBJECT, DECIMALS, PERMISSION, REQUIRED, ABS(DISPLAY_ORDER) as DISPLAY_ORDER, LOOKUP_API_NAME, FIELD_LABEL,SOURCE_DATA FROM  SYOBJD (NOLOCK)  WHERE  OBJECT_NAME='"
                + str(ObjectName)
                + "' ORDER BY ABS(DISPLAY_ORDER)"
            )


        Sqq_obj = Sql.GetList(Qstr3)
        lookup_val = [val.LOOKUP_API_NAME for val in Sqq_obj]
        lookup_list = {ins.LOOKUP_API_NAME: ins.LOOKUP_OBJECT for ins in Sqq_obj}
        lookup_list1 = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Sqq_obj}
        lookup_list1 = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Sqq_obj}
        new_value_dict1 = {}
        result = ScriptExecutor.ExecuteGlobal(
            "SYPARCEFMA", {"Object": str(ObjectName), "API_Name": record_field, "API_Value": str(primary_value),},
        )
        new_value_dict1 = {API_Names.get("API_NAME"): API_Names.get("FORMULA_RESULT") for API_Names in result}

        sec_str = (
            '<div style="margin-bottom: -1px;" class="row modulebnr brdr">'
            + str(popup_name).upper()
            + " : "
            + str(OPERATION)
            + ' <button type="button" style="float:right;" class="close" onclick="viewedit_popup_close()" data-dismiss="modal">X</button></div>'
        )
        sec_str += '<div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr">'

        if OPERATION == "EDIT":
            sec_str += func1
        elif OPERATION == "VIEW":
            sec_str += ""

        #Trace.Write("6666666666666-----" + str(ObjectName))
        if canedit.upper() == "TRUE":
            sec_str += (
                '<button type="button" id="'
                + str(ObjectName)
                + '" class="btnconfig viewvalidate" onclick="'
                + func2
                + '">'
                + btn1
                + "</button>"
            )

        else:
            if candelete.upper() == "TRUE" and OPERATION == "VIEW":
                sec_str += (
                    '<button type="button" id="'
                    + str(ObjectName)
                    + '_delete" class="btnconfig" data-target="#relcont_viewModalDelete" data-toggle="modal" onclick="'
                    + func3
                    + '">'
                    + btn3
                    + "</button>"
                )
        sec_str += '</div></div><div id="Headerbnr" class="mart_col_back"></div><div class="col-md-12"><div id="alert_msg" class="col-md-12  alert-danger rel_alertdanger pad-10 mrg-bt-10 collapse in brdr" style="display: none;"></div></div>'
        sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
        sec_str += '<table id="relpopup" class="ma_width_marg">'
        if Sqq_obj is not None and Custom_obj is not None:
            for val in Sqq_obj:
                readonly = "readonly"
                disable = "disabled"
                current_obj_api_name = val.API_NAME.strip()
                current_obj_field_lable = val.FIELD_LABEL.strip()
                readonly_val = val.PERMISSION.strip()
                #Trace.Write("readonly_val___readonly_val"+str(readonly_val)+"current_obj_api_name__current_obj_api_name"+str(current_obj_api_name))
                erp_readonly_val = val.SOURCE_DATA
                data_type = val.DATA_TYPE.strip()
                Decimal_Value = val.DECIMALS
                formula_data_type = str(val.FORMULA_DATA_TYPE).strip()
                current_obj_value = ""
                header_obj_value = ""
                datepicker = "onclick_datepicker('" + current_obj_api_name + "')"
                ids = ""
                add_style = ""
                idval = ""
                edit_warn_icon = ""
                formula_permission = ""
                left_float = ""
                id_val = ""
                id_api = ""
                edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
                priceclass_val = ""
                keypressval = ""
                datepicker_onchange = "onchangedatepicker('" + current_obj_api_name + "')"
                # Lookup Master object Value.
                if current_obj_api_name in lookup_val:
                    #Trace.Write("123454575686867965434544444444444444")
                    #Trace.Write("222222222222222222" + str(formula_permission))
                    for key, value in lookup_list.items():
                        if key == current_obj_api_name:
                            ids = value.strip()
                if current_obj_api_name in lookup_val:
                    for key, value in lookup_list1.items():
                        if key == current_obj_api_name:
                            formula_permission_qry = Sql.GetFirst(
                                "SELECT * FROM  SYOBJD (nolock) WHERE API_NAME = '"
                                + str(value)
                                + "' and OBJECT_NAME = '"
                                + str(ObjectName)
                                + "' "
                            )
                            formula_permission = str(formula_permission_qry.PERMISSION).strip()
                            #Trace.Write("formula_permission____formula_permission"+str(formula_permission))
                if (
                    str(readonly_val).upper() == "READ ONLY"
                    and OPERATION == "EDIT"
                    and str(erp_readonly_val).upper() != "ERP"
                ):
                    #Trace.Write("IF---111111111"+str(current_obj_api_name))
                    readonly = "readonly"
                    disable = "disabled"
                    edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
                elif (str(readonly_val).upper() != "READ ONLY" or formula_permission != "READ ONLY") and (
                    OPERATION == "EDIT" and str(data_type).upper() == "LONG TEXT AREA"
                ):
                    Trace.Write("IF---222222222"+str(current_obj_api_name))
                    readonly = ""
                    disable = ""
                    edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
                    if current_obj_api_name == "ATTVAL_VALFORMULA":
                        add_style = "display:none;"
                elif (str(readonly_val).upper() != "READ ONLY" or formula_permission != "READ ONLY") and (
                    OPERATION == "EDIT"
                    and str(erp_readonly_val).upper() != "ERP"
                    and str(data_type).upper() != "LONG TEXT AREA"
                ):
                    Trace.Write("IF---333333333"+str(current_obj_api_name))
                    readonly = ""
                    disable = ""
                    edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
                if header_obj != "":
                    try:
                        header_obj_value = eval(
                            str("header_obj." + str(current_obj_api_name).encode("ascii", "ignore")).strip()
                        )
                    except:
                        Trace.Write("except" + str(current_obj_value))
                if Custom_obj != "":
                    current_obj_value = eval(
                        str("Custom_obj." + str(current_obj_api_name).encode("ascii", "ignore")).strip()
                    )

                    try:
                        current_obj_value = str(current_obj_value)
                    except UnicodeEncodeError:
                        current_obj_value = current_obj_value
                    except:
                        Trace.Write("Error")

                if str(current_obj_api_name).upper() == "CPQTABLEENTRYMODIFIEDBY":
                    if ObjectName == "PRCFVA":
                        if current_obj_value != "" and len(current_obj_value) > 3:
                            Trace.Write("select USERNAME from users where id = " + str(current_obj_value))
                            current_obj_value = Sql.GetFirst(
                                "select USERNAME from users where USERNAME = '" + str(current_obj_value) + "'"
                            ).USERNAME
                    elif current_obj_value != "" and ObjectName != "PRCFVA":
                        current_obj_value = Sql.GetFirst(
                            "select USERNAME from users where id = " + str(current_obj_value)
                        ).USERNAME

                # Trace.Write("readonly_val----------> " + str(readonly_val))
                # Trace.Write("data_type-------------> " + str(data_type))
                # Trace.Write("canedit---------------> " + str(canedit))
                # Trace.Write("erp_readonly_val------> " + str(erp_readonly_val))
                if ( str(readonly_val).upper() == "READ ONLY" or data_type == "AUTO NUMBER" or canedit.upper() == "FALSE" or str(erp_readonly_val).upper() == "ERP") and str(data_type).upper() != "LONG TEXT AREA":
                    edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
                    func4 = ""
                    
                if current_obj_api_name in new_value_dict1:
                    if str(current_obj_api_name) == "TO_CURRENCY":
                        #Trace.Write("if--")
                        edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
                    else:
                        #Trace.Write("else--99999999")
                        edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
                        readonly = "readonly"
                        disable = "disabled"

                #Trace.Write("11111111111111113" + str(current_obj_api_name))
                #Trace.Write("222222222222223" + str(ObjectName))
                #Trace.Write("1111111111111111111111111111111" + str(edit_pencil_icon))
                if data_type == "FORMULA" and OPERATION == "EDIT":
                    lookup_name = str(lookup_list1.get(current_obj_api_name))
                    Trace.Write("lookup_name_lookup_name"+str(lookup_name))
                    #Trace.Write("1111111111111111 API_NAME CHECK" + str(current_obj_api_name)+"FORMULA PERMISSION"+str(formula_permission)+"readonly_val_readonly_val_____readonly_val"+str(readonly_val))
                    #Trace.Write("22222222222222 ObjectName CHECK" + str(ObjectName))
                    if ((str(current_obj_api_name) == "SAP_PART_NUMBER" and str(ObjectName) == "SGSORM") or (str(current_obj_api_name) == "SALESORG_ID" and str(ObjectName) == "SASOLG") or (str(current_obj_api_name) == "PROCEDURE_ID" and str(ObjectName) == "PRPMCL") or (str(current_obj_api_name) == "PERSONALIZATION_NAME" and str(ObjectName) == "MAPLPE") or (str(current_obj_api_name) == "SAP_PARTNUMBER" and str(ObjectName) == "MABFQM") or (str(current_obj_api_name) == "FULCTY" and str(ObjectName) == "MAPLCY") or (str(current_obj_api_name) == "STP_ACCOUNT_NUMBER" and str(ObjectName) == "MAEXMA") or (str(current_obj_api_name) == "PROCEDURE_ID" and str(ObjectName) == "PRPBMA")):
                        disable = ""
                    else:
                        #if str()
                        disable = "disabled"
                    
                    edit_pencil_icon = ( '<i class="fa fa-lock" aria-hidden="true"></i>' if str(disable) == "disabled" else '<i class="fa fa-pencil" aria-hidden="true"></i>' )

                    Trace.Write("IF---555555" + str(edit_pencil_icon)+"APIIIIIIIIIIIIIII"+str(current_obj_api_name))

                ObjectName_list = [
                    "MAVSDP",
                    "PRPMMF",
                    "MAMAEF",
                    "PRPBMA",
                    "SGASFC",
                    "SAASLG",
                    "MACPMP",
                    "MASPMC",
                    "PACAFL",
                    "PRCFVA",  
                    "PAPBEN",
                ]
                Currentobj_list = [
                    "OUT_OF_STOCK",
                    "SORTKEY3",
                    "MATEMBFND_ID",
                    "MODCLS_ID",
                    "PRICING_CURRENCY",
                    "ACCOUNT_TYPE",
                    "SORACC_ID",
                    "SORLNG_ID",
                    "SORCTYPLTMAT_ID",
                    "PERMAT_ID",
                    "FULVNDACT_ID",
                    "FACE_VALUE",
                    "MARKET_PRICE",
                    "MATERIAL_COST",
                    "GIFTCARD_COST",
                    "SORG_DEF_CURRENCY",
                    "SEGCATFLT_ID",
                    "GIFTCARD_FACEVAL_INGIFTCARD_CURRENCY",
                    "SUPERCLASS_ID",
                    "CRITERIA_11",
                    "CRITERIA_12",
                    "CRITERIA_13",
                    "CRITERIA_15",
                    "CRITERIA_16",
                    "CRITERIA_17",
                    "CRITERIA_18",
                    "CRITERIA_19",
                    "CRITERIA_20",
                    "CRITERIA_21",
                    "CRITERIA_22",
                    "CRITERIA_23",
                    "CRITERIA_24",
                    "CRITERIA_25",  # A043S001P01-7164 START,END #Removed ERROR from the list by VETRI for #A043S001P01-7282
                    "WHERE_CONDITION",
                    "LEVEL_00",
                    "LEVEL_01",
                    "LEVEL_02",
                    "LEVEL_03",
                    "LEVEL_04",
                    "LEVEL_05",
                    "LEVEL_06",
                    "LEVEL_07",  # Modified by Namrata Sivakumar - A043S001P01-9608 remove questions - SFDC order - filterlevel view
                    "FACTOR_STATUS",  ##A043S001P01-11443 START,END Hide the field from the popup only.
                ]

                if ObjectName in ObjectName_list and current_obj_api_name in Currentobj_list:
                    add_style = "display: none;"

                if data_type == "LOOKUP":
                    add_style = "display: none;"


                displaynoneList_sg = [
                    "ADJUSTMENT_CURRENCY",
                    "ADJUSTMENT_CURRENCY_RECORD_ID",
                    "ADJUSTMENT_METHOD",
                    "ADJUSTMENT_VALUE",
                    "PRICEAGREEMENT_ID",
                    "OWNER_ID",
                    "OWNED_DATE",
                ]
                displaynonelistpaffee = ["OWNER_ID", "OWNED_DATE"]

                # Trace.Write("11111111111111" + str(readonly))
                # Trace.Write("22222222222222" + str(disable))
                # Trace.Write("33333333333333" + str(current_obj_api_name))
                # Trace.Write("44444444444" + str(current_obj_field_lable))
                # Trace.Write("55555555555555" + str(data_type))
                # Trace.Write("modemode------->" + str(OPERATION))


                # Trace.Write("record_value_record_value" + str(record_value))

                sec_str += (
                    '<tr class="iconhvr brdbt" style="  '
                    + str(add_style)
                    + '"><td class="wth350"><label class="padlt15mrgbt0">'
                    + str(current_obj_field_lable)
                    + '</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="'
                    + str(current_obj_field_lable)
                    + '"  class="bgcccwth10"><i   class="fa fa-info-circle fltlt"></i>'
                )

                if str(val.REQUIRED).upper() == "TRUE" or val.REQUIRED == "1":
                    sec_str += ""
                    # sec_str+='<span class="req-field"  >*</span>'
                sec_str += "</a></td>"

                #Trace.Write("current_obj_api_name___current_obj_api_name"+str(current_obj_api_name)+"data_type___data_type"+str(data_type)+"formula_data_type___formula_data_type"+str(formula_data_type)+"readonly___readonly"+str(readonly))


                if data_type == "AUTO NUMBER":
                    if str(current_obj_api_name).strip() == "ATTRIBUTEVALUE_RECORD_ID":
                        Product.SetGlobal("attrval_record_id", str(current_obj_value).strip())
                    sec_str += (
                        '<td><input id="'
                        + str(current_obj_api_name)
                        + '" type="text" value="'
                        + input_val
                        + '" class="form-control related_popup_css" disabled></td>'
                    )
                elif formula_data_type == "PERCENT" or data_type == "PERCENT":
                    if current_obj_value:
                        my_format = "{:." + str(Decimal_Value) + "f}"
                        current_obj_value = str(my_format.format(round(float(current_obj_value), int(Decimal_Value))))
                    symbol = " %"
                    data_type = "text"
                    if OPERATION == "EDIT" or current_obj_value == "":
                        symbol = ""
                        data_type = "number"
                    sec_str += (
                        '<td><input id="'
                        + str(current_obj_api_name)
                        + '" type="text" value="'
                        + current_obj_value
                        + symbol
                        + '" class="form-control related_popup_css" disabled></td>'
                    )
                elif data_type == "NUMBER" or data_type == "CURRENCY":
                    if current_obj_value:
                        my_format = "{:." + str(Decimal_Value) + "f}"
                        current_obj_value = str(my_format.format(round(float(current_obj_value), int(Decimal_Value))))

                    symbol = " "
                    data_type = "number"
                    if OPERATION == "EDIT" or current_obj_value == "":
                        symbol = ""
                        data_type = "number"
                    # A043S001P01-12616 start
                    if str(current_obj_api_name) == "FACTOR_PCTVAR" and current_obj_value != "":
                        symbol = "%"
                    # A043S001P01-12616 end
                    sec_str += (
                        '<td><input id="'
                        + str(current_obj_api_name)
                        + '" type="text" value="'
                        + current_obj_value
                        + symbol
                        + '" class="form-control related_popup_css" '
                        + str(disable)
                        + "></td>"
                    )
                elif data_type == "LONG TEXT AREA":
                    sec_str += (
                        '<td><textarea class="form-control related_popup_css txtArea" id="'
                        + str(current_obj_api_name)
                        + '" rows="1" cols="100" >'
                        + current_obj_value
                        + "</textarea></td>"
                    )
                elif data_type == "LOOKUP":
                    sec_str += (
                        '<td><input id="'
                        + str(current_obj_api_name)
                        + '" type="text" value="'
                        + current_obj_value
                        + '" class="form-control related_popup_css" disabled></td>'
                    )
                elif (
                    data_type == "FORMULA"
                    and OPERATION == "EDIT"
                    and formula_data_type != "CHECKBOX"
                    and str(ObjectName) == "PRPBMA"
                    and str(readonly) != "readonly"
                ):
                    sec_str += (
                        '<td><input id="'
                        + str(current_obj_api_name)
                        + '" type="text" value="'
                        + current_obj_value
                        + '" class="form-control lookupBg related_popup_css fltlt"   >'
                    )
                    sec_str += (
                        '<input class="popup fltlt" id="'
                        + str(ids)
                        + '" onclick="cont_lookup_popup(this)"   type="image"  src="../mt/default/images/customer_lookup.gif"></td>'
                    )
                elif data_type == "FORMULA" and OPERATION == 'VIEW':
                    #Trace.Write("11111111111111111111-------------->PRCFVA"+str(current_obj_api_name))
                    if (
                        str(ObjectName) == "PRCFVA"
                        and str(current_obj_api_name) == "FACTOR_DATATYPE"
                        and str(current_obj_value) == "NUMBER"
                    ):
                        #Trace.Write("hide and show")
                        numlist = ["FACTOR_PCTVAR", "FACTOR_CURVAR"]
                        
                        if str(current_obj_api_name) in numlist:
                            add_style = "display: none;"
                            
                    sec_str += (
                        '<td><input id="'
                        + str(current_obj_api_name)
                        + '" type="text" value="'
                        + current_obj_value
                        + '" class="form-control related_popup_css" disabled></td>'
                    )
                elif (
                    data_type == "FORMULA"
                    and OPERATION == "EDIT"
                    and formula_data_type != "CHECKBOX"
                    and str(ObjectName) != "PRPBMA"
                ):
                    #Trace.Write("If formula data type is text")
                    lookup_valand= []
                    if (
                        header_obj_value == ""
                        and current_obj_api_name in lookup_valand
                        and str(readonly) != "readonly"
                        or current_obj_api_name == "PROCEDURE_ID"
                    ):
                        if (
                            current_obj_api_name == "PRICECLASS_ID"
                            or current_obj_api_name == "CURRENCY"
                            or current_obj_api_name == "LIST_PRICEBOOKSET_ID"
                        ):
                            sec_str += (
                                '<td><input id="'
                                + str(current_obj_api_name)
                                + '" type="text" value="'
                                + current_obj_value
                                + '" class="form-control related_popup_css fltlt"   enabled>'
                            )
                        else:
                            sec_str += (
                                '<td><input id="'
                                + str(current_obj_api_name)
                                + '" type="text" value="'
                                + current_obj_value
                                + '" class="form-control lookupBg related_popup_css fltlt"   >'
                            )
                            sec_str += (
                                '<input class="popup fltlt" id="'
                                + str(ids)
                                + '" onclick="cont_lookup_popup(this)"   type="image"  src="../mt/default/images/customer_lookup.gif"></td>'
                            )
                    else:
                        #Trace.Write("else formula data type is text")
                        if str(current_obj_api_name) == "DEFAULT_LOWPRCADJ_FACTOR":
                            if str(ObjectName) == "PRLPBK":
                                sec_str += (
                                    '<td><input id="'
                                    + str(current_obj_api_name)
                                    + '" type="number" step="0.001" value="'
                                    + current_obj_value
                                    + '" class="form-control related_popup_css fltlt" style=" '
                                    + str(left_float)
                                    + ' ">'
                                    + str(edit_warn_icon)
                                    + "</td>"
                                )
                            else:
                                sec_str += (
                                    '<td><input id="'
                                    + str(current_obj_api_name)
                                    + '" type="number" step="0.001" value="'
                                    + current_obj_value
                                    + '" class="form-control related_popup_css fltlt" style=" '
                                    + str(left_float)
                                    + ' " '
                                    + str(disable)
                                    + ">"
                                    + str(edit_warn_icon)
                                    + "</td>"
                                )
                        elif (
                            current_obj_api_name == "PRICECLASS_ID"
                            or current_obj_api_name == "CURRENCY"
                            or current_obj_api_name == "LIST_PRICEBOOKSET_ID"
                        ):
                            sec_str += (
                                '<td><input id="'
                                + str(current_obj_api_name)
                                + '" type="text" value="'
                                + current_obj_value
                                + '" class="form-control related_popup_css fltlt" disabled>'
                            )
                        else:
                            if str(formula_permission)!='EDITABLE':
                                sec_str += (
                                    '<td><input id="'
                                    + str(current_obj_api_name)
                                    + '" type="text" value="'
                                    + current_obj_value
                                    + '" data-target="#cont_viewModalSection" class="form-control related_popup_css fltlt" style=" '
                                    + str(left_float)
                                    + ' " disabled>'
                                    + "</td>"
                                )
                            else:
                                sec_str += ( '<td><input id="' + str(current_obj_api_name) + '" type="text" value="' + current_obj_value + '" class="form-control related_popup_css fltlt"  >' ) 
                                sec_str += ( '<input class="popup fltlt" id="' + str(ids) + '" onclick="cont_lookup_popup_new(this)"  type="image"  style="height:20px !important" src="../mt/default/images/customer_lookup.gif"></td>' )
                                        
                elif data_type == "CHECKBOX" or formula_data_type == "CHECKBOX":
                    if str(ObjectName) == "PAFFEE" and str(current_obj_api_name) == "ACTIVE" and OPERATION == "EDIT":
                        disable = ""
                        edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
                    if current_obj_value == "True" or current_obj_value == "1":
                        sec_str += (
                            '<td><input id="'
                            + str(current_obj_api_name)
                            + '" type="checkbox" value="'
                            + current_obj_value
                            + '" class="custom" '
                            + disable
                            + ' checked><span class="lbl"></span></td>'
                        )
                    else:
                        sec_str += (
                            '<td><input id="'
                            + str(current_obj_api_name)
                            + '" type="checkbox" value="'
                            + current_obj_value
                            + '" class="custom" '
                            + disable
                            + '><span class="lbl"></span></td>'
                        )
                elif data_type == "PICKLIST":
                    if popup_name == "ALLOWED FULFILLMENT COUNTRIES":
                        if OPERATION == "EDIT":
                            select_drop_css = "height: 28px;"
                        else:
                            select_drop_css = "border: 0;height: 28px;"
                        if str(current_obj_api_name) == "COUNTRIES":
                            cname = eval(str("Custom_obj.COUNTRIES"))
                            Trace.Write("-----Country Selected" + str(cname))
                            Sql_Countries = Sql.GetList("select COUNTRY_NAME FROM SACTRY (nolock) where COUNTRY_NAME != ''")
                            Check_Country = 0
                            Countries_List = []
                            for cont in Sql_Countries:
                                Check_Country = 1
                                Countries_List.append(cont.COUNTRY_NAME)
                            if len(Countries_List) != 0:
                                Countries_List.insert(0, "ALL COUNTRIES")
                            sec_str += (
                                '<td class="posrelclr555" onclick="showCheckboxes()"><select id="select_id" value="'
                                + current_obj_value
                                + '" type="text" class="form-control related_popup_css fltltfnt13"   '
                                + disable
                                + ' > "add" </select><input id="'
                                + str(current_obj_api_name)
                                + '" style="'
                                + select_drop_css
                                + ' background-color: #fff;" class="inp_val" type="text" disabled />'
                            )
                            sec_str += '<div id="checkboxes"  class="chxcust1">'
                            Selected_Countries = Sql.GetFirst(
                                "select INC_COUNTRY_TEMPLATES,COUNTRIES FROM MAMAFC (nolock) where MATERIAL_FULFILLMENT_COUNTRY_RECORD_ID = '"
                                + str(MATE_FULFILLMENT_COUNTRY_REC_ID)
                                + "'"
                            )
                            Sel_Coun_qry = Sql.GetList(
                                "select COUNTRIES,INC_COUNTRY_TEMPLATES FROM MAMAFC (nolock) where MATERIAL_RECORD_ID = '"
                                + str(mat_rec_id)
                                + "' and FULCTY_RECORD_ID = '"
                                + str(coun_rec_id)
                                + "'"
                            )
                            Sel_Coun_list = [ins.COUNTRIES for ins in Sel_Coun_qry]
                            Selected_Countries_List = (Selected_Countries.COUNTRIES).split(",")
                            Selected_Countries_List = Selected_Countries_List + Sel_Coun_list
                            if "ALL COUNTRIES" not in Selected_Countries_List:
                                for req in Countries_List:
                                    if str(cname).upper() in Selected_Countries_List:
                                        sec_str += (
                                            '<label><input checked = "checked" type="checkbox" onchange="labelDropdown(this)" class="'
                                            + str(cname).upper()
                                            + '" />'
                                            + str(cname).upper()
                                            + "</label>"
                                        )
                                    else:
                                        sec_str += (
                                            '<label><input  type="checkbox" onchange="labelDropdown(this)" class="'
                                            + str(req).upper()
                                            + '" />'
                                            + str(req).upper()
                                            + "</label>"
                                        )
                            else:
                                for req in Countries_List:
                                    sec_str += (
                                        '<label><input  checked = "checked" type="checkbox" onchange="labelDropdown(this)" class="'
                                        + str(req).upper()
                                        + '" />'
                                        + str(req).upper()
                                        + "</label>"
                                    )
                            sec_str += "</div></td>"
                        elif str(current_obj_api_name) == "INC_COUNTRY_TEMPLATES":
                            sec_str += (
                                '<td onclick="Default_Checkboxes()"><select id="'
                                + str(current_obj_api_name)
                                + '" value="'
                                + current_obj_value
                                + '" type="text" class="form-control related_popup_css fltltfnt13"   '
                                + disable
                                + " >"
                            )
                            Selected_Countries = Sql.GetFirst(
                                "select INC_COUNTRY_TEMPLATES,COUNTRIES FROM MAMAFC (nolock) where MATERIAL_FULFILLMENT_COUNTRY_RECORD_ID = '"
                                + str(MATE_FULFILLMENT_COUNTRY_REC_ID)
                                + "'"
                            )
                            sec_str += "<option>" + str(Selected_Countries.INC_COUNTRY_TEMPLATES) + "</option>"
                            sec_str += "</select></td>"
                    elif popup_name == "EMBLEM QUANTITY FACTORS IN SET":
                        sec_str += (
                            '<td><select id="'
                            + str(current_obj_api_name)
                            + '" value="'
                            + current_obj_value
                            + '" type="text" class="form-control related_popup_css fltltfnt13"   '
                            + disable
                            + " >"
                        )
                        Sql_Quality_Tier = Sql.GetFirst(
                            "select PICKLIST_VALUES FROM  SYOBJD (nolock) where OBJECT_NAME='MAEMQF' and DATA_TYPE='PICKLIST'"
                        )
                        Tier_List = (Sql_Quality_Tier.PICKLIST_VALUES).split(",")
                        for req1 in Tier_List:
                            sec_str += "<option>" + str(req1) + "</option>"
                        sec_str += "</select></td>"
                    elif popup_name == "AVAILABLE PROMOTIONS IN SALES ORG":
                        sec_str += (
                            '<td><select id="'
                            + str(current_obj_api_name)
                            + '" value="'
                            + current_obj_value
                            + '" type="text" class="form-control related_popup_css fltltfnt13"   '
                            + disable
                            + " >"
                        )
                        Sql_Quality_Tier = Sql.GetFirst(
                            "select PICKLIST_VALUES FROM  SYOBJD (nolock) where OBJECT_NAME='SASOPM' and DATA_TYPE='PICKLIST'"
                        )
                        Tier_List = (Sql_Quality_Tier.PICKLIST_VALUES).split(",")
                        for req1 in Tier_List:
                            sec_str += "<option>" + str(req1) + "</option>"
                        sec_str += "</select></td>"
                    else:
                        sec_str += "<td>"
                        sec_str += (
                            '<select id="'
                            + str(current_obj_api_name)
                            + '" value="'
                            + current_obj_value
                            + '" type="text" class="form-control pop_up_brd_rad related_popup_css fltltfnt13"   '
                            + disable
                            + " >"
                        )
                        Sql_Quality_Tier = Sql.GetFirst(
                            "select PICKLIST_VALUES FROM  SYOBJD (nolock) where OBJECT_NAME='"
                            + str(ObjectName)
                            + "' and DATA_TYPE='PICKLIST' and API_NAME = '"
                            + str(current_obj_api_name)
                            + "' "
                        )
                        if (
                            str(Sql_Quality_Tier.PICKLIST_VALUES).strip() is not None
                            and str(Sql_Quality_Tier.PICKLIST_VALUES).strip() != ""
                        ):
                            Tier_List = (Sql_Quality_Tier.PICKLIST_VALUES).split(",")
                            for req1 in Tier_List:
                                if current_obj_value == req1:
                                    sec_str += "<option selected>" + str(req1) + "</option>"
                                else:
                                    sec_str += "<option>" + str(req1) + "</option>"
                        else:
                            sec_str += "<option selected>" + str(current_obj_value) + "</option>"
                        sec_str += "</select></td>"
                elif data_type == "DATE" and OPERATION == "EDIT" and str(readonly_val).upper() != "READ ONLY":
                    date_field.append(current_obj_api_name)
                    if str(current_obj_api_name) == "VALID_FROM_DATE":
                        sec_str += (
                            '<td><input id="'
                            + str(current_obj_api_name)
                            + '" value="'
                            + current_obj_value
                            + '" type="text"  onclick="'
                            + str(datepicker)
                            + '" onchange="'
                            + str(datepicker_onchange)
                            + '" class="form-control datePickerField wth157fltltbrdbt"  ></td>'
                        )
                    elif str(current_obj_api_name) == "MERCH_OTH_MTRL_CST_CURR_FX_RT_DATE":
                        edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
                        sec_str += (
                            '<td><input id="'
                            + str(current_obj_api_name)
                            + '" value="'
                            + current_obj_value
                            + '" type="text"  onclick="'
                            + str(datepicker)
                            + '" onchange="'
                            + str(datepicker_onchange)
                            + '" class="form-control datePickerField wth157fltltbrdbt"   '
                            + disable
                            + " ></td>"
                        )
                    else:
                        sec_str += (
                            '<td><input id="'
                            + str(current_obj_api_name)
                            + '" value="'
                            + current_obj_value
                            + '" type="text"  onclick="'
                            + str(datepicker)
                            + '" onchange="'
                            + str(datepicker_onchange)
                            + '" class="form-control datePickerField wth157fltltbrdbt"  '
                            + disable
                            + " ></td>"
                        )
                elif data_type == "NUMBER" and OPERATION == "VIEW" and formula_data_type != "CURRENCY":
                    sec_str += (
                        '<td><input id="'
                        + str(current_obj_api_name)
                        + '" type="number" value="'
                        + current_obj_value
                        + '" class="form-control related_popup_css" style="'
                        + str(left_float)
                        + ' " '
                        + disable
                        + "></td>"
                    )
                elif data_type == "NUMBER" and OPERATION == "EDIT":
                    readonly = ""
                    if (
                        str(readonly) != "readonly" and str(readonly_val) != "READ ONLY" and lock_val.upper() != "TRUE"
                    ):  ####7108 starts...
                        sec_str += (
                            '<td><input id="'
                            + str(current_obj_api_name)
                            + '" type="number" value="'
                            + current_obj_value
                            + '" class="form-control related_popup_css" style="'
                            + str(left_float)
                            + ' "></td>'
                        )
                    else:
                        sec_str += (
                            '<td><input id="'
                            + str(current_obj_api_name)
                            + '" type="number" value="'
                            + current_obj_value
                            + '" class="form-control related_popup_css" style="'
                            + str(left_float)
                            + ' " disabled></td>'
                        )
                elif (data_type == "CURRENCY" or formula_data_type == "CURRENCY") and OPERATION == "VIEW":
                    curr_symbol = ""
                    #Trace.Write("94--------------------------------" + str(current_obj_api_name))
                    # Trace.Write(
                    #     "select CURRENCY_INDEX from  SYOBJD (nolock) where API_NAME = '"
                    #     + str(current_obj_api_name)
                    #     + "' and OBJECT_NAME = '"
                    #     + str(ObjectName)
                    #     + "' and (DATA_TYPE = 'CURRENCY' or FORMULA_DATA_TYPE = 'CURRENCY')"
                    # )
                    cur_api_name = Sql.GetList(
                        "select CURRENCY_INDEX from  SYOBJD (nolock) where API_NAME = '"
                        + str(current_obj_api_name)
                        + "' and OBJECT_NAME = '"
                        + str(ObjectName)
                        + "' and (DATA_TYPE = 'CURRENCY' or FORMULA_DATA_TYPE = 'CURRENCY') "
                    )
                    if cur_api_name:
                        for cur_api_names in cur_api_name:
                            if str(cur_api_names.CURRENCY_INDEX) != "":
                                curr_symbol_obj = Sql.GetFirst(
                                    "select SYMBOL,CURRENCY from PRCURR (NOLOCK) where CURRENCY_RECORD_ID = (select "
                                    + str(cur_api_names.CURRENCY_INDEX)
                                    + " from "
                                    + str(ObjectName)
                                    + " where "
                                    + str(lable)
                                    + " = '"
                                    + str(getcurrencyval)
                                    + "' ) "
                                )
                                if curr_symbol_obj is not None:
                                    curr_symbol = curr_symbol_obj.CURRENCY
                    if (
                        current_obj_value is not None
                        and current_obj_value != ""
                        and str(current_obj_api_name) != "LOWPRCADJ_FACTOR"
                    ):
                        if "-" in current_obj_value:
                            #Trace.Write("Inside -ve")
                            ccc = current_obj_value.split("-")
                            Trace.Write("ccccccccccccccccccccccccccc" + str(ccc))
                            """current_obj_value = (
                                current_obj_value[0] + curr_symbol + "" + ccc[1]
                            )"""
                            current_obj_value = current_obj_value[0] + "" + ccc[1] + curr_symbol
                            # Trace.Write('ccccccccccccccccccccccccccc'+str(current_obj_value))
                            # current_obj_value = curr_symbol+''+current_obj_value
                        else:
                            #Trace.Write("Inside +ve")
                            current_obj_value = current_obj_value + "" + curr_symbol

                    sec_str += (
                        '<td><input id="'
                        + str(current_obj_api_name)
                        + '" type="text" value="'
                        + current_obj_value
                        + '" class="form-control related_popup_css" style="'
                        + str(left_float)
                        + ' " '
                        + disable
                        + "></td>"
                    )
                else:
                    if current_obj_api_name == "EXCHANGE_RATE_DATE" and current_obj_value != "":
                        val = current_obj_value.split(" ")
                        sec_str += (
                            '<td><input id="'
                            + str(current_obj_api_name)
                            + '" type="text" onfocusout="attribute_checker(this)" value="'
                            + val[0]
                            + '" '
                            + str(keypressval)
                            + ' class="form-control related_popup_css" style="'
                            + str(left_float)
                            + ' " '
                            + disable
                            + ">"
                            + str(edit_warn_icon)
                            + "</td>"
                        )
                    else:
                        if str(current_obj_api_name) == "CALCULATION_VARIABLE_RECORD_ID":
                            sec_str += (
                                '<td style="display:none"><input id="'
                                + str(current_obj_api_name)
                                + '" type="text" onfocusout="attribute_checker(this)" value="'
                                + current_obj_value
                                + '" '
                                + str(keypressval)
                                + ' class="form-control related_popup_css" style="'
                                + str("display:none")
                                + ' " '
                                + disable
                                + ">"
                                + str(edit_warn_icon)
                                + "</td>"
                            )
                        else:
                            sec_str += (
                                '<td><input id="'
                                + str(current_obj_api_name)
                                + '" type="text" onfocusout="attribute_checker(this)" value="'
                                + current_obj_value
                                + '" '
                                + str(keypressval)
                                + ' class="form-control related_popup_css" style="'
                                + str(left_float)
                                + ' " '
                                + disable
                                + ">"
                                + str(edit_warn_icon)
                                + "</td>"
                            )
                # Pencil/Lock icon for the popup row.
                if canedit.upper() == "TRUE":
                    sec_str += (
                        '<td class="fltrtbrdbto"><div class="col-md-12 editiconright"><a href="#" onclick="'
                        + func4
                        + '" class="editclick">'
                        + str(edit_pencil_icon)
                        + "</i></a></div></td>"
                    )
                else:  ## 10221 for pencil icon
                    if str(current_obj_api_name) == "FACTOR_PCTVAR" or "FACTOR_NUMVAR":
                        sec_str += (
                            '<td class="fltrtbrdbto"><div class="col-md-12 editiconright"><a href="#" onclick="Pricefactor_edit_icon()" class="editclick">'
                            + str(edit_pencil_icon)
                            + "</a></div></td>"
                        )
                    else:
                        sec_str += (
                            '<td class="fltrtbrdbto"><div class="col-md-12 editiconright"><a href="#" onclick="" class="editclick">'
                            + str(edit_pencil_icon)
                            + "</a></div></td>"
                        )
                sec_str += "</tr>"
        sec_str += "</table>"
        sec_str += "</div>"
    else:
        sec_str += '<div class="txt_center">No matching records found </div><div class="modal-footer"><button type="button" class="btnstyle fltrt"   data-dismiss="modal">Close</button></div>'
    try:
        Trace.Write("sec_str" + str(sec_str))
        Trace.Write("date_field" + str(date_field))
        Trace.Write("new_value_dict" + str(new_value_dict))
    except:
        Trace.Write("errorrrrr")
    return sec_str, date_field, new_value_dict


#### SEGMENT REVISION MIGRATION CODE START...
def ProgramAddNew():
    sec_str = '<div id="VIEW_DIV_ID123"></div><div id="Headerbnr" class="mart_col_back"></div><div class="col-md-12"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert_notifcatio9" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert_notifcatio9" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger" id="alert_msg" ><label ><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg" alt="Error"> </label></div></div></div><div id="container" class="g4 pad-10 brdr except_sec"><table id="relpopup" class="ma_width_marg"><tbody><tr class="iconhvr brdbt" ><td class="wth350"><label class="padlt15mrgbt0">Key</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Key" class="bgcccwth10"><i   class="fa fa-info-circle fltlt"></i></a></td><td><input id="PRICEAGM_REV_AWARD_LEVELS_RECORD_ID" type="text" class="form-control related_popup_css" disabled=""><input id="ADDNEW__SYOBJR_30118_MMOBJ_00176" class="popup Look_up_search" type="image"  onclick="cont_openaddnew(this)" data-target="#cont_viewModalSection" data-toggle="modal" src="../mt/default/images/customer_lookup.gif" ></td><td class="fltrtbrdbto"><div class="col-md-12 editiconright"><a href="#" onclick="" class="editclick"><i class="fa fa-lock" aria-hidden="true"></i></a></div></td></tr><tr class="iconhvr brdbt" ><td class="wth350"><label class="padlt15mrgbt0">Program Award Level ID</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Program Award Level ID" class="bgcccwth10"><i   class="fa fa-info-circle fltlt"></i></a></td><td><input id="PRGAWDLVL_ID" type="text" class="form-control related_popup_css fltlt"   disabled=""></td><td class="fltrtbrdbto"><div class="col-md-12 editiconright"><a href="#" onclick="" class="editclick"><i class="fa fa-lock" aria-hidden="true"></i></a></div></td></tr><tr class="iconhvr brdbt" ><td class="wth350"><label class="padlt15mrgbt0">Program Award Level Name</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Program Award Level Name" class="bgcccwth10"><i   class="fa fa-info-circle fltlt"></i></a></td><td><input id="PRGAWD_TIER_NAME" type="text" onfocusout="attribute_checker(this)" value="" class="form-control related_popup_css ma_stylbrdr"  ></td><td class="fltrtbrdbto"><div class="col-md-12 editiconright"><a href="#" onclick="" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td></tr><tr class="iconhvr brdbt" style=" display: none;"><td class="wth350"><label class="padlt15mrgbt0">Program Award Level Record ID</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Program Award Level Record ID" class="bgcccwth10"><i  class="fltlt fa fa-info-circle"></i></a></td><td><input id="PROGRAM_AWARD_LEVEL_RECORD_ID" type="text" value="SVPGAL-07296" class="form-control related_popup_css" disabled=""></td><td class="fltrtbrdbto"><div class="col-md-12 editiconright"><a href="#" onclick="" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td></tr><tr class="iconhvr brdbt"><td class="wth350"><label class="padlt15mrgbt0">Program ID</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Program ID" class="bgcccwth10"><i   class="fa fa-info-circle fltlt"></i></a></td><td><input id="PROGRAM_ID" type="text"  class="form-control related_popup_css fltlt"   disabled=""></td><td class="fltrtbrdbto"><div class="col-md-12 editiconright"><a href="#" onclick="" class="editclick"><i class="fa fa-lock" aria-hidden="true"></i></a></div></td></tr><tr class="iconhvr brdbt"  ><td class="wth350"><label class="padlt15mrgbt0">Program Number</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Program Number" class="bgcccwth10"><i   class="fa fa-info-circle fltlt"></i></a></td><td><input id="PROGRAM_NUMBER" type="text" class="form-control related_popup_css fltlt"  disabled=""></td><td class="fltrtbrdbto"><div class="col-md-12 editiconright"><a href="#" onclick="" class="editclick"><i class="fa fa-lock" aria-hidden="true"></i></a></div></td></tr><tr class="iconhvr brdbt" ><td class="wth350"><label class="padlt15mrgbt0">Program Name</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Program Name" class="bgcccwth10"><i  class="fa fa-info-circle fltlt"></i></a></td><td><input id="PROGRAM_NAME" type="text" class="form-control related_popup_css fltlt"   disabled=""></td><td class="fltrtbrdbto"><div class="col-md-12 editiconright"><a href="#" onclick="" class="editclick"><i class="fa fa-lock" aria-hidden="true"></i></a></div></td></tr><tr class="iconhvr brdbt" style=" display: none;"><td class="wth350"><label class="padlt15mrgbt0">Price Agreement Record ID</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Price Agreement Record ID" class="bgcccwth10"><i  class="fa fa-info-circle fltlt"></i></a></td><td><input id="PRICEAGREEMENT_RECORD_ID" type="text" value="a5c2f362-50cf-4ae6-866b-85b799a90451" class="form-control related_popup_css" disabled=""></td><td class="fltrtbrdbto"><div class="col-md-12 editiconright"><a href="#" onclick="" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td></tr><tr class="iconhvr brdbt" ><td class="wth350"><label class="padlt15mrgbt0">Price Agreement ID</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Price Agreement ID" class="bgcccwth10"><i   class="fa fa-info-circle fltlt"></i></a></td><td><input id="PRICEAGREEMENT_ID" type="text" class="form-control related_popup_css fltlt"   ></td><td class="fltrtbrdbto"><div class="col-md-12 editiconright"><a href="#" onclick="" class="editclick"><i class="fa fa-lock" aria-hidden="true"></i></a></div></td></tr><tr class="iconhvr brdbt" ><td class="wth350"><label class="padlt15mrgbt0">Award or Point Name</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Award or Point Name" class="bgcccwth10"><i   class="fa fa-info-circle fltlt"></i></a></td><td><select id="AWARD_POINT_NAME" value="POINT NAME" type="text" class="form-control pop_up_brd_rad related_popup_css fltltfnt13brd1"><option>AWARD NAME</option><option selected="">POINT NAME</option></select></td><td class="fltrtbrdbto"><div class="col-md-12 editiconright"><a href="#" onclick="" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td></tr><tr class="iconhvr brdbt" ><td class="wth350"><label class="padlt15mrgbt0">Point Level Value</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Point Level Value" class="bgcccwth10""><i  class="fa fa-info-circle fltlt"></i></a></td><td><input id="POINT_LEVEL_VALUE" type="number" class="form-control related_popup_css ma_stylbrdr"  ></td><td class="fltrtbrdbto"><div class="col-md-12 editiconright"><a href="#" onclick="" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td></tr></tbody></table><div class="col-md-12"><div class="g4  except_sec removeHorLine iconhvr"><button type="button"  class="btnconfig btnMainBanner mar_lt_flt_lt" onclick="popup_cont_ProgramCancel(this)">CANCEL</button><button type="button" id="PASPAL" class="btnconfig btnMainBanner mar_lt_flt_lt"  onclick="popup_cont_ProgramSAVE(this)">SAVE</button></div></div></div>'
    return sec_str, "", ""
    #### SEGMENT REVISION MIGRATION CODE ENDS...


def SegmentProgramLookUp():
    sec_str = ""
    # select PROGRAM_AWARD_LEVEL_RECORD_ID from SVPGAL where PROGRAM_RECORD_ID ='SVABPG-107074' and PROGRAM_AWARD_LEVEL_RECORD_ID not in (select PROGRAM_AWARD_LEVEL_RECORD_ID from PASPAL where PRICEAGREEMENT_RECORD_ID ='a5c2f362-50cf-4ae6-866b-85b799a90451')
    return sec_str, "", ""


# Param Variables.
LABLE = Param.LABLE
Trace.Write("LABLE-----" + str(LABLE))
VALUE = Param.VALUE
Trace.Write("VALUE---" + str(VALUE))
TABLEID = Param.TABLEID
Trace.Write("TABLEID---123" + str(TABLEID))
OPERATION = Param.OPERATION
Trace.Write("OPERATION--------" + str(OPERATION))
RETURN = Param.RETURN
Trace.Write("RETURN--------" + str(RETURN))
try:
    RECORDID = Param.RECORDID
except:
    RECORDID = ""
Trace.Write("RECORDID---------" + str(RECORDID))
try:
    RECORDFEILD = Param.RECORDFEILD
except:
    RECORDFEILD = ""
Trace.Write("RECORDFEILD---" + str(RECORDFEILD))
NEWVAL = Param.NEWVAL
if RETURN == "1":
    Result = POPUPLISTVALUE(LABLE, VALUE, TABLEID, OPERATION, RECORDID, RECORDFEILD, RETURN, NEWVAL)
elif RETURN == "2":
    ApiResponse = ApiResponseFactory.JsonResponse(ProgramAddNew())
elif RETURN == "ProgramLookUp":
    ApiResponse = ApiResponseFactory.JsonResponse(SegmentProgramLookUp())
else:
    ApiResponse = ApiResponseFactory.JsonResponse(
        POPUPLISTVALUE(LABLE, VALUE, TABLEID, OPERATION, RECORDID, RECORDFEILD, RETURN, NEWVAL)
    )