# Conway's Game of Life

A single-page implementation of Conway's Game of Life using an HTML canvas and vanilla JS — no build step, no dependencies.

Each cell lives or dies based on its 8 neighbors (grid wraps at the edges): a live cell with 2-3 live neighbors survives, a dead cell with exactly 3 live neighbors is born, everything else dies. Endlessly variable behavior from three simple rules.

## Run it

Open `index.html` directly in a browser.

## Controls

- **Play/Pause** — start or stop the simulation
- **Step** — advance one generation while paused
- **Clear** — reset the board to empty
- **Random** — reseed with a random ~25% density
- **Speed slider** — generations per second (1-30)
- Click any cell to toggle it alive/dead, even while running
