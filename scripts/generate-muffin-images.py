#!/usr/bin/env python3
"""Generate matching muffin product photos for Kathleen's Kitchen using Gemini (nano banana).

Same method as generate-pie-images.py, but the reference image is Kathleen's OWN phone
photo of each muffin (passed in as the content anchor) so the result is genuinely her
muffin — just cleaned up and restyled onto the site's cream/blush product-photo surface
so it matches the pie family's look, lighting, and framing.

Pass the two reference photos via env or edit REFS below. Usage:
    GEMINI_API_KEY=... python3 scripts/generate-muffin-images.py [slug ...]
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

# Kathleen's real phone photos, used as the content reference for each muffin.
# Override with MUFFIN_REF_DIR if the photos live elsewhere.
REF_DIR = Path(os.environ.get("MUFFIN_REF_DIR", REPO / "scripts" / "muffin-refs"))

# Shared style rules — matched to the pie photos (dutch-apple family).
FAMILY = """
You are creating product photography for a home bakery's website (Kathleen's Kitchen).
The attached photo is the ACTUAL muffin to feature — keep its type, color, crumb, and the
natural brown parchment tulip wrapper. Do not turn it into a different baked good.

Recreate it as a clean, appetizing product photo that matches the rest of our site:

VIEW: A single whole muffin in its brown parchment tulip liner, shot from above at a slight
angle (near top-down), the muffin filling the frame and centered.

LIGHT & BACKGROUND: Soft, warm natural daylight with gentle shadows. Place it on a soft
cream / blush-pink surface with a muted grey-blue linen napkin tucked under one edge.
Remove the busy granite/marble countertop from the original — replace with the clean
cream/blush surface.

FEEL: Rustic, handmade, homemade — a real family bakery, NOT glossy commercial stock.
Warm, appetizing color. Shallow depth of field. Fully photorealistic — a real photograph,
NOT an illustration or 3D render.

STRICT: No text, no words, no watermark, no hands. Just the one muffin on the surface with
the napkin. Square 1:1 framing.
"""

MUFFINS = [
    {
        "slug": "pumpkin-choc-chip-muffins",
        "ref": "pumpkin-muffin-ref.png",
        "subject": "a PUMPKIN CHOCOLATE CHIP MUFFIN — a warm orange-gold pumpkin-spice muffin "
                   "with a domed top studded with dark chocolate chips.",
    },
    {
        "slug": "chocolate-choc-chip-muffins",
        "ref": "chocolate-muffin-ref.png",
        "subject": "a CHOCOLATE CHOCOLATE CHIP MUFFIN — a rich dark-brown chocolate muffin with "
                   "a domed, slightly craggy top and chocolate chips throughout.",
    },
]


def generate(m: dict) -> bool:
    slug = m["slug"]
    out = IMAGES_DIR / f"{slug}.png"
    ref_path = REF_DIR / m["ref"]
    if not ref_path.exists():
        print(f"  [skip] {slug}: reference photo missing at {ref_path}")
        return False
    ref_img = Image.open(ref_path)
    prompt = f"{FAMILY}\nSUBJECT: {m['subject']}\n"
    print(f"  [gen] {slug} ...", end=" ", flush=True)
    try:
        resp = client.models.generate_content(
            model=MODEL,
            contents=[ref_img, prompt],
            config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
        )
        for part in resp.candidates[0].content.parts:
            if part.inline_data is not None:
                part.as_image().save(str(out))
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
    only = set(sys.argv[1:])
    muffins = [m for m in MUFFINS if m["slug"] in only] if only else MUFFINS
    print(f"Generating {len(muffins)} muffin photo(s) with {MODEL}")
    print(f"Reference dir: {REF_DIR}\nOutput: {IMAGES_DIR}\n")
    failed = []
    for i, m in enumerate(muffins, 1):
        print(f"[{i}/{len(muffins)}] {m['slug']}")
        if not generate(m):
            failed.append(m["slug"])
        if i < len(muffins):
            time.sleep(4)
    print(f"\nDone: {len(muffins) - len(failed)} generated, {len(failed)} failed")
    if failed:
        print("Still failed:", ", ".join(failed))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
