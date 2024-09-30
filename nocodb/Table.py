from __future__ import annotations
import re
from nocodb.Record import Record
from nocodb.Column import Column, DataType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from nocodb.Base import Base
    from nocodb import NocoDB


import logging
_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


class Table:
    def __init__(self, noco_db: "NocoDB", **kwargs) -> None:

        self.noco_db = noco_db
        self.base_id = kwargs["base_id"]

        self.table_id = kwargs["id"]
        self.title = kwargs["title"]
        self.metadata = kwargs

    def get_basic_metadata(self) -> dict:
        m = self.metadata.copy()
        extra_keys = ["columns", "views", "columnsById"]
        return {k: v for k, v in m.items() if not k in extra_keys}

    def get_number_of_records(self) -> int:
        r = self.noco_db.call_noco(
            path=f"tables/{self.table_id}/records/count")
        return r.json()["count"]

    def get_columns(self, include_system: bool = False) -> list[Column]:
        r = self.noco_db.call_noco(
            path=f"meta/tables/{self.table_id}")
        cols = [Column(noco_db=self.noco_db, **f) for f in r.json()["columns"]]
        if include_system:
            return cols
        else:
            return [c for c in cols if not c.system and not c.primary_key]

    def get_columns_hash(self) -> str:
        r = self.noco_db.call_noco(
            path=f"meta/tables/{self.table_id}/columns/hash")
        return r.json()["hash"]

    def get_column_by_title(self, title: str) -> Column:
        try:
            return next((r for r in self.get_columns() if r.title == title))
        except StopIteration:
            raise Exception(f"Column with title {title} not found!")

    def create_column(self, column_name: str,
                      title: str, data_type: DataType = Column.DataType.SingleLineText,
                      **kwargs) -> Column:
        kwargs["column_name"] = column_name
        kwargs["title"] = title
        kwargs["uidt"] = str(data_type)

        r = self.noco_db.call_noco(path=f"meta/tables/{self.table_id}/columns",
                                   method="POST",
                                   json=kwargs)
        return self.get_column_by_title(title=title)

    def duplicate(self,
                  exclude_data: bool = True,
                  exclude_views: bool = True) -> None:
        r = self.noco_db.call_noco(path=f"meta/duplicate/{self.base_id}/table/{self.table_id}",
                                   method="POST",
                                   json={"excludeData": exclude_data,
                                         "excludeViews": exclude_views})
        _logger.info(f"Table {self.title} duplicated")
        return

        # Bug in noco API, wrong Id response

    def get_duplicates(self) -> list["Table"]:
        duplicates = {}
        for t in self.get_base().get_tables():
            if re.match(f"^{self.title} copy(_\\d+)?$", t.title):
                nr = re.findall("_(\\d+)", t.title)
                if nr:
                    duplicates[int(nr[0])] = t
                else:
                    duplicates[0] = t

        return list(dict(sorted(duplicates.items(), reverse=True)).values())

    def delete(self) -> bool:
        r = self.noco_db.call_noco(path=f"meta/tables/{self.table_id}",
                                   method="DELETE")
        _logger.info(f"Table {self.title} deleted")
        return r.json()

    def get_records(self, params: dict | None = None) -> list[Record]:
        params = params or {}

        if any([p in params for p in ["offset", "limit"]]):
            get_all_records = False

        else:
            get_all_records = True
            params["offset"] = 0
            params["limit"] = 1000

        records = []

        while True:

            r = self.noco_db.call_noco(
                path=f"tables/{self.table_id}/records", params=params)

            records.extend([Record(self, **r)
                            for r in r.json()["list"]])

            if r.json()["pageInfo"]["isLastPage"]:
                break
            elif not get_all_records:
                break
            else:
                params["offset"] += params["limit"]

        return records

    def get_record(self, record_id: int) -> Record:
        r = self.noco_db.call_noco(
            path=f"tables/{self.table_id}/records/{record_id}")
        return Record(self, **r.json())

    def get_records_by_field_value(self, field: str, value) -> list[Record]:
        return self.get_records(params={"where": f"({field},eq,{value})"})

    def create_record(self, **kwargs) -> Record:
        r = self.noco_db.call_noco(path=f"tables/{self.table_id}/records",
                                   method="POST",
                                   json=kwargs)
        return self.get_record(record_id=r.json()["Id"])

    def create_records(self, records: list[dict]) -> list[Record]:
        r = self.noco_db.call_noco(path=f"tables/{self.table_id}/records",
                                   method="POST",
                                   json=records)
        ids_string = ','.join([str(d["Id"]) for d in r.json()])
        return self.get_records(params={"where": f"(Id,in,{ids_string})"})

    def get_base(self) -> Base:
        return self.noco_db.get_base(self.base_id)
