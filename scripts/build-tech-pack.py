import re
from pathlib import Path

# NOTE (flagged, not fixed — see ADR-0001 / lighting subsystem work):
#   BASE and `out_html` below are hardcoded to a Windows developer path and will NOT run on
#   Linux/CI as-is. Left unchanged to avoid an unrelated behavioural change; make these
#   environment-relative (e.g. Path(__file__).resolve().parents[1]) in a dedicated fix.
BASE = Path("C:/Users/romar/projects/nomad-toronto-av")
TP   = BASE / "07-tech-pack"

def md_to_html(text):
    text = re.sub(r'^---.*?---\s*', '', text, flags=re.DOTALL)
    lines = text.split('\n')
    out = []
    in_table = False
    in_code = False
    in_ul = False
    in_ol = False

    def close_list():
        nonlocal in_ul, in_ol
        if in_ul: out.append('</ul>'); in_ul = False
        if in_ol: out.append('</ol>'); in_ol = False

    for line in lines:
        if line.startswith('```'):
            if in_code:
                out.append('</code></pre>'); in_code = False
            else:
                close_list()
                out.append('<pre><code>'); in_code = True
            continue
        if in_code:
            out.append(line.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))
            continue

        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                close_list()
                out.append('<table>')
                in_table = True
            if re.match(r'^\|[\s\-:]+\|', line):
                continue
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            is_header = out[-1] == '<table>'
            tag = 'th' if is_header else 'td'
            out.append('<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>')
            continue
        if in_table:
            out.append('</table>'); in_table = False

        m = re.match(r'^(#{1,4})\s+(.*)', line)
        if m:
            close_list()
            lvl = len(m.group(1))
            out.append(f'<h{lvl}>{m.group(2)}</h{lvl}>')
            continue

        if re.match(r'^---+\s*$', line):
            close_list()
            out.append('<hr>')
            continue

        if line.startswith('>'):
            close_list()
            content = line[1:].strip()
            out.append(f'<blockquote>{content}</blockquote>')
            continue

        m = re.match(r'^[-*]\s+(.*)', line)
        if m:
            if not in_ul:
                close_list(); out.append('<ul>'); in_ul = True
            out.append(f'<li>{m.group(1)}</li>')
            continue

        m = re.match(r'^\d+\.\s+(.*)', line)
        if m:
            if not in_ol:
                close_list(); out.append('<ol>'); in_ol = True
            out.append(f'<li>{m.group(1)}</li>')
            continue

        if not line.strip():
            close_list()
            continue

        close_list()
        out.append(f'<p>{line}</p>')

    close_list()
    if in_table: out.append('</table>')

    html = '\n'.join(out)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    html = re.sub(r'~~(.+?)~~', r'<del>\1</del>', html)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    html = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', html)
    return html

def inline_svg(path):
    try:
        content = Path(path).read_text(encoding='utf-8', errors='replace')
        content = re.sub(r'<\?xml[^>]*\?>', '', content).strip()
        return content
    except:
        return f'<p>[SVG not found: {path}]</p>'

docs = {
    'overview':          (TP / 'system-overview.md').read_text(encoding='utf-8'),
    'rider':             (TP / 'available-rider.md').read_text(encoding='utf-8'),
    'cables':            (TP / 'cable-schedule.md').read_text(encoding='utf-8'),
    'emergency':         (TP / 'emergency-procedures.md').read_text(encoding='utf-8'),
    'lighting_overview': (TP / 'lighting-system-overview.md').read_text(encoding='utf-8'),
    'dmx':               (TP / 'dmx-patch-schedule.md').read_text(encoding='utf-8'),
}

rack_svg   = inline_svg(TP / 'rack-elevation.svg')
signal_svg = inline_svg(TP / 'signal-flow.svg')
zone_svg   = inline_svg(TP / 'speaker-zone-map.svg')

CSS = """
  :root { --brand:#1a1a2e; --accent:#e8b923; --text:#1a1a1a; --muted:#555; --border:#ddd; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { font-family:'Segoe UI',Arial,sans-serif; font-size:10pt; color:var(--text); line-height:1.5; }
  .cover { background:var(--brand); color:white; min-height:100vh; display:flex; flex-direction:column;
           justify-content:center; padding:60px; page-break-after:always; }
  .cover .logo { font-size:48pt; font-weight:900; letter-spacing:-2px; }
  .cover .logo span { color:var(--accent); }
  .cover .sub { font-size:18pt; color:#aaa; margin-top:8px; }
  .cover-line { border-top:2px solid var(--accent); margin:40px 0; }
  .cover .meta { font-size:10pt; color:#888; line-height:2; }
  .cover .meta strong { color:white; }
  .section { padding:40px 50px; page-break-before:always; }
  .section-header { background:var(--brand); color:white; padding:12px 20px;
                    margin:-40px -50px 30px; display:flex; align-items:baseline; gap:16px; }
  .section-header h1 { font-size:15pt; color:white; border:none; margin:0; padding:0; }
  .section-header .num { color:var(--accent); font-size:10pt; font-weight:700; }
  h1 { font-size:14pt; color:var(--brand); border-bottom:2px solid var(--accent);
       padding-bottom:5px; margin:20px 0 10px; }
  h2 { font-size:11pt; color:var(--brand); margin:18px 0 7px; }
  h3 { font-size:10pt; color:var(--muted); margin:14px 0 5px; }
  h4 { font-size:9.5pt; color:var(--muted); margin:10px 0 4px; }
  p  { margin:5px 0; }
  hr { border:none; border-top:1px solid var(--border); margin:14px 0; }
  strong { color:var(--brand); }
  del { color:#c00; text-decoration:line-through; }
  table { width:100%; border-collapse:collapse; font-size:8.5pt; margin:8px 0 14px; }
  th { background:var(--brand); color:white; padding:5px 8px; text-align:left; font-weight:600; }
  td { padding:4px 8px; border-bottom:1px solid var(--border); }
  tr:nth-child(even) td { background:#f9f9f9; }
  pre { background:#1a1a2e; color:#c9d1d9; padding:12px 16px; border-radius:4px;
        font-size:8pt; font-family:'Consolas','Courier New',monospace;
        margin:8px 0; white-space:pre-wrap; }
  code { font-family:'Consolas','Courier New',monospace; font-size:8.5pt;
         background:#f0f0f0; padding:1px 4px; border-radius:2px; }
  pre code { background:none; padding:0; color:inherit; }
  blockquote { background:#fff8e1; border-left:4px solid #f0c040;
               padding:8px 14px; margin:8px 0; font-size:9pt; color:#555; }
  ul,ol { margin:5px 0 8px 20px; }
  li { margin:2px 0; }
  .diagram-wrap { border:1px solid var(--border); border-radius:4px; padding:10px;
                  margin:14px 0; background:#fafafa; page-break-inside:avoid; }
  .diagram-wrap svg { width:100%; height:auto; display:block; }
  .diagram-label { font-size:8pt; color:var(--muted); text-align:center;
                   margin-top:5px; font-style:italic; }
  @media print {
    .cover,.section-header,th { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  }
"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NOMAD Toronto Technical Pack 2026</title>
<style>{CSS}</style>
</head>
<body>

<div class="cover">
  <div class="logo">N<span>O</span>MAD</div>
  <div class="sub">Toronto &middot; 725 Queen Street East</div>
  <div class="cover-line"></div>
  <div style="font-size:22pt;font-weight:700;color:white;">Technical Pack</div>
  <div style="font-size:13pt;color:#aaa;margin-top:6px;">VOID Acoustics Permanent Installation &middot; April 2026</div>
  <div class="meta" style="margin-top:50px;">
    <strong>Capacity:</strong> 550 standing<br>
    <strong>System:</strong> VOID Acoustics &middot; 18 speakers &middot; 5 active amplifiers<br>
    <strong>DJ Equipment:</strong> 4&times; Pioneer CDJ-3000 &middot; Pioneer DJM-V10 &middot; Allen &amp; Heath CQ-12T<br>
    <strong>DSP Control:</strong> Armonia Pro Audio Suite &middot; 192.168.10.x<br>
    <strong>As-built:</strong> March 2026 &middot; CQ-12T confirmed April 2026<br>
    <strong>Prepared by:</strong> Emblem Projects Inc. &middot; admin+claude@emblemprojects.com
  </div>
</div>

<div class="section">
  <div class="section-header"><span class="num">01</span><h1>System Overview</h1></div>
  {md_to_html(docs['overview'])}
</div>

<div class="section">
  <div class="section-header"><span class="num">02</span><h1>System Diagrams</h1></div>
  <h2>Rack Elevation</h2>
  <div class="diagram-wrap">{rack_svg}<div class="diagram-label">Amp rack U1&ndash;U10 &middot; Armonia-controlled</div></div>
  <h2>Signal Flow</h2>
  <div class="diagram-wrap">{signal_svg}<div class="diagram-label">Full signal chain: CDJ-3000 sources to speaker zones</div></div>
  <h2>Speaker Zone Map</h2>
  <div class="diagram-wrap">{zone_svg}<div class="diagram-label">18-speaker zone layout &middot; FOH / Booth / Entrance</div></div>
</div>

<div class="section">
  <div class="section-header"><span class="num">03</span><h1>Technical Available Rider</h1></div>
  {md_to_html(docs['rider'])}
</div>

<div class="section">
  <div class="section-header"><span class="num">04</span><h1>Cable Schedule</h1></div>
  {md_to_html(docs['cables'])}
</div>

<div class="section">
  <div class="section-header"><span class="num">05</span><h1>Emergency Procedures</h1></div>
  {md_to_html(docs['emergency'])}
</div>

<div class="section">
  <div class="section-header"><span class="num">06</span><h1>Lighting System Overview</h1></div>
  {md_to_html(docs['lighting_overview'])}
</div>

<div class="section">
  <div class="section-header"><span class="num">07</span><h1>DMX Patch Schedule</h1></div>
  {md_to_html(docs['dmx'])}
</div>

</body>
</html>"""

out_html = Path("C:/tmp/nomad-tech-pack.html")
out_html.write_text(html, encoding='utf-8')
print(f"HTML written: {out_html} ({len(html)//1024} KB)")
