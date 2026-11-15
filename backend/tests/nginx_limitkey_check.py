#!/usr/bin/python3
"""Runs the rate-limit key map through a real nginx (the one installed on
the server) and compares it with ipaddress for thousands of IPv6 forms.

    python3 tests/nginx_limitkey_check.py path/to/raye-site-limitkey.conf
"""

import http.client
import os
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from limitkey_cases import cases, expected  # noqa: E402

CONF = """
pid {d}/nginx.pid;
error_log {d}/error.log;
events {{}}
http {{
    access_log off;
    client_body_temp_path {d}; proxy_temp_path {d}; fastcgi_temp_path {d};
    uwsgi_temp_path {d}; scgi_temp_path {d};
    include {map};
    server {{
        listen 127.0.0.1:{port};
        set_real_ip_from 127.0.0.1;
        real_ip_header X-Forwarded-For;
        location / {{ return 200 "$raye_limit_key"; }}
    }}
}}
"""


def main():
    mapfile = os.path.abspath(sys.argv[1])
    with tempfile.TemporaryDirectory() as d:
        port = 18099
        with open(os.path.join(d, "nginx.conf"), "w") as f:
            f.write(CONF.format(d=d, map=mapfile, port=port))
        subprocess.run(["/usr/sbin/nginx", "-p", d, "-c", "nginx.conf", "-e",
                        os.path.join(d, "error.log")], check=True)
        try:
            time.sleep(0.3)
            bad = 0
            all_cases = cases()
            conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
            for address in all_cases:
                conn.request("GET", "/", headers={"X-Forwarded-For": address})
                got = conn.getresponse().read().decode()
                if got != expected(address):
                    bad += 1
                    print(f"FAIL {address}: nginx {got!r}, want {expected(address)!r}")
            print(f"{len(all_cases)} addresses, {bad} wrong")
        finally:
            subprocess.run(["/usr/sbin/nginx", "-p", d, "-c", "nginx.conf", "-e",
                            os.path.join(d, "error.log"), "-s", "stop"], check=False)
            time.sleep(0.3)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
