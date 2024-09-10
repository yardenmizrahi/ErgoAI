import subprocess

from flask import Flask, render_template, request, send_file, jsonify
import io
import os
import tempfile
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def generate_and_obfuscate_script(server_url, salt):
    # Original Python script with placeholders
    with open("generated_client.py", "r") as fp:
        original_script = fp.read()

    # Replace placeholders with provided parameters
    script_with_values = original_script.replace('>>>SERVER_URL<<<', f'"{server_url}"').replace('>>>SALT<<<',
                                                                                                f'"{salt}"')

    # Create a temporary directory to store the script
    # temp_dir = os.path.join(".", f"temp{salt}")
    # os.makedirs(temp_dir, exist_ok=True)
    #
    # script_path = os.path.join(temp_dir, 'script.py')
    #
    # # Write the modified script to a temporary file
    # with open(script_path, 'w') as script_file:
    #     script_file.write(script_with_values)
    #     os.remove()
    #     os.rmdir(temp_dir)
    return script_with_values  # Return the compiled bytecode


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({"message": "Image received successfully"}), 200


@app.route('/user', methods=['POST'])
def receive_user_id():
    user_id = request.form.get('user_id')
    if not user_id:
        return "No user_id provided", 400

    # Dummy CSV content for demonstration
    csv_content = f"user_id\n{user_id}"
    response = app.response_class(
        response=csv_content,
        mimetype='text/csv'
    )
    response.headers.set("Content-Disposition", "attachment", filename="user_details.csv")
    return response


# Route to serve the HTML form
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle form submission and generate the client
@app.route('/generate_client', methods=['POST'])
def generate_client():
    username = request.form['username']

    # Generate a random salt and the client script
    server_url = 'http://your-server-url.com'  # You can configure the actual server URL here
    salt = os.urandom(16).hex()  # Random salt

    compiled_client = generate_and_obfuscate_script(server_url, salt)

    if compiled_client:
        # Send the compiled client as a downloadable file
        return send_file(
            io.BytesIO(compiled_client.encode("utf-8")),
            as_attachment=True,
            download_name=f'{username}_client.py',
            mimetype='application/octet-stream'
        )
    else:
        return "Failed to generate client", 500


class SessionManager:
    @staticmethod
    def get_session_token():
        return str(uuid.uuid4())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
