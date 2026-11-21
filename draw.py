#!/usr/bin/env python3
"""Draw entry.png for news-image-20261121.

One image summing up the world's news of Saturday 21 November 2026:
a newspaper front page ("THE WORLD IN ONE DAY") with a lead story on
Russia's mass drone-and-missile strike on Ukraine — missiles landing in
Poland — plus four panels (AI sell-off, ICJ genocide ruling, cancer pill,
UK-EU deal) and an "also today" ticker. Pure Pillow, flat vector
pictograms, no network, no randomness: same run, same bytes.

Run: python3 draw.py   (writes entry.png next to this file)
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (26, 26, 26)
NAVY = (20, 38, 74)
NAVY_DARK = (13, 27, 54)
RED = (192, 57, 43)
GOLD = (217, 164, 65)
TEAL = (15, 118, 110)
GREY = (96, 96, 96)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
SAND = (232, 214, 170)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = load_font("DejaVuSans-Bold.ttf", 54)
F_DATE = load_font("DejaVuSans-Bold.ttf", 28)
F_KICK = load_font("DejaVuSans-Bold.ttf", 21)
F_HEAD = load_font("DejaVuSans-Bold.ttf", 38)
F_PANEL_HEAD = load_font("DejaVuSans-Bold.ttf", 25)
F_BODY = load_font("DejaVuSans.ttf", 22)
F_PANEL_BODY = load_font("DejaVuSans.ttf", 19)
F_TAG = load_font("DejaVuSans-Bold.ttf", 17)
F_TICK_LABEL = load_font("DejaVuSans-Bold.ttf", 24)
F_TICK = load_font("DejaVuSans.ttf", 19)
F_BIG_NUM = load_font("DejaVuSans-Bold.ttf", 46)


def wrap(draw, text, font, max_width):
    """Split text into lines that fit max_width pixels."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_lines(draw, x, y, lines, font, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- pictograms

def globe(draw, cx, cy, r, fill, line):
    """A simple globe: circle with meridians and a latitude line."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=line, width=3)
    draw.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r], outline=line, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=line, width=2)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340, fill=line, width=2)


def strike_pictogram(draw, x0, y0, x1, y1):
    """Night city skyline under missile streaks and explosion bursts."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY_DARK)
    # stars
    for sx, sy in [(x0 + 30, y0 + 26), (x0 + 90, y0 + 52), (x0 + 160, y0 + 20),
                   (x0 + 230, y0 + 58), (x0 + 300, y0 + 30), (x0 + 340, y0 + 70)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=WHITE)
    # city towers
    towers = [(x0 + 8, 150), (x0 + 70, 110), (x0 + 140, 170), (x0 + 210, 120),
              (x0 + 280, 160)]
    for tx, th in towers:
        draw.rectangle([tx, y1 - th, tx + 56, y1 - 8], fill=(52, 68, 96))
        for wy in range(y1 - th + 14, y1 - 16, 22):
            draw.rectangle([tx + 10, wy, tx + 20, wy + 8], fill=GOLD)
            draw.rectangle([tx + 34, wy, tx + 44, wy + 8], fill=GOLD)
    draw.rectangle([x0, y1 - 8, x1, y1], fill=GREY)
    # missile streaks top-right with smoke puffs
    draw.line([x1 - 10, y0 + 10, x0 + 210, y0 + 110], fill=RED, width=5)
    draw.ellipse([x1 - 26, y0 + 4, x1 - 6, y0 + 24], fill=RED)
    draw.line([x1 - 60, y0 + 44, x0 + 250, y0 + 130], fill=(255, 120, 60), width=4)
    for sx, sy, sr in [(x1 - 40, y0 + 30, 9), (x1 - 58, y0 + 46, 7),
                       (x1 - 74, y0 + 60, 5)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(200, 200, 200))
    # explosion bursts over two towers
    for bx, by in [(x0 + 98, y1 - 130), (x0 + 238, y1 - 140)]:
        for dx, dy, ln in [(-26, 0, 26), (26, 0, 26), (0, -26, 26),
                           (0, 26, 26), (-18, -18, 20), (18, -18, 20),
                           (-18, 18, 20), (18, 18, 20)]:
            draw.line([bx, by, bx + dx, by + dy], fill=(255, 170, 40), width=5)
        draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(255, 210, 90))
    draw.text((x0 + 14, y1 - 34), "400+ DRONES  ·  110 MISSILES",
              font=F_TAG, fill=WHITE)


def chart_pictogram(draw, x0, y0, x1, y1):
    """Falling candlestick chart with a red trend arrow."""
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=NAVY, width=2)
    base = y1 - 34
    top = y0 + 30
    # axes
    draw.line([x0 + 28, y0 + 16, x0 + 28, base], fill=GREY, width=2)
    draw.line([x0 + 28, base, x1 - 16, base], fill=GREY, width=2)
    # five candles, falling from left to right
    closes = [0.18, 0.34, 0.52, 0.68, 0.84]
    slot = (x1 - x0 - 70) // 5
    for i, frac in enumerate(closes):
        cx = x0 + 48 + i * slot + slot // 2
        body_h = 16 + i * 3
        body_top = top + int(frac * (base - top - 40))
        colour = TEAL if i == 0 else RED
        draw.line([cx, body_top - 10, cx, body_top + body_h + 8], fill=colour, width=3)
        draw.rectangle(
            [cx - 11, body_top, cx + 11, body_top + body_h], fill=colour
        )
    # red arrow down-right
    draw.line(
        [x0 + 40, top + 6, x1 - 30, base - 14], fill=RED, width=5
    )
    draw.polygon(
        [(x1 - 30, base - 14), (x1 - 52, base - 20), (x1 - 40, base - 2)],
        fill=RED,
    )
    draw.text((x0 + 14, y1 - 30), "S&P 500  -3.7%", font=F_TAG, fill=RED)


def scales_pictogram(draw, x0, y0, x1, y1):
    """Scales of justice on a navy card."""
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    draw.rectangle([x0, y0, x1, y1], fill=(226, 234, 242))
    # post and beam
    draw.rectangle([cx - 4, cy - 66, cx + 4, cy + 70], fill=NAVY)
    draw.line([cx - 58, cy - 58, cx + 58, cy - 58], fill=NAVY, width=5)
    draw.ellipse([cx - 8, cy - 82, cx + 8, cy - 66], fill=GOLD)
    draw.rectangle([cx - 46, cy + 66, cx + 46, cy + 74], fill=NAVY)
    # pans
    for side in (-1, 1):
        px = cx + side * 58
        draw.line([px, cy - 58, px - 20, cy - 14], fill=NAVY, width=3)
        draw.line([px, cy - 58, px + 20, cy - 14], fill=NAVY, width=3)
        draw.polygon([(px - 24, cy - 14), (px + 24, cy - 14), (px, cy + 16)],
                     fill=GOLD)


def health_pictogram(draw, x0, y0, x1, y1):
    """A medical cross in a circle with a '1 IN 12' badge."""
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2 - 16
    draw.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], fill=TEAL)
    draw.rectangle([cx - 12, cy - 34, cx + 12, cy + 34], fill=WHITE)
    draw.rectangle([cx - 34, cy - 12, cx + 34, cy + 12], fill=WHITE)
    draw.text((cx - 34, cy + 58), "1 IN 12", font=F_TAG, fill=TEAL)


def deal_pictogram(draw, x0, y0, x1, y1):
    """EU circle of stars beside a Union Jack strip: the UK-EU deal."""
    cx = (x0 + x1) // 2 - 8
    cy = (y0 + y1) // 2 - 8
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    # circle of twelve gold stars
    import math
    for k in range(12):
        ang = math.pi * 2 * k / 12 - math.pi / 2
        sx = cx + int(44 * math.cos(ang))
        sy = cy + int(44 * math.sin(ang))
        draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=GOLD)
    # small Union Jack block
    jx0, jy0, jx1, jy1 = cx - 58, cy + 52, cx + 42, cy + 88
    draw.rectangle([jx0, jy0, jx1, jy1], fill=(200, 40, 50))
    draw.line([jx0, jy0, jx1, jy1], fill=WHITE, width=5)
    draw.line([jx1, jy0, jx0, jy1], fill=WHITE, width=5)
    draw.line([cx - 8, jy0, cx - 8, jy1], fill=WHITE, width=5)
    draw.line([jx0, cy + 70, jx1, cy + 70], fill=WHITE, width=5)


# ------------------------------------------------------------------- layout

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header band
    d.rectangle([0, 0, W, 104], fill=NAVY)
    globe(d, 58, 52, 32, NAVY_DARK, GOLD)
    d.text((106, 12), "THE WORLD IN ONE DAY", font=F_TITLE, fill=WHITE)
    d.text((106, 68), "SATURDAY 21 NOVEMBER 2026", font=F_DATE, fill=GOLD)
    d.text((788, 70), "make.fun", font=F_KICK, fill=(180, 195, 220))

    # ---- lead story: Russia's mass strike; missiles land in Poland
    d.rectangle([8, 112, 400, 384], fill=CARD, outline=NAVY, width=2)
    strike_pictogram(d, 20, 124, 388, 372)
    d.text((424, 118), "CONFLICT  ·  KYIV & POLAND", font=F_KICK, fill=RED)
    head_lines = wrap(
        d,
        "RUSSIA'S MASS STRIKE ON UKRAINE \u2014 MISSILES LAND IN POLAND",
        F_HEAD,
        592,
    )
    draw_lines(d, 424, 148, head_lines, F_HEAD, INK, 44)
    y = 148 + len(head_lines) * 44 + 8
    body_lines = wrap(
        d,
        "400+ drones and 110 missiles overnight; at least 8 killed in "
        "Kyiv. Two missiles and a drone come down on Polish soil \u2014 "
        "Warsaw calls it a deliberate provocation.",
        F_BODY,
        592,
    )
    draw_lines(d, 424, y, body_lines, F_BODY, INK, 28)

    # ---- four panels, 2 x 2
    panels = [
        {
            "kicker": "MARKETS  ·  NEW YORK",
            "place": "WALL STREET",
            "head": "AI ROUT SINKS S&P INTO CORRECTION",
            "body": "Wall Street falls 3.7% as AI and chip stocks plunge.",
            "pic": chart_pictogram,
        },
        {
            "kicker": "JUSTICE  ·  THE HAGUE",
            "place": "THE HAGUE",
            "head": "COURT: MYANMAR GUILTY OF GENOCIDE",
            "body": "The International Court of Justice finds Myanmar "
                    "responsible for genocide against the Rohingya.",
            "pic": scales_pictogram,
        },
        {
            "kicker": "HEALTH  ·  LONDON",
            "place": "CLINICAL TRIAL",
            "head": "CANCER PILL ERASES TUMOURS IN 1 IN 12",
            "body": "Trial pill daraxonrasib leaves pancreatic tumours "
                    "undetectable on scans in one in 12 patients.",
            "pic": health_pictogram,
        },
        {
            "kicker": "POLITICS  ·  BRUSSELS",
            "place": "BRUSSELS",
            "head": "UK\u2013EU SIGN BIGGEST POST-BREXIT DEAL",
            "body": "Three agreements on food exports, carbon markets and "
                    "youth mobility \u2014 the biggest step since Brexit.",
            "pic": deal_pictogram,
        },
    ]
    origins = [(8, 400), (520, 400), (8, 640), (520, 640)]
    for panel, (px, py) in zip(panels, origins):
        d.rectangle([px, py, px + 496, py + 232], fill=CARD, outline=NAVY, width=2)
        d.rectangle([px, py, px + 496, py + 6], fill=NAVY)
        panel["pic"](d, px + 12, py + 18, px + 152, py + 220)
        tx = px + 168
        d.text((tx, py + 16), panel["kicker"], font=F_KICK, fill=RED)
        head = wrap(d, panel["head"], F_PANEL_HEAD, 496 - 168 - 12)
        draw_lines(d, tx, py + 44, head, F_PANEL_HEAD, INK, 30)
        by = py + 44 + len(head) * 30 + 6
        body = wrap(d, panel["body"], F_PANEL_BODY, 496 - 168 - 12)
        draw_lines(d, tx, by, body, F_PANEL_BODY, INK, 24)
        d.text((tx, py + 232 - 26), panel["place"], font=F_TAG, fill=GREY)

    # ---- ticker band: also today
    d.rectangle([0, 880, W, 1016], fill=NAVY_DARK)
    d.text((16, 892), "ALSO TODAY", font=F_TICK_LABEL, fill=GOLD)
    ticker_items = [
        "FBI criminal database hacked",
        "Gen Z protests spread to 25 EU states",
        "6.9 quake shakes Peruvian Andes",
        "Indonesia hit by huge forest fires",
        "Basra power-plant fire kills 4",
        "Palisades fire arsonist convicted",
        "Bayer pays $7.25bn over Roundup",
        "GTA 6 scores ~$4.9bn on day one",
    ]
    sep = "   \u2022   "
    lines = []
    current = ""
    for item in ticker_items:
        trial = item if not current else current + sep + item
        if d.textlength(trial, font=F_TICK) <= 992:
            current = trial
        else:
            lines.append(current)
            current = item
    if current:
        lines.append(current)
    # The band holds three lines at most: drop trailing items until it fits.
    while len(lines) > 3 and ticker_items:
        ticker_items.pop()
        lines = []
        current = ""
        for item in ticker_items:
            trial = item if not current else current + sep + item
            if d.textlength(trial, font=F_TICK) <= 992:
                current = trial
            else:
                lines.append(current)
                current = item
        if current:
            lines.append(current)
    y = 918
    for line in lines:
        d.text((16, y), line, font=F_TICK, fill=WHITE)
        y += 27

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out_path, "PNG")
    print("wrote", out_path, img.size, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    main()
