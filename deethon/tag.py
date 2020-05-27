from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3, Frames

if TYPE_CHECKING:
    from .types import Track


def tag(file_path: Path, track: Track):
    ext = file_path.suffix

    if ext == ".mp3":
        tags = ID3(file_path)

        tags.add(Frames['TALB'](encoding=3, text=track.album.title))
        tags.add(Frames['TBPM'](encoding=3, text=str(track.bpm)))
        tags.add(Frames['TCON'](encoding=3, text=track.album.genres))
        tags.add(Frames['TDAT'](encoding=3,
                                text=track.release_date_four_digits))
        tags.add(Frames['TIT2'](encoding=3, text=track.title))
        tags.add(Frames['TPE1'](encoding=3, text=track.artist))
        tags.add(Frames['TPE2'](encoding=3, text=track.album.artist))
        tags.add(Frames['TPOS'](encoding=3, text=str(track.disk_number)))
        tags.add(Frames['TPUB'](encoding=3, text=track.album.label))
        tags.add(Frames['TRCK'](encoding=3,
                                text=f"{track.number}/{track.album.total_tracks}"))
        tags.add(Frames['TSRC'](encoding=3, text=track.isrc))
        tags.add(Frames['TYER'](encoding=3, text=track.release_year))

        tags.add(Frames['TXXX'](
            encoding=3,
            desc="replaygain_track_peak",
            text=str(track.replaygain_track_peak),
        ))

        tags.add(Frames['APIC'](
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=track.album.cover_xl,
        ))
        tags.save(v2_version=3)

    else:
        tags = FLAC(file_path)
        tags["album"] = track.album.title
        tags["albumartist"] = track.album.artist
        tags["artist"] = track.artist
        tags["bpm"] = str(track.bpm)
        tags["genre"] = track.album.genres
        tags["isrc"] = track.isrc
        tags["replaygain_track_peak"] = str(track.replaygain_track_peak)
        tags["title"] = track.title
        tags["tracknumber"] = str(track.number)

        cover = Picture()
        cover.type = 3
        cover.data = track.album.cover_xl
        cover.width = 1000
        cover.height = 1000
        tags.clear_pictures()
        tags.add_picture(cover)
        tags.save()
