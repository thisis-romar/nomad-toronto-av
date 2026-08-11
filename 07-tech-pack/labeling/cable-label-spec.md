---
title: Nomad Toronto — Cable & Device Label Spec (Brother DK-1221)
description: Print layout system for 23 mm square DK-1221 labels — fold geometry, safe areas, typography, naming convention, and P-touch Editor setup. Power/IEC set drafted first.
version: 0.1.0
created: 2026-08-11T00:00:00Z
last_updated: 2026-08-11T00:00:00Z
status: draft — power/IEC set ready for a test print; data and audio sets to follow
---

# Cable & Device Label Spec — DK-1221 (23 mm square)

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

| Prefix | Class | Source of IDs |
|--------|-------|---------------|
| `PWR-` | Mains / IEC | cable-schedule §8 (P1–P8) |
| `NET-` | Control network / AESOP / Dante | cable-schedule §7 (36–41) — not yet drafted |
| `AUD-` | Line-level audio | cable-schedule §1–4 (1–19) — not yet drafted |
| `SPK-` | Speaker-level | cable-schedule §5–6 (20–35) — not yet drafted |
| `DEV-` | Device ID plate (variant C) | rack elevation U-position |

Face content, power class:

```
line 1   <cable ID> · <device short name>
line 2   <rack U> · <connector> · <circuit>
```

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
| `07-tech-pack/labeling/labels-power.csv` | Merge data — one row per label design, with the schedule cross-reference |
| `07-tech-pack/labeling/dk1221-power-proof.svg` | 1:1 print proof, A4. Print at 100% to verify before running the roll |
| `scripts/build-cable-labels.py` | Regenerates the proof from the CSV |

```bash
python3 scripts/build-cable-labels.py \
    07-tech-pack/labeling/labels-power.csv \
    07-tech-pack/labeling/dk1221-power-proof.svg
```

---

## §9 Still to draft

- [ ] **Device ID plates (variant C)** — the original goal. 4-line layout is defined in §2 but
      no artwork is drafted. Content per device: name, Armonía label, rack U + S/N, IP.
- [ ] **Network set (`NET-`)** — 6 control links, but the switch they home to is still
      unlocated (rack I/O inventory §12-D8). Labelling them before that is settled would bake
      in a guess.
- [ ] **Audio and speaker sets (`AUD-`, `SPK-`)** — blocked on the connector corrections in
      rack I/O inventory §12-D1/D2/D3. Printing a label that says `Line Out 3` when the amp has
      two line outputs would make the labelling wrong on day one.
- [ ] Confirm the QL model in use, and whether it is 300 dpi.

---

*EMBLEM PROJECTS INC. · 2026-08-11 · draft for test print*
