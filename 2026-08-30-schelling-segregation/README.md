# Schelling's Segregation Model

A single-page canvas simulation of economist Thomas Schelling's 1971 segregation
model — the classic demonstration that strong group-level segregation can emerge
from mild individual preferences, with nobody in the system actually trying to
segregate.

## Why it's interesting

Each agent on the grid belongs to one of two groups and only asks a simple
question: *"is at least X% of my neighborhood the same color as me?"* If yes,
it's satisfied and stays put. If not, it hops to a random empty cell.

Set the threshold to something that sounds practically tolerant — say 35%,
meaning an agent is perfectly happy as long as roughly a third of its neighbors
match — and watch what happens anyway: within a couple dozen generations the
board reorganizes into large, near-homogeneous continents of one color or the
other. The "avg. same-type neighbors" stat climbs from ~50% (random noise) to
75-80%+, even though no agent ever asked for anything close to that. It's a
concrete, playable illustration of how weak individual preferences can compound
into strong emergent structure — a result Schelling first demonstrated with coins
and graph paper, decades before anyone ran it on a computer.

Drag the threshold slider down toward 0% and the board stays mixed. Push it up
and segregation gets faster and more total. There's a real phase-transition feel
to it around 30-40%.

## How it works

- 60x60 grid, 90% occupied, split evenly between "Group A" and "Group B", 10% empty.
- Each generation: every occupied cell checks its up-to-8 Moore neighbors. If the
  fraction of same-type neighbors (among occupied ones) is below the threshold,
  the agent is unsatisfied.
- All unsatisfied agents, in random order, jump to a random empty cell.
- Repeat until nobody moves (marked "Stable") or you pause it.

## Run it

No build step, no dependencies — just open `index.html` in any browser:

```
open index.html      # macOS
xdg-open index.html  # Linux
```

Use the **Tolerance threshold** slider to change how picky agents are, **Speed**
to control animation rate, **Step** to advance one generation at a time, **Run/Pause**
to animate continuously, and **New random grid** to reshuffle and start over.
