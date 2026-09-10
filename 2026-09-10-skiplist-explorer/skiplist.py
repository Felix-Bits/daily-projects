#!/usr/bin/env python3
"""Skip List Explorer - watch a randomized skip list build itself and
search itself, one express-lane hop at a time. Pure stdlib.

A skip list is a sorted linked list with extra "express lanes" stacked on
top of it. Each node gets its lane height by flipping a coin (heads = grow
another level) when it's inserted -- no rebalancing, no rotations, just
randomness -- and yet the expected search cost comes out O(log n), the
same as a balanced tree. This toy renders those lanes directly and then
animates a real skip-list search, level by level, so you can see exactly
where the shortcuts save the walk.

Usage:
    python3 skiplist.py                    # run the full animated demo
    python3 skiplist.py --seed 7 --count 24
    python3 skiplist.py --fast             # no delays, for scripting/testing
"""
import argparse
import random
import sys
import time

MAX_LEVEL = 5
P = 0.5  # probability a node's lane grows one level taller

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"
CYAN = "\x1b[36m"
YELLOW = "\x1b[93m"
GREEN = "\x1b[92m"
RED = "\x1b[91m"
CLEAR = "\x1b[2J\x1b[H"


def random_level(rng):
    lvl = 1
    while lvl < MAX_LEVEL and rng.random() < P:
        lvl += 1
    return lvl


class SkipList:
    def __init__(self):
        self.levels = {}  # key -> how many lanes it participates in (1..MAX_LEVEL)

    def insert(self, key, rng):
        self.levels[key] = random_level(rng)

    def sorted_keys(self):
        return sorted(self.levels)

    def top_level(self):
        return max(self.levels.values()) if self.levels else 1

    def search_path(self, target):
        """Simulate the real skip-list search algorithm: start at the
        tallest lane, walk right while the next node's key still fits,
        otherwise drop a level. Returns (path, found) where path is the
        ordered sequence of nodes actually visited ('HEAD' first)."""
        keys = self.sorted_keys()
        path = ["HEAD"]
        cur = None
        found = False
        for level in range(self.top_level(), 0, -1):
            while True:
                candidates = [
                    k for k in keys
                    if self.levels[k] >= level and (cur is None or k > cur)
                ]
                nxt = candidates[0] if candidates else None
                if nxt is not None and nxt <= target:
                    cur = nxt
                    if path[-1] != cur:
                        path.append(cur)
                    if cur == target:
                        found = True
                        break
                else:
                    break
            if found:
                break
        return path, found


def render(sl, revealed, current, status_line, header):
    keys = sl.sorted_keys()
    top = sl.top_level()
    lines = [header, ""]
    for level in range(top, 0, -1):
        parts = [f"{DIM}L{level}{RESET} "]
        if current == "HEAD":
            parts.append(f"{YELLOW}{BOLD}HEAD{RESET}")
        elif "HEAD" in revealed:
            parts.append(f"{CYAN}HEAD{RESET}")
        else:
            parts.append("HEAD")
        for k in keys:
            if sl.levels[k] >= level:
                label = f"{k:>2}"
                if k == current:
                    color = GREEN if status_line.startswith("Found") else YELLOW
                    cell = f"{color}{BOLD}[{label}]{RESET}"
                elif k in revealed:
                    cell = f"{CYAN}[{label}]{RESET}"
                else:
                    cell = f"[{label}]"
                parts.append(f"──►{cell}")
            else:
                parts.append("─" * 7)
        parts.append(f"──► NIL")
        lines.append("".join(parts))
    lines.append("")
    lines.append(status_line)
    return "\n".join(lines)


def show(sl, revealed, current, status_line, header, delay):
    sys.stdout.write(CLEAR + render(sl, revealed, current, status_line, header) + "\n")
    sys.stdout.flush()
    if delay:
        time.sleep(delay)


def animate_search(sl, target, delay, header):
    path, found = sl.search_path(target)
    revealed = set()
    for node in path:
        revealed.add(node)
        remaining = len(path) - len(revealed)
        status = (
            f"searching for {target}: at {node}, "
            f"{remaining} hop(s) left to check"
        )
        show(sl, revealed, node, status, header, delay)
    verdict = f"Found {target}!" if found else f"{target} is not in the list (search fell through)."
    show(sl, revealed, path[-1], verdict, header, delay * 2 if delay else 0)
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seed", type=int, default=None, help="random seed (default: random)")
    parser.add_argument("--count", type=int, default=20, help="number of keys to insert (default: 20)")
    parser.add_argument("--delay", type=float, default=0.45, help="seconds between animation frames")
    parser.add_argument("--fast", action="store_true", help="no delays, print frames as fast as possible")
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randrange(1 << 30)
    rng = random.Random(seed)
    delay = 0 if args.fast else args.delay

    pool = list(range(1, 100))
    rng.shuffle(pool)
    keys = pool[: min(args.count, len(pool))]

    sl = SkipList()
    header = f"{BOLD}Skip List Explorer{RESET}  (seed={seed}, p={P}, max_level={MAX_LEVEL})"

    for k in keys:
        sl.insert(k, rng)
        heads = f"{len(sl.levels)}/{len(keys)} keys inserted"
        show(sl, {k}, k, f"inserting {k} -> grew to lane {sl.levels[k]}  [{heads}]", header, delay * 0.4)

    show(sl, set(), None, "list built. now searching...", header, delay * 2 if delay else 0)

    existing = rng.choice(sl.sorted_keys())
    animate_search(sl, existing, delay, header)

    present = set(sl.sorted_keys())
    missing_candidates = [k for k in range(1, 100) if k not in present]
    if missing_candidates:
        missing = rng.choice(missing_candidates)
        show(sl, set(), None, f"list unchanged. now searching for {missing} (not present)...", header, delay * 2 if delay else 0)
        animate_search(sl, missing, delay, header)

    tallest = max(sl.levels.values())
    avg_lanes = sum(sl.levels.values()) / len(sl.levels)
    print(f"\n{len(sl.levels)} keys, tallest lane reaches L{tallest}, average lane height {avg_lanes:.2f}.")
    print("Every run reshuffles the coin flips -- pass --seed to replay one.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(0)
