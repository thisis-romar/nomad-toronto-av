# 09 — Site Survey & Photo Evidence

This slice stores **physical-observation evidence** that bridges the repository's as-built signal documentation and the remaining real-world verification gaps.

## Evidence hierarchy

1. **Rear label / serial / connector photo** — strongest model-level physical evidence.
2. **Distinctive cabinet morphology + known installed inventory** — acceptable for photo correlation when the match is unambiguous.
3. **Visible effect / generic chassis class** — establishes class and approximate location only.
4. **Expected inventory without a legible visual match** — inventory-only; never presented as photo-confirmed.

Photo evidence does not override Armonía, mixer, showfile, or measured wiring data for signal routing, DSP, DMX addresses, firmware, or channel assignments.

## Audits

| Date | View | Deliverable | Data | QA loop |
|---|---|---|---|---|
| 2026-08-12 | Dance-floor centre → DJ booth / stage | [Main-room equipment audit](main-room-equipment-audit-2026-08-12.md) | [JSON](data/main-room-equipment-audit-2026-08-12.json) | [Visual audit & refactor loop](visual-audit-refactor-loop.md) |

## Assets

- `overlays/main-room-equipment-id-2026-08-12.svg` — transparent source-aligned equipment-ID overlay for the canonical 1536×1152 frame.
- `data/main-room-equipment-audit-2026-08-12.json` — v2 manifest with native-pixel bounding boxes, derived normalized coordinates, confidence, evidence basis, review-pass results, and source-image fingerprint.
- `scripts/photo-audit-loop.py` — checksum/dimension validator and deterministic renderer.
- Source frame fingerprint: SHA-256 `0075236726c7d720c5c641211e6cc5580e15662227cebaf1cb9587ada11bfa31` · 1536×1152 JPEG.

The binary photograph is not duplicated in this repository change. The SVG/JSON are keyed to the canonical source by its dimensions and SHA-256. The renderer intentionally hard-fails if a different source image is supplied.

## Coordinate policy

`bbox_px` is authoritative and always refers to the **native source coordinate system**. Do not author geometry against a resized display derivative. `bbox_norm` is recalculated only after the pixel geometry passes visual review.

## Intended downstream use

The manifest is deliberately structured so future CV / floor-plan / lighting-plot work can ingest detections without scraping Markdown. The visual audit loop is the acceptance gate before a physical position is promoted into downstream geometry.
