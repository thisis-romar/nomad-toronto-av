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

- `photos/2026-08-12-main-room-source.jpg` — normalized web copy of source photograph.
- `photos/2026-08-12-main-room-equipment-id.jpg` — annotated evidence plate.
- `data/main-room-equipment-audit-2026-08-12.json` — pixel + normalized bounding boxes, confidence, and evidence basis.

## Intended downstream use

The JSON manifest is deliberately structured so future CV / floor-plan / lighting-plot work can ingest detections without scraping Markdown. Bounding boxes are supplied in both source-image pixels and normalized 0–1 coordinates.
