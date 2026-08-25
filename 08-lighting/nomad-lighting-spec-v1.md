---
title: NØMAD Toronto — Lighting System Specification
description: Lighting system specification for NØMAD Toronto, decoded from the grandMA2 "Nomad" showfile export (showfile 2026-06-13, exported 2026-06-24). Rev 1.0 — desktop decode; physical site verification pending.
version: 1.3.1
created: 2026-06-24T00:00:00Z
last_updated: 2026-08-25T00:00:00Z
---

# NØMAD Toronto — Lighting System Specification

**Revision:** 1.3
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

All `9 Sharpy Standard Lamp on`, 14 ch, Universe 1 — but patched on a **16-channel stride**, which
is the **YF BEAM 230**'s 16CH mode. The profile is two channels short and loses ch15 Reset and
ch16 Lamp control (§5, Open Item §9.2). The profile name is an MA label, not a Clay Paky Sharpy.

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

> ⚠️ Both CO₂ jets are a single MA fixture multipatched ×2 and are **unpatched** (address 0).
> They are **channels on an Elation DP-415 switch pack**, not DMX fixtures — what they need is the
> pack's dip-switch start address, not a patch of their own (§8, Open Item §9.11).

### §4.7 Effects — Atmospheric / Haze (MA layer `~Atmos~`)

| Fixture | FID | MA profile | Ch | Universe | Start | Abs |
|---------|----:|------------|---:|----------|-------|-----|
| -Atmos- | 420 | `2 Dimmer 00` | 1 | U2 | 356 | 868 |

> ⚠️ The hazer is a **Chauvet Hurricane Haze 2D** (533 W). Its own DMX personality is a fixed
> **2 channels** (blower speed, haze volume) and it is patched as 1. If what is patched is a DP-415
> pack channel this is correct; if it is the hazer's own DMX, haze volume never responds
> (Open Item §9.6). The Haze 2D must **not** be run on a dimmer — see §8.

---

## §5 Fixture Types / Profiles — Real-World Model Status

The showfile carries **generic MA fixture-profile names**, not confirmed manufacturer models. In
August 2026 the venue supplied three fixture manuals (`manuals/`), which identify three of the six
fixture families. Full working in `fixture-identification-audit.md`.

| MA profile | Qty | Ch | Real-world fixture | Modes | Power ea. | Status |
|------------|----:|---:|--------------------|-------|----------:|--------|
| `9 Sharpy Standard Lamp on` | 4 | 14 | **YF BEAM 230** — 189/230 W discharge beam | **16** / 20 | 350–400 W | ❌ **No 14CH mode**; stride is 16. Loses ch15 Reset + ch16 Lamp control — audit §6 |
| `5 NEW WASH` | 8 | 9 | **BETOPPER LM70S** — 7×8 W RGBW mini head | **9** / 14 | 100 W | ✅ **Match** — the only profile that does |
| `6 movingwash zone` | 2 | 9 | **BETOPPER LM70S**, hung inverted | **9** / 14 | 100 W | ✅ Match — pan/tilt-inverted duplicate, not a zoned mode (§5.1) |
| `8 LASER BARS 26CH` | 8 | 26 | **Panda Lighting LS650/LS652** — 6-head laser bar | 11 / 19 / **24** | 150 W | ❌ **No 26CH mode** — audit §5 · ☢️ Class 4 |
| `7 LASER BARS - Invert 26CH` | 1 | 26 | **Panda LS650/LS652**, hung inverted | 11 / 19 / **24** | 150 W | ❌ **No 26CH mode** · ☢️ Class 4 · inverted duplicate (§5.1) |
| `4 rgbw-13ch 13CH` | 7 | 13 | **Light4Me STROBE MULTI BAR** | 4 / **16** / 168 | 200 W | ❌ **No 13CH mode** — audit §4 |
| `3 LED Bar 2 11CH` | 1 | 11 | **Microh LEDBAR RGB** | **13** (fixed) | 50 W | ❌ **No 11CH mode**; segments offset by 2 — audit §7 |
| `2 Dimmer 00` (`-Atmos-`) | 1 | 1 | **Chauvet Hurricane Haze 2D** on a DP-415 channel | **2** (fixed) | 533 W | ❌ **No 1CH mode** · ⚠️ must **not** be dimmed — audit §8 |
| `2 Dimmer 00` (`Co2-HL.HR`) | 2 | 1 | CO₂ jets on DP-415 channels — make unknown | — | ❓ | ❓ Last unidentified device in the rig |

**Distribution:** the three `2 Dimmer 00` entries are **channels on an Elation DP-415** 4-channel
dimmer/switch pack (120 V, 15 A total, 5 A per channel), not DMX fixtures. See §8 and audit §8.

### §5.1 Pan/tilt-inverted duplicate profiles

Two of the eight profiles are duplicates of another, for fixtures hung upside down — reported by
the venue and corroborated against the export (audit §12):

| Inverted profile | Duplicate of | Fixtures | Corroboration |
|------------------|--------------|----------|---------------|
| `6 movingwash zone` | `5 NEW WASH` | M.Wash 7, M.Wash 10 | Identical sub-fixture structure (1 × 9 ch) — *not* a zoned mode, which would have cells |
| `7 LASER BARS - Invert 26CH` | `8 LASER BARS 26CH` | Laser.BAR(6) 1 | Named "Invert"; its six cell addresses run **descending** (215→210) where every other bar ascends |

**Three fixtures are therefore hung inverted:** M.Wash 7, M.Wash 10, Laser.BAR(6) 1. This is the
only orientation information the repo holds — every `AbsolutePosition` is still `0,0,0`.

> ⚠️ **"Clay Paky Sharpy" — the brand is retracted, the class is not.** `9 Sharpy Standard Lamp on`
> is an MA profile *name*. The fixture is a **YF BEAM 230**, confirmed by its manual: a 189 W 5R
> Philips / 230 W 7R Osram discharge beam. A Sharpy's own lamp is a 189 W MSD Platinum 5R, so the
> profile was a sensible pick for a Sharpy-clone. An earlier revision identified the beams as
> BETOPPER LM70S LED mini heads — **that is withdrawn** and now disproven by the manual.

> ❌ **Five of the eight profiles are patched to footprints their fixture cannot be set to** —
> beams 14CH, strobes 13CH, lasers 26CH, DJ bar 11CH, hazer 1CH. Only the moving washes match.
> The patch is internally consistent (no address overlaps), so **do not re-patch** until the
> on-site panel check in `fixture-identification-audit.md` §9 is done.

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

All three effects devices are **mains loads on a single Elation DP-415 4-channel dimmer/switch
pack** (120 V, 15 A total, **5 A per channel**, dual Edison sockets per channel, 9-way dip
address) — confirmed by the venue 2026-08-25. Three of its four channels are used, one spare. The
`2 Dimmer 00` entries in the patch are pack *channels*, not fixtures with their own DMX.

- **CO₂ jets** — `Co2-HL.HR`, one MA fixture multipatched to two physical jets. **Unpatched**
  (address 0). Make, model and wattage unknown — the last gap in the load schedule.
- **Atmospheric haze** — `-Atmos-`, **Chauvet Hurricane Haze 2D**, 533 W / 4.4 A at 120 V. That is
  **88% of its 5 A pack channel**. Its own DMX personality is 2CH; it is patched as 1CH.

> ⚠️ **The Haze 2D must not be run on a dimmer** — its manual states so outright, and the DP-415's
> Dimmer/Switch selection is **pack-wide** (dip switch 10), not per channel. Because the hazer and
> both jets are confirmed on the *same* pack, the hazer cannot be isolated onto a switch-mode pack
> of its own: **dip 10 must read Switch.** Read it before the next show (Open Item §9.8).

---

## §8 Power & Data

> ❓ **No lighting power or DMX-distribution data exists in the showfile.** Per-fixture power now
> comes from the manufacturers instead — everything else is still TBC and must be gathered on-site.

| Item | Status |
|------|--------|
| Per-fixture power draw | ✅ **Manufacturer figures on file** for every fixture except the CO₂ jets |
| Total connected load | 🟡 **5.73–5.93 kW ≈ 48–49 A @ 120 V** — a *subtotal*; only the CO₂ jets are missing. Table in `fixture-identification-audit.md` §11 |
| FX distribution | ✅ **One Elation DP-415** 4-ch pack, 120 V, 15 A total / 5 A per channel — hazer (4.44 A, 89% of its channel) plus both CO₂ jets, 3 of 4 channels used, 1 spare. Confirmed by the venue |
| DP-415 Dimmer vs Switch mode | ⚠️ **Unverified, and it has one correct answer** — the Haze 2D must not be dimmed, the pack's mode is pack-wide (dip 10), and the hazer shares the pack with the jets, so it must read **Switch** |
| Lighting mains feed / breaker(s) | ❓ TBC |
| Power factor / inrush allowance | ❓ TBC — the currents above assume unity PF and are a floor, not a design figure |
| Laser safety class and controls | ☢️ **Class 4** (9 bars × 6 × 500 mW, 638 nm). Compliance items unrecorded — audit §11 |
| DMX node make/model (ArtNet/sACN/DMX) | ❓ TBC |
| DMX node → universe/port mapping | ❓ TBC |
| Data cabling (DMX runs, topology) | ❓ TBC |

---

## §9 Open Items / Data Integrity

Everything not present in the showfile is listed here rather than invented. Consistent with the
repo's treatment of unconfirmed audio items (`❓ Unconfirmed` / "TBC" / "do not patch until
verified"). Resolved items are kept, struck through, so the history of what was believed stays
readable.

### Resolved

1. ~~**Real makes/models behind generic MA profiles**~~ — ✅ *resolved 2026-08-25.* Seven manuals
   identify every fixture: **YF BEAM 230** beams (confirmed by manual), **Panda Lighting
   LS650/LS652** laser bars, **BETOPPER LM70S** washes, **Light4Me STROBE MULTI BAR** strobes,
   **Microh LEDBAR RGB** DJ bar, **Chauvet Hurricane Haze 2D** hazer, distributed via an **Elation
   DP-415** pack. Only the CO₂ jets remain (item 11).

### Patch vs. fixture — five mode mismatches

2. **Beams patched 14CH; the YF BEAM 230 offers 16/20.** Stride is already 16, so nothing collides
   — but ch15 Reset and ch16 **Lamp control** are unreachable: the discharge lamps cannot be
   struck, doused or reset from the console. Load a 16-channel profile on the same addresses
   (audit §6).
3. **Strobe bars patched 13CH; the Light4Me offers 4/16/168.** If the bars are really in 16CH mode
   they overrun their slots and five of them collide with the next bar by 3 channels (audit §4).
   Read the mode off a bar's LCD before changing anything.
4. **Laser bars patched 26CH; the LS650/LS652 offers 11/19/24.** No collision (24 < 26), but 2
   channels per bar are dead and the profile's internal channel order cannot be verified from the
   export (audit §5).
5. **DJ bar patched 11CH; the Microh LEDBAR RGB is a fixed 13CH.** Its three RGB segments match the
   profile's three cells exactly, but the master is 2 channels where the fixture has 4, so the
   whole segment block is offset by two. Nothing collides (audit §7).
6. **Hazer patched 1CH; the Haze 2D personality is a fixed 2CH.** Either the patch is a DP-415 pack
   channel (fine) or it is the hazer's own DMX truncated, in which case haze volume never responds
   (audit §8).

### Safety and power

7. **Laser class 4 — compliance items unrecorded.** Nine bars at 6 × 500 mW / 638 nm. Audience
   reachability cannot be assessed while fixture positions are unknown (item 9). Resolve with the
   venue's safety advisor, not from the desk (audit §11).
8. **DP-415 Dimmer/Switch mode unverified — and there is only one correct setting.** The Haze 2D
   manual states it must not be run on a dimmer; the pack's mode is set pack-wide by dip switch 10;
   and the hazer shares the pack with both CO₂ jets, so it cannot be moved to a pack of its own.
   Dip 10 must read **Switch**. Read it before the next show.
9. **Lighting power/breakers** — per-fixture draw is now known (§8) but the mains feed, breaker
   sizing and power-factor allowance are not. Confirm with the venue electrician.

### Still unknown

10. **Fixture positions unknown** — every `<AbsolutePosition>` in the showfile is `0,0,0`. No
   to-scale **physical plot** can be drawn without a site survey. (A schematic **DMX patch map** —
   address allocation, not geography — is provided at `assets/svg/dmx-patch-map.svg`.) The only
   orientation data the repo holds is the three inverted fixtures in §5.1.
11. **CO₂ jets — make, model and wattage unknown.** Confirmed as two jets on the single DP-415,
   alongside the hazer. They are pack channels, not fixtures needing a patch of their own; the
   long-standing "unpatched at address 0" item was asking the wrong question. What they need is the
   pack's dip-switch address. Their draw is the last gap in the load schedule — bounded by the pack
   at ≤5 A each and ≤10.6 A between them, but unmeasured.
12. **DMX node/output topology** — map U1/U2 to physical nodes/ports.
13. **Strobe-bar address gaps** — confirm intentional spares vs. stale patch (e.g. 370–382 free).
   *Note:* that 13-channel gap is exactly the extra room a 16CH Light4Me bar would need, which may
   be the explanation — see item 3.
14. **Console make/model/location** — confirm grandMA2 hardware and booth position.

### Maintenance

15. **Inverted fixtures carried as duplicate fixture types.** M.Wash 7, M.Wash 10 and
   Laser.BAR(6) 1 are hung upside down and run on duplicate profiles (§5.1). grandMA2 patches pan
   and tilt inversion *per fixture*; using a duplicate fixture *type* instead means those units
   cannot be selected or edited as one type with the rest of their group, and the profile count
   grows with every orientation. Works, but worth revisiting (audit §12).

---

## §10 Source

| Field | Value |
|-------|-------|
| Showfile | `08-lighting/source-showfile/NOMADFIXPATCHJUNE2026.xml` |
| Fixture manuals | `08-lighting/manuals/` (7 supplied 2026-08-25) |
| Manufacturer electrical data | Vendor product pages, relayed by the venue 2026-08-25 |
| Identification audit | `08-lighting/fixture-identification-audit.md` |
| Provenance | `08-lighting/source-showfile/README.md` |
| Console | grandMA2 "Nomad" v3.9.60 |
| Showfile name | `nomad_2026-06-13_kayo-toronto-ft-pools` |
| Exported | 2026-06-24T15:15:38 |

---

*EMBLEM PROJECTS INC. · 2026-06-24*
