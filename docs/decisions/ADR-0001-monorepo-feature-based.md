# ADR-0001 — Monorepo (Feature-Based) with documented deviations

- **Status:** Accepted
- **Date:** 2026-06-10
- **Deciders:** Emblem Projects Inc. (technical lead) for client delivery repo `nomad-toronto-av`
- **Governs:** Macro/micro architecture of this repository
- **SOP reference:** EMBLEM-NLP-SOP-001 (Repository Architecture & Code Topology) v1.2.0, §7 + §8

## Context

`nomad-toronto-av` began as a single-discipline (audio) documentation archive with numbered content
folders and a handful of Node/Python automation scripts. Two forces now require a structural change:

1. **A stakeholder portal** (a real web application — Astro/Starlight + Cloudflare Pages Functions)
   must live alongside the documentation.
2. **A second discipline, lighting,** is planned. The repo must hold audio + lighting + the portal
   without another reorganization later.

Per SOP §8 Phase 1, we select a target context from the §7 Architectural Decision Matrix and record
the decision here. The repo now matches the **"Mid-to-Large Web / Product Team"** row (a product app
plus shared, versioned content domains).

## Decision

| Axis | Choice | SOP basis |
|------|--------|-----------|
| Macro pattern | **Monorepo (Pattern A)** — `apps/` + `packages/` | §2.1, §7 |
| Micro pattern | **Feature-Based** — domains as packages (`content-audio`, `content-lighting`) | §4.2, §7 |
| Build orchestration | **Turborepo + pnpm workspaces** | §2.1.1 |
| Versioning | **Independent semver via Changesets** | §2.1.2 |
| Boundary enforcement | **Dependency-Cruiser** (no-circular, barrel imports) | §4.2.1 |
| Dependency sync | **Renovate** (`config:best-practices`) | §2.2.1, §8 Ph2.5 |
| CI topology | **Affected-based** (`turbo run --filter=...[base]`) | §3.1 |

Resulting layout: `apps/portal/`, `packages/content-audio/`, `packages/content-lighting/`,
`packages/tsconfig/`, `tooling/` (former `scripts/`), `docs/decisions/`.

## Deviations from the SOP (required record per §8 Ph4.4)

**D1 — Single monorepo with domain packages, NOT full Hybrid/Polyrepo (§2.3).**
The §7 row "Enterprise Domain Segregation" prescribes Hybrid domain *monorepos* (one repo per domain,
cross-domain via a private npm registry). That is enterprise-scale tooling for two disciplines and a
single app maintained by one team. We instead keep both disciplines as **packages inside one
monorepo**, which preserves the discipline boundary (§4.2) at a fraction of the operational cost.
Re-evaluate if the repo exceeds ~3 disciplines or gains independent deployment cadences.

**D2 — Turborepo despite auxiliary Python tooling (§2.1.1 notes Turborepo = "No polyglot support").**
The repo contains Python utilities (`tooling/build-tech-pack.py`, `tooling/codex-imagegen.py`). These
are **build/authoring tools, not workspace packages or deployable services**, so they are not part of
the Turbo task graph; they are invoked directly (`python tooling/…`). The orchestrated workspace is
pure JS/TS (the portal + content packages), for which Turborepo is the lighter, Cloudflare-friendly
fit. If Python becomes a first-class build target, revisit Nx (the SOP's polyglot option).

## Consequences

- Adding lighting is now **populate `packages/content-lighting/`**, not a restructure.
- `git mv` preserved full history for all migrated content and scripts.
- CI must be affected-based (§3.1) to stay fast as packages grow — see `.github/workflows/ci.yml`.
- Dependency-Cruiser validation (`pnpm depcruise`) is a required status check (§8 Ph4.2).
- A separate concern (not architectural): the repo is mirrored to a **private** repo that hosts the
  portal; see the root README "Repo topology" section.
