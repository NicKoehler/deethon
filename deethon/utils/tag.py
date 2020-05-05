import os

from mutagen.flac import FLAC, Picture
from mutagen.id3 import (
    APIC,
    COMM,
    ID3,
    TALB,
    TBPM,
    TCOM,
    TCON,
    TDRC,
    TIT2,
    TPE1,
    TPE2,
    TRCK,
    TSRC,
    TXXX,
    TYER,
    TPOS,
    TPUB,
    TMED,
    TDAT,
    TORY,
    Frames
)


def tag(file_path, track):
    ext = file_path.suffix
    

    if ext == ".mp3":
        tag = ID3()
        
        tag["TIT2"] = Frames['TIT2'](encoding=3, text=track.title)
        tag["TPE1"] = TPE1(encoding=3, text=track.artist)
        tag["TPE2"] = TPE2(encoding=3, text=track.album.artist)
        tag["TALB"] = TALB(encoding=3, text=track.album.title)
        tag["TBPM"] = TBPM(encoding=3, text=str(track.bpm))
        tag["TSRC"] = TSRC(encoding=3, text=track.isrc)
        tag["TRCK"] = TRCK(encoding=3,
                           text=f"{track.number}/{track.album.total_tracks}")
        tag["TORY"] = TORY(encoding=3, text=track.release_year)
        tag["TYER"] = TYER(encoding=3, text=track.release_year)
        tag["TDRC"] = TDRC(encoding=3, text=track.release_date)
        tag["TDAT"] = TDAT(encoding=3, text=track.release_date_four_digits)
        tag["TPOS"] = TPOS(encoding=3, text=str(track.disk_number))
        tag["TPUB"] = TPUB(encoding=3, text=track.album.label)

        tag["TXXX"] = TXXX(
            encoding=3,
            desc="replaygain_track_peak",
            text=str(track.replaygain_track_peak),
        )

        tag["TCON"] = TCON(encoding=3, text=track.album.genres)

        tag["APIC"] = APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=track.album.cover_xl,
        )
        tag.save(file_path)

    else:
        tag = FLAC(file_path)
        tag["title"] = track.title
        tag["artist"] = track.artist
        tag["album"] = track.album.title
        tag["albumartist"] = track.album.artist
        tag["bpm"] = str(track.bpm)
        tag["isrc"] = track.isrc
        tag["tracknumber"] = str(track.number)
        tag["genre"] = track.album.genres
        tag["replaygain_track_peak"] = str(track.replaygain_track_peak)

        images = Picture()
        images.type = 3
        images.data = track.album.cover_xl
        tag.clear_pictures()
        tag.add_picture(images)
        tag.save()
