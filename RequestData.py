from dataclasses import dataclass


@dataclass
class RequestData:
    request_type: str
    session_token: str
    request_data: str

    @staticmethod
    def generate():
        pass
