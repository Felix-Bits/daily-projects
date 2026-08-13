# Doom Fire

A terminal recreation of the classic 1993 *DOOM* title-screen fire effect,
in pure-stdlib Python.

## Why it's interesting

The fire isn't a particle system or a noise texture — it's one of the
cheapest, cleverest tricks in demoscene/game history. Every pixel just
looks at the pixel *below* it, copies its heat with a random +/- 1 wobble
and a small horizontal drift, and cools by a tiny amount. Seed the bottom
row with maximum heat and let that rule run every frame, and roaring,
flickering flame emerges from nothing but neighbor-copying — no explicit
flame model, no random noise field, just local propagation. It's a neat
example of complex-looking motion falling out of a dead-simple local rule
(same spirit as this repo's cellular-automaton and reaction-diffusion
projects, but a completely different classic algorithm).

Heat values (0-36) are mapped through the real id Software fire palette
(black -> deep red -> orange -> yellow -> white) and rendered with 24-bit
ANSI truecolor. Each terminal row draws *two* fire pixels using the
half-block character `▀` (foreground = top pixel, background = bottom
pixel), doubling the vertical resolution you'd get from one row per pixel.

## Run it

```bash
python3 fire.py
```

Press `Ctrl+C` to stop (it restores your cursor and terminal colors on
exit). Needs a truecolor-capable terminal (most modern ones are).

Optional flags:

```bash
python3 fire.py --frames 200 --fps 30   # run a fixed number of frames then exit
```
