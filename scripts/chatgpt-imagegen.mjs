#!/usr/bin/env node
/**
 * chatgpt-imagegen.mjs
 * Automates ChatGPT DALL-E image generation via Playwright.
 * Uses your existing Chrome profile (already logged into ChatGPT).
 *
 * Usage:
 *   node scripts/chatgpt-imagegen.mjs \
 *     --source "C:/tmp/djm-rear-preview.png" \
 *     --output "05-speaker-assets/png/pioneer-djm-v10-rear-clean.png" \
 *     --prompt "..."
 *
 * Or use built-in presets:
 *   node scripts/chatgpt-imagegen.mjs --preset djm-v10-rear
 */

import pkg from 'file:///C:/Users/romar/projects/claude-conversation-reader/node_modules/playwright/index.js';
const { chromium } = pkg;
import { writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { resolve, join, dirname } from 'node:path';
import { parseArgs } from 'node:util';
import os from 'node:os';

// ── Chrome profile (inherits your logged-in ChatGPT session) ─────────────────
const CHROME_PROFILE = join(os.homedir(), 'AppData/Local/Google/Chrome/User Data');

// ── Built-in presets ─────────────────────────────────────────────────────────
const PRESETS = {
  'djm-v10-rear': {
    source: 'C:/tmp/djm-rear-preview.png',
    output: '05-speaker-assets/png/pioneer-djm-v10-rear-clean.png',
    prompt: `Generate an image: A clean, high-resolution technical illustration of the rear panel of a Pioneer DJ DJM-V10 mixer. The mixer is shown in a perfectly straight-on, horizontal orientation, centered on a pure white background. Lighting is flat and even, with no shadows or dramatic contrast, resembling a product manual illustration.

The full chassis is visible edge-to-edge, including:
- Pioneer DJ logo on the left
- Power button and AC IN power inlet
- SIGNAL GND terminal
- MULTI I/O, EXT 2, and EXT 1 RETURN RCA sections
- Six input channels labeled CH1 through CH6, each with clearly labeled PHONO and LINE RCA input pairs
- Microphone inputs: MIC 1 (TRS) and MIC 3 (XLR)
- REC OUT and MASTER 2 RCA outputs
- MASTER 1 balanced XLR outputs
- BOOTH outputs (TRS)
- MASTER OUT XLR section
- DIGITAL RCA input/output section
- LINK (RJ-45 Ethernet port)
- MIDI OUT (5-pin DIN)
- Kensington lock slot
- UNBALANCED label under the appropriate RCA section

All original silkscreen labels and port labels are clearly legible and preserved exactly as on the hardware.

IMPORTANT: Remove all annotation overlays. No red boxes, no arrows, no leader lines, no numbers or callouts anywhere. Only the original printed labels on the device remain.

Style: precise, minimal, technical product illustration, similar to a professional user manual or catalog image.`,
  },
};

// ── Selectors (multiple fallbacks for ChatGPT UI changes) ────────────────────
const SEL = {
  // File input (hidden, triggered by attachment button)
  fileInput: 'input[type="file"]',
  // Attachment / upload button
  attachBtn: [
    'button[aria-label*="ttach"]',
    'button[aria-label*="upload"]',
    'button[aria-label*="file"]',
    '[data-testid="composer-speech-button"]',
    'button.composer-btn svg[data-icon="paperclip"]',
    'label[for*="file"]',
    'button:has(svg[data-icon="paperclip"])',
  ],
  // Prompt text area
  promptArea: [
    '#prompt-textarea',
    'div[contenteditable="true"]',
    'textarea[placeholder*="Message"]',
    'div[data-testid="prompt-textarea"]',
  ],
  // Send button
  sendBtn: [
    'button[data-testid="send-button"]',
    'button[aria-label="Send message"]',
    'button[aria-label*="send"]',
    'button:has(svg[data-icon="send"])',
    'button.send-button',
  ],
  // New chat button
  newChat: [
    'button[data-testid="new-conversation-button"]',
    'a[href="/"]',
    'button:has-text("New chat")',
    'nav button:first-child',
  ],
  // Generated image in response
  generatedImg: [
    'img[alt*="generated"]',
    'img[src*="oaidalleapiprodscus"]',
    'img[src*="blob.core.windows"]',
    'img[src*="files.oaiusercontent"]',
    '.group img',
    'article img',
  ],
  // Download button on generated image
  downloadBtn: [
    'button[aria-label*="ownload"]',
    'button[download]',
    'a[download]',
  ],
};

// ── Helpers ───────────────────────────────────────────────────────────────────

async function tryClick(page, selectors, timeout = 5000) {
  for (const sel of [].concat(selectors)) {
    try {
      await page.locator(sel).first().click({ timeout });
      return sel;
    } catch { /* try next */ }
  }
  return null;
}

async function tryLocator(page, selectors, timeout = 5000) {
  for (const sel of [].concat(selectors)) {
    try {
      const loc = page.locator(sel).first();
      await loc.waitFor({ timeout });
      return loc;
    } catch { /* try next */ }
  }
  return null;
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function run({ source, output, prompt }) {
  source = resolve(source);
  output = resolve(output);

  if (!existsSync(source)) {
    console.error(`Source file not found: ${source}`);
    process.exit(1);
  }

  console.log(`Source:  ${source}`);
  console.log(`Output:  ${output}`);
  console.log(`Profile: ${CHROME_PROFILE}`);
  console.log();

  mkdirSync(dirname(output), { recursive: true });

  // Launch a fresh Chrome window — user will need to log into ChatGPT once
  console.log('Launching Chrome (you may need to log into ChatGPT)...');
  const browser = await chromium.launch({
    channel: 'chrome',
    headless: false,
    args: [
      '--window-size=1400,900',
      '--disable-blink-features=AutomationControlled',
      '--no-sandbox',
    ],
  });
  const context = await browser.newContext();

  const page = await context.newPage();

  try {
    // Navigate to ChatGPT
    console.log('Opening chat.openai.com...');
    await page.goto('https://chat.openai.com/', {
      waitUntil: 'domcontentloaded',
      timeout: 30_000,
    });
    await page.waitForTimeout(2000);

    // Always pause for user to confirm they are logged into ChatGPT
    await page.waitForTimeout(1500);
    console.log('');
    console.log('════════════════════════════════════════════');
    console.log('  CHECK the Chrome window that just opened.');
    console.log('  Make sure you are LOGGED INTO ChatGPT.');
    console.log('  If not logged in, click "Log in" and sign in now.');
    console.log('  Then come back here and press ENTER to continue.');
    console.log('════════════════════════════════════════════');
    await new Promise(resolve => {
      process.stdin.resume();
      process.stdin.once('data', () => { process.stdin.pause(); resolve(); });
    });
    await page.waitForTimeout(1000);

    // Start a new chat
    console.log('Starting new chat...');
    const newChatClicked = await tryClick(page, SEL.newChat, 3000);
    if (newChatClicked) {
      await page.waitForTimeout(1000);
    } else {
      // Just navigate directly to a fresh chat
      await page.goto('https://chat.openai.com/', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(2000);
    }

    // Upload the source image
    console.log('Uploading source image...');

    // Try to set file directly on the hidden file input
    const fileInputEl = page.locator(SEL.fileInput).first();
    let uploaded = false;

    try {
      await fileInputEl.waitFor({ timeout: 3000 });
      await fileInputEl.setInputFiles(source);
      uploaded = true;
      console.log('  ✓ File set via hidden input');
    } catch {
      // Click attachment button to reveal file picker
      const attachClicked = await tryClick(page, SEL.attachBtn, 5000);
      if (attachClicked) {
        console.log(`  Attachment button clicked (${attachClicked})`);
        await page.waitForTimeout(500);
        // Now try the file input again
        try {
          const [fileChooser] = await Promise.all([
            page.waitForEvent('filechooser', { timeout: 5000 }),
            page.locator(SEL.attachBtn[0]).click({ timeout: 2000 }).catch(() => {}),
          ]);
          await fileChooser.setFiles(source);
          uploaded = true;
          console.log('  ✓ File set via file chooser');
        } catch {
          // Try direct setInputFiles after click
          try {
            await page.locator(SEL.fileInput).first().setInputFiles(source);
            uploaded = true;
          } catch (e) {
            console.error(`  ✗ Could not upload file: ${e.message}`);
          }
        }
      }
    }

    if (!uploaded) {
      throw new Error('Could not upload source image — ChatGPT UI may have changed');
    }

    // Wait for upload to complete (thumbnail appears)
    await page.waitForTimeout(2000);
    console.log('  Image uploaded, waiting for preview...');
    await page.waitForTimeout(1500);

    // Type the prompt
    console.log('Typing prompt...');
    const promptLoc = await tryLocator(page, SEL.promptArea, 5000);
    if (!promptLoc) throw new Error('Could not find prompt text area');

    await promptLoc.click();
    await page.waitForTimeout(300);

    // Use clipboard paste for the prompt (avoids issues with special chars)
    await page.evaluate((text) => navigator.clipboard.writeText(text), prompt);
    await page.keyboard.press('Control+v');
    await page.waitForTimeout(500);

    // Submit
    console.log('Submitting...');
    const sendClicked = await tryClick(page, SEL.sendBtn, 5000);
    if (!sendClicked) {
      await page.keyboard.press('Enter');
    }

    // Wait for DALL-E to generate (can take 15-45 seconds)
    console.log('Waiting for DALL-E to generate image (up to 90 seconds)...');

    let imgSrc = null;
    const deadline = Date.now() + 90_000;

    while (Date.now() < deadline) {
      await page.waitForTimeout(2000);

      // Look for generated image
      for (const sel of SEL.generatedImg) {
        try {
          const img = page.locator(sel).last();
          const src = await img.getAttribute('src', { timeout: 1000 });
          if (src && src.startsWith('http') && !src.includes('openai.com/assets')) {
            imgSrc = src;
            break;
          }
        } catch { /* keep waiting */ }
      }

      if (imgSrc) {
        console.log(`  ✓ Image found: ${imgSrc.substring(0, 80)}...`);
        break;
      }

      process.stdout.write('.');
    }
    console.log();

    if (!imgSrc) {
      // Take screenshot for debugging
      const shot = `C:/tmp/chatgpt-debug-${Date.now()}.png`;
      await page.screenshot({ path: shot, fullPage: true });
      console.error(`✗ Could not find generated image. Screenshot saved: ${shot}`);
      throw new Error('Generated image not found in page');
    }

    // Download the image
    console.log(`Downloading generated image...`);
    const response = await context.request.get(imgSrc, { timeout: 30_000 });
    if (!response.ok()) throw new Error(`HTTP ${response.status()} downloading image`);

    const imgBuffer = await response.body();
    writeFileSync(output, imgBuffer);
    console.log(`\n✓ Saved: ${output} (${Math.round(imgBuffer.length / 1024)} KB)`);

  } finally {
    await page.waitForTimeout(1000);
    await context.close();
    await browser.close();
  }
}

// ── CLI ───────────────────────────────────────────────────────────────────────

const { values } = parseArgs({
  options: {
    preset: { type: 'string' },
    source: { type: 'string' },
    output: { type: 'string' },
    prompt: { type: 'string' },
  },
  allowPositionals: true,
});

let config;
if (values.preset) {
  config = PRESETS[values.preset];
  if (!config) {
    console.error(`Unknown preset: ${values.preset}`);
    console.error(`Available: ${Object.keys(PRESETS).join(', ')}`);
    process.exit(1);
  }
  console.log(`Using preset: ${values.preset}`);
} else if (values.source && values.output && values.prompt) {
  config = values;
} else {
  console.log('Usage:');
  console.log('  node scripts/chatgpt-imagegen.mjs --preset djm-v10-rear');
  console.log('  node scripts/chatgpt-imagegen.mjs --source <png> --output <png> --prompt "<text>"');
  console.log('\nPresets:', Object.keys(PRESETS).join(', '));
  process.exit(0);
}

run(config).catch((err) => {
  console.error('\nFatal:', err.message);
  process.exit(1);
});
