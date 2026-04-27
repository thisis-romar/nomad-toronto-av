# Graph Report - .  (2026-04-27)

## Corpus Check
- 78 files · ~455,441 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 202 nodes · 269 edges · 15 communities detected
- Extraction: 86% EXTRACTED · 12% INFERRED · 1% AMBIGUOUS · INFERRED: 33 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Bias V3 Amp Family|Bias V3 Amp Family]]
- [[_COMMUNITY_Armonia DSP Network|Armonia DSP Network]]
- [[_COMMUNITY_Wiring Standards & Rider Docs|Wiring Standards & Rider Docs]]
- [[_COMMUNITY_Air Vantage Speaker Specs|Air Vantage Speaker Specs]]
- [[_COMMUNITY_CQ-12T Mixer Features|CQ-12T Mixer Features]]
- [[_COMMUNITY_Air Motion V2 Specs|Air Motion V2 Specs]]
- [[_COMMUNITY_Bias Q5 Amp|Bias Q5 Amp]]
- [[_COMMUNITY_DJ Booth Zone|DJ Booth Zone]]
- [[_COMMUNITY_Rack Standards Reference|Rack Standards Reference]]
- [[_COMMUNITY_CQ-12T Dimensions|CQ-12T Dimensions]]
- [[_COMMUNITY_Source Wiring Docs|Source Wiring Docs]]
- [[_COMMUNITY_SP2120 Specs|SP2120 Specs]]
- [[_COMMUNITY_SP2120 Dimensions|SP2120 Dimensions]]
- [[_COMMUNITY_Rack Blank Panel|Rack Blank Panel]]
- [[_COMMUNITY_Rack PDU|Rack PDU]]

## God Nodes (most connected - your core abstractions)
1. `VOID Acoustics Air Motion V2 Speaker` - 19 edges
2. `Allen & Heath CQ-12T Digital Mixer` - 16 edges
3. `VOID Acoustics Air Vantage Speaker` - 16 edges
4. `VOID Acoustics Airten V3 Speaker` - 14 edges
5. `Bias Q5 Power Amplifier (Void Acoustics)` - 12 edges
6. `Nomad Toronto AV Signal Flow Diagram` - 11 edges
7. `Bias V3 #2 (S/N 341132, IP 192.168.10.14)` - 11 edges
8. `Allen & Heath CQ-12T Matrix Mixer` - 10 edges
9. `Bias V3 #2 — Outside Subs / Signal Hub` - 10 edges
10. `VOID Acoustics Stasys Xair Subwoofer` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Bias V3 Power Amplifier (Void Acoustics)` --drives--> `VOID Acoustics Airten V3 Speaker`  [AMBIGUOUS]
  05-speaker-assets/png/bias-v3-amp.png → 02-equipment-manuals/speakers/VOID-Airten-V3-User-Manual-v2.1.pdf
- `CDJ-3000 Rear: Audio Out L/R, Digital Out, AC In, LINK terminal (LAN), USB port` --feeds--> `Allen & Heath CQ-12T Digital Mixer`  [INFERRED]
  05-speaker-assets/png/pioneer-cdj-3000-rear.png → 02-equipment-manuals/mixers/Allen-Heath_CQ-12T_datasheet.pdf
- `Bias V3 Power Amplifier (Void Acoustics)` --drives--> `VOID Acoustics Air Motion V2 Speaker`  [AMBIGUOUS]
  05-speaker-assets/png/bias-v3-amp.png → 02-equipment-manuals/speakers/VOID-Air-Motion-V2-User-Guide.pdf
- `Pioneer DJM-V10 Rear Panel View` --connected_by--> `VOID Acoustics Air Motion V2 Speaker`  [INFERRED]
  05-speaker-assets/png/pioneer-djm-v10-rear.png → 02-equipment-manuals/speakers/VOID-Air-Motion-V2-User-Guide.pdf
- `Pioneer DJM-V10 (Equipment Entity)` --feeds--> `VOID Acoustics Air Vantage Speaker`  [INFERRED]
  05-speaker-assets/png/pioneer-djm-v10.png → 02-equipment-manuals/speakers/VOID-Air-Vantage-User-Guide.pdf

## Hyperedges (group relationships)
- **FOH Main Signal Chain: DJM-V10 → CQ-12T → SP2120 → V3#2 → Zones** — djmv10_unit, cq12t_unit, sp2120_unit, bias_v3_2_unit [EXTRACTED 1.00]
- **V3 #2 Line Out Distribution to Q5, Q2 #2, V3 #1** — bias_v3_2_unit, bias_q5_unit, bias_q2_2_unit, bias_v3_1_unit [EXTRACTED 1.00]
- **DJ Booth Zone: CQ-12T MonOut → Q2 #1 → Air Vantage + Venu 215** — cq12t_unit, bias_q2_1_unit, spk_air_vantage, spk_venu_215_v2 [EXTRACTED 1.00]
- **FOH Main Signal Chain: CQ-12T -> SP2120 -> Bias Q5 -> Void Speakers** — ahcq12t_mixer, drawmer_sp2120, bias_q5_amp, void_air_motion_v2, void_stasys_xair [INFERRED 0.90]
- **VOID Passive Speaker Family at NOMAD (all require external amplification)** — void_air_motion_v2, void_air_vantage, void_airten_v3, void_stasys_xair, void_venu_v2_series [INFERRED 0.95]
- **Bias Amplifier Family (Q5 and V3) driving VOID Speakers** — bias_q5_amp, bias_v3_amp, void_air_motion_v2, void_airten_v3, void_stasys_xair [INFERRED 0.75]
- **CQ-12T Documentation and Asset Cluster** — ahcq12t_datasheet, ahcq12t_userguide, ahcq12t_block_diagram_img, ahcq12t_dims_img, ahcq12t_datasheet_img, ahcq12t_mixer [EXTRACTED 1.00]
- **Bias Q5 Amplifier Documentation and Asset Cluster** — bias_q5_amp, bias_q5_dims_drawing, bias_q5_front_panel, bias_q5_speakon_output, bias_q5_phoenix_input, bias_q5_xlr_inputs, bias_q5_ethernet [EXTRACTED 1.00]
- **Pioneer DJ Equipment Set (CDJ-3000 + DJM-V10)** — pioneer_cdj3000, pioneer_djmv10, pioneer_cdj3000_cover, pioneer_cdj3000_top_view, pioneer_djmv10_cover, pioneer_djmv10_top_view, pioneer_djmv10_rear_view [INFERRED 0.95]
- **VOID FOH Speaker System (Air Motion V2 + Airten V3 + Stasys Xair)** — void_air_motion_v2, void_airten_v3, void_stasys_xair [INFERRED 0.85]
- **VOID DJ Booth Monitor System (Air Vantage + Venu 215 V2)** — void_air_vantage, void_venu_215_v2 [INFERRED 0.85]
- **VOID Air Motion V2 Asset Set** — void_air_motion_v2_dims, void_air_motion_v2_front, void_air_motion_v2_side, void_air_motion_v2_top, void_air_motion_v2_cover [EXTRACTED 1.00]
- **VOID Air Vantage Asset Set** — void_air_vantage_dims, void_air_vantage_front, void_air_vantage_side, void_air_vantage_top, void_air_vantage_cover [EXTRACTED 1.00]
- **FOH Main Signal Chain** — device_cdj3000, device_djm_v10, device_cq12t, device_sp2120, device_bias_v3_2, device_bias_q5, device_bias_q2_2, device_bias_v3_1, speaker_xair_l3, speaker_xair_r3, speaker_xair_middle_cluster, speaker_air_motion_v2_foh, speaker_airten_v3_foh [EXTRACTED 1.00]
- **DJ Booth Signal Chain** — device_djm_v10, device_cq12t, device_bias_q2_1, speaker_air_vantage_booth, speaker_venu_215_v2_booth [EXTRACTED 1.00]
- **Entrance Signal Chain** — device_cq12t, speaker_athens_entrance [EXTRACTED 1.00]
- **Bias V3 #2 Signal Distribution Hub Fan-out** — device_bias_v3_2, speaker_xair_l3, speaker_xair_r3, device_bias_q5, device_bias_q2_2, device_bias_v3_1 [EXTRACTED 1.00]
- **Void Air Motion V2 Speaker Asset Views** — speaker_void_air_motion_v2, speaker_void_air_motion_v2_front_svg, speaker_void_air_motion_v2_side_svg, speaker_void_air_motion_v2_top_svg [EXTRACTED 1.00]
- **Void Air Vantage Speaker Asset Views** — speaker_void_air_vantage, speaker_void_air_vantage_front_svg, speaker_void_air_vantage_side_svg, speaker_void_air_vantage_top_svg [EXTRACTED 1.00]
- **Void Venu 215 V2 Speaker Asset Views** — speaker_void_venu_215_v2, speaker_void_venu_215_v2_front_svg, speaker_void_venu_215_v2_side_svg, speaker_void_venu_215_v2_top_svg, speaker_void_venu_215_v2_front_png, speaker_void_venu_215_v2_side_png, speaker_void_venu_215_v2_top_png, speaker_void_venu_215_v2_png [EXTRACTED 1.00]
- **8U Amp Rack System** — rack_position_u1, rack_position_u2, rack_position_u3, rack_position_u4, rack_position_u5, rack_position_u6, rack_position_u7, rack_position_u8, rack_position_u9 [EXTRACTED 1.00]
- **FOH Zone Speaker Set (18-speaker system)** — speaker_air_motion_v2_foh, speaker_airten_v3_foh, speaker_xair_l3, speaker_xair_r3, speaker_xair_middle_cluster [EXTRACTED 1.00]
- **DJ Booth Zone Speaker Set** — speaker_air_vantage_booth, speaker_venu_215_v2_booth [EXTRACTED 1.00]

## Communities

### Community 0 - "Bias V3 Amp Family"
Cohesion: 0.11
Nodes (31): Bias V3 Amplifier, Bias V3 Amp Front View SVG, Bias V3 Amp Side View SVG, Bias Q2 #2 (S/N 00543758, IP 192.168.10.11), Bias Q5 (S/N 777758, IP 192.168.10.10), Bias V3 #1 (S/N 341130, IP 192.168.10.13), Bias V3 #2 (S/N 341132, IP 192.168.10.14), Bias V9 (OFFLINE) (+23 more)

### Community 1 - "Armonia DSP Network"
Cohesion: 0.12
Nodes (29): Armonía DSP Control Network (192.168.10.x), ArmoníaPlus Control Software v2.8, Bias Q2 #1 — DJ Monitors, Bias Q2 #2 — Air Motion Bi-amp, Bias Q2/Q1/D1 User Guide V1.0, Bias Q5 User Guide V1.1, Bias Q5 — Subs Middle (4ch), Bias V3 #1 — Airten V3 FOH Fill (+21 more)

### Community 2 - "Wiring Standards & Rider Docs"
Cohesion: 0.11
Nodes (23): AES14-1992 XLR Pin Assignment Standard, Technical Available Rider, ANSI/AVIXA D401.01:2023 Documentation Standard, Cable Schedule (41 cables), Pioneer CDJ-3000 Instruction Manual, Pioneer CDJ-3000 (×4 units), Allen & Heath CQ-12T Matrix Mixer, Pioneer DJM-V10 Instruction Manual (+15 more)

### Community 3 - "Air Vantage Speaker Specs"
Cohesion: 0.09
Nodes (23): Air Vantage Connectors: 1x speakON NL4, Air Vantage Dimensions: 719x415x660mm 23.5kg, Air Vantage Drivers: 12" LF horn-loaded + 1.5" HF coaxial, Air Vantage Specs: 2-way passive, 500W AES, 127dB cont/133dB peak, 8 Ohm, Airten V3 Connectors: 2x speakON NL4, Airten V3 Dimensions: 681x303x366mm 20kg, Airten V3 Drivers: 2x10" LF + 1.3" exit HF compression driver (coaxial), Airten V3 Specs: 2-way passive, 500W AES, 125dB cont/131dB peak, 4 Ohm (+15 more)

### Community 4 - "CQ-12T Mixer Features"
Cohesion: 0.1
Nodes (22): CQ-12T 2x Multi-FX Engines, CQ-12T 96kHz Processing / 96-bit Depth, CQ-12T Auto Mic Mixer (AMM), CQ-12T Aux/Monitor Outputs 1-6 (TRS), CQ-12T System Block Diagram (signal flow PNG), CQ-12T Bluetooth 4.1 Stereo Input, CQ-MixPad Control App (iOS/Android/Win/Mac), Allen & Heath CQ-12T Technical Datasheet (+14 more)

### Community 5 - "Air Motion V2 Specs"
Cohesion: 0.1
Nodes (22): Air Motion V2 Connectors: 2x speakON NL4 (pins 1+/1- LF, pins 2+/2- MHF), Air Motion V2 Dimensions: 854x672x658mm 35.4kg, Air Motion V2 Drivers: 12" LF + 8" MF + 1.5" HF compression driver, Air Motion V2 Specs: 3-way bi-amp, 500W LF / 250W HMF AES, 134dB cont, 137dB peak, Bias Q3/Q5 speakON Wiring to VOID Speakers, Bias V3 Power Amplifier (Void Acoustics), Bias V3 Dimensional Drawing (side view): 439mm depth, ventilation bottom, Bias V3 Front Panel Drawing: 465mm W x 32.2mm H (1U rack), with display and controls (+14 more)

### Community 6 - "Bias Q5 Amp"
Cohesion: 0.1
Nodes (21): Bias Q5 Power Amplifier (Void Acoustics), Bias Q5 Dimensional Drawing: 483mm W x 44.5mm H x 495mm D (1U rack), Bias Q5 Ethernet/eCON Primary and Secondary Ports, Bias Q5 Front Panel (User Guide V1.1 cover diagram), Bias Q5 AC Input Phoenix 5-pin Mains Connector (non-standard), Bias Q5 speakON Output Connectors, Bias Q5 XLR Analog Inputs (ch1-5) and XLR Input ch6 analog, Stasys Xair Bias Q5 speakON Wiring (output 1 or 2, max 2 parallel at 2 Ohm) (+13 more)

### Community 7 - "DJ Booth Zone"
Cohesion: 0.1
Nodes (21): Bias Q2 #1 (S/N 951058, IP 192.168.10.12), Issue #4: Athens TCS-AN Submodel Unconfirmed, Rack U4 - Bias Q2 #1 (DJ Monitors), Air Vantage DJ Booth Monitors (×2), Venu 215 V2 DJ Booth Sub (×2), Void Air Vantage, Void Air Vantage Front View SVG, Void Air Vantage Side View SVG (+13 more)

### Community 8 - "Rack Standards Reference"
Cohesion: 1.0
Nodes (3): EIA-310-D / IEC 60297 Rack Standard, 19-Inch Rack Standards Reference, SVG Rack Elevation Methodology

### Community 9 - "CQ-12T Dimensions"
Cohesion: 1.0
Nodes (2): CQ-12T Physical Dimensions 291x242x89mm 2.4kg, CQ-12T Dimensions Drawing PNG: 290.4x254.4x88.2mm

### Community 10 - "Source Wiring Docs"
Cohesion: 1.0
Nodes (1): Wiring Diagram Final PDF

### Community 11 - "SP2120 Specs"
Cohesion: 1.0
Nodes (1): SP2120 Specs: 20k Input Z, 100 Ohm Output Z, -103dB noise

### Community 12 - "SP2120 Dimensions"
Cohesion: 1.0
Nodes (1): SP2120 Dimensions 482x44x160mm 2.2kg (1U rack)

### Community 13 - "Rack Blank Panel"
Cohesion: 1.0
Nodes (1): Rack U1 - 1U Blank Panel

### Community 14 - "Rack PDU"
Cohesion: 1.0
Nodes (1): Rack U9-U10 - Tripp Lite PDU

## Ambiguous Edges - Review These
- `CQ-12T Aux/Monitor Outputs 1-6 (TRS)` → `VOID Acoustics Airten V3 Speaker`  [AMBIGUOUS]
  02-equipment-manuals/mixers/Allen-Heath_CQ-12T_datasheet.pdf · relation: feeds
- `CQ-12T Aux/Monitor Outputs 1-6 (TRS)` → `VOID Acoustics Air Vantage Speaker`  [AMBIGUOUS]
  02-equipment-manuals/mixers/Allen-Heath_CQ-12T_datasheet.pdf · relation: feeds
- `VOID Acoustics Air Motion V2 Speaker` → `Bias V3 Power Amplifier (Void Acoustics)`  [AMBIGUOUS]
  05-speaker-assets/png/bias-v3-amp-front.png · relation: drives
- `VOID Acoustics Airten V3 Speaker` → `Bias V3 Power Amplifier (Void Acoustics)`  [AMBIGUOUS]
  05-speaker-assets/png/bias-v3-amp-front.png · relation: drives

## Knowledge Gaps
- **116 isolated node(s):** `Pioneer CDJ-3000 Instruction Manual`, `Pioneer DJM-V10 Instruction Manual`, `Zone: FOH Mains`, `Zone: FOH Fill`, `Zone: Outside Subs` (+111 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `CQ-12T Dimensions`** (2 nodes): `CQ-12T Physical Dimensions 291x242x89mm 2.4kg`, `CQ-12T Dimensions Drawing PNG: 290.4x254.4x88.2mm`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Source Wiring Docs`** (1 nodes): `Wiring Diagram Final PDF`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `SP2120 Specs`** (1 nodes): `SP2120 Specs: 20k Input Z, 100 Ohm Output Z, -103dB noise`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `SP2120 Dimensions`** (1 nodes): `SP2120 Dimensions 482x44x160mm 2.2kg (1U rack)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Rack Blank Panel`** (1 nodes): `Rack U1 - 1U Blank Panel`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Rack PDU`** (1 nodes): `Rack U9-U10 - Tripp Lite PDU`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `CQ-12T Aux/Monitor Outputs 1-6 (TRS)` and `VOID Acoustics Airten V3 Speaker`?**
  _Edge tagged AMBIGUOUS (relation: feeds) - confidence is low._
- **What is the exact relationship between `CQ-12T Aux/Monitor Outputs 1-6 (TRS)` and `VOID Acoustics Air Vantage Speaker`?**
  _Edge tagged AMBIGUOUS (relation: feeds) - confidence is low._
- **What is the exact relationship between `VOID Acoustics Air Motion V2 Speaker` and `Bias V3 Power Amplifier (Void Acoustics)`?**
  _Edge tagged AMBIGUOUS (relation: drives) - confidence is low._
- **What is the exact relationship between `VOID Acoustics Airten V3 Speaker` and `Bias V3 Power Amplifier (Void Acoustics)`?**
  _Edge tagged AMBIGUOUS (relation: drives) - confidence is low._
- **Why does `Allen & Heath CQ-12T Matrix Mixer` connect `Wiring Standards & Rider Docs` to `Armonia DSP Network`, `DJ Booth Zone`?**
  _High betweenness centrality (0.157) - this node is a cross-community bridge._
- **Why does `Turbosound Athens TCS-AN — Entrance (×2)` connect `DJ Booth Zone` to `Wiring Standards & Rider Docs`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Why does `Zone: Entrance Fill` connect `DJ Booth Zone` to `Bias V3 Amp Family`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._