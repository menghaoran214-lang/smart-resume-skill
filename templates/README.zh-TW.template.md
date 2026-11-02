{{LANG_SWITCH}}

{{BANNER}}

{{BADGES}}

<p align="center"><b>{{TAGLINE}}</b></p>

{{WHAT}}

**適合誰用**：{{AUDIENCE}}

---

## 安裝

```text
{{INSTALL}}
```

Windows 用 `.\.venv\Scripts\python.exe` 取代 `python`。安裝器不覆寫既有目錄，
依賴請裝在自己的虛擬環境裡，不會改動 Agent 的執行環境。

## 30 秒看效果

```text
{{DEMO}}
```

會產生 `resume.pdf`（兩頁 A4）、`resume.html`（可編輯）與 `review.json`（驗收記錄）。
範例資料完全虛構，每頁都標註不可投遞。

## 它怎麼用

裝好後對 Agent 說一句話就行：

> 用 $smart-resume 依這張 JD 截圖製作履歷。先讀我授權範圍內的資料，
> 不夠先跟我要舊履歷，其他缺項逐項問。求職意向只用截圖裡的職缺名。

Agent 會：讀你的資料 → 缺什麼問你 → 挑相關經歷重排 → 出 PDF 加可編輯版 → 逐頁驗排版。
它不會捏造經歷，也不會混入其他職缺。

{{TOC}}

## 專案目錄

{{SKILL_TREE}}

## 邊界與限制

- 技能本體在 `skills/smart-resume/`，腳本只做檢查與排版，辨識截圖與客製內容由宿主 Agent 完成。
- 可編輯版為 HTML，**不提供 DOCX**；HTML 改動不會自動同步 PDF，改 JSON 後重新產生。
- 記憶中的經歷需你確認；腳本只能檢查「有沒有來源」，判斷不了真偽。
- 不會替你投遞、不會公開上傳，需要你授權才會動外部系統。

## 倉庫狀態

{{STATS_SVG}}

{{STATS}}

README 由 `scripts/render_readme.py` 依 `templates/` 與 `data/project.json` 產生，
改內容請改模板或資料後重新產生。

## 參與

請看 [CONTRIBUTING.md](CONTRIBUTING.md) 與 [AGENTS.md](AGENTS.md)，
變更記錄見 [CHANGELOG.md](CHANGELOG.md)，授權見 [LICENSE](LICENSE)。
