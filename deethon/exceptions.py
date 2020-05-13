class DeezerApiError(Exception):
    """ Raised when a Deezer api request returns an error"""
    def __init__(self, error: str, message: str, code: int):
        self.error = error
        self.message = message
        self.code = code

    def __str__(self):
        return f"Error {self.code} - {self.message}"


class InvalidUrlError(Exception):
    """ Raised when an invalid url is passed"""
    def __init__(self, url: str):
        self.url = url

    def __str__(self):
        return f"{self.url} is not a valid Deezer url"


class ActionNotSupported(Exception):
    """ Raised when an invalid action is called"""
    def __init__(self, mode: str):
        self.mode = mode

    def __str__(self):
        return f"Action is not (yet) supported: {self.mode}"
