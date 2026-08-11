---
title: Nomad Toronto — Cable & Device Label Spec (Brother DK-1221)
description: Print layout system for 23 mm square DK-1221 labels — fold geometry, safe areas, typography, naming convention, and P-touch Editor setup. Covers all four cable classes; CSV rows double as the source for the rack I/O schedule.
version: 0.10.0
created: 2026-08-11T00:00:00Z
last_updated: 2026-08-11T00:00:00Z
status: draft — six print sheets (power/audio/data × end A/B), 22 tags; .lbx opens in Editor, pending a test print and site verification of the unresolved rows
---

# Cable & Device Label Spec — DK-1221 (23 mm square)

## Changelog

- **0.10.0** — **The middle band carries the connectors.** Triple print spent a whole band on an
  identity copy the wrap always destroys; that band now prints `conn_a` (bold, this end) over
  `conn_b` (the far end) instead. Fold tolerance is unchanged — the two identity bands are still
  one per face — and whatever the wrap leaves of the middle band is information the outer bands
  do not carry. Object order is now `line1, line2, conn_a, conn_b, line1, line2`, so the sheet
  CSVs lead with those four columns and `split-label-ends.py` writes the abbreviated ASCII
  connector form (`etherCON RJ45` → `etherCON`) into `conn_a`/`conn_b` — the merged print and the
  proof now show the same string, which they did not before.

  Two things 0.9.0 got wrong come out with it. **The `.lbx`'s rotated bands were stacked in page
  order**, so both would have folded out reading line 2 above line 1 — the 180° angle flips the
  glyphs but not the boxes. Rotated bands are now stacked bottom-to-top, matching what the proof
  SVG always drew; the two were silently disagreeing. And it **records what triple print dropped**:
  the cable reference is printed nowhere at all — see §9.

- **0.9.0** — **Triple print replaces the two-face fold.** The same two lines are printed three
  times over the full 20 mm printable height instead of twice either side of a reserved 3 mm fold
  zone. Whichever band the fold crosses is sacrificed and the other two survive whole, one per
  face — so the fold no longer has to be accurate to a millimetre, which is the whole point.
  Bottom copy prints upright, the upper two at 180° so whichever surfaces on the back reads the
  right way up. 6 objects per tag, 6.67 mm per copy. `dk1221-tag-layout.svg` draws it, generated
  from box geometry read back out of a produced `.lbx`.

- **0.8.0** — **Six sheets: power / audio / data × end A / end B.** Each class is fitted in its
  own pass at the rack, so each pass gets its own print run. `split-label-ends.py` now emits one
  CSV per (class, end) and the combined per-end pair is retired — two overlapping sets is an
  invitation to print the wrong one. Also fixes the CP1252 mojibake Editor showed in the merge
  preview: printed fields are now ASCII (`·`→`-`, `→`→`->`, `Ω`→`OHM`) and every CSV carries a
  UTF-8 BOM, with `line1`–`line3` moved to the leading columns so Editor's auto-map lands on them.

- **0.7.0** — **Separate CSV per cable end.** `split-label-ends.py` derives
  `…-end-a.csv` and `…-end-b.csv` from any label set, one tag per end (qty 1 each) instead of two
  identical tags per cable. Each tag is now written from where it is fitted — line 1 the device,
  line 2 the socket, line 3 the cable ID and the far end — so a tag at the V3 #2 panel says
  `V3 #2 / CH1 IN / A15 → SP2120` instead of describing the other end of the cable. In the end-B
  file the end_a/end_b columns are swapped so `end_a` always means "this end", which keeps the
  proof's left-hand colour chip the end you are holding. Needed a third text line: a headline
  carrying device *and* port does not fit 17.11 mm.
- **0.6.9** — **Print area corrected.** A real Editor-authored `.lbx` showed the DK-1221 live
  area is **17.11 × 20.00 mm** (inset 2.96 mm left/right, 1.52 mm top/bottom), not the uniform
  1.5 mm margin assumed. Every line had been laid out 2.89 mm too wide. Also fixed the text
  measurement to apply Arial Narrow's 0.85 width ratio rather than treating Arial as the render
  font. `.lbx` generation rebuilt against the reference schema — see `ptouch-field-mapping.md` §7.

- **0.6.0** — Device colour key (`scripts/rack_palette.py`, shared by both builds) and
  pair-aware sheet layout. A `group` column keeps L/R partners, LF+HMF of the same cabinet, the
  four Pro DJ Link runs and the five Armonía links from being split across a row break — an L at
  the end of one row and its R at the start of the next is how one of them ends up on the wrong
  cable. Colour cannot go on the labels themselves: DK-1221 is black-only thermal.

- **0.5.0** — Scope narrowed to **rack-internal cables only**. `labels-rack-internal.csv` is now
  the print set: 11 designs / 22 labels, being the 5 cables with both ends on rack equipment plus
  6 excluded only by an unresolved fact. **No labels are printed for CQ-12T or DJM-V10
  connections.** The four class CSVs are retained as the full data set — the rack print set is
  derived from them by `build-rack-io-schedule.py`, not maintained separately.
- **0.4.0** — CSV schema extended with structured endpoint columns (`end_a/b_device`, `_port`,
  `_loc`, `conn_a/b`), so `07-tech-pack/rack-io-schedule.md` can be generated from the same rows
  that print the labels instead of being a third hand-maintained document. Added `PWR-P0` for the
  PDU's own mains feed, which every earlier draft missed — the PDU powers two devices but nothing
  documented what powered the PDU. Power set is now 10 designs / 21 labels.
- **0.3.0** — Audio, speaker and network sets drafted (39 designs, 78 labels), completing all
  four cable classes. Line structure inverted for the new sets: the **identity** takes line 1 at
  full size and the **cable ID + route** moves to line 2, because leading with `A11 · ` collapsed
  line 1 to 2.5 mm. Connector-type corrections from the I/O audit (D3) are applied at source —
  the TRS ends are labelled TRS. Two provisional labels are flagged inverse or noted; see §10.
- **0.2.0** — Bias V9 fully removed from the power set (no longer just offline). Circuit IDs
  P5–P8 renumbered to P4–P7 to close the gap; U5's freed CPC 45A / 32A breaker gets its own
  spare-identification label (`PWR-U5`) rather than disappearing silently. Added
  `dk1221-power.lbx` (best-effort, unverified — see §7) and `ptouch-field-mapping.md` (reliable
  manual rebuild path). **This set now disagrees with `cable-schedule.md` §8**, which still lists
  P4 = V9 and the old P5–P8 order — that document has not been updated in this pass.
- **0.1.0** — Initial power/IEC set, 8 circuits (P1–P8 incl. V9 offline).

**Media:** Brother DK-1221 · 23 mm × 23 mm die-cut · white paper, black thermal
**Printer:** Brother **QL series** (DK rolls are QL media — a PT-series handheld takes TZe
tape and will not accept this roll). Artwork is authored in **P-touch Editor**, which drives
both families, so "P-touch compatible" holds for the software, not the handheld.
**Print resolution:** 300 dpi on the current QL range — 1 mm = 11.8 dots.

---

## §1 What a 23 mm square can and cannot do

A label folded directly around a cable loses `π × d / 2` of its length to the cable itself.
What is left is split between the two readable faces:

| Cable OD | Consumed by the wrap | Face height each side | Verdict |
|---------:|---------------------:|----------------------:|---------|
| 5 mm | 7.9 mm | **7.6 mm** | ✅ two lines |
| 6 mm | 9.4 mm | **6.8 mm** | ✅ two lines |
| 7 mm | 11.0 mm | **6.0 mm** | ✅ one line + small second |
| 8 mm | 12.6 mm | **5.2 mm** | ✅ one line |
| 9 mm | 14.1 mm | **4.4 mm** | ⚠️ one line, tight |
| 10 mm | 15.7 mm | **3.6 mm** | ⚠️ marginal |
| 11 mm | 17.3 mm | **2.9 mm** | ❌ |
| 12 mm | 18.8 mm | **2.1 mm** | ❌ |

**Consequence for this rack:** the four Bias amp cords are IEC C19/C20 at roughly 10.5–12 mm OD.
They **cannot** be flag-folded onto the cable on this media. They get the tie-tag variant instead,
which is standard rack practice anyway. Only the C13-class cords (SP2120, CQ-12T PSU, ~7.5 mm)
could be folded directly — but we use one method throughout for consistency.

---

## §2 Variants

All three share the same 23 × 23 mm die-cut. The **live area is 17.11 × 20.00 mm** — inset
**2.96 mm left/right and 1.52 mm top/bottom**. These are the printer's own unprintable margins,
read out of a P-touch Editor file for DK-1221 on a QL-800; they are not a margin we chose, and
they are not symmetric. An earlier draft assumed a uniform 1.5 mm inset and so laid every line
out 2.89 mm too wide.

### A · TAG — fold over a cable-tie tail *(default for every rack cable)*

**Triple print.** The 20.00 mm printable height is divided into **three 6.67 mm bands**, each
holding two lines. There is no reserved fold zone and no single correct fold line: the wrap
destroys whichever band it crosses and the bands either side of it survive whole, one per face.
That is the point — the fold no longer has to be accurate to a millimetre.

```
┌───────────────────────┐  y 0
│  ▏ band 1  (rot 180°) │  y  1.52 –  8.19   line1 / line2   identity
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │  y  8.19           band tick
│  ▏ band 2  (rot 180°) │  y  8.19 – 14.85   conn_a / conn_b connectors
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │  y 14.85           band tick
│  ▏ band 3  (upright)  │  y 14.85 – 21.52   line1 / line2   identity
└───────────────────────┘  y 23
```

The bottom band prints upright and the upper two print **rotated 180°**, so whichever of them
surfaces on the back face reads the right way up once the tag is folded adhesive-to-adhesive.
1.2 mm registration ticks are printed at both edges on each band boundary.

**Why the middle band is not a third copy.** Printing the identity three times spent a whole band
on a copy the wrap always destroys. The middle band now carries the **connector at each end**
instead — `conn_a` in the bold slot, `conn_b` below it. Nothing is lost that was not already lost,
and whatever the wrap leaves is information the outer bands do not have. On a 6 mm OD cable the
wrap consumes `π × d / 2` ≈ 9.4 mm and takes the whole middle band; on a thin tie tail a usable
strip of it survives. **Treat it as a bonus, never as the only copy of anything** — the identity
is on both outer bands regardless.

`conn_a` is always *this end's* connector: `split-label-ends.py` swaps the end column groups on
the end-B sheets so the tag is written from where it is fitted. After the 180° rotation the bold
`conn_a` slot lands low in the band, next to the upright identity — the half of the middle band
that survives a fold biased towards the front face.

Line structure per band:

| Slot | Size | Floor | Content |
|------|------|-------|---------|
| upper | 3.2 mm bold | 2.6 mm | `line1` (device) · `conn_a` on the middle band |
| lower | 2.3 mm | 1.9 mm | `line2` (port) · `conn_b` on the middle band |

**`line3` is not printed.** The `A15 -> V3 #2` cross-reference is still generated into the CSV,
but a 6.67 mm band takes two lines at a readable size, not three, so nothing on the tag carries
the cable ID. The two-face layout it came from had 8.5 mm faces and room for it; that layout is
retained in the build scripts behind `TRIPLE = False`. This is an open trade, not a settled one —
see §9.

### B · FLAG — fold directly around the cable *(≤8 mm OD only)*

Same fold line, but the blank fold zone is `π × d / 2` instead of 3 mm. At 8 mm OD that is a
12.6 mm zone leaving **20 × 5.2 mm** faces — **one line only**. Reserved for control and
signal cables; not used in the power set.

### C · PLATE — flat on a connector shell or rack panel

No fold. Full **17.11 × 20.00 mm** live area, up to 4 lines. This is the device-ID plate variant
(device name · Armonía label · rack U + S/N · IP). Layout is defined but no plate artwork is
drafted yet — see §8.

---

## §3 Typography

- **Face:** Arial Narrow Bold for line 1, Arial Narrow for line 2. Any condensed grotesque
  works; avoid anything with fine hairlines — a 300 dpi thermal head drops strokes below
  ~0.1 mm.
- **Auto-fit:** the build script measures in Arial (Liberation Sans is metric-compatible), then
  scales by **0.85** for Arial Narrow's narrower advance width, and shrinks until it fits the
  17.08 mm live width. Treating the Arial measurement as final was free headroom while the live
  width was assumed to be 20 mm; against the real width it invented ~30 false "too wide" verdicts
  and shrank text that fits. A string that only fits by squeezing glyphs at the floor size raises a build warning
  — that is a signal to shorten the copy, not to accept the squeeze.
- **No hairline rules, no logos, no barcodes** at this size. Solid black inverse panels are
  fine and are used for the lockout label.
- **Separator:** middle dot `·` between fields. It reads at small sizes better than a hyphen
  and never gets mistaken for a minus sign in a circuit rating.

---

## §4 Naming convention

Cable IDs reuse the existing power IDs from `07-tech-pack/cable-schedule.md` §8 — **P1…P8** —
so the label, the schedule, and the rack elevation all speak the same language. Label IDs are
prefixed by class:

| Prefix | Class | Source of IDs | Designs |
|--------|-------|---------------|--------:|
| `PWR-` | Mains / IEC | cable-schedule §8, renumbered P1–P7 after V9 removal, plus P0 (PDU feed) | 10 |
| `AUD-` | Line-level audio | cable-schedule §1–4 (A01–A19) | 15 |
| `SPK-` | Speaker-level | cable-schedule §5–6 (S20–S35) | 14 |
| `NET-` | Control network / Pro DJ Link | cable-schedule §7 + §1 (N05–N41) | 10 |
| `DEV-` | Device ID plate (variant C) | rack elevation U-position | — not yet drafted |

Face content, power class:

```
line 1   <cable ID> · <device short name>
line 2   <rack U> · <connector> · <circuit>
```

Face content, all other classes — **identity first, ID second**:

```
line 1   <what this cable is>          MASTER L · XAIR L-3 · V3 #2
line 2   <cable ID> · <route or key fact>   A01 · DJM→CQ CH1
```

Power leads with the ID because `P4` *is* the circuit's name and there are only seven of them.
The other classes have 39 cables between them, where the useful glance-value is *what the cable
carries*, not its index — and leading with `A11 · ` pushed line 1 down to 2.5 mm, half the
intended size. Line 2 absorbs the ID at small size, where it is still perfectly readable for
cross-referencing the schedule.

Class-specific line 2 conventions:

| Class | Line 2 carries | Why |
|-------|---------------|-----|
| `AUD-` | `ID · FROM→TO` | Tracing a signal path is the whole job |
| `SPK-` | `ID · amp CH · impedance` | Load matters — a 4 Ω sub on a channel set for 8 Ω is a bad afternoon |
| `NET-` | `ID · IP address` | The IP is what you need when Armonía shows a device offline |

---

## §5 Placement

- **Both ends of every cable.** Quantity in the CSV is 2 per cable for this reason.
- Tie the tag **75–100 mm back from the connector** — close enough to be unambiguous, far
  enough that it does not foul the plug or the strain relief when the cord is seated.
- Fold so the tag hangs in the plane of the cable run, not across it. In a packed rear-of-rack
  a tag standing proud gets caught and torn off.
- Use the tie tail already present on the existing cable management where possible rather
  than adding ties — the rear of this rack is congested (see `03-rack-photos/amp-rack/`).

---

## §6 Durability caveat

DK-1221 is **uncoated paper**. Behind five amplifiers it will face heat, dust and handling.
Paper tags are fine for getting the rack identified now, but for a permanent install plan on
either:

- overwrapping each folded tag with a turn of clear tape or 12 mm clear heat-shrink, or
- reprinting the set on a laminated/film DK stock (e.g. DK-2113 continuous clear film cut to
  length) once the content is settled.

Either way, **settle the content first on paper** — that is what this draft is for.

The P4 lockout label is an **identification aid only**. It is not a lockout/tagout device and
does not substitute for a proper LOTO tag on the V9 breaker.

---

## §7 Printing from P-touch Editor

1. Load the DK-1221 roll and select the media in the **Paper / Media** selector — the
   `23mm x 23mm` DK-1221 entry sets the die-cut size and Brother's own print margins.
2. Open the matching `dk1221-rack-{class}-end-{a,b}.lbx`, or build the three-band structure from
   §2 by hand — `ptouch-field-mapping.md` has the exact mm values. The `-proof.svg` for the same
   sheet is the dimensional reference.
3. Connect the data: **Database / merge** → the matching `labels-rack-{class}-end-{a,b}.csv`.
   The six text objects run in order **Text1…Text6 = `line1`, `line2`, `conn_a`, `conn_b`,
   `line1`, `line2`**, and the sheet CSVs lead with those four columns so Editor's auto-map gets
   the first four right. **Text5 and Text6 must be pointed at `line1` and `line2` by hand** —
   Editor will not auto-map a column twice, and these are the duplicate identity band. Set every
   object to shrink-to-fit as a backstop.
4. Print options: **quality over speed**, halftone off (text only), **scaling 100% / no
   scale-to-fit**, auto-cut per label.
5. **Test print first** — run one label, measure the printed square with calipers, and confirm
   the text clears the die-cut edge by ~1.5 mm on all sides before committing the run.
6. Quantities are in the CSV `qty` column — every row is `qty 1`, 22 tags across the six sheets.

---

## §8 Files

| File | What it is |
|------|-----------|
| `07-tech-pack/labeling/labels-{power,audio,speaker,network}.csv` | Merge data — one row per label design, with the schedule cross-reference |
| `07-tech-pack/labeling/dk1221-{power,audio,speaker,network}-proof.svg` | 1:1 print proofs, A4. Print at 100% to verify before running the roll |
| `07-tech-pack/labeling/dk1221-rack-{power,audio,data}-end-{a,b}.lbx` | The six P-touch Editor templates, one per print sheet. Generated against a real Editor-authored reference file. All six share the identical 6-object triple-print layout — only the sample text differs — so if one opens correctly they all will |
| `07-tech-pack/labeling/dk1221-tag-layout.svg` | Object map: box positions, field bindings, and what each folded face reads. Generated by reading geometry back out of a produced `.lbx`, so it cannot drift |
| `07-tech-pack/labeling/ptouch-field-mapping.md` | Reliable fallback — exact mm/degree/field-binding values to rebuild the same layout natively in Editor's UI if the `.lbx` doesn't open |
| `scripts/build-cable-labels.py` | Regenerates the SVG proof from the CSV |
| `scripts/build-lbx.py` | Regenerates the `.lbx` from the CSV (first TAG, non-inverse row as sample content) |
| `scripts/build-rack-io-schedule.py` | Regenerates `07-tech-pack/rack-io-schedule.md` and the derived rack-internal CSV |
| `scripts/split-label-ends.py` | Splits a label CSV into per-end `-end-a` / `-end-b` sets, one file per class |
| `scripts/build-layout-diagram.py` | Redraws `dk1221-tag-layout.svg` from a produced `.lbx` |
| `scripts/rack_palette.py` | Device colours, short names and port abbreviations, shared by every build |

**CSV schema.** Each row carries both the printed content and the structured endpoint data:

| Columns | Used by |
|---------|---------|
| `line1`, `line2`, `conn_a`, `conn_b` | The four printed fields, in layout-object order — this is why they lead the sheet CSVs |
| `id`, `cable_ref`, `variant`, `invert`, `line3`, `qty` | Label artwork bookkeeping; `line3` is generated but not printed (see §9) |
| `class`, `end_a_device`, `end_a_port`, `end_a_loc`, `conn_a`, `end_b_device`, `end_b_port`, `end_b_loc`, `conn_b` | Rack I/O schedule — grouping, direction, connector types |
| `note` | Both, plus the provisional-row tables |

`end_*_loc` is one of `RACK`, `BOOTH`, `ROOM`, `ENTRANCE`, `PANEL`, `UNKNOWN`. The schedule derives
direction from it: both ends `RACK` → internal, one end `RACK` → in/out, neither → excluded from
the rack schedule. This is why the endpoint columns live here rather than in a separate file — the
label on the cable and the schedule row describing it are the same record.

```bash
# regenerate the schedule, the six sheets, and the layout diagram
python3 scripts/build-rack-io-schedule.py
python3 scripts/split-label-ends.py 07-tech-pack/labeling/labels-rack-internal.csv
for c in power audio data; do for e in a b; do
  python3 scripts/build-cable-labels.py \
      07-tech-pack/labeling/labels-rack-$c-end-$e.csv \
      07-tech-pack/labeling/dk1221-rack-$c-end-$e-proof.svg
  python3 scripts/build-lbx.py \
      07-tech-pack/labeling/labels-rack-$c-end-$e.csv \
      07-tech-pack/labeling/dk1221-rack-$c-end-$e.lbx
done; done
python3 scripts/build-layout-diagram.py \
    07-tech-pack/labeling/dk1221-rack-audio-end-a.lbx \
    07-tech-pack/labeling/dk1221-tag-layout.svg
```

**Print run — six sheets, one per class per cable end:**

| Sheet | Tags | Fitted at |
|-------|-----:|-----------|
| `labels-rack-power-end-a.csv` | 1 | PDU outlet |
| `labels-rack-power-end-b.csv` | 1 | SP2120 mains inlet |
| `labels-rack-audio-end-a.csv` | 5 | source ends — SP2120 outputs, V3 #2 line outs |
| `labels-rack-audio-end-b.csv` | 5 | destination ends — V3 #2 / Q5 / Q2 #2 / V3 #1 inputs |
| `labels-rack-data-end-a.csv` | 5 | switch ports |
| `labels-rack-data-end-b.csv` | 5 | amplifier Ethernet / etherCON ports |
| **total** | **22** | 11 cables × 2 ends |

Print and fit one sheet at a time: the sheet matches the pass. Every row is `qty 1` — the two ends
carry different text and are not interchangeable.

**Why the power sheets hold one tag each:** under the strict rack-internal scope only `P1`
(PDU → SP2120) has both ends on rack equipment. The five amplifier mains cords run from the venue
panel, which is outside the rack, so they are out of scope — see `rack-io-schedule.md` §4. They
are real cables in the rack with no ID on them; adding them back is a scope decision, not a
labelling one.

The four class CSVs describe 48 cables in total, but that is the system inventory, not the print
run. Nothing is printed for CQ-12T or DJM-V10 connections.

---

## §9 Still to draft

- [ ] **Decide what the tag loses: the cable ID or a connector.** Triple print gives two printed
      slots per band and the outer bands spend them on device + port. The cable reference
      (`A15`, `N36`, `P1`) — the field the schedule is indexed by — is therefore printed nowhere.
      Three ways out, none free:
      **(a)** fold `line3` into `line2` as `OUT L · A15`, which costs ~4 characters of port name;
      **(b)** give the middle band `line3` + `conn_a` and drop the far-end connector;
      **(c)** accept it — the device + port pair is unique per cable in an 11-cable rack, so the
      ID is recoverable from the schedule. Currently on (c) by default, which is the weakest
      reason to be anywhere.
- [ ] **Device ID plates (variant C)** — the original goal. 4-line layout is defined in §2 but
      no artwork is drafted. Content per device: name, Armonía label, rack U + S/N, IP.
- [ ] **Q5 → middle-sub cabinet links** — see §10.
- [ ] Confirm the QL model in use, and whether it is 300 dpi.

---

## §10 Provisional labels — print these last

Three groups encode something the I/O audit could not confirm from the manuals
(`07-tech-pack/rack-io-inventory.md` §12). They are drafted rather than withheld, because a
labelled rack with two flagged unknowns beats an unlabelled rack — but they are the ones to
re-print after the next site visit.

| Label | What is uncertain | How it is handled |
|-------|-------------------|-------------------|
| `AUD-A19` | The cable feeding V3 #1's input. The spec calls it "V3 #2 Line Out 3", but the V3 has only **two** line outputs (D1), so that source cannot be right as written. | Printed **inverse** — `V3#1 INPUT` / `A19 · SOURCE ?`. States the end that is certain and visibly flags the end that is not. Trace it and reprint. |
| `SPK-S22`, `SPK-S23` | The Q5 has **two** speakON outputs carrying two channels each, not four discrete NL4 runs (D2). How the four Xair cabinets are actually fed — breakout, or NL4 link-out cabinet to cabinet — is unconfirmed. | Only the **amp-end runs** are labelled, which are certain: `SUBS L 1+2` / `S22 · Q5 OUT1 · 4Ω`. Cabinet-to-cabinet link labels are deliberately not drafted — that would mean guessing the topology. |
| `NET-N36`–`N40` | The switch these home to is unlocated (D8). | Labelled normally. The link's identity and IP are certain; only the far-end *location* is unknown, which a cable label does not need to assert. |

**Not a guess, just corrected:** the TRS-vs-XLR items (D3) are settled facts from the manuals, so
`AUD-A03/A04` (DJM Booth out) and `AUD-A11`–`A14` (CQ Out 1–6) are labelled TRS at the source end
and are **not** provisional — even though `cable-schedule.md` still says XLR for all six.

---

*EMBLEM PROJECTS INC. · 2026-08-11 · draft for test print*
