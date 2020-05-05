from pathlib import Path

import mutagen
import requests

from .types import Track
from .utils.helper import get_quality, get_file_path
from .utils.crypt import *
from .utils.constants import Consts
from .utils.tag import tag

class Deezer:
    def __init__(self, arl_token: str):
        self.arl_token = arl_token
        self.req = requests.Session()
        self.req.cookies["arl"] = self.arl_token
        self.csrf_token = self.__get_api(Consts.METHOD_GET_USER)["checkForm"]

    def __get_api(self, method, api_token="null", json=None):
        params = {
            "api_version": "1.0",
            "api_token": api_token,
            "input": "3",
            "method": method,
        }
        resp = self.req.post(Consts.HIDDEN_API_URL, params=params,
                             json=json).json()["results"]
        return resp

    def download(self, url: str, bitrate: str) -> Path:
        track_id = url.split("/")[-1]
        track = Track(track_id)
        json = {"sng_id": track_id}
        track_info = self.__get_api(Consts.METHOD_GET_DATA, self.csrf_token,
                                    json)

        if "composer" in track_info["SNG_CONTRIBUTORS"].keys():
            track.add_tags(composer=track_info["SNG_CONTRIBUTORS"]["composer"])
        if "author" in track_info["SNG_CONTRIBUTORS"].keys():
            track.add_tags(author=track_info["SNG_CONTRIBUTORS"]["author"])

        quality = get_quality(bitrate)

        ids = track_info["SNG_ID"]
        md5 = track_info["MD5_ORIGIN"]
        download_url = genurl(md5, bitrate, ids, track_info["MEDIA_VERSION"])

        ext = ".flac" if bitrate == "9" else ".mp3"
        file_path = get_file_path(track, ext)

        crypt = self.req.get(download_url)
        decryptfile(crypt.iter_content(2048), calcbfkey(ids), file_path)
        tag(file_path, track)

        return file_path

