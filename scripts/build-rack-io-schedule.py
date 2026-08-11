#!/usr/bin/env python3
"""Generate the rack-internal connection schedule from the label CSVs.

Scope is strict: a cable is listed only if BOTH ends land on equipment inside
the rack. Booth gear (CQ-12T, DJM-V10, CDJs), the venue panel, the network
switch and the loudspeakers are all outside it, so cables to them are out of
scope even though one end sits on a rack device.

The one nuance: a handful of cables are excluded *only* because a fact is
unresolved, not because they are known to leave the rack. The network links
look external solely because nobody has located the switch, and A19's source
is unknown. Those are carried in a separate UNRESOLVED section rather than
dropped -- if the switch turns out to be rack-mounted they were internal all
along, and a document that had silently omitted them would have been wrong.

Also writes labels-rack-internal.csv, the derived print set, so the labels
that get printed are exactly the cables in this schedule.

Usage:
    python3 scripts/build-rack-io-schedule.py 07-tech-pack/rack-io-schedule.md
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from rack_palette import swatch, key_rows  # noqa: E402

CSV_DIR = Path("07-tech-pack/labeling")
SETS = ["power", "audio", "speaker", "network"]
DERIVED_CSV = CSV_DIR / "labels-rack-internal.csv"

RACK_ORDER = [
    ("Drawmer SP2120", "U2"),
    ("Bias V3 #1", "U3"),
    ("Bias Q2 #1", "U4"),
    ("— empty —", "U5"),
    ("Bias Q2 #2", "U6"),
    ("Bias V3 #2", "U7"),
    ("Bias Q5", "U8"),
    ("Tripp Lite PDU", "U9–U10"),
]
CLASS_ICON = {"POWER": "⚡", "AUDIO": "🔊", "DATA": "🔗", "SPEAKER": "🔊"}
CLASS_ORDER = {"POWER": 0, "DATA": 1, "AUDIO": 2, "SPEAKER": 3}
OUTSIDE_SWATCH = "⬜"


def load():
    rows = []
    for s in SETS:
        with (CSV_DIR / f"labels-{s}.csv").open(newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if not r.get("end_a_device") or r["end_a_device"] == "—":
                    continue
                r["_set"] = s
                rows.append(r)
    return rows


def scope(row):
    """INTERNAL, UNRESOLVED, or OUT-OF-SCOPE, from the rack's point of view."""
    a, b = row["end_a_loc"], row["end_b_loc"]
    if a == "RACK" and b == "RACK":
        return "INTERNAL"
    if {a, b} == {"RACK", "UNKNOWN"}:
        return "UNRESOLVED"
    return "OUT-OF-SCOPE"


def esc(s):
    return (s or "").replace("|", "\\|")


def ref_key(ref):
    ref = (ref or "").strip()
    if ref.upper().startswith("P") and ref[1:].isdigit():
        return (0, int(ref[1:]))
    if ref.isdigit():
        return (1, int(ref))
    return (2, 0)


def sort_rows(rs):
    return sorted(rs, key=lambda r: (CLASS_ORDER.get(r["class"], 9), ref_key(r["cable_ref"])))


EXCLUSION_REASON = {
    "PANEL": "Venue electrical panel — mains feeds to rack devices",
    "BOOTH": "DJ booth equipment — CQ-12T, DJM-V10, CDJs",
    "ROOM": "Loudspeakers on the floor",
    "ENTRANCE": "Entrance fill speakers",
    "UNKNOWN": "Location unresolved",
}


def why_excluded(row):
    """Group cables by *where* they leave the rack, not by which device.

    Grouping on the device name fragments this into one row per loudspeaker,
    which buries the point: the reader wants to know what categories of cable
    were set aside, not to re-read the speaker inventory.
    """
    outside = {loc for loc in (row["end_a_loc"], row["end_b_loc"]) if loc != "RACK"}
    return " + ".join(EXCLUSION_REASON.get(loc, loc.title()) for loc in sorted(outside))


def main():
    dst = Path(sys.argv[1] if len(sys.argv) > 1 else "07-tech-pack/rack-io-schedule.md")
    rows = load()
    internal = sort_rows([r for r in rows if scope(r) == "INTERNAL"])
    unresolved = sort_rows([r for r in rows if scope(r) == "UNRESOLVED"])
    out_of_scope = [r for r in rows if scope(r) == "OUT-OF-SCOPE"]
    in_set = internal + unresolved

    def counts(rs):
        d = {}
        for r in rs:
            d[r["class"]] = d.get(r["class"], 0) + 1
        return d

    ci, cu = counts(internal), counts(unresolved)

    L = []
    L += ["---",
          "title: Nomad Toronto — Rack Internal Connections (Power · Data · Audio)",
          "description: Cables with both ends on equipment inside the amplifier rack. "
          "Connector type at each end and both devices identified. Generated from the "
          "cable-label data.",
          "version: 2.0.0",
          "created: 2026-08-11T00:00:00Z",
          "last_updated: 2026-08-11T00:00:00Z",
          "generated_by: scripts/build-rack-io-schedule.py",
          "---", "",
          "# Nomad Toronto — Rack Internal Connections", ""]

    L += ["> **Generated file — do not hand-edit.** Source data is "
          "`07-tech-pack/labeling/labels-{power,audio,speaker,network}.csv`, the same rows that "
          "print the cable labels. Edit those and re-run "
          "`python3 scripts/build-rack-io-schedule.py`.", ""]

    L += ["## Scope", "",
          "**Strictly cables with both ends on rack equipment.** A cable is out of scope if "
          "either end lands on booth gear (CQ-12T, DJM-V10, CDJs), the venue electrical panel, "
          "the loudspeakers, or anything else outside the rack — even when its other end is on a "
          "rack device.", "",
          f"| | Cables | Power | Data | Audio |",
          f"|---|------:|------:|-----:|------:|",
          f"| **Confirmed internal** | **{len(internal)}** | {ci.get('POWER','—')} | "
          f"{ci.get('DATA','—')} | {ci.get('AUDIO','—')} |",
          f"| **Unresolved** (see §2) | **{len(unresolved)}** | {cu.get('POWER','—')} | "
          f"{cu.get('DATA','—')} | {cu.get('AUDIO','—')} |",
          f"| **Total in this document** | **{len(in_set)}** | | | |", "",
          "Bias V9 has been removed from the rack and does not appear.", "",
          "---", ""]

    # ---- colour key --------------------------------------------------------
    L += ["## Cable tie colours", "",
          "**You do not need this table to read the schedule** — every swatch below sits directly "
          "beside the device it belongs to, and on the proof sheets each chip is printed with its "
          "device name on it. This is here for one job only: knowing which tie to reach for at "
          "the rack.", "",
          "The DK-1221 roll is black thermal on white paper, so the printed labels carry no "
          "colour. On the rack the colour is carried by **the cable tie the tag folds over** — "
          "free, since the fold-over design already needs a tie.", "",
          "| | Device | Rack U | Hex | Cable tie |",
          "|---|--------|--------|-----|-----------|"]
    _u = {d: u for d, u in RACK_ORDER}
    for dev, hexv, emoji, tie in key_rows():
        L.append(f"| {emoji} | {dev} | {_u.get(dev,'—')} | `{hexv}` | {tie} |")
    L += [f"| {OUTSIDE_SWATCH} | *anything outside the rack* | — | `#BBBBBB` | — |", "",
          "Hexes are the Okabe-Ito palette, which stays distinguishable under all common forms "
          "of colour blindness — worth caring about in a dark rack room where colour "
          "discrimination is already degraded.", "", "---", ""]

    # ---- §1 confirmed ------------------------------------------------------
    L += ["## §1 Confirmed internal connections", "",
          "Both ends verified as rack equipment. These are the cables you re-make if the rack is "
          "stripped and rebuilt.", "",
          "| Cable | Class | From device | From port | Connector | To device | To port | Connector |",
          "|-------|-------|-------------|-----------|-----------|-----------|---------|-----------|"]
    for r in internal:
        L.append(f"| `{r['cable_ref']}` | {CLASS_ICON.get(r['class'],'')} {r['class'].title()} | "
                 f"{swatch(r['end_a_device'])} {esc(r['end_a_device'])} | {esc(r['end_a_port'])} | "
                 f"{esc(r['conn_a'])} | "
                 f"{swatch(r['end_b_device'])} {esc(r['end_b_device'])} | {esc(r['end_b_port'])} | "
                 f"{esc(r['conn_b'])} |")
    L += ["", "---", ""]

    # ---- §2 unresolved -----------------------------------------------------
    L += ["## §2 Unresolved — may be internal", "",
          "These are excluded from §1 **only because a fact is unknown**, not because they are "
          "known to leave the rack. They are carried here rather than dropped: if the switch is "
          "rack-mounted, the five control links were internal all along.", "",
          "| Cable | Class | Rack device | Rack port | Connector | Unknown end | What is unresolved |",
          "|-------|-------|-------------|-----------|-----------|-------------|--------------------|"]
    for r in unresolved:
        if r["end_a_loc"] == "RACK":
            rd, rp, rc, ud = r["end_a_device"], r["end_a_port"], r["conn_a"], r["end_b_device"]
        else:
            rd, rp, rc, ud = r["end_b_device"], r["end_b_port"], r["conn_b"], r["end_a_device"]
        L.append(f"| `{r['cable_ref']}` | {CLASS_ICON.get(r['class'],'')} {r['class'].title()} | "
                 f"{swatch(rd)} {esc(rd)} | {esc(rp)} | {esc(rc)} | {swatch(ud)} {esc(ud)} | "
                 f"{esc(r['note'])} |")
    L += ["", "Resolve these and re-run the build — they move into §1 automatically if both ends "
          "turn out to be in the rack.", "", "---", ""]

    # ---- §3 by device ------------------------------------------------------
    L += ["## §3 By device", "",
          "Same connections, grouped by rack unit. **Dir** is in/out at *this* device's panel.", ""]
    for device, u in RACK_ORDER:
        drows = []
        for r in in_set:
            if r["end_a_device"] == device:
                drows.append((r, "OUT ▶", r["end_a_port"], r["conn_a"],
                              r["end_b_device"], r["end_b_port"]))
            if r["end_b_device"] == device:
                drows.append((r, "◀ IN", r["end_b_port"], r["conn_b"],
                              r["end_a_device"], r["end_a_port"]))
        drows.sort(key=lambda t: (CLASS_ORDER.get(t[0]["class"], 9), ref_key(t[0]["cable_ref"])))
        L += [f"### {u} · {swatch(device)} {device}", ""]
        if not drows:
            if device == "— empty —":
                L += ["Bay empty — Bias V9 removed. The **32 A CPC 45A circuit is still live to "
                      "this bay**; it runs from the venue panel, so it is out of scope here, but "
                      "it needs capping or decommissioning. See `rack-io-inventory.md` §5.", ""]
            else:
                L += ["*No internal connections — this device's cables all leave the rack.*", ""]
            continue
        L += ["| Dir | Class | Port | Connector | Far end | Far-end port | Cable |",
              "|-----|-------|------|-----------|---------|--------------|-------|"]
        for r, dirn, port, conn, far_dev, far_port in drows:
            L.append(f"| {dirn} | {CLASS_ICON.get(r['class'],'')} {r['class'].title()} | "
                     f"{esc(port)} | {esc(conn)} | {swatch(far_dev)} {esc(far_dev)} | "
                     f"{esc(far_port)} | `{r['cable_ref']}` |")
        L.append("")
    L += ["---", ""]

    # ---- §4 excluded -------------------------------------------------------
    by_reason = {}
    for r in out_of_scope:
        key = why_excluded(r)
        by_reason.setdefault(key, []).append(r["cable_ref"])
    L += ["## §4 Out of scope", "",
          f"{len(out_of_scope)} cables in the label data have at least one end outside the rack. "
          "Summarised so their absence reads as a decision, not an oversight. Full detail for "
          "these lives in `07-tech-pack/cable-schedule.md` and the label CSVs.", "",
          "| Outside-the-rack end | Cables | Count |",
          "|----------------------|--------|------:|"]
    for reason in sorted(by_reason, key=lambda k: -len(by_reason[k])):
        refs = ", ".join(f"`{x}`" for x in sorted(by_reason[reason], key=ref_key))
        L.append(f"| {esc(reason)} | {refs} | {len(by_reason[reason])} |")
    L += ["", "---", ""]

    # ---- §5 print set ------------------------------------------------------
    total_labels = sum(int(r["qty"]) for r in in_set)
    L += ["## §5 Label print set", "",
          f"The {len(in_set)} cables above need **{total_labels} labels** (two per cable, one per "
          "end). The derived print set is written to "
          "`07-tech-pack/labeling/labels-rack-internal.csv` by this same script — build its proof "
          "and template with:", "",
          "```bash",
          "python3 scripts/build-cable-labels.py \\",
          "    07-tech-pack/labeling/labels-rack-internal.csv \\",
          "    07-tech-pack/labeling/dk1221-rack-internal-proof.svg",
          "python3 scripts/build-lbx.py \\",
          "    07-tech-pack/labeling/labels-rack-internal.csv \\",
          "    07-tech-pack/labeling/dk1221-rack-internal.lbx",
          "```", "",
          "No labels are produced for CQ-12T or DJM-V10 connections.", "",
          "---", "",
          "*EMBLEM PROJECTS INC. · generated from label data*"]

    dst.write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---- derived print-set CSV --------------------------------------------
    fields = [f for f in in_set[0].keys() if f != "_set"]
    with DERIVED_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in in_set:
            w.writerow({k: v for k, v in r.items() if k != "_set"})

    print(f"{dst}: {len(internal)} confirmed internal + {len(unresolved)} unresolved "
          f"= {len(in_set)} cables, {len(out_of_scope)} out of scope")
    print(f"{DERIVED_CSV}: {len(in_set)} designs, {total_labels} labels")


if __name__ == "__main__":
    main()
