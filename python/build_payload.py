"""
build_payload.py — full end-to-end verification helper.

Encodes the URL, then immediately decodes it and prints both
so you can confirm round-trip integrity before printing the frame.

Usage:
    python build_payload.py [optional-url]
"""

import sys
import gzip
import base64
import binascii

URL     = "https://vekonymartin.github.io/wedding-surprise/"
XOR_KEY = 0x42


def encode(url: str) -> str:
    d = url.encode()
    d = gzip.compress(d, compresslevel=9)
    d = base64.b64encode(d)
    d = bytes(b ^ XOR_KEY for b in d)
    return binascii.hexlify(d).decode()


def decode(hex_str: str) -> str:
    d = binascii.unhexlify(hex_str)
    d = bytes(b ^ XOR_KEY for b in d)
    d = base64.b64decode(d)
    d = gzip.decompress(d)
    return d.decode()


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else URL

    encoded = encode(url)
    decoded = decode(encoded)

    ok = "✔" if decoded == url else "✘"

    print()
    print("  ── Build Payload ─────────────────────────────────────")
    print(f"  Input URL : {url}")
    print(f"  HEX Payload:\n\n    {encoded}\n")
    print(f"  Round-trip: {ok}  {decoded}")
    print()

    if decoded != url:
        print("  ERROR: round-trip mismatch!")
        sys.exit(1)
