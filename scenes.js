/* =========================================================
   Process scenes — scroll-driven animations between pages.
   Each scene is a tall section with a pinned stage; its
   progress (0 → 1) is simply how far you have scrolled through
   it, so it plays forwards and backwards with the scroll and
   can never block or hide the portfolio pages.

     weave     Weave formation   (Roundup, Kargha)
     sketch    Sketch to garment (Fables of Mithila)
     moodboard Project moodboard (Unbuilt)
     motif     Motif to print    (Saandra, Seed Scriptures)
   ========================================================= */
(function () {
  "use strict";
  var DPR = Math.min(2, window.devicePixelRatio || 1);
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)) }
  function seg(p, a, b) { return clamp((p - a) / (b - a), 0, 1) }
  function eo(t) { return 1 - Math.pow(1 - t, 3) }              // ease out
  function eio(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2 }
  function lerp(a, b, t) { return a + (b - a) * t }
  function hash(x, y) { var s = Math.sin(x * 127.1 + y * 311.7) * 43758.5453; return s - Math.floor(s) }

  var cache = {};
  function img(src) {
    if (cache[src]) return cache[src];
    var im = new Image(); im.decoding = "async"; im.src = src; cache[src] = im;
    im.onload = function () { S.list.forEach(function (s) { s.dirty = true }) };
    return im;
  }
  function ok(im) { return im && im.complete && im.naturalWidth > 0 }

  var S = window.Scenes = { list: [], meta: null };

  /* ---------- shared scene plumbing ---------- */
  function Scene(el) {
    this.el = el; this.type = el.dataset.scene;
    this.cfg = JSON.parse(el.dataset.cfg || "{}");
    this.title = el.dataset.title || "";
    this.stage = el.querySelector(".sc-stage");
    this.steps = [].slice.call(el.querySelectorAll(".sc-steps li"));
    this.bar = el.querySelector(".sc-bar i");
    this.p = -1; this.dirty = true; this.loaded = false; this.top = 0; this.h = 0;
    if (this.type !== "moodboard") {
      this.canvas = document.createElement("canvas");
      this.canvas.setAttribute("aria-hidden", "true");
      this.stage.appendChild(this.canvas);
      this.ctx = this.canvas.getContext("2d");
    }
  }
  Scene.prototype.load = function () {
    if (this.loaded) return; this.loaded = true;
    var self = this, c = this.cfg;
    ["photo", "motif", "sketch", "print", "figure", "lineup", "sample", "note"].forEach(function (k) { if (c[k]) self[k] = img(c[k]) });
    if (this.type === "moodboard") this.buildBoard();
    this.resize();
  };
  Scene.prototype.resize = function () {
    var r = this.stage.getBoundingClientRect();
    this.W = Math.max(10, Math.round(r.width)); this.H = Math.max(10, Math.round(r.height));
    if (this.canvas) {
      this.canvas.width = this.W * DPR; this.canvas.height = this.H * DPR;
      this.canvas.style.width = this.W + "px"; this.canvas.style.height = this.H + "px";
    }
    if (this.type === "weave") this.setupWeave();
    this.dirty = true;
  };
  Scene.prototype.render = function (p) {
    if (!this.dirty && Math.abs(p - this.p) < 0.0004) return;
    this.p = p; this.dirty = false;
    for (var k = 0; k < this.steps.length; k++) {
      var li = this.steps[k], a = +li.dataset.a, b = +li.dataset.b;
      li.classList.toggle("on", p >= a && p < b || (k === this.steps.length - 1 && p >= a));
      li.classList.toggle("done", p >= b && k < this.steps.length - 1);
    }
    if (this.bar) this.bar.style.transform = "scaleX(" + p.toFixed(4) + ")";
    if (this.type === "weave") this.drawWeave(p);
    else if (this.type === "motif") this.drawMotif(p);
    else if (this.type === "sketch") this.drawSketch(p);
    else if (this.type === "moodboard") this.drawBoard(p);
    else if (this.type === "tiedye") this.drawTieDye(p);
  };

  /* =========================================================
     WEAVE FORMATION — warp drops in, weft travels over/under,
     the pattern appears, then the cloth turns into the product
  ========================================================= */
  Scene.prototype.setupWeave = function () {
    var c = this.cfg, W = this.W, H = this.H;
    var rows = W < 520 ? 22 : 28;
    var cols = clamp(Math.round(rows * (W * 0.94) / (H * 0.84)), 16, 60);
    var s = Math.floor(Math.min(W * 0.94 / cols, H * 0.84 / rows));
    this.wv = { cols: cols, rows: rows, s: s, tw: s * 0.8, lw: cols * s, lh: rows * s };
    this.wv.x0 = Math.round((W - this.wv.lw) / 2); this.wv.y0 = Math.round((H - this.wv.lh) / 2);
  };
  function warpColor(c, k) { var w = c.warp; return w[Math.floor(k / c.band) % w.length] }
  function weftColor(c, k) { var w = c.weft; return w[Math.floor(k / c.band) % w.length] }
  function warpOver(c, x, y) {
    if (c.pattern === "twill") return ((x + y) % 4) < 2;            // 2/2 twill: diagonal ribs
    // kargha: plain-weave ground with weft-float diamonds every 12 threads
    var dx = Math.abs((x % 12) - 5.5), dy = Math.abs((y % 12) - 5.5), d = dx + dy;
    if ((d > 2.6 && d < 4.4) || d < 1.1) return false;
    return (x + y) % 2 === 0;
  }
  function shade(ctx, x, y, w, h, vertical) {
    var g = vertical ? ctx.createLinearGradient(x, 0, x + w, 0) : ctx.createLinearGradient(0, y, 0, y + h);
    g.addColorStop(0, "rgba(0,0,0,.28)"); g.addColorStop(.35, "rgba(255,255,255,.18)");
    g.addColorStop(.6, "rgba(255,255,255,.05)"); g.addColorStop(1, "rgba(0,0,0,.32)");
    ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
  }
  Scene.prototype.drawWeave = function (p) {
    var ctx = this.ctx, c = this.cfg, v = this.wv; if (!v) return;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    ctx.clearRect(0, 0, this.W, this.H);
    var cols = v.cols, rows = v.rows, s = v.s, tw = v.tw, off = (s - tw) / 2, x0 = v.x0, y0 = v.y0;

    // loom beams
    var beam = eo(seg(p, 0, 0.06));
    if (beam > 0) {
      ctx.globalAlpha = beam; ctx.fillStyle = "#7a5a3c";
      ctx.fillRect(x0 - 14, y0 - 22, v.lw + 28, 10); ctx.fillRect(x0 - 14, y0 + v.lh + 12, v.lw + 28, 10);
      ctx.globalAlpha = 1;
    }
    var done = seg(p, 0.7, 0.95);
    if (done < 1) {
      ctx.save(); ctx.beginPath(); ctx.rect(x0 - 2, y0 - 10, v.lw + 4, v.lh + 20); ctx.clip();
      // 1. warp threads drop onto the loom, one by one
      var warpY = [];
      for (var x = 0; x < cols; x++) {
        var a = 0.015 + x / cols * 0.17, t = eo(seg(p, a, a + 0.07));
        warpY[x] = t;
        if (t <= 0) continue;
        var px = x0 + x * s + off, py = y0 - (1 - t) * (v.lh + 40);
        ctx.fillStyle = warpColor(c, x); ctx.fillRect(px, py, tw, v.lh);
        shade(ctx, px, py, tw, v.lh, true);
      }
      // 2. weft threads shoot across, going over and under
      for (var y = 0; y < rows; y++) {
        var b = 0.2 + y / rows * 0.44, u = seg(p, b, b + 0.05);
        if (u <= 0) continue;
        var ext = u * v.lw, ltr = y % 2 === 0;
        var xa = ltr ? x0 : x0 + v.lw - ext, xb = ltr ? x0 + ext : x0 + v.lw;
        var py2 = y0 + y * s + off;
        ctx.fillStyle = weftColor(c, y); ctx.fillRect(xa, py2, xb - xa, tw);
        shade(ctx, xa, py2, xb - xa, tw, false);
        for (var x2 = 0; x2 < cols; x2++) {
          var cx = x0 + x2 * s;
          if (cx + s < xa || cx > xb || warpY[x2] < 1) continue;
          if (warpOver(c, x2, y)) {            // warp lifts over the weft here
            ctx.fillStyle = warpColor(c, x2); ctx.fillRect(cx + off, y0 + y * s, tw, s);
            shade(ctx, cx + off, y0 + y * s, tw, s, true);
            ctx.fillStyle = "rgba(0,0,0,.22)"; ctx.fillRect(cx + off, y0 + y * s, tw, 1.2);
          }
        }
        if (u < 1) {                            // the shuttle
          var sx = ltr ? xb : xa;
          ctx.fillStyle = "#c9a36b"; roundRect(ctx, sx - 18, py2 - 5, 36, tw + 10, 8); ctx.fill();
          ctx.fillStyle = "rgba(0,0,0,.25)"; ctx.fillRect(sx - 10, py2 + tw / 2 - 1, 20, 2);
        }
      }
      ctx.restore();
    }
    // 3. the woven surface turns into the finished product, cell by cell
    if (done > 0 && ok(this.photo)) {
      var im = this.photo, fit = cover(im.naturalWidth, im.naturalHeight, v.lw, v.lh);
      if (done >= 1) {
        ctx.drawImage(im, fit.sx, fit.sy, fit.sw, fit.sh, x0, y0, v.lw, v.lh);
      } else {
        for (var yy = 0; yy < rows; yy++) for (var xx = 0; xx < cols; xx++) {
          var th = ((xx / cols) + (yy / rows)) / 2 * 0.8 + hash(xx, yy) * 0.12;
          var al = seg(done, th, th + 0.12); if (al <= 0) continue;
          ctx.globalAlpha = al;
          var k = fit.sw / v.lw;
          ctx.drawImage(im, fit.sx + xx * s * k, fit.sy + yy * s * k, s * k, s * k, x0 + xx * s, y0 + yy * s, s + .5, s + .5);
        }
        ctx.globalAlpha = 1;
      }
    }
  };

  /* =========================================================
     MOTIF TO PRINT — one hand-drawn motif, duplicated and
     rotated into a half-drop repeat, then the finished print
  ========================================================= */
  Scene.prototype.drawMotif = function (p) {
    var ctx = this.ctx, c = this.cfg, W = this.W, H = this.H, m = this.motif;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0); ctx.clearRect(0, 0, W, H);
    if (!ok(m)) return;
    var cx = W / 2, cy = H / 2, R = 16;
    var ar = m.naturalWidth / m.naturalHeight;
    var mh0 = Math.min(H * 0.5, W * 0.42 / ar), mw0 = mh0 * ar;          // the single motif, large
    var zoom = lerp(1, c.zoomTo || 0.42, eio(seg(p, 0.3, 0.74)));       // the repeat zooms out
    var mh = mh0 * zoom, mw = mw0 * zoom;
    var uX = mw * (c.gapX || 1.25), uY = mh * (c.gapY || 1.12);          // lattice step

    ctx.save(); roundRect(ctx, 0, 0, W, H, R); ctx.clip();
    // ground colour floods in behind the repeat
    var g = seg(p, 0.44, 0.56);
    if (g > 0) {
      ctx.fillStyle = c.ground; ctx.globalAlpha = g;
      ctx.beginPath(); ctx.arc(cx, cy, Math.hypot(W, H) * eo(g) / 1.6, 0, 7); ctx.fill(); ctx.globalAlpha = 1;
    }
    // lattice: half-drop columns
    var cells = [];
    var colsN = Math.ceil(W / 2 / (mw0 * (c.zoomTo || .42) * (c.gapX || 1.25))) + 2;
    var rowsN = Math.ceil(H / 2 / (mh0 * (c.zoomTo || .42) * (c.gapY || 1.12))) + 2;
    for (var i = -colsN; i <= colsN; i++) for (var j = -rowsN; j <= rowsN; j++) {
      if (i === 0 && j === 0) continue;
      cells.push({ i: i, j: j, d: Math.hypot(i, j + (i & 1) * 0.5) });
    }
    cells.sort(function (a, b) { return a.d - b.d });
    var n = cells.length;
    // copies fly out from the original into place, spinning into their rotation
    for (var k = 0; k < n; k++) {
      var e = cells[k], st = 0.2 + (k / n) * 0.36, t = eo(seg(p, st, st + 0.09));
      if (t <= 0) continue;
      var tx = cx + e.i * uX, ty = cy + (e.j + ((e.i & 1) ? 0.5 : 0)) * uY;
      var rot = c.rotate === "alt" ? ((e.i & 1) ? Math.PI : 0) + ((e.j & 1) ? 0.14 : -0.14) : 0;
      var x = lerp(cx, tx, t), y = lerp(cy, ty, t), sc = lerp(0.3, 1, t), r = lerp(rot + Math.PI * 1.5, rot, t);
      ctx.globalAlpha = Math.min(1, t * 1.6);
      drawRot(ctx, m, x, y, mw * sc, mh * sc, r);
    }
    ctx.globalAlpha = 1;
    // the original motif — drawn by hand first (a sweeping pen), from a sketch if there is one
    var draw = seg(p, 0.02, c.sketch ? 0.12 : 0.17), colourIn = c.sketch ? seg(p, 0.12, 0.2) : 1;
    if (draw > 0) {
      ctx.save(); ctx.beginPath(); ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, Math.max(mw, mh), -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * draw); ctx.closePath(); ctx.clip();
      if (c.sketch && ok(this.sketch) && colourIn < 1) {
        var sk = this.sketch, sa = sk.naturalWidth / sk.naturalHeight, sh = mh * 0.98, sw = sh * sa;
        ctx.globalAlpha = 1 - colourIn; ctx.drawImage(sk, cx - sw / 2, cy - sh / 2, sw, sh); ctx.globalAlpha = 1;
      }
      ctx.globalAlpha = colourIn; ctx.drawImage(m, cx - mw / 2, cy - mh / 2, mw, mh); ctx.globalAlpha = 1;
      ctx.restore();
      if (draw < 1) {                           // pen tip
        var a = -Math.PI / 2 + Math.PI * 2 * draw, pr = Math.max(mw, mh) * 0.48;
        ctx.fillStyle = "#1f2b2a"; ctx.beginPath(); ctx.arc(cx + Math.cos(a) * pr, cy + Math.sin(a) * pr, 4, 0, 7); ctx.fill();
      }
    }
    // the repeat unit, outlined
    var ru = seg(p, 0.56, 0.62) * (1 - seg(p, 0.76, 0.8));
    if (ru > 0) {
      ctx.globalAlpha = ru; ctx.setLineDash([7, 6]); ctx.lineWidth = 1.5; ctx.strokeStyle = c.unitInk || "#163b3c";
      var bw = uX * 2, bh = uY * 2;
      ctx.strokeRect(cx - uX / 2, cy - uY / 2, bw, bh); ctx.setLineDash([]);
      ctx.font = "500 12px Jost, system-ui, sans-serif"; ctx.fillStyle = c.unitInk || "#163b3c";
      var label = c.unit || "Repeat unit", lw = ctx.measureText(label).width + 16;
      ctx.fillStyle = c.unitBg || "rgba(242,235,220,.92)"; roundRect(ctx, cx - uX / 2, cy - uY / 2 - 30, lw, 22, 11); ctx.fill();
      ctx.fillStyle = c.unitInk || "#163b3c"; ctx.fillText(label, cx - uX / 2 + 8, cy - uY / 2 - 15);
      ctx.globalAlpha = 1;
    }
    // the finished print arrives as a swatch card over the repeat
    var fin = seg(p, 0.78, 0.92);
    if (fin > 0 && ok(this.print)) {
      var pi = this.print, e2 = eo(fin);
      ctx.fillStyle = "rgba(246,241,230," + (0.82 * fin) + ")"; ctx.fillRect(0, 0, W, H);
      var ar2 = pi.naturalWidth / pi.naturalHeight, cw = Math.min(W * 0.7, H * 0.74 * ar2), chh = cw / ar2, pad = 10;
      var x1 = cx - cw / 2, y1 = cy - chh / 2 - 12 + (1 - e2) * 60;
      ctx.globalAlpha = Math.min(1, fin * 1.4);
      ctx.save(); ctx.shadowColor = "rgba(31,43,42,.35)"; ctx.shadowBlur = 40; ctx.shadowOffsetY = 22;
      ctx.fillStyle = "#fbf8f1"; roundRect(ctx, x1 - pad, y1 - pad, cw + pad * 2, chh + pad * 2 + 34, 6); ctx.fill(); ctx.restore();
      ctx.drawImage(pi, x1, y1, cw, chh);
      ctx.font = "500 12px Jost, system-ui, sans-serif"; ctx.fillStyle = "#163b3c";
      ctx.fillText((c.cardLabel || "Final print") + "  ·  " + (c.unit || ""), x1, y1 + chh + 25);
      ctx.globalAlpha = 1;
    }
    ctx.restore();
  };
  function drawRot(ctx, im, x, y, w, h, r) {
    ctx.save(); ctx.translate(x, y); if (r) ctx.rotate(r); ctx.drawImage(im, -w / 2, -h / 2, w, h); ctx.restore();
  }

  /* =========================================================
     SKETCH TO GARMENT — lines draw on, colour and print fill
     the silhouette, then the whole coordinate set appears
  ========================================================= */
  Scene.prototype.drawSketch = function (p) {
    var ctx = this.ctx, c = this.cfg, W = this.W, H = this.H, M = S.meta;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0); ctx.clearRect(0, 0, W, H);
    var F = M.fablesFigure, L = M.fablesLineup.box, lines = M.fablesLines;
    if (!this.len) {                             // precompute line lengths (in figure pixels)
      var tot = 0, lens = [];
      lines.forEach(function (l) { var d = 0; for (var i = 1; i < l.length; i++) d += Math.hypot((l[i][0] - l[i - 1][0]) * F.w, (l[i][1] - l[i - 1][1]) * F.h); lens.push(d); tot += d });
      this.len = { tot: tot, each: lens };
    }
    var fb = F.box, figW = fb[2] - fb[0], figH = fb[3] - fb[1];
    var fh0 = H * 0.9, fw0 = fh0 * figW / figH, fx0 = (W - fw0) / 2, fy0 = (H - fh0) / 2;
    // final framing: the whole line-up centred in the stage
    var Lw = L[2] - L[0], Lh = L[3] - L[1], zf = Math.min(W * 0.96 / Lw, H * 0.94 / Lh);
    var lfx = (W - Lw * zf) / 2 + (fb[0] - L[0]) * zf, lfy = (H - Lh * zf) / 2 + (fb[1] - L[1]) * zf;
    var t4 = eio(seg(p, 0.8, 0.95));
    var k0 = fw0 / figW, k = lerp(k0, zf, t4);
    var fx = lerp(fx0, lfx, t4), fy = lerp(fy0, lfy, t4), fw = figW * k, fh = figH * k;

    // 4. the line-up (with the other two coordinates) fades in around the garment
    if (t4 > 0 && ok(this.lineup)) {
      ctx.globalAlpha = seg(p, 0.8, 0.9);
      var lx = fx - (fb[0] - L[0]) * k, ly = fy - (fb[1] - L[1]) * k;
      ctx.save(); roundRect(ctx, lx, ly, Lw * k, Lh * k, 8); ctx.clip();
      ctx.drawImage(this.lineup, lx, ly, Lw * k, Lh * k); ctx.restore();
      ctx.globalAlpha = 1;
    }
    // 2/3. colour & print fill the silhouette from the shoulders down
    var fill = seg(p, 0.34, 0.64);
    if (fill > 0 && ok(this.figure)) {
      var lvl = fy + fh * (fill * 1.08) - fh * 0.04;
      ctx.save();
      if (fill < 1) {
        ctx.beginPath(); ctx.moveTo(fx - 20, fy - 20); ctx.lineTo(fx + fw + 20, fy - 20); ctx.lineTo(fx + fw + 20, lvl);
        for (var x = fx + fw + 20; x >= fx - 20; x -= 8) ctx.lineTo(x, lvl + Math.sin(x * 0.045 + p * 30) * 7);
        ctx.closePath(); ctx.clip();
      }
      var lift = seg(p, 0.62, 0.8) * (1 - t4);
      if (lift > 0) { ctx.shadowColor = "rgba(0,0,0," + (0.35 * lift) + ")"; ctx.shadowBlur = 30 * lift; ctx.shadowOffsetY = 16 * lift }
      ctx.globalAlpha = 1 - seg(p, 0.92, 0.98) * (ok(this.lineup) ? 1 : 0);
      ctx.drawImage(this.figure, fx, fy, fw, fh);
      ctx.restore(); ctx.globalAlpha = 1;
    }
    // 1. sketch lines draw on, top to bottom
    var drawn = seg(p, 0.02, 0.36) * this.len.tot, lineA = 1 - seg(p, 0.6, 0.76);
    if (drawn > 0 && lineA > 0) {
      ctx.strokeStyle = "rgba(31,43,42," + (0.9 * lineA) + ")"; ctx.lineWidth = 1.4; ctx.lineJoin = "round"; ctx.lineCap = "round";
      var acc = 0, tip = null;
      for (var i = 0; i < lines.length && acc < drawn; i++) {
        var l = lines[i], need = drawn - acc, segLen = this.len.each[i];
        ctx.beginPath(); ctx.moveTo(fx + l[0][0] * fw, fy + l[0][1] * fh);
        var used = 0;
        for (var q = 1; q < l.length; q++) {
          var ax = fx + l[q - 1][0] * fw, ay = fy + l[q - 1][1] * fh, bx = fx + l[q][0] * fw, by = fy + l[q][1] * fh;
          var d = Math.hypot((l[q][0] - l[q - 1][0]) * F.w, (l[q][1] - l[q - 1][1]) * F.h);
          if (used + d > need) { var f = (need - used) / d; bx = lerp(ax, bx, f); by = lerp(ay, by, f); ctx.lineTo(bx, by); tip = [bx, by]; break }
          ctx.lineTo(bx, by); used += d;
        }
        ctx.stroke(); acc += segLen;
      }
      if (tip && drawn < this.len.tot) { ctx.fillStyle = "#1f2b2a"; ctx.beginPath(); ctx.arc(tip[0], tip[1], 3.2, 0, 7); ctx.fill() }
    }
  };

  /* =========================================================
     MOODBOARD — images, swatches and notes slide into place,
     each at its own speed; colours reveal; the concept note last
  ========================================================= */
  Scene.prototype.buildBoard = function () {
    var self = this, c = this.cfg;
    this.pieces = [].slice.call(this.stage.querySelectorAll(".mb-piece")).map(function (el) {
      var im = el.querySelector("img"); if (im && im.dataset.src) { im.src = im.dataset.src; im.removeAttribute("data-src") }
      return { el: el, a: +el.dataset.a, b: +el.dataset.b, dx: +el.dataset.dx, dy: +el.dataset.dy, r: +el.dataset.r };
    });
    this.chips = [].slice.call(this.stage.querySelectorAll(".mb-chip"));
    this.words = [].slice.call(this.stage.querySelectorAll(".mb-word"));
    var note = this.stage.querySelector(".mb-note-text");
    if (note && !note.dataset.split) {
      note.dataset.split = 1;
      note.innerHTML = note.textContent.trim().split(/\s+/).map(function (w) { return '<span class="w">' + w + "</span>" }).join(" ");
    }
    this.noteWords = note ? [].slice.call(note.querySelectorAll(".w")) : [];
    this.noteHead = this.stage.querySelector(".mb-note h3");
  };
  Scene.prototype.drawBoard = function (p) {
    if (!this.pieces) return;
    this.pieces.forEach(function (o) {
      var t = eo(seg(p, o.a, o.b));
      o.el.style.transform = "translate(" + ((1 - t) * o.dx).toFixed(2) + "%," + ((1 - t) * o.dy).toFixed(2) + "%) rotate(" + (o.r * (0.4 + 0.6 * t) + (1 - t) * o.r * 3).toFixed(2) + "deg) scale(" + (0.86 + 0.14 * t).toFixed(3) + ")";
      o.el.style.opacity = Math.min(1, t * 2.2).toFixed(3);
    });
    var n = this.chips.length;
    this.chips.forEach(function (ch, i) {
      var a = 0.36 + i * 0.03, t = eo(seg(p, a, a + 0.08));
      ch.style.setProperty("--t", t.toFixed(3));
    });
    this.words.forEach(function (w, i) {
      var a = 0.6 + i * 0.03, t = eo(seg(p, a, a + 0.06));
      w.style.opacity = t.toFixed(3); w.style.transform = "translateY(" + ((1 - t) * 14).toFixed(1) + "px)";
    });
    if (this.noteHead) { var h = eo(seg(p, 0.7, 0.76)); this.noteHead.style.opacity = h; this.noteHead.style.transform = "translateY(" + ((1 - h) * 12) + "px)" }
    var W = this.noteWords, m = W.length;
    for (var i = 0; i < m; i++) { var a = 0.72 + i / m * 0.2; W[i].style.opacity = seg(p, a, a + 0.035).toFixed(3) }
  };

  /* =========================================================
     TIE & DYE (Baandh) — fan-fold, square folds, bind, dye,
     unfold to reveal the real sample, then the cushions
  ========================================================= */
  Scene.prototype.drawTieDye = function (p) {
    var ctx = this.ctx, c = this.cfg, W = this.W, H = this.H;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0); ctx.clearRect(0, 0, W, H);
    var S0 = Math.min(W * 0.5, H * 0.66), cx = W / 2, cy = H / 2 + 6, N = 8, M = 8;
    var dye = c.dye || "#c2185b", fab = [244, 240, 232], dc = hexRgb(dye);
    var fa = eio(seg(p, 0.03, 0.2)) * (1 - eio(seg(p, 0.76, 0.86)));      // fan-fold (columns)
    var fb = eio(seg(p, 0.2, 0.34)) * (1 - eio(seg(p, 0.67, 0.76)));      // square folds (rows)
    var ta = fa * 1.42, tb = fb * 1.42;
    var colW = S0 / N * Math.cos(ta) + fa * 2.2, rowH = S0 / M * Math.cos(tb) + fb * 2.2;
    var tw = colW * N, th = rowH * M, x0 = cx - tw / 2, y0 = cy - th / 2;
    var dyed = seg(p, 0.5, 0.62);                                           // how much dye has soaked in
    var reveal = seg(p, 0.64, 0.7);                                         // tinted bundle -> real sample
    var sm = this.sample, hasS = ok(sm);
    var fin = seg(p, 0.86, 0.96);

    if (fin < 1) {
      ctx.save(); ctx.globalAlpha = 1 - fin * 0.85;
      for (var i = 0; i < N; i++) for (var j = 0; j < M; j++) {
        var x = x0 + i * colW, y = y0 + j * rowH;
        if (reveal < 1) {
          var k = dyed * (0.75 + 0.25 * hash(i, j));
          ctx.fillStyle = "rgb(" + Math.round(lerp(fab[0], dc[0], k)) + "," + Math.round(lerp(fab[1], dc[1], k)) + "," + Math.round(lerp(fab[2], dc[2], k)) + ")";
          ctx.fillRect(x, y, colW + .6, rowH + .6);
        }
        if (reveal > 0 && hasS) {
          ctx.globalAlpha = (1 - fin * 0.85) * reveal;
          var sw = sm.naturalWidth / N, sh = sm.naturalHeight / M;
          ctx.drawImage(sm, i * sw, j * sh, sw, sh, x, y, colW + .6, rowH + .6);
          ctx.globalAlpha = 1 - fin * 0.85;
        }
        // pleat shading: alternate faces catch the light
        var sa = (i % 2 ? 0.34 : 0.06) * Math.sin(ta) + (j % 2 ? 0.3 : 0.04) * Math.sin(tb);
        if (sa > 0.005) { ctx.fillStyle = "rgba(40,10,25," + sa.toFixed(3) + ")"; ctx.fillRect(x, y, colW + .6, rowH + .6) }
      }
      // fabric weave texture while it is still plain
      if (dyed < 1 && reveal === 0) {
        ctx.globalAlpha = 0.06; ctx.fillStyle = "#000";
        for (var yy = y0; yy < y0 + th; yy += 3) ctx.fillRect(x0, yy, tw, 1);
        ctx.globalAlpha = 1;
      }
      ctx.restore();
    }
    // binding threads wrap the bundle
    var bind = seg(p, 0.34, 0.47) * (1 - seg(p, 0.64, 0.68));
    if (bind > 0) {
      ctx.save(); ctx.lineCap = "round";
      var wraps = [[-0.5, -0.32, 0.5, -0.32], [-0.5, 0.0, 0.5, 0.0], [-0.5, 0.32, 0.5, 0.32], [-0.5, -0.5, 0.5, 0.5], [-0.5, 0.5, 0.5, -0.5]];
      var shown = bind * wraps.length;
      for (var w = 0; w < wraps.length && w < shown; w++) {
        var f = Math.min(1, shown - w), q = wraps[w], pad = 6;
        var ax = cx + q[0] * (tw + pad * 2), ay = cy + q[1] * (th + pad * 2), bx = cx + q[2] * (tw + pad * 2), by = cy + q[3] * (th + pad * 2);
        bx = lerp(ax, bx, f); by = lerp(ay, by, f);
        ctx.strokeStyle = "rgba(0,0,0,.35)"; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(ax, ay + 1.5); ctx.lineTo(bx, by + 1.5); ctx.stroke();
        ctx.strokeStyle = "#f6efe0"; ctx.lineWidth = 2.6; ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(bx, by); ctx.stroke();
      }
      ctx.restore();
    }
    // the dye bath rises, holds, and drains away
    var up = eo(seg(p, 0.47, 0.54)), down = eio(seg(p, 0.6, 0.66)), lvl = up * (1 - down);
    if (lvl > 0) {
      var top = lerp(H + 10, y0 - th * 0.35 - 20, lvl);
      ctx.save(); roundRect(ctx, 0, 0, W, H, 10); ctx.clip();
      ctx.fillStyle = dye; ctx.globalAlpha = 0.82;
      ctx.beginPath(); ctx.moveTo(0, H);
      for (var xw = 0; xw <= W; xw += 10) ctx.lineTo(xw, top + Math.sin(xw * 0.03 + p * 60) * 6);
      ctx.lineTo(W, H); ctx.closePath(); ctx.fill();
      ctx.globalAlpha = 0.25; ctx.fillStyle = "#fff";
      for (var xb = 0; xb <= W; xb += 10) ctx.fillRect(xb, top + Math.sin(xb * 0.03 + p * 60) * 6 - 1, 6, 1.5);
      ctx.restore();
    }
    // her own process note, pinned beside the cloth while folding
    var nt = seg(p, 0.05, 0.12) * (1 - seg(p, 0.34, 0.4));
    if (nt > 0 && ok(this.note)) {
      var nw = Math.min(220, W * 0.24), nh = nw * this.note.naturalHeight / this.note.naturalWidth;
      var nx = W - nw - 18, ny = 18 + (1 - eo(nt)) * -20;
      ctx.save(); ctx.globalAlpha = nt; ctx.translate(nx + nw / 2, ny + nh / 2); ctx.rotate(0.03);
      ctx.shadowColor = "rgba(0,0,0,.4)"; ctx.shadowBlur = 24; ctx.shadowOffsetY = 10;
      ctx.drawImage(this.note, -nw / 2, -nh / 2, nw, nh); ctx.restore();
      ctx.save(); ctx.globalAlpha = nt * 0.8; ctx.fillStyle = "#1f2b2a"; ctx.font = "500 11px Jost, system-ui, sans-serif";
      ctx.fillText("Aastha's process note", nx, ny + nh + 18); ctx.restore();
    }
    // the cushion collection, with the sample pinned in the corner
    if (fin > 0 && ok(this.photo)) {
      var im = this.photo, ft = cover(im.naturalWidth, im.naturalHeight, W, H);
      ctx.save(); roundRect(ctx, 0, 0, W, H, 10); ctx.clip(); ctx.globalAlpha = fin;
      ctx.drawImage(im, ft.sx, ft.sy, ft.sw, ft.sh, 0, 0, W, H); ctx.restore();
      if (hasS) {
        var cs = Math.min(W, H) * 0.24, e3 = eo(fin), sxp = lerp(x0, 22, e3), syp = lerp(y0, H - cs - 22, e3), ss = lerp(tw, cs, e3);
        ctx.save(); ctx.shadowColor = "rgba(0,0,0,.45)"; ctx.shadowBlur = 26; ctx.shadowOffsetY = 12;
        ctx.fillStyle = "#fbf8f1"; ctx.fillRect(sxp - 7, syp - 7, ss + 14, ss + 14); ctx.restore();
        ctx.drawImage(sm, sxp, syp, ss, ss);
      }
    }
  };
  function hexRgb(h) { h = h.replace("#", ""); return [parseInt(h.substr(0, 2), 16), parseInt(h.substr(2, 2), 16), parseInt(h.substr(4, 2), 16)] }

  /* ---------- helpers ---------- */
  function cover(iw, ih, w, h) {
    var s = Math.max(w / iw, h / ih), sw = w / s, sh = h / s;
    return { sx: (iw - sw) / 2, sy: (ih - sh) / 2, sw: sw, sh: sh };
  }
  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }

  /* ---------- public API used by the page script ---------- */
  S.init = function (meta) {
    S.meta = meta;
    S.list = [].slice.call(document.querySelectorAll(".scene")).map(function (el) { return new Scene(el) });
    S.measure();
  };
  S.measure = function () {
    var y = window.pageYOffset;
    S.list.forEach(function (s) {
      var r = s.el.getBoundingClientRect(); s.top = r.top + y; s.h = s.el.offsetHeight;
      if (s.loaded) s.resize();
    });
  };
  S.progress = function (s, y, vh) { return clamp((y - s.top) / Math.max(1, s.h - vh), 0, 1) };
  S.frame = function (y, vh, still) {
    for (var i = 0; i < S.list.length; i++) {
      var s = S.list[i];
      if (s.top - vh * 2.5 < y + vh && s.top + s.h + vh > y) s.load();       // fetch assets a little early
      if (s.top < y + vh && s.top + s.h > y) s.render(still ? 1 : S.progress(s, y, vh));
    }
  };
  S.active = function (y, vh) {                     // the scene filling the screen, if any
    for (var i = 0; i < S.list.length; i++) { var s = S.list[i]; if (y + vh * 0.5 > s.top && y + vh * 0.5 < s.top + s.h) return s }
    return null;
  };
  S.between = function (y1, y2) {                    // scenes a glide from y1 to y2 passes through
    var a = Math.min(y1, y2), b = Math.max(y1, y2);
    return S.list.filter(function (s) { return s.top >= a - 2 && s.top + s.h <= b + window.innerHeight + 2 }).length;
  };
})();
