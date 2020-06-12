"""The errors module contains all custom error classes"""


class DeezerLoginError(Exception):
    """Occurs when login to Deezer fails."""

    def __init__(self):
        super().__init__("Failed to login to Deezer. Please check your arl token.")


class DeezerApiError(Exception):
    """Occurs when a Deezer API request replies with an error."""

    def __init__(self, error: str, message: str, code: int):
        self.error: str = error
        self.code: int = code
        self.message: str = message
        super().__init__(f"Error {code}: {error} - {message}")


class InvalidUrlError(Exception):
    """Occurs when an invalid URL is passed."""

    def __init__(self, url: str):
        self.url: str = url
        super().__init__(f'"{url}" is not a valid Deezer url.')


class ActionNotSupported(Exception):
    """Occurs when an invalid action is called."""

    def __init__(self, mode: str):
        self.mode: str = mode
        super().__init__(f"Action is not (yet) supported: {self.mode}")


class DownloadError(Exception):
    """Occurs when a track cannot be downloaded."""

    def __init__(self, track_id: int):
        self.track_id: int = track_id
        super().__init__(f"Track {self.track_id} is not downloadable.")
