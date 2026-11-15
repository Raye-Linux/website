"""Shared bits for the backend tests: a temp database, a clock we can move,
and a small SMTP server that records what it receives."""

import os
import shutil
import socket
import socketserver
import ssl
import subprocess
import tempfile
import threading
from email import message_from_bytes, policy

from raye_site.config import Config, SmtpSettings


class Clock:
    def __init__(self, start=1_800_000_000.0):
        self.now = start

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


def make_config(tmp, **over):
    base = dict(
        db_path=os.path.join(tmp, "site.db"),
        site_url="https://rayelinux.com",
        listen_host="127.0.0.1",
        listen_port=0,
        smtp_env_paths=(os.path.join(tmp, "smtp.env"),),
        smtp_tls_name="mail.example.org",
        smtp_cafile=None,
    )
    base.update(over)
    return Config(**base)


def write_smtp_env(path, host="127.0.0.1", port=2525, user="bonjour@rayelinux.com",
                   password="s3cret-pass", sender="Raye Linux <bonjour@rayelinux.com>"):
    with open(path, "w", encoding="utf-8") as f:
        f.write("# test\n")
        f.write(f"SMTP_HOST={host}\nSMTP_PORT={port}\nSMTP_USER={user}\n")
        f.write(f"SMTP_PASSWORD='{password}'\nSMTP_FROM=\"{sender}\"\n")


class TempDir:
    def __enter__(self):
        self.path = tempfile.mkdtemp(prefix="raye-site-test-")
        return self.path

    def __exit__(self, *exc):
        shutil.rmtree(self.path, ignore_errors=True)


def make_certs(folder):
    """A private CA and a server certificate for mail.example.org."""
    def run(*args):
        subprocess.run(args, check=True, cwd=folder, capture_output=True)

    run("openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "2",
        "-keyout", "ca.key", "-out", "ca.pem", "-subj", "/CN=Test CA",
        "-addext", "basicConstraints=critical,CA:TRUE",
        "-addext", "keyUsage=critical,keyCertSign,cRLSign")
    run("openssl", "req", "-newkey", "rsa:2048", "-nodes", "-keyout", "srv.key",
        "-out", "srv.csr", "-subj", "/CN=mail.example.org")
    with open(os.path.join(folder, "ext.cnf"), "w") as f:
        f.write("subjectAltName=DNS:mail.example.org\n"
                "extendedKeyUsage=serverAuth\n")
    run("openssl", "x509", "-req", "-in", "srv.csr", "-CA", "ca.pem", "-CAkey", "ca.key",
        "-CAcreateserial", "-out", "srv.pem", "-days", "2", "-extfile", "ext.cnf")
    return (os.path.join(folder, "ca.pem"), os.path.join(folder, "srv.pem"),
            os.path.join(folder, "srv.key"))


class FakeSMTP:
    """Just enough ESMTP for smtplib: EHLO, STARTTLS, AUTH PLAIN/LOGIN, MAIL,
    RCPT, DATA, RSET, QUIT. Records every accepted message."""

    def __init__(self, certfile=None, keyfile=None, password="s3cret-pass",
                 offer_tls=True, reject_rcpt=False):
        self.messages = []
        self.auth_ok = []
        self.password = password
        self.offer_tls = offer_tls
        self.reject_rcpt = reject_rcpt
        self.ctx = None
        if certfile:
            self.ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.ctx.load_cert_chain(certfile, keyfile)
        outer = self

        class Handler(socketserver.StreamRequestHandler):
            def handle(self):
                try:
                    outer._session(self)
                finally:
                    tls_sock = getattr(self, "tls_sock", None)
                    if tls_sock is not None:
                        tls_sock.close()

        class Server(socketserver.ThreadingTCPServer):
            allow_reuse_address = True
            daemon_threads = True

        self.server = Server(("127.0.0.1", 0), Handler)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *exc):
        self.server.shutdown()
        self.server.server_close()

    def _session(self, h):
        sock = h.connection
        rfile, wfile = h.rfile, h.wfile
        tls = False
        authed = False

        def say(line):
            wfile.write((line + "\r\n").encode())
            wfile.flush()

        say("220 fake ESMTP")
        mail_from, rcpts = None, []
        while True:
            raw = rfile.readline()
            if not raw:
                return
            line = raw.decode("utf-8", "replace").rstrip("\r\n")
            cmd = line.split(" ", 1)[0].upper()
            if cmd in ("EHLO", "HELO"):
                caps = ["250-fake"]
                if self.ctx and self.offer_tls and not tls:
                    caps.append("250-STARTTLS")
                if tls or not self.offer_tls:
                    caps.append("250-AUTH PLAIN LOGIN")
                caps.append("250 8BITMIME")
                for c in caps:
                    say(c)
            elif cmd == "STARTTLS" and self.ctx:
                say("220 go ahead")
                try:
                    sock = self.ctx.wrap_socket(sock, server_side=True)
                except (ssl.SSLError, OSError):
                    return
                h.tls_sock = sock
                rfile = sock.makefile("rb")
                wfile = sock.makefile("wb")
                tls = True
            elif cmd == "AUTH":
                import base64
                parts = line.split(" ")
                if parts[1].upper() == "PLAIN":
                    blob = parts[2] if len(parts) > 2 else None
                    if blob is None:
                        say("334 ")
                        blob = rfile.readline().decode().strip()
                    _, user, pw = base64.b64decode(blob).decode().split("\x00")
                else:
                    say("334 VXNlcm5hbWU6")
                    user = base64.b64decode(rfile.readline().strip()).decode()
                    say("334 UGFzc3dvcmQ6")
                    pw = base64.b64decode(rfile.readline().strip()).decode()
                if pw == self.password:
                    authed = True
                    self.auth_ok.append((user, tls))
                    say("235 ok")
                else:
                    say("535 bad credentials")
            elif cmd == "MAIL":
                if not authed:
                    say("530 auth first")
                    continue
                mail_from = line[10:]
                rcpts = []
                say("250 ok")
            elif cmd == "RCPT":
                if self.reject_rcpt:
                    say("550 no such user")
                    continue
                rcpts.append(line[8:])
                say("250 ok")
            elif cmd == "DATA":
                say("354 end with .")
                data = []
                while True:
                    l = rfile.readline()
                    if l in (b".\r\n", b".\n", b""):
                        break
                    if l.startswith(b".."):
                        l = l[1:]
                    data.append(l)
                body = b"".join(data)
                self.messages.append({
                    "from": mail_from, "rcpts": rcpts, "tls": tls,
                    "msg": message_from_bytes(body, policy=policy.default),
                })
                say("250 queued")
            elif cmd == "RSET":
                say("250 ok")
            elif cmd == "NOOP":
                say("250 ok")
            elif cmd == "QUIT":
                say("221 bye")
                return
            else:
                say("502 nope")


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port
