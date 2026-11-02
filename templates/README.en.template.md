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

## What this is

{{WHAT}}

**Who it is for**: {{AUDIENCE}}

{{TOC}}

<a id="install"></a>

## How to install

<a id="install-ai"></a>

### Easiest: send one line to your AI

Send this to an AI that supports installing skills and can access the repository and write files:

```text
{{INSTALL_PROMPT}}
```

The AI needs repository access and an environment where skills can be installed.
An ordinary chat may not support installation. On a phone, use an AI connected
to a computer or cloud runtime; this is not a native iOS installation.

<a id="install-manual"></a>

### Or install it yourself (Windows, macOS and Linux)

```text
{{INSTALL}}
```

Requires Git and Python 3.10+. On Windows use `py` or `python` instead of `python3`.
The target shown is for Codex; other agents need their own skill directory.
Use a separate virtual environment for dependencies.

<a id="demo"></a>

## See the finished output in 30 seconds

After installing dependencies, run this from the repository root to preview
the layout with **fictional data**. It only generates files; it does not read a
screenshot or your personal materials.

```text
{{DEMO}}
```

| File | What it is |
| --- | --- |
| `output/demo/resume.pdf` | Two A4 sample pages for preview only; do not submit |
| `output/demo/resume.html` | The same resume as a web page; click to edit |
| `output/demo/review.json` | Layout and fact review record for you or the AI to check |

The sample data is made up, every page says "fictional sample, do not submit",
and it cannot be mistaken for a real resume.

<a id="usage"></a>

## How you use it

After installing, say one sentence to your AI:

> Use $smart-resume to tailor my resume to this JD screenshot. Read the materials
> you are authorized to access, ask for my old resume first if that is not enough,
> then ask about the rest one item at a time. Use only the exact JD title.

The AI reads your materials, asks for what is missing, reorders the relevant
experience around that role, produces the PDF and editable version, and checks
every page. It does not invent experience and does not mix in another role.

<a id="structure"></a>

## What is inside

{{SKILL_TREE}}

<a id="limits"></a>

## What it does not do

- The skill lives in `skills/smart-resume/`. The scripts validate and typeset;
  reading the screenshot and picking the right experience is the host AI's job.
- The editable format is HTML. **There is no Word/DOCX export**; HTML edits do
  not update the PDF, so change the JSON and regenerate.
- Remembered experience needs your confirmation. Scripts can check that a source
  exists; they cannot judge whether it is true.
- It never submits applications or uploads anything; it asks before touching
  any external system.

<a id="license"></a>

## License

[0BSD](LICENSE) · Use, modify and use commercially; provided as is, without warranty.
