# Nomad Toronto — AV System Documentation

**Claude.ai project:** [Nomad AV Rack](https://claude.ai/project/019dcacc-4479-778d-9be8-6d705f5b113d)  
**Last updated:** 2026-04-26  
**Status:** Tech pack in progress — see TECH-PACK-STATUS.md

---

## Goal

Complete venue tech pack for **Nomad Toronto** — two deliverable documents:
1. **Internal Technical Reference** — full system documentation for in-house production team
2. **Technical Available Rider** — artist-facing PDF for touring DJ/live act bookings

---

## System Overview (as-built, 2026-03-24)

```
4× Pioneer CDJ-3000 ──Pro DJ Link──▶ Pioneer DJM-V10
                                            │
                         ┌── Master XLR L/R (CH1+2 "Music")  ┐
                         └── Booth XLR L/R  (CH3+4 "MonIn")  ┘
                                            │
                                   Allen & Heath CQ-12T
                                            │
      ┌── Main LR XLR ──▶ Drawmer SP2120 ──▶ 1×3 XLR splitter ──┬──▶ Bias V3 #2 ──▶ Xair L-3/R-3
      │                                                            ├──▶ Bias Q2 #2 ──▶ Air Motion L/R (bi-amp)
      │                                                            └──▶ Bias V3 #1 ──▶ Airten L/R
      │                                      V3 #2 line outs ──▶ Bias Q5 ──▶ Xair L-1/2, R-1/2
      │
      ├── MonOut (−32 dB) ──▶ Bias Q2 #1 ──▶ Air Vantage L/R + Venu 215 L/R (DJ booth)
      └── BakFil (−34 dB) ──▶ Athens entrance / back-fill zone
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
| MonOut | → Q2 #1 | −32 dB | DJ booth monitors |
| BakFil | → Athens zone | −34 dB | Entrance / back-fill |
| Out4/5/6 | Unassigned | 0 dB | ⚠️ Status unknown — confirm if in use |

---

## Amplifier Assignments (Armonía network: 192.168.10.x)

| Amp | Serial | IP | Drives | Delay / Gain |
|---|---|---|---|---|
| Bias V3 #1 | 341130 | 192.168.10.13 | Airten L/R | −8 dB / 28.23 ms |
| Bias V3 #2 | 341132 | 192.168.10.14 | Xair L-3/R-3 + line outs → Q5 | — |
| Bias Q5 | 777758 | 192.168.10.10 | Xair L-1/2, R-1/2 (via V3 #2 line out) | — |
| Bias Q2 #1 | 951058 | 192.168.10.12 | Air Vantage L/R + Venu 215 L/R | 0.5 dB / 1.0 ms |
| Bias Q2 #2 | 00543758 | 192.168.10.11 | Air Motion L bi-amp (CH1/2) + R (CH3/4) | — |
| ~~Bias V9~~ | — | — | **Retired / removed** | — |

---

## Speaker System — 18 Total

| Zone | Qty | Model | Amp |
|---|---|---|---|
| Main | 2 | VOID Air Motion V2 Red | Q2 #2 (bi-amp) |
| Mains fill | 2 | VOID Airten V3 | V3 #1 |
| Sub cluster (outside) | 2 | VOID Stasys Xair | V3 #2 |
| Sub cluster (middle) | 4 | VOID Stasys Xair | Q5 |
| Sub flank | 2 | VOID Venu 215 V2 | Q2 #1 CH3/4 |
| DJ booth monitors | 2 | VOID Air Vantage | Q2 #1 CH1/2 |
| DJ booth sub | 2 | VOID Venu 215 V2 | Q2 #1 CH3/4 |
| Athens entrance | 2 | (model TBC) | CQ-12T BakFil |

---

## Conversations

| Date | Conversation | Files | Status |
|---|---|---|---|
| 2026-02-20 | [SVG Rack Elevation — Methodology](https://claude.ai/chat/77927477-ddf9-4a6e-8507-652816224db0) | 4 | Reference only |
| 2026-02-21 | [Nomad Amp Rack Cable Schedule](https://claude.ai/chat/81ef8190-238f-4f37-901d-ead397b7a6e1) | 17 | ⚠️ Stale — predates CQ-12T |
| 2026-02-23 | [19-Inch Rack Standards](https://claude.ai/chat/fb56aa22-37a8-4633-825c-6dd1c91f4db5) | 1 | General reference |
| 2026-03-16 | [Audio Rack Equipment Audit](https://claude.ai/chat/61c49787-7fd9-4227-ae32-2f3c8301d7f6) | 75 | ⚠️ Sub count corrected; impedance issue open |
| 2026-03-16 | [Yamaha MG12 Validation](https://claude.ai/chat/bfe45378-1df0-4646-b3a1-dde53b1db8c4) | 1 | ❌ Superseded by CQ-12T |
| 2026-03-24 | [CQ12 Mixer Audit ← **most current**](https://claude.ai/chat/c8999358-0d6d-42d2-8abd-d5e1b06ff2d8) | 10 | ⚠️ Signal flow JSX only, not exported |
| 2026-03-28 | [Ma2 MCP Audit](https://claude.ai/chat/7927f9e3-7bbe-454b-ab40-46ff6a3412b5) | 0 | Not AV-related |

---

## Open Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 1 | 6× Xair at 1.33Ω on V3 channels — below minimum spec | 🔴 Critical | Decide: add amp / re-wire / confirm with Powersoft |
| 2 | Rack elevation photo ≠ documented spec order; V9 removed | 🟡 Medium | Take new rack photo |
| 3 | Out4/5/6 on CQ-12T at 0 dB — purpose unknown | 🟡 Medium | Confirm if in use |
| 4 | Athens entrance speaker model not documented | 🟢 Low | Identify model |
| 5 | No production contact details | 🟢 Low | Add to available rider |

---

## Notes on Downloaded Files

- Images downloaded as **JPEG** (converted from WebP via `--convert-images`)
- PDFs: original bytes via `document_pdf` variant
- DOCX: not downloadable via API — `.NOT_DOWNLOADABLE.txt` placeholders written
