# NOMAD Toronto — Lighting

This package holds the **lighting discipline** documentation, mirroring the structure of
[`@nomad/content-audio`](../content-audio/README.md): a system spec, equipment manuals, wiring/DMX
diagrams, and an audience-facing tech pack.

It exists so the monorepo's feature-based layout (EMBLEM-NLP SOP §4.2) is in place — adding the
discipline is a matter of populating this folder, not restructuring the repo.

## grandMA2 preset workstream (`nomad22-may16/`)

The first lighting work is auditing the **grandMA2** console showfile `nomad22-may16` and designing a
safe global-preset base. This folder is the **version-controlled source of truth** the MA2 harness
reads from:

| File | Purpose |
|------|---------|
| [`nomad22-may16/fixture-inventory.md`](nomad22-may16/fixture-inventory.md) | Fixture/layer export facts — types, IDs, layers, subfixtures. **Not** a preset export. |
| [`nomad22-may16/safety-findings.md`](nomad22-may16/safety-findings.md) | FT2 CO2/Atmos collision (do not global-dim) + FT7/FT8 laser hold. |
| [`nomad22-may16/preset-strategy.md`](nomad22-may16/preset-strategy.md) | Build order + per-fixture-type coverage plan. |
| [`nomad22-may16/prompt-patch.md`](nomad22-may16/prompt-patch.md) | Verbatim `SHOWFILE-SPECIFIC CONTEXT` block to inject into the MA2 harness prompt. |
| [`nomad22-may16/audit-task.md`](nomad22-may16/audit-task.md) | Ready-to-paste **audit-only** harness run (read-only; no console writes). |

> ⚠️ **Audit before build.** The `nomad22-may16` XML is a fixture/layer export — it contains **no
> Preset pool objects**. Preset pools 1–9 and FT attributes must be audited live in the MA2 harness
> (those console tools — `list_preset_pool`, `discover_fixture_type_attributes`, `export_objects` —
> are **not** part of this repo session) before any preset is claimed audited or built.

## Planned structure (to match `content-audio`)

```
content-lighting/
├── 01-source-documents/      # lighting system spec
├── 02-equipment-manuals/     # fixture / console / DMX node manuals
├── 04-wiring-diagrams/       # DMX universes, power, data topology
├── 07-tech-pack/             # audience-facing deliverables (overview, rider, procedures)
└── README.md
```

## Surfacing in the stakeholder portal

Once populated, add the audience-facing lighting docs to the portal by extending
`apps/portal/scripts/sync-content.mjs` (a new `lighting/` sidebar group) — no auth or hosting
changes required.

> Status: **active** — grandMA2 preset-audit workstream started (`nomad22-may16/`); discipline
> docs (spec, manuals, diagrams, tech pack) still to be authored.
