"""把生圖切成零件 PNG（去背 + 自動分割 + 依列命名）。

用法：python -I tools/cut_sprites.py
輸入：assets/raw/parts-green.webp（綠幕零件）、assets/raw/sheet.webp（奶油底總表）
輸出：assets/parts/、assets/expr/、assets/props/、assets/turnaround/
"""
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "assets" / "raw"


def components(fg, min_px):
    """4-連通標記，回傳每塊的 bbox (x0,y0,x1,y1) 與像素數。"""
    h, w = fg.shape
    seen = np.zeros_like(fg, dtype=bool)
    labels = np.zeros(fg.shape, np.int32)
    out = []
    ys, xs = np.nonzero(fg)
    for y, x in zip(ys, xs):
        if seen[y, x]:
            continue
        q = deque([(y, x)])
        seen[y, x] = True
        cid = len(out) + 1
        pix = []
        x0 = x1 = x
        y0 = y1 = y
        n = 0
        while q:
            cy, cx = q.popleft()
            pix.append((cy, cx))
            n += 1
            x0, x1, y0, y1 = min(x0, cx), max(x1, cx), min(y0, cy), max(y1, cy)
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < h and 0 <= nx < w and fg[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    q.append((ny, nx))
        if n >= min_px:
            ys_, xs_ = zip(*pix)
            labels[list(ys_), list(xs_)] = cid
            out.append([x0, y0, x1, y1, {cid}])
    components.labels = labels
    return out


def merge_boxes(boxes, margin):
    """擴張後相交的 bbox 合併（汗滴、碎片、被箭穿過的兩段算同一個物件）。"""
    boxes = [b[:4] + [set(b[4])] for b in boxes]
    changed = True
    while changed:
        changed = False
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if (a[0] - margin <= b[2] and b[0] - margin <= a[2]
                        and a[1] - margin <= b[3] and b[1] - margin <= a[3]):
                    boxes[i] = [min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]), a[4] | b[4]]
                    boxes.pop(j)
                    changed = True
                    break
            if changed:
                break
    return boxes


def group_sheet(boxes, big_area=6000):
    """總表專用：大塊各自獨立（頭與頭可能只隔 1–2px，不能用 bbox 合併）；
    小塊（汗滴等）若落在大塊範圍內就併入，否則小塊彼此聚成一組（氣球爆炸碎片）。"""
    area = lambda b: (b[2] - b[0]) * (b[3] - b[1])
    big = [b[:4] + [set(b[4])] for b in boxes if area(b) >= big_area]
    small = [b for b in boxes if area(b) < big_area]
    loose = []
    for s in small:
        host = next((g for g in big if s[0] >= g[0] - 5 and s[2] <= g[2] + 5
                     and s[1] <= g[3] and s[3] >= g[1] - 30), None)
        if host:
            host[:] = [min(host[0], s[0]), min(host[1], s[1]), max(host[2], s[2]), max(host[3], s[3]), host[4] | s[4]]
        else:
            loose.append(s)
    return big + merge_boxes(loose, 60)


def rows_of(boxes, gap):
    """依 y 中心分列，列內依 x 排序。"""
    boxes = sorted(boxes, key=lambda b: (b[1] + b[3]) / 2)
    rows, cur, last = [], [], None
    for b in boxes:
        cy = (b[1] + b[3]) / 2
        if last is not None and cy - last > gap:
            rows.append(sorted(cur, key=lambda b: b[0]))
            cur = []
        cur.append(b)
        last = cy
    if cur:
        rows.append(sorted(cur, key=lambda b: b[0]))
    return rows


def save(rgba, box, path, pad=4):
    h, w = rgba.shape[:2]
    x0, y0 = max(0, box[0] - pad), max(0, box[1] - pad)
    x1, y1 = min(w, box[2] + pad + 1), min(h, box[3] + pad + 1)
    path.parent.mkdir(parents=True, exist_ok=True)
    crop = rgba[y0:y1, x0:x1].copy()
    own = np.isin(components.labels[y0:y1, x0:x1], list(box[4]))
    # 只保留自己這組的像素（加 2px 邊，保住抗鋸齒邊緣），鄰居的碎片清掉
    grow = own.copy()
    for _ in range(2):
        g2 = grow.copy()
        g2[1:] |= grow[:-1]; g2[:-1] |= grow[1:]; g2[:, 1:] |= grow[:, :-1]; g2[:, :-1] |= grow[:, 1:]
        grow = g2
    other = (components.labels[y0:y1, x0:x1] > 0) & ~own
    crop[..., 3] = np.where(grow & ~other, crop[..., 3], 0)
    Image.fromarray(crop).save(path)
    return path.relative_to(ROOT).as_posix()


def key_green(img):
    a = np.asarray(img.convert("RGB")).astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    spill = g - np.maximum(r, b)                 # 綠色優勢量
    # 萊姆綠 #C6FF00 的綠色優勢只有 ~57，背景 #00FF00 約 200+：100 以下全保留，160 以上全透明
    alpha = np.clip(255 - (spill.astype(np.float32) - 100) * 255 / 60, 0, 255).astype(np.uint8)
    rgb = a.copy()
    edge = (alpha < 255) & (spill > 0)           # 去綠溢色：邊緣的 g 壓到 max(r,b)
    rgb[..., 1] = np.where(edge, np.maximum(r, b), g)
    rgba = np.dstack([rgb.astype(np.uint8), alpha])
    return rgba, alpha > 128


def key_border_flood(img, tol=38):
    """奶油底：只把「和邊框相連、顏色接近底色」的區域當背景（臉也是奶油色，不能單純用顏色去）。"""
    a = np.asarray(img.convert("RGB")).astype(np.int16)
    h, w = a.shape[:2]
    bg_col = np.median(np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]), axis=0)
    near = np.abs(a - bg_col).sum(axis=2) < tol
    bg = np.zeros((h, w), bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if near[y, x] and not bg[y, x]:
                bg[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if near[y, x] and not bg[y, x]:
                bg[y, x] = True; q.append((y, x))
    while q:
        cy, cx = q.popleft()
        for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
            if 0 <= ny < h and 0 <= nx < w and near[ny, nx] and not bg[ny, nx]:
                bg[ny, nx] = True; q.append((ny, nx))
    # 去奶油色光暈：與背景相鄰、顏色偏底色的邊緣像素再剝兩層
    halo = np.abs(a - bg_col).sum(axis=2) < tol * 3
    for _ in range(2):
        nb = np.zeros_like(bg)
        nb[1:] |= bg[:-1]; nb[:-1] |= bg[1:]; nb[:, 1:] |= bg[:, :-1]; nb[:, :-1] |= bg[:, 1:]
        bg = bg | (nb & halo)
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    rgba = np.dstack([a.astype(np.uint8), alpha])
    return rgba, ~bg


def main():
    report = []

    # ---- 綠幕零件 ----
    rgba, fg = key_green(Image.open(RAW / "parts-green.webp"))
    boxes = merge_boxes(components(fg, 400), 6)
    rows = rows_of(boxes, 120)
    names = [["head_side", "head_front", "jacket", "hat"],
             ["quiver", "hand_open", "hand_fist", "hand_grip", "hand_pinch"],
             ["shoe", "bow", "arrow"]]
    report.append(f"parts-green: {[len(r) for r in rows]} (expect {[len(n) for n in names]})")
    for r, row in enumerate(rows):
        for c, box in enumerate(row):
            name = names[r][c] if r < len(names) and c < len(names[r]) else f"r{r}c{c}"
            report.append("  " + save(rgba, box, ROOT / "assets" / "parts" / f"{name}.png"))

    # ---- 總表（轉面、表情、物品；第 3 列零件用綠幕版，略過） ----
    rgba, fg = key_border_flood(Image.open(RAW / "sheet.webp"))
    boxes = group_sheet(components(fg, 30))
    rows = rows_of(boxes, 90)
    report.append(f"sheet: {[len(r) for r in rows]} (expect [4, 8, ~9, 6])")
    plan = [("turnaround", ["front", "three_quarter", "side", "back"]),
            ("expr", ["chill", "aim", "asleep", "laugh", "startled", "bored", "dizzy", "locked_in"]),
            (None, []),
            ("props", ["apple", "balloon", "bug", "apple_hit", "bug_hit", "balloon_pop"])]
    for r, row in enumerate(rows):
        folder, nm = plan[r] if r < len(plan) else ("extra", [])
        if folder is None:
            continue
        for c, box in enumerate(row):
            name = nm[c] if c < len(nm) else f"r{r}c{c}"
            report.append("  " + save(rgba, box, ROOT / "assets" / folder / f"{name}.png"))

    print("\n".join(report))


if __name__ == "__main__":
    main()
