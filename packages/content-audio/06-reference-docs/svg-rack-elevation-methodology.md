# SVG rack elevation diagrams: a complete technical reference

**Generating dimensionally accurate SVG rack diagrams requires three foundations: precise EIA-310-D measurements, proper SVG coordinate mapping, and structured equipment rendering patterns.** This report synthesizes rack hardware specifications, SVG engineering best practices, open-source implementation patterns, color coding conventions, and interactivity techniques into a unified reference for building a code-generation skill. Every dimension cited here is cross-verified across multiple rack manufacturers (APC, Chatsworth, Rittal, Middle Atlantic) and the EIA-310-D / IEC 60297 standards.

---

## EIA-310-D dimensional specifications for 19-inch racks

The 19-inch rack system's geometry is governed by a small set of precise, universally agreed-upon dimensions. The critical measurements for SVG generation are:

| Dimension | Imperial | Metric |
|---|---|---|
| **Overall rack width** (front panel) | 19.000" | 482.60 mm |
| **Rail/flange width** | 0.625" (5/8") | 15.875 mm |
| **Rack opening** (between inner rail edges) | 17.750" | 450.85 mm |
| **Hole-to-hole horizontal spacing** (center-to-center) | 18.312" ±0.062" | 465.12 mm |
| **1 Rack Unit (1U) height** | 1.750" | 44.45 mm |
| **Equipment panel height per U** | 1.719" | 43.66 mm |
| **Panel clearance gap** | 0.031" total | 0.794 mm |

The **rack width decomposes cleanly**: left rail (0.625") + opening (17.750") + right rail (0.625") = 19.000". Equipment bodies must not exceed 17.750" wide; the full 19" includes mounting ears/flanges. Mounting holes are not centered on the flange but offset slightly inward — the left hole center sits at **8.74 mm** from the left edge of the rack (calculated as (482.60 − 465.12) / 2), and the right hole center at **473.86 mm**.

The equipment panel height formula is `h = (44.45 × n) − 0.794 mm`, where *n* is the number of rack units. The 0.794 mm clearance gap splits approximately equally above and below the panel (~0.397 mm each), preventing equipment from binding during installation.

### The three-hole mounting pattern

Each rack unit contains **three mounting holes per rail**, following the repeating vertical sequence: **0.625", 0.625", 0.500"**. The U boundary falls at the midpoint of the 0.500" gap, so each U "owns" 0.250" on either side of that gap. The hole positions within a single U, measured from the top of the U space:

| Hole | Offset from U top | Metric |
|---|---|---|
| Hole 1 (top) | 0.250" | 6.350 mm |
| Hole 2 (middle) | 0.875" | 22.225 mm |
| Hole 3 (bottom) | 1.500" | 38.100 mm |

This verifies cleanly: holes 1→2 = 0.625", holes 2→3 = 0.625", hole 3 to next U's hole 1 = 0.250" + 0.250" = 0.500". The programmatic generation algorithm is straightforward — for U index *i* (zero-based, top to bottom): `hole_y = (i × 44.45) + offset`, where offset is 6.35, 22.225, or 38.1 mm. A 42U rack produces **126 holes per rail**. Standard square holes are **9.5 × 9.5 mm** for cage nuts; threaded holes use **#10-32** (most common US), **#12-24** (legacy), or **M6** (international).

Standard rack heights are **42U** (1866.9 mm, the traditional full-height standard) and **48U** (2133.6 mm, increasingly standard in modern data centers). Common smaller sizes include 6U, 12U, 24U, and 27U.

---

## SVG coordinate system and structural architecture

The SVG `viewBox` is the critical mechanism for mapping coordinates to real-world rack dimensions. The recommended approach uses **1 user unit = 1 mm**, making coordinate math transparent and debuggable. For a 42U rack with label margins:

```xml
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 600 1890"
     preserveAspectRatio="xMidYMin meet"
     role="img" aria-labelledby="rack-title rack-desc">
  <title id="rack-title">Rack A — Data Center Floor 3</title>
  <desc id="rack-desc">42U rack elevation showing installed equipment</desc>
```

The `preserveAspectRatio="xMidYMin meet"` setting scales uniformly and aligns to the top center — ideal for rack diagrams that may scroll vertically. The viewBox width of 600 accommodates **~60 mm of label space** on each side of the 482.6 mm rack body.

### Metadata embedding strategy

The code generator should use a **three-layer metadata approach**. First, `<title>` and `<desc>` elements as the first children of the root `<svg>` and of each equipment `<g>` group provide accessibility and native browser tooltips. Second, **`data-*` attributes** on equipment groups store structured metadata (device type, model, serial, IP, power draw) that is queryable via JavaScript's `element.dataset` API. Third, a `<metadata>` block with RDF/Dublin Core at the document level stores rack-level information (location, total units, generation date).

```xml
<g id="dev-switch-01" class="equipment switch"
   data-device-type="switch" data-model="Catalyst 9300"
   data-rack-position="5" data-rack-height="1"
   data-serial="FJC2451L0AB" data-ip="10.0.1.1">
  <title>Core Switch — Cisco Catalyst 9300</title>
  <desc>1U switch at position U5, IP: 10.0.1.1</desc>
  <rect class="device-body" x="50" y="225" width="400" height="44"/>
  <text x="250" y="247" class="device-label">Cisco 9300</text>
</g>
```

### Accessibility requires role="img" plus aria-labelledby

Deque's cross-browser testing found that the **most reliable accessible SVG pattern** is `role="img"` on the root `<svg>` combined with `aria-labelledby` referencing both the title and description IDs. For interactive diagrams where users explore individual equipment, each device group should carry `role="graphics-object"`, an `aria-label`, and `tabindex="0"` for keyboard navigation. The W3C WAI-ARIA Graphics Module defines three roles: `graphics-document` (the root), `graphics-object` (semantic components like individual devices), and `graphics-symbol` (atomic icons like status LEDs). DOM order should match the logical rack order so screen readers traverse equipment in a meaningful sequence.

---

## CSS theming with custom properties enables swappable color schemes

SVG presentation attributes (`fill="red"`) have **zero CSS specificity**, meaning CSS class rules automatically override them. This makes class-based theming clean and predictable. The recommended pattern uses CSS custom properties defined on the `<svg>` element, with theme variants toggled via a class:

```xml
<defs><style type="text/css"><![CDATA[
  svg {
    --server-fill: #4477AA; --switch-fill: #228833;
    --firewall-fill: #EE6677; --storage-fill: #AA3377;
    --power-fill: #EE7733; --patch-fill: #BBBBBB;
    --empty-fill: #E0E0E0; --text-on-device: #ffffff;
    --font-main: 'Inter', 'Segoe UI', sans-serif;
    --font-mono: 'JetBrains Mono', 'Consolas', monospace;
  }
  svg.theme-dark {
    --server-fill: #2980b9; --empty-fill: #2d2d44;
  }
  .server .device-body { fill: var(--server-fill); }
  .device-label {
    fill: var(--text-on-device); font-family: var(--font-main);
    font-size: 11px; text-anchor: middle; dominant-baseline: central;
  }
  .u-label {
    fill: #999; font-family: var(--font-mono);
    font-size: 9px; text-anchor: end; dominant-baseline: central;
  }
]]></style></defs>
```

For text rendering, **monospace fonts** should be used for U-position numbers, IP addresses, and serial numbers (digit alignment and disambiguation of 0/O, 1/l), while **sans-serif fonts** work best for equipment labels. The `text-anchor: middle` and `dominant-baseline: central` combination centers text precisely within device rectangles. For long labels, the code generator should **pre-calculate line breaks** at generation time using `<tspan>` elements with `dy` offsets, since SVG `<text>` does not support automatic word wrapping. The `<foreignObject>` alternative offers CSS text-overflow but fails in non-browser SVG renderers (Inkscape, Illustrator, email clients) and should be avoided for portable output.

---

## How NetBox and other open-source tools render rack SVGs

**NetBox** is the most mature open-source reference implementation. Its `RackElevationSVG` class in `netbox/dcim/svg/racks.py` uses Python's `svgwrite` library to programmatically construct SVG elements. The API endpoint `/api/dcim/racks/<id>/elevation/?render=svg&face=front` accepts parameters for `unit_width` (default 230px), `unit_height` (default 20px), and `legend_width`. Each device renders as the universal pattern: **`<a>` hyperlink wrapping a `<rect>` (colored by device role) and `<text>` label**, with an optional `<image>` overlay for device-type photos using `preserveAspectRatio="xMidYMid slice"`. Text color auto-calculates for contrast against the background. NetBox estimates character width at `font_size × 0.6` for label truncation.

**rackdiag** (part of Python's `nwdiag` package) takes a different approach: a text-based DSL (`rackdiag { 16U; 1: UPS [2U]; 3: DB Server }`) parsed into an internal model and rendered to SVG via the blockdiag rendering engine. It supports multiple racks, ascending/descending numbering, and per-device height annotations. It is also available through **Kroki.io**, a unified diagram API that wraps rackdiag behind a REST endpoint accepting the DSL and returning SVG.

**Rack-Visualization** (balki97, JavaScript) uses a custom XML markup ("RackML") where element names indicate device type (`<switch>`, `<server>`, `<pdu>`) with `height` and `href` attributes, rendered to SVG client-side. **allprobe/rack-visualization** takes a D3.js approach, binding JSON data to SVG elements for interactive rack displays. Notably, **RackTables does not generate SVG** — it uses HTML tables with colored cells for rack views, with GraphViz-generated SVG only for cabling topology diagrams.

The universal SVG pattern across all implementations is: colored rectangles for device slots, centered text labels, a side column for U numbers, CSS classes for device states (`slot`, `blocked`, `occupied`), and `<title>` elements for tooltip metadata. U-based vertical layout (1U = one vertical increment) is the fundamental coordinate unit everywhere.

---

## Equipment color coding has no formal standard but strong conventions

**No TIA/EIA standard governs rack diagram colors.** NetBox provides 27 predefined hex colors but lets users assign them freely to device roles. D-Tools defaults to white faceplates. Visio uses photorealistic stencils. However, a clear consensus emerges across DCIM deployments and data center documentation:

| Category | Hex | Color | Rationale |
|---|---|---|---|
| **Servers / Compute** | `#4477AA` | Blue | Most universal convention across all tools |
| **Switches / Network** | `#228833` | Green | "Go"/active connectivity association |
| **Routers** | `#009988` | Teal | Differentiated from switches |
| **Firewalls / Security** | `#EE6677` | Red | Danger/security/attention signaling |
| **Storage (SAN/NAS)** | `#AA3377` | Purple | Distinguished from blue compute |
| **Power (PDU/UPS)** | `#EE7733` | Orange | Energy/warning association |
| **Patch panels / Cabling** | `#BBBBBB` | Grey | Passive, visually recessive |
| **AV / Video** | `#CCBB44` | Yellow | Distinct from networking |
| **Audio equipment** | `#CC6677` | Rose | Differentiated from video |
| **Blank / Filler panels** | `#DDDDDD` | Light grey | Empty space, maximally recessive |
| **KVM / Console** | `#66CCEE` | Cyan | Management/out-of-band |
| **Telecom / Demarcation** | `#332288` | Indigo | Follows TIA cabling conventions |

The hex values above are drawn from **Paul Tol's colorblind-safe palettes** (Bright and Muted schemes), which maintain distinguishability for the ~5% of males with color vision deficiency. For stricter accessibility, **ColorBrewer's "Paired" palette** supports up to 12 categories while remaining colorblind-safe. The code generator should always combine color with text labels and include a legend — professional DCIM tools unanimously follow this practice.

---

## Pure CSS interactivity patterns that work without JavaScript

SVG supports rich interactivity without any JavaScript through four CSS/SVG-native mechanisms. The **layered SVG structure** is essential: rack frame → U-labels → equipment → tooltips, with tooltips rendered last (SVG has no z-index; later elements paint on top).

**Hover highlighting** uses CSS `:hover` on equipment `<g>` groups to modify `fill`, `stroke`, and `stroke-width` with smooth `transition` properties. Text labels inside clickable groups need `pointer-events: none` to prevent them from intercepting hover/click events:

```css
.equipment rect.chassis {
  transition: fill 0.2s, stroke 0.2s, stroke-width 0.15s;
  cursor: pointer;
}
.equipment:hover rect.chassis {
  stroke: #3b82f6; stroke-width: 2;
  filter: brightness(1.15);
}
.equipment text { pointer-events: none; }
```

**CSS-only tooltips** use `opacity: 0` on a child `<g class="tooltip">` group that transitions to `opacity: 1` on parent hover. The tooltip group needs `pointer-events: none` to prevent flickering. For the cleanest rendering, tooltips can be placed in a separate top-level `<g id="tooltips">` layer and linked to equipment via CSS sibling or descendant selectors. The simpler **native SVG `<title>` element** produces browser-styled plain-text tooltips with zero effort — suitable for basic metadata display.

**Clickable hyperlinks** use SVG's `<a>` element (with both `href` for SVG 2 and `xlink:href` for backward compatibility) wrapping equipment groups. The `target="_blank"` attribute opens links in new tabs. Unlike HTML, SVG `<a>` provides no default visual styling — cursor, hover states, and focus indicators must be added explicitly.

**Click-to-select** uses the CSS `:target` pseudo-class: wrapping equipment in `<a href="#unit-20">` and styling `#unit-20:target` changes appearance when the URL hash matches. **SMIL animations** remain fully supported (96.46% global browser coverage, never actually deprecated) and work even when SVG is embedded via `<img>` — useful for pulsing LED status indicators with `<animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>`. The **`<symbol>`/`<use>` pattern** enables reusable equipment templates defined once in `<defs>` and instantiated with different positions and data attributes, though CSS styling of `<use>` shadow DOM requires CSS custom properties or `currentColor` as workarounds.

---

## Conclusion: a coordinate-precise SVG generation blueprint

The complete SVG rack coordinate system maps directly from EIA-310-D specifications: left hole column at x = 8.74 mm, equipment area from x = 15.875 mm to x = 466.725 mm, right hole column at x = 473.86 mm, with each U spanning 44.45 mm vertically and three holes at offsets 6.35, 22.225, and 38.1 mm. The rendering pattern — `<a>` wrapping `<rect>` + `<text>` per device, CSS custom properties for theming, `data-*` attributes for metadata, `role="img"` with `aria-labelledby` for accessibility — is validated by NetBox's production implementation serving thousands of data centers.

The most actionable insight for the code generator is that **all dimensional math reduces to a single loop**: iterate U positions top-to-bottom, placing equipment rectangles at `y = u_index × 44.45` with height `n × 44.45 - 0.794`, while applying category colors from a colorblind-safe palette and wrapping each device in a hyperlinked, accessible, hover-interactive group. No JavaScript is required for tooltips, highlighting, or navigation — CSS `:hover`, `opacity` transitions, and SVG `<a>` elements handle all essential interactivity natively.