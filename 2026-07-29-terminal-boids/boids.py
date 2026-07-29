#!/usr/bin/env python3
"""Boids flocking simulation, rendered live in the terminal with ANSI 24-bit color.

Each boid follows three simple local rules -- separation, alignment, cohesion --
yet the flock as a whole produces emergent swarming/schooling behavior with no
central control. Watch clusters form, split, and swirl.

Run:  python3 boids.py
Quit: Ctrl+C
"""
import colorsys
import math
import random
import shutil
import sys
import time

NUM_BOIDS = 32
MAX_SPEED = 1.2
NEIGHBOR_RADIUS = 9.0
SEPARATION_RADIUS = 2.5
SEPARATION_WEIGHT = 0.06
ALIGNMENT_WEIGHT = 0.06
COHESION_WEIGHT = 0.004
FRAME_DELAY = 0.045

HEADING_CHARS = "→↗↑↖←↙↓↘"  # 8 compass directions, index by angle bucket


class Boid:
    __slots__ = ("x", "y", "vx", "vy")

    def __init__(self, width, height):
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * MAX_SPEED
        self.vy = math.sin(angle) * MAX_SPEED


def wrapped_delta(a, b, size):
    """Shortest signed distance from a to b on a wraparound axis of given size."""
    d = b - a
    if d > size / 2:
        d -= size
    elif d < -size / 2:
        d += size
    return d


def clamp_speed(vx, vy, max_speed):
    speed = math.hypot(vx, vy)
    if speed > max_speed:
        scale = max_speed / speed
        return vx * scale, vy * scale
    if speed < 1e-6:
        angle = random.uniform(0, 2 * math.pi)
        return math.cos(angle) * max_speed * 0.5, math.sin(angle) * max_speed * 0.5
    return vx, vy


def step(boids, width, height):
    for b in boids:
        sep_x = sep_y = 0.0
        align_x = align_y = 0.0
        coh_x = coh_y = 0.0
        neighbors = 0

        for other in boids:
            if other is b:
                continue
            dx = wrapped_delta(b.x, other.x, width)
            dy = wrapped_delta(b.y, other.y, height)
            dist = math.hypot(dx, dy)
            if dist < NEIGHBOR_RADIUS:
                neighbors += 1
                align_x += other.vx
                align_y += other.vy
                coh_x += dx
                coh_y += dy
                if dist < SEPARATION_RADIUS and dist > 1e-6:
                    sep_x -= dx / dist
                    sep_y -= dy / dist

        if neighbors:
            align_x /= neighbors
            align_y /= neighbors
            coh_x /= neighbors
            coh_y /= neighbors

        b.vx += sep_x * SEPARATION_WEIGHT + align_x * ALIGNMENT_WEIGHT + coh_x * COHESION_WEIGHT
        b.vy += sep_y * SEPARATION_WEIGHT + align_y * ALIGNMENT_WEIGHT + coh_y * COHESION_WEIGHT
        b.vx, b.vy = clamp_speed(b.vx, b.vy, MAX_SPEED)

    for b in boids:
        b.x = (b.x + b.vx) % width
        b.y = (b.y + b.vy) % height


def render(boids, width, height):
    grid = [[None] * width for _ in range(height)]
    for b in boids:
        col = int(b.x) % width
        row = int(b.y) % height
        angle = math.atan2(b.vy, b.vx)
        bucket = int(((angle + math.pi) / (2 * math.pi) * 8 + 0.5)) % 8
        char = HEADING_CHARS[bucket]
        hue = ((angle + math.pi) / (2 * math.pi))
        r, g, bl = colorsys.hsv_to_rgb(hue, 0.75, 1.0)
        grid[row][col] = (char, int(r * 255), int(g * 255), int(bl * 255))

    lines = []
    for row in grid:
        parts = []
        for cell in row:
            if cell is None:
                parts.append(" ")
            else:
                char, r, g, bl = cell
                parts.append(f"\x1b[38;2;{r};{g};{bl}m{char}\x1b[0m")
        lines.append("".join(parts))
    return "\n".join(lines)


def main():
    term_size = shutil.get_terminal_size(fallback=(100, 30))
    width = max(20, min(term_size.columns, 120))
    height = max(10, min(term_size.lines - 2, 40))

    boids = [Boid(width, height) for _ in range(NUM_BOIDS)]

    sys.stdout.write("\x1b[?25l")  # hide cursor
    try:
        while True:
            step(boids, width, height)
            frame = render(boids, width, height)
            sys.stdout.write("\x1b[H\x1b[J")
            sys.stdout.write(frame + "\n")
            sys.stdout.write(f"boids: {NUM_BOIDS}  (Ctrl+C to quit)\n")
            sys.stdout.flush()
            time.sleep(FRAME_DELAY)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[?25h")  # show cursor
        sys.stdout.write("\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
