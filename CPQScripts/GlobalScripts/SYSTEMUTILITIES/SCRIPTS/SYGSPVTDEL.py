# =========================================================================================================================================
#   __script_name : SYGSPVTDEL.PY
#   __script_description : THIS SCRIPT IS USED TO DELETE DATA IN A PIVOT TABLE.
#   __primary_author__ : SIVANANDHAM MURUGAN
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import SYTABACTIN as Table
from SYDATABASE import SQL
Sql = SQL()

LABLE = Param.LABLE
Attr_val = Param.ATTRVAL

LABLE = LABLE.replace(" ", "_").split(",")

VALUE = Param.VALUE
VALUE = VALUE.split(",")

TABLEID = Param.TABLEID


row = dict(zip(LABLE, VALUE))

if TABLEID == "SET_ATTRIBUTE_MATERIALS":
    
    primaryQueryItems = Sql.GetList(
        "select SETMATATTVAL_RECORD_ID FROM MASMAV where SAP_PART_NUMBER = '"
        + str(row.get("SAP_PART_NUMBER"))
        + "' and SETMAT_RECORD_ID='"
        + str(row.get("SET_MATERIAL_RECORD_ID"))
        + "'"
    )
    if primaryQueryItems is not None:
        for RECORD_ID in primaryQueryItems:
            
            Table.TableActions.Delete(
                "MASMAV", "SETMATATTVAL_RECORD_ID", str(RECORD_ID.SETMATATTVAL_RECORD_ID)
            )
elif TABLEID == "MATERIAL_ATTRIBUTES":
    if Attr_val is not None and len(VALUE) > 0:

        MAMAAT_primaryQueryItems = Sql.GetList(
            "select * FROM MAMAAT (NOLOCK) where ATTRIBUTE_RECORD_ID = '"
            + Attr_val
            + "' and MATERIAL_RECORD_ID = '"
            + VALUE[0]
            + "'"
        )
        for MAMAAT_primaryItem in MAMAAT_primaryQueryItems:
            tableInfo = Sql.GetTable("MAMAAT")
            tableInfo.AddRow(MAMAAT_primaryItem)
            Sql.Delete(tableInfo)
            

        MAMAAV_primaryQueryItems = Sql.GetList(
            "select * FROM MAMAAV (NOLOCK) where ATTRIBUTE_RECORD_ID = '"
            + Attr_val
            + "' and MATERIAL_RECORD_ID = '"
            + VALUE[0]
            + "'"
        )
        for MAMAAV_primaryItem in MAMAAV_primaryQueryItems:
            tableInfo = Sql.GetTable("MAMAAV")
            tableInfo.AddRow(MAMAAV_primaryItem)
            Sql.Delete(tableInfo)
            

        """Material = Product.GetContainerByName('CTR_MATERIALS_PIVOT_TABLE')
        if Material is not None:
            for row in Material.Rows:
                if Attr_val == row['Attribute_recordid']:
                    rowid = row.RowIndex
            Material.DeleteRow(rowid)
            Trace.Write("Material container Deleted Index Id----"+str(rowid))"""

elif TABLEID == "MATERIALS_WITH_ATTRIBUTES":
    
    if Attr_val is not None and len(VALUE) > 0:
     
        MAMAAT_primaryQueryItems = Sql.GetList(
            "select * FROM MAMAAT where ATTRIBUTE_RECORD_ID = '"
            + VALUE[0]
            + "' and SAP_PART_NUMBER = '"
            + Attr_val
            + "'"
        )
        for MAMAAT_primaryItem in MAMAAT_primaryQueryItems:
            tableInfo = Sql.GetTable("MAMAAT")
            tableInfo.AddRow(MAMAAT_primaryItem)
            Sql.Delete(tableInfo)
            

        MAMAAV_primaryQueryItems = Sql.GetList(
            "select * FROM MAMAAV where ATTRIBUTE_RECORD_ID = '"
            + VALUE[0]
            + "' and SAP_PART_NUMBER = '"
            + Attr_val
            + "'"
        )
        
        for MAMAAV_primaryItem in MAMAAV_primaryQueryItems:
            tableInfo = Sql.GetTable("MAMAAV")
            tableInfo.AddRow(MAMAAV_primaryItem)
            Sql.Delete(tableInfo)
            

        """Attribute = Product.GetContainerByName('CTR_ATTRIBUTES_PIVOT_TABLE')
        if Attribute is not None:
            for row in Attribute.Rows:
                if Attr_val == row['Attribute_recordid']:
                    rowid = row.RowIndex
            Attribute.DeleteRow(rowid)
            Trace.Write("Attribute container Deleted Index Id----"+str(rowid))"""

else:
    Trace.Write(
        "select * FROM MAMAAT where SAP_PART_NUMBER = '"
        + str(row.get("SAP_PART_NUMBER"))
        + "'"
    )
    primaryQueryItems = Sql.GetList(
        "select MATERIAL_ATTRIBUTE_RECORD_ID FROM MAMAAT where SAP_PART_NUMBER = '"
        + str(row.get("SAP_PART_NUMBER"))
        + "'"
    )
    if primaryQueryItems is not None:
        for RECORD_ID in primaryQueryItems:
            Table.TableActions.Delete(
                "MAMAAT",
                "MATERIAL_ATTRIBUTE_RECORD_ID",
                str(RECORD_ID.MATERIAL_ATTRIBUTE_RECORD_ID),
            )

    Trace.Write(
        "select * FROM MAMAAV where SAP_PART_NUMBER = '"
        + str(row.get("SAP_PART_NUMBER"))
        + "'"
    )
    primaryQueryItems = Sql.GetList(
        "select MATATTVAL_RECORD_ID FROM MAMAAV where SAP_PART_NUMBER = '"
        + str(row.get("SAP_PART_NUMBER"))
        + "'"
    )
    if primaryQueryItems is not None:
        for RECORD_ID in primaryQueryItems:
            Table.TableActions.Delete(
                "MAMAAV", "MATATTVAL_RECORD_ID", str(RECORD_ID.MATATTVAL_RECORD_ID)
            )