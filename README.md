# Deethon
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/3a54b30586b941acb82079d0252e0320)](https://www.codacy.com/gh/deethon/deethon?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=deethon/deethon&amp;utm_campaign=Badge_Grade)
[![PyPI](https://img.shields.io/pypi/v/deethon)](https://pypi.org/project/deethon/)
![PyPI - Status](https://img.shields.io/pypi/status/deethon)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/deethon)](https://pypi.org/project/deethon/)
[![GitHub license](https://img.shields.io/github/license/deethon/deethon)](https://github.com/deethon/deethon/blob/master/LICENSE)

Deethon is a lightweight Python library for downloading high quality music from Deezer.

## Gettings started

### Installation

```sh
pip install deethon
```

### Usage

```python
import deethon

deezer = deethon.Session("YOUR ARL TOKEN")

deezer.download(
    "https://www.deezer.com/track/1234567",
    bitrate="FLAC" # or MP3_320 / MP3_256 / MP3_128 (optional)
)
```
