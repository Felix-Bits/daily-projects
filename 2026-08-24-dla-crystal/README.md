# DLA Crystal

A terminal visualizer for **Diffusion-Limited Aggregation** — the process
behind snowflakes, coral, lightning branches (Lichtenberg figures), and
mineral dendrites — pure-stdlib Python, 24-bit ANSI color, no dependencies.

## The idea

Start with one fixed seed particle. Release a new particle from a random
point on a circle around it, and let it wander in a pure random walk —
one random step at a time — until it happens to bump into the growing
cluster, where it freezes permanently. Repeat this thousands of times.

Each individual step is dumb: a coin-flip walk with zero awareness of
what's already grown. Yet the *shape* that emerges is never a blob — it's
a spindly, self-similar fractal with deep fjords and reaching branches.
The reason is a rich-get-richer effect: an outer branch tip intercepts
wandering particles before they can drift all the way into the interior,
so branches grow faster than the gaps between them ever fill in. The
result has a measurable fractal dimension of about **1.71** in 2D — more
than a line (dimension 1), less than a filled disk (dimension 2) — which
the script estimates for its own output via box-counting.

Color encodes *when* each cell stuck (a violet→blue→cyan→white gradient
from the old core to the young branch tips), so growth order is visible
at a glance even in the static final frame.

## Run it

```bash
python3 dla.py
```

That grows an 800-particle crystal with a live-updating animation in your
terminal (24-bit color required — most modern terminals support it).

Options:

```bash
python3 dla.py --n 1500              # grow more particles (slower, bigger crystal)
python3 dla.py --seed 7              # reproducible run
python3 dla.py --no-anim             # skip the animation, print only the final frame
python3 dla.py --neighbors 4         # stick on orthogonal neighbors only (blockier branches)
python3 dla.py --size 301 --n 2000   # more room to grow before hitting the simulation boundary
```

The simulation grid (`--size`) is intentionally much larger than what
gets displayed — particles need room to spawn and wander far from a
young, small cluster. The renderer automatically crops to a tight box
around the actual crystal, so the picture always fits neatly regardless
of the underlying grid size.

Takes a few seconds for the default settings; runtime grows roughly with
`n` since later particles spawn farther out and take longer walks to
find the cluster.
