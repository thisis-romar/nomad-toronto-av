---
title: Nomad Toronto — Cable & Device Label Spec (Brother DK-1221)
description: Print layout system for 23 mm square DK-1221 labels — fold geometry, safe areas, typography, naming convention, and P-touch Editor setup. Covers all four cable classes; CSV rows double as the source for the rack I/O schedule.
version: 0.6.0
created: 2026-08-11T00:00:00Z
last_updated: 2026-08-11T00:00:00Z
status: draft — rack-internal print set is 11 designs / 22 labels; pending a test print and site verification of the unresolved rows
---

# Cable & Device Label Spec — DK-1221 (23 mm square)

## Changelog

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

All three share the same 23 × 23 mm die-cut and a **1.5 mm safe margin** on every edge,
leaving a **20 × 20 mm live area**.

### A · TAG — fold over a cable-tie tail *(default for all rack power)*

Fold line across the centre at **y = 11.5 mm**, with a **3 mm blank fold zone** (y 10.0–13.0)
that wraps the tie tail. Each face is then **20 mm wide × 8.5 mm tall**.

```
┌───────────────────────┐  y 0
│  ▏ face B (rot 180°)  │  y 1.5 – 10.0   text
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │  y 11.5         FOLD  (ticks printed at both edges)
│  ▏ face A (upright)   │  y 13.0 – 21.5  text
└───────────────────────┘  y 23
```

Face B is printed rotated 180° so that, once folded adhesive-to-adhesive, **both faces read
upright**. Two 1.2 mm registration ticks are printed at the left and right edges on the fold
line so the installer folds square without measuring.

Line structure per face:

| Line | Purpose | Nominal size | Floor |
|------|---------|--------------|-------|
| 1 | Cable ID + device short name — `P6 · V3 #2` | 4.0 mm (~11.3 pt) bold | 2.6 mm |
| 2 | Location + connector + circuit — `U7 · C20 · 20A` | 2.8 mm (~7.9 pt) | 1.9 mm |

### B · FLAG — fold directly around the cable *(≤8 mm OD only)*

Same fold line, but the blank fold zone is `π × d / 2` instead of 3 mm. At 8 mm OD that is a
12.6 mm zone leaving **20 × 5.2 mm** faces — **one line only**. Reserved for control and
signal cables; not used in the power set.

### C · PLATE — flat on a connector shell or rack panel

No fold. Full **20 × 20 mm** live area, up to 4 lines. This is the device-ID plate variant
(device name · Armonía label · rack U + S/N · IP). Layout is defined but no plate artwork is
drafted yet — see §8.

---

## §3 Typography

- **Face:** Arial Narrow Bold for line 1, Arial Narrow for line 2. Any condensed grotesque
  works; avoid anything with fine hairlines — a 300 dpi thermal head drops strokes below
  ~0.1 mm.
- **Auto-fit:** the build script sizes every string against **full-width Arial metrics**
  (Liberation Sans is metric-compatible) and shrinks until it fits the 20 mm live width.
  Arial Narrow is ~82% of that width, so anything that passes the check prints with margin
  in hand. A string that only fits by squeezing glyphs at the floor size raises a build warning
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
2. Set the layout to the two-face structure in §2: fold line at 11.5 mm, face B rotated 180°.
   `dk1221-power-proof.svg` is the dimensional reference; build the Editor template to match.
3. Connect the data: **Database / merge** → `labels-power.csv` → map `line1` and `line2` to the
   two text objects. Set both objects to shrink-to-fit as a backstop.
4. Print options: **quality over speed**, halftone off (text only), **scaling 100% / no
   scale-to-fit**, auto-cut per label.
5. **Test print first** — run one label, measure the printed square with calipers, and confirm
   the text clears the die-cut edge by ~1.5 mm on all sides before committing the run.
6. Quantities are in the CSV `qty` column: 20 labels total (8 cables × 2 ends + 4 spares).

---

## §8 Files

| File | What it is |
|------|-----------|
| `07-tech-pack/labeling/labels-{power,audio,speaker,network}.csv` | Merge data — one row per label design, with the schedule cross-reference |
| `07-tech-pack/labeling/dk1221-{power,audio,speaker,network}-proof.svg` | 1:1 print proofs, A4. Print at 100% to verify before running the roll |
| `07-tech-pack/labeling/dk1221-{power,audio,speaker,network}.lbx` | Best-effort P-touch Editor templates. **Unverified** — Brother's `.lbx` schema is unpublished; these were reconstructed from memory and have not been opened in real Editor. Test before trusting. All four share the identical 4-object layout, so if one opens correctly they all will |
| `07-tech-pack/labeling/ptouch-field-mapping.md` | Reliable fallback — exact mm/degree/field-binding values to rebuild the same layout natively in Editor's UI if the `.lbx` doesn't open |
| `scripts/build-cable-labels.py` | Regenerates the SVG proof from the CSV |
| `scripts/build-lbx.py` | Regenerates the `.lbx` from the CSV (first TAG, non-inverse row as sample content) |
| `scripts/build-rack-io-schedule.py` | Regenerates `07-tech-pack/rack-io-schedule.md` from all four CSVs |

**CSV schema.** Each row carries both the printed content and the structured endpoint data:

| Columns | Used by |
|---------|---------|
| `id`, `cable_ref`, `variant`, `invert`, `line1`, `line2`, `qty` | Label artwork — proof, `.lbx`, and the P-touch merge |
| `class`, `end_a_device`, `end_a_port`, `end_a_loc`, `conn_a`, `end_b_device`, `end_b_port`, `end_b_loc`, `conn_b` | Rack I/O schedule — grouping, direction, connector types |
| `note` | Both, plus the provisional-row tables |

`end_*_loc` is one of `RACK`, `BOOTH`, `ROOM`, `ENTRANCE`, `PANEL`, `UNKNOWN`. The schedule derives
direction from it: both ends `RACK` → internal, one end `RACK` → in/out, neither → excluded from
the rack schedule. This is why the endpoint columns live here rather than in a separate file — the
label on the cable and the schedule row describing it are the same record.

```bash
# regenerate every proof sheet and template
for s in power audio speaker network; do
  python3 scripts/build-cable-labels.py \
      07-tech-pack/labeling/labels-$s.csv \
      07-tech-pack/labeling/dk1221-$s-proof.svg
  python3 scripts/build-lbx.py \
      07-tech-pack/labeling/labels-$s.csv \
      07-tech-pack/labeling/dk1221-$s.lbx
done
```

**Print run — rack-internal set only:** 11 designs / **22 labels**
(`labels-rack-internal.csv`, derived by `build-rack-io-schedule.py`).

The four class CSVs together describe 48 cables / 99 labels, but that is the full
system inventory, not the print run. Only cables with both ends on rack equipment —
plus those excluded solely by an unresolved fact — get printed. Nothing is printed for
CQ-12T or DJM-V10 connections. See `07-tech-pack/rack-io-schedule.md` for the scope
boundary and what falls outside it.

---

## §9 Still to draft

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
