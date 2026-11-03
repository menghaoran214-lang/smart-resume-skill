{{BANNER}}

<h1 align="center">{{TITLE}}</h1>

<p align="center"><b>{{TAGLINE}}</b></p>

<p align="center">
{{BADGES}}
</p>

<p align="center">{{LANG_SWITCH}}</p>

---

<a id="what"></a>

## 這是什麼

{{WHAT}}

**適合誰用**：{{AUDIENCE}}

### 安裝後怎麼用

將舊履歷及目標職缺 JD（截圖或文字）傳給已安裝技能的 AI，然後說：

> 用 $smart-resume 依這份 JD 更新我的履歷。先讀既有資料，缺項逐一問。
> 幫我推薦版式，只保留有來源支持的經歷，輸出 PDF 與可編輯 HTML，最後逐頁檢查。

六種風格是同一份履歷的六種版式，不是六種職涯方向。可以讓 AI 推薦，
也可以指定「技術工程」或沿用已儲存風格，日常使用不需自己執行開發指令。
截圖辨識、追問與改寫由執行技能的 AI 負責。

### 0.2.0 更新了什麼

| 使用環節 | 舊版 | 本次新增 |
| --- | --- | --- |
| 履歷排版 | 一套固定版式 | 六套實際可產生 PDF / HTML 的版式 |
| 選擇模板 | 固定預設 | 依職缺關鍵字推薦並說明理由；可自行指定 |
| 預覽 | 一份範例 | 六款真實 PDF 與可篩選的本機圖庫 |
| 個人偏好 | 無獨立風格檔案 | 儲存基礎版式、強調色及間距以供重用 |
| 品質檢查 | 來源檢查、溢出拒絕及待複核紀錄 | 新增內容完整性、雜湊、A4、重疊檢查及審閱驗收 |
| 說明 | 既有三語 README | 補齊安裝更新、風格選擇、儲存及驗收 |

舊版的 JD 截圖流程、有來源的經歷篩選、PDF 和 HTML 輸出均保留。
自動匹配採關鍵字規則；個人風格目前調整既有版式的顏色與間距。

![六款真實 PDF 預覽](assets/styles-preview.png)

{{TOC}}

<a id="install"></a>

## 怎麼安裝

<details open>
<summary><b>最省事：把這一行傳給你的 AI</b></summary>

複製下面這行，貼到支援安裝 Skill、可存取倉庫並操作檔案的 AI 對話框：

```text
{{INSTALL_PROMPT}}
```

從既有倉庫安裝或更新，技能呼叫名仍為 `$smart-resume`。AI 需要能讀取倉庫並操作檔案；一般聊天視窗未必支援安裝。手機可透過連接電腦或雲端環境的 AI 使用，不能直接裝進 iOS。

</details>

<details>
<summary><b>或者自己裝（Windows、macOS、Linux）</b></summary>

<a id="install-manual"></a>

```text
{{INSTALL}}
```

需要 Git 及 Python 3.10+。Windows 把 `python3` 換成 `py` 或 `python`。範例目標目錄用於 Codex；其他 AI 請使用各自的技能目錄。相依套件建議裝在獨立虛擬環境中。升級時先備份既有技能目錄，再安裝到原目標；個人資料及 `~/.smart-resume/styles/` 獨立保留，安裝程式不會直接覆蓋舊版。

</details>

<a id="demo"></a>

## 30 秒看成品

安裝相依套件後，在倉庫根目錄執行下列指令，用**虛構資料**查看排版效果。這一步僅示範檔案產生，不讀取截圖或個人資料。

```text
{{DEMO}}
```

| 檔案 | 是什麼 |
| --- | --- |
| `output/demo/resume.pdf` | 兩頁 A4 範例，僅供查看效果，不可投遞 |
| `output/demo/resume.html` | 同一份履歷的網頁版，點一下就能改字 |
| `output/demo/review.json` | 排版與事實的檢查記錄，交給你或 AI 複核 |

範例資料全是編的，每頁都寫著「虛構範例 · 不可投遞」，不會被誤認成真實履歷。

### 六種可產生 PDF 的風格

{{STYLE_DIRECTORY}}

### 補齊原討論的模板庫

數據成長型取代先前誤加的內容編輯型。按「職缺類型 × 投遞管道 × 資歷」
檢索模板，先複用已認可的版本，再按缺口研究。國內求職依雇主實際要求處理
中文字型、選填照片、聯絡方式與一至兩頁篇幅。

結構品質、技術品質、真實投遞成效分開記錄。內部百分制：職缺匹配 35、
成果證明 25、事實來源 15、內容層次 10、技術品質 10、視覺 5。
這是自定審閱標準，不是招聘方演算法，也不預測面試機率。

個人模板可儲存、審核啟用、停用修復並記錄投遞回饋，保留於本機個人目錄。
公共模板須經去識別化、授權和品質檢查後以 PR 更新。
研究來源包括大學職涯中心、招聘研究、真實 JD、ATS 檢查與投遞資料，
不可複製付費模板或他人履歷；沒有真實資料不可宣稱高通過率。

```text
python scripts/library.py list --role-family ops-growth --channel cn-platform
python scripts/library.py save my-growth --style growth --role-family ops-growth --channel cn-platform --seniority mid
python scripts/library.py report my-growth
```

儲存模板分類不代表訓練模型或上傳個資。完整的審核、淘汰和回饋命令見
[模板庫與品質標準](skills/smart-resume/references/template-library.md)。

每種風格有獨立 `styles/<id>/STYLE.md`，共用已確認的內容，正文維持 10.5 pt。圖庫圖片由實際 PDF 轉成 PNG，包含所有頁面，並連結 PDF 與 HTML。

從技能目錄執行（原始碼工程先進入 `skills/smart-resume`；安裝包先進入解壓後的 `smart-resume`）：

```text
python scripts/gallery.py --compact --out output/gallery
python scripts/resume.py match examples/demo.zh-TW.json
python scripts/resume.py render examples/demo.zh-TW.json --demo --style technical --out output/technical
python scripts/resume.py save-style my-green --base technical --accent "#155e52" --spacing airy
python scripts/resume.py render examples/demo.zh-TW.json --demo --profile ~/.smart-resume/styles/my-green/profile.json --out output/my-green
```

開啟 `output/gallery/index.html` 查看六款真實預覽。圖庫另需 Poppler 的 `pdftoppm`，可用 `--pdftoppm` 指定路徑；缺少工具會明確報錯。簡體、繁體、英文範例分別為 `examples/demo.json`、`examples/demo.zh-TW.json`、`examples/demo.en.json`。

`--compact` 將虛構範例的所有章節合為一頁，便於比較風格，不刪內容或縮字；移除參數即保留原始頁數。圖庫另存實際使用的 `demo-input.json`，可用於驗收其中的 PDF。

自動匹配只讀取職缺名稱與 `--context` 關鍵字，輸出推薦理由；沒有匹配則回到經典商務。明確的 `--style` 或 `--profile` 優先，`--ats` 可要求極簡；衝突選項會拒絕執行。此功能不是職缺適配模型，不提供錄取機率。

個人風格存於 `~/.smart-resume/styles/<名稱>/`，只含 `profile.json` 和 `STYLE.md`，不保存個人經歷。可用 `--profiles-dir` 自選目錄；不覆蓋既有風格，會檢查色彩對比與間距。

### 品質驗收

```text
python scripts/quality.py output/technical examples/demo.zh-TW.json --demo
```

檢查 A4、頁數、選取內容、檔案雜湊及排版邊界，產生 `quality.json`。首次回報未完成：PDF 逐頁視覺檢查、事實複核與 HTML 檢查必須實際執行，再依 [風格與驗收說明](skills/smart-resume/references/styles.md) 記錄審閱者及結論。虛構範例只能通過預覽驗收，永遠不可投遞；內容溢出會報錯，不縮字或隱藏。HTML 與 PDF 分別渲染，修改 JSON 後重新產生兩者。

<a id="usage"></a>

## 實際怎麼用

裝好後對 AI 說一句話就行：

> 用 $smart-resume 依這張 JD 截圖製作履歷。先讀我授權範圍內的資料，
> 不夠先跟我要舊履歷，其他缺項逐項問。求職意向只用截圖裡的職缺名。

AI 會：讀你的資料 → 缺什麼問你 → 挑相關經歷重排 → 出 PDF 加可編輯版 → 逐頁驗排版。
它不會捏造經歷，也不會混入其他職缺。

<a id="structure"></a>

## 這個技能長什麼樣

{{SKILL_TREE}}

<a id="limits"></a>

## 它不做什麼

- 技能本體在 `skills/smart-resume/`，腳本只做檢查與排版；辨識截圖、挑經歷是宿主 AI 的活。
- 可編輯版為 HTML，**不提供 Word/DOCX**；改 HTML 不會同步 PDF，改 JSON 後重新產生。
- 記憶中的經歷需你確認；腳本只能檢查「有沒有來源」，判斷不了真偽。
- 不會替你投遞、不會公開上傳任何東西，動外部系統前一定問你。

<a id="license"></a>

## 授權條款

本專案採用 [MIT 授權條款](LICENSE)：可自由使用、修改、商用；散布時須保留版權及許可聲明。風格規範與圖庫機制參考 [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar)，六種履歷排版為本專案獨立實作，無須安裝其影片執行環境。
