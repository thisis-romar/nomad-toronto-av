// sync-content.mjs — copies the AUDIENCE-FACING subset of @nomad/content-audio into the
// portal's Starlight docs tree. The content package remains the single source of truth; the
// files written here are GENERATED (gitignored) and regenerated on every dev/build run.
//
// Runs as the `sync-content` npm script (invoked by `dev`, `build`, and `lint`).
import { mkdir, readFile, writeFile, rm, copyFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const PORTAL = resolve(__dirname, "..");
const AUDIO = resolve(PORTAL, "../../packages/content-audio");
const DOCS_OUT = join(PORTAL, "src/content/docs/audio");
const DIAGRAMS_OUT = join(PORTAL, "public/diagrams");

/** Audience-facing pages to expose, in sidebar order. Raw archive (manual PDFs,
 *  full source spec) is intentionally NOT surfaced. */
const PAGES = [
  { src: "README.md", dest: "operations.md", title: "Operations & Status", order: 1, desc: "Power-up / power-down sequences, the system status dashboard, and quick links." },
  { src: "07-tech-pack/system-overview.md", dest: "system-overview.md", title: "System Overview", order: 2, desc: "One-page summary of the audio system." },
  { src: "07-tech-pack/available-rider.md", dest: "available-rider.md", title: "Available Rider", order: 3, desc: "Technical rider for visiting artists and DJs." },
  { src: "07-tech-pack/emergency-procedures.md", dest: "emergency-procedures.md", title: "Emergency Procedures", order: 4, desc: "Fault response and shutdown procedures." },
  { src: "07-tech-pack/cable-schedule.md", dest: "cable-schedule.md", title: "Cable Schedule", order: 5, desc: "Complete patch / cable schedule." },
  { src: "06-reference-docs/firmware-changelog.md", dest: "firmware-changelog.md", title: "Firmware Changelog", order: 6, desc: "Equipment firmware versions and update status." },
];

const DIAGRAMS = ["signal-flow.svg", "rack-elevation.svg", "speaker-zone-map.svg"];

/** Rewrite repo-relative links to their portal routes (or to a diagram asset). */
const LINK_REWRITES = [
  [/07-tech-pack\/system-overview\.md/g, "/audio/system-overview"],
  [/07-tech-pack\/available-rider\.md/g, "/audio/available-rider"],
  [/07-tech-pack\/emergency-procedures\.md/g, "/audio/emergency-procedures"],
  [/07-tech-pack\/cable-schedule\.md/g, "/audio/cable-schedule"],
  [/06-reference-docs\/firmware-changelog\.md/g, "/audio/firmware-changelog"],
  [/01-source-documents\/nomad-system-spec-v2\.md/g, "/audio/system-overview"],
  [/07-tech-pack\/(signal-flow|rack-elevation|speaker-zone-map)\.svg/g, "/diagrams/$1.svg"],
];

const yamlEscape = (s) => String(s).replace(/"/g, '\\"');

function transform(raw, page) {
  let body = raw.replace(/\r\n/g, "\n");
  // Drop a leading top-level H1 — Starlight renders the frontmatter title as the page H1.
  body = body.replace(/^﻿?#\s+.*\n+/, "");
  for (const [re, to] of LINK_REWRITES) body = body.replace(re, to);
  const fm =
    `---\n` +
    `title: "${yamlEscape(page.title)}"\n` +
    `description: "${yamlEscape(page.desc)}"\n` +
    `sidebar:\n  order: ${page.order}\n` +
    `---\n\n`;
  return fm + body;
}

async function main() {
  if (!existsSync(AUDIO)) {
    console.error(`[sync-content] content package not found at ${AUDIO}`);
    process.exit(1);
  }
  await rm(DOCS_OUT, { recursive: true, force: true });
  await mkdir(DOCS_OUT, { recursive: true });
  await mkdir(DIAGRAMS_OUT, { recursive: true });

  let docs = 0;
  for (const page of PAGES) {
    const srcPath = join(AUDIO, page.src);
    if (!existsSync(srcPath)) {
      console.warn(`[sync-content] WARN missing source: ${page.src}`);
      continue;
    }
    await writeFile(join(DOCS_OUT, page.dest), transform(await readFile(srcPath, "utf8"), page), "utf8");
    docs++;
  }

  let svgs = 0;
  for (const svg of DIAGRAMS) {
    const srcPath = join(AUDIO, "07-tech-pack", svg);
    if (existsSync(srcPath)) {
      await copyFile(srcPath, join(DIAGRAMS_OUT, svg));
      svgs++;
    } else {
      console.warn(`[sync-content] WARN missing diagram: ${svg}`);
    }
  }

  console.log(`[sync-content] synced ${docs} docs + ${svgs} diagrams from @nomad/content-audio`);
}

main().catch((err) => {
  console.error("[sync-content] failed:", err);
  process.exit(1);
});
