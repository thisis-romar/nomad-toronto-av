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

## §2 Text objects

Every object is a **Text** object, centre-aligned horizontally and vertically in its box,
**17.11 mm wide at x = 2.96 mm**. That width is the printer's printable area for this media, not
a margin we chose — do not widen it. Rotation is applied to the whole object.

Two tag layouts exist. The per-end sets use three lines; the whole-cable sets use two.

### Three-line tag — per-end sets (`-end-a`, `-end-b`), 6 objects

Line 1 the device, line 2 the socket, line 3 the cable ID and far end. Values read back out of
the generated `.lbx`:

| # | Face | Line | X | Y (box top) | W | H | Size | Rotation |
|---|------|------|--:|-------------:|--:|--:|-----:|---------:|
| Text1 | A | 1 device | 2.96 mm | 13.05 mm | 17.11 mm | 3.56 mm | 9.6 pt **bold** | 0° |
| Text2 | A | 2 socket | 2.96 mm | 16.65 mm | 17.11 mm | 2.50 mm | 6.8 pt | 0° |
| Text3 | A | 3 route | 2.96 mm | 19.19 mm | 17.11 mm | 2.29 mm | 6.2 pt | 0° |
| Text4 | B | 1 device | 2.96 mm | 6.42 mm | 17.11 mm | 3.56 mm | 9.6 pt **bold** | **180°** |
| Text5 | B | 2 socket | 2.96 mm | 3.88 mm | 17.11 mm | 2.50 mm | 6.8 pt | **180°** |
| Text6 | B | 3 route | 2.96 mm | 1.55 mm | 17.11 mm | 2.29 mm | 6.2 pt | **180°** |

### Two-line tag — whole-cable sets, 4 objects

| # | Face | Line | X | Y (box top) | W | H | Rotation |
|---|------|------|--:|-------------:|--:|--:|---------:|
| Text1 | A | 1 | 2.96 mm | 13.37 mm | 17.11 mm | 4.59 mm | 0° |
| Text2 | A | 2 | 2.96 mm | 18.13 mm | 17.11 mm | 3.21 mm | 0° |
| Text3 | B | 1 | 2.96 mm | 5.08 mm | 17.11 mm | 4.59 mm | **180°** |
| Text4 | B | 2 | 2.96 mm | 1.69 mm | 17.11 mm | 3.21 mm | **180°** |

### Two rules that are easy to get wrong

**Boxes must not enter the fold zone (y 10.0–13.0 mm).** Editor centres text vertically inside its
box, so a box that starts above y = 13.0 puts its text on the strip that wraps the cable tie. The
generator originally derived these boxes from the SVG's text baselines and put the first box
0.6 pt into the fold; they are now stacked to fill the face instead.

**Face B is Face A rotated 180° about the label centre (11.5, 11.5) — not rotated in place.** If
your Editor rotates about the object's own centre, move the object to the Y above *first*, then
rotate. Face B is upside-down so that, once folded adhesive-to-adhesive over the tie, both faces
read upright.

---

## §3 Font settings

Arial Narrow throughout (or any condensed grotesque — avoid hairline faces; a 300 dpi thermal
head drops strokes below ~0.1 mm).

| Line | Weight | Three-line tag | Two-line tag |
|------|--------|---------------:|-------------:|
| 1 | **Bold** | 9.6 pt | 11.3 pt |
| 2 | Regular | 6.8 pt | 7.9 pt |
| 3 | Regular | 6.2 pt | — |

Turn on **Text → Auto Fit → Reduce to fit frame** as a backstop. Do not let anything fall below
**~6 pt (2.1 mm)** — below that it is not reliably legible off this head at arm's length.

---

## §4 Merge field binding (Database Connect)

1. **File → Database → Connect**, browse to the CSV for the side you are printing
   (`labels-rack-internal-end-a.csv`, then later `-end-b.csv`). First row is field names.
2. Editor shows the **Mapping Merged Fields** dialog and pre-fills it. **Its guesses are wrong
   past the first two rows** and must be corrected.

### Why it guesses wrong, and the rule that fixes it

The dialog lists one row per layout object, identified by the text currently in it, and assigns
database columns to them **in order**. The tag has each line twice — once upright for Face A,
once rotated 180° for Face B — so the duplicates run past the end of the printed fields and get
bound to whatever column comes next (`conn_a`, `conn_b`, …).

**The rule: two rows showing the same text are the two faces of the same line. Map them to the
same field.**

For a three-line per-end tag, six objects map to three columns:

| Layout object (by its text) | Database field |
|-----------------------------|----------------|
| `SP2120` *(1st occurrence — Face A)* | `line1` |
| `OUT L` *(1st)* | `line2` |
| `A15 -> V3 #2` *(1st)* | `line3` |
| `SP2120` *(2nd — Face B, rotated)* | `line1` |
| `OUT L` *(2nd)* | `line2` |
| `A15 -> V3 #2` *(2nd)* | `line3` |

A two-line whole-cable tag is the same idea with four objects → `line1, line2, line1, line2`.

The CSVs put `line1`, `line2`, `line3` as the **first columns** so Editor's own first guesses land
on the printed fields; only the duplicate half needs correcting.

### Encoding — why the text looked like `P1 Â· SP212`

Editor reads a merge CSV as Windows CP1252, not UTF-8, so `·` arrived as `Â·` and `→` as `â†'`.
Two changes prevent it:

- every CSV is written **UTF-8 with a BOM**, which Editor honours; and
- every printed field is reduced to **plain ASCII** anyway — `·` → `-`, `→` → `->`, `Ω` → `OHM`.

The ASCII reduction is the one that cannot fail, so it is not relied on the BOM alone. If you see
`Â` or `â` anywhere in the database preview, stop — something is reading the file as ANSI and the
labels will print mangled.

3. Set the merge to iterate all records. Every row is `qty 1` — one tag per cable end — so one
   pass per side prints the whole set.

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
