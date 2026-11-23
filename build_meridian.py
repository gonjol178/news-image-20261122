"""The Daily Meridian - news-image-20261122 entry composer.

Builds entry.png (1024x1024) from three photo panels generated in-session
(assets/) plus typeset headlines in an oxblood broadsheet design.

Layout (anti-convergence vs 20261120 navy/lead-right and 20261121
deep-teal/lead-left): masthead "The Daily Meridian", oxblood accent,
lead story as a full-width band across the top with a wide photo panel,
secondary stories in two columns below the band, IN BRIEF strip at foot.

Deterministic: fixed fonts, fixed geometry, fixed assets, no timestamps,
no randomness. Run: python3 build_meridian.py
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"

W, H = 1024, 1024

PAPER = (247, 242, 232)
INK = (26, 23, 20)
OXBLOOD = (110, 20, 35)
OXBLOOD_DARK = (84, 14, 26)
MUTED = (96, 88, 80)
RULE = (180, 168, 152)
BAND = (243, 230, 226)
CAPTION = (110, 102, 92)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.25)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, size=15):
    fnt = font(SANS_BOLD, size)
    draw.text((x, y), text, font=fnt, fill=OXBLOOD)
    return y + size + 6


def headline(draw, x, y, text, size, width, leading=None):
    fnt = font(SERIF_BOLD, size)
    lines = wrap(draw, text, fnt, width)
    return text_block(draw, x, y, lines, fnt, leading=leading)


def body(draw, x, y, text, size, width):
    fnt = font(SERIF, size)
    lines = wrap(draw, text, fnt, width)
    return text_block(draw, x, y, lines, fnt)


def cover(img, w, h):
    """Centre-crop image to exactly w x h."""
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    return img.crop((left, top, left + w, top + h))


def photo(draw, canvas, path, box):
    x, y, w, h = box
    img = Image.open(path).convert("RGB")
    canvas.paste(cover(img, w, h), (x, y))
    draw.rectangle((x, y, x + w - 1, y + h - 1), outline=INK, width=1)


def main():
    canvas = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(canvas)

    # ---- Masthead -------------------------------------------------------
    d.rectangle((0, 0, W, 7), fill=OXBLOOD)
    mast = font(SERIF_BOLD, 62)
    title = "The Daily Meridian"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 18), title, font=mast, fill=INK)
    d.line((36, 96, W - 36, 96), fill=RULE, width=1)
    meta = font(SANS_BOLD, 15)
    d.text((36, 102), "SUNDAY, 22 NOVEMBER 2026", font=meta, fill=OXBLOOD)
    right = "THE WORLD IN ONE PAGE"
    d.text((W - 36 - d.textlength(right, font=meta), 102), right,
           font=meta, fill=INK)
    d.line((36, 126, W - 36, 126), fill=OXBLOOD, width=2)

    # ---- Lead band: full width, photo panel right ----------------------
    band_y, band_h = 134, 252
    d.rectangle((0, band_y, W, band_y + band_h), fill=BAND)
    d.line((0, band_y, W, band_y), fill=OXBLOOD, width=2)
    d.line((0, band_y + band_h, W, band_y + band_h), fill=OXBLOOD, width=2)

    lx = 40
    y = band_y + 14
    y = kicker(d, lx, y, "CLIMATE  ·  ANTALYA, TURKEY", size=15)
    y = headline(d, lx, y, "COP31 ends with no deal", 38, 470)
    y += 6
    body(d, lx, y,
         "The UN climate summit closed on Sunday with no agreement — the "
         "longest on record — after the EU and about 130 parties rejected "
         "a draft that never mentioned fossil fuels.",
         17, 470)

    photo(d, canvas, ASSETS / "media-generation-lead-cop31-0-ae685060-cf90-4c25-8aed-c932ead23e83.png",
          (536, band_y + 14, 448, 200))
    cap = font(SANS, 12)
    d.text((536, band_y + 220),
           "An empty plenary hall in Antalya as COP31 closed without a deal.",
           font=cap, fill=CAPTION)

    # ---- Secondary stories: two columns ---------------------------------
    col_w = 458
    left_x, right_x = 40, 526
    top = 402

    # Left column: Bahrain (photo) + Mexico
    y = top
    y = kicker(d, left_x, y, "CONFLICT  ·  BAHRAIN")
    y = headline(d, left_x, y, "Iran strikes Bahrain site; Gulf states condemn",
                 23, col_w, leading=28)
    y += 4
    photo(d, canvas, ASSETS / "media-generation-bahrain-0-07376c49-5c43-42ff-b15d-5338fd8661a9.png",
          (left_x, y, col_w, 118))
    y += 118 + 6
    y = body(d, left_x, y,
             "Iranian projectiles hit an industrial site in Bahrain, injuring "
             "two people, as Gulf states condemned the attack.",
             16, col_w)
    y += 8
    d.line((left_x, y, left_x + col_w, y), fill=RULE, width=1)
    y += 8
    y = kicker(d, left_x, y, "JUSTICE  ·  SINALOA, MEXICO")
    y = headline(d, left_x, y, "Cartel boss \u201cEl Chapo Isidro\u201d captured; 11 killed",
                 23, col_w, leading=28)
    y += 4
    body(d, left_x, y,
         "Mexican special forces captured Fausto Isidro Meza Flores, one of "
         "the FBI\u2019s 10 most wanted, in Guasave; four soldiers were among "
         "the dead.",
         16, col_w)

    # Right column: Ukraine (photo) + Washington + Markets (compact row)
    y = top
    y = kicker(d, right_x, y, "CONFLICT  ·  DYMER, UKRAINE")
    y = headline(d, right_x, y, "Drone collapses apartment block; 14 missing",
                 23, col_w, leading=28)
    y += 4
    photo(d, canvas, ASSETS / "media-generation-ukraine-0-7cb5c482-6ab6-4586-89a2-77755f4e6d81.png",
          (right_x, y, col_w, 118))
    y += 118 + 6
    y = body(d, right_x, y,
             "A Russian drone partly collapsed a five-storey apartment block "
             "in Dymer, north of Kyiv, on Sunday; 14 people are unaccounted "
             "for.",
             16, col_w)
    y += 8
    d.line((right_x, y, right_x + col_w, y), fill=RULE, width=1)
    y += 8
    y = kicker(d, right_x, y, "POLITICS  ·  WASHINGTON")
    y = headline(d, right_x, y, "Democrats win largest House majority since 1992",
                 23, col_w, leading=28)
    y += 4
    y = body(d, right_x, y,
             "Democrats secured at least 258 House seats, their best since "
             "1992, setting up divided government in January.",
             16, col_w)
    y += 8
    d.line((right_x, y, right_x + col_w, y), fill=RULE, width=1)
    y += 6
    y = kicker(d, right_x, y, "ECONOMY  ·  NEW YORK")
    body(d, right_x, y,
         "Stocks slide as AI sell-off deepens: the S&P 500 fell 3.7% and "
         "Japan\u2019s Nikkei 5.06%.",
         16, col_w)

    # ---- IN BRIEF strip ---------------------------------------------------
    brief_y = 884
    d.rectangle((0, brief_y, W, brief_y + 104), fill=OXBLOOD)
    d.text((40, brief_y + 10), "IN BRIEF", font=font(SANS_BOLD, 16),
           fill=(247, 242, 232))
    brief = font(SERIF, 14)
    brief_b = font(SERIF_BOLD, 14)
    items = [
        ("MERCURY — ", "BepiColombo, the European-Japanese probe, enters "
         "orbit around Mercury after an eight-year journey."),
        ("BANTEN, INDONESIA — ", "A fire at a candy factory leaves 3 dead "
         "and dozens missing."),
        ("WASHINGTON — ", "The FBI investigates an apparent breach of its "
         "National Crime Information Center database."),
        ("WARSAW — ", "Trump calls the missiles and drone landing in Poland "
         "a \u201cmistake\u201d; PM Tusk calls it a provocation."),
    ]
    bx, by = 40, brief_y + 30
    bw = 458
    for i, (lead, rest) in enumerate(items):
        x = bx + (i % 2) * (bw + 28)
        yy = by + (i // 2) * 36
        # Rich wrap: lead words bold, rest regular, max 2 lines.
        tokens = [(w, True) for w in lead.split()] + \
                 [(w, False) for w in rest.split()]
        lines, cur, cur_w = [], [], 0
        for word, bold in tokens:
            fnt = brief_b if bold else brief
            ww = d.textlength(word + " ", font=fnt)
            if cur and cur_w + ww > bw - 16:
                lines.append(cur)
                cur, cur_w = [], 0
            cur.append((word, bold))
            cur_w += ww
        if cur:
            lines.append(cur)
        for li, line in enumerate(lines[:2]):
            xx = x + 16
            d.text((x, yy + li * 17), "▪", font=brief,
                   fill=(247, 242, 232))
            for word, bold in line:
                fnt = brief_b if bold else brief
                d.text((xx, yy + li * 17), word + " ", font=fnt,
                       fill=(247, 242, 232))
                xx += d.textlength(word + " ", font=fnt)

    # ---- Footer -----------------------------------------------------------
    foot = font(SANS, 11)
    d.text((36, 992),
           "Sources: One Turn News · The Augerton Digest · AP · Reuters · BBC · NPR.  "
           "Photo panels are AI-generated illustrations.",
           font=foot, fill=MUTED)
    d.text((36, 1006), "The Daily Meridian — Sunday 22 November 2026",
           font=foot, fill=MUTED)

    out = HERE / "entry.png"
    canvas.save(out, format="PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
