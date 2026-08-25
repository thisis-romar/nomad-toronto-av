#!/usr/bin/env python3
"""
Render the manual-to-patch correlation as a standalone HTML page.

The audit document (08-lighting/fixture-identification-audit.md) carries the reasoning across
thirteen sections. This is the same finding laid out to be *scanned*: what proved each fixture,
where the patch disagrees with it, and where every fixture sits in the two universes.

Address geometry is read from the showfile so the universe map cannot drift from the patch.
Everything else comes from FIXTURES/DISTRIBUTION in audit-dmx-patch.py, so there is one source
of truth for the fixture data.

Run from repo root:
    python3 scripts/build-correlation-page.py [out.html]
Default output: 08-lighting/assets/correlation.html
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

# Fixture families, on the Okabe-Ito palette this repo already uses for the rack labels
# (scripts/rack_palette.py). Colour-blind safe, and deliberately clear of the semantic
# teal/amber/red used for verdicts.
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

# What actually linked each manual to its profile. This is the page's subject: not "these are the
# fixtures" but "this is the fact that identified them".
SHORT = {
    "yf-beam-230": "YF BEAM 230",
    "panda-ls650": "Panda LS650 / LS652",
    "betopper-lm70s": "BETOPPER LM70S",
    "light4me-smb": "Light4Me Strobe Multi Bar",
    "microh-ledbar": "Microh LEDBAR RGB",
    "chauvet-haze-2d": "Chauvet Hurricane Haze 2D",
}

EVIDENCE = [
    dict(key="yf-beam-230", grade="confirmed", grade_label="Confirmed by manual",
         profiles=[("9 Sharpy Standard Lamp on", 4)],
         proof="The four beams are patched on a uniform <strong>16-channel stride</strong> — "
               "exactly this fixture's 16CH mode, and two wider than the 14CH profile loaded "
               "against them. The manual confirms 16/20CH and the 189 W 5R Philips / 230 W 7R "
               "Osram lamp.",
         extra="“Standard Lamp on” is a Clay&nbsp;Paky Sharpy mode name, and a Sharpy's own lamp is "
               "a 189 W MSD Platinum 5R — so the profile was a sensible pick for a Sharpy-clone. "
               "The brand was never right; the class was."),
    dict(key="panda-ls650", grade="strong", grade_label="Near-certain",
         profiles=[("8 LASER BARS 26CH", 8), ("7 LASER BARS - Invert 26CH", 1)],
         proof="Six laser eyes against the MA fixture name <code>Laser.BAR(6)</code> and its "
               "<strong>six sub-fixture cells</strong>.",
         extra="The structure matches attribute for attribute: MA records one master of 7 "
               "attributes plus 6 cells of 2. The LS650's 24CH mode gives each eye exactly two — a "
               "tilt position and a laser on/off — with seven whole-fixture attributes. "
               "7&nbsp;+&nbsp;6×2&nbsp;=&nbsp;19, which is what the export holds."),
    dict(key="betopper-lm70s", grade="probable", grade_label="Probable",
         profiles=[("5 NEW WASH", 8), ("6 movingwash zone", 2)],
         proof="Its 9CH mode is the wash footprint <em>and</em> the address stride. Both agree, "
               "which no other profile in the rig manages.",
         extra="The only fixture here whose patch is correct as it stands."),
    dict(key="light4me-smb", grade="weak", grade_label="Likely — weakest link",
         profiles=[("4 rgbw-13ch 13CH", 7)],
         proof="An RGB-background + white-strobe bar against the MA layer "
               "<code>--LED.STROBE-BAR</code> and the RGBW in the profile name.",
         extra="Circumstantial rather than structural. No mode of this fixture is 13CH, so the "
               "patch cannot corroborate it the way the beams and lasers corroborate theirs."),
    dict(key="microh-ledbar", grade="probable", grade_label="Likely",
         profiles=[("3 LED Bar 2 11CH", 1)],
         proof="Its <strong>three RGB segments</strong> match the profile's three cells on a "
               "3-channel stride, exactly.",
         extra="Which is also how the mismatch shows: the profile's master is 2 channels where the "
               "fixture has 4 (function + all-R/G/B), so 2&nbsp;+&nbsp;9&nbsp;=&nbsp;11 against the "
               "fixture's 13."),
    dict(key="chauvet-haze-2d", grade="probable", grade_label="Likely",
         profiles=[("2 Dimmer 00", 1)],
         proof="The only hazer in the rig, and the only hazer manual supplied.",
         extra="Weak as identification goes — but its 533 W and its “use on dimmer: no” are what "
               "make the DP-415's mode setting matter."),
]

MISMATCHES = [
    dict(rank="Can collide", tone="fault",
         title="Strobe bars — patched 13CH, fixture offers 4 / 16 / 168",
         body="If the bars are in 16CH they are three channels wider than their slot, and "
              "<strong>five of the seven run into the bar addressed next</strong>: 396–398, "
              "409–411, 422–424, 435–437, 448–450. Those are ch14–16 of the overrun bar — "
              "RGBW-effect speed, background colour, background dimmer — driven by ch1–3 of its "
              "neighbour. If instead they are in 4CH, nothing collides but nine of every thirteen "
              "patched channels are dead.",
         tell="BAR 7 is not in that list. It sits at 357 with the 370–382 gap after it — exactly "
              "the room a 16-channel bar needs. That gap was filed as an unexplained spare in June."),
    dict(rank="Costs a function", tone="fault",
         title="Moving beams — patched 14CH, fixture offers 16 / 20",
         body="Nothing collides: the stride is already 16. But the 14-channel profile stops at "
              "<em>Pan and Tilt speed</em>, so <strong>ch15 Reset and ch16 Lamp control</strong> "
              "are unreachable. On four discharge fixtures that means the lamps cannot be struck, "
              "doused or reset from the console.",
         tell="Everything look-critical — colour, gobo, prism, frost, focus, pan, tilt, both fine "
              "channels — sits inside 1–14 and works. The loss is entirely in lamp handling."),
    dict(rank="Lands on the wrong channel", tone="warn",
         title="DJ-deck bar — patched 11CH, fixture is a fixed 13",
         body="The profile's master is 2 channels where the Microh has 4, so the whole segment "
              "block is <strong>offset by two</strong>: the console's cell-1 red drives the "
              "fixture's all-blue, and so on down the bar.",
         tell="Nothing collides — the bar occupies 11–23 and the next fixture is a laser at 27."),
    dict(rank="Half a fixture", tone="warn",
         title="Hazer — patched 1CH, personality is a fixed 2",
         body="The Hurricane Haze 2D's own DMX is two channels: blower speed, then haze volume. "
              "If what is patched is the hazer's DMX, <strong>haze volume never responds</strong>. "
              "If it is a DP-415 pack channel instead, the patch is correct as written.",
         tell="Which of the two it is decides whether this is a fault or a non-issue. It is one "
              "look at the back of the hazer."),
    dict(rank="Wastes addresses", tone="benign",
         title="Laser bars — patched 26CH, fixture offers 11 / 19 / 24",
         body="Because 24 &lt; 26 nothing collides; each bar simply leaves two dead channels, "
              "eighteen across the nine bars.",
         tell="What cannot be checked from here is the profile's internal channel order — the "
              "export carries fixture-type names, not their definitions."),
]


def patch():
    root = ET.parse(SHOWFILE).getroot()
    out = []
    for layer in root.findall("m:Layer", NS):
        for fx in layer.findall("m:Fixture", NS):
            prof = fx.find("m:FixtureType", NS).get("name")
            addrs = [int(a.text) for a in fx.findall("m:SubFixture/m:Patch/m:Address", NS)]
            if not addrs or not min(addrs):
                continue
            a = min(addrs)
            # key names match audit-dmx-patch.py's own fixture dicts so owner_of/spacing
            # can be reused directly rather than reimplemented here
            out.append(dict(name=fx.get("name").strip(), profile=prof, prof=prof,
                            grp=GROUP_OF[prof], base=a,
                            a=a, e=a + audit.FOOTPRINT[prof] - 1,
                            u=(a - 1) // 512 + 1,
                            inv=prof in audit.INVERT_PAIRS))
    return sorted(out, key=lambda d: d["a"])


def universe_bar(rows, u):
    """Proportional 512-address strip for one universe."""
    base = (u - 1) * 512
    seg = []
    for r in (x for x in rows if x["u"] == u):
        left = (r["a"] - base - 1) / 512 * 100
        width = (r["e"] - r["a"] + 1) / 512 * 100
        col = FAMILY[r["grp"]][0]
        inv = ' data-inv="1"' if r["inv"] else ""
        seg.append(
            f'<i class="seg" style="left:{left:.4f}%;width:{max(width, 0.19):.4f}%;'
            f'--c:{col}"{inv} title="{escape(r["name"])} — {r["a"]}–{r["e"]} '
            f'({r["a"] - base}–{r["e"] - base} in U{u})"></i>')
    ticks = "".join(
        f'<i class="tick" style="left:{(n / 512 * 100):.4f}%"><b>{n + base if n else base + 1}</b></i>'
        for n in (0, 128, 256, 384))
    return f'<div class="uni"><div class="unibar">{"".join(seg)}</div><div class="ruler">{ticks}</div></div>'


SEVERITY = {"fault": 0, "warn": 1, "unknown": 2, "ok": 3}


def profile_row(rows, prof):
    """(sort key, html) for one MA profile."""
    members = [r for r in rows if r["profile"] == prof]
    foot = audit.FOOTPRINT[prof]
    stride, nat, ngap = audit.spacing(rows, prof)
    st = "—" if not stride else (f"{stride}" if nat == ngap else f"{stride}<sub>{nat}/{ngap}</sub>")
    col, _fam = FAMILY[GROUP_OF[prof]]
    _key, fx = audit.owner_of(audit.FIXTURES, members[0]) if members else (None, None)
    if not fx:
        model, modes, verdict, tone = "CO₂ jets — make unknown", "—", "Not identified", "unknown"
    else:
        model = SHORT.get(_key, fx["model"].split(" -- ")[0])
        modes = " / ".join(str(m) for m in fx["modes"])
        if foot in fx["modes"]:
            verdict, tone = "Agrees", "ok"
        elif stride and stride in fx["modes"]:
            verdict, tone = f"Stride says {stride}", "warn"
        else:
            verdict, tone = f"No {foot}CH mode", "fault"
    inv = ' <span class="inv-tag" title="pan/tilt-inverted duplicate profile">inv</span>' \
        if prof in audit.INVERT_PAIRS else ""
    html = (f'<tr><td><span class="swatch" style="--c:{col}"></span>'
            f'<code>{escape(prof)}</code>{inv}</td>'
            f'<td class="n">{len(members)}</td>'
            f'<td class="model">{escape(model)}</td>'
            f'<td class="n">{modes}</td>'
            f'<td class="n strong">{foot}</td>'
            f'<td class="n">{st}</td>'
            f'<td><span class="pill {tone}">{verdict}</span></td></tr>')
    return (SEVERITY[tone], prof), html


def rows_html(rows):
    """Profiles ordered by how badly the patch disagrees, worst first."""
    built = [profile_row(rows, prof) for prof in audit.FOOTPRINT
             if any(r["profile"] == prof for r in rows)]
    # The CO2 jets sit at address 0, so they never appear in the patched rows -- but leaving them
    # out of the table would imply the rig is smaller than it is.
    built.append(((SEVERITY["unknown"], "zz"),
                  '<tr class="unpatched"><td><span class="swatch" style="--c:'
                  + FAMILY["fx"][0] + '"></span><code>2 Dimmer 00</code> '
                  '<span class="inv-tag">unpatched</span></td>'
                  '<td class="n">2</td><td class="model">CO₂ jets — make unknown</td>'
                  '<td class="n">—</td><td class="n strong">1</td><td class="n">—</td>'
                  '<td><span class="pill unknown">Address 0</span></td></tr>'))
    return "\n".join(h for _k, h in sorted(built, key=lambda x: x[0]))


def main():
    rows = patch()
    dst = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "08-lighting/assets/correlation.html")

    ev = []
    for e in EVIDENCE:
        fx = audit.FIXTURES[e["key"]]
        model = SHORT[e["key"]]
        profs = "".join(
            f'<li><code>{escape(p)}</code> <span class="qty">×{q}</span></li>'
            for p, q in e["profiles"])
        grp = GROUP_OF[e["profiles"][0][0]]
        ev.append(f'''<article class="ev" style="--c:{FAMILY[grp][0]}">
  <header>
    <h3>{escape(model)}</h3>
    <span class="grade {e["grade"]}">{e["grade_label"]}</span>
  </header>
  <ul class="profs">{profs}</ul>
  <p class="proof">{e["proof"]}</p>
  <p class="extra">{e["extra"]}</p>
  <p class="src"><span>Manual</span><code>{escape(fx["manual"] or "—")}</code></p>
</article>''')

    pk = audit.DISTRIBUTION["elation-dp-415"]
    chans = ""
    for label, _n, amps in pk["loads"]:
        cls = ' class="known"' if amps else ""
        val = f"{amps:.2f} A" if amps else "❓ unread"
        name = escape(label.split(" -- ")[0]).replace("CO2", "CO₂")
        chans += f'<li{cls}><b>{name}</b><span>{val}</span></li>'
    chans += '<li class="spare"><b>Spare</b><span>—</span></li>'
    dist = f'''<article class="dist">
  <header>
    <h3>Elation DP-415 — 4-channel dimmer/switch pack</h3>
    <span class="grade confirmed">Confirmed by the venue</span>
  </header>
  <p class="proof">The three <code>2 Dimmer 00</code> entries are not fixtures. They are
  <strong>channels on this pack</strong> — mains switching for the hazer and both CO₂ jets, three
  of its four channels. 120 V, 15 A total, 5 A per channel.</p>
  <ul class="chans">{{chans}}</ul>
  <p class="extra">Dimmer or Switch is chosen <strong>pack-wide</strong> by dip switch 10. The
  Haze 2D must not be dimmed and it shares this pack with the jets, so it cannot be isolated:
  the pack has to be in Switch mode.</p>
  <p class="src"><span>Manual</span><code>{{manual}}</code></p>
</article>'''.format(chans=chans, manual=escape(pk["manual"]))

    mm = "".join(f'''<article class="mm {m["tone"]}">
  <span class="rank">{m["rank"]}</span>
  <h3>{m["title"]}</h3>
  <p>{m["body"]}</p>
  <p class="tell">{m["tell"]}</p>
</article>''' for m in MISMATCHES)

    legend = "".join(
        f'<span class="lg"><i style="--c:{c}"></i>{n}</span>' for c, n in
        [FAMILY[k] for k in ("beam", "laser", "wash", "strobe", "djled", "fx")])

    html = TEMPLATE.format(
        rows=rows_html(rows), evidence="\n".join(ev), mismatches=mm, dist=dist,
        u1=universe_bar(rows, 1), u2=universe_bar(rows, 2), legend=legend,
        n_manuals=len([e for e in EVIDENCE if audit.FIXTURES[e["key"]]["manual"]]) + 1,
        n_profiles=len({r["profile"] for r in rows}),
    )
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(html, encoding="utf-8")
    print(f"{dst}: {len(rows)} patched fixtures, {len(EVIDENCE)} evidence cards, "
          f"{len(MISMATCHES)} mismatches")


TEMPLATE = r'''<title>NØMAD Patch Reconciliation</title>
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
  font:400 16px/1.6 "IBM Plex Sans","Helvetica Neue",Arial,sans-serif;
  -webkit-font-smoothing:antialiased;
}}
.wrap{{max-width:1140px; margin:0 auto; padding:0 24px 96px}}
h1,h2,h3{{font-family:"IBM Plex Sans Condensed","IBM Plex Sans",Arial,sans-serif; text-wrap:balance; margin:0}}
code,.n,.mono{{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace; font-variant-numeric:tabular-nums}}

/* ---------- masthead ---------- */
.mast{{padding:72px 0 40px; border-bottom:1px solid var(--line)}}
.eyebrow{{
  font-family:"IBM Plex Mono",monospace; font-size:12px; letter-spacing:.16em;
  text-transform:uppercase; color:var(--accent); margin:0 0 18px
}}
h1{{font-size:clamp(34px,5.4vw,58px); font-weight:700; letter-spacing:-.02em; line-height:1.04}}
.dek{{max-width:64ch; color:var(--ink-2); font-size:17.5px; margin:20px 0 0}}
.counts{{display:flex; flex-wrap:wrap; gap:0; margin:36px 0 0; border:1px solid var(--line); border-radius:3px; overflow:hidden}}
.counts div{{flex:1 1 150px; padding:16px 18px; border-right:1px solid var(--line); background:var(--card)}}
.counts div:last-child{{border-right:0}}
.counts b{{display:block; font-family:"IBM Plex Mono",monospace; font-size:26px; font-weight:600; letter-spacing:-.02em}}
.counts span{{display:block; font-size:12.5px; color:var(--ink-3); margin-top:3px; letter-spacing:.02em}}
.counts .is-fault b{{color:var(--fault)}}
.counts .is-ok b{{color:var(--accent)}}

/* ---------- sections ---------- */
section{{padding:56px 0 0}}
.shead{{display:flex; align-items:baseline; gap:14px; flex-wrap:wrap; margin:0 0 6px}}
.shead h2{{font-size:26px; font-weight:600; letter-spacing:-.01em}}
.shead .num{{
  font-family:"IBM Plex Mono",monospace; font-size:12px; color:var(--ink-3);
  letter-spacing:.1em; text-transform:uppercase
}}
.lede{{color:var(--ink-2); max-width:68ch; margin:0 0 26px; font-size:16px}}

/* ---------- correlation table ---------- */
.tw{{overflow-x:auto; border:1px solid var(--line); border-radius:3px; background:var(--card)}}
table{{border-collapse:collapse; width:100%; min-width:820px; font-size:14.5px}}
thead th{{
  font-family:"IBM Plex Sans Condensed",sans-serif; font-weight:600; font-size:12px;
  letter-spacing:.09em; text-transform:uppercase; color:var(--ink-3);
  text-align:left; padding:12px 14px; border-bottom:1px solid var(--line); white-space:nowrap
}}
thead th.n{{text-align:right}}
tbody td{{padding:13px 14px; border-bottom:1px solid var(--line-2); vertical-align:middle}}
tbody tr:last-child td{{border-bottom:0}}
td.n{{text-align:right; font-family:"IBM Plex Mono",monospace; font-variant-numeric:tabular-nums; color:var(--ink-2); white-space:nowrap}}
td.n.strong{{color:var(--ink); font-weight:600}}
td.n sub{{font-size:9.5px; color:var(--ink-3)}}
td code{{font-size:13px}}
td.model{{color:var(--ink); font-weight:500}}
.swatch{{display:inline-block; width:9px; height:9px; border-radius:1px; background:var(--c); margin-right:9px; vertical-align:baseline}}
.inv-tag{{
  font-family:"IBM Plex Mono",monospace; font-size:9.5px; letter-spacing:.08em;
  text-transform:uppercase; padding:1px 4px; border:1px solid var(--line);
  border-radius:2px; color:var(--ink-3); margin-left:6px
}}
.pill{{
  display:inline-block; font-family:"IBM Plex Mono",monospace; font-size:11.5px;
  padding:3px 9px; border-radius:2px; white-space:nowrap; font-weight:500
}}
.pill.ok{{background:var(--accent-soft); color:var(--accent)}}
.pill.warn{{background:var(--warn-soft); color:var(--warn)}}
.pill.fault{{background:var(--fault-soft); color:var(--fault)}}
.pill.unknown{{background:var(--unknown-soft); color:var(--ink-3)}}
.tnote{{font-size:14px; color:var(--ink-3); margin:14px 0 0; max-width:70ch}}

/* ---------- universe map ---------- */
.legend{{display:flex; flex-wrap:wrap; gap:8px 20px; margin:0 0 22px}}
.lg{{display:flex; align-items:center; gap:7px; font-size:12.5px; color:var(--ink-2)}}
.lg i{{width:16px; height:8px; border-radius:1px; background:var(--c); display:block}}
.umap{{display:flex; flex-direction:column; gap:26px}}
.ulab{{
  display:flex; justify-content:space-between; align-items:baseline;
  font-family:"IBM Plex Mono",monospace; font-size:12px; color:var(--ink-3);
  letter-spacing:.06em; margin:0 0 7px
}}
.ulab b{{color:var(--ink); font-weight:600; letter-spacing:.1em; text-transform:uppercase}}
.uni{{position:relative}}
.unibar{{
  position:relative; height:34px; background:var(--line-2);
  border:1px solid var(--line); border-radius:2px; overflow:hidden
}}
.seg{{position:absolute; top:0; bottom:0; background:var(--c); border-radius:0}}
.seg[data-inv]{{
  background:repeating-linear-gradient(135deg,var(--c) 0 4px,color-mix(in srgb,var(--c) 55%,#000) 4px 8px)
}}
.ruler{{position:relative; height:16px; margin-top:5px}}
.tick{{position:absolute; top:0; width:1px; height:5px; background:var(--line)}}
.tick b{{
  position:absolute; left:0; top:7px; font-family:"IBM Plex Mono",monospace;
  font-size:10px; font-weight:400; color:var(--ink-3); letter-spacing:.04em
}}
.umap-note{{font-size:14px; color:var(--ink-3); margin:20px 0 0; max-width:70ch}}

/* ---------- evidence ---------- */
.evgrid{{display:grid; grid-template-columns:repeat(auto-fit,minmax(310px,1fr)); gap:16px}}
.ev{{
  background:var(--card); border:1px solid var(--line); border-radius:3px;
  padding:20px 20px 16px; border-top:2px solid var(--c); box-shadow:var(--shadow);
  display:flex; flex-direction:column; gap:12px
}}
.ev header{{display:flex; justify-content:space-between; align-items:start; gap:12px}}
.ev h3{{font-size:17.5px; font-weight:600; letter-spacing:-.005em}}
.grade{{
  font-family:"IBM Plex Mono",monospace; font-size:10.5px; letter-spacing:.05em;
  padding:3px 7px; border-radius:2px; white-space:nowrap; flex-shrink:0
}}
.grade.confirmed{{background:var(--accent-soft); color:var(--accent)}}
.grade.strong{{background:var(--accent-soft); color:var(--accent)}}
.grade.probable{{background:var(--unknown-soft); color:var(--ink-2)}}
.grade.weak{{background:var(--warn-soft); color:var(--warn)}}
.profs{{list-style:none; margin:0; padding:0; display:flex; flex-wrap:wrap; gap:6px}}
.profs li{{
  font-family:"IBM Plex Mono",monospace; font-size:11.5px; background:var(--line-2);
  border-radius:2px; padding:3px 7px; color:var(--ink-2)
}}
.profs .qty{{color:var(--ink-3)}}
.ev p{{margin:0; font-size:14.5px}}
.ev .proof{{color:var(--ink)}}
.ev .extra{{color:var(--ink-2); font-size:13.5px; padding-top:11px; border-top:1px solid var(--line-2)}}
.ev .src{{
  display:flex; gap:8px; align-items:center; font-size:11px; color:var(--ink-3);
  margin-top:auto; padding-top:11px
}}
.ev .src span{{letter-spacing:.09em; text-transform:uppercase}}
.ev .src code{{font-size:11px; color:var(--ink-2); word-break:break-all}}

.dist{{
  margin-top:16px; background:var(--card); border:1px solid var(--line);
  border-top:2px solid var(--accent); border-radius:3px; padding:20px 22px 16px;
  box-shadow:var(--shadow); display:flex; flex-direction:column; gap:12px
}}
.dist header{{display:flex; justify-content:space-between; align-items:start; gap:12px; flex-wrap:wrap}}
.dist h3{{font-size:17.5px; font-weight:600}}
.dist p{{margin:0; font-size:14.5px; max-width:82ch}}
.dist .proof{{color:var(--ink)}}
.dist .extra{{color:var(--ink-2); font-size:13.5px; padding-top:11px; border-top:1px solid var(--line-2)}}
.dist .src{{display:flex; gap:8px; align-items:center; font-size:11px; color:var(--ink-3)}}
.dist .src span{{letter-spacing:.09em; text-transform:uppercase}}
.dist .src code{{font-size:11px; color:var(--ink-2)}}
.chans{{list-style:none; margin:0; padding:0; display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:8px}}
.chans li{{
  border:1px solid var(--line); border-radius:2px; padding:9px 11px;
  display:flex; flex-direction:column; gap:2px
}}
.chans b{{font-size:12.5px; font-weight:500; color:var(--ink-2)}}
.chans span{{font-family:"IBM Plex Mono",monospace; font-size:14px; color:var(--ink-3)}}
.chans li.known span{{color:var(--warn); font-weight:500}}
.chans li.spare{{border-style:dashed}}
.chans li.spare b,.chans li.spare span{{color:var(--ink-3)}}

/* ---------- mismatches ---------- */
.mmlist{{display:flex; flex-direction:column; gap:14px}}
.mm{{
  background:var(--card); border:1px solid var(--line); border-left:3px solid var(--ink-3);
  border-radius:3px; padding:20px 22px
}}
.mm.fault{{border-left-color:var(--fault)}}
.mm.warn{{border-left-color:var(--warn)}}
.mm.benign{{border-left-color:var(--ink-3)}}
.rank{{
  font-family:"IBM Plex Mono",monospace; font-size:11px; letter-spacing:.09em;
  text-transform:uppercase; color:var(--ink-3)
}}
.mm.fault .rank{{color:var(--fault)}}
.mm.warn .rank{{color:var(--warn)}}
.mm h3{{font-size:18px; font-weight:600; margin:7px 0 10px}}
.mm p{{margin:0; font-size:15px; color:var(--ink-2); max-width:78ch}}
.mm .tell{{
  margin-top:12px; padding-top:12px; border-top:1px solid var(--line-2);
  font-size:13.5px; color:var(--ink-3)
}}
.mm strong,.ev strong{{color:var(--ink); font-weight:600}}
.mm em{{font-style:italic}}

/* ---------- open ---------- */
.open{{
  background:var(--card); border:1px solid var(--line); border-radius:3px; overflow:hidden
}}
.open li{{
  display:flex; gap:16px; align-items:baseline; padding:15px 20px;
  border-bottom:1px solid var(--line-2); font-size:14.5px; color:var(--ink-2)
}}
.open li:last-child{{border-bottom:0}}
.open ul{{list-style:none; margin:0; padding:0}}
.open .k{{
  font-family:"IBM Plex Mono",monospace; font-size:11px; letter-spacing:.07em;
  text-transform:uppercase; color:var(--ink-3); flex:0 0 108px
}}
.open .must .k{{color:var(--fault)}}
.open b{{color:var(--ink); font-weight:600}}

footer{{
  margin-top:64px; padding-top:22px; border-top:1px solid var(--line);
  font-size:13px; color:var(--ink-3); display:flex; justify-content:space-between;
  gap:16px; flex-wrap:wrap
}}
footer code{{font-size:12px}}
@media (max-width:640px){{
  .mast{{padding:48px 0 32px}}
  .counts div{{flex-basis:50%; border-bottom:1px solid var(--line)}}
}}
</style>

<div class="wrap">

<header class="mast">
  <p class="eyebrow">NØMAD Toronto · grandMA2 · showfile 2026-06-13</p>
  <h1>What the manuals say,<br>and what the patch says</h1>
  <p class="dek">Seven vendor manuals against a grandMA2 patch that names none of its fixtures.
  Every profile in the rig now has a real fixture behind it — and only one of them is patched to a
  mode that fixture can actually be set to.</p>
  <div class="counts">
    <div><b>{n_manuals}</b><span>manuals correlated</span></div>
    <div><b>{n_profiles}</b><span>MA profiles in the rig</span></div>
    <div class="is-fault"><b>5</b><span>patched to an impossible mode</span></div>
    <div class="is-ok"><b>1</b><span>profile that agrees</span></div>
    <div><b>0</b><span>address overlaps</span></div>
  </div>
</header>

<section>
  <div class="shead"><span class="num">The correlation</span><h2>Manual → profile → patch</h2></div>
  <p class="lede">One row per MA fixture profile. <b>Patched</b> is the footprint the patch
  occupies; <b>stride</b> is the gap the patcher actually left between consecutive fixtures. Where
  those two disagree, the stride is usually the truth about the fixture and the profile is the
  mistake.</p>
  <div class="tw">
    <table>
      <thead><tr>
        <th>MA profile</th><th class="n">Qty</th><th>Real fixture</th>
        <th class="n">Modes</th><th class="n">Patched</th><th class="n">Stride</th><th>Verdict</th>
      </tr></thead>
      <tbody>
{rows}
      </tbody>
    </table>
  </div>
  <p class="tnote">A stride shown as <code>13<sub>5/6</sub></code> means five of the six gaps are
  that size. <span class="inv-tag">inv</span> marks a pan/tilt-inverted duplicate profile — a
  fixture hung upside down, not a different mode.</p>
</section>

<section>
  <div class="shead"><span class="num">The evidence</span><h2>What actually made each link</h2></div>
  <p class="lede">The showfile records a profile <em>name</em> and a start address, and nothing
  else — no fixture-type definitions, no makes, no models. So each identification rests on a
  specific fact. These are those facts, strongest first.</p>
  <div class="evgrid">
{evidence}
  </div>
{dist}
</section>

<section>
  <div class="shead"><span class="num">The patch</span><h2>Where everything sits</h2></div>
  <p class="lede">Both universes to scale, 512 addresses each. Hatched blocks are the three
  fixtures hung inverted. The empty stretches are real — the patch leaves 173 clear addresses
  between the lone laser bar on U2 and the washes above it.</p>
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
  <p class="umap-note">Two CO₂ jets are not shown: they sit at address 0, unpatched. They are
  channels on an Elation DP-415 mains pack rather than DMX fixtures, so what they need is the
  pack's dip-switch address, not a patch of their own.</p>
</section>

<section>
  <div class="shead"><span class="num">The disagreements</span><h2>Five mismatches, five different costs</h2></div>
  <p class="lede">Ordered by what each one actually does to the rig, not by profile number. Only the
  first can corrupt another fixture's channels; the last is merely untidy.</p>
  <div class="mmlist">
{mismatches}
  </div>
</section>

<section>
  <div class="shead"><span class="num">Still unread</span><h2>What a walk round the rig would settle</h2></div>
  <p class="lede">Every one of these fixtures shows its mode and address on its own panel. Nothing
  here should be re-patched from a desk — the patch is internally consistent as it stands.</p>
  <div class="open"><ul>
    <li class="must"><span class="k">Must read</span><span><b>DP-415 dip switch 10.</b> The
      Hurricane Haze 2D must not be run on a dimmer, the pack's mode is pack-wide, and the hazer
      shares that pack with both CO₂ jets — so it cannot be isolated. It must read
      <b>Switch</b>. The only question here with a single correct answer.</span></li>
    <li><span class="k">Highest value</span><span><b>One strobe bar's DMX mode.</b> 13CH is
      impossible, so whatever the panel says is news. <code>CH16</code> means five bars are
      colliding.</span></li>
    <li><span class="k">Worth 1.2 kW</span><span><b>A beam's model plate.</b> Confirms the YF BEAM
      230 against the load schedule — four discharge beams are 1400–1600 W where four LED mini
      heads would have been 400 W.</span></li>
    <li><span class="k">Last unknown</span><span><b>The CO₂ jets' wattage.</b> Bounded by the pack
      at ≤5 A each and ≤10.6 A between them, but nobody has read the real figure.</span></li>
    <li><span class="k">Rigging</span><span><b>M.Wash 7, M.Wash 10, Laser.BAR 1 — hung
      inverted?</b> Confirms the duplicate-profile reading, and is the only fixture-orientation
      data the repo holds. Every position in the showfile is <code>0,0,0</code>.</span></li>
  </ul></div>
</section>

<section>
  <div class="shead"><span class="num">Load</span><h2>5.73–5.93 kW · 48–49 A at 120 V</h2></div>
  <p class="lede">A subtotal, not a total: only the CO₂ jets are missing a figure. Currents are
  real power ÷ voltage at unity power factor, so they are a <em>floor</em> — the fixtures' actual
  power factor and the discharge ballasts' inrush go on top before anything is sized. Nine laser
  bars at 6 × 500 mW / 638 nm each make this a <b>Class 4</b> installation, which is a regulated
  question rather than a lighting-design one.</p>
</section>

<footer>
  <span>EMBLEM PROJECTS INC. · audit rev 3.1 · 2026-08-25</span>
  <span>Generated from <code>NOMADFIXPATCHJUNE2026.xml</code> by <code>scripts/build-correlation-page.py</code></span>
</footer>

</div>
'''

if __name__ == "__main__":
    main()
