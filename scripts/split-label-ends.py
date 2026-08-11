#!/usr/bin/env python3
"""Split a label CSV into two — one per cable end.

A cable needs a tag at each end, and until now both tags carried identical
text. That reads badly in the rack: standing at the V3 #2 panel, a tag whose
headline says "SP2120 L" is describing the *other* end of the cable.

Splitting per end lets each tag be written from where it is actually fitted:

    end A tag   SP2120 OUT L        end B tag   V3 #2 CH1 IN
                A15 → V3 #2                     A15 → SP2120

Line 1 is always the socket you are standing at. Line 2 is always the cable
ID and the device at the far end, so either tag answers both "what am I
plugged into" and "where does this go".

In the end-B file the end_a/end_b column pairs are swapped, so "end_a" always
means "this end". That keeps every downstream consumer simple: the proof's
left-hand colour chip is always the end you are holding.

Usage:
    python3 scripts/split-label-ends.py 07-tech-pack/labeling/labels-rack-internal.csv
writes one file per (class, end) alongside it:

    labels-rack-power-end-a.csv    labels-rack-power-end-b.csv
    labels-rack-audio-end-a.csv    labels-rack-audio-end-b.csv
    labels-rack-data-end-a.csv     labels-rack-data-end-b.csv

Six sheets, because power, audio and data get fitted in separate passes and a
print run should match the pass. Only classes actually present are emitted.
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from rack_palette import short, short_port, ascii_label  # noqa: E402

A_FIELDS = ("end_a_device", "end_a_port", "end_a_loc", "conn_a")
B_FIELDS = ("end_b_device", "end_b_port", "end_b_loc", "conn_b")


def label_ref(row):
    """The prefixed short ID used everywhere else: AUD-A15 -> A15, PWR-P1 -> P1.

    cable_ref alone is a bare number for the audio/speaker/network sets, and
    "15 -> V3 #2" on a tag does not match the A15 in the schedule.
    """
    return (row.get("id") or "").split("-")[-1].strip()


def detail(row, far_device):
    """Cable ID and where the other end lands."""
    r = label_ref(row)
    far = short(far_device)
    return f"{r} → {far}" if r else f"→ {far}"


def flip(row):
    """Swap the two end column-groups so end_a always means 'this end'."""
    out = dict(row)
    for a, b in zip(A_FIELDS, B_FIELDS):
        out[a], out[b] = row[b], row[a]
    return out


def build(rows, side):
    out = []
    for r in rows:
        if not r.get("end_a_device") or r["end_a_device"] == "—":
            continue  # blank spare rows describe no cable end
        rr = dict(r) if side == "a" else flip(r)
        rr["id"] = f"{r['id']}-{side.upper()}"
        # Three lines: who I am / which socket / where the far end is. Packing
        # device+port onto one headline overran the 17.08 mm printable width.
        rr["line1"] = ascii_label(short(rr["end_a_device"]))
        rr["line2"] = ascii_label(short_port(rr["end_a_port"]) or "-")
        rr["line3"] = ascii_label(detail(r, rr["end_b_device"]))
        rr["qty"] = "1"          # one tag per end
        rr["side"] = side.upper()
        out.append(rr)
    return out


def write(path, rows):
    fields = [f for f in rows[0].keys()]
    # Printed fields lead: P-touch Editor auto-maps layout objects to database
    # columns in order, so line1..line3 first means its first guesses are right.
    lead = [k for k in ("line1", "line2", "line3") if k in fields]
    fields = lead + [k for k in fields if k not in lead]
    # BOM: Editor otherwise reads the file as CP1252 and mangles any non-ASCII.
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1
               else "07-tech-pack/labeling/labels-rack-internal.csv")
    rows = list(csv.DictReader(src.open(newline="", encoding="utf-8-sig")))

    # "rack-internal" -> "rack"; the class name carries the rest of the meaning
    stem = src.stem.replace("labels-", "").replace("-internal", "")

    total = 0
    for side in ("a", "b"):
        built = build(rows, side)
        by_class = {}
        for r in built:
            by_class.setdefault((r.get("class") or "MISC").lower(), []).append(r)
        for cls in sorted(by_class):
            group = by_class[cls]
            dst = src.with_name(f"labels-{stem}-{cls}-end-{side}.csv")
            write(dst, group)
            total += len(group)
            print(f"{dst.name}: {len(group)} tags")
            for r in group:
                print(f"    {r['line1']:<10} {r['line2']:<14} {r['line3']}")
    print(f"\n{total} tags across the sheets")


if __name__ == "__main__":
    main()
