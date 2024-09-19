import sys
from multiprocessing import Process

from flask import Flask, request, jsonify

from DB.CSVDataBase import CSVDatabase
from DB.DBAdapter import DBAdapter
from DB.RequestData import RequestData

app = Flask(__name__)
PORT = 2985
db_adapter = DBAdapter(CSVDatabase())


@app.route('/handle', methods=['POST'])
def process_request():
    data = request.get_json()
    request_data = RequestData(**data)
    print(request_data)
    if db_adapter.queue_request(request_data):
        db_adapter.handle_all_requests()
        response_data = request_data.response
        return jsonify(response_data)
    else:
        return jsonify({'error': 'Invalid request type'}), 400


def run():
    app.run(port=PORT)


def async_run():
    p = Process(target=run)
    p.start()
    return p


def async_stop(p):
    p.terminate()


def stop():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with Werkzeug')
    func()
    return 'Server shutting down...'


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        run()
    PORT = sys.argv[1]
    run()

