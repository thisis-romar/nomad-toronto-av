---
title: NØMAD Toronto — Lighting Showfile (Source Provenance)
description: Provenance and decoding conventions for the grandMA2 showfile that is the source of truth for the venue lighting subsystem.
version: 1.0.0
created: 2026-06-24T00:00:00Z
last_updated: 2026-06-24T00:00:00Z
---

# NØMAD Toronto — Lighting Showfile (Source)

This directory holds the **source-of-truth** export for the venue lighting rig. All lighting
documentation in this repo (`08-lighting/nomad-lighting-spec-v1.md`,
`07-tech-pack/dmx-patch-schedule.md`, `07-tech-pack/lighting-system-overview.md`) is **derived
from this file** and must be re-validated against it if the showfile is re-exported.

## File

| Field | Value |
|-------|-------|
| File | `NOMADFIXPATCHJUNE2026.xml` |
| Format | grandMA2 XML patch/fixture export (`http://schemas.malighting.de/grandma2/xml/MA`) |
| Console / platform | grandMA2 **"Nomad"** — MA Lighting (software platform, dongle-licensed) |
| Schema version | MA `3.9.60` (`major_vers="3" minor_vers="9" stream_vers="60"`) |
| Showfile name | `nomad_2026-06-13_kayo-toronto-ft-pools` |
| Showfile date | 2026-06-13 |
| Export datetime | 2026-06-24T15:15:38 |

> ⚠️ **"Nomad"** here is the MA Lighting product name for the dongle-licensed grandMA2 software
> platform — it is **not** a reference to the venue. The on-site control hardware
> (grandMA2 onPC + Nomad dongle, command wing, or full console) and its booth location are
> **not** described by the export. See the spec §9 open items.

## DMX addressing convention

Addresses in `<Patch><Address>` are **absolute** across the patch (1-based), not
universe-relative:

| Universe | Absolute address range |
|----------|------------------------|
| Universe 1 | 1 – 512 |
| Universe 2 | 513 – 1024 |

To convert an absolute address `A` to universe-relative: `universe = ceil(A / 512)`,
`relative = A − (universe − 1) × 512`. Example: absolute `722` → Universe 2, relative `210`.

An `<Address>` of **`0` means the fixture is unpatched** (this is the case for the CO₂ jets).

## What the showfile does and does NOT contain

**Contained:** fixture names, fixture IDs, MA fixture-profile names, channel footprints,
sub-fixture (cell) structure, DMX patch addresses, MA layer/group organisation.

**Not contained (do NOT infer — flagged TBC throughout the docs):**
- Real-world fixture manufacturers/models (only generic MA profile strings are present).
- Physical fixture positions — every `<AbsolutePosition>` is `0,0,0`.
- DMX node/output topology (which physical node/port drives each universe).
- Power, breaker, or load data for the lighting rig.

---

*EMBLEM PROJECTS INC. · 2026-06-24*
