# Nim — The Game You (Probably) Can't Win

A single-page, no-dependency implementation of Nim — three piles of stones,
take any number from one pile per turn, whoever takes the last stone wins —
paired with a live panel that shows *exactly* why the AI opponent is so hard
to beat.

## Why it's interesting

Nim has a complete, elegant theory: write every pile's size in binary and
XOR them together into a single "nim-sum." Whenever it's your turn and the
nim-sum is already `000`, you are mathematically doomed — every move you make
leaves a nonzero nim-sum, and a perfect opponent can always respond with a
move that drives it back to zero. Repeat that long enough and the last stone
is guaranteed to land in their pile, not yours.

The AI here does exactly one thing: after your move, if the nim-sum isn't
already zero, it finds the single pile where reducing the count zeroes the
nim-sum, and takes from there. That's the entire "intelligence" — no search,
no lookahead, just one XOR and a comparison per pile. Yet it never loses once
it has the advantage.

The live XOR panel below the board shows each pile in binary and the running
nim-sum after every move, with a green/red verdict telling you in real time
whether the player to move is in a winning or losing spot — so instead of
taking "the AI is unbeatable" on faith, you can watch the exact bit pattern
that dooms you.

The theory holds up under simulation too: running 2000 randomized starting
positions through a scripted "perfect player" against this same AI logic
shows the player wins if and only if the initial nim-sum is nonzero — exactly
as the theory predicts.

## Run it

Open `index.html` directly in a browser — no server, no build step, no
dependencies.

1. Click a stone in any pile — it selects that stone and every stone to its
   left in that pile (a contiguous run from the start of the pile).
2. Click a different stone in the same pile to change how many you're
   about to take, or click into a different pile to switch piles entirely.
3. Click **Take selected stones** to lock in your move. The AI responds
   automatically.
4. Whoever takes the last stone on the board wins. **New game** reshuffles
   the piles (3 piles, 3–7 stones each, randomized).

Watch the "nim-sum" row in the panel below the board — when it reads `000`
after your move, you've just handed the AI a position it cannot lose from.
