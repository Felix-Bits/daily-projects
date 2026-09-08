# Collatz Tree

A single-page canvas visualization of the Collatz conjecture, drawn as a radial tree instead of the usual list of bouncing numbers.

## The idea

The Collatz rule is simple: starting from any positive integer, if it's even divide by 2, if it's odd do `3n+1`, repeat. Every number ever tested eventually reaches 1. Normally you visualize this by plotting one number's up-and-down trajectory over time — but every trajectory ends at 1, which means you can build the **entire structure at once** by running the rule *backwards* from 1.

Because every number has exactly one forward successor, the reverse graph rooted at 1 is guaranteed to be a genuine tree — no cycles, no two branches merging. From a node `n`, its reverse-children are:

- `2n` (always valid — undoing an even step)
- `(n-1)/3`, but only if that's a positive odd integer (undoing an odd step; most `n` don't have this second child, which is why the tree is lopsided rather than a clean binary tree)

The app does a breadth-first build of this reverse tree from 1 out to a chosen depth, then lays it out radially: each node gets an angular slice proportional to how many descendants (leaves) it has, so dense sub-branches spread wide and thin chains stay narrow. The result looks like coral or a nervous system, colored from cyan (near the root) to magenta (deep chains), and it grows outward with an eased animation on load or whenever you change the depth.

Click any node and its path back to the root lights up — that path, read outward from 1, *is* that number's Collatz sequence, and its length is its "stopping time." Type any number into the jump box and it'll either highlight it in the tree (if it's within the current depth) or, if it's too deep to be charted, simulate its trajectory directly and print the sequence anyway.

## Run it

No build step, no dependencies — just open `index.html` in a browser:

```
open index.html
# or
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Controls

- **Depth slider** — how many reverse-Collatz levels to build (6–22). Higher depths reveal more of the tree's fractal-ish branching (capped at 9,000 nodes to stay smooth).
- **Click a node** — highlights its path to the root and prints its full Collatz sequence + stopping time in the side panel.
- **Jump to number** — type any positive integer and hit Enter to trace its trajectory, whether or not it's currently drawn.
