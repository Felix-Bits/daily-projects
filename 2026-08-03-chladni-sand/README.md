# Chladni Sand

A single-page canvas toy that makes standing sound waves visible, the way
physicist Ernst Chladni did in 1787: scatter sand on a vibrating plate and
watch it settle into geometric patterns along the lines that aren't moving.

## Why it's interesting

There's no image, no noise function, no pre-baked pattern here — just one
equation and a random walk:

```
U(x, y) = cos(nπx)·cos(mπy) − cos(mπx)·cos(nπy)
```

`U` is the displacement of a square plate vibrating in eigenmode `(n, m)`.
Where `U ≈ 0`, the plate is momentarily still — those are the **nodal
lines**. Everywhere else it's shaking, more violently the further `|U|` is
from zero.

Each of the 6000 grains takes a tiny random step every frame, but the *size*
of that step is scaled by `|U|` at its current position. Grains sitting on
an antinode get flung around almost every frame; grains near a node barely
move at all. No grain is ever told where to go — the pattern is just what's
left after everywhere-that-isn't-a-node keeps getting stirred. Change `n` or
`m` by one and the whole figure reorganizes into a completely different
symmetry, the same way a real Chladni plate leaps between figures as you
sweep a violin bow across it at different frequencies.

## Run it

Just open the file in a browser — no server, no build step, no dependencies:

```
open 2026-08-03-chladni-sand/index.html
```

(or `xdg-open` / drag it into a browser tab).

Drag **mode n** / **mode m** to pick a vibration mode, **jitter** to control
how hard the plate shakes, **shuffle sand** to re-scatter the grains and
watch a fresh pattern emerge, and **pause** to freeze the current figure.
