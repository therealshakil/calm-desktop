#!/usr/bin/env python3
"""calm-desktop: one switch for light and dark.

Pick calm-paper or calm-ink in Themes and everything follows: panel, icons, apps' colour scheme,
and the wallpaper (Kijani by day, Kijani at night).

    calm-mode.py watch    # runs at login; follows the theme
    calm-mode.py light | dark | toggle
"""
import sys

from gi.repository import Gio, GLib

PICS = "file:///home/shakil/Pictures/calm/"
MODES = {
    "dark": {"theme": "calm-ink", "icons": "Yaru-sage-dark", "scheme": "prefer-dark",
             "wallpaper": PICS + "kijani-night.jpeg"},
    "light": {"theme": "calm-paper", "icons": "Yaru-sage", "scheme": "prefer-light",
              "wallpaper": PICS + "kijani-3x2.png"},
}
THEME_TO_MODE = {m["theme"]: name for name, m in MODES.items()}

iface = Gio.Settings.new("org.cinnamon.desktop.interface")
gnome = Gio.Settings.new("org.gnome.desktop.interface")
shell = Gio.Settings.new("org.cinnamon.theme")
portal = Gio.Settings.new("org.x.apps.portal")
background = Gio.Settings.new("org.cinnamon.desktop.background")


def put(settings, key, value):
    if settings.get_string(key) != value:  # only write real changes, so nothing loops
        settings.set_string(key, value)


def apply(mode):
    m = MODES[mode]
    for s in (iface, gnome):
        put(s, "gtk-theme", m["theme"])
        put(s, "icon-theme", m["icons"])
    put(shell, "name", m["theme"])
    put(portal, "color-scheme", m["scheme"])
    put(background, "picture-uri", m["wallpaper"])
    put(background, "picture-options", "zoom")


def follow(settings, key):
    mode = THEME_TO_MODE.get(settings.get_string(key))
    if mode:
        apply(mode)


def current():
    return THEME_TO_MODE.get(iface.get_string("gtk-theme"), "dark")


cmd = sys.argv[1] if len(sys.argv) > 1 else "watch"
if cmd == "watch":
    apply(current())
    iface.connect("changed::gtk-theme", follow)
    shell.connect("changed::name", follow)
    GLib.MainLoop().run()
elif cmd in MODES:
    apply(cmd)
elif cmd == "toggle":
    apply("light" if current() == "dark" else "dark")
else:
    sys.exit(__doc__)
Gio.Settings.sync()
