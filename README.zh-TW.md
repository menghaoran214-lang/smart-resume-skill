[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [English](README.en.md)

<p align="center">
  <img src="assets/banner.png" alt="Smart Resume" width="820">
</p>

<img src="https://img.shields.io/badge/License-0BSD-blue.svg" alt="License: 0BSD" height="20"> <img src="https://img.shields.io/badge/Skills-1-green.svg" alt="Skills: 1" height="20"> <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python: 3.10+" height="20"> <img src="https://img.shields.io/badge/Standard-Agent%20Skills-purple.svg" alt="Standard: Agent Skills" height="20">

<p align="center"><b>一張 JD 截圖 + 你既有的資料 → 一份不捏造的兩頁 A4 履歷</b></p>

- 職缺截圖進，履歷出：截圖交給它，它照著這個職缺重排你做過的事
- 不捏造：沒做過的不寫，記不清的先問你，職缺名照抄截圖
- 交付兩件：可投的 PDF 和能直接改字的網頁版

**適合誰用**：正在投履歷、想針對某個職缺改一版的人

---

## 安裝

```text
python -m venv .venv
pip install -r skills/smart-resume/requirements.txt
python skills/smart-resume/scripts/install.py --target ~/.codex/skills/smart-resume
```

Windows 用 `.\.venv\Scripts\python.exe` 取代 `python`。安裝器不覆寫既有目錄，
依賴請裝在自己的虛擬環境裡，不會改動 Agent 的執行環境。

## 30 秒看效果

```text
cd skills/smart-resume && python scripts/resume.py render examples/demo.json --demo --out output/demo
```

會產生 `resume.pdf`（兩頁 A4）、`resume.html`（可編輯）與 `review.json`（驗收記錄）。
範例資料完全虛構，每頁都標註不可投遞。

## 它怎麼用

裝好後對 Agent 說一句話就行：

> 用 $smart-resume 依這張 JD 截圖製作履歷。先讀我授權範圍內的資料，
> 不夠先跟我要舊履歷，其他缺項逐項問。求職意向只用截圖裡的職缺名。

Agent 會：讀你的資料 → 缺什麼問你 → 挑相關經歷重排 → 出 PDF 加可編輯版 → 逐頁驗排版。
它不會捏造經歷，也不會混入其他職缺。

## 目錄

- [安裝](#安裝)
- [30 秒看效果](#30-秒看效果)
- [它怎麼用](#它怎麼用)
- [專案目錄](#專案目錄)
- [邊界與限制](#邊界與限制)
- [倉庫狀態](#倉庫狀態)
- [參與](#參與)


## 專案目錄

```text
smart-resume/
├── assets/
│   ├── intake.json
│   └── resume.html
├── examples/
│   └── demo.json
├── references/
│   └── workflow.md
├── scripts/
│   ├── install.py
│   ├── package.py
│   └── resume.py
├── tests/
│   └── test_resume.py
├── LICENSE
├── requirements.txt
├── SKILL.md
└── VERSION
```


## 邊界與限制

- 技能本體在 `skills/smart-resume/`，腳本只做檢查與排版，辨識截圖與客製內容由宿主 Agent 完成。
- 可編輯版為 HTML，**不提供 DOCX**；HTML 改動不會自動同步 PDF，改 JSON 後重新產生。
- 記憶中的經歷需你確認；腳本只能檢查「有沒有來源」，判斷不了真偽。
- 不會替你投遞、不會公開上傳，需要你授權才會動外部系統。

## 倉庫狀態

<p align="center">
  <img src="assets/stats.svg" alt="repository stats" height="26">
</p>

- 技能版本 / skill version：`0.1.0`
- 上方统计图由定时工作流自动刷新；CI 状态见仓库顶部 Actions 徽章


README 由 `scripts/render_readme.py` 依 `templates/` 與 `data/project.json` 產生，
改內容請改模板或資料後重新產生。

## 參與

請看 [CONTRIBUTING.md](CONTRIBUTING.md) 與 [AGENTS.md](AGENTS.md)，
變更記錄見 [CHANGELOG.md](CHANGELOG.md)，授權見 [LICENSE](LICENSE)。
