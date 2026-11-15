"""The nginx map that turns an IPv6 address into its /64 must agree with
ipaddress for every short form an address can take. The map is applied
here with Python's re (its patterns use nothing PCRE-only);
nginx_limitkey_check.py runs the same cases through a real nginx."""

import os
import re
import unittest

from limitkey_cases import cases, expected

MAP = os.path.join(os.path.dirname(__file__), "..", "..", "deploy", "nginx",
                   "raye-site-limitkey.conf")


def load_map():
    rules = []
    with open(MAP, encoding="utf-8") as f:
        for line in f:
            m = re.match(r'\s*"~(.+)"\s+"(.+)";\s*$', line)
            if m:
                rules.append((re.compile(m.group(1)), m.group(2)))
    return rules


def apply(rules, address):
    for pattern, value in rules:
        m = pattern.search(address)
        if m:
            return re.sub(r"\$(\d)", lambda g: m.group(int(g.group(1))), value)
    return None  # nginx falls back to the binary IPv4 address


class LimitKeyMapTests(unittest.TestCase):
    def test_every_ipv6_short_form(self):
        rules = load_map()
        self.assertEqual(len(rules), 8)
        for address in cases():
            with self.subTest(address=address):
                self.assertEqual(apply(rules, address), expected(address))

    def test_ipv4_falls_through(self):
        rules = load_map()
        for address in ("192.168.50.200", "203.0.113.4", "1.2.3.4"):
            self.assertIsNone(apply(rules, address))


if __name__ == "__main__":
    unittest.main()
