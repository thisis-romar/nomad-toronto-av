# NOMAD Toronto AV — Monorepo

Repository for the **NOMAD Toronto** (725 Queen St E) AV system: discipline documentation plus the
**stakeholder portal** that makes it visible to non-GitHub venue management. Structured per the
EMBLEM-NLP Repository Architecture SOP v1.2.0 — Monorepo / Feature-Based (see
[`docs/decisions/ADR-0001`](docs/decisions/ADR-0001-monorepo-feature-based.md)).

> Audience of this README: onboarding engineers (SOP §6 "Monorepo Root"). The venue-facing operations
> guide now lives in [`packages/content-audio/README.md`](packages/content-audio/README.md) and is
> surfaced to stakeholders through the portal.

## Layout & dependency graph

```
nomad-toronto-av/
├── apps/
│   └── portal/            @nomad/portal      → Astro + Starlight site, Cloudflare Pages, edge auth
├── packages/
│   ├── content-audio/     @nomad/content-audio    (source of truth: audio docs/diagrams/manuals)
│   ├── content-lighting/  @nomad/content-lighting  (placeholder — lighting discipline, incoming)
│   └── tsconfig/          @nomad/tsconfig          (shared TS base config)
├── tooling/               Node/Python utilities (GitHub Projects, image-gen, PDF build)
└── docs/decisions/        Architecture Decision Records
```

Dependencies: `@nomad/portal` consumes `@nomad/content-audio` **at build time** (copied by
`apps/portal/scripts/sync-content.mjs`), and `@nomad/tsconfig` as a dev dependency. The content
packages have no build step — they are the source of truth that the portal renders.

## Global setup

```bash
corepack enable          # uses the pinned pnpm (packageManager field)
pnpm install             # installs all workspaces
```

For portal auth secrets in local dev, copy the template (gitignored target):

```bash
cp apps/portal/.dev.vars.example apps/portal/.dev.vars   # then edit real values
```

## Task orchestration (Turborepo)

| Command | What it does |
|---------|--------------|
| `pnpm build` | `turbo run build` across the workspace (portal syncs content, then `astro build`). |
| `pnpm dev` | `turbo run dev` (portal at `localhost:4321`; content-only, no auth layer). |
| `pnpm lint` | `turbo run lint` (`astro check` type gate). |
| `pnpm depcruise` | SOP §4.2.1 architecture validation (no-circular, barrel imports). |
| `pnpm changeset` | Record an intent-to-release (SOP §2.1.2, Independent semver). |

Portal-specific (run the real edge auth locally):

```bash
pnpm --filter @nomad/portal build
pnpm --filter @nomad/portal pages:dev     # wrangler pages dev ./dist  → localhost:8788
```

### Clearing caches

```bash
rm -rf .turbo apps/*/.turbo                  # Turborepo cache
rm -rf apps/portal/dist apps/portal/.astro   # Astro build artifacts
rm -rf apps/portal/.wrangler                 # Wrangler/Miniflare local state
pnpm store prune                             # pnpm global content-addressable store
```

## Repo topology (public + private mirror)

Development happens here on the public `thisis-romar/nomad-toronto-av`. A
[mirror workflow](.github/workflows/mirror-to-private.yml) pushes every ref to a **private** repo
(`emblem-nlp/nomad-toronto-av`) that **Cloudflare Pages deploys from**. Stakeholder access is enforced
by the portal's login gate (email/WhatsApp-number allowlist + shared password), independent of repo
visibility. No secrets live in either repo — they are set in the Cloudflare dashboard.

See [`apps/portal/README.md`](apps/portal/README.md) for the portal architecture and deploy steps.

## CI

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs affected-based build + lint (SOP §3.1) and
the `depcruise` architecture gate (SOP §4.2.1) on every PR. `project-sync.yml` / `status-update.yml`
keep the GitHub Project board in sync.
