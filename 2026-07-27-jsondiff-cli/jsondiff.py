#!/usr/bin/env python3
"""Recursive, colorized diff of two JSON files."""
import json
import sys

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
DIM = "\033[2m"
RESET = "\033[0m"

MISSING = object()


def fmt(value):
    if value is MISSING:
        return DIM + "—" + RESET
    return json.dumps(value)


def diff(old, new, path, out):
    if isinstance(old, dict) and isinstance(new, dict):
        for key in sorted(set(old) | set(new)):
            diff(
                old.get(key, MISSING),
                new.get(key, MISSING),
                f"{path}.{key}" if path else key,
                out,
            )
    elif isinstance(old, list) and isinstance(new, list):
        for i in range(max(len(old), len(new))):
            diff(
                old[i] if i < len(old) else MISSING,
                new[i] if i < len(new) else MISSING,
                f"{path}[{i}]",
                out,
            )
    elif old != new:
        out.append((path, old, new))


def render(changes):
    if not changes:
        print(f"{GREEN}No differences.{RESET}")
        return
    for path, old, new in changes:
        if old is MISSING:
            print(f"{GREEN}+ {path}: {fmt(new)}{RESET}")
        elif new is MISSING:
            print(f"{RED}- {path}: {fmt(old)}{RESET}")
        else:
            print(f"{YELLOW}~ {path}: {fmt(old)} -> {fmt(new)}{RESET}")


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file_a.json> <file_b.json>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        a = json.load(f)
    with open(sys.argv[2]) as f:
        b = json.load(f)

    changes = []
    diff(a, b, "", changes)
    render(changes)
    sys.exit(1 if changes else 0)


if __name__ == "__main__":
    main()
