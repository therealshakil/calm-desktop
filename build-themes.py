#!/usr/bin/env python3
"""calm-desktop: build calm-paper and calm-ink from Mint-Y.

Reads Mint's own Grey themes, maps every colour onto calm's warm ink-on-paper ramp by brightness,
and writes the results to ~/.themes. Reds and oranges become the one clay accent; every other hue
falls to ink. Re-run after a Mint upgrade to rebuild against the new Mint-Y.

    python3 -I build-themes.py
"""
import colorsys
import re
import shutil
from pathlib import Path

from PIL import Image

SRC = Path("/usr/share/themes")
OUT = Path.home() / ".themes"
KEEP = {"cinnamon", "gtk-2.0", "gtk-3.0", "gtk-4.0", "libadwaita-1.5", "libadwaita-1.7"}
TEXT = {".css", ".svg", ".rc", ".xml"}

# brightness of Mint's colour -> calm colour (tokens.css, plus a few in-between steps)
PAPER = [(0.00, "14110E"), (0.19, "26231E"), (0.45, "6B6456"), (0.70, "A79E8C"),
         (0.80, "CFC6B3"), (0.88, "E4DCCB"), (0.93, "EDE7DA"), (0.97, "F7F4EC"), (1.00, "FCFAF4")]
INK = [(0.00, "0E0C0A"), (0.09, "171410"), (0.125, "1B1814"), (0.18, "221E19"), (0.22, "2C2820"),
       (0.45, "5E574A"), (0.65, "9A9080"), (0.86, "D6CEBE"), (1.00, "ECE6D8")]
CLAY = {"paper": "B5612F", "ink": "EDB489"}

THEMES = [("Mint-Y-Grey", "calm-paper", PAPER), ("Mint-Y-Dark-Grey", "calm-ink", INK)]


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lerp(ramp, lum):
    for (a, ca), (b, cb) in zip(ramp, ramp[1:]):
        if lum <= b:
            t = 0 if b == a else (lum - a) / (b - a)
            return tuple(round(x + (y - x) * t) for x, y in zip(rgb(ca), rgb(cb)))
    return rgb(ramp[-1][1])


def calm(r, g, b, ramp, clay):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    if s > 0.35 and v > 0.25 and (h < 0.125 or h > 0.92):  # red / orange -> clay
        return rgb(clay)
    return lerp(ramp, (0.299 * r + 0.587 * g + 0.114 * b) / 255)


def recolour_text(s, ramp, clay):
    hexc = lambda c: "#%02X%02X%02X" % c

    def six(m):
        return hexc(calm(*rgb(m.group(1)), ramp, clay))

    def three(m):
        return hexc(calm(*rgb("".join(ch * 2 for ch in m.group(1))), ramp, clay))

    def func(m):
        r, g, b = (int(float(x)) for x in m.group(2).split(",")[:3])
        rest = m.group(2).split(",")[3:]
        c = calm(r, g, b, ramp, clay)
        return m.group(1) + "(" + ", ".join([str(x) for x in c] + [x.strip() for x in rest]) + ")"

    s = re.sub(r"#([0-9a-fA-F]{6})\b", six, s)
    s = re.sub(r"#([0-9a-fA-F]{3})(?=\s*[;,)\"'])", three, s)
    s = re.sub(r"\b(rgba?)\(([\d.\s,]+)\)", func, s)
    s = re.sub(r"(?<![-\w#])white(?![-\w])", hexc(lerp(ramp, 1.0)), s)
    s = re.sub(r"(?<![-\w#])black(?![-\w])", hexc(lerp(ramp, 0.0)), s)
    return s


def recolour_png(path, ramp, clay):
    im = Image.open(path)
    mode = im.mode
    im = im.convert("RGBA")
    cache = {}
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a:
                c = cache.get((r, g, b)) or cache.setdefault((r, g, b), calm(r, g, b, ramp, clay))
                px[x, y] = (*c, a)
    im.convert(mode if mode in ("RGBA", "RGB", "LA", "L") else "RGBA").save(path)


def build(src, name, ramp, clay):
    dst = OUT / name
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    for part in KEEP:
        if (SRC / src / part).exists():
            shutil.copytree(SRC / src / part, dst / part, symlinks=False)
    for f in dst.rglob("*"):
        if f.is_file() and (f.suffix in TEXT or f.name == "gtkrc"):
            f.write_text(recolour_text(f.read_text(), ramp, clay))
        elif f.is_file() and f.suffix == ".png":
            recolour_png(f, ramp, clay)
    (dst / "index.theme").write_text(
        "[Desktop Entry]\nType=X-GNOME-Metatheme\nName=%s\n"
        "Comment=calm: ink on paper, built from Mint-Y\nEncoding=UTF-8\n\n"
        "[X-GNOME-Metatheme]\nGtkTheme=%s\nMetacityTheme=Mint-Y\nIconTheme=Mint-Y-Grey\n"
        "CursorTheme=Bibata-Modern-Classic\nButtonLayout=:minimize,maximize,close\n" % (name, name))
    print("built", dst)


for src, name, ramp in THEMES:
    build(src, name, ramp, CLAY[name.split("-")[1]])
