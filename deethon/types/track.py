import requests
from deethon.types.album import Album
from deethon import exceptions

 
class Track:
    def __init__(self, track_id: (str, int)):
        r = requests.get(f"https://api.deezer.com/track/{track_id}").json()
        if "error" in r:
            raise exceptions.DeezerApiError(r['error']['type'], r['error']['message'], r['error']['code'])
        self.artist = r['artist']['name']
        self.bpm = r['bpm']
        self.disk_number = r['disk_number']
        self.duration = r['duration']
        self.id = r['id']
        self.isrc = r['isrc']
        self.link = r['link']
        self.number = r['track_position']
        self.replaygain_track_peak = r['gain']
        self.release_date = r['release_date']
        self.title = r['title']
        self.title_short = r['title_short']

        ymd_date = self.release_date.split("-")  # 0 YYYY 1 MM 2 DD
        self.release_year = ymd_date[0]
        self.release_date_four_digits = f"{ymd_date[2]}{ymd_date[1]}"

        self.album_id = r['album']["id"]
        self._album = None

    @property
    def album(self) -> Album:
        if self._album:
            return self._album
        else:
            self._album = Album(self.album_id)
            return self._album

    def add_tags(self, **tags):
        for tag in tags:
            setattr(self, tag, tags[tag])
