# Butterfly Pendulums

A single-page canvas toy that puts the "butterfly effect" on screen instead of
just describing it. Two double pendulums start out with an initial angle
that differs by **0.001°** — a difference too small to see — and are then
simulated with identical physics. For the first few seconds they swing in
near-perfect lockstep. Then, because the double pendulum is a chaotic
system, the tiny initial difference gets amplified exponentially and the two
traced paths tear apart into completely different chaotic tangles, with a
live meter tracking how far apart their tips have drifted.

## Why it's interesting

Chaos theory is usually explained with the "a butterfly flapping its wings"
metaphor, but it's rare to actually *watch* sensitivity to initial
conditions happen. This does: same equations, same code path, same frame
loop — the only difference between pendulum A and B is one angle five
decimal places deep. Because the double pendulum has no closed-form
solution, the two integrated trajectories are genuinely independent chaotic
systems by the time the divergence bar fills up, even though they came from
the same source with a rounding-error-sized nudge.

The physics itself is the standard equal-mass, equal-length double pendulum
Lagrangian, integrated with RK4 (not naive Euler) so the simulation stays
numerically honest for tens of seconds instead of drifting from integration
error alone.

## How to run it

It's a single dependency-free HTML file — just open it in a browser:

```
open index.html        # macOS
xdg-open index.html    # Linux
```

or double-click `index.html` in a file browser.

- **Reset** re-releases both pendulums from the same base angle (130°) with
  the same 0.001° offset.
- **Pause** freezes the simulation so you can inspect a moment.
- **Click or drag** on the canvas to pick a new shared starting angle
  (measured from the pivot) and watch the divergence race start over.

No build step, no npm install, no network access — it's one `index.html`
with inline CSS/JS.
