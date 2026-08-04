# Reaction-Diffusion Lab

A single-page canvas toy that simulates the **Gray-Scott reaction-diffusion
model** — the same class of chemistry that Alan Turing proposed in 1952 to
explain how patterns like leopard spots and zebra stripes emerge from
nothing but two diffusing, reacting chemicals.

## Why it's interesting

Two virtual chemicals, `U` and `V`, spread across a grid and react with each
other. The whole system is governed by just two numbers: a **feed rate**
(how fast U is replenished) and a **kill rate** (how fast V is removed).
Nudge those two knobs and the *exact same equation* produces wildly
different emergent behavior — self-replicating blobs that split like cells
(mitosis), squirming worms, stable leopard spots, or coral-reef mazes —
with no randomness or hand-authored rules involved. It's a nice reminder
that complex, organic-looking structure can fall straight out of simple
local math.

The simulation runs on a 220×132 grid using flat `Float32Array` buffers and
a precomputed wrapped-neighbor lookup so the whole thing stays smooth in
plain JavaScript with no dependencies.

## How to run it

Open `index.html` in any modern browser (double-click it, or run a local
server if you prefer):

```bash
open index.html          # macOS
xdg-open index.html      # Linux
```

- Click the preset buttons (**Coral, Mitosis, Worms, Spots, Waves,
  Holes**) to jump between different feed/kill parameter sets — each
  resets the grid and reseeds it.
- **Click or drag** anywhere on the canvas to inject fresh chemical and
  watch new growth spread from your cursor.
- Use **Reset** to reseed the current pattern, **Pause/Play** to freeze
  the simulation, and the **speed** slider to change how many simulation
  steps run per animation frame.
