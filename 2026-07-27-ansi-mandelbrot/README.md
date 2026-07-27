# ANSI Mandelbrot Zoom

A terminal Mandelbrot set renderer in pure-stdlib Python — no dependencies, just 24-bit ANSI escape codes and math.

Each character cell is colored by how many iterations it takes for the point to escape (or not) under `z = z² + c`. Running it animates a continuous zoom into a well-known interesting coordinate near the boundary of the set, redrawing in place each frame.

## Run it

```
python3 mandelbrot.py          # animated zoom (Ctrl+C to stop)
python3 mandelbrot.py --static # single frame, wide view
```

Requires a terminal with 24-bit color support (most modern terminals qualify) and looks best maximized — the render size adapts to your terminal dimensions.
