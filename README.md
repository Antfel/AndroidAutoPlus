# THE NAIL HOUSE — Identidad Visual

**Luxury Purple & Gold** · Nail Studio Boutique

Identidad visual completa para un estudio de manicura en casa: monograma TH en óvalo dorado, paleta morado/dorado, sistema de logos, aplicaciones impresas, Instagram y manual de marca.

## Ver la marca

Abre `brand/index.html` en el navegador para el showcase, o `brand/brand-guidelines/index.html` / el PDF del manual.

## Estructura

```
brand/
├── logos/              # Principal, isotipo, horizontal, secundario, monocromo (SVG/PNG/JPG)
├── colors/             # Paleta, colors.css, colors.json
├── typography/         # Especímenes + fuentes TTF
├── social-media/       # Perfil, highlights, plantillas IG
├── business-cards/     # Tarjetas de presentación
├── appointments/       # Citas y fidelización
├── price-list/         # Lista de precios
├── packaging/          # Stickers, etiquetas, bolsa
├── mockups/            # Uniforme, letrero, estudio
├── brand-guidelines/   # Manual HTML + PDF
├── scripts/            # Generador de assets
└── index.html          # Showcase visual
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

El símbolo **TH** dentro del óvalo dorado es el elemento principal de reconocimiento. No reemplazar, no cambiar iniciales, no eliminar el óvalo, no añadir coronas, flores, manos ni esmaltes.

## Regenerar assets

```bash
python3 brand/scripts/generate_brand.py
```

Requiere las fuentes en `/tmp/fonts` (Playfair Display + Montserrat) y `Pillow` + `reportlab`.
