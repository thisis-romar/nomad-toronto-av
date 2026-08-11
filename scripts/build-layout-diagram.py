#!/usr/bin/env python3
"""Draw the DK-1221 tag layout: object boxes, field bindings, folded result.

Generated rather than hand-drawn so the picture cannot drift from the geometry
the label builder and the .lbx generator actually emit — box positions are read
back out of a produced .lbx.

Usage:
    python3 scripts/build-layout-diagram.py \
        07-tech-pack/labeling/dk1221-rack-audio-end-a.lbx \
        07-tech-pack/labeling/dk1221-tag-layout.svg
"""

import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

PT = 72 / 25.4
L = 23.0
SAFE_X, SAFE_Y = 2.96, 1.52
LIVE_W = L - 2 * SAFE_X
FOLD = 3.0
S = 9.0                       # drawing scale, px per mm
FONT = "Helvetica, Arial, sans-serif"

FIELD_OF = ["line1", "line2", "conn_a", "conn_b"]
FACE_OF = ["A", "A", "B", "B"]


def read_objects(lbx):
    x = zipfile.ZipFile(lbx).read("label.xml").decode()
    out = []
    for m in re.finditer(
        r'<pt:objectStyle x="([\d.]+)pt" y="([\d.]+)pt" width="([\d.]+)pt" '
        r'height="([\d.]+)pt".*?angle="(\d+)".*?objectName="(\w+)".*?'
        r'<pt:data>(.*?)</pt:data>', x, re.S,
    ):
        gx, gy, gw, gh, ang, name, data = m.groups()
        out.append(dict(name=name, x=float(gx) / PT, y=float(gy) / PT,
                        w=float(gw) / PT, h=float(gh) / PT,
                        angle=int(ang), text=data))
    return out


def t(x, y, s, size=11, weight="normal", fill="#111", anchor="start", style=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'{style}>{escape(s)}</text>')


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1
               else "07-tech-pack/labeling/dk1221-rack-audio-end-a.lbx")
    dst = Path(sys.argv[2] if len(sys.argv) > 2
               else "07-tech-pack/labeling/dk1221-tag-layout.svg")
    objs = read_objects(src)

    OX, OY = 70, 96                      # origin of the flat label drawing
    W, H = 980, 560
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="#fff"/>',
         t(28, 34, "DK-1221 fold tag — P-touch object layout", 19, "bold"),
         t(28, 54, f"4 text objects · 23 × 23 mm · sample data from {src.stem}",
           11.5, "normal", "#666"),
         t(28, 72, "line1 + line2 on the upright face · conn_a + conn_b on the rotated face",
           11.5, "normal", "#666")]

    def px(mm_x, mm_y):
        return OX + mm_x * S, OY + mm_y * S

    # fold zone
    fz0, fz1 = (L - FOLD) / 2, (L + FOLD) / 2
    x0, y0 = px(0, fz0)
    p.append(f'<rect x="{x0}" y="{y0}" width="{L*S}" height="{FOLD*S}" '
             f'fill="#eef4ff"/>')
    # printable area
    x0, y0 = px(SAFE_X, SAFE_Y)
    p.append(f'<rect x="{x0}" y="{y0}" width="{LIVE_W*S:.1f}" '
             f'height="{(L-2*SAFE_Y)*S:.1f}" fill="none" stroke="#bbb" '
             f'stroke-width="1" stroke-dasharray="4 3"/>')
    # die-cut edge
    x0, y0 = px(0, 0)
    p.append(f'<rect x="{x0}" y="{y0}" width="{L*S}" height="{L*S}" fill="none" '
             f'stroke="#c8102e" stroke-width="1.6" rx="6"/>')
    # fold line
    fx, fy = px(0, L / 2)
    p.append(f'<line x1="{fx}" y1="{fy}" x2="{fx + L*S}" y2="{fy}" stroke="#0a84ff" '
             f'stroke-width="1.4" stroke-dasharray="7 4"/>')
    p.append(t(fx + L * S + 10, fy + 4, "FOLD  y = 11.5 mm", 11, "bold", "#0a84ff"))
    p.append(t(fx + L * S + 10, fy + 20, "3 mm blank zone wraps the tie", 10, "normal", "#5a86b8"))

    # object boxes
    for i, o in enumerate(objs[:4]):
        bx, by = px(o["x"], o["y"])
        bw, bh = o["w"] * S, o["h"] * S
        rot = o["angle"] == 180
        col = "#D55E00" if rot else "#0072B2"
        p.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" '
                 f'fill="{col}14" stroke="{col}" stroke-width="1.2"/>')
        cx, cy = bx + bw / 2, by + bh / 2 + 4
        disp = o["text"]
        p.append(f'<g transform="rotate({180 if rot else 0} {cx:.1f} {cy-4:.1f})">'
                 + t(cx, cy, disp, 13 if i % 2 == 0 else 10.5,
                     "bold" if i % 2 == 0 else "normal", "#111", "middle") + '</g>')
        # callout to the right
        ly = by + bh / 2
        p.append(f'<line x1="{bx+bw:.1f}" y1="{ly:.1f}" x2="{OX + L*S + 120}" '
                 f'y2="{ly:.1f}" stroke="{col}" stroke-width="0.8" stroke-dasharray="2 2"/>')
        p.append(t(OX + L * S + 126, ly + 4,
                   f'{o["name"]}  ←  {FIELD_OF[i]}   (face {FACE_OF[i]}'
                   + (", 180°)" if rot else ")"), 11.5, "bold", col))

    # dimensions
    dx, dy = px(0, L)
    p.append(t(OX + L * S / 2, dy + 22, "23.0 mm die-cut", 10.5, "normal", "#c8102e", "middle"))
    p.append(t(OX - 10, OY + L * S / 2, "23.0", 10.5, "normal", "#c8102e", "end"))
    px0, _ = px(SAFE_X, 0)
    p.append(t(px0 + LIVE_W * S / 2, OY - 12,
               f"printable {LIVE_W:.2f} mm  (2.96 mm inset each side)", 10.5,
               "normal", "#777", "middle"))

    # folded result
    FX, FY, FW, FH = 640, 150, 150, 105
    p.append(t(FX, FY - 26, "Folded over the tie — what each side reads", 13, "bold"))
    for k, (title, lines, col) in enumerate([
        ("SIDE 1", [objs[0]["text"], objs[1]["text"]], "#0072B2"),
        ("SIDE 2", [objs[2]["text"], objs[3]["text"]], "#D55E00"),
    ]):
        oy = FY + k * (FH + 26)
        p.append(f'<rect x="{FX}" y="{oy}" width="{FW}" height="{FH}" fill="#fff" '
                 f'stroke="{col}" stroke-width="1.6" rx="7"/>')
        p.append(t(FX + 8, oy + 17, title, 10, "bold", col))
        p.append(t(FX + FW / 2, oy + 52, lines[0], 21, "bold", "#111", "middle"))
        p.append(t(FX + FW / 2, oy + 78, lines[1], 14, "normal", "#111", "middle"))
    p.append(t(FX, FY + 2 * (FH + 26) + 6,
               "Both read upright: face B is printed 180° so the fold rights it.",
               10.5, "normal", "#666"))

    # legend
    ly = OY + L * S + 60
    p.append(f'<line x1="28" y1="{ly-18}" x2="{W-28}" y2="{ly-18}" stroke="#ddd"/>')
    for i, (c, s_) in enumerate([
        ("#c8102e", "die-cut edge, 23 mm"),
        ("#bbb", "printable area — 17.08 × 20.00 mm, the printer's own margins"),
        ("#0a84ff", "fold line + 3 mm blank zone"),
        ("#0072B2", "face A objects (upright)"),
        ("#D55E00", "face B objects (rotated 180°)"),
    ]):
        yy = ly + i * 17
        p.append(f'<rect x="30" y="{yy-8}" width="11" height="11" fill="{c}" rx="2"/>')
        p.append(t(48, yy + 1, s_, 11, "normal", "#444"))

    p.append('</svg>')
    dst.write_text("\n".join(p), encoding="utf-8")
    print(f"{dst}: {len(objs)} objects drawn")
    for i, o in enumerate(objs[:4]):
        print(f"  {o['name']:<6} <- {FIELD_OF[i]:<7} face {FACE_OF[i]} "
              f"angle {o['angle']:>3}  x={o['x']:.2f} y={o['y']:.2f} "
              f"w={o['w']:.2f} h={o['h']:.2f} mm   \"{o['text']}\"")


if __name__ == "__main__":
    main()
