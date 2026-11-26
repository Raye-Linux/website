// rayelinux.com, V1 pages: the "Join the team" form and the live numbers of
// the Community page. Both talk to our own server only (/api/join,
// /api/community); nothing is loaded from elsewhere. Without this script the
// form still works (a plain POST answered by a page) and the Community page
// still has its button.
// Source: tools/site_v1.js, copied to assets/v1.js by site_v1.py.
(function () {
  "use strict";
  if (!window.fetch || !document.querySelector) return;

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  // which field an answer of /api/join is about
  var FIELD = { email: "email", discord: "discord", why_short: "why", links: "why",
    languages: "languages", consent: "consent", account: "email",
    account_unavailable: "email" };

  function setupForm(form) {
    var button = form.querySelector("button[type=submit]");
    var msg = document.getElementById("join-msg");
    var label = button.textContent;

    function clearErrors() {
      Array.prototype.forEach.call(form.querySelectorAll("[data-err-for]"), function (p) {
        p.textContent = "";
      });
      Array.prototype.forEach.call(form.querySelectorAll("[aria-invalid]"), function (el) {
        el.removeAttribute("aria-invalid");
      });
    }

    function fail(code, text) {
      var name = FIELD[code];
      var input = name && form.elements[name];
      var slot = name && form.querySelector('[data-err-for="' + name + '"]');
      if (input && slot) {
        slot.textContent = text;
        input.setAttribute("aria-invalid", "true");
        input.focus();
        msg.textContent = "";
        msg.className = "form-msg";
      } else {
        msg.textContent = text;
        msg.className = "form-msg error";
      }
    }

    function done(data) {
      var box = document.createElement("div");
      box.className = "done";
      box.setAttribute("tabindex", "-1");
      var h = document.createElement("h3");
      h.textContent = form.getAttribute("data-done");
      var p = document.createElement("p");
      p.textContent = data.message || "";
      box.appendChild(h);
      box.appendChild(p);
      if (data.reference) {
        var ref = document.createElement("p");
        ref.className = "small";
        ref.textContent = msg.getAttribute("data-ref") + " : " + data.reference;
        box.appendChild(ref);
      }
      form.parentNode.replaceChild(box, form);
      box.focus();
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      clearErrors();
      var data = {};
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name) return;
        data[el.name] = el.type === "checkbox" ? el.checked : el.value;
      });
      button.disabled = true;
      button.textContent = button.getAttribute("data-sending");
      fetch(form.getAttribute("action"), {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data),
        credentials: "same-origin"
      }).then(function (res) {
        return res.json().catch(function () { return {}; });
      }).then(function (reply) {
        if (reply.ok) return done(reply);
        fail(reply.error, reply.message || msg.getAttribute("data-failed"));
      }).catch(function () {
        fail(null, msg.getAttribute("data-failed"));
      }).then(function () {
        button.disabled = false;
        button.textContent = label;
      });
    });
  }

  function setupCommunity(box) {
    fetch("/api/community", { headers: { "Accept": "application/json" } })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (!data || !data.ok) return;
        var fmt = function (n) {
          try { return n.toLocaleString(document.documentElement.lang); } catch (e) { return String(n); }
        };
        box.querySelector("[data-members]").textContent = fmt(data.members);
        box.querySelector("[data-online]").textContent = fmt(data.online);
        Array.prototype.forEach.call(box.querySelectorAll("[data-live-count]"), function (el) {
          el.hidden = false;
        });
        box.querySelector("[data-live-wait]").hidden = true;
      })
      .catch(function () { /* the wait text stays: the button still works */ });
  }

  ready(function () {
    var form = document.getElementById("join-form");
    if (form) setupForm(form);
    var live = document.querySelector("[data-community]");
    if (live) setupCommunity(live);
  });
})();
