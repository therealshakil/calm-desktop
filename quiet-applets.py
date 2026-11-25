#!/usr/bin/env python3
"""calm-desktop: take the badges off the panel applets.

Notification count off; window-count and notification badges off; no launcher animation;
Firefox pinned in place of Brave. Cinnamon picks the change up on its next reload.
"""
import json
from pathlib import Path

SPICES = Path.home() / ".config/cinnamon/spices"


def edit(path, change):
    if not path.exists():
        print("skipped, not found:", path)
        return
    d = json.loads(path.read_text())
    change(d)
    path.write_text(json.dumps(d, indent=4))
    print("quieted", path.name)


def notifications(d):
    d["showNotificationCount"]["value"] = False


def window_list(d):
    d["enable-window-count-badges"]["value"] = False
    d["enable-notification-badges"]["value"] = False
    d["launcher-animation-effect"]["value"] = 1  # None
    pins = d["pinned-apps"]["value"]
    d["pinned-apps"]["value"] = ["firefox.desktop" if p == "brave-browser.desktop" else p for p in pins]


edit(SPICES / "notifications@cinnamon.org/notifications@cinnamon.org.json", notifications)
for f in sorted((SPICES / "grouped-window-list@cinnamon.org").glob("*.json")):
    edit(f, window_list)
