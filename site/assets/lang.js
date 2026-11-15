// The bare rayelinux.com has no language of its own. Runs before the page
// draws: a language picked with the switch wins, then the first language of
// the browser we have; anything else gets English.
(function () {
  "use strict";
  var HOMES = { fr: "/fr/", en: "/en/" };
  var target = null;
  var choice = null;
  try { choice = window.localStorage.getItem("raye-lang"); } catch (e) { /* storage off */ }
  if (HOMES.hasOwnProperty(choice)) target = HOMES[choice];
  if (!target) {
    var langs = navigator.languages && navigator.languages.length
      ? navigator.languages : [navigator.language || ""];
    for (var i = 0; i < langs.length && !target; i++) {
      var code = String(langs[i]).toLowerCase().split("-")[0];
      if (HOMES.hasOwnProperty(code)) target = HOMES[code];
    }
  }
  window.location.replace((target || HOMES.en) + window.location.search + window.location.hash);
})();
