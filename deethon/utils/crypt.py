import hashlib
from binascii import a2b_hex, b2a_hex

from Crypto.Cipher import AES, Blowfish

from .constants import Consts


def md5hex(data):
    hashed = hashlib.md5(data).hexdigest().encode()
    return hashed


def genurl(md5, quality, track_id: int, media) -> str:
    data = b"\xa4".join(a.encode() for a in [md5, quality, str(track_id), str(media)])
    data = b"\xa4".join([md5hex(data), data]) + b"\xa4"
    if len(data) % 16:
        data += b"\x00" * (16 - len(data) % 16)
    c = AES.new("jo6aey6haid2Teih".encode(), AES.MODE_ECB)
    hashs = b2a_hex(c.encrypt(data)).decode()
    return Consts.DOWNLOAD_URL.format(md5[0], hashs)


def blowfishDecrypt(data, key):
    c = Blowfish.new(key.encode(), Blowfish.MODE_CBC,
                     a2b_hex("0001020304050607"))
    return c.decrypt(data)


def decryptfile(fh, key, file_path):
    seg = 0
    with file_path.open("wb") as f:
        for data in fh:
            if not data:
                break
            if (seg % 3) == 0 and len(data) == 2048:
                data = blowfishDecrypt(data, key)
            f.write(data)
            seg += 1


def calcbfkey(songid):
    h = md5hex(b"%d" % int(songid))
    key = b"g4el58wc0zvf9na1"
    return "".join(chr(h[i] ^ h[i + 16] ^ key[i]) for i in range(16))
