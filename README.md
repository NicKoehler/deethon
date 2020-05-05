# Deethon

Python3 library to easily download music from Deezer

## Quickstart

### Installing

```sh
pip3 install deethon
```

### Initialize

```python
import deethon

deezer = deethon.Deezer("DEEZER ARL TOKEN")
```

### Download tracks

Download track by Deezer link

```python
deezer.download(
    "Deezer track url",
    bitrate="FLAC" # MP3_320 / MP3_256 / MP3_128 (optional)
)
```

## Disclaimer

Deethon - Python3 library to download music from Deezer  
Copyright (C) 2020  Aykut Yilmaz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
