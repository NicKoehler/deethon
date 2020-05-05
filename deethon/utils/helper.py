from pathlib import Path

def get_quality(bitrate: str) -> str:
    if bitrate == "FLAC":
        return "9"
    elif bitrate == "MP3_320":
        return "3"
    elif bitrate == "MP3_256":
        return "5"
    elif bitrate == "MP3_128":
        return "1"

def get_file_path(track, ext) -> Path:
    std_dir = "Songs/"
    dir_path = Path(f"{std_dir}{track.album.artist}/{track.album.title}")
    dir_path.mkdir(parents=True, exist_ok=True)
    file_name = f"{track.number} - {track.title}{ext}"
    return dir_path / file_name