import json
import os
import unittest

import cv2
import requests


class TestPostureDetectionAPI(unittest.TestCase):

    def setUp(self):
        # Define the path to the image directory
        self.image_dir = "Posture/SittingPostureRecognition/sample_images"
        # Get a list of all image files in the directory
        self.image_files = [f for f in os.listdir(self.image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]

        # Define the base URL for the Flask server (assuming it's running locally on port 2600)
        self.base_url = "http://127.0.0.1:5100/handle"

    def encode_image_to_hex(self, image_path):
        """Helper function to read an image and encode it as a hex string."""
        # Read the image using OpenCV
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)

        # Encode the image to JPEG format
        _, img_encoded = cv2.imencode('.jpg', img)

        # Convert the image to hex string
        image_hex = img_encoded.tobytes().hex()
        return image_hex

    def test_compare_analysis_results(self):
        """Test that sends the image data to the Flask server and compares the analysis results against saved text files."""
        for image_file in self.image_files:
            with self.subTest(image_file=image_file):
                # Construct the full image path
                image_path = os.path.join(self.image_dir, image_file)

                # Get the hex-encoded image data
                image_hex = self.encode_image_to_hex(image_path)

                # Prepare the request payload
                request_data = {
                    "request_type": "analyze",
                    "session_token": "test_token",
                    "payload": {
                        "session_token": "test_token",
                        "user_token": "test_user",
                        "time": 1234567890,
                        "image_data": image_hex
                    }
                }

                # Send the POST request to the Flask server
                try:
                    print(self.base_url)
                    response = requests.post(self.base_url, json=request_data)
                except requests.exceptions.RequestException as e:
                    self.fail(f"HTTP request failed for {image_file}: {e}")
                    continue

                # Check if the request was successful
                self.assertEqual(response.status_code, 200, f"Failed to analyze {image_file}")

                # Parse the server response
                response_data = response.json()

                # Define the path to the saved analysis result (txt file)
                analysis_file_name = os.path.splitext(image_file)[0] + ".txt"
                analysis_file_path = os.path.join(self.image_dir, analysis_file_name)

                # Read the saved analysis result from the text file
                with open(analysis_file_path, 'r') as f:
                    saved_analysis_result = f.read()
                    print("Expected:", saved_analysis_result)
                    print("Result:", response_data['result'])

                saved = json.loads(saved_analysis_result)

                for metric in saved.keys():
                    self.assertEqual(response_data['result'][metric], saved[metric],
                                     f"Analysis result for {image_file} does not match the saved result. "
                                     f" result: {response_data['result']}"
                                     f" expected {saved}")


if __name__ == '__main__':
    unittest.main()
