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
    let watchdog;
    const finish = () => {
      if (finished) return;
      finished = true;
      window.clearTimeout(watchdog);
      intro.hidden = true;
      intro.classList.remove('intro-playing', 'intro-filling', 'intro-leaving');
      body.classList.remove('intro-running');
      body.classList.add('hero-ready');
      inertNodes.forEach((node, index) => { node.inert = previousInert[index]; });
      window.removeEventListener('keydown', onKey);
      document.dispatchEvent(new Event('openingcomplete'));
    };
    // Each stage starts on the previous stage's end event: trace -> fill -> leave -> done.
    const logo = intro.querySelector('.intro-logo');
    const strokes = [...intro.querySelectorAll('.logo-lines path')];
    const lastStroke = strokes[strokes.length - 1];
    const fill = intro.querySelector('.logo-fill');
    const exit = () => {
      if (finished || exitStarted) return;
      exitStarted = true;
      intro.classList.add('intro-leaving');
      if (logo) logo.addEventListener('transitionend', finish, { once: true });
      else finish();
    };
    if (lastStroke) lastStroke.addEventListener('animationend', (event) => {
      if (event.animationName === 'logoTrace') intro.classList.add('intro-filling');
    });
    if (fill) fill.addEventListener('animationend', exit, { once: true });
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
    // Safety net only: if an animation event never fires, the page still unlocks.
    watchdog = window.setTimeout(finish, 3000);
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

    // Pin-prick stars that twinkle, plus a few soft motes drifting upward like plankton.
    function paint(delta) {
      ctx.clearRect(0, 0, width, height);
      particles.forEach((p) => {
        p.phase += delta * p.speed;
        if (p.mote) {
          p.y -= delta * p.rise;
          if (p.y < -.05) { p.y = 1.05; p.x = Math.random(); }
          const x = p.x * width + Math.sin(p.phase) * 18;
          const y = p.y * height;
          const alpha = p.alpha * (.7 + Math.sin(p.phase * 1.7) * .3);
          const glow = ctx.createRadialGradient(x, y, 0, x, y, p.size * 6);
          glow.addColorStop(0, 'rgba(160,240,232,' + alpha + ')');
          glow.addColorStop(.25, 'rgba(140,231,223,' + alpha * .35 + ')');
          glow.addColorStop(1, 'rgba(140,231,223,0)');
          ctx.fillStyle = glow;
          ctx.beginPath();
          ctx.arc(x, y, p.size * 6, 0, Math.PI * 2);
          ctx.fill();
          return;
        }
        const alpha = p.alpha * (.55 + Math.sin(p.phase) * .45);
        ctx.fillStyle = 'rgba(225,238,240,' + alpha + ')';
        ctx.beginPath();
        ctx.arc(p.x * width, p.y * height, p.size, 0, Math.PI * 2);
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
      const stars = width < 700 ? 90 : 190;
      const motes = width < 700 ? 9 : 18;
      particles = Array.from({ length: stars + motes }, (_, index) => {
        const mote = index >= stars;
        return {
          mote, x: Math.random(), y: Math.random(), phase: Math.random() * Math.PI * 2,
          speed: mote ? .0004 + Math.random() * .0005 : .0006 + Math.random() * .0016,
          rise: .000006 + Math.random() * .000012,
          alpha: mote ? .18 + Math.random() * .3 : .15 + Math.random() * .6,
          size: mote ? .8 + Math.random() * 1.6 : (Math.random() < .08 ? 1.1 + Math.random() * .6 : .3 + Math.random() * .6)
        };
      });
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

  // Hero page turn as a physical system, decided in real time. While input continues,
  // the page follows it against an elastic pull back to the current page. The moment
  // the displacement crosses the threshold, the target flips to the other page and a
  // damped spring, seeded with the input velocity, carries it there. Nothing waits for
  // the gesture to stop. Below the hero, scrolling is native.
  function initHeroSnap() {
    const hero = document.querySelector('.signature-hero');
    const next = document.getElementById('homeIntroduction');
    if (!hero || !next) return;
    const root = document.documentElement;
    const DRAG = .85; // fraction of input that moves the page
    const HOLD = { omega: 3, zeta: .9 }; // light elastic tension while the wheel keeps going
    const SNAP = { omega: 13, zeta: .86 }; // spring that carries the page once committed
    const GESTURE_GAP = 140; // ms without input that ends a gesture
    let x = 0; // position within the hero, px
    let v = 0; // velocity, px/s
    let origin = 0; // page the gesture started from
    let target = 0;
    let committed = false; // target flipped during this gesture
    let active = false; // physics loop owns the scroll position
    let frame = 0;
    let last = 0;
    let lastInput = 0;
    let inputVelocity = 0;
    let touch = null;

    const edge = () => next.getBoundingClientRect().top + window.scrollY;
    const threshold = () => Math.min(70, edge() * .09);
    const enabled = () => !reducedMotion.matches && !document.body.classList.contains('intro-running') && !document.body.classList.contains('viewer-open');
    const inZone = (direction) => {
      if (active) return true;
      const y = window.scrollY;
      const e = edge();
      if (y < e - 1) return true;
      return direction < 0 && Math.abs(y - e) <= 1;
    };
    const apply = () => {
      root.style.scrollBehavior = 'auto';
      window.scrollTo(0, x);
    };
    function stop() {
      cancelAnimationFrame(frame);
      frame = 0;
      active = false;
      committed = false;
      root.style.scrollBehavior = '';
    }
    function tick(now) {
      const dt = Math.min(.032, (now - last) / 1000 || .016);
      last = now;
      const gesturing = touch && touch.live ? true : now - lastInput < GESTURE_GAP;
      if (touch && touch.live && !committed) {
        // A finger on the glass pins the page where it is.
        v = 0;
      } else {
        const k = committed ? SNAP : (gesturing ? HOLD : SNAP);
        const a = -k.omega * k.omega * (x - target) - 2 * k.zeta * k.omega * v;
        v += a * dt;
        x += v * dt;
      }
      const top = edge();
      if (x < 0) { x = 0; v = 0; }
      if (x > top && !committed) { x = top; v = 0; }
      apply();
      if (!gesturing && Math.abs(x - target) < .5 && Math.abs(v) < 8) {
        x = target;
        apply();
        stop();
        return;
      }
      frame = requestAnimationFrame(tick);
    }
    function begin() {
      if (active) return;
      active = true;
      x = window.scrollY;
      v = 0;
      const e = edge();
      origin = target = Math.abs(x - e) < 2 ? e : (x < e / 2 ? 0 : e);
      committed = false;
      last = performance.now();
      frame = requestAnimationFrame(tick);
    }
    function commit(direction) {
      committed = true;
      target = direction > 0 ? edge() : 0;
      // Carry the input's momentum into the spring.
      v = inputVelocity;
    }
    function feed(delta) {
      const now = performance.now();
      const gap = now - lastInput;
      lastInput = now;
      // Once committed, the rest of this gesture (including trackpad inertia) is absorbed.
      if (committed) return;
      const move = delta * DRAG;
      x = Math.max(0, Math.min(edge(), x + move));
      inputVelocity = gap > GESTURE_GAP ? move / .016 : inputVelocity * .5 + (move / (Math.max(8, gap) / 1000)) * .5;
      apply();
      const offset = x - origin;
      if (Math.abs(offset) >= threshold() && (offset > 0 ? origin === 0 : origin > 0)) commit(offset);
    }

    window.addEventListener('wheel', (event) => {
      if (!enabled() || event.ctrlKey) return;
      const delta = event.deltaMode === 1 ? event.deltaY * 32 : event.deltaY;
      if (!delta || !inZone(delta)) return;
      // Resting on the next page and pushing further down: hand over to native scrolling.
      if (delta > 0 && !active && window.scrollY >= edge() - 1) return;
      event.preventDefault();
      begin();
      feed(delta);
    }, { passive: false });

    window.addEventListener('touchstart', (event) => {
      touch = event.touches.length === 1 ? { y: event.touches[0].clientY, live: false } : null;
    }, { passive: true });
    window.addEventListener('touchmove', (event) => {
      if (!touch || !enabled()) return;
      const y = event.touches[0].clientY;
      const delta = touch.y - y;
      if (!touch.live) {
        if (!delta || !inZone(delta)) return;
        touch.live = true;
        begin();
      }
      event.preventDefault();
      touch.y = y;
      feed(delta / DRAG);
    }, { passive: false });
    window.addEventListener('touchend', () => {
      // Lifting the finger ends the gesture now rather than after the idle gap.
      const wasLive = touch && touch.live;
      touch = null;
      if (wasLive) {
        lastInput = 0;
        if (!committed) v = inputVelocity * .5;
      }
    }, { passive: true });

    window.addEventListener('keydown', (event) => {
      if (!enabled() || event.defaultPrevented) return;
      if (event.target.closest && event.target.closest('input,textarea,select,[contenteditable]')) return;
      const down = ['ArrowDown', 'PageDown', ' '].includes(event.key) && !event.shiftKey;
      const up = ['ArrowUp', 'PageUp'].includes(event.key) || (event.key === ' ' && event.shiftKey);
      if (!down && !up) return;
      const direction = down ? 1 : -1;
      if (!inZone(direction)) return;
      if (down && !active && window.scrollY >= edge() - 1) return;
      event.preventDefault();
      begin();
      inputVelocity = direction * 900;
      commit(direction);
    });
  }

  function init() {
    setPageUtilities();
    initNavigation();
    finishOpening = playOpening();
    initAmbientScene();
    if (document.body.classList.contains('home-page')) initHeroSnap();
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
