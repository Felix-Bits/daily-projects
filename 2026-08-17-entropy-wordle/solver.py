#!/usr/bin/env python3
"""Entropy Wordle: a solver that always asks the question with the biggest
expected answer, played out loud.

Every candidate guess is scored by how many bits of information it is
expected to reveal (Shannon entropy over the distribution of feedback
patterns it would produce against the remaining candidates). The solver
always plays the guess that maximizes that expected information gain,
which is provably the greedy-optimal way to shrink the candidate pool
as fast as possible turn over turn.

Pure stdlib, no dependencies. Run `python3 solver.py` for a demo solve,
or see README.md for the other modes.
"""
import argparse
import math
import random
from collections import Counter

from words import WORDS

GREEN, YELLOW, GRAY = 2, 1, 0
RESET = "\033[0m"
COLORS = {GREEN: "\033[42;30m", YELLOW: "\033[43;30m", GRAY: "\033[100;37m"}


def feedback(guess, secret):
    """Return a 5-tuple of GREEN/YELLOW/GRAY, exactly like real Wordle:
    duplicate letters only get credit up to how many times they appear
    in the secret."""
    result = [GRAY] * 5
    remaining = Counter(secret)

    for i in range(5):
        if guess[i] == secret[i]:
            result[i] = GREEN
            remaining[guess[i]] -= 1

    for i in range(5):
        if result[i] == GRAY and remaining[guess[i]] > 0:
            result[i] = YELLOW
            remaining[guess[i]] -= 1

    return tuple(result)


def render(guess, pattern):
    return "".join(f"{COLORS[p]} {c.upper()} {RESET}" for c, p in zip(guess, pattern))


def entropy_of_guess(guess, candidates):
    """Expected bits of information: partition the candidates by the
    feedback pattern this guess would produce against each of them, then
    take the Shannon entropy of that partition's size distribution."""
    buckets = Counter(feedback(guess, secret) for secret in candidates)
    n = len(candidates)
    return -sum((count / n) * math.log2(count / n) for count in buckets.values())


def best_guess(candidates, pool):
    """Pick the guess (from `pool`) that maximizes expected entropy.
    Ties are broken in favor of a guess that could itself be the answer,
    since among equally-informative guesses that one can also win outright."""
    candidate_set = set(candidates)
    scored = ((entropy_of_guess(g, candidates), g in candidate_set, g) for g in pool)
    return max(scored)[2]


def solve(secret, verbose=True):
    candidates = list(WORDS)
    guesses = []

    while True:
        guess = "crane" if not guesses else best_guess(candidates, candidates)
        bits_available = math.log2(len(candidates))
        pattern = feedback(guess, secret)
        guesses.append(guess)

        if verbose:
            remaining_before = len(candidates)
            candidates = [w for w in candidates if feedback(guess, w) == pattern]
            bits_gained = math.log2(remaining_before / max(len(candidates), 1))
            print(
                f"  guess {len(guesses)}: {render(guess, pattern)}  "
                f"(expected {bits_available:4.1f} bits, gained {bits_gained:4.1f}, "
                f"{remaining_before} -> {len(candidates)} candidates)"
            )
        else:
            candidates = [w for w in candidates if feedback(guess, w) == pattern]

        if guess == secret:
            return guesses


def demo(secret=None):
    secret = secret or random.choice(WORDS)
    print(f"Solving for a hidden word ({len(WORDS)} possible answers)...\n")
    guesses = solve(secret, verbose=True)
    print(f"\nSolved '{secret}' in {len(guesses)} guesses: {' -> '.join(guesses)}")


def batch(n):
    random.seed()
    tally = Counter()
    for secret in random.sample(WORDS, min(n, len(WORDS))):
        tally[len(solve(secret, verbose=False))] += 1
    total_games = sum(tally.values())
    total_guesses = sum(k * v for k, v in tally.items())
    print(f"Played {total_games} games (guess pool restricted to the answer list):\n")
    for k in sorted(tally):
        bar = "#" * tally[k]
        print(f"  {k} guesses: {bar} ({tally[k]})")
    print(f"\naverage guesses: {total_guesses / total_games:.3f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--secret", help="solve for a specific 5-letter word")
    parser.add_argument("--games", type=int, help="run N random games and report stats, no per-guess output")
    args = parser.parse_args()

    if args.games:
        batch(args.games)
    else:
        secret = args.secret.lower() if args.secret else None
        if secret and (len(secret) != 5 or secret not in WORDS):
            parser.error(f"--secret must be a 5-letter word from words.py, got {args.secret!r}")
        demo(secret)
