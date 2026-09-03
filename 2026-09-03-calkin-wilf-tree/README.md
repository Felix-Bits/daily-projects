# Calkin-Wilf Tree Explorer

A pure-stdlib Python terminal toy that makes a strange fact about numbers
tangible: **every positive rational number, in lowest terms, appears
exactly once** in one infinite binary tree — no duplicates, no repeats,
no fraction ever left out.

## The idea

Start at the root, `1/1`. Every node `a/b` has two children:

- left child: `a/(a+b)`
- right child: `(a+b)/b`

That's it — one rule, applied forever. Yet this simple tree (discovered by
Calkin and Wilf in 2000, and closely related to the older Stern-Brocot
tree) enumerates *every* positive rational number exactly once. `1/2` is
in there. So is `355/113`. So is any fraction you can name, in lowest
terms, at some finite, computable depth.

The really fun part: **finding** a fraction's address in the tree is just
running a subtractive Euclidean algorithm (the same one you'd use to
compute a GCD) and recording which branch you'd have come from at each
step. This script does that, walks you down from the root move by move,
and verifies it actually lands on your target.

As a bonus, it also decomposes the walk into runs of consecutive same-
direction moves (`LLLRRR` -> `[3, 3]`) and shows that — up to the
well-known last-term ambiguity of continued fractions — **that run-length
sequence *is* the continued fraction expansion of the fraction**. The tree
isn't just enumerating rationals, it's secretly doing continued-fraction
arithmetic the whole time.

## Run it

```bash
python3 tree.py
```

With no arguments it prints the top few levels of the tree, then walks to
five interesting fractions (`3/2`, `5/8`, the pi-approximations `22/7` and
`355/113`, and a Fibonacci ratio `8/13`), showing each path and its
continued-fraction match.

Look up your own fraction:

```bash
python3 tree.py 41/17
```

Other flags:

```bash
python3 tree.py --depth 7          # print more levels of the tree
python3 tree.py 41/17 --delay 0.3  # pause between animation steps
python3 tree.py --no-color         # plain text, no ANSI color
```

Needs nothing but Python 3 (tested on 3.9+).
