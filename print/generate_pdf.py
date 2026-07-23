#!/usr/bin/env python3
"""Generate wedding_print.pdf — A4, dark theme, VS Code-style syntax colours."""

import sys, subprocess
from pathlib import Path

def _install(pkg):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.colors import HexColor
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("Installing reportlab..."); _install('reportlab')
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.colors import HexColor
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

try:
    import pygments
    from pygments.lexers import PythonLexer
except ImportError:
    print("Installing pygments..."); _install('pygments')
    import pygments
    from pygments.lexers import PythonLexer

# ── Register JetBrains Mono ───────────────────────────────────────────────────
_FONT_DIR = Path(__file__).parent / 'fonts'
pdfmetrics.registerFont(TTFont('JB',  str(_FONT_DIR / 'JetBrainsMono-Regular.ttf')))
pdfmetrics.registerFont(TTFont('JBB', str(_FONT_DIR / 'JetBrainsMono-Bold.ttf')))
pdfmetrics.registerFont(TTFont('JBI', str(_FONT_DIR / 'JetBrainsMono-Italic.ttf')))

MONO      = 'JB'
MONO_BOLD = 'JBB'
MONO_ITAL = 'JBI'

# ── Colour palette — exact match to frontend/style.css ───────────────────────
BG     = HexColor('#0d1117')
PANEL  = HexColor('#161b22')
CHROME = HexColor('#21262d')
BORDER = HexColor('#30363d')
TEXT   = HexColor('#c9d1d9')
DIM    = HexColor('#8b949e')
DOT_R  = HexColor('#ff5f57')
DOT_Y  = HexColor('#febc2e')
DOT_G  = HexColor('#28c840')
C_CMT  = HexColor('#6e7681')   # .c   comment
C_KW   = HexColor('#ff7b72')   # .kw  keyword
C_BLT  = HexColor('#ffa657')   # .bi  builtin
C_FN   = HexColor('#d2a8ff')   # .fn  function
C_STR  = HexColor('#a5d6ff')   # .st  string
C_NUM  = HexColor('#79c0ff')   # .nm  number
C_GRN  = HexColor('#3fb950')   # ok green

def _color(ttype):
    s = str(ttype)
    if 'Comment'  in s: return C_CMT
    if 'Keyword'  in s: return C_KW
    if 'Builtin'  in s: return C_BLT
    if 'Function' in s: return C_FN
    if 'String'   in s: return C_STR
    if 'Number'   in s: return C_NUM
    return TEXT

def _font(ttype, sz):
    return (MONO_ITAL, sz) if 'Comment' in str(ttype) else (MONO, sz)

# ── Page geometry ─────────────────────────────────────────────────────────────
W, H  = A4
MX    = 10 * mm
MT    = 11 * mm
CX    = MX
CW    = W - 2 * MX

FS    = 8.6                  # code font size (pt)
LH    = 11.2                 # line height (pt)
CHR_H = 28.0                 # chrome bar height
CP    = 9.0                  # code padding top/bottom
LNW   = 22.0                 # line-number column width

# ── Read source ───────────────────────────────────────────────────────────────
SRC   = Path(__file__).parent.parent / 'python' / 'wedding.py'
LINES = SRC.read_text(encoding='utf-8').splitlines()
NL    = len(LINES)

CODE_H = NL * LH + 2 * CP
TERM_H = CHR_H + CODE_H

# ── Tokenise ──────────────────────────────────────────────────────────────────
raw_toks = list(pygments.lex('\n'.join(LINES), PythonLexer()))
line_toks = [[]]
for tt, tv in raw_toks:
    parts = tv.split('\n')
    for i, p in enumerate(parts):
        if p:
            line_toks[-1].append((tt, p))
        if i < len(parts) - 1:
            line_toks.append([])

# ── Draw ──────────────────────────────────────────────────────────────────────
def build(out):
    c = rl_canvas.Canvas(str(out), pagesize=A4)

    # page background
    c.setFillColor(BG)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    TY = H - MT

    # chrome background (rounded, full terminal)
    c.setFillColor(CHROME)
    c.roundRect(CX, TY - TERM_H, CW, TERM_H, 8, stroke=0, fill=1)

    # code area (slightly darker panel)
    c.setFillColor(PANEL)
    c.rect(CX + 0.5, TY - TERM_H, CW - 1, CODE_H, stroke=0, fill=1)

    # outer border
    c.setStrokeColor(BORDER); c.setLineWidth(0.6)
    c.roundRect(CX, TY - TERM_H, CW, TERM_H, 8, stroke=1, fill=0)

    # chrome / code divider
    c.setStrokeColor(BORDER); c.setLineWidth(0.4)
    c.line(CX, TY - CHR_H, CX + CW, TY - CHR_H)

    # traffic-light dots
    DY = TY - CHR_H / 2
    for col, dx in [(DOT_R, CX + 13), (DOT_Y, CX + 27), (DOT_G, CX + 41)]:
        c.setFillColor(col)
        c.circle(dx, DY, 4.5, stroke=0, fill=1)

    # window title
    wtitle = 'wedding.py  —  Python 3'
    c.setFillColor(DIM); c.setFont(MONO, 8.5)
    c.drawString(CX + CW / 2 - c.stringWidth(wtitle, MONO, 8.5) / 2, DY - 3.2, wtitle)

    # ── code lines ──
    CY = TY - TERM_H
    for li, toks in enumerate(line_toks[:NL]):
        y = CY + CODE_H - CP - (li + 1) * LH + 2.2

        # line number
        c.setFillColor(DIM); c.setFont(MONO, FS)
        ln = str(li + 1)
        c.drawString(CX + LNW - c.stringWidth(ln, MONO, FS) - 1, y, ln)

        # separator line
        c.setStrokeColor(HexColor('#21262d')); c.setLineWidth(0.3)
        c.line(CX + LNW + 2, y - 1, CX + LNW + 2, y + FS)

        # tokens
        x = CX + LNW + 5
        for tt, tv in toks:
            fn, fz = _font(tt, FS)
            c.setFillColor(_color(tt)); c.setFont(fn, fz)
            c.drawString(x, y, tv)
            x += c.stringWidth(tv, fn, fz)

    # ── footer ──
    sep_y = CY - 7
    c.setStrokeColor(BORDER); c.setLineWidth(0.4)
    c.line(CX, sep_y, CX + CW, sep_y)

    fy = sep_y - 15
    c.setFillColor(TEXT); c.setFont(MONO_BOLD, 11)
    msg = 'Run this script to reveal the surprise.'
    c.drawString(CX + CW / 2 - c.stringWidth(msg, MONO_BOLD, 11) / 2, fy, msg)

    c.setFillColor(DIM); c.setFont(MONO, 8.5)
    sub = 'Requires Python 3  ·  pip install qrcode[pil]'
    c.drawString(CX + CW / 2 - c.stringWidth(sub, MONO, 8.5) / 2, fy - 13, sub)

    # command pill
    cmd = 'python wedding.py'
    c.setFont(MONO_BOLD, 10)
    pw = c.stringWidth(cmd, MONO_BOLD, 10) + 24
    px = CX + CW / 2 - pw / 2
    py = fy - 34
    c.setFillColor(PANEL); c.setStrokeColor(BORDER); c.setLineWidth(0.5)
    c.roundRect(px, py, pw, 19, 5, stroke=1, fill=1)
    c.setFillColor(C_GRN); c.setFont(MONO_BOLD, 10)
    c.drawString(px + 12, py + 5.5, cmd)

    c.save()
    print(f'\n  OK  PDF saved -> {out}\n')


if __name__ == '__main__':
    out = Path(__file__).parent / 'wedding_print.pdf'
    build(out)
