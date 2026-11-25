#!/bin/sh
# calm-desktop: install Plank Reloaded from its official apt repository (README, zquestz/plank-reloaded).
# Run once with sudo. Updates then arrive through apt with everything else.
set -e
apt-get remove -y plank libplank-common libplank1 2>/dev/null || true
curl -fsSL https://zquestz.github.io/ppa/ubuntu/KEY.gpg | gpg --dearmor --yes -o /usr/share/keyrings/zquestz-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/zquestz-archive-keyring.gpg] https://zquestz.github.io/ppa/ubuntu ./" > /etc/apt/sources.list.d/zquestz.list
apt-get update
apt-get install -y plank-reloaded
echo "Plank Reloaded is installed."
