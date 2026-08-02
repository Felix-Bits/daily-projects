# Diamond-Square Islands

A terminal island generator built on the **diamond-square** algorithm — the
same recursive midpoint-displacement trick used in classic terrain generators
like Populous. Pure-stdlib Python, 24-bit ANSI color, no dependencies.

## Why it's interesting

Start with four corners of a grid set to random heights. Then repeat two
steps, each time at half the spacing and half the randomness of the last:

- **Diamond step** — the center of each square becomes the average of its
  4 corners, plus a shrinking random jitter.
- **Square step** — the midpoint of each edge becomes the average of its
  (up to 4) neighbors, plus the same jitter.

That's the entire algorithm — no noise functions, no gradients, nothing
borrowed from Perlin/Simplex. Just averaging and shrinking randomness,
applied recursively, and yet it produces convincing coastlines, mountain
ranges, and lakes every time. The default mode animates the build-up so you
can watch a 3x3 grid of blocky guesses refine into a detailed 65x65 island
over a handful of frames — the recursion is the show.

Elevation is mapped to seven biome bands (deep water, shallow water, beach,
plains, forest, mountain, snow peak), each with its own glyph and true-color
ANSI fill.

## Run it

```
python3 terrain.py                    # animated build-up, random island each time
python3 terrain.py --seed 42          # reproducible island
python3 terrain.py --static           # skip the animation, print the final map
python3 terrain.py -n 7               # bigger grid (2^n+1 across, default n=6 -> 65x65)
python3 terrain.py --roughness 0.3    # lower = jagged/mountainous, higher = smoother
```

Requires a terminal with 24-bit color support (most modern terminals
qualify). Press Ctrl+C to bail out of the animation early.
