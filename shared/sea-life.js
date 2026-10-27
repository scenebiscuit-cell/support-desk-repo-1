/* ---------- sea life for the masthead: an occasional wireframe fish jump or splash ----------
   build_demo.py inlines this file into both pages; edit it here. One event at a time, every 7-13 s,
   on the right side of the water (the headline side is masked), in the same gold ink as the waves.
   The masthead animation already stops for reduced motion, the pause button, and hidden tabs. */
function makeSeaLife() {
  const events = [], ripples = [];
  let nextAt = 3 + Math.random() * 2;              // first one comes soon, so visitors notice it once
  // Surface height of row i at screen x, read off the mesh the waves just drew.
  function surfaceAt(row, x) {
    let best = row[0];
    for (const p of row) if (Math.abs(p[0] - x) < Math.abs(best[0] - x)) best = p;
    return best[1];
  }
  function burst(foam, x, y, s, n, power) {
    for (let k = 0; k < n; k++) foam.push({ x: x + (Math.random() - .5) * 6 * s, y,
      vx: (Math.random() - .5) * 1.8 * s, vy: -(power * .6 + Math.random() * power) * s, a: .5, r: .6 + Math.random() * .8 });
    ripples.push({ x, y, s, born: performance.now() });
  }
  function drawFish(ctx, x, y, ang, dir, s, ink, alpha) {
    const L = 30 * s, h = 10 * s;
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(1, dir);
    ctx.strokeStyle = `rgba(${ink},${alpha})`; ctx.lineWidth = .9;
    ctx.beginPath();                                   // body outline
    ctx.moveTo(L / 2, 0); ctx.quadraticCurveTo(0, -h, -L / 2, 0); ctx.quadraticCurveTo(0, h, L / 2, 0);
    ctx.moveTo(-L / 2, 0); ctx.lineTo(-L * .8, -h * .7); ctx.lineTo(-L * .72, 0); ctx.lineTo(-L * .8, h * .7); ctx.closePath();   // tail
    ctx.moveTo(L / 2, 0); ctx.lineTo(-L / 2, 0);       // spine
    for (const fx of [-.25, 0, .22]) {                 // wireframe ribs
      const xx = fx * L, hh = (h / 2) * (1 - (2 * xx / L) ** 2);
      ctx.moveTo(xx, -hh); ctx.lineTo(xx, hh);
    }
    ctx.moveTo(-L * .05, -h * .45); ctx.lineTo(-L * .2, -h * .85); ctx.lineTo(L * .12, -h * .4);   // dorsal fin
    ctx.stroke();
    ctx.beginPath(); ctx.arc(L * .3, -h * .12, .9 * s, 0, 6.283); ctx.stroke();                   // eye
    ctx.restore();
  }
  return {
    step(ctx, pts, t, ink, foam, W) {
      const rows = pts.length;
      if (t >= nextAt) {
        const i = 7 + Math.floor(Math.random() * 8), z = i / (rows - 1);
        events.push({ kind: Math.random() < .72 ? "fish" : "splash", start: t, i, s: .55 + .8 * z,
          x0: W * (.6 + Math.random() * .3), dir: Math.random() < .5 ? -1 : 1, dur: 1.3 + Math.random() * .5, phase: -1 });
        nextAt = t + 7 + Math.random() * 6;
      }
      for (let k = events.length - 1; k >= 0; k--) {
        const ev = events[k], row = pts[ev.i], age = t - ev.start;
        if (ev.kind === "splash") {
          if (ev.phase < 0) { burst(foam, ev.x0, surfaceAt(row, ev.x0), ev.s, 14, 1.9); ev.phase = 1; }
          if (age > 2) events.splice(k, 1);
          continue;
        }
        const dx = ev.dir * 95 * ev.s, x1 = ev.x0 + dx, hgt = 62 * ev.s, p = age / ev.dur;
        const y0 = surfaceAt(row, ev.x0), y1 = surfaceAt(row, x1);
        if (ev.phase < 0) { burst(foam, ev.x0, y0, ev.s, 8, 1.4); ev.phase = 0; }
        if (p >= 1) { if (ev.phase === 0) { burst(foam, x1, y1, ev.s, 10, 1.2); ev.phase = 1; } if (age > ev.dur + 1.5) events.splice(k, 1); continue; }
        const x = ev.x0 + dx * p, y = y0 + (y1 - y0) * p - hgt * 4 * p * (1 - p);
        const ang = Math.atan2((y1 - y0) - hgt * 4 * (1 - 2 * p), dx);
        drawFish(ctx, x, y, ang, ev.dir, ev.s, ink, .5 * Math.min(1, p * 6, (1 - p) * 6));
      }
      // rings spreading on the surface where the water was broken
      const now = performance.now();
      for (let k = ripples.length - 1; k >= 0; k--) {
        const r = ripples[k], a = (now - r.born) / 1400;
        if (a >= 1) { ripples.splice(k, 1); continue; }
        ctx.strokeStyle = `rgba(${ink},${.32 * (1 - a)})`; ctx.lineWidth = .8;
        for (const f of [1, .55]) {
          const rx = (5 + 34 * a * f) * r.s;
          ctx.beginPath(); ctx.ellipse(r.x, r.y, rx, rx * .26, 0, 0, 6.283); ctx.stroke();
        }
      }
    },
  };
}
