class BaseAppError(Exception):
    def __init__(
        self,
        status_code: int = 500,
        detail: str = "Internal Server Error",
        headers: dict[str, str] | None = None,
    ):
        self.status_code = status_code
        self.detail = detail
        self.headers = headers
