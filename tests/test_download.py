from pathlib import Path
import deethon


def test_download():
    deezer = deethon.Session('25e67e8e8100407765315a67e0d132fb88a436ffe244813b62ce7086c2efe01b3152041e4308dae45b14f22161adf525ede64cfa18eb9db01b02ec4ccac8869a7e726f372db54c313d4f5705637989ea1e20953a3ea60b5c0179ca95ddfe0516')
    track1 = deezer.download('https://www.deezer.com/track/2104162', 'MP3_320')
    track2 = deezer.download('https://www.deezer.com/track/2104162', 'FLAC')
    assert isinstance(track1, Path)
    assert isinstance(track2, Path)

