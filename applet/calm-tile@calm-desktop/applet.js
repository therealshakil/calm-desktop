// calm-desktop: open gTile's grid from the top bar, same as Super+G.
// Clicking the bar leaves focus on your window, so the grid opens for that window.
const Applet = imports.ui.applet;
const Util = imports.misc.util;

class CalmTile extends Applet.IconApplet {
    constructor(orientation, panelHeight, instanceId) {
        super(orientation, panelHeight, instanceId);
        this.set_applet_icon_symbolic_name("view-grid-symbolic");
        this.set_applet_tooltip("Tile this window (Super+G)");
    }

    on_applet_clicked() {
        Util.spawn(["xdotool", "key", "--clearmodifiers", "super+g"]);
    }
}

function main(metadata, orientation, panelHeight, instanceId) {
    return new CalmTile(orientation, panelHeight, instanceId);
}
