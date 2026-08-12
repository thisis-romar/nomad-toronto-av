# Canonical site-survey source photos

Binary site photographs are intentionally **not duplicated by this PR**. The visual-audit tooling expects the canonical source image to be staged locally at the path recorded in the audit manifest.

For `main-room-2026-08-12-001`:

- expected local path: `09-site-survey/photos/2026-08-12-main-room-source.jpg`
- dimensions: `1536 × 1152`
- SHA-256: `0075236726c7d720c5c641211e6cc5580e15662227cebaf1cb9587ada11bfa31`

`python3 scripts/photo-audit-loop.py` hard-fails if either the dimensions or fingerprint differ. This prevents annotations authored against a resized screenshot or display derivative from silently entering the evidence manifest.
