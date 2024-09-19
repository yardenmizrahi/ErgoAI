import json
import multiprocessing
import os
import unittest
from multiprocessing import Process

import requests

import DB.Endpoint
from DB.RequestData import RequestData


def send(type, table, key, value=None):
    valid = RequestData(request_type=type,
                        session_token="valid_token",
                        payload={"db_table": table, "db_key": key, "db_value": value})
    response, code = TestServerEndpoint.send_request_to_db(valid)
    return response


def client1(out_dict: dict):
    print("1")
    send("store_db", "c1", "k1", "v1")
    send("store_db", "c1", "k2", "v1")
    send("store_db", "c1", "k1", "v2")
    out_dict["out"] = send("get_db", "c1", "k1")
    print("1")


def client2(out_dict: dict):
    print("2")
    send("store_db", "c2", "k1", "v1")
    send("store_db", "c2", "k2", "v1")
    send("store_db", "c2", "k1", "v2")
    out_dict["out"] = send("get_db", "c2", "k1")
    print("2")


def client3(out_dict: dict):
    print("3")
    send("store_db", "c3", "k1", "v1")
    send("store_db", "c3", "k2", "v1")
    send("store_db", "c3", "k1", "v2")
    out_dict["out"] = send("get_db", "c3", "k1")
    print("3")


class TestServerEndpoint(unittest.TestCase):
    def setUp(self):
        # self.p = DB.Endpoint.async_run()
        self.file_name = "test"

    def tearDown(self):
        # self.p = DB.Endpoint.async_stop(self.p)
        if os.path.isfile(self.file_name+"_tbl.csv"):
            os.remove(self.file_name+"_tbl.csv")

    @staticmethod
    def send_request_to_db(request_data: RequestData) -> tuple[dict,int]:
        url = "http://localhost:2602"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=vars(request_data))

        try:
            return response.json(), response.status_code
        except json.JSONDecodeError:
            raise Exception("Invalid JSON response from server")

    def test_valid_request(self):
        valid = RequestData(request_type="store_db",
                            session_token="valid_token",
                            payload={"db_table": self.file_name, "db_key": "key1", "db_value": "value1"})

        response, code = TestServerEndpoint.send_request_to_db(valid)
        self.assertEqual(code, 200)
        self.assertEqual(response, {'status': 'done'})

        valid = RequestData(request_type="get_db",
                            session_token="valid_token",
                            payload={"db_table": self.file_name, "db_key": "key1"})

        response, code = TestServerEndpoint.send_request_to_db(valid)
        self.assertEqual(code, 200)
        self.assertEqual(response["key1"], "value1")

    def test_multiple_clients(self):
        manager = multiprocessing.Manager()
        o1 = manager.dict()
        o2 = manager.dict()
        o3 = manager.dict()

        p1 = Process(target=client1, args=(o1,))
        p2 = Process(target=client2, args=(o2,))
        p3 = Process(target=client3, args=(o3,))

        p1.start()
        p2.start()
        p3.start()

        p1.join()
        p2.join()
        p3.join()

        p1.close()
        p2.close()
        p3.close()

        self.assertEqual(o1.values()[0]["k1"], "v2")
        self.assertEqual(o2.values()[0]["k1"], "v2")
        self.assertEqual(o3.values()[0]["k1"], "v2")

    def test_invalid_request_type(self):
        invalid_data = RequestData(
            request_type="invalid_type",
            session_token="valid_token",
            payload={"data": "some_data"},
        )
        response, code = TestServerEndpoint.send_request_to_db(invalid_data)
        self.assertEqual(code, 400)
        self.assertEqual(response, {'error': 'Invalid request type'})


if __name__ == '__main__':
    unittest.main()
