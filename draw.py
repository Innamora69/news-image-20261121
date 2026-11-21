#!/usr/bin/env python3
"""Draw the v3 front page: Saturday 21 November 2026, 35 stories, all dated.

One fix over v2: every story on the page happened, or was first reported,
on Saturday 21 November 2026. Friday's news (the Kyiv barrage, the missiles
that landed in Poland, Wall Street's slide, the UK-EU deal, the ICJ Myanmar
ruling, Cyclone Akvan's landfall) is named in the DATE CHECK box as left out.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (25, 25, 25)
RED = (176, 30, 30)
BLUE = (29, 78, 137)
TEAL = (14, 122, 107)
GOLD = (168, 120, 20)
GREEN = (46, 125, 50)
PURPLE = (106, 63, 160)
GREY = (110, 105, 95)
LIGHT = (238, 232, 216)
WHITE = (255, 255, 255)
SKY = (186, 214, 235)
NIGHT = (18, 32, 66)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF_IT = lambda s: font("DejaVuSerif.ttf", s)  # no italic serif on disk; regular serif reads as the deck
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class Ink:
    """Tiny drawing helper: every method paints on the shared canvas."""

    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)

    def panel(self, x, y, w, h, fill=WHITE, outline=INK, width=1):
        self.d.rectangle([x, y, x + w, y + h], fill=fill, outline=outline, width=width)

    def bar(self, x, y, w, h, fill):
        self.d.rectangle([x, y, x + w, y + h], fill=fill)

    def rule(self, x, y, w, weight=2, fill=INK):
        self.d.rectangle([x, y, x + w, y + weight], fill=fill)

    def disc(self, x, y, r, fill, outline=None):
        self.d.ellipse([x - r, y - r, x + r, y + r], fill=fill, outline=outline)

    def text(self, x, y, s, fnt, fill=INK, anchor="la"):
        self.d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)

    def centre(self, x, y, s, fnt, fill=INK):
        self.d.text((x, y), s, font=fnt, fill=fill, anchor="ma")

    def para(self, x, y, s, fnt, width, fill=INK, gap=3):
        lines = wrap(self.d, s, fnt, width)
        for ln in lines:
            self.d.text((x, y), ln, font=fnt, fill=fill)
            y += fnt.size + gap
        return y

    def num_badge(self, x, y, n, r=9):
        self.disc(x, y, r, RED)
        self.centre(x, y - (6 if r <= 7 else 7), str(n), SANS_B(11 if r <= 7 else 12), WHITE)


# ---------------------------------------------------------------- stories
# 13 cards (1-3 lead, 4-13 small) + 22 more in the list = 35 stories.
CARDS = [
    dict(n=1, place="ANTALYA, TURKIYE", tag="CLIMATE", art="cop",
         head="Climate summit runs into Saturday with no deal",
         body="COP31 missed its Friday close. Nearly 200 countries; a draft with no mention of fossil fuels split the summit, and a third text is promised.",
         src="AFP, Al Jazeera"),
    dict(n=2, place="RIYADH, SAUDI ARABIA", tag="WAR", art="riy",
         head="Three Houthi missiles shot down over Riyadh",
         body="Air defences intercepted three ballistic missiles fired from Yemen in the small hours of Saturday; no casualties were reported.",
         src="AFP, Arab News"),
    dict(n=3, place="JUNIN, PERU", tag="EARTHQUAKE", art="peru",
         head="Magnitude 6.7 earthquake shakes central Peru",
         body="The quake struck at 00:09 UTC, 108 km deep, and was felt in Lima. No deaths were reported.",
         src="USGS, AFP"),
    dict(n=4, place="KYIV, UKRAINE", tag="WAR", art="kyiv",
         head="Zelensky: Crimea bridge \u201cwill not stay\u201d",
         body="He warns of double-tap strikes in an NBC interview.",
         src="NBC"),
    dict(n=5, place="STRAIT OF HORMUZ", tag="WAR", art="hormuz",
         head="Iran says it shot down a US drone",
         body="Tehran claims the shootdown; Washington has not confirmed it.",
         src="IRIB"),
    dict(n=6, place="TEHRAN, IRAN", tag="DIPLOMACY", art="tehran",
         head="Iran: uranium stock stays in the country",
         body="Minister still seeks a \u201cfair solution\u201d.",
         src="ToI"),
    dict(n=7, place="WASHINGTON, USA", tag="TECHNOLOGY", art="trump",
         head="Trump vows tax on data centres abroad",
         body="\u201cTremendous\u201d penalty promised; no details yet.",
         src="ABC"),
    dict(n=8, place="BEIJING, CHINA", tag="DIPLOMACY", art="beijing",
         head="China tells Japan to \u201ccorrect\u201d Taiwan words",
         body="Tokyo says its stance is unchanged.",
         src="Ministry, AFP"),
    dict(n=9, place="DAVAO, PHILIPPINES", tag="AVIATION", art="davao",
         head="Jet lands safely after engine-fire alert",
         body="Air Niugini 767 diverts after midnight; all 146 aboard safe.",
         src="AP"),
    dict(n=10, place="CANBERRA, AUSTRALIA", tag="DIPLOMACY", art="canberra",
         head="Australia and China agree to AI talks",
         body="Albanese ends an 11-day trip.",
         src="ABC"),
    dict(n=11, place="WORLD", tag="MARKETS", art="bitcoin",
         head="Bitcoin trades below $59,000 on Saturday",
         body="Down 3.9% in 24 hours; ether $1,625.",
         src="CoinGecko"),
    dict(n=12, place="LAS VEGAS, USA", tag="FORMULA ONE", art="vegas",
         head="Russell fastest in final Las Vegas practice",
         body="1:34.041 in a damp, messy session.",
         src="Formula 1"),
    dict(n=13, place="WELLINGTON, NZ", tag="CRICKET", art="rahul",
         head="Rahul hits a century against New Zealand",
         body="India 344 for 2 at tea, replying to 368.",
         src="AFP"),
]

MORE = [
    (14, "Kryvyi Rih double-tap: 2 dead, 42 hurt", "Kyiv Ind."),
    (15, "Copenhagen: Russian attach\u00e9 expelled", "Al Jazeera"),
    (16, "Antalya: EU warns of a \u201cfossil summit\u201d", "AFP"),
    (17, "Antalya: Panama may block climate text", "Al Jazeera"),
    (18, "Antalya: Indonesia PLN signs clean-power deals", "Antara"),
    (19, "Yemen: Houthis threaten Jeddah, Red Sea ports", "Al Jazeera"),
    (20, "Washington: Vance: Iran strikes were Trump\u2019s call", "Reuters"),
    (21, "Washington: Lawmaker threatens SpaceX funding", "CNN"),
    (22, "Texas: Execution of a man of 70 takes 63 minutes", "ABC"),
    (23, "Los Angeles: Palisades fire starter convicted", "ABC"),
    (24, "Missouri: $7.25bn Roundup settlement approved", "AFP"),
    (25, "Vancouver: Canada rests youth climate defence", "AFP"),
    (26, "Pyongyang: Kim tours factories, no Trump meeting", "AFP"),
    (27, "Sejong: Freight train derails; no one hurt", "Korea Herald"),
    (28, "Taipei: Budget and cash payout passed", "Taipei Times"),
    (29, "Bangkok: Arsenic plan for two rivers", "The Nation"),
    (30, "New Delhi: Pakistani minister joins SCO forum", "Dawn"),
    (31, "Eastern India: Rain alerts as Akvan remnants pass", "ETV"),
    (32, "Myanmar: Rights groups urge sanctions", "AP"),
    (33, "Port Louis: Rating agency talks to 15 states", "Al Jazeera"),
    (34, "Melbourne: Cummins keeps Australian captaincy", "ABC"),
    (35, "Las Vegas: Verstappen sent to stewards", "Autosport"),
]

# Regions of the 35, counted from the lists above: must add to 35.
REGIONS = [("EUROPE", 3, BLUE), ("ASIA", 10, RED), ("MIDDLE EAST", 4, GOLD),
           ("AFRICA", 1, GREEN), ("AMERICAS", 11, PURPLE), ("OCEANIA", 3, TEAL),
           ("GLOBAL", 3, GREY)]

STATS = [
    ("13", "days COP31 has now run in Antalya, still with no deal"),
    ("3", "ballistic missiles shot down over Riyadh before dawn"),
    ("6.7", "magnitude of the earthquake in Jun\u00edn, central Peru"),
    ("146", "people safe after the Davao engine-fire alert"),
    ("$58,983", "bitcoin early Saturday, down 3.9% in a day"),
    ("124*", "runs by K L Rahul at tea in Wellington"),
]

# ---------------------------------------------------------------- pictures
def draw_art(ink, kind, x, y, w, h):
    """One small original drawing per card, fitted in the given box."""
    d = ink.d
    if kind == "cop":  # globe, thermometer, clock
        d.rectangle([x, y, x + w, y + h], fill=SKY)
        ink.disc(x + w // 4, y + h // 2, 26, (52, 143, 90))
        ink.disc(x + w // 4 - 8, y + h // 2 - 6, 9, (120, 190, 130))
        ink.disc(x + w // 4 + 10, y + h // 2 + 10, 7, (120, 190, 130))
        d.rectangle([x + w // 2 - 4, y + 14, x + w // 2 + 4, y + h - 18], fill=RED)
        ink.disc(x + w // 2, y + h - 16, 10, RED)
        cx, cy = x + w - 42, y + h // 2
        ink.disc(cx, cy, 24, WHITE, INK)
        d.line([cx, cy, cx, cy - 15], fill=INK, width=3)
        d.line([cx, cy, cx + 11, cy + 5], fill=INK, width=3)
    elif kind == "riy":  # night skyline, missile arcs
        d.rectangle([x, y, x + w, y + h], fill=NIGHT)
        ink.disc(x + w - 26, y + 20, 11, (240, 230, 180))
        for bx, bw, bh in [(0, 46, 52), (52, 38, 70), (96, 52, 44), (154, 40, 62),
                           (200, 48, 54), (254, 40, 66)]:
            d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(38, 54, 96))
            for wy in range(y + h - bh + 8, y + h - 6, 12):
                d.rectangle([x + bx + 8, wy, x + bx + 16, wy + 6], fill=(250, 200, 80))
        for sx, sy in [(60, 26), (150, 14), (230, 30)]:
            d.line([x + sx, y + sy + 26, x + sx + 26, y + sy], fill=(250, 200, 80), width=2)
            ink.disc(x + sx + 28, y + sy - 2, 4, (250, 200, 80))
    elif kind == "peru":  # mountains, seismograph, house
        d.rectangle([x, y, x + w, y + h], fill=(232, 222, 198))
        d.polygon([(x, y + h), (x + 90, y + 18), (x + 180, y + h)], fill=(120, 110, 100))
        d.polygon([(x + 140, y + h), (x + 240, y + 30), (x + w, y + h)], fill=(90, 84, 78))
        pts = [(x + 8, y + h - 34), (x + 40, y + h - 34), (x + 52, y + h - 58),
               (x + 64, y + h - 14), (x + 78, y + h - 46), (x + 92, y + h - 34),
               (x + 130, y + h - 34), (x + 142, y + h - 62), (x + 156, y + h - 10),
               (x + 170, y + h - 40), (x + 210, y + h - 34)]
        d.line(pts, fill=RED, width=3)
        d.rectangle([x + w - 62, y + h - 42, x + w - 14, y + h - 8], fill=(190, 120, 70))
        d.polygon([(x + w - 66, y + h - 40), (x + w - 38, y + h - 58),
                   (x + w - 10, y + h - 40)], fill=RED)
    elif kind == "kyiv":  # bridge at dusk
        d.rectangle([x, y, x + w, y + h], fill=(252, 212, 90))
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(70, 90, 140))
        d.line([x + 10, y + h - 16, x + w - 10, y + h - 16], fill=INK, width=4)
        for px in (50, 110, 170, 230):
            d.line([x + px, y + 12, x + px, y + h - 16], fill=INK, width=3)
    elif kind == "hormuz":  # sea, ship, drone
        d.rectangle([x, y, x + w, y + h], fill=(120, 170, 210))
        d.rectangle([x + 30, y + h - 30, x + w - 30, y + h - 14], fill=(40, 60, 90))
        d.rectangle([x + 90, y + h - 48, x + 150, y + h - 30], fill=(40, 60, 90))
        ink.disc(x + w - 60, y + 22, 7, INK)
        d.line([x + w - 78, y + 22, x + w - 42, y + 22], fill=INK, width=2)
        d.line([x + w - 60, y + 8, x + w - 60, y + 36], fill=INK, width=2)
    elif kind == "tehran":  # atom over stripes
        d.rectangle([x, y, x + w, y + h], fill=WHITE)
        d.rectangle([x, y, x + w, y + h // 3], fill=GREEN)
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=RED)
        cx, cy = x + w // 2, y + h // 2
        ink.disc(cx, cy, 7, RED)
        for ang in (0, 60, 120):
            import math
            rx, ry = 34, 13
            pts = []
            for t in range(0, 361, 12):
                r = math.radians(t + ang)
                pts.append((cx + rx * math.cos(r), cy + ry * math.sin(r)))
            d.line(pts, fill=INK, width=2)
    elif kind == "trump":  # tower with percent
        d.rectangle([x, y, x + w, y + h], fill=(30, 50, 90))
        d.rectangle([x + w // 2 - 26, y + 8, x + w // 2 + 26, y + h], fill=(200, 170, 90))
        for wy in range(y + 16, y + h - 6, 14):
            d.rectangle([x + w // 2 - 18, wy, x + w // 2 + 18, wy + 7], fill=NIGHT)
        ink.centre(x + w - 30, y + h - 30, "%", SERIF(34), WHITE)
    elif kind == "beijing":  # two flags
        d.rectangle([x, y, x + w, y + h], fill=(240, 235, 220))
        d.rectangle([x + 16, y + 10, x + 110, y + h - 12], fill=RED)
        ink.disc(x + 40, y + 26, 7, (250, 220, 80))
        d.rectangle([x + 150, y + 10, x + 250, y + h - 12], fill=WHITE, outline=INK)
        ink.disc(x + 200, y + h // 2, 26, RED)
    elif kind == "davao":  # plane over clouds
        d.rectangle([x, y, x + w, y + h], fill=SKY)
        for cx, cy in [(60, 66), (150, 78), (240, 62)]:
            ink.disc(cx, cy, 14, WHITE)
            ink.disc(cx + 16, cy + 4, 11, WHITE)
        d.polygon([(x + 90, y + 30), (x + 210, y + 30), (x + 225, y + 40),
                   (x + 90, y + 40)], fill=WHITE)
        d.polygon([(x + 210, y + 30), (x + 250, y + 18), (x + 250, y + 44)], fill=WHITE)
        d.polygon([(x + 120, y + 40), (x + 140, y + 58), (x + 160, y + 40)], fill=WHITE)
    elif kind == "canberra":  # parliament flagpole
        d.rectangle([x, y, x + w, y + h], fill=(210, 225, 210))
        d.polygon([(x + 20, y + h), (x + w // 2, y + 26), (x + w - 20, y + h)], fill=(90, 120, 90))
        d.line([x + w // 2, y + 8, x + w // 2, y + 30], fill=INK, width=3)
        d.rectangle([x + w // 2, y + 8, x + w // 2 + 30, y + 20], fill=BLUE)
    elif kind == "bitcoin":  # falling chart
        d.rectangle([x, y, x + w, y + h], fill=(20, 20, 20))
        ink.disc(x + 34, y + h // 2, 20, (247, 147, 26))
        ink.centre(x + 34, y + h // 2 - 15, "B", SANS_B(28), WHITE)
        pts = [(x + 70, y + 16), (x + 120, y + 30), (x + 160, y + 24),
               (x + 210, y + 52), (x + 250, y + 46), (x + w - 12, y + h - 14)]
        d.line(pts, fill=RED, width=4)
        for px, py in pts:
            ink.disc(px, py, 3, WHITE)
    elif kind == "vegas":  # track curve, chequer
        d.rectangle([x, y, x + w, y + h], fill=(40, 40, 44))
        d.arc([x - 60, y - 40, x + w + 20, y + h + 30], 200, 340, fill=(250, 200, 80), width=8)
        d.arc([x - 20, y - 10, x + w + 60, y + h + 60], 200, 340, fill=WHITE, width=3)
        for i in range(6):
            for j in range(2):
                if (i + j) % 2 == 0:
                    d.rectangle([x + 14 + i * 12, y + h - 30 + j * 12,
                                 x + 26 + i * 12, y + h - 18 + j * 12], fill=WHITE)
    else:  # rahul: bat and ball
        d.rectangle([x, y, x + w, y + h], fill=(46, 125, 50))
        d.rectangle([x, y + h - 22, x + w, y + h], fill=(120, 90, 50))
        d.line([x + 60, y + h - 20, x + 150, y + 20], fill=(220, 180, 120), width=10)
        d.line([x + 150, y + 20, x + 168, y + 8], fill=(220, 180, 120), width=6)
        ink.disc(x + 220, y + 26, 12, RED, WHITE)


# ---------------------------------------------------------------- layout
def build():
    assert len(CARDS) + len(MORE) == 35
    assert sum(n for _, n, _ in REGIONS) == 35
    ink = Ink()
    d = ink.d
    mx, right = 28, W - 28
    cw = right - mx

    # Masthead
    ink.text(mx, 8, "THE WORLD IN ONE DAY", SANS_B(15), RED)
    ink.text(right, 10, "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SATURDAY 21 NOVEMBER 2026",
             SANS_B(11), INK, anchor="ra")
    ink.rule(mx, 30, cw, 3)
    ink.centre(W // 2, 44, "Saturday 21 November 2026", SERIF(56))
    ink.centre(W // 2, 122, "COP31 runs into overtime \u00b7 Missiles downed over Riyadh \u00b7 A 6.7 quake shakes Peru",
               SERIF_IT(21), INK)
    ink.rule(mx, 152, cw, 2)

    # Number strip: six facts at a glance
    y0, col = 162, cw // 6
    for i, (big, cap) in enumerate(STATS):
        x = mx + i * col
        ink.centre(x + col // 2, y0, big, SERIF(34), RED)
        ink.para(x + 8, y0 + 40, cap, SANS(11), col - 16, GREY, gap=1)
        if i:
            d.line([x, y0 + 4, x, y0 + 74], fill=GREY, width=1)
    ink.rule(mx, 246, cw, 2)

    # Region bar: coloured segments, with a legend line underneath
    y0 = 254
    x = mx
    for name, n, colr in REGIONS:
        seg = cw * n // 35
        ink.bar(x, y0, seg, 14, colr)
        x += seg
    lx = mx
    for name, n, colr in REGIONS:
        label = f"{name} {n}"
        ink.text(lx, y0 + 18, label, SANS_B(11), colr)
        lx += d.textlength(label + "   \u00b7   ", font=SANS_B(11))

    # Three lead cards
    y0, lead_h, gap = 292, 210, 12
    lw = (cw - 2 * gap) // 3
    for i, c in enumerate(CARDS[:3]):
        x = mx + i * (lw + gap)
        ink.panel(x, y0, lw, lead_h)
        draw_art(ink, c["art"], x + 1, y0 + 1, lw - 2, 80)
        d.rectangle([x, y0 + 81, x + lw, y0 + 101], fill=RED)
        ink.text(x + 8, y0 + 85, c["place"], SANS_B(11), WHITE)
        ink.text(x + lw - 8, y0 + 85, c["tag"], SANS_B(11), WHITE, anchor="ra")
        yy = ink.para(x + 8, y0 + 107, c["head"], SERIF(18), lw - 16, gap=1)
        ink.para(x + 8, yy + 2, c["body"], SANS(11), lw - 16, GREY, gap=1)
        ink.text(x + 8, y0 + lead_h - 16, c["src"], SANS(10), GREY)

    # Ten small cards, five across, two rows. Art is a flat colour band
    # with the tag: the scene drawings only fit the wide lead cards.
    TAGCOL = {"WAR": RED, "DIPLOMACY": BLUE, "TECHNOLOGY": PURPLE,
              "AVIATION": TEAL, "MARKETS": (20, 20, 20), "FORMULA ONE": (40, 40, 44),
              "CRICKET": GREEN}
    y0, small_h = 512, 104
    sw = (cw - 4 * gap) // 5
    for row in range(2):
        for col_i in range(5):
            c = CARDS[3 + row * 5 + col_i]
            x = mx + col_i * (sw + gap)
            y = y0 + row * (small_h + gap)
            ink.panel(x, y, sw, small_h)
            ink.bar(x + 1, y + 1, sw - 2, 34, TAGCOL.get(c["tag"], GREY))
            ink.centre(x + sw // 2, y + 11, c["tag"], SANS_B(13), WHITE)
            ink.num_badge(x + 14, y + 46, c["n"])
            ink.text(x + 28, y + 40, c["place"], SANS_B(9), RED)
            yy = ink.para(x + 8, y + 56, c["head"], SERIF(11), sw - 16, gap=0)
            ink.text(x + 8, y + small_h - 13, c["src"], SANS(9), GREY)

    # Bottom: map on the left, the other 22 stories on the right
    y0 = 738
    ink.text(mx, y0, "WHERE IT HAPPENED", SANS_B(13), RED)
    ink.text(mx + 272, y0, "ALSO ON SATURDAY 21 NOVEMBER \u2014 22 MORE STORIES \u00b7 35 IN ALL",
             SANS_B(13), RED)
    map_x, map_y, map_w, map_h = mx, y0 + 22, 260, 156
    ink.panel(map_x, map_y, map_w, map_h, fill=(205, 225, 240), outline=INK)
    land = [(38, 56, 90, 119), (125, 48, 170, 89), (125, 89, 175, 123),
            (170, 45, 247, 85), (163, 110, 210, 139), (215, 123, 247, 145)]
    for lx, ly, rx, ry in land:
        d.ellipse([map_x + lx, map_y + ly, map_x + rx, map_y + ry], fill=(232, 220, 180))
    dots = {1: (150, 66), 2: (185, 98), 3: (70, 120), 4: (168, 48), 5: (205, 88),
            6: (212, 66), 7: (52, 62), 8: (238, 58), 9: (244, 100), 10: (238, 128),
            12: (40, 84), 13: (252, 146)}
    for n, (dx, dy) in dots.items():
        ink.num_badge(map_x + dx, map_y + dy, n, r=7)
    ink.text(mx, map_y + map_h + 3, "Each number is the story with that number on this page.",
             SANS(9), GREY)
    ink.text(mx, map_y + map_h + 15, "11 is a market, not a place \u2014 it is in the strip above.",
             SANS(9), GREY)

    lx = mx + 272
    col_w = (right - lx - 12) // 2
    for i, (n, txt, src) in enumerate(MORE):
        col_i, row = divmod(i, 11)
        x = lx + col_i * (col_w + 12)
        y = y0 + 22 + row * 15
        ink.text(x, y, str(n), SANS_B(10), RED)
        ink.text(x + 20, y, txt, SANS(10))
        tw = d.textlength(txt, font=SANS(10))
        ink.text(x + 20 + tw + 4, y, f"({src})", SANS(9), GREY)

    # Date check: what was left out, and why
    y0 = 944
    ink.panel(mx, y0, cw, 48, fill=WHITE, outline=RED, width=2)
    ink.text(mx + 10, y0 + 5, "DATE CHECK", SANS_B(12), RED)
    ink.para(mx + 10, y0 + 21,
             "Left out \u2014 Friday 20 November\u2019s news: the Russian barrage on Kyiv, the missiles "
             "that landed in Poland, Wall Street\u2019s slide into correction, the UK\u2013EU deal, the "
             "ICJ Myanmar ruling, Cyclone Akvan\u2019s landfall. Older still: GTA VI launched Thursday.",
             SANS(11), cw - 20, gap=1)
    ink.text(mx, 998,
             "Every story here happened, or was first reported, on Saturday 21 November 2026. "
             "Sources named beside each story.",
             SANS(10), GREY)
    return ink.img


if __name__ == "__main__":
    out = os.environ.get("OUT", "entry.png")
    build().save(out)
    print("wrote", out)
