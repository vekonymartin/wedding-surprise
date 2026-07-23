"""
encrypt.py — Generate the obfuscated HEX payload from a URL.

Pipeline:  url  →  gzip  →  base64  →  XOR(0x42)  →  hex

Edit only the URL below, then run:
    python encrypt.py
"""

import sys
import gzip
import base64
import binascii

# ── Change this to your GitHub Pages URL ─────────────────────────────────────
URL = "https://vekonymartin.github.io/wedding-surprise/"
# ─────────────────────────────────────────────────────────────────────────────

_XOR_KEY = 0x42


def encode(url: str) -> str:
    data = url.encode("utf-8")
    data = gzip.compress(data, compresslevel=9)
    data = base64.b64encode(data)
    data = bytes(b ^ _XOR_KEY for b in data)
    return binascii.hexlify(data).decode("ascii")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else URL
    hex_payload = encode(target)

    print()
    print("  ╔══════════════════════════════════════════╗")
    print("  ║         Generated HEX payload            ║")
    print("  ╚══════════════════════════════════════════╝")
    print()
    print(f"  URL:  {target}")
    print()
    print("  Paste the value below into wedding.py → PAYLOAD")
    print()
    print(f"  {hex_payload}")
    print()
