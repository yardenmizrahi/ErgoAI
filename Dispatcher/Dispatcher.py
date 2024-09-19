import requests

from DB.RequestData import RequestData
from utils.RequestQueue import RequestQueue


class Dispatcher:
    def __init__(self, config):
        print("starting dispatcher")
        self.queue = RequestQueue()
        self.db_address = config.get("DB", dict()).get("Address", "localhost")
        self.db_port = config.get("DB", dict()).get("Port", 2600)
        self.posture_address = config.get("Posture", dict()).get("Address", "localhost")
        self.posture_port = config.get("Posture", dict()).get("Port", 2600)
        self.is_idle = True
        self.available_actions = ["get_db", "store_db", "analyze"]
        print("initialized")

    def queue_request(self, request: RequestData):
        if request.request_type in self.available_actions:
            self.queue.queue_request(request)
            # print(f"Request queued: {request.request_type} - {request.payload}")
            return True
        return False

    def process_request(self):
        current_handled_request = self.queue.pop_request()
        if current_handled_request:
            if current_handled_request.request_type == "analyze":
                print("Processing analyze request...")
                response = self.send_posture_request(current_handled_request)
                print(f"Analyze response: {response}")
            elif current_handled_request.request_type == "store_db" or current_handled_request.request_type == "get_db":
                print("Processing database request...")
                response = self.send_db_request(current_handled_request)
                print(f"Database response: {response}")
            return response
        else:
            print("Queue is empty.")

    def handle_all_requests(self):
        if self.is_idle:
            self.is_idle = False

            while not self.queue.is_empty():
                self.process_request()

            self.is_idle = True

    def send_posture_request(self, request_data: RequestData):
        return Dispatcher.send_request_data(self.posture_address, self.posture_port, request_data)

    def send_db_request(self, request_data: RequestData):
        return Dispatcher.send_request_data(self.db_address, self.db_port, request_data)

    @staticmethod
    def send_request_data(address, port, request_data):
        url = f'http://{address}:{port}/handle'

        request_payload = {
            "request_type": request_data.request_type,
            "session_token": request_data.session_token,
            "payload": request_data.payload
        }

        try:
            # Send POST request to the Flask server
            response = requests.post(url, json=request_payload)

            # Check if the request was successful
            if response.status_code == 200:
                return response.json()  # Return the parsed JSON response
            else:
                print(f"Failed to process request, status code: {response.status_code}")
                return {"error": f"Failed to process request, status code: {response.status_code}"}

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            return {"error": str(e)}