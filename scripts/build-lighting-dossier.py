#!/usr/bin/env python3
"""
Render the full lighting dossier: everything known about the NOMAD Toronto rig, in one document.

This is the reference companion to the scannable correlation page. Where that page answers "what
did you correlate", this one is meant to be the thing someone works from at the rig -- the complete
fixture schedule, and the DMX channel map of every fixture from its own manual, which until now
existed nowhere in this repo.

Patch geometry is read from the showfile and fixture data from audit-dmx-patch.py, so the schedule
and the load figures cannot drift from their sources. The channel maps are transcribed from the
manuals in 08-lighting/manuals/ and are the one part of this file that is hand-entered -- each one
records which manual page it came from.

Run from repo root:
    python3 scripts/build-lighting-dossier.py [out.html]
Default output: 08-lighting/assets/lighting-dossier.html
"""
import importlib.util
import sys
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHOWFILE = ROOT / "08-lighting/source-showfile/NOMADFIXPATCHJUNE2026.xml"
NS = {"m": "http://schemas.malighting.de/grandma2/xml/MA"}

_spec = importlib.util.spec_from_file_location("audit", Path(__file__).parent / "audit-dmx-patch.py")
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)

FAMILY = {
    "beam":   ("#0072B2", "Moving beams"),
    "laser":  ("#D55E00", "Laser bars"),
    "wash":   ("#009E73", "Moving washes"),
    "strobe": ("#CC79A7", "Strobe bars"),
    "djled":  ("#E69F00", "DJ-deck bar"),
    "fx":     ("#56B4E9", "Effects"),
}
GROUP_OF = {
    "3 LED Bar 2 11CH": "djled", "4 rgbw-13ch 13CH": "strobe",
    "5 NEW WASH": "wash", "6 movingwash zone": "wash",
    "9 Sharpy Standard Lamp on": "beam",
    "8 LASER BARS 26CH": "laser", "7 LASER BARS - Invert 26CH": "laser",
    "2 Dimmer 00": "fx",
}

# ---------------------------------------------------------------------------------------------
# DMX channel maps, transcribed from the manuals in 08-lighting/manuals/.
# `lost` marks a channel the patched footprint cannot reach. This is the detail that lets someone
# build a correct fixture profile without opening the PDFs.
# ---------------------------------------------------------------------------------------------
CHANNEL_MAPS = [
    dict(key="yf-beam-230", grp="beam", mode=16, patched=14, qty=4,
         profile="9 Sharpy Standard Lamp on", source="manual p.10, “10、Channels”",
         alt="A 20CH mode adds 17 Blank · 18 Colour-wheel speed · 19 Dimming/prism/atomisation "
             "speed · 20 Gobo-wheel speed.",
         ch=[(1, "Colour wheel"), (2, "Blackout / strobe"), (3, "Dimmer"), (4, "Gobo wheel"),
             (5, "Prism"), (6, "Prism rotation"), (7, "Macro"), (8, "Frost"), (9, "Focus"),
             (10, "Pan"), (11, "Pan fine"), (12, "Tilt"), (13, "Tilt fine"),
             (14, "Pan and tilt speed"), (15, "Reset"), (16, "Lamp control")]),
    dict(key="panda-ls650", grp="laser", mode=24, patched=26, qty=9,
         profile="8 LASER BARS 26CH · 7 LASER BARS - Invert 26CH", source="manual p.5, “24CH”",
         alt="Also offers 19CH (drops the effect and auto-run block) and 11CH (Y1–Y6 collapse to a "
             "single all-tilt channel). The patch reserves 26, two more than the fixture's widest "
             "mode, so channels 25–26 do not exist on the fixture.",
         ch=[(1, "X-axis stroke — 0–360°"), (2, "X-axis fine"), (3, "X-axis speed"),
             (4, "Y1 tilt — 0–106.8°"), (5, "Y2 tilt"), (6, "Y3 tilt"), (7, "Y4 tilt"),
             (8, "Y5 tilt"), (9, "Y6 tilt"), (10, "Y1–Y6 all tilt"), (11, "Y-axis speed"),
             (12, "Main switch — 0–127 off / 128–255 on"), (13, "Strobe"),
             (14, "Laser 1 on/off"), (15, "Laser 2"), (16, "Laser 3"), (17, "Laser 4"),
             (18, "Laser 5"), (19, "Laser 6"), (20, "Laser auto — 20 effects"),
             (21, "Laser auto speed"), (22, "Motor auto-run / sound"), (23, "Auto-run speed"),
             (24, "Reset — 128–255")]),
    dict(key="light4me-smb", grp="strobe", mode=16, patched=13, qty=7,
         profile="4 rgbw-13ch 13CH", source="manual p.11, “DMX structure — 16CH”",
         alt="Also offers 4CH (R/G/B/W dimmers only) and a 168CH pixel mode — 48 RGB sections on "
             "ch1–144, then 24 white sections on ch145–168.",
         ch=[(1, "Master dimmer"), (2, "Strobe — RGB"), (3, "Red dimmer"), (4, "Green dimmer"),
             (5, "Blue dimmer"), (6, "Background RGB effects"), (7, "Ch6 speed"),
             (8, "Strobe — white"), (9, "White dimmer"), (10, "Main white effects"),
             (11, "Ch10 speed"), (12, "Strobe — RGBW"), (13, "Main RGBW effects"),
             (14, "Ch13 speed"), (15, "Background colour"), (16, "Background dimmer")]),
    dict(key="betopper-lm70s", grp="wash", mode=9, patched=9, qty=10,
         profile="5 NEW WASH · 6 movingwash zone", source="manual p.4–5, “9 Channels Mode”",
         alt="Also offers 14CH: pan / pan fine / tilt / tilt fine / speed / dimmer-strobe / R / G / "
             "B / W / colour macros / colour speed / auto-programs / reset. Not in use here.",
         ch=[(1, "X axis (pan)"), (2, "Y axis (tilt)"),
             (3, "Master — 0–8 off · 8–135 dim · 136–240 strobe · 241–255 power"),
             (4, "Red"), (5, "Green"), (6, "Blue"), (7, "White"),
             (8, "XY motor speed"), (9, "Reset — 150–200")]),
    dict(key="microh-ledbar", grp="djled", mode=13, patched=11, qty=1,
         profile="3 LED Bar 2 11CH", source="manual p.3, “Channel Assignment”",
         alt="Fixed 13 channels — no other mode. The MA profile allots a 2-channel master where the "
             "fixture has four, so the segment block lands two channels early.",
         ch=[(1, "Function select — 0–10 dimmer · 11–51 strobe · 52–91 fade · 92–131 auto colour · "
                "132–255 chases 1–6"),
             (2, "All red"), (3, "All green"), (4, "All blue"),
             (5, "Segment 1 red"), (6, "Segment 1 green"), (7, "Segment 1 blue"),
             (8, "Segment 2 red"), (9, "Segment 2 green"), (10, "Segment 2 blue"),
             (11, "Segment 3 red"), (12, "Segment 3 green"), (13, "Segment 3 blue")]),
    dict(key="chauvet-haze-2d", grp="fx", mode=2, patched=1, qty=1,
         profile="2 Dimmer 00 (-Atmos-)", source="manual p.13, “DMX Channel Assignments”",
         alt="Fixed 2 channels — no other personality. Whether this matters depends on whether the "
             "patched channel is the hazer's own DMX or a DP-415 pack channel.",
         ch=[(1, "Blower speed — low→high"), (2, "Haze volume — low→high")]),
]

EVIDENCE = {
    "yf-beam-230": ("Confirmed by manual",
        "The four beams are patched on a uniform 16-channel stride — exactly this fixture's 16CH "
        "mode, and two wider than the 14CH profile loaded against them. The manual confirms the "
        "16/20CH modes and the 189 W 5R Philips / 230 W 7R Osram lamp. “Standard Lamp on” is a "
        "Clay Paky Sharpy mode name and a Sharpy's own lamp is a 189 W MSD Platinum 5R, so the "
        "profile was a reasonable pick for a Sharpy-clone — the brand was never supported, the "
        "class was."),
    "panda-ls650": ("Near-certain",
        "Six laser eyes against the MA fixture name <code>Laser.BAR(6)</code> and its six "
        "sub-fixture cells. The structure matches attribute for attribute: MA records one master "
        "of 7 attributes plus 6 cells of 2, and the LS650's 24CH mode gives each eye exactly two — "
        "a tilt position (ch4–9) and a laser on/off (ch14–19) — with seven whole-fixture "
        "attributes (ch1–3, 10–13). 7 + 6×2 = 19, which is the attribute count the export holds."),
    "betopper-lm70s": ("Probable",
        "Its 9CH mode is the wash footprint and the address stride, both. No other fixture "
        "supplied accounts for either, and this is the only profile in the rig whose patch is "
        "correct as it stands."),
    "light4me-smb": ("Likely — weakest link",
        "An RGB-background + white-strobe bar against the MA layer <code>--LED.STROBE-BAR</code> "
        "and the RGBW in the profile name. Circumstantial rather than structural: no mode of this "
        "fixture is 13CH, so unlike the beams and lasers the patch cannot corroborate it."),
    "microh-ledbar": ("Likely",
        "Its three RGB segments match the profile's three cells on a 3-channel stride, exactly — "
        "which is also how the mismatch shows, since the profile's 2-channel master stands where "
        "the fixture has four."),
    "chauvet-haze-2d": ("Likely",
        "The only hazer in the rig and the only hazer manual supplied. Weak as identification "
        "goes, but its 533 W draw and its “use on dimmer: no” are what make the DP-415's mode "
        "setting matter."),
}

MISMATCHES = [
    ("fault", "Can collide", "Strobe bars — patched 13CH against a 4 / 16 / 168 fixture",
     "If the bars are in 16CH they are three channels wider than their slot and five of the seven "
     "run into the bar addressed next — 396–398, 409–411, 422–424, 435–437, 448–450. Those are "
     "ch14–16 of the overrun bar (RGBW-effect speed, background colour, background dimmer) driven "
     "by ch1–3 of its neighbour (master dimmer, RGB strobe, red). If instead they are in 4CH, "
     "nothing collides but nine of every thirteen patched channels are dead and the console's "
     "dimmer, strobe and effects do nothing.",
     "BAR 7 is absent from that list: it sits at 357 with the 370–382 gap after it, exactly the "
     "room a 16-channel bar needs. That gap was filed as an unexplained spare in June.",
     "Set every bar to 16CH, re-patch on a 16-channel stride, load a matching profile."),
    ("fault", "Costs a function", "Moving beams — patched 14CH against a 16 / 20 fixture",
     "Nothing collides — the stride is already 16, so each beam occupies 280–295, 296–311, "
     "312–327, 328–343 with no overlap and the next fixture at 357. But the 14-channel profile "
     "stops at <em>pan and tilt speed</em>, leaving <strong>ch15 Reset and ch16 Lamp control</strong> "
     "unreachable. On four discharge fixtures that means the lamps cannot be struck, doused or "
     "reset from the console.",
     "Everything look-critical — colour, gobo, prism, frost, focus, pan, tilt and both fine "
     "channels — sits inside ch1–14 and works. The loss is confined to lamp handling.",
     "Load a 16-channel profile against the same start addresses. No re-addressing needed."),
    ("warn", "Lands on the wrong channel", "DJ-deck bar — patched 11CH against a fixed 13",
     "The MA profile allots a 2-channel master where the Microh has four (function select, then "
     "all-red / all-green / all-blue), so the nine segment channels are <strong>offset by "
     "two</strong>: the console's cell-1 red drives the fixture's all-blue, and so on down the bar.",
     "Nothing collides. The bar would occupy 11–23 and the next fixture is a laser bar at 27, so "
     "the 22–26 gap absorbs the two extra channels.",
     "Load a 13-channel profile at the same start address."),
    ("warn", "Half a fixture", "Hazer — patched 1CH against a fixed 2CH personality",
     "The Hurricane Haze 2D's own DMX is two channels: blower speed, then haze volume. If what is "
     "patched is the hazer's DMX, <strong>haze volume never responds to the console</strong>. If "
     "it is a DP-415 pack channel instead, the patch is correct as written and the hazer runs on "
     "its own front-panel settings.",
     "Which of the two it is decides whether this is a fault or a non-issue, and it is one look at "
     "the back of the hazer.",
     "Establish first whether the hazer's DMX is connected at all. Only then decide."),
    ("benign", "Wastes addresses", "Laser bars — patched 26CH against an 11 / 19 / 24 fixture",
     "Because 24 &lt; 26 nothing collides; each bar simply leaves two dead channels, eighteen "
     "across the nine bars.",
     "What cannot be checked from the export is the profile's internal channel order — grandMA2 "
     "writes fixture-type names into an XML fixture list, not their definitions. If the profile "
     "replicates the LS650's 24CH map with two pad channels everything works; if it is a different "
     "26-channel bar, every attribute lands wrong, which would be obvious on sight.",
     "Confirm the mode reads 24CH, then load a 24-channel profile and reclaim the two channels."),
]

OPEN = [
    ("must", "DP-415 dip switch 10",
     "The Hurricane Haze 2D must not be run on a dimmer, the pack's Dimmer/Switch selection is "
     "pack-wide, and the hazer shares the pack with both CO₂ jets — so it cannot be isolated. It "
     "must read <b>Switch</b>. The only question in this document with a single correct answer."),
    ("open", "Strobe-bar DMX mode",
     "13CH is impossible, so whatever the panel reads is new information. <code>CH16</code> means "
     "five bars are colliding; <code>CH04</code> means nine of thirteen channels per bar are dead."),
    ("open", "Beam model plate",
     "Confirms the YF BEAM 230 against the load schedule. Four discharge beams are 1400–1600 W "
     "where four LED mini heads would have been 400 W — a 1.2 kW swing in the total."),
    ("open", "CO₂ jet make, model and wattage",
     "The last load with no figure. Bounded by the pack at ≤5 A each and ≤10.6 A between them once "
     "the hazer's 4.44 A is accounted for, but unmeasured."),
    ("open", "Hazer DMX — connected or not",
     "Decides whether the 1CH patch is a correct pack channel or a truncated 2CH personality."),
    ("open", "DP-415 start address and socket assignment",
     "Gives the CO₂ jets and the hazer their real addresses. They are pack channels, so the "
     "long-standing “CO₂ unpatched at address 0” item was asking the wrong question."),
    ("open", "Inverted hang — M.Wash 7, M.Wash 10, Laser.BAR(6) 1",
     "Confirms the duplicate-profile reading and is the only fixture-orientation data the repo "
     "holds. Every <code>AbsolutePosition</code> in the showfile is <code>0,0,0</code>."),
    ("open", "Laser class label",
     "Confirms the Class 4 declaration on the fixture body."),
    ("open", "Fixture positions",
     "No to-scale plot can be drawn without a survey. This also blocks any assessment of whether a "
     "laser bar can reach audience-accessible space."),
    ("open", "DMX node make, model and universe/port mapping",
     "The showfile patches addresses but records nothing about what physically drives U1 and U2."),
    ("open", "Lighting mains feed, breakers and power factor",
     "Per-fixture draw is known; the feed that carries it is not. The currents in §8 assume unity "
     "power factor and are a floor, not a design figure."),
    ("open", "Console hardware and booth position",
     "“Nomad” is the dongle-licensed software. Whether the surface on site is onPC with a dongle, "
     "a command wing or a full console is not in the export."),
]


def patch_rows():
    root = ET.parse(SHOWFILE).getroot()
    out, section, order = [], "", 0
    for layer in root.findall("m:Layer", NS):
        fx = layer.findall("m:Fixture", NS)
        if not fx:
            section = layer.get("name")
            continue
        order += 1
        for f in fx:
            prof = f.find("m:FixtureType", NS).get("name")
            addrs = [int(a.text) for a in f.findall("m:SubFixture/m:Patch/m:Address", NS)]
            cells = len(f.findall("m:SubFixture", NS))
            a = min(addrs) if addrs else 0
            foot = audit.FOOTPRINT[prof]
            out.append(dict(
                name=f.get("name").strip(), fid=f.get("fixture_id"), section=section,
                layer=layer.get("name"), profile=prof, grp=GROUP_OF[prof], cells=cells,
                foot=foot, base=a, a=a, e=(a + foot - 1) if a else 0,
                u=((a - 1) // 512 + 1) if a else 0,
                order=order, inv=prof in audit.INVERT_PAIRS,
                desc=len(addrs) > 2 and addrs[1:] == sorted(addrs[1:], reverse=True)))
    return out


def universe_bar(rows, u):
    base = (u - 1) * 512
    seg = ""
    for r in (x for x in rows if x["u"] == u):
        inv = ' data-inv="1"' if r["inv"] else ""
        left = (r["a"] - base - 1) / 512 * 100
        width = max((r["e"] - r["a"] + 1) / 512 * 100, 0.19)
        seg += (f'<i class="seg" style="left:{left:.4f}%;width:{width:.4f}%;'
                f'--c:{FAMILY[r["grp"]][0]}"{inv} '
                f'title="{escape(r["name"])} — abs {r["a"]}–{r["e"]}"></i>')
    ticks = "".join(f'<i class="tick" style="left:{n / 512 * 100:.4f}%">'
                    f'<b>{n + base if n else base + 1}</b></i>' for n in (0, 128, 256, 384))
    return f'<div class="uni"><div class="unibar">{seg}</div><div class="ruler">{ticks}</div></div>'


def schedule(rows):
    """Full fixture schedule, grouped by MA layer in showfile order."""
    out, seen = [], None
    # showfile layer order, then ascending address inside each layer
    for r in sorted(rows, key=lambda r: (r["order"], r["base"] or 10**6)):
        if r["layer"] != seen:
            seen = r["layer"]
            col = FAMILY[r["grp"]][0]
            out.append(f'<tr class="grp"><td colspan="9"><span class="swatch" '
                       f'style="--c:{col}"></span><code>{escape(r["layer"])}</code>'
                       f'<span class="sect">{escape(r["section"])}</span></td></tr>')
        rel_a = r["a"] - (r["u"] - 1) * 512 if r["a"] else 0
        rel_e = r["e"] - (r["u"] - 1) * 512 if r["a"] else 0
        tags = []
        if r["inv"]:
            tags.append('<span class="tag">inverted</span>')
        if r["desc"]:
            tags.append('<span class="tag">cells descend</span>')
        if not r["a"]:
            tags.append('<span class="tag warn">unpatched</span>')
        out.append(
            f'<tr><td class="fx">{escape(r["name"])}</td>'
            f'<td class="n">{r["fid"]}</td>'
            f'<td><code>{escape(r["profile"])}</code></td>'
            f'<td class="n">{r["foot"]}</td>'
            f'<td class="n">{"U" + str(r["u"]) if r["a"] else "—"}</td>'
            f'<td class="n strong">{rel_a or "—"}</td>'
            f'<td class="n">{rel_e or "—"}</td>'
            f'<td class="n dim">{r["a"] or 0}</td>'
            f'<td>{"".join(tags) or "&nbsp;"}</td></tr>')
    return "\n".join(out)


def pretty(s):
    """The fixture table is written ASCII-only for terminal output; soften it for the page."""
    return s.replace(" -- ", " — ").replace(" x ", " × ").replace("CLASS 4", "Class 4")


def chanmap(m):
    fx = audit.FIXTURES[m["key"]]
    rows = []
    for n, fn in m["ch"]:
        lost = n > m["patched"]
        cls = ' class="lost"' if lost else ""
        flag = '<span class="tag warn">unreachable</span>' if lost else ""
        rows.append(f'<tr{cls}><td class="n strong">{n}</td><td>{fn}</td><td>{flag}</td></tr>')
    grade, why = EVIDENCE[m["key"]]
    spare = ""
    if m["patched"] > m["mode"]:
        spare = (f'<p class="note">The patch reserves {m["patched"]} channels against a '
                 f'{m["mode"]}-channel mode — channels {m["mode"] + 1}–{m["patched"]} do not exist '
                 f'on the fixture.</p>')
    return f'''<article class="fxblock" style="--c:{FAMILY[m["grp"]][0]}">
  <header>
    <div>
      <h3>{escape(fx["model"].split(" -- ")[0])}</h3>
      <p class="meta"><code>{escape(m["profile"])}</code> · ×{m["qty"]}</p>
    </div>
    <span class="grade">{grade}</span>
  </header>
  <dl class="specs">
    <div><dt>Modes</dt><dd>{" / ".join(f"{x}CH" for x in fx["modes"])}</dd></div>
    <div><dt>Patched</dt><dd class="{"bad" if m["patched"] not in fx["modes"] else "good"}">{m["patched"]}CH</dd></div>
    <div><dt>Power</dt><dd>{fx["watts"][0] if fx["watts"][0] == fx["watts"][1] else f"{fx['watts'][0]}–{fx['watts'][1]}"} W</dd></div>
    <div><dt>Source</dt><dd>{escape(pretty(fx["source"]))}</dd></div>
  </dl>
  <p class="why"><b>What identified it.</b> {why}</p>
  <div class="cmwrap">
    <p class="cmhead">{m["mode"]}-channel map <span>{escape(m["source"])}</span></p>
    <table class="cm"><tbody>{"".join(rows)}</tbody></table>
  </div>
  {spare}
  <p class="note">{m["alt"]}</p>
  <p class="src"><span>Manual</span><code>{escape(fx["manual"])}</code></p>
</article>'''


def main():
    rows = patch_rows()
    patched = [r for r in rows if r["a"]]
    dst = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "08-lighting/assets/lighting-dossier.html")

    pk = audit.DISTRIBUTION["elation-dp-415"]
    known = sum(a for _l, _n, a in pk["loads"] if a)
    lrows, lo_t, hi_t = [], 0, 0
    for fx in audit.FIXTURES.values():
        q = sum(1 for r in rows if audit.owns(fx, r))
        if not q:
            continue
        lo, hi = fx["watts"]
        lo_t += lo * q
        hi_t += hi * q
        w = f"{lo}" if lo == hi else f"{lo}–{hi}"
        tw = f"{lo * q}" if lo == hi else f"{lo * q}–{hi * q}"
        amps = f"{lo * q / 120:.2f}" if lo == hi else f"{lo * q / 120:.2f}–{hi * q / 120:.2f}"
        lrows.append(f'<tr><td>{escape(fx["model"].split(" -- ")[0])}</td><td class="n">{q}</td>'
                     f'<td class="n">{w}</td><td class="n strong">{tw}</td>'
                     f'<td class="n">{amps}</td></tr>')
    tw = f"{lo_t}" if lo_t == hi_t else f"{lo_t}–{hi_t}"
    ta = f"{lo_t / 120:.1f}" if lo_t == hi_t else f"{lo_t / 120:.1f}–{hi_t / 120:.1f}"
    lrows.append(f'<tr class="tot"><td>Identified subtotal</td><td class="n">—</td>'
                 f'<td class="n">—</td><td class="n strong">{tw} W</td><td class="n">{ta} A</td></tr>')
    lrows.append('<tr class="unk"><td>CO₂ jets — make unknown</td><td class="n">2</td>'
                 '<td class="n">❓</td><td class="n">❓</td><td class="n">❓</td></tr>')

    packrows = ""
    for label, _n, amps in pk["loads"]:
        name = escape(label.split(" -- ")[0]).replace("CO2", "CO₂")
        a_txt = "❓ unread" if amps is None else f"{amps:.2f} A"
        pct = "—" if amps is None else f"{amps / pk['amps_per_channel'] * 100:.0f}%"
        packrows += f'<tr><td>{name}</td><td class="n">{a_txt}</td><td class="n">{pct}</td></tr>'
    packrows += '<tr class="sp"><td>Spare channel</td><td class="n">—</td><td class="n">—</td></tr>'

    mm = "".join(
        f'<article class="mm {tone}"><span class="rank">{rank}</span><h3>{title}</h3>'
        f'<p>{body}</p><p class="tell">{tell}</p>'
        f'<p class="fix"><span>Fix</span>{fix}</p></article>'
        for tone, rank, title, body, tell, fix in MISMATCHES)

    op = "".join(
        f'<li class="{k}"><b>{escape(t)}</b><span>{d}</span></li>' for k, t, d in OPEN)

    legend = "".join(f'<span class="lg"><i style="--c:{c}"></i>{n}</span>'
                     for c, n in [FAMILY[k] for k in
                                  ("beam", "laser", "wash", "strobe", "djled", "fx")])

    html = TEMPLATE.format(
        schedule=schedule(rows), maps="\n".join(chanmap(m) for m in CHANNEL_MAPS),
        mismatches=mm, open=op, legend=legend,
        u1=universe_bar(patched, 1), u2=universe_bar(patched, 2),
        load="".join(lrows), pack=packrows,
        n_total=len(rows), n_patched=len(patched), n_unpatched=len(rows) - len(patched),
        pack_known=f"{known:.2f}", pack_free=f"{pk['amps_total'] - known:.1f}",
    )
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(html, encoding="utf-8")
    print(f"{dst}: {len(rows)} fixtures ({len(patched)} patched), "
          f"{len(CHANNEL_MAPS)} channel maps, {len(OPEN)} open items")


TEMPLATE = r'''<title>NØMAD Lighting Dossier</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root{{
  --paper:#f2f5f5; --card:#ffffff; --ink:#12181b; --ink-2:#46585d; --ink-3:#76898e;
  --line:#d8e0e1; --line-2:#e8eeee;
  --accent:#0d6e86; --accent-soft:#e2eff3;
  --warn:#8a5a00; --warn-soft:#f8eed6;
  --fault:#a82c27; --fault-soft:#f9e3e1;
  --unknown-soft:#eceff0;
  --shadow:0 1px 2px rgba(18,24,27,.05), 0 8px 24px -16px rgba(18,24,27,.28);
}}
@media (prefers-color-scheme:dark){{
  :root:not([data-theme="light"]){{
    --paper:#0d1215; --card:#141c20; --ink:#e6eded; --ink-2:#a3b5b9; --ink-3:#71868b;
    --line:#253338; --line-2:#1c272b;
    --accent:#4bb8d4; --accent-soft:#10333e;
    --warn:#e0a33a; --warn-soft:#33280f;
    --fault:#f08078; --fault-soft:#3a1a18;
    --unknown-soft:#1b2427;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 28px -18px rgba(0,0,0,.9);
  }}
}}
:root[data-theme="dark"]{{
  --paper:#0d1215; --card:#141c20; --ink:#e6eded; --ink-2:#a3b5b9; --ink-3:#71868b;
  --line:#253338; --line-2:#1c272b;
  --accent:#4bb8d4; --accent-soft:#10333e;
  --warn:#e0a33a; --warn-soft:#33280f;
  --fault:#f08078; --fault-soft:#3a1a18;
  --unknown-soft:#1b2427;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 28px -18px rgba(0,0,0,.9);
}}
*{{box-sizing:border-box}}
body{{
  margin:0; background:var(--paper); color:var(--ink);
  font:400 16px/1.62 "IBM Plex Sans","Helvetica Neue",Arial,sans-serif;
  -webkit-font-smoothing:antialiased;
}}
code,.n,.mono{{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace; font-variant-numeric:tabular-nums}}
h1,h2,h3,h4{{font-family:"IBM Plex Sans Condensed","IBM Plex Sans",Arial,sans-serif; text-wrap:balance; margin:0}}
a{{color:var(--accent)}}
:focus-visible{{outline:2px solid var(--accent); outline-offset:2px; border-radius:2px}}

.shell{{max-width:1280px; margin:0 auto; padding:0 24px 110px; display:grid;
  grid-template-columns:210px minmax(0,1fr); gap:52px; align-items:start}}
/* Grid items default to min-width:auto, so a wide table inside main would push the whole
   column past the viewport and drag the nav out with it. */
.shell>*{{min-width:0}}
nav{{position:sticky; top:26px; padding-top:26px}}
nav p{{
  font-family:"IBM Plex Mono",monospace; font-size:10.5px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--ink-3); margin:0 0 12px
}}
nav ol{{list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:1px}}
nav a{{
  display:flex; gap:9px; padding:5px 8px; border-radius:2px; text-decoration:none;
  color:var(--ink-2); font-size:13px; border-left:2px solid transparent
}}
nav a:hover{{background:var(--line-2); color:var(--ink)}}
nav a b{{font-family:"IBM Plex Mono",monospace; color:var(--ink-3); font-weight:400; font-size:11.5px}}

.mast{{padding:64px 0 34px; border-bottom:2px solid var(--ink)}}
.eyebrow{{
  font-family:"IBM Plex Mono",monospace; font-size:11.5px; letter-spacing:.16em;
  text-transform:uppercase; color:var(--accent); margin:0 0 16px
}}
h1{{font-size:clamp(32px,4.6vw,50px); font-weight:700; letter-spacing:-.02em; line-height:1.06}}
.dek{{max-width:66ch; color:var(--ink-2); font-size:17px; margin:18px 0 0}}
.meta-strip{{
  display:flex; flex-wrap:wrap; gap:6px 26px; margin:26px 0 0;
  font-family:"IBM Plex Mono",monospace; font-size:12px; color:var(--ink-3)
}}
.meta-strip b{{color:var(--ink-2); font-weight:500}}

section{{padding:54px 0 0; scroll-margin-top:24px}}
.shead{{display:flex; align-items:baseline; gap:13px; flex-wrap:wrap; margin:0 0 8px}}
.shead .s{{font-family:"IBM Plex Mono",monospace; font-size:13px; color:var(--accent); font-weight:500}}
.shead h2{{font-size:25px; font-weight:600; letter-spacing:-.01em}}
.lede{{color:var(--ink-2); max-width:70ch; margin:0 0 24px; font-size:15.5px}}
h3{{font-size:17.5px; font-weight:600}}
h4{{font-size:14px; font-weight:600; letter-spacing:.02em; margin:26px 0 10px; color:var(--ink-2)}}

.tw{{overflow-x:auto; border:1px solid var(--line); border-radius:3px; background:var(--card)}}
table{{border-collapse:collapse; width:100%; font-size:14px}}
thead th{{
  font-family:"IBM Plex Sans Condensed",sans-serif; font-weight:600; font-size:11.5px;
  letter-spacing:.08em; text-transform:uppercase; color:var(--ink-3); text-align:left;
  padding:11px 13px; border-bottom:1px solid var(--line); white-space:nowrap; position:sticky; top:0;
  background:var(--card)
}}
thead th.n{{text-align:right}}
tbody td{{padding:9px 13px; border-bottom:1px solid var(--line-2); vertical-align:middle}}
tbody tr:last-child td{{border-bottom:0}}
td.n{{text-align:right; font-family:"IBM Plex Mono",monospace; white-space:nowrap; color:var(--ink-2)}}
td.n.strong{{color:var(--ink); font-weight:600}}
td.n.dim{{color:var(--ink-3); font-size:12.5px}}
td.fx{{font-weight:500; white-space:nowrap}}
td code{{font-size:12.5px}}
tr.grp td{{background:var(--line-2); padding:9px 13px; border-bottom:1px solid var(--line)}}
tr.grp code{{font-size:12.5px; font-weight:600; color:var(--ink)}}
tr.grp .sect{{
  font-family:"IBM Plex Mono",monospace; font-size:11px; color:var(--ink-3); margin-left:12px
}}
.swatch{{display:inline-block; width:9px; height:9px; border-radius:1px; background:var(--c); margin-right:9px}}
.tag{{
  display:inline-block; font-family:"IBM Plex Mono",monospace; font-size:10px; letter-spacing:.05em;
  padding:2px 6px; border:1px solid var(--line); border-radius:2px; color:var(--ink-3); margin-right:4px
}}
.tag.warn{{color:var(--warn); border-color:var(--warn); background:var(--warn-soft)}}
.tnote{{font-size:13.5px; color:var(--ink-3); margin:13px 0 0; max-width:74ch}}

/* universes */
.legend{{display:flex; flex-wrap:wrap; gap:8px 20px; margin:0 0 20px}}
.lg{{display:flex; align-items:center; gap:7px; font-size:12.5px; color:var(--ink-2)}}
.lg i{{width:16px; height:8px; border-radius:1px; background:var(--c); display:block}}
.umap{{display:flex; flex-direction:column; gap:24px}}
.ulab{{display:flex; justify-content:space-between; align-items:baseline; flex-wrap:wrap; gap:8px;
  font-family:"IBM Plex Mono",monospace; font-size:12px; color:var(--ink-3); margin:0 0 7px}}
.ulab b{{color:var(--ink); font-weight:600; letter-spacing:.1em; text-transform:uppercase}}
.unibar{{position:relative; height:32px; background:var(--line-2); border:1px solid var(--line);
  border-radius:2px; overflow:hidden}}
.seg{{position:absolute; top:0; bottom:0; background:var(--c)}}
.seg[data-inv]{{background:repeating-linear-gradient(135deg,var(--c) 0 4px,
  color-mix(in srgb,var(--c) 55%,#000) 4px 8px)}}
.ruler{{position:relative; height:16px; margin-top:5px}}
.tick{{position:absolute; top:0; width:1px; height:5px; background:var(--line)}}
.tick b{{position:absolute; left:0; top:7px; font-family:"IBM Plex Mono",monospace; font-size:10px;
  font-weight:400; color:var(--ink-3)}}

/* fixture blocks */
.fxblock{{
  background:var(--card); border:1px solid var(--line); border-top:2px solid var(--c);
  border-radius:3px; padding:22px 24px 18px; box-shadow:var(--shadow); margin:0 0 18px;
  display:flex; flex-direction:column; gap:14px
}}
.fxblock header{{display:flex; justify-content:space-between; align-items:start; gap:14px; flex-wrap:wrap}}
.fxblock .meta{{margin:5px 0 0; font-size:12.5px; color:var(--ink-3)}}
.grade{{font-family:"IBM Plex Mono",monospace; font-size:10.5px; letter-spacing:.05em;
  padding:3px 8px; border-radius:2px; background:var(--accent-soft); color:var(--accent); white-space:nowrap}}
.specs{{display:flex; flex-wrap:wrap; gap:0; margin:0; border:1px solid var(--line); border-radius:2px; overflow:hidden}}
.specs div{{flex:1 1 130px; padding:9px 12px; border-right:1px solid var(--line)}}
.specs div:last-child{{border-right:0; flex:2 1 220px}}
.specs dt{{font-size:10.5px; letter-spacing:.09em; text-transform:uppercase; color:var(--ink-3); margin:0 0 3px}}
.specs dd{{margin:0; font-family:"IBM Plex Mono",monospace; font-size:13px; color:var(--ink)}}
.specs dd.bad{{color:var(--fault); font-weight:600}}
.specs dd.good{{color:var(--accent); font-weight:600}}
.why{{margin:0; font-size:14.5px; color:var(--ink-2); max-width:80ch}}
.why b{{color:var(--ink)}}
.cmwrap{{border:1px solid var(--line); border-radius:2px; overflow:hidden}}
.cmhead{{
  display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap; margin:0;
  padding:9px 13px; background:var(--line-2); font-family:"IBM Plex Sans Condensed",sans-serif;
  font-size:12px; font-weight:600; letter-spacing:.07em; text-transform:uppercase; color:var(--ink-2)
}}
.cmhead span{{font-family:"IBM Plex Mono",monospace; font-weight:400; text-transform:none;
  letter-spacing:0; color:var(--ink-3); font-size:11px}}
table.cm{{font-size:13.5px}}
table.cm td{{padding:6px 13px}}
table.cm td:first-child{{width:44px}}
table.cm tr.lost td{{background:var(--fault-soft)}}
table.cm tr.lost td:nth-child(2){{color:var(--fault)}}
.note{{margin:0; font-size:13.5px; color:var(--ink-3); max-width:82ch}}
.src{{display:flex; gap:8px; align-items:center; font-size:11px; color:var(--ink-3); margin:0}}
.src span{{letter-spacing:.09em; text-transform:uppercase}}
.src code{{font-size:11px; color:var(--ink-2)}}

/* mismatches */
.mmlist{{display:flex; flex-direction:column; gap:14px}}
.mm{{background:var(--card); border:1px solid var(--line); border-left:3px solid var(--ink-3);
  border-radius:3px; padding:19px 22px}}
.mm.fault{{border-left-color:var(--fault)}}
.mm.warn{{border-left-color:var(--warn)}}
.rank{{font-family:"IBM Plex Mono",monospace; font-size:11px; letter-spacing:.09em;
  text-transform:uppercase; color:var(--ink-3)}}
.mm.fault .rank{{color:var(--fault)}}
.mm.warn .rank{{color:var(--warn)}}
.mm h3{{margin:6px 0 10px}}
.mm p{{margin:0; font-size:14.5px; color:var(--ink-2); max-width:82ch}}
.mm .tell{{margin-top:11px; padding-top:11px; border-top:1px solid var(--line-2);
  font-size:13.5px; color:var(--ink-3)}}
.mm .fix{{margin-top:11px; display:flex; gap:9px; align-items:baseline; font-size:14px; color:var(--ink)}}
.mm .fix span{{font-family:"IBM Plex Mono",monospace; font-size:10.5px; letter-spacing:.09em;
  text-transform:uppercase; color:var(--ink-3); flex:0 0 auto}}
.mm strong,.why strong{{color:var(--ink); font-weight:600}}
.mm em{{font-style:italic}}

/* open items */
.open{{background:var(--card); border:1px solid var(--line); border-radius:3px; overflow:hidden}}
.open ul{{list-style:none; margin:0; padding:0}}
.open li{{display:grid; grid-template-columns:220px minmax(0,1fr); gap:18px; padding:14px 20px;
  border-bottom:1px solid var(--line-2); font-size:14px; color:var(--ink-2)}}
.open li:last-child{{border-bottom:0}}
.open li b{{color:var(--ink); font-weight:600; font-size:14px}}
.open li.must{{background:var(--fault-soft)}}
.open li.must b{{color:var(--fault)}}
@media (max-width:760px){{.open li{{grid-template-columns:1fr; gap:5px}}}}

.callout{{
  border:1px solid var(--line); border-left:3px solid var(--fault); background:var(--card);
  border-radius:3px; padding:18px 22px; margin:20px 0 0
}}
.callout h4{{margin:0 0 8px; color:var(--fault); font-size:14px; letter-spacing:.03em}}
.callout p{{margin:0 0 9px; font-size:14.5px; color:var(--ink-2); max-width:80ch}}
.callout p:last-child{{margin-bottom:0}}

.pack{{display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; margin-top:18px}}
tr.tot td{{border-top:1px solid var(--line); font-weight:600; color:var(--ink)}}
tr.unk td{{color:var(--ink-3)}}
tr.sp td{{color:var(--ink-3)}}

footer{{margin-top:66px; padding-top:22px; border-top:1px solid var(--line); font-size:13px;
  color:var(--ink-3); display:flex; justify-content:space-between; gap:16px; flex-wrap:wrap}}
footer code{{font-size:12px}}
@media (max-width:900px){{
  .shell{{grid-template-columns:1fr; gap:0}}
  nav{{position:static; padding:22px 0 0; border-bottom:1px solid var(--line)}}
  nav ol{{flex-direction:row; flex-wrap:wrap; gap:4px; padding-bottom:18px}}
  nav a{{border:1px solid var(--line); border-radius:2px; padding:4px 9px}}
}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important; transition:none!important}}}}
</style>

<div class="shell">

<nav aria-label="Contents">
  <p>Contents</p>
  <ol>
    <li><a href="#s1"><b>1</b>Status</a></li>
    <li><a href="#s2"><b>2</b>System</a></li>
    <li><a href="#s3"><b>3</b>Fixture schedule</a></li>
    <li><a href="#s4"><b>4</b>Universes</a></li>
    <li><a href="#s5"><b>5</b>Fixtures &amp; channel maps</a></li>
    <li><a href="#s6"><b>6</b>Mismatches</a></li>
    <li><a href="#s7"><b>7</b>Inverted fixtures</a></li>
    <li><a href="#s8"><b>8</b>Power</a></li>
    <li><a href="#s9"><b>9</b>Laser safety</a></li>
    <li><a href="#s10"><b>10</b>Open items</a></li>
    <li><a href="#s11"><b>11</b>Provenance</a></li>
  </ol>
</nav>

<main>

<header class="mast">
  <p class="eyebrow">Lighting dossier · rev 3.1</p>
  <h1>NØMAD Toronto<br>lighting rig</h1>
  <p class="dek">The complete record of the grandMA2 rig: every fixture, every address, and the DMX
  channel map of every fixture as its own manual states it. Assembled from a showfile that names
  none of its fixtures and seven vendor manuals that name no addresses.</p>
  <div class="meta-strip">
    <span><b>Console</b> grandMA2 “Nomad” v3.9.60</span>
    <span><b>Showfile</b> nomad_2026-06-13_kayo-toronto-ft-pools</span>
    <span><b>Exported</b> 2026-06-24</span>
    <span><b>Compiled</b> 2026-08-25</span>
  </div>
</header>

<section id="s1">
  <div class="shead"><span class="s">§1</span><h2>Status</h2></div>
  <p class="lede">Desktop work only. Nothing in this document has been verified at the rig, and
  nothing here should be re-patched from a desk — the patch is internally consistent as it stands,
  and a change made on inference would leave it worse.</p>
  <div class="tw"><table>
    <thead><tr><th>Item</th><th>State</th><th>Note</th></tr></thead>
    <tbody>
      <tr><td>Fixtures identified</td><td><b>All but the CO₂ jets</b></td><td>Seven manuals against eight MA profiles</td></tr>
      <tr><td>Patch address integrity</td><td><b>Clean</b></td><td>{n_patched} patched, no overlaps, no universe-boundary crossings</td></tr>
      <tr><td>Patch vs. fixture modes</td><td><b>5 mismatches</b></td><td>Only the moving washes agree — §6</td></tr>
      <tr><td>Connected load</td><td><b>Subtotal</b></td><td>CO₂ jets carry no figure — §8</td></tr>
      <tr><td>Laser class</td><td><b>Class 4</b></td><td>Compliance items unrecorded — §9</td></tr>
      <tr><td>Fixture positions</td><td><b>Unknown</b></td><td>Every position in the showfile is <code>0,0,0</code></td></tr>
      <tr><td>DMX node topology</td><td><b>Unknown</b></td><td>The export patches addresses, not ports</td></tr>
      <tr><td>Lighting mains feed</td><td><b>Unknown</b></td><td>Per-fixture draw known; the feed is not</td></tr>
    </tbody>
  </table></div>
</section>

<section id="s2">
  <div class="shead"><span class="s">§2</span><h2>System</h2></div>
  <p class="lede">Two DMX universes off a grandMA2 “Nomad”. The console is the software platform —
  what physical surface sits in the booth is not described by the export.</p>
  <div class="tw"><table>
    <thead><tr><th>Universe</th><th class="n">Absolute</th><th class="n">Fixtures</th><th class="n">Channels used</th><th>Contents</th></tr></thead>
    <tbody>
      <tr><td><b>Universe 1</b></td><td class="n">1–512</td><td class="n">28</td><td class="n">438</td>
        <td>DJ-deck bar · 7 strobe bars · M.Wash 1–8 · all 4 beams · Laser.BAR 1–8</td></tr>
      <tr><td><b>Universe 2</b></td><td class="n">513–1024</td><td class="n">4</td><td class="n">45</td>
        <td>Laser.BAR 9 · M.Wash 9 &amp; 10 · hazer</td></tr>
      <tr><td><b>Unpatched</b></td><td class="n">—</td><td class="n">2</td><td class="n">—</td>
        <td>CO₂ jets ×2, at address 0 — they are DP-415 pack channels, not DMX fixtures (§8)</td></tr>
    </tbody>
  </table></div>
  <p class="tnote">Addresses in the showfile are absolute across the whole patch. Universe-relative
  is <code>absolute − (universe − 1) × 512</code>.</p>
</section>

<section id="s3">
  <div class="shead"><span class="s">§3</span><h2>Fixture schedule</h2></div>
  <p class="lede">All {n_total} fixtures in MA layer order, {n_patched} patched and {n_unpatched}
  not. <b>Ch</b> is the footprint the patch occupies — the <code>…CH</code> in the profile name,
  which is not always a mode the fixture has. Start and end are universe-relative; the absolute
  address follows.</p>
  <div class="tw"><table>
    <thead><tr>
      <th>Fixture</th><th class="n">FID</th><th>MA profile</th><th class="n">Ch</th>
      <th class="n">Uni</th><th class="n">Start</th><th class="n">End</th><th class="n">Abs</th><th>Notes</th>
    </tr></thead>
    <tbody>
{schedule}
    </tbody>
  </table></div>
</section>

<section id="s4">
  <div class="shead"><span class="s">§4</span><h2>Universes</h2></div>
  <p class="lede">Both universes to scale, 512 addresses each. Hatched blocks are the three
  fixtures hung inverted (§7). The empty stretches are real.</p>
  <div class="legend">{legend}</div>
  <div class="umap">
    <div>
      <p class="ulab"><b>Universe 1</b><span>abs 1–512 · 28 fixtures · 438 ch used</span></p>
      {u1}
    </div>
    <div>
      <p class="ulab"><b>Universe 2</b><span>abs 513–1024 · 4 fixtures · 45 ch used</span></p>
      {u2}
    </div>
  </div>
  <p class="tnote">Notable gaps: <b>22–26</b> after the DJ bar (which a 13-channel Microh would
  partly fill), <b>342–356</b> before the strobes, <b>370–382</b> after BAR 7 — exactly the room a
  16-channel bar needs — and <b>539–711</b>, 173 clear addresses on U2.</p>
</section>

<section id="s5">
  <div class="shead"><span class="s">§5</span><h2>Fixtures &amp; channel maps</h2></div>
  <p class="lede">One block per fixture: what identified it, and its DMX channel map as the manual
  states it. Rows shaded red are channels the patched footprint cannot reach. These maps are the
  part of this document transcribed by hand — each cites its manual page.</p>
{maps}
</section>

<section id="s6">
  <div class="shead"><span class="s">§6</span><h2>Mismatches</h2></div>
  <p class="lede">Five of the eight profiles are patched to a footprint their fixture has no mode
  for. Ordered by what each actually does to the rig, not by profile number: only the first can
  corrupt another fixture's channels, and the last is merely untidy.</p>
  <div class="mmlist">
{mismatches}
  </div>
</section>

<section id="s7">
  <div class="shead"><span class="s">§7</span><h2>Inverted fixtures</h2></div>
  <p class="lede">Two of the eight profiles are pan/tilt-inverted duplicates of another profile,
  for fixtures hung upside down. Reported by the venue and corroborated against the export.</p>
  <div class="tw"><table>
    <thead><tr><th>Inverted profile</th><th>Duplicate of</th><th>Fixtures</th><th>Corroboration</th></tr></thead>
    <tbody>
      <tr><td><code>6 movingwash zone</code></td><td><code>5 NEW WASH</code></td>
        <td>M.Wash 7, M.Wash 10</td>
        <td>Identical sub-fixture structure — one cell of 9 channels. A zoned mode would have cells.</td></tr>
      <tr><td><code>7 LASER BARS - Invert 26CH</code></td><td><code>8 LASER BARS 26CH</code></td>
        <td>Laser.BAR(6) 1</td>
        <td>Named “Invert”, and its six cell addresses run descending (215→210) where every other bar ascends.</td></tr>
    </tbody>
  </table></div>
  <p class="tnote">Pan/tilt inversion lives in the fixture-type definition, which grandMA2 does not
  write into an XML fixture list — so it cannot be read out of the export directly. What the export
  <em>can</em> show is that each duplicate has the same sub-fixture shape as its base, meaning the
  two differ only in something the file cannot represent. That is corroboration, not proof.</p>
  <p class="tnote"><b>Three fixtures are therefore hung inverted</b> — M.Wash 7, M.Wash 10 and
  Laser.BAR(6) 1. This is the only fixture-orientation information the repo holds. Worth raising
  with whoever maintains the showfile: grandMA2 inverts pan and tilt <em>per fixture</em> in the
  patch, so carrying a duplicate fixture <em>type</em> works but splits each group across two types
  and grows the profile count with every orientation.</p>
</section>

<section id="s8">
  <div class="shead"><span class="s">§8</span><h2>Power</h2></div>
  <p class="lede">Manufacturer figures, none measured. Currents are real power ÷ voltage at unity
  power factor — a <em>floor</em>, not a design figure. Add the fixtures' actual power factor and
  the discharge ballasts' inrush before sizing anything.</p>
  <div class="tw"><table>
    <thead><tr><th>Fixture</th><th class="n">Qty</th><th class="n">W each</th><th class="n">W total</th><th class="n">A @ 120 V</th></tr></thead>
    <tbody>
{load}
    </tbody>
  </table></div>
  <p class="tnote">A subtotal, not a total — the two CO₂ jets are the only loads in the rig with no
  figure.</p>

  <h4>Effects distribution — Elation DP-415</h4>
  <p class="lede">One 4-channel dimmer/switch pack carries all three effects devices: 120 V 60 Hz,
  15 A total, 5 A per channel, dual Edison sockets per channel, 9-way dip-switch address.
  Confirmed by the venue. Three channels used, one spare.</p>
  <div class="tw"><table>
    <thead><tr><th>Load</th><th class="n">A @ 120 V</th><th class="n">Of channel</th></tr></thead>
    <tbody>{pack}</tbody>
  </table></div>
  <p class="tnote">{pack_known} A known. Whatever the CO₂ jets draw is bounded by the pack whether
  or not anyone measures it: at most 5 A each by channel rating, at most {pack_free} A between them
  once the hazer is accounted for. A jet is a solenoid valve, so the real figure should sit far
  below that.</p>

  <div class="callout">
    <h4>Dip switch 10 must read Switch</h4>
    <p>The Hurricane Haze 2D's manual states outright that it must not be run on a dimmer. The
    DP-415 selects Dimmer or Switch <b>pack-wide</b> on dip switch 10, not per channel. The hazer
    shares that pack with both CO₂ jets, so it cannot be moved to a switch-mode pack of its own.</p>
    <p>There is therefore exactly one correct setting, and it has not been read.</p>
  </div>
</section>

<section id="s9">
  <div class="shead"><span class="s">§9</span><h2>Laser safety</h2></div>
  <p class="lede">Each LS650 carries six 500 mW emitters at 638 nm — 3 W of optical output per bar,
  nine bars. At 500 mW per aperture these are <b>Class 4</b> by any measure: the class where the
  beam is an eye and skin hazard including from diffuse reflections, and where audience scanning
  stops being a design choice and becomes a regulated one.</p>
  <div class="tw"><table>
    <thead><tr><th>Item</th><th>State</th></tr></thead>
    <tbody>
      <tr><td>Class declared by the manufacturer</td><td>Confirm from the product page or the label on the fixture</td></tr>
      <tr><td>Whether any bar can reach audience-accessible space</td><td>Unknown — fixture positions are all <code>0,0,0</code></td></tr>
      <tr><td>Beam-stop and mounting-angle measures</td><td>Not documented</td></tr>
      <tr><td>Operator responsible during a show</td><td>Not documented</td></tr>
      <tr><td>Applicable requirements and any variance held</td><td>Not documented</td></tr>
    </tbody>
  </table></div>
  <p class="tnote">This is an open compliance item for whoever runs the venue, to be resolved with
  their own safety advisor. It is recorded here because nothing in the repo recorded it, not
  because this document can answer it.</p>
</section>

<section id="s10">
  <div class="shead"><span class="s">§10</span><h2>Open items</h2></div>
  <p class="lede">What is not known, and what would settle it. Everything above the fold here is
  readable off a fixture panel in a single walk round the rig.</p>
  <div class="open"><ul>
{open}
  </ul></div>
</section>

<section id="s11">
  <div class="shead"><span class="s">§11</span><h2>Provenance</h2></div>
  <p class="lede">What each claim in this document rests on, and what it does not.</p>
  <div class="tw"><table>
    <thead><tr><th>Source</th><th>Supplies</th><th>Confidence</th></tr></thead>
    <tbody>
      <tr><td><code>NOMADFIXPATCHJUNE2026.xml</code></td>
        <td>Every address, footprint, fixture ID, layer and sub-fixture structure</td>
        <td>Authoritative — grandMA2's own export</td></tr>
      <tr><td>Seven vendor manuals, <code>08-lighting/manuals/</code></td>
        <td>DMX modes, channel maps, electrical ratings</td>
        <td>Authoritative for the fixture; the <em>link</em> to a profile is inference — §5</td></tr>
      <tr><td>Manufacturer product pages, relayed 2026-08-25</td>
        <td>Power figures where the manual omits them</td>
        <td>Not measured</td></tr>
      <tr><td>Venue, 2026-08-25</td>
        <td>That some fixtures are pan/tilt-inverted duplicates; that one DP-415 carries both CO₂ jets and the hazer</td>
        <td>Stated by the venue</td></tr>
      <tr><td>Not in any source</td>
        <td>Fixture positions, DMX node topology, mains feed, console hardware, CO₂ jet make</td>
        <td>Recorded as unknown rather than estimated</td></tr>
    </tbody>
  </table></div>
  <p class="tnote">The showfile records a fixture-profile <em>name</em> and a start address, and no
  fixture-type definitions — so a profile's internal channel order cannot be read back from it. Two
  things can be checked mechanically, and they are what this document rests on: whether the patched
  footprint is a mode the fixture can be set to, and what address stride the patch actually leaves
  between fixtures.</p>
</section>

<footer>
  <span>EMBLEM PROJECTS INC. · NØMAD Toronto · lighting dossier rev 3.1 · 2026-08-25</span>
  <span>Generated by <code>scripts/build-lighting-dossier.py</code></span>
</footer>

</main>
</div>
'''

if __name__ == "__main__":
    main()
