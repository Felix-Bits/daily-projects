#!/usr/bin/env python3
"""Lloyd's Relaxation: watch a random scatter of points melt into a
centroidal Voronoi tessellation.

Drop N random seeds. Color every pixel by its nearest seed (that's a
Voronoi diagram). Move each seed to the centroid (center of mass) of the
pixels it owns. Repeat. The jagged random cells relax into a honeycomb of
even, soap-bubble-like regions -- the same fixed point that Lloyd's
algorithm converges to in k-means clustering, mesh generation, and blue-
noise stippling (it's literally how Photoshop-style "stipple" halftoning
and centroidal Voronoi meshes for finite-element solvers are built).

Pure stdlib, 24-bit ANSI color, no dependencies.
"""
import argparse
import math
import random
import shutil
import sys
import time

RESET = "\x1b[0m"
HIDE_CURSOR = "\x1b[?25l"
SHOW_CURSOR = "\x1b[?25h"
HOME = "\x1b[H"
CLEAR = "\x1b[2J"
GOLDEN = 0.6180339887498949


def hsl_to_rgb(h, s, l):
    h %= 1.0

    def hue2rgb(p, q, t):
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p

    if s == 0:
        r = g = b = l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue2rgb(p, q, h + 1 / 3)
        g = hue2rgb(p, q, h)
        b = hue2rgb(p, q, h - 1 / 3)
    return tuple(round(c * 255) for c in (r, g, b))


def seed_colors(n):
    return [hsl_to_rgb((i * GOLDEN) % 1.0, 0.62, 0.55) for i in range(n)]


def nearest_owners(seeds, W, H):
    owner = [[0] * W for _ in range(H)]
    for y in range(H):
        row = owner[y]
        for x in range(W):
            best_i, best_d = 0, math.inf
            for i, (sx, sy) in enumerate(seeds):
                dx, dy = x - sx, y - sy
                d = dx * dx + dy * dy
                if d < best_d:
                    best_d, best_i = d, i
            row[x] = best_i
    return owner


def centroids(owner, n, W, H):
    sx = [0.0] * n
    sy = [0.0] * n
    count = [0] * n
    for y in range(H):
        row = owner[y]
        for x in range(W):
            i = row[x]
            sx[i] += x
            sy[i] += y
            count[i] += 1
    return [
        (sx[i] / count[i], sy[i] / count[i]) if count[i] else None
        for i in range(n)
    ]


def render(owner, colors, seeds, W, H):
    dark = [tuple(c // 4 for c in col) for col in colors]
    grid = [[None] * W for _ in range(H)]
    for y in range(H):
        row = owner[y]
        for x in range(W):
            i = row[x]
            boundary = (x + 1 < W and row[x + 1] != i) or (
                y + 1 < H and owner[y + 1][x] != i
            )
            grid[y][x] = dark[i] if boundary else colors[i]
    for sx, sy in seeds:
        px, py = int(round(sx)), int(round(sy))
        if 0 <= px < W and 0 <= py < H:
            grid[py][px] = (255, 255, 255)

    lines = []
    for y in range(0, H, 2):
        parts = []
        for x in range(W):
            fr, fgc, fb = grid[y][x]
            br, bgc, bb = grid[y + 1][x] if y + 1 < H else (0, 0, 0)
            parts.append(f"\x1b[38;2;{fr};{fgc};{fb}m\x1b[48;2;{br};{bgc};{bb}m▀")
        lines.append("".join(parts) + RESET)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Lloyd's relaxation Voronoi visualizer.")
    parser.add_argument("--seeds", type=int, default=16, help="number of Voronoi seeds")
    parser.add_argument("--width", type=int, default=None, help="pixel width (cols)")
    parser.add_argument("--height", type=int, default=None, help="pixel height (rows, doubled)")
    parser.add_argument("--iterations", type=int, default=20, help="max Lloyd iterations")
    parser.add_argument("--substeps", type=int, default=5, help="animation frames per iteration")
    parser.add_argument("--fps", type=float, default=24.0, help="animation frame rate")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed for reproducibility")
    parser.add_argument("--no-anim", action="store_true", help="jump straight to convergence")
    args = parser.parse_args()

    term = shutil.get_terminal_size((100, 44))
    W = args.width or max(20, min(120, term.columns))
    H = (args.height or max(20, min(56, (term.lines - 3) * 2))) | 0
    if H % 2:
        H += 1

    rng = random.Random(args.seed)
    n = args.seeds
    seeds = [(rng.uniform(0, W - 1), rng.uniform(0, H - 1)) for _ in range(n)]
    colors = seed_colors(n)
    frame_delay = 1.0 / args.fps

    if not args.no_anim:
        sys.stdout.write(HIDE_CURSOR + CLEAR)
    try:
        it = 0
        shift = math.inf
        while it < args.iterations and shift > 0.4:
            it += 1
            owner = nearest_owners(seeds, W, H)
            targets = centroids(owner, n, W, H)
            targets = [t if t is not None else seeds[i] for i, t in enumerate(targets)]
            shift = max(math.hypot(tx - sx, ty - sy) for (sx, sy), (tx, ty) in zip(seeds, targets))

            steps = 1 if args.no_anim else args.substeps
            start = seeds
            for step in range(1, steps + 1):
                t = step / steps
                cur = [
                    (sx + (tx - sx) * t, sy + (ty - sy) * t)
                    for (sx, sy), (tx, ty) in zip(start, targets)
                ]
                if not args.no_anim:
                    frame_owner = nearest_owners(cur, W, H)
                    sys.stdout.write(HOME)
                    sys.stdout.write(render(frame_owner, colors, cur, W, H))
                    sys.stdout.write(
                        f"\n{RESET}iteration {it}/{args.iterations}   "
                        f"max centroid shift: {shift:5.2f}px\n"
                    )
                    sys.stdout.flush()
                    time.sleep(frame_delay)
            seeds = targets

        final_owner = nearest_owners(seeds, W, H)
        sys.stdout.write(HOME if not args.no_anim else "")
        sys.stdout.write(render(final_owner, colors, seeds, W, H))
        state = "converged" if shift <= 0.4 else "stopped at iteration cap"
        sys.stdout.write(f"\n{RESET}{state} after {it} iteration(s)  ({n} seeds, {W}x{H//2} cells)\n")
    finally:
        if not args.no_anim:
            sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
