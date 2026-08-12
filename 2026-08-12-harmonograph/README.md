# Harmonograph

A single-page, no-dependency canvas toy that simulates a **harmonograph** —
the Victorian drawing machine where two or three pendulums, swinging
independently, are rigged to a pen suspended over a sheet of paper. As the
pendulums swing and slowly lose energy to friction, the pen traces looping,
symmetric curves that spiral inward to a stop.

## Why it's interesting

There's no simulation of the pendulums' physical arms or pivots — just the
math they imply. Each axis is driven by the sum of two damped sine waves:

```
x(t) = A·sin(f1·t + p1)·e^(-d·t) + A·sin(f2·t + p2)·e^(-d·t)
y(t) = A·sin(f3·t + p3)·e^(-d·t) + A·sin(f4·t + p4)·e^(-d·t)
```

Four frequencies is all it takes to go from a boring ellipse to an intricate
many-petaled rosette. The shape that comes out depends almost entirely on
the *ratio* between the frequencies: small integer ratios like 2:3 or 3:5
close into clean, repeating rosettes (the way a real pendulum harmonograph
does when its two pendulums share a rational frequency relationship),
while near-irrational ratios spiral for a long time without ever quite
retracing themselves. The damping term is what turns an infinite Lissajous
curve into a finite drawing — energy bleeds out of the system every period,
so the curve always spirals down to a single point in the end, just like
the real, physical machine running out of momentum.

## Run it

Open `index.html` directly in any browser — everything is inline HTML/CSS/JS,
no build step, no server, no dependencies.

- **Sliders** control the four drive frequencies, two of the phase offsets,
  the damping rate, and the overall amplitude. Changing any slider clears
  the canvas and starts a fresh curve from t=0.
- **randomize** picks a new set of (mostly near-integer) frequencies, phases,
  damping, and amplitude — try it repeatedly to see how much variety four
  numbers can produce.
- **clear** wipes the canvas and restarts the current parameters from t=0.
- **pause** / **resume** freezes the drawing in place.
- **hide panel** tucks the controls away so you can see the full drawing.

The stroke color slowly cycles through the hue wheel as the curve is drawn,
so older and newer parts of the same curve are easy to tell apart.
