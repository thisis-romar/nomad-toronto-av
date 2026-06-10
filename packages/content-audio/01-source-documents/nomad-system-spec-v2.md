---
title: Nomad Toronto — AV System Specification
description: Full technical specification for the Nomad Toronto VOID Acoustics system. Rev 2.0 — Armonía-verified March 2026, CQ-12T confirmed April 2026. Supersedes Rev 1.0 (Feb 2026).
version: 2.0.0
created: 2026-02-01T00:00:00Z
last_updated: 2026-04-27T00:00:00Z
---

# Nomad Toronto — AV System Specification

**Revision:** 2.0  
**Date:** April 2026  
**Prepared by:** Emblem Projects Inc.  
**Venue:** Nomad Toronto  
**Status:** As-built, Armonía Pro Audio Suite verified March 2026 · CQ-12T confirmed April 2026

> **Revision history:** Rev 1.0 (Feb 2026) documented a pre-commissioning design that was approximately 60% superseded by the time of site verification. Rev 2.0 corrects all amplifier assignments, speaker counts, signal routing, mixer model, and cabinet zones to match the actual installed system. See §12 for a full diff against Rev 1.0.

---

## §1 System Overview

Nomad Toronto operates a permanent VOID Acoustics installation driven by five active Bias-platform DSP amplifiers on a single 8U rack. The signal chain runs:

```
4× Pioneer CDJ-3000
       │ (Pro DJ Link + ch inputs)
Pioneer DJM-V10 (4-channel DJ mixer)
       │ Master XLR L/R        │ Booth XLR L/R
Allen & Heath CQ-12T (digital matrix mixer)
       │ Main LR          │ MonOut −32 dB     │ BakFil −34 dB
Drawmer SP2120        Bias Q2 #1          Athens ×2
       │ XLR stereo        (DJ booth)          (entrance, self-powered)
Bias V3 #2 ──────────────────────────────────────
   CH1/CH2   Line Out 1    Line Out 2    Line Out 3
   │         │             │             │
Xair L-3   Bias Q5      Bias Q2 #2    Bias V3 #1
Xair R-3   (4ch subs)   (Air Motion   (Airten V3
           │             bi-amp)       L/R fills)
     Xair ×4
  L-1 L-2 R-1 R-2
```

**Speaker zones:** 6 (FOH mains, FOH fill, outside subs, middle subs, DJ booth, entrance)  
**Total loudspeakers:** 18  
**Active amplifiers:** 5 (Bias V3 #2, Q5, Q2 #2, V3 #1, Q2 #1)  
**Offline amplifier:** 1 (Bias V9 — physically present, all channels disconnected, breaker off)  
**Signal distribution:** Bias V3 #2 pre-DSP line outs (3× XLR-M) — no external splitter

---

## §2 Source Chain

### §2.1 Pioneer CDJ-3000 ×4

Four CDJ-3000 multi players connected via Pro DJ Link (Cat5e RJ45) to the DJM-V10 for beat sync and link play. Each CDJ also connects to a dedicated DJM-V10 channel via digital coax or RCA.

| Spec | Value |
|------|-------|
| Screen | 9" touch display |
| Storage | SD, USB, Pro DJ Link streaming |
| Network | 100BASE-T (Pro DJ Link) |
| Current firmware | 3.22 (Jan 2026) — confirm on unit |
| Manual | `02-equipment-manuals/dj-gear/Pioneer_CDJ-3000_manual.pdf` |

### §2.2 Pioneer DJM-V10

6-channel DJ mixer feeding the CQ-12T.

| Output | Destination | Level | Connector |
|--------|-------------|-------|-----------|
| Master Out L/R | CQ-12T CH1+2 | 0 dBu nominal | XLR-M |
| Booth Out L/R | CQ-12T CH3+4 | 0 dBu nominal | XLR-M |

| Spec | Value |
|------|-------|
| Channels | 6 |
| Main output | Balanced XLR |
| Booth output | Balanced XLR |
| Current firmware | Check unit — latest is 1.20 (Jan 2026) |
| Manual | `02-equipment-manuals/dj-gear/Pioneer_DJM-V10_manual.pdf` |

---

## §3 Matrix Mixer

### §3.1 Allen & Heath CQ-12T

Replaced Yamaha MG12 in April 2026. The CQ-12T functions as the signal matrix — routing DJM outputs to SP2120 (FOH), DJ booth amplifier (Q2 #1), and Athens entrance speakers (BakFil).

| Parameter | Value |
|-----------|-------|
| Firmware | 1.2.1 r4213 (on-site) · Latest: V1.2.2 (Jul 2025) |
| IP address | 169.254.182.156 (link-local — not on Armonía subnet) |
| MAC | 00:04:c4:14:9c:b5 |

**Channel assignment:**

| CH | Label | Source | Gain | Notes |
|----|-------|--------|------|-------|
| 1+2 | Music | DJM-V10 Master Out XLR L/R | +15 dB | Stereo link, AG Auto ON |
| 3+4 | MonIn | DJM-V10 Booth Out XLR L/R | 0 dB | Orange — monitor/booth feed |
| 5–10 | Ip5–Ip10 | Unassigned | 0 dB | Available for guest inputs |

**Output assignment:**

| Output | Label | Destination | Level | Connector | Notes |
|--------|-------|-------------|-------|-----------|-------|
| Main LR | Main LR | SP2120 Input L/R | 0 dB | XLR-M | FOH main path |
| Aux Out (MonOut) | MonOut | Q2 #1 Input L/R | −32 dB | XLR-M → Phoenix adapter | DJ booth monitors + Venu sub |
| Aux Out (BakFil) | BakFil | Athens entrance ×2 | −34 dB | XLR-M / TRS-XLR | ~20 m cable run to entrance |
| Out4/5/6 | Unknown | Unknown | 0 dB | XLR | ⚠️ Purpose unconfirmed — verify before patching (Issue #3) |

| Spec | Value |
|------|-------|
| Inputs | 13 (10 mono/linkable + 3 stereo) |
| Outputs | Main LR + 6 aux + headphone |
| DSP | 96 kHz, 24-bit, 2× multi-FX |
| Network | 100BASE-T (control), USB-B (audio), Bluetooth |
| Manual | `02-equipment-manuals/mixers/Allen-Heath_CQ-12T_user_guide_v1.2.pdf` |

---

## §4 Processing

### §4.1 Drawmer SP2120

Stereo speaker processor / limiter. Receives CQ-12T Main LR and feeds Bias V3 #2.

| Spec | Value |
|------|-------|
| Position | Rack Pos 2 |
| Inputs | 2× XLR-F balanced |
| Outputs | 2× XLR-M balanced, 100 Ω |
| Max output | +14 dBu |
| Mains | 115/230 V switchable, IEC C14 |
| Power | 9 VA |
| Firmware | None — analog hardware |
| Manual | `02-equipment-manuals/processing/sp2120_operators_manual.pdf` |

---

## §5 Amplifier Rack

### Rack layout (8U)

| Position | Device | Role | Mains | Status |
|----------|--------|------|-------|--------|
| 1 | — | Empty | — | — |
| 2 | Drawmer SP2120 | Stereo limiter | IEC C14 (PDU) | ✅ Active |
| 3 | Bias V3 #1 | Airten V3 FOH fill | IEC C20, 16A | ✅ Active |
| 4 | Bias Q2 #1 | DJ booth monitors + sub | IEC C20, 16A | ✅ Active |
| 5 | Bias V9 | **OFFLINE** — disconnected | CPC 45A — **breaker OFF** | ❌ Offline |
| 6 | Bias Q2 #2 | Air Motion bi-amp | IEC C20, 16A | ✅ Active |
| 7 | Bias V3 #2 | Outside subs + signal hub | IEC C20, 16A | ✅ Active |
| — | Bias Q5 | Middle subs (4ch) | Phoenix 5-pin — **TBC** | ✅ Active (Issue #7) |
| 10 | Tripp Lite PDU | Power distribution (SP2120 + control PC) | — | ✅ Active |

### §5.1 Bias V3 #2 — "Outside Subs" (signal distribution hub)

**Serial:** 341132 · **IP:** 192.168.10.14 · **Gain:** −3 dB · **Delay:** 0 ms

The V3 #2 is the sole recipient of SP2120 signal and acts as the signal distribution point for the entire FOH chain via its pre-DSP line outputs. There is no external splitter.

| Output | Connector | Destination | Notes |
|--------|-----------|-------------|-------|
| CH1 speaker out | NL4 | Xair L-3 (outside sub L) | 4 Ω single cabinet |
| CH2 speaker out | NL4 | Xair R-3 (outside sub R) | 4 Ω single cabinet |
| Line Out 1 (pre-DSP) | XLR-M | Q5 input | XLR-M → Phoenix adapter |
| Line Out 2 (pre-DSP) | XLR-M | Q2 #2 input | XLR-M → Phoenix adapter |
| Line Out 3 (pre-DSP) | XLR-M | V3 #1 input | Standard XLR |

**I/O:** IEC C20 mains · XLR-F inputs · 2× NL4 speaker outs · 3× XLR-M line outs · RJ45 AESOP

### §5.2 Bias Q5 — "Subs Middle"

**Serial:** 777758 · **IP:** 192.168.10.10 · **Gain:** 0 dB · **Delay:** 0 ms  
**Mains:** Phoenix 5-pin (non-standard) — circuit breaker rating TBC (Issue #7)

| CH | Speaker | Zone | Load | Connector |
|----|---------|------|------|-----------|
| 1 | Xair L-1 | Middle sub | 4 Ω | NL4 |
| 2 | Xair L-2 | Middle sub | 4 Ω | NL4 |
| 3 | Xair R-1 | Middle sub | 4 Ω | NL4 |
| 4 | Xair R-2 | Middle sub | 4 Ω | NL4 |

**I/O:** Phoenix 5-pin AC mains · XLR/Phoenix inputs · NL4/Phoenix outputs · RJ45 AESOP

### §5.3 Bias Q2 #2 — "Air Motion"

**Serial:** 00543758 · **IP:** 192.168.10.11 · **Gain:** +0.5 dB · **Delay:** 1.0 ms

Bi-amps the Air Motion V2 Red stereo pair (4 channels total: LF and HMF per side).

| CH | Speaker | Band | Load | Connector | NL4 pin |
|----|---------|------|------|-----------|---------|
| 1 | Air Motion V2 L — LF | LF | 8 Ω | Phoenix → NL4 #1 | 1+/1− |
| 2 | Air Motion V2 L — HMF | HMF | 8 Ω | Phoenix → NL4 #2 | 2+/2− |
| 3 | Air Motion V2 R — LF | LF | 8 Ω | Phoenix → NL4 #1 | 1+/1− |
| 4 | Air Motion V2 R — HMF | HMF | 8 Ω | Phoenix → NL4 #2 | 2+/2− |

**I/O:** IEC C20 mains · Phoenix 12-pin input block · Phoenix 8-pin speaker output block · RJ45

### §5.4 Bias V3 #1 — "air ten v3"

**Serial:** 341130 · **IP:** 192.168.10.13 · **Gain:** −8 dB · **Delay:** 28.23 ms

| CH | Speaker | Zone | Load | Connector |
|----|---------|------|------|-----------|
| 1 | Airten V3 L | FOH fill | 8 Ω | NL4 |
| 2 | Airten V3 R | FOH fill | 8 Ω | NL4 |

**I/O:** IEC C20 mains · XLR-F inputs · 2× NL4 speaker outs · 3× XLR-M line outs · RJ45 AESOP

### §5.5 Bias Q2 #1 — "DJ Monitors"

**Serial:** 951058 · **IP:** 192.168.10.12 · **Gain:** −4 dB · **Delay:** 0 ms  
**Signal source:** CQ-12T MonOut (−32 dB) via XLR-M → Phoenix adapter

| CH | Speaker | Zone | Load | Connector |
|----|---------|------|------|-----------|
| 1 | Air Vantage L | DJ booth monitor | 8 Ω | Phoenix → NL4 |
| 2 | Air Vantage R | DJ booth monitor | 8 Ω | Phoenix → NL4 |
| 3 | Venu 215 V2 L | DJ booth sub | 4 Ω | Phoenix → Phoenix |
| 4 | Venu 215 V2 R | DJ booth sub | 4 Ω | Phoenix → Phoenix |

**I/O:** IEC C20 mains · Phoenix 12-pin input block · Phoenix 8-pin speaker output block · RJ45

### §5.6 Bias V9 — "DELAY SUBS" (**OFFLINE**)

**Status:** Physically present in Pos 5. CPC 45A mains breaker OFF. All NL4 speaker cables disconnected. All XLR inputs disconnected.  
**Do not reconnect without a dedicated commissioning session.** The Armonía preset for this unit (originally planned for Stasys Xair LF duty) is obsolete — the system was rebalanced to run without it.

---

## §6 Loudspeaker Inventory

### §6.1 VOID Air Motion V2 Red — FOH Mains (×2)

| Spec | Value |
|------|-------|
| Zone | FOH mains |
| Qty | 2 (L + R) |
| Amplifier | Bias Q2 #2 (bi-amp, 4 channels) |
| Frequency response | 140 Hz – 20 kHz ±3 dB |
| Impedance | LF 8 Ω / HMF 8 Ω (separate) |
| Power handling (AES) | 500 W LF / 250 W HMF |
| Max SPL | 132 dB continuous · 138 dB peak |
| Connectors | 2× NL4 (NL4#1 = LF, NL4#2 = HMF) |
| Enclosure | Fibreglass Kevlar composite |
| Finish | Custom Red |
| Weight | 35.4 kg |
| Manual | `02-equipment-manuals/speakers/VOID-Air-Motion-V2-User-Guide.pdf` |

### §6.2 VOID Airten V3 — FOH Fill (×2)

| Spec | Value |
|------|-------|
| Zone | FOH fill |
| Qty | 2 (L + R) |
| Amplifier | Bias V3 #1 CH1/CH2 |
| Frequency response | 60 Hz – 20 kHz ±3 dB |
| Impedance | 4 Ω |
| Power handling (AES) | 500 W |
| Max SPL | 131 dB peak (1 m) |
| Connectors | 2× speakON NL4 (in + link-out) |
| Enclosure | Moulded fibreglass reinforced plastic |
| Dimensions | H 681 mm × W 303 mm × D 366 mm |
| Weight | 20 kg |
| Manual | `02-equipment-manuals/speakers/VOID-Airten-V3-User-Manual-v2.1.pdf` (UG10517 V2.1) |

### §6.3 VOID Stasys Xair — Subs (×6)

Six Xair cabinets — 2 outside subs (V3 #2 direct) + 4 middle subs (Q5). Each driven individually on its own amplifier channel at 4 Ω. No parallel wiring.

| Spec | Value |
|------|-------|
| Zone | Outside subs (L-3, R-3) + middle sub cluster (L-1, L-2, R-1, R-2) |
| Qty | 6 total |
| Amplifiers | V3 #2 CH1/CH2 (outside) · Q5 CH1–CH4 (middle) |
| Frequency response | 30 Hz – 180 Hz ±3 dB |
| Impedance | 4 Ω per cabinet |
| Power handling (AES) | 3,200 W |
| Max SPL | 139 dB continuous · 145 dB peak |
| Connectors | 2× NL4 (NL4 In + NL4 Link-Out) |
| Enclosure | Cast aluminium frame + plywood |
| Weight | 130 kg |
| Manual | `02-equipment-manuals/speakers/VOID-Stasys-Xair-User-Guide.pdf` |

> ⚠️ Xair impedance note: Rev 1.0 of this spec showed 6× Xair wired in parallel pairs at 2 Ω on V3 channels. That configuration was superseded — the Q5 was added to provide 4 individual channels, and V3 #2 was reconfigured for 2 individual outside subs. All 6 Xair are now at 4 Ω per channel.

### §6.4 VOID Air Vantage — DJ Booth Monitors (×2)

| Spec | Value |
|------|-------|
| Zone | DJ booth monitors |
| Qty | 2 (L + R) |
| Amplifier | Bias Q2 #1 CH1/CH2 |
| Frequency response | 140 Hz – 20 kHz ±3 dB |
| Impedance | 8 Ω |
| Power handling (AES) | 500 W |
| Max SPL | 126 dB continuous · 132 dB peak |
| Connectors | 1× NL4 |
| Weight | 23.5 kg |
| Manual | `02-equipment-manuals/speakers/VOID-Air-Vantage-User-Guide.pdf` |

### §6.5 VOID Venu 215 V2 — DJ Booth Sub (×2)

| Spec | Value |
|------|-------|
| Zone | DJ booth sub |
| Qty | 2 (L + R) |
| Amplifier | Bias Q2 #1 CH3/CH4 |
| Frequency response | 38 Hz – 160 Hz ±3 dB |
| Impedance | 4 Ω |
| Power handling (AES) | 1,000 W |
| Max SPL | 134 dB continuous · 140 dB peak |
| Connectors | Phoenix 8-pin recessed + NL4 recessed (both present) |
| Current connection | Phoenix (Q2 #1 CH3/CH4 Phoenix → Phoenix) |
| Weight | 62.5 kg |
| Manual | `02-equipment-manuals/speakers/VOID-Venu-V2-Series-User-Guide.pdf` |

### §6.6 Turbosound Athens TCS-AN — Entrance (×2)

| Spec | Value |
|------|-------|
| Zone | Entrance / foyer |
| Qty | 2 (L + R) |
| Type | Self-powered (active) — Klark Teknik Class-D 2,500 W + DSP |
| Amplifier | None — self-contained |
| Signal source | CQ-12T BakFil output (−34 dB) via XLR, ~20 m run |
| Input connectors | Dual XLR/TRS combo + digital input |
| Submodel | TBC — TCS122/xx-AN (12") or TCS152/xx-AN (15") · verify rear type-plate on site (Issue #4) |
| Firmware | V2.3 (Aug 2020) — update via `TURBOSOUND_UsbUpdate_V2.3.exe` (Windows) |
| QSG | `02-equipment-manuals/speakers/Turbosound-Athens-TCS-AN-Series-QSG.pdf` (pending download — Issue #4) |

---

## §7 Signal Flow — Amplifier-to-Loudspeaker Load Table

Armonía-verified, March 2026.

| Zone | Cabinet | Qty | Amp | CH | Ω | Power (AES) | Connector |
|------|---------|-----|-----|----|---|------------|-----------|
| FOH mains LF L | Air Motion V2 Red L | 1 | Q2 #2 | 1 | 8 | 500 W | Phoenix→NL4 #1 |
| FOH mains HMF L | Air Motion V2 Red L | 1 | Q2 #2 | 2 | 8 | 250 W | Phoenix→NL4 #2 |
| FOH mains LF R | Air Motion V2 Red R | 1 | Q2 #2 | 3 | 8 | 500 W | Phoenix→NL4 #1 |
| FOH mains HMF R | Air Motion V2 Red R | 1 | Q2 #2 | 4 | 8 | 250 W | Phoenix→NL4 #2 |
| FOH fill L | Airten V3 L | 1 | V3 #1 | 1 | 8 | 500 W | NL4 |
| FOH fill R | Airten V3 R | 1 | V3 #1 | 2 | 8 | 500 W | NL4 |
| Outside sub L | Stasys Xair L-3 | 1 | V3 #2 | 1 | 4 | 3,200 W | NL4 |
| Outside sub R | Stasys Xair R-3 | 1 | V3 #2 | 2 | 4 | 3,200 W | NL4 |
| Middle sub L-1 | Stasys Xair L-1 | 1 | Q5 | 1 | 4 | 3,200 W | NL4 |
| Middle sub L-2 | Stasys Xair L-2 | 1 | Q5 | 2 | 4 | 3,200 W | NL4 |
| Middle sub R-1 | Stasys Xair R-1 | 1 | Q5 | 3 | 4 | 3,200 W | NL4 |
| Middle sub R-2 | Stasys Xair R-2 | 1 | Q5 | 4 | 4 | 3,200 W | NL4 |
| DJ booth monitor L | Air Vantage L | 1 | Q2 #1 | 1 | 8 | 500 W | Phoenix→NL4 |
| DJ booth monitor R | Air Vantage R | 1 | Q2 #1 | 2 | 8 | 500 W | Phoenix→NL4 |
| DJ booth sub L | Venu 215 V2 L | 1 | Q2 #1 | 3 | 4 | 1,000 W | Phoenix→Phoenix |
| DJ booth sub R | Venu 215 V2 R | 1 | Q2 #1 | 4 | 4 | 1,000 W | Phoenix→Phoenix |
| Entrance L | Athens TCS-AN L | 1 | Self-powered | — | — | 2,500 W int. | XLR (BakFil) |
| Entrance R | Athens TCS-AN R | 1 | Self-powered | — | — | 2,500 W int. | XLR (BakFil) |

**Totals:** 18 loudspeakers · 16 active amp channels in use / 16 available (V3#1: 2, V3#2: 2, Q5: 4, Q2#1: 4, Q2#2: 4) · V9: 0/2 (offline)

---

## §8 Per-Amplifier DSP Configuration

Armonía gains and delays confirmed March 2026.

| Amp | Armonía Label | S/N | IP | Gain | Delay | Preset notes |
|-----|--------------|-----|----|------|-------|-------------|
| Bias V3 #2 | "Outside Subs" | 341132 | 192.168.10.14 | −3 dB | 0 ms | Xair sub preset, 4 Ω mode per channel |
| Bias Q5 | "Subs Middle" | 777758 | 192.168.10.10 | 0 dB | 0 ms | Xair sub preset, 4 ch, 4 Ω each |
| Bias Q2 #2 | "Air Motion" | 00543758 | 192.168.10.11 | +0.5 dB | 1.0 ms | Bi-amp preset: LF on CH1/CH3, HMF on CH2/CH4 |
| Bias V3 #1 | "air ten v3" | 341130 | 192.168.10.13 | −8 dB | 28.23 ms | Airten V3 full-range preset |
| Bias Q2 #1 | "DJ Monitors" | 951058 | 192.168.10.12 | −4 dB | 0 ms | Air Vantage full-range CH1/CH2 · Venu sub CH3/CH4 |
| Bias V9 | "DELAY SUBS" | — | — | N/A | N/A | **OFFLINE — preset obsolete** |

**Armonía network:** 192.168.10.x, star topology, dedicated switch recommended  
**Armonía software:** ArmoníaPlus 2.8 (latest) — update control PC before any DSP changes  
**Note:** 2 Ω operating mode is **not used** on any amplifier in this system.

---

## §9 Connector & Adapter Cable Requirements

| # | Type | From | To | Qty | Notes |
|---|------|------|----|-----|-------|
| 1 | XLR-M → XLR-F | DJM-V10 Master Out L/R | CQ-12T CH1/CH2 | 2 | Standard balanced XLR |
| 2 | XLR-M → XLR-F | DJM-V10 Booth Out L/R | CQ-12T CH3/CH4 | 2 | Standard balanced XLR |
| 3 | XLR-M → XLR-F | CQ-12T Main L/R | SP2120 Input L/R | 2 | Standard balanced XLR |
| 4 | XLR-M → XLR-F | SP2120 Output L/R | V3 #2 Input L/R | 2 | Standard balanced XLR |
| 5 | XLR-M → Phoenix signal | V3 #2 Line Out 1 | Q5 Input | 1 | XLR-M → Phoenix MC adapter |
| 6 | XLR-M → Phoenix signal | V3 #2 Line Out 2 | Q2 #2 Input | 1 | XLR-M → Phoenix MC adapter |
| 7 | XLR-M → XLR-F | V3 #2 Line Out 3 | V3 #1 Input | 1 | Standard balanced XLR |
| 8 | NL4 speaker | V3 #2 CH1 | Stasys Xair L-3 | 1 | 4 Ω individual |
| 9 | NL4 speaker | V3 #2 CH2 | Stasys Xair R-3 | 1 | 4 Ω individual |
| 10 | NL4 speaker | Q5 CH1 | Stasys Xair L-1 | 1 | 4 Ω individual |
| 11 | NL4 speaker | Q5 CH2 | Stasys Xair L-2 | 1 | 4 Ω individual |
| 12 | NL4 speaker | Q5 CH3 | Stasys Xair R-1 | 1 | 4 Ω individual |
| 13 | NL4 speaker | Q5 CH4 | Stasys Xair R-2 | 1 | 4 Ω individual |
| 14 | Phoenix→NL4 | Q2 #2 CH1 | Air Motion V2 L LF (NL4 #1) | 1 | NL4 pins 1+/1− |
| 15 | Phoenix→NL4 | Q2 #2 CH2 | Air Motion V2 L HMF (NL4 #2) | 1 | NL4 pins 2+/2− |
| 16 | Phoenix→NL4 | Q2 #2 CH3 | Air Motion V2 R LF (NL4 #1) | 1 | NL4 pins 1+/1− |
| 17 | Phoenix→NL4 | Q2 #2 CH4 | Air Motion V2 R HMF (NL4 #2) | 1 | NL4 pins 2+/2− |
| 18 | NL4 speaker | V3 #1 CH1 | Airten V3 L | 1 | 8 Ω |
| 19 | NL4 speaker | V3 #1 CH2 | Airten V3 R | 1 | 8 Ω |
| 20 | XLR-M → Phoenix signal | CQ-12T MonOut L/R | Q2 #1 Input L/R | 2 | XLR-M → Phoenix MC adapter |
| 21 | Phoenix→NL4 | Q2 #1 CH1 | Air Vantage L | 1 | 8 Ω |
| 22 | Phoenix→NL4 | Q2 #1 CH2 | Air Vantage R | 1 | 8 Ω |
| 23 | Phoenix→Phoenix | Q2 #1 CH3 | Venu 215 V2 L | 1 | 4 Ω |
| 24 | Phoenix→Phoenix | Q2 #1 CH4 | Venu 215 V2 R | 1 | 4 Ω |
| 25 | XLR (or TRS→XLR) ~20 m | CQ-12T BakFil L/R | Athens entrance L/R | 2 | Long cable run to entrance |

**Total signal cables:** 25  
See `07-tech-pack/cable-schedule.md` for the full 41-cable schedule including network, power, and Pro DJ Link.

---

## §10 Power Distribution

| Device | Rack Pos | Mains Connector | Max Current | Recommended Breaker | Status |
|--------|----------|----------------|-------------|--------------------|----|
| Drawmer SP2120 | 2 | IEC C14 (PDU) | <1 A | PDU | ✅ Active |
| Bias V3 #1 | 3 | IEC C20 | 16 A | 20 A C/D-curve | ✅ Active |
| Bias Q2 #1 | 4 | IEC C20 | 16 A | 20 A C/D-curve | ✅ Active |
| ~~Bias V9~~ | 5 | CPC 45A | 32 A | **BREAKER OFF — OFFLINE** | ❌ Offline |
| Bias Q2 #2 | 6 | IEC C20 | 16 A | 20 A C/D-curve | ✅ Active |
| Bias V3 #2 | 7 | IEC C20 | 16 A | 20 A C/D-curve | ✅ Active |
| Bias Q5 | — | Phoenix 5-pin | TBC | TBC | ✅ Active — ⚠️ confirm (Issue #7) |
| Allen & Heath CQ-12T | — | IEC C14 | <3 A | PDU | ✅ Active |

---

## §11 Network

| Device | IP | Port | Subnet | Notes |
|--------|-----|------|--------|-------|
| Bias V3 #2 | 192.168.10.14 | Armonía RJ45 | 192.168.10.x | Armonía control network |
| Bias Q5 | 192.168.10.10 | Armonía RJ45 | 192.168.10.x | Armonía control network |
| Bias Q2 #2 | 192.168.10.11 | Armonía RJ45 | 192.168.10.x | Armonía control network |
| Bias V3 #1 | 192.168.10.13 | Armonía RJ45 | 192.168.10.x | Armonía control network |
| Bias Q2 #1 | 192.168.10.12 | Armonía RJ45 | 192.168.10.x | Armonía control network |
| Allen & Heath CQ-12T | 169.254.182.156 | RJ45 | Link-local | Separate from Armonía subnet |
| CDJ-3000 ×4 + DJM-V10 | Dynamic | RJ45 | Pro DJ Link LAN | Separate network segment |

---

## §12 Open Issues

| # | Issue | Severity | Status | Action |
|---|-------|----------|--------|--------|
| 2 | Rack elevation photo ≠ documented spec order; V9 still physically present | 🟡 Medium | Open | Take new rack photo for tech pack (blocked on Rack Elevation SVG) |
| 3 | CQ-12T Out4/5/6 at 0 dB — purpose unknown | 🟡 Medium | Open | Verify on-site before patching |
| 4 | Athens TCS-AN exact submodel (TCS122 vs TCS152 variant) not confirmed | 🟡 Medium | Open | Photograph rear type-plate on next site visit |
| 5 | No production contact details | 🟢 Low | Open | Add to available rider |
| 7 | Bias Q5 mains connector is Phoenix 5-pin — circuit breaker rating not confirmed | 🟡 Medium | Open | Verify breaker spec on-site; Q5 manual downloaded for reference |

---

## §13 Reference Documents

| Document | Location | Status |
|----------|----------|--------|
| VOID Airten V3 User Manual V2.1 (UG10517) | `02-equipment-manuals/speakers/VOID-Airten-V3-User-Manual-v2.1.pdf` | ✅ |
| VOID Air Motion V2 User Guide | `02-equipment-manuals/speakers/VOID-Air-Motion-V2-User-Guide.pdf` | ✅ |
| VOID Air Vantage User Guide | `02-equipment-manuals/speakers/VOID-Air-Vantage-User-Guide.pdf` | ✅ |
| VOID Stasys Xair User Guide | `02-equipment-manuals/speakers/VOID-Stasys-Xair-User-Guide.pdf` | ✅ |
| VOID Venu V2 Series User Guide | `02-equipment-manuals/speakers/VOID-Venu-V2-Series-User-Guide.pdf` | ✅ |
| Turbosound Athens TCS-AN QSG | `02-equipment-manuals/speakers/Turbosound-Athens-TCS-AN-Series-QSG.pdf` | ❌ Pending |
| Bias Q5 User Guide V1.1 | `02-equipment-manuals/amplifiers/Bias_Q5_user_guide_v1.1.pdf` | ✅ |
| Bias V3/V9 User Manual | `02-equipment-manuals/amplifiers/Bias_V3_V9_user_manual.pdf` | ✅ |
| Bias Q2/Q1/D1 User Guide | `02-equipment-manuals/amplifiers/Bias_Q2Q1D1_user_guide.pdf` | ✅ |
| Drawmer SP2120 Operators Manual | `02-equipment-manuals/processing/sp2120_operators_manual.pdf` | ✅ |
| Allen & Heath CQ-12T User Guide V1.2 | `02-equipment-manuals/mixers/Allen-Heath_CQ-12T_user_guide_v1.2.pdf` | ✅ |
| Allen & Heath CQ-12T Datasheet | `02-equipment-manuals/mixers/Allen-Heath_CQ-12T_datasheet.pdf` | ✅ |
| Pioneer CDJ-3000 Instruction Manual | `02-equipment-manuals/dj-gear/Pioneer_CDJ-3000_manual.pdf` | ✅ |
| Pioneer DJM-V10 Instruction Manual | `02-equipment-manuals/dj-gear/Pioneer_DJM-V10_manual.pdf` | ✅ |
| Firmware & Software Changelog | `06-reference-docs/firmware-changelog.md` | ✅ |
| Armonía Wiring PDF (March 2026) | `01-source-documents/nomad-wiring-18spk-armonia.pdf` | ✅ |

---

## §14 Changes from Rev 1.0 (Feb 2026)

Rev 1.0 documented a pre-commissioning design. Major corrections in Rev 2.0:

| Section | Rev 1.0 (incorrect) | Rev 2.0 (correct) |
|---------|--------------------|--------------------|
| Mixer | Generic "DJ mixer" (no model) | Allen & Heath CQ-12T (3 outputs: Main LR, MonOut −32 dB, BakFil −34 dB) |
| Amp count | 6 active + no offline | 5 active + V9 offline |
| V9 status | Active — "drives Air Motion LF" | **OFFLINE** — all channels disconnected, CPC 45A breaker off |
| Q2 #3 | Listed in Pos 8 driving Cyclone 2 | **Never installed** — does not exist |
| Bias Q5 | Not mentioned | Added — 4-channel sub amp for middle cluster |
| Q2 #2 role | "DJ monitor amp" — Air Vantage L/R | "Air Motion bi-amp" — Air Motion V2 L+R LF+HMF (4ch) |
| Q2 #1 role | "Air Motion HMF amp" | "DJ Monitors" — Air Vantage + Venu 215 |
| Air Motion amp assignment | V9 #1 LF + Q2 #1 HMF (split) | Q2 #2 bi-amp 4ch (single amp, all 4 bands) |
| Xair count | 4 cabinets | **6 cabinets** (L-3, R-3, L-1, L-2, R-1, R-2) |
| Xair wiring | 2 Ω parallel pairs on V3 channels | **4 Ω individual** per channel — no parallel wiring |
| V3 #1 role | "Left sub array amp" | "Airten V3 amp" (FOH fill) |
| V3 #2 role | "Right sub array amp" | "Outside Subs + signal distribution hub" |
| Signal distribution | "Possible external splitter or V3 line out daisy-chain" | **V3 #2 pre-DSP line outs** — 3× XLR-M → Q5, Q2 #2, V3 #1; **no external splitter** |
| Venu 215 zone | "Outboard flank subs" on V3 amps | **DJ booth sub** on Q2 #1 CH3/CH4 |
| Cyclone 2 fills | Listed (×2, on Q2 #3) | **Never installed** — removed from spec |
| Airten V3 | Not mentioned | Added — 2 cabinets, FOH fill, V3 #1 CH1/CH2 |
| Athens speakers | Not mentioned | Added — 2 cabinets, entrance, self-powered, CQ-12T BakFil |
| Total loudspeakers | 14 | **18** |
| Total amp channels | 12 of 18 in use | **16 of 16 in use** |
