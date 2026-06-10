# @nomad/portal — Stakeholder Portal

Gated, mobile-first web portal that gives non-GitHub NOMAD stakeholders (ownership, bar/floor leads)
a friendly view of the venue's operational documentation. Built with **Astro + Starlight**, hosted
free on **Cloudflare Pages**, with auth handled by **Cloudflare Pages Functions** at the edge.

> Audience of this README: integrating engineers / ops (SOP §6 "Internal Service").

## How it works

- **Content** is pulled from [`@nomad/content-audio`](../../packages/content-audio) at build time by
  `scripts/sync-content.mjs` → `src/content/docs/audio/` (generated, gitignored). The content package
  stays the single source of truth — edit docs there, not here.
- **Auth** is an edge gate in [`functions/`](./functions):
  - `functions/_middleware.ts` runs on every request. No valid session cookie ⇒ the inline login page
    (for navigations) or `401` (for `/api/*`). Nothing behind the gate is served while logged out.
  - `functions/api/login.ts` checks the identifier against `ALLOWLIST` **and** the shared password
    against `SHARED_PASSWORD`, then issues an HMAC-signed, HttpOnly, Secure cookie. The password is
    verified on the edge and is **never** shipped to the browser.
  - `functions/api/logout.ts` clears the cookie.
  - `functions/_lib/session.ts` — cookie signing/verification + allowlist/normalization helpers.

Stakeholders sign in with their **email or WhatsApp number** (on the allowlist) plus the shared
password.

## Environment variables (dictionary)

| Name | Where | Purpose |
|------|-------|---------|
| `SHARED_PASSWORD` | CF dashboard / `.dev.vars` | The one password all stakeholders enter (`nomad2026`). |
| `SESSION_SECRET` | CF dashboard / `.dev.vars` | Random key used to sign session cookies. Rotating it logs everyone out. |
| `ALLOWLIST` | CF dashboard / `.dev.vars` | Comma-separated emails / E.164 numbers permitted to sign in. |

These are **never committed**. Local dev reads `.dev.vars` (gitignored); see `.dev.vars.example`.

## Local development

```bash
pnpm install                      # from repo root
cp apps/portal/.dev.vars.example apps/portal/.dev.vars   # then edit real values

# Astro dev (content + UI only, no auth layer):
pnpm --filter @nomad/portal dev

# Full stack incl. the edge auth (recommended for testing login):
pnpm --filter @nomad/portal build
pnpm --filter @nomad/portal pages:dev      # wrangler pages dev ./dist
```

Verify: `/` redirects to the login screen → allowlisted identifier + `nomad2026` → docs load;
wrong password or off-list identifier → rejected; **Log out** clears access.

## Deploy (Cloudflare Pages)

Connect the **private mirror** repo to a Cloudflare Pages project:

- **Build command:** `pnpm --filter @nomad/portal build`
- **Build output directory:** `apps/portal/dist`
- **Root directory:** repo root (monorepo)
- **Env vars (Production + Preview):** `SHARED_PASSWORD`, `SESSION_SECRET`, `ALLOWLIST`

Serves on a free `*.pages.dev` URL.

### Upgrade path

To switch to email one-time-codes later, front the project with **Cloudflare Access (Zero Trust)**
(free ≤50 users). The allowlist stays the single source of truth — no app rewrite.
