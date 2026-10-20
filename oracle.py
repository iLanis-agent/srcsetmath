#!/usr/bin/env python3
# Srcset Math oracle - mirrors engine.js with Fractions and math.ceil: pixels needed are an exact Fraction rounded up, the pick is the minimum over the listed widths that are wide enough.
import json, re, math, random
from fractions import Fraction as F

SLOT = "the slot width must be a whole number of px from 1 to 4000"
DENS = "the screen density must be a number from 1 to 5 with at most one decimal place"
LST = "the file widths must be 1 to 8 different whole numbers from 1 to 20000, separated by commas"
def num(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,5}", t) or not lo <= int(t) <= hi: raise ValueError(err)
    return int(t)
def dens(t):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9](\.[0-9])?", t) or not F(t) >= 1 or not F(t) <= 5: raise ValueError(DENS)
    return F(t)
def fx(v):  # Fraction with at most one decimal place to text
    t = v * 10
    assert t.denominator == 1
    t = int(t); ip, fp = divmod(t, 10)
    return f"{ip}.{fp}" if fp else str(ip)
def lst(t):
    if not isinstance(t, str) or t.strip() == "": raise ValueError(LST)
    parts = t.split(",")
    if len(parts) > 8: raise ValueError(LST)
    v = [num(p, LST, 1, 20000) for p in parts]
    if len(set(v)) != len(v): raise ValueError(LST)
    return v

def pix(n): return f"{n} pixel" if n == 1 else f"{n} pixels"
def need_(a, b):
    s = num(a, SLOT, 1, 4000); d = dens(b); t = s * d
    amt = "1 pixel" if t == 1 else fx(t) + " pixels"
    base = f"A {s}px wide slot on a {fx(d)}x screen needs {amt} across"
    return base + "." if t.denominator == 1 and t.numerator == int(t) else base + f", which rounds up to {pix(math.ceil(t))}."
def ladder(a, b):
    s = num(a, SLOT, 1, 4000); n = num(b, "the top density must be a whole number from 1 to 5", 1, 5)
    ws = [str(s * k) for k in range(1, n + 1)]; ls = [f"{k}x" for k in range(1, n + 1)]
    j = lambda x: x[0] if len(x) == 1 else ", ".join(x[:-1]) + " and " + x[-1]
    one = "1 pixel" if s == 1 else ws[0] + " pixels"
    if n == 1: return f"For a {s}px wide slot, the file needs to be {one} across for 1x screens."
    return f"For a {s}px wide slot, the files need to be {j(ws)} pixels across for {j(ls)} screens."
def pick(a, b, c):
    s = num(a, SLOT, 1, 4000); d = dens(b); L = lst(c)
    need = math.ceil(s * d); ok = [w for w in L if w >= need]
    head = f"The slot needs {pix(need)} across. "
    if not ok: return head + f"No listed file is wide enough. The widest, {max(L)}px, is {pix(need - max(L))} short."
    p = min(ok)
    if p == need: return head + f"The smallest listed file that is wide enough is {p}px, an exact fit."
    return head + f"The smallest listed file that is wide enough is {p}px, which is {pix(p - need)} more than needed."

FNS = {"needTruth": need_, "ladderTruth": ladder, "pickTruth": pick}

def cases():
    c = []
    slots = ["1", "300", "301", "4000", "333", "640", "17"]
    dd = ["1", "1.5", "2", "2.5", "3", "4", "5", "1.1", "2.625"[:3], "4.9", "1.0", "5.0"]
    for s in slots:
        for d in dd[:10]: c.append(("needTruth", [s, d]))
    for s in slots:
        for n in ["1", "2", "3", "4", "5"]: c.append(("ladderTruth", [s, n]))
    W = "320, 480, 640, 960"
    for s in ["300", "301", "100", "480", "1000", "4000", "1"]:
        for d in ["1", "1.5", "2", "3"]:
            c.append(("pickTruth", [s, d, W]))
    for w in ["600", "10, 20", "960,640,480,320", " 320 , 640 ", "1,2,3,4,5,6,7,8", "20000", "599, 600, 601"]:
        c.append(("pickTruth", ["300", "2", w])); c.append(("pickTruth", ["301", "2", w]))
    bad = ["", "x", "0", "1.5", "-1", "4001", "300000"]
    for v in bad: c += [("needTruth", [v, "2"]), ("ladderTruth", [v, "2"]), ("pickTruth", [v, "2", W])]
    for v in ["", "x", "0", "0.9", "5.1", "6", "1.55", "2.", ".5", "-2", "10"]: c += [("needTruth", ["300", v]), ("pickTruth", ["300", v, W])]
    for v in ["", "0", "6", "1.5", "x", "-1"]: c.append(("ladderTruth", ["300", v]))
    for v in ["", " ", "x", "0", "20001", "320,320", "320,", ",320", "1,2,3,4,5,6,7,8,9", "320 480", "3.5", "-5"]: c.append(("pickTruth", ["300", "2", v]))
    r = random.Random(707)
    for _ in range(25):
        s = str(r.randint(1, 4000)); d = f"{r.randint(1,4)}.{r.randint(0,9)}"
        ws = ",".join(str(x) for x in r.sample(range(1, 9000), r.randint(1, 8)))
        c.append(("needTruth", [s, d])); c.append(("pickTruth", [s, d, ws])); c.append(("ladderTruth", [s, str(r.randint(1, 5))]))
    return c

out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    f.write("[\n" + ",\n".join(json.dumps(o, separators=(",", ":")) for o in out) + "\n]\n")
print(len(out), "cases written")
