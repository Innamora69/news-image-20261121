#!/usr/bin/env python3
"""Front page for 21 November 2026, second revision.

Pillow only, no network, no clock, no randomness, so the bytes are
the same on every run: python3 draw.py
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu"

PAINT = {"paper": (247, 243, 232), "ink": (22, 22, 22), "navy": (20, 38, 74),
         "deep": (11, 25, 51), "red": (192, 57, 43), "gold": (217, 164, 65),
         "teal": (15, 118, 110), "pale": (228, 235, 242), "steel": (82, 100, 130),
         "grey": (112, 112, 112), "white": (255, 255, 255), "flame": (255, 150, 40),
         "ember": (255, 205, 90)}

FONTS = {}
for _k, _f, _s in [("title", "DejaVuSans-Bold.ttf", 46), ("dateline", "DejaVuSans-Bold.ttf", 22),
                   ("badge", "DejaVuSans-Bold.ttf", 17), ("kicker", "DejaVuSans-Bold.ttf", 19),
                   ("headline", "DejaVuSans-Bold.ttf", 36), ("standfirst", "DejaVuSans.ttf", 20),
                   ("card_title", "DejaVuSans-Bold.ttf", 23), ("card_text", "DejaVuSans.ttf", 17),
                   ("place", "DejaVuSans-Bold.ttf", 15), ("strip_title", "DejaVuSans-Bold.ttf", 22),
                   ("strip_text", "DejaVuSans.ttf", 16), ("ticker_title", "DejaVuSans-Bold.ttf", 21),
                   ("ticker", "DejaVuSans.ttf", 16), ("caption", "DejaVuSans-Bold.ttf", 16)]:
    FONTS[_k] = ImageFont.truetype(os.path.join(FD, _f), _s)


def rect(d, x0, y0, x1, y1, fill, outline=None, width=1):
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)


def txt(d, x, y, s, f, c):
    d.text((x, y), s, font=f, fill=c)


def ell(d, x0, y0, x1, y1, fill):
    d.ellipse([x0, y0, x1, y1], fill=fill)


def poly(d, pts, fill):
    d.polygon(pts, fill=fill)


def seg(d, pts, fill, w=3):
    d.line(pts, fill=fill, width=w, joint="curve")


def star_pts(cx, cy, outer, inner, count=8):
    pts = []
    for i in range(count * 2):
        r = outer if i % 2 == 0 else inner
        a = -math.pi / 2 + i * math.pi / count
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


class Flow:
    def __init__(self, d):
        self.d = d

    def wrap(self, s, f, width):
        lines = []
        for part in s.split("\n"):
            words = part.split()
            if not words:
                lines.append("")
                continue
            cur = words[0]
            for w in words[1:]:
                nxt = cur + " " + w
                if self.d.textlength(nxt, font=f) <= width:
                    cur = nxt
                else:
                    lines.append(cur)
                    cur = w
            lines.append(cur)
        return lines

    def stack(self, x, y, lines, f, c, lead):
        for ln in lines:
            txt(self.d, x, y, ln, f, c)
            y += lead
        return y

    def pack(self, items, f, width, limit=3):
        lines, cur = [], ""
        for item in items:
            nxt = item if not cur else cur + " \u25c6 " + item
            if self.d.textlength(nxt, font=f) <= width:
                cur = nxt
            else:
                lines.append(cur)
                cur = item
                if len(lines) == limit:
                    return lines
        if cur and len(lines) < limit:
            lines.append(cur)
        return lines


def rose(d, cx, cy, r):
    poly(d, star_pts(cx, cy, r, r * 0.38, 8), PAINT["gold"])
    ell(d, cx - r * 0.32, cy - r * 0.32, cx + r * 0.32, cy + r * 0.32, PAINT["navy"])
    ell(d, cx - 3, cy - 3, cx + 3, cy + 3, PAINT["gold"])


def night_city(d, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    rect(d, x0, y0, x1, y1, PAINT["deep"])
    for sx, sy in [(0.07, 0.09), (0.24, 0.05), (0.41, 0.13), (0.58, 0.07),
                   (0.73, 0.15), (0.88, 0.06), (0.95, 0.19), (0.50, 0.04)]:
        ell(d, x0 + sx * w - 2, y0 + sy * h - 2, x0 + sx * w + 2, y0 + sy * h + 2, PAINT["white"])
    ground = y1 - 34
    for rx, rw, rh in [(0.02, 0.14, 0.50), (0.20, 0.12, 0.66), (0.36, 0.15, 0.44),
                       (0.55, 0.12, 0.60), (0.71, 0.14, 0.48), (0.87, 0.11, 0.56)]:
        tx, tw, th = x0 + rx * w, rw * w, rh * h
        rect(d, tx, ground - th, tx + tw, ground, PAINT["steel"])
        for ri in range(int(th // 26)):
            for ci in range(int(tw // 20)):
                if (ri + ci) % 3 == 0:
                    continue
                wx, wy = tx + 7 + ci * 20, ground - th + 10 + ri * 26
                rect(d, wx, wy, wx + 8, wy + 10, PAINT["gold"])
    rect(d, x0, ground, x1, y1, (40, 44, 58))
    d.line([x1 - 8, y0 + 12, x0 + 0.58 * w, y0 + 0.42 * h], fill=PAINT["red"], width=5)
    ell(d, x1 - 24, y0 + 2, x1 - 4, y0 + 22, PAINT["red"])
    d.line([x1 - 70, y0 + 52, x0 + 0.66 * w, y0 + 0.50 * h], fill=PAINT["flame"], width=4)
    for sx, sy, sr in [(0.86, 0.16, 8), (0.82, 0.22, 6), (0.78, 0.27, 4)]:
        ell(d, x0 + sx * w - sr, y0 + sy * h - sr, x0 + sx * w + sr, y0 + sy * h + sr, (205, 205, 205))
    for bx, by in [(x0 + 0.28 * w, ground - 0.68 * h), (x0 + 0.62 * w, ground - 0.62 * h)]:
        poly(d, star_pts(bx, by, 26, 10, 8), PAINT["flame"])
        poly(d, star_pts(bx, by, 13, 5, 8), PAINT["ember"])
    txt(d, x0 + 12, y1 - 28, "400+ DRONES  \u00b7  110 MISSILES", FONTS["caption"], PAINT["white"])


def art_market(d, x0, y0, x1, y1):
    rect(d, x0, y0, x1, y1, PAINT["deep"])
    pts = [(x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)) for fx, fy in
           [(0.06, 0.30), (0.20, 0.38), (0.34, 0.34), (0.48, 0.55),
            (0.62, 0.52), (0.76, 0.72), (0.90, 0.68)]]
    seg(d, pts, PAINT["white"])
    for px, py in pts:
        ell(d, px - 4, py - 4, px + 4, py + 4, PAINT["gold"])
    lx, ly = pts[-1]
    poly(d, [(lx, ly + 14), (lx - 9, ly - 2), (lx + 9, ly - 2)], PAINT["red"])
    txt(d, x1 - 96, y0 + 6, "-3.7%", FONTS["card_title"], PAINT["red"])


def art_justice(d, x0, y0, x1, y1):
    rect(d, x0, y0, x1, y1, PAINT["pale"])
    cx = (x0 + x1) // 2
    rect(d, cx - 3, y0 + 8, cx + 3, y1 - 12, PAINT["navy"])
    d.line([cx - 120, y0 + 16, cx + 120, y0 + 16], fill=PAINT["navy"], width=4)
    ell(d, cx - 7, y0 + 6, cx + 7, y0 + 20, PAINT["gold"])
    rect(d, cx - 34, y1 - 12, cx + 34, y1 - 8, PAINT["navy"])
    for side in (-1, 1):
        px = cx + side * 120
        d.line([px, y0 + 16, px - 22, y0 + 44], fill=PAINT["navy"], width=2)
        d.line([px, y0 + 16, px + 22, y0 + 44], fill=PAINT["navy"], width=2)
        poly(d, [(px - 26, y0 + 44), (px + 26, y0 + 44), (px, y1 - 14)], PAINT["gold"])


def art_clinic(d, x0, y0, x1, y1):
    rect(d, x0, y0, x1, y1, PAINT["teal"])
    cx, cy = x0 + 60, (y0 + y1) // 2
    d.rounded_rectangle([cx - 26, cy - 26, cx + 26, cy + 26], radius=10, fill=PAINT["white"])
    rect(d, cx - 6, cy - 18, cx + 6, cy + 18, PAINT["teal"])
    rect(d, cx - 18, cy - 6, cx + 18, cy + 6, PAINT["teal"])
    txt(d, x0 + 104, cy - 16, "1 IN 12", FONTS["card_title"], PAINT["white"])
    txt(d, x0 + 104, cy + 12, "TUMOURS UNDETECTED", FONTS["place"], (210, 235, 230))


def art_deal(d, x0, y0, x1, y1):
    rect(d, x0, y0, x1, y1, PAINT["navy"])
    cx, cy = x0 + 70, (y0 + y1) // 2
    for k in range(12):
        a = -math.pi / 2 + k * 2 * math.pi / 12
        poly(d, star_pts(cx + 30 * math.cos(a), cy + 30 * math.sin(a), 6, 2.5, 5), PAINT["gold"])
    txt(d, x0 + 150, cy - 14, "UK \u2013 EU", FONTS["card_title"], PAINT["gold"])
    jx0, jy0, jx1, jy1 = x1 - 150, y0 + 12, x1 - 20, y1 - 12
    rect(d, jx0, jy0, jx1, jy1, (198, 40, 52))
    d.line([jx0, jy0, jx1, jy1], fill=PAINT["white"], width=6)
    d.line([jx1, jy0, jx0, jy1], fill=PAINT["white"], width=6)
    mx, my = (jx0 + jx1) // 2, (jy0 + jy1) // 2
    d.line([mx, jy0, mx, jy1], fill=PAINT["white"], width=8)
    d.line([jx0, my, jx1, my], fill=PAINT["white"], width=8)


def climate_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=PAINT["gold"], width=3)
    ell(d, cx - r, cy - r, cx + r, cy + r, (23, 94, 88))
    d.line([cx - r, cy, cx + r, cy], fill=PAINT["gold"], width=2)
    d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55], outline=PAINT["gold"], width=2)
    d.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45], 0, 360, fill=PAINT["ember"], width=2)


LEAD = ("1 \u00b7 CONFLICT  \u00b7  KYIV & POLAND", "RUSSIA'S MASS STRIKE ON UKRAINE \u2014 MISSILES LAND IN POLAND", "400+ drones and 110 missiles overnight; at least 8 killed in Kyiv. Two missiles and a drone come down on Polish soil \u2014 Warsaw calls it a deliberate provocation.")

CARDS = [
    ("2 \u00b7 MARKETS  \u00b7  NEW YORK", "WALL STREET", "AI SELL-OFF DRAGS S&P INTO CORRECTION", "Wall Street falls 3.7% as AI and chip shares plunge; Nasdaq down 5.3%.", art_market),
    ("3 \u00b7 JUSTICE  \u00b7  THE HAGUE", "THE HAGUE", "MYANMAR GUILTY OF GENOCIDE, COURT RULES", "The ICJ finds Myanmar responsible for genocide of the Rohingya.", art_justice),
    ("4 \u00b7 HEALTH  \u00b7  LONDON", "CLINICAL TRIAL", "CANCER PILL WIPES OUT TUMOURS IN 1 OF 12", "Trial pill daraxonrasib makes pancreatic tumours vanish on scans in 1 of 12 patients.", art_clinic),
    ("5 \u00b7 POLITICS  \u00b7  BRUSSELS", "BRUSSELS", "UK AND EU SIGN LANDMARK POST-BREXIT DEAL", "Three deals on food, carbon markets and youth mobility \u2014 the biggest step since Brexit.", art_deal),
]

ALSO = ["FBI crime database hacked", "Gen Z protests in 25 EU states", "6.9 quake in Peruvian Andes",
        "Indonesia forest fires", "Basra plant fire kills 4", "Palisades arsonist convicted",
        "Bayer pays $7.25bn over Roundup", "GTA 6: $4.9bn on day one",
        "Crypto: $2bn+ liquidated, Bitcoin ~$62K", "NASA halts Perseverance"]


def masthead(d):
    rect(d, 0, 0, 1024, 92, PAINT["navy"])
    rose(d, 52, 46, 28)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=FONTS["title"])
    txt(d, (1024 - tw) / 2, 8, title, FONTS["title"], PAINT["white"])
    day = "SATURDAY 21 NOVEMBER 2026"
    dw = d.textlength(day, font=FONTS["dateline"])
    txt(d, (1024 - dw) / 2, 58, day, FONTS["dateline"], PAINT["gold"])
    tag = "make.fun"
    cw = d.textlength(tag, font=FONTS["badge"])
    d.rounded_rectangle([1024 - cw - 36, 32, 1024 - 16, 64], radius=16, fill=PAINT["gold"])
    txt(d, 1024 - cw - 26, 38, tag, FONTS["badge"], PAINT["navy"])


def card(flow, d, x, y, w, h, item):
    kicker, place, head, body, art = item
    rect(d, x, y, x + w, y + h, PAINT["white"], outline=PAINT["navy"], width=2)
    art(d, x + 2, y + 2, x + w - 2, y + 60)
    txt(d, x + 16, y + 68, kicker, FONTS["kicker"], PAINT["red"])
    heads = flow.wrap(head, FONTS["card_title"], w - 32)[:2]
    after = flow.stack(x + 16, y + 94, heads, FONTS["card_title"], PAINT["ink"], 27)
    bodies = flow.wrap(body, FONTS["card_text"], w - 32)[:2]
    flow.stack(x + 16, after + 6, bodies, FONTS["card_text"], PAINT["ink"], 20)
    txt(d, x + 16, y + h - 24, place, FONTS["place"], PAINT["grey"])


def render():
    img = Image.new("RGB", (W, H), PAINT["paper"])
    d = ImageDraw.Draw(img)
    flow = Flow(d)

    masthead(d)
    rect(d, 0, 92, 1024, 96, PAINT["gold"])

    kicker, head, body = LEAD
    txt(d, 16, 108, kicker, FONTS["kicker"], PAINT["red"])
    heads = flow.wrap(head, FONTS["headline"], 560)
    end = flow.stack(16, 132, heads, FONTS["headline"], PAINT["ink"], 42)
    bodies = flow.wrap(body, FONTS["standfirst"], 560)
    flow.stack(16, end + 8, bodies, FONTS["standfirst"], PAINT["ink"], 25)

    rect(d, 608, 112, 1008, 352, PAINT["paper"], outline=PAINT["navy"], width=2)
    night_city(d, 610, 114, 1006, 350)

    for item, (px, py) in zip(CARDS, [(16, 364), (520, 364), (16, 596), (520, 596)]):
        card(flow, d, px, py, 488, 220, item)

    rect(d, 16, 828, 1008, 892, PAINT["teal"])
    climate_globe(d, 56, 860, 24)
    txt(d, 96, 838, "6 \u00b7 CLIMATE  \u00b7  ANTALYA \u2014 NEARLY 200 NATIONS", FONTS["kicker"], PAINT["ember"])
    txt(d, 96, 860, "COP31 TALKS OVERRUN \u2014 NO FOSSIL-FUEL DEAL", FONTS["strip_title"], PAINT["white"])

    rect(d, 0, 904, 1024, 1024, PAINT["deep"])
    label = "ALSO TODAY \u2014 10 MORE"
    lw = d.textlength(label, font=FONTS["ticker_title"])
    d.rounded_rectangle([16, 914, 16 + lw + 28, 944], radius=14, fill=PAINT["gold"])
    txt(d, 30, 919, label, FONTS["ticker_title"], PAINT["navy"])
    lines = flow.pack(ALSO, FONTS["ticker"], 992, limit=3)
    y = 952
    for ln in lines:
        txt(d, 16, y, ln, FONTS["ticker"], PAINT["white"])
        y += 21

    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "entry.png")
    img.save(target, "PNG")
    print("wrote", target, img.size, os.path.getsize(target), "bytes")


if __name__ == "__main__":
    render()
