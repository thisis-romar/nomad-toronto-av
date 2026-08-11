#!/usr/bin/env python3
"""Build a 1:1 print proof of DK-1221 cable labels from a CSV.

DK-1221 is a 23 mm x 23 mm die-cut paper label for Brother QL printers.
The proof sheet renders every label at true size on A4 so the artwork can be
checked against the roll before committing a print run.

Usage:
    python3 scripts/build-cable-labels.py \
        07-tech-pack/labeling/labels-power.csv \
        07-tech-pack/labeling/dk1221-power-proof.svg

Geometry is documented in 07-tech-pack/labeling/cable-label-spec.md.
"""

import csv
import math
import sys
from pathlib import Path
from xml.sax.saxutils import escape

try:
    from PIL import ImageFont
except ImportError:  # width estimation falls back to a per-character average
    ImageFont = None

# --- Label geometry (mm) -----------------------------------------------------

L = 23.0          # DK-1221 die-cut size
SAFE = 1.5        # unprintable / trim safe margin on all four edges
FOLD_TAG = 3.0    # blank fold zone when folding over a cable-tie tail
FOLD_FLAG_OD = 8.0  # default cable OD (mm) for the direct-to-cable flag fold
TICK = 1.2        # length of the fold-registration ticks at the label edges

FONT = "Arial Narrow, Liberation Sans Narrow, Helvetica Neue, Helvetica, sans-serif"

# Text is sized against full-width Arial metrics (Liberation Sans is metric-
# compatible). Arial Narrow is ~82% of that width, so anything that fits here
# also fits on the printer with margin to spare.
METRIC_FONTS = {
    "bold": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "normal": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
}
MIN_SIZE = {"line1": 2.6, "line2": 1.9}   # mm — floor before we give up shrinking
_fit_warnings = []

# --- Sheet layout (mm, A4 portrait) ------------------------------------------

PAGE_W, PAGE_H = 210.0, 297.0
MARGIN_X, MARGIN_TOP = 14.0, 20.0
GUTTER_X, GUTTER_Y = 8.0, 13.0   # gutter_y leaves room for the caption
COLS = 5


def flag_face_height(od_mm):
    """Face height each side when the label is folded directly around a cable."""
    return (L - math.pi * od_mm / 2) / 2


def measure(s, size_mm, weight):
    """Width of s in mm when set in Arial at size_mm."""
    if ImageFont is None:
        return len(s) * size_mm * 0.52
    px = 200  # measure at a large size, then scale — avoids hinting error
    try:
        f = ImageFont.truetype(METRIC_FONTS[weight], px)
    except OSError:
        return len(s) * size_mm * 0.52
    return f.getlength(s) / px * size_mm


def fit(s, size_mm, weight, max_w, floor):
    """Shrink size_mm until s fits max_w.

    Returns (size, textLength). textLength is always set so the proof renders at
    the intended physical width on any machine, whatever font it substitutes —
    a dimensional proof has to be font-independent. `clamped` is reported when
    the string only fits by squeezing glyphs at the minimum size.
    """
    size = size_mm
    while size > floor and measure(s, size, weight) > max_w:
        size -= 0.05
    w = measure(s, size, weight)
    return size, min(w, max_w), w > max_w


def text(x, y, s, size, weight="normal", fill="#000", anchor="middle", length=None):
    if not s:
        return ""
    extra = ""
    if length:
        extra = f' textLength="{length:.2f}" lengthAdjust="spacingAndGlyphs"'
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{size:.2f}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{extra}>{escape(s)}</text>'
    )


def face(line1, line2, invert, label_id=""):
    """One printed face of a TAG label, drawn in the lower half of the square.

    Returns SVG positioned in label-local coordinates (origin at label corner).
    """
    ink = "#fff" if invert else "#000"
    top = (L + FOLD_TAG) / 2          # 13.0
    max_w = L - 2 * SAFE - (1.0 if invert else 0.0)   # inverse panels need side padding
    out = []
    if invert:
        out.append(
            f'<rect x="{SAFE:.2f}" y="{top:.2f}" width="{L - 2 * SAFE:.2f}" '
            f'height="{L - SAFE - top:.2f}" fill="#000" rx="0.6"/>'
        )
    s1, t1, clamp1 = fit(line1, 4.0, "bold", max_w, MIN_SIZE["line1"])
    s2, t2, clamp2 = fit(line2, 2.8, "normal", max_w, MIN_SIZE["line2"])
    for name, size, clamped in (("line1", s1, clamp1), ("line2", s2, clamp2)):
        if clamped:
            _fit_warnings.append(
                f"{label_id} {name}: hit the {MIN_SIZE[name]} mm floor — glyphs squeezed, shorten the copy")
        elif size < 3.0 and name == "line1":
            _fit_warnings.append(f"{label_id} {name}: dropped to {size:.1f} mm to fit")
    out.append(text(L / 2, top + 3.6, line1, s1, "bold", ink, length=t1))
    out.append(text(L / 2, top + 7.0, line2, s2, "normal", ink, length=t2))
    return "".join(out)


def label_tag(line1, line2, invert=False, label_id=""):
    """A fold-over tag: lower half upright, upper half rotated 180 deg."""
    body = face(line1, line2, invert, label_id)
    return (
        f'<g>{body}</g>'
        f'<g transform="rotate(180 {L / 2:.2f} {L / 2:.2f})">{body}</g>'
        # fold registration ticks on both edges
        f'<line x1="0" y1="{L / 2:.2f}" x2="{TICK:.2f}" y2="{L / 2:.2f}" '
        f'stroke="#000" stroke-width="0.25"/>'
        f'<line x1="{L - TICK:.2f}" y1="{L / 2:.2f}" x2="{L:.2f}" y2="{L / 2:.2f}" '
        f'stroke="#000" stroke-width="0.25"/>'
    )


def render(rows, out_path):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAGE_W}mm" height="{PAGE_H}mm" '
        f'viewBox="0 0 {PAGE_W} {PAGE_H}">',
        '<title>NOMAD Toronto - DK-1221 power cable label proof (1:1)</title>',
        f'<rect width="{PAGE_W}" height="{PAGE_H}" fill="#fff"/>',
        text(MARGIN_X, 12, "NØMAD TORONTO — DK-1221 POWER LABEL PROOF", 4.2, "bold", "#000", "start"),
        text(MARGIN_X, 16.5,
             "23 × 23 mm at 1:1 — print at 100% (no scale-to-fit) and measure a square before running the roll.",
             2.6, "normal", "#444", "start"),
    ]

    x = MARGIN_X
    y = MARGIN_TOP + 6
    col = 0
    for row in rows:
        if col == COLS:
            col = 0
            x = MARGIN_X
            y += L + GUTTER_Y
        parts.append(f'<g transform="translate({x:.2f} {y:.2f})">')
        # die-cut outline + safe area, proof only (not printed on the roll)
        parts.append(f'<rect width="{L}" height="{L}" fill="none" stroke="#c8102e" stroke-width="0.2"/>')
        parts.append(
            f'<rect x="{SAFE}" y="{SAFE}" width="{L - 2 * SAFE}" height="{L - 2 * SAFE}" '
            f'fill="none" stroke="#bbb" stroke-width="0.15" stroke-dasharray="0.8 0.8"/>'
        )
        parts.append(
            f'<line x1="0" y1="{L / 2}" x2="{L}" y2="{L / 2}" stroke="#0a84ff" '
            f'stroke-width="0.15" stroke-dasharray="1.5 1"/>'
        )
        parts.append(label_tag(row["line1"], row["line2"],
                               row["invert"].strip().lower() == "yes", row["id"]))
        parts.append("</g>")
        # caption below the label (proof only)
        parts.append(text(x + L / 2, y + L + 3.6, row["id"], 2.4, "bold", "#000"))
        parts.append(text(x + L / 2, y + L + 6.8, f'x{row["qty"]}  {row["connector"]}', 2.2, "normal", "#666"))
        x += L + GUTTER_X
        col += 1

    y_legend = y + L + GUTTER_Y + 4
    parts += [
        f'<line x1="{MARGIN_X}" y1="{y_legend:.2f}" x2="{PAGE_W - MARGIN_X}" y2="{y_legend:.2f}" stroke="#ddd" stroke-width="0.3"/>',
        text(MARGIN_X, y_legend + 6, "PROOF GUIDES (not printed on the roll)", 3.0, "bold", "#000", "start"),
        text(MARGIN_X, y_legend + 10.5, "red = 23 mm die-cut edge   ·   grey dash = 1.5 mm safe margin   ·   blue dash = fold line", 2.5, "normal", "#444", "start"),
        text(MARGIN_X, y_legend + 15.5, "PRINTED ON THE ROLL: the two text faces and the two 1.2 mm fold ticks at the label edges.", 2.5, "normal", "#444", "start"),
        text(MARGIN_X, y_legend + 21.5, "FOLD: adhesive-to-adhesive over a cable-tie tail on the fold line. Both faces then read upright.", 2.5, "normal", "#444", "start"),
        text(MARGIN_X, y_legend + 26.5,
             f"Direct-to-cable fold is only viable to ~8 mm OD (face {flag_face_height(FOLD_FLAG_OD):.1f} mm); "
             f"a 12 mm C19 cord leaves {flag_face_height(12):.1f} mm — use the tie tag.",
             2.5, "normal", "#444", "start"),
        "</svg>",
    ]

    Path(out_path).write_text("\n".join(p for p in parts if p), encoding="utf-8")
    return len(rows)


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "07-tech-pack/labeling/labels-power.csv")
    dst = Path(sys.argv[2] if len(sys.argv) > 2 else "07-tech-pack/labeling/dk1221-power-proof.svg")
    with src.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    n = render(rows, dst)
    total = sum(int(r["qty"]) for r in rows)
    print(f"{dst}: {n} label designs, {total} labels to print")
    for w in dict.fromkeys(_fit_warnings):
        print(f"  ! {w}")


if __name__ == "__main__":
    main()
