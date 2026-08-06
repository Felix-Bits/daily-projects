#!/usr/bin/env python3
"""Maze generation and solving, made visible.

Carves a maze with randomized Kruskal's algorithm (a disjoint-set / union-find
forest merging cell by cell) and then solves it with breadth-first search,
animating both phases in the terminal with 24-bit ANSI color.

Pure standard library, no dependencies.
"""
import argparse
import random
import sys
import time
from collections import deque

WALL_COLOR = (40, 46, 74)
START_COLOR = (70, 210, 120)
END_COLOR = (230, 90, 90)
FRONTIER_COLOR = (60, 130, 210)
VISITED_COLOR = (30, 70, 120)
PATH_COLOR = (250, 190, 60)


class UnionFind:
    """Disjoint-set forest with path compression and union by rank."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def render(grid, rows, cols, highlights, message):
    """Redraw the whole maze in place. Each grid char prints as a 2-wide
    block so cells read roughly square in a normal terminal font."""
    markers = {
        (1, 1): START_COLOR,
        (2 * rows - 1, 2 * cols - 1): END_COLOR,
    }
    out = ["\x1b[2J\x1b[H", message, "\n\n"]
    for gr, row in enumerate(grid):
        for gc, ch in enumerate(row):
            color = markers.get((gr, gc)) or highlights.get((gr, gc))
            if ch == "#":
                r, g, b = WALL_COLOR
                out.append(f"\x1b[38;2;{r};{g};{b}m██\x1b[0m")
            elif color:
                r, g, b = color
                out.append(f"\x1b[48;2;{r};{g};{b}m  \x1b[0m")
            else:
                out.append("  ")
        out.append("\n")
    sys.stdout.write("".join(out))
    sys.stdout.flush()


def build_grid(rows, cols):
    gw, gh = 2 * cols + 1, 2 * rows + 1
    grid = [["#"] * gw for _ in range(gh)]
    for r in range(rows):
        for c in range(cols):
            grid[2 * r + 1][2 * c + 1] = " "
    return grid


def generate_maze(rows, cols, rng, delay):
    grid = build_grid(rows, cols)
    uf = UnionFind(rows * cols)
    edges = []
    for r in range(rows):
        for c in range(cols):
            if c + 1 < cols:
                edges.append((r * cols + c, r * cols + c + 1, r, c, r, c + 1))
            if r + 1 < rows:
                edges.append((r * cols + c, (r + 1) * cols + c, r, c, r + 1, c))
    rng.shuffle(edges)

    total = rows * cols - 1
    opened = 0
    frame_every = max(1, total // 60)
    for a, b, r, c, nr, nc in edges:
        if uf.union(a, b):
            grid[r + nr + 1][c + nc + 1] = " "
            opened += 1
            if opened % frame_every == 0 or opened == total:
                render(grid, rows, cols, {}, f"carving maze with randomized Kruskal's algorithm... {opened}/{total}")
                time.sleep(delay)
        if opened == total:
            break
    render(grid, rows, cols, {}, f"maze complete — {total} walls removed, {rows * cols} cells, one unique path between any two")
    return grid


def neighbors(grid, rows, cols, cell):
    r, c = cell
    for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
        if 0 <= nr < rows and 0 <= nc < cols and grid[r + nr + 1][c + nc + 1] == " ":
            yield nr, nc


def solve_maze(grid, rows, cols, delay):
    start, end = (0, 0), (rows - 1, cols - 1)
    parent = {start: None}
    frontier = deque([start])
    highlights = {}

    step = 0
    while frontier:
        cell = frontier.popleft()
        r, c = cell
        highlights[(2 * r + 1, 2 * c + 1)] = VISITED_COLOR
        if cell == end:
            break
        for nb in neighbors(grid, rows, cols, cell):
            if nb not in parent:
                parent[nb] = cell
                nr, nc = nb
                highlights[(r + nr + 1, c + nc + 1)] = FRONTIER_COLOR
                highlights[(2 * nr + 1, 2 * nc + 1)] = FRONTIER_COLOR
                frontier.append(nb)
        step += 1
        if step % 2 == 0:
            render(grid, rows, cols, highlights, "solving with breadth-first search — frontier expanding outward...")
            time.sleep(delay)

    render(grid, rows, cols, highlights, "solving with breadth-first search — target reached")
    time.sleep(delay * 4)

    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()

    for i in range(len(path) - 1):
        r, c = path[i]
        nr, nc = path[i + 1]
        highlights[(2 * r + 1, 2 * c + 1)] = PATH_COLOR
        highlights[(r + nr + 1, c + nc + 1)] = PATH_COLOR
    highlights[(2 * end[0] + 1, 2 * end[1] + 1)] = PATH_COLOR

    render(
        grid, rows, cols, highlights,
        f"shortest path found — {len(path) - 1} steps long; BFS had to visit {len(parent)} of {rows * cols} cells to be sure",
    )
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=17, help="maze height in cells (default 17)")
    parser.add_argument("--cols", type=int, default=29, help="maze width in cells (default 29)")
    parser.add_argument("--seed", type=int, default=None, help="random seed for a reproducible maze")
    parser.add_argument("--delay", type=float, default=0.02, help="seconds between animation frames (default 0.02)")
    parser.add_argument("--static", action="store_true", help="skip animation, just print generation then solution")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    delay = 0 if args.static else args.delay

    try:
        grid = generate_maze(args.rows, args.cols, rng, delay)
        time.sleep(0 if args.static else 0.6)
        solve_maze(grid, args.rows, args.cols, delay)
        print()
    except KeyboardInterrupt:
        print("\n\x1b[0mbailed out early")


if __name__ == "__main__":
    main()
