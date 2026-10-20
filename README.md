# Srcset Math

Responsive image width arithmetic. A 300px wide image slot on a 2x screen needs 600 pixels across, so a 640px wide file is the smallest one in a 320, 480, 640, 960 list that is wide enough.

## What it computes

- **The need truth** - the pixels across a slot needs on a screen density (slot 1 to 4000 CSS px, density 1 to 5 with one decimal place), rounded up to whole pixels.
- **The ladder truth** - the file widths for 1x up to a whole-number top density (1 to 5).
- **The pick truth** - the smallest file in your list (1 to 8 different widths, 1 to 20000) that is at least as wide as the need, and how many pixels more it has. If none is wide enough, how many pixels short the widest is.

## Boundary

Arithmetic only. It has not seen any image or page. It does not know image quality, file sizes or layout, how a browser will really choose between files, or whether the pictures will look good, and it gives no verdict that a set of files is right. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers).
- `oracle.py` - the Python mirror (Fractions, math.ceil, minimum over the wide-enough files) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (283 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/srcsetmath/
Repo: https://github.com/iLanis-agent/srcsetmath
