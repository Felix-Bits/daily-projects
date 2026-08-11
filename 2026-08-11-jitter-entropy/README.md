# Jitter Entropy

A terminal CLI tool, pure-stdlib Python, no dependencies, that builds a
random number generator out of nothing but **how long your CPU takes to do
things** — no `random` module, no `os.urandom`, no seed anywhere in sight.

## Why it's interesting

Run the same tiny loop twice in a row and it won't take the same number of
nanoseconds both times. Scheduler preemption, cache misses, branch
prediction, thermal throttling — dozens of things nudge the timing around
in ways nobody can predict from the outside. That noise is "jitter," and
it's the actual physical entropy source real hardware RNGs (Intel's
RDRAND, Linux's `/dev/random`) are ultimately built on, just with far more
engineering behind them.

This tool does the minimal version by hand: read a nanosecond clock, do a
fixed tiny amount of work, read the clock again, and keep the low bit of
the elapsed time as one "random" bit. Do that thousands of times and you
get a bitstream that's biased (way more predictable than true randomness)
but not *constant* — which is exactly the situation the **von Neumann
extractor** was invented for in 1951. It looks at bits two at a time: `01`
emits a `0`, `10` emits a `1`, and `00`/`11` are thrown away. Because
`P(01) == P(10)` no matter how skewed the underlying coin is, whatever
comes out the other end is provably unbiased — you're trading throughput
(most raw bits get discarded) for a clean signal.

The tool visualizes both the raw stream and the debiased stream as colored
bit grids, runs a couple of classic randomness sanity checks (frequency
test, longest-run test) on each, and packs the final debiased bits into a
hex string as the "output." It's a fun, honest look at where randomness
actually comes from on a real machine — **not** a cryptographically secure
RNG, and it says so.

## Run it

```
python3 jitter_entropy.py                       # 4000 samples, full visualization
python3 jitter_entropy.py --samples 10000        # more samples, cleaner stats
python3 jitter_entropy.py --width 32             # narrower bit grid
python3 jitter_entropy.py --quiet                # skip the grids, just stats + hex output
```

Requires a terminal with 24-bit color support (most modern terminals
qualify). Every run produces different output since the entropy source is
your machine's live timing noise — run it twice and diff the results.
