/* Interactive physics explorers. Pages stay complete without this file. */
(function () {
  'use strict';
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const COLORS = {
    grid: 'rgba(223,236,242,.08)', axis: 'rgba(223,236,242,.35)', text: '#9aa4ac',
    accent: '#8ce7df', warm: '#f2c38b', data: 'rgba(233,237,240,.55)'
  };

  function setupCanvas(canvas) {
    const ctx = canvas.getContext('2d');
    const size = () => {
      const rect = canvas.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(rect.width * dpr);
      canvas.height = Math.round(rect.height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      return { w: rect.width, h: rect.height };
    };
    return { ctx, size };
  }

  function bindSliders(root, onChange) {
    const values = {};
    root.querySelectorAll('input[type=range]').forEach((input) => {
      const out = root.querySelector('output[for="' + input.id + '"]');
      const digits = Number(input.dataset.digits || 2);
      const read = () => {
        values[input.name] = Number(input.value);
        if (out) out.textContent = Number(input.value).toFixed(digits) + (input.dataset.unit || '');
      };
      read();
      input.addEventListener('input', () => { read(); onChange(); });
    });
    return values;
  }

  function frame(ctx, box, pad, xLabel, yLabel) {
    ctx.clearRect(0, 0, box.w, box.h);
    ctx.strokeStyle = COLORS.grid;
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = pad.t + (box.h - pad.t - pad.b) * i / 4;
      ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(box.w - pad.r, y); ctx.stroke();
    }
    ctx.strokeStyle = COLORS.axis;
    ctx.beginPath();
    ctx.moveTo(pad.l, pad.t); ctx.lineTo(pad.l, box.h - pad.b); ctx.lineTo(box.w - pad.r, box.h - pad.b);
    ctx.stroke();
    ctx.fillStyle = COLORS.text;
    ctx.font = '10px ui-monospace, Consolas, monospace';
    ctx.textAlign = 'right';
    ctx.fillText(xLabel, box.w - pad.r, box.h - 8);
    ctx.textAlign = 'left';
    ctx.fillText(yLabel, pad.l + 6, pad.t + 10);
  }

  // Gaussian approximation to Poisson noise; every bin holds hundreds of counts.
  function gauss() {
    let u = 0, v = 0;
    while (!u) u = Math.random();
    while (!v) v = Math.random();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  function initWiggle(root) {
    const canvas = root.querySelector('canvas');
    const status = root.querySelector('[data-status]');
    const { ctx, size } = setupCanvas(canvas);
    const T_MAX = 100; // microseconds
    const BINS = 400;
    const N0 = 4000;
    const OMEGA0 = 2 * Math.PI * 0.2291; // rad / microsecond, the muon g-2 anomalous frequency
    let truth;
    let data = [];
    const model = (t, p) => p.n0 * Math.exp(-t / p.tau) * (1 + p.A * Math.cos(p.omega * t + p.phi));
    const params = bindSliders(root, draw);
    const current = () => ({ n0: N0, tau: params.tau, A: params.A, omega: OMEGA0 * params.omega, phi: params.phi });

    function generate() {
      truth = {
        n0: N0, tau: 64.4, A: 0.25 + Math.random() * 0.2,
        omega: OMEGA0 * (0.85 + Math.random() * 0.3), phi: (Math.random() * 2 - 1) * Math.PI
      };
      data = Array.from({ length: BINS }, (_, i) => {
        const t = (i + .5) * T_MAX / BINS;
        const mu = model(t, truth);
        return { t, n: Math.max(0, mu + Math.sqrt(mu) * gauss()) };
      });
      draw();
    }

    function chi2() {
      const p = current();
      let sum = 0;
      data.forEach((d) => {
        const m = model(d.t, p);
        sum += (d.n - m) * (d.n - m) / Math.max(d.n, 1);
      });
      return sum / (data.length - 5);
    }

    function draw() {
      const box = size();
      const pad = { l: 46, r: 14, t: 16, b: 30 };
      frame(ctx, box, pad, 'time (μs)', 'counts (log)');
      const yMin = Math.log10(N0 * Math.exp(-T_MAX / 64.4) * .35);
      const yMax = Math.log10(N0 * 1.9);
      const X = (t) => pad.l + (box.w - pad.l - pad.r) * t / T_MAX;
      const Y = (n) => pad.t + (box.h - pad.t - pad.b) * Math.min(1, Math.max(0, 1 - (Math.log10(Math.max(n, 1)) - yMin) / (yMax - yMin)));
      ctx.fillStyle = COLORS.text;
      ctx.textAlign = 'center';
      for (let t = 0; t <= T_MAX; t += 20) ctx.fillText(String(t), X(t), box.h - pad.b + 14);
      ctx.fillStyle = COLORS.data;
      data.forEach((d) => { ctx.fillRect(X(d.t) - 1, Y(d.n) - 1, 2, 2); });
      const p = current();
      ctx.strokeStyle = COLORS.accent;
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      for (let i = 0; i <= 900; i++) {
        const t = T_MAX * i / 900;
        const y = Y(model(t, p));
        if (i) ctx.lineTo(X(t), y); else ctx.moveTo(X(t), y);
      }
      ctx.stroke();
      if (status) {
        const c = chi2();
        status.textContent = 'χ²/ndf = ' + c.toFixed(2) + (c < 1.3 ? '  ·  good fit' : c < 3 ? '  ·  close' : '');
      }
    }

    root.querySelector('[data-action="new"]').addEventListener('click', generate);
    root.querySelector('[data-action="reveal"]').addEventListener('click', () => {
      const set = (name, value) => {
        const input = root.querySelector('input[name="' + name + '"]');
        input.value = value;
        input.dispatchEvent(new Event('input'));
      };
      set('A', truth.A); set('omega', truth.omega / OMEGA0); set('phi', truth.phi); set('tau', truth.tau);
    });
    window.addEventListener('resize', draw, { passive: true });
    generate();
  }

  function initPendulum(root) {
    const canvas = root.querySelector('canvas');
    const play = root.querySelector('[data-action="play"]');
    const { ctx, size } = setupCanvas(canvas);
    const T_MAX = 20; // seconds
    let tracks = [];
    let animStart = 0;
    let raf = 0;
    const params = bindSliders(root, () => { solve(); draw(T_MAX); });

    // RK4 for theta'' = -w0^2 sin(theta) - drag(theta').
    function integrate(drag) {
      const w2 = Math.pow(2 * Math.PI / params.period, 2);
      const dt = 0.004;
      let th = params.amp * Math.PI / 180;
      let om = 0;
      const out = [];
      const f = (a, w) => -w2 * Math.sin(a) - drag(w);
      for (let t = 0; t <= T_MAX + 1e-9; t += dt) {
        out.push(th);
        const k1a = om, k1w = f(th, om);
        const k2a = om + k1w * dt / 2, k2w = f(th + k1a * dt / 2, om + k1w * dt / 2);
        const k3a = om + k2w * dt / 2, k3w = f(th + k2a * dt / 2, om + k2w * dt / 2);
        const k4a = om + k3w * dt, k4w = f(th + k3a * dt, om + k3w * dt);
        th += dt * (k1a + 2 * k2a + 2 * k3a + k4a) / 6;
        om += dt * (k1w + 2 * k2w + 2 * k3w + k4w) / 6;
      }
      return { dt, out };
    }

    function solve() {
      tracks = [
        { color: COLORS.accent, data: integrate((w) => params.linear * w) },
        { color: COLORS.warm, data: integrate((w) => params.quad * w * Math.abs(w)) }
      ];
    }

    function draw(tNow) {
      const box = size();
      const bobArea = Math.min(150, box.w * .28);
      const pad = { l: 36 + bobArea, r: 14, t: 16, b: 30 };
      frame(ctx, box, pad, 'time (s)', 'θ (deg)');
      const amp = params.amp;
      const X = (t) => pad.l + (box.w - pad.l - pad.r) * t / T_MAX;
      const Y = (a) => pad.t + (box.h - pad.t - pad.b) * (.5 - a * 180 / Math.PI / (2.2 * amp));
      ctx.fillStyle = COLORS.text;
      ctx.textAlign = 'center';
      for (let t = 0; t <= T_MAX; t += 5) ctx.fillText(String(t), X(t), box.h - pad.b + 14);
      tracks.forEach((track, index) => {
        const { dt, out } = track.data;
        const last = Math.min(out.length - 1, Math.floor(tNow / dt));
        ctx.strokeStyle = track.color;
        ctx.lineWidth = 1.3;
        ctx.beginPath();
        for (let i = 0; i <= last; i += 2) {
          if (i) ctx.lineTo(X(i * dt), Y(out[i])); else ctx.moveTo(X(0), Y(out[0]));
        }
        ctx.stroke();
        // Both pendulums hang from one pivot so their divergence is visible.
        const pivotX = 18 + bobArea / 2;
        const pivotY = pad.t + 14;
        const r = Math.min(box.h - pad.t - pad.b - 40, bobArea * .62);
        const a = out[last];
        const bx = pivotX + Math.sin(a) * r;
        const by = pivotY + Math.cos(a) * r;
        ctx.strokeStyle = 'rgba(223,236,242,.4)';
        ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(pivotX, pivotY); ctx.lineTo(bx, by); ctx.stroke();
        ctx.globalAlpha = .85;
        ctx.fillStyle = track.color;
        ctx.beginPath(); ctx.arc(bx, by, 7, 0, Math.PI * 2); ctx.fill();
        ctx.globalAlpha = 1;
      });
    }

    function step(now) {
      if (!animStart) animStart = now;
      const t = (now - animStart) / 1000 * 2; // 2x real time
      draw(Math.min(t, T_MAX));
      if (t < T_MAX && !document.hidden) raf = window.requestAnimationFrame(step);
      else { raf = 0; play.textContent = 'Replay'; }
    }

    play.addEventListener('click', () => {
      if (raf) window.cancelAnimationFrame(raf);
      if (reducedMotion.matches) { draw(T_MAX); return; }
      animStart = 0;
      play.textContent = 'Playing…';
      raf = window.requestAnimationFrame(step);
    });
    window.addEventListener('resize', () => { if (!raf) draw(T_MAX); }, { passive: true });
    solve();
    draw(T_MAX);
  }

  function init() {
    document.querySelectorAll('[data-lab]').forEach((root) => {
      root.hidden = false;
      const fallback = root.parentElement.querySelector('[data-lab-fallback]');
      if (fallback) fallback.hidden = true;
      if (root.dataset.lab === 'wiggle') initWiggle(root);
      if (root.dataset.lab === 'pendulum') initPendulum(root);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
