#!/bin/sh
# calm-desktop: calm the login screen (slick-greeter).
# The greeter runs as its own user and can't see into /home, so the calm pieces are copied to system folders.
# Run once with sudo, and again after rebuilding the themes. To undo: sudo rm /etc/lightdm/slick-greeter.conf
set -e

# The theme, the face and the night wallpaper, where the greeter can read them.
rm -rf /usr/share/themes/calm-ink
cp -r /home/shakil/.themes/calm-ink /usr/share/themes/calm-ink
mkdir -p /usr/local/share/fonts/atkinson-hyperlegible
cp /home/shakil/.local/share/fonts/atkinson-hyperlegible/AtkinsonHyperlegible-Regular.ttf /home/shakil/.local/share/fonts/atkinson-hyperlegible/AtkinsonHyperlegible-Bold.ttf /home/shakil/.local/share/fonts/atkinson-hyperlegible/OFL.txt /usr/local/share/fonts/atkinson-hyperlegible/
fc-cache -f /usr/local/share/fonts
mkdir -p /usr/share/backgrounds/calm
cp /home/shakil/Pictures/calm/kijani-night.jpeg /usr/share/backgrounds/calm/kijani-night.jpeg
chmod -R a+rX /usr/share/themes/calm-ink /usr/local/share/fonts/atkinson-hyperlegible /usr/share/backgrounds/calm

# The greeter: calm-ink, Atkinson, the night wallpaper; no hostname in the bar.
cat > /etc/lightdm/slick-greeter.conf <<'EOF'
[Greeter]
theme-name=calm-ink
icon-theme-name=Mint-Y-Grey
font-name=Atkinson Hyperlegible 11
background=/usr/share/backgrounds/calm/kijani-night.jpeg
background-color=#0E0C0A
draw-user-backgrounds=false
draw-grid=false
show-hostname=false
clock-format=%H:%M
EOF

echo "The login screen is calm. You'll see it at your next login."
