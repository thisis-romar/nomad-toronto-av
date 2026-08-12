# Changelog

All notable changes to the NØMAD Toronto AV documentation repository are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/) conventions with semantic
versioning, per EMBLEM-NLP-SOP-001 §2.1.2. Individual documents also carry their own
independent `version` in their YAML frontmatter.

## [Unreleased]

### Added — Site-survey photo evidence (2026-08-12)

- `09-site-survey/main-room-equipment-audit-2026-08-12.md` — photo-correlated physical equipment audit for the dance-floor view facing the DJ booth/stage.
- `09-site-survey/data/main-room-equipment-audit-2026-08-12.json` — machine-readable bounding boxes, normalized coordinates, confidence and evidence basis.
- `09-site-survey/overlays/main-room-equipment-id-2026-08-12.svg` — transparent 1536×1152 source-aligned identification overlay.
- Photo correlation accounts for the complete visible audience-facing VOID inventory in this frame: 2× Air Motion V2 Red, 2× Airten V3 and 6× Stasys Xair.
- Physical lighting presence is recorded conservatively at equipment-class / approximate-position level; exact fixture FIDs and real-world models remain TBC until isolated on site.

### Added — Lighting subsystem (2026-06-24)

- **Lighting documentation subsystem**, decoded from the venue grandMA2 showfile
  (`nomad_2026-06-13_kayo-toronto-ft-pools`, exported 2026-06-24). 31 intelligent/LED fixtures
  plus CO₂ jets and haze across 2 DMX universes.
- `08-lighting/nomad-lighting-spec-v1.md` — lighting system specification (v1.0.0).
- `07-tech-pack/dmx-patch-schedule.md` — DMX patch schedule, the lighting analog of the cable
  schedule (v1.0.0).
- `07-tech-pack/lighting-system-overview.md` — one-page lighting overview (v1.0.0).
- `08-lighting/fixture-inventory.md` — fixture counts + per-fixture ID list (v1.0.0).
- `08-lighting/assets/svg/dmx-patch-map.svg` — schematic DMX patch map (address allocation per
  universe), plus `scripts/build-lighting-patch-map.py` to regenerate it from the showfile.
- `08-lighting/source-showfile/` — source-of-truth showfile XML + provenance README.
- `08-lighting/README.md`, `08-lighting/manuals/README.md` — slice index and vendor-manual
  placeholder index.
- `docs/decisions/ADR-0001-lighting-subsystem.md` — architecture decision record for the
  lighting subsystem and the Hybrid layout (per SOP §8).
- This `CHANGELOG.md` (per SOP §2.1.2).

### Changed

- `README.md` — executive summary, status dashboard, and quick links extended for lighting.
- `07-tech-pack/system-overview.md` — added a lighting summary section with cross-links.
- `07-tech-pack/available-rider.md` — house lighting moved from "Not available" to an
  available `Lighting` section with house-operated caveats.
- `TECH-PACK-STATUS.md` — added lighting deliverables, sections, and open issues.
- `scripts/build-tech-pack.py` — registered the two lighting deliverables for PDF compilation.

### Notes

- Data absent from the showfile (fixture positions, real makes/models, DMX node topology, power)
  is flagged TBC, not invented. A lighting plot SVG is deferred until positions are surveyed.
