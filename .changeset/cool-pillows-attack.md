---
"@nomad/portal": minor
"@nomad/content-audio": minor
---

Restructure into an SOP-conformant Turborepo monorepo (audio + lighting disciplines) and add the
gated stakeholder portal: an Astro + Starlight site on Cloudflare Pages with an edge auth gate
(email/WhatsApp-number allowlist + shared password, HMAC-signed session cookie). Existing audio
documentation moved into `@nomad/content-audio` (history preserved) and is surfaced read-only to
venue management through the portal.
