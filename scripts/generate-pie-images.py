#!/usr/bin/env python3
"""Generate matching pie product photos for Kathleen's Kitchen using Gemini (nano banana).

Same method as the sibling site scripts: google.genai -> generate_content with
response_modalities=["IMAGE","TEXT"] -> save part.as_image().

Style is anchored to Kathleen's real Dutch-apple pie photo (passed in as a reference
image) so the generated pies match the existing set's look, lighting, and framing.
"""

import os
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    sys.exit("Set GEMINI_API_KEY (or GOOGLE_API_KEY) in the environment before running.")
MODEL = "gemini-2.5-flash-image"  # nano banana

client = genai.Client(api_key=API_KEY)

REPO = Path(__file__).parent.parent
IMAGES_DIR = REPO / "images"
REFERENCE = IMAGES_DIR / "dutch-apple-pie.png"  # Kathleen's real photo, used as style anchor

# Shared style rules — matched to the reference photo
FAMILY = """
You are creating product photography for a home bakery's website (Kathleen's Kitchen).
An existing reference photo of one of our pies is attached. Match it EXACTLY:

VIEW: A single whole 9-inch pie in a clear glass pie dish, shot from above at a slight
angle (near top-down), the pie filling the frame and centered — same distance and
composition as the reference.

LIGHT & BACKGROUND: Soft, warm natural daylight with gentle shadows. The pie sits on a
soft cream / blush-pink surface with a muted grey-blue linen napkin tucked under one
edge, exactly like the reference.

FEEL: Rustic, handmade, homemade — a real family bakery, NOT glossy commercial stock.
Hand-crimped, slightly imperfect crust edges. Warm, appetizing color. Shallow depth of
field. Fully photorealistic — a real photograph, NOT an illustration or 3D render.

STRICT: No text, no words, no watermark, no hands, no forks or slices removed — just the
whole pie on the surface with the napkin. Square 1:1 framing.
"""

PIES = [
    {
        "slug": "apple-pie",
        "subject": "a classic 9-inch APPLE PIE with a golden-brown woven LATTICE top crust "
                   "(distinct from a crumble top), cinnamon-spiced apple filling peeking "
                   "through the lattice gaps, edges lightly sugar-dusted.",
    },
    {
        "slug": "pumpkin-pie",
        "subject": "a 9-inch PUMPKIN PIE with a smooth, deep amber custard surface, a neatly "
                   "crimped golden crust edge, and a few small decorative pie-crust leaves on "
                   "the rim. No whipped cream, just the clean custard top.",
    },
    {
        "slug": "coconut-cream-pie",
        "subject": "a 9-inch COCONUT CREAM PIE topped with billowy swirls of fresh whipped "
                   "cream and a generous sprinkle of golden toasted coconut flakes.",
    },
    {
        "slug": "pecan-pie",
        "subject": "a 9-inch PECAN PIE, deep golden-brown and glossy. The whole pecan halves "
                   "are packed NATURALLY and densely across the top the way a real homemade "
                   "pecan pie looks — halves at all different angles, some slightly overlapping, "
                   "a few tilted or sunken into the set caramel filling, with glossy caramel "
                   "showing in the gaps between them. NOT arranged in neat concentric rings or a "
                   "perfect geometric pattern; it should look hand-placed and slightly rustic, "
                   "with a gently uneven, craggy surface.",
    },
]


def generate(pie: dict, ref_img: Image.Image) -> bool:
    slug = pie["slug"]
    out = IMAGES_DIR / f"{slug}.png"
    prompt = f"{FAMILY}\nSUBJECT: {pie['subject']}\n"
    print(f"  [gen] {slug} ...", end=" ", flush=True)
    try:
        resp = client.models.generate_content(
            model=MODEL,
            contents=[ref_img, prompt],
            config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
        )
        for part in resp.candidates[0].content.parts:
            if part.inline_data is not None:
                img = part.as_image()
                img.save(str(out))
                print(f"OK ({out.stat().st_size // 1024}KB)")
                return True
        print("FAILED (no image in response)")
        for part in resp.candidates[0].content.parts:
            if getattr(part, "text", None):
                print("    note:", part.text[:200])
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def main():
    if not REFERENCE.exists():
        print(f"Reference photo missing: {REFERENCE}")
        return 1
    ref_img = Image.open(REFERENCE)

    # Optional: pass one or more slugs as args to regenerate only those pies.
    only = set(sys.argv[1:])
    pies = [p for p in PIES if p["slug"] in only] if only else PIES

    print(f"Generating {len(pies)} pie photo(s) with {MODEL}")
    print(f"Reference: {REFERENCE.name}\nOutput: {IMAGES_DIR}\n")

    failed = []
    for i, pie in enumerate(pies, 1):
        print(f"[{i}/{len(PIES)}] {pie['slug']}")
        if not generate(pie, ref_img):
            failed.append(pie["slug"])
        if i < len(pies):
            time.sleep(4)

    for pie in [p for p in pies if p["slug"] in failed]:
        print(f"\n[retry] {pie['slug']}")
        time.sleep(5)
        if generate(pie, ref_img):
            failed.remove(pie["slug"])

    print(f"\nDone: {len(pies) - len(failed)} generated, {len(failed)} failed")
    if failed:
        print("Still failed:", ", ".join(failed))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
