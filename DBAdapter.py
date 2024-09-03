from CSVDataBase import CSVDatabase
from RequestData import RequestData
from RequestQueue import RequestQueue


class DBAdapter:
    def __init__(self):
        self.queue = RequestQueue()
        self.db_mutex = None

    def queue_request(self, request: RequestData):
        self.queue.queue_request(request)

    def process_request(self):
        pass

    def sign_up_new_user(self) -> str:
        pass

    def validate_user_token(self):
        pass

    def store_user_timed_posture_data(self, user_token, posture_data):
        CSVDatabase.insert()

    def get_user_posture_data_between_times(self, user_token, start_time, end_time):
        pass
