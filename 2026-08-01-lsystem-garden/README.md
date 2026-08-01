# L-System Garden

A single-page, no-dependency canvas sketch that grows fractals from **L-systems** —
the same string-rewriting grammars Aristid Lindenmayer invented in 1968 to model
plant growth. Pick a preset, watch it "grow" segment by segment, and tweak the
angle to see how wildly the shape changes for a one-degree nudge.

## Why it's interesting

Every shape here comes from the same three ingredients: a starting symbol (the
*axiom*), a rewrite rule that expands each symbol every generation, and a turtle
that walks forward and turns for each symbol it reads. Iterate the rewrite a
handful of times and interpret the resulting string as turtle moves, and wildly
different structures fall out of near-identical mechanics:

- **Fractal Plant** — `X → F+[[X]-X]-F[-FX]+X` produces a branching structure
  that looks unmistakably organic, purely from bracketed push/pop turtle state.
- **Koch Snowflake** — `F → F+F--F+F` turns a triangle into an infinitely
  wrinkled coastline.
- **Sierpinski Arrowhead** — two mutually-recursive rules (`A → B-A-B`,
  `B → A+B+A`) trace the Sierpinski triangle without ever "deciding" to make a
  triangle.
- **Dragon Curve** — the classic paper-folding fractal, from `X → X+YF+`.
- **Lévy C Curve** — a single rule (`F → +F--F+`) that self-intersects into a
  dense, crystalline curve.

None of the rules mention "leaf," "snowflake," or "triangle" — the recognizable
shape is entirely emergent from repeated substitution + turtle geometry, the
same trick behind Mandelbrot's escape-time fractals but via a completely
different mechanism (formal grammar rewriting instead of iterated complex
functions).

## Run it

Open `index.html` directly in a browser. No build step, no dependencies.

## Controls

- **Preset** — switch between the five L-systems above.
- **Iterations** — how many times the rewrite rule is applied (more = more
  detail, exponentially more segments).
- **Angle** — the turtle's turn angle in degrees; small changes produce very
  different silhouettes, especially on the Fractal Plant.
- **Growth speed** — how many line segments are drawn per animation frame.
- **Grow** — replay the growth animation with current settings.
- **Mutate** — jitter the angle for a quick "what if" variant of the current
  preset.
