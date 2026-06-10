// Dependency-Cruiser config — enforces EMBLEM-NLP SOP §4.2.1 boundary rules.
// Validated in CI: `pnpm depcruise`.
/** @type {import('dependency-cruiser').IConfiguration} */
module.exports = {
  forbidden: [
    {
      name: "no-circular",
      comment:
        "SOP §4.2.1(3): cyclic cross-feature references are prohibited. Break the cycle " +
        "(e.g. extract a shared primitive) rather than importing back and forth.",
      severity: "error",
      from: {},
      to: { circular: true },
    },
    {
      name: "no-deep-feature-import",
      comment:
        "SOP §4.2.1(2): import a feature through its index barrel, not its internals. " +
        "Use `import { X } from '../<feature>'`, never `'../<feature>/components/internal/X'`.",
      severity: "error",
      from: { path: "(apps|packages)/[^/]+/src/features/([^/]+)/" },
      to: {
        path: "(apps|packages)/[^/]+/src/features/([^/]+)/.+",
        pathNot: [
          "(apps|packages)/[^/]+/src/features/$2/index\\.(ts|tsx|js|mjs)$",
          "(apps|packages)/[^/]+/src/features/$2/",
        ],
      },
    },
    {
      name: "no-orphans",
      comment: "Unreferenced modules usually indicate dead code or a missing barrel export.",
      severity: "warn",
      from: {
        orphan: true,
        pathNot: [
          "\\.d\\.ts$",
          "(^|/)(\\.[^/]+\\.(js|cjs|mjs|ts))$",
          "\\.(config|setup)\\.(js|cjs|mjs|ts)$",
          "(^|/)astro\\.config\\.",
        ],
      },
      to: {},
    },
  ],
  options: {
    doNotFollow: { path: "node_modules" },
    exclude: { path: "(^|/)(dist|\\.astro|\\.wrangler)/" },
    tsPreCompilationDeps: true,
    enhancedResolveOptions: {
      exportsFields: ["exports"],
      conditionNames: ["import", "require", "node", "default"],
    },
  },
};
