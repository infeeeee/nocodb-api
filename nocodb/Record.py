from __future__ import annotations
from typing import TYPE_CHECKING

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
        path = (f"tables/{self.table.table_id}/links/" +
                f"{column.column_id}/records/{self.record_id}")
        r = self.noco_db.call_noco(path=path,
                                   method="POST", json={"Id": link_record.record_id})

        return r.json()

    def link_records(self, column: Column, link_records: list["Record"]) -> bool:
        path = (f"tables/{self.table.table_id}/links/" +
                f"{column.column_id}/records/{self.record_id}")
        r = self.noco_db.call_noco(path=path,
                                   method="POST", json=[{"Id": l.record_id} for l in link_records])

        return r.json()
