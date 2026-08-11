---
title: Nomad Toronto — Rack Internal Connections (Power · Data · Audio)
description: Cables with both ends on equipment inside the amplifier rack. Connector type at each end and both devices identified. Generated from the cable-label data.
version: 2.0.0
created: 2026-08-11T00:00:00Z
last_updated: 2026-08-11T00:00:00Z
generated_by: scripts/build-rack-io-schedule.py
---

# Nomad Toronto — Rack Internal Connections

> **Generated file — do not hand-edit.** Source data is `07-tech-pack/labeling/labels-{power,audio,speaker,network}.csv`, the same rows that print the cable labels. Edit those and re-run `python3 scripts/build-rack-io-schedule.py`.

## Scope

**Strictly cables with both ends on rack equipment.** A cable is out of scope if either end lands on booth gear (CQ-12T, DJM-V10, CDJs), the venue electrical panel, the loudspeakers, or anything else outside the rack — even when its other end is on a rack device.

| | Cables | Power | Data | Audio |
|---|------:|------:|-----:|------:|
| **Confirmed internal** | **5** | 1 | — | 4 |
| **Unresolved** (see §2) | **6** | — | 5 | 1 |
| **Total in this document** | **11** | | | |

Bias V9 has been removed from the rack and does not appear.

---

## Cable tie colours

**You do not need this table to read the schedule** — every swatch below sits directly beside the device it belongs to, and on the proof sheets each chip is printed with its device name on it. This is here for one job only: knowing which tie to reach for at the rack.

The DK-1221 roll is black thermal on white paper, so the printed labels carry no colour. On the rack the colour is carried by **the cable tie the tag folds over** — free, since the fold-over design already needs a tie.

| | Device | Rack U | Hex | Cable tie |
|---|--------|--------|-----|-----------|
| 🟦 | Drawmer SP2120 | U2 | `#0072B2` | blue |
| 🟩 | Bias V3 #1 | U3 | `#009E73` | green |
| 🟨 | Bias Q2 #1 | U4 | `#F0E442` | yellow |
| 🟧 | Bias Q2 #2 | U6 | `#E69F00` | orange |
| 🟥 | Bias V3 #2 | U7 | `#D55E00` | red |
| 🟪 | Bias Q5 | U8 | `#CC79A7` | purple |
| ⬛ | Tripp Lite PDU | U9–U10 | `#444444` | black |
| ⬜ | *anything outside the rack* | — | `#BBBBBB` | — |

Hexes are the Okabe-Ito palette, which stays distinguishable under all common forms of colour blindness — worth caring about in a dark rack room where colour discrimination is already degraded.

---

## §1 Confirmed internal connections

Both ends verified as rack equipment. These are the cables you re-make if the rack is stripped and rebuilt.

| Cable | Class | From device | From port | Connector | To device | To port | Connector |
|-------|-------|-------------|-----------|-----------|-----------|---------|-----------|
| `P1` | ⚡ Power | ⬛ Tripp Lite PDU | Outlet | NEMA 5-15R | 🟦 Drawmer SP2120 | MAINS inlet | IEC C14 |
| `15` | 🔊 Audio | 🟦 Drawmer SP2120 | Output L | XLR-M | 🟥 Bias V3 #2 | ANALOG CH1 IN | XLR-F |
| `16` | 🔊 Audio | 🟦 Drawmer SP2120 | Output R | XLR-M | 🟥 Bias V3 #2 | ANALOG CH2 IN | XLR-F |
| `17` | 🔊 Audio | 🟥 Bias V3 #2 | ANALOG CH1 OUT (pre-DSP) | XLR-M | 🟪 Bias Q5 | ANALOG IN 1 | XLR-F |
| `18` | 🔊 Audio | 🟥 Bias V3 #2 | ANALOG CH2 OUT (pre-DSP) | XLR-M | 🟧 Bias Q2 #2 | LINE input CH1 | Phoenix 12-pin |

---

## §2 Unresolved — may be internal

These are excluded from §1 **only because a fact is unknown**, not because they are known to leave the rack. They are carried here rather than dropped: if the switch is rack-mounted, the five control links were internal all along.

| Cable | Class | Rack device | Rack port | Connector | Unknown end | What is unresolved |
|-------|-------|-------------|-----------|-----------|-------------|--------------------|
| `36` | 🔗 Data | 🟥 Bias V3 #2 | AESOP primary (rear) | RJ45 | ⬜ Network switch | Armonía control · switch unlocated (D8) |
| `37` | 🔗 Data | 🟪 Bias Q5 | etherCON ETH1 primary | etherCON RJ45 | ⬜ Network switch | Armonía control · switch unlocated (D8) |
| `38` | 🔗 Data | 🟧 Bias Q2 #2 | ETHERNET | RJ45 | ⬜ Network switch | Armonía control · switch unlocated (D8) |
| `39` | 🔗 Data | 🟩 Bias V3 #1 | AESOP primary (rear) | RJ45 | ⬜ Network switch | Armonía control · switch unlocated (D8) |
| `40` | 🔗 Data | 🟨 Bias Q2 #1 | ETHERNET | RJ45 | ⬜ Network switch | Armonía control · switch unlocated (D8) |
| `19` | 🔊 Audio | 🟩 Bias V3 #1 | ANALOG CH1 IN | XLR-F | ⬜ UNVERIFIED | V3 has only 2 line outs — documented Line Out 3 does not exist (D1). Trace before relabelling |

Resolve these and re-run the build — they move into §1 automatically if both ends turn out to be in the rack.

---

## §3 By device

Same connections, grouped by rack unit. **Dir** is in/out at *this* device's panel.

### U2 · 🟦 Drawmer SP2120

| Dir | Class | Port | Connector | Far end | Far-end port | Cable |
|-----|-------|------|-----------|---------|--------------|-------|
| ◀ IN | ⚡ Power | MAINS inlet | IEC C14 | ⬛ Tripp Lite PDU | Outlet | `P1` |
| OUT ▶ | 🔊 Audio | Output L | XLR-M | 🟥 Bias V3 #2 | ANALOG CH1 IN | `15` |
| OUT ▶ | 🔊 Audio | Output R | XLR-M | 🟥 Bias V3 #2 | ANALOG CH2 IN | `16` |

### U3 · 🟩 Bias V3 #1

| Dir | Class | Port | Connector | Far end | Far-end port | Cable |
|-----|-------|------|-----------|---------|--------------|-------|
| ◀ IN | 🔗 Data | AESOP primary (rear) | RJ45 | ⬜ Network switch | Port TBC | `39` |
| ◀ IN | 🔊 Audio | ANALOG CH1 IN | XLR-F | ⬜ UNVERIFIED | UNVERIFIED | `19` |

### U4 · 🟨 Bias Q2 #1

| Dir | Class | Port | Connector | Far end | Far-end port | Cable |
|-----|-------|------|-----------|---------|--------------|-------|
| ◀ IN | 🔗 Data | ETHERNET | RJ45 | ⬜ Network switch | Port TBC | `40` |

### U5 · ⬜ — empty —

Bay empty — Bias V9 removed. The **32 A CPC 45A circuit is still live to this bay**; it runs from the venue panel, so it is out of scope here, but it needs capping or decommissioning. See `rack-io-inventory.md` §5.

### U6 · 🟧 Bias Q2 #2

| Dir | Class | Port | Connector | Far end | Far-end port | Cable |
|-----|-------|------|-----------|---------|--------------|-------|
| ◀ IN | 🔗 Data | ETHERNET | RJ45 | ⬜ Network switch | Port TBC | `38` |
| ◀ IN | 🔊 Audio | LINE input CH1 | Phoenix 12-pin | 🟥 Bias V3 #2 | ANALOG CH2 OUT (pre-DSP) | `18` |

### U7 · 🟥 Bias V3 #2

| Dir | Class | Port | Connector | Far end | Far-end port | Cable |
|-----|-------|------|-----------|---------|--------------|-------|
| ◀ IN | 🔗 Data | AESOP primary (rear) | RJ45 | ⬜ Network switch | Port TBC | `36` |
| ◀ IN | 🔊 Audio | ANALOG CH1 IN | XLR-F | 🟦 Drawmer SP2120 | Output L | `15` |
| ◀ IN | 🔊 Audio | ANALOG CH2 IN | XLR-F | 🟦 Drawmer SP2120 | Output R | `16` |
| OUT ▶ | 🔊 Audio | ANALOG CH1 OUT (pre-DSP) | XLR-M | 🟪 Bias Q5 | ANALOG IN 1 | `17` |
| OUT ▶ | 🔊 Audio | ANALOG CH2 OUT (pre-DSP) | XLR-M | 🟧 Bias Q2 #2 | LINE input CH1 | `18` |

### U8 · 🟪 Bias Q5

| Dir | Class | Port | Connector | Far end | Far-end port | Cable |
|-----|-------|------|-----------|---------|--------------|-------|
| ◀ IN | 🔗 Data | etherCON ETH1 primary | etherCON RJ45 | ⬜ Network switch | Port TBC | `37` |
| ◀ IN | 🔊 Audio | ANALOG IN 1 | XLR-F | 🟥 Bias V3 #2 | ANALOG CH1 OUT (pre-DSP) | `17` |

### U9–U10 · ⬛ Tripp Lite PDU

| Dir | Class | Port | Connector | Far end | Far-end port | Cable |
|-----|-------|------|-----------|---------|--------------|-------|
| OUT ▶ | ⚡ Power | Outlet | NEMA 5-15R | 🟦 Drawmer SP2120 | MAINS inlet | `P1` |

---

## §4 Out of scope

37 cables in the label data have at least one end outside the rack. Summarised so their absence reads as a decision, not an oversight. Full detail for these lives in `07-tech-pack/cable-schedule.md` and the label CSVs.

| Outside-the-rack end | Cables | Count |
|----------------------|--------|------:|
| Loudspeakers on the floor | `20`, `21`, `22`, `23`, `26`, `27`, `28`, `29`, `30`, `31`, `32`, `33`, `34`, `35` | 14 |
| DJ booth equipment — CQ-12T, DJM-V10, CDJs | `P7`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12` | 13 |
| Venue electrical panel — mains feeds to rack devices | `P0`, `P2`, `P3`, `P4`, `P5`, `P6`, `—` | 7 |
| DJ booth equipment — CQ-12T, DJM-V10, CDJs + Entrance fill speakers | `13`, `14` | 2 |
| DJ booth equipment — CQ-12T, DJM-V10, CDJs + Location unresolved | `41` | 1 |

---

## §5 Label print set

The 11 cables above need **22 labels** (two per cable, one per end). The derived print set is written to `07-tech-pack/labeling/labels-rack-internal.csv` by this same script — build its proof and template with:

```bash
python3 scripts/build-cable-labels.py \
    07-tech-pack/labeling/labels-rack-internal.csv \
    07-tech-pack/labeling/dk1221-rack-internal-proof.svg
python3 scripts/build-lbx.py \
    07-tech-pack/labeling/labels-rack-internal.csv \
    07-tech-pack/labeling/dk1221-rack-internal.lbx
```

No labels are produced for CQ-12T or DJM-V10 connections.

---

*EMBLEM PROJECTS INC. · generated from label data*
