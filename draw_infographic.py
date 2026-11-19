#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news infographic (1024x1024 PNG).

Written from scratch for make.fun news-image-20261119. Uses Pillow only
at build time; the submitted main.py is standard-library only.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
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


def draw_icon(draw, kind, cx, cy, color):
    """Small hand-drawn geometric icon centred at (cx, cy)."""
    if kind == "summit":  # three flags / three leaders
        for i, dx in enumerate((-26, 0, 26)):
            draw.line([(cx + dx, cy + 18), (cx + dx, cy - 18)], fill=color, width=4)
            draw.polygon([(cx + dx, cy - 18), (cx + dx + 18, cy - 12),
                          (cx + dx, cy - 6)], fill=color)
    elif kind == "shield":  # shield with a star
        draw.polygon([(cx, cy - 24), (cx + 22, cy - 14), (cx + 20, cy + 12),
                      (cx, cy + 26), (cx - 20, cy + 12), (cx - 22, cy - 14)],
                     outline=color, width=4)
        draw.ellipse([cx - 6, cy - 8, cx + 6, cy + 4], fill=color)
    elif kind == "storm":  # cyclone spiral
        for r in (8, 15, 22):
            draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
                     fill=color, width=4)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=color)
    elif kind == "chart":  # rising bars
        for i, h in enumerate((14, 24, 34)):
            x0 = cx - 26 + i * 18
            draw.rectangle([x0, cy + 18 - h, x0 + 12, cy + 18], fill=color)
        draw.line([(cx - 30, cy - 20), (cx + 30, cy - 26)], fill=color, width=4)
    elif kind == "pound":  # coin with a pound sign
        draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=color, width=4)
        draw.text((cx, cy), "\u00a3", font=font(BOLD, 34), fill=color, anchor="mm")
    elif kind == "car":  # driverless car, no driver
        draw.rounded_rectangle([cx - 30, cy - 6, cx + 30, cy + 12], radius=8,
                               outline=color, width=4)
        draw.polygon([(cx - 18, cy - 6), (cx - 10, cy - 20), (cx + 12, cy - 20),
                      (cx + 20, cy - 6)], outline=color, width=4)
        draw.ellipse([cx - 22, cy + 8, cx - 10, cy + 20], fill=color)
        draw.ellipse([cx + 10, cy + 8, cx + 22, cy + 20], fill=color)
        draw.line([(cx - 34, cy + 24), (cx + 34, cy + 24)], fill=color, width=3)


CARDS = [
    dict(tag="DIPLOMACY  \u00b7  SHENZHEN", accent="#1d4e89", icon="summit",
         title="Trump, Putin and Xi meet at APEC",
         body="Leaders gather in Shenzhen for APEC. Trump and Putin are to meet on the sidelines, with a three-way session with Xi planned.",
         source="Reuters"),
    dict(tag="EUROPE  \u00b7  UKRAINE", accent="#7a3b12", icon="shield",
         title="Allies rally for Kyiv in Berlin",
         body="European leaders meet in Berlin in a show of support for Ukraine. US envoys Witkoff and Kushner also attend.",
         source="Reuters"),
    dict(tag="WEATHER  \u00b7  INDIA", accent="#0e6b6b", icon="storm",
         title="Cyclone Akvan nears India's coast",
         body="Red alerts for heavy rain on 19\u201320 Nov in Andhra Pradesh and Odisha. Schools shut; landfall expected around 20 Nov.",
         source="The Hindu / IMD"),
    dict(tag="MARKETS  \u00b7  AI", accent="#5b2d8e", icon="chart",
         title="Anthropic lists on Nasdaq today",
         body="The Claude maker priced its IPO at $83 a share, above its target range. Shares start trading today as ANT, valued at about $1.4 trillion.",
         source="Reuters"),
    dict(tag="ECONOMY  \u00b7  UK", accent="#8a6d00", icon="pound",
         title="UK inflation at 3.6%; bills set to jump",
         body="Prices rose 3.6% in the year to October, a one-year high, driven by fuel. Energy bills may rise by about \u00a3443 a year.",
         source="BBC News"),
    dict(tag="TECH  \u00b7  USA", accent="#9e2b25", icon="car",
         title="Waymo halts freeway robotaxis",
         body="Driverless taxis are pulled from all US freeways after California cited a safety risk. City-street rides continue.",
         source="BBC News"),
]


def main():
    img = Image.new("RGB", (W, H), "#f6f1e7")
    d = ImageDraw.Draw(img)

    # ---- header band ----
    d.rectangle([0, 0, W, 148], fill="#14263f")
    d.rectangle([0, 148, W, 154], fill="#d9a441")
    d.text((48, 26), "THE WORLD IN ONE DAY", font=font(BOLD, 40), fill="#ffffff")
    d.text((48, 78), "Thursday 19 November 2026",
           font=font(BOLD, 30), fill="#f2c14e")
    d.text((48, 116), "Six stories shaping the day \u2014 from Shenzhen to Berlin",
           font=font(REG, 20), fill="#cfd8e6")
    # small globe mark, top right
    gx, gy = 936, 74
    d.ellipse([gx - 38, gy - 38, gx + 38, gy + 38], outline="#f2c14e", width=4)
    d.ellipse([gx - 16, gy - 38, gx + 16, gy + 38], outline="#f2c14e", width=3)
    d.line([(gx - 38, gy), (gx + 38, gy)], fill="#f2c14e", width=3)
    d.line([(gx - 30, gy - 22), (gx + 30, gy - 22)], fill="#f2c14e", width=2)
    d.line([(gx - 30, gy + 22), (gx + 30, gy + 22)], fill="#f2c14e", width=2)

    # ---- story cards: 2 columns x 3 rows ----
    margin, gap = 28, 20
    cw = (W - 2 * margin - gap) // 2
    ch = 238
    top0 = 178
    title_f = font(BOLD, 25)
    body_f = font(REG, 18)
    tag_f = font(BOLD, 14)
    src_f = font(REG, 14)

    for i, card in enumerate(CARDS):
        col, row = i % 2, i // 2
        x0 = margin + col * (cw + gap)
        y0 = top0 + row * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill="#ffffff",
                            outline="#d8cfba", width=2)
        d.rectangle([x0, y0, x1, y0 + 6], fill=card["accent"])
        # tag + icon row
        d.text((x0 + 18, y0 + 20), card["tag"], font=tag_f, fill=card["accent"])
        draw_icon(d, card["icon"], x1 - 52, y0 + 52, card["accent"])
        # title (max 2 lines, kept clear of the icon on the right)
        tlines = wrap(d, card["title"], title_f, cw - 130)
        ty = y0 + 52
        for ln in tlines[:2]:
            d.text((x0 + 18, ty), ln, font=title_f, fill="#14263f")
            ty += 30
        # body (max 3 lines)
        blines = wrap(d, card["body"], body_f, cw - 36)
        by = ty + 8
        for ln in blines[:3]:
            d.text((x0 + 18, by), ln, font=body_f, fill="#33302a")
            by += 24
        # source line
        d.text((x0 + 18, y1 - 30), "Source: " + card["source"],
               font=src_f, fill="#7a7264")

    # ---- footer ----
    fy = top0 + 3 * ch + 2 * gap + 14
    d.line([(margin, fy), (W - margin, fy)], fill="#b9ad93", width=2)
    d.text((margin, fy + 12),
           "Compiled 19 November 2026 from Reuters, BBC News, The Hindu and the India Meteorological Department.",
           font=font(REG, 14), fill="#5c5546")
    d.text((margin, fy + 36),
           "Figures as reported; market values are approximate. Some stories were first reported on 18 Nov.",
           font=font(REG, 14), fill="#5c5546")

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
