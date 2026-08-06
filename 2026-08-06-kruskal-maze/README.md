# Kruskal Maze

A terminal maze generator and solver, pure-stdlib Python, 24-bit ANSI color,
no dependencies. It carves a maze with **randomized Kruskal's algorithm**
and then hunts down the exit with **breadth-first search**, animating both
phases live in place.

## Why it's interesting

Kruskal's algorithm is usually taught for minimum spanning trees, but a
maze is just a spanning tree of a grid graph — so the same algorithm builds
one for free. Every cell starts in its own disjoint set (a **union-find**
forest with path compression and union-by-rank). The program shuffles every
possible wall, then knocks one down whenever it would connect two cells
that aren't already reachable from each other — merging their sets. Skip
the wall if the cells are already in the same set — that wall would create
a loop, and a real maze wants exactly one path between any two cells. Union
by rank keeps `find()` nearly constant time even as the forest grows to
hundreds of trees merging into one.

Once the maze is a single connected tree, the solver does breadth-first
search from the top-left to the bottom-right corner, and the animation
makes something non-obvious visible: because the maze is a *tree* (no
loops), BFS can't shortcut toward the goal — it has to fan out and
exhaust entire dead-end branches before it's even allowed to backtrack
toward the exit. Watch the frontier (blue) and it's common to see it
sweep through 90%+ of the maze before the final path (gold) resolves,
even though that path itself is much shorter.

## Run it

```
python3 maze.py                          # animated 29x17 maze, random each run
python3 maze.py --seed 42                # reproducible maze
python3 maze.py --rows 12 --cols 20      # different dimensions
python3 maze.py --static                 # skip animation, jump to finished carve + solve
python3 maze.py --delay 0.05             # slower frames
```

Requires a terminal with 24-bit color support (most modern terminals
qualify). Press Ctrl+C to bail out of the animation early.
