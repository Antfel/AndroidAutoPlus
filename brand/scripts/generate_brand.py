#!/usr/bin/env python3
"""
THE NAIL HOUSE — Brand Asset Generator
Luxury Purple & Gold identity system
"""

from __future__ import annotations

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color, HexColor

ROOT = Path(__file__).resolve().parents[1]
FONTS = Path("/tmp/fonts")
OUT = ROOT

# Brand palette
PURPLE = (53, 32, 68)          # #352044
GOLD = (197, 161, 91)          # #C5A15B
LILA = (155, 120, 185)         # #9B78B9
LAVENDER = (217, 196, 236)     # #D9C4EC
PURPLE_BLACK = (26, 15, 36)    # #1A0F24
PEARL = (247, 241, 248)        # #F7F1F8
GOLD_LIGHT = (232, 210, 150)
GOLD_DARK = (148, 112, 48)

HEX = {
    "purple": "#352044",
    "gold": "#C5A15B",
    "lila": "#9B78B9",
    "lavender": "#D9C4EC",
    "purple_black": "#1A0F24",
    "pearl": "#F7F1F8",
}


def ensure_dirs():
    for p in [
        OUT / "logos/logo-primary",
        OUT / "logos/logo-secondary",
        OUT / "logos/logo-horizontal",
        OUT / "logos/logo-monogram",
        OUT / "logos/logo-monochrome",
        OUT / "colors",
        OUT / "typography",
        OUT / "social-media/profile",
        OUT / "social-media/highlights",
        OUT / "social-media/templates",
        OUT / "business-cards",
        OUT / "appointments",
        OUT / "price-list",
        OUT / "packaging",
        OUT / "mockups",
        OUT / "brand-guidelines",
    ]:
        p.mkdir(parents=True, exist_ok=True)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    mapping = {
        "playfair": "PlayfairDisplay-Regular.ttf",
        "playfair-bold": "PlayfairDisplay-Bold.ttf",
        "playfair-italic": "PlayfairDisplay-Italic.ttf",
        "montserrat": "Montserrat-Regular.ttf",
        "montserrat-light": "Montserrat-Light.ttf",
        "montserrat-medium": "Montserrat-Medium.ttf",
    }
    path = FONTS / mapping[name]
    return ImageFont.truetype(str(path), size)


def register_pdf_fonts():
    pdfmetrics.registerFont(TTFont("Playfair", str(FONTS / "PlayfairDisplay-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("PlayfairBold", str(FONTS / "PlayfairDisplay-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("PlayfairItalic", str(FONTS / "PlayfairDisplay-Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Montserrat", str(FONTS / "Montserrat-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("MontserratLight", str(FONTS / "Montserrat-Light.ttf")))
    pdfmetrics.registerFont(TTFont("MontserratMedium", str(FONTS / "Montserrat-Medium.ttf")))


def metallic_gold_color(t: float = 0.5) -> tuple[int, int, int]:
    """Interpolate champagne gold for metallic feel."""
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        u = t * 2
        return tuple(int(GOLD_DARK[i] + (GOLD[i] - GOLD_DARK[i]) * u) for i in range(3))
    u = (t - 0.5) * 2
    return tuple(int(GOLD[i] + (GOLD_LIGHT[i] - GOLD[i]) * u) for i in range(3))


def draw_oval(draw: ImageDraw.ImageDraw, bbox, color, width: int):
    draw.ellipse(bbox, outline=color, width=width)


def draw_monogram(
    base: Image.Image,
    cx: int,
    cy: int,
    oval_w: int,
    oval_h: int,
    letter_size: int,
    gold=GOLD,
    with_shadow: bool = True,
    stroke_scale: float = 1.0,
):
    """Draw TH monogram inside oval — core brand mark."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # Soft shadow under oval
    if with_shadow:
        shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.ellipse(
            [cx - oval_w // 2 + 4, cy - oval_h // 2 + 6, cx + oval_w // 2 + 4, cy + oval_h // 2 + 6],
            outline=(0, 0, 0, 70),
            width=max(2, int(oval_w * 0.012)),
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(6))
        base.alpha_composite(shadow)

    stroke = max(2, int(oval_w * 0.014 * stroke_scale))
    # Outer thin oval
    d.ellipse(
        [cx - oval_w // 2, cy - oval_h // 2, cx + oval_w // 2, cy + oval_h // 2],
        outline=gold + (255,),
        width=stroke,
    )
    # Inner hairline for depth
    inset = max(4, int(oval_w * 0.028))
    d.ellipse(
        [
            cx - oval_w // 2 + inset,
            cy - oval_h // 2 + inset,
            cx + oval_w // 2 - inset,
            cy + oval_h // 2 - inset,
        ],
        outline=gold + (90,),
        width=max(1, stroke // 3),
    )

    f_t = font("playfair-bold", letter_size)
    f_h = font("playfair-bold", int(letter_size * 0.92))

    # Letter shadow for embossed feel
    if with_shadow:
        ls = Image.new("RGBA", base.size, (0, 0, 0, 0))
        lsd = ImageDraw.Draw(ls)
        # T slightly higher
        t_bbox = lsd.textbbox((0, 0), "T", font=f_t)
        tw, th = t_bbox[2] - t_bbox[0], t_bbox[3] - t_bbox[1]
        tx, ty = cx - tw // 2 - int(letter_size * 0.02), cy - int(letter_size * 0.62)
        lsd.text((tx + 3, ty + 4), "T", font=f_t, fill=(0, 0, 0, 80))
        # H lower overlapping
        h_bbox = lsd.textbbox((0, 0), "H", font=f_h)
        hw, hh = h_bbox[2] - h_bbox[0], h_bbox[3] - h_bbox[1]
        hx, hy = cx - hw // 2 + int(letter_size * 0.02), cy - int(letter_size * 0.28)
        lsd.text((hx + 3, hy + 4), "H", font=f_h, fill=(0, 0, 0, 80))
        ls = ls.filter(ImageFilter.GaussianBlur(3))
        base.alpha_composite(ls)

    # Draw H first (behind), then T on top — interlocking illusion
    h_bbox = d.textbbox((0, 0), "H", font=f_h)
    hw = h_bbox[2] - h_bbox[0]
    hx = cx - hw // 2 + int(letter_size * 0.02)
    hy = cy - int(letter_size * 0.28)
    d.text((hx, hy), "H", font=f_h, fill=gold + (255,))

    t_bbox = d.textbbox((0, 0), "T", font=f_t)
    tw = t_bbox[2] - t_bbox[0]
    tx = cx - tw // 2 - int(letter_size * 0.02)
    ty = cy - int(letter_size * 0.62)
    d.text((tx, ty), "T", font=f_t, fill=gold + (255,))

    # Central flourish — curved stroke crossing the H bar (original detail)
    flourish = Image.new("RGBA", base.size, (0, 0, 0, 0))
    fd = ImageDraw.Draw(flourish)
    # Arc from mid T stem sweeping right across H
    fw = max(2, int(letter_size * 0.045))
    points = []
    for i in range(40):
        a = i / 39
        x = cx - int(letter_size * 0.05) + int(letter_size * 0.55 * a)
        y = cy - int(letter_size * 0.15) + int(letter_size * 0.08 * math.sin(a * math.pi)) + int(letter_size * 0.12 * a)
        points.append((x, y))
    if len(points) > 1:
        fd.line(points, fill=gold + (255,), width=fw, joint="curve")
    # Soft highlight on flourish tip
    tip = points[-1]
    fd.ellipse([tip[0] - fw, tip[1] - fw, tip[0] + fw, tip[1] + fw], fill=GOLD_LIGHT + (200,))

    base.alpha_composite(layer)
    base.alpha_composite(flourish)


def save_rgba(img: Image.Image, path: Path, bg=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() in {".jpg", ".jpeg"}:
        if bg is None:
            bg = PURPLE
        out = Image.new("RGB", img.size, bg)
        if img.mode == "RGBA":
            out.paste(img, mask=img.split()[3])
        else:
            out.paste(img)
        out.save(path, quality=95)
    else:
        img.save(path)


def make_monogram_svg(path: Path, fill="#C5A15B", bg=None, size=512):
    """Editable SVG monogram — oval + serif TH."""
    bg_rect = ""
    if bg:
        bg_rect = f'<rect width="{size}" height="{size}" fill="{bg}"/>'
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  <defs>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E8D296"/>
      <stop offset="45%" stop-color="#C5A15B"/>
      <stop offset="100%" stop-color="#947030"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#000000" flood-opacity="0.35"/>
    </filter>
  </defs>
  {bg_rect}
  <g filter="url(#softShadow)">
    <ellipse cx="{size/2}" cy="{size/2}" rx="{size*0.32}" ry="{size*0.40}"
             fill="none" stroke="url(#goldGrad)" stroke-width="{size*0.012}"/>
    <ellipse cx="{size/2}" cy="{size/2}" rx="{size*0.295}" ry="{size*0.375}"
             fill="none" stroke="{fill}" stroke-opacity="0.35" stroke-width="{size*0.004}"/>
    <text x="{size/2}" y="{size*0.42}" text-anchor="middle"
          font-family="Playfair Display, Georgia, serif" font-weight="700"
          font-size="{size*0.38}" fill="url(#goldGrad)">T</text>
    <text x="{size/2}" y="{size*0.68}" text-anchor="middle"
          font-family="Playfair Display, Georgia, serif" font-weight="700"
          font-size="{size*0.34}" fill="url(#goldGrad)">H</text>
    <path d="M {size*0.45} {size*0.48} Q {size*0.55} {size*0.52} {size*0.68} {size*0.58}"
          fill="none" stroke="url(#goldGrad)" stroke-width="{size*0.018}" stroke-linecap="round"/>
  </g>
</svg>
'''
    path.write_text(svg, encoding="utf-8")


def logo_monogram():
    size = 1024
    # With purple background JPG
    img = Image.new("RGBA", (size, size), PURPLE + (255,))
    draw_monogram(img, size // 2, size // 2, int(size * 0.62), int(size * 0.78), int(size * 0.36))
    save_rgba(img, OUT / "logos/logo-monogram/logo-monogram.jpg", PURPLE)
    save_rgba(img, OUT / "logos/logo-monogram/logo-monogram.png")

    # Transparent PNG
    img_t = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_monogram(img_t, size // 2, size // 2, int(size * 0.62), int(size * 0.78), int(size * 0.36))
    save_rgba(img_t, OUT / "logos/logo-monogram/logo-monogram-transparent.png")

    make_monogram_svg(OUT / "logos/logo-monogram/logo-monogram.svg", bg="#352044")
    make_monogram_svg(OUT / "logos/logo-monogram/logo-monogram-transparent.svg", bg=None)

    # Favicon sizes
    for s in (512, 256, 128, 64, 32):
        fav = img.resize((s, s), Image.Resampling.LANCZOS)
        save_rgba(fav, OUT / f"logos/logo-monogram/favicon-{s}.png")
        save_rgba(fav, OUT / f"social-media/profile/profile-{s}.png")


def logo_primary():
    """Centered: monogram + THE NAIL HOUSE + NAIL STUDIO on purple."""
    w, h = 1200, 1400
    img = Image.new("RGBA", (w, h), PURPLE + (255,))
    draw_monogram(img, w // 2, int(h * 0.38), 420, 540, 250)

    d = ImageDraw.Draw(img)
    f_name = font("playfair", 64)
    f_desc = font("montserrat-light", 22)

    name = "THE NAIL HOUSE"
    nb = d.textbbox((0, 0), name, font=f_name)
    nw = nb[2] - nb[0]
    d.text(((w - nw) // 2, int(h * 0.68)), name, font=f_name, fill=GOLD + (255,))

    # Thin gold divider
    mid_y = int(h * 0.75)
    d.line([(w // 2 - 80, mid_y), (w // 2 + 80, mid_y)], fill=GOLD + (180,), width=1)

    desc = "NAIL STUDIO"
    db = d.textbbox((0, 0), desc, font=f_desc)
    dw = db[2] - db[0]
    # Letter-spacing simulation
    spacing = 8
    total = sum(d.textbbox((0, 0), ch, font=f_desc)[2] for ch in desc) + spacing * (len(desc) - 1)
    x = (w - total) // 2
    for ch in desc:
        d.text((x, int(h * 0.77)), ch, font=f_desc, fill=LAVENDER + (230,))
        x += d.textbbox((0, 0), ch, font=f_desc)[2] + spacing

    save_rgba(img, OUT / "logos/logo-primary/logo-primary.png")
    save_rgba(img, OUT / "logos/logo-primary/logo-primary.jpg", PURPLE)

    # Transparent version
    img_t = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_monogram(img_t, w // 2, int(h * 0.38), 420, 540, 250)
    d = ImageDraw.Draw(img_t)
    d.text(((w - nw) // 2, int(h * 0.68)), name, font=f_name, fill=GOLD + (255,))
    d.line([(w // 2 - 80, mid_y), (w // 2 + 80, mid_y)], fill=GOLD + (180,), width=1)
    x = (w - total) // 2
    for ch in desc:
        d.text((x, int(h * 0.77)), ch, font=f_desc, fill=GOLD + (230,))
        x += d.textbbox((0, 0), ch, font=f_desc)[2] + spacing
    save_rgba(img_t, OUT / "logos/logo-primary/logo-primary-transparent.png")

    # SVG
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1400" viewBox="0 0 1200 1400">
  <rect width="1200" height="1400" fill="#352044"/>
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E8D296"/><stop offset="50%" stop-color="#C5A15B"/><stop offset="100%" stop-color="#947030"/>
    </linearGradient>
  </defs>
  <ellipse cx="600" cy="530" rx="210" ry="270" fill="none" stroke="url(#g)" stroke-width="8"/>
  <text x="600" y="480" text-anchor="middle" font-family="Playfair Display, Georgia, serif" font-weight="700" font-size="220" fill="url(#g)">T</text>
  <text x="600" y="640" text-anchor="middle" font-family="Playfair Display, Georgia, serif" font-weight="700" font-size="200" fill="url(#g)">H</text>
  <path d="M 540 560 Q 620 590 720 640" fill="none" stroke="url(#g)" stroke-width="10" stroke-linecap="round"/>
  <text x="600" y="980" text-anchor="middle" font-family="Playfair Display, Georgia, serif" font-size="64" fill="#C5A15B" letter-spacing="6">THE NAIL HOUSE</text>
  <line x1="520" y1="1040" x2="680" y2="1040" stroke="#C5A15B" stroke-opacity="0.7" stroke-width="1"/>
  <text x="600" y="1090" text-anchor="middle" font-family="Montserrat, Helvetica, sans-serif" font-weight="300" font-size="22" fill="#D9C4EC" letter-spacing="8">NAIL STUDIO</text>
</svg>
'''
    (OUT / "logos/logo-primary/logo-primary.svg").write_text(svg, encoding="utf-8")


def logo_horizontal():
    w, h = 1600, 500
    img = Image.new("RGBA", (w, h), PURPLE + (255,))
    draw_monogram(img, 220, h // 2, 280, 360, 170)

    d = ImageDraw.Draw(img)
    f_name = font("playfair", 58)
    f_desc = font("montserrat-light", 20)
    name = "THE NAIL HOUSE"
    d.text((420, h // 2 - 55), name, font=f_name, fill=GOLD + (255,))
    d.line([(420, h // 2 + 10), (420 + 380, h // 2 + 10)], fill=GOLD + (160,), width=1)
    desc = "NAIL STUDIO"
    spacing = 7
    x = 420
    for ch in desc:
        d.text((x, h // 2 + 25), ch, font=f_desc, fill=LAVENDER + (230,))
        x += d.textbbox((0, 0), ch, font=f_desc)[2] + spacing

    save_rgba(img, OUT / "logos/logo-horizontal/logo-horizontal.png")
    save_rgba(img, OUT / "logos/logo-horizontal/logo-horizontal.jpg", PURPLE)

    img_t = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_monogram(img_t, 220, h // 2, 280, 360, 170)
    d = ImageDraw.Draw(img_t)
    d.text((420, h // 2 - 55), name, font=f_name, fill=GOLD + (255,))
    d.line([(420, h // 2 + 10), (420 + 380, h // 2 + 10)], fill=GOLD + (160,), width=1)
    x = 420
    for ch in desc:
        d.text((x, h // 2 + 25), ch, font=f_desc, fill=GOLD + (230,))
        x += d.textbbox((0, 0), ch, font=f_desc)[2] + spacing
    save_rgba(img_t, OUT / "logos/logo-horizontal/logo-horizontal-transparent.png")

    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="500" viewBox="0 0 1600 500">
  <rect width="1600" height="500" fill="#352044"/>
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E8D296"/><stop offset="50%" stop-color="#C5A15B"/><stop offset="100%" stop-color="#947030"/>
    </linearGradient>
  </defs>
  <ellipse cx="220" cy="250" rx="140" ry="180" fill="none" stroke="url(#g)" stroke-width="6"/>
  <text x="220" y="220" text-anchor="middle" font-family="Playfair Display, Georgia, serif" font-weight="700" font-size="150" fill="url(#g)">T</text>
  <text x="220" y="320" text-anchor="middle" font-family="Playfair Display, Georgia, serif" font-weight="700" font-size="140" fill="url(#g)">H</text>
  <path d="M 180 240 Q 230 260 290 290" fill="none" stroke="url(#g)" stroke-width="7" stroke-linecap="round"/>
  <text x="420" y="230" font-family="Playfair Display, Georgia, serif" font-size="58" fill="#C5A15B">THE NAIL HOUSE</text>
  <line x1="420" y1="260" x2="800" y2="260" stroke="#C5A15B" stroke-opacity="0.6" stroke-width="1"/>
  <text x="420" y="300" font-family="Montserrat, Helvetica, sans-serif" font-weight="300" font-size="20" fill="#D9C4EC" letter-spacing="7">NAIL STUDIO</text>
</svg>
'''
    (OUT / "logos/logo-horizontal/logo-horizontal.svg").write_text(svg, encoding="utf-8")


def logo_secondary():
    """Stacked wordmark without oval for secondary uses."""
    w, h = 1000, 400
    img = Image.new("RGBA", (w, h), PURPLE + (255,))
    d = ImageDraw.Draw(img)
    f_name = font("playfair", 56)
    f_desc = font("montserrat-light", 18)
    name = "THE NAIL HOUSE"
    nb = d.textbbox((0, 0), name, font=f_name)
    nw = nb[2] - nb[0]
    d.text(((w - nw) // 2, 140), name, font=f_name, fill=GOLD + (255,))
    d.line([(w // 2 - 60, 220), (w // 2 + 60, 220)], fill=GOLD + (180,), width=1)
    desc = "NAIL STUDIO"
    spacing = 6
    total = sum(d.textbbox((0, 0), ch, font=f_desc)[2] for ch in desc) + spacing * (len(desc) - 1)
    x = (w - total) // 2
    for ch in desc:
        d.text((x, 245), ch, font=f_desc, fill=LAVENDER + (230,))
        x += d.textbbox((0, 0), ch, font=f_desc)[2] + spacing
    save_rgba(img, OUT / "logos/logo-secondary/logo-wordmark.png")
    save_rgba(img, OUT / "logos/logo-secondary/logo-wordmark.jpg", PURPLE)

    # Compact: monogram + wordmark small
    img2 = Image.new("RGBA", (800, 900), PURPLE + (255,))
    draw_monogram(img2, 400, 320, 300, 380, 180)
    d2 = ImageDraw.Draw(img2)
    f2 = font("playfair", 36)
    nb2 = d2.textbbox((0, 0), name, font=f2)
    d2.text(((800 - (nb2[2] - nb2[0])) // 2, 580), name, font=f2, fill=GOLD + (255,))
    save_rgba(img2, OUT / "logos/logo-secondary/logo-compact.png")


def logo_monochrome():
    size = 1024
    # Gold on transparent
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_monogram(img, size // 2, size // 2, int(size * 0.62), int(size * 0.78), int(size * 0.36), gold=GOLD, with_shadow=False)
    save_rgba(img, OUT / "logos/logo-monochrome/logo-gold.png")

    # Purple monochrome
    img_p = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_monogram(img_p, size // 2, size // 2, int(size * 0.62), int(size * 0.78), int(size * 0.36), gold=PURPLE, with_shadow=False)
    save_rgba(img_p, OUT / "logos/logo-monochrome/logo-purple.png")

    # White for dark embroidery
    img_w = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_monogram(img_w, size // 2, size // 2, int(size * 0.62), int(size * 0.78), int(size * 0.36), gold=(247, 241, 248), with_shadow=False)
    save_rgba(img_w, OUT / "logos/logo-monochrome/logo-pearl.png")

    # Gold on purple black
    img_d = Image.new("RGBA", (size, size), PURPLE_BLACK + (255,))
    draw_monogram(img_d, size // 2, size // 2, int(size * 0.62), int(size * 0.78), int(size * 0.36), gold=GOLD, with_shadow=False)
    save_rgba(img_d, OUT / "logos/logo-monochrome/logo-on-black.jpg", PURPLE_BLACK)

    make_monogram_svg(OUT / "logos/logo-monochrome/logo-gold.svg", fill="#C5A15B")
    make_monogram_svg(OUT / "logos/logo-monochrome/logo-purple.svg", fill="#352044")


def colors_sheet():
    w, h = 1400, 900
    img = Image.new("RGBA", (w, h), PEARL + (255,))
    d = ImageDraw.Draw(img)
    title_f = font("playfair", 42)
    label_f = font("montserrat-medium", 18)
    hex_f = font("montserrat-light", 16)
    sub_f = font("montserrat-light", 14)

    d.text((80, 50), "THE NAIL HOUSE", font=font("playfair", 28), fill=PURPLE + (255,))
    d.text((80, 100), "Paleta de color", font=title_f, fill=PURPLE + (255,))
    d.text((80, 160), "Luxury Purple & Gold", font=sub_f, fill=LILA + (255,))

    swatches = [
        ("Morado profundo", HEX["purple"], PURPLE, "Principal de marca"),
        ("Dorado champagne", HEX["gold"], GOLD, "Logotipo y premium"),
        ("Lila", HEX["lila"], LILA, "Acentos secundarios"),
        ("Lavanda", HEX["lavender"], LAVENDER, "Fondos suaves"),
        ("Negro púrpura", HEX["purple_black"], PURPLE_BLACK, "Contraste"),
        ("Blanco perlado", HEX["pearl"], PEARL, "Documentos"),
    ]

    x0, y0 = 80, 220
    card_w, card_h = 400, 280
    gap = 30
    for i, (name, hx, rgb, use) in enumerate(swatches):
        col, row = i % 3, i // 3
        x = x0 + col * (card_w + gap)
        y = y0 + row * (card_h + gap)
        # Color block
        d.rounded_rectangle([x, y, x + card_w, y + 160], radius=8, fill=rgb + (255,))
        # Border for light swatches
        if name in ("Lavanda", "Blanco perlado"):
            d.rounded_rectangle([x, y, x + card_w, y + 160], radius=8, outline=LILA + (120,), width=1)
        text_c = PURPLE if name in ("Lavanda", "Blanco perlado", "Dorado champagne") else PEARL
        if name == "Dorado champagne":
            text_c = PURPLE_BLACK
        d.text((x + 20, y + 180), name, font=label_f, fill=PURPLE + (255,))
        d.text((x + 20, y + 210), hx.upper(), font=hex_f, fill=LILA + (255,))
        d.text((x + 20, y + 240), use, font=sub_f, fill=(100, 80, 110, 255))

    save_rgba(img, OUT / "colors/palette.png")
    save_rgba(img, OUT / "colors/palette.jpg", PEARL)

    css = f"""/* THE NAIL HOUSE — Brand Colors */
:root {{
  --tnh-purple: {HEX['purple']};
  --tnh-gold: {HEX['gold']};
  --tnh-lila: {HEX['lila']};
  --tnh-lavender: {HEX['lavender']};
  --tnh-purple-black: {HEX['purple_black']};
  --tnh-pearl: {HEX['pearl']};
}}
"""
    (OUT / "colors/colors.css").write_text(css, encoding="utf-8")
    (OUT / "colors/colors.json").write_text(
        '{\n  "purple": "#352044",\n  "gold": "#C5A15B",\n  "lila": "#9B78B9",\n  "lavender": "#D9C4EC",\n  "purple_black": "#1A0F24",\n  "pearl": "#F7F1F8"\n}\n',
        encoding="utf-8",
    )


def typography_sheet():
    w, h = 1200, 1600
    img = Image.new("RGBA", (w, h), PEARL + (255,))
    d = ImageDraw.Draw(img)
    d.text((80, 60), "THE NAIL HOUSE", font=font("playfair", 24), fill=GOLD)
    d.text((80, 110), "Sistema tipográfico", font=font("playfair", 48), fill=PURPLE)
    d.line([(80, 180), (400, 180)], fill=GOLD, width=1)

    d.text((80, 220), "Principal — Playfair Display", font=font("montserrat-medium", 16), fill=LILA)
    d.text((80, 260), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", font=font("playfair", 28), fill=PURPLE)
    d.text((80, 310), "abcdefghijklmnopqrstuvwxyz", font=font("playfair", 28), fill=PURPLE)
    d.text((80, 360), "0123456789", font=font("playfair", 28), fill=PURPLE)
    d.text((80, 430), "The Nail House", font=font("playfair", 64), fill=PURPLE)
    d.text((80, 520), "Nail Studio Boutique", font=font("playfair-italic", 36), fill=GOLD)

    d.text((80, 620), "Secundaria — Montserrat", font=font("montserrat-medium", 16), fill=LILA)
    d.text((80, 660), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", font=font("montserrat", 22), fill=PURPLE)
    d.text((80, 700), "abcdefghijklmnopqrstuvwxyz", font=font("montserrat", 22), fill=PURPLE)
    d.text((80, 750), "Light · Regular · Medium", font=font("montserrat-light", 20), fill=PURPLE)

    d.text((80, 850), "Jerarquía de uso", font=font("playfair", 32), fill=PURPLE)
    rules = [
        ("H1 / Marca", "Playfair Display Regular — logotipo y titulares"),
        ("H2 / Secciones", "Playfair Display — títulos editoriales"),
        ("Body", "Montserrat Regular — párrafos y UI"),
        ("Caption / Labels", "Montserrat Light — descriptores, tracking amplio"),
        ("CTA", "Montserrat Medium — botones y CTAs"),
    ]
    y = 920
    for title, desc in rules:
        d.text((80, y), title, font=font("montserrat-medium", 18), fill=GOLD)
        d.text((320, y), desc, font=font("montserrat-light", 18), fill=PURPLE)
        y += 50

    d.text((80, 1250), "Alternativas tipográficas", font=font("playfair", 28), fill=PURPLE)
    d.text((80, 1310), "Principal: Cormorant Garamond  ·  Secundaria: Poppins", font=font("montserrat-light", 18), fill=LILA)

    save_rgba(img, OUT / "typography/typography-specimen.png")
    save_rgba(img, OUT / "typography/typography-specimen.jpg", PEARL)

    (OUT / "typography/README.md").write_text(
        """# Tipografía — THE NAIL HOUSE

## Principal
**Playfair Display** (Regular, Bold, Italic)
- Uso: logotipo, titulares, monograma
- Alternativa: Cormorant Garamond

## Secundaria
**Montserrat** (Light, Regular, Medium)
- Uso: cuerpo, UI, descriptores (NAIL STUDIO)
- Alternativa: Poppins

## Reglas
- Descriptor `NAIL STUDIO`: Montserrat Light, tracking amplio (letter-spacing 6–10px)
- Nombre de marca: Playfair Display, tracking moderado
- Nunca mezclar más de dos familias en la misma pieza
""",
        encoding="utf-8",
    )


def business_cards():
    # Front 1050x600 @ 300dpi-ish preview
    w, h = 1050, 600
    front = Image.new("RGBA", (w, h), PURPLE + (255,))
    draw_monogram(front, w // 2, int(h * 0.38), 180, 230, 110)
    d = ImageDraw.Draw(front)
    name = "THE NAIL HOUSE"
    f = font("playfair", 28)
    nb = d.textbbox((0, 0), name, font=f)
    d.text(((w - (nb[2] - nb[0])) // 2, 400), name, font=f, fill=GOLD + (255,))
    d.line([(w // 2 - 50, 445), (w // 2 + 50, 445)], fill=GOLD + (160,), width=1)
    desc = "NAIL STUDIO"
    fd = font("montserrat-light", 12)
    spacing = 4
    total = sum(d.textbbox((0, 0), ch, font=fd)[2] for ch in desc) + spacing * (len(desc) - 1)
    x = (w - total) // 2
    for ch in desc:
        d.text((x, 460), ch, font=fd, fill=LAVENDER + (230,))
        x += d.textbbox((0, 0), ch, font=fd)[2] + spacing
    save_rgba(front, OUT / "business-cards/card-front.png")
    save_rgba(front, OUT / "business-cards/card-front.jpg", PURPLE)

    # Back
    back = Image.new("RGBA", (w, h), PEARL + (255,))
    d = ImageDraw.Draw(back)
    # Small monogram top
    draw_monogram(back, 120, 100, 90, 115, 55, gold=GOLD, with_shadow=False)
    d.text((200, 70), "THE NAIL HOUSE", font=font("playfair", 22), fill=PURPLE)
    d.text((200, 105), "Nail Studio Boutique", font=font("montserrat-light", 14), fill=LILA)
    d.line([(80, 180), (w - 80, 180)], fill=GOLD + (120,), width=1)

    lines = [
        ("Reservas", "+51 000 000 000"),
        ("Instagram", "@thenailhouse"),
        ("Email", "hola@thenailhouse.com"),
        ("Atención", "Con cita previa · A domicilio / Estudio en casa"),
    ]
    y = 220
    for label, value in lines:
        d.text((80, y), label.upper(), font=font("montserrat-medium", 11), fill=GOLD)
        d.text((80, y + 22), value, font=font("montserrat", 16), fill=PURPLE)
        y += 70
    save_rgba(back, OUT / "business-cards/card-back.png")
    save_rgba(back, OUT / "business-cards/card-back.jpg", PEARL)


def appointment_cards():
    w, h = 1050, 600
    img = Image.new("RGBA", (w, h), PEARL + (255,))
    d = ImageDraw.Draw(img)
    # Left purple panel
    d.rectangle([0, 0, 320, h], fill=PURPLE + (255,))
    draw_monogram(img, 160, 220, 160, 200, 95)
    d2 = ImageDraw.Draw(img)
    d2.text((55, 380), "THE NAIL", font=font("playfair", 22), fill=GOLD)
    d2.text((55, 410), "HOUSE", font=font("playfair", 22), fill=GOLD)
    d2.text((55, 460), "CITA", font=font("montserrat-light", 14), fill=LAVENDER)

    d2.text((380, 60), "Tu próxima cita", font=font("playfair", 32), fill=PURPLE)
    d2.line([(380, 110), (700, 110)], fill=GOLD, width=1)

    fields = ["Cliente:", "Servicio:", "Fecha:", "Hora:", "Notas:"]
    y = 150
    for field in fields:
        d2.text((380, y), field, font=font("montserrat-medium", 14), fill=GOLD)
        d2.line([(480, y + 18), (980, y + 18)], fill=LILA + (100,), width=1)
        y += 70

    d2.text((380, 540), "Por favor confirma con 24h de antelación", font=font("montserrat-light", 12), fill=LILA)
    save_rgba(img, OUT / "appointments/appointment-card.png")
    save_rgba(img, OUT / "appointments/appointment-card.jpg", PEARL)


def loyalty_card():
    w, h = 1050, 600
    img = Image.new("RGBA", (w, h), PURPLE + (255,))
    draw_monogram(img, 160, 160, 140, 175, 85)
    d = ImageDraw.Draw(img)
    d.text((280, 100), "THE NAIL HOUSE", font=font("playfair", 28), fill=GOLD)
    d.text((280, 145), "Tarjeta de fidelización", font=font("montserrat-light", 16), fill=LAVENDER)
    d.text((80, 280), "Colecciona 8 sellos y recibe un servicio de regalo", font=font("montserrat", 16), fill=PEARL)

    # 8 stamp circles
    for i in range(8):
        x = 100 + i * 110
        y = 380
        d.ellipse([x, y, x + 70, y + 70], outline=GOLD + (200,), width=2)
        d.text((x + 28, y + 22), str(i + 1), font=font("montserrat-light", 16), fill=GOLD + (160,))

    d.text((80, 520), "Nombre: ____________________________", font=font("montserrat-light", 14), fill=LAVENDER)
    save_rgba(img, OUT / "appointments/loyalty-card.png")
    save_rgba(img, OUT / "appointments/loyalty-card.jpg", PURPLE)


def price_list():
    w, h = 1080, 1620
    img = Image.new("RGBA", (w, h), PEARL + (255,))
    d = ImageDraw.Draw(img)
    # Header band
    d.rectangle([0, 0, w, 280], fill=PURPLE + (255,))
    draw_monogram(img, w // 2, 120, 120, 150, 72)
    d = ImageDraw.Draw(img)
    d.text((0, 220), "LISTA DE PRECIOS", font=font("montserrat-light", 14), fill=LAVENDER)
    # Center the title manually
    title = "LISTA DE PRECIOS"
    tb = d.textbbox((0, 0), title, font=font("montserrat-light", 14))
    # letter spacing
    spacing = 6
    total = sum(d.textbbox((0, 0), ch, font=font("montserrat-light", 14))[2] for ch in title) + spacing * (len(title) - 1)
    x = (w - total) // 2
    for ch in title:
        d.text((x, 220), ch, font=font("montserrat-light", 14), fill=LAVENDER)
        x += d.textbbox((0, 0), ch, font=font("montserrat-light", 14))[2] + spacing

    services = [
        ("Manicura clásica", "S/ 45"),
        ("Manicura spa", "S/ 60"),
        ("Semipermanente", "S/ 75"),
        ("Gel / Soft gel", "S/ 90"),
        ("Nail art (por uña)", "desde S/ 8"),
        ("Diseño personalizado", "desde S/ 100"),
        ("Pedicura clásica", "S/ 55"),
        ("Pedicura spa", "S/ 70"),
        ("Retiro de esmalte", "S/ 20"),
        ("Reparación (por uña)", "S/ 15"),
    ]

    y = 340
    for name, price in services:
        d.text((100, y), name, font=font("playfair", 26), fill=PURPLE)
        pb = d.textbbox((0, 0), price, font=font("montserrat-medium", 18))
        d.text((w - 100 - (pb[2] - pb[0]), y + 6), price, font=font("montserrat-medium", 18), fill=GOLD)
        # dotted line
        name_w = d.textbbox((0, 0), name, font=font("playfair", 26))[2]
        for dx in range(name_w + 120, w - 100 - (pb[2] - pb[0]) - 20, 8):
            d.ellipse([dx, y + 18, dx + 2, y + 20], fill=LILA + (100,))
        y += 90

    d.line([(100, h - 180), (w - 100, h - 180)], fill=GOLD + (120,), width=1)
    d.text((100, h - 150), "THE NAIL HOUSE  ·  Nail Studio Boutique", font=font("playfair", 18), fill=PURPLE)
    d.text((100, h - 110), "Precios referenciales. Consulta disponibilidad y promociones.", font=font("montserrat-light", 13), fill=LILA)
    d.text((100, h - 80), "@thenailhouse", font=font("montserrat-medium", 13), fill=GOLD)

    save_rgba(img, OUT / "price-list/price-list.png")
    save_rgba(img, OUT / "price-list/price-list.jpg", PEARL)
    # Instagram version square crop of top+services conceptually - full story size
    story = img.resize((1080, 1620), Image.Resampling.LANCZOS)
    save_rgba(story, OUT / "social-media/templates/post-precios.png")


def social_templates():
    # Profile
    size = 800
    profile = Image.new("RGBA", (size, size), PURPLE + (255,))
    draw_monogram(profile, size // 2, size // 2, 480, 600, 280)
    save_rgba(profile, OUT / "social-media/profile/instagram-profile.png")
    save_rgba(profile, OUT / "social-media/profile/instagram-profile.jpg", PURPLE)

    # Cover / banner 1500x500
    cover = Image.new("RGBA", (1500, 500), PURPLE + (255,))
    draw_monogram(cover, 280, 250, 260, 330, 155)
    d = ImageDraw.Draw(cover)
    d.text((480, 180), "THE NAIL HOUSE", font=font("playfair", 52), fill=GOLD)
    d.line([(480, 255), (860, 255)], fill=GOLD + (160,), width=1)
    desc = "NAIL STUDIO BOUTIQUE"
    fd = font("montserrat-light", 18)
    x = 480
    for ch in desc:
        d.text((x, 280), ch, font=fd, fill=LAVENDER)
        x += d.textbbox((0, 0), ch, font=fd)[2] + 5
    save_rgba(cover, OUT / "social-media/profile/instagram-cover.png")
    save_rgba(cover, OUT / "social-media/profile/instagram-cover.jpg", PURPLE)

    # Highlight covers
    labels = ["Servicios", "Diseños", "Antes &\nDespués", "Precios", "Promos", "Nosotros"]
    for label in labels:
        c = Image.new("RGBA", (540, 540), PURPLE + (255,))
        d = ImageDraw.Draw(c)
        d.ellipse([40, 40, 500, 500], outline=GOLD + (220,), width=3)
        d.ellipse([55, 55, 485, 485], outline=GOLD + (80,), width=1)
        lines = label.split("\n")
        f = font("playfair", 36 if len(lines) == 1 else 30)
        total_h = len(lines) * 44
        y = 270 - total_h // 2
        for line in lines:
            bb = d.textbbox((0, 0), line, font=f)
            d.text(((540 - (bb[2] - bb[0])) // 2, y), line, font=f, fill=GOLD)
            y += 44
        slug = label.replace("\n", "-").replace(" ", "-").replace("&", "y").lower()
        save_rgba(c, OUT / f"social-media/highlights/highlight-{slug}.png")

    # Post templates
    templates = [
        ("post-bienvenida", "Bienvenida", "Un espacio boutique\npara el cuidado de tus uñas"),
        ("post-servicios", "Servicios", "Manicura · Gel · Nail Art\nPedicura · Diseños a medida"),
        ("post-promo", "Promoción", "Primera visita\n10% de descuento"),
        ("post-antes-despues", "Antes & Después", "Transformaciones\ncon firma de marca"),
        ("post-marca", "La marca", "Glamour · Elegancia\nExclusividad"),
    ]
    for slug, title, body in templates:
        p = Image.new("RGBA", (1080, 1350), PURPLE + (255,))
        draw_monogram(p, 540, 280, 200, 250, 120)
        d = ImageDraw.Draw(p)
        d.line([(340, 480), (740, 480)], fill=GOLD + (160,), width=1)
        tb = d.textbbox((0, 0), title.upper(), font=font("montserrat-light", 16))
        # spaced title
        t = title.upper()
        spacing = 8
        total = sum(d.textbbox((0, 0), ch, font=font("montserrat-light", 16))[2] for ch in t) + spacing * (len(t) - 1)
        x = (1080 - total) // 2
        for ch in t:
            d.text((x, 520), ch, font=font("montserrat-light", 16), fill=LAVENDER)
            x += d.textbbox((0, 0), ch, font=font("montserrat-light", 16))[2] + spacing

        y = 620
        for line in body.split("\n"):
            f = font("playfair", 48)
            bb = d.textbbox((0, 0), line, font=f)
            d.text(((1080 - (bb[2] - bb[0])) // 2, y), line, font=f, fill=GOLD)
            y += 70

        d.text((0, 1180), "THE NAIL HOUSE", font=font("playfair", 20), fill=GOLD)
        nb = d.textbbox((0, 0), "THE NAIL HOUSE", font=font("playfair", 20))
        # recenter
        # redraw properly
        save_rgba(p, OUT / f"social-media/templates/{slug}.png")

    # Fix brand name centering on templates - regenerate footer properly
    for slug, title, body in templates:
        p = Image.new("RGBA", (1080, 1350), PURPLE + (255,))
        draw_monogram(p, 540, 280, 200, 250, 120)
        d = ImageDraw.Draw(p)
        d.line([(340, 480), (740, 480)], fill=GOLD + (160,), width=1)
        t = title.upper()
        spacing = 8
        total = sum(d.textbbox((0, 0), ch, font=font("montserrat-light", 16))[2] for ch in t) + spacing * (len(t) - 1)
        x = (1080 - total) // 2
        for ch in t:
            d.text((x, 520), ch, font=font("montserrat-light", 16), fill=LAVENDER)
            x += d.textbbox((0, 0), ch, font=font("montserrat-light", 16))[2] + spacing
        y = 620
        for line in body.split("\n"):
            f = font("playfair", 48)
            bb = d.textbbox((0, 0), line, font=f)
            d.text(((1080 - (bb[2] - bb[0])) // 2, y), line, font=f, fill=GOLD)
            y += 70
        brand = "THE NAIL HOUSE"
        bb = d.textbbox((0, 0), brand, font=font("playfair", 22))
        d.text(((1080 - (bb[2] - bb[0])) // 2, 1180), brand, font=font("playfair", 22), fill=GOLD)
        nail = "NAIL STUDIO"
        spacing = 5
        total = sum(d.textbbox((0, 0), ch, font=font("montserrat-light", 12))[2] for ch in nail) + spacing * (len(nail) - 1)
        x = (1080 - total) // 2
        for ch in nail:
            d.text((x, 1220), ch, font=font("montserrat-light", 12), fill=LAVENDER)
            x += d.textbbox((0, 0), ch, font=font("montserrat-light", 12))[2] + spacing
        save_rgba(p, OUT / f"social-media/templates/{slug}.png")
        save_rgba(p, OUT / f"social-media/templates/{slug}.jpg", PURPLE)


def packaging_and_stickers():
    # Sticker round
    size = 800
    sticker = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(sticker)
    d.ellipse([20, 20, size - 20, size - 20], fill=PURPLE + (255,))
    draw_monogram(sticker, size // 2, size // 2 - 20, 360, 450, 210)
    d = ImageDraw.Draw(sticker)
    brand = "THE NAIL HOUSE"
    bb = d.textbbox((0, 0), brand, font=font("playfair", 22))
    d.text(((size - (bb[2] - bb[0])) // 2, 680), brand, font=font("playfair", 22), fill=GOLD)
    save_rgba(sticker, OUT / "packaging/sticker-round.png")

    # Label rectangular
    label = Image.new("RGBA", (1000, 400), PURPLE + (255,))
    draw_monogram(label, 180, 200, 180, 230, 110)
    d = ImageDraw.Draw(label)
    d.text((340, 130), "THE NAIL HOUSE", font=font("playfair", 36), fill=GOLD)
    d.line([(340, 190), (700, 190)], fill=GOLD + (140,), width=1)
    d.text((340, 220), "Nail Studio Boutique", font=font("montserrat-light", 18), fill=LAVENDER)
    d.text((340, 270), "Hecho con cuidado · Exclusivo para ti", font=font("montserrat", 14), fill=LILA)
    save_rgba(label, OUT / "packaging/label-rectangular.png")
    save_rgba(label, OUT / "packaging/label-rectangular.jpg", PURPLE)

    # Gift bag mock flat
    bag = Image.new("RGBA", (900, 1100), PEARL + (255,))
    d = ImageDraw.Draw(bag)
    d.rounded_rectangle([100, 80, 800, 1000], radius=12, fill=PURPLE + (255,))
    draw_monogram(bag, 450, 480, 260, 330, 155)
    d = ImageDraw.Draw(bag)
    bb = d.textbbox((0, 0), "THE NAIL HOUSE", font=font("playfair", 28))
    d.text(((900 - (bb[2] - bb[0])) // 2, 720), "THE NAIL HOUSE", font=font("playfair", 28), fill=GOLD)
    save_rgba(bag, OUT / "packaging/gift-bag.png")


def uniform_and_signage():
    # Uniform embroidery placement guide
    img = Image.new("RGBA", (1200, 900), PEARL + (255,))
    d = ImageDraw.Draw(img)
    d.text((60, 40), "Uniforme — guía de bordado", font=font("playfair", 36), fill=PURPLE)
    # T-shirt silhouette simplified
    d.rounded_rectangle([200, 150, 550, 750], radius=20, outline=PURPLE + (80,), width=2)
    d.polygon([(200, 200), (280, 150), (470, 150), (550, 200), (550, 280), (480, 280), (480, 200), (270, 200), (270, 280), (200, 280)], outline=PURPLE + (80,))
    draw_monogram(img, 375, 380, 120, 150, 72, with_shadow=False)
    d = ImageDraw.Draw(img)
    d.text((200, 780), "Pechera izquierda · monograma dorado 4–5 cm", font=font("montserrat-light", 14), fill=LILA)

    # Apron
    d.rounded_rectangle([700, 180, 1050, 750], radius=16, outline=PURPLE + (80,), width=2)
    draw_monogram(img, 875, 320, 110, 140, 65, with_shadow=False)
    d = ImageDraw.Draw(img)
    d.text((720, 780), "Delantal · monograma centrado pecho", font=font("montserrat-light", 14), fill=LILA)
    save_rgba(img, OUT / "mockups/uniforme-guia.png")

    # Signage
    sign = Image.new("RGBA", (1400, 700), PURPLE_BLACK + (255,))
    draw_monogram(sign, 320, 350, 280, 360, 170)
    d = ImageDraw.Draw(sign)
    d.text((560, 250), "THE NAIL HOUSE", font=font("playfair", 48), fill=GOLD)
    d.line([(560, 330), (1100, 330)], fill=GOLD + (140,), width=1)
    desc = "NAIL STUDIO BOUTIQUE"
    x = 560
    for ch in desc:
        d.text((x, 360), ch, font=font("montserrat-light", 18), fill=LAVENDER)
        x += d.textbbox((0, 0), ch, font=font("montserrat-light", 18))[2] + 5
    d.text((560, 450), "Estudio en casa · Con cita previa", font=font("montserrat", 16), fill=LILA)
    save_rgba(sign, OUT / "mockups/letrero-estudio.png")
    save_rgba(sign, OUT / "mockups/letrero-estudio.jpg", PURPLE_BLACK)

    # Studio mood board
    mood = Image.new("RGBA", (1400, 1000), PEARL + (255,))
    d = ImageDraw.Draw(mood)
    d.text((60, 40), "Dirección de interiorismo", font=font("playfair", 40), fill=PURPLE)
    d.text((60, 100), "Estudio boutique en casa — Luxury Purple & Gold", font=font("montserrat-light", 16), fill=LILA)

    panels = [
        (PURPLE, "Pared principal\nMorado profundo"),
        (LAVENDER, "Pared secundaria\nLavanda"),
        (PURPLE_BLACK, "Mobiliario\nNegro / neutro"),
        (GOLD, "Detalles\nDorado champagne"),
    ]
    for i, (color, label) in enumerate(panels):
        x = 60 + i * 330
        d.rounded_rectangle([x, 180, x + 300, 420], radius=8, fill=color + (255,))
        if color in (LAVENDER, GOLD):
            d.rounded_rectangle([x, 180, x + 300, 420], radius=8, outline=PURPLE + (60,), width=1)
        tc = PEARL if color in (PURPLE, PURPLE_BLACK) else PURPLE
        y = 460
        for line in label.split("\n"):
            d.text((x, y), line, font=font("montserrat", 16), fill=PURPLE if y == 460 else LILA)
            y += 28

    notes = [
        "• Mesa de manicura elegante en negro mate o blanco perlado",
        "• Espejo con marco dorado delgado",
        "• Iluminación cálida (2700–3000K) sin sombras duras",
        "• Estantería organizada para esmaltes — ritmo visual por color",
        "• Rincón fotográfico con fondo morado y logo dorado",
        "• Textiles: lino, terciopelo suave, sin estampados infantiles",
    ]
    y = 580
    for n in notes:
        d.text((60, y), n, font=font("montserrat-light", 18), fill=PURPLE)
        y += 40
    save_rgba(mood, OUT / "mockups/estudio-direccion.png")
    save_rgba(mood, OUT / "mockups/estudio-direccion.jpg", PEARL)


def brand_guidelines_pdf():
    register_pdf_fonts()
    path = OUT / "brand-guidelines/THE-NAIL-HOUSE-Brand-Guidelines.pdf"
    c = pdf_canvas.Canvas(str(path), pagesize=A4)
    W, H = A4
    purple = HexColor("#352044")
    gold = HexColor("#C5A15B")
    lila = HexColor("#9B78B9")
    lavender = HexColor("#D9C4EC")
    pearl = HexColor("#F7F1F8")
    pblack = HexColor("#1A0F24")

    def header(title, subtitle=None):
        c.setFillColor(purple)
        c.rect(0, H - 80, W, 80, fill=1, stroke=0)
        c.setFillColor(gold)
        c.setFont("Playfair", 18)
        c.drawString(40, H - 45, "THE NAIL HOUSE")
        c.setFont("MontserratLight", 9)
        c.setFillColor(lavender)
        c.drawString(40, H - 62, "MANUAL DE IDENTIDAD CORPORATIVA")
        c.setFillColor(purple)
        c.setFont("Playfair", 28)
        c.drawString(40, H - 130, title)
        if subtitle:
            c.setFont("MontserratLight", 11)
            c.setFillColor(lila)
            c.drawString(40, H - 155, subtitle)
        c.setStrokeColor(gold)
        c.setLineWidth(0.5)
        c.line(40, H - 170, 200, H - 170)

    def footer(page):
        c.setFillColor(lila)
        c.setFont("MontserratLight", 8)
        c.drawString(40, 30, "THE NAIL HOUSE  ·  Confidential Brand Guidelines")
        c.drawRightString(W - 40, 30, str(page))

    # PAGE 1 — Cover
    c.setFillColor(purple)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(gold)
    c.setLineWidth(1.5)
    c.ellipse(W / 2 - 55, H / 2 + 40, W / 2 + 55, H / 2 + 180, stroke=1, fill=0)
    c.setFillColor(gold)
    c.setFont("PlayfairBold", 64)
    c.drawCentredString(W / 2, H / 2 + 120, "T")
    c.setFont("PlayfairBold", 58)
    c.drawCentredString(W / 2, H / 2 + 70, "H")
    c.setFont("Playfair", 28)
    c.drawCentredString(W / 2, H / 2 - 20, "THE NAIL HOUSE")
    c.setStrokeColor(HexColor("#C5A15B"))
    c.setLineWidth(0.6)
    c.line(W / 2 - 40, H / 2 - 40, W / 2 + 40, H / 2 - 40)
    c.setFont("MontserratLight", 11)
    c.setFillColor(lavender)
    c.drawCentredString(W / 2, H / 2 - 65, "N A I L   S T U D I O   B O U T I Q U E")
    c.setFont("Montserrat", 10)
    c.drawCentredString(W / 2, 80, "Manual de Identidad Visual  ·  2026")
    c.showPage()

    # PAGE 2 — Concept
    header("01  Concepto de marca", "Historia, personalidad y posicionamiento")
    y = H - 210
    c.setFillColor(purple)
    c.setFont("Playfair", 16)
    c.drawString(40, y, "Historia")
    y -= 24
    c.setFont("Montserrat", 10)
    text = (
        "THE NAIL HOUSE nace como un estudio de manicura en casa con alma de boutique. "
        "No es un salón convencional: es un espacio íntimo donde el cuidado de las uñas "
        "se vive como un ritual de belleza exclusivo, personalizado y sofisticado."
    )
    for line in _wrap(text, 88):
        c.drawString(40, y, line)
        y -= 16
    y -= 16
    c.setFont("Playfair", 16)
    c.drawString(40, y, "Personalidad")
    y -= 24
    traits = ["Glamurosa", "Elegante", "Femenina", "Llamativa", "Exclusiva"]
    x = 40
    for t in traits:
        c.setFillColor(purple)
        c.roundRect(x, y - 8, 85, 24, 4, fill=1, stroke=0)
        c.setFillColor(gold)
        c.setFont("Montserrat", 8)
        c.drawCentredString(x + 42.5, y, t)
        x += 95
    y -= 50
    c.setFillColor(purple)
    c.setFont("Playfair", 16)
    c.drawString(40, y, "Posicionamiento")
    y -= 24
    c.setFont("Montserrat", 10)
    c.drawString(40, y, "Nail Studio Boutique — profesionalidad, confianza, belleza y exclusividad.")
    y -= 40
    c.setFont("Playfair", 16)
    c.drawString(40, y, "Público objetivo")
    y -= 24
    c.setFont("Montserrat", 10)
    for line in _wrap(
        "Mujeres de todas las edades que buscan cuidar sus uñas, disfrutar de diseños "
        "personalizados y recibir una atención especial en un entorno premium.",
        88,
    ):
        c.drawString(40, y, line)
        y -= 16
    footer(2)
    c.showPage()

    # PAGE 3 — Logo
    header("02  Sistema de logotipos", "Monograma TH · versiones oficiales")
    y = H - 210
    c.setFont("Montserrat", 10)
    c.setFillColor(purple)
    for line in _wrap(
        "El monograma TH entrelazado dentro de un óvalo dorado es el símbolo principal "
        "de reconocimiento. No debe reemplazarse, alterarse con adornos (coronas, flores, "
        "manos, esmaltes) ni modificarse en sus iniciales.",
        88,
    ):
        c.drawString(40, y, line)
        y -= 16
    y -= 20
    versions = [
        ("A. Principal", "Monograma + nombre + descriptor, centrado sobre morado."),
        ("B. Isotipo", "Solo el símbolo TH en óvalo. Instagram, favicon, marca de agua."),
        ("C. Horizontal", "Símbolo a la izquierda, wordmark a la derecha."),
        ("D. Monocromático", "Dorado, morado o perlado para bordado e impresión."),
    ]
    for title, desc in versions:
        c.setFont("Playfair", 13)
        c.setFillColor(gold)
        c.drawString(40, y, title)
        c.setFont("Montserrat", 10)
        c.setFillColor(purple)
        c.drawString(160, y, desc)
        y -= 28
    y -= 10
    c.setFont("Playfair", 14)
    c.setFillColor(purple)
    c.drawString(40, y, "Usos incorrectos")
    y -= 20
    c.setFont("Montserrat", 10)
    wrongs = [
        "• No distorsionar, rotar ni estirar el monograma",
        "• No cambiar el óvalo por círculo, escudo o corona",
        "• No usar dorado amarillo intenso (#FFD700)",
        "• No colocar el logo sobre fondos que reduzcan el contraste",
        "• No añadir sombras pesadas, brillos neón o efectos 3D exagerados",
        "• No recrear el monograma con tipografías distintas a la serif oficial",
    ]
    for wline in wrongs:
        c.drawString(40, y, wline)
        y -= 16
    footer(3)
    c.showPage()

    # PAGE 4 — Colors
    header("03  Paleta cromática", "Luxury Purple & Gold")
    swatches = [
        ("Morado profundo", "#352044", purple, "Principal"),
        ("Dorado champagne", "#C5A15B", gold, "Premium"),
        ("Lila", "#9B78B9", lila, "Acento"),
        ("Lavanda", "#D9C4EC", lavender, "Suave"),
        ("Negro púrpura", "#1A0F24", pblack, "Contraste"),
        ("Blanco perlado", "#F7F1F8", pearl, "Fondos"),
    ]
    y = H - 220
    for i, (name, hx, col, role) in enumerate(swatches):
        col_i, row = i % 3, i // 3
        x = 40 + col_i * 175
        yy = y - row * 160
        c.setFillColor(col)
        c.roundRect(x, yy - 80, 155, 90, 6, fill=1, stroke=0)
        if name in ("Lavanda", "Blanco perlado"):
            c.setStrokeColor(lila)
            c.roundRect(x, yy - 80, 155, 90, 6, fill=0, stroke=1)
        c.setFillColor(purple)
        c.setFont("MontserratMedium", 9)
        c.drawString(x, yy - 100, name)
        c.setFont("MontserratLight", 9)
        c.setFillColor(lila)
        c.drawString(x, yy - 115, hx)
        c.drawString(x, yy - 130, role)
    footer(4)
    c.showPage()

    # PAGE 5 — Typography
    header("04  Tipografías", "Playfair Display + Montserrat")
    y = H - 210
    c.setFillColor(purple)
    c.setFont("Playfair", 16)
    c.drawString(40, y, "Principal — Playfair Display")
    y -= 30
    c.setFont("Playfair", 22)
    c.drawString(40, y, "THE NAIL HOUSE")
    y -= 28
    c.setFont("PlayfairItalic", 16)
    c.setFillColor(gold)
    c.drawString(40, y, "Nail Studio Boutique")
    y -= 40
    c.setFillColor(purple)
    c.setFont("Playfair", 16)
    c.drawString(40, y, "Secundaria — Montserrat")
    y -= 26
    c.setFont("Montserrat", 12)
    c.drawString(40, y, "Cuerpo de texto, UI, descriptores y CTAs.")
    y -= 20
    c.setFont("MontserratLight", 11)
    c.drawString(40, y, "NAIL STUDIO — Light, tracking amplio")
    y -= 40
    c.setFont("Playfair", 14)
    c.drawString(40, y, "Alternativas")
    y -= 20
    c.setFont("Montserrat", 10)
    c.drawString(40, y, "Cormorant Garamond (serif)  ·  Poppins (sans)")
    footer(5)
    c.showPage()

    # PAGE 6 — Applications
    header("05  Aplicaciones", "Puntos de contacto de la marca")
    apps = [
        "Tarjetas de presentación (frente morado / reverso perlado)",
        "Tarjetas de citas y fidelización",
        "Lista de precios editorial",
        "Perfil, portada e historias destacadas de Instagram",
        "Plantillas de publicación (servicios, promos, antes/después)",
        "Stickers, etiquetas y packaging boutique",
        "Uniformes (bordado del monograma dorado)",
        "Letrero interior/exterior del estudio",
        "Dirección de interiorismo: pared morada, detalles dorados, luz cálida",
    ]
    y = H - 210
    c.setFont("Montserrat", 11)
    c.setFillColor(purple)
    for a in apps:
        c.setFillColor(gold)
        c.circle(48, y + 3, 3, fill=1, stroke=0)
        c.setFillColor(purple)
        c.drawString(60, y, a)
        y -= 28
    footer(6)
    c.showPage()

    # PAGE 7 — Clear space & closing
    header("06  Área de respeto y cierre", "Reproducción limpia y escalable")
    y = H - 210
    c.setFont("Montserrat", 10)
    c.setFillColor(purple)
    for line in _wrap(
        "Mantén un área de respeto mínima equivalente a la mitad de la altura del óvalo "
        "alrededor del monograma. El isotipo debe reproducirse nítido a partir de 24 px "
        "en digital y 10 mm en impresión. Para bordados, usar la versión monocromática dorada.",
        88,
    ):
        c.drawString(40, y, line)
        y -= 16
    y -= 30
    c.setFont("Playfair", 16)
    c.drawString(40, y, "Dirección artística")
    y -= 24
    c.setFont("Montserrat", 10)
    c.drawString(40, y, "Estética: LUXURY PURPLE & GOLD")
    y -= 18
    c.drawString(40, y, "Referencias: belleza de lujo, packaging cosmético premium, editoriales de moda.")
    y -= 40
    c.setFillColor(purple)
    c.roundRect(40, 80, W - 80, 120, 8, fill=1, stroke=0)
    c.setFillColor(gold)
    c.setFont("Playfair", 18)
    c.drawCentredString(W / 2, 155, "THE NAIL HOUSE")
    c.setFont("MontserratLight", 10)
    c.setFillColor(lavender)
    c.drawCentredString(W / 2, 130, "Una identidad reconocible, memorable y lista para crecer.")
    c.drawCentredString(W / 2, 110, "Nail Studio Boutique")
    footer(7)
    c.save()


def _wrap(text: str, width: int) -> list[str]:
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = f"{cur} {w}".strip()
        if len(test) <= width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def write_readme():
    (OUT / "README.md").write_text(
        """# THE NAIL HOUSE — Identidad Visual

**Luxury Purple & Gold** · Nail Studio Boutique

## Estructura

```
brand/
├── logos/           # Principal, isotipo, horizontal, secundario, monocromo
├── colors/          # Paleta HEX, CSS, JSON
├── typography/      # Especímenes Playfair + Montserrat
├── social-media/    # Perfil, highlights, plantillas IG
├── business-cards/  # Tarjetas de presentación
├── appointments/    # Citas y fidelización
├── price-list/      # Lista de precios
├── packaging/       # Stickers, etiquetas, bolsa
├── mockups/         # Uniforme, letrero, estudio
└── brand-guidelines/# Manual PDF + HTML
```

## Paleta

| Color | HEX | Uso |
|-------|-----|-----|
| Morado profundo | `#352044` | Principal |
| Dorado champagne | `#C5A15B` | Logo / premium |
| Lila | `#9B78B9` | Acentos |
| Lavanda | `#D9C4EC` | Fondos suaves |
| Negro púrpura | `#1A0F24` | Contraste |
| Blanco perlado | `#F7F1F8` | Documentos |

## Tipografía

- **Principal:** Playfair Display
- **Secundaria:** Montserrat
- **Alternativas:** Cormorant Garamond · Poppins

## Regla del monograma

El símbolo TH dentro del óvalo dorado es inalterable: no coronas, flores, manos ni esmaltes.
""",
        encoding="utf-8",
    )


def write_guidelines_html():
    html = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>THE NAIL HOUSE — Manual de Identidad</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Montserrat:wght@300;400;500&display=swap" rel="stylesheet"/>
<style>
:root{--purple:#352044;--gold:#C5A15B;--lila:#9B78B9;--lavender:#D9C4EC;--black:#1A0F24;--pearl:#F7F1F8}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Montserrat,sans-serif;background:var(--pearl);color:var(--purple);line-height:1.6}
.hero{background:var(--purple);color:var(--gold);min-height:70vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:4rem 1.5rem}
.oval{width:140px;height:180px;border:2px solid var(--gold);border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;margin-bottom:2rem}
.oval .t{font-family:'Playfair Display',serif;font-size:4rem;font-weight:700;line-height:0.85}
.oval .h{font-family:'Playfair Display',serif;font-size:3.5rem;font-weight:700;line-height:0.85;margin-top:-0.3rem}
.hero h1{font-family:'Playfair Display',serif;font-size:clamp(1.8rem,4vw,2.8rem);font-weight:400;letter-spacing:.08em;margin-bottom:.5rem}
.hero .desc{font-weight:300;letter-spacing:.35em;font-size:.75rem;color:var(--lavender);margin-top:1rem}
.hero .sub{margin-top:2rem;font-size:.85rem;color:var(--lila)}
section{max-width:960px;margin:0 auto;padding:4rem 1.5rem;border-bottom:1px solid rgba(155,120,185,.25)}
h2{font-family:'Playfair Display',serif;font-size:1.8rem;margin-bottom:.5rem}
.eyebrow{font-size:.7rem;letter-spacing:.25em;text-transform:uppercase;color:var(--gold);font-weight:500;margin-bottom:.75rem}
p,li{font-weight:300;font-size:.95rem}
.swatches{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:1rem;margin-top:1.5rem}
.swatch .chip{height:90px;border-radius:8px;margin-bottom:.5rem;border:1px solid rgba(155,120,185,.2)}
.swatch strong{display:block;font-weight:500;font-size:.85rem}
.swatch span{font-size:.75rem;color:var(--lila)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-top:1.5rem}
@media(max-width:700px){.grid2{grid-template-columns:1fr}}
.card{background:#fff;padding:1.25rem;border-radius:8px;border:1px solid rgba(155,120,185,.2)}
.card h3{font-family:'Playfair Display',serif;font-size:1.1rem;margin-bottom:.5rem;color:var(--gold)}
ul{padding-left:1.2rem;margin-top:.75rem}
li{margin-bottom:.4rem}
.traits{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0}
.traits span{background:var(--purple);color:var(--gold);padding:.4rem .9rem;border-radius:4px;font-size:.75rem;font-weight:500}
footer{background:var(--purple);color:var(--lavender);text-align:center;padding:3rem 1.5rem;font-weight:300;font-size:.85rem}
footer strong{font-family:'Playfair Display',serif;color:var(--gold);font-size:1.2rem;display:block;margin-bottom:.5rem;font-weight:400}
</style>
</head>
<body>
<header class="hero">
  <div class="oval"><div class="t">T</div><div class="h">H</div></div>
  <h1>THE NAIL HOUSE</h1>
  <div class="desc">NAIL STUDIO BOUTIQUE</div>
  <p class="sub">Manual de Identidad Visual · Luxury Purple &amp; Gold</p>
</header>

<section>
  <div class="eyebrow">01 — Concepto</div>
  <h2>Historia y personalidad</h2>
  <p>THE NAIL HOUSE es un estudio de manicura en casa con posicionamiento de Nail Studio Boutique. Transmite profesionalidad, confianza, belleza, cuidado personal y exclusividad.</p>
  <div class="traits">
    <span>Glamurosa</span><span>Elegante</span><span>Femenina</span><span>Llamativa</span><span>Exclusiva</span>
  </div>
</section>

<section>
  <div class="eyebrow">02 — Logotipo</div>
  <h2>Sistema de marcas</h2>
  <div class="grid2">
    <div class="card"><h3>A. Principal</h3><p>Monograma TH en óvalo + THE NAIL HOUSE + NAIL STUDIO, centrado sobre morado profundo.</p></div>
    <div class="card"><h3>B. Isotipo</h3><p>Solo el símbolo. Ideal para Instagram, favicon y marca de agua.</p></div>
    <div class="card"><h3>C. Horizontal</h3><p>Símbolo a la izquierda, wordmark a la derecha.</p></div>
    <div class="card"><h3>D. Monocromo</h3><p>Dorado, morado o perlado para bordado e impresión.</p></div>
  </div>
  <p style="margin-top:1.25rem">Regla fundamental: no reemplazar el monograma, no cambiar las iniciales, no eliminar el óvalo, no añadir coronas, flores, manos ni esmaltes.</p>
</section>

<section>
  <div class="eyebrow">03 — Color</div>
  <h2>Paleta Luxury Purple &amp; Gold</h2>
  <div class="swatches">
    <div class="swatch"><div class="chip" style="background:#352044"></div><strong>Morado profundo</strong><span>#352044 · Principal</span></div>
    <div class="swatch"><div class="chip" style="background:#C5A15B"></div><strong>Dorado champagne</strong><span>#C5A15B · Premium</span></div>
    <div class="swatch"><div class="chip" style="background:#9B78B9"></div><strong>Lila</strong><span>#9B78B9 · Acento</span></div>
    <div class="swatch"><div class="chip" style="background:#D9C4EC"></div><strong>Lavanda</strong><span>#D9C4EC · Suave</span></div>
    <div class="swatch"><div class="chip" style="background:#1A0F24"></div><strong>Negro púrpura</strong><span>#1A0F24 · Contraste</span></div>
    <div class="swatch"><div class="chip" style="background:#F7F1F8"></div><strong>Blanco perlado</strong><span>#F7F1F8 · Fondos</span></div>
  </div>
</section>

<section>
  <div class="eyebrow">04 — Tipografía</div>
  <h2>Playfair Display + Montserrat</h2>
  <p style="font-family:'Playfair Display',serif;font-size:2rem;margin:1rem 0">THE NAIL HOUSE</p>
  <p style="font-family:'Playfair Display',serif;font-style:italic;color:var(--gold);font-size:1.25rem;margin-bottom:1rem">Nail Studio Boutique</p>
  <p>Principal: Playfair Display (alternativa Cormorant Garamond).<br/>Secundaria: Montserrat Light/Regular/Medium (alternativa Poppins).</p>
</section>

<section>
  <div class="eyebrow">05 — Aplicaciones</div>
  <h2>Puntos de contacto</h2>
  <ul>
    <li>Tarjetas de presentación, citas y fidelización</li>
    <li>Lista de precios editorial</li>
    <li>Instagram: perfil, portada, highlights y plantillas</li>
    <li>Packaging, stickers y etiquetas</li>
    <li>Uniformes y letrero del estudio</li>
    <li>Interiorismo: pared morada, detalles dorados, luz cálida</li>
  </ul>
</section>

<footer>
  <strong>THE NAIL HOUSE</strong>
  Identidad visual completa · Lista para crecer como salón reconocido
</footer>
</body>
</html>
"""
    (OUT / "brand-guidelines/index.html").write_text(html, encoding="utf-8")


def main():
    ensure_dirs()
    print("→ Logos…")
    logo_monogram()
    logo_primary()
    logo_horizontal()
    logo_secondary()
    logo_monochrome()
    print("→ Colors & typography…")
    colors_sheet()
    typography_sheet()
    print("→ Print & social…")
    business_cards()
    appointment_cards()
    loyalty_card()
    price_list()
    social_templates()
    print("→ Packaging & mockups…")
    packaging_and_stickers()
    uniform_and_signage()
    print("→ Guidelines…")
    brand_guidelines_pdf()
    write_guidelines_html()
    write_readme()
    print("✓ Brand system generated at", OUT)


if __name__ == "__main__":
    main()
