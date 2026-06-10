# Preset build strategy — nomad22-may16

> The original "global per fixture-type" strategy is mostly correct, but this export proves two exceptions — (1) FT2 must NOT be globally leveled (CO2 and Atmos share the same generic dimmer fixture type), and (2) FT7/FT8 lasers must be safety-gated. See `safety-findings.md` in this folder.

## Priority build order

1. Audit Preset 1 Thru 9 pools.
2. Discover attributes for FT3, FT4, FT5, FT6, FT7, FT8, FT9.
3. Exclude FT2 from generic global dimmer levels.
4. Build FT4 RGBW/strobe base first.
5. Build FT5 and FT6 wash bases separately.
6. Build FT9 Sharpy beam base.
7. Build FT7/FT8 laser-bar bases only after safety approval.
8. Leave Shapers/Flags empty unless live attribute discovery proves shaper/blade/flag channels exist.
9. Save as: `nomad22-may16_GLOBAL_PRESET_BASE_20260610`

## Fixture-type coverage plan

| Fixture type | Build now? | Preset coverage |
| --- | --- | --- |
| FT2 Dimmer / CO2 / Atmos | No — safety hold | Off only until operator confirms. Avoid global Full/level presets. |
| FT3 DJ LED Bar | Audit first | Dimmer, RGB/color, strobe if attributes exist. |
| FT4 RGBW Strobe Bars | Yes, after preset-pool audit | Dimmer, RGBW colors, white, amber approximation (RGB mix), strobe/shutter speeds. |
| FT5 NEW WASH | Yes, separate block | Dimmer, color, position home, strobe/shutter, zoom/beam if present. |
| FT6 Movingwash Zone | Yes, separate block | Same as FT5 but separate Global scope. |
| FT7 Laser Bars Invert | Safety hold | Build only safe blackout/off/color base after approval. |
| FT8 Laser Bars | Safety hold | Same as FT7; no unsafe laser-output presets blind. |
| FT9 Sharpy | Yes | Dimmer, position, gobo, color wheel, beam/prism/frost, strobe/shutter. |

## What this changes in the agent plan

1. FT2 must not be globally leveled because CO2 and Atmos share the same generic dimmer fixture type.
2. FT7 and FT8 lasers must be safety-gated because laser-output presets can be hazardous if built blindly.

The next valid harness task is NOT "create presets" — it is an AUDIT (see `audit-task.md`).

## Required live audit (must run in the MA2 harness before any build)

- list_preset_pool(1)
- list_preset_pool(2)
- list_preset_pool(3)
- list_preset_pool(4)
- list_preset_pool(5)
- list_preset_pool(6)
- list_preset_pool(7)
- list_preset_pool(8)
- list_preset_pool(9)
- browse_preset_type(1..9)
- discover_fixture_type_attributes for FT2..FT9
- export_objects(object_type="Preset", filename="AUDIT_PRESETS_nomad22-may16_20260610")

These tools live in the MA2 console harness, not this repo session.
