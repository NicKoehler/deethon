import re
from pathlib import Path

import requests

from . import exceptions, consts, utils, tag
from .types import Track, Album


class Deezer:
    def __init__(self, arl_token: str):
        self.__arl_token = arl_token
        self.__req = requests.Session()
        self.__req.cookies["arl"] = self.__arl_token
        self.__csrf_token = self._get_api(consts.METHOD_GET_USER)["checkForm"]

    def _get_api(self, method, api_token="null", json=None) -> dict:
        params = {
            "api_version": "1.0",
            "api_token": api_token,
            "input": "3",
            "method": method,
        }
        return self.__req.post(consts.API_URL, params=params,
                               json=json).json()["results"]

    def download(self,
                 url: str,
                 bitrate: str = "FLAC",
                 progress_callback=None):
        match = re.match(
            r"https?://(?:www\.)?deezer\.com/(?:\w+/)?(\w+)/(\d+)", url)
        if match:
            mode = match.group(1)
            content_id = match.group(2)
            if mode == "track":
                return self.download_track(Track(content_id), bitrate,
                                           progress_callback)
            if mode == "album":
                return self.download_album(Album(content_id), bitrate)
            else:
                raise exceptions.ActionNotSupported(mode)
        else:
            raise exceptions.InvalidUrlError(url)

    def download_track(self,
                       track: Track,
                       bitrate: str = "FLAC",
                       progress_callback=None) -> Path:
        json = {"sng_id": track.id}
        track_info = self._get_api(consts.METHOD_GET_TRACK, self.__csrf_token,
                                    json)
        md5 = track_info["MD5_ORIGIN"]

        if "composer" in track_info["SNG_CONTRIBUTORS"]:
            track.add_tags(composer=track_info["SNG_CONTRIBUTORS"]["composer"])
        if "author" in track_info["SNG_CONTRIBUTORS"]:
            track.add_tags(author=track_info["SNG_CONTRIBUTORS"]["author"])

        bitrate = utils.get_quality(bitrate)

        download_url = utils.get_stream_url(md5, bitrate, track.id,
                                            track_info["MEDIA_VERSION"])

        ext = ".flac" if bitrate == "9" else ".mp3"
        file_path = utils.get_file_path(track, ext)
        crypt = self.__req.get(download_url)
        total = crypt.headers["Content-Length"]
        current = 0

        with file_path.open("wb") as f:
            for data in utils.decrypt_file(crypt.iter_content(2048), track.id):
                current += len(data)
                if progress_callback:
                    progress_callback(current, total)
                f.write(data)

        tag.tag(file_path, track)

        return file_path

    def download_album(self, album: Album, bitrate: str):
        return tuple(
            self.download_track(track, bitrate) for track in album.tracks)
