/* =========================================================
   Colourway studio — recolours a real motif live.
   The motif's pixels are split into its two colour families
   (pinks / blues); each family is repainted in the chosen
   colour while keeping the original brush shading, then tiled
   as a half-drop repeat on the chosen ground.
   ========================================================= */
(function () {
  "use strict";
  var DPR = Math.min(2, window.devicePixelRatio || 1);
  var reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  function rgb(h) { h = h.replace("#", ""); return [parseInt(h.substr(0, 2), 16), parseInt(h.substr(2, 2), 16), parseInt(h.substr(4, 2), 16)] }
  function hue(r, g, b) {
    var mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn; if (!d) return [0, 0, mx / 255];
    var h = mx === r ? ((g - b) / d) % 6 : mx === g ? (b - r) / d + 2 : (r - g) / d + 4;
    return [(h * 60 + 360) % 360, d / mx, mx / 255];
  }

  function Studio(el) {
    var self = this;
    this.el = el; this.stage = el.querySelector(".st-stage"); this.nameEl = el.querySelector(".st-name");
    this.canvas = document.createElement("canvas"); this.canvas.setAttribute("aria-hidden", "true");
    this.stage.insertBefore(this.canvas, this.stage.firstChild);
    this.ctx = this.canvas.getContext("2d");
    this.ways = [].slice.call(el.querySelectorAll(".st-way"));
    this.ways.forEach(function (b) { b.addEventListener("click", function () { self.choose(b) }) });
    this.drift = 0; this.wipe = 1; this.prev = null; this.cur = null; this.visible = false;
    this.img = new Image(); this.img.decoding = "async";
    this.img.onload = function () { self.prepare(); self.choose(self.ways[0], true) };
    this.started = false;
  }
  Studio.prototype.start = function () { if (this.started) return; this.started = true; this.img.src = this.el.dataset.motif; this.resize() };
  Studio.prototype.resize = function () {
    var r = this.stage.getBoundingClientRect();
    this.W = Math.max(10, Math.round(r.width)); this.H = Math.max(10, Math.round(r.height));
    this.canvas.width = this.W * DPR; this.canvas.height = this.H * DPR;
    this.canvas.style.width = this.W + "px"; this.canvas.style.height = this.H + "px";
    if (this.curWay) { this.cur = this.tile(this.curWay); this.prev = null; this.wipe = 1 }
  };
  // split the motif into colour families once
  Studio.prototype.prepare = function () {
    var im = this.img, w = im.naturalWidth, h = im.naturalHeight, c = document.createElement("canvas");
    c.width = w; c.height = h; var x = c.getContext("2d"); x.drawImage(im, 0, 0);
    this.w = w; this.h = h;
    try { this.src = x.getImageData(0, 0, w, h) } catch (e) { this.src = null; return }  // pages opened as files can't read pixels
    var d = this.src.data, n = w * h, cls = new Uint8Array(n), lum = new Float32Array(n), sum = [0, 0, 0], cnt = [0, 0, 0];
    for (var i = 0; i < n; i++) {
      var r = d[i * 4], g = d[i * 4 + 1], b = d[i * 4 + 2], a = d[i * 4 + 3];
      var hs = hue(r, g, b), L = 0.299 * r + 0.587 * g + 0.114 * b; lum[i] = L;
      var k = 0;
      if (a > 8 && hs[1] > 0.28) {
        if (hs[0] >= 290 || hs[0] < 20) k = 1;          // pinks / magentas
        else if (hs[0] >= 160 && hs[0] < 260) k = 2;    // blues / teals
      }
      cls[i] = k; sum[k] += L; cnt[k]++;
    }
    this.cls = cls; this.lum = lum; this.mean = [0, sum[1] / Math.max(1, cnt[1]), sum[2] / Math.max(1, cnt[2])];
  };
  Studio.prototype.recolour = function (way) {
    if (!this.src || way.original) return this.img;
    var w = this.w, h = this.h, out = new ImageData(w, h), s = this.src.data, d = out.data;
    var A = rgb(way.a), B = rgb(way.b), cls = this.cls, lum = this.lum, mean = this.mean;
    for (var i = 0; i < w * h; i++) {
      var k = cls[i], j = i * 4;
      if (k === 0) { d[j] = s[j]; d[j + 1] = s[j + 1]; d[j + 2] = s[j + 2]; d[j + 3] = s[j + 3]; continue }
      var T = k === 1 ? A : B, f = Math.min(1.9, Math.max(0.25, lum[i] / mean[k]));
      d[j] = Math.min(255, T[0] * f); d[j + 1] = Math.min(255, T[1] * f); d[j + 2] = Math.min(255, T[2] * f); d[j + 3] = s[j + 3];
    }
    var c = document.createElement("canvas"); c.width = w; c.height = h; c.getContext("2d").putImageData(out, 0, 0);
    return c;
  };
  // one repeat tile: half-drop, alternate columns turned 180°, a slight tilt per row
  Studio.prototype.tile = function (way) {
    var m = this.recolour(way), mh = Math.max(90, Math.min(this.H * 0.3, 190)), mw = mh * this.w / this.h;
    var ux = mw * 1.14, uy = mh * 1.06, TW = Math.round(ux * 2), TH = Math.round(uy * 2);
    var t = document.createElement("canvas"); t.width = TW * DPR; t.height = TH * DPR;
    var x = t.getContext("2d"); x.scale(DPR, DPR);
    x.fillStyle = way.ground; x.fillRect(0, 0, TW, TH);
    for (var i = -1; i <= 2; i++) for (var j = -1; j <= 2; j++) {
      var px = i * ux + ux / 2, py = j * uy + uy / 2 + (i & 1 ? uy / 2 : 0);
      x.save(); x.translate(px, py); x.rotate((i & 1 ? Math.PI : 0) + (j & 1 ? 0.14 : -0.14));
      x.drawImage(m, -mw / 2, -mh / 2, mw, mh); x.restore();
    }
    return { canvas: t, tw: TW, th: TH, pattern: null };
  };
  Studio.prototype.choose = function (b, instant) {
    this.ways.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false") });
    var way = { name: b.dataset.name, ground: b.dataset.ground, a: b.dataset.a, b: b.dataset.b, original: b.hasAttribute("data-original") };
    if (!this.img.complete || !this.img.naturalWidth) { this.curWay = way; return }
    this.curWay = way;
    if (this.nameEl) this.nameEl.textContent = way.name;
    this.prev = instant ? null : this.cur; this.cur = this.tile(way); this.wipe = (instant || reduced) ? 1 : 0;
    this.el.style.setProperty("--ground", way.ground);
  };
  Studio.prototype.paintTile = function (t, ox) {
    var ctx = this.ctx;
    if (!t.pattern) t.pattern = ctx.createPattern(t.canvas, "repeat");
    var m = new DOMMatrix([1 / DPR, 0, 0, 1 / DPR, ox, ox * 0.35]);
    if (t.pattern.setTransform) t.pattern.setTransform(m);
    ctx.fillStyle = t.pattern; ctx.fillRect(0, 0, this.W, this.H);
  };
  Studio.prototype.frame = function () {
    if (!this.cur || !this.visible) return;
    var ctx = this.ctx; ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    if (!reduced) this.drift += 0.25;
    if (this.wipe < 1) this.wipe = Math.min(1, this.wipe + 0.035);
    var e = 1 - Math.pow(1 - this.wipe, 3);
    if (this.prev && e < 1) this.paintTile(this.prev, this.drift);
    ctx.save();
    if (e < 1) { ctx.beginPath(); ctx.arc(this.W * 0.5, this.H * 0.5, Math.hypot(this.W, this.H) * 0.55 * e, 0, 7); ctx.clip() }
    this.paintTile(this.cur, this.drift); ctx.restore();
    if (e >= 1) this.prev = null;
  };

  var list = [];
  window.Studios = {
    init: function () { list = [].slice.call(document.querySelectorAll(".studio")).map(function (el) { return new Studio(el) }) },
    frame: function (y, vh) {
      list.forEach(function (s) {
        var r = s.el.getBoundingClientRect();
        if (r.top < vh * 2.5 && r.bottom > -vh) s.start();
        s.visible = r.top < vh && r.bottom > 0;
        s.frame();
      });
    },
    resize: function () { list.forEach(function (s) { if (s.started) s.resize() }) }
  };
})();
