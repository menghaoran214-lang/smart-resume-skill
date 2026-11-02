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

## 这是什么

{{WHAT}}

**适合谁用**：{{AUDIENCE}}

{{TOC}}

## 怎么安装

### 最省事：把这一行发给你的 AI

复制下面这行，粘贴到 Codex / Claude Code / 任何支持 Skill 的 AI 对话框里，它会自己去拉取并安装：

```text
{{INSTALL_PROMPT}}
```

### 或者自己装（Windows、macOS、Linux 都一样）

```text
{{INSTALL}}
```

Windows 上把 `python3` 换成 `py`，或者用 `python`。
手机上没有本地终端，但可以直接把上面那行口令发给云端 AI 帮你装。

## 30 秒看成品

这条命令会用仓库里的**虚构示例**跑一遍完整流程，生成三个文件：

```text
{{DEMO}}
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

{{SKILL_TREE}}

## 它不做什么

- 技能本体在 `skills/smart-resume/`，脚本只做校验和排版；识别截图、挑经历是宿主 AI 的活。
- 可编辑版是 HTML，**不提供 Word/DOCX**；改 HTML 不会同步 PDF，改 JSON 后重新生成。
- 记忆里的经历需要你确认；脚本只能检查"有没有来源"，判断不了真假。
- 不会替你投简历、不会公开上传任何东西，动外部系统前一定问你。

## 仓库状态

{{STATS_SVG}}

{{STATS}}

README 由 `scripts/render_readme.py` 从 `templates/` 与 `data/project.json` 生成，
改内容请改模板或数据后重新生成。

## 开源协议

本项目采用 **0BSD** 许可（见 [LICENSE](LICENSE)）：你可以自由使用、修改、再分发，
包括商用，不需要署名。给项目提改进建议或代码，看 [CONTRIBUTING.md](CONTRIBUTING.md)；
这份文件是给"想参与开发的人"看的，只是想用它做简历就不必打开。
每次改动的记录在 [CHANGELOG.md](CHANGELOG.md)。
