"""This module contains tests for the [session][deethon.session] module."""
from pathlib import Path

import pytest

import deethon


def test_session():
    """
    Test if the [Session][deethon.session.Session] class raises a
    [DeezerLoginError][deethon.types.DeezerLoginError] when an invalid
    arl token is passed.
    """
    with pytest.raises(deethon.errors.DeezerLoginError):
        deethon.Session('wrongarltoken')


def test_download():
    """Test if the download method returns a Path object."""
    deezer = deethon.Session(
        '25e67e8e8100407765315a67e0d132fb88a436ffe244813b62ce7086c2efe01b3152041e4308dae45b14f22161adf525ede64cfa18eb9db01b02ec4ccac8869a7e726f372db54c313d4f5705637989ea1e20953a3ea60b5c0179ca95ddfe0516')
    assert isinstance(deezer.download('https://www.deezer.com/track/2104162', 'MP3_320'), Path)
    assert isinstance(deezer.download('https://www.deezer.com/track/2104162', 'FLAC'), Path)
