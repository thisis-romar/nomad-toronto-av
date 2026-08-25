---
title: NØMAD Toronto — Lighting Vendor Manuals
description: Index of lighting fixture vendor manuals supplied by the venue, with manufacturer electrical data and which MA fixture profile each one is believed to belong to.
version: 3.0.0
created: 2026-06-24T00:00:00Z
last_updated: 2026-08-25T00:00:00Z
---

# Lighting Vendor Manuals

Mirrors `02-equipment-manuals/` for the lighting rig. Three manuals and four sets of manufacturer
electrical specs were supplied by the venue on **2026-08-25**; both are audited against the patch in
`../fixture-identification-audit.md`.

The showfile carries only generic MA profile names, so which fixture belongs to which profile is
**inference from DMX footprint, address stride and naming**, not a statement from the venue.
Confidence is recorded per row rather than smoothed over.

## On file

| Manual | Fixture | DMX modes | Power | Source | MA profile(s) | Confidence |
|--------|---------|-----------|------:|--------|---------------|-----------|
| `panda-lighting-ls650-ls652-6-head-laser-bar.pdf` | Panda Lighting **LS650 / LS652** 6-head laser bar, XY movement | 11 / 19 / **24** CH | 150 W | 6 × 500 mW **638 nm red** — ☢️ **Class 4** | `8 LASER BARS 26CH`, `7 LASER BARS - Invert 26CH` | ✅ Near-certain |
| `light4me-strobe-multi-bar.pdf` | **Light4Me STROBE MULTI BAR** | 4 / **16** / 168 CH | 200 W | 480 × 0.3 W RGB + 240 × 0.3 W CW | `4 rgbw-13ch 13CH` | ⚠️ Likely — **no mode is 13CH** |
| `betopper-lm70s-mini-moving-head.pdf` | **BETOPPER LM70S** (`TLM70SK`/`TLM70SP`) | **9** / 14 CH | 100 W | 7 × 8 W RGBW 4-in-1 LED | `5 NEW WASH`, `6 movingwash zone` | ⚠️ Probable |

## Specs on file, manual missing

| Fixture | DMX modes | Power | Source | MA profile | Confidence |
|---------|-----------|------:|--------|-----------|-----------|
| **YF BEAM 230** moving head | 16 / 20 CH | 350–400 W | 189 W (5R) / 230 W (7R) discharge lamp | `9 Sharpy Standard Lamp on` | ⚠️ Probable — **source the manual** |

> ❌ **Three profiles are patched to a footprint their fixture has no mode for** — strobes 13CH,
> lasers 26CH, beams 14CH. Read `../fixture-identification-audit.md` before re-patching anything.
>
> ☢️ **The laser bars are Class 4.** Nine bars × 6 × 500 mW at 638 nm. See audit §9.

## Still missing

| Category | MA profile | Manual | Power figure |
|----------|-----------|--------|--------------|
| YF BEAM 230 moving head | `9 Sharpy Standard Lamp on` | ❌ Not supplied | ✅ On file |
| DJ-deck LED bar | `3 LED Bar 2 11CH` | ❓ Not supplied | ❓ Unknown |
| CO₂ jets (×2, unpatched) | `2 Dimmer 00` | ❓ Not supplied | ❓ Unknown |
| Atmospheric hazer | `2 Dimmer 00` | ❓ Not supplied | ❓ Unknown — needed to close the load schedule |
| Console | grandMA2 "Nomad" v3.9.60 | ⏳ Reference available from MA Lighting | — |

> When a manual is obtained but cannot be committed (e.g. no download endpoint), follow the repo
> convention and add a `<file>.NOT_DOWNLOADABLE.txt` placeholder (see
> `01-source-documents/nomad-cable-schedule.docx.NOT_DOWNLOADABLE.txt`).

---

*EMBLEM PROJECTS INC. · 2026-08-25*
