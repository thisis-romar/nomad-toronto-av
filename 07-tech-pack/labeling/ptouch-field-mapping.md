---
title: Nomad Toronto — P-touch Editor Field Mapping (Power Label Set)
description: Exact object positions, rotation, and merge-field bindings to rebuild the DK-1221 fold-over tag natively in P-touch Editor — the zero-risk path if the generated .lbx will not open. Geometry derived from a real Editor-authored reference file.
version: 2.0.0
created: 2026-08-11T00:00:00Z
last_updated: 2026-08-11T00:00:00Z
---

# P-touch Editor Field Mapping — DK-1221 Fold Tag

**Why this document exists:** Brother's `.lbx` is a zip+XML format with no published schema. The
first attempt at generating one was reconstructed from memory and **failed to open** ("Failed to
open document"). The generator has since been rewritten against a real Editor-authored file, so
the `.lbx` should now open — but this document remains the zero-risk path: rebuilding the layout
by hand in Editor's own UI takes about five minutes and depends on no format guessing.

**Two corrections came out of that reference file, and they change the numbers below:**

| | Assumed before | Actual |
|---|---|---|
| Printable area | 20.0 × 20.0 mm (uniform 1.5 mm margin) | **17.11 × 20.00 mm** — inset 2.96 mm left/right, 1.52 mm top/bottom |
| Units | centi-millimetres | **PostScript points**, 72/inch (23 mm = 65.3 pt) |

Text laid out 20 mm wide ran 2.89 mm into the unprintable margin on every label. The proof sheets
and the `.lbx` are both corrected; if you have an earlier printout, discard it.

**Ground truth for visual checking:** `dk1221-rack-internal-proof.svg`, printed at 100%. If a
number here and the proof ever disagree, the proof wins — both are generated from the same
constants.

---

## §1 New label / paper setup

1. **File → New → Label size** → search **DK-1221** (23 mm × 23 mm, die-cut). Do not use a
   generic "custom size" — the die-cut sensor needs the real DK-1221 profile to auto-cut correctly.
2. Orientation: **square**, no rotation on the paper itself.
3. Turn on **View → Guides/Grid**, and place a horizontal guide at **y = 11.5 mm** (dead centre) —
   this is the fold line. If your Editor version supports named guides, label it `FOLD`.

---

## §2 Text objects (4 total — 2 per face)

All four are **Text** objects, centre-aligned horizontally and vertically within their box,
**17.11 mm wide, positioned 2.96 mm in from the left edge** — that is the printer's printable
width, not a margin we chose. Rotation is applied to the whole object, not the text-only.

These are the exact values the generator emits, read back out of the produced `.lbx`:

| # | Face | Content | X | Y (box top) | W | H | Rotation |
|---|------|---------|--:|-------------:|--:|--:|---------:|
| 1 | A (upright) | Line 1 — headline | 2.96 mm | 13.37 mm | 17.11 mm | 4.59 mm | 0° |
| 2 | A (upright) | Line 2 — detail | 2.96 mm | 18.13 mm | 17.11 mm | 3.21 mm | 0° |
| 3 | B (folded side) | Line 1 — headline | 2.96 mm | 5.08 mm | 17.11 mm | 4.59 mm | **180°** |
| 4 | B (folded side) | Line 2 — detail | 2.96 mm | 1.69 mm | 17.11 mm | 3.21 mm | **180°** |

`X = 2.96 mm` and `W = 17.11 mm` are not a design choice — they are the printer's printable
width for this media. Do not widen them.

Face B's box is Face A's box rotated 180° about the label's own centre (11.5, 11.5) — **not**
rotated in place. If your Editor rotates an object around its own centre rather than the whole
label, rotating objects 3 and 4 where they currently sit will spin them without moving them into
the upper half; drag them to the Y positions above first, *then* apply the 180° rotation.

**Why Face B is rotated:** the label folds along the y = 11.5 mm line, adhesive-to-adhesive, over
a cable-tie tail. Face B ends up on the back of that fold — printing it upside-down relative to
Face A means it reads right-side-up once folded, without re-orienting the cable to check it.

**Baselines these boxes are built around** (for reference if you're nudging by eye against the SVG
proof rather than typing coordinates):

| | Face A | Face B |
|--|--------|--------|
| Line 1 box centre | y ≈ 15.7 mm | y ≈ 7.4 mm |
| Line 2 box centre | y ≈ 19.7 mm | y ≈ 3.3 mm |

(Text is vertically centred in its box, so the box centres above are what to match by eye.)

---

## §3 Font settings

| Object | Font | Weight | Size (start) | Notes |
|--------|------|--------|--------------:|-------|
| Line 1 (objects 1 & 3) | Arial Narrow *(or Liberation Sans Narrow / any condensed grotesque)* | Bold | 11 pt | Turn on **Text → Auto Fit → Reduce to fit frame** so long IDs (e.g. `U8 · PHNX · BRK TBC`) shrink automatically rather than overflow |
| Line 2 (objects 2 & 4) | Same family | Regular | 8 pt | Same auto-fit setting |

Do not go below **~7.5 pt (≈2.6 mm)** even with auto-fit — that's the floor used in the proof
script; text smaller than that is not reliably legible off a thermal 300 dpi head at this size.

---

## §4 Merge field binding (Database Connect)

1. **File → Database → Connect** (or **Insert → Merge Field**, depending on your Editor version).
2. Browse to `07-tech-pack/labeling/labels-rack-internal.csv`. First row is the header — confirm
   "First row is field names" is checked.
3. Bind fields:

| Text object | CSV column |
|-------------|-----------|
| Objects 1 & 3 (both Line 1 boxes) | `line1` |
| Objects 2 & 4 (both Line 2 boxes) | `line2` |

   Both Face A and Face B pull from the **same two columns** — they're the same content, just
   printed twice (once upright, once rotated) so the fold produces two correctly-oriented faces.
4. Set the merge to iterate all rows. Print quantity per label comes from the CSV `qty` column —
   if your Editor version doesn't read `qty` directly, set the merge to repeat each record twice
   (every row in this set needs qty 2 or 3 — check the CSV before printing).

---

## §5 The inverse label (PWR-U5 — "spare, freed by V9 removal")

One row in the CSV (`invert = yes`) is meant to print **white text on a black background** — the
visual flag that this circuit is deliberately dead, not just unlabelled.

Editor does not do this through the database merge (merge only fills text, not object fill). Build
this one as a **separate, non-merged label**:

1. Duplicate the 4-object template.
2. Add a black rectangle behind each face's text (bounds: x=2.96, y=13.0, w=17.11, h=8.5 for
   Face A; x=2.96, y=1.52, w=17.11, h=8.5 for Face B — the full fold-half, printable edge to
   printable edge).
3. Set both text objects' font colour to white.
4. Type the content directly (2 labels needed) — no merge required for a single fixed design:
   - Line 1: `U5 · SPARE`
   - Line 2: `CPC 45A · 32A`

---

## §6 Print check before the run

1. Print **one** label of each design.
2. Measure the printed square with calipers: **23.0 mm × 23.0 mm** (±0.3 mm is normal roll
   tolerance; anything more means the media size in Editor doesn't match the loaded roll).
3. Confirm text sits inside the printable area — roughly 3 mm clear of the left and right
   die-cut edges, 1.5 mm clear of top and bottom. Text touching an edge means the media profile
   in Editor is wrong.
4. Fold one TAG label over a scrap of cable-tie and check both faces read upright and square —
   the two fold-registration marks (printed as small ticks at the label edges on the fold line in
   the SVG proof) are a visual aid only; Editor's own template does not need to reproduce them.
5. Only then run the full batch — **22 labels** for the current rack-internal set, see
   `labels-rack-internal.csv`.

---

## §7 If you'd rather not rebuild by hand

Try `dk1221-rack-internal.lbx` first. It is now generated against a real Editor file rather than
from memory, so the container and schema are no longer guesses:

| | First attempt (failed) | Now |
|---|---|---|
| zip member | `Label.xml` | `label.xml` (lowercase — this alone was fatal) |
| namespaces | `.../ptouchclipp/2001/...` | `.../ptouch/2007/lbx/...` |
| version | 1.9 | 1.7 |
| sheet / paper | `pt:sheet` / `pt:paperInfo` | `style:sheet` / `style:paper` |
| units | centi-mm | points (72/inch) |
| rotation | `<pt:rotate>` child | `angle` attribute |
| text body | `<text:data>` | `<pt:data>` |
| missing entirely | — | `style:cutLine`, `style:backGround`, `text:textStyle`, `text:stringItem`, `pt:pen`, `pt:brush`, `pt:expanded` |

**One value is still unverified:** the reference file only ever contains `angle="0"`, so whether
`angle` is degrees or tenths of a degree could not be confirmed. It is written as `180`. If the
upper face renders unrotated, the unit is tenths — change `ROT_180` in `scripts/build-lbx.py` to
`1800` and rebuild. A wrong angle value renders visibly wrong but does not stop the file opening,
which was the failure that actually mattered.

If it still won't open, discard it and rebuild from §2 — that path has no format risk at all.

---

*EMBLEM PROJECTS INC. · 2026-08-11 · companion to dk1221-power.lbx (best-effort, unverified)*
