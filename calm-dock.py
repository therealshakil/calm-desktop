#!/usr/bin/env python3
"""calm-desktop: a macOS-like layout, calm.

A slim top bar (menu left; tray, status and the time right) and a centred Plank Reloaded dock
below, in calm-ink or calm-paper. Safe to run again.

    python3 -I calm-dock.py
"""
import json
from pathlib import Path

from gi.repository import Gio

HOME = Path.home()
REPO = Path(__file__).resolve().parent
THEMES = HOME / ".local/share/plank/themes"
LAUNCHERS = HOME / ".config/plank/dock1/launchers"

# The apps that were pinned on the Cinnamon panel, in the same order, then the Trash.
APPS = [
    ("ghostty", "file:///usr/share/applications/com.mitchellh.ghostty.desktop"),
    ("nemo", "file:///usr/share/applications/nemo.desktop"),
    ("firefox", "file:///usr/share/applications/firefox.desktop"),
    ("calibre", "file:///usr/share/applications/calibre-gui.desktop"),
    ("hexchat", "file:///var/lib/flatpak/exports/share/applications/io.github.Hexchat.desktop"),
    ("terminal", "file:///usr/share/applications/org.gnome.Terminal.desktop"),
    ("whatsapp", "file://%s/.local/share/applications/brave-hnpfjngllnobngcgfapefoaidbinmjnm-Default.desktop" % HOME),
    ("separator", "docklet://separator"),
    ("trash", "docklet://trash"),
]

# 1. The two calm dock themes, linked from the repo.
THEMES.mkdir(parents=True, exist_ok=True)
for name in ("calm-ink", "calm-paper"):
    link = THEMES / name
    if not link.exists():
        link.symlink_to(REPO / "plank" / name)

# 2. The dock's items.
LAUNCHERS.mkdir(parents=True, exist_ok=True)
for name, uri in APPS:
    (LAUNCHERS / (name + ".dockitem")).write_text("[PlankDockItemPreferences]\nLauncher=%s\n" % uri)

# 3. The dock: centred at the bottom, floating a little, steps aside only when a window needs the space.
dock = Gio.Settings.new_with_path("net.launchpad.plank.dock.settings", "/net/launchpad/plank/docks/dock1/")
ink = Gio.Settings.new("org.cinnamon.desktop.interface").get_string("gtk-theme") != "calm-paper"
dock.set_string("theme", "calm-ink" if ink else "calm-paper")
dock.set_strv("dock-items", [name + ".dockitem" for name, _ in APPS])
dock.set_string("hide-mode", "window-dodge")
dock.set_int("icon-size", 44)
dock.set_int("gap-size", 8)
dock.set_boolean("zoom-enabled", False)
dock.set_boolean("show-dock-item", False)
dock.set_boolean("previews-enabled", False)
dock.set_boolean("lock-items", False)

# 4. The top bar: slim, always there. Menu left; tray, status and the time right. No window list.
cinnamon = Gio.Settings.new("org.cinnamon")
cinnamon.set_strv("panels-enabled", ["1:0:top"])
cinnamon.set_strv("panels-height", ["1:26"])
cinnamon.set_strv("panels-autohide", ["1:false"])
cinnamon.set_strv("enabled-applets", [
    "panel1:left:0:menu@cinnamon.org:0",
    "panel1:right:0:systray@cinnamon.org:3",
    "panel1:right:1:xapp-status@cinnamon.org:4",
    "panel1:right:2:notifications@cinnamon.org:5",
    "panel1:right:3:network@cinnamon.org:10",
    "panel1:right:4:sound@cinnamon.org:11",
    "panel1:right:5:power@cinnamon.org:12",
    "panel1:right:6:calendar@cinnamon.org:13",
])

# 5. The time, written the macOS way: "Wed 25 Nov  23:45".
for f in (HOME / ".config/cinnamon/spices/calendar@cinnamon.org").glob("*.json"):
    d = json.loads(f.read_text())
    if "use-custom-format" in d and "custom-format" in d:
        d["use-custom-format"]["value"] = True
        d["custom-format"]["value"] = "%a %-d %b  %H:%M"
        f.write_text(json.dumps(d, indent=4))

# 6. Start the dock at every login.
autostart = HOME / ".config/autostart/plank.desktop"
if not autostart.exists():
    autostart.symlink_to(REPO / "autostart" / "plank.desktop")
Gio.Settings.sync()  # flush before exit, or the settings never land
print("calm dock and top bar set")
