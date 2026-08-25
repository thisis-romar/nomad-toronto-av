---
title: NØMAD Toronto — DMX Patch Schedule
description: Complete DMX patch schedule for the NØMAD Toronto grandMA2 lighting rig, decoded from the venue showfile (2026-06-13, exported 2026-06-24). The lighting analog of the audio cable schedule.
version: 1.2.0
created: 2026-06-24T00:00:00Z
last_updated: 2026-08-25T00:00:00Z
---

# NØMAD Toronto — DMX Patch Schedule

**Venue:** NØMAD Toronto
**System:** grandMA2 lighting rig — 31 intelligent/LED fixtures + CO₂ + haze, 2 DMX universes
**Status:** Decoded from showfile `nomad_2026-06-13_kayo-toronto-ft-pools` (exported 2026-06-24)
**Source docs:** `08-lighting/source-showfile/NOMADFIXPATCHJUNE2026.xml` · spec `08-lighting/nomad-lighting-spec-v1.md`

> **Address convention:** the showfile uses **absolute** DMX addresses (U1 = 1–512, U2 = 513–1024).
> This schedule lists **universe-relative** Start/End (1–512) with the raw **absolute** address in
> parentheses. End = Start + channel-count − 1.
>
> **Ch = DMX footprint** per the MA fixture-profile mode (the `…CH` in the profile name), which is
> what the patch occupies. This is confirmed by the address spacing between consecutive fixtures
> (strobes 13, washes 9, lasers 26, beams 14). Note the per-sub-fixture `<Channel>` elements in the
> raw XML sum to fewer than the footprint (virtual/container channels) — they are **not** the patch
> footprint and are not used here.

---

## Section 1 — LED · DJ-Decks

MA layer `--LED.DJ-Decks`.

| # | Fixture | Group/Layer | MA Profile | Ch | Universe | Start | End | Cells | Notes |
|---|---------|-------------|------------|---:|----------|-------|-----|------:|-------|
| 1 | DJ-LED | LED.DJ-Decks | `3 LED Bar 2 11CH` | 11 | U1 | 11 (11) | 21 (21) | 4 | DJ-deck LED bar; 4 sub-cells |

---

## Section 2 — LED · Strobe Bars

MA layer `--LED.STROBE-BAR`. All `4 rgbw-13ch 13CH`, 13 ch, Universe 1.

> ❌ **Mode mismatch — do not re-patch on this alone.** These are believed to be **Light4Me STROBE
> MULTI BAR**, which offers 4CH / 16CH / 168CH. There is no 13CH mode. If they are running 16CH,
> five of the seven overrun their slot and collide with the next bar by 3 channels. Read the mode
> off a bar's LCD first — `08-lighting/fixture-identification-audit.md` §4.

| # | Fixture | Group/Layer | MA Profile | Ch | Universe | Start | End | Cells | Notes |
|---|---------|-------------|------------|---:|----------|-------|-----|------:|-------|
| 2 | LED.Strobe-BAR 1 | LED.STROBE-BAR | `4 rgbw-13ch 13CH` | 13 | U1 | 448 (448) | 460 (460) | — | FID 801 |
| 3 | LED.Strobe-BAR 2 | LED.STROBE-BAR | `4 rgbw-13ch 13CH` | 13 | U1 | 435 (435) | 447 (447) | — | FID 802 |
| 4 | LED.Strobe-BAR 3 | LED.STROBE-BAR | `4 rgbw-13ch 13CH` | 13 | U1 | 422 (422) | 434 (434) | — | FID 803 |
| 5 | LED.Strobe-BAR 4 | LED.STROBE-BAR | `4 rgbw-13ch 13CH` | 13 | U1 | 409 (409) | 421 (421) | — | FID 804 |
| 6 | LED.Strobe-BAR 5 | LED.STROBE-BAR | `4 rgbw-13ch 13CH` | 13 | U1 | 396 (396) | 408 (408) | — | FID 805 |
| 7 | LED.Strobe-BAR 6 | LED.STROBE-BAR | `4 rgbw-13ch 13CH` | 13 | U1 | 383 (383) | 395 (395) | — | FID 806 |
| 8 | LED.Strobe-BAR 7 | LED.STROBE-BAR | `4 rgbw-13ch 13CH` | 13 | U1 | 357 (357) | 369 (369) | — | FID 807 |

> ⚠️ Address gap 370–382 between BAR 7 (ends 369) and BAR 6 (starts 383). Confirm intentional spare room vs. stale patch.

---

## Section 3 — Moving Washes

MA layer `--M.WASH`. All 9 ch. Two profiles mixed: `5 NEW WASH` (×8) and `6 movingwash zone` (×2).

> ✅ Believed to be **BETOPPER LM70S** (100 W, 7×8 W RGBW) in its 9CH mode — footprint and address
> stride both 9, no conflict.

| # | Fixture | Group/Layer | MA Profile | Ch | Universe | Start | End | Cells | Notes |
|---|---------|-------------|------------|---:|----------|-------|-----|------:|-------|
| 9  | M.Wash 1  | M.WASH | `5 NEW WASH` | 9 | U1 | 498 (498) | 506 (506) | — | FID 101 |
| 10 | M.Wash 2  | M.WASH | `5 NEW WASH` | 9 | U1 | 469 (469) | 477 (477) | — | FID 102 |
| 11 | M.Wash 3  | M.WASH | `5 NEW WASH` | 9 | U1 | 244 (244) | 252 (252) | — | FID 103 |
| 12 | M.Wash 4  | M.WASH | `5 NEW WASH` | 9 | U1 | 235 (235) | 243 (243) | — | FID 104 |
| 13 | M.Wash 5  | M.WASH | `5 NEW WASH` | 9 | U1 | 271 (271) | 279 (279) | — | FID 105 |
| 14 | M.Wash 6  | M.WASH | `5 NEW WASH` | 9 | U1 | 489 (489) | 497 (497) | — | FID 106 |
| 15 | M.Wash 7  | M.WASH | `6 movingwash zone` | 9 | U1 | 262 (262) | 270 (270) | — | FID 107; zoned profile |
| 16 | M.Wash 8  | M.WASH | `5 NEW WASH` | 9 | U1 | 253 (253) | 261 (261) | — | FID 108 |
| 17 | M.Wash 9  | M.WASH | `5 NEW WASH` | 9 | U2 | 210 (722) | 218 (730) | — | FID 109; on Universe 2 |
| 18 | M.Wash 10 | M.WASH | `6 movingwash zone` | 9 | U2 | 200 (712) | 208 (720) | — | FID 110; zoned profile, Universe 2 |

---

## Section 4 — Moving Beams

MA layer `--M.Beam`. All `9 Sharpy Standard Lamp on`, 14 ch, Universe 1.

> ❌ **Mode mismatch — and the stride gives it away.** These four are patched on a uniform
> **16-channel stride** (280, 296, 312, 328) while the profile loaded against them is 14 channels.
> They are probably **YF BEAM 230** (189/230 W discharge), which offers 16CH and 20CH — so the
> spacing is right for the fixture and the profile is 2 channels short. Nothing collides; the last
> two channels of each beam are simply unreachable from the console. Load a 16-channel profile on
> the same addresses. `08-lighting/fixture-identification-audit.md` §6.
>
> The profile name is an MA label, not a model. Not a Clay Paky *Sharpy* — but a Sharpy-class
> discharge beam, which is what the profile was presumably chosen for.

| # | Fixture | Group/Layer | MA Profile | Ch | Universe | Start | End | Cells | Notes |
|---|---------|-------------|------------|---:|----------|-------|-----|------:|-------|
| 19 | M.BEAM 1 | M.Beam | `9 Sharpy Standard Lamp on` | 14 | U1 | 312 (312) | 325 (325) | — | FID 401 |
| 20 | M.BEAM 2 | M.Beam | `9 Sharpy Standard Lamp on` | 14 | U1 | 280 (280) | 293 (293) | — | FID 402 |
| 21 | M.BEAM 3 | M.Beam | `9 Sharpy Standard Lamp on` | 14 | U1 | 296 (296) | 309 (309) | — | FID 403 |
| 22 | M.BEAM 4 | M.Beam | `9 Sharpy Standard Lamp on` | 14 | U1 | 328 (328) | 341 (341) | — | FID 404 |

---

## Section 5 — Laser Bars

MA layer `--M.Laser-BAR`. All 26 ch, 7 sub-cells. Bars 2–9 use `8 LASER BARS 26CH`; bar 1 uses the inverted profile.

> ⚠️ **Mode mismatch, benign as patched.** These are the **Panda Lighting LS650/LS652** 6-head
> laser bar, which offers 11CH / 19CH / 24CH. There is no 26CH mode. Because 24 < 26 nothing
> collides — each bar just leaves 2 dead channels — but the profile's internal channel order cannot
> be verified from the showfile. `08-lighting/fixture-identification-audit.md` §5.
>
> ☢️ **Class 4.** 6 × 500 mW at 638 nm per bar, nine bars. See audit §9 before scheduling a show.

| # | Fixture | Group/Layer | MA Profile | Ch | Universe | Start | End | Cells | Notes |
|---|---------|-------------|------------|---:|----------|-------|-----|------:|-------|
| 23 | Laser.BAR(6) 1 | M.Laser-BAR | `7 LASER BARS - Invert 26CH` | 26 | U1 | 209 (209) | 234 (234) | 7 | FID 1001; inverted sub-cell order (cells 1–7 = abs 209–215) |
| 24 | Laser.BAR(6) 2 | M.Laser-BAR | `8 LASER BARS 26CH` | 26 | U1 | 183 (183) | 208 (208) | 7 | FID 1002 |
| 25 | Laser.BAR(6) 3 | M.Laser-BAR | `8 LASER BARS 26CH` | 26 | U1 | 157 (157) | 182 (182) | 7 | FID 1003 |
| 26 | Laser.BAR(6) 4 | M.Laser-BAR | `8 LASER BARS 26CH` | 26 | U1 | 131 (131) | 156 (156) | 7 | FID 1004 |
| 27 | Laser.BAR(6) 5 | M.Laser-BAR | `8 LASER BARS 26CH` | 26 | U1 | 105 (105) | 130 (130) | 7 | FID 1005 |
| 28 | Laser.BAR(6) 6 | M.Laser-BAR | `8 LASER BARS 26CH` | 26 | U1 | 79 (79) | 104 (104) | 7 | FID 1006 |
| 29 | Laser.BAR(6) 7 | M.Laser-BAR | `8 LASER BARS 26CH` | 26 | U1 | 53 (53) | 78 (78) | 7 | FID 1007 |
| 30 | Laser.BAR(6) 8 | M.Laser-BAR | `8 LASER BARS 26CH` | 26 | U1 | 27 (27) | 52 (52) | 7 | FID 1008 |
| 31 | Laser.BAR(6) 9 | M.Laser-BAR | `8 LASER BARS 26CH` | 26 | U2 | 1 (513) | 26 (538) | 7 | FID 1009; alone on Universe 2 |

---

## Section 6 — Effects (CO₂ & Haze)

MA layers `--Co2(2x)` and `~Atmos~`. All `2 Dimmer 00`, 1 ch.

| # | Fixture | Group/Layer | MA Profile | Ch | Universe | Start | End | Cells | Notes |
|---|---------|-------------|------------|---:|----------|-------|-----|------:|-------|
| 32 | Co2-HL.HR | Co2(2x) | `2 Dimmer 00` | 1 | — | **0** | **0** | — | FID 911; **UNPATCHED**, multipatched ×2 jets |
| 33 | -Atmos- | ~Atmos~ | `2 Dimmer 00` | 1 | U2 | 356 (868) | 356 (868) | — | FID 420; atmospheric hazer |

> ⚠️ **CO₂ jets are UNPATCHED (address 0).** Do not assume an address — patch and verify on-site.

---

## Summary

### Fixtures by profile

| MA profile | Qty | Ch each |
|------------|----:|--------:|
| `3 LED Bar 2 11CH` | 1 | 11 |
| `4 rgbw-13ch 13CH` | 7 | 13 |
| `5 NEW WASH` | 8 | 9 |
| `6 movingwash zone` | 2 | 9 |
| `9 Sharpy Standard Lamp on` | 4 | 14 |
| `8 LASER BARS 26CH` | 8 | 26 |
| `7 LASER BARS - Invert 26CH` | 1 | 26 |
| `2 Dimmer 00` (CO₂ ×1 / haze ×1) | 2 | 1 |
| **Total fixtures (patched + unpatched)** | **33** | — |

### Channels by universe

| Universe | Patched fixtures | Channels used |
|----------|-----------------:|--------------:|
| Universe 1 | 28 | 438 |
| Universe 2 | 4 (M.Wash 9, M.Wash 10, Laser.BAR 9, Atmos) | 45 |
| Unpatched | 1 (CO₂, address 0) | — |

---

## Open Items

- [ ] **CO₂ jets unpatched** — patch + verify on-site (address 0 in showfile).
- [ ] **Fixture positions** — all `0,0,0` in showfile; survey before producing a lighting plot.
- [ ] **Real fixture models** — confirm makes behind generic MA profiles (see spec §5).
- [ ] **DMX node/output topology** — map U1/U2 to physical nodes/ports.
- [ ] **Strobe-bar address gaps** — confirm spares vs. stale patch.

---

*Updated 2026-06-24 · Decoded from grandMA2 showfile · EMBLEM PROJECTS INC.*
