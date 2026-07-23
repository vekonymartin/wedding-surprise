#!/usr/bin/env python3
"""Generate qr_backup.pdf — small QR on a white A5 card, for framing backup."""

import sys, subprocess
from pathlib import Path

def _install(pkg):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    from reportlab.lib.pagesizes import A5
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.utils import ImageReader
except ImportError:
    print("Installing reportlab..."); _install('reportlab')
    from reportlab.lib.pagesizes import A5
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.utils import ImageReader

try:
    import qrcode
except ImportError:
    print("Installing qrcode..."); _install('qrcode[pil]')
    import qrcode

_FONT_DIR = Path(__file__).parent / 'fonts'
if (_FONT_DIR / 'JetBrainsMono-Regular.ttf').exists():
    pdfmetrics.registerFont(TTFont('JB',  str(_FONT_DIR / 'JetBrainsMono-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('JBB', str(_FONT_DIR / 'JetBrainsMono-Bold.ttf')))
    MONO = 'JB'; MONO_BOLD = 'JBB'
else:
    MONO = 'Courier'; MONO_BOLD = 'Courier-Bold'

URL    = "https://vekonymartin.github.io/wedding-surprise/"
GRN    = HexColor('#238636')
DARK   = HexColor('#0d1117')
DIMTXT = HexColor('#57606a')


def _make_qr_image():
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10, border=2,
    )
    qr.add_data(URL)
    qr.make(fit=True)
    return qr.make_image(fill_color="#0d1117", back_color="white")


def build(out: Path) -> None:
    W, H = A5
    c = rl_canvas.Canvas(str(out), pagesize=A5)

    # white background
    c.setFillColor(white)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    # ── QR ──
    qr_img = _make_qr_image()

    import io
    buf = io.BytesIO()
    qr_img.save(buf, format='PNG')
    buf.seek(0)
    ir = ImageReader(buf)

    qr_size = 70 * mm
    qr_x = (W - qr_size) / 2
    qr_y = H / 2 - qr_size / 2 + 8 * mm

    # subtle border around QR
    c.setStrokeColor(HexColor('#d0d7de')); c.setLineWidth(0.5)
    pad = 2 * mm
    c.roundRect(qr_x - pad, qr_y - pad, qr_size + 2*pad, qr_size + 2*pad, 4, stroke=1, fill=0)

    c.drawImage(ir, qr_x, qr_y, width=qr_size, height=qr_size, mask='auto')

    # ── top label ──
    c.setFillColor(DARK); c.setFont(MONO_BOLD, 11)
    title = 'WeddingOS v2.0'
    c.drawString(W/2 - c.stringWidth(title, MONO_BOLD, 11)/2, qr_y + qr_size + 10*mm, title)

    c.setFillColor(DIMTXT); c.setFont(MONO, 8)
    sub = 'Scan to open the surprise'
    c.drawString(W/2 - c.stringWidth(sub, MONO, 8)/2, qr_y + qr_size + 6*mm, sub)

    # ── bottom label ──
    c.setFillColor(DIMTXT); c.setFont(MONO, 7.5)
    url_txt = URL
    c.drawString(W/2 - c.stringWidth(url_txt, MONO, 7.5)/2, qr_y - 8*mm, url_txt)

    c.setFillColor(GRN); c.setFont(MONO_BOLD, 8)
    note = 'Kriszti & Gabor  ·  2026-07-25'
    c.drawString(W/2 - c.stringWidth(note, MONO_BOLD, 8)/2, qr_y - 13*mm, note)

    c.save()
    print(f'\n  OK  QR backup PDF saved -> {out}\n')


if __name__ == '__main__':
    out = Path(__file__).parent / 'qr_backup.pdf'
    build(out)
