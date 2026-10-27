/* Progressive enhancements: every page remains readable without this file or GSAP. */
(function () {
  'use strict';
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let finishOpening = function () {};
  let ambientEnabled = true;

  function setPageUtilities() {
    const normalize = (path) => path.replace(/\/+/g, '/').replace(/\/?$/, '/');
    const current = normalize(window.location.pathname);
    document.querySelectorAll('.nav-links a').forEach((link) => {
      const href = link.getAttribute('href');
      if (!href || !href.startsWith('/')) return;
      const target = normalize(href);
      const active = target === '/' ? current === '/' : current.startsWith(target);
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
    document.querySelectorAll('[data-year]').forEach((node) => {
      node.textContent = new Date().getFullYear();
    });
    const main = document.querySelector('main');
    if (main && !main.id) main.id = 'mainContent';
    if (main) main.setAttribute('tabindex', '-1');
  }

  function initNavigation() {
    if (!document.body.classList.contains('home-page')) return;
    document.body.classList.add('js-ready');
    let queued = false;
    const update = () => {
      document.body.classList.toggle('nav-visible', window.scrollY > 24);
      queued = false;
    };
    window.addEventListener('scroll', () => {
      if (!queued) {
        queued = true;
        window.requestAnimationFrame(update);
      }
    }, { passive: true });
    window.addEventListener('pageshow', update);
    update();
  }

  function playOpening() {
    const intro = document.getElementById('homeIntro');
    const body = document.body;
    if (!intro || reducedMotion.matches) {
      body.classList.add('hero-ready');
      return function () {};
    }
    let finished = false;
    let exitStarted = false;
    const inertNodes = [...document.querySelectorAll('.signature-hero, .home-content, .navbar')];
    const previousInert = inertNodes.map((node) => node.inert);
    let exitTimer;
    let finishTimer;
    let watchdog;
    const finish = () => {
      if (finished) return;
      finished = true;
      window.clearTimeout(exitTimer);
      window.clearTimeout(finishTimer);
      window.clearTimeout(watchdog);
      intro.hidden = true;
      intro.classList.remove('intro-playing', 'intro-leaving');
      body.classList.remove('intro-running');
      body.classList.add('hero-ready');
      inertNodes.forEach((node, index) => { node.inert = previousInert[index]; });
      window.removeEventListener('keydown', onKey);
      document.dispatchEvent(new Event('openingcomplete'));
    };
    const exit = () => {
      if (finished || exitStarted) return;
      exitStarted = true;
      intro.classList.add('intro-leaving');
      finishTimer = window.setTimeout(finish, 470);
    };
    const onKey = (event) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        finish();
      }
    };
    body.classList.remove('hero-ready');
    intro.hidden = false;
    body.classList.add('intro-running');
    inertNodes.forEach((node) => { node.inert = true; });
    window.addEventListener('keydown', onKey);
    window.requestAnimationFrame(() => {
      if (!finished) intro.classList.add('intro-playing');
    });
    exitTimer = window.setTimeout(exit, 2050);
    watchdog = window.setTimeout(finish, 3200);
    return finish;
  }

  function initAmbientScene() {
    const canvas = document.getElementById('siteStarfield');
    const scene = document.querySelector('.signature-hero');
    if (!canvas || !scene) return;
    const ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) return;
    let width = 0;
    let height = 0;
    let frame = 0;
    let lastTime = 0;
    let particles = [];
    let inView = scene.getBoundingClientRect().bottom > 0;
    const toggle = document.querySelector('[data-motion-toggle]');

    function paint(delta) {
      ctx.clearRect(0, 0, width, height);
      particles.forEach((p) => {
        p.phase += delta * .00012;
        const x = p.x * width + Math.sin(p.phase) * 9;
        const y = p.y * height + Math.cos(p.phase * .7) * 7;
        const alpha = p.alpha * (.82 + Math.sin(p.phase * 1.5) * .18);
        ctx.fillStyle = 'rgba(166,223,220,' + alpha + ')';
        ctx.beginPath();
        ctx.arc(x, y, p.size, 0, Math.PI * 2);
        ctx.fill();
      });
    }
    function shouldAnimate() {
      return inView && !document.hidden && !reducedMotion.matches && ambientEnabled;
    }
    function draw(now) {
      frame = 0;
      if (!shouldAnimate()) return;
      paint(lastTime ? Math.min(now - lastTime, 40) : 0);
      lastTime = now;
      frame = window.requestAnimationFrame(draw);
    }
    function sync() {
      if (frame) window.cancelAnimationFrame(frame);
      frame = 0;
      lastTime = 0;
      if (inView && !document.hidden) paint(0);
      if (shouldAnimate()) frame = window.requestAnimationFrame(draw);
      if (toggle) {
        toggle.hidden = false;
        toggle.disabled = reducedMotion.matches;
        toggle.textContent = reducedMotion.matches ? 'Motion reduced' : (ambientEnabled ? 'Motion on' : 'Motion off');
        toggle.setAttribute('aria-pressed', String(ambientEnabled && !reducedMotion.matches));
      }
    }
    function resize() {
      const rect = scene.getBoundingClientRect();
      width = rect.width;
      height = rect.height;
      const dpr = Math.min(window.devicePixelRatio || 1, width < 700 ? 1.5 : 2);
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const count = width < 700 ? 30 : 68;
      particles = Array.from({ length: count }, () => ({
        x: Math.random(), y: Math.random(), phase: Math.random() * Math.PI * 2,
        alpha: .12 + Math.random() * .28, size: .35 + Math.random() * .85
      }));
      sync();
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver((entries) => {
        inView = entries[0].isIntersecting;
        sync();
      }).observe(scene);
    }
    window.addEventListener('resize', resize, { passive: true });
    document.addEventListener('visibilitychange', sync);
    reducedMotion.addEventListener('change', sync);
    if (toggle) toggle.addEventListener('click', () => {
      ambientEnabled = !ambientEnabled;
      sync();
    });
    resize();
  }

  function initMotion() {
    const gsap = window.gsap;
    const ScrollTrigger = window.ScrollTrigger;
    if (!gsap || !ScrollTrigger) return;
    gsap.registerPlugin(ScrollTrigger);
    // Own geometry refreshes below: the default load/resize refresh can restore
    // an intermediate position in the middle of native smooth-anchor scrolling.
    ScrollTrigger.config({ autoRefreshEvents: 'none' });
    const media = gsap.matchMedia();
    const revealNodes = [...document.querySelectorAll('[data-reveal]')];
    const showAll = () => {
      gsap.killTweensOf(revealNodes);
      gsap.set(revealNodes, { clearProps: 'transform,opacity,visibility' });
    };
    try {
      media.add('(prefers-reduced-motion: no-preference)', () => {
        // Already-visible or history-restored content is never hidden on initialization.
        const pending = revealNodes.filter((node) => node.getBoundingClientRect().top > window.innerHeight * .96);
        if (pending.length) {
          // Opacity leaves off-screen links in the keyboard tab order. Focus reveals
          // their parent immediately; visibility:hidden would skip those links.
          gsap.set(pending, { opacity: 0, y: 24 });
          ScrollTrigger.batch(pending, {
            start: 'top 97%',
            once: true,
            interval: .06,
            batchMax: 3,
            onEnter: (batch) => gsap.to(batch, {
              opacity: 1, y: 0, duration: .65, stagger: .07,
              ease: 'power2.out', overwrite: 'auto',
              clearProps: 'transform,opacity,visibility'
            })
          });
        }
        document.querySelectorAll('.directory-group > h2').forEach((heading) => {
          gsap.fromTo(heading, { '--rule-progress': 0 }, {
            '--rule-progress': 1, duration: .8, ease: 'power2.out',
            scrollTrigger: { trigger: heading, start: 'top 97%', once: true }
          });
        });
      });
      media.add('(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)', () => {
        const cleanup = [];
        document.querySelectorAll('[data-magnetic]').forEach((button) => {
          const xTo = gsap.quickTo(button, 'x', { duration: .35, ease: 'power2.out' });
          const yTo = gsap.quickTo(button, 'y', { duration: .35, ease: 'power2.out' });
          // Read bounds on entry, before transforms change the element's bounds.
          let bounds;
          const enter = () => { bounds = button.getBoundingClientRect(); };
          const move = (event) => {
            if (!bounds) return;
            xTo(Math.max(-5, Math.min(5, (event.clientX - bounds.left - bounds.width / 2) * .06)));
            yTo(Math.max(-4, Math.min(4, (event.clientY - bounds.top - bounds.height / 2) * .12)));
          };
          const leave = () => { bounds = null; xTo(0); yTo(0); };
          button.addEventListener('pointerenter', enter);
          button.addEventListener('pointermove', move);
          button.addEventListener('pointerleave', leave);
          button.addEventListener('blur', leave);
          cleanup.push(() => {
            button.removeEventListener('pointerenter', enter);
            button.removeEventListener('pointermove', move);
            button.removeEventListener('pointerleave', leave);
            button.removeEventListener('blur', leave);
          });
        });
        const hero = document.querySelector('.signature-hero');
        const signature = document.querySelector('.hero-signature');
        if (hero && signature) {
          const xTo = gsap.quickTo(signature, 'x', { duration: 1.2, ease: 'power2.out' });
          const yTo = gsap.quickTo(signature, 'y', { duration: 1.2, ease: 'power2.out' });
          const move = (event) => {
            if (!ambientEnabled || document.hidden) return;
            const bounds = hero.getBoundingClientRect();
            xTo((event.clientX / bounds.width - .5) * 8);
            yTo(((event.clientY - bounds.top) / bounds.height - .5) * 5);
          };
          const leave = () => { xTo(0); yTo(0); };
          hero.addEventListener('pointermove', move);
          hero.addEventListener('pointerleave', leave);
          cleanup.push(() => {
            hero.removeEventListener('pointermove', move);
            hero.removeEventListener('pointerleave', leave);
          });
        }
        return () => cleanup.forEach((fn) => fn());
      });
      let refreshTimer;
      let lastScroll = 0;
      window.addEventListener('scroll', () => { lastScroll = performance.now(); }, { passive: true });
      const refresh = () => {
        window.clearTimeout(refreshTimer);
        const afterScroll = () => {
          // Refresh restores a recorded scroll position. Wait for native anchor
          // scrolling to settle so an image/font load cannot interrupt it.
          if (ScrollTrigger.isScrolling() || performance.now() - lastScroll < 180) {
            refreshTimer = window.setTimeout(afterScroll, 180);
            return;
          }
          ScrollTrigger.refresh();
        };
        refreshTimer = window.setTimeout(afterScroll, 180);
      };
      document.fonts.ready.then(refresh);
      window.addEventListener('resize', refresh, { passive: true });
      window.addEventListener('load', refresh, { once: true });
      document.addEventListener('visibilitychange', () => {
        if (!document.hidden) refresh();
      });
      document.querySelectorAll('img').forEach((img) => {
        if (!img.complete) img.addEventListener('load', refresh, { once: true });
      });
      // Neither a fixed overlay nor an anchor changes document geometry.
      window.addEventListener('hashchange', () => ScrollTrigger.update());
      window.addEventListener('pageshow', (event) => {
        if (event.persisted) { showAll(); refresh(); }
      });
      document.addEventListener('focusin', (event) => {
        const node = event.target.closest && event.target.closest('[data-reveal]');
        if (node) {
          gsap.killTweensOf(node);
          gsap.set(node, { clearProps: 'transform,opacity,visibility' });
        }
      });
    } catch (error) {
      media.revert();
      showAll();
      console.warn('Motion enhancement unavailable; the static page remains usable.', error);
    }
  }

  function initImageViewer() {
    if (!window.HTMLDialogElement || typeof HTMLDialogElement.prototype.showModal !== 'function') return;
    const links = [...document.querySelectorAll('a[data-image-viewer]')];
    if (!links.length) return;
    const dialog = document.createElement('dialog');
    dialog.className = 'image-viewer';
    dialog.setAttribute('aria-labelledby', 'viewerCaption');
    dialog.innerHTML = '<button type="button" class="button viewer-close" aria-label="Close image">Close <span aria-hidden="true">×</span></button><img alt=""><p class="viewer-caption" id="viewerCaption"></p><a class="small-link viewer-original" target="_blank" rel="noopener">View original ↗</a>';
    document.body.append(dialog);
    const image = dialog.querySelector('img');
    const caption = dialog.querySelector('.viewer-caption');
    const original = dialog.querySelector('.viewer-original');
    let opener;
    const sizeImage = () => {
      image.style.maxWidth = Math.max(1, Math.min(image.naturalWidth || 1600, window.innerWidth * .94 - 48)) + 'px';
    };
    image.addEventListener('load', sizeImage);
    window.addEventListener('resize', () => { if (dialog.open) sizeImage(); }, { passive: true });
    links.forEach((link) => link.addEventListener('click', (event) => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      opener = link;
      const source = link.querySelector('img');
      image.alt = source ? source.alt : '';
      image.src = link.href;
      image.style.maxWidth = Math.max(1, Math.min(source && source.naturalWidth || 1600, window.innerWidth * .94 - 48)) + 'px';
      caption.textContent = link.dataset.caption || image.alt;
      original.href = link.href;
      dialog.showModal();
      document.body.classList.add('viewer-open');
      dialog.querySelector('button').focus();
    }));
    dialog.querySelector('button').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', (event) => {
      const rect = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
    });
    dialog.addEventListener('close', () => {
      document.body.classList.remove('viewer-open');
      if (opener && opener.isConnected) opener.focus({ preventScroll: true });
    });
  }

  function init() {
    setPageUtilities();
    initNavigation();
    finishOpening = playOpening();
    initAmbientScene();
    initImageViewer();
    initMotion();
    reducedMotion.addEventListener('change', () => {
      if (reducedMotion.matches) finishOpening();
    });
    window.addEventListener('pagehide', () => finishOpening());
    window.addEventListener('pageshow', (event) => {
      if (event.persisted && document.body.classList.contains('home-page')) finishOpening = playOpening();
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
