#!/usr/bin/env python3
"""Dawkins' Weasel: evolve a random string into a target phrase via
cumulative selection (mutation + keep-the-fittest), with no lookahead
and no intelligence involved.

Usage:
    python3 weasel.py ["TARGET PHRASE"] [--mutation-rate 0.05] [--children 100]
"""
import argparse
import random
import sys
import time

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "


def random_string(length):
    return "".join(random.choice(ALPHABET) for _ in range(length))


def fitness(candidate, target):
    """Number of characters matching the target at the same position."""
    return sum(1 for a, b in zip(candidate, target) if a == b)


def mutate(parent, mutation_rate):
    return "".join(
        random.choice(ALPHABET) if random.random() < mutation_rate else c
        for c in parent
    )


def random_search_odds(length):
    """Expected number of guesses to hit the target by pure chance,
    and how long that would take at ~1e9 guesses/sec."""
    combos = len(ALPHABET) ** length
    seconds = combos / 1e9
    years = seconds / (60 * 60 * 24 * 365.25)
    return combos, years


def run(target, mutation_rate, children, quiet=False):
    target = target.upper()
    if any(c not in ALPHABET for c in target):
        sys.exit(f"Target may only contain A-Z and spaces, got: {target!r}")

    parent = random_string(len(target))
    best_fit = fitness(parent, target)
    generation = 0
    start = time.time()

    while parent != target:
        generation += 1
        litter = [mutate(parent, mutation_rate) for _ in range(children)]
        litter.append(parent)  # parent survives if no child beats it
        parent = max(litter, key=lambda c: fitness(c, target))
        best_fit = fitness(parent, target)
        if not quiet:
            pct = best_fit / len(target) * 100
            print(f"\rgen {generation:5d}  [{pct:5.1f}%]  {parent}", end="", flush=True)

    elapsed = time.time() - start
    if not quiet:
        print(f"\rgen {generation:5d}  [100.0%]  {parent}")
        print(f"\nConverged in {generation} generations, {elapsed:.2f}s "
              f"({children} children/generation).")

    return generation, elapsed, parent


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("target", nargs="?", default="METHINKS IT IS LIKE A WEASEL",
                     help="phrase to evolve toward (A-Z and spaces only)")
    ap.add_argument("--mutation-rate", type=float, default=0.05,
                     help="probability each character mutates per child (default 0.05)")
    ap.add_argument("--children", type=int, default=100,
                     help="mutant children spawned per generation (default 100)")
    ap.add_argument("--seed", type=int, default=None, help="random seed")
    args = ap.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    target = args.target.upper()
    combos, years = random_search_odds(len(target))
    print(f"Target: {target!r}  ({len(target)} characters, alphabet size {len(ALPHABET)})")
    print(f"Pure random guessing would need ~{combos:.2e} tries on average")
    print(f"  -> about {years:.2e} years at 1 billion guesses/sec.\n")

    generation, elapsed, result = run(target, args.mutation_rate, args.children)

    print(f"\nCumulative selection found it in {generation} generations "
          f"instead of {years:.2e} years of blind luck.")


if __name__ == "__main__":
    main()
