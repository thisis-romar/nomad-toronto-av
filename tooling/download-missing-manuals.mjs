#!/usr/bin/env node
/**
 * download-missing-manuals.mjs
 * Uses Playwright (from claude-conversation-reader) to download:
 *   1. Pioneer CDJ-3000 instruction manual (AlphaTheta JS-rendered download page)
 *   2. Pioneer DJM-V10 instruction manual (same)
 *   3. Turbosound Athens TCS-AN Series QSG (Music Tribe CDN — DNS issue workaround)
 *
 * Run from nomad-toronto-av root:
 *   node --experimental-vm-modules scripts/download-missing-manuals.mjs
 */

import { chromium } from 'C:/Users/romar/projects/claude-conversation-reader/node_modules/playwright/index.js';
import { createWriteStream, mkdirSync, existsSync, renameSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { pipeline } from 'node:stream/promises';
import { Readable } from 'node:stream';
import os from 'node:os';

const ROOT = resolve(import.meta.dirname, '..');
const MANUALS = join(ROOT, '02-equipment-manuals');
const DJ_GEAR = join(MANUALS, 'dj-gear');
const SPEAKERS = join(MANUALS, 'speakers');

mkdirSync(DJ_GEAR, { recursive: true });

// ── Targets ───────────────────────────────────────────────────────────────────

const ALPHATHETA_TARGETS = [
  {
    url: 'https://downloads.support.alphatheta.com/manuals/CDJ_3000_DRI1586A_manual/',
    label: 'Pioneer CDJ-3000 manual EN',
    dest: join(DJ_GEAR, 'Pioneer_CDJ-3000_manual.pdf'),
    // fallback: look for attachment matching "CDJ" + "manual" + "EN"
    matchKeywords: ['CDJ-3000', 'manual', 'EN', 'instruction'],
  },
  {
    url: 'https://downloads.support.alphatheta.com/manuals/DJM_V10_DRI1643C_manual/',
    label: 'Pioneer DJM-V10 manual EN',
    dest: join(DJ_GEAR, 'Pioneer_DJM-V10_manual.pdf'),
    matchKeywords: ['DJM-V10', 'manual', 'EN', 'instruction'],
  },
];

const TURBOSOUND_URL =
  'https://mediadl.musictribe.com/media/PLM/data/docs/P0B71/QSG_TS_P0B48_TCS-AN-Series_A4_WW.pdf';
const TURBOSOUND_DEST = join(SPEAKERS, 'Turbosound-Athens-TCS-AN-Series-QSG.pdf');

// ── Helpers ───────────────────────────────────────────────────────────────────

async function downloadBuffer(url, cookies = []) {
  const headers = {
    'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    Accept: 'application/pdf,*/*',
  };
  if (cookies.length) {
    headers['Cookie'] = cookies.map((c) => `${c.name}=${c.value}`).join('; ');
  }
  const res = await fetch(url, { headers });
  if (!res.ok) throw new Error(`HTTP ${res.status} from ${url}`);
  const ct = res.headers.get('content-type') || '';
  if (!ct.includes('pdf') && !ct.includes('octet-stream')) {
    throw new Error(`Non-PDF content-type: ${ct}`);
  }
  return Buffer.from(await res.arrayBuffer());
}

async function saveBuffer(buf, dest) {
  const { writeFileSync } = await import('node:fs');
  writeFileSync(dest, buf);
  const kb = Math.round(buf.length / 1024);
  console.log(`  ✓ Saved ${kb} KB → ${dest}`);
}

// ── AlphaTheta download page scraper ─────────────────────────────────────────

async function downloadAlphatheta(browser, target) {
  console.log(`\n── ${target.label} ──`);
  if (existsSync(target.dest)) {
    console.log(`  Already exists — skipping`);
    return;
  }

  const context = await browser.newContext({
    userAgent:
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    acceptDownloads: true,
  });

  const page = await context.newPage();

  try {
    console.log(`  Loading: ${target.url}`);
    await page.goto(target.url, { waitUntil: 'networkidle', timeout: 30_000 });

    // Wait for any download links to appear (rendered by JS)
    await page.waitForTimeout(2000);

    // Look for <a> tags pointing to PDF files
    const links = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('a[href]'))
        .map((a) => ({ href: a.href, text: a.textContent?.trim() || '' }))
        .filter((l) => l.href.toLowerCase().includes('.pdf') || l.text.toLowerCase().includes('pdf'));
    });

    console.log(`  Found ${links.length} PDF link(s):`);
    links.forEach((l) => console.log(`    ${l.text} → ${l.href}`));

    // Find the English instruction manual link
    const manual = links.find((l) => {
      const combined = (l.href + ' ' + l.text).toLowerCase();
      return (
        combined.includes('instruction') ||
        combined.includes('_en') ||
        combined.includes('-en') ||
        (combined.includes('manual') && !combined.includes('quick'))
      );
    }) || links[0];

    if (!manual) {
      // Try extracting from page JSON data (Next.js __NEXT_DATA__)
      const nextData = await page.evaluate(() => {
        const el = document.getElementById('__NEXT_DATA__');
        return el ? el.textContent : null;
      });
      if (nextData) {
        const data = JSON.parse(nextData);
        const json = JSON.stringify(data);
        const pdfMatch = json.match(/https?:[^"]*\.pdf[^"]*/);
        if (pdfMatch) {
          console.log(`  Found PDF URL in __NEXT_DATA__: ${pdfMatch[0]}`);
          const buf = await downloadBuffer(pdfMatch[0]);
          await saveBuffer(buf, target.dest);
          return;
        }
      }
      throw new Error('No PDF link found on page');
    }

    console.log(`  Downloading: ${manual.href}`);
    const buf = await downloadBuffer(manual.href);
    await saveBuffer(buf, target.dest);

  } catch (err) {
    console.error(`  ✗ Failed: ${err.message}`);

    // Take a screenshot for debugging
    const shot = join(os.homedir(), `.ccr/download-debug-${Date.now()}.png`);
    mkdirSync(join(os.homedir(), '.ccr'), { recursive: true });
    await page.screenshot({ path: shot, fullPage: true }).catch(() => {});
    console.error(`  Screenshot saved: ${shot}`);
  } finally {
    await context.close();
  }
}

// ── Turbosound — try browser fetch via Playwright (bypasses local DNS) ────────

async function downloadTurbosound(browser) {
  console.log(`\n── Turbosound Athens TCS-AN QSG ──`);
  if (existsSync(TURBOSOUND_DEST)) {
    console.log(`  Already exists — skipping`);
    return;
  }

  const context = await browser.newContext({
    userAgent:
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    acceptDownloads: true,
  });
  const page = await context.newPage();

  try {
    console.log(`  Attempting: ${TURBOSOUND_URL}`);

    // Use Playwright's network interception to capture the PDF response
    let pdfBuffer = null;

    const [download] = await Promise.all([
      page.waitForEvent('download', { timeout: 20_000 }).catch(() => null),
      page.goto(TURBOSOUND_URL, { waitUntil: 'commit', timeout: 20_000 }).catch(() => {}),
    ]);

    if (download) {
      const path = await download.path();
      if (path) {
        const { copyFileSync } = await import('node:fs');
        copyFileSync(path, TURBOSOUND_DEST);
        console.log(`  ✓ Saved via download → ${TURBOSOUND_DEST}`);
        return;
      }
    }

    // Try fetching via Playwright's request context (uses browser's network stack, bypasses Node DNS)
    const response = await context.request.get(TURBOSOUND_URL, {
      timeout: 20_000,
    });

    if (response.ok()) {
      const ct = response.headers()['content-type'] || '';
      if (ct.includes('pdf') || ct.includes('octet-stream')) {
        pdfBuffer = await response.body();
        await saveBuffer(pdfBuffer, TURBOSOUND_DEST);
        return;
      }
      console.error(`  Non-PDF content-type: ${ct}`);
    } else {
      console.error(`  HTTP ${response.status()}`);
    }

  } catch (err) {
    console.error(`  ✗ Failed: ${err.message}`);
  } finally {
    await context.close();
  }
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  console.log('Starting browser (headed)...');
  const browser = await chromium.launch({
    headless: false,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--window-size=1280,900',
    ],
  });

  try {
    for (const target of ALPHATHETA_TARGETS) {
      await downloadAlphatheta(browser, target);
    }
    await downloadTurbosound(browser);
  } finally {
    await browser.close();
  }

  console.log('\nDone.');
}

main().catch((err) => {
  console.error('Fatal:', err);
  process.exit(1);
});
