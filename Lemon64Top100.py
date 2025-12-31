#!/usr/bin/env python3
# Ultra-simple Lemon64 Top 100 copier (numbered output)
#
# Defaults:
# - Input list:  ./Lemon64Top100.txt   (one title per line, ordered 1–100)
# - Source:      current directory (recursive)
# - Output:      ./!Lemon64 Top 100 Games/
#
# Output filenames:
#   1. Eye of the Beholder (2024).crt
#
# No external dependencies.

import argparse
import re
import shutil
from pathlib import Path


YEAR_RE = re.compile(r"\s*\(\d{4}\)\s*$")


def normalize(s: str) -> str:
    s = YEAR_RE.sub("", s).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", default="Lemon64Top100.txt",
                    help="Plain text file with one game title per line (default: Lemon64Top100.txt)")
    ap.add_argument("--src", default=".",
                    help="Source directory to scan for .crt files (default: current directory)")
    ap.add_argument("--out", default="!Lemon64 Top 100 Games",
                    help="Output folder name (default: !Lemon64 Top 100 Games)")
    args = ap.parse_args()

    list_path = Path(args.list)
    if not list_path.exists():
        raise SystemExit(f"List file not found: {list_path}")

    titles = [
        line.strip()
        for line in list_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    if not titles:
        raise SystemExit("No titles found in list file")

    src_root = Path(args.src)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    crt_files = [(normalize(p.stem), p) for p in src_root.rglob("*.crt") if p.is_file()]
    if not crt_files:
        raise SystemExit(f"No .crt files found under: {src_root}")

    for index, title in enumerate(titles, start=1):
        key = normalize(title)
        match = None

        for stem_norm, path in crt_files:
            if key and key in stem_norm:
                match = path
                break

        if not match:
            print("MISS:", index, title)
            continue

        out_name = f"{index}. {title}.crt"
        out_name = out_name.replace("/", "-").replace("\\", "-")
        out_path = out_dir / out_name

        shutil.copy2(match, out_path)
        print("COPY:", out_name, "->", match)


if __name__ == "__main__":
    main()
