#!/usr/bin/env python3
"""Build a best-effort Brother P-touch Editor .lbx for the DK-1221 power set.

WARNING — READ BEFORE TRUSTING THIS OUTPUT
Brother has never published the .lbx schema. This script reconstructs it from
memory of genuine .lbx files, at moderate confidence on element/attribute
names and LOW confidence on the internal unit system. It has not been opened
in a real copy of P-touch Editor (not available in this environment) and so
is UNVERIFIED. Test it before relying on it; if it fails to open or the
objects are wrong, use 07-tech-pack/labeling/ptouch-field-mapping.md instead
-- that path rebuilds the identical layout natively in Editor's own UI with
no format guessing involved, in about 5 minutes.

What this script deliberately does NOT attempt:
  - Database/merge-field binding inside the XML (the riskiest, least-certain
    part of the schema). The .lbx ships with static sample text from the
    first CSV row; bind the CSV via Editor's own Database Connect (see the
    field-mapping doc section 4) once the file is open.
  - The inverse (white-on-black) spare label -- that's a second, simpler
    template; build it by hand per the field-mapping doc section 5.

Geometry mirrors scripts/build-cable-labels.py exactly (same constants), so
if that script's layout ever changes, regenerate this file from it rather
than hand-editing either one out of sync.
"""

import csv
import sys
import zipfile
from pathlib import Path

# --- Geometry (mm) -- identical constants to build-cable-labels.py ----------
L = 23.0
SAFE = 1.5
FOLD_TAG = 3.0
TOP = (L + FOLD_TAG) / 2  # 13.0

# Best-effort unit convention: 1 lbx "pt" unit = 0.01 mm (centi-mm).
# UNVERIFIED -- see module docstring.
def u(mm):
    return round(mm * 100)


def rotate_box_180(x_mm, y_mm, w_mm, h_mm):
    """Face B's box, derived from Face A's by rotating 180 deg about the label
    center -- the same transform build-cable-labels.py applies to the whole
    face group. Deriving it this way (instead of a second hand-typed set of
    coordinates) is what keeps this script, the SVG proof, and the
    field-mapping doc from drifting apart the way an earlier draft did.
    """
    x1, y1 = x_mm + w_mm, y_mm + h_mm
    return (L - x1, L - y1, w_mm, h_mm)


def text_object(x_mm, y_mm, w_mm, h_mm, rotate_deg, bold, size_pt, content):
    weight = "700" if bold else "400"
    rotate_tenths = int(round(rotate_deg * 10))
    return f'''    <text:text>
      <pt:objectStyle x="{u(x_mm)}pt" y="{u(y_mm)}pt" width="{u(w_mm)}pt" height="{u(h_mm)}pt"
          backColor="#FFFFFF" backMode="TRANSPARENT" ln="0" lnDetail="0pt">
        <pt:rotate angle="{rotate_tenths}"/>
      </pt:objectStyle>
      <text:ptFontInfo>
        <text:logFont name="Arial Narrow" width="0" italic="false" weight="{weight}" charSet="0" pitchAndFamily="34"/>
        <text:fontExt effect="NOEFFECT" underline="0" strikeout="0" size="{size_pt}pt" orgSize="{size_pt}pt"
            textColor="#000000" textPrintColorNumber="1"/>
      </text:ptFontInfo>
      <text:textControl control="AUTOLENGTH" clipFrame="false" aspectNormal="true" shrink="true" autoLF="false" avoidImage="false"/>
      <text:textAlign horizontalAlignment="CENTER" verticalAlignment="CENTER" inLineAlignment="CENTER"/>
      <text:data>{content}</text:data>
    </text:text>
'''


def label_xml(line1, line2):
    box_w = L - 2 * SAFE
    line1_box = (SAFE, TOP + 0.3, box_w, 4.6)
    line2_box = (SAFE, TOP + 4.7, box_w, 3.5)
    objs = "".join([
        text_object(*line1_box, 0, True, 11, line1),
        text_object(*line2_box, 0, False, 8, line2),
        text_object(*rotate_box_180(*line1_box), 180, True, 11, line1),
        text_object(*rotate_box_180(*line2_box), 180, False, 8, line2),
    ])
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!--
  Best-effort reconstruction of Brother's .lbx schema. UNVERIFIED.
  Not opened in a real P-touch Editor. If this file fails to open, discard it
  and use 07-tech-pack/labeling/ptouch-field-mapping.md instead.
-->
<pt:document xmlns:pt="http://schemas.brother.info/ptouchclipp/2001/pt-clip-object-format"
    xmlns:style="http://schemas.brother.info/ptouchclipp/2001/pt-clip-style-format"
    xmlns:text="http://schemas.brother.info/ptouchclipp/2001/pt-clip-text-format"
    xmlns:draw="http://schemas.brother.info/ptouchclipp/2001/pt-clip-draw-format"
    version="1.9" generator="nomad-toronto-av/scripts/build-lbx.py">
  <pt:body currentSheet="Sheet 1">
    <pt:sheet Name="Sheet 1">
      <pt:paper>
        <pt:paperInfo media="DK1221" width="{u(L)}pt" height="{u(L)}pt"
            marginLeft="0pt" marginRight="0pt" marginTop="0pt" marginBottom="0pt"
            orientation="portrait" autoLength="false" backgroundTheme="0"
            printerName="Brother QL"/>
        <pt:drawControl copies="1" printQuality="high"/>
      </pt:paper>
      <pt:objects>
{objs}      </pt:objects>
    </pt:sheet>
  </pt:body>
</pt:document>
'''


PROP_XML = '''<?xml version="1.0" encoding="UTF-8"?>
<meta:properties xmlns:meta="http://schemas.brother.info/ptouchclipp/2001/pt-clip-meta-format">
  <meta:appName>P-touch Editor</meta:appName>
  <meta:title>NOMAD Toronto - DK-1221 Power Label</meta:title>
  <meta:comments>Best-effort reconstruction - see build-lbx.py docstring. Verify before use.</meta:comments>
</meta:properties>
'''


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "07-tech-pack/labeling/labels-power.csv")
    dst = Path(sys.argv[2] if len(sys.argv) > 2 else "07-tech-pack/labeling/dk1221-power.lbx")
    with src.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    first = next(r for r in rows if r["variant"] == "TAG" and r["invert"].strip().lower() != "yes")

    xml = label_xml(first["line1"], first["line2"])

    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("Label.xml", xml)
        z.writestr("prop.xml", PROP_XML)

    print(f"{dst}: built from sample row {first['id']} ({first['line1']} / {first['line2']})")
    print("UNVERIFIED -- open in real P-touch Editor before trusting this file.")
    print("If it fails: 07-tech-pack/labeling/ptouch-field-mapping.md rebuilds it natively.")


if __name__ == "__main__":
    main()
