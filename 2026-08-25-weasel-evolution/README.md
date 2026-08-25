# Weasel Evolution

A terminal recreation of Richard Dawkins' "Weasel" program from *The Blind
Watchmaker* — the classic thought experiment showing why "evolution by pure
chance" and "evolution by cumulative selection" are wildly different things,
even though both use only random mutation.

## What it does

Starting from a completely random string, the program repeatedly:

1. Spawns a litter of mutant children from the current best string (each
   character has a small chance of randomly changing).
2. Scores every child by how many characters match the target phrase in the
   right position.
3. Keeps whichever string — parent or child — scored highest, and discards
   the rest.

No child is "trying" to reach the target and no lookahead is involved; each
generation only ever compares against the immediately preceding one. Yet the
default phrase `METHINKS IT IS LIKE A WEASEL` (28 characters, 27-symbol
alphabet) reliably assembles itself in well under 100 generations — a
fraction of a second — instead of the ~10^40 tries pure random guessing would
need on average.

That contrast is the whole point: single-step selection (keep generating
random 28-character strings until one matches) is astronomically hopeless,
but *cumulative* selection (keep small improvements, discard the rest, repeat)
turns the same random mutation into a fast, effective search. The program
prints both numbers so the gap is visible, not just asserted.

## Run it

Requires only Python 3 (pure standard library, no dependencies).

```bash
python3 weasel.py
```

Watch it converge on the default Dawkins phrase. Try your own:

```bash
python3 weasel.py "TO BE OR NOT TO BE"
```

Options:

```bash
python3 weasel.py "HELLO WORLD" --mutation-rate 0.02 --children 200 --seed 7
```

- `--mutation-rate` — probability each character mutates per child (default `0.05`)
- `--children` — mutant children spawned per generation (default `100`)
- `--seed` — fix the RNG for a reproducible run

Only `A-Z` and spaces are supported (that's the whole alphabet Dawkins used).
