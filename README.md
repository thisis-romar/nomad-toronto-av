# NØMAD Toronto — AV System Documentation

**Venue:** NØMAD Toronto  
**Address:** 725 Queen Street East, Toronto, ON M4M 1H1  
**Phone:** 647-643-8823 · **Email:** [info@nomad725.ca](mailto:info@nomad725.ca) · **Web:** [nomad725.ca](https://nomad725.ca)  
**Capacity:** 550 standing · **Instagram / Facebook:** @nomadtorontoofficial  
**System integrator:** Emblem Projects Inc. · [admin+claude@emblemprojects.com](mailto:admin+claude@emblemprojects.com)  
**Documentation last updated:** 2026-04-27 · **Spec revision:** [Rev 2.0](01-source-documents/nomad-system-spec-v2.md)

---

## Executive Summary

NØMAD Toronto operates a permanent **VOID Acoustics 18-speaker professional PA system** purpose-built for DJ-format electronic music events. The system delivers full-venue sound coverage across six independently controlled zones — front-of-house mains and fill, a six-cabinet subwoofer cluster, dedicated DJ booth monitoring, and entrance fill.

Five **Bias-platform DSP amplifiers** (by VOID Acoustics / Powersoft) provide 14,800+ watts of amplification, each networked for real-time remote monitoring and adjustment via **Armonía Pro Audio Suite** software. Source audio runs from four **Pioneer CDJ-3000** media players through a **Pioneer DJM-V10** mixer, into an **Allen & Heath CQ-12T** digital matrix mixer which handles all routing, monitor sends, and level management.

A **Drawmer SP2120** stereo processor sits in the signal chain ahead of the amplifiers as a hardware limiter and system protector, safeguarding the speakers from overdrive regardless of mixer settings.

The system was designed and installed by **Emblem Projects Inc.** and verified against the Armonía DSP network in March 2026, with the CQ-12T installation confirmed April 2026.

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
| Open issues | 5 | 2026-04-27 | See [Open Issues](#open-issues) section |
| Tech pack | ✅ Complete | 2026-04-27 | All 7 documents produced. See [Tech Pack](#tech-pack) section. |

---

## Quick Links

| Document | | Document | |
|----------|---|----------|---|
| 📋 [System Overview](07-tech-pack/system-overview.md) | One-page summary | 🎚️ [Available Rider](07-tech-pack/available-rider.md) | For touring artists |
| 🔌 [Signal Flow Diagram](07-tech-pack/signal-flow.svg) | Full signal chain | 🗺️ [Speaker Zone Map](07-tech-pack/speaker-zone-map.svg) | Top-down layout |
| 🗄️ [Rack Elevation](07-tech-pack/rack-elevation.svg) | 8U amp rack | 📡 [Cable Schedule](07-tech-pack/cable-schedule.md) | 41 cables |
| 🚨 [Emergency Procedures](07-tech-pack/emergency-procedures.md) | Fault response | 💾 [Firmware Changelog](06-reference-docs/firmware-changelog.md) | Update status |

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

## Maintenance Schedule

> Recommended baseline for a permanent nightclub installation. Adjust based on event frequency.

| Cadence | Task | Who |
|---------|------|-----|
| **After every event** | Visual rack check — all amps green, no fault LEDs. Log any anomalies. | In-house tech |
| **Weekly** | Vacuum amp rack vents. Check Armonía fault flags. Confirm CQ-12T scene is intact. | In-house tech |
| **Monthly** | Inspect all speaker grilles and cabinets for physical damage. Check NL4 and XLR connectors at rear of rack — reseat any loose connectors. Run an Armonía "Check Updates" for all amps. | In-house tech or integrator |
| **Quarterly** | Apply pending firmware updates (CQ-12T, amps). Back up CQ-12T scenes to USB. Back up Armonía workspace. Electrical safety inspection of rack cabling. | Integrator |
| **Annually** | Full system commissioning re-verification. Photograph rack for documentation update. Replace any worn consumables (IEC C20 leads, NL4 cables). Review open issues for resolution. | Integrator |

---

## Support & Escalation

### Tier 1 — In-House

| Role | Name | Contact |
|------|------|---------|
| Venue tech / system operator | *(TBC — Issue #5)* | *(TBC)* |
| General venue enquiries | — | 647-643-8823 · info@nomad725.ca |

### Tier 2 — System Integrator

| Company | Contact | Notes |
|---------|---------|-------|
| **Emblem Projects Inc.** | [admin+claude@emblemprojects.com](mailto:admin+claude@emblemprojects.com) | Original system designer. Technical questions, config changes, commissioning. |

### Tier 3 — Manufacturer Support

| Brand | Product | Contact | Hours |
|-------|---------|---------|-------|
| **VOID Acoustics** | All VOID speakers + Bias amps | +44 (0) 1202 666 006 · [hello@voidacoustics.com](mailto:hello@voidacoustics.com) | UK business hours |
| **Powersoft** | Armonía DSP software | [support@powersoft.com](mailto:support@powersoft.com) · powersoft.com | — |
| **Allen & Heath** | CQ-12T mixer | [support@allen-heath.com](mailto:support@allen-heath.com) · allen-heath.com | UK business hours |
| **AlphaTheta (Pioneer DJ)** | CDJ-3000 · DJM-V10 | support.alphatheta.com | Online portal |
| **Drawmer** | SP2120 | drawmer.com/contact | — |
| **Turbosound / Music Tribe** | Athens speakers | info@turbosound.com · musictribe.com | — |

### Emergency / After-Hours

- **Fire / medical / security:** follow venue emergency plan — audio system is secondary.
- **Audio emergency (loss of sound, feedback, burning smell):** see [Emergency Procedures](07-tech-pack/emergency-procedures.md).
- **After-hours integrator escalation:** *(TBC — add emergency contact for Emblem Projects)*

---

## Vendor & Service Information

### System Integrator

**Emblem Projects Inc.** designed and documented this system. Contact for: configuration changes, amplifier DSP edits, firmware coordination, new equipment integration, training.

### Service Contracts & Warranty

| Equipment | Warranty status | Service contract |
|-----------|----------------|-----------------|
| VOID Acoustics speakers | *(confirm purchase date with VOID — typically 3 years)* | None on file |
| Bias amplifiers | *(confirm purchase date)* | None on file |
| Allen & Heath CQ-12T | *(confirm purchase date — typically 2 years)* | None on file |
| Pioneer CDJ-3000 / DJM-V10 | *(confirm purchase date — typically 1 year)* | None on file |

> Action: Confirm all purchase dates with Emblem Projects and register products with each manufacturer to activate warranty coverage.

### Spare Parts Recommended

| Part | Qty to keep on hand | Purpose |
|------|--------------------|---------| 
| IEC C20 mains cable | 2 | Amp mains replacement |
| NL4 speaker cable (10 m) | 2 | Speaker cable replacement |
| XLR-M to Phoenix MC adapter | 2 | V3 #2 line out → Q2/Q5 input |
| XLR balanced cable (5 m) | 4 | General patching |
| Cat5e patch cable (1 m) | 2 | Armonía network |
| FAT32 USB stick (16 GB) | 1 | CQ-12T firmware/scene backup |

### Equipment Lifecycle Guidance

| Equipment | Expected lifespan | Notes |
|-----------|------------------|-------|
| CDJ-3000 ×4 | 7–10 years | High-use units — inspect jog wheel and USB ports annually |
| DJM-V10 | 7–10 years | Fader replacement ~5 years in heavy use |
| Allen & Heath CQ-12T | 10+ years | Digital console — software-serviceable |
| Bias amplifiers | 10–15 years | Powersoft platform — parts available |
| Bias V9 (offline) | — | Remove from rack and dispose or sell as asset |
| VOID speakers | 15+ years | Drivers replaceable — enclosures are permanent |

---

## Firmware & Software Status

See full details: [firmware-changelog.md](06-reference-docs/firmware-changelog.md)

| Equipment | On-Site | Latest | Action needed |
|-----------|---------|--------|---------------|
| Allen & Heath CQ-12T | 1.2.1 r4213 | **V1.2.2** | ⚠️ Update recommended |
| Pioneer CDJ-3000 ×4 | Likely 3.22 | 3.22 | Confirm on each unit |
| Pioneer DJM-V10 | Unknown | **1.20** | Check unit menu |
| Bias Q5 | Unknown | v1.12.0.76 | Check via Armonía |
| Bias Q2 ×2 | Unknown | v1.12.0.84 (Q2+) | Verify hardware gen first |
| Bias V3 ×2 | Unknown | Legacy via Armonía | Check after updating Armonía |
| ArmoníaPlus (control PC) | Unknown | **2.8** | Update before amp work |
| Turbosound Athens TCS-AN | Unknown | V2.3 (2020) | Confirm model, then check |
| Drawmer SP2120 | N/A | N/A | Analog hardware — no firmware |

---

## Asset Summary

> Approximate replacement values at April 2026 list price (USD). For insurance and asset register reference. Actual purchase prices may differ — confirm with Emblem Projects for invoice values.

### DJ Source Chain

| Item | Qty | Unit (approx.) | Total (approx.) |
|------|-----|----------------|----------------|
| Pioneer CDJ-3000 | 4 | $2,299 | $9,196 |
| Pioneer DJM-V10 | 1 | $2,499 | $2,499 |
| Allen & Heath CQ-12T | 1 | $1,499 | $1,499 |

### Amplifier Rack

| Item | Qty | Unit (approx.) | Total (approx.) |
|------|-----|----------------|----------------|
| Bias V3 amplifier | 2 | $3,500 | $7,000 |
| Bias Q5 amplifier | 1 | $4,500 | $4,500 |
| Bias Q2 amplifier | 2 | $3,200 | $6,400 |
| Bias V9 amplifier (offline) | 1 | $5,500 | $5,500 |
| Drawmer SP2120 | 1 | $750 | $750 |

### Speakers

| Item | Qty | Unit (approx.) | Total (approx.) |
|------|-----|----------------|----------------|
| VOID Air Motion V2 Red | 2 | $8,500 | $17,000 |
| VOID Airten V3 | 2 | $2,800 | $5,600 |
| VOID Stasys Xair | 6 | $6,500 | $39,000 |
| VOID Air Vantage | 2 | $2,200 | $4,400 |
| VOID Venu 215 V2 | 2 | $3,500 | $7,000 |
| Turbosound Athens TCS-AN | 2 | $1,800 | $3,600 |

### Summary

| Category | Approx. value |
|----------|--------------|
| DJ source chain | ~$13,194 |
| Amplifier rack | ~$24,150 |
| Speakers | ~$76,600 |
| **Total system (approx.)** | **~$113,944 USD** |

> ⚠️ These are list price estimates for insurance reference only. Obtain formal valuations from Emblem Projects or a certified AV appraiser for insurance documentation.

---

## Open Issues

| # | Issue | Severity | Status | Owner |
|---|-------|----------|--------|-------|
| 2 | Rack elevation photo not yet updated — V9 still physically present | 🟡 Medium | Open | Venue tech — photograph rack on next visit |
| 3 | CQ-12T Out4/5/6 at 0 dB — purpose unconfirmed | 🟡 Medium | Open | Integrator — verify before patching any signal |
| 4 | Turbosound Athens TCS-AN exact submodel unconfirmed | 🟡 Medium | Open | Venue tech — photograph rear type-plate label |
| 5 | Production / technical contact not documented | 🟢 Low | Open | Venue management — add named contact |
| 7 | Bias Q5 Phoenix 5-pin mains — breaker spec unconfirmed | 🟡 Medium | Open | Venue electrician — verify panel circuit rating |

---

## Tech Pack

All documents produced and ready to distribute: [`07-tech-pack/`](07-tech-pack/)

| Document | File | Audience |
|----------|------|----------|
| System Overview | [system-overview.md](07-tech-pack/system-overview.md) | Management + tech |
| Signal Flow Diagram | [signal-flow.svg](07-tech-pack/signal-flow.svg) | Technical |
| Rack Elevation (8U) | [rack-elevation.svg](07-tech-pack/rack-elevation.svg) | Technical |
| Speaker Zone Map | [speaker-zone-map.svg](07-tech-pack/speaker-zone-map.svg) | Technical + management |
| Cable Schedule (41 cables) | [cable-schedule.md](07-tech-pack/cable-schedule.md) | Technical |
| Emergency Procedures | [emergency-procedures.md](07-tech-pack/emergency-procedures.md) | All staff |
| Technical Available Rider | [available-rider.md](07-tech-pack/available-rider.md) | Artists + booking |

---

## Equipment Manuals

All PDFs in [`02-equipment-manuals/`](02-equipment-manuals/)

**Amplifiers:** [Bias Q5](02-equipment-manuals/amplifiers/Bias_Q5_user_guide_v1.1.pdf) · [Bias V3/V9](02-equipment-manuals/amplifiers/Bias_V3_V9_user_manual.pdf) · [Bias Q2/Q1/D1](02-equipment-manuals/amplifiers/Bias_Q2Q1D1_user_guide.pdf)

**DJ Gear:** [Pioneer CDJ-3000](02-equipment-manuals/dj-gear/Pioneer_CDJ-3000_manual.pdf) · [Pioneer DJM-V10](02-equipment-manuals/dj-gear/Pioneer_DJM-V10_manual.pdf)

**Mixers:** [Allen & Heath CQ-12T User Guide](02-equipment-manuals/mixers/Allen-Heath_CQ-12T_user_guide_v1.2.pdf) · [CQ-12T Datasheet](02-equipment-manuals/mixers/Allen-Heath_CQ-12T_datasheet.pdf)

**Processing:** [Drawmer SP2120](02-equipment-manuals/processing/sp2120_operators_manual.pdf)

**Speakers:** [Air Motion V2](02-equipment-manuals/speakers/VOID-Air-Motion-V2-User-Guide.pdf) · [Airten V3](02-equipment-manuals/speakers/VOID-Airten-V3-User-Manual-v2.1.pdf) · [Air Vantage](02-equipment-manuals/speakers/VOID-Air-Vantage-User-Guide.pdf) · [Stasys Xair](02-equipment-manuals/speakers/VOID-Stasys-Xair-User-Guide.pdf) · [Venu 215 V2](02-equipment-manuals/speakers/VOID-Venu-V2-Series-User-Guide.pdf) · Turbosound Athens TCS-AN *(pending)*

---

## Technical Drawings

All images in [`05-speaker-assets/`](05-speaker-assets/)

| Model | Cover | Dims | Front | Side | Top |
|-------|-------|------|-------|------|-----|
| VOID Air Motion V2 Red | [↗](05-speaker-assets/png/void-air-motion-v2.png) | [↗](05-speaker-assets/png/void-air-motion-v2-dims.png) | [png](05-speaker-assets/png/void-air-motion-v2-front.png) · [svg](05-speaker-assets/svg/void-air-motion-v2-front.svg) | [png](05-speaker-assets/png/void-air-motion-v2-side.png) · [svg](05-speaker-assets/svg/void-air-motion-v2-side.svg) | [png](05-speaker-assets/png/void-air-motion-v2-top.png) · [svg](05-speaker-assets/svg/void-air-motion-v2-top.svg) |
| VOID Airten V3 | [↗](05-speaker-assets/png/void-airten-v3.png) | [↗](05-speaker-assets/png/void-airten-v3-dims.png) | — | — | — |
| VOID Air Vantage | [↗](05-speaker-assets/png/void-air-vantage.png) | [↗](05-speaker-assets/png/void-air-vantage-dims.png) | [png](05-speaker-assets/png/void-air-vantage-front.png) · [svg](05-speaker-assets/svg/void-air-vantage-front.svg) | [png](05-speaker-assets/png/void-air-vantage-side.png) · [svg](05-speaker-assets/svg/void-air-vantage-side.svg) | [png](05-speaker-assets/png/void-air-vantage-top.png) · [svg](05-speaker-assets/svg/void-air-vantage-top.svg) |
| VOID Stasys Xair | [↗](05-speaker-assets/png/void-stasys-xair.png) | [↗](05-speaker-assets/png/void-stasys-xair-dims.png) | — | — | — |
| VOID Venu 215 V2 | [↗](05-speaker-assets/png/void-venu-215-v2.png) | [↗](05-speaker-assets/png/void-venu-215-v2-dims.png) | [png](05-speaker-assets/png/void-venu-215-v2-front.png) · [svg](05-speaker-assets/svg/void-venu-215-v2-front.svg) | [png](05-speaker-assets/png/void-venu-215-v2-side.png) · [svg](05-speaker-assets/svg/void-venu-215-v2-side.svg) | [png](05-speaker-assets/png/void-venu-215-v2-top.png) · [svg](05-speaker-assets/svg/void-venu-215-v2-top.svg) |
| Bias V3 amp | [↗](05-speaker-assets/png/bias-v3-amp.png) | [↗](05-speaker-assets/png/bias-v3-amp-dims.png) | [png](05-speaker-assets/png/bias-v3-amp-front.png) · [svg](05-speaker-assets/svg/bias-v3-amp-front.svg) | [svg](05-speaker-assets/svg/bias-v3-amp-side.svg) | — |
| Bias Q5 amp | [↗](05-speaker-assets/png/bias-q5-amp.png) | [↗](05-speaker-assets/png/bias-q5-amp-dims.png) | — | [png rear](05-speaker-assets/png/bias-q5-amp-rear.png) | — |
| Allen & Heath CQ-12T | [↗](05-speaker-assets/png/ah-cq-12t.png) | [↗](05-speaker-assets/png/ah-cq-12t-dims.png) | — | — | [block diagram](05-speaker-assets/png/ah-cq-12t-block.png) |
| Pioneer CDJ-3000 | [↗](05-speaker-assets/png/pioneer-cdj-3000.png) | — | [top panel](05-speaker-assets/png/pioneer-cdj-3000-top.png) | [rear panel](05-speaker-assets/png/pioneer-cdj-3000-rear.png) | — |
| Pioneer DJM-V10 | [↗](05-speaker-assets/png/pioneer-djm-v10.png) | — | [top panel](05-speaker-assets/png/pioneer-djm-v10-top.png) | [rear panel](05-speaker-assets/png/pioneer-djm-v10-rear.png) | — |

---

## Source Documents

| Document | File | Notes |
|----------|------|-------|
| System Spec Rev 2.0 (April 2026) | [nomad-system-spec-v2.md](01-source-documents/nomad-system-spec-v2.md) | Current — fully corrected |
| System Spec Rev 1.0 (Feb 2026) | [nomad-system-spec.pdf](01-source-documents/nomad-system-spec.pdf) | Legacy — ~60% superseded |
| Wiring Diagram — Armonía (March 2026) | [nomad-wiring-18spk-armonia.pdf](01-source-documents/nomad-wiring-18spk-armonia.pdf) | Ground truth for amp assignments |
| Wiring Diagram — Final | [nomad-wiring-diagram-final.pdf](01-source-documents/nomad-wiring-diagram-final.pdf) | Reference |

---

## Reference Docs

| Document | File |
|----------|------|
| Firmware & Software Changelog | [firmware-changelog.md](06-reference-docs/firmware-changelog.md) |
| 19-Inch Rack Standards (EIA-310-D) | [19-inch-rack-standards.md](06-reference-docs/19-inch-rack-standards.md) |
| Professional Audio Wiring Standards | [professional-audio-wiring-standards.md](06-reference-docs/professional-audio-wiring-standards.md) |
| SVG Rack Elevation Methodology | [svg-rack-elevation-methodology.md](06-reference-docs/svg-rack-elevation-methodology.md) |

---

## Technical Reference

### Signal Chain

```
4× Pioneer CDJ-3000 ──Pro DJ Link──▶ Pioneer DJM-V10
                                            │
                         ┌── Master XLR L/R (CH1+2 "Music")  ┐
                         └── Booth XLR L/R  (CH3+4 "MonIn")  ┘
                                            │
                                   Allen & Heath CQ-12T
                                   FW 1.2.1 · IP 169.254.182.156
                                            │
      ┌── Main LR XLR ──▶ Drawmer SP2120 ──▶ Bias V3 #2 ──┬──▶ Xair L-3 (CH1, 4Ω)
      │                                                     └──▶ Xair R-3 (CH2, 4Ω)
      │                                     V3 #2 line outs:
      │                                       ├──▶ Bias Q5  ──▶ Xair L-1/2, R-1/2 (4ch, 4Ω)
      │                                       ├──▶ Bias Q2 #2 ──▶ Air Motion L+R (bi-amp)
      │                                       └──▶ Bias V3 #1 ──▶ Airten V3 L/R
      │
      ├── MonOut (−32 dB) ──▶ Bias Q2 #1 ──▶ Air Vantage L/R + Venu 215 L/R
      └── BakFil (−34 dB) ──▶ Athens TCS-AN ×2 (self-powered, entrance)
```

### CQ-12T Configuration

**Firmware:** 1.2.1 r4213 | **IP:** 169.254.182.156 | **MAC:** 00:04:c4:14:9c:b5

| CH | Label | Source | Notes |
|----|-------|--------|-------|
| 1+2 | Music | DJM-V10 Master Out XLR L/R | Stereo link, +15 dB gain, AG Auto ON |
| 3+4 | MonIn | DJM-V10 Booth Out XLR L/R | Booth/monitor feed |
| 5–10 | Ip5–Ip10 | Unassigned | Available for guest inputs |
| Main LR | → SP2120 | 0 dB | FOH signal path |
| MonOut | → Q2 #1 | −32 dB | DJ booth monitors + Venu 215 |
| BakFil | → Athens | −34 dB | Entrance fill (~20 m cable run) |
| Out4/5/6 | Unassigned | 0 dB | ⚠️ Purpose unconfirmed — do not patch without verification |

### Amplifier Assignments

Armonía network: 192.168.10.x — verified March 2026

| Amp | Armonía Label | S/N | IP | Zone | CH Assignment | Gain / Delay |
|-----|--------------|-----|----|------|---------------|-------------|
| Bias V3 #2 | "Outside Subs" | 341132 | 192.168.10.14 | FOH + signal hub | CH1: Xair L-3 · CH2: Xair R-3 | −3 dB / 0 ms |
| Bias Q5 | "Subs Middle" | 777758 | 192.168.10.10 | FOH subs | CH1–4: Xair L-1, L-2, R-1, R-2 | 0 dB / 0 ms |
| Bias Q2 #2 | "Air Motion" | 00543758 | 192.168.10.11 | FOH mains bi-amp | CH1: AM-L LF · CH2: AM-L HMF · CH3: AM-R LF · CH4: AM-R HMF | +0.5 dB / 1.0 ms |
| Bias V3 #1 | "air ten v3" | 341130 | 192.168.10.13 | FOH fill | CH1: Airten L · CH2: Airten R | −8 dB / 28.23 ms |
| Bias Q2 #1 | "DJ Monitors" | 951058 | 192.168.10.12 | DJ booth | CH1: AV L · CH2: AV R · CH3: Venu L · CH4: Venu R | −4 dB / 0 ms |
| ~~Bias V9~~ | "DELAY SUBS" | — | — | **OFFLINE** | All channels disconnected · CPC 45A off | — |

### Speaker System — 18 Total

| Zone | Qty | Model | Amp | Impedance | Power (AES) |
|------|-----|-------|-----|-----------|------------|
| FOH mains | 2 | VOID Air Motion V2 Red | Q2 #2 bi-amp 4ch | LF 8Ω · HMF 8Ω | 500 W LF · 250 W HMF |
| FOH fill | 2 | VOID Airten V3 | V3 #1 | 8Ω | 500 W |
| Outside subs | 2 | VOID Stasys Xair (L-3, R-3) | V3 #2 CH1/2 | **4Ω each** | 3,200 W |
| Middle subs | 4 | VOID Stasys Xair (L-1/2, R-1/2) | Q5 CH1–4 | **4Ω each** | 3,200 W |
| DJ booth monitors | 2 | VOID Air Vantage | Q2 #1 CH1/2 | 8Ω | 500 W |
| DJ booth sub | 2 | VOID Venu 215 V2 | Q2 #1 CH3/4 | 4Ω | 1,000 W |
| Entrance | 2 | Turbosound Athens TCS-AN | Self-powered (BakFil) | — | 2,500 W int. |

### Power Distribution

| Device | Rack Position | Mains | Max Current | Status |
|--------|--------------|-------|-------------|--------|
| Drawmer SP2120 | U2 | IEC C14 (PDU) | <1 A | ✅ Active |
| Bias V3 #1 | U3 | IEC C20 | 16 A | ✅ Active |
| Bias Q2 #1 | U4 | IEC C20 | 16 A | ✅ Active |
| ~~Bias V9~~ | U5 | CPC 45A | 32 A | ❌ **Breaker OFF** |
| Bias Q2 #2 | U6 | IEC C20 | 16 A | ✅ Active |
| Bias V3 #2 | U7 | IEC C20 | 16 A | ✅ Active |
| Bias Q5 | U8 (provisional) | Phoenix 5-pin | TBC | ✅ Active — ⚠️ Issue #7 |
| Allen & Heath CQ-12T | — | IEC C14 (PDU) | <3 A | ✅ Active |

---

## Project History

**Claude.ai project:** [Nomad AV Rack](https://claude.ai/project/019dcacc-4479-778d-9be8-6d705f5b113d)

| Date | Session | Status |
|------|---------|--------|
| 2026-02-20 | [SVG Rack Elevation Methodology](https://claude.ai/chat/77927477-ddf9-4a6e-8507-652816224db0) | Reference only |
| 2026-02-21 | [Nomad Amp Rack Cable Schedule](https://claude.ai/chat/81ef8190-238f-4f37-901d-ead397b7a6e1) | ⚠️ Stale — predates CQ-12T |
| 2026-03-16 | [Audio Rack Equipment Audit](https://claude.ai/chat/61c49787-7fd9-4227-ae32-2f3c8301d7f6) | ⚠️ Impedance issue resolved |
| 2026-03-24 | [CQ12 Mixer Audit](https://claude.ai/chat/c8999358-0d6d-42d2-8abd-d5e1b06ff2d8) | Most current pre-April session |

---

*NØMAD Toronto · AV System Documentation · Rev 2.0 · April 2026 · Prepared by Emblem Projects Inc.*
