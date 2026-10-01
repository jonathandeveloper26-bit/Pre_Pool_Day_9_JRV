"""Generate 26 extruded 3-D capital letters (A-Z) as transparent PNGs for pygame."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import os, string

OUT_DIR   = "letters_3d"
SIZE      = 128          # final sprite size (square)
SS        = 2            # supersampling factor for smooth edges
FONT_PATH = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"

# Palette
FACE      = (255, 210, 63)      # bright yellow face
HIGHLIGHT = (255, 243, 170)     # top-left bevel
EXT_TOP   = (214, 128, 30)      # extrusion colour near the face
EXT_BOT   = (110, 56, 10)       # extrusion colour at the far end
OUTLINE   = (50, 28, 6)         # thin dark outline

DEPTH     = 11                  # extrusion depth in final pixels
STROKE    = 2                   # outline width in final pixels
BEVEL     = 3                   # highlight band width in final pixels


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def render_letter(ch):
    W = SIZE * SS
    font = ImageFont.truetype(FONT_PATH, int(W * 0.68))
    img = Image.new("RGBA", (W, W), (0, 0, 0, 0))

    # Measure glyph and centre it, leaving room for the extrusion to the bottom-right
    bbox = font.getbbox(ch)
    gw, gh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    depth = DEPTH * SS
    x = (W - gw - depth) // 2 - bbox[0]
    y = (W - gh - depth) // 2 - bbox[1]
    stroke = STROKE * SS

    # Soft drop shadow
    shadow = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((x + depth + 4 * SS, y + depth + 6 * SS), ch,
                                font=font, fill=(0, 0, 0, 110),
                                stroke_width=stroke, stroke_fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(4 * SS))
    img.alpha_composite(shadow)

    # Silhouette of the whole solid in the outline colour (gives one clean outline)
    draw = ImageDraw.Draw(img)
    for i in range(depth, -1, -1):
        draw.text((x + i, y + i), ch, font=font, fill=OUTLINE,
                  stroke_width=stroke, stroke_fill=OUTLINE)

    # Extrusion sides: stack the glyph from far (dark) to near (lighter), no stroke
    for i in range(depth, 0, -1):
        t = i / depth
        col = lerp(EXT_TOP, EXT_BOT, t)
        draw.text((x + i, y + i), ch, font=font, fill=col)

    # Face with outline
    draw.text((x, y), ch, font=font, fill=FACE,
              stroke_width=stroke, stroke_fill=OUTLINE)

    # Bevel highlight: face mask minus the face shifted down-right
    mask_face = Image.new("L", (W, W), 0)
    ImageDraw.Draw(mask_face).text((x, y), ch, font=font, fill=255)
    mask_shift = Image.new("L", (W, W), 0)
    b = BEVEL * SS
    ImageDraw.Draw(mask_shift).text((x + b, y + b), ch, font=font, fill=255)
    band = ImageChops.subtract(mask_face, mask_shift)
    hl = Image.new("RGBA", (W, W), HIGHLIGHT + (0,))
    hl.putalpha(band)
    img.alpha_composite(hl)

    return img.resize((SIZE, SIZE), Image.LANCZOS)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    sprites = []
    for ch in string.ascii_uppercase:
        im = render_letter(ch)
        im.save(os.path.join(OUT_DIR, f"{ch}.png"))
        sprites.append(im)

    # Contact sheet for a quick look
    cols, pad = 7, 8
    rows = (len(sprites) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * (SIZE + pad) + pad, rows * (SIZE + pad) + pad), (30, 34, 48, 255))
    for i, im in enumerate(sprites):
        r, c = divmod(i, cols)
        sheet.alpha_composite(im, (pad + c * (SIZE + pad), pad + r * (SIZE + pad)))
    sheet.save("letters_preview.png")
    print(f"Wrote {len(sprites)} sprites to {OUT_DIR}/ and letters_preview.png")


if __name__ == "__main__":
    main()
