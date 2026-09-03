#!/usr/bin/env python3
"""Calkin-Wilf tree explorer: every positive rational, exactly once.

Pure-stdlib terminal toy. See README.md for the idea.
"""
from __future__ import annotations

import argparse
import itertools
import sys
import time
from math import gcd

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
LEVEL_COLORS = [
    "\033[38;5;81m",   # cyan
    "\033[38;5;114m",  # green
    "\033[38;5;222m",  # tan
    "\033[38;5;210m",  # salmon
    "\033[38;5;177m",  # violet
    "\033[38;5;250m",  # grey
]
MOVE_L = "\033[38;5;114mL\033[0m"
MOVE_R = "\033[38;5;210mR\033[0m"


def color(text: str, code: str, use_color: bool) -> str:
    return f"{code}{text}{RESET}" if use_color else text


# --- The tree itself -------------------------------------------------------
# Root is 1/1. Left child of a/b is a/(a+b). Right child is (a+b)/b.
# Every positive rational in lowest terms appears exactly once, this
# way, somewhere in the tree (Calkin & Wilf, 2000).

def left_child(node: tuple[int, int]) -> tuple[int, int]:
    a, b = node
    return (a, a + b)


def right_child(node: tuple[int, int]) -> tuple[int, int]:
    a, b = node
    return (a + b, b)


def print_levels(depth: int, use_color: bool) -> None:
    level = [(1, 1)]
    for d in range(depth + 1):
        c = LEVEL_COLORS[d % len(LEVEL_COLORS)]
        labels = [color(f"{a}/{b}", c, use_color) for a, b in level]
        prefix = color(f"level {d}:", BOLD, use_color)
        print(f"{prefix} " + "  ".join(labels))
        level = list(itertools.chain.from_iterable(
            ((left_child(n), right_child(n)) for n in level)
        ))


# --- Finding a rational's address in the tree -------------------------------
# Walking from a/b back toward the root: if a<b we must have come from an
# L-move (parent = a/(b-a)); if a>b, an R-move (parent = (a-b)/b). Recording
# those moves and reversing gives the root-to-node path.

def path_to(a: int, b: int) -> list[str]:
    if a <= 0 or b <= 0:
        raise ValueError("only positive rationals live in this tree")
    g = gcd(a, b)
    a, b = a // g, b // g
    moves = []
    while (a, b) != (1, 1):
        if a < b:
            moves.append("L")
            b -= a
        else:
            moves.append("R")
            a -= b
    moves.reverse()
    return moves


def continued_fraction(a: int, b: int) -> list[int]:
    terms = []
    while b:
        terms.append(a // b)
        a, b = b, a - (a // b) * b
    return terms


def run_lengths(moves: list[str]) -> list[int]:
    return [len(list(g)) for _, g in itertools.groupby(moves)]


def walk_and_print(target_a: int, target_b: int, use_color: bool, delay: float) -> None:
    g = gcd(target_a, target_b)
    a0, b0 = target_a // g, target_b // g
    moves = path_to(a0, b0)

    print(f"\n{color(f'Finding {a0}/{b0} in the tree', BOLD, use_color)}")
    print(f"  {len(moves)} move(s) from the root:\n")

    node = (1, 1)
    print(f"  start  {color('1/1', BOLD, use_color)}   (the root)")
    for i, m in enumerate(moves, 1):
        node = left_child(node) if m == "L" else right_child(node)
        arrow = MOVE_L if (m == "L" and use_color) else (MOVE_R if use_color else m)
        label = color(f"{node[0]}/{node[1]}", DIM if node != (a0, b0) else BOLD, use_color)
        print(f"  step {i:<2} {arrow}  ->  {label}")
        if delay:
            time.sleep(delay)

    assert node == (a0, b0), "path did not land on the target -- this should be impossible"
    print(f"\n  {color('landed on target:', BOLD, use_color)} {a0}/{b0}  (verified)")

    cf = continued_fraction(a0, b0)
    rle = run_lengths(moves)
    rle_reversed = list(reversed(rle))
    print(f"\n  path as L/R:            {''.join(moves) or '(root)'}")
    print(f"  path run-lengths:       {rle}")
    print(f"  ...reversed:            {rle_reversed}")
    print(f"  continued fraction of {a0}/{b0}:  {cf}")
    if rle_reversed and cf[:-1] == rle_reversed[:-1] and cf[-1] == rle_reversed[-1] + 1:
        print(f"  {color('-> matches, up to the usual last-term +/-1 ambiguity of continued fractions.', DIM, use_color)}")
    elif cf == rle_reversed:
        print(f"  {color('-> matches exactly.', DIM, use_color)}")


DEMOS = [
    (3, 2, "simplest non-trivial rational"),
    (5, 8, "a fraction less than 1"),
    (22, 7, "the classic pi approximation"),
    (355, 113, "a much better pi approximation"),
    (8, 13, "consecutive Fibonacci numbers -> converges toward 1/phi"),
]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("fraction", nargs="?", help="a rational to locate, as p/q (default: run demos)")
    ap.add_argument("--depth", type=int, default=5, help="levels of the tree to print (default: 5)")
    ap.add_argument("--delay", type=float, default=0.0, help="seconds to pause between walk steps")
    ap.add_argument("--no-color", action="store_true", help="disable ANSI color")
    args = ap.parse_args()

    use_color = not args.no_color and sys.stdout.isatty()

    print(color("Calkin-Wilf tree", BOLD, use_color))
    print("Every positive rational appears exactly once, in lowest terms.\n")
    print_levels(args.depth, use_color)

    if args.fraction:
        if "/" not in args.fraction:
            ap.error("fraction must look like p/q, e.g. 5/8")
        p_str, q_str = args.fraction.split("/", 1)
        try:
            walk_and_print(int(p_str), int(q_str), use_color, args.delay)
        except ValueError as e:
            ap.error(str(e))
    else:
        for a, b, note in DEMOS:
            print(f"\n{color(note, DIM, use_color)}")
            walk_and_print(a, b, use_color, args.delay)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(130)
