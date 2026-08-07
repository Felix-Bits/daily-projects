#!/usr/bin/env python3
"""Brainfuck Theater: an animated, in-place terminal visualizer for a
Brainfuck interpreter. Watch the tape, the pointer, and the source's
instruction pointer move in lockstep as an esoteric program runs.

Usage:
    python3 bf_theater.py hello           # animate "Hello World!"
    python3 bf_theater.py count           # animate a counting loop (0-9)
    python3 bf_theater.py hello --speed 0.06
    python3 bf_theater.py count --fast    # skip animation, just run it
"""
import sys
import time
import argparse

TAPE_SIZE = 100
WINDOW = 10  # cells shown on each side of the pointer

RESET = "\033[0m"
REVERSE = "\033[7m"
DIM = "\033[2m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"

DESCRIPTIONS = {
    ">": "move pointer right",
    "<": "move pointer left",
    "+": "increment cell",
    "-": "decrement cell",
    ".": "output cell as char",
    ",": "read input into cell",
    "[": "jump past ] if cell == 0",
    "]": "jump back to [ if cell != 0",
}


def build_counter_program():
    """A hand-generated (not hand-typed) Brainfuck program: sets cell0 to
    10 as a loop counter, cell1 to 48 ('0'), then prints '0'..'9'."""
    return "+" * 10 + ">" + "+" * 48 + "<" + "[" + ">.+<" + "-" + "]"


PROGRAMS = {
    "hello": (
        "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]"
        ">>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
    ),
    "count": build_counter_program(),
}


def match_brackets(program):
    stack = []
    pairs = {}
    for i, c in enumerate(program):
        if c == "[":
            stack.append(i)
        elif c == "]":
            if not stack:
                raise ValueError(f"unmatched ] at {i}")
            j = stack.pop()
            pairs[i] = j
            pairs[j] = i
    if stack:
        raise ValueError(f"unmatched [ at {stack[-1]}")
    return pairs


class Interpreter:
    def __init__(self, program):
        self.program = "".join(c for c in program if c in "><+-.,[]")
        self.pairs = match_brackets(self.program)
        self.tape = [0] * TAPE_SIZE
        self.ptr = 0
        self.ip = 0
        self.output = []

    @property
    def done(self):
        return self.ip >= len(self.program)

    def step(self):
        c = self.program[self.ip]
        if c == ">":
            self.ptr = (self.ptr + 1) % TAPE_SIZE
        elif c == "<":
            self.ptr = (self.ptr - 1) % TAPE_SIZE
        elif c == "+":
            self.tape[self.ptr] = (self.tape[self.ptr] + 1) % 256
        elif c == "-":
            self.tape[self.ptr] = (self.tape[self.ptr] - 1) % 256
        elif c == ".":
            self.output.append(chr(self.tape[self.ptr]))
        elif c == ",":
            self.tape[self.ptr] = 0
        elif c == "[":
            if self.tape[self.ptr] == 0:
                self.ip = self.pairs[self.ip]
        elif c == "]":
            if self.tape[self.ptr] != 0:
                self.ip = self.pairs[self.ip]
        self.ip += 1


def render_source(program, ip):
    """Render the source with the current instruction reverse-video, in a
    sliding window so long programs stay on one line."""
    width = 60
    start = max(0, ip - width // 2)
    end = min(len(program), start + width)
    start = max(0, end - width)
    chunk = program[start:end]
    pos = ip - start
    out = []
    for i, c in enumerate(chunk):
        if i == pos:
            out.append(f"{REVERSE}{YELLOW}{c}{RESET}")
        else:
            out.append(f"{DIM}{c}{RESET}")
    return "".join(out)


def render_tape(tape, ptr):
    indices = [(ptr + off) % TAPE_SIZE for off in range(-WINDOW, WINDOW + 1)]
    cells = []
    labels = []
    for idx in indices:
        val = tape[idx]
        text = f"{val:3d}"
        if idx == ptr:
            cells.append(f"{REVERSE}{CYAN}{text}{RESET}")
            labels.append(f"{CYAN} ^ {RESET}")
        elif val != 0:
            cells.append(f"{GREEN}{text}{RESET}")
            labels.append("   ")
        else:
            cells.append(f"{DIM}{text}{RESET}")
            labels.append("   ")
    return " ".join(cells), " ".join(labels)


def frame(interp, name):
    lines = []
    lines.append(f"{MAGENTA}Brainfuck Theater{RESET} — running {YELLOW}{name}{RESET}")
    lines.append("")
    lines.append("source:")
    lines.append("  " + render_source(interp.program, min(interp.ip, len(interp.program) - 1)))
    if not interp.done:
        c = interp.program[interp.ip]
        lines.append(f"  {DIM}next: {c!r} — {DESCRIPTIONS.get(c, '')}{RESET}")
    else:
        lines.append(f"  {DIM}(halted){RESET}")
    lines.append("")
    lines.append(f"tape (pointer at cell {interp.ptr}):")
    cells, labels = render_tape(interp.tape, interp.ptr)
    lines.append("  " + cells)
    lines.append("  " + labels)
    lines.append("")
    lines.append("output:")
    lines.append("  " + "".join(interp.output) + f"{REVERSE} {RESET}")
    return "\n".join(lines)


def animate(interp, name, speed):
    prev_lines = 0
    while True:
        text = frame(interp, name)
        n_lines = text.count("\n") + 1
        if prev_lines:
            sys.stdout.write(f"\033[{prev_lines}A")
        sys.stdout.write("\033[J")
        sys.stdout.write(text + "\n")
        sys.stdout.flush()
        prev_lines = n_lines
        if interp.done:
            break
        interp.step()
        time.sleep(speed)
    print()


def run_fast(interp):
    while not interp.done:
        interp.step()
    print("".join(interp.output))


def main():
    parser = argparse.ArgumentParser(description="Animated Brainfuck interpreter/visualizer.")
    parser.add_argument("program", choices=sorted(PROGRAMS), help="which sample program to run")
    parser.add_argument("--speed", type=float, default=0.04, help="seconds between steps (default 0.04)")
    parser.add_argument("--fast", action="store_true", help="run to completion without animation")
    args = parser.parse_args()

    interp = Interpreter(PROGRAMS[args.program])
    if args.fast:
        run_fast(interp)
    else:
        try:
            animate(interp, args.program, args.speed)
        except KeyboardInterrupt:
            print(f"\n{RESET}interrupted")


if __name__ == "__main__":
    main()
