# Terminal Boids

A live-in-your-terminal flocking simulation. Each "boid" follows three dead-simple
local rules — **separation** (don't crowd your neighbors), **alignment** (match
their heading), and **cohesion** (drift toward the group's center) — and yet the
flock as a whole swirls, splits, and reforms like a school of fish or a murmuration
of starlings. Nobody is in charge; the flocking is emergent from ~30 lines of
vector math applied independently to each boid, every frame.

Rendered with 24-bit ANSI color: each boid is drawn as an arrow character
(→ ↗ ↑ ↖ ← ↙ ↓ ↘) pointing in its direction of travel, colored by heading angle
so you can visually pick out sub-flocks moving together. The world wraps at the
edges (a torus), so boids that fly off one side reappear on the other.

## Why it's interesting

Flocking is a classic example of emergence: no boid knows about "the flock," only
its nearest neighbors, yet the group behavior looks purposeful and alive. Watching
it happen as colored arrows animating directly in your terminal (no GUI, no
dependencies) makes that emergence tangible in real time.

## Run it

Pure Python 3 standard library — no dependencies required.

```bash
python3 boids.py
```

Press `Ctrl+C` to quit. Works best in a terminal that supports 24-bit ("truecolor")
ANSI escapes (most modern terminals do) and is reasonably sized — the simulation
auto-sizes to your terminal window (capped at 120x40).
