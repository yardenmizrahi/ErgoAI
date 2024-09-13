from DB.RequestData import RequestData
from utils.RequestQueue import RequestQueue


class Dispatcher:
    def __init__(self):
        self.queue = RequestQueue()

    def queue_request(self, request: RequestData):
        if request.request_type in self.available_actions.keys():
            self.queue.queue_request(request)
            return True
        return False

    def process_request(self):
        pass
