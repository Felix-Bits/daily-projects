# Truchet Flow

A single-page canvas toy that turns classic [Truchet tiles](https://en.wikipedia.org/wiki/Truchet_tiles) into a continuous, river-like flow field.

## The idea

Ordinary Truchet art picks each tile's orientation with a coin flip, which gives a busy, uniformly-random maze. Here, instead, every tile's orientation is *quantized from a continuous angle* sampled from a smoothly-varying value-noise field. Because neighboring cells sample nearly the same angle, their discrete arcs chain together into long, smooth, flowing curves — like wood grain or a fingerprint — even though each tile only ever draws one of two fixed quarter-circle pairs.

The noise field slowly drifts over time, so the pattern never stops shifting, and moving the mouse locally bends the flow direction around the cursor like a current bending around an obstacle.

## Run it

Just open `index.html` in any modern browser (double-click it, or `open index.html` / `xdg-open index.html`). No build step, no dependencies.

**Controls:**
- Move the mouse to bend the flow around the cursor
- Click, or press `space`, to reseed the noise field with a brand new pattern
- `+` / `-` to change the tile size (coarser or finer weave)
