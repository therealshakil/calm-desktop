#!/usr/bin/env python3
"""calm-desktop: build calm-mono, a monochrome icon theme.

Every app icon (from the installed launchers), and every folder, file-type and device icon, is
redrawn in calm's ink-to-paper tones by brightness, keeping its shape. It sits on Yaru sage, so
anything not redrawn (the small symbolic icons) still comes from there. Two themes share one set:
calm-mono-dark and calm-mono-light. Re-run after installing apps.

    python3 -I build-icons.py
"""
import configparser
import shutil
from pathlib import Path

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from PIL import Image

HOME = Path.home()
OUT = HOME / ".local/share/icons"
SET = OUT / "calm-mono-set"
SIZES = [16, 22, 24, 32, 48, 64, 96, 128, 256]
CONTEXTS = {"apps": "Applications", "places": "Places", "mimetypes": "MimeTypes", "devices": "Devices",
            "status": "Status"}
LAUNCHER_DIRS = [Path("/usr/share/applications"), HOME / ".local/share/applications",
                 Path("/var/lib/flatpak/exports/share/applications")]
SOURCE_THEMES = [Path("/usr/share/icons") / t for t in ("Yaru", "Yaru-sage", "Yaru-sage-dark")]

# brightness -> calm tone, from near-black ink to warm paper (tokens.css, with in-between steps)
RAMP = [(0.00, "14110E"), (0.19, "26231E"), (0.45, "6B6456"), (0.70, "A79E8C"),
        (0.85, "D6CEBE"), (0.93, "EDE7DA"), (1.00, "FCFAF4")]


def lut():
    rgb = lambda h: [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    table = []
    for v in range(256):
        x = v / 255
        for (a, ca), (b, cb) in zip(RAMP, RAMP[1:]):
            if x <= b:
                t = (x - a) / (b - a)
                table.append([round(p + (q - p) * t) for p, q in zip(rgb(ca), rgb(cb))])
                break
    return [[c[i] for c in table] for i in range(3)]


LUT = lut()


def mono(pixbuf):
    mode = "RGBA" if pixbuf.get_has_alpha() else "RGB"
    im = Image.frombytes(mode, (pixbuf.get_width(), pixbuf.get_height()), pixbuf.get_pixels(),
                         "raw", mode, pixbuf.get_rowstride())
    lum = im.convert("L")
    out = Image.merge("RGB", [lum.point(LUT[i]) for i in range(3)])
    if mode == "RGBA":
        out.putalpha(im.getchannel("A"))
    return out


def names():
    found = {c: set() for c in CONTEXTS}
    for d in LAUNCHER_DIRS:
        for f in d.glob("*.desktop"):
            cp = configparser.ConfigParser(interpolation=None, strict=False)
            try:
                cp.read(f, encoding="utf-8")
                icon = cp.get("Desktop Entry", "Icon", fallback="")
            except Exception:
                continue
            if icon and "/" not in icon:
                found["apps"].add(icon)
    for theme in SOURCE_THEMES:
        for ctx in ("places", "mimetypes", "devices", "status"):
            for f in theme.glob("*/%s/*" % ctx):
                if f.suffix in (".png", ".svg") and "-symbolic" not in f.stem:
                    found[ctx].add(f.stem)
    return found


theme = Gtk.IconTheme.new()
theme.set_custom_theme("Yaru-sage-dark")
if SET.exists():
    shutil.rmtree(SET)
count = 0
for ctx, icons in names().items():
    for name in sorted(icons):
        for size in SIZES:
            info = theme.lookup_icon(name, size, Gtk.IconLookupFlags.FORCE_SIZE)
            if info is None:
                continue
            try:
                pb = info.load_icon()
            except Exception:
                continue
            dest = SET / ("%dx%d" % (size, size)) / ctx / (name + ".png")
            dest.parent.mkdir(parents=True, exist_ok=True)
            mono(pb).save(dest)
            count += 1

dirs = ["%dx%d/%s" % (s, s, c) for s in SIZES for c in CONTEXTS]
sections = "".join("\n[%dx%d/%s]\nSize=%d\nContext=%s\nType=Fixed\n" % (s, s, c, s, CONTEXTS[c])
                   for s in SIZES for c in CONTEXTS)
for name, parent in (("calm-mono-dark", "Yaru-sage-dark"), ("calm-mono-light", "Yaru-sage")):
    t = OUT / name
    t.mkdir(parents=True, exist_ok=True)
    for s in SIZES:
        link = t / ("%dx%d" % (s, s))
        if link.is_symlink() or link.exists():
            link.unlink()
        link.symlink_to(SET / ("%dx%d" % (s, s)))
    (t / "index.theme").write_text(
        "[Icon Theme]\nName=%s\nComment=calm: monochrome icons in ink and paper, over %s\n"
        "Inherits=%s,hicolor\nDirectories=%s\n%s" % (name, parent, parent, ",".join(dirs), sections))
print("calm-mono:", count, "icons drawn")
