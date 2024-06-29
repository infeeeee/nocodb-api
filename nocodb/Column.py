class Column:
    def __init__(self, **kwargs) -> None:
        self.title = kwargs["title"]
        self.column_id = kwargs["id"]
        self.metadata = kwargs
