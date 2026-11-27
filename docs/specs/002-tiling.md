# Spec 002 — Tiling in thirds

**Status:** draft proposal — waiting for Shakil to lock · **Date:** 2026-11-27 · **Scope:** this laptop

Put any window into a third, or two thirds, of the screen from the keyboard.
Cinnamon snaps to halves and quarters on its own, but not to thirds.

## The setup

| Part | Choice |
| --- | --- |
| Tool | gTile (`gTile@shuairan`), a Cinnamon extension from Cinnamon Spices |
| Shortcut | Super+G opens the grid; Escape closes it |
| Button | a grid icon on the top bar (`calm-tile@calm-desktop`) does the same as Super+G, through `xdotool` (apt) |
| Layout | layout 2 is "Thirds": three even columns, one row |
| Keys in the grid | arrows move, Shift+arrow widens to two thirds, Enter places |
| Gap | 8 px, even between windows and at the screen edges; none when maximised |
| Motion | gTile's animation off, like the rest of the desktop |

## How it's built

`tiling.py` installs gTile from Spices if it's missing.
It sets the Thirds layout and turns gTile on.
Cinnamon writes gTile's settings back while it runs, so the script edits them with gTile switched off.

gTile has no gap setting, so `gtile-gap-patch.py` adds one to its code.
It does nothing if the gap is already there.
A systemd user watcher (`systemd/gtile-gap-patch.path`) runs it whenever an update replaces gTile, and once at login.
If an update reshapes gTile past patching, a quiet notification says so and tiling carries on without the gap.

## Considered

- Cinnamon's own snapping: halves and quarters only.
- A tiling window manager (i3 and the like): powerful, but it changes how every window behaves.
- A script per third on its own key: fewer keys to learn, but a fresh tool to keep.

## Constitution Check

1. **Serves:** I (a key, a glance, done), IX (Cinnamon stays; one small extension).
2. **Violates:** none. Two additions, chosen by Shakil: gTile (GPL, from Cinnamon's own Spices site) and xdotool (Ubuntu's archive) for the top-bar button. The gap patch is local and undoes by switching the watcher off.
3. **Subtracts:** dragging and resizing windows by hand.
4. **Calm:** no motion, gTile's animation off; a failed patch is a quiet note, never an alarm.
