# Wireworld

A single-page interactive simulator for **Wireworld**, a cellular automaton
with only four cell states and one transition rule — and yet it's Turing
complete. People have built full 8-bit computers, one electron pulse at a
time, inside this exact rule set.

## The idea

Every cell is one of:

- **empty** — does nothing, forever
- **conductor** (copper) — turns into an electron head if exactly 1 or 2 of
  its 8 neighbors are electron heads, otherwise stays conductor
- **electron head** — always decays into an electron tail next tick
- **electron tail** — always decays into conductor next tick

That's the entire rule. From it you get one-way electron flow along wires,
signals that split cleanly at a T-junction, and — if you're not careful —
signals that duplicate or annihilate themselves at a plain right-angle
corner. That last one isn't a bug in this implementation; it's a real,
well-known property of Wireworld (a lone pulse hitting a 90° bend excites
both of the corner's neighbors, sending a copy each way, which then collide
on the far side and cancel out). It's *why* real Wireworld circuit
designers route wires diagonally. There's a preset that shows exactly this
happening, on purpose, so you can watch it fizzle out.

I verified the trickier patterns (the self-sustaining loop and the
T-splitter) against a small Python reference simulation before wiring them
into the page, specifically because right-angle corners in this CA are a
known gotcha and I didn't want to ship a "clock" that silently dies after
a few dozen frames.

## What's in it

- A 80×50 canvas grid you draw on directly (click/drag with a brush:
  Wire, Electron, or Erase)
- Play/Pause, single Step, adjustable speed, and Clear
- Five presets:
  - **Straight pulse** — one electron traveling down a plain wire
  - **Diamond clock** — a diagonal-cornered loop that circulates a single
    pulse forever (no decay, no duplication — verified for 200+ generations)
  - **T-splitter** — one incoming pulse becomes two outgoing pulses
  - **Right-angle corner (buggy!)** — the classic failure mode described
    above, so you can see why it happens
  - **Two clocks, different periods** — two loops of different sizes
    ticking out of phase, just because it's pleasant to watch

## Run it

It's a single static HTML file with no dependencies — just open it in a
browser:

```
open index.html        # macOS
xdg-open index.html    # Linux
```

or serve it locally (`python3 -m http.server` in this folder) and visit
`http://localhost:8000`.
