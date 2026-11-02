[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [English](README.en.md)

# Smart Resume Skill

**一張 JD 截圖 + 既有資料 → 有依據的客製履歷。**

版本 **0.1.0** · Python **3.10+** · 授權 **0BSD**

這是可安裝的 Agent Skill。Agent 負責辨識職缺、讀取授權資料及客製內容；
本機腳本負責結構檢查、兩頁 A4 PDF、可編輯 HTML 與獨立驗收紀錄。
不是獨立聊天網站，不內建模型、歷史記憶服務或 OCR。

## 成品預覽

[`examples/demo.json`](examples/demo.json) 為完全虛構的中文範例。
執行下列指令即可產生 PDF 和 HTML，每頁都標示虛構範例，不能用於應徵。
範例以少量文字展示結構，並非完整的真實兩頁履歷。
另見[驗收文件](docs/ACCEPTANCE.md)及[任務文件](docs/TASKS.md)。

## 安裝與快速開始

解壓縮後進入包含 `SKILL.md` 的 `smart-resume` 資料夾：

```text
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/install.py --target "$HOME/.codex/skills/smart-resume"
```

macOS/Linux：

```sh
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/install.py --target "$HOME/.codex/skills/smart-resume"
```

`--target` 可換成目標 Agent 支援的 skills 路徑，資料夾必須尚未存在。
安裝器只複製白名單檔案，不覆寫既有版本、不複製個人產物，
也不會在 Agent 環境自動安裝 Python 套件。執行時使用已安裝依賴的解譯器。
請讓 Agent 重新探索 Skill；不支援原生探索時可直接讀取 `SKILL.md`，
但應明確說明不是原生安裝。手動安裝可複製乾淨專案資料夾到 skills 目錄。

以下 `python` 指上述虛擬環境中的解譯器：

```text
python scripts/resume.py validate examples/demo.json --demo
python scripts/resume.py render examples/demo.json --demo --out output/demo
```

產生 `resume.pdf`、`resume.html`、私有 `review.json`。不覆寫既有輸出；
重跑請換資料夾。Windows 優先使用宋體，其他系統請用
`--font /path/to/font.ttf` 或 `SMART_RESUME_FONT` 指定涵蓋輸出文字、
受 ReportLab 支援的 TrueType 字型。缺字會報錯，專案不分發系統字型。

## 實際使用

向安裝後的 Agent 說：

> 使用 $smart-resume，依這張 JD 截圖製作履歷。先讀取已授權的相關記憶與資料；
> 資料不足先向我要舊履歷，其他缺項逐項詢問。求職意向只用職缺原名。
> 預設兩頁 A4，交付 PDF 與可編輯版，逐頁檢查排版，不捏造經歷。

先讀資料，避免重複填寫；不足時先索取舊履歷。照片偏好不明時詢問提供或省略，
不強制上傳。記憶資料需確認，衝突需釐清，不讀取未授權帳號或他人資料。
截圖看不清楚就詢問，不猜職缺名稱。影像辨識由宿主 Agent 提供。

真實資料放在專案外的私人目錄：

```text
python scripts/resume.py init --out ../private-resume/resume.json
python scripts/resume.py validate ../private-resume/resume.json
python scripts/resume.py render ../private-resume/resume.json --out ../private-resume/delivery
```

空白模板須先補齊，不能直接通過校驗。`document_supported` 為資料支持，
`user_confirmed` 為使用者確認，皆不等於第三方認證。
推測、待確認、衝突內容不得進入成稿。腳本只能檢查結構和來源狀態，
不能判斷真偽或自動理解職缺匹配程度。

## 交付與驗收

預設兩頁 A4、正文 10.5pt；內容不足時詢問是否改一頁，不湊字數或經歷；
溢位會報錯，修改後重產，不縮字或截斷。可省略照片或嵌入私人 PNG/JPEG。
PDF 文字可選取；HTML 可點擊正文編輯並另存新檔；JSON 是重新產生的來源。
**本版可編輯格式為 HTML，不含 DOCX。** HTML 修改不會自動更新 PDF。

`review.json` 的事實、PDF 排版與 HTML 檢查預設為 `pending`；
Agent 須實際查看每頁 PDF 圖像、核對文字與來源後記錄結果。
HTML 與 PDF 使用不同排版引擎，HTML 列印不能取代 PDF 驗收。
交付雇主時只給履歷，來源及缺口紀錄保留於私人目錄。

## 專案目錄

```text
smart-resume/
├── SKILL.md                 Agent 入口
├── README*.md               三語首頁
├── assets/                  空白輸入與 HTML 模板
├── examples/demo.json       純虛構範例
├── references/workflow.md   來源與驗收約定
├── scripts/                 產生、安裝、封裝
├── tests/                   行為測試
├── docs/                    任務及驗收
└── .github/                 自動檢查與 PR 模板
```

## 使用範例

提供填好的私人資料檔，換取三個交付物：

```text
python scripts/resume.py validate ../private-resume/resume.json
python scripts/resume.py render ../private-resume/resume.json --out ../private-resume/delivery
```

輸出：`delivery/resume.pdf`（兩頁 A4）、`delivery/resume.html`（可編輯）、
`delivery/review.json`（排版與事實檢查記錄）。資料不足或衝突時腳本會報錯，
不會自行猜測內容。

## 貢獻

請閱讀 [CONTRIBUTING.md](CONTRIBUTING.md)，Agent 規則見 [AGENTS.md](AGENTS.md)。

## 授權

採用 [LICENSE](LICENSE) 所載的 0BSD 授權。

## 開發與封裝

```text
python -m unittest discover -s tests -v
python scripts/package.py --out dist/smart-resume-0.1.0.zip
```

封裝採固定白名單並輸出 SHA-256，排除個人輸入、照片、`.venv` 和產物。
白名單無法辨別檔案是否遭改成個人資料，發布前仍須審查內容差異。
CI 配置涵蓋 Windows/Linux，但配置存在不代表遠端已執行。
請閱讀 [CONTRIBUTING.md](CONTRIBUTING.md)、[AGENTS.md](AGENTS.md)。

## 常見問題與隱私

- **看不到歷史紀錄？** 只使用宿主已授權提供的相關內容。
- **只有 JD 能完成嗎？** 沒有個人經歷就須補資料，不能捏造。
- **字型錯誤？** 指定涵蓋輸出文字的 TrueType 字型，複雜文字塑形須另行確認。
- **可以公開範例嗎？** 此專案只有虛構範例，真實電話、照片、履歷不可入庫。
- **會自動投遞或推送 GitHub？** 不會，須使用者授權。
- **安裝後會自行啟用？** 依宿主探索與觸發機制而定，需在目標 Agent 確認。

授權見 [LICENSE](LICENSE)。三語 README 皆為 0.1.0，功能變更請同步維護。
