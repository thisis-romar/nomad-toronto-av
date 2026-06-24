# Changelog

All notable changes to the NØMAD Toronto AV documentation repository are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/) conventions with semantic
versioning, per EMBLEM-NLP-SOP-001 §2.1.2. Individual documents also carry their own
independent `version` in their YAML frontmatter.

## [Unreleased]

### Added — Lighting subsystem (2026-06-24)

- **Lighting documentation subsystem**, decoded from the venue grandMA2 showfile
  (`nomad_2026-06-13_kayo-toronto-ft-pools`, exported 2026-06-24). 31 intelligent/LED fixtures
  plus CO₂ jets and haze across 2 DMX universes.
- `08-lighting/nomad-lighting-spec-v1.md` — lighting system specification (v1.0.0).
- `07-tech-pack/dmx-patch-schedule.md` — DMX patch schedule, the lighting analog of the cable
  schedule (v1.0.0).
- `07-tech-pack/lighting-system-overview.md` — one-page lighting overview (v1.0.0).
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
