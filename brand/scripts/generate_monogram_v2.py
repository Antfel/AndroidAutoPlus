#!/usr/bin/env python3
"""
THE NAIL HOUSE — Monogram v2
Recreates the official TH mark: outer H stems, central T, diagonal
M-like joins locking into a central ring — gold on deep purple.
Also builds OKSANA-inspired card + original director proposal exports.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = Path("/tmp/fonts")

PURPLE = (53, 32, 68)
GOLD = (197, 161, 91)
GOLD_LIGHT = (232, 210, 150)
GOLD_DARK = (148, 112, 48)
LILA = (155, 120, 185)
LAVENDER = (217, 196, 236)
LAVENDER_CARD = (168, 148, 186)  # dusty lilac like OKSANA ref
PURPLE_BLACK = (26, 15, 36)
PEARL = (247, 241, 248)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    mapping = {
        "playfair": "PlayfairDisplay-Regular.ttf",
        "playfair-bold": "PlayfairDisplay-Bold.ttf",
        "montserrat": "Montserrat-Regular.ttf",
        "montserrat-light": "Montserrat-Light.ttf",
        "montserrat-medium": "Montserrat-Medium.ttf",
    }
    return ImageFont.truetype(str(FONTS / mapping[name]), size)


def gold_grad(y: float, y0: float, y1: float) -> tuple[int, int, int]:
    t = (y - y0) / max(1, y1 - y0)
    t = max(0.0, min(1.0, t))
    # highlight top-left feel
    if t < 0.45:
        u = t / 0.45
        return tuple(int(GOLD_LIGHT[i] + (GOLD[i] - GOLD_LIGHT[i]) * u) for i in range(3))
    u = (t - 0.45) / 0.55
    return tuple(int(GOLD[i] + (GOLD_DARK[i] - GOLD[i]) * u) for i in range(3))


def draw_thick_line(draw, p1, p2, width, color):
    draw.line([p1, p2], fill=color, width=width)


def draw_serif_bar(draw, x1, y, x2, serif_h, stroke, color):
    """Horizontal bar with end serifs (for T crossbar)."""
    draw.line([(x1, y), (x2, y)], fill=color, width=stroke)
    # left serif
    draw.line([(x1, y - serif_h), (x1, y + serif_h)], fill=color, width=max(2, stroke // 2))
    # right serif
    draw.line([(x2, y - serif_h), (x2, y + serif_h)], fill=color, width=max(2, stroke // 2))


def draw_official_monogram(
    base: Image.Image,
    cx: int,
    cy: int,
    scale: float = 1.0,
    with_shadow: bool = True,
    color: tuple[int, int, int] | None = None,
):
    """
    Official-structure monogram:
    - Vertical oval
    - Outer H uprights with base serifs
    - Central T with top bar + serifs
    - Diagonal joins meeting a central ring (the signature detail)
    """
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    oval_rx = int(180 * scale)
    oval_ry = int(230 * scale)
    stroke = max(2, int(7 * scale))
    stem = max(3, int(10 * scale))
    thin = max(2, int(6 * scale))

    # Soft shadow
    if with_shadow:
        sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(sh)
        sd.ellipse(
            [cx - oval_rx + 3, cy - oval_ry + 5, cx + oval_rx + 3, cy + oval_ry + 5],
            outline=(0, 0, 0, 60),
            width=stroke,
        )
        # rough letter shadow block
        sd.rectangle(
            [cx - int(90 * scale) + 3, cy - int(110 * scale) + 5, cx + int(90 * scale) + 3, cy + int(110 * scale) + 5],
            fill=(0, 0, 0, 25),
        )
        sh = sh.filter(ImageFilter.GaussianBlur(5))
        base.alpha_composite(sh)

    # Draw metallic feel by stacking slightly offset gold tones if no fixed color
    colors = [color] if color else [GOLD_DARK, GOLD, GOLD_LIGHT]
    offsets = [(0, 0)] if color else [(1, 1), (0, 0), (-1, -1)]

    for col, (ox, oy) in zip(colors, offsets):
        c = col + (255,)
        ocx, ocy = cx + ox, cy + oy

        # Oval
        d.ellipse(
            [ocx - oval_rx, ocy - oval_ry, ocx + oval_rx, ocy + oval_ry],
            outline=c,
            width=stroke,
        )

        # Geometry
        top = ocy - int(105 * scale)
        bottom = ocy + int(105 * scale)
        left = ocx - int(70 * scale)
        right = ocx + int(70 * scale)
        t_bar_y = ocy - int(95 * scale)
        t_bar_half = int(78 * scale)
        ring_r = int(14 * scale)
        ring_cy = ocy + int(8 * scale)

        # Outer H uprights
        d.line([(left, top + int(25 * scale)), (left, bottom)], fill=c, width=stem)
        d.line([(right, top + int(25 * scale)), (right, bottom)], fill=c, width=stem)
        # Base serifs on H stems
        ser = int(16 * scale)
        d.line([(left - ser, bottom), (left + ser, bottom)], fill=c, width=thin)
        d.line([(right - ser, bottom), (right + ser, bottom)], fill=c, width=thin)
        # Top small serifs on H stems
        d.line(
            [(left - int(10 * scale), top + int(25 * scale)), (left + int(10 * scale), top + int(25 * scale))],
            fill=c,
            width=thin,
        )
        d.line(
            [(right - int(10 * scale), top + int(25 * scale)), (right + int(10 * scale), top + int(25 * scale))],
            fill=c,
            width=thin,
        )

        # Central T stem
        d.line([(ocx, t_bar_y), (ocx, bottom)], fill=c, width=stem)
        # T top bar with end serifs
        d.line([(ocx - t_bar_half, t_bar_y), (ocx + t_bar_half, t_bar_y)], fill=c, width=stem)
        d.line(
            [(ocx - t_bar_half, t_bar_y - int(14 * scale)), (ocx - t_bar_half, t_bar_y + int(14 * scale))],
            fill=c,
            width=thin,
        )
        d.line(
            [(ocx + t_bar_half, t_bar_y - int(14 * scale)), (ocx + t_bar_half, t_bar_y + int(14 * scale))],
            fill=c,
            width=thin,
        )
        # T base serif
        d.line([(ocx - ser, bottom), (ocx + ser, bottom)], fill=c, width=thin)

        # Diagonal joins (M-like) into central ring
        # Left diagonal: from mid-left stem inward-down to ring
        mid_y = ocy - int(20 * scale)
        d.line([(left, mid_y), (ocx - ring_r - 2, ring_cy - int(4 * scale))], fill=c, width=thin)
        d.line([(right, mid_y), (ocx + ring_r + 2, ring_cy - int(4 * scale))], fill=c, width=thin)
        # Lower diagonals completing the lock
        d.line([(left, mid_y + int(35 * scale)), (ocx - ring_r - 2, ring_cy + int(6 * scale))], fill=c, width=max(2, thin - 1))
        d.line([(right, mid_y + int(35 * scale)), (ocx + ring_r + 2, ring_cy + int(6 * scale))], fill=c, width=max(2, thin - 1))

        # Central ring — signature detail (drawn last so it sits as lock)
        d.ellipse(
            [ocx - ring_r, ring_cy - ring_r, ocx + ring_r, ring_cy + ring_r],
            outline=c,
            width=max(2, thin),
        )

    base.alpha_composite(layer)


def draw_original_monogram(base: Image.Image, cx: int, cy: int, scale: float = 1.0):
    """Director's original: thinner jewelry line-art TH with pearl node + base hairline."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    oval_rx = int(160 * scale)
    oval_ry = int(205 * scale)
    stroke = max(2, int(5 * scale))
    stem = max(2, int(7 * scale))

    # Oval
    d.ellipse([cx - oval_rx, cy - oval_ry, cx + oval_rx, cy + oval_ry], outline=GOLD + (255,), width=stroke)

    top = cy - int(95 * scale)
    bottom = cy + int(70 * scale)
    left = cx - int(55 * scale)
    right = cx + int(55 * scale)
    t_y = cy - int(85 * scale)

    # H uprights — flared ends suggested with slight width at ends via short serifs
    d.line([(left, top + int(20 * scale)), (left, bottom)], fill=GOLD + (255,), width=stem)
    d.line([(right, top + int(20 * scale)), (right, bottom)], fill=GOLD + (255,), width=stem)

    # T with curved-feel serifs (approximated)
    half = int(70 * scale)
    d.line([(cx - half, t_y), (cx + half, t_y)], fill=GOLD + (255,), width=stem)
    # curved serif approx — short diagonals
    d.line([(cx - half, t_y), (cx - half - int(6 * scale), t_y + int(16 * scale))], fill=GOLD + (255,), width=max(2, stem - 1))
    d.line([(cx + half, t_y), (cx + half + int(6 * scale), t_y + int(16 * scale))], fill=GOLD + (255,), width=max(2, stem - 1))
    d.line([(cx, t_y), (cx, bottom)], fill=GOLD + (255,), width=stem)

    # H crossbar through pearl
    mid = cy + int(5 * scale)
    d.line([(left, mid), (right, mid)], fill=GOLD + (255,), width=stem)

    # Pearl node at intersection
    pr = int(10 * scale)
    d.ellipse([cx - pr, mid - pr, cx + pr, mid + pr], fill=GOLD_LIGHT + (255,), outline=GOLD_DARK + (255,), width=2)

    # Base hairline inside oval
    d.line([(cx - int(40 * scale), cy + int(100 * scale)), (cx + int(40 * scale), cy + int(100 * scale))], fill=GOLD + (200,), width=2)

    base.alpha_composite(layer)


def spaced_text(draw, text, font_obj, y, canvas_w, fill, spacing=6):
    total = sum(draw.textbbox((0, 0), ch, font=font_obj)[2] for ch in text) + spacing * (len(text) - 1)
    x = (canvas_w - total) // 2
    for ch in text:
        draw.text((x, y), ch, font=font_obj, fill=fill)
        x += draw.textbbox((0, 0), ch, font=font_obj)[2] + spacing


def save(img: Image.Image, path: Path, bg=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() in {".jpg", ".jpeg"}:
        out = Image.new("RGB", img.size, bg or PURPLE)
        if img.mode == "RGBA":
            out.paste(img, mask=img.split()[3])
        else:
            out.paste(img)
        out.save(path, quality=95)
    else:
        img.save(path)


def make_official_svg(path: Path, bg="#352044", size=512):
    # Approximate vector of the official structure
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="gold" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#E8D296"/>
      <stop offset="45%" stop-color="#C5A15B"/>
      <stop offset="100%" stop-color="#947030"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" fill="{bg}"/>
  <ellipse cx="256" cy="256" rx="150" ry="190" fill="none" stroke="url(#gold)" stroke-width="6"/>
  <!-- H uprights -->
  <line x1="186" y1="170" x2="186" y2="360" stroke="url(#gold)" stroke-width="9" stroke-linecap="square"/>
  <line x1="326" y1="170" x2="326" y2="360" stroke="url(#gold)" stroke-width="9" stroke-linecap="square"/>
  <line x1="172" y1="360" x2="200" y2="360" stroke="url(#gold)" stroke-width="5"/>
  <line x1="312" y1="360" x2="340" y2="360" stroke="url(#gold)" stroke-width="5"/>
  <!-- T -->
  <line x1="178" y1="155" x2="334" y2="155" stroke="url(#gold)" stroke-width="9"/>
  <line x1="178" y1="142" x2="178" y2="168" stroke="url(#gold)" stroke-width="5"/>
  <line x1="334" y1="142" x2="334" y2="168" stroke="url(#gold)" stroke-width="5"/>
  <line x1="256" y1="155" x2="256" y2="360" stroke="url(#gold)" stroke-width="9"/>
  <line x1="242" y1="360" x2="270" y2="360" stroke="url(#gold)" stroke-width="5"/>
  <!-- Diagonals into ring -->
  <line x1="186" y1="230" x2="240" y2="268" stroke="url(#gold)" stroke-width="5"/>
  <line x1="326" y1="230" x2="272" y2="268" stroke="url(#gold)" stroke-width="5"/>
  <line x1="186" y1="270" x2="240" y2="278" stroke="url(#gold)" stroke-width="4"/>
  <line x1="326" y1="270" x2="272" y2="278" stroke="url(#gold)" stroke-width="4"/>
  <!-- Central ring — original detail -->
  <circle cx="256" cy="272" r="14" fill="none" stroke="url(#gold)" stroke-width="5"/>
</svg>
'''
    path.write_text(svg, encoding="utf-8")


def export_official_set():
    size = 1024
    img = Image.new("RGBA", (size, size), PURPLE + (255,))
    draw_official_monogram(img, size // 2, size // 2, scale=1.55)
    save(img, ROOT / "logos/logo-official/logo-monogram.jpg", PURPLE)
    save(img, ROOT / "logos/logo-official/logo-monogram.png")
    save(img, ROOT / "logos/logo-monogram/logo-monogram.jpg", PURPLE)
    save(img, ROOT / "logos/logo-monogram/logo-monogram.png")

    img_t = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_official_monogram(img_t, size // 2, size // 2, scale=1.55, with_shadow=False)
    save(img_t, ROOT / "logos/logo-official/logo-monogram-transparent.png")
    save(img_t, ROOT / "logos/logo-monogram/logo-monogram-transparent.png")

    make_official_svg(ROOT / "logos/logo-official/logo-monogram.svg")
    make_official_svg(ROOT / "logos/logo-monogram/logo-monogram.svg")
    make_official_svg(ROOT / "logos/logo-official/logo-monogram-transparent.svg", bg="none")

    # Primary stacked
    w, h = 1200, 1400
    primary = Image.new("RGBA", (w, h), PURPLE + (255,))
    draw_official_monogram(primary, w // 2, int(h * 0.38), scale=1.35)
    d = ImageDraw.Draw(primary)
    name = "THE NAIL HOUSE"
    f = font("playfair", 64)
    nb = d.textbbox((0, 0), name, font=f)
    d.text(((w - (nb[2] - nb[0])) // 2, int(h * 0.68)), name, font=f, fill=GOLD + (255,))
    d.line([(w // 2 - 80, int(h * 0.75)), (w // 2 + 80, int(h * 0.75))], fill=GOLD + (180,), width=1)
    spaced_text(d, "NAIL STUDIO", font("montserrat-light", 22), int(h * 0.77), w, LAVENDER + (230,), 8)
    save(primary, ROOT / "logos/logo-primary/logo-primary.png")
    save(primary, ROOT / "logos/logo-primary/logo-primary.jpg", PURPLE)

    # Horizontal
    w, h = 1600, 500
    horiz = Image.new("RGBA", (w, h), PURPLE + (255,))
    draw_official_monogram(horiz, 220, h // 2, scale=0.85)
    d = ImageDraw.Draw(horiz)
    d.text((420, h // 2 - 55), "THE NAIL HOUSE", font=font("playfair", 58), fill=GOLD + (255,))
    d.line([(420, h // 2 + 10), (800, h // 2 + 10)], fill=GOLD + (160,), width=1)
    x = 420
    for ch in "NAIL STUDIO":
        d.text((x, h // 2 + 25), ch, font=font("montserrat-light", 20), fill=LAVENDER + (230,))
        x += d.textbbox((0, 0), ch, font=font("montserrat-light", 20))[2] + 7
    save(horiz, ROOT / "logos/logo-horizontal/logo-horizontal.png")
    save(horiz, ROOT / "logos/logo-horizontal/logo-horizontal.jpg", PURPLE)

    # Favicons / profile
    for s in (512, 256, 128, 64, 32):
        fav = img.resize((s, s), Image.Resampling.LANCZOS)
        save(fav, ROOT / f"logos/logo-monogram/favicon-{s}.png")
        save(fav, ROOT / f"social-media/profile/profile-{s}.png")
        save(fav, ROOT / f"social-media/profile/instagram-profile.png") if s == 512 else None

    # Monochrome
    for name, col, bg in [
        ("logo-gold", GOLD, None),
        ("logo-purple", PURPLE, None),
        ("logo-pearl", PEARL, None),
    ]:
        m = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw_official_monogram(m, size // 2, size // 2, scale=1.55, with_shadow=False, color=col)
        save(m, ROOT / f"logos/logo-monochrome/{name}.png")


def export_oksana_style_card():
    """Business card guided by OKSANA layout: dusty lavender + gold foil stack."""
    w, h = 1050, 600
    card = Image.new("RGBA", (w, h), LAVENDER_CARD + (255,))
    draw_official_monogram(card, w // 2, int(h * 0.32), scale=0.55, with_shadow=False, color=GOLD)
    d = ImageDraw.Draw(card)
    name = "THE NAIL HOUSE"
    # OKSANA ref uses bold serif or clean caps — we use Playfair gold
    f = font("playfair", 36)
    nb = d.textbbox((0, 0), name, font=f)
    d.text(((w - (nb[2] - nb[0])) // 2, 340), name, font=f, fill=GOLD + (255,))
    spaced_text(d, "NAIL STUDIO", font("montserrat-light", 14), 395, w, GOLD + (220,), 5)
    # Diamond divider
    mid = 450
    d.line([(w // 2 - 70, mid), (w // 2 - 10, mid)], fill=GOLD + (200,), width=1)
    d.polygon(
        [(w // 2, mid - 5), (w // 2 + 5, mid), (w // 2, mid + 5), (w // 2 - 5, mid)],
        fill=GOLD + (255,),
    )
    d.line([(w // 2 + 10, mid), (w // 2 + 70, mid)], fill=GOLD + (200,), width=1)
    save(card, ROOT / "business-cards/card-front-lavender.png")
    save(card, ROOT / "business-cards/card-front-lavender.jpg", LAVENDER_CARD)

    # Deep purple version same layout (brand primary)
    card2 = Image.new("RGBA", (w, h), PURPLE + (255,))
    draw_official_monogram(card2, w // 2, int(h * 0.32), scale=0.55, with_shadow=True)
    d = ImageDraw.Draw(card2)
    nb = d.textbbox((0, 0), name, font=f)
    d.text(((w - (nb[2] - nb[0])) // 2, 340), name, font=f, fill=GOLD + (255,))
    spaced_text(d, "NAIL STUDIO", font("montserrat-light", 14), 395, w, LAVENDER + (230,), 5)
    mid = 450
    d.line([(w // 2 - 70, mid), (w // 2 - 10, mid)], fill=GOLD + (200,), width=1)
    d.polygon(
        [(w // 2, mid - 5), (w // 2 + 5, mid), (w // 2, mid + 5), (w // 2 - 5, mid)],
        fill=GOLD + (255,),
    )
    d.line([(w // 2 + 10, mid), (w // 2 + 70, mid)], fill=GOLD + (200,), width=1)
    save(card2, ROOT / "business-cards/card-front.png")
    save(card2, ROOT / "business-cards/card-front.jpg", PURPLE)


def export_original_proposal():
    size = 1200
    img = Image.new("RGBA", (size, size), PURPLE_BLACK + (255,))
    draw_original_monogram(img, size // 2, int(size * 0.38), scale=1.5)
    d = ImageDraw.Draw(img)
    name = "THE NAIL HOUSE"
    f = font("playfair", 48)
    nb = d.textbbox((0, 0), name, font=f)
    d.text(((size - (nb[2] - nb[0])) // 2, 820), name, font=f, fill=GOLD + (255,))
    # diamond divider
    mid_y = 890
    d.line([(size // 2 - 80, mid_y), (size // 2 - 12, mid_y)], fill=GOLD + (200,), width=1)
    d.polygon(
        [(size // 2, mid_y - 6), (size // 2 + 6, mid_y), (size // 2, mid_y + 6), (size // 2 - 6, mid_y)],
        fill=GOLD + (255,),
    )
    d.line([(size // 2 + 12, mid_y), (size // 2 + 80, mid_y)], fill=GOLD + (200,), width=1)
    spaced_text(d, "NAIL STUDIO BOUTIQUE", font("montserrat-light", 16), 920, size, LAVENDER + (230,), 7)
    save(img, ROOT / "logos/logo-original-proposal/logo-original.png")
    save(img, ROOT / "logos/logo-original-proposal/logo-original.jpg", PURPLE_BLACK)
    save(img, ROOT / "proposals/director-original-proposal.png")
    save(img, ROOT / "proposals/director-original-proposal.jpg", PURPLE_BLACK)

    # Transparent monogram only
    m = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
    draw_original_monogram(m, 400, 400, scale=1.4)
    save(m, ROOT / "logos/logo-original-proposal/monogram-transparent.png")

    note = """# Propuesta original del director creativo

Versión alternativa — **no sustituye** el monograma oficial TH.

## Concepto
- Óvalo dorado fino (misma familia formal)
- TH entrelazada en trazo joya / line-art más delgado
- Nodo perla en el cruce (detalle propio)
- Base hairline dentro del óvalo
- Divider diamante + descriptor NAIL STUDIO BOUTIQUE
- Fondo negro púrpura `#1A0F24` para mayor exclusividad nocturna

## Uso recomendado
Campañas editoriales, packaging limited edition o colección cápsula.
El monograma oficial permanece como marca primaria de reconocimiento.
"""
    (ROOT / "logos/logo-original-proposal/README.md").write_text(note, encoding="utf-8")
    (ROOT / "proposals/README.md").write_text(note, encoding="utf-8")


def comparison_board():
    """Side-by-side: official source | vector recreation | original proposal."""
    w, h = 1800, 900
    board = Image.new("RGBA", (w, h), PEARL + (255,))
    d = ImageDraw.Draw(board)
    d.text((60, 40), "THE NAIL HOUSE — Comparativa de marcas", font=font("playfair", 36), fill=PURPLE)
    d.text((60, 95), "Oficial  ·  Recreación vectorial  ·  Propuesta original", font=font("montserrat-light", 16), fill=LILA)

    panels = [
        (ROOT / "logos/logo-official/official-source.jpg", "A. Logo oficial (referencia)", 60),
        (ROOT / "logos/logo-official/logo-monogram.jpg", "B. Recreación del sistema", 620),
        (ROOT / "logos/logo-original-proposal/logo-original.jpg", "C. Propuesta original", 1180),
    ]
    for path, label, x in panels:
        if path.exists():
            im = Image.open(path).convert("RGB")
            im = im.resize((500, 500), Image.Resampling.LANCZOS)
            board.paste(im, (x, 160))
        d.text((x, 690), label, font=font("montserrat-medium", 16), fill=PURPLE)

    d.text(
        (60, 780),
        "A y B: monograma TH oficial con anillo central.  C: interpretación propia (perla + trazo joya) — uso editorial / cápsula.",
        font=font("montserrat-light", 14),
        fill=LILA,
    )
    save(board, ROOT / "proposals/comparison-board.png")
    save(board, ROOT / "proposals/comparison-board.jpg", PEARL)


def main():
    export_official_set()
    export_oksana_style_card()
    export_original_proposal()
    comparison_board()
    print("✓ Monogram v2 + original proposal exported")


if __name__ == "__main__":
    main()
