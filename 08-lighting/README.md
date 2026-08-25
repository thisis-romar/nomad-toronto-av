---
title: NØMAD Toronto — Lighting Subsystem
description: Index and status dashboard for the venue lighting subsystem (grandMA2 rig), decoded from the showfile export.
version: 1.3.0
created: 2026-06-24T00:00:00Z
last_updated: 2026-08-25T00:00:00Z
---

# NØMAD Toronto — Lighting Subsystem

This directory is the home of the venue **lighting** documentation, parallel to the audio/PA
tech pack. The rig is a grandMA2-controlled set of moving beams, moving washes, LED strobe bars,
and laser bars, plus CO₂ jets and atmospheric haze — **31 intelligent/LED fixtures across 2 DMX
universes**, decoded from the venue showfile (June 2026).

> See `docs/decisions/ADR-0001-lighting-subsystem.md` for why lighting is organised the way it is
> (deliverables in `07-tech-pack/`; spec + source + manuals here).

## Contents

| Path | What |
|------|------|
| `nomad-lighting-spec-v1.md` | Full lighting system specification (fixtures, universes, profiles, open items) |
| `fixture-inventory.md` | Fixture counts + per-fixture ID list |
| `assets/svg/dmx-patch-map.svg` | Schematic DMX patch map (address allocation per universe) |
| `source-showfile/NOMADFIXPATCHJUNE2026.xml` | Source-of-truth grandMA2 export |
| `source-showfile/README.md` | Showfile provenance + decoding conventions |
| `manuals/` | Vendor manuals — 7 supplied by the venue 2026-08-25 |
| `fixture-identification-audit.md` | Which real fixture is behind each MA profile, and five patch/mode mismatches |
| `rev7-2-reconciliation.md` | Reconciles EMBLEM's Rev 7.2 power/DMX schedule against this audit — no conflicts of fact, three items adopted |
| `nomad-lighting-power-dmx-schedule-rev7.2.pdf` | EMBLEM's own schedule, 24 Aug 2026 — inventory, every DMX personality, 120/240 V comparison, branch allocation |
| `assets/correlation.html` | The same finding laid out to be scanned — correlation table, evidence per fixture, both universes to scale. Regenerate with `python3 scripts/build-correlation-page.py` |
| `assets/lighting-dossier.html` | **The full reference document** — every fixture, every address, and the DMX channel map of every fixture from its own manual. Regenerate with `python3 scripts/build-lighting-dossier.py` |

> The SVG is **regenerable** from the showfile: `python3 scripts/build-lighting-patch-map.py`.
> The patch/mode audit is regenerable too: `python3 scripts/audit-dmx-patch.py`.
> It is a patch/address map, **not** a physical plot (positions are unknown — all `0,0,0`).

Deliverables that mirror the audio tech pack live alongside the audio docs:

| Path | What |
|------|------|
| `../07-tech-pack/dmx-patch-schedule.md` | DMX patch schedule (the lighting analog of the cable schedule) |
| `../07-tech-pack/lighting-system-overview.md` | One-page lighting overview |

## Status Dashboard

| Item | Status | Action |
|------|--------|--------|
| Rig documented from showfile | ⚠️ Desktop decode | Physical verification pending |
| CO₂ jets DMX patch | ❓ Unpatched | Address 0 in showfile — patch & verify on-site |
| Fixture positions | ❓ Unknown | All `0,0,0` in showfile — survey on next visit |
| Real fixture makes/models | ✅ Identified | Beams **YF BEAM 230**, lasers **Panda LS650/LS652**, washes **BETOPPER LM70S**, strobes **Light4Me**, DJ bar **Microh LEDBAR RGB**, haze **Chauvet Hurricane Haze 2D**, FX distribution **Elation DP-415**. Only the CO₂ jets remain |
| Patch vs. fixture modes | ❌ **5 mismatches** | Beams 14CH, strobes 13CH, lasers 26CH, DJ bar 11CH, hazer 1CH — only the washes match (audit §3) |
| Beam lamp control | ❌ **Unreachable** | The 14CH profile stops before ch15 Reset / ch16 Lamp control — the discharge lamps cannot be struck or doused from the console (audit §6) |
| CO₂ jets "unpatched" | 🔧 Restated | Both jets are **channels on the one DP-415**, not fixtures needing a patch. Read the pack's dip switches (audit §8) |
| DP-415 Dimmer vs Switch | ⚠️ **Must read Switch** | One pack carries the hazer and both CO₂ jets, its mode is pack-wide (dip 10), and the Haze 2D must not be dimmed — so there is only one correct setting (audit §8) |
| Inverted fixtures | 🔁 3 known | M.Wash 7, M.Wash 10, Laser.BAR 1 run on pan/tilt-inverted duplicate profiles — the repo's only orientation data (audit §12) |
| Lighting connected load | 🟡 Subtotal | **5.73–5.93 kW ≈ 48–49 A @ 120 V**; only the CO₂ jets missing (audit §11) |
| Laser safety class | ☢️ **Class 4** | 9 bars × 6 × 500 mW @ 638 nm. Compliance items unrecorded (audit §11) |
| Patch address integrity | ✅ Verified | No overlaps, no universe-boundary crossings (`scripts/audit-dmx-patch.py`) |
| DMX node/output topology | ❓ TBC | Map U1/U2 to physical nodes/ports |
| Lighting power/breakers | 🟡 Partly | Per-fixture W known; a 4-branch 120 V/20 A allocation adopted from Rev 7.2. The installed feed, breakers and PF are still TBC |
| Console make/model/location | ❓ TBC | grandMA2 "Nomad" per export; confirm hardware on-site |
| Lighting plot (SVG) | ❌ Blocked | Cannot draw without real positions |

---

*EMBLEM PROJECTS INC. · 2026-06-24*
