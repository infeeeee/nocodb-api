from __future__ import annotations
from typing import TYPE_CHECKING, Any
from pathlib import Path

from nocodb.Column import Column

if TYPE_CHECKING:
    from nocodb.Table import Table


class Record:
    def __init__(self, table: "Table", **kwargs) -> None:
        self.table = table
        self.noco_db = table.noco_db

        self.record_id = kwargs["Id"]
        self.metadata = kwargs

    def link_record(self, column: Column, link_record: "Record") -> bool:
        path = (
            f"tables/{self.table.table_id}/links/"
            + f"{column.column_id}/records/{self.record_id}"
        )
        r = self.noco_db.call_noco(
            path=path, method="POST", json={"Id": link_record.record_id}
        )

        return r.json()

    def link_records(self, column: Column, link_records: list["Record"]) -> bool:
        path = (
            f"tables/{self.table.table_id}/links/"
            + f"{column.column_id}/records/{self.record_id}"
        )
        r = self.noco_db.call_noco(
            path=path, method="POST", json=[{"Id": l.record_id} for l in link_records]
        )

        return r.json()

    def get_linked_records(self, column: Column) -> list[Record]:
        path = (
            f"tables/{self.table.table_id}/links/"
            + f"{column.column_id}/records/{self.record_id}"
        )
        r = self.noco_db.call_noco(path=path)

        if "list" in r.json():
            if not r.json()["list"]:
                return []
            elif isinstance(r.json()["list"], list):
                record_ids = [l["Id"] for l in r.json()["list"]]
            elif "Id" in r.json()["list"]:
                record_ids = [r.json()["list"]["Id"]]
            else:
                raise Exception("Invalid response")
        else:
            record_ids = [r.json()["Id"]]

        linked_table = self.noco_db.get_table(column.linked_table_id)
        return linked_table.get_records_by_id(record_ids)

    def get_value(self, field: str) -> Any:
        return self.get_values([field])[field]

    def get_column_value(self, column: Column) -> Any:
        return self.get_value(column.title)

    def get_values(self, fields: list[str] | None = None, include_system: bool = True) -> dict:
        if not include_system:
            cols = [c.title for c in self.table.get_columns(include_system)]
            if fields:
                fields = [f for f in fields if f in cols]
            else:
                fields = cols

        field_str = ",".join(fields) if fields else ""
        r = self.noco_db.call_noco(
            path=f"tables/{self.table.table_id}/records/{self.record_id}",
            params={"fields": field_str}
        )
        return r.json()

    def get_attachments(self, field: str, encoding: str = "utf-8") -> list[str]:
        value_list = self.get_value(field)
        if not isinstance(value_list, list):
            raise Exception("Invalid field value")

        return [
            self.noco_db.get_file(p["signedUrl"], encoding=encoding)
            for p in value_list
        ]

    def update(self, **kwargs) -> Record:
        kwargs["Id"] = self.record_id
        r = self.noco_db.call_noco(
            path=f"tables/{self.table.table_id}/records",
            method="PATCH",
            json=kwargs,
        )
        return self.table.get_record(record_id=r.json()["Id"])

    def upload_attachment(
        self, field: str, filepath: Path, mimetype: str = ""
    ) -> Record:
        value = self.get_value(field=field) or []
        value.append(self.noco_db.upload_file(
            filepath=filepath, mimetype=mimetype))

        return self.update(**{field: value})
