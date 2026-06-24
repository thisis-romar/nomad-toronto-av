---
title: Nomad Toronto — System Overview
description: One-page system overview for internal tech pack. Summarises venue, equipment, zones, and quick-reference signal chain.
version: 1.0.0
created: 2026-04-27T00:00:00Z
last_updated: 2026-04-27T00:00:00Z
---

# Nomad Toronto — System Overview

**Venue:** NØMAD Toronto · 725 Queen Street East, Toronto, ON M4M 1H1 · 647-643-8823 · info@nomad725.ca  
**Capacity:** 550 standing  
**System type:** Permanent VOID Acoustics installation  
**Operated by:** In-house production team  
**Prepared by:** Emblem Projects Inc. · admin+claude@emblemprojects.com  
**As-built date:** March 2026 (Armonía-verified) · CQ-12T confirmed April 2026

---

## Venue Summary

Nomad Toronto is a nightclub/bar venue with a permanent professional PA system. The system is designed for DJ-format events (4-deck setup) with full FOH sound reinforcement, DJ booth monitoring, and entrance fill.

---

## Signal Chain (Quick Reference)

```
4× Pioneer CDJ-3000
       │  Pro DJ Link
Pioneer DJM-V10  (DJ mixer)
       │  Master XLR L/R          │  Booth XLR L/R
Allen & Heath CQ-12T  (matrix mixer · FW 1.2.1 · IP 169.254.182.156)
       │  Main LR  0 dB           │  MonOut  −32 dB      │  BakFil  −34 dB
Drawmer SP2120                 Q2 #1                  Athens ×2
(limiter/processor)            (DJ booth)             (entrance, self-pwr)
       │  XLR stereo
Bias V3 #2  "Outside Subs"  [signal hub]
   CH1 → Xair L-3              Line Out 1 → Q5 → Xair ×4 (middle)
   CH2 → Xair R-3              Line Out 2 → Q2 #2 → Air Motion ×2 (bi-amp)
                                Line Out 3 → V3 #1 → Airten V3 ×2
```

---

## Speaker Zones

| Zone | Speakers | Qty | Amplifier |
|------|----------|-----|-----------|
| FOH Mains | VOID Air Motion V2 Red | 2 | Bias Q2 #2 (bi-amp, 4ch) |
| FOH Fill | VOID Airten V3 | 2 | Bias V3 #1 |
| Outside Subs | VOID Stasys Xair (L-3, R-3) | 2 | Bias V3 #2 CH1/CH2 |
| Middle Subs | VOID Stasys Xair (L-1/2, R-1/2) | 4 | Bias Q5 (4ch) |
| DJ Booth Monitors | VOID Air Vantage | 2 | Bias Q2 #1 CH1/CH2 |
| DJ Booth Sub | VOID Venu 215 V2 | 2 | Bias Q2 #1 CH3/CH4 |
| Entrance | Athens TCS-AN (Turbosound) | 2 | Self-powered (CQ-12T BakFil) |
| **Total** | | **18** | 5 active amps |

---

## Amplifier Rack Summary

| U | Device | Role | IP | Status |
|---|--------|------|----|--------|
| 2 | Drawmer SP2120 | Stereo limiter | — | ✅ Active |
| 3 | Bias V3 #1 | Airten fills | 192.168.10.13 | ✅ Active |
| 4 | Bias Q2 #1 | DJ booth | 192.168.10.12 | ✅ Active |
| 5 | Bias V9 | **OFFLINE** | — | ❌ Offline |
| 6 | Bias Q2 #2 | Air Motion bi-amp | 192.168.10.11 | ✅ Active |
| 7 | Bias V3 #2 | Outside subs + hub | 192.168.10.14 | ✅ Active |
| 8 | Bias Q5 | Middle subs | 192.168.10.10 | ✅ Active |

**DSP control:** Armonía Pro Audio Suite · 192.168.10.x network  
**Mixer control:** Allen & Heath MixPad app (iOS/Android) or front panel

---

## DJ Equipment

| Item | Model | Qty |
|------|-------|-----|
| Media player | Pioneer CDJ-3000 | 4 |
| DJ mixer | Pioneer DJM-V10 | 1 |
| Matrix mixer | Allen & Heath CQ-12T | 1 |

**Available inputs:** CH5–CH10 on CQ-12T (unassigned — Mic/Line XLR-TRS combo)  
**Booth monitor feed:** CQ-12T MonOut → Q2 #1 (−32 dB)  
**Entrance fill feed:** CQ-12T BakFil → Athens self-powered (−34 dB)

---

## Key Reference Documents

| Document | Location |
|----------|----------|
| Full system spec (Rev 2.0) | `01-source-documents/nomad-system-spec-v2.md` |
| Cable schedule (41 cables) | `07-tech-pack/cable-schedule.md` |
| Signal flow diagram | `07-tech-pack/signal-flow.svg` |
| Rack elevation | `07-tech-pack/rack-elevation.svg` |
| Speaker zone map | `07-tech-pack/speaker-zone-map.svg` |
| Firmware changelog | `06-reference-docs/firmware-changelog.md` |
| Lighting overview | `07-tech-pack/lighting-system-overview.md` |
| DMX patch schedule | `07-tech-pack/dmx-patch-schedule.md` |

---

## Lighting (Summary)

NØMAD Toronto also runs a **grandMA2-controlled lighting rig** (documented separately from the
audio system). Decoded from the venue showfile (June 2026); physical positions, real fixture
models, DMX-node topology, and power are pending site verification.

| Group | Fixtures | Qty | Universe(s) |
|-------|----------|----:|-------------|
| DJ-deck LED bar | `3 LED Bar 2 11CH` | 1 | U1 |
| LED strobe bars | `4 rgbw-13ch 13CH` | 7 | U1 |
| Moving washes | `5 NEW WASH` / `6 movingwash zone` | 10 | U1 + U2 |
| Moving beams (Sharpy) | `9 Sharpy Standard Lamp on` | 4 | U1 |
| Laser bars | `8 LASER BARS 26CH` / invert | 9 | U1 + U2 |
| CO₂ jets | `2 Dimmer 00` (×2, **unpatched**) | 1 | — |
| Atmospheric haze | `2 Dimmer 00` | 1 | U2 |
| **Total intelligent/LED** | | **31** | 2 universes |

**Full detail:** lighting overview `07-tech-pack/lighting-system-overview.md` · DMX patch schedule
`07-tech-pack/dmx-patch-schedule.md` · spec `08-lighting/nomad-lighting-spec-v1.md`.

---

*EMBLEM PROJECTS INC. · 2026-04-27 · lighting added 2026-06-24*
