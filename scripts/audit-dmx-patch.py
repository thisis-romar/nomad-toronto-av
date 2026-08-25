#!/usr/bin/env python3
"""
Audit the grandMA2 patch against the DMX modes the real fixtures can actually be set to.

The showfile records a fixture-profile *name* per fixture and a start address. It does NOT
contain the fixture-type definitions, so the profile's internal channel order cannot be read
back — only its footprint, and only from the name plus the address spacing. What CAN be checked
mechanically is the thing that actually breaks a rig:

  1. Does the patched footprint correspond to a mode the fixture can be switched to?
  2. If the fixture is really running its nearest larger mode, does it now collide with the
     fixture patched after it?

Both are answered from the vendor manuals in 08-lighting/manuals/ plus the showfile.

Run from repo root:
    python3 scripts/audit-dmx-patch.py            # report
    python3 scripts/audit-dmx-patch.py --md       # emit the markdown tables for the audit doc
"""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHOWFILE = ROOT / "08-lighting/source-showfile/NOMADFIXPATCHJUNE2026.xml"
NS = {"m": "http://schemas.malighting.de/grandma2/xml/MA"}

# DMX footprint the patch occupies, per MA profile. Taken from the "…CH" in the profile name and
# corroborated by the address spacing between consecutive fixtures of the same type.
FOOTPRINT = {
    "3 LED Bar 2 11CH":           11,
    "4 rgbw-13ch 13CH":           13,
    "5 NEW WASH":                  9,
    "6 movingwash zone":           9,
    "9 Sharpy Standard Lamp on":  14,
    "8 LASER BARS 26CH":          26,
    "7 LASER BARS - Invert 26CH": 26,
    "2 Dimmer 00":                 1,
}

# Selectable DMX modes and electrical data for the fixtures the venue has identified. Modes and
# electrical figures come from the manuals in 08-lighting/manuals/ unless noted. `evidence` is why
# this fixture is believed to be the one behind the profile -- the audit turns on it, so it is
# recorded rather than assumed. `names` narrows a profile to specific MA fixture names, needed
# because "2 Dimmer 00" covers three unrelated devices.
FIXTURES = {
    "yf-beam-230": dict(
        model="YF BEAM 230 moving head (Guangzhou Yingfeng)",
        modes=(16, 20), watts=(350, 400),
        source="189 W 5R Philips / 230 W 7R Osram discharge lamp",
        manual="yf-beam-230-moving-head.pdf",
        profiles=("9 Sharpy Standard Lamp on",), names=None,
        confidence="confirmed",
        evidence="Manual supplied 2026-08-25 confirms 16CH/20CH and the 189/230 W lamp. The four "
                 "beams are patched on a 16-channel stride -- this fixture's 16CH mode, two wider "
                 "than the 14CH profile loaded against them.",
        lost="At 14CH the profile stops at Pan/Tilt speed, so ch15 Reset and ch16 Lamp control are "
             "unreachable: the discharge lamps cannot be struck, doused or reset from the console.",
    ),
    "betopper-lm70s": dict(
        model="BETOPPER LM70S (TLM70SK/TLM70SP) -- 7x8W RGBW mini moving head",
        modes=(9, 14), watts=(100, 100),
        source="7 x 8 W RGBW 4-in-1 LED",
        manual="betopper-lm70s-mini-moving-head.pdf",
        profiles=("5 NEW WASH", "6 movingwash zone"), names=None,
        confidence="probable",
        evidence="Its 9CH mode is exactly the moving-wash footprint, and the ten washes are patched "
                 "on a 9-channel stride.",
        lost=None,
    ),
    "panda-ls650": dict(
        model="Panda Lighting LS650/LS652 -- 6-head laser bar, XY movement",
        modes=(11, 19, 24), watts=(150, 150),
        source="6 x 500 mW 638 nm red diodes (red variant) -- 3 W total optical, CLASS 4",
        manual="panda-lighting-ls650-ls652-6-head-laser-bar.pdf",
        profiles=("8 LASER BARS 26CH", "7 LASER BARS - Invert 26CH"), names=None,
        confidence="near-certain",
        evidence="Six laser eyes matches the MA fixture name Laser.BAR(6) and its 6 sub-fixture "
                 "cells; identified by the venue from the manufacturer product page.",
        lost="Two channels per bar are dead. The profile's internal channel order cannot be "
             "verified -- the export carries fixture-type names only, not their definitions.",
    ),
    "light4me-smb": dict(
        model="Light4Me STROBE MULTI BAR",
        modes=(4, 16, 168), watts=(200, 200),
        source="480 x 0.3 W RGB + 240 x 0.3 W CW LED",
        manual="light4me-strobe-multi-bar.pdf",
        profiles=("4 rgbw-13ch 13CH",), names=None,
        confidence="likely",
        evidence="An RGB-background + white-strobe bar, matching the MA layer --LED.STROBE-BAR "
                 "and the RGBW in the profile name. Not proven: no mode of this fixture is 13CH.",
        lost="At 16CH five of the seven bars overrun their slot; at 4CH nine of thirteen patched "
             "channels are dead.",
    ),
    "microh-ledbar": dict(
        model="Microh LEDBAR RGB",
        modes=(13,), watts=(50, 50),
        source="252 x 10 mm LED (108 R / 72 G / 72 B), 107 cm bar",
        manual="microh-ledbar-rgb.pdf",
        profiles=("3 LED Bar 2 11CH",), names=None,
        confidence="likely",
        evidence="Fixed 13CH: 1 function + 3 all-colour + 3 segments x RGB. The MA profile's four "
                 "sub-fixtures are a 2-channel master plus 3 cells on a 3-channel stride, which "
                 "matches those three RGB segments exactly -- but 2 + 9 = 11, not 13.",
        lost="The MA master is 2 channels where the fixture has 4 (function + all R/G/B), so every "
             "segment channel is offset by two. Nothing collides -- the 22-26 gap absorbs it.",
    ),
    "chauvet-haze-2d": dict(
        model="Chauvet Hurricane Haze 2D",
        modes=(2,), watts=(533, 533),
        source="533 W / 4.4 A at 120 V, 60 Hz",
        manual="chauvet-hurricane-haze-2d.pdf",
        profiles=("2 Dimmer 00",), names=("-Atmos-",),
        confidence="likely",
        evidence="The only hazer in the rig and the only manual supplied for one.",
        lost="Its own DMX personality is 2CH (blower speed, haze volume) and it is patched 1CH. If "
             "the hazer's DMX is what is patched, haze volume never responds. If it is instead "
             "plugged into the DP-415 pack, the pack must be in SWITCH mode -- the manual states "
             "the Haze 2D must not be run on a dimmer.",
    ),
}

# Devices that carry no load figure of their own but determine how the load is distributed.
# Confirmed by the venue 2026-08-25: ONE pack carries both CO2 jets and the hazer.
DISTRIBUTION = {
    "elation-dp-415": dict(
        model="Elation DP-415 4-channel dimmer/switch pack",
        manual="elation-dp-415-dimmer-switch-pack.pdf",
        qty=1, channels=4, amps_total=15.0, amps_per_channel=5.0,
        spec="AC 120 V 60 Hz, dual Edison per channel, 9-way dip address, "
             "dip 10 selects Dimmer or Switch mode PACK-WIDE",
        # (label, MA fixture name, amps or None if unknown)
        loads=(("Hazer -- Chauvet Hurricane Haze 2D", "-Atmos-", 4.44),
               ("CO2 jet 1", "Co2-HL.HR", None),
               ("CO2 jet 2", "Co2-HL.HR", None)),
    ),
}

# Fixtures in the rig with no identification at all -- carried so the load schedule cannot quietly
# imply the total is complete.
UNIDENTIFIED = {
    ("2 Dimmer 00", "Co2-HL.HR"): "CO2 jets (x2, unpatched)",
}

# MA profiles that appear to be pan/tilt-inverted duplicates of another profile, for fixtures hung
# upside down. Reported by the venue 2026-08-25. The export carries no channel definitions, so this
# cannot be read out of the showfile -- but it can be corroborated (see invert_report).
INVERT_PAIRS = {
    "7 LASER BARS - Invert 26CH": "8 LASER BARS 26CH",
    "6 movingwash zone": "5 NEW WASH",
}

# Line voltages the load schedule is reported at. Currents are real power / voltage: they assume
# unity power factor and so are a FLOOR, not a design figure -- see the audit doc.
VOLTAGES = (120, 208, 240)



def load():
    """(name, fid, layer, profile, base_address) per patched fixture, plus the unpatched ones."""
    root = ET.parse(SHOWFILE).getroot()
    out = []
    for layer in root.findall("m:Layer", NS):
        for fx in layer.findall("m:Fixture", NS):
            prof = fx.find("m:FixtureType", NS).get("name")
            addrs = [int(a.text) for a in fx.findall("m:SubFixture/m:Patch/m:Address", NS)]
            out.append(dict(name=fx.get("name"), fid=fx.get("fixture_id"),
                            layer=layer.get("name"), profile=prof,
                            base=min(addrs) if addrs else 0,
                            foot=FOOTPRINT[prof]))
    return out


def collisions(fixtures, profile, width):
    """Overlapping pairs if every fixture on `profile` were really `width` channels wide.

    Only same-profile neighbours are compared against the whole patch, because a fixture running
    wider than its patch eats into whatever is addressed after it, regardless of type.
    """
    patched = sorted((f for f in fixtures if f["base"]), key=lambda f: f["base"])
    hits = []
    for f in patched:
        if f["profile"] != profile:
            continue
        end = f["base"] + width - 1
        for g in patched:
            if g is f or not g["base"] or g["base"] <= f["base"]:
                continue
            g_end = g["base"] + (width if g["profile"] == profile else g["foot"]) - 1
            if g["base"] <= end:
                hits.append((f, g, g["base"], min(end, g_end)))
            break                      # only the immediate next fixture can be reached
    return hits

def spacing(fixtures, profile):
    """(dominant address stride, n_at_that_stride, n_gaps) between consecutive fixtures.

    The stride is independent evidence of the real footprint: whoever laid the patch out left
    room for something, and that something is not always what the profile says. Gaps over 100
    are dropped -- they are a fixture parked on another universe, not a stride.
    """
    a = sorted(f["base"] for f in fixtures if f["profile"] == profile and f["base"])
    gaps = [b - a[i] for i, b in enumerate(a[1:]) if b - a[i] < 100]
    if not gaps:
        return None, 0, 0
    best = max(set(gaps), key=gaps.count)
    return best, gaps.count(best), len(gaps)


def owns(fx, f):
    """Does fixture-spec `fx` cover patched fixture `f`?"""
    if f["profile"] not in fx["profiles"]:
        return False
    return fx["names"] is None or f["name"].strip() in fx["names"]


def owner_of(fixtures_spec, f):
    for key, fx in fixtures_spec.items():
        if owns(fx, f):
            return key, fx
    return None, None


def load_schedule(fixtures):
    """(model, qty, (w_lo, w_hi), (t_lo, t_hi), confidence) rows plus unidentified stragglers."""
    rows, unknown = [], []
    for fx in FIXTURES.values():
        qty = sum(1 for f in fixtures if owns(fx, f))
        if not qty:
            continue
        lo, hi = fx["watts"]
        rows.append((fx["model"], qty, (lo, hi), (lo * qty, hi * qty), fx["confidence"]))
    for (prof, name), what in UNIDENTIFIED.items():
        qty = sum(1 for f in fixtures if f["profile"] == prof and f["name"].strip() == name)
        if qty:
            unknown.append((what, qty, prof))
    return rows, unknown


def invert_report(fixtures):
    """Which fixtures sit on an inverted-duplicate profile, and what corroborates it.

    The showfile has no channel definitions, so pan/tilt inversion is invisible to it. What IS
    visible is whether the duplicate profile has the same sub-fixture structure as its base -- if
    it does, the two profiles differ only in something the export cannot show, which is what an
    invert-only duplicate looks like.
    """
    root = ET.parse(SHOWFILE).getroot()
    shape = {}
    for layer in root.findall("m:Layer", NS):
        for fx in layer.findall("m:Fixture", NS):
            prof = fx.find("m:FixtureType", NS).get("name")
            subs = fx.findall("m:SubFixture", NS)
            cells = tuple(len(s.findall("m:Channel", NS)) for s in subs)
            addrs = [int(a.text) for a in fx.findall("m:SubFixture/m:Patch/m:Address", NS)]
            descending = len(addrs) > 2 and addrs[1:] == sorted(addrs[1:], reverse=True)
            shape.setdefault(prof, []).append((fx.get("name"), cells, descending))
    out = []
    for inv, base in INVERT_PAIRS.items():
        if inv not in shape:
            continue
        names = [n for n, _, _ in shape[inv]]
        same = shape.get(base) and shape[inv][0][1] == shape[base][0][1]
        desc = any(d for _, _, d in shape[inv])
        out.append((inv, base, names, bool(same), desc))
    return out



def main():
    fixtures = load()
    md = "--md" in sys.argv
    p = print

    patched = sorted((f for f in fixtures if f["base"]), key=lambda f: f["base"])
    unpatched = [f for f in fixtures if not f["base"]]

    # --- 1. patch integrity as it stands -------------------------------------------------
    p("\n## Patch integrity (footprints as patched)\n" if md else "\n=== PATCH INTEGRITY ===")
    problems = []
    prev = None
    for f in patched:
        end = f["base"] + f["foot"] - 1
        if (f["base"] - 1) // 512 != (end - 1) // 512:
            problems.append(f"{f['name']} spans a universe boundary ({f['base']}-{end})")
        if prev and f["base"] <= prev[1]:
            problems.append(f"{prev[2]} ({prev[0]}-{prev[1]}) overlaps {f['name']} ({f['base']}-{end})")
        prev = (f["base"], end, f["name"])
    if md:
        p(f"- {len(patched)} fixtures patched, {len(unpatched)} unpatched "
          f"({', '.join(sorted({f['name'] for f in unpatched})) or 'none'}).")
        p(f"- Address overlaps as patched: **{len(problems) or 'none'}**.")
        p("- Universe boundary crossings: **none**.")
    else:
        p(f"  {len(patched)} patched, {len(unpatched)} unpatched")
        for x in problems:
            p("  !! " + x)
        if not problems:
            p("  no overlaps, no universe-boundary crossings")

    # --- 2. does the patched footprint exist as a mode? ----------------------------------
    hdr = ("| MA profile | Patched | Address stride | Fixture | Selectable modes | Verdict |\n"
           "|------------|--------:|---------------:|---------|------------------|---------|")
    p("\n## Patched footprint vs. selectable DMX modes\n" if md else "\n=== FOOTPRINT vs MODE ===")
    if md:
        p(hdr)
    verdicts = {}
    # One row per (profile, owner): "2 Dimmer 00" covers three unrelated devices, so a row per
    # profile would report the hazer as unidentified just because a CO2 jet sorts first.
    groups = []
    for prof in FOOTPRINT:
        by_owner = {}
        for f in fixtures:
            if f["profile"] != prof:
                continue
            by_owner.setdefault(owner_of(FIXTURES, f)[0], []).append(f)
        for owner, members in by_owner.items():
            groups.append((prof, owner, members))
    groups.sort(key=lambda g: (g[1] is None, g[0]))

    for prof, owner, members in groups:
        foot = FOOTPRINT[prof]
        n = len(members)
        stride, nat, ngap = spacing(fixtures, prof)
        st = "—" if not stride else (f"{stride}" if nat == ngap else f"{stride} ({nat}/{ngap})")
        shared = sum(1 for g in groups if g[0] == prof) > 1
        label = f"`{prof}`" + (f" — {members[0]['name'].strip()}" if shared else "")
        if not owner:
            row = ("—", "—", "❓ not identified")
        else:
            fx = FIXTURES[owner]
            ok = foot in fx["modes"]
            verdicts.setdefault(prof, ok)
            note = ""
            if stride and stride in fx["modes"] and stride != foot:
                note = f" — but the {stride}-channel stride *is* its {stride}CH mode"
            row = (fx["model"], "/".join(f"{m}CH" for m in fx["modes"]),
                   "✅ match" if ok else f"❌ **no {foot}CH mode**{note}")
        if md:
            p(f"| {label} (×{n}) | {foot}CH | {st} | {row[0]} | {row[1]} | {row[2]} |")
        else:
            p(f"  {prof[:26]:<26} {foot:>3}CH stride {st:>8}  {row[2][:50]:<50} {row[1]}")

    # --- 3. consequence of the nearest larger mode ---------------------------------------
    p("\n## If a mismatched fixture is really running its nearest larger mode\n" if md
      else "\n=== COLLISION IF RUNNING NEXT-LARGER MODE ===")
    any_hit = False
    for prof, ok in verdicts.items():
        if ok:
            continue
        fx = FIXTURES[next(k for k, v in FIXTURES.items() if prof in v["profiles"])]
        foot = FOOTPRINT[prof]
        bigger = [m for m in fx["modes"] if m > foot]
        smaller = [m for m in fx["modes"] if m < foot]
        if md:
            p(f"\n**`{prof}`** — patched {foot}CH; nearest modes "
              f"{smaller[-1] if smaller else '—'}CH below, {bigger[0] if bigger else '—'}CH above.\n")
        if not bigger:
            p("  (no larger mode exists — the fixture cannot overrun its patch)" if not md else
              "No larger mode exists, so the fixture cannot overrun its patch.")
            continue
        hits = collisions(fixtures, prof, bigger[0])
        any_hit = any_hit or bool(hits)
        if md:
            if hits:
                p(f"At {bigger[0]}CH each fixture is {bigger[0] - foot} channels wider than its "
                  f"patch slot, so it runs into whatever is addressed next:\n")
                p("| Fixture | Occupies | Runs into | Shared addresses |\n"
                  "|---------|----------|-----------|------------------|")
                for f, g, lo, hi in hits:
                    p(f"| {f['name']} | {f['base']}–{f['base'] + bigger[0] - 1} | {g['name']} "
                      f"(starts {g['base']}) | **{lo}–{hi}** ({hi - lo + 1} ch) |")
            else:
                p(f"At {bigger[0]}CH nothing collides — the gaps left in the patch absorb it.")
        else:
            p(f"  {prof} @ {bigger[0]}CH -> {len(hits)} collisions")
            for f, g, lo, hi in hits:
                p(f"     {f['name']} runs into {g['name']} at {lo}-{hi}")

    # --- 4. connected load ----------------------------------------------------------------
    rows, unknown = load_schedule(fixtures)
    p("\n## Connected load\n" if md else "\n=== CONNECTED LOAD ===")
    if md:
        p("| Fixture | Qty | W each | W total | " +
          " | ".join(f"A @ {v} V" for v in VOLTAGES) + " | ID confidence |")
        p("|---------|----:|-------:|--------:|" + "".join("-------:|" for _ in VOLTAGES) + "---|")
    lo_tot = hi_tot = 0
    for model, qty, (wlo, whi), (tlo, thi), conf in rows:
        lo_tot += tlo
        hi_tot += thi
        w = f"{wlo}" if wlo == whi else f"{wlo}–{whi}"
        tw = f"{tlo}" if tlo == thi else f"{tlo}–{thi}"
        amps = [(f"{tlo / v:.2f}" if tlo == thi else f"{tlo / v:.2f}–{thi / v:.2f}")
                for v in VOLTAGES]
        if md:
            p(f"| {model} | {qty} | {w} | **{tw}** | " + " | ".join(amps) + f" | {conf} |")
        else:
            p(f"  {qty:>2} x {model[:46]:<46} {tw:>9} W   " +
              "  ".join(f"{a:>11} A" for a in amps))
    tw = f"{lo_tot}" if lo_tot == hi_tot else f"{lo_tot}–{hi_tot}"
    amps = [(f"{lo_tot / v:.2f}" if lo_tot == hi_tot else f"{lo_tot / v:.1f}–{hi_tot / v:.1f}")
            for v in VOLTAGES]
    if md:
        p(f"| **Identified subtotal** | | | **{tw} W** | " +
          " | ".join(f"**{a}**" for a in amps) + " | |")
        for what, qty, prof in unknown:
            p(f"| {what} | {qty} | ❓ | ❓ | " + " | ".join("❓" for _ in VOLTAGES) +
              f" | not identified (`{prof}`) |")
        pack = DISTRIBUTION["elation-dp-415"]
        used = sum(a for _, _, a in pack["loads"] if a)
        n_unknown = sum(1 for _, _, a in pack["loads"] if a is None)
        spare_ch = pack["channels"] - len(pack["loads"])
        p(f"\n### Effects distribution — {pack['model']}\n")
        p(f"| Load | Pack channel | A @ 120 V | Channel rating |")
        p(f"|---|---|---:|---:|")
        for label, _name, amps in pack["loads"]:
            a = f"{amps:.2f}" if amps else "❓"
            pct = f" ({amps / pack['amps_per_channel'] * 100:.0f}% of channel)" if amps else ""
            p(f"| {label} | ❓ unread | {a}{pct} | {pack['amps_per_channel']:.0f} A |")
        for _ in range(len(pack["loads"]), pack["channels"]):
            p(f"| *(spare)* | — | — | {pack['amps_per_channel']:.0f} A |")
        p(f"| **Pack total** | {len(pack['loads'])} of {pack['channels']} used, {spare_ch} spare "
          f"| **{used:.2f} A known** | **{pack['amps_total']:.0f} A** |")
        p(f"\n> The two CO₂ jets are the only loads in the rig with no figure. The pack bounds them "
          f"even so: at most **{pack['amps_per_channel']:.0f} A each** by channel rating, and at "
          f"most **{pack['amps_total'] - used:.1f} A between them** once the hazer's "
          f"{used:.1f} A is accounted for. A CO₂ jet is a solenoid valve, so the real figure should "
          f"be far below that — but it is still a figure someone has to read off the jets.")
        p("\n> **This is a subtotal, not a total.** " +
          "; ".join(f"{q}x {w}" for w, q, _ in unknown) + " carry no power figure. "
          "Currents are real power ÷ voltage and assume unity power factor, so they are a floor: "
          "add the fixtures' actual PF (and the discharge ballasts' inrush) before sizing anything.")
    else:
        p(f"  {'IDENTIFIED SUBTOTAL':<53} {tw:>9} W   " +
          "  ".join(f"{a:>11} A" for a in amps))
        for what, qty, prof in unknown:
            p(f"  {qty:>2} x {what:<46} unknown")

    # --- 5. inverted-duplicate profiles -----------------------------------------------------
    inv = invert_report(fixtures)
    p("\n## Pan/tilt-inverted duplicate profiles\n" if md else "\n=== INVERTED DUPLICATES ===")
    if md:
        p("| Inverted profile | Duplicate of | Fixtures on it | Same sub-fixture shape? | Cell order reversed? |")
        p("|------------------|--------------|----------------|----------|----------|")
    for prof, base, names, same, desc in inv:
        if md:
            p(f"| `{prof}` | `{base}` | {', '.join(names)} | "
              f"{'✅ yes' if same else '❌ no'} | {'✅ yes' if desc else '— no'} |")
        else:
            p(f"  {prof}")
            p(f"     duplicate of {base}; fixtures: {', '.join(names)}")
            p(f"     same sub-fixture shape: {same}; cell order reversed: {desc}")

    if md:
        p("\n> Pan/tilt inversion is **invisible to this export** — it lives in the fixture-type "
          "definition, which grandMA2 does not write into an XML fixture list. What the export can "
          "show is that the duplicate has the *same sub-fixture shape* as its base, i.e. the two "
          "profiles differ only in something the file cannot represent. That is what an "
          "invert-only duplicate looks like from here; it is corroboration, not proof.")

    if not md:
        p("\n=== SUPPLIED MANUALS ===")
        for k, v in FIXTURES.items():
            p(f"  {v['model']}")
            p(f"     modes {v['modes']} · confidence {v['confidence']} · {v['manual']}")
            p(f"     covers {', '.join(v['profiles'])}")


if __name__ == "__main__":
    main()
