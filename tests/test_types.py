import pytest

import deethon


def test_track():
    assert deethon.Track(95813354).id == 95813354
    with pytest.raises(deethon.errors.DeezerApiError):
        deethon.Track(1234567890)


def test_album():
    assert deethon.Album(103248).id == 103248
    with pytest.raises(deethon.errors.DeezerApiError):
        deethon.Album(1234567890)
