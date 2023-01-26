"""Build index.md from directory listing

make_index.py </path/to/directory>
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

EXCLUDED = ("index.md",)
BASE_URL = "https://marcelotduarte.github.io/packages"


def normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def index_md(
        directory: Path, masks: list[str], base: str, output: Path | None
    ) -> None:
    normalized_directory = directory.with_name(normalize(directory.name))
    if directory.name != normalized_directory.name:
        directory.rename(normalized_directory)
    fnames = []
    for mask in masks:
        fnames += [
            file.relative_to(normalized_directory).as_posix()
            for file in normalized_directory.glob("**/" + mask)
            if file.is_file() and file.name not in EXCLUDED
        ]
    mark = [f"## Links for {base}"]
    normalized_base = normalized_directory.name
    for name in sorted(fnames):
        mark.append(f"[{name}]({BASE_URL}/{normalized_base}/{name})")
    if output is None:
        output = normalized_directory / "index.md"
    output.write_text("\n\n".join(mark))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--mask", action="append")
    parser.add_argument("--base")
    parser.add_argument("--output")
    args = parser.parse_args()
    directory = Path(args.directory)
    if args.base is None:
        args.base = directory.name
    if args.output is None:
        output = directory / "index.md"
    else:
        output = Path(args.output)
    index_md(directory, args.mask or ["*"], args.base, output)


if __name__ == "__main__":
    main()
