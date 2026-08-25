---
title: NØMAD Toronto — Lighting Vendor Manuals
description: Index of lighting fixture vendor manuals supplied by the venue, and which MA fixture profile each one is believed to belong to.
version: 2.0.0
created: 2026-06-24T00:00:00Z
last_updated: 2026-08-25T00:00:00Z
---

# Lighting Vendor Manuals

Mirrors `02-equipment-manuals/` for the lighting rig. Three manuals were supplied by the venue on
**2026-08-25**; they are audited against the patch in `../fixture-identification-audit.md`.

The showfile carries only generic MA profile names, so which manual belongs to which profile is
**inference from DMX footprint and naming**, not a statement from the venue. Confidence is recorded
per row rather than smoothed over.

## On file

| Manual | Fixture | DMX modes | MA profile(s) | Confidence |
|--------|---------|-----------|---------------|-----------|
| `ls650-six-eye-swing-laser.pdf` | LS650 six-eye swing laser (OEM, unbranded) | 11 / 19 / **24** CH | `8 LASER BARS 26CH`, `7 LASER BARS - Invert 26CH` | ✅ Near-certain — six eyes matches `Laser.BAR(6)` and its six cells |
| `betopper-lm70s-mini-moving-head.pdf` | BETOPPER LM70S (`TLM70SK`/`TLM70SP`), 7×8 W RGBW, 100 W | **9** / **14** CH | `5 NEW WASH`, `6 movingwash zone`, `9 Sharpy Standard Lamp on` | ⚠️ Probable — its two modes are exactly the two moving-head footprints in the patch |
| `light4me-strobe-multi-bar.pdf` | Light4Me STROBE MULTI BAR | 4 / 16 / 168 CH | `4 rgbw-13ch 13CH` | ⚠️ Likely — but **no mode is 13CH**; see audit §4 |

> ⚠️ **Two of the three are patched to a footprint their fixture has no mode for** — lasers 26CH,
> strobes 13CH. Read `../fixture-identification-audit.md` before re-patching anything.

## Still missing

| Category | MA profile | Manual status |
|----------|-----------|---------------|
| DJ-deck LED bar | `3 LED Bar 2 11CH` | ❓ Not supplied — make/model unknown |
| CO₂ jets (×2, unpatched) | `2 Dimmer 00` | ❓ Not supplied — make/model and trigger wiring unknown |
| Atmospheric hazer | `2 Dimmer 00` | ❓ Not supplied — make/model unknown |
| Console | grandMA2 "Nomad" v3.9.60 | ⏳ Reference available from MA Lighting |

> When a manual is obtained but cannot be committed (e.g. no download endpoint), follow the repo
> convention and add a `<file>.NOT_DOWNLOADABLE.txt` placeholder (see
> `01-source-documents/nomad-cable-schedule.docx.NOT_DOWNLOADABLE.txt`).

---

*EMBLEM PROJECTS INC. · 2026-08-25*
