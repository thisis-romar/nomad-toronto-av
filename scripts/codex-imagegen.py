#!/usr/bin/env python3
"""
Iterative equipment diagram generator using OpenAI gpt-image-2.

Usage:
  python scripts/codex-imagegen.py <source.png> <output.png> [options]

Options:
  --prompt TEXT      Generation prompt (default: clean technical line art)
  --criteria TEXT    Quality evaluation criteria for vision scoring
  --max-iter INT     Max refinement iterations (default: 5, env: CODEX_IMAGEGEN_MAX_ITER)
  --size SIZE        Output size: 1024x1024, 1024x1536, 1536x1024, or auto
  --no-score         Skip vision scoring (just generate one pass)

Environment:
  OPENAI_API_KEY     Required. Project-scoped key from platform.openai.com/api-keys
  CODEX_IMAGEGEN_MODEL              Default: gpt-image-2
  CODEX_IMAGEGEN_MAX_ITER           Default: 5
  CODEX_IMAGEGEN_QUALITY_THRESHOLD  Default: 7 (out of 10)
"""
import os
import sys
import argparse
import base64
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

MODEL = os.environ.get("CODEX_IMAGEGEN_MODEL", "gpt-image-2")
THRESHOLD = int(os.environ.get("CODEX_IMAGEGEN_QUALITY_THRESHOLD", "7"))
MAX_ITER = int(os.environ.get("CODEX_IMAGEGEN_MAX_ITER", "5"))

DEFAULT_PROMPT = (
    "Clean technical line drawing, white background, precise engineering illustration, "
    "no text annotations or callout numbers, no legend boxes, accurate detail"
)
DEFAULT_CRITERIA = (
    "Clean technical line art with no annotation boxes, callout numbers, or legend text. "
    "Accurate representation of the source equipment. Score 1-10."
)


def get_client() -> OpenAI:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("Error: OPENAI_API_KEY not set. Add it to your .env file.")
        sys.exit(1)
    return OpenAI(api_key=key)


def generate_image(client: OpenAI, source_path: Path, prompt: str, size: str) -> bytes:
    """Call gpt-image-2 image edit endpoint with source as reference."""
    with open(source_path, "rb") as f:
        response = client.images.edit(
            model=MODEL,
            image=f,
            prompt=prompt,
            n=1,
            size=size if size != "auto" else "1024x1024",
            response_format="b64_json",
        )
    return base64.standard_b64decode(response.data[0].b64_json)


def score_image(client: OpenAI, result_path: Path, criteria: str) -> int:
    """Use gpt-4o-mini vision to score the generated image 1-10."""
    b64 = base64.standard_b64encode(result_path.read_bytes()).decode()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        f"Evaluate this image against these criteria: {criteria}\n"
                        "Reply with ONLY a single integer from 1 to 10. No explanation."
                    )
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{b64}"}
                }
            ]
        }],
        max_tokens=5,
    )
    try:
        return int(resp.choices[0].message.content.strip())
    except (ValueError, AttributeError):
        return 5  # neutral default if parse fails


def main():
    parser = argparse.ArgumentParser(
        description="Iterative equipment diagram generator using gpt-image-2"
    )
    parser.add_argument("source", help="Source PNG path")
    parser.add_argument("output", help="Output PNG path")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--criteria", default=DEFAULT_CRITERIA)
    parser.add_argument("--max-iter", type=int, default=MAX_ITER)
    parser.add_argument("--size", default="auto",
                        choices=["auto", "1024x1024", "1024x1536", "1536x1024"])
    parser.add_argument("--no-score", action="store_true",
                        help="Skip vision scoring — single generation pass only")
    args = parser.parse_args()

    source = Path(args.source)
    output = Path(args.output)

    if not source.exists():
        print(f"Error: source file not found: {source}")
        sys.exit(1)

    output.parent.mkdir(parents=True, exist_ok=True)
    client = get_client()

    print(f"Source: {source}")
    print(f"Output: {output}")
    print(f"Model:  {MODEL}")
    print(f"Max iterations: {args.max_iter}")
    if not args.no_score:
        print(f"Quality threshold: {THRESHOLD}/10")
    print()

    prompt = args.prompt
    best_score = 0
    best_bytes = None

    for iteration in range(1, args.max_iter + 1):
        print(f"[{iteration}/{args.max_iter}] Generating...")
        try:
            img_bytes = generate_image(client, source, prompt, args.size)
        except Exception as e:
            print(f"  Error during generation: {e}")
            sys.exit(1)

        output.write_bytes(img_bytes)
        print(f"  Saved to: {output}")

        if args.no_score:
            print("  Scoring skipped (--no-score).")
            break

        print("  Scoring with gpt-4o-mini vision...")
        try:
            score = score_image(client, output, args.criteria)
        except Exception as e:
            print(f"  Scoring error (using neutral 5): {e}")
            score = 5

        print(f"  Quality score: {score}/10")

        if score > best_score:
            best_score = score
            best_bytes = img_bytes

        if score >= THRESHOLD:
            print(f"\n✓ Quality threshold ({THRESHOLD}/10) met at iteration {iteration}.")
            break

        if iteration < args.max_iter:
            prompt = (
                f"{args.prompt} "
                f"(refinement pass {iteration + 1}: higher precision, "
                f"remove any remaining text labels or annotation boxes)"
            )
            print(f"  Refining prompt for next pass...")
    else:
        if best_bytes and best_score > 0:
            output.write_bytes(best_bytes)
            print(f"\n⚠ Max iterations reached. Best result (score {best_score}/10) saved.")
        else:
            print(f"\n⚠ Max iterations reached. Last result saved.")

    print(f"\nDone: {output} ({output.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
