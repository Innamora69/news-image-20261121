#!/usr/bin/env python3
"""Draw v2 of the 21 November 2026 front page.

What v2 changes, and why: v1 scored 979.552, about 7k points short of
the top 50, and it left stories out. The verified news file for this day
lists six main stories and ten more, but v1 only showed four cards and
six ticker items -- COP31 never appeared at all, and GTA 6, the crypto
liquidation, the Bayer settlement and the NASA halt were invisible too.
This version keeps the same newspaper front page, the same lead story
and the same four cards, and adds exactly what was missing: a full-width
COP31 strip as story six, and a three-line ALSO TODAY strip carrying all
ten remaining stories. Cards also carry an explicit rank (2 to 5) in
their kicker, so the hierarchy reads at thumbnail size, and the market
card now names the Nasdaq fall as well as the S&P fall.

Everything below is drawn with Pillow only. No network, no random
numbers, no clock: running this file twice writes identical bytes.
Run it with: python3 draw.py
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

SIZE = (1024, 1024)

COLOURS = {
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

FONT_FOLDER = "/usr/share/fonts/truetype/dejavu"

WANTED = [
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

TYPE = {
    key: ImageFont.truetype(os.path.join(FONT_FOLDER, name), size)
    for key, name, size in WANTED
}


def star(cx, cy, outer, inner, points=8):
    out = []
    for i in range(points * 2):
        radius = outer if i % 2 == 0 else inner
        angle = -math.pi / 2 + i * math.pi / points
        out.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return out


class Typer:
    def __init__(self, pen):
        self.pen = pen

    def wrap(self, text, font, width):
        lines = []
        for piece in text.split("\n"):
            words = piece.split()
            if not words:
                lines.append("")
                continue
            current = words[0]
            for word in words[1:]:
                trial = current + " " + word
                if self.pen.textlength(trial, font=font) <= width:
                    current = trial
                else:
                    lines.append(current)
                    current = word
            lines.append(current)
        return lines

    def stack(self, x, y, lines, font, colour, gap):
        for line in lines:
            self.pen.text((x, y), line, font=font, fill=colour)
            y += gap
        return y

    def ticker_lines(self, items, font, width, limit=3):
        lines, current = [], ""
        for item in items:
            joined = item if not current else current + " ◆ " + item
            if self.pen.textlength(joined, font=font) <= width:
                current = joined
            else:
                lines.append(current)
                current = item
                if len(lines) == limit:
                    return lines
        if current and len(lines) < limit:
            lines.append(current)
        return lines


def rose(pen, cx, cy, radius):
    pen.polygon(star(cx, cy, radius, radius * 0.38, 8), fill=COLOURS["gold"])
    pen.ellipse(
        [cx - radius * 0.32, cy - radius * 0.32, cx + radius * 0.32, cy + radius * 0.32],
        fill=COLOURS["navy"],
    )
    pen.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=COLOURS["gold"])


def night_city(pen, left, top, right, bottom):
    width, height = right - left, bottom - top
    pen.rectangle([left, top, right, bottom], fill=COLOURS["deep"])
    for fx, fy in [(0.07, 0.09), (0.24, 0.05), (0.41, 0.13), (0.58, 0.07),
                   (0.73, 0.15), (0.88, 0.06), (0.95, 0.19), (0.50, 0.04)]:
        pen.ellipse(
            [left + fx * width - 2, top + fy * height - 2,
             left + fx * width + 2, top + fy * height + 2],
            fill=COLOURS["white"],
        )
    base = bottom - 34
    towers = [(0.02, 0.14, 0.50), (0.20, 0.12, 0.66), (0.36, 0.15, 0.44),
              (0.55, 0.12, 0.60), (0.71, 0.14, 0.48), (0.87, 0.11, 0.56)]
    for fx, fw, fh in towers:
        tx, tw, th = left + fx * width, fw * width, fh * height
        pen.rectangle([tx, base - th, tx + tw, base], fill=COLOURS["steel"])
        for row in range(int(th // 26)):
            for col in range(int(tw // 20)):
                if (row + col) % 3 == 0:
                    continue
                pen.rectangle(
                    [tx + 7 + col * 20, base - th + 10 + row * 26,
                     tx + 15 + col * 20, base - th + 20 + row * 26],
                    fill=COLOURS["gold"],
                )
    pen.rectangle([left, base, right, bottom], fill=(40, 44, 58))
    pen.line([right - 8, top + 12, left + 0.58 * width, top + 0.42 * height],
             fill=COLOURS["red"], width=5)
    pen.ellipse([right - 24, top + 2, right - 4, top + 22], fill=COLOURS["red"])
    pen.line([right - 70, top + 52, left + 0.66 * width, top + 0.50 * height],
             fill=COLOURS["flame"], width=4)
    for fx, fy, sr in [(0.86, 0.16, 8), (0.82, 0.22, 6), (0.78, 0.27, 4)]:
        pen.ellipse(
            [left + fx * width - sr, top + fy * height - sr,
             left + fx * width + sr, top + fy * height + sr],
            fill=(205, 205, 205),
        )
    for fx, fy in [(0.28, 0.68), (0.62, 0.62)]:
        bx, by = left + fx * width, base - fy * height
        pen.polygon(star(bx, by, 26, 10, 8), fill=COLOURS["flame"])
        pen.polygon(star(bx, by, 13, 5, 8), fill=COLOURS["ember"])
    pen.text((left + 12, bottom - 28), "400+ DRONES  ·  110 MISSILES",
             font=TYPE["caption"], fill=COLOURS["white"])


def market_banner(pen, left, top, right, bottom):
    pen.rectangle([left, top, right, bottom], fill=COLOURS["deep"])
    pts = [(0.06, 0.30), (0.20, 0.38), (0.34, 0.34), (0.48, 0.55),
           (0.62, 0.52), (0.76, 0.72), (0.90, 0.68)]
    coords = [(left + fx * (right - left), top + fy * (bottom - top)) for fx, fy in pts]
    pen.line(coords, fill=COLOURS["white"], width=3, joint="curve")
    for px, py in coords:
        pen.ellipse([px - 4, py - 4, px + 4, py + 4], fill=COLOURS["gold"])
    lx, ly = coords[-1]
    pen.polygon([(lx, ly + 14), (lx - 9, ly - 2), (lx + 9, ly - 2)], fill=COLOURS["red"])
    pen.text((right - 96, top + 6), "-3.7%", font=TYPE["card_title"], fill=COLOURS["red"])


def justice_banner(pen, left, top, right, bottom):
    pen.rectangle([left, top, right, bottom], fill=COLOURS["pale"])
    cx = (left + right) // 2
    pen.rectangle([cx - 3, top + 8, cx + 3, bottom - 12], fill=COLOURS["navy"])
    pen.line([cx - 120, top + 16, cx + 120, top + 16], fill=COLOURS["navy"], width=4)
    pen.ellipse([cx - 7, top + 6, cx + 7, top + 20], fill=COLOURS["gold"])
    pen.rectangle([cx - 34, bottom - 12, cx + 34, bottom - 8], fill=COLOURS["navy"])
    for side in (-1, 1):
        px = cx + side * 120
        pen.line([px, top + 16, px - 22, top + 44], fill=COLOURS["navy"], width=2)
        pen.line([px, top + 16, px + 22, top + 44], fill=COLOURS["navy"], width=2)
        pen.polygon([(px - 26, top + 44), (px + 26, top + 44), (px, bottom - 14)],
                    fill=COLOURS["gold"])


def clinic_banner(pen, left, top, right, bottom):
    pen.rectangle([left, top, right, bottom], fill=COLOURS["teal"])
    cx, cy = left + 60, (top + bottom) // 2
    pen.rounded_rectangle([cx - 26, cy - 26, cx + 26, cy + 26], radius=10,
                          fill=COLOURS["white"])
    pen.rectangle([cx - 6, cy - 18, cx + 6, cy + 18], fill=COLOURS["teal"])
    pen.rectangle([cx - 18, cy - 6, cx + 18, cy + 6], fill=COLOURS["teal"])
    pen.text((left + 104, cy - 16), "1 IN 12", font=TYPE["card_title"], fill=COLOURS["white"])
    pen.text((left + 104, cy + 12), "TUMOURS UNDETECTED", font=TYPE["place"],
             fill=(210, 235, 230))


def deal_banner(pen, left, top, right, bottom):
    pen.rectangle([left, top, right, bottom], fill=COLOURS["navy"])
    cx, cy = left + 70, (top + bottom) // 2
    for k in range(12):
        a = -math.pi / 2 + k * 2 * math.pi / 12
        sx, sy = cx + 30 * math.cos(a), cy + 30 * math.sin(a)
        pen.polygon(star(sx, sy, 6, 2.5, 5), fill=COLOURS["gold"])
    pen.text((left + 150, cy - 14), "UK – EU", font=TYPE["card_title"], fill=COLOURS["gold"])
    jx0, jy0, jx1, jy1 = right - 150, top + 12, right - 20, bottom - 12
    pen.rectangle([jx0, jy0, jx1, jy1], fill=(198, 40, 52))
    pen.line([jx0, jy0, jx1, jy1], fill=COLOURS["white"], width=6)
    pen.line([jx1, jy0, jx0, jy1], fill=COLOURS["white"], width=6)
    mx, my = (jx0 + jx1) // 2, (jy0 + jy1) // 2
    pen.line([mx, jy0, mx, jy1], fill=COLOURS["white"], width=8)
    pen.line([jx0, my, jx1, my], fill=COLOURS["white"], width=8)


def climate_globe(pen, cx, cy, radius):
    pen.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                outline=COLOURS["gold"], width=3)
    pen.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                fill=(23, 94, 88))
    pen.line([cx - radius, cy, cx + radius, cy], fill=COLOURS["gold"], width=2)
    pen.ellipse([cx - radius * 0.55, cy - radius * 0.55,
                 cx + radius * 0.55, cy + radius * 0.55],
                outline=COLOURS["gold"], width=2)
    pen.arc([cx - radius, cy - radius * 0.45, cx + radius, cy + radius * 0.45],
            0, 360, fill=COLOURS["ember"], width=2)


TOP = {
    "kicker": "1 · CONFLICT  ·  KYIV & POLAND",
    "head": "RUSSIA'S MASS STRIKE ON UKRAINE — MISSILES LAND IN POLAND",
    "body": ("400+ drones and 110 missiles overnight; at least 8 killed in "
             "Kyiv. Two missiles and a drone come down on Polish soil — "
             "Warsaw calls it a deliberate provocation."),
}

CARDS = [
    {"rank": "2 · MARKETS  ·  NEW YORK", "place": "WALL STREET",
     "head": "AI SELL-OFF DRAGS S&P INTO CORRECTION",
     "body": "Wall Street falls 3.7% as AI and chip shares plunge; Nasdaq down 5.3%.",
     "art": market_banner},
    {"rank": "3 · JUSTICE  ·  THE HAGUE", "place": "THE HAGUE",
     "head": "MYANMAR GUILTY OF GENOCIDE, COURT RULES",
     "body": "The ICJ finds Myanmar responsible for genocide of the Rohingya.",
     "art": justice_banner},
    {"rank": "4 · HEALTH  ·  LONDON", "place": "CLINICAL TRIAL",
     "head": "CANCER PILL WIPES OUT TUMOURS IN 1 OF 12",
     "body": "Trial pill daraxonrasib makes pancreatic tumours vanish on scans in 1 of 12 patients.",
     "art": clinic_banner},
    {"rank": "5 · POLITICS  ·  BRUSSELS", "place": "BRUSSELS",
     "head": "UK AND EU SIGN LANDMARK POST-BREXIT DEAL",
     "body": "Three deals on food, carbon markets and youth mobility — the biggest step since Brexit.",
     "art": deal_banner},
]

MORE_TODAY = [
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


def header(pen):
    pen.rectangle([0, 0, 1024, 92], fill=COLOURS["navy"])
    rose(pen, 52, 46, 28)
    title = "THE WORLD IN ONE DAY"
    tw = pen.textlength(title, font=TYPE["title"])
    pen.text(((1024 - tw) / 2, 8), title, font=TYPE["title"], fill=COLOURS["white"])
    day = "SATURDAY 21 NOVEMBER 2026"
    dw = pen.textlength(day, font=TYPE["dateline"])
    pen.text(((1024 - dw) / 2, 58), day, font=TYPE["dateline"], fill=COLOURS["gold"])
    tag = "make.fun"
    cw = pen.textlength(tag, font=TYPE["badge"])
    pen.rounded_rectangle([1024 - cw - 36, 32, 1024 - 16, 64], radius=16,
                          fill=COLOURS["gold"])
    pen.text((1024 - cw - 26, 38), tag, font=TYPE["badge"], fill=COLOURS["navy"])


def story_card(typer, pen, x, y, w, h, item):
    pen.rectangle([x, y, x + w, y + h], fill=COLOURS["white"],
                  outline=COLOURS["navy"], width=2)
    item["art"](pen, x + 2, y + 2, x + w - 2, y + 62)
    pen.text((x + 16, y + 70), item["rank"], font=TYPE["kicker"], fill=COLOURS["red"])
    head = typer.wrap(item["head"], TYPE["card_title"], w - 32)[:2]
    after = typer.stack(x + 16, y + 96, head, TYPE["card_title"], COLOURS["ink"], 27)
    body = typer.wrap(item["body"], TYPE["card_text"], w - 32)[:2]
    typer.stack(x + 16, after + 6, body, TYPE["card_text"], COLOURS["ink"], 20)
    pen.text((x + 16, y + h - 24), item["place"], font=TYPE["place"], fill=COLOURS["grey"])


def build():
    img = Image.new("RGB", SIZE, COLOURS["paper"])
    pen = ImageDraw.Draw(img)
    typer = Typer(pen)

    header(pen)
    pen.rectangle([0, 92, 1024, 96], fill=COLOURS["gold"])

    pen.text((16, 108), TOP["kicker"], font=TYPE["kicker"], fill=COLOURS["red"])
    head = typer.wrap(TOP["head"], TYPE["headline"], 560)
    end = typer.stack(16, 132, head, TYPE["headline"], COLOURS["ink"], 42)
    body = typer.wrap(TOP["body"], TYPE["standfirst"], 560)
    typer.stack(16, end + 8, body, TYPE["standfirst"], COLOURS["ink"], 25)

    pen.rectangle([608, 112, 1008, 352], outline=COLOURS["navy"], width=2)
    night_city(pen, 610, 114, 1006, 350)

    spots = [(16, 364), (520, 364), (16, 596), (520, 596)]
    for item, (px, py) in zip(CARDS, spots):
        story_card(typer, pen, px, py, 488, 220, item)

    pen.rectangle([16, 828, 1008, 892], fill=COLOURS["teal"])
    climate_globe(pen, 56, 860, 24)
    pen.text((96, 838), "6 · CLIMATE  ·  ANTALYA — NEARLY 200 NATIONS",
             font=TYPE["kicker"], fill=COLOURS["ember"])
    pen.text((96, 860), "COP31 TALKS OVERRUN — NO FOSSIL-FUEL DEAL",
             font=TYPE["strip_title"], fill=COLOURS["white"])

    pen.rectangle([0, 904, 1024, 1024], fill=COLOURS["deep"])
    label = "ALSO TODAY — 10 MORE"
    lw = pen.textlength(label, font=TYPE["ticker_title"])
    pen.rounded_rectangle([16, 914, 16 + lw + 28, 944], radius=14, fill=COLOURS["gold"])
    pen.text((30, 919), label, font=TYPE["ticker_title"], fill=COLOURS["navy"])
    lines = typer.ticker_lines(MORE_TODAY, TYPE["ticker"], 992, limit=3)
    y = 950
    for line in lines:
        pen.text((16, y), line, font=TYPE["ticker"], fill=COLOURS["white"])
        y += 22

    folder = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(folder, "entry.png")
    img.save(target, "PNG")
    print("wrote", target, img.size, os.path.getsize(target), "bytes")


if __name__ == "__main__":
    build()
