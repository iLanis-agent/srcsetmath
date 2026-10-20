// Srcset Math engine: responsive image width arithmetic. Pixels a slot needs on a screen density, the file widths for 1x up to Nx, and the smallest listed file that is wide enough. Exact integers.
function _int(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,5}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _SLOT = "the slot width must be a whole number of px from 1 to 4000";
var _DENS = "the screen density must be a number from 1 to 5 with at most one decimal place";
function _dens(t) { // tenths
  t = typeof t === "string" ? t.trim() : "";
  var m = /^([0-9])(?:\.([0-9]))?$/.exec(t);
  if (!m) throw new Error(_DENS);
  var v = parseInt(m[1], 10) * 10 + (m[2] ? parseInt(m[2], 10) : 0);
  if (v < 10 || v > 50) throw new Error(_DENS);
  return v;
}
function _dec1(v) { var s = String(Math.floor(v / 10)), f = v % 10; return f ? s + "." + f : s; }
function _list(t) {
  var err = "the file widths must be 1 to 8 different whole numbers from 1 to 20000, separated by commas";
  if (typeof t !== "string" || t.trim() === "") throw new Error(err);
  var parts = t.split(","), out = [];
  if (parts.length > 8) throw new Error(err);
  for (var i = 0; i < parts.length; i++) {
    var v = _int(parts[i], err, 1, 20000);
    if (out.indexOf(v) >= 0) throw new Error(err);
    out.push(v);
  }
  return out.sort(function (a, b) { return a - b; });
}
function _px(n) { return n + "px"; }
function _pix(n) { return n + (n === 1 ? " pixel" : " pixels"); }

function needTruth(slotW, density) {
  var s = _int(slotW, _SLOT, 1, 4000), d = _dens(density);
  var t = s * d, need = Math.floor((t + 9) / 10);
  var text = "A " + s + "px wide slot on a " + _dec1(d) + "x screen needs " + (t === 10 ? "1 pixel" : _dec1(t) + " pixels") + " across";
  if (t % 10 === 0) return text + ".";
  return text + ", which rounds up to " + _pix(need) + ".";
}
function ladderTruth(slotW, topDensity) {
  var s = _int(slotW, _SLOT, 1, 4000);
  var n = _int(topDensity, "the top density must be a whole number from 1 to 5", 1, 5);
  var w = [], l = [];
  for (var k = 1; k <= n; k++) { w.push(String(s * k)); l.push(k + "x"); }
  function join(a) { return a.length === 1 ? a[0] : a.slice(0, -1).join(", ") + " and " + a[a.length - 1]; }
  if (n === 1) return "For a " + s + "px wide slot, the file needs to be " + (s === 1 ? "1 pixel" : w[0] + " pixels") + " across for 1x screens.";
  return "For a " + s + "px wide slot, the files need to be " + join(w) + " pixels across for " + join(l) + " screens.";
}
function pickTruth(slotW, density, widths) {
  var s = _int(slotW, _SLOT, 1, 4000), d = _dens(density), L = _list(widths);
  var need = Math.floor((s * d + 9) / 10), pick = -1;
  for (var i = 0; i < L.length; i++) if (L[i] >= need) { pick = L[i]; break; }
  var head = "The slot needs " + _pix(need) + " across. ";
  if (pick < 0) {
    var top = L[L.length - 1];
    return head + "No listed file is wide enough. The widest, " + _px(top) + ", is " + _pix(need - top) + " short.";
  }
  if (pick === need) return head + "The smallest listed file that is wide enough is " + _px(pick) + ", an exact fit.";
  return head + "The smallest listed file that is wide enough is " + _px(pick) + ", which is " + _pix(pick - need) + " more than needed.";
}
