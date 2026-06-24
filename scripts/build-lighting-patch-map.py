#!/usr/bin/env python3
"""
Generate a schematic DMX patch-map SVG for the NOMAD Toronto lighting rig directly from the
grandMA2 showfile. This is a PATCH map (address allocation per universe), NOT a physical plot:
all fixture positions in the showfile are 0,0,0, so no to-scale layout can be drawn.

Run from repo root:
    python3 scripts/build-lighting-patch-map.py
Writes: 08-lighting/assets/svg/dmx-patch-map.svg
Regenerate whenever the showfile is re-exported.
"""
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHOWFILE = ROOT / "08-lighting/source-showfile/NOMADFIXPATCHJUNE2026.xml"
OUT = ROOT / "08-lighting/assets/svg/dmx-patch-map.svg"
NS = {"m": "http://schemas.malighting.de/grandma2/xml/MA"}

# MA profile name -> (group key, DMX footprint, short label prefix)
PROFILE = {
    "3 LED Bar 2 11CH":            ("djled",  11, "DJ"),
    "4 rgbw-13ch 13CH":            ("strobe", 13, "S"),
    "5 NEW WASH":                  ("wash",    9, "W"),
    "6 movingwash zone":           ("wash",    9, "W"),
    "9 Sharpy Standard Lamp on":   ("beam",   14, "B"),
    "8 LASER BARS 26CH":           ("laser",  26, "L"),
    "7 LASER BARS - Invert 26CH":  ("laser",  26, "L"),
    "2 Dimmer 00":                 ("fx",      1, "FX"),
}
GROUP = {
    "djled":  ("#f1c40f", "DJ LED bar"),
    "strobe": ("#e74c3c", "LED strobe bar"),
    "wash":   ("#1abc9c", "Moving wash"),
    "beam":   ("#3498db", "Moving beam (Sharpy)"),
    "laser":  ("#e67e22", "Laser bar"),
    "fx":     ("#95a5a6", "CO2 / haze (FX)"),
}

def short(name):
    # "Laser.BAR(6) 8" -> 8 ; "M.Wash 10" -> 10 ; "M.BEAM 2" -> 2 ; "LED.Strobe-BAR 7" -> 7
    tail = name.replace("(6)", "").split()[-1]
    return tail

def parse():
    root = ET.parse(SHOWFILE).getroot()
    fixtures = []  # (group, footprint, label, universe, rel_start, abs_start, unpatched)
    for layer in root.findall("m:Layer", NS):
        for fx in layer.findall("m:Fixture", NS):
            if fx.get("is_multipatch") == "true":
                continue
            prof = fx.find("m:FixtureType", NS).get("name")
            grp, fp, pre = PROFILE[prof]
            addr = int(fx.find("m:SubFixture/m:Patch/m:Address", NS).text)
            name = fx.get("name")
            # short label
            lbl = pre + short(name) if pre not in ("DJ", "FX") else ("DJ" if pre == "DJ" else short(name)[:4])
            if pre == "FX":
                lbl = "Haze" if name.strip().startswith("-Atmos") else "CO2"
            if addr == 0:
                fixtures.append((grp, fp, lbl, None, 0, 0, True))
            else:
                u = (addr - 1) // 512 + 1
                rel = addr - (u - 1) * 512
                fixtures.append((grp, fp, lbl, u, rel, addr, False))
    return fixtures

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def build():
    fx = parse()
    # layout
    W, MARGIN = 1120, 40
    track_w = W - 2 * MARGIN - 90      # space for the 1-512 axis
    x0 = MARGIN + 90
    px = track_w / 512.0
    row_h = 120
    bar_h = 34
    universes = [1, 2]
    H = 150 + row_h * len(universes) + 150
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Segoe UI,Arial,sans-serif">')
    s.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    # header
    s.append(f'<rect x="0" y="0" width="{W}" height="86" fill="#1a1a2e"/>')
    s.append(f'<text x="{MARGIN}" y="40" fill="#ffffff" font-size="22" font-weight="700">N<tspan fill="#e8b923">O</tspan>MAD Toronto — DMX Patch Map</text>')
    s.append(f'<text x="{MARGIN}" y="66" fill="#aaaaaa" font-size="12">grandMA2 "Nomad" v3.9.60 · showfile nomad_2026-06-13_kayo-toronto-ft-pools · schematic address allocation (NOT a physical plot — positions unknown)</text>')

    y = 140
    for u in universes:
        s.append(f'<text x="{MARGIN}" y="{y-14}" fill="#1a1a2e" font-size="14" font-weight="700">Universe {u}</text>')
        s.append(f'<text x="{MARGIN}" y="{y+2}" fill="#777" font-size="10">{(u-1)*512+1}–{u*512}</text>')
        # axis track
        s.append(f'<rect x="{x0}" y="{y}" width="{track_w}" height="{bar_h}" fill="#f2f2f4" stroke="#ddd"/>')
        # ticks every 64
        for a in range(0, 513, 64):
            tx = x0 + a * px
            s.append(f'<line x1="{tx:.1f}" y1="{y}" x2="{tx:.1f}" y2="{y+bar_h+4}" stroke="#ccc"/>')
            s.append(f'<text x="{tx:.1f}" y="{y+bar_h+16}" fill="#999" font-size="8" text-anchor="middle">{a if a else 1}</text>')
        # fixtures in this universe
        ufx = sorted([f for f in fx if f[3] == u], key=lambda f: f[4])
        stagger = 0
        for grp, fp, lbl, uni, rel, absa, unp in ufx:
            bx = x0 + (rel - 1) * px
            bw = max(fp * px, 2.0)
            color = GROUP[grp][0]
            s.append(f'<rect x="{bx:.1f}" y="{y}" width="{bw:.1f}" height="{bar_h}" fill="{color}" stroke="#1a1a2e" stroke-width="0.5"><title>{esc(lbl)} · {GROUP[grp][1]} · abs {absa} (U{uni}/{rel}) · {fp}ch</title></rect>')
            # staggered label above to reduce overlap
            ly = y - 6 - (stagger % 3) * 12
            lx = bx + bw / 2
            s.append(f'<line x1="{lx:.1f}" y1="{ly+2}" x2="{lx:.1f}" y2="{y}" stroke="#bbb" stroke-width="0.5"/>')
            s.append(f'<text x="{lx:.1f}" y="{ly}" fill="#333" font-size="8.5" text-anchor="middle">{esc(lbl)}</text>')
            stagger += 1
        y += row_h

    # unpatched callout
    unp = [f for f in fx if f[6]]
    if unp:
        labels = ", ".join(sorted({f[2] for f in unp}))
        s.append(f'<rect x="{MARGIN}" y="{y-10}" width="{W-2*MARGIN}" height="30" fill="#fff3cd" stroke="#f0c040"/>')
        s.append(f'<text x="{MARGIN+12}" y="{y+9}" fill="#7a5c00" font-size="11">⚠ UNPATCHED (DMX address 0): {esc(labels)} — patch &amp; verify on-site.</text>')
        y += 44

    # legend
    s.append(f'<text x="{MARGIN}" y="{y+10}" fill="#1a1a2e" font-size="11" font-weight="700">Legend</text>')
    lx = MARGIN; ly = y + 28
    for key, (color, name) in GROUP.items():
        s.append(f'<rect x="{lx}" y="{ly-10}" width="14" height="14" fill="{color}" stroke="#1a1a2e" stroke-width="0.5"/>')
        s.append(f'<text x="{lx+20}" y="{ly+1}" fill="#333" font-size="10">{esc(name)}</text>')
        lx += 175
    s.append(f'<text x="{MARGIN}" y="{ly+28}" fill="#888" font-size="9">Block width scales with DMX footprint. Full per-fixture detail: 07-tech-pack/dmx-patch-schedule.md · EMBLEM PROJECTS INC. · 2026-06-24</text>')

    s.append('</svg>')
    OUT.write_text("\n".join(s), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(fx)} fixtures, {OUT.stat().st_size} bytes)")

if __name__ == "__main__":
    build()
