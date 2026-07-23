# WeddingOS v2.0 — Esküvői meglepetés projekt

> **Egy bekeretezett Python forráskód, amely egy titkosított QR-kódot generál — a QR egy animált "WeddingOS" terminálélményre mutat.**

---

## Projekt felépítése

```
wedding-surprise/
├── frontend/
│   ├── index.html      # WeddingOS terminal UI
│   ├── style.css       # GitHub Dark téma
│   ├── app.js          # Boot szekvencia, animációk, easter egg
│   └── confetti.js     # Canvas konfetti engine
├── python/
│   ├── wedding.py      # A keretbe kerülő forráskód
│   ├── encrypt.py      # URL → HEX payload generátor
│   ├── build_payload.py # Round-trip ellenőrzés
│   └── requirements.txt
└── README.md
```

---

## 1. GitHub Pages beállítása

1. Menj a repo **Settings → Pages** oldalára.
2. Source: **Deploy from a branch**
3. Branch: `main`, mappa: `/ (root)` — **vagy** `/ frontend` ha a frontend mappa gyökerét akarod.
4. Mentés → néhány perc után él: `https://<username>.github.io/wedding-surprise/`

> A `frontend/index.html` fog betöltődni, mert a repo gyökerében lévő `index.html` átirányítja oda (vagy a Pages `docs/` mappát is használhatod — lásd lent).

**Alternatív**: ha a Pages-t a gyökérből töltöd, másold a `frontend/` fájlokat a repo gyökerébe, vagy adj meg `docs/` mappát és másold oda.

---

## 2. Payload generálása (ha URL-t változtatsz)

```bash
cd python
pip install -r requirements.txt

# Ellenőrzés és generálás egyben:
python build_payload.py https://<username>.github.io/wedding-surprise/
```

A kimenetből másold a HEX stringet.

---

## 3. Payload bemásolása a wedding.py-ba

Nyisd meg `python/wedding.py`-t, és cseréld le a `PAYLOAD` változó értékét:

```python
PAYLOAD = (
    "az_uj_hex_payload_ide_jon"
)
```

---

## 4. QR generálása

```bash
cd python
pip install -r requirements.txt
python wedding.py
```

Létrejön a `surprise.png` — ez a QR-kód.

---

## 5. Nyomtatás és keretbe helyezés

- Nyomtasd ki a `python/wedding.py` forráskódot (pl. [carbon.now.sh](https://carbon.now.sh) segítségével szép formában).
- A QR-kódot (`surprise.png`) nyomtasd a kód mellé vagy alá.
- Keretezd be — kész az ajándék!

---

## Az animáció menete (frontend)

```
WeddingOS boot
  ↓
Relationship modules betöltve (Love, Trust, Respect, Humor, Coffee)
  ↓
Payload decryption progress bar
  ↓
Compatibility check: 99.9999998%
  ↓
Marriage deployment progress bar
  ↓
happily_ever_after() launch
  ↓
S U C C E S S  + konfetti
  ↓
Terminál fade + zsugorodás
  ↓
Gratulációs kártya animálva
  ↓
git status: "nothing to commit, working tree clean ❤️"
```

---

## Easter egg

A SUCCESS után megjelenik egy parancssori beviteli mező.
Írd be: `help` — megjelenik a titkos parancsok listája:

| Parancs             | Leírás                               |
|---------------------|--------------------------------------|
| `brew coffee`       | Kávéfőzés ☕                          |
| `git hug`           | Unconditional hug                    |
| `deploy vacation`   | Honeymoon pipeline indítása           |
| `restart honeymoon` | happily_ever_after() újraindítás     |
| `git blame love`    | Author: \<You two\>                  |
| `sudo kiss`         | Permission always granted            |
| `ping happiness`    | 0% packet loss                       |

---

## Nevek / dátum módosítása

`frontend/app.js` tetején:

```js
const CONFIG = {
  names:      "Kriszti & Gabor",   // ← ide a nevek
  commitDate: "2026-09-12",        // ← esküvő dátuma
  author:     "Your Friends",      // ← ajándékozó neve
  ...
};
```

---

## Technológiák

| Réteg    | Technológia                          |
|----------|--------------------------------------|
| Frontend | Vanilla JS, Canvas API, CSS3         |
| Betűtípus| JetBrains Mono (Google Fonts)        |
| Téma     | GitHub Dark (`#0d1117`, `#161b22`)   |
| Háttér   | Matrix 0/1 canvas animáció           |
| Konfetti | Saját canvas-alapú engine            |
| Python   | qrcode, Pillow, gzip, base64, XOR    |

---

*Készült szeretettel — mert két fejlesztő megérdemli, hogy a legnagyobb deployment is production-quality legyen.*
