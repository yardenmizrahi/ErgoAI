from RequestData import RequestData


class RequestQueue:
    def __init__(self):
        self.queue = []

    def queue_request(self, request: RequestData):
        self.queue.append(request)

    def pop_request(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None
