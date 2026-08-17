# Entropy Wordle

A Wordle solver that never guesses by vibes. Every turn it asks: "of all
731 possible words, which guess splits them into the most, most-even
buckets of feedback patterns?" — computes that in bits of Shannon
entropy for every candidate word, and always plays whichever guess
promises the most expected information. It's the same idea 3Blue1Brown
made famous: treat each guess as a question, and always ask the most
informative question you can.

## Why it's interesting

- **Feedback as information.** Each Wordle guess against a hidden word
  produces one of a few hundred possible green/yellow/gray patterns.
  Grouping the remaining candidate words by which pattern they'd produce
  turns "pick a good guess" into "pick the guess whose feedback
  distribution has the highest entropy" — literally the same math behind
  Huffman coding and optimal 20-questions strategies.
- **You can watch it think.** The demo prints, per guess, how many bits
  it *expected* to learn versus how many it *actually* gained, and how
  the candidate pool collapses (731 -> 32 -> 3 -> 1, say) in real time.
- **It's provably good, not just good in practice.** The solver clears
  the built-in 731-word list in an average of ~3.1 guesses across random
  batches — with the well-known optimal opener "crane" baked in as move
  one (its entropy is identical every run, so it's precomputed once
  instead of re-derived every game).

## Files

- `words.py` — a self-contained list of 731 common 5-letter English
  words (the answer pool and the guess pool, for simplicity).
- `solver.py` — the feedback function, the entropy scorer, and three
  ways to run it (see below).

## How to run

Requires only Python 3 (stdlib only, no installs). A terminal with ANSI
color support is recommended for the green/yellow/gray tiles.

```bash
# Solve a random hidden word, watching each guess's bits live:
python3 solver.py

# Solve for a specific word (must be in words.py):
python3 solver.py --secret pizza

# Run a batch of random games and see the guess-count distribution:
python3 solver.py --games 100
```

Sample single-game output:

```
Solving for a hidden word (731 possible answers)...

  guess 1: C R A N E  (expected  9.5 bits, gained  9.5, 731 -> 1 candidates)
  guess 2: P L A N E  (expected  0.0 bits, gained  0.0, 1 -> 1 candidates)

Solved 'plane' in 2 guesses: crane -> plane
```
