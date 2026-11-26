```
   calm · desktop
   ink on paper, all the way down
```

The calm desktop for a Linux Mint Cinnamon laptop.
Cinnamon stays; what's left on it is quiet, still, and dressed in calm's ink and paper.

Part of the calm suite — it inherits calm's Constitution, identity, and voice (see [`CLAUDE.md`](./CLAUDE.md)).

## What it does

Two themes, calm-ink and calm-paper, rebuilt from Mint's own Mint-Y.
Atkinson Hyperlegible across the interface.
No animations, no badges, small quiet notification popups, nothing on the desktop but the Kijani wallpaper.
Nemo with less chrome, and Firefox with AI blocked and calm-firefox's declutter.
A macOS-like layout: a slim top bar and a centred Plank Reloaded dock, both in ink or paper.

The decision behind it: [`docs/specs/001-calm-desktop.md`](./docs/specs/001-calm-desktop.md).

## Use

The dock needs Plank Reloaded, installed once from its official repository:

```sh
sudo sh /home/shakil/Projects/calm-desktop/install-plank.sh
```

Then run this once, and again after a Mint upgrade or a reinstall:

```sh
sh /home/shakil/Projects/calm-desktop/apply.sh
```

Then restart Firefox so it reads its calm prefs.

Light, mixed, or dark: click the sun-and-moon switch on the top bar.
Mixed is paper apps under an ink top bar and dock; calm-ink is the default.
The apps half carries the wallpaper (Kijani by day or at night), icons, and apps' colour scheme;
the desktop half carries the top bar and the dock.
The Themes window works too, and each half follows its own setting.
Or switch from a terminal:

```sh
python3 -I /home/shakil/Projects/calm-desktop/calm-mode.py mixed
```

## Undo

Every Cinnamon setting goes back with one line:

```sh
dconf load /org/cinnamon/ < /home/shakil/Projects/calm-desktop/docs/cinnamon-before-2026-11-25.dconf
```

Timeshift also takes a snapshot every evening, so nothing here is out of reach.
