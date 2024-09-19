import os
import unittest

from DB.CSVDataBase import CSVDatabase


class TestCSVDatabase(unittest.TestCase):
    def setUp(self):
        self.file_name = "test_tbl.csv"

    def tearDown(self):
        os.remove(self.file_name)

    def test_get(self):
        CSVDatabase.insert("test", "key1", "value1")
        CSVDatabase.insert("test", "key2", "value2")

        result = CSVDatabase.get("test", keys=["key1"])

        self.assertEqual(result['key1'], 'value1')


if __name__ == '__main__':
    unittest.main()
