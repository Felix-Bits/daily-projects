# Diffie-Hellman, via Paint Cans

A single-page visualization of the Diffie-Hellman key exchange, told two ways at once:

1. **The paint analogy** — Alice and Bob each mix a public "base" paint with their own secret paint and swap the results in the open. Each then stirs their *own* secret paint into what they received. Because mixing is order-independent, they both land on the exact same three-way blend — without ever sending their private paint, and without anyone watching the exchange (Eve) being able to un-mix it back into its ingredients.
2. **The real math** — right below, the same exchange runs as actual modular exponentiation with the classic textbook demo values `p = 23`, `g = 5`. You see Alice's and Bob's private exponents, their public values, and the final shared secret computed two different ways (`B^a mod p` and `A^b mod p`) landing on the same number — plus exactly what an eavesdropper sees on the wire and why recovering the private exponents from it is a discrete-logarithm problem.

It's interesting because Diffie-Hellman's "how can two people agree on a secret while a spy watches every message?" trick is usually explained with either the paint metaphor *or* the modular arithmetic — rarely both, wired to the same numbers, side by side, so you can see exactly where the intuition and the real math correspond.

Click **New Key Exchange** to re-roll fresh random private keys and watch both panels recompute and land on a match every time.

## Run it

No build step, no dependencies — just open `index.html` in any browser:

```
open index.html        # macOS
xdg-open index.html    # Linux
```

or double-click the file / drag it into a browser tab.
