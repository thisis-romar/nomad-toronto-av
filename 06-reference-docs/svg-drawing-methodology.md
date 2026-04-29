# SVG asset methodology: PDF extraction → clean vectors

**Purpose:** Defines the end-to-end workflow for sourcing clean equipment SVGs and PNGs for the tech pack. The primary approach is direct vector extraction from manufacturer PDF manuals using `pdftocairo`. Hand-crafting SVGs is a last resort.

**Last updated:** 2026-04-29

---

## 1. Decision tree — how to source an equipment asset

```
Does a manufacturer PDF exist for the equipment?
│
├─ YES → Which page has the best diagram?
│         ├─ Cover page (clean product illustration, no annotations) → pdftocairo → -front.svg or -cover.png
│         ├─ Dimensions page (technical drawing with mm dims) → pdftocairo → -dims.svg
│         └─ Labeled panel page (callout numbers/letters in black) → pdftocairo won't help; use Option B
│
└─ NO / PDF has only raster images →
          ├─ Search retailer CDN for official product photo (Thomann, Sweetwater, B&H)
          │   → download as PNG, save as -rear.png or -cover.png
          └─ Last resort: hand-craft SVG using dark-theme template (§5)
```

### When pdftocairo fails
- **All paths rendered black** (Pioneer CDJ-3000, DJM-V10): the PDF uses a color space pdftocairo flattens. Callout lines can't be filtered by color → source a clean page or use the cover image instead.
- **Labeled diagrams with black callout letters** (Bias V3 rear panel, p.5): no automated way to remove callouts → source from a retailer CDN photo.

---

## 2. Extraction command — pdftocairo

```bash
# Extract a single page as SVG (preferred for line-art/technical drawings)
pdftocairo -svg -f <PAGE> -l <PAGE> "<path/to/manual.pdf>" "<output-prefix>"
mv "<output-prefix>" "<output-prefix>.svg"   # pdftocairo omits .svg extension

# Extract a single page as high-res PNG (preferred for photographic covers)
pdftocairo -png -r 150 -f <PAGE> -l <PAGE> "<path/to/manual.pdf>" "<output-prefix>"
# Output: <output-prefix>-<PAGE>.png  (zero-padded, e.g. -01.png)

# Scout all pages at 72 DPI (for finding the right page)
pdftocairo -png -r 72 "<path/to/manual.pdf>" "C:/tmp/<prefix>"
```

**Which page to use:**
- `cover page (p.1)` — clean product illustration, no dimension lines → ideal for `-front.svg` or `-cover.png`
- `dimensions/mechanical drawings page` — technical orthographic with mm callouts → ideal for `-dims.svg`
- Avoid pages with numbered callout bubbles or labeled leader lines unless you can filter them by color.

---

## 3. Current asset inventory and status

### SVG assets (`05-speaker-assets/svg/`)

| File | Source | Notes |
|---|---|---|
| `speakers/void-air-motion-v2-dims.svg` | Air Motion V2 User Guide p.8 | Multi-view + dims, clean ✅ |
| `speakers/void-air-vantage-dims.svg` | Air Vantage User Guide p.8 | Multi-view + dims, clean ✅ |
| `speakers/void-airten-v3-dims.svg` | Airten V3 User Manual p.8 | Multi-view + dims, clean ✅ |
| `speakers/void-stasys-xair-dims.svg` | Stasys Xair User Guide p.7 | Dims + specs same page ✅ |
| `speakers/void-venu-215-v2-dims.svg` | Venu V2 Series User Guide p.45 | Appendix B.9, clean ✅ |
| `mixers/ah-cq-12t-front.svg` | CQ-12T datasheet p.1 | Clean I/O surface illustration ✅ |
| `mixers/ah-cq-12t-dims.svg` | CQ-12T datasheet p.3 | 290.4×254.4mm ortho views ✅ |
| `amplifiers/bias-q5-front.svg` | Bias Q5 User Guide p.1 | 1U rack front illustration ✅ |
| `amplifiers/bias-q5-dims.svg` | Bias Q5 User Guide p.4 | 483×44.5mm dims ✅ |
| `amplifiers/bias-v3-dims.svg` | Bias V3/V9 User Manual p.8 | Bias V3 mechanical drawing ✅ |
| `amplifiers/bias-v9-dims.svg` | Bias V3/V9 User Manual p.9 | Bias V9 mechanical drawing ✅ |
| `dj-gear/pioneer-cdj-3000-top.svg` | CDJ-3000 manual p.1 (cover) | Clean top panel, all controls ✅ |
| `dj-gear/pioneer-djm-v10-panel.svg` | DJM-V10 manual p.1 | Clean top panel ✅ |
| `dj-gear/pioneer-djm-v10-rear.svg` | DJM-V10 manual p.9 | Red callouts removed ✅ |
| `connectors/xlr-female.svg` | Wikimedia Commons | ✅ |
| `connectors/xlr-male.svg` | Wikimedia Commons | ✅ |
| `connectors/iec-c14-inlet.svg` | Wikimedia Commons | ✅ |
| `connectors/midi-din-5pin.svg` | Wikimedia Commons | ✅ |
| `connectors/rj45-plug.svg` | Wikimedia Commons | ✅ |

### PNG assets (`05-speaker-assets/png/`)

**speakers/** — VOID speaker photos and dims renders  
**mixers/** — Allen & Heath CQ-12T photos  
**amplifiers/** — Bias Q5/V3 photos  
**dj-gear/** — Pioneer CDJ-3000 / DJM-V10 photos  

Key clean PNGs (no callouts):

| File | Source | Notes |
|---|---|---|
| `speakers/void-*-cover.png` | Manual p.1 at 150 DPI | 1241×1754, dark bg product renders ✅ |
| `mixers/ah-cq-12t-rear.png` | Thomann CDN (official A&H photo) | 1000×1000, top-down I/O view ✅ |
| `mixers/ah-cq-12t-rear-angled.png` | Thomann CDN | 1000×1000, rear-quarter ✅ |
| `dj-gear/pioneer-cdj-3000-rear-clean.png` | DJ TechTools CDN (Pioneer official) | 2000×1334, studio photo ✅ |
| `dj-gear/pioneer-djm-v10-rear-clean.png` | sourced | Clean, no annotations ✅ |

---

## 4. File naming conventions

```
<brand>-<model>-<view>.<ext>

brand:   ah (Allen & Heath), bias, pioneer, void
model:   cdj-3000, djm-v10, cq-12t, q5, v3, v9,
         air-motion-v2, air-vantage, airten-v3, stasys-xair, venu-215-v2
view:    front, rear, side, top, dims, cover, panel
ext:     .svg (vector), .png (raster)
```

Subfolders by category: `speakers/`, `mixers/`, `amplifiers/`, `dj-gear/`, `connectors/`

---

## 5. Dark-theme SVG template (hand-craft fallback only)

Use only when PDF extraction is not possible. Match the palette from `07-tech-pack/rack-elevation.svg`:

| Role | Value |
|---|---|
| Document background | `#0d1117` |
| Enclosure body fill | `#1e293b` |
| Enclosure stroke | `#475569` stroke-width 1.5 |
| Dimension lines | `#4b5563` stroke-width 0.5 |
| Dimension text | `#fcd34d` |
| Primary label | `#f0f6fc` |
| Sub-label | `#8b949e` |
| Driver cone | `#111827` fill, `#334155` stroke |
| Port | `#0a0f1a` fill |

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
  Equipment: <Brand Model> — <view>
  Source: 05-speaker-assets/png/<category>/<filename>-dims.png
  Dimensions: W<w>mm × H<h>mm × D<d>mm
  Drawn: YYYY-MM-DD
  Methodology: 06-reference-docs/svg-drawing-methodology.md
-->
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 <w> <h>" width="<w>" height="<h>"
     role="img" aria-labelledby="id-title id-desc">

  <title id="id-title"><Brand Model> — <View></title>
  <desc id="id-desc">Technical drawing. W<w>mm × H<h>mm × D<d>mm.</desc>

  <defs>
    <style>
      text { font-family: 'Segoe UI', Arial, sans-serif; }
      .lbl  { fill: #f0f6fc; font-size: 12px; font-weight: 700; text-anchor: middle; }
      .sub  { fill: #8b949e; font-size: 9px; text-anchor: middle; }
      .dim  { fill: #fcd34d; font-size: 8px; font-family: monospace; text-anchor: middle; }
      .dln  { stroke: #4b5563; stroke-width: 0.5; fill: none; }
      .body { fill: #1e293b; stroke: #475569; stroke-width: 1.5; }
      .drv  { fill: #111827; stroke: #334155; stroke-width: 1; }
      .port { fill: #0a0f1a; stroke: #334155; stroke-width: 0.5; }
    </style>
  </defs>

  <rect width="<w>" height="<h>" fill="#0d1117"/>
  <!-- add enclosure, drivers, ports, labels here -->

</svg>
```

**Mandatory inspection before commit:** Read the SVG as an image, read the source PNG, compare side-by-side, list every discrepancy, fix before committing.

---

## 6. SVGO optimisation (optional)

Run after hand-crafting an SVG (not needed for PDF-extracted files — they're already minimal).

```bash
npx svgo 05-speaker-assets/svg/<category>/<filename>.svg \
         --output 05-speaker-assets/svg/<category>/<filename>.svg
```

---

## 7. Validation

For PDF-extracted SVGs: render the source PDF page at 120 DPI (`pdftocairo -png -r 120`) and visually compare against the extracted SVG to confirm the correct page was used.

For hand-crafted SVGs: mandatory inspect loop — SVG rendered vs source PNG — no commit until they match.

---

## 8. Commit convention

```
feat(assets): extract <equipment> <view> SVG/PNG from <source>

Source: <PDF filename> p.<page> / <retailer> CDN
Resolution/format: <e.g. pdftocairo -svg / 1000×1000 JPEG>
No annotation overlays: confirmed
```
