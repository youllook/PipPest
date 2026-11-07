# 潮版橡皮水管弓箭手：生圖提示詞（網頁版 image gen 2.6）

> **骨架不變、衣服換潮**：保留 1930s 橡皮水管的靈魂（派餅眼、水管手腳、白手套、粗黑線），
> 服裝換成現代潮流。這種「復古卡通 × 街頭潮牌」的混搭本身就是現在很紅的插畫路線。
>
> 用法：
> 1. 先把 **1A / 1B / 1C 三個造型都生一次**，挑一個最喜歡的。
> 2. 之後的 2、3、4 張都**附上挑中的那張當參考圖**（提示詞開頭已寫好那句）。
> 3. 不要寫 Disney、Mickey、Cuphead 等名稱；角色必須原創。

---

## 1A. 街頭潮牌（Streetwear）— 推薦

```
Character model sheet of an original cartoon character that fuses 1930s rubber hose animation with modern streetwear: a small, round, bean-shaped archer named "Pip".
Rubber hose DNA: pie-cut eyes, wide cheeky grin, thin noodle-like black arms and legs with no elbows or knees, white four-finger cartoon gloves.
Streetwear outfit: oversized boxy cropped puffer jacket, a black bucket hat pulled low, one small hoop earring,
baggy cargo shorts, huge chunky dad sneakers with thick soles, the quiver is a crossbody sling bag with arrows poking out,
a tiny arrow logo patch on the chest.
Palette: cream white, ink black, warm grey, and ONE acid lime green accent (#C6FF00) used only on the sneakers' soles, the arrow fletching and the logo.
Style: 2D hand-inked cel animation, thick clean black outlines, flat colors, no gradients, subtle vintage print grain.
Show the same character in 4 views side by side: front, 3/4 front, side profile (facing right), back.
Full body, cool relaxed standing pose, hands in pockets is fine. Plain flat cream background (#F4ECD8), no text, no ground shadows.
```

## 1B. 機能風（Techwear / Gorpcore）

```
Character model sheet of an original cartoon character that fuses 1930s rubber hose animation with techwear: a small, round, bean-shaped archer named "Pip".
Rubber hose DNA: pie-cut eyes, wide grin, thin noodle-like black arms and legs with no elbows or knees, white four-finger cartoon gloves.
Techwear outfit: matte black hooded windbreaker with straps and buckles, a utility chest rig with pockets, snow goggles pushed up on the hood,
carabiners hanging from the belt, tapered cargo pants, chunky trail-running shoes, the quiver is a cylindrical tactical tube on the back.
Palette: ink black, charcoal, cream white, and ONE safety orange accent (#FF5A1F) used only on zipper pulls, shoe laces and arrow fletching.
Style: 2D hand-inked cel animation, thick clean black outlines, flat colors, no gradients, subtle vintage print grain.
Show the same character in 4 views side by side: front, 3/4 front, side profile (facing right), back.
Full body, confident standing pose. Plain flat cream background (#F4ECD8), no text, no ground shadows.
```

## 1C. 滑板 Y2K

```
Character model sheet of an original cartoon character that fuses 1930s rubber hose animation with Y2K skater style: a small, round, bean-shaped archer named "Pip".
Rubber hose DNA: pie-cut eyes, wide grin, thin noodle-like black arms and legs with no elbows or knees, white four-finger cartoon gloves.
Skater outfit: a slouchy beanie with a pom-pom, small wraparound chrome sunglasses, an oversized graphic tee with a big target logo,
super baggy cargo pants, puffy skate shoes, the quiver is covered in stickers, a skateboard tucked under one arm.
Palette: cream white, ink black, baby blue, bubblegum pink, with chrome silver highlights on the sunglasses only.
Style: 2D hand-inked cel animation, thick clean black outlines, flat colors, no gradients, subtle vintage print grain.
Show the same character in 4 views side by side: front, 3/4 front, side profile (facing right), back.
Full body, playful standing pose. Plain flat cream background (#F4ECD8), no text, no ground shadows.
```

---

## 2. 零件拆分圖（給程式組裝用，最重要）

程式會自己畫「水管手腳」和弓弦，所以零件**不要畫手臂和腿**。

```
Use the attached character sheet as the exact character reference, same outfit, same palette.
A clean game asset parts sheet for this character, every part separated with generous spacing, nothing overlapping:
- head facing right (with its headwear and accessories), and head facing front
- torso only (the jacket/top + belt), NO arms, NO legs, facing right
- the headwear alone
- the quiver alone (in its streetwear form), with 3 arrows sticking out
- 4 white glove hands: open palm, fist, gripping a bow handle, pinching a bowstring
- 2 shoes: side view, facing right
- a modern recurve bow WITHOUT string, side view, vertical, matching the outfit's accent color
- a single arrow, horizontal, pointing right
Plain solid chroma green background (#00FF00), flat colors, thick black outlines, no shadows, no text, no labels.
Do NOT draw any arms or legs on the torso.
```

> 若網頁版支援透明背景，把背景那行改成 `transparent background`，省去去背。

## 3. 表情表（狀態機用）

```
Use the attached character sheet as the exact character reference, same headwear and accessories.
An expression sheet of this character's HEAD ONLY, facing right, 8 heads in a 4x2 grid, same size and alignment:
1 chill smirk, 2 focused squinting one eye (aiming), 3 asleep with eyes closed and a bubble,
4 big hype laugh, 5 startled with eyes wide and sweat drops, 6 bored half-lidded,
7 dizzy with spiral eyes, 8 locked-in determined gritted teeth.
Plain solid chroma green background (#00FF00), thick black outlines, flat colors, no text.
```

對應：1 待命｜2 思考／瞄準｜3 不在｜4 完成｜5 閃避｜6 無聊｜7 出錯｜8 執行（瘋狂連射）

## 4. 游標掛的物品

```
A game asset sheet that fuses 1930s rubber hose cartoon style with modern streetwear graphics,
thick black outlines, flat colors, pie-cut eyes on every object, using the same palette as the attached character:
- a red apple with a leaf, smirking
- a round balloon with a short knot, smiling nervously
- a small cartoon bug with six noodle legs and antennae, wearing a tiny cap backwards, grinning mischievously
- the same apple with an arrow stuck through it, dizzy spiral eyes
- the same bug with an arrow stuck through it, dizzy spiral eyes
- a popped balloon: a few torn rubber shreds and a puff of smoke
Each object separated with generous spacing. Plain solid chroma green background (#00FF00), no text.
```

---

## 交件檢查

- 每張都存原尺寸 PNG，放到 `assets/raw/`（我再切圖、去背、對位）。
- 風格跑掉（變 3D、漸層、寫實）→ 加 `2D hand-inked cel animation, absolutely no 3D, no gradients, no realism.`
- 太像普通潮牌插畫、失去復古感 → 加 `keep the 1930s rubber hose proportions: tiny body, big head, pie-cut eyes, bouncy noodle limbs.`
- 強調色到處亂用 → 再強調一次 `the accent color appears ONLY on ...`。
