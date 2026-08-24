#!/usr/bin/env python3
"""Diffusion-Limited Aggregation: grow a fractal crystal from random walkers.

Pure stdlib, no dependencies. Renders live in the terminal with 24-bit ANSI
color and half-block double vertical resolution.
"""
import argparse
import math
import random
import sys
import time

RESET = "\x1b[0m"
HIDE_CURSOR = "\x1b[?25l"
SHOW_CURSOR = "\x1b[?25h"
HOME = "\x1b[H"
CLEAR = "\x1b[2J"

NEIGHBORS_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
NEIGHBORS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def heat_color(t):
    """t in [0, 1] -> (r, g, b), deep violet core fading to bright cyan/white tips."""
    t = max(0.0, min(1.0, t))
    stops = [
        (0.00, (30, 8, 60)),
        (0.35, (90, 20, 140)),
        (0.60, (30, 90, 200)),
        (0.80, (0, 200, 220)),
        (1.00, (230, 255, 255)),
    ]
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if t0 <= t <= t1:
            f = 0 if t1 == t0 else (t - t0) / (t1 - t0)
            return tuple(round(c0[i] + f * (c1[i] - c0[i])) for i in range(3))
    return stops[-1][1]


class DLA:
    def __init__(self, size, stick_neighbors, max_walker_steps):
        self.size = size
        self.half = size // 2
        self.occupied = {}  # (x, y) -> step index at which it stuck
        self.order = []  # list of (x, y) in the order they stuck
        self.neighbor_offsets = NEIGHBORS_8 if stick_neighbors == 8 else NEIGHBORS_4
        self.max_walker_steps = max_walker_steps
        self.max_radius = 0.0
        origin = (0, 0)
        self.occupied[origin] = 0
        self.order.append(origin)

    def in_bounds(self, x, y):
        return -self.half < x < self.half and -self.half < y < self.half

    def touches_cluster(self, x, y):
        for dx, dy in self.neighbor_offsets:
            if (x + dx, y + dy) in self.occupied:
                return True
        return False

    def spawn_point(self, rng):
        spawn_r = min(self.max_radius + 8, self.half - 1)
        angle = rng.uniform(0, 2 * math.pi)
        x = round(spawn_r * math.cos(angle))
        y = round(spawn_r * math.sin(angle))
        return x, y, spawn_r

    def run_one_walker(self, rng):
        x, y, spawn_r = self.spawn_point(rng)
        kill_r = min(spawn_r * 2.5 + 10, self.half - 1)
        for _ in range(self.max_walker_steps):
            if self.touches_cluster(x, y):
                step = len(self.order)
                self.occupied[(x, y)] = step
                self.order.append((x, y))
                r = math.hypot(x, y)
                if r > self.max_radius:
                    self.max_radius = r
                return True
            dx, dy = rng.choice(self.neighbor_offsets)
            x, y = x + dx, y + dy
            r = math.hypot(x, y)
            if r > kill_r or not self.in_bounds(x, y):
                x, y, spawn_r = self.spawn_point(rng)
                kill_r = min(spawn_r * 2.5 + 10, self.half - 1)
        return False

    def render(self, total_target):
        xs = [p[0] for p in self.occupied]
        ys = [p[1] for p in self.occupied]
        margin = 2
        min_x, max_x = min(xs) - margin, max(xs) + margin
        min_y, max_y = min(ys) - margin, max(ys) + margin
        if (max_y - min_y) % 2 == 1:
            max_y += 1
        lines = []
        for y in range(min_y, max_y, 2):
            row_chars = []
            for x in range(min_x, max_x + 1):
                top_step = self.occupied.get((x, y))
                bot_step = self.occupied.get((x, y + 1))
                if top_step is None and bot_step is None:
                    row_chars.append(" ")
                    continue
                fg = heat_color(top_step / total_target) if top_step is not None else (0, 0, 0)
                bg = heat_color(bot_step / total_target) if bot_step is not None else (0, 0, 0)
                fr, fgc, fb = fg
                br, bgc, bb = bg
                if top_step is not None and bot_step is not None:
                    row_chars.append(f"\x1b[38;2;{fr};{fgc};{fb}m\x1b[48;2;{br};{bgc};{bb}m▀")
                elif top_step is not None:
                    row_chars.append(f"\x1b[38;2;{fr};{fgc};{fb}m▀")
                else:
                    row_chars.append(f"\x1b[38;2;{br};{bgc};{bb}m▄")
            lines.append("".join(row_chars) + RESET)
        return "\n".join(lines)

    def box_count_dimension(self):
        """Rough fractal dimension estimate via box counting on the final cluster."""
        pts = self.order
        sizes = [2, 4, 8, 16, 32]
        counts = []
        for box in sizes:
            boxes = set((x // box, y // box) for x, y in pts)
            counts.append(len(boxes))
        # Linear fit of log(count) vs log(1/box) -> slope is the dimension.
        xs = [math.log(1.0 / b) for b in sizes]
        ys = [math.log(c) for c in counts]
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
        den = sum((xs[i] - mx) ** 2 for i in range(n))
        return num / den if den else 0.0


def main():
    parser = argparse.ArgumentParser(description="Diffusion-Limited Aggregation crystal grower.")
    parser.add_argument("--n", type=int, default=800, help="number of particles to stick")
    parser.add_argument("--size", type=int, default=201, help="grid width/height (odd number)")
    parser.add_argument("--neighbors", type=int, choices=(4, 8), default=8, help="stick-neighborhood")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed for reproducibility")
    parser.add_argument("--no-anim", action="store_true", help="skip live animation, print final frame only")
    parser.add_argument("--render-every", type=int, default=None, help="sticks between animation frames")
    args = parser.parse_args()

    if args.size % 2 == 0:
        args.size += 1
    rng = random.Random(args.seed)
    render_every = args.render_every or max(1, args.n // 150)

    dla = DLA(args.size, args.neighbors, max_walker_steps=20000)

    if not args.no_anim:
        sys.stdout.write(HIDE_CURSOR + CLEAR)
    try:
        stuck = 1
        while stuck < args.n and dla.max_radius < dla.half - 2:
            if dla.run_one_walker(rng):
                stuck += 1
                if not args.no_anim and stuck % render_every == 0:
                    sys.stdout.write(HOME)
                    sys.stdout.write(dla.render(args.n))
                    sys.stdout.write(f"\n{RESET}particles: {stuck}/{args.n}   radius: {dla.max_radius:.1f}\n")
                    sys.stdout.flush()
        sys.stdout.write(HOME if not args.no_anim else "")
        sys.stdout.write(dla.render(max(stuck, 2)))
        dim = dla.box_count_dimension()
        sys.stdout.write(
            f"\n{RESET}particles: {stuck}   radius: {dla.max_radius:.1f}   "
            f"box-counting dimension: ~{dim:.2f}  (theoretical 2D DLA: ~1.71)\n"
        )
    finally:
        if not args.no_anim:
            sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
