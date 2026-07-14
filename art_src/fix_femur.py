#!/usr/bin/env python3
"""Femur: u2net keeps the full solid bone but leaves a soft dark-leather bg.
Combine u2net mask AND a luminance key (bone is pale, leather is dark) so the
whole bone survives and the leather is dropped. Then feather+erode the edge."""
import os
from PIL import Image, ImageChops, ImageFilter
from rembg import remove, new_session

SRC = r"D:\Dev\BoneCrush\art_src\pieces_sheet.png"
ASSETS = r"D:\Dev\BoneCrush\assets"
CANVAS, PAD = 128, 6
LUMA_CUT = 70   # pixels darker than this (leather shadow) -> transparent

sheet = Image.open(SRC).convert("RGB")
session = new_session("u2net")
box = (275, 25, 510, 255)


def process(crop):
    cut = remove(crop, session=session).convert("RGBA")
    r, g, b, a = cut.split()
    rgb = cut.convert("RGB")
    luma = rgb.convert("L")
    # luminance mask: bone (pale) -> keep, dark leather -> drop.
    # smoothstep-ish: below LUMA_CUT scales to 0, above ramps to 255 over 40 levels
    def lum_map(v):
        if v <= LUMA_CUT:
            return 0
        if v >= LUMA_CUT + 40:
            return 255
        return int((v - LUMA_CUT) / 40 * 255)
    lmask = luma.point(lum_map)
    # final alpha = u2net alpha AND luminance mask
    a2 = ImageChops.multiply(a, lmask)
    a2 = a2.point(lambda v: 255 if v > 90 else (0 if v < 30 else v))
    # 1px erode to kill any residual halo
    a_er = a2.filter(ImageFilter.MinFilter(3))
    a2 = ImageChops.darker(a2, a_er)
    return Image.merge("RGBA", (r, g, b, a2))


def autocrop(img):
    bb = img.split()[3].getbbox()
    return img.crop(bb) if bb else img


def fit_center(img):
    target = CANVAS - 2 * PAD
    w, h = img.size
    scale = min(target / w, target / h)
    nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
    img = img.resize((nw, nh), Image.LANCZOS)
    out = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    out.paste(img, ((CANVAS - nw) // 2, (CANVAS - nh) // 2), img)
    return out


crop = sheet.crop(box)
cut = process(crop)
cut = autocrop(cut)
final = fit_center(cut)
out = os.path.join(ASSETS, "femur.png")
final.save(out)
print("femur redone (u2net + luma key) trimmed=", cut.size, "->", out)
