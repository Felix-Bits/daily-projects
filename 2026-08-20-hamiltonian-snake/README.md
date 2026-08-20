# Hamiltonian Snake

A Snake AI that is mathematically incapable of losing.

## The idea

Classic Snake AIs chase the apple with pathfinding (A*, BFS) and eventually
corner themselves once the snake gets long enough — the shortest path to the
apple isn't always a *safe* path. This one sidesteps the whole problem: it
precomputes a **Hamiltonian cycle** through the grid — a single closed loop
that visits every cell exactly once — and the snake simply walks that loop
forever, lap after lap.

Because the snake's body is always a contiguous arc of the cycle, it can
*never* run into itself, no matter how long it gets. Apples that happen to
lie ahead on the loop get eaten as the snake passes over them. The strategy
is slow (worst case it has to walk almost the whole board to reach one
apple) but it is a guaranteed win: given enough time, the snake eats every
apple and fills all 400 cells.

The cycle itself is built with a simple zig-zag construction: column 0 goes
straight down, every other column snakes between row 1 and the bottom row,
and a final pass back along row 0 closes the loop. It's drawn faintly on the
board so you can see the track the snake is committed to.

The board ships with 4 apples on screen at once (rather than 1) purely so
growth is visible on human timescales instead of averaging one apple every
~400 moves.

## Run it

Just open `index.html` in any browser — no build step, no dependencies.

```
open index.html      # macOS
xdg-open index.html  # Linux
```

Controls:
- **Pause / Reset** — stop the loop or start a fresh snake.
- **show cycle path** — toggle the faint guide line showing the full loop.
- **speed** — steps per second.

Stats track apples eaten, total moves, board coverage, and full laps
completed.
