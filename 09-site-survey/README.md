# 09 — Site Survey & Photo Evidence

This slice stores **physical-observation evidence** that bridges the repository's as-built signal documentation and the remaining real-world verification gaps.

## Evidence hierarchy

1. **Rear label / serial / connector photo** — strongest model-level physical evidence.
2. **Distinctive cabinet morphology + known installed inventory** — acceptable for photo correlation when the match is unambiguous.
3. **Visible effect / generic chassis class** — establishes class and approximate location only.
4. **Expected inventory without a legible visual match** — inventory-only; never presented as photo-confirmed.

Photo evidence does not override Armonía, mixer, showfile, or measured wiring data for signal routing, DSP, DMX addresses, firmware, or channel assignments.

## Audits

| Date | View | Deliverable | Data |
|---|---|---|---|
| 2026-08-12 | Dance-floor centre → DJ booth / stage | [Main-room equipment audit](main-room-equipment-audit-2026-08-12.md) | [JSON](data/main-room-equipment-audit-2026-08-12.json) |

## Assets

- `overlays/main-room-equipment-id-2026-08-12.svg` — transparent source-aligned equipment-ID overlay for the 1536×1152 source frame.
- `data/main-room-equipment-audit-2026-08-12.json` — pixel + normalized bounding boxes, confidence, evidence basis, and source-image fingerprint.
- Source frame fingerprint: SHA-256 `0075236726c7d720c5c641211e6cc5580e15662227cebaf1cb9587ada11bfa31` · 1536×1152 JPEG.

The binary photograph is not duplicated in this repository change; the SVG overlay is aligned to the original source frame and the hash preserves evidence identity.

## Intended downstream use

The JSON manifest is deliberately structured so future CV / floor-plan / lighting-plot work can ingest detections without scraping Markdown. Bounding boxes are supplied in both source-image pixels and normalized 0–1 coordinates.
