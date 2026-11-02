"""Generate one language-specific banner image per README.

The banner text used to live inside a single English-only PNG, so the
Simplified and Traditional Chinese pages still showed English. The banner is
now drawn from `data/project.json`, one image per language.
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 1200, 440
OUTPUTS = {"zh-CN": "assets/banner.zh-CN.png",
           "zh-TW": "assets/banner.zh-TW.png",
           "en": "assets/banner.en.png"}
FONT_CANDIDATES = {
    "zh-CN": ["msyh.ttc", "msyhbd.ttc", "simhei.ttf"],
    "zh-TW": ["msjh.ttc", "msjhbd.ttc", "msyh.ttc"],
    "en": ["segoeuib.ttf", "arialbd.ttf", "arial.ttf"],
}


def load_font(names, size):
    for name in names:
        path = Path("C:/Windows/Fonts") / name
        if path.is_file():
            try:
                return ImageFont.truetype(str(path), size)
            except OSError:
                continue
    return ImageFont.load_default()


def draw_gradient():
    image = Image.new("RGB", (WIDTH, HEIGHT), "#0b1020")
    pixels = image.load()
    for x in range(WIDTH):
        ratio = x / (WIDTH - 1)
        red = int(11 + ratio * 60)
        green = int(16 + ratio * 10)
        blue = int(32 + ratio * 150)
        for y in range(HEIGHT):
            pixels[x, y] = (red, green, blue)
    return image


def draw_grid(image):
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    pen = ImageDraw.Draw(overlay)
    for x in range(0, WIDTH, 40):
        pen.line([(x, 0), (x, HEIGHT)], fill=(255, 255, 255, 12), width=1)
    for y in range(0, HEIGHT, 40):
        pen.line([(0, y), (WIDTH, y)], fill=(255, 255, 255, 10), width=1)
    for x in range(0, WIDTH, 40):
        pen.line([(x, 0), (x, HEIGHT)], fill=(120, 90, 255, 26), width=1)
    return Image.alpha_composite(image.convert("RGBA"), overlay)


def draw_glow(image):
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    pen = ImageDraw.Draw(glow)
    pen.ellipse([WIDTH * 0.45, -HEIGHT * 0.55, WIDTH * 1.25, HEIGHT * 0.95],
                fill=(120, 70, 255, 70))
    glow = glow.filter(__import__("PIL.ImageFilter", fromlist=["ImageFilter"]).GaussianBlur(140))
    return Image.alpha_composite(image, glow)


def centered(pen, text, font, y, fill):
    box = pen.textbbox((0, 0), text, font=font)
    pen.text(((WIDTH - (box[2] - box[0])) / 2 - box[0], y), text, font=font, fill=fill)


def render(language, title, tagline):
    image = draw_glow(draw_grid(draw_gradient()))
    pen = ImageDraw.Draw(image)
    title_font = load_font(FONT_CANDIDATES[language], 96)
    tagline_font = load_font(FONT_CANDIDATES[language], 34)
    centered(pen, title, title_font, 140, (255, 255, 255, 255))
    centered(pen, tagline, tagline_font, 280, (225, 230, 245, 255))
    return image.convert("RGB")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="Fail when a banner image is out of date")
    arguments = parser.parse_args()
    import json
    data = json.loads((ROOT / "data/project.json").read_text(encoding="utf-8-sig"))
    stale = []
    for language, relative in OUTPUTS.items():
        image = render(language, data["titles"][language], data["tagline"][language])
        target = ROOT / relative
        if arguments.check:
            if not target.is_file() or target.stat().st_size == 0:
                stale.append(relative)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        image.save(target, "PNG", optimize=True)
        print(f"Wrote {relative}")
    if stale:
        print(f"Out of date: {', '.join(stale)}. Run scripts/make_banner.py.", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
