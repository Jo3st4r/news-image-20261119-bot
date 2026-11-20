"""Draw the 19 November 2026 front-page poster (1024x1024 PNG).

Flat-vector editorial style, real text throughout, no AI imagery.
Run from the repository root: python3 tools/render.py
Writes assets/entry.png. Fully deterministic: fixed palette, fixed
geometry, fixed font sizes, no randomness, no network, no clock.

Page rhythm (y bands): masthead 0-112, lead story 126-388, two
half-width rows 398-646 and 656-904, footer ticker 912-1024.
"""

from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "entry.png"

W = H = 1024
MARGIN = 28
GUTTER = 16

PAPER = (246, 239, 227)
INK = (24, 24, 28)
NAVY = (27, 42, 74)
NAVY_DARK = (16, 24, 48)
GOLD = (212, 160, 44)
RED = (178, 34, 34)
ORANGE = (214, 104, 24)
TEAL = (14, 122, 120)
PURPLE = (104, 66, 150)
GREY = (96, 96, 104)
WHITE = (255, 255, 255)
SKY = (223, 233, 245)
SAND = (244, 214, 158)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    """Load a DejaVu font, falling back to PIL's default bitmap font."""
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


def serif_big(size: int) -> ImageFont.FreeTypeFont:
    return load_font("DejaVuSerif-Bold.ttf", size)


def sans_bold(size: int) -> ImageFont.FreeTypeFont:
    return load_font("DejaVuSans-Bold.ttf", size)


def sans(size: int) -> ImageFont.FreeTypeFont:
    return load_font("DejaVuSans.ttf", size)


def wrap(draw: ImageDraw.ImageDraw, text: str,
         font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    """Greedy word wrap; returns lines that fit within max_w pixels."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_w or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw: ImageDraw.ImageDraw, lines: list[str], x: int, y: int,
               font: ImageFont.FreeTypeFont, fill: tuple[int, int, int],
               leading: int) -> int:
    """Draw stacked lines; returns the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def panel(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int,
          accent: tuple[int, int, int]) -> None:
    """White story panel with a dark outline and a coloured top bar."""
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 7], fill=accent)


def kicker(draw: ImageDraw.ImageDraw, x: int, y: int, text: str,
           colour: tuple[int, int, int]) -> int:
    """Small bold section label; returns the y below it."""
    font = sans_bold(20)
    draw.text((x, y), text, font=font, fill=colour)
    return y + 28


def headline(draw: ImageDraw.ImageDraw, x: int, y: int, text: str,
             max_w: int, size: int = 38) -> int:
    """Serif headline wrapped to max_w; returns the y below it."""
    font = serif_big(size)
    lines = wrap(draw, text, font, max_w)
    return draw_lines(draw, lines, x, y, font, INK, size + 6)


def body(draw: ImageDraw.ImageDraw, x: int, y: int, text: str,
         max_w: int, size: int = 20) -> int:
    """Sans body copy wrapped to max_w; returns the y below it."""
    font = sans(size)
    lines = wrap(draw, text, font, max_w)
    return draw_lines(draw, lines, x, y, font, INK, size + 6)


def subline(draw: ImageDraw.ImageDraw, x: int, y: int, text: str,
            max_w: int, size: int = 20) -> int:
    """Grey secondary line wrapped to max_w; returns the y below it."""
    font = sans(size)
    lines = wrap(draw, text, font, max_w)
    return draw_lines(draw, lines, x, y, font, GREY, size + 5)


# ---------------------------------------------------------------- flags

def flag_us(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    """Stylised Stars and Stripes, 74x48."""
    fw, fh = 74, 48
    draw.rectangle([x, y, x + fw, y + fh], fill=WHITE, outline=INK, width=1)
    for i in range(7):
        if i % 2 == 0:
            draw.rectangle([x, y + i * 7, x + fw, y + i * 7 + 7], fill=RED)
    draw.rectangle([x, y, x + 30, y + 27], fill=NAVY)
    for r in range(3):
        for c in range(4):
            draw.ellipse([x + 4 + c * 7, y + 4 + r * 8,
                          x + 8 + c * 7, y + 8 + r * 8], fill=WHITE)


def flag_cn(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    """Stylised Chinese flag, 74x48: red field, five gold stars."""
    fw, fh = 74, 48
    draw.rectangle([x, y, x + fw, y + fh], fill=RED, outline=INK, width=1)
    draw.ellipse([x + 8, y + 8, x + 20, y + 20], fill=GOLD)
    for sx, sy in [(28, 8), (36, 14), (36, 24), (28, 30)]:
        draw.ellipse([x + sx, y + sy, x + sx + 6, y + sy + 6], fill=GOLD)


def flag_ru(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    """Stylised Russian tricolour, 74x48."""
    fw, fh = 74, 48
    draw.rectangle([x, y, x + fw, y + 16], fill=WHITE, outline=INK, width=1)
    draw.rectangle([x, y + 16, x + fw, y + 32], fill=(0, 90, 170))
    draw.rectangle([x, y + 32, x + fw, y + fh], fill=RED)


def skyline(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    """Dark city silhouette with lit windows, anchored at (x, y+h)."""
    base = y + h
    blocks = [(0, 62, 48), (58, 84, 56), (130, 48, 52),
              (184, 74, 54), (252, 56, 50)]
    for bx, bw, bh in blocks:
        draw.rectangle([x + bx, base - bh, x + bx + bw, base], fill=NAVY_DARK)
        for wy in range(base - bh + 8, base - 6, 14):
            for wx in range(x + bx + 8, x + bx + bw - 8, 14):
                draw.rectangle([wx, wy, wx + 5, wy + 6], fill=GOLD)


def palm(draw: ImageDraw.ImageDraw, x: int, y: int, s: float) -> None:
    """Tiny palm tree: trunk plus five fronds."""
    draw.line([x, y, x + 4 * s, y - 20 * s], fill=(90, 60, 20), width=3)
    top_x, top_y = x + 4 * s, y - 20 * s
    for dx, dy in [(-11, -5), (-7, -9), (0, -10), (7, -9), (11, -5)]:
        draw.line([top_x, top_y, top_x + dx * s, top_y + dy * s],
                  fill=(46, 120, 60), width=3)


def starfield(draw: ImageDraw.ImageDraw, x: int, y: int,
              w: int, h: int) -> None:
    """Fixed star field: no randomness, same dots every run."""
    spots = [(12, 8, 2), (48, 20, 2), (90, 6, 3), (140, 22, 2),
             (190, 8, 2), (240, 20, 3), (290, 8, 2), (330, 18, 2),
             (370, 6, 2), (420, 20, 3), (30, 28, 2), (210, 28, 2)]
    for sx, sy, r in spots:
        draw.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                     fill=WHITE)


# ---------------------------------------------------------------- page

def draw_header(draw: ImageDraw.ImageDraw) -> None:
    """Navy masthead with the paper name, date and standfirst."""
    draw.rectangle([0, 0, W, 112], fill=NAVY)
    eyebrow = "T H E   W O R L D   I N   O N E   I M A G E"
    font = sans_bold(21)
    tw = draw.textlength(eyebrow, font=font)
    draw.text(((W - tw) / 2, 10), eyebrow, font=font, fill=WHITE)
    date_font = serif_big(54)
    date = "19 NOVEMBER 2026"
    tw = draw.textlength(date, font=date_font)
    draw.text(((W - tw) / 2, 32), date, font=date_font, fill=WHITE)
    stand = "THURSDAY  ·  THE DAY'S WORLD NEWS IN ONE PAGE"
    sfont = sans_bold(18)
    tw = draw.textlength(stand, font=sfont)
    draw.text(((W - tw) / 2, 90), stand, font=sfont, fill=GOLD)
    draw.rectangle([0, 112, W, 116], fill=RED)


def draw_lead(draw: ImageDraw.ImageDraw) -> None:
    """Lead story: the Shenzhen trilateral, text left, art right."""
    x, y, w, h = MARGIN, 126, W - 2 * MARGIN, 262
    panel(draw, x, y, w, h, RED)
    tx = x + 20
    cy = kicker(draw, tx, y + 20, "DIPLOMACY  ·  SHENZHEN, CHINA", RED)
    cy = headline(draw, tx, cy + 4, "THREE AT ONE TABLE", 560, size=52)
    cy = body(draw, tx, cy + 6,
              "Trump, Xi and Putin hold the first-ever trilateral "
              "summit in Shenzhen.", 560, size=22)
    subline(draw, tx, cy + 4,
            "Nuclear arms on the agenda; no deal expected.", 560)
    # illustration: sky, sun, three flags, skyline
    ix, iy, iw, ih = 640, 142, 340, 230
    draw.rectangle([ix, iy, ix + iw, iy + ih], fill=SKY, outline=INK, width=1)
    draw.ellipse([ix + 235, iy + 14, ix + 295, iy + 74], fill=GOLD,
                 outline=INK, width=2)
    flag_us(draw, ix + 18, iy + 92)
    flag_cn(draw, ix + 108, iy + 92)
    flag_ru(draw, ix + 198, iy + 92)
    lab = sans_bold(17)
    lab_text = "US  ·  CHINA  ·  RUSSIA"
    tw = draw.textlength(lab_text, font=lab)
    draw.text((ix + (iw - tw) / 2, iy + 146), lab_text, font=lab, fill=INK)
    skyline(draw, ix + 12, iy + 172, iw - 24, 58)


def draw_gta(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    """Culture panel: GTA VI launch, with a Vice City strip."""
    panel(draw, x, y, w, h, ORANGE)
    tx = x + 18
    cy = kicker(draw, tx, y + 16, "CULTURE  ·  VICE CITY", ORANGE)
    cy = headline(draw, tx, cy + 2, "GTA VI ROLLS OUT", w - 36, size=38)
    body(draw, tx, cy + 6,
         "The 13-year wait ends as the game unlocks worldwide "
         "at midnight — Metacritic 99.", w - 36)
    sy = y + h - 48
    draw.rectangle([x + 14, sy, x + w - 14, y + h - 14], fill=SAND,
                   outline=INK, width=1)
    palm(draw, x + 44, y + h - 20, 0.9)
    palm(draw, x + 92, y + h - 20, 0.7)
    draw.ellipse([x + w - 72, sy + 6, x + w - 44, sy + 34], fill=ORANGE,
                 outline=INK, width=2)


def draw_space(draw: ImageDraw.ImageDraw, x: int, y: int, w: int,
               h: int) -> None:
    """Space panel: Voyager 1 one light-day out, with a signal strip."""
    panel(draw, x, y, w, h, NAVY)
    tx = x + 18
    cy = kicker(draw, tx, y + 16, "SPACE  ·  NASA", NAVY)
    cy = headline(draw, tx, cy + 2, "ONE LIGHT-DAY FROM EARTH",
                  w - 36, size=38)
    body(draw, tx, cy + 6,
         "Voyager 1 is the first human object this far out — "
         "a signal now takes a full day.", w - 36)
    sy = y + h - 48
    draw.rectangle([x + 14, sy, x + w - 14, y + h - 14], fill=NAVY_DARK,
                   outline=INK, width=1)
    starfield(draw, x + 14, sy, w - 28, 34)
    draw.line([x + 40, sy + 18, x + w - 100, sy + 18], fill=WHITE, width=2)
    for d in range(0, w - 140, 14):
        draw.ellipse([x + 44 + d, sy + 16, x + 48 + d, sy + 20], fill=GOLD)
    draw.rectangle([x + w - 94, sy + 10, x + w - 40, sy + 26], fill=GOLD,
                   outline=INK, width=1)


def draw_weather(draw: ImageDraw.ImageDraw, x: int, y: int, w: int,
                 h: int) -> None:
    """Weather panel: Cyclone Akvan, with a spiral mark."""
    panel(draw, x, y, w, h, TEAL)
    tx = x + 18
    cy = kicker(draw, tx, y + 16, "WEATHER  ·  BAY OF BENGAL", TEAL)
    cy = headline(draw, tx, cy + 2, "AKVAN BEARS DOWN", w - 36, size=38)
    body(draw, tx, cy + 6,
         "A severe cyclone nears India's east coast — red "
         "alerts, schools shut, landfall 20 Nov.", w - 36)
    cx, cy2 = x + w - 46, y + h - 28
    for r, a0, a1 in [(24, 20, 300), (18, 200, 120), (12, 20, 300),
                      (6, 200, 120)]:
        draw.arc([cx - r, cy2 - r, cx + r, cy2 + r], a0, a1, fill=TEAL,
                 width=3)


def draw_faith(draw: ImageDraw.ImageDraw, x: int, y: int, w: int,
               h: int) -> None:
    """Faith panel: Pew projection, with two comparison bars."""
    panel(draw, x, y, w, h, PURPLE)
    tx = x + 18
    cy = kicker(draw, tx, y + 16, "FAITH  ·  PEW RESEARCH", PURPLE)
    cy = headline(draw, tx, cy + 2, "ISLAM TO BE LARGEST FAITH",
                  w - 36, size=38)
    body(draw, tx, cy + 6,
         "Pew projects Muslims will outnumber Christians by "
         "2035 — higher birth rates.", w - 36)
    lab = sans_bold(17)
    by = y + h - 54
    draw.rectangle([tx, by, tx + 258, by + 16], fill=PURPLE)
    draw.text((tx + 268, by - 2), "ISLAM", font=lab, fill=INK)
    by += 26
    draw.rectangle([tx, by, tx + 198, by + 16], fill=(150, 150, 165))
    draw.text((tx + 208, by - 2), "CHRISTIANITY", font=lab, fill=INK)


def draw_ticker(draw: ImageDraw.ImageDraw) -> None:
    """Black footer band with the day's other headlines, in white."""
    draw.rectangle([0, 912, W, H], fill=(12, 12, 14))
    lab = sans_bold(22)
    draw.text((MARGIN, 926), "ALSO TODAY", font=lab, fill=GOLD)
    font = sans(22)
    lines = wrap(draw,
                 "Fed minutes point to more rate hikes  ·  EU proposes a "
                 "€45bn Ukraine loan  ·  Democrats nominate Jeffries as "
                 "first Black Speaker", font, W - 2 * MARGIN)
    draw_lines(draw, lines, MARGIN, 956, font, WHITE, 28)


def render() -> Path:
    """Compose the poster and save it to assets/entry.png."""
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_lead(draw)
    half_w = (W - 2 * MARGIN - GUTTER) // 2
    draw_gta(draw, MARGIN, 398, half_w, 248)
    draw_space(draw, MARGIN + half_w + GUTTER, 398, half_w, 248)
    draw_weather(draw, MARGIN, 656, half_w, 248)
    draw_faith(draw, MARGIN + half_w + GUTTER, 656, half_w, 248)
    draw_ticker(draw)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    path = render()
    print(f"wrote {path} ({path.stat().st_size} bytes)")
