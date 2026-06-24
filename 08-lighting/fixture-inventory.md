---
title: NØMAD Toronto — Lighting Fixture Inventory
description: Fixture counts and per-fixture ID list for the venue lighting rig, decoded from the grandMA2 showfile. Companion to the full spec and DMX patch schedule.
version: 1.0.0
created: 2026-06-24T00:00:00Z
last_updated: 2026-06-24T00:00:00Z
---

# NØMAD Toronto — Lighting Fixture Inventory

Counts and fixture IDs decoded from `08-lighting/source-showfile/NOMADFIXPATCHJUNE2026.xml`.
Per-fixture DMX addresses are in `07-tech-pack/dmx-patch-schedule.md`; full detail and the
profile→real-model status table are in `nomad-lighting-spec-v1.md`.

## Counts by type

| MA profile | Presumed type | Qty | Ch (footprint) | Universe(s) |
|------------|---------------|----:|---------------:|-------------|
| `3 LED Bar 2 11CH` | DJ-deck LED bar | 1 | 11 | U1 |
| `4 rgbw-13ch 13CH` | LED strobe bar | 7 | 13 | U1 |
| `5 NEW WASH` | Moving wash | 8 | 9 | U1 + U2 |
| `6 movingwash zone` | Moving wash (zoned) | 2 | 9 | U1 + U2 |
| `9 Sharpy Standard Lamp on` | Moving beam (Clay Paky Sharpy — confirm) | 4 | 14 | U1 |
| `8 LASER BARS 26CH` | Laser bar | 8 | 26 | U1 + U2 |
| `7 LASER BARS - Invert 26CH` | Laser bar (inverted patch) | 1 | 26 | U1 |
| `2 Dimmer 00` | CO₂ jet (×2 multipatch, **unpatched**) | 1 | 1 | — |
| `2 Dimmer 00` | Atmospheric hazer | 1 | 1 | U2 |
| **Total** | | **33** | | 2 universes |

**Intelligent/LED fixtures:** 31 · **Effects:** 2 CO₂ jets (1 multipatched fixture) + 1 hazer.

## Fixture IDs

| Group | Fixtures (FID) |
|-------|----------------|
| DJ-deck LED | DJ-LED (1) |
| LED strobe bars | LED.Strobe-BAR 1 (801) … 7 (807) |
| Moving washes | M.Wash 1 (101) … 10 (110) |
| Moving beams | M.BEAM 1 (401), 2 (402), 3 (403), 4 (404) |
| Laser bars | Laser.BAR(6) 1 (1001) … 9 (1009) |
| CO₂ jets | Co2-HL.HR (911) — multipatched ×2 |
| Atmospheric | -Atmos- (420) |

## Visual

Schematic DMX patch map (address allocation per universe, not a physical plot):
`08-lighting/assets/svg/dmx-patch-map.svg` — regenerate with
`python3 scripts/build-lighting-patch-map.py`.

> A to-scale physical lighting **plot** is not provided: all fixture positions in the showfile are
> `0,0,0`. Survey required (see spec §9.2).

---

*EMBLEM PROJECTS INC. · 2026-06-24*
