# Abelian Sandpile

A terminal visualizer for the **Abelian sandpile model** (a.k.a. the
Bak–Tang–Wiesenfeld model), pure-stdlib Python, 24-bit ANSI color, no
dependencies.

## The idea

The rule is almost insultingly simple: every cell on a grid holds a stack of
sand grains. Drop a grain on a cell — if it now holds 4 or more, the cell
"topples," giving one grain to each of its four neighbors and going back to
0 (mod 4, the excess carries over). A topple can push a neighbor over the
threshold too, so one dropped grain can trigger a cascade.

Do that tens of thousands of times, always dropping at the same center
point, and something strange happens: from that single trivial local rule,
without any randomness or noise, the *global* result is an intricate,
perfectly symmetric fractal — self-similar patterned rings radiating out
from the center, made purely of cells holding 0, 1, 2, or 3 grains (a
stable pile can never hold 4+, by definition). It's a clean example of how
simple deterministic local rules can produce large-scale complexity without
anyone designing the pattern — "self-organized criticality," the same
concept behind avalanches and earthquake size distributions.

The colors here map directly to grain count: near-black for 0, blue for 1,
green for 2, gold for 3.

## Running it

```bash
python3 sandpile.py
```

It sizes the pile automatically to fill your terminal window (resize your
terminal before running for a bigger pattern) and animates the grains
dropping and the toppling cascades rippling outward, using the same
half-block double-vertical-resolution trick as some of this repo's other
terminal toys, until the whole thing settles into a stable fractal. Takes
a few seconds; press Ctrl+C to stop early and see the pile as-is.

Options:

```bash
python3 sandpile.py -n 60000      # drop a specific number of grains instead of auto-sizing
python3 sandpile.py --fps-cap 0.05  # cap redraw rate (seconds between frames) if it flickers
```

Best viewed in a terminal with true-color (24-bit) ANSI support and a
reasonably large window — the bigger the window, the more grains it drops
and the more detail the fractal shows.
