import unittest
from unittest.mock import patch

from DB.RequestData import RequestTypes, RequestData, generate


class TestRequestData(unittest.TestCase):
    def test_generate_valid_request(self):
        request_type = RequestTypes.store_db
        session_token = "valid_token"
        payload = {"data": "some_data"}

        result = generate(request_type, session_token, payload)

        self.assertIsInstance(result, RequestData)
        self.assertEqual(result.request_type, request_type)
        self.assertEqual(result.session_token, session_token)
        self.assertEqual(result.payload, payload)

    def test_generate_invalid_request(self):
        invalid_type = "invalid_type"
        session_token = "valid_token"
        payload = {"data": "some_data"}

        result = generate(invalid_type, session_token, payload)

        self.assertIsNone(result)

    def test_generate_with_empty_payload(self):
        request_type = RequestTypes.store_db
        session_token = "valid_token"
        payload = {}

        result = generate(request_type, session_token, payload)

        self.assertIsInstance(result, RequestData)
        self.assertEqual(result.request_type, request_type)
        self.assertEqual(result.session_token, session_token)
        self.assertEqual(result.payload, payload)

    def test_generate_with_none_payload(self):
        request_type = RequestTypes.store_db
        session_token = "valid_token"
        payload = None

        result = generate(request_type, session_token, payload)

        self.assertIsInstance(result, RequestData)
        self.assertEqual(result.request_type, request_type)
        self.assertEqual(result.session_token, session_token)
        self.assertIsNone(result.payload)

    @patch('your_module.RequestTypes.get_types', return_value=['store_db', 'get_db', 'analyze'])
    def test_generate_with_mocked_types(self, mock_get_types):
        request_type = "store_db"
        session_token = "valid_token"
        payload = {"data": "some_data"}

        result = generate(request_type, session_token, payload)

        self.assertIsInstance(result, RequestData)
        mock_get_types.assert_called_once()


if __name__ == '__main__':
    unittest.main()
