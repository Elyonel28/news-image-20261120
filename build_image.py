#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper infographic summing up the world
news of Friday 20 November 2026. Uses only the Python standard library
plus Pillow. Run: python3 build_image.py  (writes entry.png next to it).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 40

PAPER = (248, 244, 236)      # warm newsprint
INK = (20, 20, 20)           # near-black text
NAVY = (20, 38, 76)          # masthead + also band
RED = (178, 32, 44)          # date band + lead kicker
RULE = (120, 116, 108)       # thin grey rules
FAINT = (90, 86, 78)         # source line
GOLD = (232, 185, 60)        # ALSO label on navy

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Outer frame.
    d.rectangle([14, 14, W - 15, H - 15], outline=NAVY, width=3)
    d.rectangle([20, 20, W - 21, H - 21], outline=RULE, width=1)

    # ---- Masthead -------------------------------------------------
    mast = font(SERIF, 66)
    d.text((W // 2, 30), "WORLD NEWS", font=mast, fill=NAVY, anchor="ma")
    tag = font(SANS_BOLD, 15)
    d.text((W // 2, 100), "T H E   D A Y   I N   O N E   P I C T U R E",
           font=tag, fill=FAINT, anchor="ma")
    d.line([(MARGIN, 126), (W - MARGIN, 126)], fill=NAVY, width=2)

    # ---- Red date band --------------------------------------------
    d.rectangle([MARGIN, 138, W - MARGIN, 178], fill=RED)
    date_f = font(SANS_BOLD, 30)
    d.text((W // 2, 158), "FRIDAY, 20 NOVEMBER 2026", font=date_f,
           fill=(255, 255, 255), anchor="mm")

    # ---- Lead story -----------------------------------------------
    x0 = MARGIN
    inner = W - 2 * MARGIN
    y = 196
    kick = font(SANS_BOLD, 17)
    d.text((x0, y), "LEAD  ·  EUROPE", font=kick, fill=RED)
    y += 30
    head = font(SERIF, 42)
    lines = wrap(d, "UK and EU agree 100,000-a-year youth mobility scheme",
                 head, inner)
    y = draw_lines(d, lines, x0, y, head, INK, 50)
    y += 8
    deck = font(SANS, 20)
    lines = wrap(d, "Brussels summit seals the centrepiece of a post-Brexit "
                    "reset — food-trade and carbon-market deals too.",
                 deck, inner)
    y = draw_lines(d, lines, x0, y, deck, (50, 48, 44), 26)
    y += 14
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)

    # ---- Story cards: 2 columns x 3 rows -------------------------
    cards = [
        ("MARKETS · ASIA", (31, 78, 121),
         "Taiwan stocks crash 6% in worst week since 1991",
         "Taiex fell 6.2% on Friday to 36,033, down 17% on the week. "
         "TSMC slid below NT$2,000 as AI doubts spread."),
        ("ASIA · DIPLOMACY", (14, 124, 107),
         "Prabowo and Xi open trade-pact talks",
         "Indonesia and China launched talks on a trade pact and joint "
         "South China Sea development."),
        ("TECH · ASIA", (106, 46, 110),
         "Taiwan flags 2,700 China-linked accounts to Meta",
         "Taipei says the accounts are part of a Chinese influence drive "
         "ahead of next week's local elections."),
        ("TECH · POLICY", (46, 107, 46),
         "Jakarta asks Google to explain 19,000 channel takedowns",
         "The digital ministry wants Google to justify removing channels "
         "supportive of the government."),
        ("MARKETS", (140, 106, 0),
         "Dollar at 19-month high as AI rout spreads",
         "Investors fled to safe havens as AI-trade jitters rattled "
         "markets; oil edged up on supply worries."),
        ("ECONOMY · ASIA", (60, 60, 80),
         "Jakarta mining shake-up rattles investors",
         "Miners face fresh cost pressures after Prabowo's call for the "
         "state to take 70% of mining benefits; shares fell for a fifth day."),
    ]
    # The sixth card is the Reuters 20 Nov mining-policy story; the
    # "Europe ready for talks" line was a 19 Nov Berlin statement, so it
    # is not used.
    tag_f = font(SANS_BOLD, 15)
    chead = font(SERIF, 23)
    cbody = font(SANS, 16)
    col_w = (inner - 24) // 2
    row_h = 152
    grid_y = y + 16
    for i, (tag, colour, headline, body) in enumerate(cards):
        col = i % 2
        row = i // 2
        cx = MARGIN + col * (col_w + 24)
        cy = grid_y + row * (row_h + 14)
        d.text((cx, cy), tag, font=tag_f, fill=colour)
        hl = wrap(d, headline, chead, col_w)
        by = draw_lines(d, hl, cx, cy + 22, chead, INK, 28)
        bl = wrap(d, body, cbody, col_w)
        draw_lines(d, bl, cx, by + 4, cbody, (52, 50, 46), 21)
        if col == 0:
            d.line([(cx + col_w + 12, cy), (cx + col_w + 12, cy + row_h - 8)],
                   fill=RULE, width=1)

    # ---- ALSO strip (navy band) ------------------------------------
    band_y = grid_y + 3 * row_h + 2 * 14 + 12
    d.rectangle([MARGIN, band_y, W - MARGIN, band_y + 58], fill=NAVY)
    also_f = font(SANS_BOLD, 15)
    also_body = font(SANS, 15)
    d.text((MARGIN + 14, band_y + 29), "ALSO", font=also_f, fill=GOLD,
           anchor="lm")
    items = ("5.1 quake rattles California  •  Thomas Markle fit to stand "
             "trial  •  Harris meets Macron in Paris")
    lines = wrap(d, items, also_body, inner - 90)
    ly = band_y + 29 - (len(lines) - 1) * 10
    for line in lines:
        d.text((MARGIN + 84, ly), line, font=also_body,
               fill=(255, 255, 255), anchor="lm")
        ly += 20

    # ---- Source line (on the paper, below the ALSO band) ------------
    src = font(SANS, 12)
    d.text((W // 2, band_y + 58 + 16),
           "Sources: BBC · Reuters · The Times · The Guardian · Bloomberg · "
           "Dow Jones · Xinhua",
           font=src, fill=FAINT, anchor="mm")

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
