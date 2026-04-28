(function () {
  const state = {
    homeReveal: 0
  };

  function setActiveNavLink() {
    const path = window.location.pathname.replace(/\/+/g, '/');

    document.querySelectorAll('.nav-links a').forEach((link) => {
      const href = link.getAttribute('href');
      if (!href) return;

      const normalizedHref = href.endsWith('/') ? href : `${href}/`;

      if (
        path === href ||
        path === normalizedHref ||
        (href === '/' && path === '/')
      ) {
        link.classList.add('active');
      }
    });
  }

  function setCurrentYear() {
    const yearElement = document.querySelector('[data-year]');
    if (yearElement) {
      yearElement.textContent = new Date().getFullYear();
    }
  }

  function initHomeReveal() {
    const isHomePage = document.body.classList.contains('home-page');
    if (!isHomePage) return;

    const maxRevealDistance = () => Math.max(window.innerHeight * 0.9, 520);

    let rafId = 0;

    const updateHomeReveal = () => {
      rafId = 0;

      const y = window.scrollY || window.pageYOffset || 0;
      const reveal = Math.min(Math.max(y / maxRevealDistance(), 0), 1);
      const revealed = reveal > 0.03;

      state.homeReveal = reveal;

      document.body.style.setProperty('--home-reveal', reveal.toFixed(4));
      document.body.classList.toggle('home-revealed', revealed);
      document.body.classList.toggle('intro-visible', reveal < 0.98);
    };

    const requestHomeRevealUpdate = () => {
      if (rafId) return;
      rafId = window.requestAnimationFrame(updateHomeReveal);
    };

    window.addEventListener('scroll', requestHomeRevealUpdate, { passive: true });
    window.addEventListener('resize', requestHomeRevealUpdate);

    requestHomeRevealUpdate();
  }

  function initLogoDrift() {
    const intro = document.getElementById('homeIntro');
    if (!intro) return;

    let targetX = 0;
    let targetY = 0;
    let currentX = 0;
    let currentY = 0;
    let rafId = 0;

    const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

    const getMaxDrift = () => {
      return window.innerWidth < 700 ? 9 : 16;
    };

    const writeDrift = () => {
      const maxDrift = getMaxDrift();

      intro.style.setProperty('--logo-drift-x', `${(currentX * maxDrift).toFixed(2)}px`);
      intro.style.setProperty('--logo-drift-y', `${(currentY * maxDrift).toFixed(2)}px`);
    };

    const update = () => {
      rafId = 0;

      currentX += (targetX - currentX) * 0.085;
      currentY += (targetY - currentY) * 0.085;

      writeDrift();

      if (
        Math.abs(targetX - currentX) > 0.0008 ||
        Math.abs(targetY - currentY) > 0.0008
      ) {
        rafId = window.requestAnimationFrame(update);
      }
    };

    const requestUpdate = () => {
      if (rafId) return;
      rafId = window.requestAnimationFrame(update);
    };

    window.addEventListener(
      'mousemove',
      (event) => {
        const width = window.innerWidth || 1;
        const height = window.innerHeight || 1;

        targetX = clamp((event.clientX / width) * 2 - 1, -1, 1);
        targetY = clamp((event.clientY / height) * 2 - 1, -1, 1);

        requestUpdate();
      },
      { passive: true }
    );

    window.addEventListener(
      'mouseleave',
      () => {
        targetX = 0;
        targetY = 0;
        requestUpdate();
      },
      { passive: true }
    );

    writeDrift();
  }

  function initScrollCue() {
    const cue = document.getElementById('scrollCue');
    if (!cue) return;

    let lastMouseY = -1;

    function updateCue() {
      const nearTop = window.scrollY < 24;
      const mouseNearBottom = lastMouseY > window.innerHeight * 0.74;

      cue.classList.toggle('is-visible', nearTop && mouseNearBottom);
    }

    window.addEventListener(
      'mousemove',
      (event) => {
        lastMouseY = event.clientY;
        updateCue();
      },
      { passive: true }
    );

    window.addEventListener(
      'mouseleave',
      () => {
        lastMouseY = -1;
        updateCue();
      },
      { passive: true }
    );

    window.addEventListener('scroll', updateCue, { passive: true });
    window.addEventListener('resize', updateCue);
  }

  function initStarfield() {
    const canvas = document.getElementById('introStars');
    if (!canvas) return;

    const ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) return;

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    let width = 0;
    let height = 0;
    let dpr = 1;
    let particles = [];
    let rafId = 0;

    const pointer = {
      x: -9999,
      y: -9999,
      active: false
    };

    const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

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

    function createParticles() {
      const area = width * height;
      const count = prefersReducedMotion
        ? 75
        : clamp(Math.floor(area / 12500), 100, 185);

      particles = Array.from({ length: count }, () => {
        const x = Math.random() * width;
        const y = Math.random() * height;
        const radius = Math.random() * 1.35 + 0.35;

        return {
          x,
          y,
          baseX: x,
          baseY: y,
          vx: 0,
          vy: 0,
          radius,
          alpha: Math.random() * 0.5 + 0.2,
          twinkle: Math.random() * Math.PI * 2,
          drift: Math.random() * 0.22 + 0.05
        };
      });
    }

    function drawParticle(p, centerX, centerY) {
      p.twinkle += 0.012 + p.drift * 0.015;

      let forceX = 0;
      let forceY = 0;

      if (pointer.active && !prefersReducedMotion) {
        const dx = p.x - pointer.x;
        const dy = p.y - pointer.y;
        const distSq = dx * dx + dy * dy;
        const repelRadius = 145;
        const repelRadiusSq = repelRadius * repelRadius;

        if (distSq < repelRadiusSq && distSq > 0.001) {
          const dist = Math.sqrt(distSq);
          const strength = (1 - dist / repelRadius) * 1.65;

          forceX += (dx / dist) * strength;
          forceY += (dy / dist) * strength;
        }
      }

      const slowOrbitX = Math.cos(p.twinkle * 0.34) * p.drift;
      const slowOrbitY = Math.sin(p.twinkle * 0.31) * p.drift;

      const pullX = (p.baseX - p.x) * 0.006;
      const pullY = (p.baseY - p.y) * 0.006;

      p.vx = (p.vx + pullX + forceX + slowOrbitX * 0.015) * 0.91;
      p.vy = (p.vy + pullY + forceY + slowOrbitY * 0.015) * 0.91;

      p.x += p.vx;
      p.y += p.vy;

      const dxCenter = p.x - centerX;
      const dyCenter = p.y - centerY;
      const centerDist = Math.sqrt(dxCenter * dxCenter + dyCenter * dyCenter);
      const centerGlow = Math.max(0, 1 - centerDist / Math.min(width, height) * 1.15);

      const twinkleAlpha = p.alpha * (0.74 + Math.sin(p.twinkle) * 0.26);
      const finalAlpha = Math.min(1, twinkleAlpha + centerGlow * 0.18);

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(139, 241, 238, ${finalAlpha})`;
      ctx.fill();
    }

    function draw() {
      rafId = 0;

      ctx.clearRect(0, 0, width, height);

      if (!document.hidden) {
        const centerX = width / 2;
        const centerY = height / 2;

        for (const p of particles) {
          drawParticle(p, centerX, centerY);
        }
      }

      rafId = window.requestAnimationFrame(draw);
    }

    function start() {
      if (rafId) return;
      rafId = window.requestAnimationFrame(draw);
    }

    window.addEventListener(
      'mousemove',
      (event) => {
        pointer.x = event.clientX;
        pointer.y = event.clientY;
        pointer.active = true;
      },
      { passive: true }
    );

    window.addEventListener(
      'mouseleave',
      () => {
        pointer.active = false;
        pointer.x = -9999;
        pointer.y = -9999;
      },
      { passive: true }
    );

    window.addEventListener('resize', resize);

    document.addEventListener('visibilitychange', () => {
      if (!document.hidden) {
        start();
      }
    });

    resize();
    start();
  }

  document.addEventListener('DOMContentLoaded', () => {
    setActiveNavLink();
    setCurrentYear();
    initHomeReveal();
    initLogoDrift();
    initScrollCue();
    initStarfield();
  });
})();