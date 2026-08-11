#!/usr/bin/env python3
"""Jitter Entropy — a homebrew hardware RNG built from CPU timing noise.

No `random`, no `os.urandom`, no seed. The only source of randomness is
how unpredictably long a few nanosecond-scale operations take on real
hardware, thanks to scheduler preemption, cache misses, and thermal/clock
jitter. This is an educational demo of the technique real hardware RNGs
(and Linux's own entropy pool) are built on — NOT a cryptographically
secure RNG. Don't use this to generate real passwords or keys.
"""
import argparse
import sys
import time

RESET = "\033[0m"
DIM = "\033[2m"


def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"


def collect_raw_bits(n):
    """Extract one 'random' bit per sample from the low bit of a timing delta.

    Between two nanosecond-clock reads we do a tiny, fixed amount of
    busy-work. How long that takes is dominated by things we don't
    control: which core we land on, what's in L1 cache, whether the OS
    scheduler steals the CPU mid-loop. The exact nanosecond count is
    unpredictable even though the work is identical every time — so its
    least-significant bit is our raw entropy.
    """
    bits = []
    for _ in range(n):
        t0 = time.perf_counter_ns()
        x = 0
        for _ in range(8):
            x ^= time.perf_counter_ns()
        t1 = time.perf_counter_ns()
        bits.append((t1 - t0) & 1)
    return bits


def von_neumann_debias(bits):
    """Classic von Neumann extractor: look at bits in pairs.

    01 -> emit 0, 10 -> emit 1, 00/11 -> discard. Whatever constant bias
    the raw source has (say P(1) = 0.52 instead of 0.5), P(01) == P(10)
    always holds, so the output is unbiased no matter how skewed the
    input was. The cost is throughput: on average you need 4 raw bits per
    unbiased output bit at 50% raw bias, more if the source is skewed.
    """
    out = []
    for i in range(0, len(bits) - 1, 2):
        a, b = bits[i], bits[i + 1]
        if a != b:
            out.append(a)
    return out


def frequency_test(bits):
    if not bits:
        return 0.0
    return sum(bits) / len(bits)


def longest_run(bits):
    best = cur = 0
    prev = None
    for b in bits:
        if b == prev:
            cur += 1
        else:
            cur = 1
            prev = b
        best = max(best, cur)
    return best


def runs_count(bits):
    """Number of maximal same-value runs — a healthy random stream has many."""
    if not bits:
        return 0
    n = 1
    for i in range(1, len(bits)):
        if bits[i] != bits[i - 1]:
            n += 1
    return n


def render_grid(bits, width, on_color, off_color, label):
    print(f"{DIM}{label}{RESET}")
    for i in range(0, len(bits), width):
        row = bits[i:i + width]
        line = "".join(
            (on_color if b else off_color) + ("█" if b else "░") for b in row
        )
        print(line + RESET)
    print()


def bits_to_hex(bits):
    out = []
    for i in range(0, len(bits) - 3, 4):
        nibble = bits[i] << 3 | bits[i + 1] << 2 | bits[i + 2] << 1 | bits[i + 3]
        out.append("0123456789abcdef"[nibble])
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--samples", type=int, default=4000,
                     help="raw timing samples to collect (default: 4000)")
    ap.add_argument("--width", type=int, default=64,
                     help="grid width in bits per row (default: 64)")
    ap.add_argument("--quiet", action="store_true",
                     help="skip the bit grids, just print stats + output")
    args = ap.parse_args()

    print(f"Collecting {args.samples} raw timing samples...\n")
    raw = collect_raw_bits(args.samples)
    debiased = von_neumann_debias(raw)

    if not args.quiet:
        render_grid(raw[: args.width * 8], args.width,
                    rgb(255, 90, 90), rgb(60, 20, 20), "raw bits (LSB of timing deltas)")
        render_grid(debiased[: args.width * 8], args.width,
                    rgb(90, 220, 140), rgb(20, 50, 35), "debiased bits (von Neumann extractor)")

    raw_freq = frequency_test(raw)
    deb_freq = frequency_test(debiased)
    keep_rate = len(debiased) / (len(raw) // 2) if len(raw) >= 2 else 0.0

    print(f"{DIM}stats{RESET}")
    print(f"  raw samples          : {len(raw)}")
    print(f"  raw P(1)             : {raw_freq:.4f}  (bias from 0.5: {abs(raw_freq - 0.5):.4f})")
    print(f"  raw longest run      : {longest_run(raw)}")
    print(f"  raw run count        : {runs_count(raw)}  (higher = more alternation)")
    print(f"  debiased bits kept   : {len(debiased)}  ({keep_rate:.1%} of raw pairs)")
    print(f"  debiased P(1)        : {deb_freq:.4f}  (bias from 0.5: {abs(deb_freq - 0.5):.4f})")
    print(f"  debiased longest run : {longest_run(debiased)}")
    print()

    hexout = bits_to_hex(debiased)
    if hexout:
        print(f"{DIM}output (debiased bits packed to hex){RESET}")
        print(f"  {hexout}")
    else:
        print("Not enough debiased bits for hex output — try a larger --samples.")

    if abs(deb_freq - 0.5) > abs(raw_freq - 0.5) and len(debiased) > 100:
        print(f"\n{DIM}(debiasing didn't help this run — timing noise is itself noisy;{RESET}")
        print(f"{DIM} try again or bump --samples for a cleaner statistical picture){RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
