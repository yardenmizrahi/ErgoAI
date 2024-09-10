import csv
import os

import AbstractDB


class CSVDatabase(AbstractDB.AbstractDB):
    @staticmethod
    def insert(table: str, key: str, value: str):
        file_name = table + "_tbl.csv"
        file_exists = os.path.isfile(file_name)

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

    @staticmethod
    def get(table: str, key: str):
        file_name = table + "tbl.csv"
        if not os.path.isfile(file_name):
            return None

        with open(file_name, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['key'] == key:
                    return row['value']

        return None
