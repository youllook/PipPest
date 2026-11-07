"""把 assets 下切好的 PNG 拼成一張棋盤格底的檢視圖：assets/contact.png"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent / "assets"
GROUPS = ["parts", "expr", "props", "turnaround"]
CELL, PAD = 170, 8

def checker(w, h, s=12):
    im = Image.new("RGB", (w, h), (58, 70, 84))
    d = ImageDraw.Draw(im)
    for y in range(0, h, s):
        for x in range(0, w, s):
            if (x // s + y // s) % 2:
                d.rectangle([x, y, x + s - 1, y + s - 1], fill=(40, 50, 62))
    return im

files = [(g, p) for g in GROUPS for p in sorted((ROOT / g).glob("*.png"))]
cols = 7
rows = (len(files) + cols - 1) // cols
sheet = checker(cols * (CELL + PAD) + PAD, rows * (CELL + 20 + PAD) + PAD)
d = ImageDraw.Draw(sheet)
for i, (g, p) in enumerate(files):
    im = Image.open(p).convert("RGBA")
    im.thumbnail((CELL, CELL))
    x = PAD + (i % cols) * (CELL + PAD)
    y = PAD + (i // cols) * (CELL + 20 + PAD)
    sheet.paste(im, (x + (CELL - im.width) // 2, y + (CELL - im.height) // 2), im)
    d.text((x, y + CELL + 4), f"{g}/{p.stem}", fill=(230, 238, 245))
sheet.save(ROOT / "contact.png")
print(sheet.size, len(files))
