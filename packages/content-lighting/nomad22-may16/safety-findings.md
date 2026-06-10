# Critical safety findings — nomad22-may16

## FT2 `Dimmer 00` — CO2 / Atmos collision (safety-critical)

FT2 contains BOTH `Co2-HL.HR` at fixture ID `911` (incl. a multipatch record) AND `-Atmos-` at fixture ID `420`. Because they share the same fixture type, a Global Dimmer preset for FT2 could affect BOTH CO2 and atmosphere. Therefore the agent must NOT create generic FT2 global intensity presets (Full / 75 / 50) until intent is split by layer (`--Co2(2x)` vs `~Atmos~`) or by fixture ID (911 vs 420).

```text
FT2 Dimmer 00:
- Do not build global dimmer base by fixture type.
- Treat CO2 as SFX / safety-critical.
- Treat Atmos as haze/atmosphere.
- Use Selective or group-scoped presets only after operator approval.
- Default safe preset: Off only.
```

## FT7 / FT8 — laser bars (safety hold)

FT7 `7 LASER BARS - Invert 26CH` (FID 1001) and FT8 `8 LASER BARS 26CH` (FIDs 1002–1009) are laser/SFX fixture types on layer `--M.Laser-BAR`. Build ONLY safe base presets (blackout/off/color base) AFTER attribute discovery and operator approval. Do NOT create unsafe laser-output presets blind. Keep FT7 and FT8 separate (inverted vs standard).

## Summary table

| Fixture type | Status | Allowed now |
| --- | --- | --- |
| FT2 CO2/Atmos | Safety hold | Off only; selective/group-scoped after operator approval |
| FT7 Laser Bars Invert | Safety hold | safe blackout/off/color base only after approval |
| FT8 Laser Bars | Safety hold | same as FT7 |
