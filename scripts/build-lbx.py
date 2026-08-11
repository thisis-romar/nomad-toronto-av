#!/usr/bin/env python3
"""Build a Brother P-touch Editor .lbx for the DK-1221 fold-over tag.

Schema is no longer guessed. It is derived from a real Editor-authored file
(P-touch Editor 5.4.007, DK-1221 on a QL-800) supplied after an earlier
hand-reconstructed attempt failed to open. Everything structural below --
namespaces, element names and order, units, the paper and backGround blocks --
is copied from that file rather than inferred.

What the earlier attempt got wrong, for the record:
  * zip member was Label.xml; Editor wants lowercase label.xml
  * namespaces were .../ptouchclipp/2001/... ; real is .../ptouch/2007/lbx/...
  * version 1.9; real is 1.7
  * <pt:sheet>/<pt:paperInfo>; real is <style:sheet>/<style:paper>
  * units were centi-mm; real is PostScript points (72/inch)
  * rotation as a <pt:rotate> child; real is an `angle` attribute
  * <text:data>; real is <pt:data>
  * missing <style:cutLine>, <style:backGround>, <text:textStyle>,
    <text:stringItem>, <pt:pen>, <pt:brush>, <pt:expanded>
  * prop.xml had 3 elements in a made-up namespace; real has 18 in
    .../lbx/meta plus Dublin Core

The printable area also came out of that file and is NOT the 20x20 mm the
proof sheets assumed: Editor reports 48.5 x 56.7 pt = 17.11 x 20.00 mm,
inset 2.96 mm left/right and 1.52 mm top/bottom. Text laid out to 20 mm wide
would have run into the unprintable margin on every label.

Usage:
    python3 scripts/build-lbx.py \
        07-tech-pack/labeling/labels-rack-internal.csv \
        07-tech-pack/labeling/dk1221-rack-internal.lbx
"""

import csv
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

# --- Units -------------------------------------------------------------------
PT = 72 / 25.4            # PostScript points per mm, as Editor uses

# --- Ground truth from the Editor-authored reference file --------------------
# DK-1221 (23 x 23 mm) on a Brother QL-800. Reproduced verbatim: these values
# encode the media profile and the printer's unprintable margins, and guessing
# at them is what broke the previous attempt.
PAPER = ('<style:paper media="0" width="65.3pt" height="65.3pt" marginLeft="4.3pt" '
         'marginTop="8.4pt" marginRight="4.4pt" marginBottom="8.5pt" '
         'orientation="landscape" autoLength="false" monochromeDisplay="true" '
         'printColorDisplay="false" printColorsID="0" paperColor="#FFFFFF" '
         'paperInk="#000000" split="1" format="370" backgroundTheme="0" '
         'printerID="14388" printerName="Brother QL-800"/>')
CUTLINE = '<style:cutLine regularCut="0pt" freeCut=""/>'
BACKGROUND = ('<style:backGround x="8.4pt" y="4.3pt" width="48.5pt" height="56.7pt" '
              'brushStyle="NULL" brushId="0" userPattern="NONE" userPatternId="0" '
              'color="#000000" printColorNumber="1" backColor="#FFFFFF" '
              'backPrintColorNumber="0"/>')

LABEL_PT = 65.3           # Editor's own figure for a 23 mm label
PRINT_X, PRINT_Y = 8.4, 4.3      # printable origin, pt
PRINT_W, PRINT_H = 48.5, 56.7    # printable size, pt  (17.11 x 20.00 mm)

# Editor's generator string is reproduced so the file is not rejected on a
# version check. Provenance is recorded honestly in prop.xml instead.
GENERATOR = "P-touch Editor 5.4.007 Windows"
CREATED = "2026-08-11T00:00:00Z"

FONT_NAME = "Arial Narrow"

NS = ('xmlns:pt="http://schemas.brother.info/ptouch/2007/lbx/main" '
      'xmlns:style="http://schemas.brother.info/ptouch/2007/lbx/style" '
      'xmlns:text="http://schemas.brother.info/ptouch/2007/lbx/text" '
      'xmlns:draw="http://schemas.brother.info/ptouch/2007/lbx/draw" '
      'xmlns:image="http://schemas.brother.info/ptouch/2007/lbx/image" '
      'xmlns:barcode="http://schemas.brother.info/ptouch/2007/lbx/barcode" '
      'xmlns:database="http://schemas.brother.info/ptouch/2007/lbx/database" '
      'xmlns:table="http://schemas.brother.info/ptouch/2007/lbx/table" '
      'xmlns:cable="http://schemas.brother.info/ptouch/2007/lbx/cable"')

# --- Tag geometry, in pt -----------------------------------------------------
FOLD_MM = 3.0                                  # blank zone over the tie tail
CENTRE = LABEL_PT / 2                          # 32.65 pt
FOLD_HALF = (FOLD_MM / 2) * PT
FACE_A_TOP = CENTRE + FOLD_HALF                # lower face
FACE_B_BOT = CENTRE - FOLD_HALF                # upper face
PRINT_BOT = PRINT_Y + PRINT_H

# Two-line and three-line layouts, mirroring scripts/build-cable-labels.py.
# (font mm, bold, baseline offset from the top of the face, in mm)
LAYOUT_2 = ((4.0, True, 3.6), (2.8, False, 7.0))
LAYOUT_3 = ((3.4, True, 2.7), (2.4, False, 5.4), (2.2, False, 7.9))

# Face B is Face A rotated 180 deg about the label centre. Editor expresses
# rotation as an `angle` attribute on objectStyle; the reference file only ever
# uses angle="0", so the unit (degrees vs tenths) is the one thing still
# unverified. Degrees is used here -- a wrong value renders visibly wrong but
# does not stop the file opening, which is the failure that mattered.
ROT_180 = 180


def fmt(v):
    return f"{round(v, 1)}pt"


def rot180_box(x, y, w, h):
    """Box position after rotating 180 deg about the label centre."""
    return (LABEL_PT - (x + w), LABEL_PT - (y + h), w, h)


def font_info(size_pt, bold):
    weight = 700 if bold else 400
    return (f'<text:ptFontInfo>'
            f'<text:logFont name="{FONT_NAME}" width="0" italic="false" '
            f'weight="{weight}" charSet="0" pitchAndFamily="34"/>'
            f'<text:fontExt effect="NOEFFECT" underline="0" strikeout="0" '
            f'size="{fmt(size_pt)}" orgSize="{fmt(size_pt)}" textColor="#000000" '
            f'textPrintColorNumber="1"/>'
            f'</text:ptFontInfo>')


def text_object(name, x, y, w, h, size_pt, bold, content, angle=0):
    """One text object, mirroring the reference file's element order exactly."""
    fi = font_info(size_pt, bold)
    body = escape(content)
    return (
        f'<text:text>'
        f'<pt:objectStyle x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" '
        f'backColor="#FFFFFF" backPrintColorNumber="0" ropMode="COPYPEN" '
        f'angle="{angle}" anchor="TOPLEFT" flip="NONE">'
        f'<pt:pen style="NULL" widthX="0.5pt" widthY="0.5pt" color="#000000" '
        f'printColorNumber="1"/>'
        f'<pt:brush style="NULL" color="#000000" printColorNumber="1" id="0"/>'
        f'<pt:expanded objectName="{name}" ID="0" lock="0" '
        f'templateMergeTarget="LABELLIST" templateMergeType="NONE" templateMergeID="0" '
        f'linkStatus="NONE" linkID="0"/>'
        f'</pt:objectStyle>'
        f'{fi}'
        f'<text:textControl control="FREE" clipFrame="false" aspectNormal="false" '
        f'shrink="false" autoLF="false" avoidImage="false"/>'
        f'<text:textAlign horizontalAlignment="CENTER" verticalAlignment="CENTER" '
        f'inLineAlignment="CENTER"/>'
        f'<text:textStyle vertical="false" nullBlock="false" charSpace="0" lineSpace="0" '
        f'orgPoint="{fmt(size_pt)}" combinedChars="false"/>'
        f'<pt:data>{body}</pt:data>'
        # One run covering the whole string. Editor splits runs by character
        # class; a single run of the full length is the simplest valid form and
        # charLen must equal len(data) or the file is rejected.
        f'<text:stringItem charLen="{len(content)}">{fi}</text:stringItem>'
        f'</text:text>'
    )


def label_xml(lines):
    """Face A in the lower half; Face B is the same, rotated 180 about centre."""
    layout = LAYOUT_3 if len(lines) >= 3 else LAYOUT_2

    # Editor centres text vertically inside its object box, so the boxes are
    # stacked to fill the face rather than derived from the SVG's baselines.
    # Deriving from baselines put the first box 0.6 pt above the face and into
    # the fold zone -- text there lands on the part that wraps the cable tie.
    avail = PRINT_BOT - FACE_A_TOP
    heights = [size_mm * 1.05 * PT for (size_mm, _b, _d) in layout]
    slack = avail - sum(heights)
    if slack < 0:
        raise SystemExit(f"layout too tall for the face by {-slack:.2f}pt")
    lead = slack / (len(heights) + 1)

    boxes, sizes, bolds = [], [], []
    y = FACE_A_TOP + lead
    for (size_mm, bold, _dy), h in zip(layout, heights):
        boxes.append((PRINT_X, y, PRINT_W, h))
        sizes.append(size_mm * PT)
        bolds.append(bold)
        y += h + lead

    objs = []
    for i, (box, sz, bold, txt) in enumerate(zip(boxes, sizes, bolds, lines)):
        objs.append(text_object(f"Text{i + 1}", *box, sz, bold, txt))
    for i, (box, sz, bold, txt) in enumerate(zip(boxes, sizes, bolds, lines)):
        objs.append(text_object(f"Text{len(lines) + i + 1}", *rot180_box(*box),
                                sz, bold, txt, ROT_180))
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<pt:document {NS} version="1.7" generator="{GENERATOR}">'
        '<pt:body currentSheet="Sheet 1" direction="LTR">'
        '<style:sheet name="Sheet 1">'
        f'{PAPER}{CUTLINE}{BACKGROUND}'
        f'<pt:objects>{"".join(objs)}</pt:objects>'
        '</style:sheet>'
        '</pt:body>'
        '</pt:document>'
    )


def prop_xml(title, note):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<meta:properties '
        'xmlns:meta="http://schemas.brother.info/ptouch/2007/lbx/meta" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/">'
        '<meta:appName>P-touch Editor</meta:appName>'
        f'<dc:title>{escape(title)}</dc:title>'
        '<dc:subject/>'
        '<dc:creator>Emblem Projects Inc.</dc:creator>'
        '<meta:keyword/>'
        f'<dc:description>{escape(note)}</dc:description>'
        '<meta:template/>'
        f'<dcterms:created>{CREATED}</dcterms:created>'
        f'<dcterms:modified>{CREATED}</dcterms:modified>'
        '<meta:lastPrinted/>'
        '<meta:modifiedBy>scripts/build-lbx.py</meta:modifiedBy>'
        '<meta:revision>1</meta:revision>'
        '<meta:editTime>0</meta:editTime>'
        '<meta:numPages>1</meta:numPages>'
        '<meta:numWords>0</meta:numWords>'
        '<meta:numChars>0</meta:numChars>'
        '<meta:security>0</meta:security>'
        '</meta:properties>'
    )


def write_lbx(path, lines, title, note):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        # lowercase label.xml, and first in the archive, as Editor writes it
        z.writestr("label.xml", label_xml(lines))
        z.writestr("prop.xml", prop_xml(title, note))


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else
               "07-tech-pack/labeling/labels-rack-internal.csv")
    dst = Path(sys.argv[2] if len(sys.argv) > 2 else
               "07-tech-pack/labeling/dk1221-rack-internal.lbx")
    with src.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    first = next(r for r in rows
                 if r["variant"] == "TAG" and r["invert"].strip().lower() != "yes")

    lines = [first["line1"], first["line2"]]
    if (first.get("line3") or "").strip():
        lines.append(first["line3"])
    write_lbx(dst, lines,
              f"NOMAD Toronto — DK-1221 fold tag ({dst.stem})",
              "Generated by scripts/build-lbx.py from the label CSV. Structure derived "
              "from an Editor-authored reference file. Connect the CSV via Database "
              "Connect to merge the remaining rows.")

    print(f"{dst}: template built from {first['id']} ({' / '.join(lines)})")
    print(f"  printable area {PRINT_W / PT:.2f} x {PRINT_H / PT:.2f} mm "
          f"(NOT 20x20 — Editor's own margins)")
    print(f"  {2 * len(lines)} text objects; Face B at angle={ROT_180} "
          f"(degrees assumed — see docstring)")


if __name__ == "__main__":
    main()
