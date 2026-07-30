#!/usr/bin/env python3
"""Slice pieces_sheet.png into transparent, trimmed, centered 128x128 sprites."""
import os
import io
import sys
from PIL import Image, ImageChops
from rembg import remove, new_session

SRC = r"D:\Dev\BoneCrush\art_src\pieces_sheet.png"
# Second asset drop (2026-07-11): "Bon crush assets 02" sheet, 2066x2048
SRC2 = r"D:\Dev\BoneCrush\art_src\pieces_sheet_02.png"
ASSETS = r"D:\Dev\BoneCrush\assets"
TMP = r"D:\Dev\BoneCrush\art_src\_tmp_crops"
EVID = r"C:\Users\MiSTRFiNGA\Desktop\Tests\BoneCrush_gfx"

CANVAS = 128
PAD = 6          # px of transparent padding inside canvas
ALPHA_THRESH = 20  # pixels with alpha below this become fully transparent (kills dark fringe)
ERODE = True

# (name, (x0,y0,x1,y1)) crop boxes on the 1024x1015 sheet
ITEMS = [
    ("skull",      (15, 15, 275, 275)),
    ("femur",      (275, 25, 510, 255)),
    ("femur_alt",  (505, 90, 780, 215)),
    ("crossbones", (770, 15, 1015, 255)),
    ("ribcage",    (10, 315, 370, 725)),
    ("gem",        (445, 385, 675, 660)),
    ("hand",       (800, 335, 1010, 710)),
    ("key",        (15, 745, 255, 1010)),
    ("coin",       (270, 755, 510, 1000)),
    ("potion",     (575, 735, 720, 1010)),
    ("eyeball",    (785, 765, 995, 985)),
]

# (name, (x0,y0,x1,y1)) crop boxes on the 2066x2048 sheet 02.
# "circle" flag = punch a circular alpha mask instead of rembg (moon sits on a starry sky).
ITEMS2 = [
    ("moon",      (836, 26, 1203, 381)),      # full moon (special: wolf howl)
    ("voodoo",    (1689, 484, 2003, 932)),    # voodoo doll (reserved)
    ("cross",     (77, 1092, 355, 1488)),     # crucifix (special: holy blast)
    ("eyecoin",   (793, 1020, 1071, 1282)),   # occult eye coin (alt coin art, reserved)
    ("book",      (1524, 1015, 1962, 1329)),  # spellbook (reserved)
    ("coffin",    (494, 1303, 979, 1633)),    # coffin (reserved)
    ("knife",     (1080, 560, 1245, 1300)),   # bloody knife, vertical w/ handle (special: slash)
    ("cauldron",  (88, 1488, 469, 1988)),     # cauldron (NEW normal piece)
    ("heart",     (762, 1535, 1231, 1988)),   # anatomical heart (NEW normal piece)
    ("blackcat",  (1329, 1509, 1705, 1993)),  # black cat (NEW normal piece)
    ("fingerjar", (1751, 1473, 2024, 1993)),  # finger in jar (special: glass shatter)
]
CIRCLE_MASK = {"moon"}   # items cut with a circular mask instead of rembg
NO_MATTING = {"knife"}   # alpha matting + erode eats the dark handle; plain rembg keeps it

os.makedirs(ASSETS, exist_ok=True)
os.makedirs(TMP, exist_ok=True)
os.makedirs(EVID, exist_ok=True)

session = new_session("isnet-general-use")

# usage: slice_pieces.py [sheet1|sheet2|all] [name filter...]
MODE = sys.argv[1] if len(sys.argv) > 1 else "all"
ONLY = set(sys.argv[2:])


def clean_alpha(img):
    """Threshold + optional 1px erosion of alpha to remove dark halo fringe."""
    img = img.convert("RGBA")
    r, g, b, a = img.split()
    # threshold: kill near-transparent fringe pixels
    a = a.point(lambda v: 0 if v < ALPHA_THRESH else v)
    if ERODE:
        from PIL import ImageFilter
        # MinFilter erodes the alpha mask by ~1px, trimming edge halo
        a_er = a.filter(ImageFilter.MinFilter(3))
        a = ImageChops.darker(a, a_er)
    return Image.merge("RGBA", (r, g, b, a))


def autocrop_alpha(img):
    bbox = img.split()[3].getbbox()
    if bbox:
        return img.crop(bbox)
    return img


def fit_center(img, canvas=CANVAS, pad=PAD):
    target = canvas - 2 * pad
    w, h = img.size
    scale = min(target / w, target / h, 1.0) if max(w, h) > target else min(target / w, target / h)
    nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
    img = img.resize((nw, nh), Image.LANCZOS)
    out = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    out.paste(img, ((canvas - nw) // 2, (canvas - nh) // 2), img)
    return out


def circle_cut(crop):
    """Circular alpha mask (for the moon: rembg can't separate glow from night sky)."""
    from PIL import ImageDraw
    w, h = crop.size
    d = min(w, h)
    cxc, cyc = w // 2, h // 2
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse((cxc - d//2, cyc - d//2, cxc + d//2, cyc + d//2), fill=255)
    out = crop.convert("RGBA")
    out.putalpha(mask)
    return out


def process(sheet, items, tag):
    results = {}
    for name, box in items:
        if ONLY and name not in ONLY:
            continue
        crop = sheet.crop(box)
        crop_path = os.path.join(TMP, f"{name}_crop.png")
        crop.save(crop_path)
        if name in CIRCLE_MASK:
            cut = circle_cut(crop)
        elif name in NO_MATTING:
            cut = remove(crop, session=session)   # plain rembg, gentle alpha threshold only
            img = cut.convert("RGBA")
            r, g, b, a = img.split()
            a = a.point(lambda v: 0 if v < 12 else v)
            cut = Image.merge("RGBA", (r, g, b, a))
        else:
            # rembg with alpha matting for cleaner edges on detailed structures
            cut = remove(
                crop,
                session=session,
                alpha_matting=True,
                alpha_matting_foreground_threshold=240,
                alpha_matting_background_threshold=15,
                alpha_matting_erode_size=3,
            )
            cut = clean_alpha(cut)
        cut = autocrop_alpha(cut)
        final = fit_center(cut)
        out_path = os.path.join(ASSETS, f"{name}.png")
        final.save(out_path)
        results[name] = (out_path, cut.size)
        print(f"[{tag}] {name:11s} crop={box} trimmed={cut.size} -> {out_path}")
    return results


total = 0
if MODE in ("sheet1", "all"):
    sheet = Image.open(SRC).convert("RGB")
    print("sheet1 size", sheet.size)
    total += len(process(sheet, ITEMS, "sheet1"))
if MODE in ("sheet2", "all"):
    sheet2 = Image.open(SRC2).convert("RGB")
    print("sheet2 size", sheet2.size)
    total += len(process(sheet2, ITEMS2, "sheet2"))

print("DONE", total)
