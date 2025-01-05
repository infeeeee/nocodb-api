from __future__ import annotations


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nocodb.Table import Table
    from nocodb import NocoDB


class DataType:

    def __init__(self, uidt: str) -> None:
        self.name = uidt

    def __str__(self) -> str:
        return self.name


class Column:
    def __init__(self, noco_db: "NocoDB", **kwargs) -> None:
        self.noco_db = noco_db
        self.title = kwargs["title"]
        self.column_id = kwargs["id"]
        self.table_id = kwargs["fk_model_id"]

        self.system = bool(kwargs["system"])
        self.primary_key = bool(kwargs["pk"])

        self.data_type = Column.DataType.get_data_type(kwargs["uidt"])

        self.col_options = kwargs.get("colOptions", {})
        self.formula_raw = self.col_options.get("formula_raw", None)
        self.linked_table_id = self.col_options.get(
            "fk_related_model_id", None)

        self.metadata = kwargs

    def get_linked_table(self) -> Table:
        if self.linked_table_id:
            return self.noco_db.get_table(self.linked_table_id)
        else:
            raise Exception("Not linked column!")

    def update(self, **kwargs) -> Column:
        r = self.noco_db.call_noco(
            path=f"meta/columns/{self.column_id}",
            method="PATCH",
            json=kwargs,
        )
        return self.noco_db.get_column(self.column_id)

    def delete(self) -> bool:
        r = self.noco_db.call_noco(
            path=f"meta/columns/{self.column_id}", method="DELETE")
        return r.json()

    @staticmethod
    def get_default_columns() -> list[dict]:
        return [
            {
                "title": "Id",
                "column_name": "id",
                "uidt": str(Column.DataType.ID),
                "pk": True,
                "dtx": "integer",
            },
            {
                "title": "Title",
                "column_name": "title",
                "uidt": str(Column.DataType.SingleLineText),
            }
        ]

    class DataType:
        Formula = DataType("Formula")
        LinkToAnotherRecord = DataType("LinkToAnotherRecord")
        Links = DataType("Links")
        Lookup = DataType("Lookup")
        Rollup = DataType("Rollup")
        Attachment = DataType("Attachment")
        AutoNumber = DataType("AutoNumber")
        Barcode = DataType("Barcode")
        Button = DataType("Button")
        Checkbox = DataType("Checkbox")
        Collaborator = DataType("Collaborator")
        Count = DataType("Count")
        CreatedBy = DataType("CreatedBy")
        CreatedTime = DataType("CreatedTime")
        Currency = DataType("Currency")
        Date = DataType("Date")
        DateTime = DataType("DateTime")
        Decimal = DataType("Decimal")
        Duration = DataType("Duration")
        Email = DataType("Email")
        ForeignKey = DataType("ForeignKey")
        GeoData = DataType("GeoData")
        Geometry = DataType("Geometry")
        ID = DataType("ID")
        JSON = DataType("JSON")
        LastModifiedBy = DataType("LastModifiedBy")
        LastModifiedTime = DataType("LastModifiedTime")
        LongText = DataType("LongText")
        MultiSelect = DataType("MultiSelect")
        Number = DataType("Number")
        Order = DataType("Order")
        Percent = DataType("Percent")
        PhoneNumber = DataType("PhoneNumber")
        QrCode = DataType("QrCode")
        Rating = DataType("Rating")
        SingleLineText = DataType("SingleLineText")
        SingleSelect = DataType("SingleSelect")
        SpecificDBType = DataType("SpecificDBType")
        Time = DataType("Time")
        URL = DataType("URL")
        User = DataType("User")
        Year = DataType("Year")

        @classmethod
        def get_data_type(cls, uidt: str) -> DataType:
            if hasattr(cls, uidt):
                return getattr(cls, uidt)
            else:
                raise Exception(f"Invalid datatype {uidt}")
