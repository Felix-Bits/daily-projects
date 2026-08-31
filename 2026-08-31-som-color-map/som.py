#!/usr/bin/env python3
"""
Self-Organizing Map: watch a grid of "neurons" sort random RGB colors into a
smooth rainbow map with zero labels, zero backpropagation, and zero idea
of what a color even is -- just local competition and neighbor pull.

Pure stdlib, 24-bit ANSI terminal animation.
"""
import argparse
import math
import random
import sys
import time


def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v


def render(grid, width, height):
    out = ["\x1b[H"]  # cursor home (no full clear -> no flicker)
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = grid[y][x]
            r, g, b = int(clamp(r, 0, 255)), int(clamp(g, 0, 255)), int(clamp(b, 0, 255))
            row.append(f"\x1b[48;2;{r};{g};{b}m  ")
        out.append("".join(row) + "\x1b[0m\n")
    sys.stdout.write("".join(out))
    sys.stdout.flush()


def main():
    ap = argparse.ArgumentParser(description="Self-organizing map of random colors, animated in the terminal.")
    ap.add_argument("--width", type=int, default=50, help="neurons per row")
    ap.add_argument("--height", type=int, default=25, help="neurons per column")
    ap.add_argument("--iterations", type=int, default=4000, help="training steps")
    ap.add_argument("--frame-every", type=int, default=25, help="render a frame every N steps")
    ap.add_argument("--fps-delay", type=float, default=0.02, help="seconds to sleep between frames")
    ap.add_argument("--seed", type=int, default=None, help="random seed for reproducibility")
    ap.add_argument("--quiet", action="store_true", help="skip animation, just print the final map")
    args = ap.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    width, height = args.width, args.height
    grid = [[[random.uniform(0, 255) for _ in range(3)] for _ in range(width)] for _ in range(height)]

    max_radius = max(width, height) / 2.0
    time_constant = args.iterations / math.log(max_radius) if max_radius > 1 else args.iterations
    initial_lr = 0.5

    if not args.quiet:
        sys.stdout.write("\x1b[2J\x1b[H\x1b[?25l")  # clear, home, hide cursor

    try:
        for step in range(args.iterations):
            target = [random.uniform(0, 255) for _ in range(3)]

            # find best matching unit: the neuron whose weights are closest to target
            bmu_x, bmu_y, best_dist = 0, 0, float("inf")
            for y in range(height):
                row = grid[y]
                for x in range(width):
                    w = row[x]
                    d = (w[0] - target[0]) ** 2 + (w[1] - target[1]) ** 2 + (w[2] - target[2]) ** 2
                    if d < best_dist:
                        best_dist, bmu_x, bmu_y = d, x, y

            radius = max_radius * math.exp(-step / time_constant)
            lr = initial_lr * math.exp(-step / args.iterations)
            radius_sq = radius * radius

            # pull every neuron within the shrinking radius toward the target,
            # strongest at the BMU and fading out with a Gaussian falloff
            for y in range(height):
                row = grid[y]
                dy = y - bmu_y
                dy2 = dy * dy
                if dy2 > radius_sq:
                    continue
                for x in range(width):
                    dx = x - bmu_x
                    dist_sq = dx * dx + dy2
                    if dist_sq > radius_sq:
                        continue
                    influence = math.exp(-dist_sq / (2 * radius_sq)) if radius_sq > 0 else 1.0
                    w = row[x]
                    factor = lr * influence
                    w[0] += factor * (target[0] - w[0])
                    w[1] += factor * (target[1] - w[1])
                    w[2] += factor * (target[2] - w[2])

            if not args.quiet and step % args.frame_every == 0:
                render(grid, width, height)
                time.sleep(args.fps_delay)

        if not args.quiet:
            render(grid, width, height)
    finally:
        if not args.quiet:
            sys.stdout.write("\x1b[?25h")  # show cursor again
            sys.stdout.flush()

    if args.quiet:
        render(grid, width, height)

    print(f"\ndone: {args.iterations} steps, {width}x{height} neurons, "
          f"final radius {max_radius * math.exp(-args.iterations / time_constant):.2f}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write("\x1b[?25h\n")
        sys.exit(0)
