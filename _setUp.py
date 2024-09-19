import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
import requests


def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    ret, frame = cap.read()

    if not ret:
        raise IOError("Failed to capture image")

    image_path = 'captured_image.jpg'
    cv2.imwrite(image_path, frame)

    cap.release()

    return image_path


def send_image(image_path, ip_address, port):
    url = f"http://{ip_address}:{port}/upload"
    files = {'file': open(image_path, 'rb')}

    response = requests.post(url, files=files)

    if response.status_code == 200:
        messagebox.showinfo("Success", "Image successfully sent")
    else:
        messagebox.showerror("Error", f"Failed to send image. Status code: {response.status_code}")


def send_user_id(user_id, ip_address, port):
    url = f"http://{ip_address}:{port}/user"
    data = {'user_id': user_id}

    response = requests.post(url, data=data)

    if response.status_code == 200:
        csv_path = 'user_details.csv'
        with open(csv_path, 'wb') as f:
            f.write(response.content)
        messagebox.showinfo("Success", f"CSV saved to {csv_path}")
    else:
        messagebox.showerror("Error", f"Failed to get CSV. Status code: {response.status_code}")


def capture_and_send_image():
    try:
        image_path = capture_image()
        send_image(image_path, ip_address_entry.get(), port_entry.get())
    except Exception as e:
        messagebox.showerror("Error", str(e))


def send_existing_image():
    try:
        image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if image_path:
            send_image(image_path, ip_address_entry.get(), port_entry.get())
    except Exception as e:
        messagebox.showerror("Error", str(e))


def send_user_id_request():
    try:
        user_id = user_id_entry.get()
        if not user_id:
            raise ValueError("User ID cannot be empty")
        send_user_id(user_id, ip_address_entry.get(), port_entry.get())
    except Exception as e:
        messagebox.showerror("Error", str(e))


app = tk.Tk()
app.title("Image and User ID Client App")

# IP Address
tk.Label(app, text="IP Address:").grid(row=0, column=0, padx=10, pady=10)
ip_address_entry = tk.Entry(app)
ip_address_entry.grid(row=0, column=1, padx=10, pady=10)

# Port
tk.Label(app, text="Port:").grid(row=1, column=0, padx=10, pady=10)
port_entry = tk.Entry(app)
port_entry.grid(row=1, column=1, padx=10, pady=10)

# User ID
tk.Label(app, text="User ID:").grid(row=2, column=0, padx=10, pady=10)
user_id_entry = tk.Entry(app)
user_id_entry.grid(row=2, column=1, padx=10, pady=10)

# Capture and Send Image Button
capture_button = tk.Button(app, text="Capture and Send Image", command=capture_and_send_image)
capture_button.grid(row=3, column=0, columnspan=2, pady=10)

# Send Existing Image Button
send_button = tk.Button(app, text="Send Existing Image", command=send_existing_image)
send_button.grid(row=4, column=0, columnspan=2, pady=10)

# Send User ID Button
user_id_button = tk.Button(app, text="Send User ID", command=send_user_id_request)
user_id_button.grid(row=5, column=0, columnspan=2, pady=10)

app.mainloop()
