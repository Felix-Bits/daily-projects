#!/usr/bin/env python3
"""
Braille Dither — image dithering algorithms rendered as Unicode Braille art.

No image libraries: a small grayscale test image is generated procedurally,
run through four classic dithering algorithms, and the resulting 1-bit
bitmaps are packed into Unicode Braille characters (U+2800..U+28FF), which
pack a 2x4 grid of sub-pixels into a single terminal cell. That gives roughly
8x the apparent resolution of a plain block-character render, so a fairly
detailed image fits in a normal terminal window.

Run with no arguments for a demo image + side-by-side comparison of:
  threshold | bayer (ordered) | floyd-steinberg | atkinson
"""
import argparse
import math
import os

ALGORITHMS = ["threshold", "bayer", "floyd-steinberg", "atkinson"]

BAYER4 = [
    [0, 8, 2, 10],
    [12, 4, 14, 6],
    [3, 11, 1, 9],
    [15, 7, 13, 5],
]


def make_test_image(width, height):
    """Procedural grayscale image: soft gradient backdrop + a shaded sphere
    + a sine ripple band, so every dithering algorithm has smooth gradients,
    flat regions, and fine detail to struggle with."""
    img = [[0.0] * width for _ in range(height)]
    cx, cy, r = width * 0.62, height * 0.45, min(width, height) * 0.30
    for y in range(height):
        for x in range(width):
            # background: diagonal gradient
            bg = (x / width) * 0.5 + (y / height) * 0.2

            # shaded sphere (simple fake-Lambertian lighting)
            dx, dy = (x - cx) / r, (y - cy) / r
            d2 = dx * dx + dy * dy
            sphere = None
            if d2 <= 1.0:
                dz = math.sqrt(1.0 - d2)
                # light coming from upper-left
                lx, ly, lz = -0.5, -0.6, 0.62
                nl = dx * lx + dy * ly + dz * lz
                sphere = max(0.0, nl) ** 1.4

            # sine ripple band near the bottom
            ripple = 0.5 + 0.5 * math.sin(x * 0.35 + y * 0.12)
            band = ripple if y > height * 0.78 else None

            if sphere is not None:
                v = 0.15 + 0.85 * sphere
            elif band is not None:
                v = 0.25 + 0.5 * band
            else:
                v = bg
            img[y][x] = min(1.0, max(0.0, v))
    return img


def clone(img):
    return [row[:] for row in img]


def dither_threshold(img):
    h, w = len(img), len(img[0])
    return [[1 if img[y][x] < 0.5 else 0 for x in range(w)] for y in range(h)]


def dither_bayer(img):
    h, w = len(img), len(img[0])
    out = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            t = (BAYER4[y % 4][x % 4] + 0.5) / 16.0
            out[y][x] = 1 if img[y][x] < t else 0
    return out


def dither_error_diffusion(img, pattern):
    """pattern: list of (dx, dy, weight) fractions of quantization error to push forward."""
    h, w = len(img), len(img[0])
    buf = clone(img)
    out = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            old = buf[y][x]
            new = 1.0 if old >= 0.5 else 0.0
            out[y][x] = 0 if new else 1  # 1 == "ink" (dark pixel)
            err = old - new
            for dx, dy, wgt in pattern:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    buf[ny][nx] += err * wgt
    return out


FLOYD_STEINBERG_PATTERN = [
    (1, 0, 7 / 16),
    (-1, 1, 3 / 16),
    (0, 1, 5 / 16),
    (1, 1, 1 / 16),
]

ATKINSON_PATTERN = [
    (1, 0, 1 / 8),
    (2, 0, 1 / 8),
    (-1, 1, 1 / 8),
    (0, 1, 1 / 8),
    (1, 1, 1 / 8),
    (0, 2, 1 / 8),
]


def run_dither(name, img):
    if name == "threshold":
        return dither_threshold(img)
    if name == "bayer":
        return dither_bayer(img)
    if name == "floyd-steinberg":
        return dither_error_diffusion(img, FLOYD_STEINBERG_PATTERN)
    if name == "atkinson":
        return dither_error_diffusion(img, ATKINSON_PATTERN)
    raise ValueError(f"unknown algorithm: {name}")


def to_braille(bitmap):
    """Pack a 1-bit bitmap (1 = ink) into Braille characters, 2 cols x 4 rows per char."""
    h, w = len(bitmap), len(bitmap[0])
    dot_bits = [
        (0, 0, 0x01), (0, 1, 0x02), (0, 2, 0x04), (0, 3, 0x40),
        (1, 0, 0x08), (1, 1, 0x10), (1, 2, 0x20), (1, 3, 0x80),
    ]
    lines = []
    for cy in range(0, h, 4):
        chars = []
        for cx in range(0, w, 2):
            mask = 0
            for ox, oy, bit in dot_bits:
                px, py = cx + ox, cy + oy
                if py < h and px < w and bitmap[py][px]:
                    mask |= bit
            chars.append(chr(0x2800 + mask))
        lines.append("".join(chars))
    return "\n".join(lines)


def side_by_side(blocks, headers, gap="   "):
    grids = [b.split("\n") for b in blocks]
    height = max(len(g) for g in grids)
    col_widths = [max(len(line) for line in g) for g in grids]
    out_lines = []
    header_line = gap.join(h.center(w) for h, w in zip(headers, col_widths))
    out_lines.append(header_line)
    for i in range(height):
        row = []
        for g, w in zip(grids, col_widths):
            cell = g[i] if i < len(g) else ""
            row.append(cell.ljust(w))
        out_lines.append(gap.join(row))
    return "\n".join(out_lines)


def write_pbm(path, bitmap):
    """Plain-text PBM (P1): '1' = black ink, '0' = white. No deps required."""
    h, w = len(bitmap), len(bitmap[0])
    with open(path, "w") as f:
        f.write("P1\n")
        f.write(f"{w} {h}\n")
        for row in bitmap:
            f.write(" ".join(str(v) for v in row) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Dither a procedural test image and render it with Unicode Braille art.")
    parser.add_argument("--width", type=int, default=160, help="image width in pixels (default 160)")
    parser.add_argument("--height", type=int, default=80, help="image height in pixels (default 80)")
    parser.add_argument("--algo", choices=ALGORITHMS + ["all"], default="all")
    parser.add_argument("--save-dir", default=None, help="also write .pbm bitmap files here")
    args = parser.parse_args()

    # Braille needs width/height to be multiples of 2/4 for clean packing.
    width = args.width - (args.width % 2)
    height = args.height - (args.height % 4)

    img = make_test_image(width, height)
    algos = ALGORITHMS if args.algo == "all" else [args.algo]

    blocks, headers = [], []
    for name in algos:
        bitmap = run_dither(name, img)
        blocks.append(to_braille(bitmap))
        headers.append(name)
        if args.save_dir:
            os.makedirs(args.save_dir, exist_ok=True)
            write_pbm(os.path.join(args.save_dir, f"{name}.pbm"), bitmap)

    if len(blocks) == 1:
        print(headers[0])
        print(blocks[0])
    else:
        print(side_by_side(blocks, headers))


if __name__ == "__main__":
    main()
