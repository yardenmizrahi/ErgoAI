class AbstractDB:
    @staticmethod
    def insert(table: str, key: str, value: str):
        pass

    @staticmethod
    def get(table: str, key: str | None = None, keys: list | None = None) -> dict:
        pass
