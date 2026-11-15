// The help box, bottom right of every page. Questions go to our own server
// (/api/support/chat) and are answered from the handbook and the site. The
// conversation lives in this page only: nothing is stored, here or on the
// server, and closing the tab forgets it. "Report a bug" sends a short form
// to /api/support/bug, which checks it before anything reaches our Discord.
(function () {
  "use strict";

  if (!window.fetch || !window.TextDecoder || !document.querySelector) return;

  var lang = document.documentElement.lang === "en" ? "en" : "fr";
  var TEXT = {
    fr: {
      open: "Aide",
      openLabel: "Poser une question sur Raye Linux",
      title: "Aide Raye Linux",
      local: "IA locale sur nos propres serveurs. Rien n'est envoyé à un tiers.",
      close: "Fermer",
      restart: "Nouvelle conversation",
      welcome: "Comment peut-on vous aider ?",
      hello: "Posez votre question sur l'installation, les programmes, les mises à jour "
        + "ou un problème. Je réponds à partir du manuel et du site.",
      notice: "Réponses écrites par une IA sur notre propre serveur. Elle peut se tromper. "
        + "Vos questions ne sont pas gardées.",
      ideas: ["Comment j'installe Raye Linux ?", "Mes programmes .exe vont-ils marcher ?",
        "Comment se font les mises à jour ?"],
      ideasLabel: "Questions fréquentes",
      placeholder: "Écrivez votre question…",
      send: "Envoyer",
      thinking: "Je cherche… La première réponse peut prendre une minute.",
      sources: "Pour en savoir plus",
      copy: "Copier la réponse",
      copied: "Copié",
      pageDownload: "Télécharger",
      pageQuestions: "Questions",
      busy: "Beaucoup de questions en ce moment. Réessayez dans une minute.",
      rate: "Vous avez posé beaucoup de questions. Attendez quelques minutes, ou demandez sur Discord.",
      long: "Votre message est trop long. Raccourcissez-le un peu.",
      down: "Je ne peux pas répondre pour l'instant. Demandez sur Discord, forum #help.",
      network: "Impossible de joindre le serveur. Vérifiez votre connexion, puis réessayez.",
      you: "Vous",
      them: "Réponse",
      server: "Raye Linux",
      serverLine: "Serveur officiel, l'équipe y répond",
      join: "Rejoindre le serveur",
      bug: "Signaler un bogue",
      bugIntro: "Dites-nous ce qui ne marche pas. Chaque rapport est vérifié avant d'être "
        + "publié dans le forum #bugs de notre serveur Discord.",
      bugWhat: "Que s'est-il passé ?",
      bugWhatHint: "Par exemple : Fichiers se fige quand j'ouvre une clé USB.",
      bugSteps: "Comment le refaire (facultatif)",
      bugShot: "Ajouter une capture d'écran (facultatif)",
      bugShotRemove: "Retirer la capture",
      bugShotAdded: "Capture ajoutée",
      bugContact: "Comment vous joindre (facultatif)",
      bugContactHint: "Courriel ou nom Discord",
      bugPrivacy: "Le texte, la capture, la page et votre navigateur partent sur notre serveur "
        + "Discord. Le moyen de vous joindre n'est jamais publié : seule l'équipe le voit.",
      bugSend: "Envoyer le rapport",
      back: "Retour",
      bugSent: "Merci, c'est envoyé. L'équipe va y jeter un œil.",
      bugShort: "Décrivez le problème en au moins dix caractères.",
      bugImage: "Cette image ne peut pas être envoyée. Essayez une capture en PNG ou en JPEG.",
      bugImageBig: "Cette image est trop grosse.",
      bugFailed: "Le rapport n'est pas parti. Réessayez dans un moment, ou écrivez dans #bugs sur Discord.",
      bugRate: "Vous avez déjà envoyé plusieurs rapports. Réessayez dans une heure."
    },
    en: {
      open: "Help",
      openLabel: "Ask a question about Raye Linux",
      title: "Raye Linux help",
      local: "Local AI on our own servers. Nothing is sent to a third party.",
      close: "Close",
      restart: "New conversation",
      welcome: "How can we help?",
      hello: "Ask about installing, programs, updates or a problem. "
        + "I answer from the handbook and the site.",
      notice: "Answers are written by an AI on our own server. It can be wrong. "
        + "Your questions are not kept.",
      ideas: ["How do I install Raye Linux?", "Will my .exe programs work?",
        "How do updates work?"],
      ideasLabel: "Common questions",
      placeholder: "Type your question…",
      send: "Send",
      thinking: "Looking… The first answer can take a minute.",
      sources: "Read more",
      copy: "Copy the answer",
      copied: "Copied",
      pageDownload: "Download",
      pageQuestions: "Questions",
      busy: "Lots of questions right now. Try again in a minute.",
      rate: "You've asked a lot of questions. Wait a few minutes, or ask on Discord.",
      long: "Your message is too long. Make it a bit shorter.",
      down: "I can't answer right now. Ask on Discord, in the #help forum.",
      network: "Can't reach the server. Check your connection, then try again.",
      you: "You",
      them: "Answer",
      server: "Raye Linux",
      serverLine: "Official server, where the team answers",
      join: "Join the server",
      bug: "Report a bug",
      bugIntro: "Tell us what doesn't work. Every report is checked before it goes up in "
        + "the #bugs forum of our Discord server.",
      bugWhat: "What happened?",
      bugWhatHint: "For example: Files freezes when I open a USB stick.",
      bugSteps: "How to make it happen again (optional)",
      bugShot: "Add a screenshot (optional)",
      bugShotRemove: "Remove the screenshot",
      bugShotAdded: "Screenshot added",
      bugContact: "How to reach you (optional)",
      bugContactHint: "Email or Discord name",
      bugPrivacy: "The text, the screenshot, the page and your browser go to our Discord "
        + "server. How to reach you is never posted: only the team sees it.",
      bugSend: "Send the report",
      back: "Back",
      bugSent: "Thanks, it's sent. The team will look at it.",
      bugShort: "Describe the problem in at least ten characters.",
      bugImage: "This picture can't be sent. Try a PNG or JPEG screenshot.",
      bugImageBig: "This picture is too big.",
      bugFailed: "The report didn't go through. Try again in a moment, or write in #bugs on Discord.",
      bugRate: "You've already sent several reports. Try again in an hour."
    }
  }[lang];

  var MAX = 1000;
  var BUG_MAX = 1500;
  var IMAGE_IN_MAX = 15 * 1024 * 1024;   // what we agree to open
  var IMAGE_OUT_MAX = 580 * 1000;        // what the server takes, once squeezed
  var IMAGE_SIDE = 1600;
  var discordLink = document.querySelector('a[href*="discord.gg/"]');
  var DISCORD = discordLink ? discordLink.getAttribute("href") : null;
  var LOGO = "/assets/raye-mark.svg";
  var SVGNS = "http://www.w3.org/2000/svg";

  var history = [];
  var sending = false;
  var shot = null;

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text) e.textContent = text;
    return e;
  }

  function link(href, text, cls) {
    var a = el("a", cls, text);
    a.href = href;
    if (/^https?:/.test(href)) a.rel = "noopener";
    return a;
  }

  // Line icons, 20 px, drawn here so the page loads nothing more.
  var ICONS = {
    close: "M5 5l10 10M15 5L5 15",
    restart: "M4 10a6 6 0 1 0 1.8-4.3M4 4v3.5h3.5",
    send: "M10 16V4M5 9l5-5 5 5",
    copy: "M7 7h8v9H7zM5 13H4V4h8v1",
    check: "M4.5 10.5l3.5 3.5 7.5-8",
    bug: "M7 7a3 3 0 0 1 6 0v1H7zM6 8h8v4a4 4 0 0 1-8 0zM10 9v7M3 10h3M14 10h3M4 15l2-1M16 15l-2-1M4 5l2 2M16 5l-2 2",
    image: "M3 5h14v10H3zM6.5 9a1 1 0 1 0 0-.1M17 13l-4-4-6 6"
  };

  function icon(name) {
    var svg = document.createElementNS(SVGNS, "svg");
    svg.setAttribute("viewBox", "0 0 20 20");
    svg.setAttribute("aria-hidden", "true");
    svg.setAttribute("class", "help-icon");
    var path = document.createElementNS(SVGNS, "path");
    path.setAttribute("d", ICONS[name]);
    svg.appendChild(path);
    return svg;
  }

  function iconButton(name, label, cls) {
    var b = el("button", "help-iconbtn" + (cls ? " " + cls : ""));
    b.type = "button";
    b.setAttribute("aria-label", label);
    b.title = label;
    b.appendChild(icon(name));
    return b;
  }

  function avatar(size) {
    var span = el("span", "help-avatar help-avatar-" + size);
    var img = el("img");
    img.src = LOGO;
    img.alt = "";
    span.appendChild(img);
    return span;
  }

  // Light formatting from the answers: **bold**, *italic*, `code`, lists, and links
  // to this site only. Built node by node, never as HTML.
  function inline(parent, text) {
    var re = /(\*\*[^*]+\*\*|\*[^*\s][^*]*\*|`[^`]+`|(?:https:\/\/rayelinux\.com)?\/[A-Za-z0-9\-\/#]*\/(?=[\s.,;:)]|$))/g;
    var at = 0, m;
    while ((m = re.exec(text))) {
      if (m.index > at) parent.appendChild(document.createTextNode(text.slice(at, m.index)));
      var t = m[0];
      if (t.slice(0, 2) === "**") parent.appendChild(el("strong", null, t.slice(2, -2)));
      else if (t[0] === "*") parent.appendChild(el("em", null, t.slice(1, -1)));
      else if (t[0] === "`") parent.appendChild(el("code", null, t.slice(1, -1)));
      else parent.appendChild(link(t.replace(/^https:\/\/rayelinux\.com/, ""), t));
      at = m.index + t.length;
    }
    if (at < text.length) parent.appendChild(document.createTextNode(text.slice(at)));
  }

  function render(box, text) {
    while (box.firstChild) box.removeChild(box.firstChild);
    var list = null;
    text.split("\n").forEach(function (line) {
      var item = /^\s*(?:[-*•]|\d+[.)])\s+(.*)/.exec(line);
      if (item) {
        if (!list) {
          list = el(/^\s*\d/.test(line) ? "ol" : "ul");
          box.appendChild(list);
        }
        var li = el("li");
        inline(li, item[1]);
        list.appendChild(li);
        return;
      }
      list = null;
      if (!line.trim()) return;
      var p = el("p");
      inline(p, line);
      box.appendChild(p);
    });
  }

  // the launcher
  var button = el("button", "help-open");
  button.type = "button";
  button.setAttribute("aria-expanded", "false");
  button.setAttribute("aria-controls", "help-panel");
  button.setAttribute("aria-label", TEXT.openLabel);
  button.appendChild(el("span", "help-open-mark"));
  button.appendChild(el("span", null, TEXT.open));

  // the panel
  var panel = el("section", "help-panel");
  panel.id = "help-panel";
  panel.hidden = true;
  panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-labelledby", "help-title");

  var head = el("header", "help-head");
  var headText = el("div", "help-head-text");
  var title = el("h2", null, TEXT.title);
  title.id = "help-title";
  headText.appendChild(title);
  headText.appendChild(el("p", null, TEXT.local));
  var restart = iconButton("restart", TEXT.restart);
  restart.hidden = true;
  var close = iconButton("close", TEXT.close);
  head.appendChild(avatar("head"));
  head.appendChild(headText);
  head.appendChild(restart);
  head.appendChild(close);

  // chat view
  var chat = el("div", "help-view help-chat");
  var log = el("div", "help-log");
  log.setAttribute("role", "log");
  log.setAttribute("aria-live", "polite");
  log.tabIndex = 0;

  var welcome = el("div", "help-welcome");
  welcome.appendChild(avatar("big"));
  welcome.appendChild(el("h3", null, TEXT.welcome));
  welcome.appendChild(el("p", null, TEXT.hello));
  var ideas = el("ul", "help-ideas");
  ideas.setAttribute("aria-label", TEXT.ideasLabel);
  TEXT.ideas.forEach(function (q) {
    var li = el("li");
    var b = el("button", "help-idea", q);
    b.type = "button";
    b.addEventListener("click", function () { ask(q); });
    li.appendChild(b);
    ideas.appendChild(li);
  });
  welcome.appendChild(ideas);
  welcome.appendChild(el("p", "help-notice", TEXT.notice));
  log.appendChild(welcome);

  var bottom = el("div", "help-bottom");
  var form = el("form", "help-form");
  var label = el("label", "visually-hidden", TEXT.placeholder);
  label.htmlFor = "help-input";
  var input = el("textarea");
  input.id = "help-input";
  input.rows = 1;
  input.maxLength = MAX;
  input.placeholder = TEXT.placeholder;
  var send = el("button", "help-send");
  send.type = "submit";
  send.setAttribute("aria-label", TEXT.send);
  send.title = TEXT.send;
  send.appendChild(icon("send"));
  send.disabled = true;
  form.appendChild(label);
  form.appendChild(input);
  form.appendChild(send);
  bottom.appendChild(form);
  bottom.appendChild(serverCard());
  chat.appendChild(log);
  chat.appendChild(bottom);

  function serverCard() {
    var card = el("section", "help-server");
    card.setAttribute("aria-label", TEXT.server);
    var top = el("div", "help-server-top");
    top.appendChild(avatar("card"));
    var words = el("div");
    words.appendChild(el("p", "help-server-name", TEXT.server));
    words.appendChild(el("p", "help-server-line", TEXT.serverLine));
    top.appendChild(words);
    card.appendChild(top);
    var row = el("div", "help-server-row");
    if (DISCORD) row.appendChild(link(DISCORD, TEXT.join, "help-join"));
    var bugButton = el("button", "help-bugbtn");
    bugButton.type = "button";
    bugButton.appendChild(icon("bug"));
    bugButton.appendChild(document.createTextNode(TEXT.bug));
    bugButton.addEventListener("click", function () { show("bug"); });
    row.appendChild(bugButton);
    card.appendChild(row);
    return card;
  }

  // bug report view
  var bugView = el("form", "help-view help-bug");
  bugView.noValidate = true;
  bugView.appendChild(el("p", "help-bug-intro", TEXT.bugIntro));

  function field(id, text, control, hint) {
    var wrap = el("div", "help-field");
    var l = el("label", null, text);
    l.htmlFor = id;
    control.id = id;
    wrap.appendChild(l);
    if (hint) control.placeholder = hint;
    wrap.appendChild(control);
    return wrap;
  }

  var bugWhat = el("textarea");
  bugWhat.rows = 4;
  bugWhat.maxLength = BUG_MAX;
  bugWhat.required = true;
  var bugSteps = el("textarea");
  bugSteps.rows = 3;
  bugSteps.maxLength = 1000;
  var bugContact = el("input");
  bugContact.type = "text";
  bugContact.maxLength = 200;
  bugContact.autocomplete = "email";
  var trap = el("input", "help-trap");
  trap.type = "text";
  trap.tabIndex = -1;
  trap.autocomplete = "off";
  trap.setAttribute("aria-hidden", "true");
  var fileInput = el("input", "visually-hidden");
  fileInput.type = "file";
  fileInput.accept = "image/png,image/jpeg,image/webp";
  fileInput.tabIndex = -1;
  fileInput.setAttribute("aria-hidden", "true");

  var shotRow = el("div", "help-shot");
  var shotButton = el("button", "help-ghost");
  shotButton.type = "button";
  shotButton.appendChild(icon("image"));
  shotButton.appendChild(document.createTextNode(TEXT.bugShot));
  var shotChip = el("div", "help-shot-chip");
  shotChip.hidden = true;
  var shotThumb = el("img");
  shotThumb.alt = "";
  var shotRemove = iconButton("close", TEXT.bugShotRemove);
  shotChip.appendChild(shotThumb);
  shotChip.appendChild(el("span", null, TEXT.bugShotAdded));
  shotChip.appendChild(shotRemove);
  shotRow.appendChild(shotButton);
  shotRow.appendChild(shotChip);

  var bugError = el("p", "help-error");
  bugError.setAttribute("role", "alert");
  var bugButtons = el("div", "help-bug-buttons");
  var bugBack = el("button", "help-ghost", TEXT.back);
  bugBack.type = "button";
  var bugSend = el("button", "help-primary", TEXT.bugSend);
  bugSend.type = "submit";
  bugButtons.appendChild(bugBack);
  bugButtons.appendChild(bugSend);

  bugView.appendChild(field("help-bug-what", TEXT.bugWhat, bugWhat, TEXT.bugWhatHint));
  bugView.appendChild(field("help-bug-steps", TEXT.bugSteps, bugSteps));
  bugView.appendChild(shotRow);
  bugView.appendChild(field("help-bug-contact", TEXT.bugContact, bugContact, TEXT.bugContactHint));
  bugView.appendChild(trap);
  bugView.appendChild(fileInput);
  bugView.appendChild(el("p", "help-small", TEXT.bugPrivacy));
  bugView.appendChild(bugError);
  bugView.appendChild(bugButtons);
  bugView.hidden = true;

  // sent view
  var sentView = el("div", "help-view help-sent");
  sentView.setAttribute("role", "status");
  sentView.appendChild(avatar("big"));
  sentView.appendChild(el("p", null, TEXT.bugSent));
  var sentBack = el("button", "help-ghost", TEXT.back);
  sentBack.type = "button";
  sentView.appendChild(sentBack);
  sentView.hidden = true;

  panel.appendChild(head);
  panel.appendChild(chat);
  panel.appendChild(bugView);
  panel.appendChild(sentView);

  function show(view) {
    chat.hidden = view !== "chat";
    bugView.hidden = view !== "bug";
    sentView.hidden = view !== "sent";
    restart.hidden = view !== "chat" || !history.length;
    if (view === "bug") { bugError.textContent = ""; bugWhat.focus(); }
    else if (view === "sent") sentBack.focus();
    else input.focus();
  }

  var phone = window.matchMedia ? window.matchMedia("(max-width: 30rem)") : null;
  var bodyOverflow = "";

  function open() {
    panel.hidden = false;
    button.setAttribute("aria-expanded", "true");
    button.hidden = true;
    if (phone && phone.matches) {
      bodyOverflow = document.body.style.overflow;
      document.body.style.overflow = "hidden";
    }
    if (!chat.hidden) input.focus();
  }

  function shut() {
    panel.hidden = true;
    button.hidden = false;
    button.setAttribute("aria-expanded", "false");
    document.body.style.overflow = bodyOverflow;
    button.focus();
  }

  function grow() {
    input.style.height = "auto";
    input.style.height = Math.min(input.scrollHeight, 128) + "px";
    send.disabled = sending || !input.value.trim();
  }

  button.addEventListener("click", open);
  close.addEventListener("click", shut);
  restart.addEventListener("click", function () {
    if (sending) return;
    history = [];
    while (log.lastChild !== welcome) log.removeChild(log.lastChild);
    welcome.hidden = false;
    input.value = "";
    grow();
    show("chat");
  });
  panel.addEventListener("keydown", function (e) {
    if (e.key === "Escape") shut();
  });
  input.addEventListener("input", grow);
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey && !e.isComposing) {
      e.preventDefault();
      ask();
    }
  });
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    ask();
  });

  function userBubble(text) {
    var row = el("div", "help-row help-row-you");
    var box = el("div", "help-msg help-you");
    box.appendChild(el("span", "visually-hidden", TEXT.you + (lang === "fr" ? " : " : ": ")));
    box.appendChild(document.createTextNode(text));
    row.appendChild(box);
    log.appendChild(row);
  }

  function answerBubble() {
    var row = el("div", "help-row help-row-them");
    row.appendChild(avatar("msg"));
    var col = el("div", "help-col");
    var box = el("div", "help-msg help-them");
    box.appendChild(el("span", "visually-hidden", TEXT.them + (lang === "fr" ? " : " : ": ")));
    var body = el("div", "help-body");
    box.appendChild(body);
    col.appendChild(box);
    row.appendChild(col);
    log.appendChild(row);
    log.scrollTop = log.scrollHeight;
    return { row: row, col: col, box: box, body: body };
  }

  function pageName(url) {
    return /download|telecharger/.test(url) ? TEXT.pageDownload : TEXT.pageQuestions;
  }

  function chips(col, sources) {
    if (!sources.length) return;
    var nav = el("nav", "help-chips");
    nav.setAttribute("aria-label", TEXT.sources);
    sources.slice(0, 4).forEach(function (s) {
      if (!s || typeof s.url !== "string" || s.url.charAt(0) !== "/") return;
      var a = link(s.url, null, "help-chip");
      a.appendChild(el("span", "help-chip-page", pageName(s.url)));
      a.appendChild(document.createTextNode(" · " + s.title));
      nav.appendChild(a);
    });
    if (nav.firstChild) col.appendChild(nav);
  }

  function copyButton(col, text) {
    if (!navigator.clipboard) return;
    var b = el("button", "help-copy");
    b.type = "button";
    var label = el("span", null, TEXT.copy);
    b.appendChild(icon("copy"));
    b.appendChild(label);
    b.addEventListener("click", function () {
      navigator.clipboard.writeText(text).then(function () {
        b.replaceChild(icon("check"), b.firstChild);
        label.textContent = TEXT.copied;
        setTimeout(function () {
          b.replaceChild(icon("copy"), b.firstChild);
          label.textContent = TEXT.copy;
        }, 2000);
      }, function () {});
    });
    col.appendChild(b);
  }

  function failed(m, msg) {
    m.box.classList.add("help-failed");
    render(m.body, msg);
    m.row.removeAttribute("aria-busy");
  }

  function ask(given) {
    var q = (given || input.value).trim();
    if (!q || sending) return;
    welcome.hidden = true;
    if (q.length > MAX) { failed(answerBubble(), TEXT.long); return; }
    sending = true;
    input.value = "";
    grow();
    userBubble(q);
    history.push({ role: "user", content: q });
    restart.hidden = false;
    var m = answerBubble();
    m.row.setAttribute("aria-busy", "true");
    var wait = el("p", "help-wait");
    wait.appendChild(el("span", "help-dots"));
    wait.appendChild(document.createTextNode(TEXT.thinking));
    m.body.appendChild(wait);

    var answer = "";
    var sources = [];
    fetch("/api/support/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "text/event-stream" },
      body: JSON.stringify({ lang: lang, messages: history.slice(-10) })
    }).then(function (r) {
      var type = r.headers.get("Content-Type") || "";
      if (type.indexOf("text/event-stream") !== 0) {
        return r.json().catch(function () { return {}; }).then(function (j) {
          var code = j && j.error;
          throw new Error(code === "rate_limited" || r.status === 429 ? "rate"
            : code === "too_long" ? "long" : code === "busy" ? "busy" : "down");
        });
      }
      var reader = r.body.getReader();
      var decoder = new TextDecoder();
      var buffer = "";
      var ended = null;
      function step() {
        return reader.read().then(function (part) {
          if (part.done) return;
          buffer += decoder.decode(part.value, { stream: true });
          var cut;
          while ((cut = buffer.indexOf("\n\n")) >= 0) {
            var block = buffer.slice(0, cut);
            buffer = buffer.slice(cut + 2);
            var name = null, data = null;
            block.split("\n").forEach(function (line) {
              if (line.indexOf("event: ") === 0) name = line.slice(7);
              else if (line.indexOf("data: ") === 0) data = line.slice(6);
            });
            if (data === null) continue;
            var v = JSON.parse(data);
            if (name === "meta") sources = v.sources || [];
            else if (name === "error") ended = "down";
            else if (name === "done") ended = "ok";
            else if (v.t) {
              answer += v.t;
              render(m.body, answer);
              log.scrollTop = log.scrollHeight;
            }
          }
          return step();
        });
      }
      return step().then(function () {
        if (ended !== "ok" || !answer) throw new Error("down");
      });
    }).then(function () {
      history.push({ role: "assistant", content: answer });
      chips(m.col, sources);
      copyButton(m.col, answer);
      m.row.removeAttribute("aria-busy");
    }).catch(function (err) {
      history.pop();
      var key = err && TEXT[err.message] ? err.message : "network";
      if (err && err.message === "down" && answer) key = "down";
      failed(m, TEXT[key]);
    }).then(function () {
      sending = false;
      grow();
      log.scrollTop = log.scrollHeight;
    });
  }

  // bug report
  function squeeze(file) {
    return new Promise(function (resolve, reject) {
      var url = URL.createObjectURL(file);
      var img = new Image();
      img.onload = function () {
        var scale = Math.min(1, IMAGE_SIDE / Math.max(img.naturalWidth, img.naturalHeight));
        var canvas = document.createElement("canvas");
        canvas.width = Math.max(1, Math.round(img.naturalWidth * scale));
        canvas.height = Math.max(1, Math.round(img.naturalHeight * scale));
        var ctx = canvas.getContext("2d");
        URL.revokeObjectURL(url);
        if (!ctx) { reject(new Error("image")); return; }
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        var qualities = [0.85, 0.7, 0.55, 0.4];
        for (var i = 0; i < qualities.length; i++) {
          var data = canvas.toDataURL("image/jpeg", qualities[i]);
          if ((data.length - 23) * 3 / 4 <= IMAGE_OUT_MAX) { resolve(data); return; }
        }
        reject(new Error("big"));
      };
      img.onerror = function () { URL.revokeObjectURL(url); reject(new Error("image")); };
      img.src = url;
    });
  }

  function setShot(data) {
    shot = data;
    shotChip.hidden = !data;
    shotButton.hidden = !!data;
    if (data) shotThumb.src = data;
    else shotThumb.removeAttribute("src");
  }

  shotButton.addEventListener("click", function () { fileInput.click(); });
  shotRemove.addEventListener("click", function () { setShot(null); shotButton.focus(); });
  fileInput.addEventListener("change", function () {
    var file = fileInput.files && fileInput.files[0];
    fileInput.value = "";
    bugError.textContent = "";
    if (!file) return;
    if (!/^image\/(png|jpeg|webp)$/.test(file.type)) { bugError.textContent = TEXT.bugImage; return; }
    if (file.size > IMAGE_IN_MAX) { bugError.textContent = TEXT.bugImageBig; return; }
    squeeze(file).then(setShot, function (err) {
      bugError.textContent = err.message === "big" ? TEXT.bugImageBig : TEXT.bugImage;
    });
  });
  bugBack.addEventListener("click", function () { show("chat"); });
  sentBack.addEventListener("click", function () { show("chat"); });

  bugView.addEventListener("submit", function (e) {
    e.preventDefault();
    var what = bugWhat.value.trim();
    if (what.length < 10) { bugError.textContent = TEXT.bugShort; bugWhat.focus(); return; }
    if (bugSend.disabled) return;
    bugSend.disabled = true;
    bugError.textContent = "";
    fetch("/api/support/bug", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify({
        lang: lang, what: what, steps: bugSteps.value.trim(),
        contact: bugContact.value.trim(), page: location.pathname,
        agent: navigator.userAgent.slice(0, 200), image: shot, website: trap.value
      })
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (r.ok && j.ok) return;
        throw new Error(r.status === 429 ? "bugRate" : j.error === "too_short" ? "bugShort"
          : /image/.test(j.error || "") ? "bugImage" : "bugFailed");
      });
    }).then(function () {
      bugWhat.value = "";
      bugSteps.value = "";
      bugContact.value = "";
      setShot(null);
      show("sent");
    }).catch(function (err) {
      bugError.textContent = TEXT[err && TEXT[err.message] ? err.message : "bugFailed"];
    }).then(function () {
      bugSend.disabled = false;
    });
  });

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }
  ready(function () {
    document.body.appendChild(button);
    document.body.appendChild(panel);
  });
})();
