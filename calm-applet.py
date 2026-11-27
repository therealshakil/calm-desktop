#!/usr/bin/env python3
"""calm-desktop: put a calm applet on the top bar.

Links applet/<uuid> into Cinnamon and adds it at the start of the bar's right side.
With no argument it's the light / mixed / dark switch, calm-mode@calm-desktop.
Safe to run again. To remove: right-click it on the bar, then "Remove".
"""
import sys
from pathlib import Path

from gi.repository import Gio

UUID = sys.argv[1] if len(sys.argv) > 1 else "calm-mode@calm-desktop"
SRC = Path(__file__).resolve().parent / "applet" / UUID
DEST = Path.home() / ".local/share/cinnamon/applets" / UUID

DEST.parent.mkdir(parents=True, exist_ok=True)
if not DEST.is_symlink():
    DEST.symlink_to(SRC)

cinnamon = Gio.Settings.new("org.cinnamon")
applets = cinnamon.get_strv("enabled-applets")
if any(f":{UUID}:" in a for a in applets):
    print("already on the bar")
else:
    next_id = 1 + max(int(a.rsplit(":", 1)[1]) for a in applets)
    shifted = []
    for a in applets:  # panel:zone:order:uuid:id
        panel, zone, order, uuid, iid = a.split(":")
        if panel == "panel1" and zone == "right":
            order = str(int(order) + 1)
        shifted.append(":".join((panel, zone, order, uuid, iid)))
    cinnamon.set_strv("enabled-applets", [f"panel1:right:0:{UUID}:{next_id}"] + shifted)
    Gio.Settings.sync()
    print("added to the bar")
