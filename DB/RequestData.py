from dataclasses import dataclass


class RequestTypes():
    store_db = "store_db",
    get_db = "get_db",
    analyze = "analyze"

    @staticmethod
    def get_types():
        return [i for i in RequestTypes.__dict__.keys() if "__" not in i]


@dataclass
class RequestData:
    request_type: str
    session_token: str
    payload: dict
    response: dict = None


def generate(type: str, session_token: str, payload: dict) -> RequestData | None:
    if type not in RequestTypes.get_types():
        return None

    return RequestData(request_type=type, payload=payload, session_token=session_token)
