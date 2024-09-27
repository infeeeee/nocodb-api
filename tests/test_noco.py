from time import sleep
import unittest
import json
import os

from nocodb import NocoDB
from nocodb.Base import Base
from nocodb.Column import Column
from nocodb.Table import Table


import logging

logging.basicConfig()
logging.getLogger('nocodb').setLevel(level=logging.DEBUG)

CONFIG = {
    "NOCO_URL": "https://app.nocodb.com",
    "NOCO_API_KEY": "",
    "NOCO_BASE_ID": "",
    "TIMEOUT": "30"
}


def setUpModule():

    try:
        with open("test_config.json") as config_file:
            CONFIG.update(json.load(config_file))

    except FileNotFoundError:
        for s in CONFIG:
            if s in os.environ:
                CONFIG[s] = os.environ[s]

    TestData.noco = NocoDB(url=CONFIG["NOCO_URL"],
                           api_key=CONFIG["NOCO_API_KEY"])
    TestData.base = TestData.noco.get_base(base_id=CONFIG["NOCO_BASE_ID"])

    [t.delete() for t in TestData.base.get_tables()]


class TestData:
    noco: NocoDB
    base: Base
    table_nr: int = 0

    @classmethod
    def setUpClass(cls) -> None:
        sleep(int(CONFIG["TIMEOUT"]))

    @classmethod
    def get_new_table(cls) -> Table:
        tablename = cls.base.title + str(TestData.table_nr)
        TestData.table_nr += 1

        return cls.base.create_table(tablename)


class Test01Base(TestData, unittest.TestCase):

    def test_get_base(self):
        # get_bases
        # get_base_by_title

        # get_base
        self.assertIsInstance(self.base, Base)

        # create_base

    def test_empty_base(self):
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
            self.base.get_table_by_title(self.base.title)


class Test02Tables(TestData, unittest.TestCase):

    def setUp(self) -> None:
        # tablename = self.base.title + str(Test02Tables.table_nr)
        # Test02Tables.table_nr += 1

        # create_table
        self.table = self.get_new_table()

    def test_create_table(self):

        # get_table_by_title
        table_title = self.base.get_table_by_title(self.table.title)

        # get_table
        table_id = self.base.get_table(table_id=self.table.table_id)

        self.assertDictEqual(self.table.get_basic_metadata(),
                             table_title.get_basic_metadata())
        self.assertDictEqual(self.table.get_basic_metadata(),
                             table_id.get_basic_metadata())
        self.assertDictEqual(table_title.get_basic_metadata(),
                             table_id.get_basic_metadata())

    def test_empty_table(self):

        # get_number_of_records
        self.assertEqual(self.table.get_number_of_records(), 0)

        # get_columns
        self.assertEqual(len(self.table.get_columns(include_system=False)), 1)
        self.assertEqual(len(self.table.get_columns(include_system=True)), 6)

        # get_columns_hash
        # get_column_by_title
        with self.assertRaises(Exception):
            self.table.get_column_by_title("WrongTitle")

        self.assertIsInstance(self.table.get_column_by_title("Title"), Column)

        # duplicate
        self.assertEqual(len(self.table.get_duplicates()), 0)
        self.table.duplicate()

        sleep(3)

        duplicates = self.table.get_duplicates()

        self.assertEqual(len(duplicates), 1)

        duplicate = duplicates[0]
        self.assertIsInstance(duplicate, Table)

        self.assertIsNotNone(duplicate)

        # delete
        duplicate.delete()

        with self.assertRaises(Exception):
            self.base.get_table_by_title(duplicate.title)


class Test03Records(TestData, unittest.TestCase):

    def setUp(self) -> None:
        self.table = self.get_new_table()

    def test_empty_records(self):
        self.assertEqual(len(self.table.get_records()), 0)

    def test_create_records(self):

        # create_record
        self.table.create_record(Title="First Record")

        # get_records
        self.assertEqual(len(self.table.get_records()), 1)

        # get_record
        # get_records_by_field_value
        # create_records
