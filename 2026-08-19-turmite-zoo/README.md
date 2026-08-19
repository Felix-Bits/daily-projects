# Turmite Zoo

A single-page, no-dependency canvas toy for **turmites** — Langton's Ant
generalized to an arbitrary state string. The classic Langton's Ant rule is
just two states: on a white cell turn Right, on a black cell turn Left, flip
the cell, step forward. Turmites extend that to *n* states with one rule
character per state (`R`/`L`), each state getting its own color.

## The idea

Langton's Ant is famous for one specific trick: from an empty grid, a single
ant following `RL` scribbles what looks like pure noise for roughly the
first 10,000 steps — then, out of nowhere, it locks onto a diagonal
"highway" and marches off in a straight line forever. Nobody has ever proved
*why* every known variant eventually finds order (or doesn't); it's one of
the more famous open questions in cellular automata.

This toy lets you flip between six hand-picked rule strings and watch
completely different long-run fates fall out of the same one-line update
rule:

- `RL` — the original: chaos, then a highway, forever
- `RLR` — chaos that never resolves, sprawling outward
- `LLRR` — chaos that stays contained in a roughly circular blob
- `RRLLLRLLLRRR` — grows filled triangles and spins off diagonal highways
- `LLRRRLRLRLLR` — a chaotic core that ejects a repeating scalloped highway in both directions
- `LRRRRRLLR` — floods the whole visible grid with one color, then grows coral-like branches on top

You can also drop in 2 or 4 ants on the same grid (sharing the same cell
states), which makes them steer each other via the trails they leave behind
— same rule, but now with collisions.

## Run it

Just open `index.html` in any browser — no build step, no server, no
dependencies.

- **Rule** — pick a turmite rule to watch
- **Ants** — run 1, 2, or 4 ants simultaneously on the shared grid
- **Speed** — steps simulated per animation frame
- **Play/Pause**, **Reset**

The grid wraps at the edges (a torus), which is why the `RL` highway
reappears as parallel diagonal stripes instead of a single line walking off
to infinity.

## How it works

Each cell stores a small integer state (0 = background). On every step, the
ant looks up its rule character at the cell's current state, turns left or
right accordingly, advances that cell's state by one (mod rule length), and
moves forward one cell in the new heading. Only the ant's current cell ever
changes, so each step is `O(1)` — the whole simulation is just an array
lookup, a turn, and a `fillRect`.
