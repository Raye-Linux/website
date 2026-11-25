"""What a search engine reads on the V1 site: the sitemap (every page in both
languages, with its hreflang pair), robots.txt, the IndexNow key file and the
schema.org data of each page. Every address is on https://www.rayelinux.com
(build_pages.URL); the bare name redirects to it at the server.

A data block, not a script: the CSP does not apply to it and nothing runs."""

import json

import site_v1_download as download
import site_v1_text as V


def pages():
    """(key, fr path, en path) of every page, the home page first."""
    return [(k, p["path"]["fr"], p["path"]["en"]) for k, p in V.PAGES.items()]


def lastmod(site):
    """The date of the last published release; a build must give the same
    files twice, so it is never today's date."""
    return site.b.release_info()["date"]


def sitemap(site):
    url, day = site.b.URL, lastmod(site)
    rows = []
    for key, fr, en in pages():
        for here in (fr, en):
            rows.append(f"""<url>
<loc>{url}{here}</loc>
<lastmod>{day}</lastmod>
<xhtml:link rel="alternate" hreflang="fr" href="{url}{fr}"/>
<xhtml:link rel="alternate" hreflang="en" href="{url}{en}"/>
<xhtml:link rel="alternate" hreflang="x-default" href="{url}{fr}"/>
</url>""")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(rows) + "\n</urlset>\n")


def robots(site):
    return f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {site.b.URL}/sitemap.xml\n"


def ldjson(site, lang, key, title):
    """The schema.org block of a page, or "" (the 404 has none)."""
    url, b = site.b.URL, site.b
    org = {"@type": "Organization", "@id": url + "/#organization", "name": "Raye Linux",
           "url": url + "/", "logo": url + "/assets/raye-mark.svg",
           "email": "bonjour@rayelinux.com",
           "sameAs": ["https://github.com/Raye-Linux", "https://codeberg.org/Raye-Linux",
                      "https://gitlab.com/raye-linux", b.DISCORD]}
    if key == "home":
        app = {"@type": "SoftwareApplication", "@id": url + "/#software", "name": "Raye Linux",
               "description": V.HOME["description"][lang],
               "applicationCategory": "OperatingSystem", "operatingSystem": "Linux",
               "softwareVersion": V.VERSION, "isAccessibleForFree": True,
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CAD"},
               "inLanguage": ["fr", "en"], "url": url + site.path("home", lang),
               "publisher": {"@id": url + "/#organization"}}
        if site.has_shot("desktop", lang):
            app["screenshot"] = f"{url}/assets/shots/desktop-{lang}-1600.jpg"
        if not download.is_pending():
            info = b.release_info()
            app["downloadUrl"] = info["urls"]["r2"]
            app["datePublished"] = info["date"]
        site_ = {"@type": "WebSite", "@id": url + "/#website", "name": "Raye Linux", "url": url + "/",
                 "inLanguage": lang, "publisher": {"@id": url + "/#organization"}}
        data = {"@context": "https://schema.org", "@graph": [site_, org, app]}
    else:
        data = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": site.name("home", lang),
                     "item": url + site.path("home", lang)},
                    {"@type": "ListItem", "position": 2, "name": site.name(key, lang),
                     "item": url + site.path(key, lang)}]}
    text = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return f'\n<script type="application/ld+json">\n{text}\n</script>'
