#!/bin/sh
# calm-desktop: apply the calm desktop to this Mint Cinnamon laptop.
# Safe to run again (after a Mint upgrade or a reinstall). Every line is one plain setting.
# To undo everything: dconf load /org/cinnamon/ < docs/cinnamon-before-2026-11-25.dconf

# 1. Themes: rebuild calm-paper and calm-ink from this Mint's own Mint-Y.
python3 -I /home/shakil/Projects/calm-desktop/build-themes.py

# 2. Look: calm-ink by default; calm-paper is there for bright days.
gsettings set org.cinnamon.desktop.interface gtk-theme 'calm-ink'
gsettings set org.gnome.desktop.interface gtk-theme 'calm-ink'
gsettings set org.cinnamon.theme name 'calm-ink'
python3 -I /home/shakil/Projects/calm-desktop/calm-icons.py
python3 -I /home/shakil/Projects/calm-desktop/build-icons.py
gsettings set org.cinnamon.desktop.interface icon-theme 'calm-mono-dark'
gsettings set org.gnome.desktop.interface icon-theme 'calm-mono-dark'
gsettings set org.cinnamon.desktop.background picture-uri 'file:///home/shakil/Pictures/calm/kijani-3x2.png'
gsettings set org.cinnamon.desktop.background picture-options 'zoom'

# 3. Type: Atkinson Hyperlegible (user font, ~/.local/share/fonts/atkinson-hyperlegible).
gsettings set org.cinnamon.desktop.interface font-name 'Atkinson Hyperlegible 10'
gsettings set org.gnome.desktop.interface font-name 'Atkinson Hyperlegible 10'
gsettings set org.gnome.desktop.interface document-font-name 'Atkinson Hyperlegible 10'
gsettings set org.cinnamon.desktop.wm.preferences titlebar-font 'Atkinson Hyperlegible Bold 10'
gsettings set org.nemo.desktop font 'Atkinson Hyperlegible 10'

# 4. Stillness: no effects, no animations.
gsettings set org.cinnamon desktop-effects false
gsettings set org.cinnamon desktop-effects-workspace false
gsettings set org.cinnamon desktop-effects-on-menus false
gsettings set org.cinnamon desktop-effects-on-dialogs false
gsettings set org.cinnamon desktop-effects-change-size false
gsettings set org.cinnamon startup-animation false
gsettings set org.cinnamon.desktop.interface enable-animations false
gsettings set org.gnome.desktop.interface enable-animations false

# 5. Quiet: small calm notification popups (styled in build-themes.py); nothing on the desktop; a trimmed panel.
gsettings set org.cinnamon.desktop.notifications display-notifications true
gsettings set org.nemo.desktop show-desktop-icons false
python3 -I /home/shakil/Projects/calm-desktop/quiet-applets.py

# 5b. macOS-like layout: slim top bar and a centred Plank Reloaded dock.
# Needs Plank Reloaded installed once: sudo sh /home/shakil/Projects/calm-desktop/install-plank.sh
python3 -I /home/shakil/Projects/calm-desktop/calm-dock.py

# 5c. Lock screen: the clock stays still, in calm's face; no notification count, no album art.
gsettings set org.cinnamon.desktop.screensaver floating-widgets false
gsettings set org.cinnamon.desktop.screensaver show-info-panel false
gsettings set org.cinnamon.desktop.screensaver show-album-art false
gsettings set org.cinnamon.desktop.screensaver font-time 'Atkinson Hyperlegible 56'
gsettings set org.cinnamon.desktop.screensaver font-date 'Atkinson Hyperlegible 18'
gsettings set org.cinnamon.desktop.screensaver font-message 'Atkinson Hyperlegible 12'
gsettings set org.cinnamon.desktop.screensaver date-format '%A %-e %B'

# 5d. Login screen: slick-greeter can't read /home, so it needs the calm pieces copied out once.
# Run with sudo, and again after rebuilding the themes: sudo sh /home/shakil/Projects/calm-desktop/login-screen.sh

# 5e. Tiling: gTile, with an even-thirds layout and an 8 px gap kept in place across gTile updates.
# Super+G opens the grid; 2 picks Thirds. Spec: docs/specs/002-tiling.md
python3 -I /home/shakil/Projects/calm-desktop/tiling.py
mkdir -p /home/shakil/.config/systemd/user
ln -sf /home/shakil/Projects/calm-desktop/systemd/gtile-gap-patch.path /home/shakil/.config/systemd/user/gtile-gap-patch.path
ln -sf /home/shakil/Projects/calm-desktop/systemd/gtile-gap-patch.service /home/shakil/.config/systemd/user/gtile-gap-patch.service
systemctl --user daemon-reload
systemctl --user enable --now gtile-gap-patch.path gtile-gap-patch.service
# A grid button on the top bar does the same as Super+G. Needs xdotool once: pkexec apt install -y xdotool
python3 -I /home/shakil/Projects/calm-desktop/calm-applet.py calm-tile@calm-desktop

# 6. Files: Nemo in list view, with less chrome.
gsettings set org.nemo.preferences default-folder-viewer 'list-view'
gsettings set org.nemo.window-state start-with-menu-bar false
gsettings set org.nemo.window-state start-with-status-bar false
gsettings set org.nemo.window-state network-expanded false
gsettings set org.nemo.preferences show-compact-view-icon-toolbar false
gsettings set org.nemo.preferences show-icon-view-icon-toolbar false
gsettings set org.nemo.preferences show-list-view-icon-toolbar false
gsettings set org.nemo.preferences show-edit-icon-toolbar false

# 7. Light and dark: calm-mode follows the theme (wallpaper, icons, panel, apps) from login onward.
mkdir -p /home/shakil/.config/autostart
ln -sf /home/shakil/Projects/calm-desktop/autostart/calm-mode.desktop /home/shakil/.config/autostart/calm-mode.desktop
python3 -I /home/shakil/Projects/calm-desktop/calm-applet.py

# 8. Browser: Firefox, linked to calm-firefox's prefs and stylesheets (restart Firefox after).
# calm-firefox is its own repo (it serves any Firefox); fetch it if it isn't here, else bring it up to date.
if [ -d /home/shakil/Projects/calm-firefox/.git ]; then
  git -C /home/shakil/Projects/calm-firefox pull --ff-only
else
  git clone https://github.com/therealshakil/calm-firefox.git /home/shakil/Projects/calm-firefox
fi
xdg-settings set default-web-browser firefox.desktop
mkdir -p /home/shakil/.mozilla/firefox/snmwf616.default-release/chrome
ln -sf /home/shakil/Projects/calm-firefox/user.js /home/shakil/.mozilla/firefox/snmwf616.default-release/user.js
ln -sf /home/shakil/Projects/calm-firefox/chrome/userChrome.css /home/shakil/.mozilla/firefox/snmwf616.default-release/chrome/userChrome.css
ln -sf /home/shakil/Projects/calm-firefox/chrome/userContent.css /home/shakil/.mozilla/firefox/snmwf616.default-release/chrome/userContent.css
