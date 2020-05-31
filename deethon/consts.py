"""
This module contains several constants.
"""

LEGACY_API_URL: str = "https://api.deezer.com/"
"""The url of Deezer's official API server."""

API_URL: str = "http://www.deezer.com/ajax/gw-light.php"
"""The url of Deezer's unofficial API server."""

METHOD_GET_USER: str = "deezer.getUserData"
"""The `deezer.getUserData` method for the Deezer API request."""

METHOD_GET_TRACK: str = "song.getData"
"""The `song.getData` method for the Deezer API request."""
