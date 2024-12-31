from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nocodb import NocoDB


from nocodb.Base import Base
from nocodb.Table import Table

import logging

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


class Workspace:
    def __init__(self, noco_db: "NocoDB", **kwargs) -> None:

        self.noco_db = noco_db
        self.workspace_id = kwargs["id"]
        self.title = kwargs["title"]
        self.metadata = kwargs

        self.bases_path = f"meta/workspaces/{self.workspace_id}/bases"

    def get_bases(self) -> list[Base]:
        r = self.noco_db.call_noco(path=self.bases_path)
        return [Base(noco_db=self.noco_db, **f) for f in r.json()["list"]]

    def create_base(self, title: str, **kwargs) -> Base:
        defaults = {"title": title, "type": "database"}
        kwargs = {**defaults, **kwargs}

        r = self.noco_db.call_noco(path=self.bases_path,
                                   method="POST",
                                   json=kwargs)
        return self.noco_db.get_base(base_id=r.json()["id"])


class OSSWorkspace(Workspace):
    def __init__(self, noco_db: "NocoDB") -> None:
        super().__init__(noco_db, id="", title="")

        self.bases_path = f"meta/bases"
