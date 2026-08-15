#!/usr/bin/env python3
"""Abelian sandpile — terminal toppling-automaton visualizer.

Pure-stdlib Python, 24-bit ANSI color, no dependencies.
"""
import sys
import time
import shutil
import argparse

# Colors for grain counts 0-3 (a stable sandpile cell never holds more than 3).
COLORS = [
    (12, 12, 24),     # 0 grains -- background
    (40, 90, 210),    # 1 grain  -- blue
    (70, 190, 110),   # 2 grains -- green
    (235, 195, 45),   # 3 grains -- gold
]

RESET = "\x1b[0m"
HIDE_CURSOR = "\x1b[?25l"
SHOW_CURSOR = "\x1b[?25h"
HOME = "\x1b[H"
CLEAR = "\x1b[2J"


def make_grid(width, height):
    return [[0] * width for _ in range(height)]


def topple(grid, width, height, queue):
    """Drain every unstable (>=4 grain) cell via BFS/DFS-style flood, pure stdlib."""
    while queue:
        y, x = queue.pop()
        if grid[y][x] < 4:
            continue
        grid[y][x] -= 4
        if grid[y][x] >= 4:
            queue.append((y, x))
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width:
                grid[ny][nx] += 1
                if grid[ny][nx] >= 4:
                    queue.append((ny, nx))


def render(grid, width, height, added, total):
    """Render two simulation rows per terminal row with a half-block char,
    doubling vertical resolution the same way the doom-fire toy does."""
    out = [HOME]
    for row in range(0, height - 1, 2):
        top = grid[row]
        bottom = grid[row + 1]
        line = []
        for x in range(width):
            fr, fg, fb = COLORS[top[x]]
            br, bg, bb = COLORS[bottom[x]]
            line.append(f"\x1b[38;2;{fr};{fg};{fb}m\x1b[48;2;{br};{bg};{bb}m▀")
        out.append("".join(line) + RESET)
    out.append(f"\ngrains dropped: {added:>7}/{total}   (Ctrl+C to stop early)")
    sys.stdout.write("\n".join(out))
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser(description="Abelian sandpile terminal visualizer")
    parser.add_argument("-n", "--grains", type=int, default=None,
                         help="total grains dropped at the center "
                              "(default: sized automatically to fill the terminal)")
    parser.add_argument("--fps-cap", type=float, default=0,
                         help="min seconds between frames, 0 = as fast as possible")
    args = parser.parse_args()

    term_cols, term_rows = shutil.get_terminal_size(fallback=(120, 40))
    width = max(41, min(term_cols - 1, 121)) | 1          # odd width, has a center column
    height = (max(41, min((term_rows - 2) * 2, 121)) | 1) + 1  # even height for half-block pairing

    grid = make_grid(width, height)
    cy, cx = height // 2, width // 2

    if args.grains is not None:
        total_grains = args.grains
    else:
        # The stabilized pile's radius grows like ~0.745*sqrt(grains) (measured
        # empirically); pick a grain count that fills the grid without spilling
        # grains off its edge.
        target_span = min(width, height) - 8
        total_grains = int((target_span / 0.745) ** 2)
    batch = max(30, total_grains // 150)

    sys.stdout.write(CLEAR + HIDE_CURSOR)
    added = 0
    last_frame = 0.0
    try:
        while added < total_grains:
            queue = []
            for _ in range(batch):
                grid[cy][cx] += 1
                if grid[cy][cx] >= 4:
                    queue.append((cy, cx))
                added += 1
                if added >= total_grains:
                    break
            topple(grid, width, height, queue)

            now = time.monotonic()
            if now - last_frame >= args.fps_cap:
                render(grid, width, height, added, total_grains)
                last_frame = now
        render(grid, width, height, added, total_grains)
        print("\n\ndone -- stable pile reached." if added >= total_grains else "")
    except KeyboardInterrupt:
        render(grid, width, height, added, total_grains)
        print("\n\nstopped early.")
    finally:
        sys.stdout.write(SHOW_CURSOR + "\n")


if __name__ == "__main__":
    main()
