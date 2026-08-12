---
title: NØMAD Toronto — Main-Room Equipment Photo Audit
description: Photo-correlated equipment identification for the dance-floor view facing the DJ booth and stage.
version: 1.0.0
created: 2026-08-12T00:00:00-04:00
last_updated: 2026-08-12T00:00:00-04:00
audit_id: main-room-2026-08-12-001
---

# NØMAD Toronto — Main-Room Equipment Photo Audit

**View:** dance-floor centre, facing the DJ booth / stage  
**Source photo:** [`photos/2026-08-12-main-room-source.jpg`](photos/2026-08-12-main-room-source.jpg)  
**Annotated photo:** [`photos/2026-08-12-main-room-equipment-id.jpg`](photos/2026-08-12-main-room-equipment-id.jpg)  
**Machine-readable detections:** [`data/main-room-equipment-audit-2026-08-12.json`](data/main-room-equipment-audit-2026-08-12.json)

This audit cross-correlates visible cabinet morphology and placement with the installed-system inventory already documented in `01-source-documents/nomad-system-spec-v2.md`, `07-tech-pack/system-overview.md`, and the speaker reference assets in `05-speaker-assets/`.

## Identification summary

### Audio — model-level correlation

| ID | Visible equipment | Qty in frame | Role | Confidence | Result |
|---|---|---:|---|---|---|
| A1 | VOID Air Motion V2 Red | 1 | FOH main L | **High** | Photo morphology and location agree with repo inventory. |
| A2 | VOID Air Motion V2 Red | 1 | FOH main R | **High** | Photo morphology and location agree with repo inventory. |
| A3 | VOID Airten V3 | 1 | FOH fill L | **High** | White jet-engine/pod cabinet, mirrored toward room centre. |
| A4 | VOID Airten V3 | 1 | FOH fill R | **High** | White jet-engine/pod cabinet, mirrored toward room centre. |
| A5 | VOID Stasys Xair | 1 | Outside sub L-3 | **High** | Distinctive Xair horn/bracing geometry visible. |
| A6 | VOID Stasys Xair | 4 | Middle subs L-1/L-2/R-1/R-2 | **High** | Four cabinets visibly form the centre 2×2 cluster. |
| A7 | VOID Stasys Xair | 1 | Outside sub R-3 | **High** | Distinctive Xair horn/bracing geometry visible. |

**Important:** this single frame therefore visually accounts for the repo's complete **6× Stasys Xair subwoofer inventory** and both pairs of audience-facing VOID tops/fills: **2× Air Motion V2 + 2× Airten V3**.

### DJ surface — inventory supported, not photo-confirmed

The booth surface is visible, but the image does not resolve faceplates, screens, or device count cleanly enough to assert model-level visual identification. The current repo inventory remains:

- 4× Pioneer / AlphaTheta CDJ-3000
- 1× Pioneer DJM-V10

Treat these as **inventory-confirmed, photo-unresolved** in this frame.

### Lighting — physical presence observed, exact FID/model still open

| ID | Observation | Confidence | What the photo establishes | What remains TBC |
|---|---|---|---|---|
| L1 | Stage-left narrow green multi-beam output | Medium | An active laser/beam-class source exists at this physical region. | Whether it is one of the 9 laser bars or a Sharpy-profile moving beam; exact FID/model. |
| L2 | Stage-right narrow green multi-beam output | Medium | Symmetric active laser/beam-class source exists at this region. | Same unresolved mapping as L1. |
| L3 | Linear ceiling emitter — left | Medium | A physical linear LED/strobe-class fixture is present. | Exact MA profile/FID/manufacturer/model. |
| L4 | Linear ceiling emitter — centre | Medium | A physical linear LED/strobe-class fixture is present. | Exact MA profile/FID/manufacturer/model. |
| L5 | Linear ceiling emitter — right | Medium | A physical linear LED/strobe-class fixture is present. | Exact MA profile/FID/manufacturer/model. |

The June 2026 showfile contains 7 RGBW strobe bars, 1 DJ-deck LED bar, 9 laser bars, 4 Sharpy-profile moving beams, and 10 moving washes. This photograph **reduces the physical-position unknowns** but does **not** justify mapping the visible fixtures to specific showfile FIDs.

## Equipment not resolved in this view

The following repo inventory is either hidden, outside the camera field, or visually ambiguous:

- 2× VOID Air Vantage DJ booth monitors
- 2× VOID Venu 215 V2 DJ booth subs
- 2× Turbosound Athens TCS-AN entrance speakers
- Allen & Heath CQ-12T matrix mixer
- Drawmer SP2120 limiter
- Bias amplifier rack
- lighting fixture rear labels / manufacturer-model markings
- exact grandMA2 FID-to-physical-position mapping

## Evidence standard

A photo audit may elevate an item to **High** only when visible geometry/finish/placement agree with an already documented installed model. It must **not** infer serial numbers, wiring, amplifier channels, DMX addresses, firmware, or hidden equipment from appearance alone.

For lighting, a visible effect or chassis shape may establish **class and approximate physical position**, but the FID remains TBC until one of the following is captured:

1. rear/side fixture label;
2. controlled single-fixture identify test from grandMA2;
3. DMX unplug/flash isolation;
4. unique physical geometry matched to a manufacturer manual.

## Next site capture

For the next pass, shoot:

- straight-on wide frame with lighting at work-light level;
- ceiling-only panorama with all fixtures off;
- one close-up per fixture family, including rear label and DMX/power connectors;
- booth rear / monitor view for Air Vantage and Venu 215 V2;
- DJ surface overhead for explicit CDJ/DJM visual confirmation;
- rack front/rear to close existing amplifier-rack evidence gaps.

---

*EMBLEM PROJECTS INC. · 2026-08-12*
