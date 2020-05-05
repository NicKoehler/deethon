import requests


class Album:
    def __init__(self, album_id):
        r = requests.get(f"https://api.deezer.com/album/{album_id}").json()
        self.id = r["id"]
        self.title = r["title"]
        self.artist = r["artist"]["name"]
        self.upc = r["upc"]
        self.link = r["link"]
        self.record_type = r["record_type"]
        self.release_date = r["release_date"]
        self.total_tracks = r["nb_tracks"]
        genres_list = []
        for genre in r["genres"]["data"]:
            genres_list.append(genre["name"])
        self.genres = genres_list
        self.genre = genres_list[0]
        self.label = r["label"]
        self._cover_xl = None
        self.cover_xl_url = r["cover_xl"]

    @property
    def cover_xl(self):
        if self._cover_xl is None:
            self._cover_xl = requests.get(self.cover_xl_url).content
        return self._cover_xl
