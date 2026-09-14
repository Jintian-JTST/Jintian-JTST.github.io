(function () {
  function normalizePath(value) {
    const normalized = value.replace(/\/+/g, '/');
    return normalized === '/' ? '/' : `${normalized.replace(/\/$/, '')}/`;
  }

  function setActiveNavLink() {
    const path = normalizePath(window.location.pathname);

    document.querySelectorAll('.nav-links a').forEach((link) => {
      const href = link.getAttribute('href');
      if (!href || !href.startsWith('/')) return;

      const target = normalizePath(href);
      const isCurrent = target === '/' ? path === '/' : path.startsWith(target);

      link.classList.toggle('active', isCurrent);
      if (isCurrent) {
        link.setAttribute('aria-current', 'page');
      } else {
        link.removeAttribute('aria-current');
      }
    });
  }

  function setCurrentYear() {
    document.querySelectorAll('[data-year]').forEach((element) => {
      element.textContent = new Date().getFullYear();
    });
  }

  function initStarfield() {
    const canvas = document.getElementById('siteStarfield');
    if (!canvas) return;

    const ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) return;

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let width = 0;
    let height = 0;
    let dpr = 1;
    let particles = [];
    let rafId = 0;

    const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

    function createParticles() {
      const area = width * height;
      const count = prefersReducedMotion ? 60 : clamp(Math.floor(area / 14500), 80, 150);

      particles = Array.from({ length: count }, () => {
        const x = Math.random() * width;
        const y = Math.random() * height;

        return {
          x,
          y,
          baseX: x,
          baseY: y,
          vx: 0,
          vy: 0,
          radius: Math.random() * 1.15 + 0.3,
          alpha: Math.random() * 0.38 + 0.14,
          phaseA: Math.random() * Math.PI * 2,
          phaseB: Math.random() * Math.PI * 2,
          speedA: Math.random() * 0.006 + 0.002,
          speedB: Math.random() * 0.005 + 0.0015,
          wanderX: Math.random() * 28 + 8,
          wanderY: Math.random() * 24 + 8
        };
      });
    }

    function resize() {
      dpr = clamp(window.devicePixelRatio || 1, 1, 2);
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      createParticles();
    }

    function drawParticle(particle) {
      particle.phaseA += particle.speedA;
      particle.phaseB += particle.speedB;

      const targetX = particle.baseX + Math.cos(particle.phaseA) * particle.wanderX;
      const targetY = particle.baseY + Math.sin(particle.phaseB) * particle.wanderY;
      particle.vx = (particle.vx + (targetX - particle.x) * 0.006) * 0.965;
      particle.vy = (particle.vy + (targetY - particle.y) * 0.006) * 0.965;
      particle.x += particle.vx;
      particle.y += particle.vy;

      const twinkle = 0.74 + Math.sin(particle.phaseA * 2.4 + particle.phaseB) * 0.26;
      ctx.beginPath();
      ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(139, 241, 238, ${particle.alpha * twinkle})`;
      ctx.fill();
    }

    function draw() {
      ctx.clearRect(0, 0, width, height);
      particles.forEach(drawParticle);
      rafId = window.requestAnimationFrame(draw);
    }

    window.addEventListener('resize', resize);
    document.addEventListener('visibilitychange', () => {
      if (document.hidden && rafId) {
        window.cancelAnimationFrame(rafId);
        rafId = 0;
      } else if (!document.hidden && !rafId) {
        rafId = window.requestAnimationFrame(draw);
      }
    });

    resize();
    if (prefersReducedMotion) {
      particles.forEach(drawParticle);
    } else {
      rafId = window.requestAnimationFrame(draw);
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    setActiveNavLink();
    setCurrentYear();
    initStarfield();
  });
})();
