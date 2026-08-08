# WFC Pipe Weaver

A single-page, no-dependency canvas toy that watches **Wave Function Collapse**
generate a fully-connected pipe network from nothing but local adjacency rules.

## Why it's interesting

WFC is the algorithm behind a lot of "impossible to hand-author" procedural
content in games (Townscaper's building layouts, Bad North's islands,
countless roguelike dungeon generators). The trick: every grid cell starts as
a *superposition* of all 12 possible pipe tiles (blank, straights, corners,
T-junctions, a cross). The algorithm repeatedly

1. finds the cell with the **fewest remaining options** ("lowest entropy"),
2. **collapses** it to one tile, weighted-random among what's left, and
3. **propagates** that choice outward — every neighbor drops any tile whose
   touching edge wouldn't match, and *that* can cascade further out —

until the whole grid is collapsed. There's no global plan for "where should
the pipes go" — connectivity is a side effect of every tile's edges having to
locally agree with its neighbors, the same way Sudoku digits fall out of
purely local constraints. You can watch it happen: the highlighted cell is
the one currently being decided, and you can see constraint waves ripple
outward from each collapse. If propagation ever paints a cell into a corner
with zero valid options (a contradiction), it just throws the whole grid away
and starts over — cheap and correct, since board sizes here are tiny.

## Run it

Open `index.html` directly in any browser — pure HTML/CSS/JS, no build step,
no dependencies, no network calls. Click **Regenerate** for a new layout, or
change the speed dropdown (Slow / Normal / Fast / Instant) to control how
many cells collapse per animation frame.
