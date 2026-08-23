# Consistent Hashing Ring

A single-page interactive visualization of **consistent hashing** — the technique
behind sharding in distributed caches, databases, and CDNs (Dynamo, Cassandra,
memcached client libraries, etc.) — built to make its core payoff obvious at a glance:
adding or removing a server barely disturbs anything.

## Why it's interesting

The naive way to shard N keys across N servers is `hash(key) % N`. It's simple,
but the moment N changes (a server dies, you scale up), the modulus changes and
almost *every* key gets reassigned to a different server — a cache stampede or a
massive data migration.

Consistent hashing fixes this by placing both servers ("nodes") and keys on the
same circular hash ring (angle = `hash(name) / 2^32 * 360°`). A key belongs to
the first node clockwise from it. Removing a node only reshuffles the keys that
node owned — everyone else's assignment is untouched. Each node also gets a
few "virtual points" on the ring so ownership arcs are spread out instead of
one node getting a lucky giant slice.

The page puts both algorithms side by side and counts, live, how many keys
actually move on each add/remove — e.g. removing 1 of 3 nodes might move ~40%
of keys under consistent hashing, versus ~70%+ under naive mod-N, and the gap
widens fast as the node count grows.

While building this I actually hit a real bug worth mentioning: my first hash
function (plain FNV-1a) diffused trailing-character changes poorly, so virtual
points for the same node (`"node-A#0"`, `"node-A#1"`, `"node-A#2"`) landed
suspiciously close together on the ring instead of spreading out — which
silently broke the whole demo (nearly all keys funneled to whichever node
happened to own the largest empty gap). Fixed by adding a murmur3-style
`fmix32` avalanche finalizer after the FNV-1a mix. Verified with a headless
Playwright pass plus a standalone Node script comparing remap percentages
before/after the fix.

## How to run it

It's a single static HTML file with no build step and no dependencies.

```bash
open index.html          # macOS
# or just double-click the file, or serve it:
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Using it

- **+ Add node** / **− Remove node** — grows or shrinks the ring (up to 8 nodes).
  Each node gets 3 virtual points (small dots of the same color), and the ring
  is shaded by which node owns each arc.
- **+ Add key** — drops a new key (up to 30, from a fixed pool of realistic
  names like `user:42`, `cart:x12`) onto the ring.
- **Reset** — reseeds with 3 nodes and 10 keys.
- The right panel tracks, for the *last* add/remove, how many keys changed
  owner under consistent hashing vs. under naive `hash(key) % N`, both as raw
  counts and as a percentage bar. Keys that moved are highlighted with a red
  ring on the canvas.
