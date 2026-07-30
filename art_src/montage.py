#!/usr/bin/env python3
"""Montage the 11 final sprites on a checkerboard bg for transparency preview."""
import os
from PIL import Image, ImageDraw, ImageFont

ASSETS = r"D:\Dev\BoneCrush\assets"
EVID = r"C:\Users\MiSTRFiNGA\Desktop\Tests\BoneCrush_gfx"
NAMES = ["skull", "femur", "crossbones", "ribcage", "gem",
         "hand", "key", "coin", "potion", "eyeball", "femur_alt"]
CELL = 128
GAP = 12
COLS = 6
LABEL_H = 18
os.makedirs(EVID, exist_ok=True)


def checker(size, c1=(200, 200, 200), c2=(150, 150, 150), sq=16):
    img = Image.new("RGB", (size, size), c1)
    d = ImageDraw.Draw(img)
    for y in range(0, size, sq):
        for x in range(0, size, sq):
            if (x // sq + y // sq) % 2:
                d.rectangle([x, y, x + sq, y + sq], fill=c2)
    return img


rows = (len(NAMES) + COLS - 1) // COLS
W = COLS * CELL + (COLS + 1) * GAP
H = rows * (CELL + LABEL_H) + (rows + 1) * GAP
canvas = Image.new("RGB", (W, H), (40, 40, 45))
draw = ImageDraw.Draw(canvas)
try:
    font = ImageFont.truetype("arial.ttf", 13)
except Exception:
    font = ImageFont.load_default()

for i, name in enumerate(NAMES):
    r, c = divmod(i, COLS)
    x = GAP + c * (CELL + GAP)
    y = GAP + r * (CELL + LABEL_H + GAP)
    bg = checker(CELL)
    sprite = Image.open(os.path.join(ASSETS, f"{name}.png")).convert("RGBA")
    bg.paste(sprite, (0, 0), sprite)
    canvas.paste(bg, (x, y))
    draw.text((x + 2, y + CELL + 2), name, fill=(230, 230, 230), font=font)

out = os.path.join(EVID, "final_sprites_montage.png")
canvas.save(out)
print("montage ->", out, canvas.size)

# copy all 11 PNGs to evidence folder
import shutil
for name in NAMES:
    shutil.copy2(os.path.join(ASSETS, f"{name}.png"), os.path.join(EVID, f"{name}.png"))
print("copied 11 pngs to", EVID)
