#!/usr/bin/python3
"""Smoke test of an installed backend, on a throw-away database.

Starts the real server (raye-site-server) on another port with a temporary
database and a fake SMTP server (STARTTLS, private CA, certificate for
mail.example.org), signs up, reads the links from the mail that arrives,
then confirms and unsubscribes. Leaves nothing behind.

    python3 tests/e2e_smoke.py [/opt/raye-site/backend]
"""

import http.client
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
BACKEND = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..")
sys.path[:0] = [HERE, BACKEND]

from helpers import FakeSMTP, TempDir, free_port, make_certs, write_smtp_env  # noqa: E402


def request(port, method, path, body=None, headers=None):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request(method, path, body=body, headers=headers or {})
    r = conn.getresponse()
    data = r.read().decode("utf-8", "replace")
    conn.close()
    return r.status, data


def check(label, ok):
    print(("ok   " if ok else "FAIL ") + label)
    if not ok:
        raise SystemExit(1)


def main():
    backend = BACKEND
    from raye_site.store import Store

    with TempDir() as tmp:
        ca, cert, key = make_certs(tmp)
        port = free_port()
        with FakeSMTP(cert, key) as smtp:
            write_smtp_env(os.path.join(tmp, "smtp.env"), port=smtp.port)
            env = {"PATH": "/usr/bin:/bin", "RAYE_SITE_DB": os.path.join(tmp, "site.db"),
                   "RAYE_SITE_PORT": str(port),
                   "RAYE_SITE_SMTP_ENV": os.path.join(tmp, "smtp.env"),
                   "RAYE_SITE_SMTP_CAFILE": ca}
            server = subprocess.Popen(
                [sys.executable, "-E", "-s", "-B", os.path.join(backend, "raye-site-server")],
                env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            try:
                for _ in range(50):
                    try:
                        if request(port, "GET", "/api/health")[0] == 200:
                            break
                    except OSError:
                        time.sleep(0.1)
                status, body = request(
                    port, "POST", "/api/subscribe",
                    json.dumps({"email": "essai@rayelinux.com", "lang": "fr", "consent": True}),
                    {"Content-Type": "application/json", "X-Real-IP": "203.0.113.7"})
                check("signup answered 200", status == 200 and json.loads(body)["ok"])
                for _ in range(100):
                    if smtp.messages:
                        break
                    time.sleep(0.1)
                check("confirmation mail delivered over STARTTLS",
                      bool(smtp.messages) and smtp.messages[0]["tls"])
                msg = smtp.messages[0]["msg"]
                check("mail has List-Unsubscribe and One-Click",
                      "https://" in msg["List-Unsubscribe"]
                      and msg["List-Unsubscribe-Post"] == "List-Unsubscribe=One-Click")
                text = msg.get_body(("plain",)).get_content()
                confirm = re.search(r"/api/confirm\?t=([A-Za-z0-9_-]{43})", text).group(1)
                unsub = re.search(r"/api/unsubscribe\?t=([A-Za-z0-9_-]{43})", text).group(1)

                status, page = request(port, "GET", "/api/confirm?t=" + confirm)
                check("GET confirm shows a button and confirms nothing",
                      status == 200 and 'method="post"' in page
                      and Store(env["RAYE_SITE_DB"]).counts()["confirmed"] == 0)
                status, page = request(port, "POST", "/api/confirm",
                                       urllib.parse.urlencode({"t": confirm}),
                                       {"Content-Type": "application/x-www-form-urlencoded"})
                check("POST confirm confirms",
                      status == 200 and Store(env["RAYE_SITE_DB"]).counts()["confirmed"] == 1)
                status, page = request(port, "POST", "/api/unsubscribe?t=" + unsub,
                                       "List-Unsubscribe=One-Click",
                                       {"Content-Type": "application/x-www-form-urlencoded"})
                counts = Store(env["RAYE_SITE_DB"]).counts()
                check("one-click unsubscribe", status == 200 and counts["confirmed"] == 0
                      and counts["unsubscribed"] == 1)
                status, _ = request(port, "GET", "/api/confirm?t=" + confirm)
                check("old confirmation link is dead after unsubscribe", status == 404)
            finally:
                server.terminate()
                server.wait(timeout=10)
    print("all good, temporary files removed")


if __name__ == "__main__":
    main()
