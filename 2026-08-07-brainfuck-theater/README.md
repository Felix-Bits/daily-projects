# Brainfuck Theater

A terminal "theater" for watching a **Brainfuck** program actually run:
the tape, the pointer, and the source's instruction pointer all animate
in place, one instruction at a time, so you can *see* how eight symbols
(`><+-.,[]`) turn into "Hello World!".

Pure-stdlib Python, 24-bit-free ANSI (just basic SGR codes), no
dependencies.

## Why it's interesting

Brainfuck is a famous esoteric programming language: a single tape of
byte cells, a pointer, and eight one-character instructions — no
variables, no functions, no numbers in the source at all. It's usually
either run silently or read as an inscrutable wall of symbols. This
project turns the interpreter inside-out: every step redraws the tape
window around the pointer (dim for zero cells, green for touched ones,
reverse-video for the pointer itself), highlights the instruction about
to execute in the source line, and grows the output live. Watching the
classic Hello World program's opening `[...]` loop, you can actually see
it multiplying 8 by increasing amounts into four tape cells to build up
the ASCII codes for `H`, `e`, `l`, `o` before a single character is
printed — the "trick" becomes visible instead of theoretical.

The second sample program, `count`, is generated (not hand-typed) by a
tiny Python helper in the script to keep it obviously correct: it sets
one cell to 10 as a loop counter and another to 48 (`'0'`), then loops
`print, increment, decrement-counter` to print `0123456789` — a clean,
short loop to watch cell values climb in real time.

## How to run it

```bash
cd 2026-08-07-brainfuck-theater
python3 bf_theater.py hello          # animate the classic Hello World program
python3 bf_theater.py count          # animate a short counting loop
python3 bf_theater.py hello --speed 0.08   # slower animation
python3 bf_theater.py count --fast   # skip the animation, just print the result
```

Requires Python 3 and a terminal that understands basic ANSI escape
codes (any modern terminal). No install, no dependencies.
