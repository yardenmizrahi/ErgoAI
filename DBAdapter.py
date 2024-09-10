from AbstractDB import AbstractDB
from RequestData import RequestData
from RequestQueue import RequestQueue


class DBAdapter:
    class inner_db_methods:
        def __init__(self, db):
            self.db = db

        def store_db(self, request: RequestData):
            if self.db:
                table: str | None = request.payload.get("db_table", None)
                key: str | None = request.payload.get("db_key", None)
                value: str | None = request.payload.get("db_value", None)

                if table and key:
                    return self.db.insert(table, key, value)
                else:
                    return None

        def get_db(self, request: RequestData):
            if self.db:
                table: str | None = request.payload.get("db_table", None)
                key: str | None = request.payload.get("db_key", None)

                if table and key:
                    return self.db.get(table, key)
                else:
                    return None

    def __init__(self, db: AbstractDB):
        self.queue = RequestQueue()
        self.db_mutex = None
        self.db = DBAdapter.inner_db_methods(db)
        self.available_actions = {"store_db": self.db.store_db, "get_db": self.db.get_db}

    def queue_request(self, request: RequestData) -> bool:
        if request.request_type in self.available_actions.keys():
            self.queue.queue_request(request)
            return True
        return False

    def process_request(self):
        current_handled_request = self.queue.pop_request()
        self.available_actions[current_handled_request.request_type](current_handled_request)

    def sign_up_new_user(self) -> str:
        pass

    def validate_user_token(self):
        pass

    def store_user_timed_posture_data(self, user_token, posture_data):
        self.db.insert()

    def get_user_posture_data_between_times(self, user_token, start_time, end_time):
        pass
