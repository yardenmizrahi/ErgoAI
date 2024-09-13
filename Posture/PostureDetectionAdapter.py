import os

import cv2

from DB.RequestData import RequestData
from utils.RequestQueue import RequestQueue


class PostureDetectionAdapter:
    def __init__(self):
        self.queue = RequestQueue()
        self.available_actions = {"analyze": self.analyze}
        self.is_idle = True

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

        # Decode the image using OpenCV
        img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

        # Save the image locally (replace with your desired directory)
        image_path = os.path.join("images", f"{request.session_token}_{request.payload['time']}.jpg")
        cv2.imwrite(image_path, img)

        request.result = posture_image.process_image_for_pose_analysis(image_path)

        return request.response


def test_analyze_with_image_path():
    image_path = "uploads/captured_image_20240623_143857.jpg"  # Replace with your test image path
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    _, img_encoded = cv2.imencode('.jpg', img)
    request_data = RequestData(
        request_type="analyze",
        session_token="test_token",
        payload={
            'session_token': "test_token",
            'user_token': "test_user",
            'time': 1234567890,
            'image_data': img_encoded.tobytes()
        }
    )

    PostureDetectionAdapter().analyze(request_data)


test_analyze_with_image_path()
