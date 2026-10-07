"""Decrypt Cisco Packet Tracer .pkt/.pka files (PT 7.x/8.x) to XML.
Scheme (as in the public pka2xml project, include/pka2xml.hpp): reversed XOR stage -> Twofish-EAX decrypt -> XOR stage -> zlib (4-byte BE length prefix).
Usage: python3 -I pktdecrypt.py in.pkt out.xml

Dependency: the "twofish" package from PyPI (C extension around Niels Ferguson's Twofish).
  pip install twofish      # on Python 3.12+ its twofish.py still does "import imp"; replace the
                           # imp.find_module(...) line with a glob for the _twofish*.so next to it,
                           # or build the sdist in a venv and copy twofish.py plus _twofish*.so beside this file.
Both HelpYou .pkt files (Packet Tracer 8.2.1) decrypt with this scheme and the EAX tag verifies.
"""
import sys, zlib, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from twofish import Twofish

KEY = bytes([0x89] * 16)   # all bytes 137
IV  = bytes([0x10] * 16)   # all bytes 16

def _xor(a, b): return bytes(x ^ y for x, y in zip(a, b))
def _dbl(b):
    n = int.from_bytes(b, 'big') << 1
    if n >> 128: n = (n & ((1 << 128) - 1)) ^ 0x87
    return n.to_bytes(16, 'big')

class EAX:
    def __init__(self, key):
        self.tf = Twofish(key)
        L = self.tf.encrypt(bytes(16))
        self.K1 = _dbl(L); self.K2 = _dbl(self.K1)
    def cmac(self, msg):
        if len(msg) % 16 == 0 and len(msg) > 0:
            blocks = [msg[i:i+16] for i in range(0, len(msg), 16)]
            blocks[-1] = _xor(blocks[-1], self.K1)
        else:
            pad = msg + b'\x80' + bytes(15 - (len(msg) % 16))
            blocks = [pad[i:i+16] for i in range(0, len(pad), 16)]
            blocks[-1] = _xor(blocks[-1], self.K2)
        x = bytes(16)
        for b in blocks: x = self.tf.encrypt(_xor(x, b))
        return x
    def omac(self, t, msg): return self.cmac(bytes(15) + bytes([t]) + msg)
    def decrypt(self, nonce, ct, header=b''):
        N = self.omac(0, nonce); H = self.omac(1, header)
        C, tag = ct[:-16], ct[-16:]
        ctr = int.from_bytes(N, 'big'); out = bytearray()
        for i in range(0, len(C), 16):
            ks = self.tf.encrypt(((ctr + i // 16) & ((1 << 128) - 1)).to_bytes(16, 'big'))
            out += _xor(C[i:i+16], ks)
        tag_ok = _xor(_xor(N, self.omac(2, C)), H) == tag
        return bytes(out), tag_ok

def stage1(data):
    # processed[i] = input[length - 1 - i] ^ (length - i*length)   (input is read in reverse)
    n = len(data); return bytes((data[n - 1 - i] ^ ((n - i*n) & 0xFF)) for i in range(n))
def stage3(data):
    n = len(data); return bytes((b ^ ((n - i) & 0xFF)) for i, b in enumerate(data))

def decrypt(raw):
    d = stage1(raw)
    d, tag_ok = EAX(KEY).decrypt(IV, d)
    d = stage3(d)
    expected = int.from_bytes(d[:4], 'big')
    xml = zlib.decompress(d[4:])
    return xml, tag_ok, expected

if __name__ == '__main__':
    raw = open(sys.argv[1], 'rb').read()
    xml, tag_ok, expected = decrypt(raw)
    print(f'decrypted: {len(xml)} bytes (header said {expected}); EAX tag verified: {tag_ok}')
    open(sys.argv[2], 'wb').write(xml)
