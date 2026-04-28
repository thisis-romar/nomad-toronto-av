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
| 9. Armonía DSP Config | ⚠️ Partial | Delays/gains in conversations; no preset export |
| 10. Power Requirements | ⚠️ Partial | Amp mains noted; no load calc |
| 11. Emergency Procedures | ✅ Complete | `07-tech-pack/emergency-procedures.md` |

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
