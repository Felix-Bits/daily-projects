# Barnes-Hut Galaxy

A single-page canvas simulation of a spiral galaxy — hundreds to thousands of
mutually-gravitating stars orbiting a central mass — driven by the same
algorithmic trick real astrophysics codes use to make N-body gravity
tractable: the **Barnes-Hut approximation**.

## Why it's interesting

Simulating gravity honestly means computing the pull between *every pair* of
bodies — O(n²) work. At a few thousand stars that's tens of millions of force
calculations per frame, every frame, forever. Real N-body codes dodge this
with a neat idea:

1. Recursively bucket all the bodies into a **quadtree**, subdividing space
   into four squares whenever a cell holds more than one body.
2. Give every internal node an aggregate mass and center of mass — a whole
   cluster of far-away stars can be treated as one heavy point.
3. When computing the force on a star, walk the tree: if a node is "far
   enough away" relative to its size (governed by the accuracy parameter
   `theta = size / distance`), just use its aggregate mass instead of
   recursing into its children.

That single trick turns an O(n²) simulation into an O(n log n) one, and
you can *see* it happening — toggle "Show quadtree" and watch the grid
subdivide densely near the crowded galactic core and stay coarse out in the
empty edges, live, every frame.

Left running, the disk of stars doesn't stay a tidy ring — individual stars
perturb their neighbors just enough that faint spiral arms and clumps
emerge on their own, the same instability that gives real spiral galaxies
their shape.

## What you can do

- **Click and drag** anywhere to fling a new star into the simulation with
  whatever velocity your drag implies.
- **Stars** slider + **New Galaxy** — regenerate with a different star count
  (try pushing it to 3000 to feel the tree's speed advantage).
- **Theta** slider — lower means more exact (falls back toward brute-force
  pairwise gravity), higher means faster and blobbier approximations.
- **Show quadtree** — overlay the live spatial partition.
- **Star trails** — toggle the motion-blur trail effect on/off.

## Run it

No build step, no dependencies — just open `index.html` in any browser:

```
open index.html
# or
python3 -m http.server 8000   # then visit http://localhost:8000
```
