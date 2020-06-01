"""This module contains all available type classes."""
from __future__ import annotations

from datetime import datetime
from typing import Union, TYPE_CHECKING, Optional

import requests

from . import consts, errors

if TYPE_CHECKING:
    from .session import Session


class Album:
    """The Album class contains several information about an album."""
    _cache = {}

    def __new__(cls, album_id: Union[int, str]):
        """
        If an album instance with the specified album ID already exists,
        this method returns the cached instance, otherwise a new album
        instance is created.

        Args:
            album_id (Union[int, str]): The Deezer album ID.
        """
        if album_id in cls._cache.keys():
            return cls._cache[album_id]
        _album = super(Album, cls).__new__(cls)
        cls._cache[album_id] = _album
        return _album

    def __init__(self, album_id: Union[int, str]):
        """
        Create a new album instance with the specified album ID.

        Args:
            album_id (Union[int, str]): The Deezer album ID.

        Raises:
            DeezerApiError: The Deezer API request replied with an error.
        """
        r = requests.get(
            f"https://api.deezer.com/album/{album_id}").json()
        if "error" in r:
            raise errors.DeezerApiError(r['error']['type'],
                                        r['error']['message'],
                                        r['error']['code'])

        self.artist: str = r["artist"]["name"]
        """The main artist of the album."""

        self.basic_tracks_data: list = r["tracks"]["data"]
        """A list that contains basic tracks data."""

        self.cover_small_link: str = r["cover_small"]
        """The link for the album cover in small size."""

        self.cover_medium_link: str = r["cover_medium"]
        """The link for the album cover in medium size"""

        self.cover_big_link: str = r["cover_big"]
        """The link for the album cover in big size"""

        self.cover_xl_link: str = r["cover_xl"]
        """The link for the album cover in xl size"""

        self.duration: int = r["duration"]
        """The duration in seconds of the album."""

        self.genres: list = [genre["name"] for genre in r["genres"]["data"]]
        """A list of genres of the album."""

        self.id: int = r["id"]
        """The ID of the album."""

        self.label: str = r["label"]
        """The label of the album."""

        self.link: str = r["link"]
        """The Deezer link of the album."""

        self.record_type: str = r["record_type"]
        """The record type of the album."""

        date = r["release_date"]
        self.release_date: datetime = datetime.strptime(date, '%Y-%m-%d')
        """The release date of the album."""

        self.title: str = r["title"]
        """The title of the album."""

        self.total_tracks: int = r["nb_tracks"]
        """The total number of tracks in the album."""

        self.upc: str = r["upc"]
        """The Universal Product Code (UPC) of the album."""

        self._cover_small = None
        self._cover_medium = None
        self._cover_big = None
        self._cover_xl = None

    @property
    def cover_small(self) -> bytes:
        """The album cover in small size"""
        if self._cover_small:
            return self._cover_small
        self._cover_small = requests.get(self.cover_small_link).content
        return self._cover_small

    @property
    def cover_medium(self) -> bytes:
        """The album cover in medium size"""
        if self._cover_medium:
            return self._cover_medium
        self._cover_medium = requests.get(self.cover_medium_link).content
        return self._cover_medium

    @property
    def cover_big(self) -> bytes:
        """The album cover in big size"""
        if self._cover_big:
            return self._cover_big
        self._cover_big = requests.get(self.cover_big_link).content
        return self._cover_big

    @property
    def cover_xl(self) -> bytes:
        """The album cover in xl size"""
        if self._cover_xl:
            return self._cover_xl
        self._cover_xl = requests.get(self.cover_xl_link).content
        return self._cover_xl

    @property
    def tracks(self) -> list:
        """A list of [Track][deethon.types.Track] objects for each
        track in the album.
        """
        return [Track(x["id"]) for x in self.basic_tracks_data]


class Track:
    """
    The Track class contains several information about a track.
    """
    _cache = {}

    def __new__(cls, track_id: Union[int, str]):
        """
        If a track instance with the specified track ID already exists,
        this method returns the cached instance, otherwise a new track
        instance is created and cached.

        Args:
            track_id (Union[int, str]): The Deezer album ID.
        """
        track_id = int(track_id)

        if track_id in cls._cache.keys():
            return cls._cache[track_id]
        track = super(Track, cls).__new__(cls)
        cls._cache[track_id] = track
        return track

    def __init__(self, track_id: Union[int, str]):
        """
        Create a new track instance with the specified track ID.

        Args:
            track_id (Union[int, str]): The Deezer track ID.

        Raises:
            DeezerApiError: The Deezer API request replied with an error.
        """
        r = requests.get(f"https://api.deezer.com/track/{track_id}").json()
        if "error" in r:
            raise errors.DeezerApiError(r['error']['type'],
                                        r['error']['message'],
                                        r['error']['code'])
        self.artist: str = r['artist']['name']
        """The main artist of the track."""

        self.bpm: int = r['bpm']
        """Beats per minute of the track."""

        self.disk_number: int = r['disk_number']
        """The disc number of the track."""

        self.duration: int = r['duration']
        """The duration of the track."""

        self.id: int = r['id']
        """The Deezer ID of the track."""

        self.isrc: str = r['isrc']
        """The International Standard Recording Code (ISRC) of the track."""

        self.link: str = r['link']
        """The Deezer link of the track."""

        self.number: int = r['track_position']
        """The position of the track."""

        self.replaygain_track_peak: int = r['gain']
        """The Replay Gain value of the track."""

        date: str = r["release_date"]
        self.release_date: datetime = datetime.strptime(date, '%Y-%m-%d')
        """The release date of the track."""

        self.title: str = r['title']
        """The title of the track."""

        self.title_short: str = r['title_short']
        """The short title of the track."""

        self.album_id = r['album']["id"]
        """The Deezer album ID to which the track belongs."""

        self.md5_origin: Optional[str] = None
        """
        The md5 origin of the track.

        Warning:
            This attribute is only set after
            [add_more_tags()][deethon.types.Track.add_more_tags] is
            called. Defaults to `None`.
        """
        self.media_version: Optional[str] = None
        """
        The media version of the track.

        Warning:
            This attribute is only set after
            [add_more_tags()][deethon.types.Track.add_more_tags] is
            called. Defaults to `None`.
        """
        self.composer: Optional[str] = None
        """
        The author of the track.

        Warning:
            This attribute is only set after
            [add_more_tags()][deethon.types.Track.add_more_tags] is
            called. Defaults to `None`.
        """
        self.author: Optional[str] = None
        """
        The author of the track.

        Warning:
            This attribute is only set after
            [add_more_tags()][deethon.types.Track.add_more_tags] is
            called. Defaults to `None`.
        """

    @property
    def album(self) -> Album:
        """Return an Album instance."""
        return Album(self.album_id)

    def add_more_tags(self, session: Session) -> None:
        """
        Adds more tags using Deezer's unofficial API.

        Args:
            session: A deethon.Session object is required to connect
                to the Deezer API.
        """
        track_info = session.get_api(consts.METHOD_GET_TRACK, session.csrf_token,
                                     {"sng_id": self.id})
        self.md5_origin = track_info["MD5_ORIGIN"]
        self.media_version = track_info["MEDIA_VERSION"]

        if "composer" in track_info["SNG_CONTRIBUTORS"]:
            self.composer = track_info["SNG_CONTRIBUTORS"]["composer"]
        if "author" in track_info["SNG_CONTRIBUTORS"]:
            self.author = track_info["SNG_CONTRIBUTORS"]["author"]
