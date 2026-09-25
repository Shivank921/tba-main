#!/usr/bin/env python3
"""Generate frontend/public/og-image.png — the 1200x630 social share card.

WhatsApp/Facebook/iMessage don't render SVG og:images, so this raster
version carries the TBA branding. Regenerate with:

    python3 scripts/generate_og_png.py
"""

import glob
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (24, 14, 10)        # deep maroon-black
CREAM = (247, 238, 219)
GOLD = (212, 166, 74)
DIM = (206, 190, 164)


def find_font(pattern):
    roots = ["/usr/share/fonts", os.path.expanduser("~/.local/lib/python3*/site-packages/matplotlib/mpl-data/fonts/ttf")]
    for root in roots:
        hits = glob.glob(os.path.join(root, "**", pattern), recursive=True)
        if hits:
            return hits[0]
    return None


def font(pattern, size):
    path = find_font(pattern)
    if path:
        return ImageFont.truetype(path, size)
    print(f"WARNING: font {pattern} not found, using default", file=sys.stderr)
    return ImageFont.load_default(size)


def spaced_text(d, cx, y, text, f, fill, spacing):
    widths = [d.textlength(ch, font=f) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=f, fill=fill)
        x += w + spacing
    return total


def emblem(d, cx, cy, R):
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=GOLD, width=5)
    r2 = R - 20
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=GOLD, width=2)

    def tri(scale, width):
        rc = R * scale
        pts = [
            (cx, cy - rc),
            (cx - rc * math.sin(math.radians(60)), cy + rc * math.cos(math.radians(60))),
            (cx + rc * math.sin(math.radians(60)), cy + rc * math.cos(math.radians(60))),
        ]
        d.polygon(pts, outline=GOLD, width=width)

    tri(0.74, 4)
    tri(0.56, 2)

    f_tba = font("DejaVuSerif-Bold.ttf", 34)
    bbox = d.textbbox((0, 0), "TBA", font=f_tba)
    d.text((cx - (bbox[2] - bbox[0]) / 2, cy + 6 - (bbox[3] - bbox[1]) / 2), "TBA",
           font=f_tba, fill=CREAM)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # decorative gold rules top and bottom
    for y in (46, H - 46):
        d.line([(W * 0.28, y), (W * 0.72, y)], fill=GOLD, width=2)

    cx = W // 2
    emblem(d, cx, 165, 110)

    f_kicker = font("DejaVuSerif-Bold.ttf", 32)
    f_title = font("DejaVuSerif-Bold.ttf", 52)
    f_sub = font("DejaVuSans.ttf", 26)
    f_url = font("DejaVuSans.ttf", 25)

    y = 306
    spaced_text(d, cx, y, "THE BENGALI ASSOCIATION", f_kicker, GOLD, spacing=8)
    y += 66
    title = "Durga Puja · Culture · Community"
    d.text((cx - d.textlength(title, font=f_title) / 2, y), title, font=f_title, fill=CREAM)
    y += 84
    sub1 = "Celebrating, preserving, and sharing Bengali heritage"
    d.text((cx - d.textlength(sub1, font=f_sub) / 2, y), sub1, font=f_sub, fill=DIM)
    y += 38
    sub2 = "in Coimbatore — Peace · Prayer · Service since 2002."
    d.text((cx - d.textlength(sub2, font=f_sub) / 2, y), sub2, font=f_sub, fill=DIM)

    # url chip
    url = "thebengaliassociation.vercel.app"
    uw = d.textlength(url, font=f_url)
    y0 = H - 122
    d.rounded_rectangle([cx - uw / 2 - 28, y0, cx + uw / 2 + 28, y0 + 56], radius=28, outline=GOLD, width=2)
    d.text((cx - uw / 2, y0 + 13), url, font=f_url, fill=GOLD)

    # overflow guard: nothing may paint outside the canvas
    assert 0 < cx - d.textlength(title, font=f_title) / 2, "title overflows left edge"

    out = os.path.join(os.path.dirname(__file__), "..", "public", "og-image.png")
    img.save(out, optimize=True)
    print(f"wrote {os.path.abspath(out)} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
