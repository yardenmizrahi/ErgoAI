import threading
from datetime import datetime
from tkinter import messagebox

import cv2
import requests

# Constants for server configuration
IP_ADDRESS = '127.0.0.1'
PORT = 5000
UPLOAD_URL = f"http://{IP_ADDRESS}:{PORT}/upload"
USER_URL = f"http://{IP_ADDRESS}:{PORT}/user"
IMAGE_PATH = 'captured_image.jpg'
CAPTURE_INTERVAL = 15  # 4 minutes in seconds


def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    ret, frame = cap.read()

    if not ret:
        raise IOError("Failed to capture image")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f'captured_image_{timestamp}.jpg'
    cv2.imwrite(image_path, frame)

    cap.release()

    return image_path


def send_image(image_path):
    files = {'file': open(image_path, 'rb')}
    response = requests.post(UPLOAD_URL, files=files)

    if response.status_code == 200:
        confirmation_message = response.json().get("message", "No message from server")
        print(f"Server response: {confirmation_message}")
        messagebox.showinfo("Success", f"Server response: {confirmation_message}")
    else:
        print(f"Failed to send image. Status code: {response.status_code}")
        messagebox.showerror("Failed", f"Failed to send image. Status code: {response.status_code}")


def send_user_id(user_id):
    data = {'user_id': user_id}
    response = requests.post(USER_URL, data=data)

    if response.status_code == 200:
        csv_path = 'user_details.csv'
        with open(csv_path, 'wb') as f:
            f.write(response.content)
        print(f"CSV saved to {csv_path}")
    else:
        print(f"Failed to get CSV. Status code: {response.status_code}")


def capture_and_send_image():
    try:
        image_path = capture_image()
        send_image(image_path)
    except Exception as e:
        print(f"Error: {str(e)}")


def start_auto_capture():
    capture_and_send_image()
    threading.Timer(CAPTURE_INTERVAL, start_auto_capture).start()


if __name__ == '__main__':
    start_auto_capture()
