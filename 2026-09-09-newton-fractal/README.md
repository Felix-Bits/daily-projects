# Newton Fractal Explorer

A pure-stdlib Python terminal toy that turns a first-year calculus algorithm into a
genuine fractal: Newton's method for root-finding, run from every point in the complex
plane at once.

## The idea

Newton's method finds a root of `f(z) = 0` by repeatedly refining a guess:

```
z_{n+1} = z_n - f(z_n) / f'(z_n)
```

Taught on the real line, it just politely slides downhill to the nearest root. But run
it on a **complex** polynomial like `f(z) = z^n - 1` (whose roots are the `n`-th roots of
unity, evenly spaced on the unit circle) and start it from *every point* in the complex
plane, and something much stranger shows up: the set of starting points that converge to
each particular root forms an intricate "basin of attraction," and the boundary between
basins is a fractal. Two starting points a hair's-width apart can be flung toward
completely different roots after just a handful of iterations — the same sensitive
dependence on initial conditions you'd expect from a chaotic dynamical system, produced
here by a numerical method usually presented as perfectly tame.

Each pixel is colored by *which* root it converged to, and shaded by *how many
iterations* it took (brighter = faster). Basin interiors are smooth and calm; the
swirling, self-similar boundary between them is where all the visual chaos lives — and
where you're looking, no matter how far you zoom in, you'll never leave it.

The renderer packs two vertical samples into every character cell using the Unicode
half-block trick (foreground = top pixel, background = bottom pixel, `▀`) with 24-bit
ANSI color, then animates a zoom into one of those boundary points, revealing more and
more fractal detail as the frames progress.

## Run it

No dependencies beyond the Python standard library:

```
python3 newton_fractal.py        # z^3 - 1 = 0, three basins (default)
python3 newton_fractal.py 5      # z^5 - 1 = 0, five basins
```

Pass any integer from 2 to 5 as the polynomial's degree — more roots means more colors
and a more tangled boundary. A true-color (24-bit ANSI) terminal is recommended; a wider
terminal window gives a bigger, more detailed image. Press Ctrl+C to stop early.
