# Burrows–Wheeler Transform Playground

A single-page toy that makes the algorithm behind `bzip2` tangible: type any word or short phrase and watch it get scrambled into long runs of repeated characters — reversibly.

## What it does

1. **Sorts every rotation** of your text (plus an end-of-string sentinel `$`) and reads off the **last column**. That column is the Burrows–Wheeler Transform — the same string content, wildly reordered.
2. Runs that output through **Move-to-Front encoding**, which turns "a character I just saw" into a `0`. Because the BWT clusters identical characters together (rotations starting with similar contexts sort next to each other), the MTF stream ends up full of zeros.
3. **Run-length encodes** the MTF stream into (value×count) pairs — the actual compression payoff, and the reason this pipeline is the core of `bzip2`.
4. **Reconstructs the original from the BWT string alone**, with no side information: repeatedly prepend the BWT string to a growing table of rows and re-sort. After *n* rounds (n = length of the string), the full sorted rotation matrix reappears out of nowhere, and the row ending in `$` is your original text. You can step through this animation and watch the matrix rebuild itself.

The "aha" here is that the last column of the sorted rotation matrix is secretly enough information to reconstruct the *entire* matrix — nothing is lost, even though what you're looking at initially looks like anagram soup.

## Why it's interesting

BWT is the unsung middle step in real-world compressors (`bzip2`, and in spirit, tools like `samtools`/FM-indexes in bioinformatics). It doesn't compress anything by itself — it's a *sorting* transform that makes text far more compressible for a simple, dumb encoder (MTF + RLE + entropy coding) than the raw bytes ever were. Seeing "mississippi" turn into `ipssm$pissii` and then watching that same scrambled string rebuild the full sorted matrix and hand back "mississippi" with zero extra bookkeeping is the kind of thing that's more convincing watched than read.

## Run it

No build step, no dependencies. Just open the file in a browser:

```bash
open index.html        # macOS
xdg-open index.html    # Linux
```

or serve it locally:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000/
```

Type a word (avoid using `$` — it's reserved as the sentinel), hit **Transform ▶** or Enter, then click **▶ Animate reconstruction** to watch the matrix rebuild itself from the BWT string alone.
