<p align="center">
  <img src="assets/banner.png" alt="Smart Resume" width="760">
</p>

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

{{TOC}}

<a id="install"></a>

## 怎麼安裝

<details open>
<summary><b>最省事：把這一行傳給你的 AI</b></summary>

複製下面這行，貼到支援安裝 Skill、可存取倉庫並操作檔案的 AI 對話框：

```text
{{INSTALL_PROMPT}}
```

AI 需要倉庫存取權限及可安裝技能的執行環境；一般聊天視窗未必支援安裝。手機可透過連接電腦或雲端環境的 AI 使用，不能直接裝進 iOS。

</details>

<details>
<summary><b>或者自己裝（Windows、macOS、Linux）</b></summary>

<a id="install-manual"></a>

```text
{{INSTALL}}
```

需要 Git 與 Python 3.10+。Windows 把 `python3` 換成 `py` 或 `python`。範例目標目錄用於 Codex；其他 AI 請使用各自的技能目錄。相依套件建議裝在獨立虛擬環境中。

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

## 開源授權

[0BSD 授權](LICENSE) · 可使用、修改及商用；按原樣提供，不作擔保。
