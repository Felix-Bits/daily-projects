# Braille Dither

A dependency-free CLI that generates a small grayscale test image (a shaded
sphere over a gradient background, with a sine-ripple band), runs it through
four classic dithering algorithms, and renders the resulting 1-bit bitmaps
as **Unicode Braille art** directly in your terminal.

## Why it's interesting

Braille characters (`U+2800`–`U+28FF`) encode an 8-dot pattern — a 2-column
by 4-row grid of sub-pixels — inside a single character cell. Using them as
a bitmap font gives roughly **8x the apparent resolution** of the usual
block-character (`█`/`░`) ASCII art trick, so a 160x80 dithered image still
reads clearly in a normal terminal window.

Seeing all four dithering algorithms side by side on the same image makes
their trade-offs obvious at a glance:

- **threshold** — flat black/white split, loses all gradient detail, banding
- **bayer (ordered)** — a fixed 4x4 dot pattern, uniform crosshatch texture, no error carried between pixels
- **floyd-steinberg** — classic error-diffusion, smooth gradients, some diagonal "worm" artifacts
- **atkinson** — diffuses only 6/8 of the error (the rest is simply discarded), giving the higher-contrast, punchier look classic Mac software used

No image libraries (PIL, etc.) are used anywhere — the test image, the
dithering, and the Braille packing are all plain Python.

## How to run it

```bash
python3 dither.py
```

That prints all four algorithms side by side. Useful flags:

```bash
# Custom image size (auto-rounded to multiples of 2 wide / 4 tall for clean Braille packing)
python3 dither.py --width 200 --height 100

# Just one algorithm
python3 dither.py --algo floyd-steinberg

# Also save each dithered bitmap as a plain-text .pbm file you can open elsewhere
python3 dither.py --save-dir out
```

Requires only Python 3 (tested on 3.11), no packages to install.
