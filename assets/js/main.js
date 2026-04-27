(function () {
  // Set active navigation link
  function setActiveNavLink() {
    const path = window.location.pathname.replace(/\/+/g, '/');
    document.querySelectorAll('.nav-links a').forEach((link) => {
      const href = link.getAttribute('href');
      if (!href) return;
      const normalized = href.endsWith('/') ? href : href + '/';
      if (path === href || path === normalized || (href === '/' && path === '/')) {
        link.classList.add('active');
      }
    });
  }

  // Set current year for elements with data-year attribute
  function setCurrentYear() {
    const yearElement = document.querySelector('[data-year]');
    if (yearElement) {
      yearElement.textContent = new Date().getFullYear();
    }
  }

  // Initialize home page scroll reveal animation
  function initHomeReveal() {
    const isHomePage = document.body.classList.contains('home-page');
    if (!isHomePage) return;

    const maxRevealDistance = () => Math.max(window.innerHeight * 0.9, 520);
    let revealed = false;
    let rafId = 0;

    const updateHomeReveal = () => {
      rafId = 0;
      const y = window.scrollY || window.pageYOffset || 0;
      const reveal = Math.min(Math.max(y / maxRevealDistance(), 0), 1);
      revealed = reveal > 0.03;

      document.body.style.setProperty('--home-reveal', reveal.toFixed(4));
      document.body.classList.toggle('home-revealed', revealed);
    };

    const requestHomeRevealUpdate = () => {
      if (rafId) return;
      rafId = window.requestAnimationFrame(updateHomeReveal);
    };

    window.addEventListener('scroll', requestHomeRevealUpdate, { passive: true });
    window.addEventListener('resize', requestHomeRevealUpdate);
    requestHomeRevealUpdate(); // Initial call
  }

  // Execute functions on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', () => {
    setActiveNavLink();
    setCurrentYear();
    initHomeReveal();
  });

})();