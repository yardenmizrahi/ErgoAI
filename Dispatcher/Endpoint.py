import hashlib
import sys
import io
import os
import socket
import uuid
import tomllib
import json
from flask import Flask, render_template, request, send_file, jsonify
from Dispatcher.Dispatcher import Dispatcher
from DB.RequestData import RequestData


app = Flask(__name__)
dispatcher: Dispatcher = None
USERS_FILE = os.path.join("tbls", 'usernames.json')


def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()


def generate_and_obfuscate_script(server_url, salt):
    with open("generated_client.py", "r") as fp:
        original_script = fp.read()
    script_with_values = original_script.replace('>>>SERVER_URL<<<', f'"{server_url}"').replace('>>>SALT<<<',
                                                                                                f'"{salt}"')
    return script_with_values


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(USERS_FILE, 'w+') as f:
        json.dump(users, f)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_client', methods=['POST'])
def generate_client():
    username = request.form['username']
    password = request.form['password']

    server_url = f"http://{socket.gethostbyname(socket.gethostname())}:{sys.argv[1]}"

    compiled_client = None

    users = load_users()

    # Authentication logic
    if username in users:
        # User exists, check password
        if users[username] != password:
            return jsonify({"error": "Invalid password"}), 403
    else:
        salt = os.urandom(16).hex()
        compiled_client = generate_and_obfuscate_script(server_url, salt)
        users[username] = hash_password(password, salt)
        save_users(users)

    if compiled_client:
        return send_file(
            io.BytesIO(compiled_client.encode("utf-8")),
            as_attachment=True,
            download_name=f'{username}_client.py',
            mimetype='application/octet-stream'
        )
    else:
        return "Failed to generate client", 500


@app.route('/handle', methods=['POST'])
def enqueue_request():
    try:
        data = request.get_json()

        if not all(key in data for key in ['request_type', 'session_token', 'payload']):
            return jsonify({"error": "Invalid request format"}), 400

        # Extract username and password from payload
        if 'payload' not in data or not isinstance(data['payload'], dict):
            return jsonify({"error": "Invalid payload format"}), 400

        payload = data['payload']
        if 'username' not in payload or 'password' not in payload:
            return jsonify({"error": "Username and password required"}), 400

        username = payload['username']
        password = payload['password']

        # Load existing users
        users = load_users()

        # Authentication logic
        if username in users:
            # User exists, check password
            if users[username] != password:
                return jsonify({"error": "Invalid password"}), 403
        else:
            # New user, save credentials
            print("new user")
            users[username] = password
            save_users(users)

        # Create RequestData object
        req_data = RequestData(
            request_type=data['request_type'],
            session_token=data['session_token'],
            payload=data['payload']
        )

        # Queue the request
        if dispatcher.queue_request(req_data):
            dispatcher.handle_all_requests()
            if data["request_type"] == "get_db":
                timeout = 99
                while req_data.response is None and timeout > 0:
                    print(req_data.response)
                    timeout -= 1
                return jsonify(req_data.response), 200
            return jsonify({"status": "200", "message": "Request queued successfully"}), 200
        else:
            return jsonify({"error": "Request type not recognized"}), 400

    except Exception as e:
        print(e.with_traceback())
        return jsonify({"error": str(e)}), 500


def main():
    global dispatcher
    global app
    with open(sys.argv[2], "rb") as fp:
        config = tomllib.load(fp)
    try:
        dispatcher = Dispatcher(config)
    except Exception as e:
        print(e.with_traceback())
    app.run(port=int(sys.argv[1]), host="0.0.0.0")


if __name__ == '__main__':
    if len(sys.argv) > 2:
        main()
