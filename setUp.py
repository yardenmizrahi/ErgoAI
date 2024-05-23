import cv2
import requests


def capture_image():
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # Capture a frame
    ret, frame = cap.read()

    if not ret:
        raise IOError("Failed to capture image")

    # Save the captured image to a file
    image_path = 'captured_image.jpg'
    cv2.imwrite(image_path, frame)

    # Release the camera
    cap.release()

    return image_path


def send_image(image_path, ip_address, port):
    url = f"http://{ip_address}:{port}/upload"
    files = {'file': open(image_path, 'rb')}

    response = requests.post(url, files=files)

    if response.status_code == 200:
        print("Image successfully sent")
    else:
        print(f"Failed to send image. Status code: {response.status_code}")


def send_user_id(user_id, ip_address, port):
    url = f"http://{ip_address}:{port}/user"
    data = {'user_id': user_id}

    response = requests.post(url, data=data)

    if response.status_code == 200:
        # Save the CSV content to a file
        csv_path = 'user_details.csv'
        with open(csv_path, 'wb') as f:
            f.write(response.content)
        print(f"CSV saved to {csv_path}")
    else:
        print(f"Failed to get CSV. Status code: {response.status_code}")


if __name__ == "__main__":
    # Replace with the actual IP address and port
    ip_address = '192.168.1.1'
    port = '8000'

    # Replace with the actual user ID
    user_id = '12345'

    # Capture an image and save it
    image_path = capture_image()
    print(f"Image saved to {image_path}")

    # Send the captured image
    send_image(image_path, ip_address, port)

    # Send the user ID and get the CSV
    send_user_id(user_id, ip_address, port)
