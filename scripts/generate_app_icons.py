#!/usr/bin/env python3
"""Generate the production Shijian app icon set.

The icon is drawn as a crisp, square iOS artwork (the OS applies its own
rounded mask): a midnight glass field, a fine gold poetry book, and an
insight star. Pillow is the only runtime dependency.
"""
from __future__ import annotations

import json
import math
import pathlib
from typing import Dict, Iterable

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError as exc:  # pragma: no cover - imported in CI
    raise SystemExit(
        "Pillow is required to generate the app icons. Install it with 'pip install pillow'."
    ) from exc

ROOT = pathlib.Path(__file__).resolve().parents[1]
ICONSET_PATH = ROOT / "ChatGPTWebView/ChatGPTWebView/Assets.xcassets/AppIcon.appiconset"
CONTENTS_PATH = ICONSET_PATH / "Contents.json"
SOURCE_ICON_PATH = ROOT / "assets" / "icon_1024.png"
CANVAS = 1024


def load_images() -> Iterable[Dict[str, str]]:
    if not CONTENTS_PATH.exists():
        raise SystemExit(f"Missing Contents.json at {CONTENTS_PATH}")
    data = json.loads(CONTENTS_PATH.read_text(encoding="utf-8"))
    return data.get("images", [])


def make_icon() -> Image.Image:
    """Draw artwork at 1024px so all requested icon sizes share one master."""
    image = Image.new("RGB", (CANVAS, CANVAS), "#101a31")
    draw = ImageDraw.Draw(image)

    # Restrained navy-to-indigo background gradient.
    top = (32, 42, 76)
    bottom = (8, 20, 34)
    for y in range(CANVAS):
        t = y / (CANVAS - 1)
        color = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        draw.line((0, y, CANVAS, y), fill=color)

    # Soft color bloom behind the symbol; keep the outer silhouette calm.
    glow = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((185, 125, 855, 795), fill=(127, 112, 255, 76))
    gd.ellipse((350, 360, 950, 940), fill=(56, 205, 213, 38))
    glow = glow.filter(ImageFilter.GaussianBlur(125))
    image = Image.alpha_composite(image.convert("RGBA"), glow)
    draw = ImageDraw.Draw(image)

    # Thin inset glass edge, intentionally away from the system icon mask.
    draw.rounded_rectangle((94, 94, 930, 930), radius=190,
                           fill=(255, 255, 255, 9), outline=(224, 225, 255, 48), width=3)
    draw.rounded_rectangle((111, 111, 913, 913), radius=174,
                           outline=(158, 148, 255, 58), width=2)

    # Book shadow on its own blurred layer.
    shadow = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    book = [(274, 326), (311, 275), (493, 275), (512, 305),
            (531, 275), (713, 275), (750, 326), (750, 686),
            (712, 724), (536, 724), (512, 704), (488, 724),
            (312, 724), (274, 686)]
    sd.polygon([(x + 4, y + 22) for x, y in book], fill=(0, 0, 0, 140))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    image = Image.alpha_composite(image, shadow)
    draw = ImageDraw.Draw(image)

    gold = (225, 193, 126, 255)
    pale_gold = (255, 239, 198, 255)
    page = (18, 29, 49, 255)
    draw.polygon(book, fill=page, outline=gold)
    draw.line(book + [book[0]], fill=gold, width=15, joint="curve")

    # Page glow at the top and the central book fold.
    draw.arc((300, 270, 512, 372), start=180, end=360, fill=pale_gold, width=8)
    draw.arc((512, 270, 724, 372), start=180, end=360, fill=pale_gold, width=8)
    draw.line((512, 309, 512, 692), fill=(235, 208, 153, 215), width=8)

    # Minimal poetry strokes, with generous spacing for legibility when small.
    for x1, x2, y, alpha in [
        (350, 462, 393, 255),
        (350, 438, 451, 225),
        (350, 466, 509, 210),
        (350, 426, 567, 190),
        (562, 674, 393, 165),
        (562, 650, 451, 150),
        (562, 674, 509, 138),
        (562, 638, 567, 125),
    ]:
        draw.line((x1, y, x2, y), fill=(244, 220, 166, alpha), width=13)

    # Four-point insight star with a tiny highlight at its center.
    cx, cy = 676, 625
    star_points = []
    for i in range(8):
        angle = -math.pi / 2 + i * math.pi / 4
        radius = 116 if i % 2 == 0 else 31
        star_points.append((cx + math.cos(angle) * radius,
                            cy + math.sin(angle) * radius))
    star_glow = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    ImageDraw.Draw(star_glow).ellipse((cx - 130, cy - 130, cx + 130, cy + 130),
                                      fill=(242, 207, 135, 80))
    star_glow = star_glow.filter(ImageFilter.GaussianBlur(32))
    image = Image.alpha_composite(image, star_glow)
    draw = ImageDraw.Draw(image)
    draw.polygon(star_points, fill=(235, 207, 143, 255))
    draw.ellipse((cx - 11, cy - 11, cx + 11, cy + 11), fill=(255, 249, 226, 255))

    # One cool-toned glint balances the warm book and star.
    draw.ellipse((704, 342, 736, 374), fill=(115, 225, 222, 245))
    draw.ellipse((696, 334, 744, 382), outline=(115, 225, 222, 95), width=3)

    # Small seal-like finishing detail; abstract, without tiny unreadable text.
    draw.rounded_rectangle((697, 739, 790, 832), radius=24,
                           fill=(225, 193, 126, 25), outline=(232, 203, 143, 150), width=3)
    for y, x2 in [(767, 767), (786, 754), (805, 740)]:
        draw.line((720, y, x2, y), fill=(246, 220, 164, 220), width=5)

    return image.convert("RGB")


def generate_icon(master: Image.Image, size: int, destination: pathlib.Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    artwork = master if master.size == (size, size) else master.resize(
        (size, size), Image.Resampling.LANCZOS
    )
    artwork.save(destination, format="PNG", optimize=True)


def main() -> None:
    master = make_icon()
    # Keep the repository's 1024px master aligned with the actual Xcode icon.
    generate_icon(master, 1024, SOURCE_ICON_PATH)
    for entry in load_images():
        filename = entry.get("filename")
        size_value = entry.get("size")
        scale = entry.get("scale", "1x")
        if not filename or not size_value:
            continue
        pixel_size = round(float(size_value.split("x")[0]) * int(scale.rstrip("x")))
        generate_icon(master, pixel_size, ICONSET_PATH / filename)


if __name__ == "__main__":
    main()
