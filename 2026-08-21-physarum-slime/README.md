# Physarum Slime Mold Simulation

A single-page canvas simulation of *Physarum polycephalum* (slime mold) transport-network
formation, using the classic agent-based model popularized by Jeff Jones (2010) and later
by Sage Jenson's generative-art work.

## The idea

Tens of thousands of independent, blind "agents" wander a 2D dish. Each one only knows how
to do two things every step:

1. **Sense** the pheromone trail intensity at three points ahead of it — front-left,
   straight ahead, front-right.
2. **Turn** toward whichever of those three is strongest, then step forward and deposit a
   bit of its own trail.

That's the entire rule. No agent has a map, a goal, or any notion that a "network" is being
built. Yet after a few seconds, the trails self-reinforce into thin filaments, weak filaments
starve and vanish (nothing is depositing near them anymore), and what's left settles into a
branching, near-minimal network connecting the busiest regions — visually close to real
slime mold's famous experiments (e.g. approximating the Tokyo rail system by growing between
oat-flake "stations"). It's a nice demonstration of *stigmergy*: coordination through shared
environment markings rather than communication.

Two implementation details that mattered for getting a good-looking result instead of an
inert blob or a single dominant line:
- **Agents scatter uniformly across the whole dish** at start (not seeded from one point) —
  local trail fragments form everywhere and then merge into a connected network, rather than
  radiating from a single blob that never thins out.
- **The dish has walls, not a wraparound torus.** On a small periodic grid the network
  eventually collapses into one repeating stripe (a stable but boring pattern once every path
  competes for the same wraparound shortcut). Bounded edges with reflecting agents keep it a
  genuine branching tree.

## Run it

Just open `index.html` in any modern browser — no build step, no dependencies:

```
open index.html      # macOS
xdg-open index.html  # Linux
```

Pick a preset from the dropdown (Transport network, Veins, Chaotic swarm, Radial bloom —
each is a different sensor angle / turn angle / deposit-rate combination) and hit **Restart**
to reseed. Uncheck "color trail" for a plain grayscale heat-map view of the pheromone field.
