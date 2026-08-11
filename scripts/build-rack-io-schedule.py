#!/usr/bin/env python3
"""Generate the rack I/O schedule from the label CSVs.

Every connection in the rack is already described once, in the label data --
endpoints, ports, connector types, location of each end. This script derives
the schedule from that same data rather than restating it, so the labels on
the cables and the schedule on the wall cannot drift apart.

Scope is strictly the rack: a cable appears only if at least one end sits in
the rack. Booth-to-booth runs (DJM->CQ, Pro DJ Link) and room runs that never
touch it (CQ->Athens) are counted and listed as excluded, not silently
dropped -- "not in this document" should be a visible decision.

Usage:
    python3 scripts/build-rack-io-schedule.py 07-tech-pack/rack-io-schedule.md
"""

import csv
import sys
from collections import OrderedDict
from pathlib import Path

CSV_DIR = Path("07-tech-pack/labeling")
SETS = ["power", "audio", "speaker", "network"]

# Rack devices in rack order. U5 is deliberately listed: an empty bay with a
# live 32 A circuit behind it is a fact a reader needs, not an absence.
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


def load():
    rows = []
    for s in SETS:
        with (CSV_DIR / f"labels-{s}.csv").open(newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if not r.get("end_a_device") or r["end_a_device"] == "—":
                    continue  # blank spare-label rows describe no connection
                rows.append(r)
    return rows


def direction(row):
    """From the rack's point of view."""
    a, b = row["end_a_loc"], row["end_b_loc"]
    if a == "RACK" and b == "RACK":
        return "INTERNAL"
    if b == "RACK":
        return "IN"
    if a == "RACK":
        return "OUT"
    return "EXTERNAL"


def esc(s):
    return (s or "").replace("|", "\\|")


def ref_key(ref):
    """Sort cable refs naturally: 9 before 10, and P-numbers before plain ones."""
    ref = (ref or "").strip()
    if ref.upper().startswith("P") and ref[1:].isdigit():
        return (0, int(ref[1:]))
    if ref.isdigit():
        return (1, int(ref))
    return (2, 0)


def device_rows(rows, device):
    """Every connection touching one rack device, from its own point of view."""
    out = []
    for r in rows:
        if r["end_a_device"] == device:
            out.append((r, "out", r["end_a_port"], r["conn_a"],
                        r["end_b_device"], r["end_b_port"], r["conn_b"]))
        if r["end_b_device"] == device:
            out.append((r, "in", r["end_b_port"], r["conn_b"],
                        r["end_a_device"], r["end_a_port"], r["conn_a"]))
    order = {"POWER": 0, "DATA": 1, "AUDIO": 2, "SPEAKER": 3}
    return sorted(out, key=lambda t: (order.get(t[0]["class"], 9), ref_key(t[0]["cable_ref"])))


def main():
    dst = Path(sys.argv[1] if len(sys.argv) > 1 else "07-tech-pack/rack-io-schedule.md")
    rows = load()
    rack = [r for r in rows if direction(r) != "EXTERNAL"]
    external = [r for r in rows if direction(r) == "EXTERNAL"]

    counts = OrderedDict()
    for d in ("IN", "OUT", "INTERNAL"):
        counts[d] = OrderedDict()
        for c in ("POWER", "DATA", "AUDIO", "SPEAKER"):
            n = len([r for r in rack if direction(r) == d and r["class"] == c])
            if n:
                counts[d][c] = n

    L = []
    L.append("---")
    L.append("title: Nomad Toronto — Rack I/O Schedule (Power · Data · Audio)")
    L.append("description: Every connection into, out of, and within the amplifier rack. "
             "One row per cable end, with connector type and the device at the far end. "
             "Generated from the label data so the cables and this schedule cannot disagree.")
    L.append("version: 1.0.0")
    L.append("created: 2026-08-11T00:00:00Z")
    L.append("last_updated: 2026-08-11T00:00:00Z")
    L.append("generated_by: scripts/build-rack-io-schedule.py")
    L.append("---")
    L.append("")
    L.append("# Nomad Toronto — Rack I/O Schedule")
    L.append("")
    L.append("> **Generated file — do not hand-edit.** Source data lives in "
             "`07-tech-pack/labeling/labels-{power,audio,speaker,network}.csv`, the same rows "
             "that print the cable labels. Edit those and re-run "
             "`python3 scripts/build-rack-io-schedule.py`.")
    L.append("")
    L.append("**Scope:** strictly the amplifier rack. A cable is listed only if at least one end "
             "terminates in the rack. Bias V9 has been removed from the rack and does not appear.")
    L.append("")
    L.append("| Direction | Meaning |")
    L.append("|-----------|---------|")
    L.append("| **IN** | Enters the rack from outside (booth, venue panel, network) |")
    L.append("| **OUT** | Leaves the rack (loudspeakers, booth PSU) |")
    L.append("| **INTERNAL** | Both ends inside the rack |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## §1 Rack boundary — totals")
    L.append("")
    L.append("| Direction | Power | Data | Audio | Speaker | Total |")
    L.append("|-----------|------:|-----:|------:|--------:|------:|")
    for d in ("IN", "OUT", "INTERNAL"):
        c = counts[d]
        tot = sum(c.values())
        L.append(f"| **{d}** | {c.get('POWER','—')} | {c.get('DATA','—')} | "
                 f"{c.get('AUDIO','—')} | {c.get('SPEAKER','—')} | **{tot}** |")
    L.append(f"| | | | | | **{len(rack)} cables** |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## §2 Connections by device")
    L.append("")
    L.append("Each table is written from that device's point of view: **Dir** is in/out at "
             "*this* device's panel, **Port** is its own connector, **Far end** is what sits "
             "on the other end of the cable.")
    L.append("")

    for device, u in RACK_ORDER:
        drows = device_rows(rack, device)
        L.append(f"### {u} · {device}")
        L.append("")
        if not drows:
            if device == "— empty —":
                spare = [r for r in rows if r["end_b_port"].startswith("U5")]
                note = spare[0]["note"] if spare else ""
                L.append(f"Bay empty — Bias V9 removed. A **32 A CPC 45A circuit remains live to "
                         f"this bay**. {note}")
            else:
                L.append("*No connections recorded.*")
            L.append("")
            continue
        L.append("| Dir | Class | Port / channel | Connector | Far end | Far-end port | Cable |")
        L.append("|-----|-------|----------------|-----------|---------|--------------|-------|")
        for r, dirn, port, conn, far_dev, far_port, far_conn in drows:
            icon = CLASS_ICON.get(r["class"], "")
            arrow = "◀ IN" if dirn == "in" else "OUT ▶"
            L.append(f"| {arrow} | {icon} {r['class'].title()} | {esc(port)} | {esc(conn)} | "
                     f"{esc(far_dev)} | {esc(far_port)} | `{r['cable_ref']}` |")
        L.append("")

    L.append("---")
    L.append("")
    L.append("## §3 Crossing the rack boundary")
    L.append("")
    L.append("Everything that physically enters or leaves the rack — the list to check when the "
             "rack is moved, re-terminated, or handed to a visiting engineer.")
    L.append("")
    L.append("| Cable | Class | Dir | Outside the rack | Connector | Rack device | Rack port |")
    L.append("|-------|-------|-----|------------------|-----------|-------------|-----------|")
    for r in sorted([x for x in rack if direction(x) in ("IN", "OUT")],
                    key=lambda x: ({"POWER": 0, "DATA": 1, "AUDIO": 2, "SPEAKER": 3}
                                   .get(x["class"], 9), ref_key(x["cable_ref"]))):
        d = direction(r)
        if d == "IN":
            outside, out_conn = r["end_a_device"], r["conn_a"]
            rack_dev, rack_port = r["end_b_device"], r["end_b_port"]
        else:
            outside, out_conn = r["end_b_device"], r["conn_b"]
            rack_dev, rack_port = r["end_a_device"], r["end_a_port"]
        icon = CLASS_ICON.get(r["class"], "")
        L.append(f"| `{r['cable_ref']}` | {icon} {r['class'].title()} | {d} | {esc(outside)} | "
                 f"{esc(out_conn)} | {esc(rack_dev)} | {esc(rack_port)} |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## §4 Deliberately excluded — never touches the rack")
    L.append("")
    L.append(f"{len(external)} cables in the label sets run entirely outside the rack. They are "
             "listed here so their absence above reads as a decision rather than an oversight.")
    L.append("")
    L.append("| Cable | Class | From | To | Why excluded |")
    L.append("|-------|-------|------|----|--------------|")
    for r in sorted(external, key=lambda x: (x["class"], ref_key(x["cable_ref"]))):
        icon = CLASS_ICON.get(r["class"], "")
        L.append(f"| `{r['cable_ref']}` | {icon} {r['class'].title()} | {esc(r['end_a_device'])} | "
                 f"{esc(r['end_b_device'])} | {esc(r['end_a_loc'])} → {esc(r['end_b_loc'])} |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## §5 Rows carrying an unverified fact")
    L.append("")
    prov = [r for r in rack if "UNKNOWN" in (r["end_a_loc"], r["end_b_loc"])
            or "(D" in r.get("note", "")]
    L.append("| Cable | What is unverified |")
    L.append("|-------|--------------------|")
    for r in sorted(prov, key=lambda x: ref_key(x["cable_ref"])):
        L.append(f"| `{r['cable_ref']}` | {esc(r['note'])} |")
    L.append("")
    L.append("Cross-referenced to the discrepancy IDs in "
             "`07-tech-pack/rack-io-inventory.md` §12.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("*EMBLEM PROJECTS INC. · generated from label data · "
             "re-run the build script after editing any labels-*.csv*")

    dst.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{dst}: {len(rack)} rack cables "
          f"({sum(counts['IN'].values())} in, {sum(counts['OUT'].values())} out, "
          f"{sum(counts['INTERNAL'].values())} internal), {len(external)} excluded")


if __name__ == "__main__":
    main()
