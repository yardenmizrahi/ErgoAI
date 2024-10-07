import hashlib
import os
import cv2
import time
import json

import requests

IMAGE_DIRECTORY = r"C:\Users\Oded\PycharmProjects\ErgoAI\uploads\temp3"
RESULT_DIRECTORY = r"C:\Users\Oded\PycharmProjects\ErgoAI\uploads\temp3"


def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()


def get_data(username, password, keys=[], SERVER_URL="http://127.0.0.1:5000"):
    payload = {
        'session_token': username,
        'request_type': 'get_db',
        'payload': {
            'username': username,
            'password': password,
            "db_table": username,
            'db_keys': keys,
        }
    }
    response = requests.post(f"{SERVER_URL}/handle", json=payload)
    return response


def upload_image(username, password, timestamp, image_data, SERVER_URL="http://127.0.0.1:5000"):
    upload_payload = {
        'session_token': username,
        'request_type': 'analyze',
        'payload': {
            'username': username,
            'password': password,
            'time': timestamp,
            'image_data': image_data.hex()  # Convert image data to hex string
        }
    }

    response = requests.post(f"{SERVER_URL}/handle", json=upload_payload)

    if response.status_code == 200:
        print("Image uploaded successfully")
    else:
        print("Failed to upload image")


# Function to upload an image and get the result
def analyze_image(username, salted_password, image_path):
    # Read the image from file
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to read image: {image_path}")
        return

    # Convert the image to JPEG format
    _, img_encoded = cv2.imencode('.jpg', image)
    image_data = img_encoded.tobytes()

    # Capture current timestamp
    timestamp = str(int(time.time()))

    # Upload the image to the server
    upload_image(username, salted_password, timestamp, image_data)

    # Fetch the analysis result
    response = get_data(username, salted_password, [timestamp])

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to analyze image: {image_path}")
        return None


# Function to save analysis results to a text file
def save_result(image_path, result):
    image_name = os.path.basename(image_path)
    result_filename = os.path.splitext(image_name)[0] + ".txt"
    result_path = os.path.join(RESULT_DIRECTORY, result_filename)

    # Save the result as JSON in a text file
    with open(result_path, 'w') as result_file:
        json.dump(result, result_file, indent=4)

    print(f"Result saved: {result_path}")


def main():
    # Set up user credentials
    username = "test"
    # password = input("Enter your password: ")

    # Hash the password with the salt
    salted_password = "123" #"#hash_password(password, SALT)

    # Ensure result directory exists
    if not os.path.exists(RESULT_DIRECTORY):
        os.makedirs(RESULT_DIRECTORY)

    # Iterate through all image files in the directory
    for image_filename in os.listdir(IMAGE_DIRECTORY):
        image_path = os.path.join(IMAGE_DIRECTORY, image_filename)

        # Only process files with image extensions
        if image_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            print(f"Processing {image_filename}...")
            result = analyze_image(username, salted_password, image_path)

            if result:
                save_result(image_path, result)
        else:
            print(f"Skipping non-image file: {image_filename}")


if __name__ == "__main__":
    main()
