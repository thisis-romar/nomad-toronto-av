# Graph Report - nomad-toronto-av  (2026-04-29)

## Corpus Check
- 8 files · ~4,378,214 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 239 nodes · 316 edges · 21 communities detected
- Extraction: 88% EXTRACTED · 10% INFERRED · 1% AMBIGUOUS · INFERRED: 33 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]

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
- `VOID Acoustics Airten V3 Speaker` --drives--> `Bias V3 Power Amplifier (Void Acoustics)`  [AMBIGUOUS]
  02-equipment-manuals/speakers/VOID-Airten-V3-User-Manual-v2.1.pdf → 05-speaker-assets/png/bias-v3-amp.png
- `Allen & Heath CQ-12T Digital Mixer` --feeds--> `CDJ-3000 Rear: Audio Out L/R, Digital Out, AC In, LINK terminal (LAN), USB port`  [INFERRED]
  02-equipment-manuals/mixers/Allen-Heath_CQ-12T_datasheet.pdf → 05-speaker-assets/png/pioneer-cdj-3000-rear.png
- `VOID Acoustics Air Motion V2 Speaker` --drives--> `Bias V3 Power Amplifier (Void Acoustics)`  [AMBIGUOUS]
  02-equipment-manuals/speakers/VOID-Air-Motion-V2-User-Guide.pdf → 05-speaker-assets/png/bias-v3-amp.png
- `VOID Acoustics Air Motion V2 Speaker` --connected_by--> `Pioneer DJM-V10 Rear Panel View`  [INFERRED]
  02-equipment-manuals/speakers/VOID-Air-Motion-V2-User-Guide.pdf → 05-speaker-assets/png/pioneer-djm-v10-rear.png
- `VOID Acoustics Air Vantage Speaker` --feeds--> `Pioneer DJM-V10 (Equipment Entity)`  [INFERRED]
  02-equipment-manuals/speakers/VOID-Air-Vantage-User-Guide.pdf → 05-speaker-assets/png/pioneer-djm-v10.png

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

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (31): Bias V3 Amplifier, Bias V3 Amp Front View SVG, Bias V3 Amp Side View SVG, Bias Q2 #2 (S/N 00543758, IP 192.168.10.11), Bias Q5 (S/N 777758, IP 192.168.10.10), Bias V3 #1 (S/N 341130, IP 192.168.10.13), Bias V3 #2 (S/N 341132, IP 192.168.10.14), Bias V9 (OFFLINE) (+23 more)

### Community 1 - "Community 1"
Cohesion: 0.1
Nodes (27): AES14-1992 XLR Pin Assignment Standard, Technical Available Rider, ANSI/AVIXA D401.01:2023 Documentation Standard, Bias V9 — OFFLINE (Delay Subs), Cable Schedule (41 cables), Pioneer CDJ-3000 Instruction Manual, Pioneer CDJ-3000 (×4 units), Allen & Heath CQ-12T Matrix Mixer (+19 more)

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (25): Armonía DSP Control Network (192.168.10.x), ArmoníaPlus Control Software v2.8, Bias Q2 #1 — DJ Monitors, Bias Q2 #2 — Air Motion Bi-amp, Bias Q2/Q1/D1 User Guide V1.0, Bias Q5 User Guide V1.1, Bias Q5 — Subs Middle (4ch), Bias V3 #1 — Airten V3 FOH Fill (+17 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (23): Air Vantage Connectors: 1x speakON NL4, Air Vantage Dimensions: 719x415x660mm 23.5kg, Air Vantage Drivers: 12" LF horn-loaded + 1.5" HF coaxial, Air Vantage Specs: 2-way passive, 500W AES, 127dB cont/133dB peak, 8 Ohm, Airten V3 Connectors: 2x speakON NL4, Airten V3 Dimensions: 681x303x366mm 20kg, Airten V3 Drivers: 2x10" LF + 1.3" exit HF compression driver (coaxial), Airten V3 Specs: 2-way passive, 500W AES, 125dB cont/131dB peak, 4 Ohm (+15 more)

### Community 4 - "Community 4"
Cohesion: 0.1
Nodes (22): CQ-12T 2x Multi-FX Engines, CQ-12T 96kHz Processing / 96-bit Depth, CQ-12T Auto Mic Mixer (AMM), CQ-12T Aux/Monitor Outputs 1-6 (TRS), CQ-12T System Block Diagram (signal flow PNG), CQ-12T Bluetooth 4.1 Stereo Input, CQ-MixPad Control App (iOS/Android/Win/Mac), Allen & Heath CQ-12T Technical Datasheet (+14 more)

### Community 5 - "Community 5"
Cohesion: 0.1
Nodes (22): Air Motion V2 Connectors: 2x speakON NL4 (pins 1+/1- LF, pins 2+/2- MHF), Air Motion V2 Dimensions: 854x672x658mm 35.4kg, Air Motion V2 Drivers: 12" LF + 8" MF + 1.5" HF compression driver, Air Motion V2 Specs: 3-way bi-amp, 500W LF / 250W HMF AES, 134dB cont, 137dB peak, Bias Q3/Q5 speakON Wiring to VOID Speakers, Bias V3 Power Amplifier (Void Acoustics), Bias V3 Dimensional Drawing (side view): 439mm depth, ventilation bottom, Bias V3 Front Panel Drawing: 465mm W x 32.2mm H (1U rack), with display and controls (+14 more)

### Community 6 - "Community 6"
Cohesion: 0.1
Nodes (21): Bias Q5 Power Amplifier (Void Acoustics), Bias Q5 Dimensional Drawing: 483mm W x 44.5mm H x 495mm D (1U rack), Bias Q5 Ethernet/eCON Primary and Secondary Ports, Bias Q5 Front Panel (User Guide V1.1 cover diagram), Bias Q5 AC Input Phoenix 5-pin Mains Connector (non-standard), Bias Q5 speakON Output Connectors, Bias Q5 XLR Analog Inputs (ch1-5) and XLR Input ch6 analog, Stasys Xair Bias Q5 speakON Wiring (output 1 or 2, max 2 parallel at 2 Ohm) (+13 more)

### Community 7 - "Community 7"
Cohesion: 0.1
Nodes (21): Bias Q2 #1 (S/N 951058, IP 192.168.10.12), Issue #4: Athens TCS-AN Submodel Unconfirmed, Rack U4 - Bias Q2 #1 (DJ Monitors), Air Vantage DJ Booth Monitors (×2), Venu 215 V2 DJ Booth Sub (×2), Void Air Vantage, Void Air Vantage Front View SVG, Void Air Vantage Side View SVG (+13 more)

### Community 8 - "Community 8"
Cohesion: 0.43
Nodes (6): generate_image(), get_client(), main(), Call gpt-image-2 image edit endpoint with source as reference., Use gpt-4o-mini vision to score the generated image 1-10., score_image()

### Community 9 - "Community 9"
Cohesion: 0.67
Nodes (5): downloadAlphatheta(), downloadBuffer(), downloadTurbosound(), main(), saveBuffer()

### Community 10 - "Community 10"
Cohesion: 0.6
Nodes (5): buildOptionMaps(), ensureLabels(), getExistingIssues(), ghRaw(), setField()

### Community 11 - "Community 11"
Cohesion: 0.7
Nodes (4): callOpenAI(), handleCheckQuota(), handleGenerateImage(), handleRequest()

### Community 12 - "Community 12"
Cohesion: 0.83
Nodes (3): run(), tryClick(), tryLocator()

### Community 13 - "Community 13"
Cohesion: 0.67
Nodes (2): gql(), gqlAll()

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (3): EIA-310-D / IEC 60297 Rack Standard, 19-Inch Rack Standards Reference, SVG Rack Elevation Methodology

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (2): CQ-12T Physical Dimensions 291x242x89mm 2.4kg, CQ-12T Dimensions Drawing PNG: 290.4x254.4x88.2mm

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (1): Wiring Diagram Final PDF

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): SP2120 Specs: 20k Input Z, 100 Ohm Output Z, -103dB noise

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): SP2120 Dimensions 482x44x160mm 2.2kg (1U rack)

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): Rack U1 - 1U Blank Panel

### Community 22 - "Community 22"
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
- **118 isolated node(s):** `Call gpt-image-2 image edit endpoint with source as reference.`, `Use gpt-4o-mini vision to score the generated image 1-10.`, `Pioneer CDJ-3000 Instruction Manual`, `Pioneer DJM-V10 Instruction Manual`, `Zone: FOH Mains` (+113 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 13`** (4 nodes): `gh()`, `gql()`, `gqlAll()`, `gql.mjs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (2 nodes): `CQ-12T Physical Dimensions 291x242x89mm 2.4kg`, `CQ-12T Dimensions Drawing PNG: 290.4x254.4x88.2mm`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `Wiring Diagram Final PDF`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `SP2120 Specs: 20k Input Z, 100 Ohm Output Z, -103dB noise`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `SP2120 Dimensions 482x44x160mm 2.2kg (1U rack)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `Rack U1 - 1U Blank Panel`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `Rack U9-U10 - Tripp Lite PDU`
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
- **Why does `Allen & Heath CQ-12T Matrix Mixer` connect `Community 1` to `Community 2`, `Community 7`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Why does `Turbosound Athens TCS-AN — Entrance (×2)` connect `Community 7` to `Community 1`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Why does `Zone: Entrance Fill` connect `Community 7` to `Community 0`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._