import unittest
import json
from nocodb import NocoDB
from nocodb.Base import Base
from nocodb.Column import Column
import os

from nocodb.Table import Table


class TestBase(unittest.TestCase):

    noco: NocoDB
    base: Base

    @classmethod
    def setUpClass(cls) -> None:

        CONFIG = {
            "url": "",
            "api_key": ""
        }

        try:
            with open("test_config.json") as config_file:
                CONFIG.update(json.load(config_file))

        except FileNotFoundError:
            for s in CONFIG:

                if isinstance(CONFIG[s], dict):
                    CONFIG[s] = json.loads(os.environ[s])
                else:
                    CONFIG[s] = os.environ[s]

        cls.noco = NocoDB(url=CONFIG["url"],
                          api_key=CONFIG["api_key"])
        cls.base = cls.noco.get_base(base_id="ppfdduj9kao482y")

        [t.delete() for t in cls.base.get_tables()]

    def test_00_init(self):

        # get_bases

        # get_base
        self.assertEqual(self.base.title, "UnitTest")

        # get_base_by_title
        # create_base

    def test_01_empty_base(self):
        # duplicate
        # delete
        # update
        # get_base_info
        base_info = self.base.get_base_info()
        for k in ['Node', 'Arch', 'Platform', 'Docker', 'RootDB', 'PackageVersion']:
            self.assertIn(k, base_info)

        # get_tables
        self.assertEqual(len(self.base.get_tables()), 0)

        # get_table_by_title
        with self.assertRaises(Exception):
            self.base.get_table_by_title("UnitTest")

    def test_02_create_table(self):

        # create_table
        table = self.base.create_table("UnitTest1")

        # get_table_by_title
        table_title = self.base.get_table_by_title("UnitTest1")

        # get_table
        table_id = self.base.get_table(table_id=table.table_id)

        self.assertDictEqual(table.get_basic_metadata(),
                             table_title.get_basic_metadata())
        self.assertDictEqual(table.get_basic_metadata(),
                             table_id.get_basic_metadata())
        self.assertDictEqual(table_title.get_basic_metadata(),
                             table_id.get_basic_metadata())

    def test_03_empty_table(self):

        table2 = self.base.create_table("UnitTest2")

        # get_number_of_records
        self.assertEqual(table2.get_number_of_records(), 0)

        # get_columns
        self.assertEqual(len(table2.get_columns(include_system=False)), 1)
        self.assertEqual(len(table2.get_columns(include_system=True)), 6)

        # get_columns_hash
        # get_column_by_title
        with self.assertRaises(Exception):
            table2.get_column_by_title("WrongTitle")

        self.assertIsInstance(table2.get_column_by_title("Title"), Column)

        # duplicate
        table2.duplicate()
        self.assertIsInstance(
            self.base.get_table_by_title("UnitTest2 copy"), Table)

        # delete
        self.base.get_table_by_title("UnitTest2 copy").delete()
        with self.assertRaises(Exception):
            self.base.get_table_by_title("UnitTest2 copy")

    def test_04_table_records(self):

        table3 = self.base.create_table("UnitTest3")

        # create_record
        table3.create_record(Title="First Record")

        # get_records
        # get_record
        # get_records_by_field_value
        # create_records
