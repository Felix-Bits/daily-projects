# Skip List Explorer

A pure-stdlib Python terminal toy that builds a randomized **skip list** and
then animates a real search across it, one express-lane hop at a time.

## The idea

A skip list is a sorted linked list with extra "express lanes" stacked on
top. Every key lives on lane 1 (the full sorted list), but when a key is
inserted it also gets a random *height*: flip a coin, heads means "grow one
lane taller," repeat. Tails, and you're done. No rebalancing, no rotations,
no comparisons against siblings — just independent coin flips per node.

That's the whole trick, and it's a genuinely strange one: with no
coordination between nodes at all, the *expected* shape that falls out is
close to a balanced structure, giving `O(log n)` search, insert, and delete
— the same asymptotic guarantee as a red-black tree, for a fraction of the
implementation complexity (skip lists back Redis's sorted sets and
LevelDB/RocksDB's memtables for exactly this reason).

This toy makes the shortcut visible instead of theoretical:

1. It inserts a batch of random keys one at a time, showing each one's coin
   flips as it grows into its lane.
2. It renders every lane as its own row, tallest at the top, with keys
   present only on the lanes they earned.
3. It then runs the actual skip-list search algorithm for a key that exists
   and one that doesn't — starting at the top-left lane, walking right while
   the next node still fits under the target, dropping a level whenever it
   doesn't — and animates the pointer frame by frame so you can watch it
   skip clean over long stretches of the bottom lane by riding a higher one.

Run it a few times and you'll see the same 20 keys build wildly different
skylines depending on the coin flips — that randomness is the whole point,
not a bug to be engineered away.

## Running it

```bash
python3 skiplist.py                    # full animated demo, random seed
python3 skiplist.py --seed 7           # reproducible layout
python3 skiplist.py --count 30         # more keys, taller/denser lanes
python3 skiplist.py --fast             # no animation delay (good for piping to a file)
```

No dependencies beyond the Python standard library (uses only `argparse`,
`random`, `sys`, `time`, and raw ANSI escape codes for color/clearing).
