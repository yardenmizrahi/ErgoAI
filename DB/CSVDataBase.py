import csv
import os

from DB.AbstractDB import AbstractDB


class CSVDatabase(AbstractDB):
    @staticmethod
    def insert(table: str, key: str, value: str):
        file_name = CSVDatabase.get_table_filename(table)
        file_exists = os.path.isfile(file_name)
        print(os.path.abspath("."))

        data = {}
        if file_exists:
            with open(file_name, mode='r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data[row['key']] = row['value']

        data[key] = value

        with open(file_name, mode='w', newline='') as csvfile:
            fieldnames = ['key', 'value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for k, v in data.items():
                writer.writerow({'key': k, 'value': v})
        return {"status": "done"}

    @staticmethod
    def get(table: str, key: str | None = None, keys: list | None = None) -> dict:
        out = {}
        file_name = CSVDatabase.get_table_filename(table)
        if not os.path.isfile(file_name):
            return None

        if not keys:
            keys = []

        if key:
            keys.append(key)

        with open(file_name, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                if row['key'] in keys:
                    out[row['key']] = row['value']

        return out

    @staticmethod
    def get_table_filename(table):
        return os.path.join("tbls", f"{table}_tbl.csv")
