# Pixel Whisper

A steganography CLI that hides a text message inside the least-significant
bits (LSBs) of an image's pixels — the picture looks completely unchanged,
but a message is smuggled inside it.

## Why it's interesting

Every pixel in an RGB image has 8 bits per channel. Flipping the very last
bit of a channel changes its value by at most 1 out of 255 — invisible to
the human eye, but perfectly readable by a program that knows to look for
it. `pixel-whisper` writes each bit of a secret message into the LSB of
successive color-channel bytes, prefixed by a 32-bit length header so
decoding knows exactly where the message ends.

It's pure Python standard library with no image dependencies at all,
because it works directly with the **PPM (P6)** format — a binary image
format so simple its entire "spec" is a text header (`P6\n<width>
<height>\n255\n`) followed by raw R,G,B bytes. No parsing library needed.

The included `diff` and `preview` commands let you prove to yourself that
the stego image is indistinguishable from the original: fewer than 0.4% of
bytes change, and every change is a delta of exactly 1.

## Files

- `stego.py` — the CLI (generate sample images, encode, decode, diff, preview)
- `sample.ppm` — a procedurally generated 160x120 cover image (gradient + checker)
- `stego.ppm` — that same image with a message already hidden inside it

## How to run

Requires only Python 3, no installs.

```bash
# Generate a fresh cover image (or reuse the included sample.ppm)
python3 stego.py gen-sample --out sample.ppm

# Hide a message inside it
python3 stego.py encode --in sample.ppm --out stego.ppm \
  --message "Meet at the old lighthouse, midnight. Bring the map."

# Extract it back out
python3 stego.py decode --in stego.ppm

# Prove the image barely changed
python3 stego.py diff sample.ppm stego.ppm
# -> 201/57600 bytes differ (0.349%), max channel delta = 1

# Look at both in your terminal (24-bit ANSI half-block rendering) —
# they should look identical
python3 stego.py preview --in sample.ppm
python3 stego.py preview --in stego.ppm
```

If you'd rather look at the images in a normal viewer, convert them with
any tool that reads PPM (e.g. `magick sample.ppm sample.png`, or GIMP).
