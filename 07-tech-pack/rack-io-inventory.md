---
title: Nomad Toronto — Rack I/O Inventory (Power · Data · Audio)
description: Connector-level inventory of every input and output on every device in the Nomad amp rack, plus the CQ-12T and DJ booth sources that terminate into it. Each port lists connector type, channel/port name, and what it is patched to.
version: 1.0.0
created: 2026-08-11T00:00:00Z
last_updated: 2026-08-11T00:00:00Z
---

# Nomad Toronto — Rack I/O Inventory

**Venue:** NØMAD Toronto · 725 Queen Street East, Toronto, ON
**Scope:** Every physical connector on every device in the amplifier rack (U1–U10), plus the
Allen & Heath CQ-12T and the DJ booth sources whose cables terminate in the rack.
**Method:** Port lists are taken from the manufacturer manuals held in `02-equipment-manuals/`
(cited per device). Patch assignments and channel names are taken from the as-built documents
(`01-source-documents/nomad-system-spec-v2.md`, `07-tech-pack/cable-schedule.md`).
**Status:** Desk-verified against manuals — **not** re-verified at the rack. Items where the manual
and the as-built documents disagree are listed in §12 and must be confirmed on-site.

---

## §0 How to read this document

Every device gets up to four tables:

| Table | Covers |
|-------|--------|
| ⚡ **Power** | Mains inlets, DC inlets, remote-on/off and external-voltage terminals |
| 🔗 **Data / Control** | Ethernet, Dante/AESOP, USB, SD, serial, GPI/GPO, footswitch, smart card |
| 🔊 **Audio inputs** | Every analog/digital audio input socket on the device |
| 🔊 **Audio outputs** | Every line-level and speaker-level output socket on the device |

**Status column:**

| Mark | Meaning |
|------|---------|
| ✅ | Patched and in service |
| ⭕ | Physically present, not patched (spare capacity) |
| ⚠️ | Patched but unverified / disputed — see §12 |
| ❌ | Disconnected / out of service |

**Channel name** is the label the system uses — the silkscreen label where the device has one,
otherwise the Armonía / CQ-12T scene name in use at the venue.

---

## §1 Rack elevation — device index

| U | Device | Role | Section |
|---|--------|------|---------|
| U1 | 1U blank | — | — |
| U2 | Drawmer SP2120 | Stereo limiter / speaker protector | [§2](#2-drawmer-sp2120--u2) |
| U3 | Bias V3 #1 "air ten v3" | FOH fill amp | [§3](#3-bias-v3-1--air-ten-v3--u3) |
| U4 | Bias Q2 #1 "DJ Monitors" | Booth monitor + booth sub amp | [§4](#4-bias-q2-1--dj-monitors--u4) |
| U5 | Bias V9 "DELAY SUBS" | **OFFLINE** | [§5](#5-bias-v9--delay-subs--u5--offline) |
| U6 | Bias Q2 #2 "Air Motion" | FOH mains bi-amp | [§6](#6-bias-q2-2--air-motion--u6) |
| U7 | Bias V3 #2 "Outside Subs" | Outside sub amp + signal hub | [§7](#7-bias-v3-2--outside-subs--u7) |
| U8 | Bias Q5 "Subs Middle" | Middle sub amp (4 ch) | [§8](#8-bias-q5--subs-middle--u8) |
| U9–U10 | Tripp Lite PDU | Control-power distribution | [§9](#9-tripp-lite-pdu--u9u10) |
| — | Allen & Heath CQ-12T | Matrix mixer (booth, feeds the rack) | [§10](#10-allen--heath-cq-12t--dj-booth) |
| — | Pioneer DJM-V10 / CDJ-3000 ×4 | Sources (booth, feed the rack) | [§11](#11-dj-booth-sources--appendix) |

---

## §2 Drawmer SP2120 — U2

Analog 2-channel speaker protector. No network, no digital I/O.
*Source: `02-equipment-manuals/processing/sp2120_operators_manual.pdf` — Installation/Audio
Connections (p. 4), Data Specification (p. 8).*

### ⚡ Power

| Port | Connector | Channel name | Direction | Connected to | Status |
|------|-----------|--------------|-----------|--------------|--------|
| Mains inlet | IEC C14, 115/230 V switchable | `MAINS` | In | Tripp Lite PDU (U9–U10) | ✅ |
| Fuse holder | 20 mm, T100 mA @115 V / T50 mA @230 V | — | — | Integral to inlet | ✅ |

Draw: 9 VA.

### 🔗 Data / Control

| Port | Connector | Notes |
|------|-----------|-------|
| — | None | Analog hardware; front-panel key lock is the only access control |

### 🔊 Audio inputs

| Port | Connector | Channel name | From | Level | Status |
|------|-----------|--------------|------|-------|--------|
| Input L | XLR-F balanced (1 = GND, 2 = hot, 3 = cold), 20 kΩ, max +21 dBu | `Input L` | CQ-12T `Main L` | 0 dB | ✅ |
| Input R | XLR-F balanced, 20 kΩ, max +21 dBu | `Input R` | CQ-12T `Main R` | 0 dB | ✅ |

### 🔊 Audio outputs

| Port | Connector | Channel name | To | Level | Status |
|------|-----------|--------------|----|-------|--------|
| Output L | XLR-M balanced, 100 Ω, max +14 dBu | `Output L` | Bias V3 #2 `ANALOG CH1 IN` | variable | ✅ |
| Output R | XLR-M balanced, 100 Ω, max +14 dBu | `Output R` | Bias V3 #2 `ANALOG CH2 IN` | variable | ✅ |

> Optional output isolation transformers can be fitted; a tamper-proof bracket (traps the XLRs)
> is available and recommended where noise-abatement compliance is enforced.

---

## §3 Bias V3 #1 — "air ten v3" — U3

**S/N 341130 · IP 192.168.10.13 · Gain −8 dB · Delay 28.23 ms**
*Source: `02-equipment-manuals/amplifiers/Bias_V3_V9_user_manual.pdf` — Front and rear panels
(pp. 4–5), Connections §7.2–7.7 (pp. 8–10).*

### ⚡ Power

| Port | Connector | Channel name | Direction | Connected to | Status |
|------|-----------|--------------|-----------|--------------|--------|
| Mains inlet | IEC C20 (takes a C19 cord), 100–240 V, max mains current user-set to 16 A | `MAINS` | In | Dedicated circuit, 20 A C/D-curve | ✅ |
| V Ext | Phoenix MCV 1,5/2-G-3,81, 2-pin, 12 VDC 1 A | `Vext` | In | — (keeps DSP/remote-on alive without mains) | ⭕ |

### 🔗 Data / Control

| Port | Connector | Channel name | Direction | Connected to | Status |
|------|-----------|--------------|-----------|--------------|--------|
| AESOP primary 1 | RJ45 (rear) — Ethernet + 2× AES3 streams | `DATA PORT` | Bi | Armonía network (192.168.10.x) | ✅ |
| AESOP primary 2 | RJ45 (rear) | `DATA PORT` | Bi | — (loop/repeat spare) | ⭕ |
| AESOP secondary 1–2 | 2× RJ45 (front) — data only, no AES3 | — | Bi | — | ⭕ |
| Smart Card slot | Front card slot | — | — | Preset/config card | ⭕ |
| Link button | Rear pushbutton | `LINK ON/OFF` | — | Bridges Input 1 to both channels | ⚠️ see §12-D1 |

### 🔊 Audio inputs

| Port | Connector | Channel name | From | Status |
|------|-----------|--------------|------|--------|
| Input 1 | XLR-F balanced | `ANALOG CH1 IN` | Bias V3 #2 line output (XLR) | ✅ |
| Input 2 | XLR-F balanced, switchable to AES3 by adjacent `AES/EBU–ANALOG` toggle | `ANALOG CH2 IN / AES3` | Fed by LINK from Input 1 (to confirm) | ⚠️ |

### 🔊 Audio outputs

| Port | Connector | Channel name | To | Load | Status |
|------|-----------|--------------|----|------|--------|
| Line out 1 | XLR-M, pre-DSP replica of Input 1 | `ANALOG CH1 OUT` | — | — | ⭕ |
| Line out 2 | XLR-M, pre-DSP replica of Input 2 (muted in AES3 mode) | `ANALOG CH2 OUT` | — | — | ⭕ |
| Speaker out 1 | Neutrik NL4MD speakON (1+/2+ bridged to +, 1−/2− bridged to −) | `OUT1` = CH1 | VOID Airten V3 **L** (FOH fill) | 8 Ω | ✅ |
| Speaker out 2 | Neutrik NL4MD speakON | `OUT2` = CH2 | VOID Airten V3 **R** (FOH fill) | 8 Ω | ✅ |

---

## §4 Bias Q2 #1 — "DJ Monitors" — U4

**S/N 951058 · IP 192.168.10.12 · Gain −4 dB · Delay 0 ms**
4-channel amp. Every audio connection is a Phoenix terminal block — no XLR, no speakON.
*Source: `02-equipment-manuals/amplifiers/Bias_Q2Q1D1_user_guide.pdf` — rear-panel legend
(pp. 8–9), package list (p. 5).*

### ⚡ Power

| Port | Connector | Channel name | Direction | Connected to | Status |
|------|-----------|--------------|-----------|--------------|--------|
| Mains inlet | IEC C20 (takes a C19 cord), 100–240 V | `MAINS` | In | Dedicated circuit, 20 A C/D-curve | ✅ |
| Remote On/Off | Phoenix MC 1,5/4-ST-3,81, 4-pin (5–24 VDC differential, never >28 V) | `GPI — REMOTE ON / REMOTE OFF` | In | — | ⭕ |

### 🔗 Data / Control

| Port | Connector | Channel name | Direction | Connected to | Status |
|------|-----------|--------------|-----------|--------------|--------|
| Ethernet | RJ45 | `ETHERNET` | Bi | Armonía network (192.168.10.12) | ✅ |
| Dante | RJ45 (DSP+D models only) | `DANTE` | Bi | — | ⚠️ see §12-D7 |
| Remote Level | Phoenix MC 1,5/12-ST-3,81, 12-pin (G/↓/+ per channel) | `INPUTS — LEVEL` | In | — (external attenuators) | ⭕ |
| GPO / Alarm | Phoenix block, per-channel contact + common (CH1–CH4) | `ALARM` | Out | — (fault reporting) | ⭕ |
| Config DIP switches | 8-way DIP: gain 26/29/32/35 dB, CH1 Master, BRK Save, NRG Save, USR A/B, 2 Ω | `CONFIG` | — | Set locally | ✅ |
| Output DIP switches | 8-way DIP: Lo-Z/Hi-Z, 100 V/70 V, HPF 35 Hz/70 Hz | — | — | Lo-Z (A) expected | ⚠️ confirm |
| Serial port | Front, service only | — | — | — | ⭕ |

### 🔊 Audio inputs

Single 12-pin block carries all four channels (3 poles each: `+`, `−`, `⏚`).

| Pins | Connector | Channel name | From | Status |
|------|-----------|--------------|------|--------|
| CH1 | Phoenix MC 1,5/12-ST-3,81 `INPUTS — LINE` | `CH1` | CQ-12T `MonOut L` (−32 dB) via TRS/XLR → Phoenix adapter | ✅ |
| CH2 | same block | `CH2` | CQ-12T `MonOut R` (−32 dB) via adapter | ✅ |
| CH3 | same block | `CH3` | Source not documented — paralleled from CH1 in the connector, or DSP-routed in Armonía | ⚠️ see §12-D5 |
| CH4 | same block | `CH4` | Source not documented — as CH3 from `MonOut R` | ⚠️ see §12-D5 |

### 🔊 Audio outputs

Single 8-pin block carries all four channels (`+`/`−` per channel).

| Pins | Connector | Channel name | To | Load | Status |
|------|-----------|--------------|----|------|--------|
| CH1 ± | Phoenix PC 5/8-STF1-7,62 `OUTPUTS` | `CH1` | VOID Air Vantage **L** (booth monitor) via Phoenix → NL4 | 8 Ω | ✅ |
| CH2 ± | same block | `CH2` | VOID Air Vantage **R** (booth monitor) via Phoenix → NL4 | 8 Ω | ✅ |
| CH3 ± | same block | `CH3` | VOID Venu 215 V2 **L** (booth sub), Phoenix → Phoenix | 4 Ω | ✅ |
| CH4 ± | same block | `CH4` | VOID Venu 215 V2 **R** (booth sub), Phoenix → Phoenix | 4 Ω | ✅ |

---

## §5 Bias V9 — "DELAY SUBS" — U5 — ❌ OFFLINE

Physically present, breaker off, all inputs and outputs disconnected. Listed here so the panel is
documented if it is ever recommissioned or removed.
*Source: `02-equipment-manuals/amplifiers/Bias_V3_V9_user_manual.pdf` — rear panel (p. 5), §6.3 (p. 7).*

### ⚡ Power

| Port | Connector | Channel name | Direction | Connected to | Status |
|------|-----------|--------------|-----------|--------------|--------|
| Mains inlet | **AMP CPC 45A** industrial (hard-wired — not IEC), max 32 A | `MAINS` | In | Dedicated circuit — **breaker OFF** | ❌ |
| V Ext | Phoenix 2-pin, 12 VDC 1 A | `Vext` | In | — | ❌ |

### 🔗 Data / Control

| Port | Connector | Channel name | Status |
|------|-----------|--------------|--------|
| AESOP primary ×2 | RJ45 (rear) | `DATA PORT` | ❌ disconnected |
| AESOP secondary ×2 | RJ45 (front, data only) | — | ❌ |
| Smart Card slot | Front | — | ❌ |

### 🔊 Audio inputs / outputs

| Port | Connector | Channel name | Status |
|------|-----------|--------------|--------|
| Input 1 | XLR/TRS combo, balanced | `ANALOG IN1` | ❌ |
| Input 2 | XLR/TRS combo, switchable to AES3 | `ANALOG IN2 / AES/EBU` | ❌ |
| Line outputs | **None** — the V9 has no line outs (unlike the V3) | — | — |
| Speaker out 1 | Neutrik NL4MD speakON | `OUT1` = CH1 | ❌ |
| Speaker out 2 | Neutrik NL4MD speakON | `OUT2` = CH2 | ❌ |

> Do not reconnect without a dedicated commissioning session — the stored Armonía preset is obsolete.

---

## §6 Bias Q2 #2 — "Air Motion" — U6

**S/N 00543758 · IP 192.168.10.11 · Gain +0.5 dB · Delay 1.0 ms**
Same panel as Q2 #1 (§4). Bi-amps the Air Motion V2 Red pair across all four channels.

### ⚡ Power

| Port | Connector | Channel name | Direction | Connected to | Status |
|------|-----------|--------------|-----------|--------------|--------|
| Mains inlet | IEC C20, 100–240 V | `MAINS` | In | Dedicated circuit, 20 A C/D-curve | ✅ |
| Remote On/Off | Phoenix 4-pin | `GPI` | In | — | ⭕ |

### 🔗 Data / Control

| Port | Connector | Channel name | Connected to | Status |
|------|-----------|--------------|--------------|--------|
| Ethernet | RJ45 | `ETHERNET` | Armonía network (192.168.10.11) | ✅ |
| Dante | RJ45 (DSP+D only) | `DANTE` | — | ⚠️ §12-D7 |
| Remote Level | Phoenix 12-pin | `INPUTS — LEVEL` | — | ⭕ |
| GPO / Alarm | Phoenix block, CH1–CH4 + common | `ALARM` | — | ⭕ |
| Config / Output DIPs | 2× 8-way DIP | `CONFIG` | Bi-amp preset set in Armonía | ✅ |

### 🔊 Audio inputs

| Pins | Connector | Channel name | From | Status |
|------|-----------|--------------|------|--------|
| CH1 | Phoenix 12-pin `INPUTS — LINE` | `CH1` | Bias V3 #2 line out (L) via XLR-M → Phoenix adapter | ✅ |
| CH2 | same block | `CH2` | Fed from the same L leg (HMF band) | ⚠️ §12-D5 |
| CH3 | same block | `CH3` | Bias V3 #2 line out (R) leg | ⚠️ §12-D5 |
| CH4 | same block | `CH4` | Same R leg (HMF band) | ⚠️ §12-D5 |

### 🔊 Audio outputs

| Pins | Connector | Channel name | To | Band | Load | Status |
|------|-----------|--------------|----|------|------|--------|
| CH1 ± | Phoenix PC 5/8 `OUTPUTS` | `CH1` | Air Motion V2 **L** — NL4 #1, pins 1+/1− | LF | 8 Ω | ✅ |
| CH2 ± | same block | `CH2` | Air Motion V2 **L** — NL4 #2, pins 2+/2− | HMF | 8 Ω | ✅ |
| CH3 ± | same block | `CH3` | Air Motion V2 **R** — NL4 #1, pins 1+/1− | LF | 8 Ω | ✅ |
| CH4 ± | same block | `CH4` | Air Motion V2 **R** — NL4 #2, pins 2+/2− | HMF | 8 Ω | ✅ |

---

## §7 Bias V3 #2 — "Outside Subs" — U7

**S/N 341132 · IP 192.168.10.14 · Gain −3 dB · Delay 0 ms**
The system's signal distribution point — its pre-DSP line outputs feed the downstream amps.
Same panel as V3 #1 (§3).

### ⚡ Power

| Port | Connector | Channel name | Direction | Connected to | Status |
|------|-----------|--------------|-----------|--------------|--------|
| Mains inlet | IEC C20, 100–240 V, max 16 A | `MAINS` | In | Dedicated circuit, 20 A C/D-curve | ✅ |
| V Ext | Phoenix 2-pin, 12 VDC 1 A | `Vext` | In | — | ⭕ |

### 🔗 Data / Control

| Port | Connector | Channel name | Connected to | Status |
|------|-----------|--------------|--------------|--------|
| AESOP primary 1 | RJ45 (rear) | `DATA PORT` | Armonía network (192.168.10.14) | ✅ |
| AESOP primary 2 | RJ45 (rear) | `DATA PORT` | — | ⭕ |
| AESOP secondary ×2 | RJ45 (front, data only) | — | — | ⭕ |
| Smart Card slot | Front | — | — | ⭕ |

### 🔊 Audio inputs

| Port | Connector | Channel name | From | Status |
|------|-----------|--------------|------|--------|
| Input 1 | XLR-F balanced | `ANALOG CH1 IN` | Drawmer SP2120 `Output L` | ✅ |
| Input 2 | XLR-F balanced (AES3-switchable) | `ANALOG CH2 IN / AES3` | Drawmer SP2120 `Output R` | ✅ |

### 🔊 Audio outputs

| Port | Connector | Channel name | To | Load | Status |
|------|-----------|--------------|----|------|--------|
| Line out 1 | XLR-M, pre-DSP replica of Input 1 | `ANALOG CH1 OUT` | Documented as feeding Bias Q5 input (via XLR-M → Phoenix) | ⚠️ §12-D1 |
| Line out 2 | XLR-M, pre-DSP replica of Input 2 | `ANALOG CH2 OUT` | Documented as feeding Bias Q2 #2 input (via XLR-M → Phoenix) | ⚠️ §12-D1 |
| *(no third line out exists)* | — | documented as `Line Out 3` → Bias V3 #1 | **Not a physical port** | ❌ §12-D1 |
| Speaker out 1 | Neutrik NL4MD speakON | `OUT1` = CH1 | VOID Stasys Xair **L-3** (outside sub L) | 4 Ω | ✅ |
| Speaker out 2 | Neutrik NL4MD speakON | `OUT2` = CH2 | VOID Stasys Xair **R-3** (outside sub R) | 4 Ω | ✅ |

---

## §8 Bias Q5 — "Subs Middle" — U8

**S/N 777758 · IP 192.168.10.10 · Gain 0 dB · Delay 0 ms**
4-channel amp with XLR inputs and **two** speakON outputs (two channels per connector).
*Source: `02-equipment-manuals/amplifiers/Bias_Q5_user_guide_v1.1.pdf` — Panels B & C (p. 5),
AC mains supply §4.4 (pp. 13–14), Connections §6 (p. 16), Appendix B specifications (p. 23).*

### ⚡ Power

| Port | Connector | Channel name | Direction | Connected to | Status |
|------|-----------|--------------|-----------|--------------|--------|
| AC mains | **Phoenix PC 5/5-STF1-7,62**, 5-pole flying plug (3PH: `N L3 L2 L1 ⏚` / 1PH: `N L ⏚`) | `MAINS` | In | Terminal box + sectioning breaker. Manual recommends **16 A C/D-curve, 10 kA** single-phase — installed rating still unconfirmed | ⚠️ §12-D6 |
| Remote ON/OFF | Phoenix 2-pin, +12 VDC | `REM ON/OFF` | In | — | ⭕ |

### 🔗 Data / Control

| Port | Connector | Channel name | Direction | Connected to | Status |
|------|-----------|--------------|-----------|--------------|--------|
| Ethernet primary | Neutrik etherCON RJ45 | `Primary ETH1` | Bi | Armonía network (192.168.10.10) | ✅ |
| Ethernet secondary | Neutrik etherCON RJ45 | `Secondary ETH2` | Bi | — (daisy-chain / loop spare) | ⭕ |
| USB | Front USB port | — | Bi | Service / config | ⭕ |
| Wi-Fi | Front on/off switch (internal radio) | — | — | Confirm disabled in a fixed install | ⚠️ confirm |

### 🔊 Audio inputs

| Port | Connector | Channel name | From | Status |
|------|-----------|--------------|------|--------|
| Analog in 1 | XLR-F balanced, 20 kΩ, +27 dBu acceptance | `ANALOG IN 1` (CH1) | Bias V3 #2 `ANALOG CH1 OUT` via XLR-M → Phoenix adapter *(adapter spec unconfirmed — the Q5 input is XLR, not Phoenix)* | ⚠️ §12-D2 |
| Analog in 2 | XLR-F balanced | `ANALOG IN 2` (CH2) | Same feed, split/linked | ⚠️ |
| Analog in 3 | XLR-F balanced | `ANALOG IN 3` (CH3) | Same feed, split/linked | ⚠️ |
| Analog in 4 | XLR-F balanced | `ANALOG IN 4` (CH4) | Same feed, split/linked | ⚠️ |
| AES3 in 1–2 | XLR-F, AES3 (110 Ω) | `AES3 IN 1-2` | — | ⭕ |
| AES3 in 3–4 | XLR-F, AES3 (110 Ω) | `AES3 IN 3-4` | — | ⭕ |

### 🔊 Audio outputs

| Port | Connector | Channel name | To | Load | Status |
|------|-----------|--------------|----|------|--------|
| Output 1 | speakON — **carries two channels**: pins 1+/1− = CH1, 2+/2− = CH2 | `OUT1 CH1-2` | Stasys Xair **L-1** (CH1) and **L-2** (CH2) | 4 Ω each | ⚠️ §12-D2 |
| Output 2 | speakON — pins 1+/1− = CH3, 2+/2− = CH4 | `OUT2 CH3-4` | Stasys Xair **R-1** (CH3) and **R-2** (CH4) | 4 Ω each | ⚠️ §12-D2 |

> Channels are bridgeable per pair — **not** used here; all four run single-ended at 4 Ω.

---

## §9 Tripp Lite PDU — U9–U10

Rack-mount PDU feeding control-class equipment only (SP2120 + Armonía control PC). The five
active amplifiers are **not** on this PDU — each is on its own panel circuit.
*No manual for this unit is held in the repo; the entries below are read off the rack photos
(`03-rack-photos/amp-rack/`) and the Rev 1.0 spec, and need a model number confirmed on site.*

### ⚡ Power

| Port | Connector | Channel name | Direction | Connected to | Status |
|------|-----------|--------------|-----------|--------------|--------|
| Mains feed | Line cord to venue control circuit | `IN` | In | Control circuit (<5 A total draw) | ⚠️ confirm plug type |
| Outlets | NEMA 5-15R ×n (count and switched/unswitched grouping unconfirmed) | `OUT 1…n` | Out | Drawmer SP2120, Armonía control PC | ⚠️ confirm |
| Breaker / master switch | Front rocker + breaker | — | — | — | ✅ |

### 🔗 Data / Control

| Port | Connector | Notes |
|------|-----------|-------|
| — | Unknown | If this is a monitored/switched Tripp Lite model there may be an RJ45 or USB management port. Not identifiable from the photos — confirm on site. |

---

## §10 Allen & Heath CQ-12T — DJ booth

**FW 1.2.1 r4213 · IP 169.254.182.156 (link-local) · MAC 00:04:c4:14:9c:b5**
Not rack-mounted, but it is the source of every audio cable that lands in the rack.
*Source: `02-equipment-manuals/mixers/Allen-Heath_CQ-12T_user_guide_v1.2.pdf` §4 Connections
(pp. 13–15) and `Allen-Heath_CQ-12T_datasheet.pdf` (pp. 1, 4).*

### ⚡ Power

| Port | Connector | Channel name | Direction | Connected to | Status |
|------|-----------|--------------|-----------|--------------|--------|
| DC inlet | **12 VDC, 5 A, centre-positive, with locking clip** | `DC IN` | In | Supplied external switching PSU | ✅ |
| PSU mains inlet | IEC on the PSU brick (site notes record C14) | — | In | Booth outlet / PDU | ✅ |

Max draw 35 W.

### 🔗 Data / Control

| Port | Connector | Channel name | Direction | Connected to | Status |
|------|-----------|--------------|-----------|--------------|--------|
| Network | RJ45 100BASE-T (CQ acts as client) | `NETWORK` | Bi | Link-local — **not** on the Armonía subnet | ✅ |
| USB-A | USB Type-A (host) | `USB-A` | Bi | Stereo record/playback, data, firmware | ⭕ |
| USB-B | USB Type-B, USB 2.0 class-compliant, 16×16 ch audio + MIDI | `USB-B` | Bi | — | ⭕ |
| SD card | Full-size SDHC slot (≤32 GB, UHS-I C10), 16-ch multitrack | `SD` | Bi | — | ⭕ |
| Bluetooth | Internal, BT 4.1 stereo playback | `BT` | In | — | ⭕ |
| Footswitch | ¼" TS (single) or TRS (dual) jack | `FOOTSWITCH` | In | — | ⭕ |

### 🔊 Audio inputs

| Port | Connector | Channel name | From | Gain | Status |
|------|-----------|--------------|------|------|--------|
| Input 1 | XLR-F, recallable preamp, +48 V | `Ch1 — Music L` | DJM-V10 `MASTER1 L` (XLR) | +15 dB, AG Auto ON | ✅ |
| Input 2 | XLR-F | `Ch2 — Music R` | DJM-V10 `MASTER1 R` (XLR) | +15 dB, stereo-linked | ✅ |
| Input 3 | XLR-F | `Ch3 — MonIn L` | DJM-V10 `BOOTH L` (**TRS** — see §12-D3) | 0 dB | ⚠️ |
| Input 4 | XLR-F | `Ch4 — MonIn R` | DJM-V10 `BOOTH R` (**TRS**) | 0 dB | ⚠️ |
| Input 5 | XLR-F (**XLR only — not a combi socket**) | `Ch5 — Ip5` | — | 0 dB | ⭕ |
| Inputs 6–10 | XLR/TRS combi, −20 dB fixed pad on the TRS path | `Ch6–Ch10 — Ip6…Ip10` | — | 0 dB | ⭕ |
| ST IN | 2× ¼" TRS balanced, normalled L/mono | `ST` | — | — | ⭕ |
| USB / SD / BT | Digital | `USB`, `SD`, `BT` | — | — | ⭕ |

**Guest-input capacity:** 6 mono channels free (Ch5 XLR-only + Ch6–Ch10 combi) plus the stereo
ST IN pair.

### 🔊 Audio outputs

| Port | Connector | Channel name | To | Level | Status |
|------|-----------|--------------|----|-------|--------|
| Main L | XLR-M balanced, +4 dBu nominal, +22 dBu max | `Main L` | Drawmer SP2120 `Input L` | 0 dB | ✅ |
| Main R | XLR-M balanced | `Main R` | Drawmer SP2120 `Input R` | 0 dB | ✅ |
| Out *n* (pair) | Balanced **¼" TRS** (Out 1–6 are TRS on the CQ-12T) | `MonOut L/R` | Bias Q2 #1 `CH1`/`CH2` via adapter | −32 dB | ⚠️ §12-D3 |
| Out *n* (pair) | Balanced ¼" TRS | `BakFil L/R` | Turbosound Athens L/R at entrance (~20 m run) | −34 dB | ⚠️ §12-D3 |
| Out 4/5/6 | Balanced ¼" TRS | unnamed | Unknown — sitting at 0 dB | ⚠️ do not patch (GH #2) |
| Headphones | Stereo ¼" TRS | `PHONES` | Booth headphones | — | ⭕ |

> The physical socket numbers (Out 1–6) carrying `MonOut` and `BakFil` are not recorded anywhere in
> the documentation set — record them at the mixer on the next visit so the aux labels map to sockets.

---

## §11 DJ booth sources — appendix

Not in the rack; listed because their cables terminate at the CQ-12T and, through it, the rack.

### Pioneer DJM-V10 (×1)
*Source: `02-equipment-manuals/dj-gear/Pioneer_DJM-V10_manual.pdf` — Part names, rear panel (pp. 9–11).*

| Class | Port | Connector | Channel name | In use |
|-------|------|-----------|--------------|--------|
| ⚡ | AC IN | IEC mains inlet | `AC IN` | ✅ |
| 🔗 | LINK | RJ45 100BASE-TX | `LINK` | ✅ Pro DJ Link to the 4 CDJs (via hub) |
| 🔗 | MIDI OUT | 5-pin DIN | `MIDI OUT` | ⭕ |
| 🔗 | USB (top panel) | USB-B ×2 | `USB A/B` | ⭕ |
| 🔊 in | DIGITAL IN CH | RCA coaxial, per channel | `DIGITAL IN` | ✅ CDJ digital feeds |
| 🔊 in | LINE | RCA, per channel | `LINE` | ⭕ |
| 🔊 in | PHONO + SIGNAL GND | RCA + ground post | `PHONO` | ⭕ |
| 🔊 in | MIC1 / MIC2 | XLR-or-¼" TRS combo / ¼" TRS | `MIC1`, `MIC2` | ⭕ |
| 🔊 in | MULTI I/O EXT1/EXT2 RETURN | ¼" TS | `RETURN` | ⭕ |
| 🔊 out | MASTER1 | Balanced XLR-M L/R | `MASTER1` | ✅ → CQ-12T Ch1/Ch2 |
| 🔊 out | MASTER2 | RCA L/R | `MASTER2` | ⭕ |
| 🔊 out | BOOTH | **¼" TRS** L/R | `BOOTH` | ✅ → CQ-12T Ch3/Ch4 (§12-D3) |
| 🔊 out | REC OUT | RCA L/R | `REC OUT` | ⭕ |
| 🔊 out | DIGITAL MASTER OUT | XLR (AES/EBU) | `DIGITAL MASTER OUT` | ⭕ |
| 🔊 out | MULTI I/O EXT1/EXT2 SEND | ¼" TS | `SEND` | ⭕ |
| 🔊 out | PHONES A / B | ¼" TRS (top / front) | `PHONES A/B` | ✅ |

### Pioneer CDJ-3000 (×4)
*Source: `02-equipment-manuals/dj-gear/Pioneer_CDJ-3000_manual.pdf` — rear panel (p. 17), specifications (p. 83).*

Per unit:

| Class | Port | Connector | Channel name | In use |
|-------|------|-----------|--------------|--------|
| ⚡ | AC IN | IEC mains inlet | `AC IN` | ✅ |
| 🔗 | LINK | RJ45 | `LINK` | ✅ Pro DJ Link |
| 🔗 | USB | USB Type-B (to PC/Mac) | `USB` | ⭕ |
| 🔊 out | AUDIO OUT L/R | RCA, 2.0 Vrms | `AUDIO OUT` | ⭕ (digital preferred) |
| 🔊 out | DIGITAL OUT | RCA coaxial S/PDIF, 96 kHz/24-bit | `DIGITAL OUT` | ✅ → DJM-V10 `DIGITAL IN` |

---

## §12 Discrepancies found during this audit

Each item is a conflict between a manufacturer manual in this repo and the as-built documentation.
The manual wins on *what connectors exist*; only a site visit settles *what is actually patched*.

| # | Finding | Evidence | Impact | Action |
|---|---------|----------|--------|--------|
| **D1** | **The Bias V3 has two line outputs, not three.** The spec and cable schedule describe `Line Out 1/2/3` on V3 #2 feeding Q5, Q2 #2 and V3 #1. | Bias V3/V9 manual §7.3 p. 8 ("line out … via a couple of XLR connectors") and rear-panel legend p. 4 items 7 & 9 (`ANALOG CH1 OUT`, `ANALOG CH2 OUT`). | The third feed (to V3 #1, driving both Airten fills) must come from somewhere else — a Y-split on one line out, or a different source entirely. Cables 17–19 in the cable schedule cannot all originate at V3 #2 as documented. | Trace the V3 #1 input cable back to its actual source at the next visit. |
| **D2** | **The Bias Q5 has two speakON outputs, not four.** `OUT1` carries CH1 (1+/1−) and CH2 (2+/2−); `OUT2` carries CH3 and CH4. | Q5 user guide Panel B p. 5, items I & J; §6.4 p. 16. | Cable schedule rows 22–25 list four discrete NL4 runs from "Q5 CH1…CH4". Physically this is two 4-pole runs, or two runs into NL4 splitters/link-outs at the Xair cabinets. | Re-draw the Q5 → middle-sub cabling as 2 runs + breakouts; confirm the split point on site. |
| **D3** | **TRS, not XLR, at three points.** CQ-12T `Out 1–6` are balanced ¼" TRS (XLR outputs exist only on the CQ-20B), and the DJM-V10 `BOOTH` outputs are ¼" TRS. | CQ-12T datasheet p. 4 ("Outputs 1-6: Balanced, 1/4\" TRS Jack") and user guide p. 14; DJM-V10 manual p. 10 item 12. | Cable schedule rows 3, 4, 11, 12, 13, 14 are all specified with XLR-M at the source end. Those six cables need a TRS source end (TRS→XLR-F, or TRS→Phoenix for the Q2 #1 feed). | Correct the cable schedule connector column; verify the adapters actually fitted. |
| **D4** | **CQ-12T Ch5 is an XLR-only socket**, not a combi. Inputs 1–5 are XLR; 6–10 are XLR/TRS combi. | CQ-12T user guide p. 13; datasheet p. 1 ("5x XLR Mic/Line Input Sockets, 5x XLR/Jack 'Combi'"). | The rider and system overview advertise "CH5–CH10 … Mic/Line XLR-TRS combo". A guest arriving with a ¼" TRS source can use Ch6–Ch10 or ST IN, not Ch5. | Fix the wording in `system-overview.md` and `available-rider.md`. |
| **D5** | **Q2 channels 3 and 4 have no documented input source.** Both Q2s drive four loudspeaker channels but the documentation shows only a stereo pair arriving at the 12-pin line-input block. | Q2 rear-panel legend p. 8 (Line Input block is 4 channels × 3 poles); cable schedule rows 11–12 and 18 show one stereo feed per amp. | Either the connector is wired with CH1→CH3 and CH2→CH4 paralleled internally, or Armonía is routing one input pair to all four DSP channels. Both are valid; neither is recorded. | Photograph the Phoenix line-input block wiring and export the Armonía input-routing page (ties into GH #6). |
| **D6** | **Q5 breaker recommendation is now known.** The manual specifies a sectioning breaker: 16 A, C or D curve, 10 kA for single-phase (P+N+E). | Q5 user guide §4.4 p. 14. | Open issue GH #5 / spec Issue #7 can be closed once the *installed* breaker is read off the panel and compared to this figure. | Read the breaker rating on site. |
| **D7** | **Dante port presence unconfirmed.** The Q2 has a Dante RJ45 only on DSP+D variants. | Q2/Q1/D1 user guide p. 8 items 16–17; p. 6 (Dante networking on DSP+D models). | Determines whether the system has any spare digital audio transport. | Check the rear panel of both Q2s for a populated Dante port. |
| **D8** | **No network switch is documented in the rack.** Cat5 runs leave the rack to an unidentified switch or router. | Rev 1.0 spec p. 4 ("Position 9 — Empty / TBD. No network switch was identified in the photos"); rack photos `03-rack-photos/amp-rack/`; cable schedule rows 36–40 reference a "network switch / router" with no location. | Six control links (five Armonía + CQ-12T) terminate at an undocumented device. Single point of failure for all DSP control. | Locate, photograph and add the switch to the rack elevation and cable schedule. |

---

## §13 Connector count summary (rack only)

| Device | ⚡ Power | 🔗 Data / control | 🔊 Audio in | 🔊 Audio out | Amp ch (used/total) |
|--------|---------|------------------|------------|-------------|---------------------|
| Drawmer SP2120 | 1 (IEC C14) | 0 | 2 (XLR-F) | 2 (XLR-M) | — |
| Bias V3 #1 | 2 (IEC C20 + Vext) | 4 RJ45 + card slot | 2 (XLR-F) | 2 line (XLR-M) + 2 speakON | 2 / 2 |
| Bias Q2 #1 | 2 (IEC C20 + GPI 4-pin) | 2 RJ45 + level/alarm blocks + serial | 1 block (4 ch) | 1 block (4 ch) | 4 / 4 |
| Bias V9 ❌ | 2 (CPC 45A + Vext) | 4 RJ45 + card slot | 2 (combo) | 2 speakON, no line out | 0 / 2 |
| Bias Q2 #2 | 2 (IEC C20 + GPI 4-pin) | 2 RJ45 + level/alarm blocks + serial | 1 block (4 ch) | 1 block (4 ch) | 4 / 4 |
| Bias V3 #2 | 2 (IEC C20 + Vext) | 4 RJ45 + card slot | 2 (XLR-F) | 2 line (XLR-M) + 2 speakON | 2 / 2 |
| Bias Q5 | 2 (Phoenix 5-pin + rem 2-pin) | 2 etherCON + USB | 4 analog XLR + 2 AES3 XLR | 2 speakON (4 ch) | 4 / 4 |
| Tripp Lite PDU | 1 in + *n* out | TBC | — | — | — |
| **Total in service** | | | | | **16 / 16 active ch** (+2 offline) |

**Spare capacity in the rack today:** 4 spare line outputs (V3 #1 ×2, and whichever V3 #2 line out
is not in use once D1 is resolved), 6 unused digital inputs on the Q5 (4 analog XLR + 2 AES3 pairs
share the same channels), 2 offline V9 amp channels, and all GPI/GPO/remote-level terminals.

---

## §14 Sources

| Device | Document |
|--------|----------|
| Bias V3 / V9 | `02-equipment-manuals/amplifiers/Bias_V3_V9_user_manual.pdf` (V1.0) |
| Bias Q2 / Q1 / D1 | `02-equipment-manuals/amplifiers/Bias_Q2Q1D1_user_guide.pdf` |
| Bias Q5 | `02-equipment-manuals/amplifiers/Bias_Q5_user_guide_v1.1.pdf` (UG11068-1.1) |
| Drawmer SP2120 | `02-equipment-manuals/processing/sp2120_operators_manual.pdf` |
| Allen & Heath CQ-12T | `02-equipment-manuals/mixers/Allen-Heath_CQ-12T_user_guide_v1.2.pdf` · `…_datasheet.pdf` |
| Pioneer DJM-V10 | `02-equipment-manuals/dj-gear/Pioneer_DJM-V10_manual.pdf` |
| Pioneer CDJ-3000 | `02-equipment-manuals/dj-gear/Pioneer_CDJ-3000_manual.pdf` |
| As-built patch data | `01-source-documents/nomad-system-spec-v2.md` (Rev 2.0) · `07-tech-pack/cable-schedule.md` |
| Rack layout | `07-tech-pack/rack-elevation.svg` · `03-rack-photos/amp-rack/` |
| Superseded (panel descriptions only) | `01-source-documents/nomad-system-spec.pdf` (Rev 1.0 — routing content obsolete) |

---

*EMBLEM PROJECTS INC. · 2026-08-11 · Desk audit from manufacturer manuals — §12 items require site verification*
