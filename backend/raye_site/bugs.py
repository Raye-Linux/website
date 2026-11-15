"""Bug reports from the help box. A report that passes moderation.py is
posted to the #bugs forum of the Raye Linux Discord server; the others go
to a private staff channel, or nowhere when they are abuse.

The two webhook addresses are secrets: they live in /etc/raye-site
(bug-webhook, bug-review-webhook, root only), reach the service as a
credential, and are never printed or logged. A report is not kept here
either: it goes to Discord and only counters stay."""

import base64
import binascii
import json
import logging
import re
import threading
import urllib.error
import urllib.request
import uuid

from .ratelimit import RateLimiter

log = logging.getLogger(__name__)

MAX_BODY = 900_000            # the text and a screenshot, base64 included
WHAT_MIN = 10
WHAT_MAX = 1500
STEPS_MAX = 1000
CONTACT_MAX = 200
PAGE_MAX = 200
AGENT_MAX = 400
IMAGE_MAX = 600_000           # bytes, once decoded
THREAD_NAME_MAX = 90
REPORTS_PER_HOUR = 3          # per visitor
REPORTS_PER_HOUR_ALL = 30     # everyone together
SENDING_MAX = 2               # webhook calls at the same time
TIMEOUT = 15
AGENT = "DiscordBot (https://rayelinux.com, 1)"  # Cloudflare refuses Python-urllib

WEBHOOK_RE = re.compile(r"^https://(?:discord\.com|discordapp\.com|ptb\.discord\.com|canary\.discord\.com)"
                        r"/api/webhooks/\d{5,30}/[A-Za-z0-9_\-]{20,100}$")
CONTROL_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f​-‏‪-‮⁦-⁩]")


def load_webhook(paths):
    """The webhook address from the first readable file, or None. Anything
    that is not a Discord webhook address is ignored."""
    for path in paths:
        try:
            with open(path, encoding="utf-8") as f:
                value = f.read().strip()
        except (OSError, UnicodeDecodeError):
            continue
        if WEBHOOK_RE.match(value):
            return value
    return None


def clean(text, limit):
    """One field of the report: no control or direction characters, no
    @everyone that could ping, cut to its size."""
    text = CONTROL_RE.sub("", str(text).replace("\r\n", "\n").replace("\r", "\n"))
    text = re.sub(r"@(everyone|here)", "@\u200b\\1", text)
    text = text.replace("<@", "<\u200b@")
    return text.strip()[:limit]


def decode_image(value):
    """(bytes, extension) of a data: URL holding a JPEG or a PNG."""
    m = re.match(r"^data:image/(jpeg|png);base64,([A-Za-z0-9+/=\s]+)$", value or "")
    if not m:
        raise ValueError("bad_image")
    if len(m.group(2)) > IMAGE_MAX * 4 // 3 + 8:
        raise ValueError("image_too_large")
    try:
        raw = base64.b64decode(m.group(2), validate=False)
    except (binascii.Error, ValueError):
        raise ValueError("bad_image")
    if len(raw) > IMAGE_MAX:
        raise ValueError("image_too_large")
    if raw.startswith(b"\xff\xd8\xff"):
        return raw, "jpg"
    if raw.startswith(b"\x89PNG\r\n\x1a\n"):
        return raw, "png"
    raise ValueError("bad_image")


def validate(fields):
    """A report as a dict, or ValueError(code)."""
    lang = "en" if fields.get("lang") == "en" else "fr"
    raw_what = fields.get("what")
    if not isinstance(raw_what, str):
        raise ValueError("too_short")
    if len(raw_what) > WHAT_MAX:
        raise ValueError("too_long")
    what = clean(raw_what, WHAT_MAX)
    if len(what) < WHAT_MIN:
        raise ValueError("too_short")
    report = {"lang": lang, "what": what}
    for key, limit in (("steps", STEPS_MAX), ("contact", CONTACT_MAX),
                       ("page", PAGE_MAX), ("agent", AGENT_MAX)):
        value = fields.get(key)
        if value is None or value == "":
            report[key] = ""
            continue
        if not isinstance(value, str):
            raise ValueError("bad_request")
        if key in ("steps", "contact") and len(value) > limit:
            raise ValueError("too_long")
        report[key] = clean(value, limit)
    if report["page"] and not report["page"].startswith("/"):
        report["page"] = ""
    image = fields.get("image")
    report["image"] = decode_image(image) if image else None
    return report


BROWSERS = (("Edg", "Edge"), ("EdgA", "Edge"), ("EdgiOS", "Edge"), ("OPR", "Opera"),
            ("SamsungBrowser", "Samsung Internet"), ("Vivaldi", "Vivaldi"),
            ("FxiOS", "Firefox"), ("Firefox", "Firefox"), ("CriOS", "Chrome"),
            ("Chromium", "Chromium"), ("Chrome", "Chrome"))
LANGUAGES = {"en": "English", "fr": "French"}


def short_agent(agent):
    """"Firefox 160 on Linux" from a user agent string, or "" when it is not
    one we recognise. The raw string is never shown."""
    agent = agent or ""
    name = ""
    for token, label in BROWSERS:
        m = re.search(r"\b%s/(\d{1,4})" % token, agent)
        if m:
            name = "%s %s" % (label, m.group(1))
            break
    else:
        m = re.search(r"Version/(\d{1,4})[.\d]* (?:Mobile/\S+ )?Safari/", agent)
        if m:
            name = "Safari " + m.group(1)
    if re.search(r"iPhone|iPad|iPod", agent):
        system = "iOS"
    elif "Android" in agent:
        system = "Android"
    elif "CrOS" in agent:
        system = "ChromeOS"
    elif "Windows" in agent:
        system = "Windows"
    elif "Mac OS X" in agent or "Macintosh" in agent:
        system = "macOS"
    elif "Linux" in agent or "X11" in agent:
        system = "Linux"
    else:
        system = ""
    if name and system:
        return name + " on " + system
    return name or system


def thread_name(what):
    """A short title: the first sentence, capital first, no trailing junk."""
    first = what.strip().split("\n", 1)[0].strip()
    m = re.match(r"(.+?[.!?])(?:\s|$)", first)
    if m and len(m.group(1)) >= 12:
        first = m.group(1)
    first = re.sub(r"\s+", " ", first)
    first = re.sub(r"[\s.,;:!?…\-–—_*~\"'()\[\]]+$", "", first)
    first = re.sub(r"^[\s\-–—*_~\"'.,;:]+", "", first)
    if len(first) > THREAD_NAME_MAX:
        cut = first[:THREAD_NAME_MAX - 1]
        if " " in cut[THREAD_NAME_MAX // 2:]:
            cut = cut[:cut.rindex(" ")]
        first = cut.rstrip(" .,;:-") + "…"
    if not first:
        return "Bug report"
    return first[0].upper() + first[1:]


def numbered(steps):
    """Several lines become a numbered list; one line stays as it is."""
    lines = [re.sub(r"^\s*(?:\d{1,2}[.)\-:]|[-*•·>])\s*", "", line).strip()
             for line in steps.split("\n")]
    lines = [line for line in lines if line]
    if len(lines) < 2:
        return lines[0] if lines else ""
    return "\n".join("%d. %s" % (i, line) for i, line in enumerate(lines, 1))


def footer(report):
    parts = ["Sent from rayelinux.com", short_agent(report["agent"]),
             LANGUAGES.get(report["lang"], "")]
    return " · ".join(p for p in parts if p)


def message(report):
    """The public forum post: no contact, no raw browser string."""
    embed = {
        "color": 0x7B3CFF,
        "fields": [{"name": "What happened", "value": report["what"][:1024]}],
        "footer": {"text": footer(report)},
    }
    steps = numbered(report["steps"])
    if steps:
        embed["fields"].append({"name": "Steps to reproduce", "value": steps[:1024]})
    if report["image"]:
        embed["image"] = {"url": "attachment://screenshot." + report["image"][1]}
    return {
        "thread_name": thread_name(report["what"]),
        "username": "rayelinux.com",
        "embeds": [embed],
        "allowed_mentions": {"parse": []},
    }


def review_message(report, reason):
    """The post for the private staff channel: everything, with why it was
    held. Contact and page only ever go here."""
    embed = {
        "title": "Held: " + reason,
        "color": 0x7B3CFF,
        "fields": [{"name": "Title it would get", "value": thread_name(report["what"])},
                   {"name": "What happened", "value": report["what"][:1024]}],
        "footer": {"text": footer(report)},
    }
    steps = numbered(report["steps"])
    if steps:
        embed["fields"].append({"name": "Steps to reproduce", "value": steps[:1024]})
    if report["contact"]:
        embed["fields"].append({"name": "Contact (private)", "value": report["contact"][:1024]})
    if report["page"]:
        embed["fields"].append({"name": "Page", "value": "https://rayelinux.com" + report["page"]})
    if report["image"]:
        embed["image"] = {"url": "attachment://screenshot." + report["image"][1]}
    return {
        "username": "rayelinux.com",
        "embeds": [embed],
        "allowed_mentions": {"parse": []},
    }


def multipart(payload, image):
    """(body, content type) for a webhook call with an optional file."""
    boundary = "raye" + uuid.uuid4().hex
    parts = [
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"payload_json\"\r\n"
        f"Content-Type: application/json\r\n\r\n".encode()
        + json.dumps(payload).encode() + b"\r\n"
    ]
    if image:
        raw, ext = image
        ctype = "image/jpeg" if ext == "jpg" else "image/png"
        parts.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"files[0]\"; "
            f"filename=\"screenshot.{ext}\"\r\nContent-Type: {ctype}\r\n\r\n".encode()
            + raw + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


class Bugs:
    def __init__(self, url, clock=None, opener=None, review_url=None, duplicates=None,
                 classifier=None):
        from . import moderation
        kw = {"clock": clock} if clock else {}
        self.url = url
        self.review_url = review_url
        self.limiter = RateLimiter(REPORTS_PER_HOUR, 3600, **kw)
        self.everyone = RateLimiter(REPORTS_PER_HOUR_ALL, 3600, **kw)
        self.slots = threading.BoundedSemaphore(SENDING_MAX)
        self.opener = opener or urllib.request.build_opener()
        self.duplicates = duplicates or moderation.Duplicates(**kw)
        self.classifier = classifier or moderation.Classifier(None, None)
        self.counts = {"public": 0, "review": 0, "drop": 0, "failed": 0}
        self.count_lock = threading.Lock()

    def ready(self):
        return bool(self.url and self.review_url)

    def handle(self, report):
        """True when the report went where it belongs (dropping counts), False
        when Discord did not take it. The visitor sees the same either way."""
        from . import moderation
        outcome, reason = moderation.decide(report, self.duplicates, self.classifier)
        if outcome == "drop":
            self._count("drop", reason)
            return True
        if outcome == "public":
            ok = self._post(self.url, message(report), report["image"])
        else:
            ok = self._post(self.review_url, review_message(report, reason), report["image"],
                            thread=thread_name(report["what"]))
        if ok:
            self.duplicates.remember(report["what"])
        self._count(outcome if ok else "failed", reason)
        return ok

    def _count(self, kind, reason):
        with self.count_lock:
            self.counts[kind] += 1
            c = dict(self.counts)
        line = "public=%d review=%d drop=%d failed=%d" % (c["public"], c["review"], c["drop"],
                                                          c["failed"])
        # only the rule's name goes in the journal, never the text
        if kind == "failed":
            log.warning("bug report not sent (%s)", line)
        else:
            log.info("bug report %s%s (%s)", kind, " (%s)" % reason if reason else "", line)

    def _post(self, url, payload, image, thread=None):
        """Discord took it or not. A forum channel needs a topic title: when
        the private channel turns out to be one, the post is sent again with
        it. Never logs the address nor the text."""
        status, raw = self._call(url, payload, image)
        if status == 400 and thread and b"thread_name" in (raw or b""):
            status, raw = self._call(url, dict(payload, thread_name=thread), image)
        if isinstance(status, int) and 200 <= status < 300:
            return True
        log.warning("bug webhook answered %s", status)
        return False

    def _call(self, url, payload, image):
        body, ctype = multipart(payload, image)
        req = urllib.request.Request(url + "?wait=true", data=body, method="POST",
                                     headers={"Content-Type": ctype, "User-Agent": AGENT})
        if not self.slots.acquire(timeout=TIMEOUT):
            return "busy", None
        try:
            with self.opener.open(req, timeout=TIMEOUT) as r:
                return r.status, r.read(65536)
        except urllib.error.HTTPError as exc:
            try:
                raw = exc.read(4096)
            except OSError:
                raw = None
            return exc.code, raw
        except (OSError, ValueError) as exc:
            return type(exc).__name__, None
        finally:
            self.slots.release()


# The other way: the topics of #bugs, read from the Discord bot's API on our own
# network (it holds the Discord session; the bot token never comes here).
# The browser only talks to this server, which keeps each answer a minute
# and passes on the fields the page shows, nothing else.

FEED_TTL = 60
FEED_TIMEOUT = 8
FEED_KEYS = 200


def _text(value, limit):
    return value[:limit] if isinstance(value, str) else ""


def _tags(value):
    return [_text(t, 60) for t in value[:10] if isinstance(t, str)] if isinstance(value, list) else []


def clean_topic(t):
    """One topic of the list, only the fields the page shows."""
    if not isinstance(t, dict) or not isinstance(t.get("id"), str) or not t["id"].isdigit():
        return None
    replies = t.get("replies")
    return {
        "id": t["id"][:20],
        "title": _text(t.get("title"), 200),
        "tags": _tags(t.get("tags")),
        "created": _text(t.get("created"), 40),
        "replies": replies if isinstance(replies, int) and 0 <= replies < 100000 else 0,
        "closed": bool(t.get("archived") or t.get("locked")),
    }


def clean_message(m):
    if not isinstance(m, dict):
        return None
    files = m.get("attachments") if isinstance(m.get("attachments"), list) else []
    return {
        "author": _text(m.get("author"), 80),
        "text": _text(m.get("text"), 4100),
        "date": _text(m.get("date"), 40),
        "files": [_text(f.get("name"), 100) for f in files[:10] if isinstance(f, dict)],
    }


class Feed:
    def __init__(self, base, guild=None, clock=None, opener=None):
        import time
        self.base = base
        self.guild = guild
        self.clock = clock or time.time
        self.opener = opener or urllib.request.build_opener()
        self.cache = {}
        self.lock = threading.Lock()

    def _get(self, path):
        req = urllib.request.Request(self.base + path, headers={"Accept": "application/json",
                                                                "User-Agent": "rayelinux.com"})
        try:
            with self.opener.open(req, timeout=FEED_TIMEOUT) as r:
                return r.status, json.loads(r.read(4_000_000))
        except urllib.error.HTTPError as exc:
            return exc.code, None
        except (OSError, ValueError):
            return 502, None

    def _cached(self, key, fetch):
        now = self.clock()
        with self.lock:
            hit = self.cache.get(key)
            if hit and now - hit[0] < FEED_TTL:
                return hit[1]
        value = fetch()
        if value[0] in (200, 404):
            with self.lock:
                if len(self.cache) >= FEED_KEYS:
                    self.cache.clear()
                self.cache[key] = (now, value)
        elif hit:
            return hit[1]  # an older answer beats an error
        return value

    def topics(self):
        """(status, payload) of the list."""
        def fetch():
            status, data = self._get("/api/public/raye/bugs")
            if status != 200 or not isinstance(data, dict) or not isinstance(data.get("bugs"), list):
                return (502, {"ok": False, "error": "unavailable"})
            bugs = [b for b in map(clean_topic, data["bugs"][:500]) if b]
            return (200, {"ok": True, "tags": _tags(data.get("tags")), "bugs": bugs})
        if not self.base:
            return 503, {"ok": False, "error": "not_configured"}
        return self._cached("list", fetch)

    def topic(self, ident):
        if not self.base:
            return 503, {"ok": False, "error": "not_configured"}
        if not (isinstance(ident, str) and ident.isdigit() and 0 < len(ident) <= 20):
            return 404, {"ok": False, "error": "not_found"}

        def fetch():
            status, data = self._get("/api/public/raye/bugs/" + ident)
            if status == 404:
                return (404, {"ok": False, "error": "not_found"})
            if status != 200 or not isinstance(data, dict):
                return (502, {"ok": False, "error": "unavailable"})
            topic = clean_topic(data)
            if not topic or not isinstance(data.get("messages"), list):
                return (502, {"ok": False, "error": "unavailable"})
            topic["messages"] = [m for m in map(clean_message, data["messages"][:100]) if m]
            if self.guild:
                topic["discord"] = f"https://discord.com/channels/{self.guild}/{topic['id']}"
            return (200, dict(ok=True, **topic))
        return self._cached("t" + ident, fetch)
