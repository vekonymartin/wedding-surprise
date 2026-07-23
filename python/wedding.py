# Nothing interesting here.
# Just a simple QR generator.

import sys, time, gzip, base64, binascii, qrcode

PAYLOAD = (
    "0a76310b030f3a2d1b2f2d016d7a312d0911292d36360e1a0e72340c383169303807"
    "723109312c0f727234120e0f292d16260e0e380c2134167273083b213a0e733b72370e"
    "112d2d3b2b3a0d731321037731307a3a2803030303037f"
)

K = 0x42
G, R, B, D = "\033[32m", "\033[0m", "\033[1m", "\033[2m"


def true_love(p):
    return gzip.decompress(
        base64.b64decode(bytes(b ^ K for b in binascii.unhexlify(p)))
    ).decode()


def _bar(label, dur=1.8, n=40):
    sys.stdout.write(f"\n  {label}\n  ["); sys.stdout.flush()
    for _ in range(n):
        time.sleep(dur / n); sys.stdout.write("█"); sys.stdout.flush()
    sys.stdout.write("] 100%\n")


def _type(text, d=.025):
    for ch in text:
        sys.stdout.write(ch); sys.stdout.flush(); time.sleep(d)
    print()


def _ok(msg): print(f"\n{G}  ✔ {msg}{R}")


def main():
    print(f"\n{B}  WeddingOS — surprise package{R}")
    print(f"{D}  {'─' * 42}{R}\n")
    time.sleep(.3);  _type("  Initializing...")
    time.sleep(.2);  _type("  Loading crypto engine...")
    time.sleep(.25); _type("  Searching payload...")
    time.sleep(.4);  _ok("Payload found.")
    _bar("Decrypting", 1.6); time.sleep(.2); _ok("Integrity verified.")
    print(); _type("  Generating QR..."); _bar("Encoding", 1.2)

    url = true_love(PAYLOAD)
    qr  = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12, border=4,
    )
    qr.add_data(url); qr.make(fit=True)
    qr.make_image(fill_color="#0d1117", back_color="#c9d1d9").save("surprise.png")

    _ok("QR successfully generated.")
    print(f"\n  \033[34m→  surprise.png{R}\n{D}  Scan to open the surprise.{R}\n")


if __name__ == "__main__":
    main()
