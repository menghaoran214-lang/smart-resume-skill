"""Install a new skill directory; never replace an existing installation."""

import argparse
from pathlib import Path
import shutil
import tempfile

from package import ROOT, package_files


def install(target, root=ROOT):
    target = Path(target).expanduser().resolve()
    root = Path(root).resolve()
    if target.exists():
        raise ValueError("Target already exists; back it up and choose a new target")
    if target.is_relative_to(root) or root.is_relative_to(target):
        raise ValueError("Installation and source directories must be separate")
    entries = list(package_files(root))
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".smart-resume-install-", dir=target.parent) as temporary:
        staging = Path(temporary) / "smart-resume"
        staging.mkdir()
        for relative, source in entries:
            destination = staging / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        staging.rename(target)
    return target


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True, help="New skill folder, e.g. ~/.codex/skills/smart-resume")
    args = parser.parse_args()
    try:
        print(f"Installed: {install(args.target)}")
    except (ValueError, OSError) as error:
        parser.exit(2, f"Error: {error}\n")
