"""This module contains the Session class."""
import re
from pathlib import Path
from typing import Union, Generator, Any, Tuple, Optional, Callable

import requests

from . import errors, consts, utils, types


class Session:
    """A session is required to connect to Deezer's unofficial API."""

    def __init__(self, arl_token: str):
        """
        Creates a new Deezer session instance.

        Args:
            arl_token (str): The arl token is used to make API requests
                on Deezers unofficial API

        Raises:
            DeezerLoginError: The specified arl token is not valid.
        """
        self._arl_token: str = arl_token
        self._req = requests.Session()
        self._req.cookies["arl"] = self._arl_token
        user = self.get_api(consts.METHOD_GET_USER)
        if user["USER"]["USER_ID"] == 0:
            raise errors.DeezerLoginError
        self._csrf_token = user["checkForm"]

    def get_api(self, method: str, api_token="null", json=None) -> dict:
        params = {
            "api_version": "1.0",
            "api_token": api_token,
            "input": "3",
            "method": method,
        }
        return self._req.post(consts.API_URL, params=params,
                              json=json).json()["results"]

    def download(self,
                 url: str,
                 bitrate: str = "FLAC",
                 progress_callback: Optional[Callable] = None):
        """
        Downloads the given Deezer url if possible.

        Args:
            url: The URL of the track or album to download.
            bitrate: The preferred bitrate to download
                (`FLAC`, `MP3_320`, `MP3_256`, `MP3_128`).
            progress_callback (callable): A callable that accepts
                `current` and `bytes` arguments.

        Raises:
            ActionNotSupported: The specified URL is not (yet)
                supported for download.
            InvalidUrlError: The specified URL is not a valid deezer link.
        """
        match = re.match(
            r"https?://(?:www\.)?deezer\.com/(?:\w+/)?(\w+)/(\d+)", url)
        if match:
            mode = match.group(1)
            content_id = int(match.group(2))
            if mode == "track":
                return self.download_track(types.Track(content_id), bitrate,
                                           progress_callback)
            if mode == "album":
                return self.download_album(types.Album(content_id), bitrate)
            raise errors.ActionNotSupported(mode)
        raise errors.InvalidUrlError(url)

    def download_track(self,
                       track: types.Track,
                       bitrate: str = "FLAC",
                       progress_callback=None) -> Path:
        """
        Downloads the given [Track][deethon.types.Track] object.

        Args:
            track: A [Track][deethon.types.Track] instance.
            bitrate: The preferred bitrate to download
                (`FLAC`, `MP3_320`, `MP3_256`, `MP3_128`).
            progress_callback: A callable that accepts
                `current` and `bytes` arguments.

        Returns:
            The file path of the downloaded track.
        """
        track.add_more_tags(self)
        bitrate = utils.get_quality(bitrate)
        download_url = utils.get_stream_url(track, bitrate)

        ext = ".flac" if bitrate == "9" else ".mp3"
        file_path = utils.get_file_path(track, ext)
        crypt = self._req.get(download_url, stream=True)
        total = int(crypt.headers["Content-Length"])
        current = 0

        with file_path.open("wb") as f:
            for data in utils.decrypt_file(crypt.iter_content(2048), track.id):
                current += len(data)
                f.write(data)
                if progress_callback:
                    progress_callback(current, total)

        utils.tag(file_path, track)

        return file_path

    def download_album(
            self,
            album: types.Album,
            bitrate: str = None,
            stream: bool = False
    ) -> Union[Generator[Path, Any, None], Tuple[Path, ...]]:
        """
        Downloads an album from Deezer using the specified Album object.

        Args:
            album: An [Album][deethon.types.Album] instance.
            bitrate: The preferred bitrate to download
                (`FLAC`, `MP3_320`, `MP3_256`, `MP3_128`).
            stream: If `true`, this method returns a generator object,
                otherwise the downloaded files are returned as a tuple
                that contains the file paths.

        Returns:
            The file paths.
        """
        tracks = (self.download_track(track, bitrate)
                  for track in album.tracks)
        if stream:
            return tracks
        return tuple(tracks)

    @property
    def csrf_token(self):
        return self._csrf_token
