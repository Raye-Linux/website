// The signup form without a page reload, and the language switch memory.
// The form still works with scripts off: it posts to /api/subscribe and
// the server answers with a page.
(function () {
  "use strict";

  var lang = document.documentElement.lang === "en" ? "en" : "fr";

  var TEXT = {
    fr: {
      email: "Entrez une adresse courriel valide, par exemple vous@exemple.com.",
      consent: "Cochez la case pour accepter de recevoir le courriel de lancement.",
      sending: "Envoi…",
      network: "Impossible de joindre le serveur. Vérifiez votre connexion, puis réessayez.",
      doneTitle: "Vérifiez votre boîte de réception",
      doneText: "Si l'adresse est valide, un courriel de confirmation est en route. "
        + "Cliquez sur son lien pour finaliser l'inscription. Rien reçu d'ici "
        + "quelques minutes ? Regardez dans les indésirables."
    },
    en: {
      email: "Enter a valid email address, for example you@example.com.",
      consent: "Tick the box to agree to get the launch email.",
      sending: "Sending…",
      network: "Can't reach the server. Check your connection, then try again.",
      doneTitle: "Check your inbox",
      doneText: "If the address is valid, a confirmation email is on its way. "
        + "Click its link to finish signing up. Nothing after a few minutes? "
        + "Have a look in your spam folder."
    }
  }[lang];

  // same local part the server accepts (letters, digits, . _ + -); the
  // domain is left loose here, the server has the last word
  var EMAIL = /^(?=.{1,64}@)[A-Za-z0-9_+-]+(?:\.[A-Za-z0-9_+-]+)*@[^\s@]{1,251}\.[^\s@.]{2,}$/;

  document.addEventListener("click", function (event) {
    var link = event.target.closest && event.target.closest("[data-set-lang]");
    if (!link) return;
    try { window.localStorage.setItem("raye-lang", link.getAttribute("data-set-lang")); }
    catch (e) { /* storage off: the link still works */ }
  });

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var form = document.getElementById("signup-form");
    if (!form || !window.fetch) return;
    var email = form.elements.email;
    var consent = form.elements.consent;
    var button = form.querySelector("button[type=submit]");
    var msg = document.getElementById("form-msg");

    function say(text, kind) {
      msg.textContent = text;
      msg.className = "form-msg" + (kind ? " " + kind : "");
    }

    function invalid(field, text) {
      field.setAttribute("aria-invalid", "true");
      say(text, "error");
      field.focus();
    }

    function clear(field) { field.removeAttribute("aria-invalid"); }
    email.addEventListener("input", function () { clear(email); });
    consent.addEventListener("change", function () { clear(consent); });

    function done() {
      var box = form.parentNode;
      while (box.firstChild) box.removeChild(box.firstChild);
      var wrap = document.createElement("div");
      wrap.className = "done";
      wrap.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        + 'stroke-width="1.8" aria-hidden="true" focusable="false"><circle cx="12" cy="12" '
        + 'r="9.5"/><path d="M7.8 12.3l2.8 2.8 5.6-5.8"/></svg>';
      var text = document.createElement("div");
      var h = document.createElement("h2");
      h.id = "signup-title";
      h.textContent = TEXT.doneTitle;
      var p = document.createElement("p");
      p.textContent = TEXT.doneText;
      p.setAttribute("role", "status");
      text.appendChild(h);
      text.appendChild(p);
      wrap.appendChild(text);
      box.appendChild(wrap);
      var section = document.getElementById("signup");
      if (section) section.focus();
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      try {
        send();
      } catch (err) {
        // a script error must never leave the button dead: post the plain way
        button.disabled = false;
        form.submit();
      }
    });

    function send() {
      var value = email.value.trim();
      if (!EMAIL.test(value) || value.length > 254) return invalid(email, TEXT.email);
      if (!consent.checked) return invalid(consent, TEXT.consent);

      var body = {
        email: value,
        lang: lang,
        consent: true,
        website: form.elements.website.value
      };
      button.disabled = true;
      say(TEXT.sending, "");
      fetch(form.action, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(body),
        credentials: "omit"
      }).then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (data) {
          return { status: res.status, data: data };
        });
      }).then(function (r) {
        button.disabled = false;
        if (r.status === 200 && r.data.ok) return done();
        if (r.data.error === "email") return invalid(email, r.data.message || TEXT.email);
        if (r.data.error === "consent") return invalid(consent, r.data.message || TEXT.consent);
        say(r.data.message || TEXT.network, "error");
      }).catch(function () {
        button.disabled = false;
        say(TEXT.network, "error");
      });
    }
  });
})();

// The screenshot tabs. Without scripts the tabs are plain links and every
// screenshot is shown one under the other; with them, one at a time, and the
// arrow keys move between tabs (WAI-ARIA tabs pattern).
(function () {
  "use strict";

  function setup(box) {
    var list = box.querySelector(".shot-tabs");
    var tabs = Array.prototype.slice.call(box.querySelectorAll("[data-tab]"));
    var panels = Array.prototype.slice.call(box.querySelectorAll("[data-panel]"));
    if (!list || !tabs.length || tabs.length !== panels.length) return;

    list.setAttribute("role", "tablist");
    tabs.forEach(function (tab, i) {
      tab.parentNode.setAttribute("role", "presentation");
      tab.setAttribute("role", "tab");
      tab.setAttribute("aria-controls", panels[i].id);
      panels[i].setAttribute("role", "tabpanel");
      panels[i].setAttribute("aria-labelledby", tab.id);
    });

    function select(n, focus) {
      tabs.forEach(function (tab, i) {
        var on = i === n;
        tab.setAttribute("aria-selected", on ? "true" : "false");
        tab.setAttribute("tabindex", on ? "0" : "-1");
        if (on) panels[i].removeAttribute("hidden");
        else panels[i].setAttribute("hidden", "");
      });
      if (focus) tabs[n].focus();
    }

    list.addEventListener("click", function (event) {
      var tab = event.target.closest && event.target.closest("[data-tab]");
      if (!tab) return;
      event.preventDefault();
      select(tabs.indexOf(tab), false);
    });

    list.addEventListener("keydown", function (event) {
      var now = tabs.indexOf(document.activeElement);
      if (now < 0) return;
      var next = { ArrowRight: now + 1, ArrowLeft: now - 1, Home: 0, End: tabs.length - 1 }[event.key];
      if (next === undefined) return;
      event.preventDefault();
      select((next + tabs.length) % tabs.length, true);
    });

    box.classList.add("is-tabs");
    select(0, false);
  }

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    Array.prototype.forEach.call(document.querySelectorAll("[data-tabs]"), setup);
  });
})();

// Public beta: the download only starts once the warnings are accepted.
// With scripts on, they open in a dialog; with scripts off, the download
// button leads to the same warnings on the page, and the link is under them.
(function () {
  "use strict";
  var box = document.getElementById("accept");
  if (!box) return;
  var check = document.getElementById("accept-check");
  var go = box.querySelector(".dl-go");
  var cancel = box.querySelector(".dl-cancel");
  function sync() { go.setAttribute("aria-disabled", check.checked ? "false" : "true"); }
  check.addEventListener("change", sync);
  go.addEventListener("click", function (e) {
    if (!check.checked) { e.preventDefault(); check.focus(); }
  });
  sync();
  if (typeof HTMLDialogElement !== "function") return;
  var home = box.parentNode, next = box.nextSibling;
  var dialog = document.createElement("dialog");
  dialog.className = "dl-dialog";
  dialog.setAttribute("aria-labelledby", "accept-title");
  document.body.appendChild(dialog);
  function close() { if (dialog.open) dialog.close(); }
  dialog.addEventListener("close", function () {
    home.insertBefore(box, next); cancel.hidden = true;
  });
  cancel.addEventListener("click", close);
  go.addEventListener("click", function () { if (check.checked) setTimeout(close, 0); });
  Array.prototype.forEach.call(document.querySelectorAll("[data-accept]"), function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      dialog.appendChild(box); cancel.hidden = false; dialog.showModal(); check.focus();
    });
  });
})();

// Downloads and active PCs: the page is built with the numbers of its last
// deploy, then /stats.json (refreshed every hour by the lab) updates them.
// On arrival the numbers count up; when one goes up later, a small "+N"
// shows next to it. No motion for people who asked for less of it.
(function () {
  "use strict";
  var cells = document.querySelectorAll("[data-stat]");
  if (!cells.length || !window.fetch) return;
  var fr = document.documentElement.lang.indexOf("fr") === 0;
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var num = new Intl.NumberFormat(fr ? "fr-CA" : "en-US");
  var shown = {};
  cells.forEach(function (el) {
    var k = el.getAttribute("data-stat");
    if (k !== "date") shown[k] = parseInt(el.textContent.replace(/\D/g, ""), 10) || 0;
  });

  function count(el, from, to, ms) {
    if (still || from === to) { el.textContent = num.format(to); return; }
    var t0 = null;
    function step(t) {
      if (t0 === null) t0 = t;
      var p = Math.min(1, (t - t0) / ms), e = 1 - Math.pow(1 - p, 3);
      el.textContent = num.format(Math.round(from + (to - from) * e));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
    // the last value is written even if frames stop (hidden tab, slow PC)
    setTimeout(function () { el.textContent = num.format(to); }, ms + 150);
  }

  function bump(el, n) {
    if (still) return;
    var b = document.createElement("span");
    b.className = "stat-bump"; b.setAttribute("aria-hidden", "true");
    b.textContent = "+" + num.format(n);
    el.appendChild(b);
    setTimeout(function () { b.remove(); }, 2400);
  }

  function apply(s, first) {
    cells.forEach(function (el) {
      var k = el.getAttribute("data-stat");
      if (k === "date") {
        el.textContent = new Date(s.date + "T12:00:00Z").toLocaleDateString(fr ? "fr-CA" : "en-US",
          { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" });
        return;
      }
      if (typeof s[k] !== "number") return;
      var old = shown[k];
      if (first) {
        count(el, 0, s[k], 900);
        if (s[k] > old) setTimeout(function () { bump(el, s[k] - old); }, 950);
      } else if (s[k] !== old) {
        count(el, old, s[k], 600);
        if (s[k] > old) bump(el, s[k] - old);
      }
      shown[k] = s[k];
    });
  }

  function load(first) {
    fetch("/stats.json?t=" + Date.now(), { cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (s) { if (s) apply(s, first); })
      .catch(function () {});
  }
  load(true);
  setInterval(function () { if (!document.hidden) load(false); }, 120000);
})();
