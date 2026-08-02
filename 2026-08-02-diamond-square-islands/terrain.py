#!/usr/bin/env python3
"""Procedural island generator using the diamond-square midpoint-displacement algorithm.

Pure standard library, no dependencies. Run directly with python3.
"""
import argparse
import random
import sys
import time

# Elevation bands, checked low-to-high: (upper threshold, RGB color, glyph).
BIOMES = [
    (0.32, (8, 34, 82), "≈"),      # deep ocean
    (0.42, (26, 92, 158), "≈"),    # shallow water
    (0.46, (196, 180, 128), "."),  # beach
    (0.62, (72, 148, 58), '"'),    # plains
    (0.74, (30, 96, 46), "\N{BLACK CLUB SUIT}"),  # forest
    (0.87, (118, 108, 98), "^"),   # mountains
    (2.00, (248, 248, 250), "*"),  # snow peak
]


def glyph_for(v):
    for threshold, color, ch in BIOMES:
        if v <= threshold:
            r, g, b = color
            return f"\x1b[38;2;{r};{g};{b}m{ch}\x1b[0m"
    r, g, b = BIOMES[-1][1]
    return f"\x1b[38;2;{r};{g};{b}m{BIOMES[-1][2]}\x1b[0m"


def diamond_square(n, roughness, rng, on_level=None):
    """Build a (2**n + 1)-square heightmap by recursive midpoint displacement.

    Start with four random corners. Each round alternates a "diamond" step
    (fill each square's center from its 4 corners) and a "square" step (fill
    each diamond's edge midpoints from its neighbors), halving the random
    jitter every round so detail gets finer and gentler as it's added.
    """
    size = 2 ** n + 1
    grid = [[None] * size for _ in range(size)]
    grid[0][0] = rng.uniform(0.2, 0.8)
    grid[0][size - 1] = rng.uniform(0.2, 0.8)
    grid[size - 1][0] = rng.uniform(0.2, 0.8)
    grid[size - 1][size - 1] = rng.uniform(0.2, 0.8)

    step = size - 1
    scale = 1.0
    while step > 1:
        half = step // 2

        # Diamond step: center of each step-sized square = avg of its 4 corners + noise.
        for y in range(half, size, step):
            for x in range(half, size, step):
                avg = (grid[y - half][x - half] + grid[y - half][x + half] +
                       grid[y + half][x - half] + grid[y + half][x + half]) / 4
                grid[y][x] = avg + rng.uniform(-1, 1) * scale

        # Square step: midpoint of each edge = avg of whichever of its up-to-4
        # neighbors exist (edges of the map have fewer), + noise.
        for y in range(0, size, half):
            for x in range((y + half) % step, size, step):
                total, count = 0.0, 0
                for dy, dx in ((-half, 0), (half, 0), (0, -half), (0, half)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < size and 0 <= nx < size and grid[ny][nx] is not None:
                        total += grid[ny][nx]
                        count += 1
                grid[y][x] = total / count + rng.uniform(-1, 1) * scale

        if on_level:
            sub = [[grid[y][x] for x in range(0, size, half)] for y in range(0, size, half)]
            on_level(sub)

        step = half
        scale *= 2 ** (-roughness)

    return grid, size


def render(grid):
    """Normalize a heightmap to [0, 1] and render it as colored terrain glyphs.

    Skips every other row to correct for terminal characters being roughly
    twice as tall as they are wide, so islands come out round, not squashed.
    """
    flat = [v for row in grid for v in row]
    lo, hi = min(flat), max(flat)
    span = (hi - lo) or 1e-9
    rows = grid[::2] if len(grid) > 10 else grid
    lines = ["".join(glyph_for((v - lo) / span) for v in row) for row in rows]
    return "\n".join(lines)


def print_legend():
    labels = ["deep water", "shallow water", "beach", "plains", "forest", "mountain", "snow peak"]
    parts = [f"{glyph_for(t - 0.001)} {label}" for (t, _, _), label in zip(BIOMES, labels)]
    print("  ".join(parts))


def print_stats(grid, seed, n, roughness):
    flat = [v for row in grid for v in row]
    lo, hi = min(flat), max(flat)
    span = (hi - lo) or 1e-9
    normalized = [(v - lo) / span for v in flat]
    land = sum(1 for v in normalized if v > 0.42) / len(normalized)
    print(f"\nseed={seed}  size={2 ** n + 1}x{2 ** n + 1}  roughness={roughness}  land={land:.0%}")


def main():
    parser = argparse.ArgumentParser(description="Generate an island with the diamond-square algorithm.")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed (default: random)")
    parser.add_argument("-n", "--size", type=int, default=6, help="grid is 2^n+1 across (default: 6 -> 65)")
    parser.add_argument("--roughness", type=float, default=0.55, help="0=jagged, 1=smooth (default: 0.55)")
    parser.add_argument("--static", action="store_true", help="skip the build-up animation")
    parser.add_argument("--delay", type=float, default=0.12, help="seconds between animation frames")
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randrange(1_000_000)
    rng = random.Random(seed)

    if args.static:
        grid, _ = diamond_square(args.size, args.roughness, rng)
    else:
        def on_level(sub):
            sys.stdout.write("\x1b[2J\x1b[H")
            sys.stdout.write(render(sub))
            sys.stdout.write(f"\n\x1b[0mresolution {len(sub)}x{len(sub)}\n")
            sys.stdout.flush()
            time.sleep(args.delay)

        try:
            grid, _ = diamond_square(args.size, args.roughness, rng, on_level=on_level)
        except KeyboardInterrupt:
            sys.stdout.write("\x1b[0m\n")
            return
        sys.stdout.write("\x1b[2J\x1b[H")

    print(render(grid))
    print_legend()
    print_stats(grid, seed, args.size, args.roughness)


if __name__ == "__main__":
    main()
