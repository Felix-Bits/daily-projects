# JSON Diff CLI

A small command-line tool that recursively diffs two JSON files and prints a colorized, dot-path report of what changed — additions in green, removals in red, changed values in yellow.

It's a genuinely useful pocket tool: comparing two config files, two API responses, or two versions of a data export usually means squinting at two blobs of text side by side. This walks the structure recursively (objects by key, arrays by index) and reports exactly which paths differ, with old and new values shown inline.

Pure Python standard library — no dependencies, no install step.

## Run it

```
python3 jsondiff.py example_a.json example_b.json
```

Sample output:

```
~ config.retries: 3 -> 5
- config.timeout: 30
+ tags[2]: "beta"
~ version: "1.2.0" -> "1.3.0"
```

Exits with status `0` if the files are identical, `1` if differences were found (handy for scripting/CI checks).

Try it on your own files:

```
python3 jsondiff.py path/to/old.json path/to/new.json
```
