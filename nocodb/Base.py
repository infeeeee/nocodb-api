from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from nocodb import NocoDB


from nocodb.Column import Column
from nocodb.Table import Table

import logging
_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


class Base:
    def __init__(self, noco_db: "NocoDB",
                 **kwargs) -> None:

        self.noco_db = noco_db
        self.base_id = kwargs["id"]
        self.title = kwargs["title"]
        self.metadata = kwargs

    def duplicate(self,
                  exclude_data: bool = True,
                  exclude_views: bool = True,
                  exclude_hooks: bool = True
                  ) -> "Base":

        r = self.noco_db.call_noco(path=f"meta/duplicate/{self.base_id}",
                                   method="POST",
                                   json={
            "excludeData": exclude_data,
            "excludeViews": exclude_views,
            "excludeHooks": exclude_hooks})
        _logger.info(f"Base {self.title} duplicated")

        return self.noco_db.get_base(base_id=r.json()["base_id"])

    def delete(self) -> bool:
        r = self.noco_db.call_noco(path=f"meta/bases/{self.base_id}",
                                   method="DELETE")
        _logger.info(f"Base {self.title} deleted")
        return r.json()

    def update(self, **kwargs) -> None:
        self.noco_db.call_noco(path=f"meta/bases/{self.base_id}",
                               method="PATCH",
                               json=kwargs)

    def get_base_info(self) -> dict:
        r = self.noco_db.call_noco(path=f"meta/bases/{self.base_id}/info")
        return r.json()

    def get_tables(self) -> list[Table]:
        r = self.noco_db.call_noco(path=f"meta/bases/{self.base_id}/tables")
        tables = [Table(noco_db=self.noco_db, **t) for t in r.json()["list"]]
        _logger.debug(f"Tables in base {self.title}: "
                      + str([t.title for t in tables]))
        return tables

    def get_table(self, table_id: str) -> Table:
        r = self.noco_db.call_noco(
            path=f"meta/tables/{table_id}")
        return Table(noco_db=self.noco_db, **r.json())

    def get_table_by_title(self, title: str) -> Table:
        try:
            return next((b for b in self.get_tables() if b.title == title))
        except StopIteration:
            raise Exception(f"Table with name {title} not found!")

    def create_table(self, table_name: str,
                     columns: list[dict] | None = None, add_default_columns: bool = True,
                     **kwargs) -> Table:
        kwargs["table_name"] = table_name

        if not columns:
            kwargs["columns"] = Column.get_id_metadata()
        elif add_default_columns:
            columns.extend(Column.get_id_metadata())
            kwargs["columns"] = columns
        else:
            kwargs["columns"] = columns

        r = self.noco_db.call_noco(path=f"meta/bases/{self.base_id}/tables",
                                   method="POST",
                                   json=kwargs)
        return self.get_table(table_id=r.json()["id"])
