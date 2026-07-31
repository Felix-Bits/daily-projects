# Bloom Filter Playground

A single-page, no-dependency visualization of a Bloom filter — the probabilistic
data structure that trades a small, tunable chance of lying for huge space savings.
Type words in, watch them light up bits in a shared array, then test membership and
catch it *actually make a mistake* in real time.

## Why it's interesting

A Bloom filter never says "yes, this is definitely in the set." It only ever says
"definitely not" or "possibly" — and that "possibly" can be wrong. This playground
makes that abstract trade-off tangible: every word you add flips `k` bits (picked by
hashing the word `k` different ways). Testing a word checks those same bits — if any
of them are unset, the word is *definitely* not in the set (no false negatives,
ever). If they're all set, it's only *probably* in the set, because some other
combination of words could have set the exact same bits by coincidence.

The playground tracks the real ground-truth set behind the scenes (just for the
demo) so it can tell you, live, whether a "possibly in the set" answer was a true
positive or an honest-to-goodness false positive — and tallies an empirical false
positive rate that you can watch converge toward the textbook formula
`(1 − e^(−kn/m))^k` as you shrink the bit array, add more words, or change `k`.

## Run it

Open `index.html` directly in a browser — no server, no build step, no dependencies.

1. Type a word and click **Add to filter** (or press Enter) — its `k` hash bits light up blue.
2. Type any word and click **Test membership** — bits flash green (all set) or red
   (a miss found). A green flash for a word you *never* added is a live false positive,
   called out explicitly in the result banner.
3. Adjust bit array size (`m`) and hash count (`k`) to see the false-positive rate
   climb as the array fills up, or shrink as you add more hash functions per word.
4. **Reset filter** clears everything and re-rolls a fresh empty bit array.

Comes pre-seeded with a few fruit words so the grid isn't empty on first load.
