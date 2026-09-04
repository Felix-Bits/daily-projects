# Karplus-Strong Harp

A single-page Web Audio instrument built entirely on the Karplus-Strong plucked-string
algorithm — no samples, no synth libraries, just a ring buffer of noise that averages and
fades itself into a musical tone.

## Why it's interesting

Karplus-Strong is one of the oldest "cheat codes" in digital audio: instead of modeling a
vibrating string with physics equations, you fill a short buffer with white noise and then
repeatedly output the next sample and overwrite it with the average of itself and its
neighbor, scaled down slightly. That's it — two lines of math per sample. Yet it produces a
remarkably convincing plucked-string sound, because the averaging step is a low-pass filter:
high harmonics cancel out fastest, exactly like they do when you pluck a real string and its
sharp attack rounds off into a warm sustained tone.

The buffer's *length* is the pitch (`N = sampleRate / frequency`) — there's no oscillator, no
frequency parameter anywhere in the DSP code. This page makes that mechanism visible instead
of hiding it behind an API: the bottom strip is a live oscilloscope reading the actual ring
buffer of whichever string you last plucked, so you can watch the noise burst smooth itself
into a decaying wave in real time. The "Character" slider exposes the classic Karplus-Strong
extension: with some probability, a sample gets negated instead of averaged, breaking the
harmonic series and turning the pluck into an inharmonic drum hit.

## How to run

Open `index.html` in any modern browser (double-click it, or `open index.html` /
`xdg-open index.html`). No build step, no server, no dependencies.

- **Click** one of the 8 horizontal strings, or **press `a s d f g h j k`** to pluck the notes
  of a C major pentatonic-ish scale (C4 up to E5).
- **Sustain** controls the damping factor applied on each feedback pass — higher values ring
  out longer.
- **Character** blends from a clean string (0) toward a noisy drum (0.5) by randomly flipping
  the sign of samples in the feedback loop.
- **Volume** is an overall gain (soft-clipped with `tanh` so stacking plucks doesn't crackle).

Multiple strings can ring at once — polyphony comes from just running several independent
ring buffers and summing their output each sample.
