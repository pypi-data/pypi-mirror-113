from typing import Any, TypedDict

class Client:
    def flush(self) -> None: ...

class Response(TypedDict):
    status_code: int
    duration: int
    metadata: Any
    body: str
    error: str
