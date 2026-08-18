# SDF Raymarcher

A terminal 3D renderer, pure-stdlib Python, that draws a real lit, shaded,
tumbling object — with no triangles, no rasterizer, and no graphics library.

## The idea

Traditional 3D rendering rasterizes triangle meshes. This does something
different: the scene is defined as a **signed distance function (SDF)** — a
math function that, for any point in 3D space, answers "how far is the
nearest surface?" A torus's SDF and a sphere's SDF are each a few lines of
arithmetic; blending the two with a smooth minimum (`smin`) makes the sphere
melt into the torus instead of just clipping through it, no mesh boolean
required.

Each of the (up to) thousands of rays — one per screen sub-pixel — is
**sphere-traced**: step forward by exactly the distance the SDF reports (that
distance is *guaranteed* safe, since nothing is closer), then ask again,
until the distance is ~0 (a hit) or has grown past the far clip (a miss). No
Z-buffer, no barycentric coordinates — just repeatedly asking "how far to the
nearest thing?" and walking there.

Surface normals fall out of the SDF for free, via its numerical gradient
(finite differences in x/y/z), which feeds a diffuse + Blinn-Phong specular
light model. Intensity maps through a purple → cyan → white color ramp,
rendered in 24-bit ANSI color using half-block (`▀`) characters so each
terminal cell carries two independently-colored pixels (top = foreground,
bottom = background) for roughly double vertical resolution — the same trick
classic terminal fire effects use, aimed here at a real camera and light
instead of a heat table.

The object itself (a torus with a sphere orbiting through it, smoothly
blended) tumbles on two axes while the sphere orbits, so the smin blend
constantly reshapes — nothing about the silhouette repeats exactly.

## Run it

```
python3 raymarch.py
```

Ctrl+C to stop. Needs a truecolor-capable terminal (iTerm2, most modern
Linux/macOS terminals, Windows Terminal).

Options:

```
python3 raymarch.py --frames 50        # run exactly 50 frames then exit
python3 raymarch.py --fps 20           # target frame rate
python3 raymarch.py --width 60 --height 24   # override render size (default: auto-fit terminal)
```
