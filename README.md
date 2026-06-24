# NØMAD Toronto — AV System Documentation

**Venue:** NØMAD Toronto  
**Address:** 725 Queen Street East, Toronto, ON M4M 1H1  
**Phone:** 647-643-8823 · **Email:** [info@nomad725.ca](mailto:info@nomad725.ca) · **Web:** [nomad725.ca](https://nomad725.ca)  
**Capacity:** 550 standing · **Instagram / Facebook:** @nomadtorontoofficial  
**System integrator:** Emblem Projects Inc. · [admin+claude@emblemprojects.com](mailto:admin+claude@emblemprojects.com)  
**Documentation last updated:** 2026-04-27 · **Spec revision:** [Rev 2.0](01-source-documents/nomad-system-spec-v2.md)

---

## Executive Summary

NØMAD Toronto operates a permanent **VOID Acoustics 18-speaker professional PA system** purpose-built for DJ-format electronic music events. The system delivers full-venue sound coverage across s[...]

Five **Bias-platform DSP amplifiers** (by VOID Acoustics / Powersoft) provide 14,800+ watts of amplification, each networked for real-time remote monitoring and adjustment via **Armonía Pro Audio[...]

A **Drawmer SP2120** stereo processor sits in the signal chain ahead of the amplifiers as a hardware limiter and system protector, safeguarding the speakers from overdrive regardless of mixer sett[...]

The system was designed and installed by **Emblem Projects Inc.** and verified against the Armonía DSP network in March 2026, with the CQ-12T installation confirmed April 2026.

NØMAD Toronto also operates a **grandMA2-controlled lighting rig** — 31 intelligent/LED fixtures (4 Sharpy moving beams, 10 moving washes, 7 LED strobe bars, 9 laser bars, 1 DJ-deck LED bar) plus CO₂ jets and atmospheric haze across 2 DMX universes. The rig is **decoded from the venue showfile (June 2026)**; physical fixture positions, real-world fixture models, DMX-node topology, and lighting power are pending on-site verification. See the [Lighting Subsystem](08-lighting/README.md).

---

## System Status Dashboard

| Item | Status | Last Verified | Action |
|------|--------|--------------|--------|
| Overall system health | ✅ Operational | 2026-04-27 | — |
| Bias V9 amplifier | ❌ OFFLINE | 2026-03-16 | Physically present — all channels disconnected, breaker off. Remove when rack is serviced. |
| CQ-12T firmware | ⚠️ Update available | 2026-04-27 | V1.2.1 on-site → V1.2.2 available. Update at next maintenance window. |
| DJM-V10 firmware | ❓ Unconfirmed | — | Check firmware version on unit via Settings menu. Latest: 1.20. |
| CDJ-3000 firmware | ✅ Likely current | 2026-01 | Latest 3.22 released Jan 2026. Confirm on each unit. |
| Bias Q5 breaker spec | ❓ Unconfirmed | — | Phoenix 5-pin mains connector — breaker rating not yet confirmed. Issue #7. |
| Athens speaker submodel | ❓ Unconfirmed | — | Turbosound TCS-AN series confirmed; exact model TBC. Photograph rear label on next visit. |
| Lighting rig | ⚠️ Documented from showfile | 2026-06-24 | grandMA2 patch decoded; physical verification pending. See [Lighting Subsystem](08-lighting/README.md). |
| Lighting — CO₂ jets patch | ❓ Unpatched | — | Both CO₂ jets at DMX address 0 in showfile. Patch & verify on-site. |
| Lighting — fixture positions | ❓ Unknown | — | All fixtures at 0,0,0 in showfile. Survey on next visit. |
| Lighting — fixture makes/models | ❓ Unconfirmed | — | Only generic MA profiles in showfile (Sharpy name-suggestive). Identify on-site. |
| Open issues | 5 | 2026-04-27 | See [Open Issues](#open-issues) section |
| Tech pack | ✅ Complete | 2026-06-24 | 7 audio documents + lighting subsystem. See [Tech Pack](#tech-pack) section. |

---

## Quick Links

| Document | | Document | |
|----------|---|----------|---|
| 📋 [System Overview](07-tech-pack/system-overview.md) | One-page summary | 🎚️ [Available Rider](07-tech-pack/available-rider.md) | For touring artists |
| 🔌 [Signal Flow Diagram](07-tech-pack/signal-flow.svg) | Full signal chain | 🗺️ [Speaker Zone Map](07-tech-pack/speaker-zone-map.svg) | Top-down layout |
| 🗄️ [Rack Elevation](07-tech-pack/rack-elevation.svg) | 8U amp rack | 📡 [Cable Schedule](07-tech-pack/cable-schedule.md) | 41 cables |
| 🚨 [Emergency Procedures](07-tech-pack/emergency-procedures.md) | Fault response | 💾 [Firmware Changelog](06-reference-docs/firmware-changelog.md) | Update status |
| 💡 [Lighting Overview](07-tech-pack/lighting-system-overview.md) | grandMA2 rig | 🎛️ [DMX Patch Schedule](07-tech-pack/dmx-patch-schedule.md) | 31 fixtures · 2 universes |
| 🔦 [Lighting Spec](08-lighting/nomad-lighting-spec-v1.md) | Full fixture spec | 🗂️ [Lighting Subsystem](08-lighting/README.md) | Source + manuals |
| 🗺️ [DMX Patch Map](08-lighting/assets/svg/dmx-patch-map.svg) | Schematic address map | 📇 [Fixture Inventory](08-lighting/fixture-inventory.md) | Counts + FIDs |

---

## Operations

### Power-Up Sequence (Pre-Event)

> Allow **60 minutes** before doors open.

1. **Turn on the PDU** (Tripp Lite, rack U9–U10) — powers SP2120 and control PC.
2. **Turn on the CQ-12T** (front panel button). Wait 30 seconds for boot.
3. **Recall the house scene** on CQ-12T — confirm Main LR, MonOut, and BakFil levels are set.
4. **Turn on amplifiers** — power each Bias amp individually or via rack power sequencer. Allow 60 seconds for DSP initialisation.
5. **Launch Armonía** on the control PC. Confirm all 5 active amps show green (192.168.10.10–.14).
6. **Turn on CDJ-3000s and DJM-V10** — Pro DJ Link will connect automatically.
7. **Sound check** — play test tone or music at low level. Verify signal at all zones (mains, booth, entrance).
8. **Set DJM-V10 master** to nominal level (0 dB reference). Confirm SP2120 clip indicators are dark.
9. **Brief the DJ** on monitor levels and available inputs (CH5–10 on CQ-12T for guest sources).

### Power-Down Sequence (Post-Event)

1. Fade **DJM-V10 master** to zero.
2. **Save current CQ-12T scene** (Settings → Scenes → Save).
3. Power down **CDJ-3000s** and **DJM-V10**.
4. Power down **amplifiers** (allow 2 minutes for thermal cooldown on high-output events).
5. Power down **CQ-12T**.
6. Power down **PDU**.
7. Log any anomalies (unusual noise, distortion, indicator lights) in the event log.

> ⚠️ **Do NOT power down by cutting the main breaker while amps are active** — this can damage speakers due to DC offset on shutdown.

### During Events

- Monitor the **SP2120 bargraphs** (rack U2). Frequent clipping = mixer levels too high. Reduce DJM-V10 master or ask the DJ to lower output.
- Armonía will alert if any amp enters protection mode. Check the control PC if sound drops in one zone.
- For guest DJs bringing external equipment — connect to **CQ-12T CH5–CH10** (XLR or TRS ¼" combo). Do not adjust the existing house channel assignments.

---