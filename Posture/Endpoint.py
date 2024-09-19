import sys
import tomllib

from flask import Flask, request, jsonify

from DB.RequestData import RequestData
from Posture.PostureDetectionAdapter import PostureDetectionAdapter

app = Flask(__name__)
adapter = None
# Initialize the posture detection adapter


@app.route('/handle', methods=['POST'])
def analyze_image():
    try:
        # Parse the incoming JSON request data
        data = request.get_json()

        # Ensure required fields are present in the request
        if not all(key in data for key in ['request_type', 'session_token', 'payload']):
            return jsonify({"error": "Invalid request format"}), 400

        # Extract payload fields
        payload = data.get('payload')
        image_data = payload.get('image_data')

        if not image_data:
            return jsonify({"error": "Image data not found in the request"}), 400

        # Create RequestData object
        req_data = RequestData(
            request_type=data['request_type'],
            session_token=data['session_token'],
            payload=payload
        )

        # Queue and process the request using the adapter
        adapter.queue_request(req_data)
        adapter.handle_all_requests()

        # Return response when processing is done
        return jsonify({"status": "200", "message": "Request received and processed", "result": req_data.response}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 508


class Endpoint:
    def __init__(self, port,):
        global adapter
        with open(sys.argv[2], "rb") as fp:
            config = tomllib.load(fp)
        try:
            adapter = PostureDetectionAdapter(config)
        except Exception as e:
            print(e.with_traceback())
        app.run(port=port)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        Endpoint("2609")
    Endpoint(sys.argv[1])
