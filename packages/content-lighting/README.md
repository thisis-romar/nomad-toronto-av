# NOMAD Toronto — Lighting (placeholder)

This package will hold the **lighting discipline** documentation, mirroring the structure of
[`@nomad/content-audio`](../content-audio/README.md): a system spec, equipment manuals, wiring/DMX
diagrams, and an audience-facing tech pack.

It exists now so the monorepo's feature-based layout (EMBLEM-NLP SOP §4.2) is in place **before**
lighting work begins — adding the discipline is a matter of populating this folder, not restructuring
the repo.

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

> Status: **placeholder** — no lighting documentation has been authored yet.
