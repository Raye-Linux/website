// Runs before the page draws: send visitors whose browser is not in French
// to the English page, unless they already picked a language with the switch.
// Written by tools/site_v1.py from the list of pages.
(function () {
  "use strict";
  var MAP = {
    "/": "/en/",
    "/bureau/": "/en/desktop/",
    "/programmes-windows/": "/en/windows-programs/",
    "/mises-a-jour/": "/en/updates/",
    "/securite/": "/en/security/",
    "/materiel/": "/en/hardware/",
    "/installer/": "/en/install/",
    "/questions/": "/en/questions/",
    "/versions/": "/en/releases/",
    "/a-propos/": "/en/about/",
    "/confidentialite/": "/en/privacy/",
    "/telecharger/": "/en/download/"
  };
  var target = MAP[window.location.pathname];
  if (!target) return;
  var choice = null;
  try { choice = window.localStorage.getItem("raye-lang"); } catch (e) { /* storage off */ }
  if (choice === "fr") return;
  if (choice !== "en") {
    var langs = navigator.languages && navigator.languages.length
      ? navigator.languages : [navigator.language || "fr"];
    for (var i = 0; i < langs.length; i++) {
      if (/^fr\b/i.test(String(langs[i]))) return;
    }
  }
  window.location.replace(target + window.location.search + window.location.hash);
})();
