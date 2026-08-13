#!/usr/bin/env python3
"""Doom-style ASCII fire in the terminal, pure stdlib.

Classic per-pixel fire propagation algorithm (as used in the 1993 DOOM
title screen): each pixel's "heat" spreads upward from the row below it,
with a random horizontal drift and a random chance to cool by one step.
Heat values map through a 37-color fire palette (black -> red -> orange
-> yellow -> white) rendered with 24-bit ANSI color.

Usage:
    python3 fire.py              # run until Ctrl+C
    python3 fire.py --frames 50  # run exactly 50 frames then exit (for testing)
"""
import argparse
import random
import shutil
import sys
import time

PALETTE = [
    (0x07, 0x07, 0x07), (0x1F, 0x07, 0x07), (0x2F, 0x0F, 0x07), (0x47, 0x0F, 0x07),
    (0x57, 0x17, 0x07), (0x67, 0x1F, 0x07), (0x77, 0x1F, 0x07), (0x8F, 0x27, 0x07),
    (0x9F, 0x2F, 0x07), (0xAF, 0x3F, 0x07), (0xBF, 0x47, 0x07), (0xC7, 0x47, 0x07),
    (0xDF, 0x4F, 0x07), (0xDF, 0x57, 0x07), (0xDF, 0x57, 0x07), (0xD7, 0x5F, 0x07),
    (0xD7, 0x5F, 0x07), (0xD7, 0x67, 0x0F), (0xCF, 0x6F, 0x0F), (0xCF, 0x77, 0x0F),
    (0xCF, 0x7F, 0x0F), (0xCF, 0x87, 0x17), (0xC7, 0x87, 0x17), (0xC7, 0x8F, 0x17),
    (0xC7, 0x97, 0x1F), (0xBF, 0x9F, 0x1F), (0xBF, 0x9F, 0x1F), (0xBF, 0xA7, 0x27),
    (0xBF, 0xA7, 0x27), (0xBF, 0xAF, 0x2F), (0xB7, 0xAF, 0x2F), (0xB7, 0xB7, 0x2F),
    (0xB7, 0xB7, 0x37), (0xCF, 0xCF, 0x6F), (0xDF, 0xDF, 0x9F), (0xEF, 0xEF, 0xC7),
    (0xFF, 0xFF, 0xFF),
]
MAX_HEAT = len(PALETTE) - 1


def spread_fire(fire, src, width):
    heat = fire[src]
    if heat == 0:
        fire[src - width] = 0
        return
    drift = random.randint(0, 3)
    dst = src - drift + 1
    if 0 <= dst - width < len(fire):
        fire[dst - width] = max(0, heat - (drift & 1))


def render_frame(fire, width, height):
    rows = []
    for r in range(height // 2):
        top_row, bot_row = 2 * r, 2 * r + 1
        chars = []
        for x in range(width):
            tr, tg, tb = PALETTE[fire[top_row * width + x]]
            br, bg, bb = PALETTE[fire[bot_row * width + x]]
            chars.append(f"\x1b[38;2;{tr};{tg};{tb}m\x1b[48;2;{br};{bg};{bb}m▀")
        rows.append("".join(chars) + "\x1b[0m")
    return "\x1b[H" + "\n".join(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=0, help="run N frames then exit (0 = forever)")
    parser.add_argument("--fps", type=float, default=24.0, help="target frames per second")
    args = parser.parse_args()

    cols, rows = shutil.get_terminal_size((80, 24))
    width = max(20, min(cols, 100))
    height = max(20, min(rows * 2, 80))
    fire = [0] * (width * height)
    for x in range(width):
        fire[(height - 1) * width + x] = MAX_HEAT

    sys.stdout.write("\x1b[2J\x1b[?25l")
    frame_count = 0
    try:
        while args.frames == 0 or frame_count < args.frames:
            for x in range(width):
                for y in range(1, height):
                    spread_fire(fire, y * width + x, width)
            sys.stdout.write(render_frame(fire, width, height))
            sys.stdout.flush()
            frame_count += 1
            time.sleep(1.0 / args.fps)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[0m\x1b[?25h\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
