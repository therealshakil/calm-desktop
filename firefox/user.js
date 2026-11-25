// calm-desktop: Firefox prefs, read at every start. Linked into the profile, so editing here is enough.
// Delete a line (or this file's link) and restart to undo it.

// The chrome takes its colours from the GTK theme (calm-ink / calm-paper) via "System theme — auto".
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true); // allow calm-firefox's userChrome.css

// Still the motion (calm-firefox spec 001).
user_pref("ui.prefersReducedMotion", 1);
user_pref("toolkit.cosmeticAnimations.enabled", false);

// No AI. Same switch as Settings > AI Controls > "Block AI enhancements" (Firefox 148+).
user_pref("browser.ai.control.default", "blocked");
user_pref("browser.ml.chat.enabled", false);

// No nags, no sponsored rows (calm-firefox spec 002).
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("browser.urlbar.suggest.quicksuggest.sponsored", false);
user_pref("browser.urlbar.suggest.quicksuggest.nonsponsored", false);
user_pref("browser.newtabpage.activity-stream.showSponsored", false);
user_pref("browser.newtabpage.activity-stream.showSponsoredTopSites", false);
user_pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);
