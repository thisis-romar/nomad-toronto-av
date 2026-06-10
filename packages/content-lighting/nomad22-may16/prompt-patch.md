# Harness prompt patch — SHOWFILE-SPECIFIC CONTEXT (nomad22-may16)

Inject the following block into the MA2 harness system prompt under a `SHOWFILE-SPECIFIC CONTEXT` heading. It is the canonical, version-controlled source of truth for this showfile.

```text
SHOWFILE-SPECIFIC CONTEXT FROM XML EXPORT
The active exported showfile is:
- showfile: nomad22-may16
- export datetime: 2026-06-10T03:18:32
- MA XML version: 3.9.60
This XML is a fixture/layer export only. It contains Layers, Fixtures, FixtureTypes, SubFixtures, Patch Addresses, and Channel indexes. It does NOT contain Preset pool objects. Therefore:
- Do not claim preset objects have been audited from this file alone.
- A live or separate XML audit of Preset 1 Thru 9 is still required.
- Use this export as the fixture-type inventory for the preset audit plan.
Fixture types present:
1. FT2 — "2 Dimmer 00"
   - Fixtures: 911, 911 multipatch, 420
   - Layers: --Co2(2x), ~Atmos~
   - SAFETY EXCEPTION: Do not create global dimmer level presets for FT2.
   - Reason: CO2 and Atmos share the same fixture type. Global FT2 dimmer presets could trigger SFX.
   - Allowed initial plan: Off/safe only. Any Full/level presets must be Selective or group-scoped and require operator approval.
2. FT3 — "3 LED Bar 2 11CH"
   - Fixture: 1
   - Layer: --LED.DJ-Decks
   - Multi-subfixture LED bar.
   - Audit attributes before assigning RGB/strobe/dim presets.
3. FT4 — "4 rgbw-13ch 13CH"
   - Fixtures: 801 Thru 807
   - Layer: --LED.STROBE-BAR
   - Strong candidate for global RGBW color presets and strobe/shutter presets.
   - Discover exact attributes before store.
4. FT5 — "5 NEW WASH"
   - Fixtures: 101, 102, 103, 104, 105, 106, 108, 109
   - Layer: --M.WASH
   - Candidate for dimmer, color, position, strobe/shutter, zoom/beam if present.
   - Keep separate from FT6 unless attribute maps prove compatibility.
5. FT6 — "6 movingwash zone"
   - Fixtures: 107, 110
   - Layer: --M.WASH
   - Separate moving-wash fixture type.
   - Do not merge presets with FT5 without verification.
6. FT7 — "7 LASER BARS - Invert 26CH"
   - Fixture: 1001
   - Layer: --M.Laser-BAR
   - Inverted laser-bar type.
   - Keep separate from FT8.
7. FT8 — "8 LASER BARS 26CH"
   - Fixtures: 1002 Thru 1009
   - Layer: --M.Laser-BAR
   - Laser/SFX fixture type.
   - Build only safe base presets after attribute discovery.
   - Avoid unsafe laser output presets until operator confirms use case.
8. FT9 — "9 Sharpy Standard Lamp on"
   - Fixtures: 401 Thru 404
   - Layer: --M.Beam
   - Candidate for beam fixture base:
     Dimmer, Position, Gobo, Color wheel, Beam, Focus if present, Shutter/Strobe.
   - Do not create lamp/reset/control presets without approval.
SHOWFILE-SPECIFIC PRESET STRATEGY
Priority build order:
1. Audit Preset 1 Thru 9 pools.
2. Discover attributes for FT3, FT4, FT5, FT6, FT7, FT8, FT9.
3. Exclude FT2 from generic global dimmer levels.
4. Build FT4 RGBW/strobe base first.
5. Build FT5 and FT6 wash bases separately.
6. Build FT9 Sharpy beam base.
7. Build FT7/FT8 laser-bar bases only after safety approval.
8. Leave Shapers/Flags empty unless live attribute discovery proves shaper/blade/flag channels exist.
9. Save as:
   nomad22-may16_GLOBAL_PRESET_BASE_20260610
Required live audit after this export:
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
```
