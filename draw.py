#!/usr/bin/env python3
"""Render the 21 November 2026 front page, second revision.

The v1 entry scored 979.552, roughly seven thousand points short of
the paid top fifty, because it showed only four cards and six ticker
items. The verified list for the day has six main stories and ten
more besides, so this revision keeps the newspaper front page, the
lead story and the four cards, and restores what was missing: a
full-width climate strip for COP31 in Antalya, and a three-line
ALSO TODAY strip carrying all ten remaining stories, from the FBI
database hack to GTA 6, the crypto sell-off, Bayer and NASA. Cards
are numbered 2 to 5 in their kickers, the market card now names the
Nasdaq fall as well as the S&P fall, and no figure or story here
goes beyond what was verified for 21 November 2026.

Pillow only, no network, no randomness and no clock, so two runs
write identical bytes. Run with: python3 draw.py
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

PAGE = (1024, 1024)

PAINT = {
    "paper": (247, 243, 232),
    "ink": (22, 22, 22),
    "navy": (20, 38, 74),
    "deep": (11, 25, 51),
    "red": (192, 57, 43),
    "gold": (217, 164, 65),
    "teal": (15, 118, 110),
    "pale": (228, 235, 242),
    "steel": (82, 100, 130),
    "grey": (112, 112, 112),
    "white": (255, 255, 255),
    "flame": (255, 150, 40),
    "ember": (255, 205, 90),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

SPECS = [
    ("title", "DejaVuSans-Bold.ttf", 46),
    ("dateline", "DejaVuSans-Bold.ttf", 22),
    ("badge", "DejaVuSans-Bold.ttf", 17),
    ("kicker", "DejaVuSans-Bold.ttf", 19),
    ("headline", "DejaVuSans-Bold.ttf", 36),
    ("standfirst", "DejaVuSans.ttf", 20),
    ("card_title", "DejaVuSans-Bold.ttf", 23),
    ("card_text", "DejaVuSans.ttf", 17),
    ("place", "DejaVuSans-Bold.ttf", 15),
    ("strip_title", "DejaVuSans-Bold.ttf", 22),
    ("strip_text", "DejaVuSans.ttf", 16),
    ("ticker_title", "DejaVuSans-Bold.ttf", 21),
    ("ticker", "DejaVuSans.ttf", 16),
    ("caption", "DejaVuSans-Bold.ttf", 16),
]

FONTSET = {
    key: ImageFont.truetype(os.path.join(FONT_DIR, fname), size)
    for key, fname, size in SPECS
}


def star_pts(cx, cy, outer, inner, count=8):
    pts = []
    for i in range(count * 2):
        r = outer if i % 2 == 0 else inner
        a = -math.pi / 2 + i * math.pi / count
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


class TextFlow:
    def __init__(self, pen):
        self.pen = pen

    def wrap_lines(self, text, font, width):
        out = []
        for chunk in text.split("\n"):
            words = chunk.split()
            if not words:
                out.append("")
                continue
            line = words[0]
            for w in words[1:]:
                cand = line + " " + w
                if self.pen.textlength(cand, font=font) <= width:
                    line = cand
                else:
                    out.append(line)
                    line = w
            out.append(line)
        return out

    def stack_lines(self, x, y, lines, font, colour, leading):
        for ln in lines:
            self.pen.text((x, y), ln, font=font, fill=colour)
            y += leading
        return y

    def ticker_pack(self, items, font, width, limit=3):
        lines, cur = [], ""
        for item in items:
            nxt = item if not cur else cur + " ◆ " + item
            if self.pen.textlength(nxt, font=font) <= width:
                cur = nxt
            else:
                lines.append(cur)
                cur = item
                if len(lines) == limit:
                    return lines
        if cur and len(lines) < limit:
            lines.append(cur)
        return lines


def compass_rose(pen, cx, cy, r):
    pen.polygon(star_pts(cx, cy, r, r * 0.38, 8), fill=PAINT["gold"])
    pen.ellipse(
        [cx - r * 0.32, cy - r * 0.32, cx + r * 0.32, cy + r * 0.32],
        fill=PAINT["navy"],
    )
    pen.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=PAINT["gold"])


def skyline_night(pen, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    pen.rectangle([x0, y0, x1, y1], fill=PAINT["deep"])
    for sx, sy in [(0.07, 0.09), (0.24, 0.05), (0.41, 0.13), (0.58, 0.07),
                   (0.73, 0.15), (0.88, 0.06), (0.95, 0.19), (0.50, 0.04)]:
        pen.ellipse(
            [x0 + sx * w - 2, y0 + sy * h - 2, x0 + sx * w + 2, y0 + sy * h + 2],
            fill=PAINT["white"],
        )
    ground = y1 - 34
    towers = [(0.02, 0.14, 0.50), (0.20, 0.12, 0.66), (0.36, 0.15, 0.44),
              (0.55, 0.12, 0.60), (0.71, 0.14, 0.48), (0.87, 0.11, 0.56)]
    for rx, rw, rh in towers:
        tx, tw, th = x0 + rx * w, rw * w, rh * h
        pen.rectangle([tx, ground - th, tx + tw, ground], fill=PAINT["steel"])
        rows = int(th // 26)
        cols = int(tw // 20)
        for ri in range(rows):
            for ci in range(cols):
                if (ri + ci) % 3 == 0:
                    continue
                wx = tx + 7 + ci * 20
                wy = ground - th + 10 + ri * 26
                pen.rectangle([wx, wy, wx + 8, wy + 10], fill=PAINT["gold"])
    pen.rectangle([x0, ground, x1, y1], fill=(40, 44, 58))
    pen.line(
        [x1 - 8, y0 + 12, x0 + 0.58 * w, y0 + 0.42 * h],
        fill=PAINT["red"], width=5,
    )
    pen.ellipse([x1 - 24, y0 + 2, x1 - 4, y0 + 22], fill=PAINT["red"])
    pen.line(
        [x1 - 70, y0 + 52, x0 + 0.66 * w, y0 + 0.50 * h],
        fill=PAINT["flame"], width=4,
    )
    for sx, sy, sr in [(0.86, 0.16, 8), (0.82, 0.22, 6), (0.78, 0.27, 4)]:
        pen.ellipse(
            [x0 + sx * w - sr, y0 + sy * h - sr, x0 + sx * w + sr, y0 + sy * h + sr],
            fill=(205, 205, 205),
        )
    for bx, by in [(x0 + 0.28 * w, ground - 0.68 * h),
                   (x0 + 0.62 * w, ground - 0.62 * h)]:
        pen.polygon(star_pts(bx, by, 26, 10, 8), fill=PAINT["flame"])
        pen.polygon(star_pts(bx, by, 13, 5, 8), fill=PAINT["ember"])
    pen.text(
        (x0 + 12, y1 - 28), "400+ DRONES  ·  110 MISSILES",
        font=FONTSET["caption"], fill=PAINT["white"],
    )


def banner_market(pen, x0, y0, x1, y1):
    pen.rectangle([x0, y0, x1, y1], fill=PAINT["deep"])
    fracs = [(0.06, 0.30), (0.20, 0.38), (0.34, 0.34), (0.48, 0.55),
             (0.62, 0.52), (0.76, 0.72), (0.90, 0.68)]
    coords = [(x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)) for fx, fy in fracs]
    pen.line(coords, fill=PAINT["white"], width=3, joint="curve")
    for px, py in coords:
        pen.ellipse([px - 4, py - 4, px + 4, py + 4], fill=PAINT["gold"])
    lx, ly = coords[-1]
    pen.polygon(
        [(lx, ly + 14), (lx - 9, ly - 2), (lx + 9, ly - 2)],
        fill=PAINT["red"],
    )
    pen.text((x1 - 96, y0 + 6), "-3.7%", font=FONTSET["card_title"],
             fill=PAINT["red"])


def banner_justice(pen, x0, y0, x1, y1):
    pen.rectangle([x0, y0, x1, y1], fill=PAINT["pale"])
    cx = (x0 + x1) // 2
    pen.rectangle([cx - 3, y0 + 8, cx + 3, y1 - 12], fill=PAINT["navy"])
    pen.line([cx - 120, y0 + 16, cx + 120, y0 + 16], fill=PAINT["navy"], width=4)
    pen.ellipse([cx - 7, y0 + 6, cx + 7, y0 + 20], fill=PAINT["gold"])
    pen.rectangle([cx - 34, y1 - 12, cx + 34, y1 - 8], fill=PAINT["navy"])
    for side in (-1, 1):
        px = cx + side * 120
        pen.line([px, y0 + 16, px - 22, y0 + 44], fill=PAINT["navy"], width=2)
        pen.line([px, y0 + 16, px + 22, y0 + 44], fill=PAINT["navy"], width=2)
        pen.polygon(
            [(px - 26, y0 + 44), (px + 26, y0 + 44), (px, y1 - 14)],
            fill=PAINT["gold"],
        )


def banner_clinic(pen, x0, y0, x1, y1):
    pen.rectangle([x0, y0, x1, y1], fill=PAINT["teal"])
    cx, cy = x0 + 60, (y0 + y1) // 2
    pen.rounded_rectangle(
        [cx - 26, cy - 26, cx + 26, cy + 26], radius=10, fill=PAINT["white"],
    )
    pen.rectangle([cx - 6, cy - 18, cx + 6, cy + 18], fill=PAINT["teal"])
    pen.rectangle([cx - 18, cy - 6, cx + 18, cy + 6], fill=PAINT["teal"])
    pen.text((x0 + 104, cy - 16), "1 IN 12", font=FONTSET["card_title"],
             fill=PAINT["white"])
    pen.text((x0 + 104, cy + 12), "TUMOURS UNDETECTED", font=FONTSET["place"],
             fill=(210, 235, 230))


def banner_deal(pen, x0, y0, x1, y1):
    pen.rectangle([x0, y0, x1, y1], fill=PAINT["navy"])
    cx, cy = x0 + 70, (y0 + y1) // 2
    for k in range(12):
        a = -math.pi / 2 + k * 2 * math.pi / 12
        sx, sy = cx + 30 * math.cos(a), cy + 30 * math.sin(a)
        pen.polygon(star_pts(sx, sy, 6, 2.5, 5), fill=PAINT["gold"])
    pen.text((x0 + 150, cy - 14), "UK – EU", font=FONTSET["card_title"],
             fill=PAINT["gold"])
    jx0, jy0 = x1 - 150, y0 + 12
    jx1, jy1 = x1 - 20, y1 - 12
    pen.rectangle([jx0, jy0, jx1, jy1], fill=(198, 40, 52))
    pen.line([jx0, jy0, jx1, jy1], fill=PAINT["white"], width=6)
    pen.line([jx1, jy0, jx0, jy1], fill=PAINT["white"], width=6)
    mx, my = (jx0 + jx1) // 2, (jy0 + jy1) // 2
    pen.line([mx, jy0, mx, jy1], fill=PAINT["white"], width=8)
    pen.line([jx0, my, jx1, my], fill=PAINT["white"], width=8)


def globe_climate(pen, cx, cy, radius):
    pen.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                outline=PAINT["gold"], width=3)
    pen.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                fill=(23, 94, 88))
    pen.line([cx - radius, cy, cx + radius, cy], fill=PAINT["gold"], width=2)
    pen.ellipse([cx - radius * 0.55, cy - radius * 0.55,
                 cx + radius * 0.55, cy + radius * 0.55],
                outline=PAINT["gold"], width=2)
    pen.arc([cx - radius, cy - radius * 0.45, cx + radius, cy + radius * 0.45],
            0, 360, fill=PAINT["ember"], width=2)


LEAD_STORY = {
    "kicker": "1 · CONFLICT  ·  KYIV & POLAND",
    "head": "RUSSIA'S MASS STRIKE ON UKRAINE — MISSILES LAND IN POLAND",
    "body": ("400+ drones and 110 missiles overnight; at least 8 killed in "
             "Kyiv. Two missiles and a drone come down on Polish soil — "
             "Warsaw calls it a deliberate provocation."),
}

STORIES = [
    {
        "kicker": "2 · MARKETS  ·  NEW YORK",
        "place": "WALL STREET",
        "head": "AI SELL-OFF DRAGS S&P INTO CORRECTION",
        "body": "Wall Street falls 3.7% as AI and chip shares plunge; Nasdaq down 5.3%.",
        "art": banner_market,
    },
    {
        "kicker": "3 · JUSTICE  ·  THE HAGUE",
        "place": "THE HAGUE",
        "head": "MYANMAR GUILTY OF GENOCIDE, COURT RULES",
        "body": "The ICJ finds Myanmar responsible for genocide of the Rohingya.",
        "art": banner_justice,
    },
    {
        "kicker": "4 · HEALTH  ·  LONDON",
        "place": "CLINICAL TRIAL",
        "head": "CANCER PILL WIPES OUT TUMOURS IN 1 OF 12",
        "body": ("Trial pill daraxonrasib makes pancreatic tumours vanish "
                 "on scans in 1 of 12 patients."),
        "art": banner_clinic,
    },
    {
        "kicker": "5 · POLITICS  ·  BRUSSELS",
        "place": "BRUSSELS",
        "head": "UK AND EU SIGN LANDMARK POST-BREXIT DEAL",
        "body": ("Three deals on food, carbon markets and youth mobility — "
                 "the biggest step since Brexit."),
        "art": banner_deal,
    },
]

ALSO_ITEMS = [
    "FBI crime database hacked",
    "Gen Z protests in 25 EU states",
    "6.9 quake in Peruvian Andes",
    "Indonesia forest fires",
    "Basra plant fire kills 4",
    "Palisades arsonist convicted",
    "Bayer pays $7.25bn over Roundup",
    "GTA 6: $4.9bn on day one",
    "Crypto: $2bn+ liquidated, Bitcoin ~$62K",
    "NASA halts Perseverance",
]


def masthead_draw(pen):
    pen.rectangle([0, 0, 1024, 92], fill=PAINT["navy"])
    compass_rose(pen, 52, 46, 28)
    title = "THE WORLD IN ONE DAY"
    tw = pen.textlength(title, font=FONTSET["title"])
    pen.text(((1024 - tw) / 2, 8), title, font=FONTSET["title"],
             fill=PAINT["white"])
    day = "SATURDAY 21 NOVEMBER 2026"
    dw = pen.textlength(day, font=FONTSET["dateline"])
    pen.text(((1024 - dw) / 2, 58), day, font=FONTSET["dateline"],
             fill=PAINT["gold"])
    tag = "make.fun"
    cw = pen.textlength(tag, font=FONTSET["badge"])
    pen.rounded_rectangle([1024 - cw - 36, 32, 1024 - 16, 64], radius=16,
                          fill=PAINT["gold"])
    pen.text((1024 - cw - 26, 38), tag, font=FONTSET["badge"], fill=PAINT["navy"])


def card_draw(flow, pen, x, y, w, h, item):
    pen.rectangle([x, y, x + w, y + h], fill=PAINT["white"],
                  outline=PAINT["navy"], width=2)
    item["art"](pen, x + 2, y + 2, x + w - 2, y + 60)
    pen.text((x + 16, y + 68), item["kicker"], font=FONTSET["kicker"],
             fill=PAINT["red"])
    head = flow.wrap_lines(item["head"], FONTSET["card_title"], w - 32)[:2]
    after = flow.stack_lines(x + 16, y + 94, head, FONTSET["card_title"],
                             PAINT["ink"], 27)
    body = flow.wrap_lines(item["body"], FONTSET["card_text"], w - 32)[:2]
    flow.stack_lines(x + 16, after + 6, body, FONTSET["card_text"],
                     PAINT["ink"], 20)
    pen.text((x + 16, y + h - 24), item["place"], font=FONTSET["place"],
             fill=PAINT["grey"])


def render_page():
    img = Image.new("RGB", PAGE, PAINT["paper"])
    pen = ImageDraw.Draw(img)
    flow = TextFlow(pen)

    masthead_draw(pen)
    pen.rectangle([0, 92, 1024, 96], fill=PAINT["gold"])

    pen.text((16, 108), LEAD_STORY["kicker"], font=FONTSET["kicker"],
             fill=PAINT["red"])
    head = flow.wrap_lines(LEAD_STORY["head"], FONTSET["headline"], 560)
    end = flow.stack_lines(16, 132, head, FONTSET["headline"], PAINT["ink"], 42)
    body = flow.wrap_lines(LEAD_STORY["body"], FONTSET["standfirst"], 560)
    flow.stack_lines(16, end + 8, body, FONTSET["standfirst"], PAINT["ink"], 25)

    pen.rectangle([608, 112, 1008, 352], outline=PAINT["navy"], width=2)
    skyline_night(pen, 610, 114, 1006, 350)

    spots = [(16, 364), (520, 364), (16, 596), (520, 596)]
    for item, (px, py) in zip(STORIES, spots):
        card_draw(flow, pen, px, py, 488, 220, item)

    pen.rectangle([16, 828, 1008, 892], fill=PAINT["teal"])
    globe_climate(pen, 56, 860, 24)
    pen.text((96, 838), "6 · CLIMATE  ·  ANTALYA — NEARLY 200 NATIONS",
             font=FONTSET["kicker"], fill=PAINT["ember"])
    pen.text((96, 860), "COP31 TALKS OVERRUN — NO FOSSIL-FUEL DEAL",
             font=FONTSET["strip_title"], fill=PAINT["white"])

    pen.rectangle([0, 904, 1024, 1024], fill=PAINT["deep"])
    label = "ALSO TODAY — 10 MORE"
    lw = pen.textlength(label, font=FONTSET["ticker_title"])
    pen.rounded_rectangle([16, 914, 16 + lw + 28, 944], radius=14,
                          fill=PAINT["gold"])
    pen.text((30, 919), label, font=FONTSET["ticker_title"], fill=PAINT["navy"])
    lines = flow.ticker_pack(ALSO_ITEMS, FONTSET["ticker"], 992, limit=3)
    y = 952
    for line in lines:
        pen.text((16, y), line, font=FONTSET["ticker"], fill=PAINT["white"])
        y += 21

    folder = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(folder, "entry.png")
    img.save(target, "PNG")
    print("wrote", target, img.size, os.path.getsize(target), "bytes")


if __name__ == "__main__":
    render_page()
