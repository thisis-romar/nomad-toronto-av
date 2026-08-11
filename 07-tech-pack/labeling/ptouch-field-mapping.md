---
title: Nomad Toronto — P-touch Editor Field Mapping (Power Label Set)
description: Exact object positions, rotation, and merge-field bindings to rebuild the DK-1221 power label template natively in P-touch Editor — the reliable path if the bundled dk1221-power.lbx doesn't open cleanly.
version: 1.0.0
created: 2026-08-11T00:00:00Z
last_updated: 2026-08-11T00:00:00Z
---

# P-touch Editor Field Mapping — Power Label Set

**Why this document exists:** Brother's `.lbx` file is a semi-proprietary zip+XML format with no
published schema. `dk1221-power.lbx` in this folder is a **best-effort reconstruction** — it may
not open, and if it does, positions may need a nudge. This document is the reliable fallback: every
number below comes straight out of `scripts/build-cable-labels.py`, the same source that generates
`dk1221-power-proof.svg`, so it can't drift out of sync with the proof. Rebuilding from this table
takes about 5 minutes and carries zero format risk.

**Ground truth for visual checking:** `dk1221-power-proof.svg`, printed at 100%. If a number here
and the proof ever disagree, the proof wins — re-derive from the script.

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
20 mm wide, positioned 1.5 mm in from the left edge (the safe margin). Rotation is applied to the
whole object, not the text-only.

| # | Face | Content | X | Y (box top) | W | H | Rotation |
|---|------|---------|--:|-------------:|--:|--:|---------:|
| 1 | A (upright) | Line 1 — headline | 1.5 mm | 13.3 mm | 20.0 mm | 4.6 mm | 0° |
| 2 | A (upright) | Line 2 — detail | 1.5 mm | 17.7 mm | 20.0 mm | 3.5 mm | 0° |
| 3 | B (folded side) | Line 1 — headline | 1.5 mm | 5.1 mm | 20.0 mm | 4.6 mm | **180°** |
| 4 | B (folded side) | Line 2 — detail | 1.5 mm | 1.8 mm | 20.0 mm | 3.5 mm | **180°** |

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
| Line 1 baseline | y = 16.6 mm | y = 6.4 mm |
| Line 2 baseline | y = 20.0 mm | y = 3.0 mm |

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
2. Browse to `07-tech-pack/labeling/labels-power.csv`. First row is the header — confirm
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
2. Add a black rectangle behind each face's text (bounds: x=1.5, y=13.0, w=20, h=8.5 for Face A;
   x=1.5, y=1.5, w=20, h=8.5 for Face B — i.e. the full fold-half, safe-margin to safe-margin).
3. Set both text objects' font colour to white.
4. Type the content directly (2 labels needed) — no merge required for a single fixed design:
   - Line 1: `U5 · SPARE`
   - Line 2: `CPC 45A · 32A`

---

## §6 Print check before the run

1. Print **one** label of each design.
2. Measure the printed square with calipers: **23.0 mm × 23.0 mm** (±0.3 mm is normal roll
   tolerance; anything more means the media size in Editor doesn't match the loaded roll).
3. Confirm text clears the die-cut edge by roughly 1.5 mm on all sides.
4. Fold one TAG label over a scrap of cable-tie and check both faces read upright and square —
   the two fold-registration marks (printed as small ticks at the label edges on the fold line in
   the SVG proof) are a visual aid only; Editor's own template does not need to reproduce them.
5. Only then run the full batch (19 labels for the current power set — see
   `labels-power.csv`).

---

## §7 If you'd rather not rebuild by hand

Try `dk1221-power.lbx` first — open it in P-touch Editor before doing anything in this document.
If it opens and the objects are roughly where §2 says they should be, you're done: just re-run
Database Connect (§4) against the current `labels-power.csv` and print. If it doesn't open, or
opens with garbled/missing objects, discard it — this document rebuilds the identical layout with
zero guesswork.

---

*EMBLEM PROJECTS INC. · 2026-08-11 · companion to dk1221-power.lbx (best-effort, unverified)*
