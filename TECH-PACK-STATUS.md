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
| 3. Signal Flow Diagram (SVG) | ⚠️ JSX only | New conversation needed → Conversation A |
| 4. Rack Elevation (SVG) | ❌ Not started | Need new rack photo first (Issue #2) |
| 5. Speaker Zone Map (SVG) | ❌ Not started | New conversation needed → Conversation D |
| 6. Amplifier Assignments | ✅ Complete | Data in README |
| 7. CQ-12T I/O List | ✅ Confirmed from photos | Data in README |
| 8. Cable Schedule | ⚠️ Stale (39 cables, pre-CQ12) | New conversation needed → Conversation C |
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

| Conv | Purpose | Source files | Blocker |
|---|---|---|---|
| A | Signal Flow SVG | JSX from c8999358 | None — can start today |
| B | Rack Elevation SVG | New rack photo + nomad system spec.pdf | 🔴 Need rack photo first |
| C | Updated Cable Schedule | nomad cable schedule.docx + nomad wiring 18spk armonia.pdf + AH CQ-12T guide | None — can start today |
| D | Speaker Zone Map SVG | Zone data from 81ef8190 | None — can start today |
| E | Master tech pack compile | All of the above | Needs A–D complete |

---

## Open Issues Before Sign-Off

- 🔴 **Issue 1 — Xair impedance:** 6× Stasys Xair at 1.33Ω on Bias V3 — below minimum spec. Must resolve (add amp / rewire / Powersoft confirmation).
- 🟡 **Issue 2 — Rack photo:** Physical rack ≠ documented spec order. V9 removed. Need current photo.
- 🟡 **Issue 3 — Out4/5/6:** CQ-12T outputs at 0 dB, unlabelled. In use or spare?
- 🟢 **Issue 4 — Athens speakers:** Model not documented.
- 🟢 **Issue 5 — Production contact:** Needed for available rider.
