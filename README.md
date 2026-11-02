<p align="center">
  <img src="assets/banner.zh-CN.png" alt="Smart Resume" width="820">
</p>

<h1 align="center">智能简历</h1>

<p align="center"><b>一张 JD 截图 + 你已有的资料 → 一份不编造的两页 A4 简历</b></p>

<p align="center">
<img src="https://img.shields.io/badge/License-0BSD-blue.svg" alt="License: 0BSD" height="20"> <img src="https://img.shields.io/badge/Skills-1-green.svg" alt="Skills: 1" height="20"> <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python: 3.10+" height="20"> <img src="https://img.shields.io/badge/Standard-Agent%20Skills-purple.svg" alt="Standard: Agent Skills" height="20">
</p>

<p align="center"><a href="README.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.en.md">English</a></p>

---

<a id="what"></a>

## 这是什么

- 岗位截图进，简历出：截图交给它，它照着这个岗位重排你做过的事
- 不编造：没做过的不写，记不清的先问你，岗位名照抄截图
- 交付两件：可投的 PDF 和能直接改字的网页版

**适合谁用**：正在投简历、想针对某个岗位改一版的人

## 目录

- [这是什么](#what)
- [怎么安装](#install)
- [30 秒看成品](#demo)
- [实际怎么用](#usage)
- [这个技能长什么样](#structure)
- [它不做什么](#limits)
- [开源协议](#license)


<a id="install"></a>

## 怎么安装

<details open>
<summary><b>最省事：把这一行发给你的 AI</b></summary>

复制下面这行，粘贴到支持安装 Skill、能访问仓库并操作文件的 AI 对话框：

```text
请安装这个技能：https://github.com/menghaoran214-lang/smart-resume-skill
```

AI 需要有仓库访问权限和可安装技能的运行环境；普通聊天窗口不一定支持安装。手机可通过连接电脑或云端运行环境的 AI 使用，不能直接装进 iOS。

</details>

<details>
<summary><b>或者自己装（Windows、macOS、Linux）</b></summary>

<a id="install-manual"></a>

```text
git clone https://github.com/menghaoran214-lang/smart-resume-skill.git
cd smart-resume-skill
python3 -m pip install -r skills/smart-resume/requirements.txt
python3 skills/smart-resume/scripts/install.py --target ~/.codex/skills/smart-resume
```

需要 Git 和 Python 3.10+。Windows 上把 `python3` 换成 `py` 或 `python`。示例目标目录用于 Codex；其他 AI 请使用它自己的技能目录。依赖建议装在独立虚拟环境中。

</details>

<a id="demo"></a>

## 30 秒看成品

安装依赖后，在仓库根目录运行下面这行，用**虚构资料**查看排版效果。这一步只演示文件生成，不读取截图，也不读取你的个人资料。

```text
cd skills/smart-resume && python3 scripts/resume.py render examples/demo.json --demo --out output/demo
```

| 文件 | 是什么 |
| --- | --- |
| `output/demo/resume.pdf` | 两页 A4 示例，仅用于查看效果，不可投递 |
| `output/demo/resume.html` | 同一份简历的网页版，点一下就能改字 |
| `output/demo/review.json` | 排版与事实的检查记录，交给你或 AI 复核 |

示例数据全是编的，每页都写着"虚构示例 · 不可投递"，不会被误当成真实简历。

<a id="usage"></a>

## 实际怎么用

装好后对 AI 说一句话就行：

> 用 $smart-resume 按这张 JD 截图做定制简历。先读我授权范围内的资料，
> 不够先问我要旧简历，其他缺项逐项问。求职意向只用截图里的岗位名。

AI 会：读你的资料 → 缺什么问你 → 挑相关经历重排 → 出 PDF + 可编辑版 → 逐页验排版。
它不会编造经历，也不会把别的岗位混进来。

<a id="structure"></a>

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


<a id="limits"></a>

## 它不做什么

- 技能本体在 `skills/smart-resume/`，脚本只做校验和排版；识别截图、挑经历是宿主 AI 的活。
- 可编辑版是 HTML，**不提供 Word/DOCX**；改 HTML 不会同步 PDF，改 JSON 后重新生成。
- 记忆里的经历需要你确认；脚本只能检查"有没有来源"，判断不了真假。
- 不会替你投简历、不会公开上传任何东西，动外部系统前一定问你。

<a id="license"></a>

## 开源协议

[0BSD 许可证](LICENSE) · 可使用、修改和商用；按原样提供，不作担保。
