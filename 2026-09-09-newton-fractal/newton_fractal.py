#!/usr/bin/env python3
"""Terminal Newton fractal renderer with ANSI color and a zoom animation.

Pure standard library, no dependencies. Run directly with python3.

Newton's method for finding a root of f(z) = 0 iterates
    z_{n+1} = z_n - f(z_n) / f'(z_n)
Applied to a real function this converges to *a* root from almost any
starting guess. Applied to a *complex* function and started from every
point in the complex plane, something wilder happens: for polynomials
with more than one root, the set of starting points that converge to each
root forms an intricate, infinitely detailed "basin of attraction" whose
boundary is a fractal. Nearby points can be flung toward completely
different roots after just a few iterations -- textbook sensitive
dependence on initial conditions, produced by a numerical method taught
in first-year calculus as if it always behaves politely.

Each pixel is colored by *which* root it converged to, and shaded by *how
fast* -- fewer iterations to converge means brighter. Basin interiors are
smooth; the boundary between basins is where the chaos lives.
"""
import cmath
import shutil
import sys
import time

MAX_ITER = 40
TOL = 1e-6

# Colors for each root's basin (r, g, b), brightest at convergence.
ROOT_COLORS = [
    (255, 90, 90),   # red
    (90, 200, 255),  # cyan
    (255, 220, 90),  # yellow
    (140, 255, 140), # green
    (200, 140, 255), # violet
]


def poly_and_roots(degree):
    """f(z) = z^degree - 1, f'(z) = degree * z^(degree-1).

    Roots are the `degree`-th roots of unity, evenly spaced on the unit
    circle -- enough to keep the basin count (and color count) equal to
    the exponent you pick.
    """
    roots = [cmath.exp(2j * cmath.pi * k / degree) for k in range(degree)]

    def f(z):
        return z ** degree - 1

    def fprime(z):
        return degree * z ** (degree - 1)

    return f, fprime, roots


def newton_iters(z, f, fprime, roots):
    """Run Newton's method from z; return (root_index, iterations_taken)."""
    for i in range(MAX_ITER):
        fz = f(z)
        if abs(fz) < TOL:
            break
        d = fprime(z)
        if d == 0:
            break
        z = z - fz / d
    best = min(range(len(roots)), key=lambda k: abs(z - roots[k]))
    return best, i


def shade(rgb, t):
    """t in [0, 1]: 1 = just converged (bright), 0 = maxed out (dark)."""
    r, g, b = rgb
    return (int(r * t), int(g * t), int(b * t))


def render_frame(width, height, cx, cy, scale, degree):
    f, fprime, roots = poly_and_roots(degree)
    aspect_fix = 0.5  # terminal cells are roughly twice as tall as wide
    # Sample two vertical sub-rows per text row so a half-block character
    # can carry two pixels (foreground = top half, background = bottom half),
    # doubling the effective vertical resolution.
    out_rows = []
    for row in range(height):
        top_y = cy + (2 * row - height) * scale * aspect_fix
        bot_y = cy + (2 * row + 1 - height) * scale * aspect_fix
        chars = []
        for col in range(width):
            x = cx + (col - width / 2) * scale

            k, it = newton_iters(complex(x, top_y), f, fprime, roots)
            top_rgb = shade(ROOT_COLORS[k % len(ROOT_COLORS)], 1.0 - it / MAX_ITER)

            k, it = newton_iters(complex(x, bot_y), f, fprime, roots)
            bot_rgb = shade(ROOT_COLORS[k % len(ROOT_COLORS)], 1.0 - it / MAX_ITER)

            tr, tg, tb = top_rgb
            br, bg, bb = bot_rgb
            chars.append(f"\x1b[38;2;{tr};{tg};{tb}m\x1b[48;2;{br};{bg};{bb}m▀")
        out_rows.append("".join(chars) + "\x1b[0m")
    return "\n".join(out_rows)


def animate_zoom(degree=3, target=(0.30096, 0.02), frames=45, delay=0.06):
    """Zoom into a point on the basin boundary near a root, where the
    fractal detail is densest."""
    cols, rows = shutil.get_terminal_size(fallback=(100, 40))
    width = max(20, cols - 2)
    height = max(10, (rows - 3))
    scale = 2.4 / width

    sys.stdout.write("\x1b[2J")
    for frame in range(frames):
        image = render_frame(width, height, target[0], target[1], scale, degree)
        sys.stdout.write("\x1b[H")
        sys.stdout.write(image)
        sys.stdout.write(
            f"\n\x1b[0mNewton fractal for z^{degree} - 1 = 0   "
            f"frame {frame + 1}/{frames}   scale={scale:.2e}\n"
        )
        sys.stdout.flush()
        scale *= 0.87
        time.sleep(delay)
    sys.stdout.write("\nDone. Try: python3 newton_fractal.py 5\n")


if __name__ == "__main__":
    degree = 3
    if len(sys.argv) > 1:
        try:
            degree = max(2, min(len(ROOT_COLORS), int(sys.argv[1])))
        except ValueError:
            pass
    try:
        animate_zoom(degree=degree)
    except KeyboardInterrupt:
        sys.stdout.write("\x1b[0m\n")
