"""
The errors module contains all custom error classes
"""


class DeezerApiError(Exception):
    """Raised when a Deezer api request returns an error"""

    def __init__(self, error: str, message: str, code: int):
        self.error: str = error
        self.message: str = message
        self.code: int = code

    def __str__(self) -> str:
        return f"Error {self.code} - {self.message}"


class InvalidUrlError(Exception):
    """Raised when an invalid url is passed"""

    def __init__(self, url: str):
        self.url: str = url

    def __str__(self) -> str:
        return f"{self.url} is not a valid Deezer url"


class ActionNotSupported(Exception):
    """Raised when an invalid action is called"""

    def __init__(self, mode: str):
        self.mode: str = mode

    def __str__(self) -> str:
        return f"Action is not (yet) supported: {self.mode}"
