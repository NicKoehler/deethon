import re
from pathlib import Path

import requests

from . import exceptions, consts, utils, tag
from .types import Track


class Deezer:
    def __init__(self, arl_token: str):
        self.arl_token = arl_token
        self.req = requests.Session()
        self.req.cookies["arl"] = self.arl_token
        self.csrf_token = self.__get_api(consts.METHOD_GET_USER)["checkForm"]

    def __get_api(self, method, api_token="null", json=None) -> dict:
        params = {
            "api_version": "1.0",
            "api_token": api_token,
            "input": "3",
            "method": method,
        }
        return self.req.post(consts.API_URL, params=params,
                             json=json).json()["results"]

    def download(self, url: str, bitrate: str):
        match = re.match(r"https?://(?:www\.)?deezer\.com/(?:\w+/)?(\w+)/(\d+)", url)
        if match:
            mode = match.group(1)
            content_id = match.group(2)
            if mode == "track":
                return self.download_track(Track(content_id), bitrate)
            else:
                raise exceptions.ActionNotSupported(mode)
        else:
            raise exceptions.InvalidUrlError(url)

    def download_track(self, track: Track, bitrate: str) -> Path:
        json = {"sng_id": track.id}
        track_info = self.__get_api(consts.METHOD_GET_TRACK, self.csrf_token,
                                    json)

        md5 = track_info["MD5_ORIGIN"]

        if "composer" in track_info["SNG_CONTRIBUTORS"]:
            track.add_tags(composer=track_info["SNG_CONTRIBUTORS"]["composer"])
        if "author" in track_info["SNG_CONTRIBUTORS"]:
            track.add_tags(author=track_info["SNG_CONTRIBUTORS"]["author"])

        bitrate = utils.get_quality(bitrate)

        download_url = utils.get_stream_url(md5, bitrate, track.id, track_info["MEDIA_VERSION"])

        ext = ".flac" if bitrate == "9" else ".mp3"
        file_path = utils.get_file_path(track, ext)

        crypt = self.req.get(download_url)
        utils.decrypt_file(crypt.iter_content(2048), track.id, file_path)
        tag.tag(file_path, track)

        return file_path
