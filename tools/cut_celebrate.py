"""從 Codex 生的待命 GIF 切出「握拳慶祝」影格：去綠幕、以腳底對齊、輸出序列與 sprite sheet。

用法：python -I tools/cut_celebrate.py
輸入：assets/raw/anim-3.gif
輸出：assets/anim/celebrate_XX.png、celebrate_sheet.png、celebrate.json、celebrate_preview.png
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cut_sprites import key_green  # noqa: E402  共用同一套萊姆綠安全的去背

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "raw" / "anim-3.gif"
OUT = ROOT / "assets" / "anim"

# GIF 第 3–7 格：放鬆 → 握拳上提（動態線）→ 瞇眼用力 → 握拳收回 → 回到放鬆
FRAMES = [3, 4, 5, 6, 7]
# 原檔每格 180ms 太慢；改成有預備、有停頓的節奏（ms）
TIMING = [70, 80, 260, 120, 110]


def feet_anchor(alpha):
    """以最底下 12 列（鞋底）的不透明像素算 x 中心與底線，當對齊錨點。"""
    ys = np.nonzero(alpha.max(axis=1) > 128)[0]
    bottom = ys.max()
    band = alpha[bottom - 12:bottom + 1] > 128
    xs = np.nonzero(band.any(axis=0))[0]
    return (xs.min() + xs.max()) / 2, bottom


def main():
    gif = Image.open(SRC)
    frames = []
    for i in FRAMES:
        gif.seek(i)
        rgba, _ = key_green(gif.convert("RGB"))
        frames.append(rgba)

    anchors = [feet_anchor(f[..., 3]) for f in frames]
    ax = np.mean([a[0] for a in anchors])
    ay = max(a[1] for a in anchors)

    # 每格平移到同一個腳底錨點，消除 AI 影格的位置跳動
    h, w = frames[0].shape[:2]
    aligned = []
    for f, (fx, fy) in zip(frames, anchors):
        dx, dy = int(round(ax - fx)), int(round(ay - fy))
        canvas = np.zeros_like(f)
        ys0, ys1 = max(0, dy), min(h, h + dy)
        xs0, xs1 = max(0, dx), min(w, w + dx)
        canvas[ys0:ys1, xs0:xs1] = f[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx]
        aligned.append(canvas)

    # 所有影格共用同一個裁切框（含動態線），讓序列尺寸一致
    union = np.zeros((h, w), bool)
    for f in aligned:
        union |= f[..., 3] > 0
    ys, xs = np.nonzero(union)
    pad = 4
    y0, y1 = max(0, ys.min() - pad), min(h, ys.max() + pad + 1)
    x0, x1 = max(0, xs.min() - pad), min(w, xs.max() + pad + 1)

    OUT.mkdir(parents=True, exist_ok=True)
    cells = []
    for n, f in enumerate(aligned):
        im = Image.fromarray(f[y0:y1, x0:x1])
        im.save(OUT / f"celebrate_{n:02d}.png")
        cells.append(im)

    cw, ch = cells[0].size
    sheet = Image.new("RGBA", (cw * len(cells), ch), (0, 0, 0, 0))
    for n, im in enumerate(cells):
        sheet.paste(im, (n * cw, 0))
    sheet.save(OUT / "celebrate_sheet.png")

    meta = {
        "frameWidth": cw, "frameHeight": ch, "frames": len(cells),
        "durations": TIMING, "loop": False,
        # 腳底中心在影格內的位置：程式用它把動畫放在角色站的地方
        "anchor": {"x": round(ax - x0, 1), "y": int(ay - y0)},
        "source": f"anim-3.gif frames {FRAMES}",
    }
    (OUT / "celebrate.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    # 檢查用：深色底並排
    prev = Image.new("RGBA", (cw * len(cells), ch), (24, 32, 42, 255))
    for n, im in enumerate(cells):
        prev.paste(im, (n * cw, 0), im)
    prev.save(OUT / "celebrate_preview.png")
    print(meta)


if __name__ == "__main__":
    main()
