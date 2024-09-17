from __future__ import annotations
class Column:
    def __init__(self, **kwargs) -> None:
        self.title = kwargs["title"]
        self.column_id = kwargs["id"]
        self.system = bool(kwargs["system"])
        self.primary_key = bool(kwargs["pk"])
        self.metadata = kwargs

    @staticmethod
    def get_id_metadata() -> list[dict]:
        return [
            {'title': 'Id', 'column_name': 'id', 'uidt': 'ID',
             'dt': 'int4', 'np': '11', 'ns': '0', 'clen': None,
             'pk': True, 'pv': None, 'rqd': True, 'ct': 'int(11)', 'ai': True,
             'dtx': 'integer', 'dtxp': '11', },
            {'title': 'Title', 'column_name': 'title', 'uidt': 'SingleLineText',
             'dt': 'character varying', 'np': None, 'ns': None, 'clen': '45',
             'pk': False, 'pv': True, 'rqd': False, 'ct': 'varchar(45)', 'ai': False,
             'dtx': 'specificType', 'dtxp': '45', }
        ]
