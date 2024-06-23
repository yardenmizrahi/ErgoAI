from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
