
from nocodb.Record import Record
from nocodb.Column import Column

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from nocodb.Base import Base


class Table:
    def __init__(self, base: "Base", **kwargs) -> None:

        self.base = base
        self.noco_db = base.noco_db

        self.table_id = kwargs["id"]
        self.title = kwargs["title"]
        self.metadata = kwargs

    def get_number_of_records(self) -> int:
        r = self.noco_db.call_noco(
            path=f"tables/{self.table_id}/records/count")
        return r.json()["count"]

    def get_columns(self) -> list[Column]:
        r = self.noco_db.call_noco(
            path=f"meta/tables/{self.table_id}")
        return [Column(**f) for f in r.json()["columns"]]

    def get_columns_hash(self) -> str:
        r = self.noco_db.call_noco(
            path=f"meta/tables/{self.table_id}/columns/hash")
        return r.json()["hash"]

    def get_column_by_title(self, title: str) -> Column:
        try:
            return next((r for r in self.get_columns() if r.title == title))
        except StopIteration:
            raise Exception(f"Column with title {title} not found!")

    def duplicate(self,
                  exclude_data: bool = True,
                  exclude_views: bool = True) -> None:
        r = self.noco_db.call_noco(path=f"meta/duplicate/{self.base.base_id}/table/{self.table_id}",
                                   method="POST",
                                   json={"excludeData": exclude_data,
                                         "excludeViews": exclude_views})

        # Bug in noco API, wrong Id response

    def delete(self) -> bool:
        r = self.noco_db.call_noco(path=f"meta/tables/{self.table_id}",
                                   method="DELETE")
        return r.json()

    def get_records(self, params: dict = {}) -> list[Record]:

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
