---
title: NØMAD Toronto — Rev 7.2 ⇄ Fixture Audit Reconciliation
description: Reconciles EMBLEM's Complete Lighting Power & DMX Schedule Rev 7.2 (24 Aug 2026) against the showfile-derived fixture identification audit. Two documents, two independent routes, the same seven fixtures — plus what each one holds that the other does not.
version: 1.0.0
created: 2026-08-25T00:00:00Z
last_updated: 2026-08-25T00:00:00Z
status: desktop reconciliation — no conflicts of fact found; three items adopted from Rev 7.2, two documentation defects raised against it
---

# Rev 7.2 ⇄ Fixture Audit Reconciliation

Two documents now describe the NØMAD lighting rig, written a day apart and from opposite
directions:

| | Route | Holds |
|---|-------|-------|
| **Rev 7.2** — `nomad-lighting-power-dmx-schedule-rev7.2.pdf` (EMBLEM, 24 Aug 2026) | Manuals → fixtures → power | Inventory, every DMX personality in full, 120/240 V comparison, branch allocation |
| **This audit** — `fixture-identification-audit.md` (25 Aug 2026) | Showfile → patch → manuals | Addresses, universes, the schedule, mode mismatches, orientation, laser class |

Neither document derives from the other. That makes the overlap between them the most useful thing
here.

---

## §1 The headline: independent confirmation

**Rev 7.2 identifies exactly the same seven devices, in the same quantities, with the same DMX
modes and the same wattages** — reached from the manuals alone, without ever opening the showfile.
This audit reached the same list from the patch, using the manuals only to test it.

| Device | Rev 7.2 | This audit | Agree |
|--------|---------|-----------|:---:|
| Light4Me Strobe Multi Bar | ×7 · 200 W · 4/16/168 CH | ×7 · 200 W · 4/16/168 CH | ✅ |
| BETOPPER LM70S | ×10 · 100 W · 9/14 CH | ×10 · 100 W · 9/14 CH | ✅ |
| YF Beam 230 | ×4 · 400 W planning · 16/20 CH | ×4 · 350–400 W · 16/20 CH | ✅ |
| Panda LS650 | ×9 · 150 W · 11/19/24 CH | ×9 · 150 W · 11/19/24 CH | ✅ |
| Microh LEDBAR RGB | ×1 · 50 W · 13 CH | ×1 · 50 W · 13 CH | ✅ |
| Chauvet Hurricane Haze 2D | ×1 · 533 W · 2 CH | ×1 · 533 W · 2 CH | ✅ |
| Elation DP-415 | ×1 · 120 V, 15 A, 5 A/ch | ×1 · 120 V, 15 A, 5 A/ch | ✅ |

The channel maps agree too — Rev 7.2 §5–§11 and audit §5 give the same assignment for every
channel of every personality they both cover, including the YF Beam's ch15 Reset / ch16 Lamp
control and the Microh's three RGB segments.

**No conflict of fact was found between the two documents.** Everything below is one holding
something the other does not.

### Arithmetic check

Rev 7.2's power and circuit tables were recomputed independently. Every figure reproduces: the
per-fixture currents, the 5,933 W total, all four branch loads and their margins, and the 1,747 W
aggregate. One rounding difference, correctly attributed: Rev 7.2 quotes the hazer at **4.40 A**,
which is the Chauvet manual's own figure; 533 W ÷ 120 V computes to 4.44 A. The 0.04 A carries into
the total (49.40 vs 49.44 A) and matters nowhere.

---

## §2 Adopted from Rev 7.2

Three things Rev 7.2 has that this audit did not, now folded into the dossier (`assets/lighting-dossier.html` §8):

**1. The Hurricane Haze 2D is a fixed-voltage product family.** Rev 7.2 flags that the 120 V unit
must not be treated as universal input. That is correct and this audit missed it — the manual
offers 120 VAC 60 Hz *or* 230 VAC 50 Hz depending on the model, with the same 533 W drawing 4.4 A
or 2.3 A. Recorded.

**2. The Microh's voltage rating is contradictory in its own manual.** Rev 7.2 states 120–220 V
switchable; this audit had recorded AC 100–240 V. Both are in the manual — the specification page
says 100–240 V, the connection page says 120–220 V switchable. Rev 7.2 took the narrower reading,
which is the right instinct. Both are now recorded, with the data plate as the tiebreak.

**3. The 120 V / 20 A branch allocation.** This audit had a total and no plan. Rev 7.2's is sound
and is now carried in the dossier:

| Circuit | Allocation | W | A @ 120 V | Margin to 80% |
|---------|-----------|--:|----------:|--------------:|
| LX-1 | 4 × YF Beam 230 | 1,600 | 13.33 | 320 W · 2.67 A |
| LX-2 | 7 × Light4Me Strobe Multi Bar | 1,400 | 11.67 | 520 W · 4.33 A |
| LX-3 | 9 × Panda LS650 | 1,350 | 11.25 | 570 W · 4.75 A |
| LX-4 | 10 × LM70S + Microh + Haze 2D | 1,583 | 13.19 | 337 W · 2.81 A |
| **Total** | 4 branches | **5,933** | **49.44** | 1,747 W aggregate |

> **One gap, and it is this audit's finding rather than a fault in Rev 7.2.** The two CO₂ jets
> appear in neither load table — Rev 7.2 counts "32 fixture/effect loads", which is the 32 lighting
> fixtures. But the jets are DP-415 channels, and the DP-415's feed sits inside **LX-4**, the
> second-tightest branch in the plan at 2.81 A of margin. Whatever the jets draw comes out of that
> margin and out of the pack's own 15 A. Nobody has a figure for them.

---

## §3 What this audit holds that Rev 7.2 does not

Rev 7.2 contains no DMX addresses at all — it is the fixture-and-power half of the picture. The
patch half is only in this audit:

| | Detail |
|---|--------|
| **Addressing** | Every fixture's universe, universe-relative start/end and absolute address; the full 34-fixture schedule; both universes drawn to scale |
| **Patch integrity** | 32 patched, 2 unpatched, **no address overlaps**, no universe-boundary crossings — never previously checked |
| **The mismatches, quantified** | Rev 7.2 §4 notes that "current June grandMA2 personalities still differ from several supplied manuals", which is true and unquantified. This audit names five, with the consequence of each: which one can collide (strobes, at 396–398, 409–411, 422–424, 435–437, 448–450), which costs a function (beams — ch15 Reset, ch16 Lamp control), which lands on the wrong channel (DJ bar, offset by two), which is half a fixture (hazer), which merely wastes addresses (lasers) |
| **The address stride** | The evidence that identified the beams: they are patched on a uniform 16-channel stride, which is the YF Beam's 16CH mode and not the profile's 14 |
| **Inverted fixtures** | M.Wash 7, M.Wash 10 and Laser.BAR(6) 1 run on pan/tilt-inverted duplicate profiles — the only fixture-orientation data the project holds |
| **Laser class** | Nine bars × 6 × 500 mW at 638 nm is **Class 4**. Rev 7.2 does not raise it; nothing in the repo did either until this audit |
| **CO₂ jets on the DP-415** | Reframes the long-standing "CO₂ unpatched at address 0" item — they do not take a patch of their own |

Read together, the two documents cover the rig completely. Neither does alone.

---

## §4 Raised against Rev 7.2

Two documentation defects, neither affecting a number.

**1. The page headers say Rev 7.0; the footers say Rev 7.2.** Every one of the ten pages carries
both. In a document titled `…FINAL`, that is worth a pass.

**2. The sources page links to a superseded file.** Rev 7.2 cites
`08-lighting/nomad-lighting-spec-v1.md` on **`main`** as its reference for "fixture quantities and
current grandMA2 showfile profiles". That file on `main` is v1.0.0 and **22 commits behind** this
work: it still attributes the moving beams to a **Clay Paky Sharpy**, an identification Rev 7.2
itself supersedes by naming the YF Beam 230. Anyone following the link from the PDF lands on the
retracted claim.

> Either merge `claude/nomad-rack-io-inventory-fpq2ni` to `main`, or repoint the link at the
> branch. The first is better — the PDF's own fixture list is the thing that makes the branch
> correct.

---

## §5 What neither document has

- The **CO₂ jets' make, model and wattage** — the last load with no figure anywhere.
- **Fixture positions.** Every `AbsolutePosition` in the showfile is `0,0,0`, so no plot can be
  drawn and no assessment can be made of whether a laser bar reaches audience-accessible space.
- **DMX node topology** — what physically drives U1 and U2.
- **The lighting mains feed and breakers.** Rev 7.2's branch allocation is a *recommendation*; what
  is actually installed is unrecorded.
- **Power factor and inrush.** Both documents compute current as W ÷ V at unity PF. That is a
  floor. Four discharge ballasts and a rig of switch-mode supplies will draw more.
- **Anything verified at the rig.** Both documents say so; Rev 7.2 §12 and audit §9 give
  substantially the same instruction, which is worth stating once more here: preserve the working
  showfile until a channel-by-channel test confirms the personality.

---

## §6 Sources

| | |
|---|---|
| Rev 7.2 | `08-lighting/nomad-lighting-power-dmx-schedule-rev7.2.pdf` — EMBLEM PROJECTS INC., 24 Aug 2026, 10 pp. |
| This audit | `08-lighting/fixture-identification-audit.md` rev 3.1 · `assets/lighting-dossier.html` |
| Showfile | `08-lighting/source-showfile/NOMADFIXPATCHJUNE2026.xml` (grandMA2 3.9.60, exported 2026-06-24) |
| Manuals | `08-lighting/manuals/` — the same seven both documents draw on |
| Arithmetic check | Recomputed from the manual wattages; see §1 |

---

*EMBLEM PROJECTS INC. · 2026-08-25*
