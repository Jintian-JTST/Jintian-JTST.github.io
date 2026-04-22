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
})();
