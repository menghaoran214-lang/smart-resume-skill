{{LANG_SWITCH}}

{{BANNER}}

{{BADGES}}

<p align="center"><b>{{TAGLINE}}</b></p>

{{WHAT}}

**适合谁用**：{{AUDIENCE}}

---

## 安装

```text
{{INSTALL}}
```

Windows 用 `.\.venv\Scripts\python.exe` 替换 `python`。安装器不覆盖已有目录，
依赖请装在自己的虚拟环境里，不会改动 Agent 的运行环境。

## 30 秒看效果

```text
{{DEMO}}
```

会生成 `resume.pdf`（两页 A4）、`resume.html`（可编辑）和 `review.json`（验收记录）。
示例数据完全是虚构的，每页都标注不可投递。

## 它怎么用

装好后对 Agent 说一句话就行：

> 用 $smart-resume 按这张 JD 截图做定制简历。先读我授权范围内的资料，
> 不够先问我要旧简历，其他缺项逐项问。求职意向只用截图里的岗位名。

Agent 会：读你的资料 → 缺什么问你 → 挑相关经历重排 → 出 PDF + 可编辑版 → 逐页验排版。
它不会编造经历，也不会把别的岗位混进来。

{{TOC}}

## 目录结构

{{SKILL_TREE}}

## 边界与限制

- 技能本体在 `skills/smart-resume/`，脚本只做校验和排版，识别截图和定制内容由宿主 Agent 完成。
- 可编辑版是 HTML，**不提供 DOCX**；HTML 改动不会自动同步 PDF，改 JSON 后重新生成。
- 记忆里的经历需要你确认；脚本只能检查"有没有来源"，判断不了真假。
- 不会替你投简历、不会公开上传，需要你授权才会动外部系统。

## 仓库状态

{{STATS_SVG}}

{{STATS}}

README 由 `scripts/render_readme.py` 从 `templates/` 与 `data/project.yaml` 生成，
改内容请改模板或数据后重新生成。

## 参与

见 [CONTRIBUTING.md](CONTRIBUTING.md) 与 [AGENTS.md](AGENTS.md)，
变更记录见 [CHANGELOG.md](CHANGELOG.md)，许可证见 [LICENSE](LICENSE)。
