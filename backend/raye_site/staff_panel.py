"""The three files of the staff panel page. They hold no data and no secret:
the token is typed by the person and kept in the tab (sessionStorage) only.
Everything the script writes in the page goes through textContent."""

HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>Raye Team panel</title>
<link rel="stylesheet" href="/api/staff/panel.css">
</head><body>
<header><h1>Raye Team panel</h1><p id="who" class="muted"></p></header>
<main>
<section id="login">
<form id="login-form" autocomplete="off">
<p>This panel is for the Raye Team. Give your name and the staff token.</p>
<label>Your name <input id="name" required minlength="3" maxlength="40"></label>
<label>Staff token <input id="token" type="password" required></label>
<button type="submit">Sign in</button>
<p id="login-error" role="alert" class="error"></p>
</form></section>
<section id="app" hidden>
<nav id="tabs" aria-label="Lists"></nav>
<div class="cols">
<div><h2>Applications</h2><ul id="list" class="list"></ul><p id="empty" class="muted" hidden>Nothing here.</p></div>
<div id="detail" aria-live="polite"><p class="muted">Pick an application.</p></div>
</div>
<details id="logbox"><summary>Action log</summary><ol id="log"></ol></details>
<p><button id="signout" type="button">Sign out</button></p>
</section></main>
<script src="/api/staff/panel.js"></script>
</body></html>
"""

CSS = """
:root{color-scheme:dark;--bg:#0f1220;--card:#181c30;--line:#2b3150;--fg:#e8eaf6;--mute:#9aa3c7;--acc:#7aa2ff;--bad:#ff8a8a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif}
header,main{max-width:1100px;margin:0 auto;padding:12px 16px}h1{font-size:1.3rem;margin:0}h2{font-size:1.05rem}
.muted{color:var(--mute)}.error{color:var(--bad);min-height:1.5em}
label{display:block;margin:10px 0}input,textarea,select{width:100%;max-width:420px;background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:8px}
textarea{max-width:none;min-height:80px}
button{background:var(--acc);color:#0b0e1c;border:0;border-radius:6px;padding:8px 14px;font:inherit;cursor:pointer}
button.alt{background:var(--card);color:var(--fg);border:1px solid var(--line)}button:focus-visible,input:focus-visible,textarea:focus-visible,li button:focus-visible{outline:3px solid #fff;outline-offset:2px}
#tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}#tabs button[aria-pressed=true]{background:var(--acc);color:#0b0e1c}#tabs button{background:var(--card);color:var(--fg);border:1px solid var(--line)}
.cols{display:grid;grid-template-columns:minmax(240px,1fr) 2fr;gap:16px}@media(max-width:700px){.cols{grid-template-columns:1fr}}
.list{list-style:none;margin:0;padding:0}.list li button{display:block;width:100%;text-align:left;background:var(--card);color:var(--fg);border:1px solid var(--line);margin-bottom:6px}
.list li button[aria-current=true]{border-color:var(--acc)}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin-bottom:10px}
.why{white-space:pre-wrap}dl{display:grid;grid-template-columns:max-content 1fr;gap:4px 12px}dt{color:var(--mute)}dd{margin:0;overflow-wrap:anywhere}
.row{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}
.tag{display:inline-block;padding:0 8px;border-radius:99px;border:1px solid var(--line);font-size:.85rem}
@media(forced-colors:active){button{border:1px solid ButtonText}}
"""

JS = r"""
(function () {
  'use strict';
  var KEY = 'raye-staff';
  var STATES = [['new', 'New'], ['in_review', 'In review'], ['accepted', 'Accepted'], ['declined', 'Declined']];
  var creds = null, state = 'new', current = null;
  var $ = function (id) { return document.getElementById(id); };

  function el(tag, text, cls) {
    var e = document.createElement(tag);
    if (text != null) e.textContent = text;
    if (cls) e.className = cls;
    return e;
  }
  function when(ts) { return ts ? new Date(ts * 1000).toISOString().replace('T', ' ').slice(0, 16) + ' UTC' : ''; }

  function api(method, path, body) {
    var opt = { method: method, headers: { 'Authorization': 'Bearer ' + creds.token, 'X-Staff-Name': creds.name }, cache: 'no-store' };
    if (body) { opt.headers['Content-Type'] = 'application/json'; opt.body = JSON.stringify(body); }
    return fetch('/api/staff/' + path, opt).then(function (r) {
      return r.json().catch(function () { return { ok: false, error: 'bad_response' }; }).then(function (j) { j.status = r.status; return j; });
    });
  }

  function signOut() { sessionStorage.removeItem(KEY); creds = null; $('app').hidden = true; $('login').hidden = false; $('who').textContent = ''; }

  function signIn(c) {
    creds = c;
    return api('GET', 'me').then(function (j) {
      if (!j.ok) {
        creds = null;
        var m = { denied: 'Wrong name or token.', limited: 'Too many tries. Wait ten minutes.', name: 'Give a name of 3 to 40 letters or digits.', staff_off: 'The panel is switched off.' };
        $('login-error').textContent = m[j.error] || 'Cannot sign in.';
        return;
      }
      sessionStorage.setItem(KEY, JSON.stringify(c));
      $('login-error').textContent = '';
      $('login').hidden = true; $('app').hidden = false;
      $('who').textContent = 'Signed in as ' + j.staff;
      drawTabs(j.counts); load();
    });
  }

  function drawTabs(counts) {
    var nav = $('tabs'); nav.textContent = '';
    STATES.forEach(function (s) {
      var b = el('button', s[1] + ' (' + (counts[s[0]] || 0) + ')');
      b.type = 'button'; b.setAttribute('aria-pressed', String(s[0] === state));
      b.addEventListener('click', function () { state = s[0]; current = null; refresh(); });
      nav.appendChild(b);
    });
  }

  function refresh() { api('GET', 'me').then(function (j) { if (j.ok) drawTabs(j.counts); }); load(); showDetail(null); }

  function load() {
    api('GET', 'applications?state=' + state).then(function (j) {
      var ul = $('list'); ul.textContent = '';
      if (!j.ok) { $('empty').hidden = false; $('empty').textContent = 'Cannot load the list.'; return; }
      $('empty').hidden = j.applications.length > 0; $('empty').textContent = 'Nothing here.';
      j.applications.forEach(function (a) {
        var li = el('li'), b = el('button', a.role + ' / ' + a.discord + ' / ' + when(a.created_at));
        b.type = 'button'; if (a.ref === current) b.setAttribute('aria-current', 'true');
        b.addEventListener('click', function () { current = a.ref; load(); open(a.ref); });
        li.appendChild(b); ul.appendChild(li);
      });
    });
  }

  function open(ref) { api('GET', 'applications/' + ref).then(function (j) { showDetail(j.ok ? j.application : null); }); }

  function showDetail(a) {
    var d = $('detail'); d.textContent = '';
    if (!a) { d.appendChild(el('p', 'Pick an application.', 'muted')); return; }
    var card = el('div', null, 'card');
    card.appendChild(el('h2', a.role + ' (' + a.lang + ')'));
    card.appendChild(el('span', a.state.replace('_', ' '), 'tag'));
    var dl = el('dl');
    [['Reference', a.ref], ['Discord', a.discord], ['Email', a.email || (a.account ? 'Raye account' : '')], ['Languages', a.languages],
     ['Skills', a.skills], ['Sent', when(a.created_at)], ['Decided', a.decided_at ? when(a.decided_at) + ' by ' + (a.decided_by || '') : ''],
     ['Decision note', a.decision_note || ''], ['Discord role given', a.role_given_at ? when(a.role_given_at) : '']].forEach(function (p) {
      if (!p[1]) return; dl.appendChild(el('dt', p[0])); dl.appendChild(el('dd', p[1]));
    });
    card.appendChild(dl);
    card.appendChild(el('h3', 'Why'));
    card.appendChild(el('p', a.why, 'why'));
    d.appendChild(card);

    var acts = el('div', null, 'row');
    function act(label, action, alt, ask) {
      var b = el('button', label); b.type = 'button'; if (alt) b.className = 'alt';
      b.addEventListener('click', function () {
        var note = '';
        if (ask) { note = window.prompt('Note for the record (optional)', '') || ''; }
        api('POST', 'applications/' + a.ref + '/state', { action: action, note: note }).then(function (j) {
          if (!j.ok) { window.alert(j.error === 'cannot' ? 'It cannot move that way now.' : 'Failed.'); return; }
          refresh(); open(a.ref);
        });
      });
      acts.appendChild(b);
    }
    if (a.state === 'new') act('Start review', 'in_review', true);
    if (a.state === 'in_review') act('Back to new', 'new', true);
    if (a.state === 'new' || a.state === 'in_review') { act('Accept', 'accepted', false, true); act('Decline', 'declined', true, true); }
    if (a.state === 'accepted' && !a.role_given_at) act('Mark the Discord role as given', 'role_given', true);
    d.appendChild(acts);

    var nc = el('div', null, 'card'); nc.appendChild(el('h3', 'Internal notes'));
    a.notes.forEach(function (n) { var p = el('p'); p.appendChild(el('span', when(n.at) + ' ' + n.staff + ': ', 'muted')); p.appendChild(el('span', n.text, 'why')); nc.appendChild(p); });
    var f = el('form'), ta = el('textarea'); ta.maxLength = 1000; ta.setAttribute('aria-label', 'New note');
    var sb = el('button', 'Add note'); sb.type = 'submit';
    f.appendChild(ta); f.appendChild(sb);
    f.addEventListener('submit', function (e) {
      e.preventDefault(); if (!ta.value.trim()) return;
      api('POST', 'applications/' + a.ref + '/note', { text: ta.value }).then(function (j) { if (j.ok) open(a.ref); });
    });
    nc.appendChild(f); d.appendChild(nc);
  }

  $('login-form').addEventListener('submit', function (e) {
    e.preventDefault(); signIn({ name: $('name').value.trim(), token: $('token').value.trim() }); $('token').value = '';
  });
  $('signout').addEventListener('click', signOut);
  $('logbox').addEventListener('toggle', function () {
    if (!$('logbox').open) return;
    api('GET', 'log').then(function (j) {
      var ol = $('log'); ol.textContent = '';
      (j.log || []).forEach(function (r) { ol.appendChild(el('li', when(r.at) + ' ' + r.staff + ' ' + r.action + (r.ref ? ' ' + r.ref : ''))); });
    });
  });
  try { var saved = JSON.parse(sessionStorage.getItem(KEY) || 'null'); if (saved && saved.token) signIn(saved); } catch (e) { signOut(); }
})();
"""
