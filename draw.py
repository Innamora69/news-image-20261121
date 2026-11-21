#!/usr/bin/env python3
"""Render the front page for news-image-20261121.

Saturday 21 November 2026, drawn as a newspaper front page: a masthead,
a lead story on Russia's mass strike on Ukraine (missiles landing in
Poland), four story cards (AI sell-off, ICJ genocide ruling, cancer
trial pill, UK-EU deal) and an "also today" strip. Pillow only, no
network access, no randomness — rerunning draws identical bytes.

Usage: python3 draw.py  (writes entry.png beside this file)
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)

PALETTE = {
    "paper": (247, 243, 232),
    "ink": (24, 24, 24),
    "navy": (20, 38, 74),
    "navy_deep": (12, 26, 52),
    "red": (192, 57, 43),
    "gold": (217, 164, 65),
    "teal": (15, 118, 110),
    "grey": (110, 110, 110),
    "white": (255, 255, 255),
    "card": (255, 255, 255),
    "mist": (228, 235, 242),
    "steel": (82, 100, 130),
    "orange": (255, 150, 40),
    "amber": (255, 205, 90),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

_SPECS = [
    ("masthead", "DejaVuSans-Bold.ttf", 48),
    ("date", "DejaVuSans-Bold.ttf", 23),
    ("chip", "DejaVuSans-Bold.ttf", 18),
    ("kicker", "DejaVuSans-Bold.ttf", 20),
    ("lead_head", "DejaVuSans-Bold.ttf", 38),
    ("lead_body", "DejaVuSans.ttf", 21),
    ("card_head", "DejaVuSans-Bold.ttf", 24),
    ("card_body", "DejaVuSans.ttf", 18),
    ("tag", "DejaVuSans-Bold.ttf", 16),
    ("tick_head", "DejaVuSans-Bold.ttf", 22),
    ("tick", "DejaVuSans.ttf", 18),
    ("stat", "DejaVuSans-Bold.ttf", 17),
]

FONTS = {
    name: ImageFont.truetype(os.path.join(FONT_DIR, fname), size)
    for name, fname, size in _SPECS
}


def star_points(cx, cy, outer, inner, count=8):
    """Vertices of a star polygon, alternating outer/inner radius."""
    pts = []
    for i in range(count * 2):
        r = outer if i % 2 == 0 else inner
        a = -math.pi / 2 + i * math.pi / count
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


class Flow:
    """Greedy word wrap, stacked text, and ticker packing on one canvas."""

    def __init__(self, draw):
        self.d = draw

    def wrap(self, text, font, width):
        out = []
        for chunk in text.split("\n"):
            words = chunk.split()
            if not words:
                out.append("")
                continue
            line = words[0]
            for w in words[1:]:
                cand = line + " " + w
                if self.d.textlength(cand, font=font) <= width:
                    line = cand
                else:
                    out.append(line)
                    line = w
            out.append(line)
        return out

    def block(self, x, y, lines, font, fill, leading):
        for ln in lines:
            self.d.text((x, y), ln, font=font, fill=fill)
            y += leading
        return y

    def pack(self, items, font, width, sep="  ◆  ", limit=2):
        """Greedily fill up to `limit` lines with ticker items; drop the rest."""
        lines, cur = [], ""
        for item in items:
            nxt = item if not cur else cur + sep + item
            if self.d.textlength(nxt, font=font) <= width:
                cur = nxt
            else:
                lines.append(cur)
                cur = item
                if len(lines) == limit:
                    return lines
        if cur and len(lines) < limit:
            lines.append(cur)
        return lines


def compass(draw, cx, cy, r):
    """Eight-point compass rose for the masthead."""
    draw.polygon(star_points(cx, cy, r, r * 0.38, 8), fill=PALETTE["gold"])
    draw.ellipse(
        [cx - r * 0.32, cy - r * 0.32, cx + r * 0.32, cy + r * 0.32],
        fill=PALETTE["navy"],
    )
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=PALETTE["gold"])


def skyline(draw, x0, y0, x1, y1):
    """Night skyline under missile streaks and two explosion bursts."""
    w, h = x1 - x0, y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=PALETTE["navy_deep"])
    for sx, sy in [(0.08, 0.10), (0.22, 0.06), (0.38, 0.14), (0.55, 0.08),
                   (0.70, 0.16), (0.86, 0.07), (0.94, 0.20), (0.47, 0.05)]:
        draw.ellipse(
            [x0 + sx * w - 2, y0 + sy * h - 2, x0 + sx * w + 2, y0 + sy * h + 2],
            fill=PALETTE["white"],
        )
    towers = [(0.03, 0.15, 0.52), (0.21, 0.13, 0.68), (0.37, 0.16, 0.46),
              (0.56, 0.13, 0.62), (0.72, 0.15, 0.50), (0.88, 0.11, 0.58)]
    ground = y1 - 34
    for rx, rw, rh in towers:
        tx, tw, th = x0 + rx * w, rw * w, rh * h
        draw.rectangle([tx, ground - th, tx + tw, ground], fill=PALETTE["steel"])
        rows = int(th // 26)
        cols = int(tw // 20)
        for ri in range(rows):
            for ci in range(cols):
                if (ri + ci) % 3 == 0:
                    continue
                wx = tx + 7 + ci * 20
                wy = ground - th + 10 + ri * 26
                draw.rectangle([wx, wy, wx + 8, wy + 10], fill=PALETTE["gold"])
    draw.rectangle([x0, ground, x1, y1], fill=(40, 44, 58))
    draw.line(
        [x1 - 8, y0 + 12, x0 + 0.58 * w, y0 + 0.42 * h],
        fill=PALETTE["red"], width=5,
    )
    draw.ellipse([x1 - 24, y0 + 2, x1 - 4, y0 + 22], fill=PALETTE["red"])
    draw.line(
        [x1 - 70, y0 + 52, x0 + 0.66 * w, y0 + 0.50 * h],
        fill=PALETTE["orange"], width=4,
    )
    for sx, sy, sr in [(0.86, 0.16, 8), (0.82, 0.22, 6), (0.78, 0.27, 4)]:
        draw.ellipse(
            [x0 + sx * w - sr, y0 + sy * h - sr, x0 + sx * w + sr, y0 + sy * h + sr],
            fill=(205, 205, 205),
        )
    for bx, by in [(x0 + 0.28 * w, ground - 0.68 * h),
                   (x0 + 0.62 * w, ground - 0.62 * h)]:
        draw.polygon(star_points(bx, by, 26, 10, 8), fill=PALETTE["orange"])
        draw.polygon(star_points(bx, by, 13, 5, 8), fill=PALETTE["amber"])
    draw.text(
        (x0 + 12, y1 - 28), "400+ DRONES  ·  110 MISSILES",
        font=FONTS["stat"], fill=PALETTE["white"],
    )


def chart_strip(draw, x0, y0, x1, y1):
    """Falling market line on a dark strip, with a red drop marker."""
    draw.rectangle([x0, y0, x1, y1], fill=PALETTE["navy_deep"])
    fracs = [(0.06, 0.30), (0.20, 0.38), (0.34, 0.34), (0.48, 0.55),
             (0.62, 0.52), (0.76, 0.72), (0.90, 0.68)]
    coords = [(x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)) for fx, fy in fracs]
    draw.line(coords, fill=PALETTE["white"], width=3, joint="curve")
    for px, py in coords:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=PALETTE["gold"])
    lx, ly = coords[-1]
    draw.polygon(
        [(lx, ly + 14), (lx - 9, ly - 2), (lx + 9, ly - 2)],
        fill=PALETTE["red"],
    )
    draw.text((x1 - 92, y0 + 8), "-3.7%", font=FONTS["card_head"],
              fill=PALETTE["red"])


def scales_strip(draw, x0, y0, x1, y1):
    """Scales of justice stretched across a pale strip."""
    draw.rectangle([x0, y0, x1, y1], fill=PALETTE["mist"])
    cx = (x0 + x1) // 2
    draw.rectangle([cx - 3, y0 + 8, cx + 3, y1 - 12], fill=PALETTE["navy"])
    draw.line([cx - 120, y0 + 16, cx + 120, y0 + 16], fill=PALETTE["navy"], width=4)
    draw.ellipse([cx - 7, y0 + 6, cx + 7, y0 + 20], fill=PALETTE["gold"])
    draw.rectangle([cx - 34, y1 - 12, cx + 34, y1 - 8], fill=PALETTE["navy"])
    for side in (-1, 1):
        px = cx + side * 120
        draw.line([px, y0 + 16, px - 22, y0 + 48], fill=PALETTE["navy"], width=2)
        draw.line([px, y0 + 16, px + 22, y0 + 48], fill=PALETTE["navy"], width=2)
        draw.polygon(
            [(px - 26, y0 + 48), (px + 26, y0 + 48), (px, y1 - 14)],
            fill=PALETTE["gold"],
        )


def health_strip(draw, x0, y0, x1, y1):
    """Teal strip: white medical cross in a round tile, '1 IN 12' beside it."""
    draw.rectangle([x0, y0, x1, y1], fill=PALETTE["teal"])
    cx, cy = x0 + 60, (y0 + y1) // 2
    draw.rounded_rectangle(
        [cx - 26, cy - 26, cx + 26, cy + 26], radius=10, fill=PALETTE["white"],
    )
    draw.rectangle([cx - 6, cy - 18, cx + 6, cy + 18], fill=PALETTE["teal"])
    draw.rectangle([cx - 18, cy - 6, cx + 18, cy + 6], fill=PALETTE["teal"])
    draw.text((x0 + 104, cy - 16), "1 IN 12", font=FONTS["card_head"],
              fill=PALETTE["white"])
    draw.text((x0 + 104, cy + 12), "TUMOURS UNDETECTED", font=FONTS["tag"],
              fill=(210, 235, 230))


def deal_strip(draw, x0, y0, x1, y1):
    """Navy strip: ring of EU stars, a UK–EU label, and a Union Jack block."""
    draw.rectangle([x0, y0, x1, y1], fill=PALETTE["navy"])
    cx, cy = x0 + 70, (y0 + y1) // 2
    for k in range(12):
        a = -math.pi / 2 + k * 2 * math.pi / 12
        sx, sy = cx + 30 * math.cos(a), cy + 30 * math.sin(a)
        draw.polygon(star_points(sx, sy, 6, 2.5, 5), fill=PALETTE["gold"])
    draw.text((x0 + 150, cy - 14), "UK – EU", font=FONTS["card_head"],
              fill=PALETTE["gold"])
    jx0, jy0 = x1 - 150, y0 + 12
    jx1, jy1 = x1 - 20, y1 - 12
    draw.rectangle([jx0, jy0, jx1, jy1], fill=(198, 40, 52))
    draw.line([jx0, jy0, jx1, jy1], fill=PALETTE["white"], width=6)
    draw.line([jx1, jy0, jx0, jy1], fill=PALETTE["white"], width=6)
    mx, my = (jx0 + jx1) // 2, (jy0 + jy1) // 2
    draw.line([mx, jy0, mx, jy1], fill=PALETTE["white"], width=8)
    draw.line([jx0, my, jx1, my], fill=PALETTE["white"], width=8)


LEAD = {
    "kicker": "CONFLICT  ·  KYIV & POLAND",
    "head": "RUSSIA'S MASS STRIKE ON UKRAINE — MISSILES LAND IN POLAND",
    "body": ("400+ drones and 110 missiles overnight; at least 8 killed in "
             "Kyiv. Two missiles and a drone come down on Polish soil — "
             "Warsaw calls it a deliberate provocation."),
}

PANELS = [
    {
        "kicker": "MARKETS  ·  NEW YORK",
        "place": "WALL STREET",
        "head": "AI SELL-OFF DRAGS S&P INTO CORRECTION",
        "body": "Wall Street drops 3.7% as AI and chip shares plunge.",
        "banner": chart_strip,
    },
    {
        "kicker": "JUSTICE  ·  THE HAGUE",
        "place": "THE HAGUE",
        "head": "MYANMAR GUILTY OF GENOCIDE, COURT RULES",
        "body": "The ICJ finds Myanmar responsible for genocide of the Rohingya.",
        "banner": scales_strip,
    },
    {
        "kicker": "HEALTH  ·  LONDON",
        "place": "CLINICAL TRIAL",
        "head": "CANCER PILL WIPES OUT TUMOURS IN 1 OF 12",
        "body": ("Trial pill daraxonrasib makes pancreatic tumours vanish "
                 "on scans in 1 of 12 patients."),
        "banner": health_strip,
    },
    {
        "kicker": "POLITICS  ·  BRUSSELS",
        "place": "BRUSSELS",
        "head": "UK AND EU SIGN LANDMARK POST-BREXIT DEAL",
        "body": ("Three deals on food, carbon markets and youth mobility — "
                 "the biggest step since Brexit."),
        "banner": deal_strip,
    },
]


def masthead(draw):
    draw.rectangle([0, 0, 1024, 96], fill=PALETTE["navy"])
    compass(draw, 54, 48, 30)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=FONTS["masthead"])
    draw.text(((1024 - tw) / 2, 10), title, font=FONTS["masthead"],
              fill=PALETTE["white"])
    date = "SATURDAY 21 NOVEMBER 2026"
    dw = draw.textlength(date, font=FONTS["date"])
    draw.text(((1024 - dw) / 2, 62), date, font=FONTS["date"],
              fill=PALETTE["gold"])
    chip = "make.fun"
    cw = draw.textlength(chip, font=FONTS["chip"])
    draw.rounded_rectangle(
        [1024 - cw - 36, 34, 1024 - 16, 66], radius=16, fill=PALETTE["gold"],
    )
    draw.text((1024 - cw - 26, 40), chip, font=FONTS["chip"],
              fill=PALETTE["navy"])


def card(flow, draw, x, y, w, h, spec):
    """One story card: banner pictogram on top, kicker, headline, body."""
    draw.rectangle([x, y, x + w, y + h], fill=PALETTE["card"],
                   outline=PALETTE["navy"], width=2)
    spec["banner"](draw, x + 2, y + 2, x + w - 2, y + 74)
    draw.text((x + 16, y + 86), spec["kicker"], font=FONTS["kicker"],
              fill=PALETTE["red"])
    head = flow.wrap(spec["head"], FONTS["card_head"], w - 32)[:2]
    ycur = flow.block(x + 16, y + 112, head, FONTS["card_head"],
                      PALETTE["ink"], 27)
    body = flow.wrap(spec["body"], FONTS["card_body"], w - 32)[:2]
    flow.block(x + 16, ycur + 6, body, FONTS["card_body"], PALETTE["ink"], 21)
    draw.text((x + 16, y + h - 26), spec["place"], font=FONTS["tag"],
              fill=PALETTE["grey"])


def ticker(flow, draw):
    draw.rectangle([0, 908, 1024, 1024], fill=PALETTE["navy_deep"])
    label = "ALSO TODAY"
    lw = draw.textlength(label, font=FONTS["tick_head"])
    draw.rounded_rectangle([16, 920, 16 + lw + 28, 950], radius=14,
                           fill=PALETTE["gold"])
    draw.text((30, 925), label, font=FONTS["tick_head"], fill=PALETTE["navy"])
    items = [
        "FBI criminal database hacked",
        "Gen Z protests spread to 25 EU states",
        "6.9 quake shakes Peruvian Andes",
        "Indonesia hit by huge forest fires",
        "Basra power-plant fire kills 4",
        "Palisades fire arsonist convicted",
    ]
    lines = flow.pack(items, FONTS["tick"], 992, limit=2)
    y = 956
    for ln in lines:
        draw.text((16, y), ln, font=FONTS["tick"], fill=PALETTE["white"])
        y += 23


def main():
    img = Image.new("RGB", CANVAS, PALETTE["paper"])
    draw = ImageDraw.Draw(img)
    flow = Flow(draw)

    masthead(draw)
    draw.rectangle([0, 96, 1024, 100], fill=PALETTE["gold"])

    # Lead story: words on the left, picture on the right.
    draw.text((16, 118), LEAD["kicker"], font=FONTS["kicker"],
              fill=PALETTE["red"])
    head = flow.wrap(LEAD["head"], FONTS["lead_head"], 576)
    end = flow.block(16, 146, head, FONTS["lead_head"], PALETTE["ink"], 44)
    body = flow.wrap(LEAD["body"], FONTS["lead_body"], 576)
    flow.block(16, end + 10, body, FONTS["lead_body"], PALETTE["ink"], 26)

    draw.rectangle([608, 112, 1008, 368], outline=PALETTE["navy"], width=2)
    skyline(draw, 610, 114, 1006, 366)

    spots = [(16, 384), (520, 384), (16, 644), (520, 644)]
    for spec, (px, py) in zip(PANELS, spots):
        card(flow, draw, px, py, 488, 248, spec)

    ticker(flow, draw)

    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "entry.png")
    img.save(target, "PNG")
    print("wrote", target, img.size, os.path.getsize(target), "bytes")


if __name__ == "__main__":
    main()
