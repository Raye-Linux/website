"""HTTP side of the staff panel (see staff.py for the rules).

    GET  /api/staff/panel | panel.js | panel.css   the page itself, no data
    GET  /api/staff/me                              who am I, how many of each
    GET  /api/staff/applications[?state=&role=]     the list (no email)
    GET  /api/staff/applications/<ref>              one application, logged
    POST /api/staff/applications/<ref>/state        {"action": in_review|new|accepted|declined|role_given, "note"}
    POST /api/staff/applications/<ref>/note         {"text"}
    GET  /api/staff/log                             what staff did

The credential goes in `Authorization: Bearer ...`; with the admin token the
caller also gives `X-Staff-Name`."""

import logging
from http import HTTPStatus

from . import applications as apps
from . import staff as st
from .staff_panel import CSS, HTML, JS

log = logging.getLogger(__name__)

PANEL_CSP = ("default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; "
             "img-src 'self'; form-action 'none'; base-uri 'none'; frame-ancestors 'none'")
NOINDEX = {"X-Robots-Tag": "noindex, nofollow, noarchive"}


def handle(h, method, path, query):
    app = h.app
    tail = path[len("/api/staff/"):]
    # the page and its two files hold no data: anyone may fetch them,
    # nothing in them works without the token
    if method == "GET" and tail in ("panel", "panel.js", "panel.css"):
        kind = {"panel": ("text/html; charset=utf-8", HTML),
                "panel.js": ("text/javascript; charset=utf-8", JS),
                "panel.css": ("text/css; charset=utf-8", CSS)}[tail]
        extra = dict(NOINDEX)
        if tail == "panel":
            extra["Content-Security-Policy"] = PANEL_CSP
        return h._send(200, kind[1].encode("utf-8"), kind[0], extra)

    def fail(status, code, extra=None):
        h.close_connection = True
        h._json(status, {"ok": False, "error": code}, {**NOINDEX, **(extra or {})})

    sf = app.staff
    if not sf.enabled():
        return fail(503, "staff_off")
    bearer = h.headers.get("Authorization", "")
    bearer = bearer[7:].strip() if bearer[:7].lower() == "bearer " else ""
    try:
        who = sf.authenticate(h._ip(), bearer, h.headers.get("X-Staff-Name"))
    except st.Forbidden as exc:
        code = str(exc)
        if code == "limited":
            return fail(429, "limited", {"Retry-After": "600"})
        if code == "name":
            return fail(400, "name")
        return fail(401, "denied")

    def ok(payload, status=200):
        h._json(status, dict(payload, ok=True), NOINDEX)

    parts = tail.split("/")
    if method == "GET":
        if tail == "me":
            return ok({"staff": who, "counts": sf.counts(), "roles": apps.ROLE_NAMES})
        if tail == "applications":
            try:
                return ok({"applications": sf.list(query.get("state"), query.get("role"))})
            except ValueError:
                return fail(400, "bad_request")
        if len(parts) == 2 and parts[0] == "applications" and st.REF_RE.match(parts[1]):
            data = sf.detail(parts[1], who)
            return ok({"application": data}) if data else fail(404, "not_found")
        if tail == "log":
            return ok({"log": sf.log_rows()})
        return fail(404, "not_found")

    # POST: only JSON, so no form on another site can send it
    if h.headers.get("Content-Type", "").split(";")[0].strip().lower() != "application/json":
        return fail(415, "bad_request")
    try:
        kind, fields = h._read_body(4096)
    except Exception as exc:  # BadRequest, kept generic here
        status = getattr(exc, "status", HTTPStatus.BAD_REQUEST)
        return fail(status.value, "bad_request")
    if len(parts) == 3 and parts[0] == "applications" and st.REF_RE.match(parts[1]):
        ref = parts[1]
        if parts[2] == "state":
            note = fields.get("note") if isinstance(fields.get("note"), str) else ""
            try:
                new = sf.act(ref, fields.get("action"), who, note)
            except ValueError:
                return fail(400, "bad_request")
            if new is None:
                return fail(409, "cannot")
            return ok({"state": new})
        if parts[2] == "note":
            try:
                found = sf.add_note(ref, who, fields.get("text"))
            except ValueError:
                return fail(400, "note")
            return ok({"notes": sf.notes(ref)}) if found else fail(404, "not_found")
    return fail(404, "not_found")
