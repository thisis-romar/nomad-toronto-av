---
title: NØMAD Toronto — Lighting System Specification
description: Lighting system specification for NØMAD Toronto, decoded from the grandMA2 "Nomad" showfile export (showfile 2026-06-13, exported 2026-06-24). Rev 1.0 — desktop decode; physical site verification pending.
version: 1.2.0
created: 2026-06-24T00:00:00Z
last_updated: 2026-08-25T00:00:00Z
---

# NØMAD Toronto — Lighting System Specification

**Revision:** 1.2
**Date:** June 2026
**Prepared by:** Emblem Projects Inc.
**Venue:** NØMAD Toronto
**Status:** Decoded from grandMA2 showfile `nomad_2026-06-13_kayo-toronto-ft-pools` (exported 2026-06-24). **Desktop decode only — physical positions, real fixture models, DMX node topology, and power are NOT in the showfile and are flagged TBC throughout.**

> **Source of truth:** `08-lighting/source-showfile/NOMADFIXPATCHJUNE2026.xml`. Every fixture,
> channel count, and DMX address in this document is derived from that export. If the showfile
> is re-exported, this spec must be re-validated against it.

---

## §1 System Overview

NØMAD Toronto operates a grandMA2-controlled intelligent lighting rig alongside its permanent
VOID Acoustics PA system (documented separately in `01-source-documents/nomad-system-spec-v2.md`).
The rig is built for DJ-format electronic-music events: moving beams, moving washes, LED strobe
bars, laser bars, plus CO₂ jets and atmospheric haze.

| Subsystem | Fixtures | MA profile(s) | Universe(s) |
|-----------|---------:|---------------|-------------|
| DJ-deck LED bar | 1 | `3 LED Bar 2 11CH` | U1 |
| LED strobe bars | 7 | `4 rgbw-13ch 13CH` | U1 |
| Moving washes | 10 | `5 NEW WASH` ×8 · `6 movingwash zone` ×2 | U1 + U2 |
| Moving beams (Sharpy) | 4 | `9 Sharpy Standard Lamp on` | U1 |
| Laser bars | 9 | `8 LASER BARS 26CH` ×8 · `7 LASER BARS - Invert 26CH` ×1 | U1 + U2 |
| CO₂ jets | 1 (multipatch ×2) | `2 Dimmer 00` | **unpatched** |
| Atmospheric (haze) | 1 | `2 Dimmer 00` | U2 |

**Total intelligent/LED fixtures:** 31
**Effects devices:** 2 CO₂ jets (1 fixture, multipatched) + 1 hazer
**DMX universes in use:** 2
**Console:** grandMA2 "Nomad" v3.9.60

```
                       grandMA2 "Nomad" (v3.9.60)
                                │
              ┌─────────────────┴─────────────────┐
          Universe 1                           Universe 2
   (abs 1–512)                          (abs 513–1024)
   ├── DJ-LED bar (1)                   ├── M.Wash 9, 10  (2)
   ├── Strobe bars (7)                  ├── Laser.BAR 9   (1)
   ├── M.Wash 1–8 (8)                   └── Atmos hazer   (1)
   ├── M.Beam 1–4 (4)
   └── Laser.BAR 1–8 (8)

   CO₂ jets (Co2-HL.HR ×2) — UNPATCHED (address 0)
```

---

## §2 Lighting Console

| Field | Value |
|-------|-------|
| Platform | grandMA2 "Nomad" (MA Lighting) |
| Schema version | 3.9.60 |
| Showfile | `nomad_2026-06-13_kayo-toronto-ft-pools` |
| Showfile date | 2026-06-13 |
| Export | 2026-06-24T15:15:38 |

> ❓ **On-site hardware unconfirmed.** "Nomad" is the MA Lighting dongle-licensed software
> platform. The physical control surface on-site — grandMA2 onPC + Nomad dongle, a command
> wing, or a full grandMA2 console — and its booth location are **not** described by the export.
> Confirm on next site visit (Open Item §9.7).

---

## §3 DMX Universe Map

Addresses in the showfile are **absolute** (1-based across the whole patch). Universe-relative
addresses are derived as `relative = absolute − (universe − 1) × 512`.

| Universe | Absolute range | Fixtures patched | Approx. channels used |
|----------|----------------|------------------|----------------------:|
| Universe 1 | 1 – 512 | DJ-LED, 7 strobe bars, M.Wash 1–8, M.Beam 1–4, Laser.BAR 1–8 | 438 |
| Universe 2 | 513 – 1024 | M.Wash 9 & 10, Laser.BAR 9, Atmos | 45 |

> ❓ **DMX node/output topology unknown.** The showfile patches addresses but does not record
> which physical DMX node/port (ArtNet/sACN/DMX output) drives each universe. Confirm on-site
> (Open Item §9.4).

---

## §4 Fixture Inventory

Per-group inventory below. Addresses are shown universe-relative with the absolute address in
parentheses. End address = start + channel-count − 1. This inventory is the single source feeding
`07-tech-pack/dmx-patch-schedule.md`.

### §4.1 LED — DJ-Decks (MA layer `--LED.DJ-Decks`)

| Fixture | FID | MA profile | Ch | Universe | Start | End | Cells |
|---------|----:|------------|---:|----------|-------|-----|------:|
| DJ-LED | 1 | `3 LED Bar 2 11CH` | 11 | U1 | 11 | 21 | 4 |

### §4.2 LED Strobe Bars (MA layer `--LED.STROBE-BAR`)

All `4 rgbw-13ch 13CH`, 13 ch, Universe 1.

| Fixture | FID | Start | End |
|---------|----:|-------|-----|
| LED.Strobe-BAR 1 | 801 | 448 | 460 |
| LED.Strobe-BAR 2 | 802 | 435 | 447 |
| LED.Strobe-BAR 3 | 803 | 422 | 434 |
| LED.Strobe-BAR 4 | 804 | 409 | 421 |
| LED.Strobe-BAR 5 | 805 | 396 | 408 |
| LED.Strobe-BAR 6 | 806 | 383 | 395 |
| LED.Strobe-BAR 7 | 807 | 357 | 369 |

> Note an address gap between BAR 7 (ends 369) and BAR 6 (starts 383): 370–382 is free. Confirm
> whether intentional spare room or a stale patch (Open Item §9.5).

### §4.3 Moving Washes (MA layer `--M.WASH`)

All 9 ch. Two MA profiles are mixed within this logical group.

| Fixture | FID | MA profile | Universe | Start | End | Abs |
|---------|----:|------------|----------|-------|-----|-----|
| M.Wash 1 | 101 | `5 NEW WASH` | U1 | 498 | 506 | 498 |
| M.Wash 2 | 102 | `5 NEW WASH` | U1 | 469 | 477 | 469 |
| M.Wash 3 | 103 | `5 NEW WASH` | U1 | 244 | 252 | 244 |
| M.Wash 4 | 104 | `5 NEW WASH` | U1 | 235 | 243 | 235 |
| M.Wash 5 | 105 | `5 NEW WASH` | U1 | 271 | 279 | 271 |
| M.Wash 6 | 106 | `5 NEW WASH` | U1 | 489 | 497 | 489 |
| M.Wash 7 | 107 | `6 movingwash zone` | U1 | 262 | 270 | 262 |
| M.Wash 8 | 108 | `5 NEW WASH` | U1 | 253 | 261 | 253 |
| M.Wash 9 | 109 | `5 NEW WASH` | U2 | 210 | 218 | 722 |
| M.Wash 10 | 110 | `6 movingwash zone` | U2 | 200 | 208 | 712 |

### §4.4 Moving Beams (MA layer `--M.Beam`)

All `9 Sharpy Standard Lamp on`, 14 ch, Universe 1. Profile name indicates a **Clay Paky Sharpy**
beam (confirm physical model — Open Item §9.3).

| Fixture | FID | Start | End |
|---------|----:|-------|-----|
| M.BEAM 1 | 401 | 312 | 325 |
| M.BEAM 2 | 402 | 280 | 293 |
| M.BEAM 3 | 403 | 296 | 309 |
| M.BEAM 4 | 404 | 328 | 341 |

### §4.5 Laser Bars (MA layer `--M.Laser-BAR`)

All 26 ch, 7 sub-cells.

| Fixture | FID | MA profile | Universe | Start | End | Abs |
|---------|----:|------------|----------|-------|-----|-----|
| Laser.BAR(6) 1 | 1001 | `7 LASER BARS - Invert 26CH` | U1 | 209 | 234 | 209 |
| Laser.BAR(6) 2 | 1002 | `8 LASER BARS 26CH` | U1 | 183 | 208 | 183 |
| Laser.BAR(6) 3 | 1003 | `8 LASER BARS 26CH` | U1 | 157 | 182 | 157 |
| Laser.BAR(6) 4 | 1004 | `8 LASER BARS 26CH` | U1 | 131 | 156 | 131 |
| Laser.BAR(6) 5 | 1005 | `8 LASER BARS 26CH` | U1 | 105 | 130 | 105 |
| Laser.BAR(6) 6 | 1006 | `8 LASER BARS 26CH` | U1 | 79 | 104 | 79 |
| Laser.BAR(6) 7 | 1007 | `8 LASER BARS 26CH` | U1 | 53 | 78 | 53 |
| Laser.BAR(6) 8 | 1008 | `8 LASER BARS 26CH` | U1 | 27 | 52 | 27 |
| Laser.BAR(6) 9 | 1009 | `8 LASER BARS 26CH` | U2 | 1 | 26 | 513 |

> Note Laser.BAR 1 uses the **invert** profile and its sub-cell addresses run in descending order
> (abs 209–215 across cells 1–7), the mirror of bars 2–9. Laser.BAR 9 is alone on Universe 2.

### §4.6 Effects — CO₂ (MA layer `--Co2(2x)`)

| Fixture | FID | MA profile | Ch | Universe | Address |
|---------|----:|------------|---:|----------|---------|
| Co2-HL.HR | 911 | `2 Dimmer 00` | 1 | — | **0 (UNPATCHED)** |
| Co2-HL.HR (multipatch) | 911 | `2 Dimmer 00` | 1 | — | **0 (UNPATCHED)** |

> ⚠️ Both CO₂ jets are a single fixture multipatched ×2 and are **unpatched** (address 0). Patch
> and verify on-site before use (Open Item §9.1).

### §4.7 Effects — Atmospheric / Haze (MA layer `~Atmos~`)

| Fixture | FID | MA profile | Ch | Universe | Start | Abs |
|---------|----:|------------|---:|----------|-------|-----|
| -Atmos- | 420 | `2 Dimmer 00` | 1 | U2 | 356 | 868 |

---

## §5 Fixture Types / Profiles — Real-World Model Status

The showfile carries **generic MA fixture-profile names**, not confirmed manufacturer models. In
August 2026 the venue supplied three fixture manuals (`manuals/`), which identify three of the six
fixture families. Full working in `fixture-identification-audit.md`.

| MA profile | Qty | Ch | Real-world fixture | Modes | Power ea. | Status |
|------------|----:|---:|--------------------|-------|----------:|--------|
| `9 Sharpy Standard Lamp on` | 4 | 14 | **YF BEAM 230** — 189/230 W discharge beam | 16 / 20 | 350–400 W | ❌ **No 14CH mode** — but patched on a 16-ch stride, audit §6 |
| `5 NEW WASH` | 8 | 9 | **BETOPPER LM70S** — 7×8 W RGBW mini head | **9** / 14 | 100 W | ⚠️ Probable — footprint and stride both 9 |
| `6 movingwash zone` | 2 | 9 | **BETOPPER LM70S** | **9** / 14 | 100 W | ⚠️ Probable |
| `8 LASER BARS 26CH` | 8 | 26 | **Panda Lighting LS650/LS652** — 6-head laser bar | 11 / 19 / 24 | 150 W | ❌ **No 26CH mode** — audit §5 · ☢️ Class 4 |
| `7 LASER BARS - Invert 26CH` | 1 | 26 | **Panda Lighting LS650/LS652** | 11 / 19 / 24 | 150 W | ❌ **No 26CH mode** · ☢️ Class 4 |
| `4 rgbw-13ch 13CH` | 7 | 13 | **Light4Me STROBE MULTI BAR** | 4 / 16 / 168 | 200 W | ❌ **No 13CH mode** — audit §4 |
| `3 LED Bar 2 11CH` | 1 | 11 | LED bar (unknown make) | — | ❓ | ❓ TBC — nothing supplied |
| `2 Dimmer 00` | 3 | 1 | Relay/dimmer (CO₂ ×2, hazer ×1) | — | ❓ | ❓ TBC — nothing supplied |

> ⚠️ **"Clay Paky Sharpy" — the brand is retracted, the class is not.** `9 Sharpy Standard Lamp on`
> is an MA profile *name*. The fixture is probably a **YF BEAM 230**, a 189/230 W discharge beam;
> a Sharpy's own lamp is a 189 W MSD Platinum 5R, so the profile was a sensible pick for a
> Sharpy-clone. An earlier revision of this document identified the beams as BETOPPER LM70S LED
> mini heads — **that is withdrawn**: it fit the 14CH profile but not the 16-channel address stride,
> and it understated the beams by ~1.2 kW.

> ❌ **Three profiles are patched to footprints their fixture cannot be set to** — strobes 13CH,
> lasers 26CH, beams 14CH. The patch is internally consistent (no address overlaps), so **do not
> re-patch** until the on-site panel check in `fixture-identification-audit.md` §7 is done.

---

## §6 Groups & Layers

The MA showfile organises the rig into named layers, grouped under three section header layers
(`//LED`, `//BEAMS`, `//SFX`):

| Section | MA layer | Contents |
|---------|----------|----------|
| `//LED` | `--LED.DJ-Decks` | DJ-LED bar |
| `//LED` | `--LED.STROBE-BAR` | LED.Strobe-BAR 1–7 |
| `//LED` | `--M.WASH` | M.Wash 1–10 |
| `//BEAMS` | `--M.Beam` | M.BEAM 1–4 |
| `//SFX` | `--M.Laser-BAR` | Laser.BAR(6) 1–9 |
| `//SFX` | `--Co2(2x)` | Co2-HL.HR (×2 multipatch) |
| `//SFX` | `~Atmos~` | -Atmos- hazer |

---

## §7 Effects Devices

- **CO₂ jets** — `Co2-HL.HR`, single MA fixture multipatched to two physical jets, controlled as
  a 1-channel dimmer/relay. **Currently unpatched** (address 0).
- **Atmospheric haze** — `-Atmos-`, a 1-channel dimmer/relay on Universe 2 (abs 868).

Real controller make/model and trigger wiring for both are **not** in the showfile (Open Item §9.3, §9.6).

---

## §8 Power & Data

> ❓ **No lighting power or DMX-distribution data exists in the showfile.** Per-fixture power now
> comes from the manufacturers instead — everything else is still TBC and must be gathered on-site.

| Item | Status |
|------|--------|
| Per-fixture power draw | 🟡 **Manufacturer figures on file** for 4 of 6 fixture types |
| Total connected load | 🟡 **5.15–5.35 kW identified ≈ 43–45 A @ 120 V** — a *subtotal*; DJ bar, CO₂ and hazer missing. Table in `fixture-identification-audit.md` §9 |
| Lighting mains feed / breaker(s) | ❓ TBC |
| Power factor / inrush allowance | ❓ TBC — the currents above assume unity PF and are a floor, not a design figure |
| Laser safety class and controls | ☢️ **Class 4** (9 bars × 6 × 500 mW, 638 nm). Compliance items unrecorded — audit §9 |
| DMX node make/model (ArtNet/sACN/DMX) | ❓ TBC |
| DMX node → universe/port mapping | ❓ TBC |
| Data cabling (DMX runs, topology) | ❓ TBC |

---

## §9 Open Items / Data Integrity

Everything not present in the showfile is listed here rather than invented. Consistent with the
repo's treatment of unconfirmed audio items (`❓ Unconfirmed` / "TBC" / "do not patch until
verified").

1. **CO₂ jets unpatched** — `Co2-HL.HR` at DMX address 0. Patch + verify on-site.
2. **Fixture positions unknown** — every `<AbsolutePosition>` in the showfile is `0,0,0`. No
   to-scale **physical plot** can be drawn without a site survey. (A schematic **DMX patch map**
   — address allocation, not geography — is provided at `assets/svg/dmx-patch-map.svg`.)
3. **Real makes/models behind generic MA profiles** — *mostly resolved.* Manuals and manufacturer
   data supplied 2026-08-25 identify the laser bars (**Panda Lighting LS650/LS652**, near-certain),
   the moving beams (**YF BEAM 230**, probable), the moving washes (**BETOPPER LM70S**, probable)
   and the strobe bars (**Light4Me STROBE MULTI BAR**, likely). Still unidentified:
   `3 LED Bar 2 11CH` (DJ-deck bar) and `2 Dimmer 00` (CO₂ ×2 + hazer). The Clay Paky *brand* claim
   is **retracted**, but the beams are a Sharpy-class discharge fixture after all — see §5 and
   `fixture-identification-audit.md`.
8. **Strobe bars patched 13CH — the Light4Me offers 4/16/168.** If the bars are really in 16CH mode
   they overrun their slots and five of them collide with the next bar by 3 channels
   (`fixture-identification-audit.md` §4). Read the mode off a bar's LCD before changing anything.
9. **Laser bars patched 26CH — the LS650/LS652 offers 11/19/24.** No collision (24 < 26), but 2 channels
   per bar are dead and the profile's internal channel order cannot be verified from the export
   (audit §5).
10. **Beams patched 14CH but spaced 16 — the YF BEAM 230 offers 16/20.** Nothing collides; the last
   two channels of each beam are simply unreachable from the console. Load a 16-channel profile on
   the same addresses (audit §6).
11. **Laser class 4 — compliance items unrecorded.** Nine bars at 6 × 500 mW / 638 nm. Audience
   reachability cannot be assessed while fixture positions are unknown (Open Item 2). Resolve with
   the venue's safety advisor, not from the desk (audit §9).
12. **YF BEAM 230 manual not on file** — its 16/20CH modes are from the published manual for that
   model, not from a document the venue supplied. Source it, or confirm from the fixture panel.
4. **DMX node/output topology** — map U1/U2 to physical nodes/ports.
5. **Strobe-bar address gaps** — confirm intentional spares vs. stale patch (e.g. 370–382 free).
   *Note:* that 13-channel gap is exactly the extra room a 16CH Light4Me bar would need, which may
   be the explanation — see Open Item 8.
6. **Lighting power/breakers** — no PSU/load/breaker data; confirm with venue electrician.
7. **Console make/model/location** — confirm grandMA2 hardware and booth position.

---

## §10 Source

| Field | Value |
|-------|-------|
| Showfile | `08-lighting/source-showfile/NOMADFIXPATCHJUNE2026.xml` |
| Fixture manuals | `08-lighting/manuals/` (3 supplied 2026-08-25) |
| Manufacturer electrical data | Vendor product pages, relayed by the venue 2026-08-25 |
| Identification audit | `08-lighting/fixture-identification-audit.md` |
| Provenance | `08-lighting/source-showfile/README.md` |
| Console | grandMA2 "Nomad" v3.9.60 |
| Showfile name | `nomad_2026-06-13_kayo-toronto-ft-pools` |
| Exported | 2026-06-24T15:15:38 |

---

*EMBLEM PROJECTS INC. · 2026-06-24*
