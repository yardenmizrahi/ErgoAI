import pip

pip.main(["install", "opencv-python"])
pip.main(["install", "requests"])

import hashlib
import uuid
import cv2
import requests
import time

SERVER_URL = >>>SERVER_URL<<<
SALT = >>>SALT<<<

# Hash the password with the generated salt
def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()


# Capture an image from the webcam
def capture_image():
    cap = cv2.VideoCapture(0)  # 0 is the default camera
    ret, frame = cap.read()

    if ret:
        cap.release()
        # Convert the image to JPEG format
        _, img_encoded = cv2.imencode('.jpg', frame)
        return img_encoded.tobytes()
    else:
        cap.release()
        raise Exception("Failed to capture image")


# Authenticate the user and get a session token
def authenticate(username, password):
    hashed_password = hash_password(password, SALT)

    # Prepare the authentication payload
    auth_payload = {
        'username': username,
        'password': password,
        'user_token': hashed_password
    }

    response = requests.post(f"{SERVER_URL}/getdata", json=auth_payload)

    if response.status_code == 200:
        return response.json().get("session_token")
    else:
        raise Exception("Authentication failed")


# Upload the image to the server
def upload_image(session_token, user_token, timestamp, image_data):
    upload_payload = {
        'session_token': session_token,
        'user_token': user_token,
        'time': timestamp,
        'image_data': image_data.hex()  # Convert image data to hex string
    }

    response = requests.post(f"{SERVER_URL}/upload", json=upload_payload)

    if response.status_code == 200:
        print("Image uploaded successfully")
    else:
        print("Failed to upload image")


# Main function
def main():
    # Ask for user credentials
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Authenticate the user and get the session token
    try:
        session_token = authenticate(username, password)
        print(f"Authenticated! Session token: {session_token}")
    except Exception as e:
        print(str(e))
        return

    user_token = hash_password(password, SALT)

    while True:
        try:
            # Capture the current timestamp
            timestamp = int(time.time())

            # Capture an image from the webcam
            image_data = capture_image()
            print("Image captured successfully")

            # Upload the image to the server
            upload_image(session_token, user_token, timestamp, image_data)

            # Wait for the next interval (e.g., 10 seconds)
            time.sleep(10)

        except Exception as e:
            print(f"Error: {str(e)}")
            break


if __name__ == "__main__":
    main()
