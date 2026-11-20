"""The live numbers of the Discord server on the Community page.

The browser never talks to Discord: this server asks Discord's public
invite address (the same one any invite link preview uses, no token),
keeps the answer ten minutes, and passes on three things only: the server
name and how many members are in it and online. No visitor address,
cookie or identifier ever reaches Discord through the page."""

import json
import re
import threading
import time
import urllib.error
import urllib.request

TTL = 600
TIMEOUT = 8
CODE = re.compile(r"^[A-Za-z0-9-]{2,32}$")


class Community:
    def __init__(self, invite, clock=time.time, opener=None):
        self.invite = invite if isinstance(invite, str) and CODE.match(invite) else None
        self.clock = clock
        self.opener = opener or urllib.request.build_opener()
        self.cached = None          # (time, payload)
        self.lock = threading.Lock()

    def _fetch(self):
        url = "https://discord.com/api/v10/invites/%s?with_counts=true" % self.invite
        req = urllib.request.Request(url, headers={"Accept": "application/json",
                                                   "User-Agent": "rayelinux.com"})
        try:
            with self.opener.open(req, timeout=TIMEOUT) as r:
                data = json.loads(r.read(200_000))
        except (urllib.error.HTTPError, OSError, ValueError):
            return None
        if not isinstance(data, dict):
            return None
        guild = data.get("guild") if isinstance(data.get("guild"), dict) else {}
        members, online = data.get("approximate_member_count"), data.get("approximate_presence_count")
        if not all(isinstance(n, int) and 0 <= n < 10_000_000 for n in (members, online)):
            return None
        name = guild.get("name") if isinstance(guild.get("name"), str) else ""
        return {"ok": True, "name": name[:100], "members": members, "online": online,
                "invite": "https://discord.gg/" + self.invite}

    def status(self):
        """(http status, payload)."""
        if not self.invite:
            return 503, {"ok": False, "error": "not_configured"}
        now = self.clock()
        with self.lock:
            if self.cached and now - self.cached[0] < TTL:
                return 200, self.cached[1]
        fresh = self._fetch()
        with self.lock:
            if fresh:
                self.cached = (now, fresh)
                return 200, fresh
            if self.cached:
                return 200, self.cached[1]     # an older number beats an error
        return 502, {"ok": False, "error": "unavailable"}
