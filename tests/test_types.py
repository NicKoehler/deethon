"""This module contains tests for the types module."""
import pytest

import deethon


def test_track():
    """
    Test if the [Track][deethon.types.Track] class raises a
    [DeezerApiError][deethon.errors.DeezerApiError] when an invalid
    track ID is passed.
    """
    assert deethon.Track(95813354).id == 95813354
    with pytest.raises(deethon.errors.DeezerApiError):
        deethon.Track(1234567890)


def test_album():
    """
    Test if the [Album][deethon.types.Album] class raises a
    [DeezerApiError][deethon.errors.DeezerApiError] when an invalid
    album ID is passed.
    """
    assert deethon.Album(103248).id == 103248
    with pytest.raises(deethon.errors.DeezerApiError):
        deethon.Album(1234567890)
