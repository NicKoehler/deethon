Deethon
=======
Python3 library to easily download music from `Deezer`_.

Quickstart
----------
Installing
^^^^^^^^^^
.. code-block:: sh

    pip3 install deethon

Initialize
^^^^^^^^^^
.. code-block:: python

    import deethon

    deezer = deethon.Session("DEEZER ARL TOKEN")

Download tracks
^^^^^^^^^^^^^^^
Download track by Deezer link

.. code-block:: python

    deezer.download(
        "Deezer track url",
        bitrate="FLAC" # MP3_320 / MP3_256 / MP3_128 (optional)
    )

Disclaimer
----------
| Deethon - Python3 library to download music from Deezer
| Copyright (C) 2020  Aykut Yilmaz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/.

Do not use this package illegaly and against Deezer's `Terms Of Use`_.

.. _Deezer: https://www.deezer.com
.. _Terms Of Use: https://www.deezer.com/legal/cgu/