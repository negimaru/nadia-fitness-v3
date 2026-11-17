"""Generate placeholder images for classes without a photo (assets/img/clases/<slug>.webp).

Usage (from the repo root): python3 tools/make_placeholders.py
To use a real photo, overwrite the file with the same name (landscape, ~1200x750).
Style follows DESIGN.md: flat warm dark, one accent line, no gradients or glows.
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, "assets/fonts/bricolage-grotesque-latin.woff2")
W, H = 1200, 750
BG = (22, 18, 15)          # --dark
INK = (242, 238, 232)      # dark-theme --ink
MUTED = (168, 162, 158)    # dark-theme --muted
ACCENT = (255, 90, 168)    # dark-theme --accent
LINE = (54, 49, 44)        # dark-theme --line


def font(size, weight, width=92):
    f = ImageFont.truetype(FONT, size)
    try:
        axes = {a["name"]: a for a in f.get_variation_axes()}
        values = []
        for a in f.get_variation_axes():
            n = a["name"].decode() if isinstance(a["name"], bytes) else a["name"]
            values.append({"Weight": weight, "Width": width}.get(n, a["default"]))
        f.set_variation_by_axes(values)
    except Exception:
        pass
    return f


def make(slug, name, group):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((24, 24, W - 25, H - 25), outline=LINE, width=2)       # quiet frame
    label = font(30, 600)
    title = font(96 if len(name) < 18 else 80, 700)
    small = font(26, 500)
    d.text((80, 80), group.upper(), font=label, fill=MUTED)
    d.rectangle((80, 128, 176, 132), fill=ACCENT)
    # class name, wrapped to two lines at most, bottom-left like a poster caption
    words, lines, cur = name.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textlength(test, font=title) > W - 160 and cur:
            lines.append(cur); cur = w
        else:
            cur = test
    lines.append(cur)
    y = H - 110 - len(lines) * title.size * 1.05
    for line in lines:
        d.text((80, y), line, font=title, fill=INK)
        y += title.size * 1.05
    d.text((80, H - 96), "Nadia Fitness Dance Studio · Torrox Costa", font=small, fill=MUTED)
    out = os.path.join(ROOT, "assets/img/clases", f"{slug}.webp")
    im.save(out, "WEBP", quality=86, method=6)
    print("wrote", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    data = json.load(open(os.path.join(ROOT, "data/site.json"), encoding="utf-8"))
    for c in data["classes"]:
        if c.get("placeholder"):
            make(c["c"], c["name"], "Baile" if c["group"] == "baile" else "Fitness")
