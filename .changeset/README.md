# Changesets

This folder holds **intent-to-release** records for the monorepo, per EMBLEM-NLP SOP §2.1.2
(Independent semver).

When you make a change worth releasing, run:

```bash
pnpm changeset
```

Select the affected package(s) (`@nomad/content-audio`, `@nomad/portal`, …), the bump type
(major/minor/patch), and write a one-line summary. Commit the generated markdown file alongside your
code. On merge, CI runs `changeset version` to apply bumps and update changelogs.

See the [Changesets docs](https://github.com/changesets/changesets) for details.
