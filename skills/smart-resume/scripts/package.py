"""Build an allowlisted, reproducible skill archive without personal artifacts."""

import argparse
import hashlib
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "SKILL.md", "VERSION", "LICENSE", "requirements.txt",
    "references/workflow.md", "assets/intake.json",
    "assets/resume.html", "examples/demo.json", "scripts/resume.py",
    "scripts/install.py", "scripts/package.py", "tests/test_resume.py",
)


def package_files(root=ROOT):
    root = Path(root).resolve()
    for relative in FILES:
        path = root / relative
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError(f"Missing or unsafe package file: {relative}")
        yield relative, path


def build(output, root=ROOT):
    output = Path(output)
    if output.exists():
        raise ValueError("Archive already exists; use a new filename")
    entries = [(relative, path.read_bytes()) for relative, path in package_files(root)]
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as stream:
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for relative, content in entries:
                info = zipfile.ZipInfo(f"smart-resume/{relative}", date_time=(2026, 11, 2, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, content)
    return hashlib.sha256(output.read_bytes()).hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    print(f"SHA256 {build(args.out)}")
