#!/usr/bin/env python3
"""
Recolor the round POI icons in osm-liberty's svgs/svgs_iconset for a dark theme.

Only touches <rect> fills/strokes (the white circle + gray shadow ring),
never <path> fills (the category-color glyphs) — so it's safe to run even
on folders that also contain your already-adapted transport-style icons
(entrance.svg, bus.svg, car.svg, etc.), which use #fff on a <path>, not
a <rect>, and are left untouched.

Usage:
    cd svgs/svgs_iconset
    python3 recolor.py

Edit CIRCLE_BG / RING below to taste, then rerun any time.
"""
import re
import glob

CIRCLE_BG = "#2b2f33"   # was #fff  (the round background)
RING      = "#45484d"   # was #bbb  (the thin border/shadow ring)


def fix_rects(svg: str) -> str:
    def repl(m: re.Match) -> str:
        tag = m.group(0)
        tag = re.sub(r'fill="#fff"', f'fill="{CIRCLE_BG}"', tag)
        tag = re.sub(r'fill="#bbb"', f'fill="{RING}"', tag)
        tag = re.sub(r'stroke="#bbb"', f'stroke="{RING}"', tag)
        return tag
    return re.sub(r'<rect\b[^>]*>', repl, svg)


def main():
    changed = 0
    files = glob.glob("*.svg")
    if not files:
        print("No .svg files found in the current directory. "
              "Run this from svgs/svgs_iconset/.")
        return
    for f in files:
        with open(f, encoding="utf-8") as fh:
            src = fh.read()
        out = fix_rects(src)
        if out != src:
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(out)
            changed += 1
    print(f"Updated {changed} of {len(files)} files")


if __name__ == "__main__":
    main()
