{{BANNER}}

<h1 align="center">{{TITLE}}</h1>

<p align="center"><b>{{TAGLINE}}</b></p>

<p align="center">
{{BADGES}}
</p>

<p align="center">{{LANG_SWITCH}}</p>

---

<a id="what"></a>

## 这是什么

{{WHAT}}

**适合谁用**：{{AUDIENCE}}

### 已安装后怎么用

把旧简历和目标岗位 JD（截图或文字）发给装好技能的 AI，然后说：

> 用 $smart-resume 按这个 JD 更新我的简历。先看我已有资料，缺什么逐项问。
> 帮我推荐排版风格，只保留有来源支持的经历，输出 PDF 和可编辑 HTML，最后逐页检查。

这六种风格是同一份简历的六种版式，不是六份职业方向。你可以让 AI 推荐，
也可以说“用技术工程风格”或“沿用我保存的风格”。日常使用不需要自己运行下面的开发命令。
安装的是技能；读取截图、追问和改写由运行它的 AI 完成。

### 0.2.0 与旧版相比更新了什么

| 使用环节 | 旧版 | 这次新增 |
| --- | --- | --- |
| 简历排版 | 一套固定版式 | 六套实际可生成 PDF / HTML 的版式 |
| 选择模板 | 固定默认 | 按岗位关键词推荐并解释理由；支持手动指定 |
| 预览效果 | 一份示例 | 六款真实 PDF 样张及可筛选的本地画廊 |
| 保存个人偏好 | 没有独立风格档案 | 保存基础版式、强调色、间距，下次复用 |
| 交付检查 | 证据校验、溢出拒绝与待复核记录 | 增加内容完整性、文件哈希、A4、重叠检查及审阅验收 |
| 使用说明 | 原有三语 README | 三语补齐安装更新、风格选择、保存与验收方法 |

旧版已有的“JD 截图工作流、有来源的经历筛选、PDF 与 HTML 输出”继续保留。
自动匹配是关键词规则；个人风格目前只调整已有版式的颜色与间距。

![六种风格的真实 PDF 预览](assets/styles-preview.png)

{{TOC}}

<a id="install"></a>

## 怎么安装

<details open>
<summary><b>最省事：把这一行发给你的 AI</b></summary>

复制下面这行，粘贴到支持安装 Skill、能访问仓库并操作文件的 AI 对话框：

```text
{{INSTALL_PROMPT}}
```

使用现有仓库安装或更新，技能调用名仍为 `$smart-resume`。AI 需要能读取仓库并操作文件；普通聊天窗口不一定支持安装。手机可通过连接电脑或云端运行环境的 AI 使用，不能直接装进 iOS。

</details>

<details>
<summary><b>或者自己装（Windows、macOS、Linux）</b></summary>

<a id="install-manual"></a>

```text
{{INSTALL}}
```

需要 Git 和 Python 3.10+。Windows 上把 `python3` 换成 `py` 或 `python`。示例目标目录用于 Codex；其他 AI 请使用它自己的技能目录。依赖建议装在独立虚拟环境中。已有技能目录会拒绝覆盖；升级时先备份旧目录，再安装到原目标，个人资料及 `~/.smart-resume/styles/` 独立保留。MIT 许可证声明需随副本保留。

</details>

<a id="demo"></a>

## 30 秒看成品

安装依赖后，在仓库根目录运行下面这行，用**虚构资料**查看排版效果。这一步只演示文件生成，不读取截图，也不读取你的个人资料。

```text
{{DEMO}}
```

| 文件 | 是什么 |
| --- | --- |
| `output/demo/resume.pdf` | 两页 A4 示例，仅用于查看效果，不可投递 |
| `output/demo/resume.html` | 同一份简历的网页版，点一下就能改字 |
| `output/demo/review.json` | 排版与事实的检查记录，交给你或 AI 复核 |

示例数据全是编的，每页都写着"虚构示例 · 不可投递"，不会被误当成真实简历。

### 六种可生成 PDF 的风格

{{STYLE_DIRECTORY}}

### 补齐「⭐定制简历制作」讨论的更新

按原讨论恢复六种风格，新增数据增长型，取代此前误加的内容编辑型。
模板按“岗位类型 × 投递渠道 × 资历”归类，先复用已认可模板，再按缺口搜索。
国内求职按目标岗位要求处理中文字体、照片、联系方式和一至两页篇幅。

结构质量、技术质量、投递效果分别记录；内部百分制中岗位匹配 35 分、
成果证明 25 分、事实来源 15 分、内容层次 10 分、技术质量 10 分、视觉 5 分。
这是自定审阅标准，不是招聘方算法，也不预测面试概率。

个人模板支持保存、审核启用、停用修复及投递反馈记录，资料保存在本机个人目录。
公共模板通过脱敏、许可与质量检查后的 PR 更新；不自动上传个人简历。
研究来源分为大学职业中心、招聘研究、真实 JD、ATS 检查与真实投递反馈四类，
不会直接复制收费模板或他人简历。

从技能目录运行：

```text
python scripts/library.py list --role-family ops-growth --channel cn-platform
python scripts/library.py save my-growth --style growth --role-family ops-growth --channel cn-platform --seniority mid
python scripts/library.py report my-growth
```

保存的是可复用模板分类和风格，不是自动训练模型。完整的启用、淘汰、反馈命令见
[模板库与质量标准](skills/smart-resume/references/template-library.md)。
没有真实投递数据时只能说“通过质量检查”，不能说“高通过率”。

每种风格都有独立 `styles/<id>/STYLE.md`；共享同一份已核实内容，正文保持 10.5 pt。真实图库由 PDF 转成 PNG，包含每种风格的全部页面，可直接打开 PDF 或 HTML。

从技能目录运行（源码工程先进入 `skills/smart-resume`；安装包先进入解压后的 `smart-resume`）：

```text
python scripts/gallery.py --compact --out output/gallery
python scripts/resume.py match examples/demo.json
python scripts/resume.py render examples/demo.json --demo --style technical --out output/technical
python scripts/resume.py save-style my-green --base technical --accent "#155e52" --spacing airy
python scripts/resume.py render examples/demo.json --demo --profile ~/.smart-resume/styles/my-green/profile.json --out output/my-green
```

打开 `output/gallery/index.html` 查看六款真实预览。图库额外需要 Poppler 的 `pdftoppm`，缺失会明确报错；可用 `--pdftoppm` 指定路径。简体、繁体、英文示例分别为 `examples/demo.json`、`examples/demo.zh-TW.json`、`examples/demo.en.json`。

`--compact` 将虚构示例的全部章节合成一页，便于比较风格，不删内容、不缩字；去掉该参数保留原始页数。图库会保存实际使用的 `demo-input.json`，可用它验收图库中的 PDF。

自动匹配只使用 JD 岗位名和 `--context` 的关键词，输出推荐理由；无匹配回到经典商务。显式 `--style` 或 `--profile` 优先，`--ats` 可要求极简；冲突选项拒绝执行。它不是岗位适配模型，不提供录用概率。

个人风格保存到 `~/.smart-resume/styles/<名称>/`，只含 `profile.json` 与 `STYLE.md`，不保存个人经历。可用 `--profiles-dir` 自选目录，已有风格拒绝覆盖；颜色对比度与间距会校验。随包发布的风格画廊不含个人资料。

### 质量验收

```text
python scripts/quality.py output/technical examples/demo.json --demo
```

校验 A4、页数、选中内容、文件哈希和排版边界，生成 `quality.json`。首次会返回未完成：PDF 逐页视觉复核、事实复核及 HTML 检查均须实际执行，再按 [风格与验收说明](skills/smart-resume/references/styles.md) 记录审阅者与结论。虚构示例只能验收为预览，永远不可投递；溢出会报错，不缩字、不隐藏内容。HTML 与 PDF 为两种独立渲染，修改 JSON 后重新生成两者。

<a id="usage"></a>

## 实际怎么用

装好后对 AI 说一句话就行：

> 用 $smart-resume 按这张 JD 截图做定制简历。先读我授权范围内的资料，
> 不够先问我要旧简历，其他缺项逐项问。求职意向只用截图里的岗位名。

AI 会：读你的资料 → 缺什么问你 → 挑相关经历重排 → 出 PDF + 可编辑版 → 逐页验排版。
它不会编造经历，也不会把别的岗位混进来。

<a id="structure"></a>

## 这个技能长什么样

{{SKILL_TREE}}

<a id="limits"></a>

## 它不做什么

- 技能本体在 `skills/smart-resume/`，脚本只做校验和排版；识别截图、挑经历是宿主 AI 的活。
- 可编辑版是 HTML，**不提供 Word/DOCX**；改 HTML 不会同步 PDF，改 JSON 后重新生成。
- 记忆里的经历需要你确认；脚本只能检查"有没有来源"，判断不了真假。
- 不会替你投简历、不会公开上传任何东西，动外部系统前一定问你。

<a id="license"></a>

## 许可证

本项目采用 [MIT 许可证](LICENSE)：可自由使用、修改、商用；分发时须保留版权及许可声明。风格规范与画廊机制参考 [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar)，六种简历排版为本项目独立实现，无须安装其视频运行环境。
