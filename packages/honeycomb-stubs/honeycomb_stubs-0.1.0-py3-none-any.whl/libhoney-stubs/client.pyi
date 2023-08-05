from typing import Any, TypedDict

class Client: ...

class Response(TypedDict):
    status_code: int
    duration: int
    metadata: Any
    body: str
    error: str
