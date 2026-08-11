---
title: Nomad Toronto — Rack I/O Schedule (Power · Data · Audio)
description: Every connection into, out of, and within the amplifier rack. One row per cable end, with connector type and the device at the far end. Generated from the label data so the cables and this schedule cannot disagree.
version: 1.0.0
created: 2026-08-11T00:00:00Z
last_updated: 2026-08-11T00:00:00Z
generated_by: scripts/build-rack-io-schedule.py
---

# Nomad Toronto — Rack I/O Schedule

> **Generated file — do not hand-edit.** Source data lives in `07-tech-pack/labeling/labels-{power,audio,speaker,network}.csv`, the same rows that print the cable labels. Edit those and re-run `python3 scripts/build-rack-io-schedule.py`.

**Scope:** strictly the amplifier rack. A cable is listed only if at least one end terminates in the rack. Bias V9 has been removed from the rack and does not appear.

| Direction | Meaning |
|-----------|---------|
| **IN** | Enters the rack from outside (booth, venue panel, network) |
| **OUT** | Leaves the rack (loudspeakers, booth PSU) |
| **INTERNAL** | Both ends inside the rack |

---

## §1 Rack boundary — totals

| Direction | Power | Data | Audio | Speaker | Total |
|-----------|------:|-----:|------:|--------:|------:|
| **IN** | 7 | 5 | 5 | — | **17** |
| **OUT** | 1 | — | — | 14 | **15** |
| **INTERNAL** | 1 | — | 4 | — | **5** |
| | | | | | **37 cables** |

---

## §2 Connections by device

Each table is written from that device's point of view: **Dir** is in/out at *this* device's panel, **Port** is its own connector, **Far end** is what sits on the other end of the cable.

### U2 · Drawmer SP2120

| Dir | Class | Port / channel | Connector | Far end | Far-end port | Cable |
|-----|-------|----------------|-----------|---------|--------------|-------|
| ◀ IN | ⚡ Power | MAINS inlet | IEC C14 | Tripp Lite PDU | Outlet | `P1` |
| ◀ IN | 🔊 Audio | Input L | XLR-F | Allen & Heath CQ-12T | Main L | `9` |
| ◀ IN | 🔊 Audio | Input R | XLR-F | Allen & Heath CQ-12T | Main R | `10` |
| OUT ▶ | 🔊 Audio | Output L | XLR-M | Bias V3 #2 | ANALOG CH1 IN | `15` |
| OUT ▶ | 🔊 Audio | Output R | XLR-M | Bias V3 #2 | ANALOG CH2 IN | `16` |

### U3 · Bias V3 #1

| Dir | Class | Port / channel | Connector | Far end | Far-end port | Cable |
|-----|-------|----------------|-----------|---------|--------------|-------|
| ◀ IN | ⚡ Power | MAINS inlet | IEC C20 | Venue panel — 20 A C/D-curve | Dedicated breaker | `P2` |
| ◀ IN | 🔗 Data | AESOP primary (rear) | RJ45 | Network switch | Port TBC | `39` |
| ◀ IN | 🔊 Audio | ANALOG CH1 IN | XLR-F | UNVERIFIED | UNVERIFIED | `19` |
| OUT ▶ | 🔊 Speaker | OUT1 (CH1) | speakON NL4 | Airten V3 L | NL4 In | `30` |
| OUT ▶ | 🔊 Speaker | OUT2 (CH2) | speakON NL4 | Airten V3 R | NL4 In | `31` |

### U4 · Bias Q2 #1

| Dir | Class | Port / channel | Connector | Far end | Far-end port | Cable |
|-----|-------|----------------|-----------|---------|--------------|-------|
| ◀ IN | ⚡ Power | MAINS inlet | IEC C20 | Venue panel — 20 A C/D-curve | Dedicated breaker | `P3` |
| ◀ IN | 🔗 Data | ETHERNET | RJ45 | Network switch | Port TBC | `40` |
| ◀ IN | 🔊 Audio | LINE input CH1 | Phoenix 12-pin | Allen & Heath CQ-12T | MonOut L (Out 1-6) | `11` |
| ◀ IN | 🔊 Audio | LINE input CH2 | Phoenix 12-pin | Allen & Heath CQ-12T | MonOut R (Out 1-6) | `12` |
| OUT ▶ | 🔊 Speaker | OUTPUTS CH1 | Phoenix PC 5/8 | Air Vantage L | NL4 In | `32` |
| OUT ▶ | 🔊 Speaker | OUTPUTS CH2 | Phoenix PC 5/8 | Air Vantage R | NL4 In | `33` |
| OUT ▶ | 🔊 Speaker | OUTPUTS CH3 | Phoenix PC 5/8 | Venu 215 V2 L | Phoenix recessed | `34` |
| OUT ▶ | 🔊 Speaker | OUTPUTS CH4 | Phoenix PC 5/8 | Venu 215 V2 R | Phoenix recessed | `35` |

### U5 · — empty —

Bay empty — Bias V9 removed. A **32 A CPC 45A circuit remains live to this bay**. Freed by V9 removal · do not reconnect without a load review

### U6 · Bias Q2 #2

| Dir | Class | Port / channel | Connector | Far end | Far-end port | Cable |
|-----|-------|----------------|-----------|---------|--------------|-------|
| ◀ IN | ⚡ Power | MAINS inlet | IEC C20 | Venue panel — 20 A C/D-curve | Dedicated breaker | `P4` |
| ◀ IN | 🔗 Data | ETHERNET | RJ45 | Network switch | Port TBC | `38` |
| ◀ IN | 🔊 Audio | LINE input CH1 | Phoenix 12-pin | Bias V3 #2 | ANALOG CH2 OUT (pre-DSP) | `18` |
| OUT ▶ | 🔊 Speaker | OUTPUTS CH1 | Phoenix PC 5/8 | Air Motion V2 L | NL4 #1 pins 1+/1- | `26` |
| OUT ▶ | 🔊 Speaker | OUTPUTS CH2 | Phoenix PC 5/8 | Air Motion V2 L | NL4 #2 pins 2+/2- | `27` |
| OUT ▶ | 🔊 Speaker | OUTPUTS CH3 | Phoenix PC 5/8 | Air Motion V2 R | NL4 #1 pins 1+/1- | `28` |
| OUT ▶ | 🔊 Speaker | OUTPUTS CH4 | Phoenix PC 5/8 | Air Motion V2 R | NL4 #2 pins 2+/2- | `29` |

### U7 · Bias V3 #2

| Dir | Class | Port / channel | Connector | Far end | Far-end port | Cable |
|-----|-------|----------------|-----------|---------|--------------|-------|
| ◀ IN | ⚡ Power | MAINS inlet | IEC C20 | Venue panel — 20 A C/D-curve | Dedicated breaker | `P5` |
| ◀ IN | 🔗 Data | AESOP primary (rear) | RJ45 | Network switch | Port TBC | `36` |
| ◀ IN | 🔊 Audio | ANALOG CH1 IN | XLR-F | Drawmer SP2120 | Output L | `15` |
| ◀ IN | 🔊 Audio | ANALOG CH2 IN | XLR-F | Drawmer SP2120 | Output R | `16` |
| OUT ▶ | 🔊 Audio | ANALOG CH1 OUT (pre-DSP) | XLR-M | Bias Q5 | ANALOG IN 1 | `17` |
| OUT ▶ | 🔊 Audio | ANALOG CH2 OUT (pre-DSP) | XLR-M | Bias Q2 #2 | LINE input CH1 | `18` |
| OUT ▶ | 🔊 Speaker | OUT1 (CH1) | speakON NL4 | Stasys Xair L-3 | NL4 In | `20` |
| OUT ▶ | 🔊 Speaker | OUT2 (CH2) | speakON NL4 | Stasys Xair R-3 | NL4 In | `21` |

### U8 · Bias Q5

| Dir | Class | Port / channel | Connector | Far end | Far-end port | Cable |
|-----|-------|----------------|-----------|---------|--------------|-------|
| ◀ IN | ⚡ Power | MAINS inlet | Phoenix PC 5/5 | Venue panel — rating TBC | Dedicated breaker | `P6` |
| ◀ IN | 🔗 Data | etherCON ETH1 primary | etherCON RJ45 | Network switch | Port TBC | `37` |
| ◀ IN | 🔊 Audio | ANALOG IN 1 | XLR-F | Bias V3 #2 | ANALOG CH1 OUT (pre-DSP) | `17` |
| OUT ▶ | 🔊 Speaker | OUT1 (CH1+CH2) | speakON NL4 | Stasys Xair L-1 / L-2 | NL4 In | `22` |
| OUT ▶ | 🔊 Speaker | OUT2 (CH3+CH4) | speakON NL4 | Stasys Xair R-1 / R-2 | NL4 In | `23` |

### U9–U10 · Tripp Lite PDU

| Dir | Class | Port / channel | Connector | Far end | Far-end port | Cable |
|-----|-------|----------------|-----------|---------|--------------|-------|
| ◀ IN | ⚡ Power | Mains inlet | TBC | Venue panel — control circuit | Dedicated breaker | `P0` |
| OUT ▶ | ⚡ Power | Outlet | NEMA 5-15R | Drawmer SP2120 | MAINS inlet | `P1` |
| OUT ▶ | ⚡ Power | Outlet | NEMA 5-15R | CQ-12T external PSU | Mains inlet | `P7` |

---

## §3 Crossing the rack boundary

Everything that physically enters or leaves the rack — the list to check when the rack is moved, re-terminated, or handed to a visiting engineer.

| Cable | Class | Dir | Outside the rack | Connector | Rack device | Rack port |
|-------|-------|-----|------------------|-----------|-------------|-----------|
| `P0` | ⚡ Power | IN | Venue panel — control circuit | TBC | Tripp Lite PDU | Mains inlet |
| `P2` | ⚡ Power | IN | Venue panel — 20 A C/D-curve | TBC | Bias V3 #1 | MAINS inlet |
| `P3` | ⚡ Power | IN | Venue panel — 20 A C/D-curve | TBC | Bias Q2 #1 | MAINS inlet |
| `P4` | ⚡ Power | IN | Venue panel — 20 A C/D-curve | TBC | Bias Q2 #2 | MAINS inlet |
| `P5` | ⚡ Power | IN | Venue panel — 20 A C/D-curve | TBC | Bias V3 #2 | MAINS inlet |
| `P6` | ⚡ Power | IN | Venue panel — rating TBC | TBC | Bias Q5 | MAINS inlet |
| `P7` | ⚡ Power | OUT | CQ-12T external PSU | IEC C14 | Tripp Lite PDU | Outlet |
| `—` | ⚡ Power | IN | Venue panel — 32 A | CPC 45A | — none — | U5 bay empty |
| `36` | 🔗 Data | IN | Network switch | RJ45 | Bias V3 #2 | AESOP primary (rear) |
| `37` | 🔗 Data | IN | Network switch | RJ45 | Bias Q5 | etherCON ETH1 primary |
| `38` | 🔗 Data | IN | Network switch | RJ45 | Bias Q2 #2 | ETHERNET |
| `39` | 🔗 Data | IN | Network switch | RJ45 | Bias V3 #1 | AESOP primary (rear) |
| `40` | 🔗 Data | IN | Network switch | RJ45 | Bias Q2 #1 | ETHERNET |
| `9` | 🔊 Audio | IN | Allen & Heath CQ-12T | XLR-M | Drawmer SP2120 | Input L |
| `10` | 🔊 Audio | IN | Allen & Heath CQ-12T | XLR-M | Drawmer SP2120 | Input R |
| `11` | 🔊 Audio | IN | Allen & Heath CQ-12T | TRS | Bias Q2 #1 | LINE input CH1 |
| `12` | 🔊 Audio | IN | Allen & Heath CQ-12T | TRS | Bias Q2 #1 | LINE input CH2 |
| `19` | 🔊 Audio | IN | UNVERIFIED | XLR-M | Bias V3 #1 | ANALOG CH1 IN |
| `20` | 🔊 Speaker | OUT | Stasys Xair L-3 | speakON NL4 | Bias V3 #2 | OUT1 (CH1) |
| `21` | 🔊 Speaker | OUT | Stasys Xair R-3 | speakON NL4 | Bias V3 #2 | OUT2 (CH2) |
| `22` | 🔊 Speaker | OUT | Stasys Xair L-1 / L-2 | speakON NL4 | Bias Q5 | OUT1 (CH1+CH2) |
| `23` | 🔊 Speaker | OUT | Stasys Xair R-1 / R-2 | speakON NL4 | Bias Q5 | OUT2 (CH3+CH4) |
| `26` | 🔊 Speaker | OUT | Air Motion V2 L | speakON NL4 | Bias Q2 #2 | OUTPUTS CH1 |
| `27` | 🔊 Speaker | OUT | Air Motion V2 L | speakON NL4 | Bias Q2 #2 | OUTPUTS CH2 |
| `28` | 🔊 Speaker | OUT | Air Motion V2 R | speakON NL4 | Bias Q2 #2 | OUTPUTS CH3 |
| `29` | 🔊 Speaker | OUT | Air Motion V2 R | speakON NL4 | Bias Q2 #2 | OUTPUTS CH4 |
| `30` | 🔊 Speaker | OUT | Airten V3 L | speakON NL4 | Bias V3 #1 | OUT1 (CH1) |
| `31` | 🔊 Speaker | OUT | Airten V3 R | speakON NL4 | Bias V3 #1 | OUT2 (CH2) |
| `32` | 🔊 Speaker | OUT | Air Vantage L | speakON NL4 | Bias Q2 #1 | OUTPUTS CH1 |
| `33` | 🔊 Speaker | OUT | Air Vantage R | speakON NL4 | Bias Q2 #1 | OUTPUTS CH2 |
| `34` | 🔊 Speaker | OUT | Venu 215 V2 L | Phoenix | Bias Q2 #1 | OUTPUTS CH3 |
| `35` | 🔊 Speaker | OUT | Venu 215 V2 R | Phoenix | Bias Q2 #1 | OUTPUTS CH4 |

---

## §4 Deliberately excluded — never touches the rack

11 cables in the label sets run entirely outside the rack. They are listed here so their absence above reads as a decision rather than an oversight.

| Cable | Class | From | To | Why excluded |
|-------|-------|------|----|--------------|
| `1` | 🔊 Audio | Pioneer DJM-V10 | Allen & Heath CQ-12T | BOOTH → BOOTH |
| `2` | 🔊 Audio | Pioneer DJM-V10 | Allen & Heath CQ-12T | BOOTH → BOOTH |
| `3` | 🔊 Audio | Pioneer DJM-V10 | Allen & Heath CQ-12T | BOOTH → BOOTH |
| `4` | 🔊 Audio | Pioneer DJM-V10 | Allen & Heath CQ-12T | BOOTH → BOOTH |
| `13` | 🔊 Audio | Allen & Heath CQ-12T | Turbosound Athens L | BOOTH → ENTRANCE |
| `14` | 🔊 Audio | Allen & Heath CQ-12T | Turbosound Athens R | BOOTH → ENTRANCE |
| `5` | 🔗 Data | Pioneer CDJ-3000 #1 | DJM-V10 / Pro DJ Link hub | BOOTH → BOOTH |
| `6` | 🔗 Data | Pioneer CDJ-3000 #2 | DJM-V10 / Pro DJ Link hub | BOOTH → BOOTH |
| `7` | 🔗 Data | Pioneer CDJ-3000 #3 | DJM-V10 / Pro DJ Link hub | BOOTH → BOOTH |
| `8` | 🔗 Data | Pioneer CDJ-3000 #4 | DJM-V10 / Pro DJ Link hub | BOOTH → BOOTH |
| `41` | 🔗 Data | Separate network / link-local | Allen & Heath CQ-12T | UNKNOWN → BOOTH |

---

## §5 Rows carrying an unverified fact

| Cable | What is unverified |
|-------|--------------------|
| `11` | −32 dB · CQ Out 1-6 are TRS (D3) |
| `12` | −32 dB · TRS source end (D3) |
| `17` | Q5 input is XLR — the documented Phoenix adapter may be unnecessary (D2) |
| `19` | V3 has only 2 line outs — documented Line Out 3 does not exist (D1). Trace before relabelling |
| `22` | One NL4 carries 2 ch — CH1 on 1+/1- CH2 on 2+/2- (D2) |
| `23` | One NL4 carries 2 ch — CH3 on 1+/1- CH4 on 2+/2- (D2) |
| `36` | Armonía control · switch unlocated (D8) |
| `37` | Armonía control · switch unlocated (D8) |
| `38` | Armonía control · switch unlocated (D8) |
| `39` | Armonía control · switch unlocated (D8) |
| `40` | Armonía control · switch unlocated (D8) |

Cross-referenced to the discrepancy IDs in `07-tech-pack/rack-io-inventory.md` §12.

---

*EMBLEM PROJECTS INC. · generated from label data · re-run the build script after editing any labels-*.csv*
