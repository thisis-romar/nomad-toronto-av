# Nomad Toronto — Tech Pack Status

## Target Deliverables

- [ ] **Document 1:** Internal Technical Reference (PDF)
- [ ] **Document 2:** Technical Available Rider (downloadable PDF for touring artists)

---

## Sections — Document 1 (Internal)

| Section | Status | Blocker |
|---|---|---|
| 1. System Overview | ✅ Complete | `07-tech-pack/system-overview.md` |
| 2. Equipment Inventory | ✅ Complete | `01-source-documents/nomad-system-spec-v2.md` §2–§7 |
| 3. Signal Flow Diagram (SVG) | ✅ Complete | `07-tech-pack/signal-flow.svg` |
| 4. Rack Elevation (SVG) | ✅ Complete | `07-tech-pack/rack-elevation.svg` — sourced from Armonía screenshot (March 2026). V9 shown offline. Q5 position provisional. |
| 5. Speaker Zone Map (SVG) | ✅ Complete | `07-tech-pack/speaker-zone-map.svg` |
| 6. Amplifier Assignments | ✅ Complete | Data in README |
| 7. CQ-12T I/O List | ✅ Confirmed from photos | Data in README |
| 8. Cable Schedule | ✅ Complete | `07-tech-pack/cable-schedule.md` (41 cables, CQ-12T current) |
| 8b. Rack I/O Inventory | ✅ Complete (desk audit) | `07-tech-pack/rack-io-inventory.md` — every power/data/audio port on every rack device, from the manufacturer manuals. 8 discrepancies vs. the as-built docs logged in §12 for site verification. |
| 9. Armonía DSP Config | ⚠️ Partial | Delays/gains in conversations; no preset export |
| 10. Power Requirements | ⚠️ Partial | Amp mains noted; no load calc |
| 11. Emergency Procedures | ✅ Complete | `07-tech-pack/emergency-procedures.md` |
| 12. Lighting System Overview | ✅ Complete | `07-tech-pack/lighting-system-overview.md` |
| 13. DMX Patch Schedule | ✅ Complete | `07-tech-pack/dmx-patch-schedule.md` (31 fixtures + CO₂ + haze, 2 universes) |
| 14. Lighting System Spec | ✅ Complete | `08-lighting/nomad-lighting-spec-v1.md` |
| 15a. DMX Patch Map (SVG) | ✅ Complete | `08-lighting/assets/svg/dmx-patch-map.svg` — schematic address allocation, generated from showfile |
| 15b. Physical Lighting Plot (SVG) | ❌ Blocked | To-scale plot blocked — fixture positions unknown (all 0,0,0). Survey required. |
| 16. Lighting Power / DMX Topology | ⚠️ Partial | No node/breaker/load data in showfile — TBC on-site |
| 17. Lighting Vendor Manuals | ⚠️ Partial | `08-lighting/manuals/` — blocked on fixture identification |

## Sections — Document 2 (Available Rider)

| Section | Status |
|---|---|
| Venue overview (name, address, capacity) | ⚠️ Partial — address/capacity TBC (Issue #5) |
| DJ equipment list | ✅ Ready (CDJ-3000 ×4, CQ-12T) |
| PA system overview | ✅ Ready (VOID 18-speaker system) |
| Available inputs | ✅ Ready (from CQ-12T photos) |
| Monitor outputs | ✅ Ready (MonOut, BakFil) |
| Power spec | ⚠️ Needs confirmation |
| Production contact | ❌ Not started — `07-tech-pack/available-rider.md` has placeholder (Issue #5) |

---

## New Conversations Needed (Nomad AV Rack project)

| Conv | Purpose | Source files | Blocker | Status |
|---|---|---|---|---|
| A | Signal Flow SVG | JSX from c8999358 | None | ✅ Done — `07-tech-pack/signal-flow.svg` |
| B | Rack Elevation SVG | Armonía screenshot (Mar 2026) | None | ✅ Done — `07-tech-pack/rack-elevation.svg` |
| C | Updated Cable Schedule | nomad cable schedule.docx + wiring PDF | None | ✅ Done — `07-tech-pack/cable-schedule.md` |
| D | Speaker Zone Map SVG | Zone data from README | None | ✅ Done — `07-tech-pack/speaker-zone-map.svg` |
| E | Master tech pack compile | All SVGs complete | None | ⏳ In progress |

---

## Open Issues Before Sign-Off

All issues tracked on [GitHub Project #5 — Nomad Toronto AV](https://github.com/users/thisis-romar/projects/5)

- ~~🔴 **Issue 1 — Xair impedance**~~ ✅ Resolved
- 🟡 [**GH #1**](https://github.com/thisis-romar/nomad-toronto-av/issues/1) **Rack photo:** V9 physically present. Photograph rack on next site visit.
- 🟡 [**GH #2**](https://github.com/thisis-romar/nomad-toronto-av/issues/2) **CQ-12T Out4/5/6:** Do not patch until purpose confirmed on-site.
- 🟡 [**GH #3**](https://github.com/thisis-romar/nomad-toronto-av/issues/3) **Athens submodel:** Turbosound TCS-AN confirmed; exact variant TBC — photograph rear type-plate.
- 🟢 [**GH #4**](https://github.com/thisis-romar/nomad-toronto-av/issues/4) **Production contact:** Needed for available rider. Call 647-643-8823.
- 🟡 [**GH #5**](https://github.com/thisis-romar/nomad-toronto-av/issues/5) **Q5 breaker spec:** Phoenix 5-pin mains — verify rating with venue electrician.
- ~~🟢 **Issue 6 — Airten V3 PDF**~~ ✅ Resolved — `VOID-Airten-V3-User-Manual-v2.1.pdf` downloaded
- 🟢 [**GH #6**](https://github.com/thisis-romar/nomad-toronto-av/issues/6) **Armonía DSP backup:** Export .aps preset file via ArmoníaPlus on LAN.
- 🟢 [**GH #7**](https://github.com/thisis-romar/nomad-toronto-av/issues/7) **PDF compile:** Both tech pack deliverables ready to compile.
- 🟢 [**GH #8**](https://github.com/thisis-romar/nomad-toronto-av/issues/8) **Booth dimensions:** Measure on next site visit for available rider.

### Lighting open issues (new — June 2026)

Decoded from the grandMA2 showfile; to be registered on the GitHub project. See
`08-lighting/nomad-lighting-spec-v1.md` §9 and `docs/decisions/ADR-0001-lighting-subsystem.md`.

- 🟡 **L1 — CO₂ jets unpatched:** both CO₂ jets at DMX address 0 in the showfile. Patch & verify on-site.
- 🟡 **L2 — Fixture positions unknown:** all fixtures at 0,0,0 in showfile. Survey before producing a lighting plot.
- ✅ **L3 — Generic MA profiles → real models:** *resolved.* Seven manuals identify every fixture: **YF BEAM 230** beams (confirmed), **Panda Lighting LS650/LS652** lasers, **BETOPPER LM70S** washes, **Light4Me STROBE MULTI BAR** strobes, **Microh LEDBAR RGB** DJ bar, **Chauvet Hurricane Haze 2D** hazer, all FX distributed via an **Elation DP-415** pack. Only the CO₂ jets' make and wattage remain. The **Clay Paky brand** claim is retracted, though the beams are a Sharpy-class discharge fixture after all. See `08-lighting/fixture-identification-audit.md`.
- 🔴 **L8 — Patch/mode mismatch (×5):** beams 14CH (fixture offers 16/20), strobes 13CH (4/16/168), lasers 26CH (11/19/24), DJ bar 11CH (fixed 13), hazer 1CH (fixed 2). Only the moving washes match. The beams' 16-channel stride matches the fixture rather than the profile — a wrong-profile error with no collision, but it costs **ch15 Reset and ch16 Lamp control**, so the discharge lamps cannot be struck or doused from the console. The strobes collide if they are really in 16CH. No address overlaps as patched, so **do not re-patch** until the panel check in audit §9 is done.
- 🟡 **L9 — Lighting load:** 5.73–5.93 kW ≈ 48–49 A @ 120 V, a subtotal — only the CO₂ jets carry no power figure, and the currents assume unity PF. Mains feed and breakers still TBC. The hazer, at 4.4 A, sits on a DP-415 channel rated 5 A.
- 🔴 **L10 — Laser safety:** the nine laser bars are **Class 4** (6 × 500 mW, 638 nm each). Audience reachability, beam stops, responsible operator and any variance are all unrecorded, and cannot be assessed while fixture positions are unknown.
- 🔴 **L11 — DP-415 Dimmer/Switch mode:** the Chauvet Hurricane Haze 2D must **not** be run on a dimmer, and the DP-415's mode is selected pack-wide by dip switch 10. Unverified. Read it before the next show.
- 🟡 **L12 — Inverted fixtures carried as duplicate profiles:** M.Wash 7, M.Wash 10 and Laser.BAR(6) 1 are hung upside down and run on pan/tilt-inverted duplicate fixture *types*. grandMA2 inverts pan/tilt per fixture in the patch; the duplicate-type approach works but splits each group across two types. This is also the repo's only fixture-orientation data — every position in the showfile is `0,0,0`.
- 🟡 **L4 — DMX node/output topology:** map U1/U2 to physical nodes/ports. Not in showfile.
- 🟢 **L5 — Strobe-bar address gaps:** confirm spare room (e.g. 370–382 free) vs. stale patch.
- 🟡 **L6 — Lighting power/breakers:** no PSU/load/breaker data. Confirm with venue electrician.
- 🟡 **L7 — Console make/model/location:** grandMA2 "Nomad" v3.9.60 per export — confirm hardware and booth location.
- 🟢 **L8 — Vendor manuals:** source fixture manuals into `08-lighting/manuals/` once fixtures identified.
