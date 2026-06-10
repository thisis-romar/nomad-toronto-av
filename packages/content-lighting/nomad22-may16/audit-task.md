# Audit-only harness task — nomad22-may16

Paste this into the MA2 console harness. This is an AUDIT-ONLY run — it must NOT write/store any objects to the console.

## Task

```text
Using the uploaded fixture/layer export for nomad22-may16, audit the live Preset pools 1 through 9 and the fixture-type attributes for FT2 through FT9. DO NOT WRITE — read-only. Produce a "missing global-preset coverage matrix", excluding FT2 CO2/Atmos from generic global dimmer levels, and holding FT7/FT8 laser-output presets behind operator approval.
```

## Read-only tool sequence

1. list_preset_pool(1) through list_preset_pool(9) — enumerate existing presets in each pool.
2. browse_preset_type(1..9) — inspect preset types present.
3. discover_fixture_type_attributes for FT2, FT3, FT4, FT5, FT6, FT7, FT8, FT9 — map real attributes per type.
4. export_objects(object_type="Preset", filename="AUDIT_PRESETS_nomad22-may16_20260610") — snapshot current presets.

## Guards (must hold during this run)

- No write/store/create/update operations of any kind.
- FT2: excluded from generic global dimmer-level coverage (CO2/Atmos collision — see safety-findings.md).
- FT7 / FT8: laser output presets are out of scope until operator approval.
- Shapers/Flags: treat as absent unless attribute discovery proves shaper/blade/flag channels exist.

## Deliverable

- A coverage matrix: per fixture type (FT2–FT9) × intended preset categories (Dimmer, Color/RGBW, Position, Gobo, Beam/Prism/Frost, Strobe/Shutter, Zoom), marking PRESENT / MISSING / N-A / HELD.
- An explicit list of safe presets that CAN be built next, and the held items requiring operator approval.
- No console writes performed.
