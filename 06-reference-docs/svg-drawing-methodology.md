# SVG drawing methodology: PNG source → validated SVG

**Purpose:** This document defines the end-to-end workflow for redrawing the nine VOID speaker SVGs from source PNGs. All redrawn SVGs must match the dark-theme aesthetic established in `07-tech-pack/rack-elevation.svg`.

**Applies to:** Every file in `05-speaker-assets/svg/` that is currently a VTracer auto-trace (identified by `<!-- Generator: visioncortex VTracer -->` in the header). As of 2026-04-28, all nine speaker SVGs and both amp SVGs fall into this category — they are monochrome path-dumps unsuitable for use in the tech pack.

---

## 1. Toolchain availability (as of 2026-04-28)

| Tool | Status | Command | Notes |
|---|---|---|---|
| **Node.js** | Unknown — not verified; shell execution restricted | `node --version` | Required for SVGO |
| **SVGO** | Unknown | `npx svgo --version` | SVG optimiser; run after drawing |
| **ImageMagick** | Unknown — not verified; shell execution restricted | `magick --version` | Pixel-diff validator |
| **Browser (Chrome/Edge)** | Available | — | Primary render+screenshot validator |

**To verify locally, run:**
```bash
node --version
npx svgo --version
magick --version
```

If ImageMagick is absent, use the browser screenshot workflow described in §7.

---

## 2. Source PNG format

The source PNGs live in `05-speaker-assets/png/`. Each speaker has four variants:

| Suffix | Contents |
|---|---|
| *(none)* | Marketing/composite photo — skip |
| `-front` | Front elevation with visible panel features |
| `-side` | Side elevation — use for depth context only |
| `-top` | Top-down view — rarely needed |
| `-dims` | Dimensional drawing with mm annotations (primary reference) |

**Always start with `-dims.png`.** This is the manufacturer spec sheet image and carries the accurate width × height × depth values.

### Extracting dimensions via Claude vision

Claude can read PNG files directly. Paste or attach `<speaker>-dims.png` and ask:

```
Read all dimension annotations from this drawing.
Return: width (mm), height (mm), depth (mm), driver diameter(s) (mm),
port dimensions if visible, and any other labelled measurements.
```

Record the values in a comment block at the top of the SVG (see §4 template).

---

## 3. SVG element selection guide

Choose the simplest element that accurately represents the shape.

| Shape | Element | When to use |
|---|---|---|
| Rectangular panel, grille, port slot | `<rect>` | Any axis-aligned rectangle. Add `rx`/`ry` for rounded corners. |
| Driver cone, port circle, LED | `<circle>` | Perfect circles. Use `cx`, `cy`, `r`. |
| Elliptical tweeter horn | `<ellipse>` | Oval shapes. Use `cx`, `cy`, `rx`, `ry`. |
| Straight dimension line, rule | `<line>` | Single straight segment with `x1 y1 x2 y2`. |
| Angled or chamfered edge | `<polygon>` or `<path>` | Multi-point closed shapes that are not rectangles. |
| Curved driver surround, complex grille cutout | `<path>` | Only when `rect`/`circle`/`ellipse` cannot represent it. Use SVG arc commands (`A`) rather than cubic Bézier approximations where possible. |
| Reusable component (e.g. a rigging point repeated 4×) | `<symbol>` + `<use>` | Define once in `<defs>`, instantiate with `<use href="#id">`. |

**Avoid:** Auto-traced `<path>` data from VTracer or Inkscape's "trace bitmap" — these produce thousands of points and are not maintainable.

---

## 4. Dark-theme colour palette

All speaker SVGs must use these exact values to match the rack elevation style.

| Role | Property | Value |
|---|---|---|
| Document background | `fill` | `#0d1117` |
| Enclosure body fill | `fill` | `#1e293b` |
| Enclosure stroke | `stroke` | `#475569` |
| Dimension lines | `stroke` | `#4b5563` |
| Dimension text / annotations | `fill` | `#fcd34d` |
| Primary label (model name) | `fill` | `#f0f6fc` |
| Sub-label (spec line) | `fill` | `#8b949e` |
| Driver cone fill | `fill` | `#111827` |
| Driver surround stroke | `stroke` | `#334155` |
| Grille fill | `fill` | `#0f172a` |
| Grille stroke | `stroke` | `#1e293b` |
| Port slot fill | `fill` | `#0a0f1a` |

---

## 5. SVG document structure template

Every redrawn speaker SVG must follow this structure exactly.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
  Speaker: VOID <Model Name> — <view: front | side | top>
  Source PNG: 05-speaker-assets/png/<filename>-dims.png
  Actual dimensions: W <width>mm × H <height>mm × D <depth>mm
  Driver(s): <size>mm LF, <size>mm HF
  Drawn: YYYY-MM-DD
  Methodology: 06-reference-docs/svg-drawing-methodology.md
-->
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 <width> <height>"
     width="<width>" height="<height>"
     role="img"
     aria-labelledby="<id>-title <id>-desc">

  <title id="<id>-title">VOID <Model> — <View> Elevation</title>
  <desc id="<id>-desc">Technical line drawing of the VOID <Model> <view> view.
    Dimensions: W<width>mm × H<height>mm × D<depth>mm. Source: <filename>-dims.png.</desc>

  <defs>
    <style>
      text { font-family: 'Segoe UI', Arial, sans-serif; }
      .lbl  { fill: #f0f6fc; font-size: 12px; font-weight: 700; text-anchor: middle; }
      .sub  { fill: #8b949e; font-size: 9px; text-anchor: middle; }
      .dim  { fill: #fcd34d; font-size: 8px; font-family: 'Segoe UI Mono', monospace; text-anchor: middle; }
      .dln  { stroke: #4b5563; stroke-width: 0.5; fill: none; }
      .body { fill: #1e293b; stroke: #475569; stroke-width: 1.5; }
      .drv  { fill: #111827; stroke: #334155; stroke-width: 1; }
      .port { fill: #0a0f1a; stroke: #334155; stroke-width: 0.5; }
    </style>
  </defs>

  <!-- ── Background ─────────────────────────────────────────────── -->
  <rect width="<width>" height="<height>" fill="#0d1117"/>

  <!-- ── Enclosure body ─────────────────────────────────────────── -->
  <!-- Replace with actual dimensions. x/y add margin for dim lines. -->
  <rect class="body" x="40" y="40" width="<body-w>" height="<body-h>" rx="2"/>

  <!-- ── Drivers ────────────────────────────────────────────────── -->
  <!-- LF driver -->
  <circle class="drv" cx="<cx>" cy="<cy>" r="<r>"/>
  <!-- HF driver / tweeter -->
  <circle class="drv" cx="<cx>" cy="<cy>" r="<r>"/>

  <!-- ── Port(s) ────────────────────────────────────────────────── -->
  <rect class="port" x="<x>" y="<y>" width="<w>" height="<h>"/>

  <!-- ── Dimension lines ───────────────────────────────────────── -->
  <!-- Width arrow — horizontal, above enclosure -->
  <line class="dln" x1="40" y1="30" x2="<body-w+40>" y2="30"/>
  <text class="dim" x="<mid>" y="26">W<width>mm</text>
  <!-- Height arrow — vertical, left of enclosure -->
  <line class="dln" x1="30" y1="40" x2="30" y2="<body-h+40>"/>
  <text class="dim" x="20" y="<mid>" transform="rotate(-90,20,<mid>)">H<height>mm</text>

  <!-- ── Labels ─────────────────────────────────────────────────── -->
  <text class="lbl" x="<mid>" y="<bottom+18>">VOID <MODEL></text>
  <text class="sub" x="<mid>" y="<bottom+30>"><spec line></text>

</svg>
```

### viewBox sizing convention

- Add **40 px margin on each side** of the enclosure body for dimension lines and labels.
- Scale: use **1 SVG user unit = 1 mm** where the drawing fits within ~600 × 800 px. Scale to 0.5 px/mm for large enclosures (e.g. the Venu 215, 600mm wide).
- Always set both `width`/`height` attributes and `viewBox` to identical values so the SVG renders at its natural size without scaling artefacts.

---

## 6. SVGO optimisation step

Run SVGO after completing the drawing and before committing. SVGO removes redundant attributes, normalises whitespace, and shrinks file size without altering visual output.

**Requires Node.js.**

```bash
# Single file
npx svgo 05-speaker-assets/svg/<filename>.svg --output 05-speaker-assets/svg/<filename>.svg

# All SVGs in the directory (destructive — commit first)
npx svgo --folder 05-speaker-assets/svg/

# Recommended config (creates svgo.config.js in project root if not present)
# Disable plugins that alter semantics: removeTitle, removeDesc, removeViewBox
npx svgo --config svgo.config.js 05-speaker-assets/svg/<filename>.svg
```

**Minimum safe SVGO config** (`svgo.config.js` at project root):

```js
module.exports = {
  plugins: [
    { name: 'preset-default', params: {
        overrides: {
          removeTitle: false,      // keep <title> for accessibility
          removeDesc: false,       // keep <desc> for accessibility
          removeViewBox: false,    // never remove viewBox
          cleanupIds: false,       // keep aria-labelledby IDs
        }
    }}
  ]
};
```

**If SVGO / Node.js is unavailable:** skip this step. The unoptimised SVG is still valid. Record "SVGO not run" in the commit message.

---

## 7. Validation — ImageMagick pixel-diff (primary)

After drawing, render the SVG to PNG and compare it against the source PNG to verify proportions and driver placement are reasonable.

### Step 1 — Render SVG to PNG

```bash
magick -background "#0d1117" 05-speaker-assets/svg/<name>-front.svg \
       05-speaker-assets/svg/validation/<name>-front-rendered.png
```

### Step 2 — Compare rendered PNG vs source PNG

```bash
magick compare -metric RMSE \
  05-speaker-assets/png/<name>-front.png \
  05-speaker-assets/svg/validation/<name>-front-rendered.png \
  05-speaker-assets/svg/validation/<name>-front-diff.png
```

The command prints `<RMSE value> (<normalised>)` to stderr. Because the source PNGs are manufacturer photos (not line drawings), a perfect pixel-match is neither expected nor required. The diff image is useful for **checking driver position, port location, and overall aspect ratio**, not for achieving a low RMSE score.

**Interpreting the diff:**
- Bright red pixels in the diff = large deviation at that location.
- Focus on the enclosure outline and driver centres — these should roughly align.
- Ignore colour differences entirely (source PNGs are colour photos; SVGs are dark-theme line drawings).

**Store diff images** in `05-speaker-assets/svg/validation/` — this directory exists for exactly this purpose (`.gitkeep` included).

### Step 3 — Side-by-side visual check

Open both the source PNG and the rendered SVG in a browser or image viewer. Confirm:
- [ ] Enclosure aspect ratio matches (W:H proportions)
- [ ] LF driver is centred in the enclosure (or matches source position)
- [ ] HF driver / tweeter is in the correct quadrant
- [ ] Ports are at the correct edge (top, bottom, or front)
- [ ] No clipping — enclosure body fully visible within viewBox

---

## 8. Validation — browser screenshot (fallback, ImageMagick absent)

If `magick` is not installed:

1. Open the SVG file directly in Chrome or Edge (drag-and-drop to address bar, or `file:///...`).
2. Use DevTools → toggle device toolbar → set a fixed viewport matching the SVG's `width`/`height`.
3. Take a screenshot (`Ctrl+Shift+P` → "Capture screenshot").
4. Open the source PNG alongside the screenshot.
5. Visually check the five items in §7 Step 3.
6. Save the screenshot to `05-speaker-assets/svg/validation/<name>-front-browser.png`.

---

## 9. Accessibility requirements

Every SVG must include:

```xml
<!-- On the root <svg> element: -->
role="img"
aria-labelledby="<id>-title <id>-desc"

<!-- As first children of <svg>: -->
<title id="<id>-title">...</title>
<desc id="<id>-desc">...</desc>
```

The `<title>` should name the speaker and view. The `<desc>` should include physical dimensions and source reference. This pattern matches `rack-elevation.svg` exactly.

---

## 10. Commit convention

```
feat(speaker-svg): redraw <model> <view> from dims PNG

Source: 05-speaker-assets/png/<name>-dims.png
Dimensions: W<w>mm × H<h>mm × D<d>mm
SVGO: run / not run (Node.js unavailable)
ImageMagick diff: <pass | browser screenshot saved>
```

---

## 11. Speaker redraw queue

| SVG file | Source PNG | Status |
|---|---|---|
| `void-air-motion-v2-front.svg` | `void-air-motion-v2-dims.png` | VOID — needs redraw |
| `void-air-motion-v2-side.svg` | `void-air-motion-v2-dims.png` | VOID — needs redraw |
| `void-air-motion-v2-top.svg` | `void-air-motion-v2-dims.png` | VOID — needs redraw |
| `void-venu-215-v2-front.svg` | `void-venu-215-v2-dims.png` | VOID — needs redraw |
| `void-venu-215-v2-side.svg` | `void-venu-215-v2-dims.png` | VOID — needs redraw |
| `void-venu-215-v2-top.svg` | `void-venu-215-v2-dims.png` | VOID — needs redraw |
| `void-air-vantage-front.svg` | `void-air-vantage-dims.png` | VOID — needs redraw |
| `void-air-vantage-side.svg` | `void-air-vantage-dims.png` | VOID — needs redraw |
| `void-air-vantage-top.svg` | `void-air-vantage-dims.png` | VOID — needs redraw |

The two Bias amp SVGs (`bias-v3-amp-front.svg`, `bias-v3-amp-side.svg`) are also VTracer dumps but are lower priority — the rack elevation SVG already renders the amp visually.

---

## 12. Reference: rack-elevation.svg style patterns

The established style (from `07-tech-pack/rack-elevation.svg`) uses these specific patterns — all speaker SVGs should be consistent:

- `font-family: 'Segoe UI', Arial, sans-serif` for all text
- `font-family: 'Segoe UI Mono', monospace` for spec/dimension labels
- `dominant-baseline: central` for vertically-centred inline text
- `stroke-width: 1.5` for primary enclosure outlines
- `stroke-width: 0.5` for internal detail lines (grille dots, port slots)
- `rx="2"` on enclosure `<rect>` elements for slightly rounded corners
- Mounting hole circles: `fill="#0f172a" stroke="#475569" stroke-width="1"`
