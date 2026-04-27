---
title: Nomad Toronto — Cable Schedule
description: Complete cable schedule for the VOID Acoustics system, updated for CQ-12T (April 2026)
version: 2.0.0
created: 2026-04-27T00:00:00Z
last_updated: 2026-04-27T00:00:00Z
---

# Nomad Toronto — Cable Schedule

**Venue:** Nomad Toronto  
**System:** VOID Acoustics 18-speaker installation  
**Status:** Updated April 2026 — CQ-12T replaces Yamaha MG12  
**Source docs:** nomad-wiring-18spk-armonia.pdf · CQ-12T confirmation April 2026

---

## Section 1 — DJ Source to Matrix Mixer

| # | Type | Con. A | From | Con. B | To | Qty | Notes |
|---|------|--------|------|--------|-----|-----|-------|
| 1 | XLR balanced | XLR-M | DJM-V10 Master Out L | XLR-F | CQ-12T CH1 | 1 | 15 dB gain, AG Auto ON |
| 2 | XLR balanced | XLR-M | DJM-V10 Master Out R | XLR-F | CQ-12T CH2 | 1 | Stereo link with CH1 |
| 3 | XLR balanced | XLR-M | DJM-V10 Booth Out L | XLR-F | CQ-12T CH3 | 1 | "MonIn" — monitor/booth feed |
| 4 | XLR balanced | XLR-M | DJM-V10 Booth Out R | XLR-F | CQ-12T CH4 | 1 | Stereo link with CH3 |
| 5 | Cat5e/6 RJ45 | RJ45 | CDJ-3000 #1 | RJ45 | DJM-V10 network | 1 | Pro DJ Link |
| 6 | Cat5e/6 RJ45 | RJ45 | CDJ-3000 #2 | RJ45 | DJM-V10 network | 1 | Pro DJ Link |
| 7 | Cat5e/6 RJ45 | RJ45 | CDJ-3000 #3 | RJ45 | DJM-V10 network | 1 | Pro DJ Link |
| 8 | Cat5e/6 RJ45 | RJ45 | CDJ-3000 #4 | RJ45 | DJM-V10 network | 1 | Pro DJ Link |

---

## Section 2 — CQ-12T Outputs to Amplifiers / Destinations

| # | Type | Con. A | From | Con. B | To | Qty | Level | Notes |
|---|------|--------|------|--------|-----|-----|-------|-------|
| 9 | XLR balanced | XLR-M | CQ-12T Main L | XLR-F | SP2120 Input L | 1 | 0 dB | FOH main path |
| 10 | XLR balanced | XLR-M | CQ-12T Main R | XLR-F | SP2120 Input R | 1 | 0 dB | FOH main path |
| 11 | XLR balanced | XLR-M | CQ-12T MonOut L | Phoenix signal | Q2 #1 Input L | 1 | −32 dB | Booth/monitor path |
| 12 | XLR balanced | XLR-M | CQ-12T MonOut R | Phoenix signal | Q2 #1 Input R | 1 | −32 dB | Booth/monitor path |
| 13 | XLR balanced | XLR-M | CQ-12T BakFil L | XLR-F | Athens L (entrance) | 1 | −34 dB | ~20 m run to entrance |
| 14 | XLR balanced | XLR-M | CQ-12T BakFil R | XLR-F | Athens R (entrance) | 1 | −34 dB | ~20 m run to entrance |

> ⚠️ **Out4/5/6** on CQ-12T currently at 0 dB — purpose unconfirmed. Do not patch until verified on-site.

---

## Section 3 — Processor to FOH Driver Amp

| # | Type | Con. A | From | Con. B | To | Qty | Notes |
|---|------|--------|------|--------|-----|-----|-------|
| 15 | XLR balanced | XLR-M | SP2120 Output L | XLR-F | Bias V3 #2 Input L | 1 | Rack pos 2 → pos 7 |
| 16 | XLR balanced | XLR-M | SP2120 Output R | XLR-F | Bias V3 #2 Input R | 1 | |

---

## Section 4 — V3 #2 Distribution (Signal Hub)

> V3 #2 pre-DSP line outputs (3× XLR-M) are the signal distribution point — no external splitter.

| # | Type | Con. A | From | Con. B | To | Qty | Notes |
|---|------|--------|------|--------|-----|-----|-------|
| 17 | XLR-M → Phoenix | XLR-M | V3 #2 Line Out 1 | Phoenix 12-pin | Q5 Input | 1 | XLR-M to Phoenix signal adapter |
| 18 | XLR-M → Phoenix | XLR-M | V3 #2 Line Out 2 | Phoenix 12-pin | Q2 #2 Input | 1 | XLR-M to Phoenix signal adapter |
| 19 | XLR balanced | XLR-M | V3 #2 Line Out 3 | XLR-F | Bias V3 #1 Input | 1 | Standard XLR |

---

## Section 5 — Amplifier to Speaker (FOH)

### Bias V3 #2 → Outside Sub cluster

| # | Type | Con. A | From | Con. B | To | Qty | Load | Notes |
|---|------|--------|------|--------|-----|-----|------|-------|
| 20 | NL4 speaker | NL4 | V3 #2 CH1 Spk Out | NL4 | Xair L-3 (NL4 In) | 1 | 4 Ω | Outside sub Left |
| 21 | NL4 speaker | NL4 | V3 #2 CH2 Spk Out | NL4 | Xair R-3 (NL4 In) | 1 | 4 Ω | Outside sub Right |

### Bias Q5 → Middle Sub cluster (4× Xair)

| # | Type | Con. A | From | Con. B | To | Qty | Load | Notes |
|---|------|--------|------|--------|-----|-----|------|-------|
| 22 | NL4 speaker | NL4 | Q5 CH1 Spk Out | NL4 | Xair L-1 (NL4 In) | 1 | 4 Ω | Middle sub L-1 |
| 23 | NL4 speaker | NL4 | Q5 CH2 Spk Out | NL4 | Xair L-2 (NL4 In) | 1 | 4 Ω | Middle sub L-2 |
| 24 | NL4 speaker | NL4 | Q5 CH3 Spk Out | NL4 | Xair R-1 (NL4 In) | 1 | 4 Ω | Middle sub R-1 |
| 25 | NL4 speaker | NL4 | Q5 CH4 Spk Out | NL4 | Xair R-2 (NL4 In) | 1 | 4 Ω | Middle sub R-2 |

### Bias Q2 #2 → Air Motion V2 (bi-amp, 4 channels)

> Air Motion V2 uses NL4 connector wired for bi-amp: NL4#1 = LF (pins 1+/1−), NL4#2 = HMF (pins 2+/2−)

| # | Type | Con. A | From | Con. B | To | Qty | Load | Notes |
|---|------|--------|------|--------|-----|-----|------|-------|
| 26 | Phoenix → NL4 | Phoenix 8-pin | Q2 #2 CH1 Spk Out | NL4 #1 | Air Motion L — LF | 1 | 8 Ω LF | NL4 pins 1+/1− |
| 27 | Phoenix → NL4 | Phoenix 8-pin | Q2 #2 CH2 Spk Out | NL4 #2 | Air Motion L — HMF | 1 | 8 Ω HMF | NL4 pins 2+/2− |
| 28 | Phoenix → NL4 | Phoenix 8-pin | Q2 #2 CH3 Spk Out | NL4 #1 | Air Motion R — LF | 1 | 8 Ω LF | NL4 pins 1+/1− |
| 29 | Phoenix → NL4 | Phoenix 8-pin | Q2 #2 CH4 Spk Out | NL4 #2 | Air Motion R — HMF | 1 | 8 Ω HMF | NL4 pins 2+/2− |

### Bias V3 #1 → Airten V3

| # | Type | Con. A | From | Con. B | To | Qty | Load | Notes |
|---|------|--------|------|--------|-----|-----|------|-------|
| 30 | NL4 speaker | NL4 | V3 #1 CH1 Spk Out | NL4 | Airten V3 L | 1 | 8 Ω | FOH fill Left |
| 31 | NL4 speaker | NL4 | V3 #1 CH2 Spk Out | NL4 | Airten V3 R | 1 | 8 Ω | FOH fill Right |

---

## Section 6 — Amplifier to Speaker (Booth)

### Bias Q2 #1 → DJ Monitors + Booth Sub

| # | Type | Con. A | From | Con. B | To | Qty | Load | Notes |
|---|------|--------|------|--------|-----|-----|------|-------|
| 32 | Phoenix → NL4 | Phoenix 8-pin | Q2 #1 CH1 Spk Out | NL4 | Air Vantage L | 1 | 8 Ω | DJ booth monitor Left |
| 33 | Phoenix → NL4 | Phoenix 8-pin | Q2 #1 CH2 Spk Out | NL4 | Air Vantage R | 1 | 8 Ω | DJ booth monitor Right |
| 34 | Phoenix → Phoenix | Phoenix 8-pin | Q2 #1 CH3 Spk Out | Phoenix | Venu 215 V2 L | 1 | 4 Ω | Booth sub Left |
| 35 | Phoenix → Phoenix | Phoenix 8-pin | Q2 #1 CH4 Spk Out | Phoenix | Venu 215 V2 R | 1 | 4 Ω | Booth sub Right |

> **Venu 215 connector note:** Both Phoenix and NL4 inputs are present on the Venu 215 recessed panel. Current connection is via Phoenix. NL4 wiring: pin 1+ / 1−.

---

## Section 7 — Network / Control

| # | Type | From | To | Notes |
|---|------|------|-----|-------|
| 36 | Cat5e RJ45 | Network switch / router | Bias V3 #2 (192.168.10.14) | Armonía control network |
| 37 | Cat5e RJ45 | Network switch / router | Bias Q5 (192.168.10.10) | Armonía control network |
| 38 | Cat5e RJ45 | Network switch / router | Bias Q2 #2 (192.168.10.11) | Armonía control network |
| 39 | Cat5e RJ45 | Network switch / router | Bias V3 #1 (192.168.10.13) | Armonía control network |
| 40 | Cat5e RJ45 | Network switch / router | Bias Q2 #1 (192.168.10.12) | Armonía control network |
| 41 | Cat5e RJ45 | Separate network / link-local | CQ-12T (169.254.182.156) | Not on Armonía subnet — link-local only |

---

## Section 8 — Power (Mains)

| # | Device | Rack Pos | Connector | Max Current | Breaker | Status |
|---|--------|----------|-----------|-------------|---------|--------|
| P1 | Drawmer SP2120 | 2 | IEC C14 (115/230 V sw) | <1 A | PDU | Active |
| P2 | Bias V3 #1 | 3 | IEC C20 | 16 A | 20 A C/D-curve | Active |
| P3 | Bias Q2 #1 | 4 | IEC C20 | 16 A | 20 A C/D-curve | Active |
| P4 | ~~Bias V9~~ | 5 | CPC 45A | 32 A | **OFFLINE — breaker OFF** | Inactive |
| P5 | Bias Q2 #2 | 6 | IEC C20 | 16 A | 20 A C/D-curve | Active |
| P6 | Bias V3 #2 | 7 | IEC C20 | 16 A | 20 A C/D-curve | Active |
| P7 | Bias Q5 | — | Phoenix 5-pin | TBC | TBC | Active — ⚠️ confirm breaker |
| P8 | Allen & Heath CQ-12T | — | IEC C14 | <3 A | PDU | Active |

---

## Cable Summary

| Section | Cable count |
|---------|-------------|
| DJ source → CQ-12T (audio) | 4 |
| Pro DJ Link (data) | 4 |
| CQ-12T outputs | 6 |
| Processor to V3 #2 | 2 |
| V3 #2 line out distribution | 3 |
| V3 #2 speaker outputs (direct) | 2 |
| Q5 speaker outputs | 4 |
| Q2 #2 speaker outputs (bi-amp) | 4 |
| V3 #1 speaker outputs | 2 |
| Q2 #1 speaker outputs (booth) | 4 |
| Armonía network (control) | 5 |
| CQ-12T network | 1 |
| **Total signal cables** | **36** |
| **Total network/data cables** | **10** |

---

## Open Items

- [ ] **Cable 13/14 length:** BakFil run to Athens entrance estimated ~20 m — confirm actual run
- [ ] **Cable 17/18:** Confirm XLR-M → Phoenix adapter spec for Q5 and Q2 #2 inputs
- [ ] **Power P7:** Q5 mains is Phoenix 5-pin — confirm circuit breaker rating on-site
- [ ] **Out4/5/6:** CQ-12T outputs 4–6 cabling unknown — audit before patching
- [ ] **V9 cables:** All V9 speaker cables should be removed or clearly tagged DISCONNECTED
- [ ] **Athens model:** Identify Athens speaker model to confirm XLR input wiring polarity

---

*Updated 2026-04-27 · Supersedes pre-CQ-12T schedule (39 cables, Yamaha MG12 era) · EMBLEM PROJECTS INC.*
