---
title: NØMAD Toronto — Lighting System Overview
description: One-page lighting overview for the internal tech pack. Summarises the grandMA2 rig, DMX universes, fixture groups, and quick-reference data — decoded from the venue showfile.
version: 1.0.0
created: 2026-06-24T00:00:00Z
last_updated: 2026-06-24T00:00:00Z
---

# NØMAD Toronto — Lighting System Overview

**Venue:** NØMAD Toronto · 725 Queen Street East, Toronto, ON M4M 1H1 · 647-643-8823 · info@nomad725.ca
**System type:** grandMA2-controlled intelligent lighting rig
**Operated by:** In-house production team / house LD
**Prepared by:** Emblem Projects Inc. · admin+claude@emblemprojects.com
**Source:** showfile `nomad_2026-06-13_kayo-toronto-ft-pools` (grandMA2 "Nomad" v3.9.60, exported 2026-06-24)

> Desktop decode from the venue showfile. Physical positions, real fixture models, DMX node
> topology, and power are **not** in the showfile — flagged TBC here and in the full spec.

---

## Rig Summary

| Group | Fixtures | Qty | Universe(s) |
|-------|----------|----:|-------------|
| DJ-deck LED bar | `3 LED Bar 2 11CH` | 1 | U1 |
| LED strobe bars | `4 rgbw-13ch 13CH` | 7 | U1 |
| Moving washes | `5 NEW WASH` ×8 · `6 movingwash zone` ×2 | 10 | U1 + U2 |
| Moving beams (Sharpy) | `9 Sharpy Standard Lamp on` | 4 | U1 |
| Laser bars | `8 LASER BARS 26CH` ×8 · `7 LASER BARS - Invert 26CH` ×1 | 9 | U1 + U2 |
| CO₂ jets | `2 Dimmer 00` (multipatch ×2) | 1 | **unpatched** |
| Atmospheric haze | `2 Dimmer 00` | 1 | U2 |
| **Total intelligent/LED** | | **31** | 2 universes |

---

## DMX Universe Map (Quick Reference)

```
grandMA2 "Nomad" v3.9.60
   │
   ├── Universe 1 (abs 1–512) ── ~438 ch
   │     DJ-LED · Strobe 1–7 · M.Wash 1–8 · M.Beam 1–4 · Laser.BAR 1–8
   │
   └── Universe 2 (abs 513–1024) ── ~45 ch
         M.Wash 9 · M.Wash 10 · Laser.BAR 9 · Atmos hazer

   CO₂ jets (Co2-HL.HR ×2) — UNPATCHED (address 0)
```

Addresses in the showfile are absolute; the patch schedule lists universe-relative addresses with
the absolute in parentheses.

---

## DMX Data & Power

> ❓ None of the following is present in the showfile. All TBC pending site survey.

| Item | Status |
|------|--------|
| DMX node make/model (ArtNet/sACN/DMX) | ❓ TBC |
| DMX node → universe/port mapping | ❓ TBC |
| Lighting mains feed / breakers | ❓ TBC |
| Per-fixture / total power draw | ❓ TBC |
| Fixture physical positions | ❓ TBC — all `0,0,0` in showfile |
| Real-world fixture makes/models | ❓ TBC — only generic MA profiles present |

---

## Key Reference Documents

| Document | Location |
|----------|----------|
| Lighting system spec (Rev 1.0) | `08-lighting/nomad-lighting-spec-v1.md` |
| DMX patch schedule (33 entries) | `07-tech-pack/dmx-patch-schedule.md` |
| Fixture inventory | `08-lighting/fixture-inventory.md` |
| DMX patch map (SVG, schematic) | `08-lighting/assets/svg/dmx-patch-map.svg` |
| Source showfile + provenance | `08-lighting/source-showfile/` |
| Architecture decision (subsystem) | `docs/decisions/ADR-0001-lighting-subsystem.md` |

---

*EMBLEM PROJECTS INC. · 2026-06-24*
