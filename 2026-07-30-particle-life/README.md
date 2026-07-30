# Particle Life

A single-page canvas simulation of "particle life" — a handful of colored particle
species pushing and pulling on each other according to a random attraction matrix,
producing lifelike clusters, orbits, chases, and membranes with no rule that ever
says "flock," "hunt," or "cluster."

## Why it's interesting

Every pair of species gets a random number in `[-1, 1]`: positive means attract,
negative means repel, and every particle always repels anything that gets too
close (so things don't collapse into a point). That's the entire rulebook — a
6x6 matrix of 36 numbers, re-rolled per particle-species pair, applied identically
to every particle every frame. There's no notion of a "group" or a "goal"
anywhere in the code. And yet depending on the matrix you get: predator/prey
chases (species A flees B, B chases A), stable orbiting rings, cell-like blobs
with a repelling membrane, or a static frozen mess — the same three lines of
physics producing wildly different "species" of emergent behavior each time you
reroll. The matrix is shown live in the top-right corner so you can see the
"genome" that's driving whatever pattern is currently on screen.

The world wraps at the edges (a torus, so nothing gets lost off-screen), and the
attraction/repulsion strength for each pair fades in from a repulsive core,
peaks in the middle of the interaction radius, and fades back to zero at the
edge — the classic "particle life" force curve.

## Run it

Open `index.html` directly in a browser — no server, no build step, no
dependencies.

- **Randomize rules** — reroll the 6x6 attraction matrix for a completely new
  "universe" (particles keep their current positions, but now obey new rules)
- **Reset particles** — respawn all particles at random positions under the
  current rules
- **Pause / Resume** — freeze or continue the simulation
- **Particles per type** — how many particles each of the 6 species has
- **Friction** — how quickly velocity bleeds off each frame; higher friction
  settles into stable clusters faster, lower friction gives looser, more fluid
  motion
