---
title: Nomad Toronto — P-touch Editor Field Mapping (rack print sheets)
description: Exact object positions, rotation, and merge-field bindings to rebuild the DK-1221 triple-print fold tag natively in P-touch Editor — the zero-risk path if the generated .lbx will not open. Geometry derived from a real Editor-authored reference file.
version: 3.0.0
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

**Ground truth for visual checking:** the `dk1221-rack-{class}-end-{a,b}-proof.svg` for the
sheet you are printing, at 100%, plus `dk1221-tag-layout.svg` for the object map. If a
number here and the proof ever disagree, the proof wins — both are generated from the same
constants.

---

## §1 New label / paper setup

1. **File → New → Label size** → search **DK-1221** (23 mm × 23 mm, die-cut). Do not use a
   generic "custom size" — the die-cut sensor needs the real DK-1221 profile to auto-cut correctly.
2. Orientation: **square**, no rotation on the paper itself.
3. Turn on **View → Guides/Grid**, and place horizontal guides at **y = 8.19 mm** and
   **y = 14.85 mm** — the band boundaries, either of which can be the fold. If your Editor
   version supports named guides, label them `BAND`.

---

## §2 Text objects

Every object is a **Text** object, centre-aligned horizontally and vertically in its box,
**17.11 mm wide at x = 2.96 mm**. That width is the printer's printable area for this media, not
a margin we chose — do not widen it. Rotation is applied to the whole object.

### Triple-print tag — every rack sheet, 6 objects

Three 6.67 mm bands filling the 20.00 mm printable height, two lines each. There is no reserved
fold zone. The bottom band prints upright; the upper two print rotated 180° so whichever lands on
the back face reads the right way up once folded.

Values read back out of the generated `.lbx` (`build-layout-diagram.py` prints this table):

| # | Band | Reads as | Field | X | Y (box top) | W | H | Size | Rotation |
|---|------|----------|-------|--:|-------------:|--:|--:|-----:|---------:|
| Text1 | 3 bottom | line 1 | `line1` device | 2.96 mm | **15.13 mm** | 17.11 mm | 3.35 mm | 9.1 pt **bold** | 0° |
| Text2 | 3 bottom | line 2 | `line2` socket | 2.96 mm | **18.80 mm** | 17.11 mm | 2.40 mm | 6.5 pt | 0° |
| Text3 | 2 middle | line 1 | `conn_a` this end | 2.96 mm | **11.18 mm** | 17.11 mm | 3.35 mm | 9.1 pt **bold** | **180°** |
| Text4 | 2 middle | line 2 | `conn_b` far end | 2.96 mm | **8.47 mm** | 17.11 mm | 2.40 mm | 6.5 pt | **180°** |
| Text5 | 1 top | line 1 | `line1` device | 2.96 mm | **4.52 mm** | 17.11 mm | 3.35 mm | 9.1 pt **bold** | **180°** |
| Text6 | 1 top | line 2 | `line2` socket | 2.96 mm | **1.80 mm** | 17.11 mm | 2.40 mm | 6.5 pt | **180°** |

Band boundaries fall at **y = 8.19 mm and y = 14.85 mm**; registration ticks print at both edges
on each.

**A rotated band is stacked bottom-to-top — check this against the table.** In bands 1 and 2 the
line-1 object sits *below* its line-2 object on the sheet (Text3 at 11.18 is below Text4 at 8.47).
That is not a typo. The 180° angle flips the glyphs but does not move the boxes, so a rotated band
laid out in page order reads *line 2 above line 1* once the tag is folded. Reversing the stack is
what makes the back face read the right way round, and it is also what puts the bold `conn_a` at
the bottom of the middle band, adjacent to the upright identity — the half of that band most
likely to survive the wrap.

### Two rules that are easy to get wrong

**Every box must stay inside y 1.52–21.48 mm and x 2.96–20.07 mm.** Editor centres text vertically
inside its box, so a box that starts outside the printable area silently clips the glyphs rather
than the box. An earlier generator derived these boxes from the SVG's text baselines and put the
first one 0.6 pt out; they are now stacked to fill each band instead.

**Position the box first, then rotate it in place.** Every Y in the table is a *final* position,
so the 180° is a glyph flip and nothing else. If your Editor rotates about the label centre rather
than the object's own, it will move the box — undo, rotate, then set X/Y from the table. The
generated `.lbx` sidesteps the question entirely by writing final positions with the angle on the
object, which is why it does not care which convention Editor uses.

---

## §3 Font settings

Arial Narrow throughout (or any condensed grotesque — avoid hairline faces; a 300 dpi thermal
head drops strokes below ~0.1 mm).

| Slot | Weight | Size | mm |
|------|--------|-----:|---:|
| upper (`line1` / `conn_a`) | **Bold** | 9.1 pt | 3.2 mm |
| lower (`line2` / `conn_b`) | Regular | 6.5 pt | 2.3 mm |

Both slots use the same sizes in all three bands — the middle band is a peer of the other two,
not a footnote.

Turn on **Text → Auto Fit → Reduce to fit frame** as a backstop. Do not let anything fall below
**~6 pt (2.1 mm)** — below that it is not reliably legible off this head at arm's length.

---

## §4 Merge field binding (Database Connect)

1. **File → Database → Connect**, browse to the sheet you are printing —
   `labels-rack-{power,audio,data}-end-{a,b}.csv`. First row is field names.
2. Editor shows the **Mapping Merged Fields** dialog and pre-fills it. **The first four rows are
   right; the last two must be corrected by hand.**

### Why the last two are wrong, and the rule that fixes it

The dialog lists one row per layout object, identified by the text currently in it, and assigns
database columns to them **in order**. Six objects therefore consume six columns — but the tag
only has four distinct fields, because the identity band is printed twice. Editor will not assign
a column twice, so objects 5 and 6 get bound to whatever comes next.

The sheet CSVs lead with the four printed columns in object order, so the mapping you want is:

| # | Layout object (by its text) | Database field | Auto-mapped? |
|---|-----------------------------|----------------|--------------|
| Text1 | `SP2120` *(1st — upright band)* | `line1` | ✅ |
| Text2 | `OUT L` *(1st)* | `line2` | ✅ |
| Text3 | `XLR-M` | `conn_a` | ✅ |
| Text4 | `XLR-F` | `conn_b` | ✅ |
| Text5 | `SP2120` *(2nd — rotated band)* | `line1` | ❌ **set by hand** |
| Text6 | `OUT L` *(2nd)* | `line2` | ❌ **set by hand** |

**The rule: two rows showing the same text are the same field printed twice. Point the second
occurrence at the same column as the first.** Whatever Editor guessed for Text5/Text6 (`line3`,
`id`, …) is wrong by construction.

`conn_a` is always *this end's* connector — the end-B sheets have the end column groups swapped —
so the bold middle line describes the plug in your hand, not the one at the far end.

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

## §5 The inverse labels (`AUD-A19` — source end unconfirmed)

Rows with `invert = yes` print **white text on a black background** — the visual flag that
something on the tag is provisional, not merely unlabelled. In the current print set that is
`AUD-A19-A` and `AUD-A19-B`, one tag on each sheet, where the source device is still `?`
(`rack-io-inventory.md` §12).

Editor does not do this through the database merge (merge only fills text, not object fill). Build
these as **separate, non-merged labels**:

1. Duplicate the 6-object template.
2. Add a black rectangle behind each band, x = 2.96 mm, w = 17.11 mm, h = 6.67 mm, at
   **y = 1.52 / 8.19 / 14.85 mm** — printable edge to printable edge, band by band.
3. Set all six text objects' font colour to white.
4. Type the content directly — one label per end, no merge needed for a fixed design.

---

## §6 Print check before the run

1. Print **one** label of each design.
2. Measure the printed square with calipers: **23.0 mm × 23.0 mm** (±0.3 mm is normal roll
   tolerance; anything more means the media size in Editor doesn't match the loaded roll).
3. Confirm text sits inside the printable area — roughly 3 mm clear of the left and right
   die-cut edges, 1.5 mm clear of top and bottom. Text touching an edge means the media profile
   in Editor is wrong.
4. Fold one tag over a scrap of cable-tie on either band boundary and check that an identity
   band reads upright and square on each face. The band ticks at the label edges in the SVG proof
   are a visual aid only; Editor's own template does not need to reproduce them.
5. Only then run the sheet — **22 tags across the six sheets**, 1 / 5 / 5 per end for
   power / audio / data.

---

## §7 If you'd rather not rebuild by hand

Try the `dk1221-rack-{class}-end-{a,b}.lbx` for the sheet you are printing. It is now generated against a real Editor file rather than
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

*EMBLEM PROJECTS INC. · 2026-08-11 · companion to the six `dk1221-rack-*-end-*.lbx` sheets*
