---
title: Nomad Toronto — Emergency Procedures (AV System)
description: Emergency shutdown, fault isolation, and recovery procedures for the Nomad Toronto VOID Acoustics system.
version: 1.0.0
created: 2026-04-27T00:00:00Z
last_updated: 2026-04-27T00:00:00Z
---

# Nomad Toronto — Emergency Procedures (AV System)

> **For fire / medical / security emergencies: follow venue emergency plan first. Audio system is secondary.**

---

## 1. Full Emergency Shutdown (fastest)

**Use when:** fire alarm, power emergency, venue evacuation, or uncontrolled feedback/noise.

1. Press the **MASTER** fader on the **DJM-V10** to minimum (zero).
2. Press **MUTE ALL** on the **Allen & Heath CQ-12T** (front panel button or MixPad app).
3. If sound continues — cut power at the **Tripp Lite PDU** (rear of rack, U9–U10).
4. If PA is still active — the amp rack has individual IEC C20 breakers. Pull the rack from power at the wall breaker panel.

**Do NOT touch the Bias V9 CPC 45A breaker** — it is already OFF and the unit is disconnected. Leave it alone.

---

## 2. Feedback / Runaway Noise

**Use when:** loud feedback, uncontrolled oscillation, or distortion from PA.

1. **DJM-V10:** Pull master fader to zero immediately.
2. **CQ-12T:** Press MUTE on the affected output (Main LR, MonOut, or BakFil).
3. Identify source:
   - Check all open mic/line inputs on CQ-12T CH5–CH10 for accidental signal.
   - Check DJM-V10 channel gains — ensure no channel is peaking.
   - Check SP2120 clip indicators (front panel LED bargraphs).
4. Once muted, investigate root cause before un-muting.

---

## 3. Amplifier Fault / Blown Amp

**Signs:** single zone suddenly silent, amp STATUS LED red, burning smell from rack.

1. Mute the CQ-12T output feeding that amp.
2. In Armonía (if accessible): check Device Status for the affected amp (192.168.10.x).
3. Do NOT leave the rack running if there is a burning smell — shut down the full system.
4. **Affected zones and their impact:**

| Amp | Zone lost if amp fails |
|-----|----------------------|
| V3 #2 | Outside subs L+R AND signal to Q5 + Q2 #2 + V3 #1 (entire FOH!) |
| Q5 | Middle subs only |
| Q2 #2 | FOH mains (Air Motion) |
| V3 #1 | FOH fills (Airten) |
| Q2 #1 | DJ booth monitors + booth sub |

> ⚠️ **V3 #2 is the signal hub.** If V3 #2 fails, the entire FOH system loses signal — not just outside subs. Use the Drawmer SP2120 line outputs directly to patch Q5/Q2 #2/V3 #1 as a bypass if needed (requires cabling change).

---

## 4. CQ-12T Freeze / App Disconnect

**Use when:** MixPad app loses connection or CQ-12T touchscreen freezes.

1. All audio continues at last set levels — this is NOT a system emergency.
2. Restart the MixPad app on the control device.
3. If the unit is frozen: hold the power button on the CQ-12T for 5 seconds to reboot. Audio will drop briefly during reboot (~30 seconds).
4. Scene recall: the CQ-12T stores the last scene on power cycle. Confirm all output levels after reboot.
5. Firmware note: V1.2.2 (available) fixes some CQ-12T stability issues. Update at next maintenance window.

---

## 5. Armonía DSP Loss (amps go to default)

**Use when:** control PC or Armonía software disconnects from amp network.

1. All amps continue operating at their **last DSP settings** — this is normal and safe.
2. Armonía is control-only; amps are standalone and do not require it to run.
3. Reconnect the control PC to the 192.168.10.x network and relaunch Armonía to restore remote monitoring.
4. Do NOT factory reset any amplifier unless explicitly authorised — all crossover, delay, and gain settings will be lost.

---

## 6. Power Failure (partial)

**If one amp circuit trips:**
1. Check the venue breaker panel for the affected circuit.
2. Do NOT reset a tripped breaker without investigating the cause.
3. The Q5 uses a Phoenix 5-pin mains connector — its breaker rating is TBC (Issue #7). Confirm with the venue electrician before resetting.

**If total power loss:**
1. All amps have soft-start protection — they will come up automatically when power is restored.
2. The CQ-12T will reboot and recall its last scene.
3. Allow 30–60 seconds for amps to initialise before sending signal.
4. Check Armonía for any fault flags after power restoration.

---

## 7. Booth Monitor Loss

**Use when:** DJ cannot hear monitors.

1. Check the CQ-12T MonOut fader — confirm it is not muted and is set to −32 dB or above.
2. Check Q2 #1 STATUS LED (Pos 4 in rack) — should be green.
3. Check Phoenix→NL4 cables at rear of Q2 #1 — confirm not unplugged.
4. If booth sub (Venu 215) is working but monitors (Air Vantage) are not: check Phoenix→NL4 adapter cables for Air Vantage (Q2 #1 CH1/CH2).

---

## 8. Entrance Speakers (Athens) Silent

**Use when:** entrance fill speakers not producing sound.

1. Athens speakers are **self-powered** — check their individual power switches (rear panel).
2. Check the XLR cables from the CQ-12T BakFil output to each Athens speaker.
3. Check the BakFil level on CQ-12T — confirm not muted, set to −34 dB or above.
4. Athens firmware may need updating (V2.3) — see `06-reference-docs/firmware-changelog.md`.

---

## 9. Contact for Technical Emergencies

| Role | Contact |
|------|---------|
| Venue general | 647-643-8823 · info@nomad725.ca |
| In-house technician | *(named contact TBC — Issue #5)* |
| VOID Acoustics support | +44 (0) 1202 666 006 · hello@voidacoustics.com |
| Allen & Heath support | support@allen-heath.com |
| Emblem Projects | admin+claude@emblemprojects.com |

---

## 10. Post-Emergency Checklist

After any emergency shutdown or fault:

- [ ] Identify and document the cause
- [ ] Inspect SP2120 clip indicators — reset if tripped
- [ ] Check all amplifier STATUS LEDs in Armonía before full restart
- [ ] Confirm CQ-12T scene settings are intact after any reboot
- [ ] Log the incident with date, time, and description

---

*Nomad Toronto · Emergency Procedures · Rev 1.0 · April 2026 · EMBLEM PROJECTS INC.*
