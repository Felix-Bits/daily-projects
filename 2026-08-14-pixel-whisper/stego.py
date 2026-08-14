#!/usr/bin/env python3
"""Pixel Whisper: hide a text message in the least-significant bits of a PPM image.

Pure standard library. No image libraries needed because PPM (P6) is a
trivial binary format: a short text header followed by raw R,G,B bytes.
"""

import argparse
import struct
import sys

LENGTH_HEADER_BITS = 32  # bits reserved up front for the message's byte length


def read_ppm(path):
    with open(path, "rb") as f:
        data = f.read()
    if not data.startswith(b"P6"):
        raise ValueError(f"{path}: not a binary PPM (P6) file")

    pos = 2
    tokens = []
    while len(tokens) < 3:
        while data[pos:pos + 1].isspace():
            pos += 1
        if data[pos:pos + 1] == b"#":
            while data[pos:pos + 1] not in (b"\n", b""):
                pos += 1
            continue
        start = pos
        while not data[pos:pos + 1].isspace():
            pos += 1
        tokens.append(data[start:pos])
    width, height, maxval = (int(t) for t in tokens)
    pos += 1  # single whitespace byte separating header from pixel data

    pixel_count = width * height * 3
    pixels = bytearray(data[pos:pos + pixel_count])
    if len(pixels) != pixel_count:
        raise ValueError(f"{path}: truncated pixel data")
    return width, height, maxval, pixels


def write_ppm(path, width, height, maxval, pixels):
    with open(path, "wb") as f:
        f.write(f"P6\n{width} {height}\n{maxval}\n".encode("ascii"))
        f.write(bytes(pixels))


def make_sample(path, width=160, height=120):
    """Procedurally generate a gradient + checker cover image, no source photo needed."""
    pixels = bytearray(width * height * 3)
    for y in range(height):
        for x in range(width):
            i = (y * width + x) * 3
            pixels[i] = int(255 * x / width)
            pixels[i + 1] = int(255 * y / height)
            pixels[i + 2] = 255 if ((x // 8) ^ (y // 8)) % 2 == 0 else 60
    write_ppm(path, width, height, 255, pixels)
    return width, height


def _bits_of_bytes(data):
    for byte in data:
        for i in range(7, -1, -1):
            yield (byte >> i) & 1


def _bytes_of_bits(bits):
    out = bytearray()
    for i in range(0, len(bits) - 7, 8):
        b = 0
        for j in range(8):
            b = (b << 1) | bits[i + j]
        out.append(b)
    return bytes(out)


def capacity_bytes(pixels):
    usable_bits = len(pixels) - LENGTH_HEADER_BITS
    return max(usable_bits, 0) // 8


def encode(in_path, out_path, message):
    width, height, maxval, pixels = read_ppm(in_path)
    message_bytes = message.encode("utf-8")

    header_bits = list(_bits_of_bytes(struct.pack(">I", len(message_bytes))))
    payload_bits = list(_bits_of_bytes(message_bytes))
    total_bits = header_bits + payload_bits

    if len(total_bits) > len(pixels):
        raise ValueError(
            f"message needs {len(total_bits)} bits but the image only holds "
            f"{len(pixels)} ({capacity_bytes(pixels)} bytes max)"
        )

    for i, bit in enumerate(total_bits):
        pixels[i] = (pixels[i] & 0xFE) | bit

    write_ppm(out_path, width, height, maxval, pixels)
    return len(message_bytes), capacity_bytes(pixels)


def decode(in_path):
    _, _, _, pixels = read_ppm(in_path)
    length_bits = [pixels[i] & 1 for i in range(LENGTH_HEADER_BITS)]
    length = struct.unpack(">I", _bytes_of_bits(length_bits))[0]

    start = LENGTH_HEADER_BITS
    end = start + length * 8
    if length < 0 or end > len(pixels):
        raise ValueError("corrupt stego image, or no message was ever hidden here")

    payload_bits = [pixels[i] & 1 for i in range(start, end)]
    return _bytes_of_bits(payload_bits).decode("utf-8")


def diff_stats(path_a, path_b):
    wa, ha, _, pa = read_ppm(path_a)
    wb, hb, _, pb = read_ppm(path_b)
    if (wa, ha) != (wb, hb):
        raise ValueError("images have different dimensions")
    changed = sum(1 for x, y in zip(pa, pb) if x != y)
    max_delta = max((abs(x - y) for x, y in zip(pa, pb)), default=0)
    return changed, len(pa), max_delta


ANSI_RESET = "\x1b[0m"


def preview(path, cols=80):
    """Render a downsampled terminal preview using half-block double vertical resolution."""
    width, height, _, pixels = read_ppm(path)

    def pixel_at(px, py):
        px = min(px, width - 1)
        py = min(py, height - 1)
        i = (py * width + px) * 3
        return pixels[i], pixels[i + 1], pixels[i + 2]

    cols = min(cols, width)
    rows = int(height * (cols / width) / 2)  # /2 because each row of text = 2 pixel rows
    rows = max(rows, 1)

    lines = []
    for row in range(rows):
        y_top = int(row * 2 * height / (rows * 2))
        y_bot = int((row * 2 + 1) * height / (rows * 2))
        line = []
        for col in range(cols):
            x = int(col * width / cols)
            rt, gt, bt = pixel_at(x, y_top)
            rb, gb, bb = pixel_at(x, y_bot)
            line.append(f"\x1b[38;2;{rt};{gt};{bt}m\x1b[48;2;{rb};{gb};{bb}m▀")
        lines.append("".join(line) + ANSI_RESET)
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_sample = sub.add_parser("gen-sample", help="generate a procedural cover image")
    p_sample.add_argument("--out", default="sample.ppm")
    p_sample.add_argument("--width", type=int, default=160)
    p_sample.add_argument("--height", type=int, default=120)

    p_enc = sub.add_parser("encode", help="hide a message inside an image")
    p_enc.add_argument("--in", dest="in_path", required=True)
    p_enc.add_argument("--out", dest="out_path", required=True)
    p_enc.add_argument("--message", required=True)

    p_dec = sub.add_parser("decode", help="extract a hidden message")
    p_dec.add_argument("--in", dest="in_path", required=True)

    p_diff = sub.add_parser("diff", help="compare two images byte-for-byte")
    p_diff.add_argument("a")
    p_diff.add_argument("b")

    p_prev = sub.add_parser("preview", help="render an image in the terminal")
    p_prev.add_argument("--in", dest="in_path", required=True)
    p_prev.add_argument("--cols", type=int, default=80)

    args = parser.parse_args(argv)

    if args.command == "gen-sample":
        w, h = make_sample(args.out, args.width, args.height)
        print(f"wrote {args.out} ({w}x{h})")

    elif args.command == "encode":
        used, cap = encode(args.in_path, args.out_path, args.message)
        print(f"hid {used} bytes of {cap} available -> {args.out_path}")

    elif args.command == "decode":
        print(decode(args.in_path))

    elif args.command == "diff":
        changed, total, max_delta = diff_stats(args.a, args.b)
        pct = 100 * changed / total if total else 0
        print(f"{changed}/{total} bytes differ ({pct:.3f}%), max channel delta = {max_delta}")

    elif args.command == "preview":
        print(preview(args.in_path, args.cols))

    return 0


if __name__ == "__main__":
    sys.exit(main())
