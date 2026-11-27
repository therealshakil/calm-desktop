#!/usr/bin/env python3
"""Re-apply the even-gap patch to the gTile Cinnamon extension when it's missing.

Safe to run any time: it does nothing if every gTile.js is already patched.
Run by systemd/gtile-gap-patch.path (on any change to gTile) and .service (at login).
"""
import glob
import os
import shutil
import subprocess
import time

EXT = "/home/shakil/.local/share/cinnamon/extensions/gTile@shuairan"
UUID = "gTile@shuairan"
GAP = 8
MARKER = "Local patch: even gap"

ANCHOR = """const move_resize_window = (metaWindow, x, y, width, height) => {
    if (!metaWindow)
        return;
"""

PATCH = f"""    // {MARKER} (px) around and between tiles. Original in gTile.js.orig.
    const GAP = {GAP};
    const wa = metaWindow.get_work_area_current_monitor();
    const near = (a, b) => Math.abs(a - b) < 2;
    const left = near(x, wa.x) ? GAP : GAP / 2;
    const top = near(y, wa.y) ? GAP : GAP / 2;
    const right = near(x + width, wa.x + wa.width) ? GAP : GAP / 2;
    const bottom = near(y + height, wa.y + wa.height) ? GAP : GAP / 2;
    x = x + left;
    y = y + top;
    width = width - left - right;
    height = height - top - bottom;
"""


def notify(msg):
    subprocess.run(["notify-send", "-i", "preferences-desktop", "gTile gap", msg], check=False)


def notify_once(path, msg):
    # Say it once per gTile version, never again at each login.
    seen = os.path.expanduser("~/.cache/gtile-gap-patch-notified")
    stamp = f"{path} {os.path.getmtime(path)}"
    if os.path.exists(seen) and open(seen).read() == stamp:
        return
    notify(msg)
    with open(seen, "w") as f:
        f.write(stamp)


def patch_file(path):
    src = open(path).read()
    if MARKER in src:
        return False
    if ANCHOR not in src:
        notify_once(path, "gTile changed shape after an update, so the gap couldn't be added this time. Tiling still works.")
        return False
    shutil.copyfile(path, path + ".orig")
    with open(path, "w") as f:
        f.write(src.replace(ANCHOR, ANCHOR + PATCH, 1))
    return True


def reload_extension():
    out = subprocess.run(["gsettings", "get", "org.cinnamon", "enabled-extensions"],
                         capture_output=True, text=True).stdout.strip()
    if UUID not in out:
        return
    without = out.replace(f"'{UUID}', ", "").replace(f", '{UUID}'", "").replace(f"'{UUID}'", "")
    subprocess.run(["gsettings", "set", "org.cinnamon", "enabled-extensions", without], check=False)
    time.sleep(1)
    subprocess.run(["gsettings", "set", "org.cinnamon", "enabled-extensions", out], check=False)


def main():
    time.sleep(3)  # let an in-progress update finish writing files
    changed = False
    for path in glob.glob(f"{EXT}/*/gTile.js") + glob.glob(f"{EXT}/gTile.js"):
        changed = patch_file(path) or changed
    if changed:
        reload_extension()


if __name__ == "__main__":
    main()
