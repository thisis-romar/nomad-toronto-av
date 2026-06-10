#!/usr/bin/env node
/**
 * gh-project-views.mjs
 * Creates board views, active-work table, and roadmap in the
 * Nomad Toronto AV GitHub Project (#5) via Playwright browser automation.
 *
 * GitHub Projects API does not expose createProjectV2View — UI only.
 *
 * Usage:
 *   node scripts/gh-project-views.mjs
 *
 * Requires: Chrome installed, already logged into github.com in Chrome profile
 */

import pkg from 'file:///C:/Users/romar/projects/claude-conversation-reader/node_modules/playwright/index.js';
const { chromium } = pkg;

const PROJECT_URL = 'https://github.com/users/thisis-romar/projects/5';

const VIEWS = [
  { name: 'All Issues',   layout: 'table',   groupBy: null,    filter: null },
  { name: 'Board',        layout: 'board',   groupBy: 'Status', filter: null },
  { name: 'By Owner',     layout: 'board',   groupBy: 'Owner',  filter: null },
  { name: 'Active Work',  layout: 'table',   groupBy: null,    filter: 'status:in-progress' },
  { name: 'Roadmap',      layout: 'roadmap', groupBy: null,    filter: null },
];

async function wait(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function tryClick(page, selectors, timeout = 4000) {
  for (const sel of [].concat(selectors)) {
    try {
      await page.locator(sel).first().click({ timeout });
      return sel;
    } catch { /* try next */ }
  }
  return null;
}

async function saveViewName(page, name) {
  // After a new view tab opens, it's in edit mode — type the name and press Enter
  try {
    const input = page.locator('input[aria-label="Rename view"], input[placeholder*="view name"], input[data-testid*="view"]').first();
    await input.waitFor({ timeout: 4000 });
    await input.selectAll?.();
    await input.fill(name);
    await page.keyboard.press('Enter');
    await wait(600);
    return true;
  } catch {
    // Fallback: just press Enter without renaming — we'll rename later
    await page.keyboard.press('Escape');
    return false;
  }
}

async function createView(page, viewDef, isFirst) {
  console.log(`\n→ Creating view: "${viewDef.name}" (${viewDef.layout})`);

  if (isFirst) {
    // Rename "View 1" instead of creating a new one
    try {
      const tab = page.locator('[data-testid="project-view-tab"], .js-project-view-tab, [role="tab"]').first();
      await tab.dblclick({ timeout: 3000 });
      await wait(400);
      const input = page.locator('input').filter({ hasText: '' }).first();
      await input.selectAll?.();
      await input.fill(viewDef.name);
      await page.keyboard.press('Enter');
      await wait(800);
      console.log(`  ✓ Renamed "View 1" → "${viewDef.name}"`);
      return;
    } catch {
      console.log('  Could not rename View 1 via dblclick — will create new view');
    }
  }

  // Click the "+ New view" or "+" button
  const newViewClicked = await tryClick(page, [
    'button[data-testid="new-view-button"]',
    'button[aria-label="New view"]',
    'button[aria-label*="new view" i]',
    '[data-testid="add-view-button"]',
    'button:has-text("New view")',
    'a:has-text("New view")',
    'button[aria-label="+"]',
  ], 5000);

  if (!newViewClicked) {
    const shot = `C:/tmp/gh-project-debug-newview-${Date.now()}.png`;
    await page.screenshot({ path: shot });
    console.error(`  ✗ Could not find "New view" button. Screenshot: ${shot}`);
    return;
  }
  await wait(800);

  // Select layout from the dropdown/dialog that appears
  const layoutMap = {
    table:   ['Table', 'table layout', 'table'],
    board:   ['Board', 'board layout', 'board'],
    roadmap: ['Roadmap', 'roadmap layout', 'roadmap'],
  };

  for (const label of layoutMap[viewDef.layout]) {
    const clicked = await tryClick(page, [
      `[role="option"]:has-text("${label}")`,
      `[role="menuitem"]:has-text("${label}")`,
      `button:has-text("${label}")`,
      `li:has-text("${label}")`,
    ], 2000);
    if (clicked) { await wait(600); break; }
  }

  // Name the new view
  await saveViewName(page, viewDef.name);
  await wait(1000);

  // Configure group-by if needed
  if (viewDef.groupBy) {
    await configureGroupBy(page, viewDef.groupBy);
  }

  // Configure filter if needed
  if (viewDef.filter) {
    await configureFilter(page, viewDef.filter);
  }

  console.log(`  ✓ View "${viewDef.name}" created`);
}

async function configureGroupBy(page, fieldName) {
  console.log(`    Setting group-by: ${fieldName}`);
  // Open view settings / group-by menu
  const settingsClicked = await tryClick(page, [
    'button[aria-label*="group" i]',
    'button[aria-label*="Group by" i]',
    '[data-testid="view-options-button"]',
    'button:has-text("Group by")',
  ], 3000);

  if (!settingsClicked) {
    // Try through the "..." view options menu
    await tryClick(page, [
      'button[aria-label*="options" i]',
      'button[aria-label*="settings" i]',
      '[data-testid="view-menu"]',
    ], 2000);
    await wait(400);
    await tryClick(page, ['button:has-text("Group by")', '[role="menuitem"]:has-text("Group by")'], 2000);
  }
  await wait(600);

  // Pick the field
  const fieldClicked = await tryClick(page, [
    `[role="option"]:has-text("${fieldName}")`,
    `[role="menuitem"]:has-text("${fieldName}")`,
    `button:has-text("${fieldName}")`,
    `li:has-text("${fieldName}")`,
  ], 3000);

  if (fieldClicked) {
    await wait(600);
    // Close dropdown
    await page.keyboard.press('Escape');
    await wait(400);
  }
}

async function configureFilter(page, filter) {
  console.log(`    Setting filter: ${filter}`);
  // Click the filter bar / search
  const filterClicked = await tryClick(page, [
    '[data-testid="filter-bar"]',
    'input[placeholder*="Filter"]',
    'input[aria-label*="filter" i]',
    'button:has-text("Filter")',
  ], 3000);
  if (filterClicked) {
    await page.keyboard.type(filter);
    await page.keyboard.press('Enter');
    await wait(600);
  }
}

const CHROME_PROFILE = 'C:/Users/romar/AppData/Local/Google/Chrome/User Data';

async function run() {
  // Use persistent context with existing Chrome profile (already logged into GitHub)
  const context = await chromium.launchPersistentContext(CHROME_PROFILE, {
    channel: 'chrome',
    headless: false,
    args: [
      '--window-size=1400,900',
      '--disable-blink-features=AutomationControlled',
      '--profile-directory=Default',
    ],
  });
  const page = await context.newPage();

  try {
    console.log('Opening GitHub Project (using saved Chrome session)...');
    await page.goto(PROJECT_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await wait(3000);

    // Verify we are logged in
    const url = page.url();
    if (url.includes('/login') || url.includes('404')) {
      console.error('Not logged into GitHub — open Chrome, log in, then rerun.');
      process.exit(1);
    }

    console.log('Logged in ✓ — waiting for project to load...');
    await wait(6000);

    // Take screenshot to see current state
    await page.screenshot({ path: 'C:/tmp/gh-project-start.png' });
    console.log('Start state: C:/tmp/gh-project-start.png');

    // Process each view definition
    for (let i = 0; i < VIEWS.length; i++) {
      await createView(page, VIEWS[i], i === 0);
      await wait(1500);
    }

    // Final screenshot
    await page.screenshot({ path: 'C:/tmp/gh-project-final.png', fullPage: false });
    console.log('\n✓ Done. Final state: C:/tmp/gh-project-final.png');
    console.log(`  Project: ${PROJECT_URL}`);

  } finally {
    await wait(2000);
    await context.close();
  }
}

run().catch(err => {
  console.error('\nFatal:', err.message);
  process.exit(1);
});
