# Lloyd's Voronoi Relaxation

A terminal visualizer for **Lloyd's algorithm**: scatter random points, color
every pixel by its nearest point (that's a Voronoi diagram), then move each
point to the centroid (center of mass) of the region it owns, and repeat.

Watch the jagged, random-looking cells melt into a honeycomb of even,
soap-bubble-shaped regions — a **centroidal Voronoi tessellation**. It's the
same fixed point that shows up all over computing: it's the core loop of
k-means clustering, it's how CAD/FEM tools generate well-shaped triangle
meshes, and it's the classic trick (Secord 2002) for turning a photo into
blue-noise stipple dots that look hand-drawn instead of a printer's
halftone grid.

## The idea

1. Drop N random seeds on a pixel grid.
2. For every pixel, find the nearest seed — that partitions the grid into a
   Voronoi diagram.
3. For each region, compute the centroid (average x, y of its pixels).
4. Move every seed to its region's centroid.
5. Go to 2.

Cells that are "too small" get pulled outward by their neighbors' growth,
cells that are "too big" shrink — after a dozen or so iterations the system
settles into a near-uniform tiling. The animation interpolates each seed
smoothly toward its target centroid so you can watch the cells breathe and
resettle each iteration, and stops automatically once the largest single
seed movement drops below 0.4 pixels (true convergence), holding the final
frame on screen.

Cell interiors are colored by seed (golden-angle hue spacing so no two
neighbors look alike), boundaries are drawn darker for a stained-glass look,
and each seed's current position is marked with a bright white pixel.

Pure stdlib Python, 24-bit ANSI color (half-block characters for double
vertical resolution), no dependencies.

## Run it

```
python3 voronoi.py
```

Useful flags:

```
python3 voronoi.py --seeds 24              # more/fewer regions
python3 voronoi.py --seed 42                # reproducible layout
python3 voronoi.py --no-anim                # skip animation, jump to convergence
python3 voronoi.py --iterations 40 --fps 30 # tune length/speed
python3 voronoi.py --width 80 --height 40   # force a pixel grid size
```

Needs a truecolor-capable terminal (iTerm2, most modern Linux terminals,
Windows Terminal). Press Ctrl+C to stop early — the cursor is restored on
exit either way.
