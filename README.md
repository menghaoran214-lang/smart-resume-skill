<p align="center">
  <img src="assets/banner.png" alt="Smart Resume" width="760">
</p>

<h1 align="center">Smart Resume</h1>

<p align="center"><b>一张 JD 截图 + 你已有的资料 → 一份不编造的两页 A4 简历</b></p>

<p align="center">
<img src="https://img.shields.io/badge/License-0BSD-blue.svg" alt="License: 0BSD" height="20"> <img src="https://img.shields.io/badge/Skills-1-green.svg" alt="Skills: 1" height="20"> <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python: 3.10+" height="20"> <img src="https://img.shields.io/badge/Standard-Agent%20Skills-purple.svg" alt="Standard: Agent Skills" height="20">
</p>

<p align="center">[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [English](README.en.md)</p>

---

## 这是什么

- 岗位截图进，简历出：截图交给它，它照着这个岗位重排你做过的事
- 不编造：没做过的不写，记不清的先问你，岗位名照抄截图
- 交付两件：可投的 PDF 和能直接改字的网页版

**适合谁用**：正在投简历、想针对某个岗位改一版的人

## 目录

- [这是什么](#这是什么)
- [怎么安装](#怎么安装)
  - [最省事：把这一行发给你的 AI](#最省事把这一行发给你的-ai)
  - [或者自己装（Windows、macOS、Linux 都一样）](#或者自己装windowsmacoslinux-都一样)
- [30 秒看成品](#30-秒看成品)
- [实际怎么用](#实际怎么用)
- [这个技能长什么样](#这个技能长什么样)
- [它不做什么](#它不做什么)
- [仓库状态](#仓库状态)
- [开源协议](#开源协议)


## 怎么安装

### 最省事：把这一行发给你的 AI

复制下面这行，粘贴到 Codex / Claude Code / 任何支持 Skill 的 AI 对话框里，它会自己去拉取并安装：

```text
请安装这个技能：https://github.com/menghaoran214-lang/smart-resume-skill
```

### 或者自己装（Windows、macOS、Linux 都一样）

```text
git clone https://github.com/menghaoran214-lang/smart-resume-skill.git
cd smart-resume-skill
python3 -m pip install -r skills/smart-resume/requirements.txt
python3 skills/smart-resume/scripts/install.py --target ~/.codex/skills/smart-resume
```

Windows 上把 `python3` 换成 `py`，或者用 `python`。
手机上没有本地终端，但可以直接把上面那行口令发给云端 AI 帮你装。

## 30 秒看成品

这条命令会用仓库里的**虚构示例**跑一遍完整流程，生成三个文件：

```text
cd skills/smart-resume && python3 scripts/resume.py render examples/demo.json --demo --out output/demo
```

| 文件 | 是什么 |
| --- | --- |
| `output/demo/resume.pdf` | 两页 A4 简历，文字可选中复制，直接就能投 |
| `output/demo/resume.html` | 同一份简历的网页版，点一下就能改字 |
| `output/demo/review.json` | 排版与事实的检查记录，交给你或 AI 复核 |

示例数据全是编的，每页都写着"虚构示例 · 不可投递"，不会被误当成真实简历。

## 实际怎么用

装好后对 AI 说一句话就行：

> 用 $smart-resume 按这张 JD 截图做定制简历。先读我授权范围内的资料，
> 不够先问我要旧简历，其他缺项逐项问。求职意向只用截图里的岗位名。

AI 会：读你的资料 → 缺什么问你 → 挑相关经历重排 → 出 PDF + 可编辑版 → 逐页验排版。
它不会编造经历，也不会把别的岗位混进来。

## 这个技能长什么样

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


## 它不做什么

- 技能本体在 `skills/smart-resume/`，脚本只做校验和排版；识别截图、挑经历是宿主 AI 的活。
- 可编辑版是 HTML，**不提供 Word/DOCX**；改 HTML 不会同步 PDF，改 JSON 后重新生成。
- 记忆里的经历需要你确认；脚本只能检查"有没有来源"，判断不了真假。
- 不会替你投简历、不会公开上传任何东西，动外部系统前一定问你。

## 仓库状态

<p align="center">
  <img src="assets/stats.svg" alt="repository stats" height="26">
</p>

- 技能版本 / skill version：`0.1.0`
- 上方统计图由定时工作流自动刷新；CI 状态见仓库顶部 Actions 徽章


README 由 `scripts/render_readme.py` 从 `templates/` 与 `data/project.json` 生成，
改内容请改模板或数据后重新生成。

## 开源协议

本项目采用 **0BSD** 许可（见 [LICENSE](LICENSE)）：你可以自由使用、修改、再分发，
包括商用，不需要署名。给项目提改进建议或代码，看 [CONTRIBUTING.md](CONTRIBUTING.md)；
这份文件是给"想参与开发的人"看的，只是想用它做简历就不必打开。
每次改动的记录在 [CHANGELOG.md](CHANGELOG.md)。
