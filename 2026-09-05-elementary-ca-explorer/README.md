# Elementary Cellular Automaton Explorer

A single-page toy for exploring Wolfram's **elementary cellular automata** — the simplest possible
"programs": each new row is generated from the row above using only three neighboring cells
(left, self, right). There are exactly `2^8 = 256` such rules, since a rule is just a lookup table
mapping each of the 8 possible 3-cell neighborhoods to a 0 or 1 output. That entire 8-bit number
*is* the program.

## Why it's interesting

- **Rule 30** looks completely chaotic despite being fully deterministic — Mathematica actually
  uses its center column as a random-number generator.
- **Rule 90** is `left XOR right`, which quietly builds a perfect Sierpinski triangle — the same
  recurrence as Pascal's triangle mod 2.
- **Rule 110** was proven **Turing-complete** by Matthew Cook: colliding "glider" structures in its
  output can simulate any computation.
- **Rule 184** models single-lane traffic flow: a "car" cell moves right whenever the space ahead
  is empty.

The whole rule is rendered as 8 clickable truth-table tiles (the classic Wolfram diagram: three
input squares over one output square). Click any tile to flip that one output bit and watch the
entire triangular history redraw instantly — you're hand-editing the program, one bit at a time.

## How to run

Just open `index.html` in any browser. No build step, no dependencies, no network access.

```
open 2026-09-05-elementary-ca-explorer/index.html
```

## Controls

- **Rule number / slider** — jump directly to any of the 256 rules.
- **Genome tiles** — click a tile to flip that neighborhood's output bit.
- **Presets** — jump to a handful of the most famous/interesting rules (30, 54, 60, 90, 102, 110,
  122, 150, 182, 184), each with a short note on what makes it notable.
- **Seed: Single cell / Random noise** — start from one black cell in the middle (the classic
  choice) or from a fully random top row.
- **Click a cell in the canvas** — toggles that cell in the current top row and re-runs the
  simulation from there.

Grid is 181 columns wide with wrap-around (toroidal) edges, so edge effects don't dominate the
picture.
