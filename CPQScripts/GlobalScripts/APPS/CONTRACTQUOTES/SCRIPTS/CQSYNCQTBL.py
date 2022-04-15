# =========================================================================================================================================
#   __script_name : CQSYNCQTBL.PY
#   __script_description : THIS SCRIPT IS USED TO SYNC THE QUOTE TABLES AND CONTRACT QUOTE CUSTOM TABLES WHEN WE CREATE A QUOTE FROM C4C
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :01-10-2020
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# =========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import datetime
import time
from SYDATABASE import SQL
import clr
import sys
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
import re
from datetime import timedelta, date
import CQCPQC4CWB
import CQREVSTSCH
import CQPARTIFLW
import CQIFLSPARE

# ---------------------------------------------------CONFIGURATION------------------------------------------------#
Sql = SQL()

CUSTOM_FIELDS_DETAIL = [
    ("STPAccountID", "STPAccountID"),
    ("STPAccountName", "STPAccountName"),
    ("STPAccountType", "STPAccountType"),
    ("Region", "Region"),
    ("TransactionType", "TransactionType"),
    ("OpportunityId", "OpportunityId"),
    ("OpportunityType", "OpportunityType"),
    ("QuoteLevel", "QuoteLevel"),
    ("OpportunityOwner", "OpportunityOwner"),
    ("OpportunityStage", "OpportunityStage"),
    ("SalesOrgID", "SalesOrgID"),
    ("SalesOrgName", "SalesOrgName"),
    ("SalesUnit", "SalesUnit"),
    ("DistributionChannel", "DistributionChannel"),
    ("Division", "Division"),
    ("PrimaryContactName", "PrimaryContactName"),
    ("PrimaryContactId", "PrimaryContactId"),
    ("SoldToAddress", "SoldToAddress"),
    ("SoldToPhone", "SoldToPhone"),
    ("SoldToEmail", "SoldToEmail"),
    ("SalesOfficeID", "SalesOfficeID"),
    ("SalesPerson", "SalesPerson"),
    ("PaymentTerms", "PaymentTerms"),
    ("CustomerPO", "CustomerPO"),
    ("FabLocationID", "FabLocationID"),
    ("FabLocationName", "FabLocationName"),
    ("FabLocation", "FabLocation"),
    ("AdditionalShipToName", "AdditionalShipToName"),
    ("AdditionalShipToEmail", "AdditionalShipToEmail"),
    ("AdditionalShipToPhone", "AdditionalShipToPhone"),
    ("AdditionalShipToID", "AdditionalShipToID"),
    ("AdditionalShipToAddress1", "AdditionalShipToAddress1"),
    ("ContractType", "ContractType"),
    ("Currency", "Currency"),
    ("Incoterms", "Incoterms"),
    ("ExchangeRateType", "ExchangeRateType"),
    ("PayerName", "PayerName"),
    ("PayerAddress1", "PayerAddress1"),
    ("PayerCity", "PayerCity"),
    ("PayerState", "PayerState"),
    ("PayerCountry", "PayerCountry"),
    ("PayerPostalCode", "PayerPostalCode"),
    ("PayerEmail", "PayerEmail"),
    ("PayerPhone", "PayerPhone"),
    ("SellerName", "SellerName"),
    ("SellerAddress", "SellerAddress"),
    ("SellerEmail", "SellerEmail"),
    ("SellerPhone", "SellerPhone"),
    ("SalesUnitName", "SalesUnitName"),
    ("SalesUnitAddress", "SalesUnitAddress"),
    ("SalesUnitEmail", "SalesUnitEmail"),
    ("SalesUnitPhone", "SalesUnitPhone"),
    ("SalesEmployeeName", "SalesEmployeeName"),
    ("SalesEmployeePhone", "SalesEmployeePhone"),
    ("EmployeeResponsibleName", "EmployeeResponsibleName"),
    ("EmployeeResponsibleAddress", "EmployeeResponsibleAddress"),
    ("EmployeeResponsibleEmail", "EmployeeResponsibleEmail"),
    ("EmployeeResponsiblePhone", "EmployeeResponsiblePhone"),
    ("SalesPersonPhone", "SalesPersonPhone"),
    ("ContractManagerName", "ContractManagerName"),
    ("ContractManagerPhone", "ContractManagerPhone"),
    ("ContractManagerEmail", "ContractManagerEmail"),
    ("ContractManagerAddress", "ContractManagerAddress"),
    ("PaymentTermName", "PaymentTermName"),
    ("ContractManagerID", "ContractManagerID"),
    ("PayerID", "PayerID"),
    ("SellerID", "SellerID"),
    ("SalesUnitID", "SalesUnitID"),
    ("SalesEmployeeID", "SalesEmployeeID"),
    ("EmployeeResponsibleID", "EmployeeResponsibleID"),
    ("SalesEmployeeEmail", "SalesEmployeeEmail"),
    ("SalesEmployeeAddress", "SalesEmployeeAddress"),
    ("IncotermsLocation", "IncotermsLocation"),
    ("SourceContractID", "SourceContractID"),
    ("SourceAccountID", "SourceAccountID"),
    ("SourceAccountAddress", "SourceAccountAddress"),
    ("SourceAccountEmail", "SourceAccountEmail"),
    ("SourceAccountName", "SourceAccountName"),
    ("SourceAccountPhone", "SourceAccountPhone"),
    ("POES", "POES"),
    ("LOW", "LOW"),
    ("C4C_Quote_Object_ID", "C4C_Quote_Object_ID"),
    ("AccountAssignmentGroup", "AccountAssignmentGroup"),
    ("QuoteExpirationDate", "QuoteExpirationDate"),
    ("PricingDate", "PricingDate"),
    ("QuoteStartDate", "QuoteStartDate"),
    ("SIGFPOpportunityID", "SIGFPOpportunityID"),
    ("SIGFPOpportunityName","SIGFPOpportunityName"),
    ("SIGFPQuoteID","SIGFPQuoteID"),
    ("SIGFPQuoteDate","SIGFPQuoteDate"),
    ("LowID","LowID"),
]

# ---------------------------------------------------CONFIGURATION------------------------------------------------ #


class SyncQuoteAndCustomTables:
    def __init__(self, quote):
        self.quote_start_time = time.time()
        self.quote = quote
        self.field_mapping = CUSTOM_FIELDS_DETAIL
        self.datetime_formatting_fields = {
            "QuoteExpirationDate": self.datetime_format_field,
            "PricingDate": self.datetime_format_field,
            "QuoteStartDate": self.datetime_format_field,
        }

    def default_field_format(self, _field_name):
        return self.quote.GetCustomField(_field_name).Content

    def datetime_format_field(self, _field_name):
        return datetime.datetime.strptime(self.quote.GetCustomField(_field_name).Content, "%Y-%m-%d").date()

    def format(self, _field):
        return self.datetime_formatting_fields.get(_field, self.default_field_format)(_field)

    def _get_custom_fields_detail(self):
        _map_data = {}
        for fi, eld in self.field_mapping:
            _map_data[fi] = self.format(eld)
        return _map_data

    @staticmethod
    def get_formatted_date(year, month, day, date_format="", separator=""):
        stryear = str(year)
        strmonth = str(month)
        strday = str(day)

        if month < 10:
            strmonth = "0" + str(month)

        if day < 10:
            strday = "0" + str(day)
        date_str = date_format.format(Date=strday, Month=strmonth, Year=stryear, Separator=separator)
        return date_str

    def CreateEntitlements(self, quote_record_id):
        custom_fields_detail = self._get_custom_fields_detail()
        quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
        SAQTSVObj = Sql.GetList(
            "Select * from SAQTSV (nolock) where QUOTE_RECORD_ID= '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(
                QuoteRecordId=quote_record_id,
                quote_revision_record_id=Quote.GetGlobal("quote_revision_record_id"),
            )
        )
        x = datetime.datetime.today()
        x = str(x)
        y = x.split(" ")
        ent_disp_val = ent_val_code = get_tooltip_desc = ""
        for OfferingRow_detail in SAQTSVObj:

            Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"

            Fullresponse = ScriptExecutor.ExecuteGlobal(
                "CQENTLNVAL",
                {
                    "action": "GET_RESPONSE",
                    "partnumber": OfferingRow_detail.SERVICE_ID,
                    "request_url": Request_URL,
                    "request_type": "New",
                },
            )
            Fullresponse = str(Fullresponse).replace(": true", ': "true"').replace(": false", ': "false"')
            Fullresponse = eval(Fullresponse)
            if Fullresponse["complete"] == "true" and Fullresponse["consistent"] == "true":
                configuration_status = "COMPLETE"
            elif Fullresponse["complete"] == "false":
                configuration_status = "INCOMPLETE"
            else:
                configuration_status = "ERROR"
            attributesdisallowedlst = []
            attributeReadonlylst = []
            attributesallowedlst = []
            attributedefaultvalue = []
            overallattributeslist = []
            attributevalues = {}
            for rootattribute, rootvalue in Fullresponse.items():
                if rootattribute == "rootItem":
                    for Productattribute, Productvalue in rootvalue.items():
                        if Productattribute == "characteristics":
                            for prdvalue in Productvalue:
                                overallattributeslist.append(prdvalue["id"])
                                if prdvalue["visible"] == "false":
                                    attributesdisallowedlst.append(prdvalue["id"])
                                else:
                                    attributesallowedlst.append(prdvalue["id"])
                                if prdvalue["readOnly"] == "true":
                                    attributeReadonlylst.append(prdvalue["id"])
                                for attribute in prdvalue["values"]:
                                    attributevalues[str(prdvalue["id"])] = attribute["value"]
                                    if attribute["author"] in ("Default", "System"):
                                        Trace.Write("524------" + str(prdvalue["id"]))
                                        attributedefaultvalue.append(prdvalue["id"])

            attributesallowedlst = list(set(attributesallowedlst))
            overallattributeslist = list(set(overallattributeslist))
            Trace.Write("attributesallowedlst---" + str(attributesallowedlst))
            HasDefaultvalue = False
            get_tooltip_desc = AttributeID_Pass = ""
            ProductVersionObj = Sql.GetFirst(
                "Select product_id from product_versions(nolock) where SAPKBId = '"
                + str(Fullresponse["kbId"])
                + "' AND SAPKBVersion='"
                + str(Fullresponse["kbKey"]["version"])
                + "'"
            )
            if ProductVersionObj is not None:
                tbrow = {}
                insertservice = ""
                for attrs in overallattributeslist:
                    if attrs in attributevalues:
                        HasDefaultvalue = True
                        STANDARD_ATTRIBUTE_VALUES = Sql.GetFirst(
                            "SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(
                                attrs, attributevalues[attrs]
                            )
                        )
                        ent_disp_val = attributevalues[attrs]
                        ent_val_code = attributevalues[attrs]
                    else:
                        HasDefaultvalue = False
                        ent_disp_val = ""
                        ent_val_code = ""
                        STANDARD_ATTRIBUTE_VALUES = Sql.GetFirst(
                            "SELECT S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(
                                attrs
                            )
                        )
                    ATTRIBUTE_DEFN = Sql.GetFirst("SELECT * FROM ATTRIBUTE_DEFN (NOLOCK) WHERE SYSTEM_ID='{}'".format(attrs))
                    PRODUCT_ATTRIBUTES = Sql.GetFirst(
                        "SELECT A.ATT_DISPLAY_DESC,P.ATTRDESC FROM ATT_DISPLAY_DEFN (NOLOCK) A INNER JOIN PRODUCT_ATTRIBUTES (NOLOCK) P ON A.ATT_DISPLAY=P.ATT_DISPLAY WHERE P.PRODUCT_ID={} AND P.STANDARD_ATTRIBUTE_CODE={}".format(
                            ProductVersionObj.product_id,
                            STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,
                        )
                    )
                    if PRODUCT_ATTRIBUTES:
                        if PRODUCT_ATTRIBUTES.ATTRDESC:
                            get_tooltip_desc = PRODUCT_ATTRIBUTES.ATTRDESC
                        if PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC in ("Drop Down", "Check Box") and ent_disp_val:
                            get_display_val = Sql.GetFirst(
                                "SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(
                                    STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,
                                    attrs,
                                    attributevalues[attrs],
                                )
                            )
                            ent_disp_val = get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL

                        # A055S000P01-7401 START
                        if (
                            str(attrs)
                            in (
                                "AGS_POA_PROD_TYPE",
                                "AGS_{}_GEN_POAPDT".format(OfferingRow_detail.SERVICE_ID),
                            )
                            and ent_disp_val != ""
                        ):
                            val = ""
                            if str(ent_disp_val) == "Comprehensive":
                                val = "COMPREHENSIVE SERVICES"
                            elif str(ent_disp_val) == "Complementary":
                                val = "COMPLEMENTARY PRODUCTS"
                            Sql.RunQuery(
                                "UPDATE SAQTSV SET SERVICE_TYPE = '{}' WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                                    str(val),
                                    quote_record_id,
                                    OfferingRow_detail.SERVICE_ID,
                                    Quote.GetGlobal("quote_revision_record_id"),
                                )
                            )
                        # A055S000P01-7401 END
                        DTypeset = {
                            "Drop Down": "DropDown",
                            "Free Input, no Matching": "FreeInputNoMatching",
                            "Check Box": "CheckBox",
                        }

                        # 9226 starts
                        getquote_sales_val = ""
                        getslaes_value = Sql.GetFirst(
                            "SELECT SALESORG_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '" + str(OfferingRow_detail.QUOTE_RECORD_ID) + "'"
                        )
                        if getslaes_value:
                            getquote_sales_val = getslaes_value.SALESORG_ID

                        get_il_sales = Sql.GetList("select SALESORG_ID from SASORG where country = 'IL'")
                        get_il_sales_list = [val.SALESORG_ID for val in get_il_sales]
                        if ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME.upper() == "FAB LOCATION":
                            AttributeID_Pass = attrs
                            if getquote_sales_val in get_il_sales_list:
                                NewValue = "Israel"
                            else:
                                NewValue = "ROW"
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
                        </QUOTE_ITEM_ENTITLEMENT>""".format(
                            ent_name=str(attrs),
                            ent_val_code=ent_val_code,
                            ent_type=DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC] if PRODUCT_ATTRIBUTES else "",
                            ent_desc=ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME.replace("&", ";#38").replace(">", "&gt;").replace("<", "&lt;"),
                            ent_disp_val=ent_disp_val.replace("&", ";#38").replace(">", "&gt;").replace("<", "&lt;")
                            if HasDefaultvalue
                            else "",
                            ct="",
                            pi="",
                            is_default="1" if str(attrs) in attributedefaultvalue else "0",
                            pm="",
                            cf="",
                            tool_desc=get_tooltip_desc.replace("'", "''").replace("&", ";#38").replace(">", "&gt;").replace("<", "&lt;"),
                        )
                insertservice = insertservice.encode("ascii", "ignore").decode("ascii")
                tbrow.update({"QUOTE_SERVICE_ENTITLEMENT_RECORD_ID": str(Guid.NewGuid()).upper(),
                              "QUOTE_ID": OfferingRow_detail.QUOTE_ID, "ENTITLEMENT_XML": insertservice,
                              "QUOTE_NAME": OfferingRow_detail.QUOTE_NAME,
                              "QUOTE_RECORD_ID": OfferingRow_detail.QUOTE_RECORD_ID,
                              "QTESRV_RECORD_ID": OfferingRow_detail.QUOTE_SERVICE_RECORD_ID,
                              "SERVICE_RECORD_ID": OfferingRow_detail.SERVICE_RECORD_ID,
                              "SERVICE_ID": OfferingRow_detail.SERVICE_ID,
                              "SERVICE_DESCRIPTION": OfferingRow_detail.SERVICE_DESCRIPTION,
                              "CPS_CONFIGURATION_ID": Fullresponse["id"],
                              "SALESORG_RECORD_ID": OfferingRow_detail.SALESORG_RECORD_ID,
                              "SALESORG_ID": OfferingRow_detail.SALESORG_ID,
                              "SALESORG_NAME": OfferingRow_detail.SALESORG_NAME, "CPS_MATCH_ID": 1,
                              "CPQTABLEENTRYADDEDBY": User.Id,
                              "CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
                              "QTEREV_RECORD_ID": Quote.GetGlobal("quote_revision_record_id"),
                              "QTEREV_ID": Quote.GetGlobal("quote_revision_id"),
                              "CONFIGURATION_STATUS": configuration_status})

                columns = ", ".join("" + str(x) + "" for x in tbrow.keys())
                values = ", ".join("'" + str(x) + "'" for x in tbrow.values())

                insert_qtqtse_query = "INSERT INTO SAQTSE ( %s ) VALUES ( %s );" % (
                    columns,
                    values,
                )
                Sql.RunQuery(insert_qtqtse_query)
                if AttributeID_Pass:
                    try:
                        Trace.Write("312---AttributeID_Pass--" + str(AttributeID_Pass))

                        Trace.Write("312---AttributeID_Pass--" + str(AttributeID_Pass))
                        add_where = ""
                        ServiceId = OfferingRow_detail.SERVICE_ID
                        whereReq = "QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                            OfferingRow_detail.QUOTE_RECORD_ID,
                            OfferingRow_detail.SERVICE_ID,
                            Quote.GetGlobal("quote_revision_record_id"),
                        )
                        ent_params_list = (
                            str(whereReq)
                            + "||"
                            + str(add_where)
                            + "||"
                            + str(AttributeID_Pass)
                            + "||"
                            + str(NewValue)
                            + "||"
                            + str(ServiceId)
                            + "||"
                            + "SAQTSE"
                        )
                        result = ScriptExecutor.ExecuteGlobal(
                            "CQASSMEDIT",
                            {
                                "ACTION": "UPDATE_ENTITLEMENT",
                                "ent_params_list": ent_params_list,
                            },
                        )
                    except:
                        Trace.Write("error--296")
                # 9226 starts
                if AttributeID_Pass:
                    try:
                        add_where = ""
                        ServiceId = OfferingRow_detail.SERVICE_ID
                        whereReq = "QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                            OfferingRow_detail.QUOTE_RECORD_ID,
                            OfferingRow_detail.SERVICE_ID,
                            Quote.GetGlobal("quote_revision_record_id"),
                        )
                        ent_params_list = (
                            str(whereReq)
                            + "||"
                            + str(add_where)
                            + "||"
                            + str(AttributeID_Pass)
                            + "||"
                            + str(NewValue)
                            + "||"
                            + str(ServiceId)
                            + "||"
                            + "SAQTSE"
                        )
                        result = ScriptExecutor.ExecuteGlobal(
                            "CQASSMEDIT",
                            {
                                "ACTION": "UPDATE_ENTITLEMENT",
                                "ent_params_list": ent_params_list,
                            },
                        )
                    except:
                        Trace.Write("error--296")
                # 9226 ends
                try:
                    if "Z0016" in OfferingRow_detail.SERVICE_ID:
                        try:
                            QuoteEndDate = datetime.datetime.strptime(
                                Quote.GetCustomField("QuoteExpirationDate").Content,
                                "%Y-%m-%d",
                            ).date()
                            QuoteStartDate = datetime.datetime.strptime(
                                Quote.GetCustomField("QuoteStartDate").Content,
                                "%Y-%m-%d",
                            ).date()
                            contract_days = (QuoteEndDate - QuoteStartDate).days
                            ent_disp_val = str(contract_days)
                        except:
                            ent_disp_val = ent_disp_val

                        if int(ent_disp_val) > 364:
                            try:
                                quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
                                AttributeID = "AGS_CON_DAY"
                                NewValue = ent_disp_val
                                add_where = ""
                                ServiceId = OfferingRow_detail.SERVICE_ID
                                whereReq = (
                                    "QUOTE_RECORD_ID = '"
                                    + str(quote_record_id)
                                    + "' and SERVICE_ID LIKE '%Z0016%'  AND QTEREV_RECORD_ID = '"
                                    + str(quote_revision_record_id)
                                    + "'"
                                )
                                ent_params_list = (
                                    str(whereReq)
                                    + "||"
                                    + str(add_where)
                                    + "||"
                                    + str(AttributeID)
                                    + "||"
                                    + str(ent_disp_val)
                                    + "||"
                                    + str(ServiceId)
                                    + "||"
                                    + "SAQTSE"
                                )
                                result = ScriptExecutor.ExecuteGlobal(
                                    "CQASSMEDIT",
                                    {
                                        "ACTION": "UPDATE_ENTITLEMENT",
                                        "ent_params_list": ent_params_list,
                                    },
                                )
                            except:
                                pass
                except:
                    Trace.Write("except scenario----final--")
                # calling pre-logic valuedriver script
                try:
                    where_condition = " WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND SERVICE_ID = '{}' ".format(
                        quote_record_id,
                        quote_revision_record_id,
                        OfferingRow_detail.SERVICE_ID,
                    )

                    predefined = ScriptExecutor.ExecuteGlobal(
                        "CQVLDPRDEF",
                        {
                            "where_condition": where_condition,
                            "quote_rec_id": quote_record_id,
                            "level": "SERVICE_LEVEL",
                            "treeparam": OfferingRow_detail.SERVICE_ID,
                            "user_id": User.Id,
                            "quote_rev_id": quote_revision_record_id,
                        },
                    )

                except:
                    Trace.Write("EXCEPT----PREDEFINED DRIVER IFLOW")

    def create_custom_table_record(self):
        contract_quote_data = {}
        sync_start_time = time.time()

        try:
            if self.quote:
                quote_table_info = Sql.GetTable("SAQTMT")
                quote_involved_party_table_info = Sql.GetTable("SAQTIP")
                quote_opportunity_table_info = Sql.GetTable("SAOPQT")
                custom_fields_detail = self._get_custom_fields_detail()
                start_date = self.get_formatted_date(
                    custom_fields_detail.get("QuoteStartDate").year,
                    custom_fields_detail.get("QuoteStartDate").month,
                    custom_fields_detail.get("QuoteStartDate").day,
                    "{Month}{Separator}{Date}{Separator}{Year}",
                    "/",
                )
                end_date = self.get_formatted_date(
                    custom_fields_detail.get("QuoteExpirationDate").year,
                    custom_fields_detail.get("QuoteExpirationDate").month,
                    custom_fields_detail.get("QuoteExpirationDate").day,
                    "{Month}{Separator}{Date}{Separator}{Year}",
                    "/",
                )
                quote_id = self.quote.CompositeNumber
                quote_obj = Sql.GetFirst(
                    "SELECT * FROM SAQTMT (NOLOCK) WHERE QUOTE_ID = '{}' AND C4C_QUOTE_ID = '{}'".format(
                        quote_id, self.quote.CompositeNumber
                    )
                )
                # To Set the Quote Revision Record while refreshing the page..
                payid = ""
                paydesc = ""
                payrec = ""
                pay_days = pay_name = ""
                if not quote_obj:
                    if custom_fields_detail.get("SalesOrgID"):
                        salesorg_obj = Sql.GetFirst(
                            """
                            SELECT
                                SALESORG_ID,
                                SALES_ORG_RECORD_ID,
                                SALESORG_NAME,
                                REGION,
                                REGION_RECORD_ID,
                                COMPANY_ID,
                                COMPANY_NAME,
                                COMPANY_RECORD_ID
                            FROM
                                SASORG (NOLOCK)
                            WHERE
                                SALESORG_ID = '{}'
                            """.format(
                                custom_fields_detail.get("SalesOrgID")
                            )
                        )
                    if custom_fields_detail.get("STPAccountID"):
                        salesorg_country = Sql.GetFirst(
                            "SELECT COUNTRY,COUNTRY_RECORD_ID FROM SASORG (NOLOCK) WHERE SALESORG_ID = '{}'".format(
                                custom_fields_detail.get("SalesOrgID")
                            )
                        )
                        salesorg_country_name = Sql.GetFirst(
                            "SELECT COUNTRY_NAME FROM SACTRY (NOLOCK) WHERE COUNTRY = '{}'".format(salesorg_country.COUNTRY)
                        )

                    if custom_fields_detail.get("PaymentTerms"):
                        payterm_obj = Sql.GetFirst(
                            """
                            SELECT
                                PAYMENT_TERM_ID,
                                PAYMENT_TERM_NAME,
                                NUMBER_OF_DAYS,
                                PAYMENT_TERM_RECORD_ID,
                                DESCRIPTION
                            FROM
                                PRPTRM (NOLOCK)
                            WHERE
                                PAYMENT_TERM_ID = '{}'
                            """.format(
                                custom_fields_detail.get("PaymentTerms")
                            )
                        )
                        if payterm_obj:
                            payid = payterm_obj.PAYMENT_TERM_ID
                            paydesc = payterm_obj.DESCRIPTION
                            payrec = payterm_obj.PAYMENT_TERM_RECORD_ID
                            pay_days = payterm_obj.NUMBER_OF_DAYS
                            pay_name = payterm_obj.PAYMENT_TERM_NAME

                    created_date = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
                    # Please set native custom field CTX tag days calculation also:
                    # Quote Expiration Date - https://rssandbox.webcomcpq.com/admin/QuotePropertyEdit.aspx?Id=27
                    expired_date = date.today() + timedelta(days=365)

                    # A055S000P01-7866
                    quote_type = {
                        "ZTBC": "ZTBC - TOOL BASED",
                        "ZNBC": "ZNBC - NON TOOL BASED",
                        "ZWK1": "ZWK1 - SPARES",
                        "ZSWC": "ZSWC - SOLD WITH SYSTEM",
                    }
                    Region_Code = {
                        "01": "AMNA",
                        "02": "AMJ",
                        "03": "AME",
                        "04": "AMT",
                        "07": "AMK",
                        "08": "AMSEA",
                        "09": "AMC",
                    }
                    AccountAssignmentGroup = Region_Code.get(custom_fields_detail.get("AccountAssignmentGroup"))
                    # opportunity_type = {"ZTBC":"Service", "ZWK1":"Parts"}
                    contract_quote_data.update(
                        {
                            "QUOTE_ID": quote_id,
                            "C4C_QUOTE_ID": self.quote.CompositeNumber,
                            "MASTER_TABLE_QUOTE_RECORD_ID": str(Guid.NewGuid()).upper(),
                            "REGION": salesorg_obj.REGION,
                            # "SALESORG_ID": custom_fields_detail.get("SalesOrgID"),
                            "SALE_TYPE": custom_fields_detail.get("TransactionType"),
                            "QUOTE_STATUS": "IN-PROGRESS",
                            "QUOTE_LEVEL": custom_fields_detail.get("QuoteLevel")
                            if custom_fields_detail.get("QuoteLevel")
                            else "SALES ORG LEVEL",
                            "POES": custom_fields_detail.get("POES")
                            if custom_fields_detail.get("POES")
                            else "FALSE",  # A055S000P01-9777 Code starts..ends..
                            "LOW": custom_fields_detail.get("LOW") if custom_fields_detail.get("LOW") else "FALSE",
                            "EXPIRED": "FALSE",  # A055S000P01-12558
                            "CONTRACT_VALID_FROM": start_date,
                            "CONTRACT_VALID_TO": end_date,
                            "QUOTE_CREATED_DATE": str(created_date),
                            "QUOTE_EXPIRE_DATE": str(expired_date),
                            "QUOTE_NAME": self.quote.OpportunityName,  # custom_fields_detail.get("STPAccountName"),
                            "SOURCE_CONTRACT_ID": custom_fields_detail.get("SourceContractID"),
                            "QUOTE_TYPE": quote_type.get(custom_fields_detail.get("ContractType")),
                            "QUOTE_CURRENCY": custom_fields_detail.get("Currency"),
                            "GLOBAL_CURRENCY": "USD",
                            "QTEREV_STATUS": "NEW REVISION",
                        }
                    )
                    # insert in revision table while creating quote start
                    # quote_revision_table_info = Sql.GetTable("SAQTRV")
                    quote_revision_id = str(Guid.NewGuid()).upper()
                    get_rev_details = Sql.GetFirst(
                        """
                        SELECT
                            DISTINCT TOP 1000 CART2.CARTCOMPOSITENUMBER,
                            CART_REVISIONS.REVISION_ID as REVISION_ID,
                            CART_REVISIONS.DESCRIPTION as DESCRIPTION,
                            CART.ACTIVE_REV as ACTIVE_REV,
                            CART_REVISIONS.CART_ID as CART_ID,
                            CART_REVISIONS.PARENT_ID,
                            CART.USERID
                        FROM
                            CART_REVISIONS (nolock)
                            INNER JOIN CART2 (nolock) ON CART_REVISIONS.CART_ID = CART2.CartId
                            INNER JOIN CART(NOLOCK) ON CART.CART_ID = CART2.CartId
                        WHERE
                            CART2.CARTCOMPOSITENUMBER = '{}'
                            and CART.USERID = '{}'
                        """.format(
                            Quote.CompositeNumber, Quote.UserId
                        )
                    )
                    Quote.SetGlobal(
                        "contract_quote_record_id",
                        str(contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID")),
                    )
                    Quote.SetGlobal("quote_revision_record_id", str(quote_revision_id))
                    quote_rev_id = get_rev_details.REVISION_ID
                    Quote.SetGlobal("quote_revision_id", str(quote_rev_id))
                    expired_date_val = datetime.datetime.strptime(end_date, "%m/%d/%Y").date()
                    expired_date_val = expired_date_val + timedelta(days=365)

                    if custom_fields_detail.get("Currency"):
                        Currency_obj = Sql.GetFirst(
                            "SELECT CURRENCY,CURRENCY_NAME, CURRENCY_RECORD_ID FROM PRCURR (NOLOCK) WHERE CURRENCY = '{}'".format(
                                custom_fields_detail.get("Currency")
                            )
                        )
                        # get global currency_rec_id
                        global_currency_obj = Sql.GetFirst(
                            "SELECT CURRENCY,CURRENCY_NAME, CURRENCY_RECORD_ID FROM PRCURR (NOLOCK) WHERE CURRENCY = '{}'".format(
                                contract_quote_data.get("GLOBAL_CURRENCY")
                            )
                        )
                        if Currency_obj and global_currency_obj:
                            contract_quote_data.update(
                                {
                                    "QUOTE_CURRENCY": Currency_obj.CURRENCY,
                                    "QUOTE_CURRENCY_RECORD_ID": Currency_obj.CURRENCY_RECORD_ID,
                                    "GLOBAL_CURRENCY_RECORD_ID": global_currency_obj.CURRENCY_RECORD_ID,
                                }
                            )
                    if custom_fields_detail.get("EmployeeResponsibleID"):
                        Employee_obj = Sql.GetFirst(
                            "SELECT EMPLOYEE_ID,FIRST_NAME,LAST_NAME,EMPLOYEE_RECORD_ID FROM SAEMPL (NOLOCK) WHERE EMPLOYEE_ID = '{}'".format(
                                custom_fields_detail.get("EmployeeResponsibleID")
                            )
                        )
                        if Employee_obj:
                            Owner_name = Employee_obj.FIRST_NAME + " " + Employee_obj.LAST_NAME
                            contract_quote_data.update(
                                {
                                    "OWNER_ID": Employee_obj.EMPLOYEE_ID,
                                    "OWNER_NAME": Owner_name,
                                    "OWNER_RECORD_ID": Employee_obj.EMPLOYEE_RECORD_ID,
                                }
                            )

                    # insert in revision table while creating quote
                    if salesorg_obj and get_rev_details:
                        revision_start_date = datetime.datetime.now().strftime("%m/%d/%Y")
                        revision_end_date = date.today() + timedelta(days=365)
                        quote_salesorg_table_info = Sql.GetTable("SAQTRV")
                        salesorg_data = {
                            "QUOTE_REVISION_RECORD_ID": str(quote_revision_id),
                            "QUOTE_ID": quote_id,
                            "QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
                            "SALESORG_ID": custom_fields_detail.get("SalesOrgID"),
                            "COUNTRY": salesorg_country.COUNTRY,
                            "COUNTRY_NAME": salesorg_country_name.COUNTRY_NAME,
                            "COUNTRY_RECORD_ID": salesorg_country.COUNTRY_RECORD_ID,
                            "REGION": str(AccountAssignmentGroup),
                            "SALESORG_NAME": salesorg_obj.SALESORG_NAME,
                            "SALESORG_RECORD_ID": salesorg_obj.SALES_ORG_RECORD_ID,
                            "GLOBAL_CURRENCY": contract_quote_data.get("GLOBAL_CURRENCY"),
                            "GLOBAL_CURRENCY_RECORD_ID": contract_quote_data.get("GLOBAL_CURRENCY_RECORD_ID"),
                            "QTEREV_RECORD_ID": quote_revision_id,
                            "QTEREV_ID": quote_rev_id,
                            "REVISION_DESCRIPTION": "REVISION 0 DESCRIPTION",
                            "ACTIVE": get_rev_details.ACTIVE_REV,
                            "REV_CREATE_DATE": revision_start_date,
                            "REV_EXPIRE_DATE": "",
                            "REVISION_STATUS": "CFG-CONFIGURING",
                            "WORKFLOW_STATUS": "CONFIGURE",
                            "REV_APPROVE_DATE": "",
                            "CART_ID": get_rev_details.CART_ID,
                            "CONTRACT_VALID_FROM": start_date,
                            "CONTRACT_VALID_TO": end_date,
                            "PAYMENTTERM_DAYS": pay_days,
                            "PAYMENTTERM_ID": payid,
                            "PAYMENTTERM_NAME": pay_name,
                            "PAYMENTTERM_RECORD_ID": payrec,
                            "EXCHANGE_RATE_TYPE": custom_fields_detail.get("ExchangeRateType"),
                            "CANCELLATION_PERIOD": "180",
                            "CANCELLATION_PERIOD_NOTPER": "",
                            "COMPANY_ID": salesorg_obj.COMPANY_ID,
                            "COMPANY_NAME": salesorg_obj.COMPANY_NAME,
                            "COMPANY_RECORD_ID": salesorg_obj.COMPANY_RECORD_ID,
                            "INCOTERM_LOCATION": custom_fields_detail.get("IncotermsLocation"),
                            "HLV_ORG_BUN": "AGS - SSC",
                            "TRANSACTION_TYPE": "O-QUOTE",
                        }

                        if custom_fields_detail.get("AccountAssignmentGroup"):
                            region_object = Sql.GetFirst(
                                "SELECT REGION_RECORD_ID FROM SAREGN (NOLOCK) WHERE EXTERNAL_ID = '{}'".format(
                                    custom_fields_detail.get("AccountAssignmentGroup")
                                )
                            )
                            if region_object:
                                salesorg_data["REGION_RECORD_ID"] = region_object.REGION_RECORD_ID
                        exchange_rate_type_object = None
                        if custom_fields_detail.get("AccountAssignmentGroup"):
                            exchange_rate_type_object = Sql.GetFirst(
                                "SELECT BANK_ID, BANK_NAME, EXCRATTYP_ID, EXCHANGE_RATE_RECORD_ID FROM PRERTY (NOLOCK) WHERE REGION = '{}'".format(
                                    AccountAssignmentGroup
                                )
                            )
                            if exchange_rate_type_object:
                                salesorg_data.update(
                                    {
                                        "BANK_ID": exchange_rate_type_object.BANK_ID,
                                        "BANK_NAME": exchange_rate_type_object.BANK_NAME,
                                        "BANK_RECORD_ID": exchange_rate_type_object.EXCHANGE_RATE_RECORD_ID,
                                        "EXCHANGE_RATE_TYPE": exchange_rate_type_object.EXCRATTYP_ID,
                                    }
                                )

                        # UPDATE REVISION DETAILS TO SAQTMT
                        contract_quote_data.update(
                            {
                                "QTEREV_RECORD_ID": quote_revision_id,
                                "QTEREV_ID": quote_rev_id,
                            }
                        )
                        Quote.GetCustomField("QUOTE_REVISION_ID").Content = quote_revision_id
                        Quote.GetCustomField("QUOTE_REVISION_DESC").Content = salesorg_data.get("REVISION_DESCRIPTION")
                        Quote.GetCustomField("QUOTE_EXCHANGE_RATE").Content = salesorg_data.get("EXCHANGE_RATE")
                        Quote.GetCustomField("QUOTE_PAYMENT_TERM").Content = salesorg_data.get("PAYMENTTERM_NAME")
                        bluebook_obj = Sql.GetFirst(
                            """SELECT BLUEBOOK,BLUEBOOK_RECORD_ID FROM SAACNT WHERE ACCOUNT_ID = '{}' AND ACCOUNT_NAME = '{}'""".format(
                                custom_fields_detail.get("STPAccountID"),
                                custom_fields_detail.get("STPAccountName"),
                            )
                        )
                        if bluebook_obj:
                            if bluebook_obj.BLUEBOOK and bluebook_obj.BLUEBOOK_RECORD_ID:
                                salesorg_data.update(
                                    {
                                        "BLUEBOOK": bluebook_obj.BLUEBOOK,
                                        "BLUEBOOK_RECORD_ID": bluebook_obj.BLUEBOOK_RECORD_ID,
                                    }
                                )
                        if custom_fields_detail.get("Incoterms"):
                            getInc = Sql.GetFirst(
                                "SELECT INCOTERM_ID,DESCRIPTION,INCOTERM_RECORD_ID FROM SAICTM WHERE INCOTERM_ID = '{}'".format(
                                    custom_fields_detail.get("Incoterms")
                                )
                            )
                            if getInc:
                                salesorg_data.update(
                                    {
                                        "INCOTERM_ID": getInc.INCOTERM_ID,
                                        "INCOTERM_NAME": getInc.DESCRIPTION,
                                        "INCOTERM_RECORD_ID": getInc.INCOTERM_RECORD_ID,
                                    }
                                )

                        if custom_fields_detail.get("DistributionChannel"):
                            distribution_obj = Sql.GetFirst(
                                "SELECT DISTRIBUTION_CHANNEL_RECORD_ID, DISTRIBUTIONCHANNEL_ID FROM SADSCH (NOLOCK) WHERE DISTRIBUTIONCHANNEL_ID = '{}'".format(
                                    custom_fields_detail.get("DistributionChannel")
                                )
                            )
                            if distribution_obj:
                                salesorg_data.update(
                                    {
                                        "DISTRIBUTIONCHANNEL_ID": distribution_obj.DISTRIBUTIONCHANNEL_ID,
                                        "DISTRIBUTIONCHANNEL_RECORD_ID": distribution_obj.DISTRIBUTION_CHANNEL_RECORD_ID,
                                    }
                                )
                        if custom_fields_detail.get("SalesOrgID"):
                            createddate_up = ""
                            SalesOrg_obj = Sql.GetFirst(
                                "SELECT DEF_CURRENCY, DEF_CURRENCY_RECORD_ID FROM SASORG (NOLOCK) WHERE SALESORG_ID = '{}'".format(
                                    custom_fields_detail.get("SalesOrgID")
                                )
                            )

                            salesorg_currency = Sql.GetFirst(
                                "SELECT CURRENCY,CURRENCY_RECORD_ID FROM PRCURR (NOLOCK) WHERE CURRENCY = '"
                                + str(custom_fields_detail.get("Currency"))
                                + "'"
                            )
                            if salesorg_currency:
                                salesorg_data.update(
                                    {
                                        "DOC_CURRENCY": salesorg_currency.CURRENCY,
                                        "DOCCURR_RECORD_ID": salesorg_currency.CURRENCY_RECORD_ID,
                                    }
                                )
                            if SalesOrg_obj:
                                # A055S000P01-4418 exchange rate details starts..
                                exchange_obj = Sql.GetFirst(
                                    """
                                    SELECT
                                        EXCHANGE_RATE,
                                        EXCHANGE_RATE_BEGIN_DATE,
                                        EXCHANGE_RATE_END_DATE,
                                        EXCHANGE_RATE_RECORD_ID
                                    from
                                        PREXRT
                                    where
                                        FROM_CURRENCY = '{}'
                                        and TO_CURRENCY = '{}'
                                        AND ACTIVE = 1
                                        and EXCHANGE_RATE_TYPE = '{}'
                                    """.format(
                                        contract_quote_data.get("GLOBAL_CURRENCY"),
                                        salesorg_currency.CURRENCY,
                                        salesorg_data.get("EXCHANGE_RATE_TYPE"),
                                    )
                                )
                                if exchange_obj:
                                    createddate = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
                                    if createddate > exchange_obj.EXCHANGE_RATE_BEGIN_DATE:
                                        createddate_up = createddate
                                    else:
                                        createddate_up = exchange_obj.EXCHANGE_RATE_BEGIN_DATE

                                    salesorg_data.update(
                                        {
                                            "EXCHANGE_RATE": exchange_obj.EXCHANGE_RATE,
                                            "EXCHANGE_RATE_DATE": start_date,
                                            "EXCHANGERATE_RECORD_ID": exchange_obj.EXCHANGE_RATE_RECORD_ID,
                                        }
                                    )
                                    # A055S000P01-4418 exchange rate details ends..
                                else:
                                    # If condition commented for FPM scenario - getting currency = NTD, global currency = USD and exchnage rate tyep = ZC07.
                                    # There is no record for this combination in PREXRT so we update exchange rate as 1 and exchange rate as current date
                                    # if contract_quote_data.get("GLOBAL_CURRENCY") == salesorg_currency.CURRENCY:
                                    createddate = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
                                    salesorg_data.update(
                                        {
                                            "EXCHANGE_RATE": 1.00,
                                            "EXCHANGE_RATE_DATE": start_date,
                                        }
                                    )

                                # Commented the below code already we updated the exchange rate details in the above code..
                                # TO_CURRENCY_val = contract_quote_data.get("GLOBAL_CURRENCY")
                                # if 	TO_CURRENCY_val == 'USD' and SalesOrg_obj.DEF_CURRENCY == 'USD':
                                # 	try:
                                # 		QuoteStartDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteStartDate').Content, '%Y-%m-%d').date()
                                # 	except:
                                # 		QuoteStartDate =''
                                # 	Trace.Write('QuoteStartDate------'+str(QuoteStartDate))
                                # 	salesorg_data.update({'EXCHANGE_RATE':'1'})
                                # 	salesorg_data.update({'EXCHANGE_RATE_DATE':str(QuoteStartDate)})
                                # Commented the below code already we updated the exchange rate details in the above code..

                                # commented the below code we updated the exchange rate type from Custom field.
                                # exchange_rate_obj = Sql.GetFirst("SELECT EXCHANGE_RATE_TYPE from SASAAC where SALESORG_ID = '{}' and DIVISION_ID='{}' AND ACCOUNT_ID LIKE '%{}' AND DISTRIBUTIONCHANNEL_ID = '{}'".format(custom_fields_detail.get("SalesOrgID"),custom_fields_detail.get('Division'),custom_fields_detail.get("STPAccountID"),custom_fields_detail.get('DistributionChannel')))

                                # if exchange_rate_obj:
                                # salesorg_data.update({'EXCHANGE_RATE_TYPE':exchange_rate_obj.EXCHANGE_RATE_TYPE})
                        if custom_fields_detail.get("Division"):
                            division_obj = Sql.GetFirst(
                                "SELECT DIVISION_RECORD_ID, DIVISION_ID FROM SADIVN (NOLOCK) WHERE DIVISION_ID = '{}'".format(
                                    custom_fields_detail.get("Division")
                                )
                            )
                            if division_obj:
                                salesorg_data.update(
                                    {
                                        "DIVISION_RECORD_ID": division_obj.DIVISION_RECORD_ID,
                                        "DIVISION_ID": division_obj.DIVISION_ID,
                                    }
                                )

                        if custom_fields_detail.get("SalesOfficeID"):
                            salesoffice_obj = Sql.GetFirst(
                                "SELECT SALES_OFFICE_RECORD_ID, SALES_OFFICE_ID, SALES_OFFICE_NAME FROM SASLOF (NOLOCK) WHERE SALES_OFFICE_ID = '{}'".format(
                                    custom_fields_detail.get("SalesOfficeID")
                                )
                            )
                            if salesoffice_obj:
                                salesorg_data.update(
                                    {
                                        "SALESOFFICE_ID": salesoffice_obj.SALES_OFFICE_ID,
                                        "SALESOFFICE_NAME": salesoffice_obj.SALES_OFFICE_NAME,
                                        "SALESOFFICE_RECORD_ID": salesoffice_obj.SALES_OFFICE_RECORD_ID,
                                    }
                                )
                        if str(salesorg_data.get("SALESORG_ID")):
                            tax_details = Sql.GetFirst(
                                """
                                SELECT
                                    *
                                FROM
                                    SAASCT (NOLOCK)
                                WHERE
                                    SALESORG_ID = '{}'
                                    AND DISTRIBUTIONCHANNEL_ID = '{}'
                                    AND DIVISION_ID = '{}'
                                    AND COUNTRY_NAME = '{}'
                                    AND ACCOUNT_ID LIKE '%{}%'
                                """.format(
                                    salesorg_data.get("SALESORG_ID"),
                                    salesorg_data.get("DISTRIBUTIONCHANNEL_ID"),
                                    salesorg_data.get("DIVISION_ID"),
                                    salesorg_data.get("COUNTRY_NAME"),
                                    custom_fields_detail.get("STPAccountID"),
                                )
                            )

                            if tax_details:
                                salesorg_data.update(
                                    {
                                        "ACCTAXCAT_ID": tax_details.TAXCATEGORY_ID,
                                        "ACCTAXCAT_DESCRIPTION": tax_details.TAXCATEGORY_DESCRIPTION,
                                        "ACCTAXCAT_RECORD_ID": tax_details.TAXCATEGORY_RECORD_ID,
                                        "ACCTAXCLA_ID": tax_details.TAXCLASSIFICATION_ID,
                                        "ACCTAXCLA_DESCRIPTION": tax_details.TAXCLASSIFICATION_DESCRIPTION,
                                        "ACCTAXCLA_RECORD_ID": tax_details.TAXCLASSIFICATION_RECORD_ID,
                                    }
                                )
                        # Commented the condition to update the pricing procedure for both spare and tool based quote
                        # if 'SPARE' in str(contract_quote_data.get('QUOTE_TYPE')):
                        # Get Pricing Procedure

                        GetPricingProcedure = Sql.GetFirst(
                            """
                            SELECT
                                DISTINCT SASAPP.PRICINGPROCEDURE_ID,
                                SASAPP.PRICINGPROCEDURE_NAME,
                                SASAPP.PRICINGPROCEDURE_RECORD_ID,
                                SASAPP.DOCUMENT_PRICING_PROCEDURE,
                                SASAPP.CUSTOMER_PRICING_PROCEDURE
                            FROM
                                SASAPP (NOLOCK)
                                JOIN SASAAC (NOLOCK) ON SASAPP.SALESORG_ID = SASAAC.SALESORG_ID
                                AND SASAPP.DIVISION_ID = SASAAC.DIVISION_ID
                                AND SASAPP.DISTRIBUTIONCHANNEL_ID = SASAAC.DISTRIBUTIONCHANNEL_ID
                                JOIN SAQTRV (NOLOCK) ON SAQTRV.DIVISION_ID = SASAPP.DIVISION_ID
                                AND SAQTRV.DISTRIBUTIONCHANNEL_ID = SASAPP.DISTRIBUTIONCHANNEL_ID
                                AND SAQTRV.SALESORG_ID = SASAPP.SALESORG_ID
                            WHERE
                                SASAPP.DOCUMENT_PRICING_PROCEDURE = 'A'
                                AND SAQTRV.QUOTE_ID = '{}'
                                AND SAQTRV.QTEREV_RECORD_ID = '{}'
                            """.format(
                                quote_id, quote_revision_id
                            )
                        )

                        if GetPricingProcedure:
                            CustPricing = GetPricingProcedure.CUSTOMER_PRICING_PROCEDURE
                        else:
                            CustPricing = ""
                        if GetPricingProcedure:

                            UpdateSAQTRV = """
                            UPDATE
                                SAQTRV
                            SET
                                SAQTRV.PRICINGPROCEDURE_ID = '{pricingprocedure_id}',
                                SAQTRV.PRICINGPROCEDURE_NAME = '{prcname}',
                                SAQTRV.PRICINGPROCEDURE_RECORD_ID = '{prcrec}',
                                SAQTRV.DOCUMENT_PRICING_PROCEDURE = '{docpricingprocedure}'
                            WHERE
                                SAQTRV.QUOTE_ID = '{quote_id}'
                                AND SAQTRV.QTEREV_RECORD_ID = '{quote_revision_id}'
                            """.format(
                                pricingprocedure_id=GetPricingProcedure.PRICINGPROCEDURE_ID,
                                prcname=GetPricingProcedure.PRICINGPROCEDURE_NAME,
                                prcrec=GetPricingProcedure.PRICINGPROCEDURE_RECORD_ID,
                                customer_pricing_procedure=GetPricingProcedure.CUSTOMER_PRICING_PROCEDURE,
                                docpricingprocedure=GetPricingProcedure.DOCUMENT_PRICING_PROCEDURE,
                                quote_id=quote_id,
                                quote_revision_id=quote_revision_id,
                            )

                            Sql.RunQuery(UpdateSAQTRV)

                    if custom_fields_detail.get("STPAccountID"):
                        account_obj = Sql.GetFirst(
                            "SELECT ACCOUNT_RECORD_ID, ACCOUNT_TYPE FROM SAACNT(NOLOCK) WHERE ACCOUNT_ID LIKE '%{}'".format(
                                custom_fields_detail.get("STPAccountID")
                            )
                        )
                        getSales = Sql.GetFirst(
                            "SELECT CpqTableEntryId FROM SASOAC (NOLOCK) WHERE SALESORG_ID = '{}' AND ACCOUNT_ID = '{}'".format(
                                custom_fields_detail.get("SalesOrgID"),
                                custom_fields_detail.get("STPAccountID"),
                            )
                        )

                        if not account_obj:
                            getState = Sql.GetFirst(
                                "SELECT STATE_RECORD_ID FROM SACYST (NOLOCK) WHERE STATE = '{}' AND COUNTRY = '{}'".format(
                                    custom_fields_detail.get("PayerState"),
                                    custom_fields_detail.get("PayerCountry"),
                                )
                            )
                            NewAccountRecordId = str(Guid.NewGuid()).upper()
                            Sql.RunQuery(
                                """
                                INSERT INTO
                                    SAACNT (
                                        ACCOUNT_RECORD_ID,
                                        ACCOUNT_ID,
                                        ACCOUNT_NAME,
                                        ACCOUNT_TYPE,
                                        ACTIVE,
                                        ADDRESS_1,
                                        CITY,
                                        COUNTRY,
                                        COUNTRY_RECORD_ID,
                                        PHONE,
                                        POSTAL_CODE,
                                        REGION,
                                        REGION_RECORD_ID,
                                        STATE,
                                        STATE_RECORD_ID,
                                        CPQTABLEENTRYADDEDBY,
                                        CPQTABLEENTRYDATEADDED
                                    )
                                VALUES
                                (
                                        '{AccountRecordId}',
                                        '{AccountId}',
                                        '{AccountName}',
                                        '{Type}',
                                        1,
                                        '{Address}',
                                        '{City}',
                                        '{Country}',
                                        '{CountryRecordId}',
                                        '{Phone}',
                                        '{PostalCode}',
                                        '{Region}',
                                        '{RegionRecordId}',
                                        '{State}',
                                        '{StateRecordId}',
                                        '{UserName}',
                                        GETDATE()
                                    )
                            """.format(
                                    AccountRecordId=NewAccountRecordId,
                                    AccountId=custom_fields_detail.get("STPAccountID"),
                                    AccountName=custom_fields_detail.get("STPAccountName"),
                                    Type=custom_fields_detail.get("STPAccountType"),
                                    Address=custom_fields_detail.get("PayerAddress1"),
                                    City=custom_fields_detail.get("PayerCity"),
                                    Country=custom_fields_detail.get("PayerCountry"),
                                    CountryRecordId=salesorg_country.COUNTRY_RECORD_ID,
                                    Phone=custom_fields_detail.get("PayerPhone"),
                                    PostalCode=custom_fields_detail.get("PayerPostalCode"),
                                    Region="",
                                    RegionRecordId="",
                                    State=custom_fields_detail.get("PayerState"),
                                    StateRecordId=getState.STATE_RECORD_ID,
                                    UserName=User.UserName,
                                )
                            )
                            account_obj = Sql.GetFirst(
                                "SELECT ACCOUNT_RECORD_ID, ACCOUNT_TYPE FROM SAACNT(NOLOCK) WHERE ACCOUNT_ID LIKE '%{}'".format(
                                    custom_fields_detail.get("STPAccountID")
                                )
                            )
                        getAcc = Sql.GetFirst(
                            "SELECT ACCOUNT_RECORD_ID FROM SAACNT (NOLOCK) WHERE ACCOUNT_ID = '{}'".format(
                                custom_fields_detail.get("STPAccountID")
                            )
                        )

                        getDistr = Sql.GetFirst(
                            "SELECT CpqTableEntryId FROM SASOAC (NOLOCK) WHERE ACCOUNT_ID = '{}' AND SALESORG_ID = '{}' AND DISTRIBUTIONCHANNEL_ID = '{}'".format(
                                custom_fields_detail.get("STPAccountID"),
                                custom_fields_detail.get("SalesOrgID"),
                                distribution_obj.DISTRIBUTIONCHANNEL_ID,
                            )
                        )

                        getDiv = Sql.GetFirst(
                            "SELECT CpqTableEntryId FROM SASAAC (NOLOCK) WHERE ACCOUNT_ID = '{}' AND SALESORG_ID = '{}' AND DIVISION_ID = '{}'".format(
                                custom_fields_detail.get("STPAccountID"),
                                custom_fields_detail.get("SalesOrgID"),
                                division_obj.DIVISION_ID,
                            )
                        )

                        if not getSales:
                            NewSalesAccountRecordId = str(Guid.NewGuid()).upper()
                            Sql.RunQuery(
                                """
                                INSERT INTO
                                    SASOAC (
                                        SALESORG_ACCOUNTS_RECORD_ID,
                                        ACCOUNT_RECORD_ID,
                                        ACCOUNT_ID,
                                        ACCOUNT_NAME,
                                        DISTRIBUTIONCHANNEL_RECORD_ID,
                                        DISTRIBUTIONCHANNEL_ID,
                                        SALESORG_RECORD_ID,
                                        SALESORG_ID,
                                        SALESORG_NAME
                                    )
                                VALUES
                                (
                                        '{RecordId}',
                                        '{AccountRecordId}',
                                        '{AccountId}',
                                        '{AccountName}',
                                        '{DistRecordId}',
                                        '{DistId}',
                                        '{SalesRecordId}',
                                        '{SalesOrgId}',
                                        '{SalesOrgName}'
                                    )
                            """.format(
                                    RecordId=NewSalesAccountRecordId,
                                    AccountRecordId=getAcc.ACCOUNT_RECORD_ID,
                                    AccountId=custom_fields_detail.get("STPAccountID"),
                                    AccountName=custom_fields_detail.get("STPAccountName"),
                                    DistRecordId=distribution_obj.DISTRIBUTION_CHANNEL_RECORD_ID,
                                    DistId=distribution_obj.DISTRIBUTIONCHANNEL_ID,
                                    SalesRecordId=salesorg_obj.SALES_ORG_RECORD_ID,
                                    SalesOrgId=custom_fields_detail.get("SalesOrgID"),
                                    SalesOrgName=salesorg_obj.SALESORG_NAME,
                                )
                            )

                            if not getDiv or not getDistr:
                                incid = ""
                                incdesc = ""
                                increc = ""
                                if custom_fields_detail.get("Incoterms"):
                                    getInc = Sql.GetFirst(
                                        "SELECT INCOTERM_ID,DESCRIPTION,INCOTERM_RECORD_ID FROM SAICTM WHERE INCOTERM_ID = '{}'".format(
                                            custom_fields_detail.get("Incoterms")
                                        )
                                    )
                                    if getInc:
                                        incid = getInc.INCOTERM_ID
                                        incdesc = getInc.DESCRIPTION
                                        increc = getInc.INCOTERM_RECORD_ID

                                NewSalesAreaAccountRecordId = str(Guid.NewGuid()).upper()
                                Sql.RunQuery(
                                    """
                                    INSERT INTO
                                        SASAAC (
                                            SALES_AREA_ACCOUNT_RECORD_ID,
                                            ACCOUNT_RECORD_ID,
                                            ACCOUNT_ID,
                                            ACCOUNT_NAME,
                                            DISTRIBUTIONCHANNEL_RECORD_ID,
                                            DISTRIBUTIONCHANNEL_ID,
                                            SALESORG_RECORD_ID,
                                            SALESORG_ID,
                                            SALESORG_NAME,
                                            DIVISION_ID,
                                            DIVISION_RECORD_ID,
                                            CUSTOMER_PRICING_PROCEDURE,
                                            INCOTERM_ID,
                                            INCOTERM_DESCRIPTION,
                                            INCOTERM_RECORD_ID,
                                            PAYMENTTERM_ID,
                                            PAYMENTTERM_DESCRIPTION,
                                            PAYMENTTERM_RECORD_ID
                                        )
                                    VALUES
                                    (
                                            '{RecordId}',
                                            '{AccountRecordId}',
                                            '{AccountId}',
                                            '{AccountName}',
                                            '{DistRecordId}',
                                            '{DistId}',
                                            '{SalesRecordId}',
                                            '{SalesOrgId}',
                                            '{SalesOrgName}',
                                            '{DivisionId}',
                                            '{DivisionRecordId}',
                                            '{CustPricing}',
                                            '{incid}',
                                            '{incdesc}',
                                            '{increc}',
                                            '{payid}',
                                            '{paydesc}',
                                            '{payrec}'
                                        )
                                """.format(
                                        RecordId=NewSalesAreaAccountRecordId,
                                        AccountRecordId=getAcc.ACCOUNT_RECORD_ID,
                                        AccountId=custom_fields_detail.get("STPAccountID"),
                                        AccountName=custom_fields_detail.get("STPAccountName"),
                                        DistRecordId=distribution_obj.DISTRIBUTION_CHANNEL_RECORD_ID,
                                        DistId=distribution_obj.DISTRIBUTIONCHANNEL_ID,
                                        SalesRecordId=salesorg_obj.SALES_ORG_RECORD_ID,
                                        SalesOrgId=custom_fields_detail.get("SalesOrgID"),
                                        SalesOrgName=salesorg_obj.SALESORG_NAME,
                                        DivisionId=division_obj.DIVISION_ID,
                                        DivisionRecordId=division_obj.DIVISION_RECORD_ID,
                                        CustPricing=CustPricing,
                                        incid=incid,
                                        incdesc=incdesc,
                                        increc=increc,
                                        payid=payid,
                                        paydesc=paydesc,
                                        payrec=payrec,
                                    )
                                )
                                getCtry = Sql.GetFirst(
                                    "SELECT COUNTRY_RECORD_ID FROM SACTRY WHERE COUNTRY = '{}'".format(
                                        custom_fields_detail.get("PayerCountry")
                                    )
                                )
                                NewRecordId = str(Guid.NewGuid()).upper()
                                Sql.RunQuery(
                                    """
                                    INSERT INTO
                                        SAASCT (
                                            ACCOUNT_SALES_AREA_COUNTRY_TAX_RECORD_ID,
                                            ACCOUNT_RECORD_ID,
                                            ACCOUNT_ID,
                                            ACCOUNT_NAME,
                                            DISTRIBUTIONCHANNEL_RECORD_ID,
                                            DISTRIBUTIONCHANNEL_ID,
                                            SALESORG_RECORD_ID,
                                            SALESORG_ID,
                                            SALESORG_NAME,
                                            DIVISION_ID,
                                            DIVISION_RECORD_ID,
                                            COUNTRY,
                                            COUNTRY_NAME,
                                            COUNTRY_RECORD_ID
                                        )
                                    VALUES
                                    (
                                            '{RecordId}',
                                            '{AccountRecordId}',
                                            '{AccountId}',
                                            '{AccountName}',
                                            '{DistRecordId}',
                                            '{DistId}',
                                            '{SalesRecordId}',
                                            '{SalesOrgId}',
                                            '{SalesOrgName}',
                                            '{DivisionId}',
                                            '{DivisionRecordId}',
                                            '{Country}',
                                            '{CountryName}',
                                            '{CountryRecordId}'
                                        )
                                    """.format(
                                        RecordId=NewRecordId,
                                        AccountRecordId=getAcc.ACCOUNT_RECORD_ID,
                                        AccountId=custom_fields_detail.get("STPAccountID"),
                                        AccountName=custom_fields_detail.get("STPAccountName"),
                                        DistRecordId=distribution_obj.DISTRIBUTION_CHANNEL_RECORD_ID,
                                        DistId=distribution_obj.DISTRIBUTIONCHANNEL_ID,
                                        SalesRecordId=salesorg_obj.SALES_ORG_RECORD_ID,
                                        SalesOrgId=custom_fields_detail.get("SalesOrgID"),
                                        SalesOrgName=salesorg_obj.SALESORG_NAME,
                                        DivisionId=division_obj.DIVISION_ID,
                                        DivisionRecordId=division_obj.DIVISION_RECORD_ID,
                                        Country=salesorg_country.COUNTRY,
                                        CountryName=salesorg_country_name.COUNTRY_NAME,
                                        CountryRecordId=getCtry.COUNTRY_RECORD_ID,
                                    )
                                )

                        if account_obj:
                            contract_quote_data.update(
                                {
                                    "ACCOUNT_RECORD_ID": account_obj.ACCOUNT_RECORD_ID,
                                    "ACCOUNT_ID": custom_fields_detail.get("STPAccountID"),
                                    "ACCOUNT_NAME": custom_fields_detail.get("STPAccountName"),
                                }
                            )

                            if custom_fields_detail.get("OpportunityId"):
                                opportunity_obj = Sql.GetFirst(
                                    """
                                    SELECT
                                        OPPORTUNITY_RECORD_ID,
                                        OPPORTUNITY_ID,
                                        OPPORTUNITY_STAGE,
                                        OPPORTUNITY_NAME
                                    FROM
                                        SAOPPR(NOLOCK)
                                    WHERE
                                        OPPORTUNITY_ID = '{}'
                                        AND ACCOUNT_RECORD_ID = '{}'
                                    """.format(
                                        custom_fields_detail.get("OpportunityId"),
                                        contract_quote_data.get("ACCOUNT_RECORD_ID"),
                                    )
                                )
                                Opportunitystagedict = {}
                                if custom_fields_detail.get("OpportunityStage"):
                                    Opportunitystagedict = {
                                        "Z0001": "NEW",
                                        "Z0002": "DEFINE OPPORTUNITY",
                                        "Z0003": "CONFIGURE QUOTE",
                                        "Z0004": "MANUAL PRICING REQUESTED",
                                        "Z0005": "FINANCE/BD/NSDR/APPROVAL",
                                        "Z0006": "FINANCE/BD/NSDR APPROVED",
                                        "Z0007": "QUOTE GENERATED",
                                        "Z0008": "QUOTE ACCEPTED â€“ CUSTOMER",
                                        "Z0009": "BOOKING SUBMITTED",
                                        "Z0010": "WON",
                                        "Z0011": "STOPPED",
                                        "Z0012": "LOST",
                                        "Z0013": "POES PRICING REQUESTED",
                                        "Z0014": "POES PRICING GENERATED",
                                        "Z0017": "PRICING DETERMINED",
                                    }
                                if not opportunity_obj:
                                    master_opportunity_table_info = Sql.GetTable("SAOPPR")
                                    master_opportunity_data = {
                                        "OPPORTUNITY_RECORD_ID": str(Guid.NewGuid()).upper(),
                                        "ACCOUNT_ID": custom_fields_detail.get("STPAccountID"),
                                        "ACCOUNT_NAME": custom_fields_detail.get("STPAccountName"),
                                        "ACCOUNT_RECORD_ID": account_obj.ACCOUNT_RECORD_ID,
                                        "DOCUMENT_TYPE": contract_quote_data.get("DOCUMENT_TYPE"),
                                        "CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
                                        "OPPORTUNITY_ID": custom_fields_detail.get("OpportunityId"),
                                        "OPPORTUNITY_NAME": self.quote.OpportunityName,
                                        "OPPORTUNITY_TYPE": custom_fields_detail.get("OpportunityType"),
                                        "SALESORG_ID": salesorg_data.get("SALESORG_ID"),
                                        "SALESORG_NAME": salesorg_data.get("SALESORG_NAME"),
                                        "SALESORG_RECORD_ID": salesorg_data.get("SALESORG_RECORD_ID"),
                                        "SALE_TYPE": "NEW",
                                        "OPPORTUNITY_STAGE": Opportunitystagedict.get(custom_fields_detail.get("OpportunityStage")),
                                        "ACCOUNT_TYPE": "Sold to Party",
                                        "OPPORTUNITY_OWNER_ID": custom_fields_detail.get("OpportunityOwner"),
                                        "SIGFP_OPP_ID":custom_fields_detail.get("SIGFPOpportunityID"),
                                        "SIGFP_OPR_NAME":custom_fields_detail.get("SIGFPOpportunityName"),
                                        "SIGFP_QUOTE_ID":custom_fields_detail.get("SIGFPQuoteID"),
                                        "SIGFP_QUOTE_DATE":custom_fields_detail.get("SIGFPQuoteDate"),
                                        "LOW_ID":custom_fields_detail.get("LowID"),
                                    }
                                    master_opportunity_table_info.AddRow(master_opportunity_data)
                                    Sql.Upsert(master_opportunity_table_info)
                                    opportunity_obj = Sql.GetFirst(
                                        """SELECT OPPORTUNITY_RECORD_ID, OPPORTUNITY_ID, OPPORTUNITY_NAME, OPPORTUNITY_STAGE FROM SAOPPR(NOLOCK) 
                                                            WHERE OPPORTUNITY_RECORD_ID = '{}'""".format(
                                            master_opportunity_data.get("OPPORTUNITY_RECORD_ID")
                                        )
                                    )
                                opportunity_quote_data = {
                                    "OPPORTUNITY_QUOTE_RECORD_ID": str(Guid.NewGuid()).upper(),
                                    "OPPORTUNITY_ID": opportunity_obj.OPPORTUNITY_ID,
                                    "OPPORTUNITY_NAME": opportunity_obj.OPPORTUNITY_NAME,
                                    "OPPORTUNITY_RECORD_ID": opportunity_obj.OPPORTUNITY_RECORD_ID,
                                    "QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
                                    "POES": custom_fields_detail.get("POES")
                                    if custom_fields_detail.get("POES")
                                    else "FALSE",  # A055S000P01-9777 Code starts..ends...
                                    "CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
                                    "QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
                                    "ACCOUNT_ID": custom_fields_detail.get("STPAccountID"),
                                    "ACCOUNT_NAME": custom_fields_detail.get("STPAccountName"),
                                    "ACCOUNT_TYPE": account_obj.ACCOUNT_TYPE,
                                    "C4C_QTEOBJ_ID": custom_fields_detail.get("C4C_Quote_Object_ID"),
                                    "SIGFP_OPP_ID":custom_fields_detail.get("SIGFPOpportunityID"), ##A055S000P01-18093 code starts..
                                    "SIGFP_OPR_NAME":custom_fields_detail.get("SIGFPOpportunityName"),
                                    "SIGFP_QUOTE_ID":custom_fields_detail.get("SIGFPQuoteID"),
                                    "SIGFP_QUOTE_DATE":custom_fields_detail.get("SIGFPQuoteDate"),
                                    "LOW_ID":custom_fields_detail.get("LowID") ##A055S000P01-18093 code ends..
                                }
                                Log.Info("opportunity_quote_data---"+str(opportunity_quote_data))
                                quote_opportunity_table_info.AddRow(opportunity_quote_data)
                    # A055S000P01-12754 code starts...
                    if (
                        custom_fields_detail.get("SalesOrgID")
                        and custom_fields_detail.get("Division")
                        and custom_fields_detail.get("STPAccountID")
                        and custom_fields_detail.get("DistributionChannel")
                    ):
                        salesorg_account_obj = Sql.GetFirst(
                            """
                            SELECT
                                CURRENCY,
                                CURRENCY_RECORD_ID
                            FROM
                                SASAAC (NOLOCK)
                            WHERE
                                SALESORG_ID = '{}'
                                AND DIVISION_ID = '{}'
                                AND ACCOUNT_ID = '{}'
                                AND DISTRIBUTIONCHANNEL_ID = '{}'
                            """.format(
                                custom_fields_detail.get("SalesOrgID"),
                                custom_fields_detail.get("Division"),
                                custom_fields_detail.get("STPAccountID"),
                                custom_fields_detail.get("DistributionChannel"),
                            )
                        )
                        if salesorg_account_obj:
                            salesorg_data.update(
                                {
                                    "DOC_CURRENCY": salesorg_account_obj.CURRENCY,
                                    "DOCCURR_RECORD_ID": salesorg_account_obj.CURRENCY_RECORD_ID,
                                }
                            )
                    # A055S000P01-12754 code ends..

                    # Updating the Document currency into the SAQTRV TABLE...
                    if custom_fields_detail.get("STPAccountID"):
                        get_customer_segment = Sql.GetFirst(
                            "Select AGS_CUST_SGMT FROM SAACNT(NOLOCK) WHERE ACCOUNT_ID ='{account_id}'".format(
                                account_id=custom_fields_detail.get("STPAccountID")
                            )
                        )
                        if get_customer_segment:
                            customer_level = str(get_customer_segment.AGS_CUST_SGMT).upper()
                        else:
                            customer_level = ""
                        quote_involved_party_table_info.AddRow({
                            "QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
                            "ADDRESS": custom_fields_detail.get("SoldToAddress"),
                            "EMAIL": custom_fields_detail.get("SoldToEmail"),
                            "PRIMARY": "1",
                            "QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
                            "QUOTE_NAME": self.quote.OpportunityName,  # custom_fields_detail.get("STPAccountName"),
                            "QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
                            "PARTY_ID": custom_fields_detail.get("STPAccountID"),
                            "PARTY_NAME": custom_fields_detail.get("STPAccountName"),
                            "CPQ_PARTNER_FUNCTION": "SOLD TO",
                            "PHONE": custom_fields_detail.get("SoldToPhone"),
                            "QTEREV_RECORD_ID": quote_revision_id,
                            "QTEREV_ID": quote_rev_id,
                            "CUSTOMER_SEGMENT": customer_level,
                        })
                    if self.quote.BillToCustomer:
                        bill_to_customer = self.quote.BillToCustomer
                        quote_involved_party_table_info.AddRow({
                            "QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
                            "ADDRESS": bill_to_customer.Address1
                            + ", "
                            + bill_to_customer.City
                            + ", "
                            + bill_to_customer.StateAbbreviation
                            + ", "
                            + bill_to_customer.CountryAbbreviation
                            + ", "
                            + bill_to_customer.ZipCode,
                            "EMAIL": bill_to_customer.Email,
                            "PRIMARY": bill_to_customer.Active,
                            "QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
                            "QUOTE_NAME": self.quote.OpportunityName,
                            "QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
                            "PARTY_ID": bill_to_customer.CustomerCode,
                            "PARTY_NAME": bill_to_customer.FirstName,
                            "CPQ_PARTNER_FUNCTION": "BILL TO",
                            "PHONE": bill_to_customer.BusinessPhone,
                            "QTEREV_RECORD_ID": quote_revision_id,
                            "QTEREV_ID": quote_rev_id,
                        })

                    if self.quote.ShipToCustomer:
                        partner_function_obj = Sql.GetFirst("Select * from SYPFTY(nolock) where PARTNERFUNCTION_ID = 'SH'")
                        ship_to_customer = self.quote.ShipToCustomer
                        quote_involved_party_table_info.AddRow({
                            "QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
                            "ADDRESS": ship_to_customer.Address1
                            + ", "
                            + ship_to_customer.City
                            + ", "
                            + ship_to_customer.StateAbbreviation
                            + ", "
                            + ship_to_customer.CountryAbbreviation
                            + ", "
                            + ship_to_customer.ZipCode,
                            "EMAIL": ship_to_customer.Email,
                            "PRIMARY": ship_to_customer.Active,
                            "QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
                            "QUOTE_NAME": self.quote.OpportunityName,
                            "QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
                            "PARTY_ID": ship_to_customer.CustomerCode,
                            "PARTY_NAME": ship_to_customer.FirstName,
                            "CPQ_PARTNER_FUNCTION": "SHIP TO",
                            "PHONE": ship_to_customer.BusinessPhone,
                            "QTEREV_RECORD_ID": quote_revision_id,
                            "QTEREV_ID": quote_rev_id,
                            "PARTNERFUNCTION_DESC": partner_function_obj.PARTNERFUNCTION_DESCRIPTION,
                            "PARTNERFUNCTION_ID": partner_function_obj.PARTNERFUNCTION_ID,
                            "PARTNERFUNCTION_RECORD_ID": partner_function_obj.PARTNERFUNCTION_RECORD_ID,
                        })
                    if custom_fields_detail.get("PayerID"):
                        quote_involved_party_table_info.AddRow({
                            "QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
                            "ADDRESS": custom_fields_detail.get("PayerAddress1"),
                            "EMAIL": custom_fields_detail.get("PayerEmail"),
                            "PRIMARY": "1",
                            "QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
                            "QUOTE_NAME": self.quote.OpportunityName,
                            "QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
                            "PARTY_ID": custom_fields_detail.get("PayerID"),
                            "PARTY_NAME": custom_fields_detail.get("PayerName"),
                            "CPQ_PARTNER_FUNCTION": "PAYER",
                            "PHONE": custom_fields_detail.get("PayerPhone"),
                            "QTEREV_RECORD_ID": quote_revision_id,
                            "QTEREV_ID": quote_rev_id,
                        })
                    if custom_fields_detail.get("AdditionalShipToName"):
                        quote_involved_party_table_info.AddRow({
                            "QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
                            "ADDRESS": custom_fields_detail.get("AdditionalShipToAddress1"),
                            "EMAIL": custom_fields_detail.get("AdditionalShipToEmail"),
                            "PRIMARY": "0",
                            "QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
                            "QUOTE_NAME": self.quote.OpportunityName,
                            "QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
                            "PARTY_ID": custom_fields_detail.get("AdditionalShipToID"),
                            "PARTY_NAME": custom_fields_detail.get("AdditionalShipToName"),
                            "CPQ_PARTNER_FUNCTION": "SHIP TO",
                            "PHONE": custom_fields_detail.get("AdditionalShipToPhone"),
                            "QTEREV_RECORD_ID": quote_revision_id,
                            "QTEREV_ID": quote_rev_id,
                        })
                    if custom_fields_detail.get("SellerID"):
                        SellerDetails = {
                            "QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
                            "ADDRESS": custom_fields_detail.get("SellerAddress"),
                            "EMAIL": custom_fields_detail.get("SellerEmail"),
                            "PRIMARY": "1",
                            "QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
                            "QUOTE_NAME": self.quote.OpportunityName,
                            "QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
                            "PARTY_ID": custom_fields_detail.get("SellerID"),
                            "PARTY_NAME": custom_fields_detail.get("SellerName"),
                            "CPQ_PARTNER_FUNCTION": "SELLER",
                            "PHONE": custom_fields_detail.get("SellerPhone"),
                            "QTEREV_RECORD_ID": quote_revision_id,
                            "QTEREV_ID": quote_rev_id,
                        }
                        quote_involved_party_table_info.AddRow(SellerDetails)
                    if custom_fields_detail.get("SalesUnitID"):
                        quote_involved_party_table_info.AddRow({
                            "QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
                            "ADDRESS": custom_fields_detail.get("SalesUnitAddress"),
                            "EMAIL": custom_fields_detail.get("SalesUnitEmail"),
                            "PRIMARY": "1",
                            "QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
                            "QUOTE_NAME": self.quote.OpportunityName,
                            "QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
                            "PARTY_ID": custom_fields_detail.get("SalesUnitID"),
                            "PARTY_NAME": custom_fields_detail.get("SalesUnitName"),
                            "CPQ_PARTNER_FUNCTION": "SALES UNIT",
                            "PHONE": custom_fields_detail.get("SalesUnitPhone"),
                            "QTEREV_RECORD_ID": quote_revision_id,
                            "QTEREV_ID": quote_rev_id,
                        })

                    if custom_fields_detail.get("SourceAccountID"):
                        quote_involved_party_table_info.AddRow({
                            "QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
                            "ADDRESS": custom_fields_detail.get("SourceAccountAddress"),
                            "EMAIL": custom_fields_detail.get("SourceAccountEmail"),
                            "PRIMARY": "1",
                            "QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
                            "QUOTE_NAME": self.quote.OpportunityName,
                            "QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
                            "PARTY_ID": custom_fields_detail.get("SourceAccountID"),
                            "PARTY_NAME": custom_fields_detail.get("SourceAccountName"),
                            "CPQ_PARTNER_FUNCTION": "SOURCE ACCOUNT",
                            "PHONE": custom_fields_detail.get("SourceAccountPhone"),
                            "QTEREV_RECORD_ID": quote_revision_id,
                            "QTEREV_ID": quote_rev_id,
                        })
                    quote_salesorg_table_info.AddRow(salesorg_data)
                    Sql.Upsert(quote_salesorg_table_info)
                    quote_table_info.AddRow(contract_quote_data)
                    Sql.Upsert(quote_table_info)
                    Sql.Upsert(quote_opportunity_table_info)
                    Sql.Upsert(quote_involved_party_table_info)
                    GetPricingProcedure = Sql.GetFirst(
                        """
                        SELECT
                            DISTINCT SASAPP.PRICINGPROCEDURE_ID,
                            SASAPP.PRICINGPROCEDURE_NAME,
                            SASAPP.PRICINGPROCEDURE_RECORD_ID,
                            SASAPP.DOCUMENT_PRICING_PROCEDURE,
                            SASAPP.CUSTOMER_PRICING_PROCEDURE
                        FROM
                            SASAPP (NOLOCK)
                            JOIN SASAAC (NOLOCK) ON SASAPP.SALESORG_ID = SASAAC.SALESORG_ID
                            AND SASAPP.DIVISION_ID = SASAAC.DIVISION_ID
                            AND SASAPP.DISTRIBUTIONCHANNEL_ID = SASAAC.DISTRIBUTIONCHANNEL_ID
                            JOIN SAQTRV (NOLOCK) ON SAQTRV.DIVISION_ID = SASAPP.DIVISION_ID
                            AND SAQTRV.DISTRIBUTIONCHANNEL_ID = SASAPP.DISTRIBUTIONCHANNEL_ID
                            AND SAQTRV.SALESORG_ID = SASAPP.SALESORG_ID
                        WHERE
                            SASAPP.DOCUMENT_PRICING_PROCEDURE = 'A'
                            AND SAQTRV.QUOTE_ID = '{}'
                            AND SAQTRV.QTEREV_RECORD_ID = '{}'
                        """.format(
                            quote_id, quote_revision_id
                        )
                    )

                    if GetPricingProcedure:
                        UpdateSAQTRV = """
                        UPDATE
                            SAQTRV
                        SET
                            SAQTRV.PRICINGPROCEDURE_ID = '{pricingprocedure_id}',
                            SAQTRV.PRICINGPROCEDURE_NAME = '{prcname}',
                            SAQTRV.PRICINGPROCEDURE_RECORD_ID = '{prcrec}',
                            SAQTRV.DOCUMENT_PRICING_PROCEDURE = '{docpricingprocedure}'
                        WHERE
                            SAQTRV.QUOTE_ID = '{quote_id}'
                            AND SAQTRV.QTEREV_RECORD_ID = '{quote_revision_id}'
                        """.format(
                            pricingprocedure_id=GetPricingProcedure.PRICINGPROCEDURE_ID,
                            prcname=GetPricingProcedure.PRICINGPROCEDURE_NAME,
                            prcrec=GetPricingProcedure.PRICINGPROCEDURE_RECORD_ID,
                            customer_pricing_procedure=GetPricingProcedure.CUSTOMER_PRICING_PROCEDURE,
                            docpricingprocedure=GetPricingProcedure.DOCUMENT_PRICING_PROCEDURE,
                            quote_id=quote_id,
                            quote_revision_id=quote_revision_id,
                        )
                        Sql.RunQuery(UpdateSAQTRV)

                    # Calling the iflow script to insert the records into SAQRSH custom table(Capture Date/Time for Quote Revision Status update.)
                    CQREVSTSCH.Revisionstatusdatecapture(
                        Quote.GetGlobal("contract_quote_record_id"),
                        Quote.GetGlobal("quote_revision_record_id"),
                    )
                    # Insert SAQCBC while creating quote in c4c - start A055S000P01-11413
                    checklist_desc = [
                        "Signed agreement is current or a temporary extension is approved by legal. If using a quote and PO, they must be valid.",
                        "Signed agreement has all of the terms and conditions that would be on a PO. (i.e. ship to, bill to, incoterms, payment terms, etc..). If Std Svc, Proj Eng, & FTS under $1M and booking using a quote and PO,all SOW terms must be listed on the quote and PO must reference quote.",
                        "All customer-facing agreements require legal review/approval per the SAM (except NDAs) and must receive a Legal Review Mark prior to being signed by Applied. Note: This does not apply to contracts for WEB, Solar products and services, and if booking using a PO and Quote, legal does not need to review as long as all terms are listed on the quote and a sales order acknowledgement is sent to the customer.",
                        "The customer PO and/or any other document (e.g. SOW, CL) or communication relating to the order received does not contain unacceptable commercial terms such as:",
                        "-The right to receive Appliedâ€™s best pricing for purchased products or services;",
                        "-The right to receive better or more favorable pricing compared than other Applied customers;",
                        "-Process or method patent infringement indemnification by Applied;",
                        "-The customer right to review or audit any Applied sales records",
                        "The master agreement is valid for the full duration for the contract booking (Contact the Law Department 6for expired Master Agreements).",
                        "The master agreement is referenced on the PO/Signed Agreement and the Quote.",
                        "Terms, Conditions, and Pricing on the Quote, PO, and/or Sales Agreement are per Master Agreement.",
                        "Clarification letters received for any exceptions or non standard approvals (legal entity and dollar amount changes required a change PO, a revised signed agreement, or an ORCA exception).",
                        "Delivery Dates and INCO terms on the PO match the signed agreement/quote (applicable to FPM and equipment upgrades).",
                        "Proper sizing and billing data available in a PO, the signed agreement, or a clarification letter in order to book for the full duration.For Variable bookings:",
                        "-You can only book for the full duration of the deal if the customer is committing to the full $ within the agreement;",
                        "-If you do not have commitment for the full duration but you have a customer commitment to a minimum purchase, you can book for the minimum committed $;",
                        "-If you have a signed agreement with an estimate $, no commitment from the customer, PO/No PO, you book for $1.",
                        "Enter 0 if the customer can walk away at any time for the duration of the agreement.",
                        "Enter NA if there is a cancellation/termination of convenience clause stating the contract cannot be cancelled or if the cancellation/termination for convenience cannot be identified (silent).",
                        "Enter NA for POES and MEA",
                        "When using the Ts&Cs shown on the website link on the bottom of the quote, enter 90 days",
                        "If the agreement with the customer provides a specific number of days to cancel at their convenience,enter that number of days. If there is no cancellation for an initial period of time, enter the total period (i.e.18 months no cancel + 90 days cancellation = 637 days entered).",
                        "All CRM Service Contracts must include equipment numbers. (Excluding FPM)",
                        "The Contract/P.O. is made out to the correct Applied Materials entity for the specific delivery location (e.g., Applied Materials, Inc for US delivery locations or Applied Materials South East Asia Pte. Ltd. ALL non US delivery locations).",
                        "If any tax is applicable, it is capture at the correct rate on the quote, PO, and/or the signed agreement.",
                        "If booking using a Quote and PO, the funding amount on PO matches or exceeds the Quote (partial POs require a clarification from the customer on the remaining PO submission).",
                        "PO references the Signed Agreement or Quote",
                        "If booking with a PO, the terms match the quote.(i.e. ship to, bill to, payment terms, etc)",
                        "The start and end dates on each line are accurate against the signed agreement, PO, quote, or CL",
                        "The billing amounts for each line are accurate against the signed agreement, PO, quote, or CL",
                        "SDA assessment worksheet attached (Display only) and specify RRA CAR/SHPOD",
                        "The signed customer spec has been received (if applicable)",
                        'If this booking requires an MEA template, obtain a copy of the template from Sales. Attach the template to the booking package and email a copy of the template to regional finance and Judy Mock. If the answer to any of the following questions is "yes", the MEA template is required:',
                        "-Does this transaction include deliverables other than a single service? If the answer to this question is Yes but the additional deliverables are for ONLY Services (PMSA, Standard service, Managed Services or Credits that have amounts which are all priced out then an MEA is not needed and thus the answer to the question should be NA.",
                        "-Is this a POSS Deal? The MEA template only has to be initiated at the time of booking.",
                        "-Are there any deliverables free of charge or not priced out e.g. CSA sold with an NSO at 1 price for both items?",
                    ]
                    checklist_id = 0
                    finalchecklist_id = 0
                    for field_desc in checklist_desc:
                        if re.match(r"^\-", field_desc):
                            checklist_id = str(finalchecklist_id) + "." + str(cnt)
                            field_desc = re.sub(r"^\-", "", field_desc)
                            cnt += 1
                        else:
                            finalchecklist_id = finalchecklist_id + 1
                            checklist_id = finalchecklist_id
                            cnt = 1
                        insert_saqcbc = """
                        INSERT INTO
                            SAQCBC (
                                QUOTE_REV_CLEAN_BOOKING_CHECKLIST_ID,
                                CPQTABLEENTRYADDEDBY,
                                CPQTABLEENTRYDATEADDED,
                                CHECKLIST_DESCRIPTION,
                                CHECKLIST_ID,
                                COMMENT,
                                SERVICE_CONTRACT,
                                SPECIALIST_REVIEW,
                                QUOTE_ID,
                                QUOTE_RECORD_ID,
                                QTEREV_ID,
                                QTEREV_RECORD_ID
                            )
                        VALUES
                        (
                                '{AccountRecordId}',
                                '{UserName}',
                                GETDATE(),
                                '{description}',
                                '{chek_id}',
                                '',
                                'False',
                                'False',
                                '{quote_id}',
                                '{quote_rec_id}',
                                '{quote_rev_id}',
                                '{quote_rev_rec_id}'
                            )
                        """.format(
                            AccountRecordId=str(Guid.NewGuid()).upper(),
                            UserName=User.UserName,
                            quote_id=salesorg_data.get("QUOTE_ID"),
                            quote_rec_id=salesorg_data.get("QUOTE_RECORD_ID"),
                            quote_rev_id=salesorg_data.get("QTEREV_ID"),
                            quote_rev_rec_id=salesorg_data.get("QTEREV_RECORD_ID"),
                            description=field_desc,
                            chek_id=checklist_id,
                        )
                        insert_saqcbc = insert_saqcbc.encode("ascii", "ignore").decode("ascii")
                        Sql.RunQuery(insert_saqcbc)

                    # CALLING IFLOW C4C_TO_CPQ_TOOLS
                    LOGIN_CREDENTIALS = Sql.GetFirst("SELECT USER_NAME AS Username,Password,Domain FROM SYCONF where Domain='AMAT_TST'")
                    if LOGIN_CREDENTIALS is not None:
                        Login_Username = str(LOGIN_CREDENTIALS.Username)
                        Login_Password = str(LOGIN_CREDENTIALS.Password)
                        authorization = Login_Username + ":" + Login_Password
                        binaryAuthorization = UTF8.GetBytes(authorization)
                        authorization = Convert.ToBase64String(binaryAuthorization)
                        authorization = "Basic " + authorization

                        webclient = System.Net.WebClient()
                        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
                        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization

                        LOGIN_CRE = Sql.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME  ='C4C_TO_CPQ_TOOLS'")

                        QuoteId_info = contract_quote_data.get("C4C_QUOTE_ID")
                        OpportunityId_info = custom_fields_detail.get("OpportunityId")

                        requestdata = (
                            '{\n  "OpportunityId": "'
                            + str(OpportunityId_info)
                            + '",\n  "QuoteId": "'
                            + str(QuoteId_info)
                            + '"\n,\n  "PrimaryContactId": "'
                            + str(custom_fields_detail.get("PrimaryContactId"))
                            + '"\n}'
                        )

                        response_SAQTMT = webclient.UploadString(str(LOGIN_CRE.URL), str(requestdata))

                    payload_json_obj = Sql.GetFirst(
                        "SELECT INTEGRATION_PAYLOAD, CpqTableEntryId FROM SYINPL (NOLOCK) WHERE INTEGRATION_KEY = '{}' AND ISNULL(STATUS,'') = ''".format(
                            contract_quote_data.get("C4C_QUOTE_ID")
                        )
                    )

                    if payload_json_obj:
                        contract_quote_obj = None
                        fab_location_ids, service_ids = [], []
                        equipment_data = {}
                        covered_object_data = {}
                        payload_json = eval(payload_json_obj.INTEGRATION_PAYLOAD)
                        payload_json = eval(payload_json.get("Param"))
                        payload_json = payload_json.get("CPQ_Columns")
                        if payload_json.get("OPPORTUNITY_ID"):
                            contract_quote_obj = Sql.GetFirst(
                                """
                                SELECT
                                    SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID,
                                    SAQTMT.QUOTE_ID,
                                    SAQTMT.QUOTE_NAME,
                                    SAQTMT.ACCOUNT_RECORD_ID,
                                    SAQTMT.CONTRACT_VALID_FROM,
                                    SAQTMT.CONTRACT_VALID_TO
                                FROM
                                    SAQTMT (NOLOCK)
                                WHERE
                                    SAQTMT.C4C_QUOTE_ID = '{}'
                                """.format(
                                    contract_quote_data.get("C4C_QUOTE_ID")
                                )
                            )
                        if payload_json.get("C4C_Opportunity_Object_ID"):
                            c4c_opppbj_id = payload_json.get("C4C_Opportunity_Object_ID")
                            c4c_Opportunity_obj = (
                                "UPDATE SAOPPR SET C4C_OPPOBJ_ID = '{c4c_opppbj_id}' where OPPORTUNITY_ID = '{OpportunityId}'".format(
                                    c4c_opppbj_id=payload_json.get("C4C_Opportunity_Object_ID"),
                                    OpportunityId=custom_fields_detail.get("OpportunityId"),
                                )
                            )
                            Sql.RunQuery(c4c_Opportunity_obj)
                        if payload_json.get("FAB_LOCATION_IDS"):
                            fab_location_ids = "','".join(
                                list(
                                    set(
                                        [
                                            str(int(fab_location))
                                            for fab_location in payload_json.get("FAB_LOCATION_IDS").split(",")
                                            if fab_location
                                        ]
                                    )
                                )
                            )
                        product_offering = []
                        if payload_json.get("SERVICE_IDS"):
                            service_ids = "','".join(list(set(payload_json.get("SERVICE_IDS").split(","))))
                            if re.match(r"C4C_GEN_SRV", payload_json.get("SERVICE_IDS")):
                                service_id_first = payload_json.get("SERVICE_IDS").split(",")[1]
                            else:
                                service_id_first = payload_json.get("SERVICE_IDS").split(",")[0]

                            product_offering = payload_json.get("SERVICE_IDS").split(",")

                        if payload_json.get("SAQFEQ"):
                            for equipment_json_data in payload_json.get("SAQFEQ"):
                                if equipment_json_data.get("FAB_LOCATION_ID") in equipment_data:
                                    equipment_data[equipment_json_data.get("FAB_LOCATION_ID")].append(
                                        equipment_json_data.get("EQUIPMENT_ID")
                                    )
                                else:
                                    equipment_data[equipment_json_data.get("FAB_LOCATION_ID")] = [equipment_json_data.get("EQUIPMENT_ID")]

                        # A055S000P01-8690 starts..
                        if payload_json.get("SAEMPL"):
                            employee = payload_json.get("SAEMPL")
                            quote_object = Sql.GetFirst(
                                "select QUOTE_ID from SAQDLT(NOLOCK) where QUOTE_ID = '{}'".format(contract_quote_data.get("C4C_QUOTE_ID"))
                            )
                            if not quote_object:
                                if type(employee) is dict:
                                    employee_obj = Sql.GetFirst(
                                        "select EMPLOYEE_ID from SAEMPL(nolock) where EMPLOYEE_ID = '{employee_id}'".format(
                                            employee_id=employee.get("EMPLOYEE_ID")
                                        )
                                    )
                                    if employee_obj is None:
                                        country_obj = Sql.GetFirst(
                                            "select COUNTRY_RECORD_ID from SACTRY(nolock) where COUNTRY = '{country}'".format(
                                                country=employee.get("COUNTRY")
                                            )
                                        )
                                        salesorg_obj = Sql.GetFirst(
                                            "select STATE_RECORD_ID from SASORG(nolock) where STATE = '{state}'".format(
                                                state=employee.get("STATE")
                                            )
                                        )
                                        employee_dict = {"EMPLOYEE_RECORD_ID": str(Guid.NewGuid()).upper(),
                                                         "ADDRESS_1": employee.get("ADDRESS1"),
                                                         "ADDRESS_2": employee.get("ADDRESS2"),
                                                         "CITY": employee.get("CITY"),
                                                         "COUNTRY": employee.get("COUNTRY"),
                                                         "COUNTRY_RECORD_ID": country_obj.COUNTRY_RECORD_ID if country_obj else "",
                                                         "EMAIL": employee.get("EMAIL"),
                                                         "EMPLOYEE_ID": employee.get("EMPLOYEE_ID"),
                                                         "EMPLOYEE_NAME": employee.get("EMPLOYEE_NAME"),
                                                         "EMPLOYEE_STATUS": employee.get("EMPLOYEE_STATUS"),
                                                         "FIRST_NAME": employee.get("FIRST_NAME"),
                                                         "LAST_NAME": employee.get("LAST_NAME"),
                                                         "PHONE": employee.get("PHONE"),
                                                         "POSTAL_CODE": employee.get("POSTAL_CODE"),
                                                         "STATE": employee.get("STATE"),
                                                         "STATE_RECORD_ID": salesorg_obj.STATE_RECORD_ID if salesorg_obj else "",
                                                         "CRM_EMPLOYEE_ID": employee.get("CRM_EMPLOYEE_ID"),
                                                         "C4C_EMPLOYEE_ID": employee.get("C4C_EMPLOYEE_ID"),
                                                         "CPQTABLEENTRYADDEDBY": User.UserName,
                                                         "CpqTableEntryModifiedBy": User.Id,
                                                         "ADDUSR_RECORD_ID": User.Id}
                                        tableInfo = Sql.GetTable("SAEMPL")
                                        tablerow = employee_dict
                                        tableInfo.AddRow(tablerow)
                                        Sql.Upsert(tableInfo)
                                    else:
                                        c4c_employee_update = "UPDATE SAEMPL SET C4C_EMPLOYEE_ID = '{c4c_employee_id}' WHERE EMPLOYEE_ID = '{employee_id}'".format(
                                            c4c_employee_id=employee.get("C4C_EMPLOYEE_ID"),
                                            employee_id=employee.get("EMPLOYEE_ID"),
                                        )
                                        Sql.RunQuery(c4c_employee_update)
                                    self.salesteam_insert(
                                        employee,
                                        contract_quote_data,
                                        quote_rev_id,
                                        quote_revision_id,
                                        custom_fields_detail,
                                    )
                                else:
                                    for employee in payload_json.get("SAEMPL"):
                                        employee_obj = SqlHelper.GetFirst(
                                            "select EMPLOYEE_ID from SAEMPL(nolock) where EMPLOYEE_ID = '{employee_id}'".format(
                                                employee_id=employee.get("EMPLOYEE_ID")
                                            )
                                        )
                                        if employee_obj is None:
                                            country_obj = SqlHelper.GetFirst(
                                                "select COUNTRY_RECORD_ID from SACTRY(nolock) where COUNTRY = '{country}'".format(
                                                    country=employee.get("COUNTRY")
                                                )
                                            )
                                            salesorg_obj = SqlHelper.GetFirst(
                                                "select STATE_RECORD_ID from SASORG(nolock) where STATE = '{state}'".format(
                                                    state=employee.get("STATE")
                                                )
                                            )
                                            employee_dict = {
                                                "EMPLOYEE_RECORD_ID": str(Guid.NewGuid()).upper(),
                                                "ADDRESS_1": employee.get("ADDRESS1"),
                                                "ADDRESS_2": employee.get("ADDRESS2"),
                                                "CITY": employee.get("CITY"),
                                                "COUNTRY": employee.get("COUNTRY"),
                                                "COUNTRY_RECORD_ID": country_obj.COUNTRY_RECORD_ID if country_obj else "",
                                                "EMAIL": employee.get("EMAIL"),
                                                "EMPLOYEE_ID": employee.get("EMPLOYEE_ID"),
                                                "EMPLOYEE_NAME": employee.get("EMPLOYEE_NAME"),
                                                "EMPLOYEE_STATUS": employee.get("EMPLOYEE_STATUS"),
                                                "FIRST_NAME": employee.get("FIRST_NAME"),
                                                "LAST_NAME": employee.get("LAST_NAME"),
                                                "PHONE": employee.get("PHONE"),
                                                "POSTAL_CODE": employee.get("POSTAL_CODE"),
                                                "STATE": employee.get("STATE"),
                                                "STATE_RECORD_ID": salesorg_obj.STATE_RECORD_ID if salesorg_obj else "",
                                                "CRM_EMPLOYEE_ID": employee.get("CRM_EMPLOYEE_ID"),
                                                "C4C_EMPLOYEE_ID": employee.get("C4C_EMPLOYEE_ID"),
                                                "CPQTABLEENTRYADDEDBY": User.UserName,
                                                "CpqTableEntryModifiedBy": User.Id,
                                                "ADDUSR_RECORD_ID": User.Id,
                                            }
                                            tableInfo = Sql.GetTable("SAEMPL")
                                            tablerow = employee_dict
                                            tableInfo.AddRow(tablerow)
                                            Sql.Upsert(tableInfo)
                                        else:
                                            c4c_employee_update = "UPDATE SAEMPL SET C4C_EMPLOYEE_ID = '{c4c_employee_id}' WHERE EMPLOYEE_ID = '{employee_id}'".format(
                                                c4c_employee_id=employee.get("C4C_EMPLOYEE_ID"),
                                                employee_id=employee.get("EMPLOYEE_ID"),
                                            )
                                            Sql.RunQuery(c4c_employee_update)
                                        self.salesteam_insert(
                                            employee,
                                            contract_quote_data,
                                            quote_rev_id,
                                            quote_revision_id,
                                            custom_fields_detail,
                                        )
                            employee_object = Sql.GetFirst(
                                "SELECT FIRST_NAME,LAST_NAME,EMPLOYEE_ID,EMPLOYEE_RECORD_ID FROM SAEMPL WHERE EMPLOYEE_ID = '{employee_id}'".format(
                                    employee_id=custom_fields_detail.get("EmployeeResponsibleID")
                                )
                            )
                            if employee_object is not None:
                                Sql.RunQuery(
                                    """
                                    UPDATE
                                        SAQTMT
                                    SET
                                        OWNER_ID = '{owner_id}',
                                        OWNER_NAME = '{owner_name}',
                                        OWNER_RECORD_ID = '{owner_record_id}'
                                    WHERE
                                        QUOTE_ID = '{Quote_Id}'
                                    """.format(
                                        Quote_Id=contract_quote_data.get("C4C_QUOTE_ID"),
                                        owner_id=employee_object.EMPLOYEE_ID,
                                        owner_name=employee_object.FIRST_NAME + " " + employee_object.LAST_NAME,
                                        owner_record_id=employee_object.EMPLOYEE_RECORD_ID,
                                    )
                                )
                        # A055S000P01-8690 endss..
                        #MULTIPLE CONTACT FROM C4C to CPQ Completed
                        
                        if payload_json.get("SAQICT"):
                            for employees in payload_json.get("SAQICT"):
                                employee_obj = Sql.GetFirst("select EMPLOYEE_ID from SAEMPL(nolock) where CRM_EMPLOYEE_ID = '{crm_employee_id}'".format(crm_employee_id=employees.get("CRM_EMPLOYEE_ID")))
                                partner_function_obj = Sql.GetFirst("Select * from SYPFTY(nolock) where PARTNERFUNCTION_ID = 'CP'")
                                contact_master_table = Sql.GetFirst("SELECT CONTACT_RECORD_ID FROM SACONT (NOLOCK) WHERE CONTACT_ID = '{contact_id}'".format(contact_id=employees.get("PRIMARY_CONTACT_ID")))
                                if employee_obj is None:
                                    country_obj = Sql.GetFirst("select COUNTRY_RECORD_ID from SACTRY(nolock) where COUNTRY = '{country}'".format(country=employees.get("COUNTRY")))
                                    salesorg_obj = Sql.GetFirst("select STATE_RECORD_ID from SASORG(nolock) where STATE = '{state}'".format(state=employees.get("STATE")))
                                    try:
                                        employee_dict = {"EMPLOYEE_RECORD_ID": str(Guid.NewGuid()).upper(),
                                                        "ADDRESS_1": employees.get("ADDRESS1"),
                                                        "ADDRESS_2": employees.get("ADDRESS2"),
                                                        "CITY": employees.get("CITY"),
                                                        "COUNTRY": employees.get("COUNTRY"),
                                                        "COUNTRY_RECORD_ID": country_obj.COUNTRY_RECORD_ID if country_obj else "",
                                                        "EMAIL": employees.get("EMAIL"),
                                                        "EMPLOYEE_ID": employees.get("PRIMARY_CONTACT_ID"),
                                                        "EMPLOYEE_NAME": employees.get("PRIMARY_CONTACT_NAME"),
                                                        "EMPLOYEE_STATUS": employees.get("EMPLOYEE_STATUS"),
                                                        "FIRST_NAME": employees.get("FIRST_NAME"),
                                                        "LAST_NAME": employees.get("LAST_NAME"),
                                                        "PHONE": employees.get("PHONE"),
                                                        "POSTAL_CODE": employees.get("POSTAL_CODE"),
                                                        "STATE": employees.get("STATE"),
                                                        "STATE_RECORD_ID": salesorg_obj.STATE_RECORD_ID if salesorg_obj else "",
                                                        "CRM_EMPLOYEE_ID": employees.get("CRM_EMPLOYEE_ID"),
                                                        "CPQTABLEENTRYADDEDBY": User.UserName,
                                                        "CpqTableEntryModifiedBy": User.Id,
                                                        "ADDUSR_RECORD_ID": User.Id}
                                    except:
                                          employee_dict = {"EMPLOYEE_RECORD_ID": str(Guid.NewGuid()).upper(),
                                                        "ADDRESS_1": employees.get("ADDRESS1"),
                                                        "ADDRESS_2": employees.get("ADDRESS2"),
                                                        "CITY": employees.get("CITY"),
                                                        "COUNTRY": employees.get("COUNTRY"),
                                                        "COUNTRY_RECORD_ID": country_obj.COUNTRY_RECORD_ID if country_obj else "",
                                                        "EMAIL": employees.get("EMAIL"),
                                                        "EMPLOYEE_ID": employees.get("PRIMARY_CONTACT_ID"),
                                                        "EMPLOYEE_NAME": employees.get("PRIMARY_CONTACT_NAME").encode("utf-8"),
                                                        "EMPLOYEE_STATUS": employees.get("EMPLOYEE_STATUS"),
                                                        "FIRST_NAME": employees.get("FIRST_NAME").encode("utf-8"),
                                                        "LAST_NAME": employees.get("LAST_NAME").encode("utf-8"),
                                                        "PHONE": employees.get("PHONE"),
                                                        "POSTAL_CODE": employees.get("POSTAL_CODE"),
                                                        "STATE": employees.get("STATE"),
                                                        "STATE_RECORD_ID": salesorg_obj.STATE_RECORD_ID if salesorg_obj else "",
                                                        "CRM_EMPLOYEE_ID": employees.get("CRM_EMPLOYEE_ID"),
                                                        "CPQTABLEENTRYADDEDBY": User.UserName,
                                                        "CpqTableEntryModifiedBy": User.Id,
                                                        "ADDUSR_RECORD_ID": User.Id} 
                                    tableInfo = Sql.GetTable("SAEMPL")
                                    tablerow = employee_dict
                                    tableInfo.AddRow(tablerow)
                                    Sql.Upsert(tableInfo)      
                                if contact_master_table is None:
                                    employee_obj = Sql.GetFirst("select EMPLOYEE_ID from SAEMPL(nolock) where CRM_EMPLOYEE_ID = '{crm_employee_id}'".format(crm_employee_id=employees.get("CRM_EMPLOYEE_ID")))
                                    contact_master_table_update = {"CONTACT_RECORD_ID": str(Guid.NewGuid()).upper(),
                                                                    "ADDRESS": employee_obj.ADDRESS_1 or "",
                                                                    "CITY": employee_obj.CITY,
                                                                    "CONTACT_ID": employees.get("PRIMARY_CONTACT_ID"),
                                                                    "CONTACT_NAME": employee_obj.EMPLOYEE_NAME or NULL,
                                                                    "CONTACT_TYPE": "",
                                                                    "COUNTRY": employee_obj.COUNTRY,
                                                                    "COUNTRY_RECORD_ID": employee_obj.COUNTRY_RECORD_ID,
                                                                    "DEPARTMENT": "",
                                                                    "EMAIL": employee_obj.EMAIL or " ",
                                                                    "EXTERNAL_ID": "",
                                                                    "FAX": "",
                                                                    "FUNCTION": "",
                                                                    "MOBILE": "",
                                                                    "PHONE": employees.get("PHONE"),
                                                                    "POSTAL_CODE": employees.get("POSTAL_CODE"),
                                                                    "STATE_RECORD_ID": employee_obj.STATE_RECORD_ID,
                                                                    "STATE": employee_obj.STATE,
                                                                    "STATUS": "",
                                                                    "FIRST_NAME": employees.get("FIRST_NAME"),
                                                                    "LAST_NAME": employees.get("LAST_NAME")}
                                    tableInfo = Sql.GetTable("SACONT")
                                    tablerow = contact_master_table_update
                                    tableInfo.AddRow(tablerow)
                                    Sql.Upsert(tableInfo)       
                                employee_obj = Sql.GetFirst("select * from SAEMPL(nolock) where CRM_EMPLOYEE_ID = '{crm_employee_id}'".format(crm_employee_id=employees.get("CRM_EMPLOYEE_ID")))
                                contact_master_table = Sql.GetFirst("SELECT * FROM SACONT (NOLOCK) WHERE CONTACT_ID = '{contact_id}'".format(contact_id=employees.get("PRIMARY_CONTACT_ID")))
                                if employee_obj and contact_master_table:
                                    quote_involved_party_contact_table_info = Sql.GetTable("SAQICT")
                                    contact_info_update = {
                                        "QUOTE_REV_INVOLVED_PARTY_CONTACT_ID": str(Guid.NewGuid()).upper(),
                                        "EMAIL": employee_obj.EMAIL,
                                        "QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
                                        "QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
                                        "CONTACT_ID": contact_master_table.CONTACT_ID,
                                        "CONTACT_NAME": contact_master_table.CONTACT_NAME ,
                                        "CONTACT_RECORD_ID": contact_master_table.CONTACT_RECORD_ID,
                                        "PRIMARY": employees.get("PRIMARY"),
                                        "PHONE": employee_obj.PHONE,
                                        "QTEREV_RECORD_ID": quote_revision_id,
                                        "QTEREV_ID": quote_rev_id,
                                        "COUNTRY": salesorg_country.COUNTRY,
                                        "COUNTRY_RECORD_ID": salesorg_country.COUNTRY_RECORD_ID,
                                        "STATE": employee_obj.STATE,
                                        "STATE_RECORD_ID": employee_obj.STATE_RECORD_ID if employee_obj else "",
                                        "CITY": employee_obj.CITY,
                                        "POSTAL_CODE": employee_obj.POSTAL_CODE,
                                        "PARTNERFUNCTION_RECORD_ID": partner_function_obj.PARTNERFUNCTION_RECORD_ID,
                                        "PARTNERFUNCTION_ID": partner_function_obj.PARTNERFUNCTION_ID,
                                        "PARTNERFUNCTION_DESCRIPTION": partner_function_obj.PARTNERFUNCTION_DESCRIPTION,
                                        "PARTNERTYPE_ID": partner_function_obj.PARTNERTYPE_ID,
                                        "PARTNERTYPE_DESCRIPTION": partner_function_obj.PARTNERTYPE_DESCRIPTION,
                                        "CRM_PARTNERFUNCTION": partner_function_obj.CRM_PARTNERFUNCTION,
                                    }
                                    quote_involved_party_contact_table_info.AddRow(contact_info_update)
                                    Sql.Upsert(quote_involved_party_contact_table_info)
                   
                        if contract_quote_obj and payload_json.get("TransactionType") and payload_json.get("OpportunityType"):
                            OpportunityType = {
                                "23": "PROSPECT FOR PRODUCT SALES",
                                "24": "PROSPECT FOR SERVICE",
                                "25": "PROSPECT FOR TRAINING",
                                "26": "PROSPECT FOR CONSULTING",
                                "Z27": "FPM/EXE",
                                "Z28": "TKM",
                                "Z29": "POES",
                                "Z30": "LOW",
                                "Z31": "AGS",
                            }
                            Sql.RunQuery(Contract_child)
                            if custom_fields_detail.get("OpportunityId"):
                                Opportunity_obj = "UPDATE SAOPPR SET OPPORTUNITY_TYPE = '{OpportunityType}' where OPPORTUNITY_ID = '{OpportunityId}'".format(
                                    OpportunityType=OpportunityType.get(payload_json.get("OpportunityType")),
                                    OpportunityId=custom_fields_detail.get("OpportunityId"),
                                )
                                Sql.RunQuery(Opportunity_obj)

                        if str(payload_json.get("TransactionType")) == "Z19":
                            getState = Sql.GetFirst(
                                "SELECT STATE_RECORD_ID FROM SACYST (NOLOCK) WHERE STATE = '{}' AND COUNTRY = '{}'".format(
                                    custom_fields_detail.get("PayerState"),
                                    custom_fields_detail.get("PayerCountry"),
                                )
                            )
                            quote_sending_account_details = Sql.GetTable("SAQSRA")
                            sending_account_detail_data = {
                                "ACCOUNT_ID": custom_fields_detail.get("STPAccountID"),
                                "ACCOUNT_NAME": custom_fields_detail.get("STPAccountName"),
                                "ACCOUNT_RECORD_ID": contract_quote_obj.ACCOUNT_RECORD_ID,
                                "QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
                                "QUOTE_NAME": self.quote.OpportunityName,
                                "QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
                                "RELOCATION_TYPE": "SENDING ACCOUNT",
                                "SALESORG_ID": salesorg_data.get("SALESORG_ID"),
                                "SALESORG_NAME": salesorg_data.get("SALESORG_NAME"),
                                "SALESORG_RECORD_ID": salesorg_data.get("SALESORG_RECORD_ID"),
                                "QUOTE_SENDING_RECEIVING_ACCOUNT": str(Guid.NewGuid()).upper(),
                                "ADDRESS_1": bill_to_customer.Address1,
                                "ADDRESS_2": "",
                                "CITY": bill_to_customer.City,
                                "COUNTRY": salesorg_country.COUNTRY,
                                "COUNTRY_RECORD_ID": salesorg_country_name.COUNTRY_NAME,
                                "EMAIL": bill_to_customer.Email,
                                "PHONE": bill_to_customer.BusinessPhone,
                                "POSTAL_CODE": custom_fields_detail.get("PayerPostalCode"),
                                "STATE": custom_fields_detail.get("PayerState"),
                                "STATE_RECORD_ID": getState.STATE_RECORD_ID,
                                "QTEREV_RECORD_ID": quote_revision_id,
                                "QTEREV_ID": quote_rev_id,
                            }
                            quote_sending_account_details.AddRow(sending_account_detail_data)
                            Sql.Upsert(quote_sending_account_details)
                        if contract_quote_obj:
                            quote_record_id = contract_quote_obj.MASTER_TABLE_QUOTE_RECORD_ID
                            quote_id = contract_quote_obj.QUOTE_ID

                            if fab_location_ids:
                                SAQFBL_start = time.time()
                                fab_insert = Sql.RunQuery(
                                    """
                                    INSERT
                                        SAQFBL (
                                            FABLOCATION_ID,
                                            FABLOCATION_NAME,
                                            FABLOCATION_RECORD_ID,
                                            QTEREV_RECORD_ID,
                                            QTEREV_ID,
                                            QUOTE_ID,
                                            QUOTE_RECORD_ID,
                                            COUNTRY,
                                            COUNTRY_RECORD_ID,
                                            MNT_PLANT_ID,
                                            MNT_PLANT_NAME,
                                            MNT_PLANT_RECORD_ID,
                                            SALESORG_ID,
                                            SALESORG_NAME,
                                            SALESORG_RECORD_ID,
                                            FABLOCATION_STATUS,
                                            ADDRESS_1,
                                            ADDRESS_2,
                                            CITY,
                                            STATE,
                                            STATE_RECORD_ID,
                                            QUOTE_FABLOCATION_RECORD_ID,
                                            CPQTABLEENTRYADDEDBY,
                                            CPQTABLEENTRYDATEADDED,
                                            CpqTableEntryModifiedBy,
                                            CpqTableEntryDateModified
                                        )
                                    SELECT
                                        A.*,
                                        CONVERT(VARCHAR(4000), NEWID()) as QUOTE_FABLOCATION_RECORD_ID,
                                        '{UserName}' as CPQTABLEENTRYADDEDBY,
                                        GETDATE() as CPQTABLEENTRYDATEADDED,
                                        '{UserId}' as CpqTableEntryModifiedBy,
                                        GETDATE() as CpqTableEntryDateModified
                                    FROM
                                        (
                                            SELECT
                                                DISTINCT FAB_LOCATION_ID,
                                                FAB_LOCATION_NAME,
                                                FAB_LOCATION_RECORD_ID,
                                                '{quote_revision_id}' AS QTEREV_RECORD_ID,
                                                '{quote_rev_id}' AS QTEREV_ID,
                                                {QuoteId} as QUOTE_ID,
                                                '{QuoteRecordId}' as QUOTE_RECORD_ID,
                                                COUNTRY,
                                                COUNTRY_RECORD_ID,
                                                MNT_PLANT_ID,
                                                '' as MNT_PLANT_NAME,
                                                MNT_PLANT_RECORD_ID,
                                                SALESORG_ID,
                                                SALESORG_NAME,
                                                SALESORG_RECORD_ID,
                                                STATUS,
                                                ADDRESS_1,
                                                ADDRESS_2,
                                                CITY,
                                                STATE,
                                                STATE_RECORD_ID
                                            FROM
                                                MAFBLC (NOLOCK)
                                            WHERE
                                                FAB_LOCATION_ID IN ('{FabLocationIds}')
                                        ) A
                                    """.format(
                                        UserId=User.Id,
                                        UserName=User.UserName,
                                        QuoteId=quote_id,
                                        QuoteRecordId=quote_record_id,
                                        FabLocationIds=fab_location_ids,
                                        quote_revision_id=quote_revision_id,
                                        quote_rev_id=quote_rev_id,
                                    )
                                )
                                SAQFBL_end = time.time()
                            if payload_json.get("SAQSCO"):
                                equipment_fab_data = {}
                                for service_level_temp_equipment_json_data in payload_json.get("SAQSCO"):
                                    # temptool logic starts:A055S000P01-16705
                                    if service_level_temp_equipment_json_data.get("TEMP_TOOL") == "true":
                                        if service_level_temp_equipment_json_data.get("FAB_LOCATION_ID") in equipment_fab_data:
                                            equipment_fab_data[service_level_temp_equipment_json_data.get("FAB_LOCATION_ID")].append(
                                                service_level_temp_equipment_json_data.get("EQUIPMENT_ID")
                                            )
                                        else:
                                            equipment_fab_data[service_level_temp_equipment_json_data.get("FAB_LOCATION_ID")] = [
                                                service_level_temp_equipment_json_data.get("EQUIPMENT_ID")
                                            ]
                                if equipment_fab_data:
                                    for (
                                        fab_location_id,
                                        value,
                                    ) in equipment_fab_data.items():
                                        Log.Info(
                                            """
                                            INSERT
                                                SAQFEQ (
                                                    QTEREV_RECORD_ID,
                                                    QTEREV_ID,
                                                    EQUIPMENT_DESCRIPTION,
                                                    EQUIPMENT_ID,
                                                    EQUIPMENT_RECORD_ID,
                                                    FABLOCATION_ID,
                                                    FABLOCATION_NAME,
                                                    FABLOCATION_RECORD_ID,
                                                    MNT_PLANT_ID,
                                                    MNT_PLANT_NAME,
                                                    MNT_PLANT_RECORD_ID,
                                                    PLATFORM,
                                                    QUOTE_ID,
                                                    QUOTE_NAME,
                                                    QUOTE_RECORD_ID,
                                                    SALESORG_ID,
                                                    SALESORG_NAME,
                                                    SALESORG_RECORD_ID,
                                                    SERIAL_NUMBER,
                                                    WAFER_SIZE,
                                                    TECHNOLOGY,
                                                    EQUIPMENTCATEGORY_ID,
                                                    EQUIPMENTCATEGORY_RECORD_ID,
                                                    EQUIPMENTCATEGORY_DESCRIPTION,
                                                    EQUIPMENT_STATUS,
                                                    PBG,
                                                    KPU,
                                                    WARRANTY_END_DATE,
                                                    WARRANTY_START_DATE,
                                                    CUSTOMER_TOOL_ID,
                                                    GREENBOOK,
                                                    GREENBOOK_RECORD_ID,
                                                    TEMP_TOOL,
                                                    QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
                                                    CPQTABLEENTRYADDEDBY,
                                                    CPQTABLEENTRYDATEADDED,
                                                    CpqTableEntryModifiedBy,
                                                    CpqTableEntryDateModified
                                                )
                                            SELECT
                                                A.*,
                                                CONVERT(VARCHAR(4000), NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
                                                '{UserName}' as CPQTABLEENTRYADDEDBY,
                                                GETDATE() as CPQTABLEENTRYDATEADDED,
                                                '{UserId}' as CpqTableEntryModifiedBy,
                                                GETDATE() as CpqTableEntryDateModified
                                            FROM
                                                (
                                                    SELECT
                                                        '{quote_revision_id}' AS QTEREV_RECORD_ID,
                                                        '{quote_rev_id}' AS QTEREV_ID,
                                                        EQUIPMENT_DESCRIPTION,
                                                        EQUIPMENT_ID,
                                                        EQUIPMENT_RECORD_ID,
                                                        '{FabLocationId}' as FABLOCATION_ID,
                                                        FABLOCATION_NAME,
                                                        FABLOCATION_RECORD_ID,
                                                        MNT_PLANT_ID,
                                                        '' as MNT_PLANT_NAME,
                                                        MNT_PLANT_RECORD_ID,
                                                        PLATFORM,
                                                        {QuoteId} as QUOTE_ID,
                                                        '{QuoteName}' as QUOTE_NAME,
                                                        '{QuoteRecordId}' as QUOTE_RECORD_ID,
                                                        SALESORG_ID,
                                                        SALESORG_NAME,
                                                        SALESORG_RECORD_ID,
                                                        SERIAL_NO,
                                                        SUBSTRATE_SIZE,
                                                        TECHNOLOGY,
                                                        EQUIPMENTCATEGORY_ID,
                                                        EQUIPMENTCATEGORY_RECORD_ID,
                                                        EQUIPMENTCATEGORY_DESCRIPTION,
                                                        EQUIPMENT_STATUS,
                                                        PBG,
                                                        KPU,
                                                        WARRANTY_END_DATE,
                                                        WARRANTY_START_DATE,
                                                        CUSTOMER_TOOL_ID,
                                                        GREENBOOK,
                                                        GREENBOOK_RECORD_ID,
                                                        'True' as TEMP_TOOL
                                                    FROM
                                                        MAEQUP (NOLOCK)
                                                        JOIN (
                                                            SELECT
                                                                NAME
                                                            FROM
                                                                SPLITSTRING('{EquipmentIds}')
                                                        ) B ON MAEQUP.EQUIPMENT_ID = NAME
                                                    WHERE
                                                        ISNULL(SERIAL_NO, '') <> ''
                                                ) A
                                            """.format(
                                                UserId=User.Id,
                                                UserName=User.Name,
                                                QuoteId=contract_quote_obj.QUOTE_ID,
                                                QuoteName=contract_quote_obj.QUOTE_NAME,
                                                QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
                                                FabLocationId=fab_location_id,
                                                EquipmentIds=",".join(value),
                                                quote_revision_id=Quote.GetGlobal("quote_revision_record_id"),
                                                quote_rev_id=quote_rev_id,
                                            )
                                        )
                                        equipment_temp_insert = Sql.RunQuery(
                                            """
                                            INSERT
                                                SAQFEQ (
                                                    QTEREV_RECORD_ID,
                                                    QTEREV_ID,
                                                    EQUIPMENT_DESCRIPTION,
                                                    EQUIPMENT_ID,
                                                    EQUIPMENT_RECORD_ID,
                                                    FABLOCATION_ID,
                                                    FABLOCATION_NAME,
                                                    FABLOCATION_RECORD_ID,
                                                    MNT_PLANT_ID,
                                                    MNT_PLANT_NAME,
                                                    MNT_PLANT_RECORD_ID,
                                                    PLATFORM,
                                                    QUOTE_ID,
                                                    QUOTE_NAME,
                                                    QUOTE_RECORD_ID,
                                                    SALESORG_ID,
                                                    SALESORG_NAME,
                                                    SALESORG_RECORD_ID,
                                                    SERIAL_NUMBER,
                                                    WAFER_SIZE,
                                                    TECHNOLOGY,
                                                    EQUIPMENTCATEGORY_ID,
                                                    EQUIPMENTCATEGORY_RECORD_ID,
                                                    EQUIPMENTCATEGORY_DESCRIPTION,
                                                    EQUIPMENT_STATUS,
                                                    PBG,
                                                    KPU,
                                                    WARRANTY_END_DATE,
                                                    WARRANTY_START_DATE,
                                                    CUSTOMER_TOOL_ID,
                                                    GREENBOOK,
                                                    GREENBOOK_RECORD_ID,
                                                    TEMP_TOOL,
                                                    QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
                                                    CPQTABLEENTRYADDEDBY,
                                                    CPQTABLEENTRYDATEADDED,
                                                    CpqTableEntryModifiedBy,
                                                    CpqTableEntryDateModified
                                                )
                                            SELECT
                                                A.*,
                                                CONVERT(VARCHAR(4000), NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
                                                '{UserName}' as CPQTABLEENTRYADDEDBY,
                                                GETDATE() as CPQTABLEENTRYDATEADDED,
                                                '{UserId}' as CpqTableEntryModifiedBy,
                                                GETDATE() as CpqTableEntryDateModified
                                            FROM
                                                (
                                                    SELECT
                                                        '{quote_revision_id}' AS QTEREV_RECORD_ID,
                                                        '{quote_rev_id}' AS QTEREV_ID,
                                                        EQUIPMENT_DESCRIPTION,
                                                        EQUIPMENT_ID,
                                                        EQUIPMENT_RECORD_ID,
                                                        '{FabLocationId}' as FABLOCATION_ID,
                                                        FABLOCATION_NAME,
                                                        FABLOCATION_RECORD_ID,
                                                        MNT_PLANT_ID,
                                                        '' as MNT_PLANT_NAME,
                                                        MNT_PLANT_RECORD_ID,
                                                        PLATFORM,
                                                        {QuoteId} as QUOTE_ID,
                                                        '{QuoteName}' as QUOTE_NAME,
                                                        '{QuoteRecordId}' as QUOTE_RECORD_ID,
                                                        SALESORG_ID,
                                                        SALESORG_NAME,
                                                        SALESORG_RECORD_ID,
                                                        SERIAL_NO,
                                                        SUBSTRATE_SIZE,
                                                        TECHNOLOGY,
                                                        EQUIPMENTCATEGORY_ID,
                                                        EQUIPMENTCATEGORY_RECORD_ID,
                                                        EQUIPMENTCATEGORY_DESCRIPTION,
                                                        EQUIPMENT_STATUS,
                                                        PBG,
                                                        KPU,
                                                        WARRANTY_END_DATE,
                                                        WARRANTY_START_DATE,
                                                        CUSTOMER_TOOL_ID,
                                                        GREENBOOK,
                                                        GREENBOOK_RECORD_ID,
                                                        'True' as TEMP_TOOL
                                                    FROM
                                                        MAEQUP (NOLOCK)
                                                        JOIN (
                                                            SELECT
                                                                NAME
                                                            FROM
                                                                SPLITSTRING('{EquipmentIds}')
                                                        ) B ON MAEQUP.EQUIPMENT_ID = NAME
                                                    WHERE
                                                        ISNULL(SERIAL_NO, '') <> ''
                                                ) A
                                            """.format(
                                                UserId=User.Id,
                                                UserName=User.Name,
                                                QuoteId=contract_quote_obj.QUOTE_ID,
                                                QuoteName=contract_quote_obj.QUOTE_NAME,
                                                QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
                                                FabLocationId=fab_location_id,
                                                EquipmentIds=",".join(value),
                                                quote_revision_id=Quote.GetGlobal("quote_revision_record_id"),
                                                quote_rev_id=quote_rev_id,
                                            )
                                        )
                                    ##Removed the serial number is null condition in SAQFEA table insert for HPQC 178 Defect....
                                    equipment_assembly_temp_insert = Sql.RunQuery(
                                        """
                                            INSERT
                                                SAQFEA (
                                                    QTEREV_RECORD_ID,
                                                    QTEREV_ID,
                                                    ASSEMBLY_DESCRIPTION,
                                                    ASSEMBLY_ID,
                                                    ASSEMBLY_RECORD_ID,
                                                    EQUIPMENTCATEGORY_ID,
                                                    EQUIPMENTTYPE_ID,
                                                    EQUIPMENTCATEGORY_RECORD_ID,
                                                    EQUIPMENT_DESCRIPTION,
                                                    EQUIPMENT_ID,
                                                    EQUIPMENT_RECORD_ID,
                                                    FABLOCATION_ID,
                                                    FABLOCATION_NAME,
                                                    FABLOCATION_RECORD_ID,
                                                    GOT_CODE,
                                                    MNT_PLANT_ID,
                                                    MNT_PLANT_RECORD_ID,
                                                    QUOTE_ID,
                                                    QUOTE_NAME,
                                                    QUOTE_RECORD_ID,
                                                    SALESORG_ID,
                                                    SALESORG_NAME,
                                                    SALESORG_RECORD_ID,
                                                    SERIAL_NUMBER,
                                                    WARRANTY_END_DATE,
                                                    WARRANTY_START_DATE,
                                                    SUBSTRATE_SIZE,
                                                    ASSEMBLY_STATUS,
                                                    QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,
                                                    CPQTABLEENTRYADDEDBY,
                                                    CPQTABLEENTRYDATEADDED
                                                )
                                            SELECT
                                                A.*,
                                                CONVERT(VARCHAR(4000), NEWID()) as QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,
                                                '{UserId}' as CPQTABLEENTRYADDEDBY,
                                                GETDATE() as CPQTABLEENTRYDATEADDED
                                            FROM
                                                (
                                                    SELECT
                                                        DISTINCT '{quote_revision_id}' AS QTEREV_RECORD_ID,
                                                        '{quote_rev_id}' AS QTEREV_ID,
                                                        MAEQUP.EQUIPMENT_DESCRIPTION as ASSEMBLY_DESCRIPTION,
                                                        MAEQUP.EQUIPMENT_ID as ASSEMBLY_ID,
                                                        MAEQUP.EQUIPMENT_RECORD_ID as ASSEMBLY_RECORD_ID,
                                                        MAEQUP.EQUIPMENTCATEGORY_ID,
                                                        MAEQUP.EQUIPMENTTYPE_ID,
                                                        MAEQUP.EQUIPMENTCATEGORY_RECORD_ID,
                                                        SAQFEQ.EQUIPMENT_DESCRIPTION,
                                                        SAQFEQ.EQUIPMENT_ID,
                                                        SAQFEQ.EQUIPMENT_RECORD_ID,
                                                        SAQFEQ.FABLOCATION_ID,
                                                        SAQFEQ.FABLOCATION_NAME,
                                                        SAQFEQ.FABLOCATION_RECORD_ID,
                                                        MAEQUP.GOT_CODE,
                                                        MAEQUP.MNT_PLANT_ID,
                                                        MAEQUP.MNT_PLANT_RECORD_ID,
                                                        {QuoteId} as QUOTE_ID,
                                                        '{QuoteName}' as QUOTE_NAME,
                                                        '{QuoteRecordId}' as QUOTE_RECORD_ID,
                                                        SAQFEQ.SALESORG_ID,
                                                        SAQFEQ.SALESORG_NAME,
                                                        SAQFEQ.SALESORG_RECORD_ID,
                                                        MAEQUP.SERIAL_NO as SERIAL_NUMBER,
                                                        MAEQUP.WARRANTY_END_DATE,
                                                        MAEQUP.WARRANTY_START_DATE,
                                                        MAEQUP.SUBSTRATE_SIZE,
                                                        MAEQUP.EQUIPMENT_STATUS as ASSEMBLY_STATUS
                                                    FROM
                                                        SAQFEQ (NOLOCK)
                                                        JOIN MAEQUP (NOLOCK) ON MAEQUP.PAR_EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID
                                                    WHERE
                                                        SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}'
                                                        AND SAQFEQ.QTEREV_RECORD_ID = '{quote_revision_id}'
                                                        AND SAQFEQ.TEMP_TOOL = 'True'
                                                ) A
                                        """.format(
                                            UserId=User.Id,
                                            QuoteId=quote_id,
                                            QuoteName=contract_quote_obj.QUOTE_NAME,
                                            QuoteRecordId=quote_record_id,
                                            AccountRecordId=contract_quote_obj.ACCOUNT_RECORD_ID,
                                            quote_revision_id=quote_revision_id,
                                            quote_rev_id=quote_rev_id,
                                        )
                                    )

                            if product_offering:
                                mamtrl_record_obj = Sql.GetFirst(
                                    "SELECT CLM_CONTRACT_TYPE,CLM_TEMPLATE_NAME FROM MAMTRL (NOLOCK) WHERE SAP_PART_NUMBER = '"
                                    + str(product_offering[0])
                                    + "'"
                                )
                                if mamtrl_record_obj:
                                    sow_update_query = """
                                    UPDATE
                                        SAQTRV
                                    SET
                                        CLM_CONTRACT_TYPE = '{ClmContractType}',
                                        CLM_TEMPLATE_NAME = '{ClmTemplateName}'
                                    WHERE
                                        QUOTE_RECORD_ID = '{QuoteRecordId}'
                                        AND QUOTE_REVISION_RECORD_ID = '{QuoteRevisionRecordId}'
                                    """.format(
                                        QuoteRecordId=quote_record_id,
                                        QuoteRevisionRecordId=quote_revision_id,
                                        ClmContractType=mamtrl_record_obj.CLM_CONTRACT_TYPE,
                                        ClmTemplateName=mamtrl_record_obj.CLM_TEMPLATE_NAME,
                                    )
                                    Sql.RunQuery(sow_update_query)
                            if not service_ids:
                                ScriptExecutor.ExecuteGlobal(
                                    "CQDOCUTYPE",
                                    {
                                        "QUOTE_RECORD_ID": quote_record_id,
                                        "QTEREV_RECORD_ID": quote_revision_id,
                                        "SERVICE_ID": "",
                                    },
                                )
                            if service_ids:
                                SAQTSV_start = time.time()
                                service_insert = Sql.RunQuery(
                                    """
                                    INSERT
                                        SAQTSV (
                                            OBJECT_QUANTITY,
                                            QTEREV_RECORD_ID,
                                            QTEREV_ID,
                                            QUOTE_ID,
                                            QUOTE_NAME,
                                            UOM_ID,
                                            QUOTE_RECORD_ID,
                                            SERVICE_DESCRIPTION,
                                            SERVICE_ID,
                                            SERVICE_RECORD_ID,
                                            SERVICE_TYPE,
                                            CONTRACT_VALID_FROM,
                                            CONTRACT_VALID_TO,
                                            SALESORG_ID,
                                            SALESORG_NAME,
                                            SALESORG_RECORD_ID,
                                            QUOTE_SERVICE_RECORD_ID,
                                            CPQTABLEENTRYADDEDBY,
                                            CPQTABLEENTRYDATEADDED,
                                            CpqTableEntryModifiedBy,
                                            CpqTableEntryDateModified
                                        )
                                    SELECT
                                        A.*,
                                        CONVERT(VARCHAR(4000), NEWID()) as QUOTE_SERVICE_RECORD_ID,
                                        '{UserName}' as CPQTABLEENTRYADDEDBY,
                                        GETDATE() as CPQTABLEENTRYDATEADDED,
                                        '{UserId}' as CpqTableEntryModifiedBy,
                                        GETDATE() as CpqTableEntryDateModified
                                    FROM
                                        (
                                            SELECT
                                                DISTINCT 1 AS OBJECT_QUANTITY,
                                                '{quote_revision_id}' AS QTEREV_RECORD_ID,
                                                '{quote_rev_id}' AS QTEREV_ID,
                                                {QuoteId} as QUOTE_ID,
                                                'QuoteName' as QUOTE_NAME,
                                                UNIT_OF_MEASURE,
                                                '{QuoteRecordId}' as QUOTE_RECORD_ID,
                                                SAP_DESCRIPTION as SERVICE_DESCRIPTION,
                                                SAP_PART_NUMBER as SERVICE_ID,
                                                MATERIAL_RECORD_ID as SERVICE_RECORD_ID,
                                                PRODUCT_TYPE as SERVICE_TYPE,
                                                '{ContractValidFrom}' as CONTRACT_VALID_FROM,
                                                '{ContractValidTo}' as CONTRACT_VALID_TO,
                                                '{SalesorgId}' as SALESORG_ID,
                                                '{SalesorgName}' as SALESORG_NAME,
                                                '{SalesorgRecordId}' as SALESORG_RECORD_ID
                                            FROM
                                                MAMTRL (NOLOCK)
                                            WHERE
                                                SAP_PART_NUMBER IN ('{ServiceIds}')
                                        ) A
                                    """.format(
                                        UserId=User.Id,
                                        UserName=User.UserName,
                                        QuoteId=quote_id,
                                        QuoteName=contract_quote_obj.QUOTE_NAME,
                                        QuoteRecordId=quote_record_id,
                                        SalesorgId=salesorg_data.get("SALESORG_ID"),
                                        SalesorgName=salesorg_data.get("SALESORG_NAME"),
                                        SalesorgRecordId=salesorg_data.get("SALESORG_RECORD_ID"),
                                        ServiceIds=service_ids,
                                        quote_revision_id=quote_revision_id,
                                        quote_rev_id=quote_rev_id,
                                        ContractValidFrom=contract_quote_obj.CONTRACT_VALID_FROM,
                                        ContractValidTo=contract_quote_obj.CONTRACT_VALID_TO,
                                    )
                                )

                                ServicerecordId = service_id_first
                                getRevision = Sql.GetFirst(
                                    "SELECT CpqTableEntryId FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QUOTE_REVISION_RECORD_ID = '{}' AND DOCTYP_ID IS NOT NULL AND DOCTYP_ID != '' ".format(
                                        quote_record_id, quote_revision_id
                                    )
                                )
                                getService = Sql.GetFirst(
                                    "SELECT CpqTableEntryId FROM SAQTSV WHERE  QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                                        quote_record_id, quote_revision_id
                                    )
                                )
                                if getRevision is None and getService is not None:
                                    ScriptExecutor.ExecuteGlobal(
                                        "CQDOCUTYPE",
                                        {
                                            "QUOTE_RECORD_ID": quote_record_id,
                                            "QTEREV_RECORD_ID": quote_revision_id,
                                            "SERVICE_ID": ServicerecordId,
                                        },
                                    )
                                else:
                                    ScriptExecutor.ExecuteGlobal(
                                        "CQDOCUTYPE",
                                        {
                                            "QUOTE_RECORD_ID": quote_record_id,
                                            "QTEREV_RECORD_ID": quote_revision_id,
                                            "SERVICE_ID": "",
                                        },
                                    )

                                contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                                quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
                                get_party_role = Sql.GetList(
                                    "SELECT CPQ_PARTNER_FUNCTION, PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID = '"
                                    + str(quote_record_id)
                                    + "' AND QTEREV_RECORD_ID = '"
                                    + str(quote_revision_id)
                                    + "' and CPQ_PARTNER_FUNCTION in ('SOLD TO')"
                                )
                                account_info = {}
                                for keyobj in get_party_role:
                                    account_info[keyobj.CPQ_PARTNER_FUNCTION] = keyobj.PARTY_ID

                                get_party_role = Sql.GetList(
                                    "SELECT CPQ_PARTNER_FUNCTION, PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID = '"
                                    + str(quote_record_id)
                                    + "' AND QTEREV_RECORD_ID = '"
                                    + str(quote_revision_id)
                                    + "' and CPQ_PARTNER_FUNCTION in ('SHIP TO')"
                                )
                                shipto_list = []
                                for keyobj in get_party_role:
                                    shipto_list.append("00" + str(keyobj.PARTY_ID))
                                shiptostr = str(shipto_list)
                                shiptostr = re.sub(r"'", '"', shiptostr)
                                account_info["SHIP TO"] = shiptostr
                                # get info from revision table start
                                sales_id = sales_rec = qt_rev_id = qt_id = ""
                                get_rev_sales_ifo = Sql.GetFirst(
                                    "select QUOTE_ID,SALESORG_ID,SALESORG_RECORD_ID,QTEREV_ID,CONTRACT_VALID_TO,CONTRACT_VALID_FROM from SAQTRV where QUOTE_RECORD_ID = '"
                                    + str(quote_record_id)
                                    + "' AND QUOTE_REVISION_RECORD_ID = '"
                                    + str(quote_revision_id)
                                    + "'"
                                )
                                if get_rev_sales_ifo:
                                    sales_id = get_rev_sales_ifo.SALESORG_ID
                                    sales_rec = get_rev_sales_ifo.SALESORG_RECORD_ID
                                    qt_rev_id = get_rev_sales_ifo.QTEREV_ID
                                    qt_id = get_rev_sales_ifo.QUOTE_ID
                                # get info from revision table end
                                fpm_service_ids = service_ids
                                fpm_service_ids += ","

                                fpm_service_ids_list = fpm_service_ids.split(",")
                                for val in fpm_service_ids_list:
                                    if val != "" and val in ("Z0108", "Z0110"):

                                        GetPricingProcedure = Sql.GetFirst(
                                            """
                                            SELECT
                                                DISTINCT SASAPP.PRICINGPROCEDURE_ID,
                                                SASAPP.PRICINGPROCEDURE_NAME,
                                                SASAPP.PRICINGPROCEDURE_RECORD_ID,
                                                SASAPP.DOCUMENT_PRICING_PROCEDURE,
                                                SASAPP.CUSTOMER_PRICING_PROCEDURE
                                            FROM
                                                SASAPP (NOLOCK)
                                                JOIN SASAAC (NOLOCK) ON SASAPP.SALESORG_ID = SASAAC.SALESORG_ID
                                                AND SASAPP.DIVISION_ID = SASAAC.DIVISION_ID
                                                AND SASAPP.DISTRIBUTIONCHANNEL_ID = SASAAC.DISTRIBUTIONCHANNEL_ID
                                                JOIN SAQTRV (NOLOCK) ON SAQTRV.DIVISION_ID = SASAPP.DIVISION_ID
                                                AND SAQTRV.DISTRIBUTIONCHANNEL_ID = SASAPP.DISTRIBUTIONCHANNEL_ID
                                                AND SAQTRV.SALESORG_ID = SASAPP.SALESORG_ID
                                            WHERE
                                                SASAPP.FPM = 'True'
                                                AND SAQTRV.QUOTE_RECORD_ID = '{}'
                                                AND SAQTRV.QTEREV_RECORD_ID = '{}'
                                            """.format(
                                                contract_quote_record_id,
                                                quote_revision_record_id,
                                            )
                                        )
                                        if GetPricingProcedure:
                                            UpdateSAQTRV = """
                                            UPDATE
                                                SAQTRV
                                            SET
                                                SAQTRV.PRICINGPROCEDURE_ID = '{pricingprocedure_id}',
                                                SAQTRV.PRICINGPROCEDURE_NAME = '{prcname}',
                                                SAQTRV.PRICINGPROCEDURE_RECORD_ID = '{prcrec}',
                                                SAQTRV.DOCUMENT_PRICING_PROCEDURE = '{docpricingprocedure}'
                                            WHERE
                                                SAQTRV.QUOTE_RECORD_ID = '{quote_id}'
                                                AND SAQTRV.QTEREV_RECORD_ID = '{quote_revision_id}'
                                            """.format(
                                                pricingprocedure_id=GetPricingProcedure.PRICINGPROCEDURE_ID,
                                                prcname=GetPricingProcedure.PRICINGPROCEDURE_NAME,
                                                prcrec=GetPricingProcedure.PRICINGPROCEDURE_RECORD_ID,
                                                customer_pricing_procedure=GetPricingProcedure.CUSTOMER_PRICING_PROCEDURE,
                                                docpricingprocedure=GetPricingProcedure.DOCUMENT_PRICING_PROCEDURE,
                                                quote_id=contract_quote_record_id,
                                                quote_revision_id=quote_revision_record_id,
                                            )

                                            Sql.RunQuery(UpdateSAQTRV)

                                        Service = "Z0108"
                                        entitlement_obj = Sql.GetFirst(
                                            "select ENTITLEMENT_XML from SAQTSE (nolock) where QUOTE_RECORD_ID  = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(
                                                QuoteRecordId=contract_quote_record_id,
                                                RevisionRecordId=quote_revision_record_id,
                                            )
                                        )
                                        if entitlement_obj:
                                            entitlement_xml = entitlement_obj.ENTITLEMENT_XML
                                            quote_item_tag = re.compile(r"(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)")
                                            entitlement_value_str = re.compile(
                                                r"<ENTITLEMENT_ID>AGS_" + str(Service) + "[^>]*?_TSC_SCPT</ENTITLEMENT_ID>"
                                            )
                                            value = re.compile(r"<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>")
                                            for m in re.finditer(quote_item_tag, entitlement_xml):
                                                sub_string = m.group(1)
                                                scheduled_parts = re.findall(entitlement_value_str, sub_string)
                                                scheduled_value = re.findall(value, sub_string)
                                                if scheduled_parts and scheduled_value:
                                                    break
                                        requestdata = "client_id=application&grant_type=client_credentials&username=ef66312d-bf20-416d-a902-4c646a554c10&password=Ieo.6c8hkYK9VtFe8HbgTqGev4&scope=fpmxcsafeaccess"
                                        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
                                        webclient.Headers[
                                            System.Net.HttpRequestHeader.Authorization
                                        ] = "Basic ZWY2NjMxMmQtYmYyMC00MTZkLWE5MDItNGM2NDZhNTU0YzEwOkllby42Yzhoa1lLOVZ0RmU4SGJnVHFHZXY0"
                                        response = webclient.UploadString(
                                            "https://oauth2.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com/oauth2/token",
                                            str(requestdata),
                                        )
                                        response = response.replace("null", '""')
                                        response = eval(response)
                                        auth = "Bearer" + " " + str(response["access_token"])

                                        get_party_role = Sql.GetList(
                                            "SELECT CPQ_PARTNER_FUNCTION, PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID = '"
                                            + str(contract_quote_record_id)
                                            + "' AND QTEREV_RECORD_ID = '"
                                            + str(quote_revision_record_id)
                                            + "' and CPQ_PARTNER_FUNCTION in ('SOLD TO')"
                                        )
                                        account_info = {}
                                        for keyobj in get_party_role:
                                            account_info[keyobj.CPQ_PARTNER_FUNCTION] = keyobj.PARTY_ID

                                        get_party_role = Sql.GetList(
                                            "SELECT CPQ_PARTNER_FUNCTION, PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID = '"
                                            + str(contract_quote_record_id)
                                            + "' AND QTEREV_RECORD_ID = '"
                                            + str(quote_revision_record_id)
                                            + "' and CPQ_PARTNER_FUNCTION in ('SHIP TO')"
                                        )
                                        shipto_list = []
                                        for keyobj in get_party_role:
                                            shipto_list.append("00" + str(keyobj.PARTY_ID))
                                        shiptostr = str(shipto_list)
                                        shiptostr = re.sub(r"'", '"', shiptostr)
                                        account_info["SHIP TO"] = shiptostr
                                        contract_quote_id = contract_quote_obj.QUOTE_ID
                                        get_sales_ifo = Sql.GetFirst(
                                            "select SALESORG_ID,CONTRACT_VALID_TO,CONTRACT_VALID_FROM,PRICELIST_ID,PRICEGROUP_ID from SAQTRV where QUOTE_RECORD_ID = '"
                                            + str(contract_quote_record_id)
                                            + "' AND QUOTE_REVISION_RECORD_ID = '"
                                            + str(quote_revision_record_id)
                                            + "'"
                                        )

                                        if get_sales_ifo:
                                            salesorg = get_sales_ifo.SALESORG_ID
                                            pricelist = get_sales_ifo.PRICELIST_ID
                                            pricegroup = get_sales_ifo.PRICEGROUP_ID
                                            cv = str(get_sales_ifo.CONTRACT_VALID_FROM)
                                            (cm, cd, cy) = re.sub(r"\s+([^>]*?)$", "", cv).split("/")
                                            cd = "0" + str(cd) if len(cd) == 1 else cd
                                            cm = "0" + str(cm) if len(cm) == 1 else cm
                                            validfrom = cy + cm + cd
                                            cv = str(get_sales_ifo.CONTRACT_VALID_TO)
                                            (cm, cd, cy) = re.sub(r"\s+([^>]*?)$", "", cv).split("/")
                                            cd = "0" + str(cd) if len(cd) == 1 else cd
                                            cm = "0" + str(cm) if len(cm) == 1 else cm
                                            validto = cy + cm + cd

                                        CQIFLSPARE.iflow_pullspareparts_call(
                                            str(User.UserName),
                                            str(account_info.get("SOLD TO")),
                                            str(account_info.get("SHIP TO")),
                                            salesorg,
                                            pricelist,
                                            pricegroup,
                                            "Yes",
                                            "Yes",
                                            "",
                                            validfrom,
                                            validto,
                                            contract_quote_id,
                                            quote_revision_record_id,
                                            auth,
                                        )

                                try:
                                    self.CreateEntitlements(quote_record_id)
                                except:
                                    Log.Info("CreateEntitlements Error")

                            if equipment_data:
                                get_sales_org_data = Sql.GetFirst(
                                    """
                                    Select
                                        SALESORG_ID,
                                        SALESORG_NAME,
                                        SALESORG_RECORD_ID
                                    FROM
                                        SAQTRV(NOLOCK)
                                    WHERE
                                        QUOTE_RECORD_ID = '{QuoteRecordId}'
                                        AND QTEREV_RECORD_ID = '{quote_revision_id}'
                                    """.format(
                                        QuoteRecordId=quote_record_id,
                                        quote_revision_id=quote_revision_id,
                                    )
                                )
                                for fab_location_id, value in equipment_data.items():
                                    Log.Info(
                                        """
                                        INSERT
                                        SAQFEQ (
                                            QTEREV_RECORD_ID,
                                            QTEREV_ID,
                                            EQUIPMENT_DESCRIPTION,
                                            EQUIPMENT_ID,
                                            EQUIPMENT_RECORD_ID,
                                            FABLOCATION_ID,
                                            FABLOCATION_NAME,
                                            FABLOCATION_RECORD_ID,
                                            MNT_PLANT_ID,
                                            MNT_PLANT_NAME,
                                            MNT_PLANT_RECORD_ID,
                                            PLATFORM,
                                            QUOTE_ID,
                                            QUOTE_NAME,
                                            QUOTE_RECORD_ID,
                                            SALESORG_ID,
                                            SALESORG_NAME,
                                            SALESORG_RECORD_ID,
                                            SERIAL_NUMBER,
                                            WAFER_SIZE,
                                            TECHNOLOGY,
                                            EQUIPMENTCATEGORY_ID,
                                            EQUIPMENTCATEGORY_RECORD_ID,
                                            EQUIPMENTCATEGORY_DESCRIPTION,
                                            EQUIPMENT_STATUS,
                                            PBG,
                                            KPU,
                                            WARRANTY_END_DATE,
                                            WARRANTY_START_DATE,
                                            CUSTOMER_TOOL_ID,
                                            GREENBOOK,
                                            GREENBOOK_RECORD_ID,
                                            TEMP_TOOL,
                                            QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
                                            CPQTABLEENTRYADDEDBY,
                                            CPQTABLEENTRYDATEADDED,
                                            CpqTableEntryModifiedBy,
                                            CpqTableEntryDateModified
                                        )
                                    SELECT
                                        A.*,
                                        CONVERT(VARCHAR(4000), NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
                                        '{UserName}' as CPQTABLEENTRYADDEDBY,
                                        GETDATE() as CPQTABLEENTRYDATEADDED,
                                        '{UserId}' as CpqTableEntryModifiedBy,
                                        GETDATE() as CpqTableEntryDateModified
                                    FROM
                                        (
                                            SELECT
                                                DISTINCT '{quote_revision_id}' AS QTEREV_RECORD_ID,
                                                '{quote_rev_id}' AS QTEREV_ID,
                                                EQUIPMENT_DESCRIPTION,
                                                EQUIPMENT_ID,
                                                EQUIPMENT_RECORD_ID,
                                                FABLOCATION_ID,
                                                FABLOCATION_NAME,
                                                FABLOCATION_RECORD_ID,
                                                MNT_PLANT_ID,
                                                '' as MNT_PLANT_NAME,
                                                MNT_PLANT_RECORD_ID,
                                                PLATFORM,
                                                {QuoteId} as QUOTE_ID,
                                                '{QuoteName}' as QUOTE_NAME,
                                                '{QuoteRecordId}' as QUOTE_RECORD_ID,
                                                '{salesId}' as SALESORG_ID,
                                                '{salesname}' as SALESORG_NAME,
                                                '{salesrecordid}' as SALESORG_RECORD_ID,
                                                SERIAL_NO,
                                                SUBSTRATE_SIZE,
                                                TECHNOLOGY,
                                                EQUIPMENTCATEGORY_ID,
                                                EQUIPMENTCATEGORY_RECORD_ID,
                                                EQUIPMENTCATEGORY_DESCRIPTION,
                                                EQUIPMENT_STATUS,
                                                PBG,
                                                KPU,
                                                WARRANTY_END_DATE,
                                                WARRANTY_START_DATE,
                                                CUSTOMER_TOOL_ID,
                                                GREENBOOK,
                                                GREENBOOK_RECORD_ID,
                                                'False' as TEMP_TOOL
                                            FROM
                                                MAEQUP (NOLOCK)
                                                JOIN (
                                                    SELECT
                                                        NAME
                                                    FROM
                                                        SPLITSTRING('{EquipmentIds}')
                                                ) B ON MAEQUP.EQUIPMENT_ID = NAME
                                            WHERE
                                                ISNULL(SERIAL_NO, '') <> ''
                                                AND FABLOCATION_ID = '{FabLocationId}'
                                        ) A""".format(
                                            UserId=User.Id,
                                            UserName=User.Name,
                                            QuoteId=quote_id,
                                            QuoteName=contract_quote_obj.QUOTE_NAME,
                                            QuoteRecordId=quote_record_id,
                                            FabLocationId=fab_location_id,
                                            EquipmentIds=",".join(value),
                                            quote_revision_id=quote_revision_id,
                                            quote_rev_id=quote_rev_id,
                                            salesId=get_sales_org_data.SALESORG_ID,
                                            salesname=get_sales_org_data.SALESORG_NAME,
                                            salesrecordid=get_sales_org_data.SALESORG_RECORD_ID,
                                        )
                                    )
                                    equipment_insert = Sql.RunQuery(
                                        """
                                        INSERT
                                        SAQFEQ (
                                            QTEREV_RECORD_ID,
                                            QTEREV_ID,
                                            EQUIPMENT_DESCRIPTION,
                                            EQUIPMENT_ID,
                                            EQUIPMENT_RECORD_ID,
                                            FABLOCATION_ID,
                                            FABLOCATION_NAME,
                                            FABLOCATION_RECORD_ID,
                                            MNT_PLANT_ID,
                                            MNT_PLANT_NAME,
                                            MNT_PLANT_RECORD_ID,
                                            PLATFORM,
                                            QUOTE_ID,
                                            QUOTE_NAME,
                                            QUOTE_RECORD_ID,
                                            SALESORG_ID,
                                            SALESORG_NAME,
                                            SALESORG_RECORD_ID,
                                            SERIAL_NUMBER,
                                            WAFER_SIZE,
                                            TECHNOLOGY,
                                            EQUIPMENTCATEGORY_ID,
                                            EQUIPMENTCATEGORY_RECORD_ID,
                                            EQUIPMENTCATEGORY_DESCRIPTION,
                                            EQUIPMENT_STATUS,
                                            PBG,
                                            KPU,
                                            WARRANTY_END_DATE,
                                            WARRANTY_START_DATE,
                                            CUSTOMER_TOOL_ID,
                                            GREENBOOK,
                                            GREENBOOK_RECORD_ID,
                                            TEMP_TOOL,
                                            QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
                                            CPQTABLEENTRYADDEDBY,
                                            CPQTABLEENTRYDATEADDED,
                                            CpqTableEntryModifiedBy,
                                            CpqTableEntryDateModified
                                        )
                                    SELECT
                                        A.*,
                                        CONVERT(VARCHAR(4000), NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
                                        '{UserName}' as CPQTABLEENTRYADDEDBY,
                                        GETDATE() as CPQTABLEENTRYDATEADDED,
                                        '{UserId}' as CpqTableEntryModifiedBy,
                                        GETDATE() as CpqTableEntryDateModified
                                    FROM
                                        (
                                            SELECT
                                                DISTINCT '{quote_revision_id}' AS QTEREV_RECORD_ID,
                                                '{quote_rev_id}' AS QTEREV_ID,
                                                EQUIPMENT_DESCRIPTION,
                                                EQUIPMENT_ID,
                                                EQUIPMENT_RECORD_ID,
                                                FABLOCATION_ID,
                                                FABLOCATION_NAME,
                                                FABLOCATION_RECORD_ID,
                                                MNT_PLANT_ID,
                                                '' as MNT_PLANT_NAME,
                                                MNT_PLANT_RECORD_ID,
                                                PLATFORM,
                                                {QuoteId} as QUOTE_ID,
                                                '{QuoteName}' as QUOTE_NAME,
                                                '{QuoteRecordId}' as QUOTE_RECORD_ID,
                                                '{salesId}' as SALESORG_ID,
                                                '{salesname}' as SALESORG_NAME,
                                                '{salesrecordid}' as SALESORG_RECORD_ID,
                                                SERIAL_NO,
                                                SUBSTRATE_SIZE,
                                                TECHNOLOGY,
                                                EQUIPMENTCATEGORY_ID,
                                                EQUIPMENTCATEGORY_RECORD_ID,
                                                EQUIPMENTCATEGORY_DESCRIPTION,
                                                EQUIPMENT_STATUS,
                                                PBG,
                                                KPU,
                                                WARRANTY_END_DATE,
                                                WARRANTY_START_DATE,
                                                CUSTOMER_TOOL_ID,
                                                GREENBOOK,
                                                GREENBOOK_RECORD_ID,
                                                'False' as TEMP_TOOL
                                            FROM
                                                MAEQUP (NOLOCK)
                                                JOIN (
                                                    SELECT
                                                        NAME
                                                    FROM
                                                        SPLITSTRING('{EquipmentIds}')
                                                ) B ON MAEQUP.EQUIPMENT_ID = NAME
                                            WHERE
                                                ISNULL(SERIAL_NO, '') <> ''
                                                AND FABLOCATION_ID = '{FabLocationId}'
                                        ) A""".format(
                                            UserId=User.Id,
                                            UserName=User.Name,
                                            QuoteId=quote_id,
                                            QuoteName=contract_quote_obj.QUOTE_NAME,
                                            QuoteRecordId=quote_record_id,
                                            FabLocationId=fab_location_id,
                                            EquipmentIds=",".join(value),
                                            quote_revision_id=quote_revision_id,
                                            quote_rev_id=quote_rev_id,
                                            salesId=get_sales_org_data.SALESORG_ID,
                                            salesname=get_sales_org_data.SALESORG_NAME,
                                            salesrecordid=get_sales_org_data.SALESORG_RECORD_ID,
                                        )
                                    )

                                greenbook_detail_insert = Sql.RunQuery(
                                    """ INSERT
                                        SAQFGB (
                                            QTEREV_RECORD_ID,
                                            QTEREV_ID,
                                            FABLOCATION_ID,
                                            FABLOCATION_NAME,
                                            FABLOCATION_RECORD_ID,
                                            GREENBOOK,
                                            GREENBOOK_RECORD_ID,
                                            QTEFBL_RECORD_ID,
                                            QUOTE_ID,
                                            QUOTE_NAME,
                                            QUOTE_RECORD_ID,
                                            SALESORG_ID,
                                            SALESORG_NAME,
                                            SALESORG_RECORD_ID,
                                            QUOTE_FAB_LOC_GB_RECORD_ID,
                                            CPQTABLEENTRYADDEDBY,
                                            CPQTABLEENTRYDATEADDED,
                                            CpqTableEntryModifiedBy,
                                            CpqTableEntryDateModified
                                        )
                                    SELECT
                                        A.*,
                                        CONVERT(VARCHAR(4000), NEWID()) as QUOTE_FAB_LOC_GB_RECORD_ID,
                                        '{UserName}' as CPQTABLEENTRYADDEDBY,
                                        GETDATE() as CPQTABLEENTRYDATEADDED,
                                        '{UserId}' as CpqTableEntryModifiedBy,
                                        GETDATE() as CpqTableEntryDateModified
                                    FROM
                                        (
                                            select
                                                '{quote_revision_id}' AS QTEREV_RECORD_ID,
                                                '{quote_rev_id}' AS QTEREV_ID,
                                                FABLOCATION_ID,
                                                FABLOCATION_NAME,
                                                FABLOCATION_RECORD_ID,
                                                GREENBOOK,
                                                GREENBOOK_RECORD_ID,
                                                QTEFBL_RECORD_ID,
                                                QUOTE_ID,
                                                QUOTE_NAME,
                                                QUOTE_RECORD_ID,
                                                SALESORG_ID,
                                                SALESORG_NAME,
                                                SALESORG_RECORD_ID
                                            from
                                                SAQFEQ
                                            where
                                                QUOTE_RECORD_ID = '{QuoteRecordId}'
                                            group by
                                                FABLOCATION_ID,
                                                FABLOCATION_NAME,
                                                FABLOCATION_RECORD_ID,
                                                GREENBOOK,
                                                GREENBOOK_RECORD_ID,
                                                QTEFBL_RECORD_ID,
                                                QUOTE_ID,
                                                QUOTE_NAME,
                                                QUOTE_RECORD_ID,
                                                SALESORG_ID,
                                                SALESORG_NAME,
                                                SALESORG_RECORD_ID
                                        ) A""".format(
                                        UserId=User.Id,
                                        UserName=User.UserName,
                                        QuoteId=quote_id,
                                        QuoteName=contract_quote_obj.QUOTE_NAME,
                                        QuoteRecordId=quote_record_id,
                                        quote_revision_id=quote_revision_id,
                                        quote_rev_id=quote_rev_id,
                                    )
                                )
                                ##Removed the serial number is null condition in SAQFEA table insert for HPQC 178 Defect....
                                query = """
                                    INSERT
                                    SAQFEA (
                                        QTEREV_RECORD_ID,
                                        QTEREV_ID,
                                        ASSEMBLY_DESCRIPTION,
                                        ASSEMBLY_ID,
                                        ASSEMBLY_RECORD_ID,
                                        EQUIPMENTCATEGORY_ID,
                                        EQUIPMENTTYPE_ID,
                                        EQUIPMENTCATEGORY_RECORD_ID,
                                        EQUIPMENT_DESCRIPTION,
                                        EQUIPMENT_ID,
                                        EQUIPMENT_RECORD_ID,
                                        FABLOCATION_ID,
                                        FABLOCATION_NAME,
                                        FABLOCATION_RECORD_ID,
                                        GOT_CODE,
                                        MNT_PLANT_ID,
                                        MNT_PLANT_RECORD_ID,
                                        QUOTE_ID,
                                        QUOTE_NAME,
                                        QUOTE_RECORD_ID,
                                        SALESORG_ID,
                                        SALESORG_NAME,
                                        SALESORG_RECORD_ID,
                                        SERIAL_NUMBER,
                                        WARRANTY_END_DATE,
                                        WARRANTY_START_DATE,
                                        SUBSTRATE_SIZE,
                                        ASSEMBLY_STATUS,
                                        QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,
                                        CPQTABLEENTRYADDEDBY,
                                        CPQTABLEENTRYDATEADDED
                                    )
                                SELECT 
                                    A.*,
                                    CONVERT(VARCHAR(4000), NEWID()) as QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID, 
                                    '{UserId}' as CPQTABLEENTRYADDEDBY,
                                    GETDATE() as CPQTABLEENTRYDATEADDED
                                FROM
                                    (
                                        SELECT
                                            DISTINCT '{quote_revision_id}' AS QTEREV_RECORD_ID,
                                            '{quote_rev_id}' AS QTEREV_ID,
                                            MAEQUP.EQUIPMENT_DESCRIPTION as ASSEMBLY_DESCRIPTION,
                                            MAEQUP.EQUIPMENT_ID as ASSEMBLY_ID,
                                            MAEQUP.EQUIPMENT_RECORD_ID as ASSEMBLY_RECORD_ID,
                                            MAEQUP.EQUIPMENTCATEGORY_ID,
                                            MAEQUP.EQUIPMENTTYPE_ID,
                                            MAEQUP.EQUIPMENTCATEGORY_RECORD_ID,
                                            SAQFEQ.EQUIPMENT_DESCRIPTION,
                                            SAQFEQ.EQUIPMENT_ID,
                                            SAQFEQ.EQUIPMENT_RECORD_ID,
                                            SAQFEQ.FABLOCATION_ID,
                                            SAQFEQ.FABLOCATION_NAME,
                                            SAQFEQ.FABLOCATION_RECORD_ID,
                                            MAEQUP.GOT_CODE,
                                            MAEQUP.MNT_PLANT_ID,
                                            MAEQUP.MNT_PLANT_RECORD_ID,
                                            {QuoteId} as QUOTE_ID,
                                            '{QuoteName}' as QUOTE_NAME,
                                            '{QuoteRecordId}' as QUOTE_RECORD_ID,
                                            SAQFEQ.SALESORG_ID,
                                            SAQFEQ.SALESORG_NAME,
                                            SAQFEQ.SALESORG_RECORD_ID,
                                            MAEQUP.SERIAL_NO as SERIAL_NUMBER,
                                            MAEQUP.WARRANTY_END_DATE,
                                            MAEQUP.WARRANTY_START_DATE,
                                            MAEQUP.SUBSTRATE_SIZE,
                                            MAEQUP.EQUIPMENT_STATUS as ASSEMBLY_STATUS
                                        FROM
                                            SAQFEQ (NOLOCK)
                                            JOIN MAEQUP (NOLOCK) ON MAEQUP.PAR_EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID
                                            AND MAEQUP.FABLOCATION_ID = SAQFEQ.FABLOCATION_ID
                                        WHERE
                                            SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}'
                                            AND SAQFEQ.QTEREV_RECORD_ID = '{quote_revision_id}'
                                            AND ISNULL(SAQFEQ.TEMP_TOOL, '') = ''
                                    ) A
                                    """.format(
                                        UserId=User.Id,
                                        QuoteId=quote_id,
                                        QuoteName=contract_quote_obj.QUOTE_NAME,
                                        QuoteRecordId=quote_record_id,
                                        AccountRecordId=contract_quote_obj.ACCOUNT_RECORD_ID,
                                        quote_revision_id=quote_revision_id,
                                        quote_rev_id=quote_rev_id,
                                    )

                                equipment_assembly_insert = Sql.RunQuery(query)
                                Log.Info(query)

                            # A055S000P01-10174 code starts...modified for A055S000P01-16530
                            try:
                                coverd_object_tool_dates = []
                                for service_level_equipment_json_data in payload_json.get("SAQSCO"):
                                    if service_level_equipment_json_data.get("SERVICE_OFFERING_ID") in covered_object_data:
                                        covered_object_data[service_level_equipment_json_data.get("SERVICE_OFFERING_ID")].append(
                                            service_level_equipment_json_data.get("EQUIPMENT_ID")
                                        )
                                    else:
                                        covered_object_data[service_level_equipment_json_data.get("SERVICE_OFFERING_ID")] = [
                                            service_level_equipment_json_data.get("EQUIPMENT_ID")
                                        ]
                                    # getting Contract dates and temp tools
                                    equipment_id = service_level_equipment_json_data.get("EQUIPMENT_ID")
                                    start_date = service_level_equipment_json_data.get("CONTRACT_START_DATE").replace("T00:00:00.000", "")
                                    end_date = service_level_equipment_json_data.get("CONTRACT_END_DATE").replace("T00:00:00.000", "")
                                    service_id = service_level_equipment_json_data.get("SERVICE_OFFERING_ID")
                                    coverd_object_tool_dates.append(
                                        [
                                            equipment_id,
                                            start_date,
                                            end_date,
                                            service_id,
                                            Quote.GetGlobal("contract_quote_record_id"),
                                            Quote.GetGlobal("quote_revision_record_id"),
                                        ]
                                    )
                                records = (
                                    ", ".join(
                                        map(
                                            str,
                                            [str(tuple(equipment_record)) for equipment_record in coverd_object_tool_dates],
                                        )
                                    )
                                    .replace("None", "null")
                                    .replace("'", "''")
                                )
                                # covered object insert
                                if covered_object_data:
                                    for (
                                        service_id,
                                        value,
                                    ) in covered_object_data.items():
                                        if len(value) >= 1000:
                                            previous_index = 0
                                            count = 0
                                            while count <= len(value):
                                                equipment_records = value[previous_index : count + 1000]
                                                previous_index = count + 1000
                                                equipment_records = ",".join(equipment_records)
                                                count = count + 1000
                                                quote_fab_equipments_obj = Sql.GetList(
                                                    """
                                                    Select
                                                        QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID
                                                    FROM
                                                        SAQFEQ(NOLOCK)
                                                    WHERE
                                                        EQUIPMENT_ID IN ({equipment_ids})
                                                        AND QUOTE_RECORD_ID = '{quote_record_id}'
                                                        AND QTEREV_RECORD_ID = '{quote_revision_record_id}'
                                                    """.format(
                                                        equipment_ids=equipment_records,
                                                        quote_record_id=Quote.GetGlobal("contract_quote_record_id"),
                                                        quote_revision_record_id=Quote.GetGlobal("quote_revision_record_id"),
                                                    )
                                                )
                                                quote_service_obj = Sql.GetFirst(
                                                    """
                                                    select
                                                        SERVICE_TYPE
                                                    from
                                                        SAQTSV
                                                    where
                                                        SERVICE_ID = '{Service_Id}'
                                                        AND QUOTE_RECORD_ID = '{quote_record_id}'
                                                        AND QTEREV_RECORD_ID = '{quote_revision_record_id}'
                                                    """.format(
                                                        Service_Id=service_id,
                                                        quote_record_id=Quote.GetGlobal("contract_quote_record_id"),
                                                        quote_revision_record_id=Quote.GetGlobal("quote_revision_record_id"),
                                                    )
                                                )
                                                quote_fab_equipments_record_id = [
                                                    quote_fab_equipment_obj.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID
                                                    for quote_fab_equipment_obj in quote_fab_equipments_obj
                                                ]
                                                service_id = service_id
                                                service_type = quote_service_obj.SERVICE_TYPE
                                                quote_record_id = contract_quote_obj.MASTER_TABLE_QUOTE_RECORD_ID
                                                Product.SetGlobal(
                                                    "contract_quote_record_id",
                                                    str(quote_record_id),
                                                )
                                                ScriptExecutor.ExecuteGlobal(
                                                    "CQCRUDOPTN",
                                                    {
                                                        "NodeType": "COVERED OBJ MODEL",
                                                        "ActionType": "ADD_COVERED_OBJ",
                                                        "Opertion": "ADD",
                                                        "AllValues": False,
                                                        "TriggerFrom": "python_script",
                                                        "Values": quote_fab_equipments_record_id,
                                                        "ServiceId": service_id,
                                                        "ServiceType": service_type,
                                                    },
                                                )
                                        else:
                                            elements = ",".join(value)
                                            quote_fab_equipments_obj = Sql.GetList(
                                                """
                                                Select
                                                    QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID
                                                FROM
                                                    SAQFEQ(NOLOCK)
                                                WHERE
                                                    EQUIPMENT_ID IN ({equipment_ids})
                                                    AND QUOTE_RECORD_ID = '{quote_record_id}'
                                                    AND QTEREV_RECORD_ID = '{quote_revision_record_id}'
                                                """.format(
                                                    equipment_ids=elements,
                                                    quote_record_id=Quote.GetGlobal("contract_quote_record_id"),
                                                    quote_revision_record_id=Quote.GetGlobal("quote_revision_record_id"),
                                                )
                                            )
                                            quote_service_obj = Sql.GetFirst(
                                                """
                                                select
                                                    SERVICE_TYPE
                                                from
                                                    SAQTSV
                                                where
                                                    SERVICE_ID = '{Service_Id}'
                                                    AND QUOTE_RECORD_ID = '{quote_record_id}'
                                                    AND QTEREV_RECORD_ID = '{quote_revision_record_id}'
                                                """.format(
                                                    Service_Id=service_id,
                                                    quote_record_id=Quote.GetGlobal("contract_quote_record_id"),
                                                    quote_revision_record_id=Quote.GetGlobal("quote_revision_record_id"),
                                                )
                                            )
                                            quote_fab_equipments_record_id = [
                                                quote_fab_equipment_obj.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID
                                                for quote_fab_equipment_obj in quote_fab_equipments_obj
                                            ]
                                            service_id = service_id
                                            service_type = quote_service_obj.SERVICE_TYPE
                                            quote_record_id = contract_quote_obj.MASTER_TABLE_QUOTE_RECORD_ID
                                            Product.SetGlobal(
                                                "contract_quote_record_id",
                                                str(quote_record_id),
                                            )
                                            ScriptExecutor.ExecuteGlobal(
                                                "CQCRUDOPTN",
                                                {
                                                    "NodeType": "COVERED OBJ MODEL",
                                                    "ActionType": "ADD_COVERED_OBJ",
                                                    "Opertion": "ADD",
                                                    "AllValues": False,
                                                    "TriggerFrom": "python_script",
                                                    "Values": quote_fab_equipments_record_id,
                                                    "ServiceId": service_id,
                                                    "ServiceType": service_type,
                                                },
                                            )
                                    # update for temp tool and dates
                                    QuoteId = quote_id
                                    datetime_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
                                    columns = (
                                        "EQUIPMENT_ID,CONTRACT_START_DATE,CONTRACT_END_DATE,SERVICE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID"
                                    )
                                    coverd_object_temp_table_name = "SAQSCO_BKP_{}_{}".format(QuoteId, datetime_string)
                                    coverd_object_temp_table_drop = SqlHelper.GetFirst(
                                        "sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"
                                        + str(coverd_object_temp_table_name)
                                        + "'' ) BEGIN DROP TABLE "
                                        + str(coverd_object_temp_table_name)
                                        + " END  ' "
                                    )
                                    coverd_object_temp_table_bkp = SqlHelper.GetFirst(
                                        "sp_executesql @T=N'SELECT "
                                        + str(columns)
                                        + " INTO "
                                        + str(coverd_object_temp_table_name)
                                        + " FROM (SELECT DISTINCT "
                                        + str(columns)
                                        + " FROM (VALUES "
                                        + str(records)
                                        + ") AS TEMP("
                                        + str(columns)
                                        + ")) OQ ' "
                                    )
                                    saqsco_update = """
                                    UPDATE
                                        A
                                    SET
                                        A.CONTRACT_VALID_FROM = B.CONTRACT_START_DATE,
                                        A.CONTRACT_VALID_TO = B.CONTRACT_END_DATE
                                    FROM
                                        SAQSCO A
                                        INNER JOIN {} B on A.EQUIPMENT_ID = B.EQUIPMENT_ID
                                        and A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID
                                        and A.SERVICE_ID = B.SERVICE_ID
                                    where
                                        A.QUOTE_RECORD_ID = '{Quote_id}'
                                        AND A.QTEREV_RECORD_ID = '{qtrv_id}'
                                        """.format(
                                        coverd_object_temp_table_name,
                                        Quote_id=Quote.GetGlobal("contract_quote_record_id"),
                                        qtrv_id=Quote.GetGlobal("quote_revision_record_id"),
                                    )
                                    #Sql.RunQuery(saqsco_update)
                                    coverd_object_temp_table_drop = SqlHelper.GetFirst(
                                        "sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"
                                        + str(coverd_object_temp_table_name)
                                        + "'' ) BEGIN DROP TABLE "
                                        + str(coverd_object_temp_table_name)
                                        + " END  ' "
                                    )
                            except Exception as e:
                                Log.Info("EXCEPTION: Iteration Over non sequence for none type" + str(e))
                            # A055S000P01-10174 code ends...A055S000P01-16530

                        payload_table_info = Sql.GetTable("SYINPL")
                        payload_table_data = {
                            "CpqTableEntryId": payload_json_obj.CpqTableEntryId,
                            "STATUS": "COMPLETED",
                        }
                        payload_table_info.AddRow(payload_table_data)
                        Sql.Upsert(payload_table_info)

                    # Calling the iflow for quote header writeback to cpq to c4c code starts..
                    CQCPQC4CWB.writeback_to_c4c(
                        "quote_header",
                        Quote.GetGlobal("contract_quote_record_id"),
                        Quote.GetGlobal("quote_revision_record_id"),
                    )
                    time.sleep(3)  # A055S000P01-16535
                    CQCPQC4CWB.writeback_to_c4c(
                        "opportunity_header",
                        Quote.GetGlobal("contract_quote_record_id"),
                        Quote.GetGlobal("quote_revision_record_id"),
                    )

        except Exception:
            Log.Info("SYPOSTINSG ERROR---->:" + str(sys.exc_info()[1]))
            Log.Info("SYPOSTINSG ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))

        sync_end_time = time.time()
        quote_end_time = time.time()

        Log.Info("Sync end==> " + str(sync_end_time - sync_start_time))
        Log.Info("Quote CreationTime==> " + str(quote_end_time - self.quote_start_time))

    # A055S000P01-8690 starts..
    def salesteam_insert(
        self,
        employee,
        contract_quote_data,
        quote_rev_id,
        quote_revision_id,
        custom_fields_detail,
    ):
        query = """
        INSERT
            SAQDLT (
                C4C_PARTNERFUNCTION_ID,
                CRM_PARTNERFUNCTION_ID,
                PARTNERFUNCTION_DESC,
                PARTNERFUNCTION_ID,
                PARTNERFUNCTION_RECORD_ID,
                EMAIL,
                MEMBER_ID,
                MEMBER_NAME,
                MEMBER_RECORD_ID,
                [PRIMARY],
                QUOTE_ID,
                QUOTE_RECORD_ID,
                QTEREV_ID,
                QTEREV_RECORD_ID,
                QUOTE_REV_DEAL_TEAM_MEMBER_ID,
                CPQTABLEENTRYADDEDBY,
                CPQTABLEENTRYDATEADDED,
                CpqTableEntryModifiedBy,
                CpqTableEntryDateModified
            )
        SELECT
            emp.*,
            CONVERT(VARCHAR(4000), NEWID()) as QUOTE_REV_DEAL_TEAM_MEMBER_ID,
            '{UserName}' as CPQTABLEENTRYADDEDBY,
            GETDATE() as CPQTABLEENTRYDATEADDED,
            '{UserId}' as CpqTableEntryModifiedBy,
            GETDATE() as CpqTableEntryDateModified
        FROM
            (
                SELECT
                    DISTINCT (
                        SELECT
                            TOP 1 C4C_PARTNER_FUNCTION
                        FROM
                            SYPFTY
                        WHERE
                            C4C_PARTNER_FUNCTION = CASE
                                '{C4c_partner_function}'
                                WHEN '39' THEN 'EMPLOYEE RESPONSIBLE'
                                WHEN '46' THEN 'SALES EMPLOYEE'
                                WHEN '213' THEN 'PARTNER CONTACT'
                                WHEN 'Z1' THEN 'BD'
                                WHEN 'Z2' THEN 'BD MANAGER'
                                WHEN 'Z3' THEN 'SALES CONTRACT SUPPORT'
                                WHEN 'Z4' THEN 'SALES MANAGER'
                                WHEN 'Z5' THEN 'SALES REP'
                                WHEN 'ZCM' THEN 'CONTRACT MANAGER'
                                WHEN 'ZFM' THEN 'FINANCE MANAGER'
                                WHEN 'Z10' THEN 'LEGAL PERSON'
                                WHEN 'Z11' THEN 'PRICING PERSON'
                                WHEN 'Z12' THEN 'MARKETING AND BD HEAD'
                                WHEN 'Z13' THEN 'SSC HEAD'
                                WHEN 'Z14' THEN 'AGS HEAD'
                                WHEN 'Z15' THEN 'CM MANAGER'
                                WHEN 'Z16' THEN 'AGS REV REC FINANCE MANAGER'
                                WHEN 'Z6' THEN 'BD HEAD'
                                WHEN 'Z7' THEN 'MARKETING HEAD'
                                WHEN 'Z8' THEN 'REGIONAL FINANCE CONTROLLER'
                                WHEN 'Z9' THEN 'AGS FINANCE CONTROLLER'
                                WHEN 'ZF' THEN 'FAB'
                                ELSE 'FOB'
                            END
                    ) AS C4C_PARTNERFUNCTION_ID,
                    (
                        SELECT
                            TOP 1 CRM_PARTNERFUNCTION
                        FROM
                            SYPFTY
                        WHERE
                            C4C_PARTNER_FUNCTION = CASE
                                '{C4c_partner_function}'
                                WHEN '39' THEN 'EMPLOYEE RESPONSIBLE'
                                WHEN '46' THEN 'SALES EMPLOYEE'
                                WHEN '213' THEN 'PARTNER CONTACT'
                                WHEN 'Z1' THEN 'BD'
                                WHEN 'Z2' THEN 'BD MANAGER'
                                WHEN 'Z3' THEN 'SALES CONTRACT SUPPORT'
                                WHEN 'Z4' THEN 'SALES MANAGER'
                                WHEN 'Z5' THEN 'SALES REP'
                                WHEN 'ZCM' THEN 'CONTRACT MANAGER'
                                WHEN 'ZFM' THEN 'FINANCE MANAGER'
                                WHEN 'Z10' THEN 'LEGAL PERSON'
                                WHEN 'Z11' THEN 'PRICING PERSON'
                                WHEN 'Z12' THEN 'MARKETING AND BD HEAD'
                                WHEN 'Z13' THEN 'SSC HEAD'
                                WHEN 'Z14' THEN 'AGS HEAD'
                                WHEN 'Z15' THEN 'CM MANAGER'
                                WHEN 'Z16' THEN 'AGS REV REC FINANCE MANAGER'
                                WHEN 'Z6' THEN 'BD HEAD'
                                WHEN 'Z7' THEN 'MARKETING HEAD'
                                WHEN 'Z8' THEN 'REGIONAL FINANCE CONTROLLER'
                                WHEN 'Z9' THEN 'AGS FINANCE CONTROLLER'
                                WHEN 'ZF' THEN 'FAB'
                                ELSE 'FOB'
                            END
                    ) AS CRM_PARTNERFUNCTION_ID,
                    (
                        SELECT
                            TOP 1 PARTNERFUNCTION_DESCRIPTION
                        FROM
                            SYPFTY
                        WHERE
                            C4C_PARTNER_FUNCTION = CASE
                                '{C4c_partner_function}'
                                WHEN '39' THEN 'EMPLOYEE RESPONSIBLE'
                                WHEN '46' THEN 'SALES EMPLOYEE'
                                WHEN '213' THEN 'PARTNER CONTACT'
                                WHEN 'Z1' THEN 'BD'
                                WHEN 'Z2' THEN 'BD MANAGER'
                                WHEN 'Z3' THEN 'SALES CONTRACT SUPPORT'
                                WHEN 'Z4' THEN 'SALES MANAGER'
                                WHEN 'Z5' THEN 'SALES REP'
                                WHEN 'ZCM' THEN 'CONTRACT MANAGER'
                                WHEN 'ZFM' THEN 'FINANCE MANAGER'
                                WHEN 'Z10' THEN 'LEGAL PERSON'
                                WHEN 'Z11' THEN 'PRICING PERSON'
                                WHEN 'Z12' THEN 'MARKETING AND BD HEAD'
                                WHEN 'Z13' THEN 'SSC HEAD'
                                WHEN 'Z14' THEN 'AGS HEAD'
                                WHEN 'Z15' THEN 'CM MANAGER'
                                WHEN 'Z16' THEN 'AGS REV REC FINANCE MANAGER'
                                WHEN 'Z6' THEN 'BD HEAD'
                                WHEN 'Z7' THEN 'MARKETING HEAD'
                                WHEN 'Z8' THEN 'REGIONAL FINANCE CONTROLLER'
                                WHEN 'Z9' THEN 'AGS FINANCE CONTROLLER'
                                WHEN 'ZF' THEN 'FAB'
                                ELSE 'FOB'
                            END
                    ) AS PARTNERFUNCTION_DESC,
                    (
                        SELECT
                            TOP 1 PARTNERFUNCTION_ID
                        FROM
                            SYPFTY
                        WHERE
                            C4C_PARTNER_FUNCTION = CASE
                                '{C4c_partner_function}'
                                WHEN '39' THEN 'EMPLOYEE RESPONSIBLE'
                                WHEN '46' THEN 'SALES EMPLOYEE'
                                WHEN '213' THEN 'PARTNER CONTACT'
                                WHEN 'Z1' THEN 'BD'
                                WHEN 'Z2' THEN 'BD MANAGER'
                                WHEN 'Z3' THEN 'SALES CONTRACT SUPPORT'
                                WHEN 'Z4' THEN 'SALES MANAGER'
                                WHEN 'Z5' THEN 'SALES REP'
                                WHEN 'ZCM' THEN 'CONTRACT MANAGER'
                                WHEN 'ZFM' THEN 'FINANCE MANAGER'
                                WHEN 'Z10' THEN 'LEGAL PERSON'
                                WHEN 'Z11' THEN 'PRICING PERSON'
                                WHEN 'Z12' THEN 'MARKETING AND BD HEAD'
                                WHEN 'Z13' THEN 'SSC HEAD'
                                WHEN 'Z14' THEN 'AGS HEAD'
                                WHEN 'Z15' THEN 'CM MANAGER'
                                WHEN 'Z16' THEN 'AGS REV REC FINANCE MANAGER'
                                WHEN 'Z6' THEN 'BD HEAD'
                                WHEN 'Z7' THEN 'MARKETING HEAD'
                                WHEN 'Z8' THEN 'REGIONAL FINANCE CONTROLLER'
                                WHEN 'Z9' THEN 'AGS FINANCE CONTROLLER'
                                WHEN 'ZF' THEN 'FAB'
                                ELSE 'FOB'
                            END
                    ) AS PARTNERFUNCTION_ID,
                    (
                        SELECT
                            TOP 1 PARTNERFUNCTION_RECORD_ID
                        FROM
                            SYPFTY
                        WHERE
                            C4C_PARTNER_FUNCTION = CASE
                                '{C4c_partner_function}'
                                WHEN '39' THEN 'EMPLOYEE RESPONSIBLE'
                                WHEN '46' THEN 'SALES EMPLOYEE'
                                WHEN '213' THEN 'PARTNER CONTACT'
                                WHEN 'Z1' THEN 'BD'
                                WHEN 'Z2' THEN 'BD MANAGER'
                                WHEN 'Z3' THEN 'SALES CONTRACT SUPPORT'
                                WHEN 'Z4' THEN 'SALES MANAGER'
                                WHEN 'Z5' THEN 'SALES REP'
                                WHEN 'ZCM' THEN 'CONTRACT MANAGER'
                                WHEN 'ZFM' THEN 'FINANCE MANAGER'
                                WHEN 'Z10' THEN 'LEGAL PERSON'
                                WHEN 'Z11' THEN 'PRICING PERSON'
                                WHEN 'Z12' THEN 'MARKETING AND BD HEAD'
                                WHEN 'Z13' THEN 'SSC HEAD'
                                WHEN 'Z14' THEN 'AGS HEAD'
                                WHEN 'Z15' THEN 'CM MANAGER'
                                WHEN 'Z16' THEN 'AGS REV REC FINANCE MANAGER'
                                WHEN 'Z6' THEN 'BD HEAD'
                                WHEN 'Z7' THEN 'MARKETING HEAD'
                                WHEN 'Z8' THEN 'REGIONAL FINANCE CONTROLLER'
                                WHEN 'Z9' THEN 'AGS FINANCE CONTROLLER'
                                WHEN 'ZF' THEN 'FAB'
                                ELSE 'FOB'
                            END
                    ) AS PARTNERFUNCTION_RECORD_ID,
                    SAEMPL.EMAIL,
                    SAEMPL.EMPLOYEE_ID,
                    SAEMPL.EMPLOYEE_NAME,
                    SAEMPL.EMPLOYEE_RECORD_ID,
                    '{is_primary}' as [PRIMARY],
                    {QuoteId} as QUOTE_ID,
                    '{QuoteRecordId}' as QUOTE_RECORD_ID,
                    '{RevisionId}' as QTEREV_ID,
                    '{RevisionRecordId}' as QTEREV_RECORD_ID
                FROM
                    SAEMPL
                WHERE
                    EMPLOYEE_ID = '{EmployeeId}'
            ) emp
        """.format(
            UserId=User.Id,
            EmployeeId=employee.get("EMPLOYEE_ID"),
            C4c_partner_function=employee.get("C4C_PARTNER_FUNCTION"),
            UserName=User.Name,
            QuoteId=contract_quote_data.get("QUOTE_ID"),
            QuoteRecordId=contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
            RevisionId=quote_rev_id,
            RevisionRecordId=quote_revision_id,
            is_primary="1" if employee.get("PRIMARY").upper() == "TRUE" else "0",
        )
        Sql.RunQuery(query)
        created_by_master_rec = Sql.GetFirst("SELECT * FROM SYPFTY (NOLOCK) WHERE C4C_PARTNER_FUNCTION = 'CREATED BY'")
        if created_by_master_rec:
            saempl_data = Sql.GetFirst(
                "SELECT * FROM SAEMPL (NOLOCK) WHERE EMPLOYEE_ID = '{EmployeeId}'".format(EmployeeId=employee.get("EMPLOYEE_ID"))
            )
            saqdlt_data = Sql.GetFirst(
                "SELECT C4C_PARTNERFUNCTION_ID FROM SAQDLT (NOLOCK) WHERE QUOTE_RECORD_ID = '"
                + str(contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"))
                + "' AND C4C_PARTNERFUNCTION_ID = 'CREATED BY'"
            )
            if not saqdlt_data:
                sales_team_table = Sql.GetTable("SAQDLT")
                sales_team_createdby_insert = {
                    "QUOTE_REV_DEAL_TEAM_MEMBER_ID": str(Guid.NewGuid()).upper(),
                    "C4C_PARTNERFUNCTION_ID": created_by_master_rec.C4C_PARTNER_FUNCTION,
                    "PARTNERFUNCTION_DESC": created_by_master_rec.PARTNERFUNCTION_DESCRIPTION,
                    "PARTNERFUNCTION_ID": created_by_master_rec.PARTNERFUNCTION_ID,
                    "PARTNERFUNCTION_RECORD_ID": created_by_master_rec.PARTNERFUNCTION_RECORD_ID,
                    "EMAIL": saempl_data.EMAIL,
                    "MEMBER_ID": saempl_data.EMPLOYEE_ID,
                    "MEMBER_NAME": saempl_data.EMPLOYEE_NAME,
                    "MEMBER_RECORD_ID": saempl_data.EMPLOYEE_RECORD_ID,
                    "QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
                    "QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
                    "QTEREV_ID": quote_rev_id,
                    "QTEREV_RECORD_ID": quote_revision_id,
                    "PRIMARY": "1",
                }
                sales_team_table.AddRow(sales_team_createdby_insert)
                Sql.Upsert(sales_team_table)


# A055S000P01-8690 starts..
sync_obj = SyncQuoteAndCustomTables(Quote)
sync_obj.create_custom_table_record()

