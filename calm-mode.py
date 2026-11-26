#!/usr/bin/env python3
"""calm-desktop: one switch for light, dark, and mixed.

Two halves move on their own, so they can be mixed:
  apps     the Applications theme; icons, apps' colour scheme and the wallpaper follow it.
  desktop  the Desktop theme (top bar); the dock follows it.
Light is paper/paper, dark is ink/ink, mixed is paper apps under an ink bar and dock.
The top-bar switcher (applet/) and the Themes window both work; this keeps the rest in step.

    calm-mode.py watch    # runs at login; follows the two themes
    calm-mode.py light | dark | mixed | toggle
"""
import sys

from gi.repository import Gio, GLib

PICS = "file:///home/shakil/Pictures/calm/"
INK, PAPER = "calm-ink", "calm-paper"
APPS = {  # theme → what follows it
    INK: {"icons": "calm-mono-dark", "scheme": "prefer-dark", "wallpaper": PICS + "kijani-night.jpeg"},
    PAPER: {"icons": "calm-mono-light", "scheme": "prefer-light", "wallpaper": PICS + "kijani-3x2.png"},
}
MODES = {"dark": (INK, INK), "light": (PAPER, PAPER), "mixed": (PAPER, INK)}  # (apps, desktop)

iface = Gio.Settings.new("org.cinnamon.desktop.interface")
gnome = Gio.Settings.new("org.gnome.desktop.interface")
shell = Gio.Settings.new("org.cinnamon.theme")
portal = Gio.Settings.new("org.x.apps.portal")
background = Gio.Settings.new("org.cinnamon.desktop.background")
_source = Gio.SettingsSchemaSource.get_default()
dock = (Gio.Settings.new_with_path("net.launchpad.plank.dock.settings", "/net/launchpad/plank/docks/dock1/")
        if _source.lookup("net.launchpad.plank.dock.settings", True) else None)


def put(settings, key, value):
    if settings.get_string(key) != value:  # only write real changes, so nothing loops
        settings.set_string(key, value)


def apps(theme):
    if theme not in APPS:
        return
    a = APPS[theme]
    for s in (iface, gnome):
        put(s, "gtk-theme", theme)
        put(s, "icon-theme", a["icons"])
    put(portal, "color-scheme", a["scheme"])
    put(background, "picture-uri", a["wallpaper"])
    put(background, "picture-options", "zoom")


def desktop(theme):
    if theme not in APPS:
        return
    put(shell, "name", theme)
    if dock:
        put(dock, "theme", theme)  # the dock themes share the names calm-ink / calm-paper


def apply(mode):
    a, d = MODES[mode]
    apps(a)
    desktop(d)


def current():
    pair = (iface.get_string("gtk-theme"), shell.get_string("name"))
    return next((m for m, p in MODES.items() if p == pair), "dark")


cmd = sys.argv[1] if len(sys.argv) > 1 else "watch"
if cmd == "watch":
    apps(iface.get_string("gtk-theme"))
    desktop(shell.get_string("name"))
    iface.connect("changed::gtk-theme", lambda s, k: apps(s.get_string(k)))
    shell.connect("changed::name", lambda s, k: desktop(s.get_string(k)))
    GLib.MainLoop().run()
elif cmd in MODES:
    apply(cmd)
elif cmd == "toggle":
    apply("light" if current() == "dark" else "dark")
else:
    sys.exit(__doc__)
Gio.Settings.sync()
