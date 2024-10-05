import json
from datetime import datetime

import cv2
import numpy
from Posture.SittingPostureRecognition import posture_image
from DB.RequestData import RequestData
from utils.RequestQueue import RequestQueue
import requests


class PostureDetectionAdapter:
    def __init__(self, config):
        self.queue = RequestQueue()
        self.available_actions = {"analyze": self.analyze}
        self.is_idle = True
        self.dispatcher_address = config.get("Dispatcher", dict()).get("Address", "localhost")
        self.dispatcher_port = config.get("Dispatcher", dict()).get("Port", 2600)

    def queue_request(self, request: RequestData) -> bool:
        if request.request_type in self.available_actions.keys():
            self.queue.queue_request(request)
            return True
        return False

    def handle_all_requests(self):
        if self.is_idle:
            self.is_idle = False

            while not self.queue.is_empty():
                self.process_request()

            self.is_idle = True

    def process_request(self):
        current_handled_request = self.queue.pop_request()
        current_handled_request.response = (
            self.available_actions[current_handled_request.request_type](current_handled_request))

    def analyze(self, request: RequestData):
        # Extract image data from the request
        image_data = request.payload['image_data']

        # Decode the image data from hex string
        image_bytes = bytes.fromhex(image_data)
        np_array = numpy.frombuffer(image_bytes, dtype=numpy.uint8)
        img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        request.response = posture_image.process_image_for_pose_analysis(img)
        url = f'http://{self.dispatcher_address}:{self.dispatcher_port}/handle'

        request.response["time"] = request.payload.get("time", str(datetime.now()))
        store_value = json.dumps(request.response)

        store_request = {"request_type": "store_db",
                         "session_token": request.session_token,
                         "payload": {"db_table": request.session_token,  # TODO
                                     "db_key": request.payload.get("time", str(datetime.now())),
                                     "db_value": store_value,
                                     "username": request.payload['username'],
                                     "password":  request.payload['password']}}
        print("POSTURE: ", url)

        print(requests.post(url, json=store_request))
        return request.response


# def test_analyze_with_image_path():
#     import json
#     # Define the path to the image directory
#     image_dir = "SittingPostureRecognition/sample_images"
#
#     # Get a list of all image files in the directory
#     image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
#
#     # Iterate over each image file
#     for image_file in image_files:
#         # Construct the full image path
#         image_path = os.path.join(image_dir, image_file)
#
#         # Read the image using OpenCV
#         img = cv2.imread(image_path, cv2.IMREAD_COLOR)
#
#         # Encode the image to JPEG format
#         _, img_encoded = cv2.imencode('.jpg', img)
#
#         # Prepare request data for analysis
#         request_data = RequestData(
#             request_type="analyze",
#             session_token="test_token",
#             payload={
#                 'session_token': "test_token",
#                 'user_token': "test_user",
#                 'time': 1234567890,
#                 'image_data': img_encoded.tobytes().hex()
#             }
#         )
#
#         # Perform the analysis
#         analysis_result = PostureDetectionAdapter().analyze(request_data)
#
#         # Save the analysis result to a text file with the same name as the image
#         analysis_file_name = os.path.splitext(image_file)[0] + ".txt"
#         analysis_file_path = os.path.join(image_dir, analysis_file_name)
#
#         with open(analysis_file_path, 'w') as f:
#             f.write(json.dumps(analysis_result))
#
#
# test_analyze_with_image_path()
