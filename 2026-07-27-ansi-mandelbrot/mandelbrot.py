#!/usr/bin/env python3
"""Terminal Mandelbrot set renderer with ANSI color and a zoom animation.

Pure standard library, no dependencies. Run directly with python3.
"""
import os
import sys
import time
import shutil

MAX_ITER = 60

# 24-bit ANSI gradient stops (dark blue -> orange -> white), interpolated per-pixel.
GRADIENT = [
    (7, 7, 40), (10, 20, 90), (20, 60, 160), (60, 120, 220),
    (180, 200, 240), (255, 220, 120), (255, 140, 30), (20, 10, 10),
]


def color_for(t):
    """t in [0, 1) -> (r, g, b) by interpolating through GRADIENT."""
    if t >= 1.0:
        return (0, 0, 0)
    segments = len(GRADIENT) - 1
    pos = t * segments
    i = int(pos)
    frac = pos - i
    r1, g1, b1 = GRADIENT[i]
    r2, g2, b2 = GRADIENT[min(i + 1, segments)]
    r = int(r1 + (r2 - r1) * frac)
    g = int(g1 + (g2 - g1) * frac)
    b = int(b1 + (b2 - b1) * frac)
    return (r, g, b)


def mandelbrot_iters(cx, cy, max_iter):
    x, y = 0.0, 0.0
    for i in range(max_iter):
        x2, y2 = x * x, y * y
        if x2 + y2 > 4.0:
            return i
        y = 2 * x * y + cy
        x = x2 - y2 + cx
    return max_iter


def render_frame(width, height, center_x, center_y, scale, max_iter=MAX_ITER):
    lines = []
    aspect_fix = 0.5  # terminal cells are roughly twice as tall as wide
    for row in range(height):
        cy = center_y + (row - height / 2) * scale * aspect_fix
        chars = []
        for col in range(width):
            cx = center_x + (col - width / 2) * scale
            n = mandelbrot_iters(cx, cy, max_iter)
            if n == max_iter:
                chars.append("\x1b[38;2;0;0;0m \x1b[0m")
            else:
                r, g, b = color_for(n / max_iter)
                chars.append(f"\x1b[38;2;{r};{g};{b}m#\x1b[0m")
        lines.append("".join(chars))
    return "\n".join(lines)


def animate_zoom(target=(-0.743643887037151, 0.13182590420533), frames=40, delay=0.05):
    cols, rows = shutil.get_terminal_size(fallback=(100, 40))
    width = max(20, cols - 2)
    height = max(10, rows - 4)
    scale = 3.0 / width
    zoom_factor = 0.85

    sys.stdout.write("\x1b[2J")  # clear screen once
    for frame in range(frames):
        frame_iter = min(MAX_ITER, 30 + frame * 3)
        image = render_frame(width, height, target[0], target[1], scale, frame_iter)
        sys.stdout.write("\x1b[H")  # cursor home, redraw in place
        sys.stdout.write(image)
        sys.stdout.write(f"\n\x1b[0mframe {frame + 1}/{frames}  scale={scale:.2e}  iter={frame_iter}\n")
        sys.stdout.flush()
        scale *= zoom_factor
        time.sleep(delay)


def static_render():
    cols, rows = shutil.get_terminal_size(fallback=(100, 40))
    width = max(20, cols - 2)
    height = max(10, rows - 4)
    image = render_frame(width, height, -0.5, 0.0, 3.0 / width)
    print(image)


if __name__ == "__main__":
    if "--static" in sys.argv:
        static_render()
    else:
        try:
            animate_zoom()
        except KeyboardInterrupt:
            sys.stdout.write("\x1b[0m\n")
