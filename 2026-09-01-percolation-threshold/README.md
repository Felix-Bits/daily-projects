# Percolation Threshold

A single-page canvas visualization of **site percolation** — the statistical-physics
model behind everything from forest-fire spread to porous rock to network robustness —
built to make its central surprise visible: a genuine phase transition happening inside
a grid of independent coin flips.

## The idea

Fill an N×N grid where each cell is independently "open" with probability `p`. Ask one
question: is there a connected path of open cells running from the top row to the bottom
row?

For small `p` the answer is obviously no — open cells are scattered, isolated islands.
For large `p` it's obviously yes — almost everything is open. But the interesting part is
what happens in between: instead of the "spans / doesn't span" probability climbing
smoothly from 0 to 1, it snaps from "almost never" to "almost always" over a narrow band
of `p`, centered on a specific constant, **p<sub>c</sub> ≈ 0.592746**, for an infinite
square lattice. Nobody has ever found a closed-form formula for that number — it's known
only numerically. And as the grid gets bigger, the snap gets sharper, approaching a true
discontinuity (a step function) in the infinite-size limit — a textbook example of a
second-order phase transition, built from nothing but independent coin flips and
connectivity.

The page has three linked panels:

1. **Live grid** — a 50×50 grid you can drive with a slider, or animate with
   "Auto-sweep p: 0→1", which regenerates the grid at each step and stops the instant it
   first spans top to bottom, highlighting the spanning cluster in orange.
2. **Critical-p histogram** — every auto-sweep records the exact `p` where percolation
   first happened. Run it a few times and the values cluster tightly around the
   theoretical threshold.
3. **Finite-size scaling** — a Monte-Carlo estimate (union-find, no visualization) of the
   percolation probability curve for three grid sizes (20, 50, 80), overlaid, showing the
   transition visibly sharpen as the grid grows.

Spanning is detected with union-find (path compression + union by rank): open cells are
unioned with their open right/down neighbors, every open cell in the top row is unioned
to a virtual `TOP` node, every open cell in the bottom row to a virtual `BOTTOM` node, and
the grid percolates the instant `find(TOP) === find(BOTTOM)`.

## Run it

It's a single self-contained HTML file with no dependencies — just open it in a browser:

```
open index.html
```

(or double-click it / drag it into any browser tab).
