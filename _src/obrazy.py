# -*- coding: utf-8 -*-
"""Przygotowanie zdjęć (Unsplash, Vitaly Gariev) do assets/img: python -I _src/obrazy.py"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src" / "orig" / "unsplash"
OUT = ROOT / "assets" / "img"


def zapisz(im, nazwa, w, q=78):
    im = im.copy()
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(OUT / f"{nazwa}-{w}.webp", "WEBP", quality=q, method=6)
    print(nazwa, w, im.size)


# hero: odbicie lustrzane - doradczyni po prawej, klient (ciemna marynarka) po lewej pod tekstem
h = ImageOps.mirror(Image.open(SRC / "vitaly-gariev-M5k978V3qBc.jpg").convert("RGB"))
for w in (1200, 1800, 2400):
    zapisz(h, "hero", w, 76)
# telefon: wycinek 4:3 z doradczynią i rozmową
W, H = h.size
tel = h.crop((int(W * 0.30), 0, int(W * 0.30) + int(H * 1.25), H))
zapisz(tel, "hero-tel", 900, 74)

for plik, nazwa in [("vitaly-gariev-yQhNMgl5Lag.jpg", "rozmowa"), ("vitaly-gariev-RbYg6fKSfcY.jpg", "zespol"),
                    ("vitaly-gariev-f4TM45jATYU.jpg", "spotkanie"), ("vitaly-gariev-KDWgcgMFFVI.jpg", "narada")]:
    im = Image.open(SRC / plik).convert("RGB")
    for w in (800, 1400):
        zapisz(im, nazwa, w, 76)
