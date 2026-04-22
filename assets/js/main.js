(function () {
  const path = window.location.pathname.replace(/\/+/g, '/');
  document.querySelectorAll('.nav-links a').forEach((link) => {
    const href = link.getAttribute('href');
    if (!href) return;
    const normalized = href.endsWith('/') ? href : href + '/';
    if (path === href || path === normalized || (href === '/' && path === '/')) {
      link.classList.add('active');
    }
  });

  const year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();

  const isHomePage = document.body.classList.contains('home-page');
  if (!isHomePage) return;

  const revealOnScrollY = 48;
  const hideOnScrollY = 18;
  let revealed = false;
  let rafId = 0;

  const updateHomeReveal = () => {
    rafId = 0;
    const y = window.scrollY || window.pageYOffset || 0;

    if (!revealed && y > revealOnScrollY) {
      revealed = true;
    }

    if (revealed && y <= hideOnScrollY) {
      revealed = false;
    }

    document.body.style.setProperty('--home-reveal', revealed ? '1' : '0');
    document.body.classList.toggle('home-revealed', revealed);
  };

  const requestHomeRevealUpdate = () => {
    if (rafId) return;
    rafId = window.requestAnimationFrame(updateHomeReveal);
  };

  window.addEventListener('scroll', requestHomeRevealUpdate, { passive: true });
  window.addEventListener('resize', requestHomeRevealUpdate);
  requestHomeRevealUpdate();
})();
