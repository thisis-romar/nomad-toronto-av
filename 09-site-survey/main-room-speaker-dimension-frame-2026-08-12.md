---
title: NØMAD Toronto — Main-Room Speaker Dimension Frame
description: Speaker-only photo framing pass using documented VOID enclosure dimensions as aspect-ratio constraints.
version: 1.0.0
created: 2026-08-12T00:00:00-04:00
---

# NØMAD Toronto — Main-Room Speaker Dimension Frame

This pass deliberately removes DJ and lighting annotations and starts with only the ten audience-facing speaker cabinets visible in the main-room photograph.

## Repository dimension extraction

Dimensions below are interpreted as **W × H × D** from the repository's equipment manuals / extracted graph metadata.

| Family | Qty visible | W | H | D | Front envelope | Side envelope | Repo source |
|---|---:|---:|---:|---:|---|---|---|
| VOID Air Motion V2 | 2 | 854 mm | 672 mm | 658 mm | 854 × 672 mm | 658 × 672 mm | `02-equipment-manuals/speakers/VOID-Air-Motion-V2-User-Guide.pdf` p.7–8 |
| VOID Airten V3 | 2 | 681 mm | 303 mm | 366 mm | 681 × 303 mm | 366 × 303 mm | `02-equipment-manuals/speakers/VOID-Airten-V3-User-Manual-v2.1.pdf` p.8 |
| VOID Stasys Xair | 6 | 1226 mm | 562 mm | 903 mm | 1226 × 562 mm | 903 × 562 mm | `02-equipment-manuals/speakers/VOID-Stasys-Xair-User-Guide.pdf` p.7 |

## Framing rule

The source photograph is perspective-distorted, so these dimensions do **not** establish a single global `mm/px` scale. In this pass they are used only as physical-envelope/aspect-ratio constraints:

- Air Motion frame ratio = `854 / 672 = 1.2708`.
- Airten frame ratio = `681 / 303 = 2.2475`.
- Horizontal Xair frame ratio = `1226 / 562 = 2.1815`.
- The two outside Xair cabinets are installed on end, so their image-space frame uses the front envelope rotated 90°: `562 / 1226 = 0.4584`.

The four centre Xairs are split into four individual frames rather than one cluster frame. This is required before any later perspective solve because each cabinet becomes an independent physical reference rectangle.

## Deliverables

- `data/main-room-speaker-dimension-frame-2026-08-12.json` — physical dimensions plus native-pixel reference frames.
- `overlays/main-room-speaker-dimension-frame-2026-08-12.svg` — source-aligned speaker-only dimensional overlay.

## Next calibration gate

Before using the speakers to infer room dimensions, solve a perspective model rather than converting pixels directly to millimetres. The preferred next step is to use the four centre Xair front faces as repeated coplanar rectangles of known `1226 × 562 mm` size, estimate the booth-front homography/vanishing geometry, and then validate the result against the left/right Air Motion and Airten pairs.

---

*EMBLEM PROJECTS INC. · 2026-08-12*
