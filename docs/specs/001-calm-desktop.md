# Spec 001 — Calm Cinnamon

**Status:** locked — Shakil confirmed path A on 2026-11-25 ("confirmed, lets go") · **Scope:** this laptop

The calm desktop for one Mint laptop.
Keep Cinnamon, take things off it, and dress what's left in ink and paper.

## Why

The desktop is the surface under every other calm tool.
Researched and debated by the calm council on 2026-11-25
([the options page](https://claude.ai/artifact/MfTzQd1fdA17viE8TJwXm3)).
All five lenses chose to subtract rather than swap.
A new desktop is a future repair job, and breakage costs more calm than looks can repay.
Mint 23 keeps Cinnamon on X11 as its default, so this rides the next upgrade.

## The setup

| Part | Choice |
| --- | --- |
| Desktop and WM | Cinnamon on X11, effects and animations off |
| Theme | calm-ink (default) and calm-paper, rebuilt from Mint-Y |
| Icons | Yaru sage (dark): muted folders with a sage tab that echoes Kijani (chosen 2026-11-25) |
| Type | Atkinson Hyperlegible, interface and titles |
| Top bar | slim, macOS-like: menu left; tray, status and "Wed 25 Nov  23:45" right; no window list |
| Dock | Plank Reloaded (official apt repo), centred and floating, calm-ink / calm-paper; no zoom, bounce, glow or badges; steps aside for windows (chosen 2026-11-25) |
| Notifications | small calm popups: 22em wide, thin border, no accent bar, short shadow |
| Desktop | Kijani by day, Kijani at night; no icons |
| Light and dark | pick calm-paper or calm-ink in Themes; calm-mode.py flips wallpaper, icons, panel and apps to match |
| Files | Nemo, list view, less chrome |
| Browser | Firefox, AI blocked, compact two-row chrome (Brave-like), tabs restored on start |
| Start page | the search box alone, on calm ink or paper (calm-firefox userContent) |
| Terminal | Ghostty, already calm |

## How it's built

The themes are generated, not hand-edited.
`build-themes.py` maps every colour in Mint-Y onto calm's warm ink-on-paper ramp by brightness.
Reds and oranges become the one clay accent; every other hue falls to ink.
After a Mint upgrade, `apply.sh` rebuilds against the new Mint-Y and replays every setting.

## Set aside

- niri: the calmest shape, but a bare compositor to assemble and maintain. Revisit after Mint 23.
- COSMIC: on Mint only via an unofficial PPA that replaces core packages.
- GNOME, KDE, Xfce: extension churn, a settings timesink, and a sideways move.
- LibreWolf: needs a third-party repo; Firefox now blocks AI itself.

## Open

- Brave stays installed for now; the WhatsApp web app still lives in it.
- calm-firefox's selectors are unverified on Firefox 161 — a stale one fails safe.

## Constitution Check

1. **Serves:** VI (calm over alarm: no badges, no red, small quiet popups), IX (nothing new to maintain), I (a desktop to glance past).
2. **Violates:** none. Two additions, each chosen by Shakil: one user font from Google Fonts' own repo, and Plank Reloaded from its official, actively maintained apt repo (X11 only; Mint stays X11 by default).
3. **Subtracts:** five applets, desktop icons, every animation, a third of each popup, Brave as default.
4. **Calm:** every step undoes with one dconf load; Timeshift snapshots nightly; motion off everywhere.
