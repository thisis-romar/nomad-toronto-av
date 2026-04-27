# Nomad Toronto — AV System Documentation

**Claude.ai project:** [Nomad AV Rack](https://claude.ai/project/019dcacc-4479-778d-9be8-6d705f5b113d)  
**Last updated:** 2026-04-27  
**Status:** Tech pack in progress — see TECH-PACK-STATUS.md  
**Source docs:** `01-source-documents/nomad-system-spec.pdf` (Feb 2026) · `01-source-documents/nomad-wiring-18spk-armonia.pdf` (March 2026, Armonía-verified)

---

## Goal

Complete venue tech pack for **Nomad Toronto** — two deliverable documents:
1. **Internal Technical Reference** — full system documentation for in-house production team
2. **Technical Available Rider** — artist-facing PDF for touring DJ/live act bookings

---

## System Overview (as-built, Armonía-verified March 2026 + CQ-12T confirmed April 2026)

```
4× Pioneer CDJ-3000 ──Pro DJ Link──▶ Pioneer DJM-V10
                                            │
                         ┌── Master XLR L/R (CH1+2 "Music")  ┐
                         └── Booth XLR L/R  (CH3+4 "MonIn")  ┘
                                            │
                                   Allen & Heath CQ-12T
                                   (replaced Yamaha MG12, April 2026)
                                            │
      ┌── Main LR XLR ──▶ Drawmer SP2120 ──▶ Bias V3 #2 ──┬──▶ Xair L-3 (CH1, 4Ω)
      │                                                     └──▶ Xair R-3 (CH2, 4Ω)
      │                                      V3 #2 line outs:
      │                                        ├──▶ Bias Q5  ──▶ Xair L-1/2, R-1/2 (4ch, 4Ω each)
      │                                        ├──▶ Bias Q2 #2 ──▶ Air Motion L+R (bi-amp, 4ch)
      │                                        └──▶ Bias V3 #1 ──▶ Airten V3 L/R
      │
      ├── MonOut (−32 dB) ──▶ Bias Q2 #1 ──▶ Air Vantage L/R (CH1/2) + Venu 215 L/R (CH3/4)
      └── BakFil (−34 dB) ──▶ Athens entrance (self-powered, XLR feed)
```

---

## CQ-12T Configuration (confirmed 2026-04-26)

**Firmware:** 1.2.1 r4213 | **IP:** 169.254.182.156 (link-local) | **MAC:** 00:04:c4:14:9c:b5

| CH | Label | Source | Notes |
|---|---|---|---|
| 1+2 | Music | DJM-V10 Master Out XLR L/R | Stereo link, 15 dB gain, AG Auto ON |
| 3+4 | MonIn | DJM-V10 Booth Out XLR L/R | Orange — booth/monitor feed |
| 5–10 | Ip5–Ip10 | Unassigned | Available for guest inputs |
| Main LR | → SP2120 | 0 dB | FOH signal path |
| MonOut | → Q2 #1 | −32 dB | DJ booth monitors + Venu 215 |
| BakFil | → Athens zone | −34 dB | Entrance / back-fill (self-powered speakers) |
| Out4/5/6 | Unassigned | 0 dB | ⚠️ Status unknown — confirm if in use |

---

## Amplifier Assignments (Armonía network: 192.168.10.x — verified March 2026)

| Amp | Label (Armonía) | Serial | IP | Zone | CH Assignment | Gain / Delay |
|---|---|---|---|---|---|---|
| Bias V3 #2 | "Outside Subs" | 341132 | 192.168.10.14 | FOH | CH1: Xair L-3 · CH2: Xair R-3 | −3 dB / 0 ms |
| Bias Q5 | "Subs Middle" | 777758 | 192.168.10.10 | FOH | CH1: Xair L-1 · CH2: Xair L-2 · CH3: Xair R-1 · CH4: Xair R-2 | 0 dB / 0 ms |
| Bias Q2 #2 | "Air Motion" | 00543758 | 192.168.10.11 | FOH | CH1: AM L LF · CH2: AM L HMF · CH3: AM R LF · CH4: AM R HMF | +0.5 dB / 1.0 ms |
| Bias V3 #1 | "air ten v3" | 341130 | 192.168.10.13 | FOH | CH1: Airten L · CH2: Airten R | −8 dB / 28.23 ms |
| Bias Q2 #1 | "DJ Monitors" | 951058 | 192.168.10.12 | Booth | CH1: AV L · CH2: AV R · CH3: Venu L · CH4: Venu R | −4 dB / 0 ms |
| ~~Bias V9~~ | "DELAY SUBS" | — | — | **OFFLINE** — all channels disconnected, CPC 45A off | — | — |

**Signal distribution:** SP2120 → V3 #2 (XLR). V3 #2 line outs (3× XLR-M) distribute to Q5, Q2 #2, and V3 #1. No external splitter — the V3's pre-DSP line outputs are the distribution point.

---

## Speaker System — 18 Total

| Zone | Qty | Model | Amp | Ch per cab | Impedance | Power (AES) |
|---|---|---|---|---|---|---|
| FOH mains | 2 | VOID Air Motion V2 Red | Q2 #2 (bi-amp, 4ch) | 2 × NL4 | LF 8Ω · HMF 8Ω | 500 W LF · 250 W HMF |
| FOH fill | 2 | VOID Airten V3 | V3 #1 | 1 × NL4 | 8Ω | TBC |
| Sub cluster (outside) | 2 | VOID Stasys Xair | V3 #2 (1 per ch) | 1 × NL4 | **4Ω** | 3,200 W |
| Sub cluster (middle) | 4 | VOID Stasys Xair | Q5 (1 per ch) | 1 × NL4 | **4Ω** | 3,200 W |
| DJ booth monitors | 2 | VOID Air Vantage | Q2 #1 CH1/2 | 1 × NL4 | 8Ω | 500 W |
| DJ booth sub | 2 | VOID Venu 215 V2 | Q2 #1 CH3/4 | 1 × NL4 or Phoenix | 4Ω | 1,000 W |
| Entrance | 2 | Athens (model TBC) | Self-powered (XLR from CQ-12T BakFil) | — | — | — |

> **Xair impedance note:** Each of the 6 Stasys Xair cabinets is driven individually on its own amplifier channel at 4Ω. The February 2026 spec showed pairs paralleled at 2Ω on V3 channels — this configuration was superseded when the Q5 was added, giving 4 dedicated channels for the middle cluster. ~~Issue #1 resolved.~~

---

## Speaker Specifications (from nomad-system-spec.pdf Rev 1.0)

| Model | Freq Response | Impedance | Power (AES) | Max SPL | Connectors | Weight |
|---|---|---|---|---|---|---|
| Air Motion V2 Red | 140 Hz – 20 kHz ±3 dB | LF 8Ω / HMF 8Ω | 500 W LF / 250 W HMF | 132 dB cont · 138 dB peak | 2× NL4 (NL4#1=LF, NL4#2=HMF) | 35.4 kg |
| Stasys Xair | 30 Hz – 180 Hz ±3 dB | 4Ω | 3,200 W | 139 dB cont · 145 dB peak | 2× NL4 (in + link-out) | 130 kg |
| Venu 215 V2 | 38 Hz – 160 Hz ±3 dB | 4Ω | 1,000 W | 134 dB cont · 140 dB peak | Phoenix + NL4 (both present, recessed panel) | 62.5 kg |
| Air Vantage | 140 Hz – 20 kHz ±3 dB | 8Ω | 500 W | 126 dB cont · 132 dB peak | 1× NL4 | 23.5 kg |
| Airten V3 | TBC | TBC | TBC | TBC | TBC | TBC |
| Athens | Self-powered | — | — | — | XLR in | — |

---

## Connector & Adapter Cable Requirements (Armonía-verified)

| Type | Qty | Connection |
|---|---|---|
| XLR-M → Phoenix signal | 2 | V3 #2 line out → Q2 #2 Air Motion inputs |
| XLR-M → Phoenix signal | 2 | CQ-12T MonOut → Q2 #1 DJ Monitor inputs |
| Phoenix → NL4 speaker | 4 | Q2 #2 CH1–4 → Air Motion LF/HMF NL4 #1/#2 |
| Phoenix → NL4 speaker | 2 | Q2 #1 CH1/2 → Air Vantage NL4 |
| Phoenix → Phoenix speaker | 2 | Q2 #1 CH3/4 → Venu 215 V2 Phoenix |
| TRS → XLR 20m | 1 | ~~MG12 Group Out → Athens~~ (now CQ-12T BakFil XLR → Athens) |

**Connector types summary:**
- V3 amps: XLR-F inputs · XLR-M line outs · NL4 speaker outs · IEC C20 mains
- Q5: XLR-F inputs · NL4 speaker outs · **Phoenix 5-pin mains** (non-standard)
- Q2 amps: Phoenix 12-pin input block · Phoenix 8-pin speaker out · IEC C20 mains
- V9 (offline): XLR/TRS combo inputs · NL4 speaker outs · **CPC 45A mains** (hardwired)

---

## Power Distribution

| Amp | Position | Mains Connector | Max Current | Recommended Breaker |
|---|---|---|---|---|
| Bias V3 #1 | Pos 3 | IEC C20 | 16A | 20A C/D-curve |
| Bias Q2 #1 | Pos 4 | IEC C20 | 16A | 20A C/D-curve |
| ~~Bias V9~~ | Pos 5 | CPC 45A | 32A | **OFFLINE — breaker off** |
| Bias Q2 #2 | Pos 6 | IEC C20 | 16A | 20A C/D-curve |
| Bias V3 #2 | Pos 7 | IEC C20 | 16A | 20A C/D-curve |
| Bias Q5 | — | Phoenix 5-pin | TBC | TBC |
| Drawmer SP2120 | Pos 2 | IEC (115/230V sw) | <1A | PDU (9VA) |

---

## Conversations

| Date | Conversation | Files | Status |
|---|---|---|---|
| 2026-02-20 | [SVG Rack Elevation — Methodology](https://claude.ai/chat/77927477-ddf9-4a6e-8507-652816224db0) | 4 | Reference only |
| 2026-02-21 | [Nomad Amp Rack Cable Schedule](https://claude.ai/chat/81ef8190-238f-4f37-901d-ead397b7a6e1) | 17 | ⚠️ Stale — predates CQ-12T |
| 2026-02-23 | [19-Inch Rack Standards](https://claude.ai/chat/fb56aa22-37a8-4633-825c-6dd1c91f4db5) | 1 | General reference |
| 2026-03-16 | [Audio Rack Equipment Audit](https://claude.ai/chat/61c49787-7fd9-4227-ae32-2f3c8301d7f6) | 75 | ⚠️ Sub count corrected; impedance issue now resolved |
| 2026-03-16 | [Yamaha MG12 Validation](https://claude.ai/chat/bfe45378-1df0-4646-b3a1-dde53b1db8c4) | 1 | ❌ Superseded by CQ-12T |
| 2026-03-24 | [CQ12 Mixer Audit ← **most current**](https://claude.ai/chat/c8999358-0d6d-42d2-8abd-d5e1b06ff2d8) | 10 | ⚠️ Signal flow JSX only, not exported |
| 2026-03-28 | [Ma2 MCP Audit](https://claude.ai/chat/7927f9e3-7bbe-454b-ab40-46ff6a3412b5) | 0 | Not AV-related |

---

## Open Issues

| # | Issue | Severity | Status | Action |
|---|---|---|---|---|
| ~~1~~ | ~~6× Xair at 1.33Ω on V3 channels~~ | ~~🔴 Critical~~ | ✅ **Resolved** — each Xair driven individually at 4Ω (Q5 provides 4 channels) | No action needed |
| 2 | Rack elevation photo ≠ documented spec order; V9 still physically present (offline) | 🟡 Medium | Open | Take new rack photo |
| 3 | Out4/5/6 on CQ-12T at 0 dB — purpose unknown | 🟡 Medium | Open | Confirm if in use |
| 4 | Athens entrance speaker model not documented | 🟢 Low | Open | Identify model on-site |
| 5 | No production contact details | 🟢 Low | Open | Add to available rider |
| 6 | Airten V3 PDF missing — wrong URL in asset registry | 🟢 Low | Open | Source correct PDF |
| 7 | Q5 mains connector is Phoenix 5-pin — confirm circuit/breaker spec | 🟡 Medium | Open | Verify on-site |

---

## Source Document Reconciliation

| Claim | Feb 2026 Spec | March 2026 Wiring (Armonía) | April 2026 Current | Verdict |
|---|---|---|---|---|
| Xair count | 4 (2 stacks of 2) | 6 (L-3, R-3, L-1, L-2, R-1, R-2) | 6 | ✅ Wiring/current correct |
| Xair impedance | 2Ω (parallel pairs) | 4Ω (individual per channel) | 4Ω | ✅ Resolved — no impedance issue |
| Air Motion amp | V9 #1 (LF) + Q2 #1 (HMF) | Q2 #2 bi-amp 4ch | Q2 #2 bi-amp | ✅ Wiring/current correct |
| Airten amp | Not in spec | V3 #1 | V3 #1 | ✅ Wiring/current correct |
| V9 status | Active (LF mains) | OFFLINE, disconnected | OFFLINE (physically present) | ✅ Wiring/current correct |
| Q2 #1 gain | N/A | −4 dB / 0 ms | −4 dB | ✅ Updated (was 0.5 dB in README — wrong) |
| V3 #2 gain | N/A | −3 dB / 0 ms | −3 dB | ✅ Added (was missing from README) |
| Mixer | DJM-V10 → MG12 → SP2120 | DJM-V10 → MG12 → SP2120 | DJM-V10 → **CQ-12T** → SP2120 | ✅ CQ-12T confirmed April 2026 |
| Athens routing | Not mentioned | MG12 Group 1 Out → Athens | CQ-12T BakFil → Athens | ✅ Updated with CQ-12T |
| Venu 215 zone | Flank subs (V3 #2) | Booth (Q2 #1 CH3/4) | Booth | ✅ Fixed — was "Sub flank" in README |
| Cyclone 2 / Q2 #3 | Mid-room fills planned | Not present | Not installed | ❌ Never installed — removed from docs |
| Signal splitter | External splitter assumed | V3 #2 line outputs (no splitter) | V3 #2 line outputs | ✅ Fixed — no separate splitter box |

---

## Notes on Downloaded Files

- Images downloaded as **JPEG** (converted from WebP via `--convert-images`)
- PDFs: original bytes via `document_pdf` variant
- DOCX: not downloadable via API — `.NOT_DOWNLOADABLE.txt` placeholders written
