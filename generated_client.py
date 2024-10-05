import pip

pip.main(["install", "opencv-python"])
pip.main(["install", "requests"])

import hashlib
import cv2
import requests
import time
import tkinter as tk
from tkinter import messagebox
import json
from collections import Counter

SERVER_URL = >>>SERVER_URL<<<
SALT = >>>SALT<<<


# Hash the password with the generated salt
def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()


# Capture an image from the webcam
def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if ret:
        cap.release()
        # Convert the image to JPEG format
        _, img_encoded = cv2.imencode('.jpg', frame)
        return img_encoded.tobytes()
    else:
        cap.release()
        raise Exception("Failed to capture image")


def upload_image(username, password, timestamp, image_data):
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


def get_data(username, password, keys=[]):
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


def show_summary(data):
    # Create the main Tkinter window
    root = tk.Tk()
    root.withdraw()
    # root.after(10, lambda: root.destroy())  # Close the mainloop automatically
    messagebox.showinfo("Posture", f"Summary for the last minute:\n{data}")
    root.destroy()
    # Show the window and keep it updated without blocking
    # root.mainloop()  # Start the mainloop to show the window


def most_common_posture(data_dict):
    # Step 1: Parse the JSON strings into Python dictionaries
    postures = []

    for value in data_dict.values():
        parsed_value = json.loads(value)
        posture = parsed_value.get("posture")  # Extract the "posture" key
        if posture:
            postures.append(posture)

    # Step 2: Use Counter to find the most common posture
    counter = Counter(postures)
    most_common = counter.most_common(1)[0]  # Get the most common posture and its frequency

    return most_common[0]


def main():
    # Ask for user credentials
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Authenticate the user and get the session token
    # try:
    #     session_token = authenticate(username, password)
    #     print(f"Authenticated! Session token: {session_token}")
    # except Exception as e:
    #     print(str(e))
    #     return


    salted_password = hash_password(password, SALT)

    while True:
        try:
            # Capture the current timestamp
            timestamp = str(int(time.time()))

            # Capture an image from the webcam
            image_data = capture_image()
            print("Image captured successfully")

            # Upload the image to the server
            upload_image(username, salted_password, timestamp, image_data)
            print(get_data(username, salted_password, [timestamp]))
            # Wait for the next interval (e.g., 10 seconds)

            if time.localtime().tm_min == 0:
                data = get_data(username, salted_password, [str(t) for t in range(int(time.time()) - 3600, int(time.time()))])
                show_summary(most_common_posture(data.json()))

            time.sleep(10)

        except Exception as e:
            print(f"Error: {str(e)}")
            break


if __name__ == "__main__":
    main()
