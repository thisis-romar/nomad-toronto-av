# ADR-0001 — Add a Lighting Subsystem to the NØMAD Toronto Tech Pack

- **Status:** Accepted
- **Date:** 2026-06-24
- **Owner:** Emblem Projects Inc.
- **Governs:** repository `nomad-toronto-av`
- **Relates to:** EMBLEM-NLP-SOP-001 (Repository Architecture & Code Topology) v1.2.0 — §4.2, §8

## Context

`nomad-toronto-av` documented only the audio/PA system. The venue also operates a
grandMA2-controlled lighting rig, supplied as a showfile export
(`nomad_2026-06-13_kayo-toronto-ft-pools`, exported 2026-06-24). We need to add the lighting
rig as a documented subsystem without disturbing the existing audio documentation.

EMBLEM-NLP-SOP-001 §8 requires that structural decisions be recorded in an ADR. This repo had no
`docs/decisions/` ADRs; this is the first. The SOP is primarily a **software/code-repository**
standard; this repo is a **documentation deliverable**, so most SOP clauses (build orchestration,
CI/CD, dependency tooling, web/ML layouts) are not applicable. The clauses that do apply are
§4.2 (feature-based / strict containment), §2.1.2 (independent semver + Keep-a-Changelog),
§6 (README by audience), and §8 (this ADR).

## Decision

1. **Lighting is added as an in-repo subsystem** (no separate repository). The repo is treated as
   a single client-delivery monorepo.
2. **Layout = Hybrid:**
   - **Deliverables** that have an audio analog live next to the audio deliverables in
     `07-tech-pack/` — `dmx-patch-schedule.md` (analog of `cable-schedule.md`) and
     `lighting-system-overview.md` (analog of `system-overview.md`). This preserves
     discoverability parity with the audio tech pack.
   - **Subsystem-specific material** is contained in a new `08-lighting/` slice — the system
     spec, the source showfile + provenance, and vendor manuals.
3. **Independent semver + Keep-a-Changelog** (SOP §2.1.2): new lighting docs are versioned
   independently starting at `1.0.0`; a root `CHANGELOG.md` is introduced.
4. **Data integrity:** values absent from the showfile (physical positions, real fixture
   makes/models, DMX node topology, power) are flagged TBC, never invented — consistent with how
   the repo already flags unconfirmed audio items.

## Alternatives considered

- **Full `08-lighting/` containment** (every lighting doc, including deliverables, under one
  slice). Strongest match to SOP §4.2 strict containment, but breaks parity with the audio tech
  pack, where deliverables live in `07-tech-pack/`. Rejected in favour of the Hybrid layout for
  discoverability.
- **Scatter lighting across the existing `01–07` buckets** (spec → `01-source-documents/`,
  assets → `05-speaker-assets/`, etc.). Rejected: those buckets are implicitly audio-scoped
  (`05-speaker-assets` is literally named for speakers), and scattering is the §4.1 layered
  anti-pattern the SOP warns against.
- **Separate repository for lighting.** Rejected: one venue, one delivery; cross-referencing
  audio and lighting in a single tech pack is the deliverable.

## Consequences

- New top-level `08-lighting/` directory and new `docs/decisions/` + `CHANGELOG.md` conventions.
- Two new deliverables in `07-tech-pack/` must be wired into `scripts/build-tech-pack.py` to
  appear in the compiled PDF.
- Lighting docs carry their own semver line independent of the audio spec's `2.0.0`.
- A lighting plot SVG is intentionally **not** produced until real fixture positions are surveyed.
