import sys
import tomllib
from flask import Flask, request, jsonify
from Dispatcher.Dispatcher import Dispatcher
from DB.RequestData import RequestData


app = Flask(__name__)
dispatcher: Dispatcher = None


@app.route('/handle', methods=['POST'])
def enqueue_request():
    try:
        # Parse JSON request
        data = request.get_json()

        # Ensure required fields are present
        if not all(key in data for key in ['request_type', 'session_token', 'payload']):
            return jsonify({"error": "Invalid request format"}), 400

        # Create RequestData object
        req_data = RequestData(
            request_type=data['request_type'],
            session_token=data['session_token'],
            payload=data['payload']
        )

        # Queue the request
        if dispatcher.queue_request(req_data):
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
    app.run(port=int(sys.argv[1]))


if __name__ == '__main__':
    if len(sys.argv) > 2:
        main()
