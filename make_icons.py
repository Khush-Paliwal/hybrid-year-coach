"""Draw the app icons: a blue bumper plate on graphite, with a safe-zone version for Android's maskable icon."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
BG, PLATE, HUB, SLEEVE = (15, 19, 23), (74, 141, 247), (233, 237, 241), (143, 154, 166)


def draw(size, plate_frac, rounded):
    s = size * 4  # supersample, then downscale for smooth edges
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if rounded:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.22), fill=BG)
    else:
        d.rectangle([0, 0, s, s], fill=BG)
    c, r = s / 2, s * plate_frac / 2
    bar_h = s * 0.07
    d.rounded_rectangle([s * 0.06, c - bar_h / 2, s * 0.94, c + bar_h / 2], radius=int(bar_h / 2), fill=SLEEVE)
    d.ellipse([c - r, c - r, c + r, c + r], fill=PLATE)
    d.ellipse([c - r * 0.78, c - r * 0.78, c + r * 0.78, c + r * 0.78], outline=BG, width=int(s * 0.012))
    d.ellipse([c - r * 0.28, c - r * 0.28, c + r * 0.28, c + r * 0.28], fill=HUB)
    d.ellipse([c - r * 0.12, c - r * 0.12, c + r * 0.12, c + r * 0.12], fill=BG)
    return img.resize((size, size), Image.LANCZOS)


(ROOT / "icons").mkdir(exist_ok=True)
draw(192, 0.62, True).save(ROOT / "icons" / "icon-192.png")
draw(512, 0.62, True).save(ROOT / "icons" / "icon-512.png")
draw(512, 0.46, False).save(ROOT / "icons" / "icon-maskable-512.png")
print("icons written")
