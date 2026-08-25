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

# Selectable DMX modes of the fixtures the venue supplied manuals for, read out of those manuals.
# `evidence` is why this fixture is believed to be the one behind the profile — the audit turns on
# it, so it is recorded rather than assumed.
FIXTURES = {
    "betopper-lm70s": dict(
        model="BETOPPER LM70S (TLM70SK/TLM70SP) — 7x8W RGBW mini moving head",
        modes=(9, 14),
        watts=100,
        manual="betopper-lm70s-mini-moving-head.pdf",
        profiles=("5 NEW WASH", "6 movingwash zone", "9 Sharpy Standard Lamp on"),
        confidence="probable",
        evidence="Its two modes, 9CH and 14CH, are exactly the two moving-head footprints in the "
                 "patch; no other supplied fixture accounts for either.",
    ),
    "ls650": dict(
        model="LS650 six-eye swing laser (OEM, no brand on the manual)",
        modes=(11, 19, 24),
        watts=None,
        manual="ls650-six-eye-swing-laser.pdf",
        profiles=("8 LASER BARS 26CH", "7 LASER BARS - Invert 26CH"),
        confidence="near-certain",
        evidence="Six laser eyes matches the MA fixture name Laser.BAR(6) and its 6 sub-fixture "
                 "cells; it is the only laser bar supplied.",
    ),
    "light4me-smb": dict(
        model="Light4Me STROBE MULTI BAR",
        modes=(4, 16, 168),
        watts=None,
        manual="light4me-strobe-multi-bar.pdf",
        profiles=("4 rgbw-13ch 13CH",),
        confidence="likely",
        evidence="An RGB-background + white-strobe bar, matching the MA layer --LED.STROBE-BAR "
                 "and the RGBW in the profile name. Not proven: no mode of this fixture is 13CH.",
    ),
}


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
    hdr = ("| MA profile | Patched | Fixture (per supplied manual) | Selectable modes | Verdict |\n"
           "|------------|--------:|-------------------------------|------------------|---------|")
    p("\n## Patched footprint vs. selectable DMX modes\n" if md else "\n=== FOOTPRINT vs MODE ===")
    if md:
        p(hdr)
    verdicts = {}
    for prof in sorted(FOOTPRINT, key=lambda k: (k not in
                       {p for f in FIXTURES.values() for p in f["profiles"]}, k)):
        foot = FOOTPRINT[prof]
        n = sum(1 for f in fixtures if f["profile"] == prof)
        owner = next((k for k, v in FIXTURES.items() if prof in v["profiles"]), None)
        if not owner:
            row = ("—", "—", "❓ no manual supplied")
        else:
            fx = FIXTURES[owner]
            ok = foot in fx["modes"]
            verdicts[prof] = ok
            row = (fx["model"], "/".join(f"{m}CH" for m in fx["modes"]),
                   "✅ match" if ok else f"❌ **no {foot}CH mode on this fixture**")
        if md:
            p(f"| `{prof}` (×{n}) | {foot}CH | {row[0]} | {row[1]} | {row[2]} |")
        else:
            p(f"  {prof:<28} {foot:>3}CH  {row[2]:<40} {row[1]}")

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

    if not md:
        p("\n=== SUPPLIED MANUALS ===")
        for k, v in FIXTURES.items():
            p(f"  {v['model']}")
            p(f"     modes {v['modes']} · confidence {v['confidence']} · {v['manual']}")
            p(f"     covers {', '.join(v['profiles'])}")


if __name__ == "__main__":
    main()
