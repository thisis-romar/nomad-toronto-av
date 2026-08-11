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

sys.path.insert(0, str(Path(__file__).parent))
from rack_palette import hex_of, short, ink_on  # noqa: E402

# --- Label geometry (mm) -----------------------------------------------------

L = 23.0          # DK-1221 die-cut size

# Printable area, taken from a real P-touch Editor file for DK-1221 on a QL-800:
# backGround x=8.4pt y=4.3pt w=48.5pt h=56.7pt  ->  17.11 x 20.00 mm, inset
# 2.96 mm left/right and 1.52 mm top/bottom. This is NOT the uniform 1.5 mm
# margin an earlier draft assumed -- that put every line of text 2.89 mm wider
# than the head can mark, so the ends would have been clipped on the roll.
SAFE_X = 2.96     # unprintable margin, left/right
SAFE_Y = 1.52     # unprintable margin, top/bottom
SAFE = SAFE_Y     # vertical margin is what the face geometry keys off
LIVE_W = L - 2 * SAFE_X   # 17.08 mm of usable text width
FOLD_TAG = 3.0    # blank fold zone when folding over a cable-tie tail
FOLD_FLAG_OD = 8.0  # default cable OD (mm) for the direct-to-cable flag fold
TICK = 1.2        # length of the fold-registration ticks at the label edges

FONT = "Arial Narrow, Liberation Sans Narrow, Helvetica Neue, Helvetica, sans-serif"

# Liberation Sans is metric-compatible with Arial, but the label prints in
# Arial NARROW, which is ~82% of Arial's advance width. Measuring in Arial and
# pretending that is the render font was a free safety margin while the live
# width was assumed to be 20 mm; against the real 17.08 mm it manufactures
# false "too wide" verdicts and shrinks text that would have fitted. Measure in
# Arial, then scale by the narrow ratio -- 0.85 rather than 0.82, keeping a
# little headroom for whatever condensed face is actually installed.
NARROW_RATIO = 0.85
METRIC_FONTS = {
    "bold": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "normal": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
}
MIN_SIZE = {"line1": 2.6, "line2": 1.9, "line3": 1.8}  # mm — floor before we give up shrinking
# Nominal sizes per layout. The face is 8.5 mm tall; two lines leave ~1.5 mm of it
# unused, which is exactly the room a third line needs once the headline has to
# carry a device AND a port.
LAYOUT_2 = ((4.0, True, 3.6), (2.8, False, 7.0))
LAYOUT_3 = ((3.4, True, 2.7), (2.4, False, 5.4), (2.2, False, 7.9))
_fit_warnings = []

# --- Sheet layout (mm, A4 portrait) ------------------------------------------

PAGE_W, PAGE_H = 210.0, 297.0
MARGIN_X, MARGIN_TOP = 14.0, 20.0
GUTTER_X, GUTTER_Y = 8.0, 17.0   # gutter_y leaves room for the device swatch + caption
COLS = 5


def connector_pair(row):
    """Caption text for the connector at each end: 'XLR-M→XLR-F', or just the
    one type when both ends match. Collapses to '—' for spare/blank rows."""
    a, b = row.get("conn_a", "").strip(), row.get("conn_b", "").strip()
    if not a and not b:
        return "—"
    if a == b or not b:
        return a or "—"
    if not a:
        return b
    return f"{a}→{b}"


def flag_face_height(od_mm):
    """Face height each side when the label is folded directly around a cable."""
    return (L - math.pi * od_mm / 2) / 2


def measure(s, size_mm, weight):
    """Width of s in mm when set in Arial at size_mm."""
    if ImageFont is None:
        return len(s) * size_mm * 0.52 * NARROW_RATIO
    px = 200  # measure at a large size, then scale — avoids hinting error
    try:
        f = ImageFont.truetype(METRIC_FONTS[weight], px)
    except OSError:
        return len(s) * size_mm * 0.52 * NARROW_RATIO
    return f.getlength(s) / px * size_mm * NARROW_RATIO


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


def face(lines, invert, label_id=""):
    """One printed face of a TAG label, drawn in the lower half of the square.

    `lines` is 2 or 3 strings. Returns SVG in label-local coordinates.
    """
    ink = "#fff" if invert else "#000"
    top = (L + FOLD_TAG) / 2          # 13.0
    # Inverse panels need real padding: white text butted against the edge of a
    # black field reads as clipped, and thermal ink bleed eats the gap further.
    max_w = LIVE_W - (2.5 if invert else 0.0)
    out = []
    if invert:
        out.append(
            f'<rect x="{SAFE_X:.2f}" y="{top:.2f}" width="{LIVE_W:.2f}" '
            f'height="{L - SAFE_Y - top:.2f}" fill="#000" rx="0.6"/>'
        )
    layout = LAYOUT_3 if len(lines) >= 3 else LAYOUT_2
    for i, (s, (nominal, bold, dy)) in enumerate(zip(lines, layout)):
        key = f"line{i + 1}"
        size, tl, clamped = fit(s, nominal, "bold" if bold else "normal",
                                max_w, MIN_SIZE[key])
        if clamped:
            _fit_warnings.append(
                f"{label_id} {key}: hit the {MIN_SIZE[key]} mm floor — glyphs squeezed, shorten the copy")
        elif i == 0 and size < nominal * 0.75:
            _fit_warnings.append(f"{label_id} {key}: dropped to {size:.1f} mm to fit")
        out.append(text(L / 2, top + dy, s, size, "bold" if bold else "normal",
                        ink, length=tl))
    return "".join(out)


def label_tag(lines, invert=False, label_id=""):
    """A fold-over tag: lower half upright, upper half rotated 180 deg."""
    body = face(lines, invert, label_id)
    return (
        f'<g>{body}</g>'
        f'<g transform="rotate(180 {L / 2:.2f} {L / 2:.2f})">{body}</g>'
        # fold registration ticks on both edges
        f'<line x1="0" y1="{L / 2:.2f}" x2="{TICK:.2f}" y2="{L / 2:.2f}" '
        f'stroke="#000" stroke-width="0.25"/>'
        f'<line x1="{L - TICK:.2f}" y1="{L / 2:.2f}" x2="{L:.2f}" y2="{L / 2:.2f}" '
        f'stroke="#000" stroke-width="0.25"/>'
    )


def walk(rows):
    """Yield (row, starts_group, group_len) so the layout can avoid splitting.

    A row with an empty `group` is a group of one. Rows sharing a group value
    are assumed contiguous in the CSV, which is how the sets are authored.
    """
    i = 0
    while i < len(rows):
        g = (rows[i].get("group") or "").strip()
        if not g:
            yield rows[i], True, 1
            i += 1
            continue
        j = i
        while j < len(rows) and (rows[j].get("group") or "").strip() == g:
            j += 1
        for k in range(i, j):
            yield rows[k], k == i, j - i
        i = j


def render(rows, out_path, set_name="POWER"):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAGE_W}mm" height="{PAGE_H}mm" '
        f'viewBox="0 0 {PAGE_W} {PAGE_H}">',
        f'<title>NOMAD Toronto - DK-1221 {set_name.lower()} cable label proof (1:1)</title>',
        f'<rect width="{PAGE_W}" height="{PAGE_H}" fill="#fff"/>',
        text(MARGIN_X, 12, f"NØMAD TORONTO — DK-1221 {set_name} LABEL PROOF", 4.2, "bold", "#000", "start"),
        text(MARGIN_X, 16.5,
             "23 × 23 mm at 1:1 — print at 100% (no scale-to-fit) and measure a square before running the roll.",
             2.6, "normal", "#444", "start"),
    ]

    x = MARGIN_X
    y = MARGIN_TOP + 6
    col = 0
    for row, starts_group, group_len in walk(rows):
        # Never split a group across a row break. An L/R pair with the L at the
        # end of one row and the R at the start of the next is the kind of thing
        # that gets one of them stuck on the wrong cable.
        if col == COLS or (starts_group and group_len <= COLS and col + group_len > COLS):
            col = 0
            x = MARGIN_X
            y += L + GUTTER_Y
        parts.append(f'<g transform="translate({x:.2f} {y:.2f})">')
        # die-cut outline + safe area, proof only (not printed on the roll)
        parts.append(f'<rect width="{L}" height="{L}" fill="none" stroke="#c8102e" stroke-width="0.2"/>')
        parts.append(
            f'<rect x="{SAFE_X}" y="{SAFE_Y}" width="{LIVE_W:.2f}" height="{L - 2 * SAFE_Y:.2f}" '
            f'fill="none" stroke="#bbb" stroke-width="0.15" stroke-dasharray="0.8 0.8"/>'
        )
        parts.append(
            f'<line x1="0" y1="{L / 2}" x2="{L}" y2="{L / 2}" stroke="#0a84ff" '
            f'stroke-width="0.15" stroke-dasharray="1.5 1"/>'
        )
        lines = [row["line1"], row["line2"]]
        if (row.get("line3") or "").strip():
            lines.append(row["line3"])
        parts.append(label_tag(lines, row["invert"].strip().lower() == "yes", row["id"]))
        parts.append("</g>")
        # Device swatch, proof only: end A | end B, each carrying the device's
        # short name printed on its own colour. Naming it here is what stops the
        # colour needing a legend lookup every time.
        bar_y, bar_h, half = y + L + 1.2, 3.4, (L - 0.6) / 2
        for idx, end in enumerate(("end_a_device", "end_b_device")):
            dev = row.get(end, "")
            hexv = hex_of(dev)
            bx = x + idx * (half + 0.6)
            parts.append(f'<rect x="{bx:.2f}" y="{bar_y:.2f}" width="{half:.2f}" '
                         f'height="{bar_h}" fill="{hexv}" rx="0.4"/>')
            name = short(dev)
            fs, tl, _ = fit(name, 2.1, "bold", half - 1.0, 1.5)
            parts.append(text(bx + half / 2, bar_y + 2.45, name, fs, "bold",
                              ink_on(hexv), length=tl))
        # caption below the label (proof only)
        parts.append(text(x + L / 2, y + L + 8.4, row["id"], 2.4, "bold", "#000"))
        parts.append(text(x + L / 2, y + L + 11.4,
                          f'x{row["qty"]}  {connector_pair(row)}', 2.2, "normal", "#666"))
        x += L + GUTTER_X
        col += 1

    y_legend = y + L + GUTTER_Y + 4
    parts += [
        f'<line x1="{MARGIN_X}" y1="{y_legend:.2f}" x2="{PAGE_W - MARGIN_X}" y2="{y_legend:.2f}" stroke="#ddd" stroke-width="0.3"/>',
        text(MARGIN_X, y_legend + 6, "PROOF GUIDES (not printed on the roll)", 3.0, "bold", "#000", "start"),
        text(MARGIN_X, y_legend + 10.5, "red = 23 mm die-cut edge   ·   grey dash = printable area 17.1 × 20.0 mm (Editor's own margins)   ·   blue dash = fold line", 2.5, "normal", "#444", "start"),
        text(MARGIN_X, y_legend + 15.5, "PRINTED ON THE ROLL: the two text faces and the two 1.2 mm fold ticks at the label edges.", 2.5, "normal", "#444", "start"),
        text(MARGIN_X, y_legend + 21.5, "FOLD: adhesive-to-adhesive over a cable-tie tail on the fold line. Both faces then read upright.", 2.5, "normal", "#444", "start"),
        text(MARGIN_X, y_legend + 26.5,
             f"Every set uses the tie tag for consistency. Folding straight onto the cable is only viable to "
             f"~8 mm OD (face {flag_face_height(FOLD_FLAG_OD):.1f} mm) and is single-line at that size.",
             2.5, "normal", "#444", "start"),
        # No colour key: each swatch carries its own device name, so there is
        # nothing to look up. The only fact colour alone still encodes is which
        # tie to reach for, and the swatch names that device too.
        text(MARGIN_X, y_legend + 33.0, "DEVICE SWATCH — the two chips under each label are end A | end B, each named on its own colour.", 2.5, "bold", "#000", "start"),
        text(MARGIN_X, y_legend + 36.6, "DK-1221 prints BLACK ONLY: the labels themselves carry no colour. On the rack, match the cable tie to the chip colour.", 2.5, "normal", "#444", "start"),
    ]

    parts.append("</svg>")

    Path(out_path).write_text("\n".join(p for p in parts if p), encoding="utf-8")
    return len(rows)


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "07-tech-pack/labeling/labels-power.csv")
    dst = Path(sys.argv[2] if len(sys.argv) > 2 else "07-tech-pack/labeling/dk1221-power-proof.svg")
    # Set name for the sheet header: 3rd arg, else inferred from labels-<name>.csv
    set_name = sys.argv[3] if len(sys.argv) > 3 else src.stem.replace("labels-", "").upper()
    with src.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    n = render(rows, dst, set_name)
    total = sum(int(r["qty"]) for r in rows)
    print(f"{dst}: {n} label designs, {total} labels to print")
    for w in dict.fromkeys(_fit_warnings):
        print(f"  ! {w}")


if __name__ == "__main__":
    main()
