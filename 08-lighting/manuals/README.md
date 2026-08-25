---
title: NØMAD Toronto — Lighting Vendor Manuals
description: Index of the seven lighting manuals supplied by the venue, with manufacturer electrical data and the MA fixture profile each one belongs to.
version: 4.1.0
created: 2026-06-24T00:00:00Z
last_updated: 2026-08-25T00:00:00Z
---

# Lighting Vendor Manuals

Mirrors `02-equipment-manuals/` for the lighting rig. Seven manuals were supplied by the venue on
**2026-08-25** in three batches, together with manufacturer electrical data. Every MA profile in the
rig now has a fixture behind it; all of it is audited against the patch in
`../fixture-identification-audit.md`.

The showfile carries only generic MA profile names, so which fixture belongs to which profile is
**inference from DMX footprint, address stride, sub-fixture structure and naming**, except where a
manual settles it outright. Confidence is recorded per row rather than smoothed over.

## Lighting fixtures

| Manual | Fixture | DMX modes | Power | Light source | MA profile(s) | Confidence |
|--------|---------|-----------|------:|--------------|---------------|-----------|
| `yf-beam-230-moving-head.pdf` | **YF BEAM 230** moving head (Guangzhou Yingfeng) | **16** / 20 CH | 350–400 W | 189 W 5R Philips / 230 W 7R Osram discharge | `9 Sharpy Standard Lamp on` | ✅ **Confirmed** — patched 14CH, see audit §6 |
| `panda-lighting-ls650-ls652-6-head-laser-bar.pdf` | Panda Lighting **LS650 / LS652** 6-head laser bar, XY movement | 11 / 19 / **24** CH | 150 W | 6 × 500 mW **638 nm red** — ☢️ **Class 4** | `8 LASER BARS 26CH`, `7 LASER BARS - Invert 26CH` | ✅ Near-certain — patched 26CH |
| `light4me-strobe-multi-bar.pdf` | **Light4Me STROBE MULTI BAR** | 4 / **16** / 168 CH | 200 W | 480 × 0.3 W RGB + 240 × 0.3 W CW | `4 rgbw-13ch 13CH` | ⚠️ Likely — patched 13CH, **no such mode** |
| `betopper-lm70s-mini-moving-head.pdf` | **BETOPPER LM70S** (`TLM70SK`/`TLM70SP`) | **9** / 14 CH | 100 W | 7 × 8 W RGBW 4-in-1 LED | `5 NEW WASH`, `6 movingwash zone` | ⚠️ Probable — **the only profile that matches** |
| `microh-ledbar-rgb.pdf` | **Microh LEDBAR RGB** | **13 CH** (fixed) | 50 W | 252 × 10 mm LED (108 R / 72 G / 72 B), 107 cm | `3 LED Bar 2 11CH` | ⚠️ Likely — patched 11CH, see audit §7 |
| `chauvet-hurricane-haze-2d.pdf` | **Chauvet Hurricane Haze 2D** | **2 CH** (fixed) | 533 W / 4.4 A @ 120 V | water-based hazer | `2 Dimmer 00` (`-Atmos-`) | ⚠️ Likely — ⚠️ **"Use on dimmer: no"** |

## Distribution

| Manual | Device | Spec | What it drives |
|--------|--------|------|----------------|
| `elation-dp-415-dimmer-switch-pack.pdf` | **Elation DP-415** 4-channel dimmer/switch pack — **×1** | 120 V 60 Hz, **15 A total, 5 A per channel**, dual Edison per channel, 9-way dip address, **dip 10 selects Dimmer or Switch for the whole pack** | The three `2 Dimmer 00` entries — **CO₂ jets ×2 and the hazer, all on this one pack** (3 of 4 channels, 1 spare; confirmed by the venue) — are **pack channels, not DMX fixtures** |

> ❌ **Five of the eight profiles are patched to a footprint their fixture has no mode for** —
> beams 14CH, strobes 13CH, lasers 26CH, DJ bar 11CH, hazer 1CH. Only the moving washes match.
> Read `../fixture-identification-audit.md` before re-patching anything.
>
> ⚠️ **Check DP-415 dip switch 10 — it must read Switch.** The Haze 2D must not be run on a
> dimmer, the pack's mode is pack-wide, and the hazer shares the pack with both CO₂ jets, so it
> cannot be isolated onto a pack of its own.
>
> ☢️ **The laser bars are Class 4.** Nine bars × 6 × 500 mW at 638 nm. See audit §11.

## Still missing

| Category | MA profile | Manual | Power figure |
|----------|-----------|--------|--------------|
| CO₂ jets (×2, on DP-415 channels) | `2 Dimmer 00` | ❓ Not supplied | ❓ Unknown — the last gap in the load schedule. Bounded by the pack at ≤5 A each |
| Console | grandMA2 "Nomad" v3.9.60 | ⏳ Reference available from MA Lighting | — |

> When a manual is obtained but cannot be committed (e.g. no download endpoint), follow the repo
> convention and add a `<file>.NOT_DOWNLOADABLE.txt` placeholder (see
> `01-source-documents/nomad-cable-schedule.docx.NOT_DOWNLOADABLE.txt`).

---

*EMBLEM PROJECTS INC. · 2026-08-25*
