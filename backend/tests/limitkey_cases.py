"""IPv6 addresses for the /64 rate-limit key tests, and what the key must be."""

import ipaddress
import random


def expected(address: str) -> str:
    ip = ipaddress.IPv6Address(address)
    groups = ip.exploded.split(":")[:4]
    return "6:" + ":".join(format(int(g, 16), "x") for g in groups)


def cases(n: int = 3000, seed: int = 64) -> list[str]:
    """Addresses in short form, with zero runs everywhere, so every way
    "::" can land is covered."""
    rnd = random.Random(seed)
    out = ["::", "::1", "1::", "2001:db8::", "2001:db8::1", "2001:db8:0:0:1::",
           "2001:db8:0:0:1:0:0:1", "::1:2:3:4:5", "::1:2:3:4:5:6", "1::2:3:4:5:6",
           "1:2:3:4:5:6:7:8", "fe80::1", "2607:f8b0:4004:c1b::64", "1:0:0:2::",
           "0:0:1::", "1:2:3::"]
    for _ in range(n):
        words = [rnd.choice([0, 0, 0, rnd.randrange(1, 16), rnd.randrange(65536)])
                 for _ in range(8)]
        out.append(str(ipaddress.IPv6Address(b"".join(w.to_bytes(2, "big") for w in words))))
    return out
