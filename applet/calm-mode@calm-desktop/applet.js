// calm-desktop: light, mixed, or dark, from the top bar.
// The menu only asks calm-mode.py to switch; it reads the two themes back to show where you are.
const Applet = imports.ui.applet;
const PopupMenu = imports.ui.popupMenu;
const Util = imports.misc.util;
const Gio = imports.gi.Gio;

const SCRIPT = "/home/shakil/Projects/calm-desktop/calm-mode.py";
const MODES = [  // [mode, label, icon, apps theme, desktop theme]
    ["light", "Light", "weather-clear-symbolic", "calm-paper", "calm-paper"],
    ["mixed", "Mixed", "weather-few-clouds-symbolic", "calm-paper", "calm-ink"],
    ["dark", "Dark", "weather-clear-night-symbolic", "calm-ink", "calm-ink"],
];

class CalmMode extends Applet.IconApplet {
    constructor(orientation, panelHeight, instanceId) {
        super(orientation, panelHeight, instanceId);
        this.iface = new Gio.Settings({ schema_id: "org.cinnamon.desktop.interface" });
        this.shell = new Gio.Settings({ schema_id: "org.cinnamon.theme" });

        this.menuManager = new PopupMenu.PopupMenuManager(this);
        this.menu = new Applet.AppletPopupMenu(this, orientation);
        this.menuManager.addMenu(this.menu);
        this.items = {};
        for (const [mode, label] of MODES) {
            const item = new PopupMenu.PopupMenuItem(label);
            item.connect("activate", () => Util.spawn(["python3", "-I", SCRIPT, mode]));
            this.menu.addMenuItem(item);
            this.items[mode] = item;
        }

        this.ids = [
            [this.iface, this.iface.connect("changed::gtk-theme", () => this.refresh())],
            [this.shell, this.shell.connect("changed::name", () => this.refresh())],
        ];
        this.refresh();
    }

    refresh() {
        const apps = this.iface.get_string("gtk-theme");
        const desktop = this.shell.get_string("name");
        const now = MODES.find((m) => m[3] === apps && m[4] === desktop);
        for (const [mode] of MODES) {
            const on = now !== undefined && now[0] === mode;
            this.items[mode].setOrnament(PopupMenu.OrnamentType.DOT, on);
        }
        this.set_applet_icon_symbolic_name(now ? now[2] : "weather-few-clouds-symbolic");
        this.set_applet_tooltip(now ? "Theme: " + now[1] : "Theme: your own mix");
    }

    on_applet_clicked() {
        this.menu.toggle();
    }

    on_applet_removed_from_panel() {
        for (const [settings, id] of this.ids) settings.disconnect(id);
    }
}

function main(metadata, orientation, panelHeight, instanceId) {
    return new CalmMode(orientation, panelHeight, instanceId);
}
