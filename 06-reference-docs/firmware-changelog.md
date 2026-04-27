---
title: Nomad Toronto — Firmware & Software Changelog
description: Current firmware versions, latest available, download links, and update procedures for all AV system equipment
version: 1.0.0
created: 2026-04-27T00:00:00Z
last_updated: 2026-04-27T00:00:00Z
---

# Nomad Toronto — Firmware & Software Changelog

**Venue:** Nomad Toronto  
**System:** VOID Acoustics 18-speaker installation + Pioneer DJ source chain  
**Last audited:** 2026-04-27

---

## Status Summary

| Equipment | On-Site Version | Latest Available | Status | Priority |
|-----------|----------------|-----------------|--------|----------|
| Allen & Heath CQ-12T | 1.2.1 r4213 | **V1.2.2** | ⚠️ One release behind | Update recommended |
| Pioneer CDJ-3000 ×4 | Likely 3.22 | **3.22** | ✅ Current (verify on unit) | Confirm only |
| Pioneer DJM-V10 | Unknown | **1.20** | ❓ Unconfirmed | Check unit menu |
| VOID Bias V3 #1 (S/N 341130) | Unknown | Legacy — via ArmoníaPlus | ❓ Check in Armonía | N/A — legacy model |
| VOID Bias V3 #2 (S/N 341132) | Unknown | Legacy — via ArmoníaPlus | ❓ Check in Armonía | N/A — legacy model |
| VOID Bias Q5 (S/N 777758) | Unknown | **v1.12.0.76** | ❓ Check in Armonía | Update if behind |
| VOID Bias Q2 #1 (S/N 951058) | Unknown | **v1.12.0.84** (Q2+) | ❓ Verify amp generation first | Caution — see notes |
| VOID Bias Q2 #2 (S/N 00543758) | Unknown | **v1.12.0.84** (Q2+) | ❓ Verify amp generation first | Caution — see notes |
| VOID Bias V9 (offline) | Unknown | Legacy — via ArmoníaPlus | N/A — offline | No action |
| Drawmer SP2120 | N/A | N/A — analog hardware | ✅ No firmware | None |
| Turbosound Athens TCS-AN ×2 | Unknown | **V2.3** (Aug 2020) | ❓ Unconfirmed | Check via firmware tool |
| ArmoníaPlus (control software) | Unknown | **2.8** (Apr 2025) | Update before amp work | Update PC first |

---

## Allen & Heath CQ-12T

**On-site:** 1.2.1 r4213 (confirmed April 2026)  
**Latest:** V1.2.2

| Field | Detail |
|-------|--------|
| Release date | July 2025 |
| Release notes PDF | https://www.allen-heath.com/content/uploads/2025/07/CQ_FirmwareReleaseNotes_V1_2_2.pdf |
| Download page | https://www.allen-heath.com/hardware/cq/cq-12t/resources/ |
| Direct download | Navigate to Resources page above — A&H blocks direct deep-links; file is `.bin` format |
| Update method | **USB stick** (copy `.bin` to root of FAT32 USB, apply via console Settings menu) OR via MixPad app |
| Approximate time | 2–3 minutes |

**Changes in V1.2.2 vs on-site V1.2.1:**
- Improved USB-B streaming stability (CQ-12T specific)
- Added MIDI Active Sense
- Fixed Trim value loss on scene recall
- Fixed Output pre/post setting disappearing after reboot
- Fixed stereo USB channel name display on Windows
- Improved firmware update flow via MixPad app

> ⚠️ **Action:** Download V1.2.2 from Resources page and apply via USB before next event.

---

## Pioneer CDJ-3000 ×4

**On-site:** Likely 3.22 — confirm via UTILITY menu on unit  
**Latest:** 3.22 (January 15, 2026)

| Field | Detail |
|-------|--------|
| Release date | January 15, 2026 |
| Direct .zip download | https://downloads.support.alphatheta.com/firmwares/dj-players/CDJ-3000/CDJ3Kv322.zip (155 MB) |
| File in archive | `CDJ3Kv322.UPD` |
| Firmware page | https://support.alphatheta.com/en-US/articles/4404623755545 |
| Change history PDF | https://downloads.support.alphatheta.com/firmwares/dj-players/CDJ-3000/CDJ-3000-Firmware-Change-History-Ver322-en.pdf |
| Update guide | https://support.alphatheta.com/en-US/articles/4413929605529 |
| Update method | **USB stick only.** Format USB FAT/FAT32, copy `CDJ3Kv322.UPD` to root (do not rename). Power on while holding **IN/CUE + RELOOP/EXIT** simultaneously. ~1 minute per unit. |

**Changes in 3.22:**
- PRO DJ LINK compatibility with RMX-IGNITE
- Minor bug fixes

> ✅ **Action:** Confirm current version on each unit (UTILITY menu). If already 3.22 — no action needed. Update all 4 units simultaneously if behind.

---

## Pioneer DJM-V10

**On-site:** Unknown — check Settings menu  
**Latest:** 1.20 (January 15, 2026)

| Field | Detail |
|-------|--------|
| Release date | January 15, 2026 |
| Direct .zip download | https://downloads.support.alphatheta.com/firmwares/dj-mixers/DJM-V10/DJM-V10_120.zip (2.43 MB) |
| File in archive | `DJM-V10_120.upd` |
| Firmware page | https://support.alphatheta.com/en-US/articles/4404969283353 |
| Change history PDF | https://downloads.support.alphatheta.com/firmwares/dj-mixers/DJM-V10/DJM-V10-Firmware-Change-History-Ver120-en.pdf |
| Update guide | https://support.alphatheta.com/en-US/articles/4413930572441 |
| Update method | **USB stick.** Enter update mode: power on while holding **BEAT FX ON/OFF + FX FREQUENCY MID**. Insert USB with `.upd` at root. Wait for COMPLETE message. |

**Notable versions:**
| Version | Date | Key change |
|---------|------|-----------|
| 1.20 | Jan 15, 2026 | RMX-IGNITE support via USB digital send/return |
| 1.16 | May 14, 2025 | Fixed UASP USB storage device recognition |
| < 1.16 | — | UASP USB drives not recognized |

> ⚠️ **Action:** Check current version on unit. If below 1.16, USB drives (UASP type) may not work. **Use a non-UASP USB drive for the update process itself.**

---

## VOID Bias Amplifiers (V3, Q5, Q2, V9)

All Bias amplifiers run on Powersoft DSP platform. Firmware is delivered and managed via **ArmoníaPlus** software over the Armonía LAN (192.168.10.x network).

### ArmoníaPlus Control Software (update this first)

| Field | Detail |
|-------|--------|
| Latest version | **2.8** |
| Release date | April 1, 2025 |
| Download page | https://www.powersoft.com/en/download/software/armoniaplus |
| Release notes PDF | https://www.powersoft.com/wp-content/uploads/2025/03/Release-Note-ArmoniaPlus-2.8.pdf |
| Update method | Download installer from Powersoft, run on control PC |

**Changes in ArmoníaPlus 2.8:**
- New Channel Strip Mode (unified Gain/Mute/EQ/Delay/Polarity per channel)
- Combined Mute/Solo page
- Support for Unica 4T and Unica 8T touring amplifiers
- Various stability improvements

> ⚠️ **Update ArmoníaPlus on the control PC before performing any amp firmware updates.**

### Per-amplifier firmware

| Amp | S/N | IP | Latest FW | Download | Notes |
|-----|-----|----|-----------|----------|-------|
| Bias V3 #1 "air ten v3" | 341130 | 192.168.10.13 | Legacy — via ArmoníaPlus | ArmoníaPlus → Check Updates | VOID classifies V3 as **Legacy**; no standalone package |
| Bias V3 #2 "Outside Subs" | 341132 | 192.168.10.14 | Legacy — via ArmoníaPlus | ArmoníaPlus → Check Updates | Same as above |
| Bias Q5 "Subs Middle" | 777758 | 192.168.10.10 | **v1.12.0.76** | https://void-ponwxbckrv.s3.eu-west-2.amazonaws.com/bin-files/update-void-v1.12.0.76-x4.bin | x4 = 4-channel variant |
| Bias Q2 #1 "DJ Monitors" | 951058 | 192.168.10.12 | **v1.12.0.84** (Q2+) | https://d181c7pevbxova.cloudfront.net/media/support-materials/zips/upgrade4-void-v1.12.0.84.zip | ⚠️ Verify generation before applying — see caution below |
| Bias Q2 #2 "Air Motion" | 00543758 | 192.168.10.11 | **v1.12.0.84** (Q2+) | Same as above | Same caution |
| Bias V9 "DELAY SUBS" (**OFFLINE**) | — | — | Legacy | N/A | Do not update — unit is offline and disconnected |

**Update method for Q5/Q2 (manual USB):**
1. Download the `.bin` / `.zip` file
2. Extract to get the `.bin` firmware file
3. Copy to root of FAT32 USB stick
4. Apply via ArmoníaPlus → Firmware Update, or via front USB port per VOID guide

**VOID firmware update video guide:** https://www.youtube.com/watch?v=7eLW9-J9IRE

> ⚠️ **Bias Q2 caution:** The `upgrade4-void-v1.12.0.84.zip` targets the **Q2+ generation**. The serials on-site (951058, 00543758) may be original Q2 (pre-Plus) hardware. Applying Q2+ firmware to original Q2 hardware could brick the unit. **Verify hardware revision via ArmoníaPlus Device Info before applying standalone firmware.** Normal ArmoníaPlus "Check Updates" is the safe path — it will only offer compatible firmware.

> ⚠️ **Bias V3 / V9 legacy note:** VOID Acoustics classifies the Bias V3 and V9 as Legacy products. No standalone firmware package is published for these models. ArmoníaPlus may or may not offer updates via its automatic check — contact VOID Acoustics support (hello@voidacoustics.com) before attempting.

---

## Drawmer SP2120

**No firmware.** The SP2120 is a fully analog signal processor. No DSP, no microcontroller, no software companion. The only user controls are physical presets behind a key-locked front panel. No firmware updates exist or will ever exist for this unit.

Manual: https://www.drawmer.com/uploads/manuals/sp2120_operators_manual.pdf

---

## Turbosound Athens TCS-AN ×2

**On-site version:** Unknown — check via firmware update tool  
**Latest known:** V2.3 (August 3, 2020)

| Field | Detail |
|-------|--------|
| Release date | August 3, 2020 |
| Update tool | `TURBOSOUND_UsbUpdate_V2.3.exe` (Windows only) |
| Download page | https://www.musictribe.com/brand/c/Turbosound/downloads (navigate to specific TCS-AN model) |
| Direct .exe URL | Currently unreachable via `mediadl.musictribe.com` CDN — download from musictribe.com product page |
| Update method | Windows PC + USB cable to speaker. Run `.exe`, follow prompts. Speaker must be powered on. |
| Connection | USB-B port on rear panel of speaker |

**Firmware history:**
| Version | Notes |
|---------|-------|
| V2.3 | Latest known. Fixes for HW:B hardware revision; improved error messaging |
| V2.x | Current firmware generation (units pre-2018 shipped with V1) |
| V1.x | Legacy — upgrade to V2.3 recommended if found |

> ⚠️ **Submodel not yet confirmed** — Athens TCS-AN exact model (TCS122/64-AN, TCS122/96-AN, TCS152/64-AN, etc.) to be identified via rear type-plate photo on next site visit (open issue #4). Confirm correct firmware package for your exact model on musictribe.com before updating.

---

## Open Actions

| # | Device | Action | Urgency |
|---|--------|--------|---------|
| 1 | **CQ-12T** | Update 1.2.1 → V1.2.2 | Medium — one maintenance release behind |
| 2 | **DJM-V10** | Check on-unit firmware version via Settings | Low |
| 3 | **CDJ-3000 ×4** | Confirm 3.22 via UTILITY menu | Low — likely current |
| 4 | **All Bias amps** | Update ArmoníaPlus to 2.8 on control PC | Medium — prerequisite for amp updates |
| 5 | **Bias Q5** | Check v1.12.0.76 via ArmoníaPlus after updating software | Low |
| 6 | **Bias Q2 ×2** | Verify hardware generation, then check firmware via ArmoníaPlus | Medium — caution applies |
| 7 | **Athens TCS-AN ×2** | Identify exact model (rear type-plate), then check firmware V2.3 | Low |

---

*Generated 2026-04-27 · Sources: Allen & Heath, AlphaTheta, VOID Acoustics, Powersoft, Turbosound/Music Tribe · EMBLEM PROJECTS INC.*
