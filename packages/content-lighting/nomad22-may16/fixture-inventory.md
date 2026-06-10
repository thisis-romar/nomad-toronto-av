# Showfile fixture/layer inventory — nomad22-may16

> **This is a FIXTURE/LAYER PATCH EXPORT, not a preset export.** It contains Layers, Fixtures, FixtureTypes, SubFixtures, Patch Addresses, and Channel indexes. It does **NOT** contain Preset pool objects. Therefore the preset audit is **NOT complete** from this file alone — Preset pools 1–9 must still be audited live/separately. Do not claim presets have been audited from this file.

## Showfile context

- Showfile: nomad22-may16
- Export timestamp: 2026-06-10T03:18:32
- MA2 XML version: 3.9.60
- Layers: 10
- Fixture records: 34
- Unique fixture types: 8 (FT1 has zero fixtures — console-reserved/default; only FT2–FT9 carry fixtures)
- SubFixtures: 91
- Channel index entries: 424
- Consistency check: 3+1+7+8+2+1+8+4 = 34 fixture records ✓

## Fixture types

| FT No. | Fixture type | Count | Fixture IDs | Layer | Preset implication |
| --- | --- | --- | --- | --- | --- |
| 2 | `2 Dimmer 00` | 3 records | `911`, `911` multipatch, `420` | `--Co2(2x)`, `~Atmos~` | SAFETY EXCEPTION — do not global-dim this FT blindly. CO2 and Atmos share the same FT. |
| 3 | `3 LED Bar 2 11CH` | 1 | `1` | `--LED.DJ-Decks` | RGB/dimmer/strobe likely; attributes must be discovered. |
| 4 | `4 rgbw-13ch 13CH` | 7 | `801–807` | `--LED.STROBE-BAR` | RGBW + strobe/shutter base likely. Strong global-preset candidate. |
| 5 | `5 NEW WASH` | 8 | `101–106`, `108–109` | `--M.WASH` | Moving wash base: dimmer/color/position/strobe/zoom if present. |
| 6 | `6 movingwash zone` | 2 | `107`, `110` | `--M.WASH` | Separate from FT5. Do not merge with NEW WASH until attributes match. |
| 7 | `7 LASER BARS - Invert 26CH` | 1 | `1001` | `--M.Laser-BAR` | Inverted laser-bar type. Keep separate from FT8. |
| 8 | `8 LASER BARS 26CH` | 8 | `1002–1009` | `--M.Laser-BAR` | Laser-bar base; SFX/control-heavy, not generic lighting. |
| 9 | `9 Sharpy Standard Lamp on` | 4 | `401–404` | `--M.Beam` | Beam base: dimmer, position, gobo, color wheel, beam, strobe/shutter. |

## Notes

- FT4 is RGBW (White emitter, NOT amber) — any amber look is an RGB color mix, name it accordingly (e.g. "Amber (mix)").
- FT5 and FT6 both live on layer `--M.WASH` but are DISTINCT fixture types — keep separate scopes and verify attribute parity before any shared look.
- Fixture 911 has a multipatch record, so a by-fixture-ID preset on 911 also affects its multipatch instance.
