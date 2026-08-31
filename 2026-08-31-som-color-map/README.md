# Self-Organizing Color Map

A single-file, pure-stdlib Python terminal animation of a **Kohonen
self-organizing map (SOM)** — a 1980s unsupervised neural network — learning
to sort random RGB colors into a smooth rainbow-like grid, live, with 24-bit
ANSI color.

## The idea

Start with a grid of "neurons," each holding a random RGB weight vector (so
the grid starts as pure static). Then, thousands of times:

1. Draw a random target color.
2. Find the neuron whose weights are closest to it (the "best matching
   unit," or BMU) — the neuron that "wins."
3. Nudge the BMU *and its neighbors on the grid* toward that color, with the
   pull strength falling off with distance (a Gaussian) and both the
   neighborhood radius and learning rate shrinking over time.

No labels, no loss function, no backpropagation, no gradient descent — just
"the winner and its neighbors move a little closer to what they just saw."
And yet after a few thousand iterations, a field of random noise
self-organizes into a smooth, continuous map where similar colors sit next
to each other and the whole grid tiles through hue space — the same
mechanism (minus the RGB toy setting) that SOMs use for dimensionality
reduction and clustering on real high-dimensional data.

Watching it animate is the fun part: the first frames are visibly chaotic
mush, and within a couple hundred steps you can see bands and blobs of
similar hue crystallize and slide around to settle into flowing gradients.

## Run it

```bash
python3 som.py
```

Needs nothing but Python 3 and a terminal that supports 24-bit ANSI color
(most modern terminals do). Runs the default animation (50x25 neurons, 4000
training steps) in a couple of seconds.

Useful flags:

```bash
python3 som.py --width 60 --height 30 --iterations 6000   # bigger map, longer training
python3 som.py --seed 42                                   # reproducible run
python3 som.py --quiet                                     # skip animation, print final map only
python3 som.py --frame-every 10 --fps-delay 0.05            # slower, smoother animation
```

Press Ctrl+C any time to stop early (the cursor is restored on exit either way).
