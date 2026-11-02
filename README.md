[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [English](README.en.md)

# Smart Resume Skill

**一张 JD 截图 + 已有资料 → 有据可查的定制简历。**

版本 **0.1.0** · Python **3.10+** · 许可证 **0BSD**

这是一套可安装的 Agent Skill：Agent 负责识别岗位、读取获准资料和定制内容；
本地脚本负责资料结构检查、两页 A4 PDF、可编辑 HTML 和独立验收记录。
它不是单独的聊天网站，也不自带模型、历史记忆服务或 OCR。

## 先看成品

[`examples/demo.json`](examples/demo.json) 是完全虚构的中文示例。
执行下方命令即可得到实际 PDF 与可编辑 HTML；每页标注“虚构示例 · 不可投递”。
示例采用少量文字说明结构，不代表真实候选人的完整两页履历。
交付说明与实测结果见 [验收文档](docs/ACCEPTANCE.md)，任务范围见 [任务文档](docs/TASKS.md)。

## 安装和快速开始

解压下载包，进入包含 `SKILL.md` 的 `smart-resume` 目录。Windows/macOS/Linux：

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

也可使用自己的 Agent 支持的 skills 目录作为 `--target`；目录必须尚不存在，
安装器不会覆盖已有版本。安装只复制白名单项目文件，不复制个人输入和产物，
也不会替 Agent 安装 Python 依赖。执行脚本时继续使用上述已装依赖的解释器。
让 Agent 重新发现 Skill；若环境不支持 Skill 发现，可直接读取 `SKILL.md` 执行，
但这不等于已完成原生安装。手动安装时可将整个干净项目文件夹复制至 skills 目录。

以下示例中的 `python` 指上述虚拟环境的 Python：

```text
python scripts/resume.py validate examples/demo.json --demo
python scripts/resume.py render examples/demo.json --demo --out output/demo
```

得到 `output/demo/resume.pdf`、`resume.html` 和私有 `review.json`。
已有输出目录不会覆盖；再次运行请换目录。中文字体优先查找 Windows 宋体；
其他系统用 `--font /path/to/font.ttf`，或设置 `SMART_RESUME_FONT`。
字体必须覆盖所有输出文字，且应为 ReportLab 支持的 TrueType 字体。
字体缺失会报错，不会用方框代替文字继续交付。项目不分发系统字体。

## 实际使用

向已安装 Skill 的 Agent 发送：

> 使用 $smart-resume，按这张 JD 截图做定制简历。先读取我已授权的相关记忆和资料；
> 不足时先向我要旧简历，其他缺项逐项询问。求职意向只用截图中的岗位名称。
> 默认两页 A4，交付 PDF 和可编辑版，逐页检查排版，不编造经历。

Agent 应先读资料，再询问，不要求重新填写所有信息。没有旧简历且其他材料不足时，
先索取旧简历；照片未确定时询问“提供还是不放”，不能默认强制上传。
记忆中的经历要确认，资料冲突要澄清，不可读取未经授权的账号或其他人的信息。
截图不可读就询问，不猜岗位名。图片识别能力由宿主 Agent 提供。

创建私有工作文件（真实资料请放到项目外的私人目录）：

```text
python scripts/resume.py init --out ../private-resume/resume.json
python scripts/resume.py validate ../private-resume/resume.json
python scripts/resume.py render ../private-resume/resume.json --out ../private-resume/delivery
```

空白模板故意无法通过校验；Agent 必须根据真实来源补齐后再生成。
`document_supported` 表示资料支持，`user_confirmed` 表示用户确认，
两者均不等于第三方认证。推测、待确认、冲突内容不能进入成稿。
脚本检查来源引用与状态，**不能判断内容真假或自动理解 JD 匹配度**。

## 交付与排版验收

默认两页 A4，正文 10.5pt。内容不够时询问是否改为一页，不凑经历；
内容过多时报错，修改内容再生成，不静默缩字或截断。
支持不放照片，或从私有目录嵌入 PNG/JPEG，不联网加载照片。
PDF 可选择文字；HTML 可点击正文编辑并“另存为”；JSON 是再次生成的内容源。
**本版可编辑版为 HTML，不包含 DOCX。** 编辑 HTML 不会自动更新 PDF。

自动生成的 `review.json` 排版、事实和 HTML 检查均为 `pending`；
Agent 必须实际查看 PDF 每页图像，核对文字和事实，再记录验收结果。
PDF 和 HTML 使用不同排版引擎，HTML 打印效果不能代替 PDF 验收。
交给招聘方时只给简历，来源记录、缺口说明留在私人目录。

## 项目目录

```text
smart-resume/
├── SKILL.md                 Agent 执行入口
├── README*.md               三语言首页
├── assets/                  空白输入和 HTML 模板
├── examples/demo.json       纯虚构示例
├── references/workflow.md   资料、证据、验收约定
├── scripts/                 生成、安装、打包
├── tests/                   行为测试
├── docs/                    任务与验收
└── .github/                 自动检查和 PR 模板
```

## 使用示例

输入一份填好的私人资料文件，得到 PDF、可编辑 HTML 和验收记录：

```text
python scripts/resume.py validate ../private-resume/resume.json
python scripts/resume.py render ../private-resume/resume.json --out ../private-resume/delivery
```

交付物：`delivery/resume.pdf`（两页 A4）、`delivery/resume.html`（可编辑）、
`delivery/review.json`（排版与事实检查记录）。资料不足或存在冲突时，
脚本会报错而不是猜内容。

## 贡献

阅读 [CONTRIBUTING.md](CONTRIBUTING.md)；Agent 请遵守 [AGENTS.md](AGENTS.md)。

## 许可证

本项目采用 [LICENSE](LICENSE) 所载的 0BSD 许可。

## 开发、测试和打包

```text
python -m unittest discover -s tests -v
python scripts/package.py --out dist/smart-resume-0.1.0.zip
```

打包采用固定白名单，输出 SHA-256；不包含 `output`、`.venv`、真实简历或照片。
白名单无法判断白名单文件是否被人改成个人资料，发布前仍要人工审查差异。
CI 配置在 Windows/Linux 测试，配置存在不代表远端 CI 已运行。
贡献请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，Agent 请遵守 [AGENTS.md](AGENTS.md)。

## 常见问题与隐私

- **找不到历史记录？** 只能使用宿主实际授权提供的资料，不会凭空取得其他聊天。
- **只给一张截图能自动完工吗？** 缺少个人经历时必须补资料，不会生成虚假经历。
- **字体报错？** 指定覆盖输出文字的 TrueType 字体；复杂文字塑形需另行验证。
- **可以公开示例吗？** 项目只有虚构示例；不要把真实输入、电话、照片加入仓库。
- **会自动投递或发布 GitHub 吗？** 不会。发送简历、上传或推送需要用户授权。
- **安装完成就会自己运行吗？** 取决于宿主发现与触发机制；本项目已提供安装器，
  原生发现应在目标 Agent 中确认。

许可证见 [LICENSE](LICENSE)。三种 README 同属 0.1.0，功能变化请同步维护。
