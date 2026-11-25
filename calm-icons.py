#!/usr/bin/env python3
"""calm-desktop: calm icons for apps whose own icon is loud.

For each override: a scalable SVG under the app's icon name, and every fixed-size PNG the app
installed redrawn from it (originals kept once under icons/originals/). Safe to run again,
for example after Brave refreshes a web app.

    python3 -I calm-icons.py
"""
import shutil
from pathlib import Path

import gi
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf

REPO = Path(__file__).resolve().parent
HICOLOR = Path.home() / ".local/share/icons/hicolor"

# icon name the app asks for -> calm SVG in this repo
OVERRIDES = {
    "brave-hnpfjngllnobngcgfapefoaidbinmjnm-Default": "whatsapp-calm.svg",  # WhatsApp web app
}

for name, svg in OVERRIDES.items():
    src = REPO / "icons" / svg
    scalable = HICOLOR / "scalable/apps" / (name + ".svg")
    scalable.parent.mkdir(parents=True, exist_ok=True)
    if not scalable.exists():
        scalable.symlink_to(src)
    for png in HICOLOR.glob("*x*/apps/%s.png" % name):
        keep = REPO / "icons/originals" / png.parent.parent.name / png.name
        if not keep.exists():
            keep.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(png, keep)
        size = int(png.parent.parent.name.split("x")[0])
        GdkPixbuf.Pixbuf.new_from_file_at_size(str(src), size, size).savev(str(png), "png", [], [])
        print("calm", name, size)
