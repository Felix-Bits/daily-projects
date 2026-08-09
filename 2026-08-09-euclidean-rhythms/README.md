# Euclidean Rhythms

A single-page, no-dependency drum machine built entirely around one idea:
spread *k* beats as evenly as possible across *n* steps, and you get the
rhythms most of the world's percussion traditions independently arrived at —
the Cuban tresillo, the flamenco *soleá*, West African bell patterns, even
the bell pattern in Steve Reich's *Clapping Music*. This is the
[Euclidean rhythm](https://en.wikipedia.org/wiki/Euclidean_rhythm) algorithm
(Godfried Toussaint's 2005 formalization of Bjorklund's algorithm), made
audible.

## Why it's interesting

Five concentric rings, five drum voices (kick, snare, hat, clap, bell), each
with its own step count, pulse count, and rotation. A shared 16th-note clock
sweeps all five rings at once, so a 6-step ring and a 16-step ring loop at
different lengths but the same pulse rate — a polymeter, the same trick
Elektron's Euclidean sequencers use. Turning "pulses" up or down doesn't just
add random hits: the whole pattern re-flows to stay maximally even, which is
the entire point of the algorithm and is oddly satisfying to watch happen in
real time.

Every sound is synthesized on the spot with the Web Audio API — a
pitch-swept sine for the kick, filtered noise bursts for snare/hat/clap, two
detuned sines for the bell — so there are no audio files, no dependencies,
just oscillators and gain envelopes.

## How to run it

Open `index.html` in any modern browser (Chrome, Firefox, Safari — no
server, build step, or network access needed).

- **▶ Play** starts the shared clock.
- Each ring's **steps** / **pulses** / **rotate** sliders reshape that
  voice's Euclidean pattern live, even while playing.
- Click directly on a dot on the wheel to hand-toggle that step (overrides
  the generated pattern until you change steps/pulses/rotate again).
- **mute** silences a voice without stopping its ring from animating.
- **🎲 Randomize** rolls fresh steps/pulses/rotation for all five rings at
  once — a quick way to stumble into a groove you wouldn't have dialed in
  by hand.
- **BPM** slider changes tempo live.

Best with sound on.
