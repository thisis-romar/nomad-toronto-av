# Nomad Toronto — Tech Pack Status

## Target Deliverables

- [ ] **Document 1:** Internal Technical Reference (PDF)
- [ ] **Document 2:** Technical Available Rider (downloadable PDF for touring artists)

---

## Sections — Document 1 (Internal)

| Section | Status | Blocker |
|---|---|---|
| 1. System Overview | ❌ Not started | — |
| 2. Equipment Inventory | ⚠️ Partial | CQ-12T now confirmed; needs compile |
| 3. Signal Flow Diagram (SVG) | ✅ Complete | `07-tech-pack/signal-flow.svg` |
| 4. Rack Elevation (SVG) | ❌ Not started | Need new rack photo first (Issue #2) |
| 5. Speaker Zone Map (SVG) | ✅ Complete | `07-tech-pack/speaker-zone-map.svg` |
| 6. Amplifier Assignments | ✅ Complete | Data in README |
| 7. CQ-12T I/O List | ✅ Confirmed from photos | Data in README |
| 8. Cable Schedule | ✅ Complete | `07-tech-pack/cable-schedule.md` (41 cables, CQ-12T current) |
| 9. Armonía DSP Config | ⚠️ Partial | Delays/gains in conversations; no preset export |
| 10. Power Requirements | ⚠️ Partial | Amp mains noted; no load calc |
| 11. Emergency Procedures | ❌ Not started | — |

## Sections — Document 2 (Available Rider)

| Section | Status |
|---|---|
| Venue overview (name, address, capacity) | ❌ Not started |
| DJ equipment list | ✅ Ready (CDJ-3000 ×4, CQ-12T) |
| PA system overview | ✅ Ready (VOID 18-speaker system) |
| Available inputs | ✅ Ready (from CQ-12T photos) |
| Monitor outputs | ✅ Ready (MonOut, BakFil) |
| Power spec | ⚠️ Needs confirmation |
| Production contact | ❌ Not started |

---

## New Conversations Needed (Nomad AV Rack project)

| Conv | Purpose | Source files | Blocker | Status |
|---|---|---|---|---|
| A | Signal Flow SVG | JSX from c8999358 | None | ✅ Done — `07-tech-pack/signal-flow.svg` |
| B | Rack Elevation SVG | New rack photo + nomad system spec.pdf | 🔴 Need rack photo first | ❌ Blocked |
| C | Updated Cable Schedule | nomad cable schedule.docx + wiring PDF | None | ✅ Done — `07-tech-pack/cable-schedule.md` |
| D | Speaker Zone Map SVG | Zone data from README | None | ✅ Done — `07-tech-pack/speaker-zone-map.svg` |
| E | Master tech pack compile | All of the above | Needs A + B complete | ⏳ Blocked on B |

---

## Open Issues Before Sign-Off

- ~~🔴 **Issue 1 — Xair impedance**~~ ✅ Resolved
- 🟡 **Issue 2 — Rack photo:** Physical rack ≠ documented spec order. V9 still physically present but offline. Need current photo.
- 🟡 **Issue 3 — Out4/5/6:** CQ-12T outputs at 0 dB, unlabelled. In use or spare?
- 🟡 **Issue 4 — Athens speakers:** Manufacturer confirmed = **Turbosound Athens TCS-AN series** (Music Tribe). Exact submodel (TCS122 vs TCS152, dispersion variant) TBC — photograph rear type-plate on next site visit. QSG covers full family but DNS blocked download; try from browser: `https://mediadl.musictribe.com/media/PLM/data/docs/P0B71/QSG_TS_P0B48_TCS-AN-Series_A4_WW.pdf`
- 🟢 **Issue 5 — Production contact:** Needed for available rider.
- ~~🟢 **Issue 6 — Airten V3 PDF**~~ ✅ Resolved — `VOID-Airten-V3-User-Manual-v2.1.pdf` downloaded
