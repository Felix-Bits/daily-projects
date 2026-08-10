# Strange Attractor Explorer

A single-page, no-dependency canvas toy that renders **strange attractors** —
the intricate, never-repeating shapes traced out by simple iterated maps like
`x' = sin(a·y) - cos(b·x)`. Four numbers and one formula, applied three
million times in a row, produce fractal-looking clouds and ribbons that look
hand-drawn but are 100% deterministic.

## Why it's interesting

There's no randomness in the picture itself — every pixel's brightness is
just a count of how often the same four-parameter formula, iterated from a
fixed starting point, happened to land there. Tiny changes to `a`, `b`, `c`,
`d` swing the result from a boring straight line to a dense, wing-like cloud
to a fine lattice of nested curves, with no way to predict which from the
numbers alone — you just have to run it and look.

The fun part was making "New Attractor" reliably interesting instead of a
coin flip. Most random `(a, b, c, d)` draws for these formulas produce either
a divergent mess or a handful of thin, periodic loops that don't fill any
real area — visually boring. So each click does a fast 20,000-point probe
run, buckets the points into a coarse 40×40 grid, and rejects the draw
unless it covers at least a quarter of the grid — a cheap proxy for "this is
a genuine 2D chaotic attractor, not a degenerate cycle." Rejected draws are
retried (up to 400 times) until a good one is found, all in a few
milliseconds.

Four classic attractor families are included, each with its own character:

- **De Jong** — trig-only, often produces wide layered "wings"
- **Clifford** — De Jong's cousin with an extra linear term, tends toward
  ribbon-like spirals
- **Svensson** — frequently forms ring / donut shapes
- **Bedhead** — coupled `x`/`y` terms, produces twisting, asymmetric braids

## How to run it

Open `index.html` in any browser — no server, build step, or dependencies
needed.

- **New Attractor** — picks a new random attractor within the selected
  family
- **Family dropdown** — switch between De Jong, Clifford, Svensson, Bedhead
- **Cycle Palette** — recolors the *current* shape without rerolling it
- **Download PNG** — saves the current canvas as an image

Each render plots 3,000,000 points into a 900×900 density grid, then maps
point-count to color on a logarithmic scale (so both the faint outer wisps
and the dense fractal core stay visible) — all synchronous, all done in well
under a second.
