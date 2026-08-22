# Fourier Epicycles

A single-page canvas toy: draw any closed-ish shape with your mouse, and a chain of
rotating circles (an "epicycle" chain, decomposed by a Discrete Fourier Transform)
draws it right back for you — with no image data, just spinning vectors.

## The idea

Any 2D path can be treated as a sequence of complex numbers `z(t) = x(t) + i*y(t)`.
Run a DFT over that sequence and you get back a set of rotating vectors — one per
frequency — each with its own radius (amplitude) and starting angle (phase). Chain
them tip-to-tail, spin each one at its own frequency, and the *sum* traces the
original path exactly once you include enough of them. This is the same trick
behind epicycle models of planetary motion (which is how it got its name) and
Fourier series in general: a handful of big, slow circles rough out the overall
shape, and each smaller, faster circle added on top sharpens the detail.

Two things that made it feel right instead of jittery:
- **Sorting the frequency terms by amplitude** (not by frequency number) before
  drawing, so the *biggest* circles are always drawn first — dragging the "circles"
  slider down shows the coarse approximation first, not an arbitrary subset.
- **Treating the DC term (frequency 0) as an ordinary member of the sum** rather
  than centering the path manually — it naturally reconstructs at the same
  coordinates you drew in, no offset bookkeeping needed.

## Run it

Just open `index.html` in any modern browser — no build step, no dependencies:

```
open index.html      # macOS
xdg-open index.html  # Linux
```

It loads with a demo heart curve animating by default. Click **Clear & draw your
own** and drag out any shape (letters, a face, a squiggle) — release the mouse and
the epicycles rebuild themselves to draw it. Drag the **circles** slider to see how
few terms are needed before the shape falls apart, and **speed** to change how fast
the chain spins.
