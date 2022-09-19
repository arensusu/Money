import unittest
from unittest.mock import patch

from table_method import *

class TestTableInsertion(unittest.TestCase):

    def setUp(self):
        self.table_method = Table()

    def test_insert_with_table_not_found(self):
        attr = {
            "user": "user",
            "date": "date",
            "year": "year",
            "month": "month",
            "day": "day",
            "term": "term",
            "price": 0
        }

        with patch("table_method.DBMethod.check_table_existed") as check:
            check.return_value = False
            self.assertEqual(self.table_method.insert("money_outcome", attr), "Error: Table not found")

    def test_insert_with_attribute_lost(self):
        attr = {
            "user": "user"
        }

        self.assertEqual(self.table_method.insert("money_outcome", attr), "Error: Lost")

    def test_insert_with_dummy_attribute(self):
        attr = {
            "dummy": "dummy",
            "user": "user",
            "date": "date",
            "year": "year",
            "month": "month",
            "day": "day",
            "term": "term",
            "price": 0
        }
        self.assertEqual(self.table_method.insert("money_outcome", attr), "Error: Dummy")

    def test_insert_completed(self):
        attr = {
            "user": "user",
            "date": "date",
            "year": "year",
            "month": "month",
            "day": "day",
            "term": "term",
            "price": 0
        }

        with patch("table_method.DBMethod.insert") as put_success:
            put_success.return_value = None
            self.assertEqual(self.table_method.insert("money_outcome", attr), f"已存入({attr['user']})")

    def test_insert_corupted(self):
        attr = {
            "user": "user",
            "date": "date",
            "year": "year",
            "month": "month",
            "day": "day",
            "term": "term",
            "price": 0
        }

        with patch("table_method.DBMethod.insert") as put_success:
            put_success.return_value = Exception()
            self.assertEqual(self.table_method.insert("money_outcome", attr), "Error: Insertion failed")

class TestTableQuery(unittest.TestCase):

    def setUp(self):
        self.table_method = Table()

    def test_query_with_table_not_found(self):
        attr = {
            "user": "user",
            "year": "year",
        }

        with patch("table_method.DBMethod.check_table_existed") as check:
            check.return_value = False
            self.assertEqual(self.table_method.query("money_outcome", attr), "Error: Table not found")

    def test_query_with_dummy_attribute(self):
        attr = {
            "dummy": "dummy",
            "user": "user"
        }
        self.assertEqual(self.table_method.query("money_outcome", attr), "Error: Dummy")

    def test_query_completed(self):
        attr = {
            "user": "user",
            "year": "year"
        }

        with patch("table_method.DBMethod.query") as put_success:
            put_success.return_value = None
            self.assertEqual(self.table_method.query("money_outcome", attr), "Query completed")

    def test_query_failed(self):
        attr = {
            "user": "user",
            "year": "year"
        }

        with patch("table_method.DBMethod.query") as put_success:
            put_success.return_value = Exception()
            self.assertEqual(self.table_method.query("money_outcome", attr), "Error: Query failed")


class TestTableDelete(unittest.TestCase):

    def setUp(self):
        self.table_method = Table()

    def test_delete_with_table_not_found(self):
        attr = {
            "user": "user",
            "date": "date"
        }

        with patch("table_method.DBMethod.check_table_existed") as check:
            check.return_value = False
            self.assertEqual(self.table_method.delete("money_outcome", attr), "Error: Table not found")

    def test_delete_with_key_lost(self):
        attr = {
            "user": "user"
        }

        self.assertEqual(self.table_method.delete("money_outcome", attr), "Error: Lost")

    def test_delete_with_dummy_key(self):
        attr = {
            "dummy": "dummy",
            "user": "user",
            "date": "date"
        }
        self.assertEqual(self.table_method.delete("money_outcome", attr), "Error: Dummy")

    def test_delete_completed(self):
        attr = {
            "user": "user",
            "date": "date"
        }

        with patch("table_method.DBMethod.delete") as put_success:
            put_success.return_value = None
            self.assertEqual(self.table_method.delete("money_outcome", attr), "Delete completed")

    def test_delete_failed(self):
        attr = {
            "user": "user",
            "date": "date"
        }

        with patch("table_method.DBMethod.delete") as put_success:
            put_success.return_value = Exception()
            self.assertEqual(self.table_method.delete("money_outcome", attr), "Error: Delete failed")

if __name__ == "__main__":
    unittest.main()