# NØMAD Toronto — AV System Documentation

**Venue:** NØMAD Toronto  
**Address:** 725 Queen Street East, Toronto, ON M4M 1H1  
**Phone:** 647-643-8823 · **Email:** [info@nomad725.ca](mailto:info@nomad725.ca) · **Web:** [nomad725.ca](https://nomad725.ca)  
**Capacity:** 550 standing · **Instagram / Facebook:** @nomadtorontoofficial  
**System integrator:** Emblem Projects Inc. · [admin+claude@emblemprojects.com](mailto:admin+claude@emblemprojects.com)  
**Documentation last updated:** 2026-04-27 · **Spec revision:** [Rev 2.0](01-source-documents/nomad-system-spec-v2.md)

---

## Executive Summary

NØMAD Toronto operates a permanent **VOID Acoustics 18-speaker professional PA system** purpose-built for DJ-format electronic music events. The system delivers full-venue sound coverage across multiple zones, supporting high-energy performances with an emphasis on sound clarity and reliability.

Five **Bias-platform DSP amplifiers** (by VOID Acoustics / Powersoft) provide 14,800+ watts of amplification, each networked for real-time remote monitoring and adjustment via **Armonía Pro Audio Suite** software.

A **Drawmer SP2120** stereo processor sits in the signal chain ahead of the amplifiers as a hardware limiter and system protector, safeguarding the speakers from overdrive regardless of mixer settings.

The system was designed and installed by **Emblem Projects Inc.** and verified against the Armonía DSP network in March 2026, with the CQ-12T installation confirmed April 2026.

---

## Asset Summary

### DJ Source Chain

| Item                      | Qty | Description                      |
|---------------------------|-----|----------------------------------|
| Pioneer CDJ-3000          | 4   | Industry-standard media players  |
| Pioneer DJM-V10           | 1   | Professional 6-channel DJ mixer  |
| Allen & Heath CQ-12T      | 1   | Digital mixing console           |

### Amplifier Rack

| Item                     | Qty | Description                   |
|--------------------------|-----|-------------------------------|
| Bias V3 amplifier        | 2   | Amplifiers for subwoofer zones|
| Bias Q5 amplifier        | 1   | Mid-range amplifier            |
| Bias Q2 amplifier        | 2   | High-frequency amplification   |
| Bias V9 amplifier        | 1   | Currently offline              |
| Drawmer SP2120           | 1   | System limiter and protector   |

### Speakers

| Item                        | Qty | Description                                       |
|-----------------------------|-----|-------------------------------------------------|
| VOID Air Motion V2 Red      | 2   | FOH main speakers                                |
| VOID Airten V3              | 2   | FOH fill speakers                                |
| VOID Stasys Xair            | 6   | Subwoofers for low frequencies                   |
| VOID Air Vantage            | 2   | DJ booth speakers                                |
| VOID Venu 215 V2            | 2   | DJ subwoofers                                    |
| Turbosound Athens TCS-AN    | 2   | Entrance fill zone                               |

---

## Equipment Lifecycle Guidance

| Equipment                   | Expected Lifespan  | Notes                                          |
|-----------------------------|--------------------|------------------------------------------------|
| CDJ-3000 ×4                | 7–10 years          | High-use units — inspect jog wheels annually   |
| DJM-V10                    | 7–10 years          | Fader replacement ~5 years in heavy use       |
| Allen & Heath CQ-12T       | 10+ years           | Digital console — software serviceable        |
| Bias amplifiers            | 10–15 years         | Powersoft platform — parts available          |
| Bias V9 (offline)          | —                   | Remove from rack and dispose or repurpose     |
| VOID speakers              | 15+ years           | Drivers replaceable — enclosures are permanent|

---

## Technical Overview

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

---

*NØMAD Toronto · AV System Documentation · Rev 2.0 · April 2026 · Prepared by Emblem Projects Inc.*