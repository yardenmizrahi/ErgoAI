from DB.RequestData import RequestData


class RequestQueue:
    def __init__(self):
        self.queue = []

    def queue_request(self, request: RequestData):
        self.queue.append(request)

    def pop_request(self) -> RequestData:
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None

    def is_empty(self):
        return len(self.queue) <= 0
