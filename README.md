# Pip — Claude Code 桌面寵物

> 一隻站在工作列上的弓箭手，跟著 Claude Code 的工作節奏動：思考時瞇眼拉弓、跑工具時瘋狂連射、等你回覆時盯著你、做完握拳慶祝。
>
> A rubber-hose streetwear archer that lives on your Windows taskbar and reacts to what Claude Code is doing — aims while it thinks, rapid-fires while it runs tools, stares at you while it waits, fist-pumps when it's done.

![Pip](assets/contact.png)

## 它會做什麼

| Claude 在做什麼 | Pip 的動作 |
|---|---|
| 對話開始 | 待命 |
| 開始思考 | 瞇眼拉弓 |
| 用工具 | 瘋狂連射，箭沿拋物線飛過你的視窗；姿勢依工具分四類（改檔、讀檔、查網路／外部工具、其他指令） |
| 問你問題、等你批准計畫 | 盯著你等 |
| 派出子代理 | 多一個小弓箭手幫忙，子代理跑完就離開 |
| 回答完成 | 握拳慶祝 |
| 出錯 | 頭暈，弓斷掉 |
| 對話結束 | 睡著 |

- **箭袋**＝ context 還剩多少；**體力**＝額度還剩多少。
- 游標上掛著一顆蘋果／氣球／蟲，Pip 閒著會瞄準射牠。
- 滑鼠會**穿過** Pip 以外的地方，照常點後面的程式；移到 Pip 身上可以摸摸頭，甩滑鼠牠會嚇到閃開。
- 右下角系統匣有 Pip 圖示：顯示／隱藏、結束。

## 架構

```
Claude Code ──(Mod: pip-bridge)──▶ http://127.0.0.1:38917/state ──▶ Tauri (Rust) ──emit──▶ Canvas
```

| 層 | 技術 | 位置 |
|---|---|---|
| 桌面視窗 | Tauri 2（Rust）：全螢幕透明、置頂、不進工作列；每 30ms 輪詢游標、tiny_http 收狀態、系統匣 | `pet/src-tauri/` |
| Pip 本身 | 單檔 HTML + Canvas，零框架：貼圖零件＋程式畫的橡皮水管手腳、節拍彈跳、彈道射擊、Verlet 擺盪 | `prototype/pip.html` |
| 接上 Claude | Claude Code Mod **pip-bridge**（在 [ClaudeMods](https://github.com/youllook/ClaudeMods/tree/main/plugins/pip-bridge)） | 另一個 repo |
| 素材 | 角色圖用 AI 生成，Python（numpy + Pillow）去背切零件 | `assets/`、`tools/`、`prompts/` |

## 安裝與執行（Windows）

需要 [Rust](https://rustup.rs/)、Node.js、WebView2（Windows 10/11 內建）。

```bash
cd pet
npm install
npm run sync          # 把 prototype/pip.html 和 assets 複製進 dist/
npm run build         # 產出 release 執行檔
```

執行 `pet/src-tauri/target/release/pip-pet.exe`，Pip 會出現在主螢幕右下角。

接著裝 Mod，讓 Pip 跟著 Claude 動：

```bash
claude plugin marketplace add youllook/ClaudeMods
claude plugin install pip-bridge@claude-mods
```

沒裝 Mod 也能手動玩：

```bash
curl "http://127.0.0.1:38917/state?mode=exec&tool=Bash"
```

參數：`mode`＝`away|idle|think|exec|wait|ok|err`，`tool`＝`Bash|Edit|Read|WebSearch`，`arrows`＝0–20，`stamina`＝0.1–1，`sub`＝`+|-`。

## 只想看動畫

不用編譯，直接在瀏覽器開原型（數字鍵 1–7 切狀態）：

```bash
python -m http.server 4317 --bind 127.0.0.1
# 開 http://127.0.0.1:4317/prototype/pip.html
```

`prototype/archer.html` 是最早的像素風版本。

## 已知限制

- 只在主螢幕顯示。
- 目前只測過 Windows。

## 授權

[MIT](LICENSE)，程式碼與角色素材皆同。
