#!/usr/bin/env python3
"""Tell search engines (Bing, Yandex, Seznam, Naver) which pages changed,
through IndexNow. Run it after a deploy.

  tools/indexnow.py                 # shows what would be sent, sends nothing
  tools/indexnow.py --send          # every page of site/sitemap.xml
  tools/indexnow.py --send /en/download/ /telecharger/   # only these

The key is INDEXNOW_KEY in build_pages.py; the site serves it at /<key>.txt,
which is how the engines know the request comes from the site's owner.
"""

import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
import build_pages  # noqa: E402

ENDPOINT = "https://api.indexnow.org/indexnow"
SM = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def sitemap_urls(path=os.path.join(TOOLS, "..", "site", "sitemap.xml")):
    tree = ET.parse(path)
    return [u.find(SM + "loc").text for u in tree.getroot().findall(SM + "url")]


def payload(urls):
    url, key = build_pages.URL, build_pages.INDEXNOW_KEY
    host = url.split("://", 1)[1]
    for u in urls:
        if not u.startswith(url + "/"):
            raise SystemExit(f"not a page of {host}: {u}")
    return {"host": host, "key": key, "keyLocation": f"{url}/{key}.txt", "urlList": urls}


def main(argv):
    send = "--send" in argv
    paths = [a for a in argv if a != "--send"]
    urls = [build_pages.URL + p for p in paths] if paths else sitemap_urls()
    body = payload(urls)
    if not send:
        print(json.dumps(body, indent=1))
        print("dry run: add --send to submit", file=sys.stderr)
        return 0
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json; charset=utf-8",
                 "User-Agent": "raye-site-indexnow/1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            status = r.status
    except urllib.error.HTTPError as e:
        status = e.code
    print(f"IndexNow: HTTP {status} for {len(urls)} page(s)")
    # 200 accepted, 202 accepted while the key is being checked
    return 0 if status in (200, 202) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
