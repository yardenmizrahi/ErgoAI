import time
import uuid

from DB.AbstractDB import AbstractDB
from DB.RequestData import RequestData
from utils.RequestQueue import RequestQueue


class DBAdapter:
    def handle_all_requests(self):
        if self.is_idle:
            self.is_idle = False

            while not self.queue.is_empty():
                self.process_request()

            self.is_idle = True

    class inner_db_methods:
        def __init__(self, db: AbstractDB):
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
                keys: str | None = request.payload.get("db_keys", None)

                if table and key:
                    return self.db.get(table, key=key)
                elif table and keys:
                    return self.db.get(table, keys=keys)
                else:
                    return None

    def __init__(self, db: AbstractDB):
        self.queue = RequestQueue()
        self.db_mutex = None
        self.db = DBAdapter.inner_db_methods(db)
        self.available_actions = {"store_db": self.db.store_db, "get_db": self.db.get_db}
        self.is_idle = True

    def queue_request(self, request: RequestData) -> bool:
        if request.request_type in self.available_actions.keys():
            self.queue.queue_request(request)
            return True
        return False

    def process_request(self):
        current_handled_request = self.queue.pop_request()
        current_handled_request.response = (
            self.available_actions[current_handled_request.request_type](current_handled_request))

    def sign_up_new_user(self) -> str:
        """
        Signs up a new user by generating a unique token and storing it in the database.
        Returns the user token.
        """
        user_token = str(uuid.uuid4())  # Generate a unique user token (UUID)
        request_data = RequestData(
            request_type="store_db",
            payload={
                "db_table": "users",
                "db_key": user_token,
                "db_value": {"sign_up_time": time.time()}
            }
        )
        self.queue_request(request_data)
        return user_token

    def validate_user_token(self, user_token: str) -> bool:
        """
        Validates if the provided user token exists in the database.
        Returns True if valid, False otherwise.
        """
        request_data = RequestData(
            request_type="get_db",
            payload={
                "db_table": "users",
                "db_key": user_token
            }
        )
        user = self.queue_request(request_data)
        return user is not None

    def store_user_timed_posture_data(self, user_token: str, posture_data: dict):
        """
        Stores the user's posture data associated with a specific time.
        """
        if self.validate_user_token(user_token):
            timestamp = time.time()  # Current timestamp
            request_data = RequestData(
                request_type="store_db",
                payload={
                    "db_table": "posture_data",
                    "db_key": f"{user_token}_{timestamp}",
                    "db_value": posture_data
                }
            )
            self.queue_request(request_data)
        else:
            raise ValueError("Invalid user token")

    def get_user_posture_data_between_times(self, user_token: str, start_time: float, end_time: float):
        """
        Retrieves the user's posture data between the specified start and end times.
        """
        if self.validate_user_token(user_token):
            # Simulate a request to fetch data between start_time and end_time.
            # This logic assumes we can query a range from the DB, and it's just a placeholder.
            posture_data = []
            for timestamp in range(int(start_time), int(end_time)):
                request_data = RequestData(
                    request_type="get_db",
                    payload={
                        "db_table": "posture_data",
                        "db_key": f"{user_token}_{timestamp}"
                    }
                )
                data = self.db.get_db(request_data)
                if data:
                    posture_data.append(data)
            return posture_data
        else:
            raise ValueError("Invalid user token")
