"""Build an offline gallery backed by six real PDF renders of synthetic data."""

import argparse
import html
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import resume
import styles


def build(out, input_path=None, font=None, pdftoppm="pdftoppm", compact=False):
    out = Path(out).resolve()
    if out.exists():
        raise ValueError("Gallery exists; choose a new output directory")
    executable = shutil.which(str(pdftoppm))
    if not executable:
        raise ValueError("Poppler pdftoppm is required for real PDF previews; pass --pdftoppm")
    input_path = Path(input_path) if input_path else resume.ROOT / "examples/demo.json"
    data = resume.load(input_path)
    resume.validate(data, demo=True)
    if compact:
        data["pages"] = [[section for page in data["pages"] for section in page]]
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".gallery-", dir=out.parent) as temporary:
        staging = Path(temporary) / "gallery"
        staging.mkdir()
        (staging / "demo-input.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        cards, manifest = [], []
        for item in styles.CATALOG["styles"]:
            slug = item["id"]
            target = staging / slug
            report = resume.render(data, input_path.resolve().parent, target, font, True, style=slug)
            subprocess.run([executable, "-r", "85", "-png", str(target / "resume.pdf"), str(target / "page")],
                           check=True, capture_output=True, timeout=90)
            images = sorted(target.glob("page-*.png"))
            if len(images) != report["page_count"]:
                raise ValueError(f"Missing PDF preview pages for {slug}")
            name = item["names"][data["language"]]
            detail = styles.describe(slug, data["language"])
            guidance = html.escape(" · ".join(detail["roles"]) + " | " + " · ".join(detail["channels"])
                                   + " | ATS: " + detail["ats"] + " — " + detail["ats_note"])
            thumbnails = "".join(
                f'<a href="{slug}/{image.name}"><img loading="lazy" src="{slug}/{image.name}" alt="{html.escape(name)} · {index}"></a>'
                for index, image in enumerate(images, 1))
            cards.append(
                f'<article data-style="{slug}"><header><span>{slug.upper()}</span><h2>{html.escape(name)}</h2><p>{guidance}</p></header>'
                f'<div class="pages{" single" if len(images) == 1 else ""}">{thumbnails}</div><nav aria-label="{slug} downloads">'
                f'<a href="{slug}/resume.pdf">PDF ↗</a><a href="{slug}/resume.html">HTML ↗</a>'
                f'<a href="{slug}/review.json">Review JSON ↗</a></nav></article>')
            manifest.append({"id": slug, "names": item["names"], "pdf": f"{slug}/resume.pdf",
                             "html": f"{slug}/resume.html", "pages": [f"{slug}/{image.name}" for image in images]})
        title = {"zh-CN": "选择你的简历风格", "zh-TW": "選擇你的履歷風格", "en": "Choose your resume style"}[data["language"]]
        notice = resume.LANGUAGES[data["language"]][1]
        body = """<!doctype html><html lang="LANG"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Smart Resume · Gallery</title>
<style>*{box-sizing:border-box}body{margin:0;background:#f3f4f2;color:#202a26;font:16px Arial,"Microsoft YaHei",sans-serif}
main{max-width:1440px;margin:auto;padding:48px 32px}h1{font-size:clamp(28px,4vw,48px);margin:16px 0}
.eyebrow{letter-spacing:.16em;font-size:12px;color:#416454}.notice{color:#853b36;line-height:1.6}
.filter{display:flex;gap:12px;align-items:center;margin:28px 0}select{padding:10px;font:inherit;max-width:100%}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}article{background:white;border:1px solid #d6ddd7;border-radius:6px;overflow:hidden}
header{padding:20px}header span{font-size:11px;letter-spacing:.1em;color:#56675d}h2{font-size:21px;margin:10px 0 0}
.pages{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:0 16px 16px}.pages img{display:block;width:100%;height:auto;border:1px solid #e4e8e4}
.pages.single{grid-template-columns:minmax(0,1fr)}
nav{display:flex;flex-wrap:wrap;gap:18px;border-top:1px solid #e4e8e4;padding:16px}a{color:#244d68;text-underline-offset:4px}
[hidden]{display:none!important}@media(max-width:1050px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:600px){main{padding:24px 16px}.grid{grid-template-columns:minmax(0,1fr)}.filter{flex-wrap:wrap}}
</style><main><p class="eyebrow">SMART RESUME / STYLE LIBRARY / 06</p><h1>TITLE</h1>
<p class="notice">NOTICE</p><p>PDF → PNG · A4 · 10.5 pt · 6 PDF + 6 HTML</p>
<div class="filter"><label for="style">Style / 风格 / 風格</label><select id="style"><option value="all">All / 全部</option>OPTIONS</select></div>
<div class="grid">CARDS</div></main><script>
document.getElementById('style').addEventListener('change',function(){
document.querySelectorAll('article[data-style]').forEach(card=>card.hidden=this.value!=='all'&&card.dataset.style!==this.value);
});</script></html>"""
        options = "".join(f'<option value="{item["id"]}">{html.escape(item["names"][data["language"]])}</option>' for item in styles.CATALOG["styles"])
        for token, value in (("LANG", data["language"]), ("TITLE", html.escape(title)), ("NOTICE", html.escape(notice)),
                             ("OPTIONS", options), ("CARDS", "".join(cards))):
            body = body.replace(token, value)
        (staging / "index.html").write_text(body, encoding="utf-8")
        (staging / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        staging.rename(out)
    return out / "index.html"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--font", type=Path)
    parser.add_argument("--pdftoppm", default="pdftoppm")
    parser.add_argument("--compact", action="store_true", help="Combine all fictional sections onto one page; never shrink text")
    args = parser.parse_args()
    try:
        print(build(args.out, args.input, args.font, args.pdftoppm, args.compact))
    except (ValueError, OSError, subprocess.SubprocessError, ImportError) as error:
        parser.exit(2, f"Error: {error}\n")
