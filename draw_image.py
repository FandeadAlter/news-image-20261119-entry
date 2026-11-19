#!/usr/bin/env python3
"""Draw the news-image-20261119 entry: a 1024x1024 newspaper front page.

One image summing up 19 November 2026, drawn from scratch with PIL.
No external images, no copied starter code. Every shape and every line
of text below is drawn here, in this file.

Stories (researched 19 Nov 2026; sources: JagranJosh,
Education Times, SimpleLife.news):
  1. Grand Theft Auto VI begins global rollout - gamers enter Vice City.
  2. Trump, Xi and Putin hold trilateral talks at the APEC summit
     in Shenzhen.
  3. US and Iran exchange fire in the Gulf - US struck a missile
     site on Iran's Qeshm Island; Iran hit a US base in Kuwait and
     struck Bahrain; the US has 3 carriers in the region.
  4. Nvidia: founder Jensen Huang resigned; acting CEO Colette
     Kress promises earlier pay raises; Nvidia stopped shipping
     H-series chips to China.
  5. NASA Voyager 1 reaches one light-day from Earth.
  6. EU proposes a 45 billion euro Ukraine loan.
  7. Cyclone Akvan intensifies toward the Andhra Pradesh coast
     (landfall 20 November).

Layout (fixed vertical budget, measured 2026-11-19 after the first
render overflowed past 1024px): masthead ~156px, lead story
~375px (headline 52pt, skyline panel 118px), 2x2 secondary grid
2 x 208px, footer one line at the bottom with room to spare.
Inside every secondary cell the graphic strip is placed FIRST
(strip_top is computed up front) and the deck is truncated to the
lines that fit above it, so no graphic can ever cover a deck.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 32
CONTENT_W = W - 2 * MARGIN

PAPER = (253, 252, 246)   # off-white newsprint
INK = (17, 17, 17)
GREY = (90, 90, 90)
RED = (178, 34, 24)       # masthead rule / kickers
BLUE = (29, 78, 216)
TEAL = (13, 116, 128)
GREEN = (22, 101, 52)
SUNSET_TOP = (255, 183, 77)
SUNSET_MID = (255, 122, 89)
SUNSET_LOW = (198, 84, 128)
SEA = (30, 90, 160)
DARK = (32, 24, 56)

SERIF_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
]
SERIF = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif.ttf",
]
SERIF_ITALIC = [
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]
SANS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
SANS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans.ttf",
]


def load_font(candidates, size):
    """First usable font file, else PIL's built-in bitmap font."""
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines fitting max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, lines, x, y, font, fill=INK, leading=None):
    """Draw lines top-left aligned; returns y just below the last line."""
    if leading is None:
        leading = int(font.size * 1.18)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def draw_centred(draw, text, cx, y, font, fill=INK):
    """Draw one line centred on cx."""
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return y + int(font.size * 1.2)


def draw_skyline_panel(draw, x0, y0, x1, y1):
    """Vice City at sunset: banded sky, sun, towers, palms, water."""
    w, h = x1 - x0, y1 - y0
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    # Sunset sky in three horizontal bands.
    bands = [(SUNSET_TOP, 0.00), (SUNSET_MID, 0.38), (SUNSET_LOW, 0.68)]
    for i, (colour, frac) in enumerate(bands):
        top = y0 + int(h * frac)
        bottom = y0 + int(h * bands[i + 1][1]) if i + 1 < len(bands) else y0 + int(h * 0.82)
        draw.rectangle([x0 + 2, top, x1 - 2, bottom], fill=colour)
    # Sun, low over the skyline.
    cx, cy, r = x0 + int(w * 0.72), y0 + int(h * 0.42), 26
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 244, 190),
                 outline=(255, 220, 120), width=3)
    # Tower silhouettes with a few lit windows.
    towers = [(0.02, 0.55, 0.13, 0.82), (0.14, 0.42, 0.24, 0.82),
              (0.26, 0.58, 0.34, 0.82), (0.38, 0.34, 0.50, 0.82),
              (0.52, 0.50, 0.60, 0.82), (0.62, 0.44, 0.74, 0.82),
              (0.76, 0.60, 0.86, 0.82), (0.88, 0.48, 0.98, 0.82)]
    for fx0, fy0, fx1, fy1 in towers:
        tx0, ty0 = x0 + int(w * fx0), y0 + int(h * fy0)
        tx1, ty1 = x0 + int(w * fx1), y0 + int(h * fy1)
        draw.rectangle([tx0, ty0, tx1, ty1], fill=DARK)
        for wy in range(ty0 + 6, ty1 - 6, 14):
            for wx in range(tx0 + 6, tx1 - 6, 14):
                if (wx + wy) % 28 == 0:
                    draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
    # Two palm silhouettes at the left edge.
    for px, ph in [(x0 + 52, 48), (x0 + 96, 36)]:
        base = y0 + int(h * 0.82)
        draw.line([px, base, px + 6, base - ph], fill=DARK, width=5)
        for dx, dy in [(-22, -12), (-12, -20), (4, -24), (18, -17), (26, -7)]:
            draw.line([px + 6, base - ph, px + 6 + dx, base - ph + dy],
                      fill=DARK, width=4)
    # Water at the bottom with light reflections.
    draw.rectangle([x0 + 2, y0 + int(h * 0.82), x1 - 2, y1 - 2], fill=SEA)
    for i, fx in enumerate([0.10, 0.32, 0.55, 0.78]):
        ry = y0 + int(h * (0.87 + 0.03 * (i % 2)))
        draw.line([x0 + int(w * fx), ry, x0 + int(w * fx) + 70, ry],
                  fill=(180, 220, 255), width=3)


def draw_strip(draw, kind, x0, y0, x1, y1):
    """Small graphic strip at the foot of a secondary story cell.

    The strip is only 30px tall, so every drawing here is sized for
    that height: nothing may extend above y0 or below y1.
    """
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=1)
    w, h = x1 - x0, y1 - y0
    if kind == "apec":
        # Three meeting flags: red, blue, green blocks with a star dot.
        draw.rectangle([x0, y0, x1, y1], fill=(238, 238, 228))
        colours = [(178, 34, 24), (29, 78, 216), (22, 101, 52)]
        for i, colour in enumerate(colours):
            fx0 = x0 + 18 + i * 150
            draw.rectangle([fx0, y0 + 5, fx0 + 120, y1 - 5], fill=colour)
            draw.ellipse([fx0 + 54, y0 + 10, fx0 + 66, y0 + 22], fill=(255, 255, 255))
    elif kind == "gulf":
        # Sea with three carrier silhouettes.
        draw.rectangle([x0, y0, x1, y1], fill=(198, 224, 245))
        draw.rectangle([x0, y0 + int(h * 0.60), x1, y1], fill=SEA)
        for i, fx in enumerate([0.08, 0.40, 0.72]):
            sx = x0 + int(w * fx)
            sy = y0 + int(h * 0.45)
            draw.rectangle([sx, sy, sx + 110, sy + 12], fill=(60, 60, 60))
            draw.rectangle([sx + 44, sy - 10, sx + 62, sy], fill=(60, 60, 60))
    elif kind == "nvidia":
        # A chip: dark square, green centre, gold pins.
        draw.rectangle([x0, y0, x1, y1], fill=(20, 24, 20))
        cx, cy = x0 + w // 2, y0 + h // 2
        draw.rectangle([cx - 52, cy - 13, cx + 52, cy + 13], fill=(118, 185, 0))
        draw.text((cx - 34, cy - 10), "H-SERIES", font=load_font(SANS_BOLD, 12),
                  fill=(20, 24, 20))
        for px in range(x0 + 60, x1 - 50, 26):
            draw.line([px, y0 + 3, px, y0 + 9], fill=(212, 175, 55), width=3)
            draw.line([px, y1 - 9, px, y1 - 3], fill=(212, 175, 55), width=3)
    elif kind == "cyclone":
        # Spiral storm: concentric arcs over a teal sea.
        draw.rectangle([x0, y0, x1, y1], fill=(224, 242, 242))
        cx, cy = x0 + w // 2, y0 + h // 2
        for r in (14, 10, 7, 4):
            draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
                     fill=TEAL, width=3)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)


STORIES = [
    {
        "kind": "apec", "kicker": "APEC SUMMIT  •  SHENZHEN",
        "headline": "Trump, Xi and Putin hold trilateral talks",
        "deck": "At the APEC summit in Shenzhen.",
    },
    {
        # "3 US carriers" lives in the kicker so the deck stays 2 lines.
        "kind": "gulf", "kicker": "THE GULF  •  3 US CARRIERS",
        "headline": "US and Iran exchange fire in the Gulf",
        "deck": "US hit Qeshm Island; Iran hit a US base in Kuwait "
                "and Bahrain.",
    },
    {
        # Role + surname in the kicker, first name in the deck.
        "kind": "nvidia", "kicker": "TECH  •  NVIDIA  •  ACTING CEO KRESS",
        "headline": "Nvidia chief Jensen Huang resigns",
        "deck": "Colette Kress promises earlier pay raises. H-series "
                "shipments to China stopped.",
    },
    {
        "kind": "cyclone", "kicker": "WEATHER  •  INDIA",
        "headline": "Cyclone Akvan nears Andhra Pradesh",
        "deck": "Storm intensifies toward the coast. Landfall expected "
                "20 November.",
    },
]


def draw_secondary_cell(draw, story, x0, y0, w, h):
    """One secondary story: kicker, headline, deck, graphic strip.

    The strip position is fixed first (bottom of the cell, 30px
    tall). The deck is then limited to the lines that fit in the
    space above it, with an 8px gap -- it can never run under the
    strip or past the cell border.
    """
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=INK, width=2)
    pad = 12
    strip_h = 30
    strip_top = y0 + h - pad - strip_h
    kicker_font = load_font(SANS_BOLD, 18)
    head_font = load_font(SERIF_BOLD, 29)
    deck_font = load_font(SANS, 19)
    y = y0 + pad
    draw.text((x0 + pad, y), story["kicker"], font=kicker_font, fill=RED)
    y += 26
    lines = wrap_text(draw, story["headline"], head_font, w - 2 * pad)
    y = draw_lines(draw, lines[:2], x0 + pad, y, head_font, leading=33)
    y += 4
    deck_lines = wrap_text(draw, story["deck"], deck_font, w - 2 * pad)
    max_deck_lines = max(1, (strip_top - 8 - y) // 23)
    deck_end = draw_lines(draw, deck_lines[:max_deck_lines], x0 + pad, y,
                          deck_font, leading=23)
    assert deck_end <= strip_top - 8, f"deck overflows strip: {story['kind']}"
    draw_strip(draw, story["kind"], x0 + pad, strip_top,
               x0 + w - pad, strip_top + strip_h)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    cx = W // 2

    # --- Masthead -------------------------------------------------------
    masthead_font = load_font(SERIF_BOLD, 84)
    draw_centred(draw, "THE WORLD", cx, 12, masthead_font)
    draw.line([MARGIN, 108, W - MARGIN, 108], fill=INK, width=2)
    date_font = load_font(SERIF_BOLD, 28)
    draw_centred(draw, "Thursday 19 November 2026", cx, 114, date_font)
    draw.line([MARGIN, 150, W - MARGIN, 150], fill=RED, width=4)
    draw.line([MARGIN, 156, W - MARGIN, 156], fill=INK, width=1)

    # --- Lead story: GTA VI --------------------------------------------
    y = 168
    kicker_font = load_font(SANS_BOLD, 20)
    draw.text((MARGIN, y), "LEAD STORY  •  GAMING", font=kicker_font, fill=RED)
    y += 28
    head_font = load_font(SERIF_BOLD, 52)
    headline = "Grand Theft Auto VI begins global rollout"
    y = draw_lines(draw, wrap_text(draw, headline, head_font, CONTENT_W),
                   MARGIN, y, head_font, leading=57)
    y += 4
    deck_font = load_font(SANS, 23)
    deck = "Gamers enter Vice City as the long-awaited game reaches " \
           "players around the world."
    y = draw_lines(draw, wrap_text(draw, deck, deck_font, CONTENT_W),
                   MARGIN, y, deck_font, leading=28)
    y += 8
    panel_y0, panel_y1 = y, y + 118
    draw_skyline_panel(draw, MARGIN, panel_y0, W - MARGIN, panel_y1)
    y = panel_y1 + 6
    caption_font = load_font(SERIF_ITALIC, 19)
    draw.text((MARGIN, y), "Vice City returns as GTA VI rolls out worldwide.",
              font=caption_font, fill=GREY)
    y += 26
    draw.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)

    # --- Secondary stories: 2x2 grid -----------------------------------
    grid_y = y + 12
    cell_w = (CONTENT_W - 16) // 2
    # 208px: deck gets 2 full lines above the strip (strip_top - deck_y
    # = 58px); at 198px the guard truncated every 2-line deck to 1 line.
    cell_h = 208
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = MARGIN + col * (cell_w + 16)
        y0 = grid_y + row * (cell_h + 10)
        draw_secondary_cell(draw, story, x0, y0, cell_w, cell_h)
    grid_bottom = grid_y + 2 * cell_h + 10

    # --- Footer strip: the two remaining stories, one line -------------
    footer_y = grid_bottom + 10
    footer_font = load_font(SANS_BOLD, 18)  # measured: 925px wide, fits 960px
    footer = ("Also: Voyager 1 reaches one light-day from Earth  •  "
              "EU proposes a 45bn euro Ukraine loan")
    footer_lines = wrap_text(draw, footer, footer_font, CONTENT_W)
    assert len(footer_lines) == 1, f"footer wraps to {len(footer_lines)} lines"
    assert footer_y + 24 <= H - 10, "footer past bottom edge"
    draw_lines(draw, footer_lines, MARGIN, footer_y, footer_font, leading=24)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(f"saved {out} ({W}x{H}, {out.stat().st_size} bytes)")
    print(f"layout: grid_y={grid_y} grid_bottom={grid_bottom} "
          f"footer_y={footer_y} footer_bottom={footer_y + 24}")


if __name__ == "__main__":
    main()
