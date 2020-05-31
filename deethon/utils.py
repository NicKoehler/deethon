"""
The utils module contains several useful functions that are used within the package.
"""

from __future__ import annotations

import hashlib
from binascii import a2b_hex, b2a_hex
from pathlib import Path
from typing import Iterator, TYPE_CHECKING, Generator, Any

from Crypto.Cipher import AES, Blowfish
from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3, Frames

if TYPE_CHECKING:
    from .types import Track


def md5hex(data: bytes) -> bytes:
    return hashlib.md5(data).hexdigest().encode()


def get_quality(bitrate: str) -> str:
    if bitrate == "FLAC":
        return "9"
    elif bitrate == "MP3_320":
        return "3"
    elif bitrate == "MP3_256":
        return "5"
    elif bitrate == "MP3_128":
        return "1"


def get_file_path(track: Track, ext) -> Path:
    std_dir = "Songs/"
    dir_path = Path(f"{std_dir}{track.album.artist}/{track.album.title}")
    dir_path.mkdir(parents=True, exist_ok=True)
    file_name = f"{track.number} - {track.title}{ext}"
    return dir_path / file_name


def get_stream_url(track: Track, quality: str) -> str:
    """
    Get the direct download url for the encrypted track.

    Args:
        track: A [Track][deethon.types.Track] instance.
        quality: The preferred quality.

    Returns:
        The direct download url.
    """
    data = b"\xa4".join(
        a.encode()
        for a in [track.md5_origin, quality, str(track.id),
                  str(track.media_version)])
    data = b"\xa4".join([md5hex(data), data]) + b"\xa4"
    if len(data) % 16:
        data += b"\x00" * (16 - len(data) % 16)
    c = AES.new("jo6aey6haid2Teih".encode(), AES.MODE_ECB)
    hashs = b2a_hex(c.encrypt(data)).decode()
    return f"https://e-cdns-proxy-{track.md5_origin[0]}.dzcdn.net/mobile/1/{hashs}"


def decrypt_file(input_data: Iterator, track_id: int) -> Generator[bytes, Any, None]:
    """
    Decrypt an encrypted track.

    Args:
        input_data: The input stream must have a chunk size of 2048.
        track_id: The id of the track to be decrypted.

    Returns:
        A Generator object containing the decrypted data
    """
    h = md5hex(str(track_id).encode())
    key = "".join(
        chr(h[i] ^ h[i + 16] ^ b"g4el58wc0zvf9na1"[i]) for i in range(16))
    seg = 0
    for data in input_data:
        if not data:
            break
        if (seg % 3) == 0 and len(data) == 2048:
            data = Blowfish.new(key.encode(), Blowfish.MODE_CBC,
                                a2b_hex("0001020304050607")).decrypt(data)
        seg += 1
        yield data


def tag(file_path: Path, track: Track) -> None:
    """
    Tag the music file at the given file path using the specified
    [Track][deethon.types.Track] instance.

    Args:
        file_path (Path): The music file to be tagged
        track: The [Track][deethon.types.Track] instance to be used for tagging.
    """
    ext = file_path.suffix

    if ext == ".mp3":
        tags = ID3()

        tags.add(Frames['TALB'](encoding=3, text=track.album.title))
        tags.add(Frames['TBPM'](encoding=3, text=str(track.bpm)))
        tags.add(Frames['TCON'](encoding=3, text=track.album.genres))
        tags.add(Frames['TDAT'](encoding=3,
                                text=track.release_date.strftime('%d%m')))
        tags.add(Frames['TIT2'](encoding=3, text=track.title))
        tags.add(Frames['TPE1'](encoding=3, text=track.artist))
        tags.add(Frames['TPE2'](encoding=3, text=track.album.artist))
        tags.add(Frames['TPOS'](encoding=3, text=str(track.disk_number)))
        tags.add(Frames['TPUB'](encoding=3, text=track.album.label))
        tags.add(Frames['TRCK'](encoding=3,
                                text=f"{track.number}/{track.album.total_tracks}"))
        tags.add(Frames['TSRC'](encoding=3, text=track.isrc))
        tags.add(Frames['TYER'](encoding=3, text=str(track.release_date.year)))

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
        tags.save(file_path, v2_version=3)

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