#!/usr/bin/env python3
"""
Render and validate NØMAD photo-equipment audits.

Core invariant:
  bbox_px is ALWAYS expressed in native source-image pixels.
  Never resize/crop the source before applying bbox_px.
  bbox_norm is derived output, not authoritative input.

Usage:
  python3 scripts/photo-audit-loop.py \
    --image 09-site-survey/photos/2026-08-12-main-room-source.jpg \
    --manifest 09-site-survey/data/main-room-equipment-audit-2026-08-12.json \
    --out 09-site-survey/rendered/main-room-equipment-audit.jpg
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

COLORS = {
    "audio": (255, 205, 70),
    "lighting": (65, 210, 235),
    "dj": (235, 105, 220),
}

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def validate(image: Image.Image, manifest: dict, image_path: Path) -> list[str]:
    errors = []
    src = manifest["source"]
    if [image.width, image.height] != [src["width_px"], src["height_px"]]:
        errors.append(
            f"source dimensions mismatch: actual={image.size} expected="
            f"({src['width_px']}, {src['height_px']})"
        )
    if src.get("sha256") and digest(image_path) != src["sha256"]:
        errors.append("source SHA-256 mismatch")
    for item in manifest["items"]:
        x1, y1, x2, y2 = item["bbox_px"]
        if not (0 <= x1 < x2 <= image.width and 0 <= y1 < y2 <= image.height):
            errors.append(f"{item['id']}: bbox outside native source bounds")
    return errors

def load_font(size: int):
    for p in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def render(image: Image.Image, manifest: dict) -> Image.Image:
    out = image.copy().convert("RGB")
    d = ImageDraw.Draw(out)
    f = load_font(21)
    for item in manifest["items"]:
        box = item["bbox_px"]
        color = COLORS.get(item["category"], (255,255,255))
        d.rectangle(tuple(box), outline=color, width=4)
        x, y = box[0] + 5, max(6, box[1] - 27)
        bb = d.textbbox((x,y), item["id"], font=f)
        d.rectangle((bb[0]-5, bb[1]-5, bb[2]+5, bb[3]+5), fill=color)
        d.text((x,y), item["id"], fill=(0,0,0), font=f)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True, type=Path)
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    image = Image.open(args.image)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors = validate(image, manifest, args.image)
    if errors:
        raise SystemExit("AUDIT VALIDATION FAILED:\n- " + "\n- ".join(errors))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    render(image, manifest).save(args.out, quality=94)
    print(f"PASS: {len(manifest['items'])} detections validated and rendered -> {args.out}")

if __name__ == "__main__":
    main()
