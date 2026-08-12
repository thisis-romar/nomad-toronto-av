---
title: NØMAD Toronto — Visual Audit & Refactor Loop
description: Repeatable human-in-the-loop geometry review for photo-correlated AV equipment evidence.
version: 1.0.0
created: 2026-08-12T04:22:00-04:00
last_updated: 2026-08-12T04:22:00-04:00
---

# NØMAD Toronto — Visual Audit & Refactor Loop

## North star

A photo annotation is accepted only when the **native source image, evidence manifest, overlay and rendered review plate remain in the same coordinate system** and the visible geometry supports the claim being made.

The 2026-08-12 main-room audit exposed the failure mode this loop is designed to catch: the equipment IDs were broadly correct, but several bounding boxes were visibly displaced or oversized and callout labels obscured the scene. The data could therefore be semantically right while the visual evidence layer was geometrically wrong.

## Hard invariant

`bbox_px` is expressed in **native source-image pixels**.

Do not resize, crop, rotate, perspective-correct or otherwise transform the source before applying `bbox_px`. If a derivative image is needed for display, render the annotations on the native source first and transform the complete composite afterward.

`bbox_norm` is derived from accepted `bbox_px`; it is never the authoritative geometry.

## Six-pass review loop

| Pass | Gate | Required result |
|---:|---|---|
| 0 | Baseline capture | Preserve the current render and record visible failures before editing. |
| 1 | Coordinate-system lock | Source width, height and SHA-256 match the manifest. Abort on mismatch. |
| 2 | Primary equipment geometry | Refit high-confidence loudspeaker boxes to the visible cabinet extents. |
| 3 | Occlusion / semantic separation | Separate overlapping semantic regions; e.g. DJ surface vs. loudspeakers in front of it. |
| 4 | Secondary / lighting geometry | Record only the physical emitter/source region supported by the image; do not infer a showfile FID from an effect alone. |
| 5 | Presentation + QA | Labels remain readable without obscuring critical geometry; all boxes are in bounds; mirrored pairs are checked for gross asymmetry. |

After pass 5, rerun the renderer and inspect the plate at **100% and 200%**. Any failed gate returns to the earliest affected pass rather than being patched downstream.

## Failure taxonomy

- `COORDINATE_DRIFT` — source dimensions/checksum and bbox coordinate space disagree.
- `UNDER_BOX` — box excludes a material part of the equipment.
- `OVER_BOX` — box contains excessive unrelated scene area.
- `SEMANTIC_OVERLAP` — one annotation claims pixels belonging to a different semantic object without an explicit reason.
- `LABEL_OCCLUSION` — label blocks equipment needed to review another detection.
- `PAIR_ASYMMETRY` — a mirrored L/R pair differs enough to warrant review.
- `MODEL_OVERCLAIM` — photo only proves equipment class or effect, but annotation claims a specific model/FID.
- `SOURCE_MUTATION` — annotation was authored against a transformed derivative instead of the canonical source.

## 2026-08-12 refactor result

The v2 pass changes the visible geometry to the native 1536×1152 source:

- Air Motion V2 L/R boxes now fit the red three-horn cabinets.
- Airten V3 L/R boxes now fit the two white/red fill cabinets.
- Outside Xair L/R boxes are moved to the actual visible cabinet fronts.
- The centre Xair cluster box spans the complete four-cabinet red-framed array.
- The DJ region is constrained to the visible work surface rather than sharing the same broad box as the speaker layer.
- Lighting boxes are tightened to the visible linear emitters / green source regions while retaining `FID TBC`.
- Long descriptions are moved to a legend rather than placed over the equipment.

## Tooling

Run:

```bash
python3 scripts/photo-audit-loop.py \
  --image 09-site-survey/photos/2026-08-12-main-room-source.jpg \
  --manifest 09-site-survey/data/main-room-equipment-audit-2026-08-12.json \
  --out 09-site-survey/rendered/main-room-equipment-audit.jpg
```

The command validates the canonical image before rendering. A checksum or dimension mismatch is a hard failure.

## Review policy

Photo evidence may improve **physical position, cabinet visibility and morphology confidence**. It does not supersede the repository's stronger sources for signal flow, serials, DSP parameters, amplifier channels, DMX addresses or firmware. Lighting FIDs remain unresolved until rear-label capture, controlled fixture isolation, DMX flash/unplug testing, or another uniquely identifying observation closes the gap.
