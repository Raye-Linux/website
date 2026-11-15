#!/usr/bin/env python3
"""Writes the Raye eye as SVG, from the same grid as the theme's eye.py:
an almond made of two circles, an amber-ringed iris, three scanline
slices and their trails. Run it again after changing the numbers."""

import math
import os

CX, CY = 120, 100
A, B = 76, 34
STROKE = 5
IRIS, PUPIL = 25, 10
SLICES = [(CY - 15, 4, 7), (CY + 5, 3, -5), (CY + 19, 2, 10)]
R = (A * A + B * B) / (2 * B)

VIOLET, MAGENTA, LILAC = "#7B3CFF", "#D946EF", "#B88CFF"
AMBER, INK, DEEP, WHITE = "#E0A458", "#12081F", "#2A1052", "#F3EAFF"


def almond(inset=0):
    r = R - inset
    half = math.sqrt(r * r - (R - B) ** 2)
    x0, x1 = CX - half, CX + half
    return (f"M{x0:.2f} {CY}A{r:.2f} {r:.2f} 0 0 1 {x1:.2f} {CY}"
            f"A{r:.2f} {r:.2f} 0 0 1 {x0:.2f} {CY}Z")


def eye_defs(p):
    return f"""<defs>
<linearGradient id="{p}rim" x1="{CX - A}" y1="0" x2="{CX + A}" y2="0" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{MAGENTA}"/></linearGradient>
<radialGradient id="{p}iris" cx="{CX}" cy="{CY}" r="{IRIS}" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="{AMBER}"/><stop offset="{(PUPIL + 1) / IRIS:.3f}" stop-color="{AMBER}"/>
<stop offset="{(PUPIL + 4) / IRIS:.3f}" stop-color="{LILAC}"/>
<stop offset="{(IRIS - 6) / IRIS:.3f}" stop-color="{VIOLET}"/><stop offset="1" stop-color="{DEEP}"/></radialGradient>
<clipPath id="{p}inner"><path d="{almond(STROKE)}"/></clipPath>
<clipPath id="{p}rest">{''.join(f'<rect x="0" y="{y0}" width="320" height="{y1 - y0}"/>' for y0, y1 in gaps())}</clipPath>
{''.join(f'<clipPath id="{p}s{i}"><rect x="0" y="{t - 0.35}" width="320" height="{h + 0.7}"/></clipPath>' for i, (t, h, _) in enumerate(SLICES))}
<g id="{p}eye">
<path d="{almond(STROKE)}" fill="{INK}"/>
<circle cx="{CX}" cy="{CY}" r="{IRIS}" fill="url(#{p}iris)" clip-path="url(#{p}inner)"/>
<circle cx="{CX}" cy="{CY}" r="{PUPIL}" fill="#000"/>
<circle cx="{CX - 6}" cy="{CY - 6}" r="3" fill="{WHITE}"/>
<circle cx="{CX + 4}" cy="{CY + 4}" r="1.2" fill="{WHITE}"/>
<path d="{almond()}{almond(STROKE)}" fill="url(#{p}rim)" fill-rule="evenodd"/>
</g>
{''.join(trail_gradient(p, i, dx) for i, (_, _, dx) in enumerate(SLICES))}
</defs>"""


def gaps():
    edges = [0]
    for t, h, _ in SLICES:
        edges += [t, t + h]
    edges.append(240)
    return list(zip(edges[::2], edges[1::2]))


def trail_gradient(p, i, dx):
    colour = MAGENTA if dx > 0 else LILAC
    return (f'<linearGradient id="{p}t{i}"><stop offset="0" stop-color="{colour}"/>'
            f'<stop offset=".45" stop-color="{colour}" stop-opacity=".38"/>'
            f'<stop offset="1" stop-color="{colour}" stop-opacity="0"/></linearGradient>')


def body(p, trails):
    out = [f'<use href="#{p}eye" clip-path="url(#{p}rest)"/>']
    for i, (top, h, dx) in enumerate(SLICES):
        out.append(f'<g transform="translate({dx} 0)"><use href="#{p}eye" '
                   f'clip-path="url(#{p}s{i})"/></g>')
        if trails:
            x = CX + A - 6 + max(dx, 0) + 14
            out.append(f'<rect x="{x}" y="{top + 1}" width="77" height="1.4" fill="url(#{p}t{i})"/>')
    return "\n".join(out)


def svg(view, trails, p, title, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" role="img" '
            f'aria-label="{title}">\n<title>{title}</title>\n{eye_defs(p)}\n{extra}'
            f'{body(p, trails)}\n</svg>\n')


def main():
    out = os.path.join(os.path.dirname(__file__), "..", "site", "assets")
    files = {
        "raye-eye.svg": svg("40 60 252 80", True, "e", "Raye"),
        "raye-mark.svg": svg("40 62 172 76", False, "m", "Raye"),
        "favicon.svg": svg("38 16 168 168", False, "f", "Raye",
                           '<rect x="38" y="16" width="168" height="168" rx="38" fill="#141318"/>\n'),
    }
    for name, text in files.items():
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(text)


if __name__ == "__main__":
    main()
