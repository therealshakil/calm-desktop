#!/usr/bin/env python3
"""calm-desktop: tile windows into even thirds with gTile.

Installs the gTile extension from Cinnamon Spices if it isn't here, makes its
second layout three even columns named "Thirds", and turns it on.
Super+G opens the grid; 2 picks Thirds; arrows move, Shift+arrow widens, Enter places.
The 8 px gap comes from gtile-gap-patch.py, kept in place by systemd/gtile-gap-patch.path.
Safe to run again.
"""
import io
import json
import os
import subprocess
import time
import urllib.request
import zipfile

UUID = "gTile@shuairan"
URL = f"https://cinnamon-spices.linuxmint.com/files/extensions/{UUID}.zip"
EXTENSIONS = "/home/shakil/.local/share/cinnamon/extensions"
SETTINGS = f"/home/shakil/.config/cinnamon/spices/{UUID}/{UUID}.json"


def enabled():
    out = subprocess.run(["gsettings", "get", "org.cinnamon", "enabled-extensions"],
                         capture_output=True, text=True).stdout.strip()
    if out.startswith("@as"):
        out = out[3:].strip()
    return [x.strip().strip("'") for x in out.strip("[]").split(",") if x.strip()]


def set_enabled(uuids):
    value = "[" + ", ".join(f"'{u}'" for u in uuids) + "]"
    subprocess.run(["gsettings", "set", "org.cinnamon", "enabled-extensions", value], check=True)
    time.sleep(2)


def install():
    if os.path.isdir(f"{EXTENSIONS}/{UUID}"):
        return
    with urllib.request.urlopen(URL, timeout=30) as r:
        data = r.read()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for name in z.namelist():
            if not name.startswith(f"{UUID}/") or ".." in name:
                raise SystemExit(f"gTile's download had an unexpected file in it ({name}); left it alone.")
        z.extractall(EXTENSIONS)


def thirds():
    # Cinnamon writes its own settings back while gTile runs, so edit with it off.
    others = [u for u in enabled() if u != UUID]
    if not os.path.exists(SETTINGS):
        set_enabled(others + [UUID])  # first run creates the settings file
    set_enabled(others)
    with open(SETTINGS) as f:
        s = json.load(f)
    s["grid2x"]["value"] = [{"span": 1}, {"span": 1}, {"span": 1}]
    s["grid2y"]["value"] = [{"span": 1}]
    s["grid2NameOverride"]["value"] = "Thirds"
    s["animation"]["value"] = False  # stillness, like the rest of the desktop
    with open(SETTINGS, "w") as f:
        json.dump(s, f, indent=4)
    set_enabled(others + [UUID])


install()
thirds()
