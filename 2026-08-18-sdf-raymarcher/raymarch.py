#!/usr/bin/env python3
"""ASCII/ANSI raymarched 3D renderer, pure stdlib.

No triangles, no rasterizer: the scene is defined purely as a signed
distance function (SDF) — for any 3D point, "how far to the nearest
surface?". Each screen ray is sphere-traced: step forward by exactly that
safe distance, repeat, until the distance is ~0 (a hit) or too large (a
miss). Surface normals fall out of the SDF's gradient, lit with a
diffuse + Blinn-Phong specular model, and shaded in 24-bit ANSI color
using half-block characters for double vertical resolution (same trick
as a classic terminal fire effect, applied to a real 3D camera instead).

The scene itself is a smoothly-blended torus + orbiting sphere, tumbling
in place — smin() (a polynomial "soft minimum") is what makes the sphere
melt into the torus instead of just overlapping it.

Usage:
    python3 raymarch.py              # run until Ctrl+C
    python3 raymarch.py --frames 50  # run exactly 50 frames then exit
    python3 raymarch.py --width 60 --height 24 --fps 10
"""
import argparse
import math
import shutil
import sys
import time

MAX_STEPS = 40
MAX_DIST = 10.0
EPS = 0.006
LIGHT_DIR = None  # set in main() after normalization


def vsub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def vadd(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vscale(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


def vdot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vlen(a):
    return math.sqrt(vdot(a, a))


def vnorm(a):
    l = vlen(a)
    return (a[0] / l, a[1] / l, a[2] / l) if l > 1e-9 else (0.0, 0.0, 0.0)


def sd_torus(p, big_r, small_r):
    qx = math.hypot(p[0], p[2]) - big_r
    return math.hypot(qx, p[1]) - small_r


def sd_sphere(p, r):
    return vlen(p) - r


def smin(a, b, k):
    """Polynomial smooth minimum: blends two surfaces instead of a hard union."""
    h = max(k - abs(a - b), 0.0) / k
    return min(a, b) - h * h * h * k * (1.0 / 6.0)


def rotate_y(p, a):
    ca, sa = math.cos(a), math.sin(a)
    x, y, z = p
    return (x * ca + z * sa, y, -x * sa + z * ca)


def rotate_x(p, a):
    ca, sa = math.cos(a), math.sin(a)
    x, y, z = p
    return (x, y * ca - z * sa, y * sa + z * ca)


def scene_sdf(p, t):
    q = rotate_x(rotate_y(p, t * 0.6), t * 0.37)
    torus = sd_torus(q, 1.1, 0.42)
    orbit = (0.9 * math.sin(t * 1.7), 0.55 * math.cos(t * 1.7), 0.0)
    sphere = sd_sphere(vsub(q, orbit), 0.5)
    return smin(torus, sphere, 0.6)


def estimate_normal(p, t):
    e = 0.0015
    dx = scene_sdf((p[0] + e, p[1], p[2]), t) - scene_sdf((p[0] - e, p[1], p[2]), t)
    dy = scene_sdf((p[0], p[1] + e, p[2]), t) - scene_sdf((p[0], p[1] - e, p[2]), t)
    dz = scene_sdf((p[0], p[1], p[2] + e), t) - scene_sdf((p[0], p[1], p[2] - e), t)
    return vnorm((dx, dy, dz))


def raymarch(ro, rd, t):
    dist = 0.0
    for _ in range(MAX_STEPS):
        p = vadd(ro, vscale(rd, dist))
        d = scene_sdf(p, t)
        if d < EPS:
            return p
        dist += d
        if dist > MAX_DIST:
            return None
    return None


def shade(p, rd, t):
    n = estimate_normal(p, t)
    diff = max(vdot(n, LIGHT_DIR), 0.0)
    half_v = vnorm(vsub(LIGHT_DIR, rd))
    spec = max(vdot(n, half_v), 0.0) ** 40
    return 0.12 + 0.78 * diff + 1.1 * spec


STOPS = [
    (0.0, (10, 6, 30)),
    (0.3, (90, 20, 120)),
    (0.65, (30, 150, 210)),
    (1.0, (170, 235, 255)),
    (1.5, (255, 255, 255)),
]


def color_from_intensity(inten):
    inten = min(inten, STOPS[-1][0])
    for (t0, c0), (t1, c1) in zip(STOPS, STOPS[1:]):
        if inten <= t1:
            f = (inten - t0) / (t1 - t0)
            return tuple(int(c0[i] + (c1[i] - c0[i]) * f) for i in range(3))
    return STOPS[-1][1]


def bg_color(ny):
    top, bottom = (10, 9, 26), (2, 2, 10)
    f = (ny + 1) / 2
    return tuple(int(top[i] + (bottom[i] - top[i]) * f) for i in range(3))


def render_frame(width, height, t):
    cam_pos = (0.0, 0.0, -3.6)
    sub_h = height * 2
    aspect = width / sub_h
    rows = []
    for cy in range(height):
        chars = []
        for cx in range(width):
            px_colors = []
            for sub in (0, 1):
                py = cy * 2 + sub
                nx = ((cx + 0.5) / width * 2 - 1) * aspect
                ny = 1 - (py + 0.5) / sub_h * 2
                rd = vnorm((nx, ny, 1.0))
                hit = raymarch(cam_pos, rd, t)
                if hit is not None:
                    px_colors.append(color_from_intensity(shade(hit, rd, t)))
                else:
                    px_colors.append(bg_color(ny))
            top, bot = px_colors
            chars.append(
                f"\x1b[38;2;{top[0]};{top[1]};{top[2]}m"
                f"\x1b[48;2;{bot[0]};{bot[1]};{bot[2]}m▀"
            )
        rows.append("".join(chars) + "\x1b[0m")
    return "\x1b[H" + "\n".join(rows)


def main():
    global LIGHT_DIR
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--frames", type=int, default=0, help="run N frames then exit (0 = forever)")
    parser.add_argument("--fps", type=float, default=12.0, help="target frames per second")
    parser.add_argument("--width", type=int, default=0, help="render width in characters (0 = auto)")
    parser.add_argument("--height", type=int, default=0, help="render height in characters (0 = auto)")
    args = parser.parse_args()

    LIGHT_DIR = vnorm((0.6, 0.8, -0.6))

    cols, rows = shutil.get_terminal_size((80, 24))
    width = args.width or max(20, min(cols, 70))
    height = args.height or max(12, min(rows - 1, 30))

    sys.stdout.write("\x1b[2J\x1b[?25l")
    frame_count = 0
    t = 0.0
    try:
        while args.frames == 0 or frame_count < args.frames:
            start = time.time()
            sys.stdout.write(render_frame(width, height, t))
            sys.stdout.flush()
            frame_count += 1
            t += 0.06
            elapsed = time.time() - start
            time.sleep(max(0.0, 1.0 / args.fps - elapsed))
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[0m\x1b[?25h\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
