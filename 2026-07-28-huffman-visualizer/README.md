# Huffman Tree Visualizer

A single-page, no-dependency visualization of Huffman coding: type text, watch the greedy merge algorithm build a coding tree one step at a time, then see the actual bit codes it assigns and how much smaller the text gets.

It's interesting because Huffman coding is usually explained with a static diagram — here you watch the "forest" of frequency chips shrink in real time as the two rarest characters keep pairing off, then get the final tree drawn as an SVG with 0/1 edge labels, a per-character code table, and a live compression ratio against plain 8-bit-per-char encoding. It also handles the classic edge case (a string with only one distinct character) by giving that character a synthetic sibling so it still gets a real 1-bit code instead of an empty one.

## Run it

Open `index.html` directly in a browser — no server, no build step, no dependencies.

1. Type or paste any text (defaults to a pangram).
2. Click **Build tree** to compute character frequencies and the full merge sequence.
3. Click **Play** to watch it animate automatically, or **Step** to advance one merge at a time. The speed slider controls playback pace.
4. Once merging finishes, the final tree, code table, and compression stats appear below.
