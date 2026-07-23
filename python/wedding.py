"""
# Nothing interesting here.
# Just a simple QR generator.
"""

import sys
import time
import gzip
import base64
import binascii
import qrcode
from PIL import Image

# ── payload (hex-encoded, XOR-obfuscated, base64-gzip of the target URL) ─────
PAYLOAD = (
    "0a76310b030f3a2d1b2f2d016d7a312d0911292d36360e1a0e72340c383169303807"
    "723109312c0f727234120e0f292d16260e0e380c2134167273083b213a0e733b72370e"
    "112d2d3b2b3a0d731321037731307a3a2803030303037f"
)

_XOR_KEY = 0x42


# ─────────────────────────────────────────────────────────────────────────────
def true_love(payload: str) -> str:
    """Decode the hidden message — reverse of: url → gzip → b64 → XOR → hex."""
    raw   = binascii.unhexlify(payload)
    xored = bytes(b ^ _XOR_KEY for b in raw)
    b64d  = base64.b64decode(xored)
    url   = gzip.decompress(b64d).decode("utf-8")
    return url


# ─────────────────────────────────────────────────────────────────────────────
def _bar(label: str, duration: float = 1.8, steps: int = 40) -> None:
    """Print an animated progress bar in the terminal."""
    delay = duration / steps
    sys.stdout.write(f"\n  {label}\n  [")
    sys.stdout.flush()
    for i in range(steps):
        time.sleep(delay)
        sys.stdout.write("█")
        sys.stdout.flush()
    sys.stdout.write("] 100%\n")
    sys.stdout.flush()


def _typed(text: str, delay: float = 0.03) -> None:
    """Print text character by character, like a typewriter."""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()


def _section(text: str) -> None:
    colour_green = "\033[32m"
    colour_reset = "\033[0m"
    sys.stdout.write(f"\n{colour_green}  ✔ {text}{colour_reset}\n")
    sys.stdout.flush()


# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    colour_blue  = "\033[34m"
    colour_bold  = "\033[1m"
    colour_reset = "\033[0m"
    colour_dim   = "\033[2m"

    print()
    print(f"{colour_bold}  WeddingOS — surprise package{colour_reset}")
    print(f"{colour_dim}  {'─' * 42}{colour_reset}")
    print()

    time.sleep(.3)
    _typed("  Initializing...",          .025)
    time.sleep(.2)
    _typed("  Loading crypto engine...", .025)
    time.sleep(.25)
    _typed("  Searching payload...",     .025)
    time.sleep(.4)
    _section("Payload found.")

    _bar("Decrypting", duration=1.6)
    time.sleep(.2)
    _section("Integrity verified.")

    print()
    _typed("  Generating QR...", .025)
    _bar("Encoding", duration=1.2)

    # ── Decode the URL ──
    url = true_love(PAYLOAD)

    # ── Build QR ──
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img: Image.Image = qr.make_image(fill_color="#0d1117", back_color="#c9d1d9")
    img.save("surprise.png")

    _section("QR successfully generated.")
    print()
    print(f"  {colour_blue}→  surprise.png{colour_reset}")
    print()
    print(f"{colour_dim}  Scan to open the surprise.{colour_reset}")
    print()


if __name__ == "__main__":
    main()
