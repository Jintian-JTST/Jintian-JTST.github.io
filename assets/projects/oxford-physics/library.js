(() => {
  'use strict';
  const list = document.querySelector('.resource-list');
  if (!list) return;
  const resources = [...list.querySelectorAll('.resource')];
  const tabs = [...document.querySelectorAll('[data-category]')];
  const search = document.getElementById('library-search');
  const course = document.getElementById('filter-course');
  const type = document.getElementById('filter-type');
  const year = document.getElementById('filter-year');
  const form = document.getElementById('library-filter-form');
  const more = document.getElementById('library-more');
  const count = document.getElementById('result-count');
  let category = 'all';
  let limit = 40;
  const labels = {all: '全部资料', year1: '大一', year2: '大二', other: '其他课程', exams: '历年考试', mine: '我的解答', lab: '实验与代码'};
  const params = new URLSearchParams(location.search);
  if (Object.hasOwn(labels, params.get('category'))) category = params.get('category');
  search.value = params.get('q') || '';
  [course, type, year].forEach(select => {
    const value = params.get(select.id.replace('filter-', ''));
    if ([...select.options].some(option => option.value === value)) select.value = value;
  });
  function render(updateUrl = true) {
    const tokens = search.value.trim().toLocaleLowerCase().split(/\s+/u).filter(Boolean);
    const matches = resources.filter(item =>
      (category === 'all' || item.dataset.groups.split(' ').includes(category)) &&
      (!course.value || item.dataset.courses.split('|').includes(course.value)) &&
      (!type.value || item.dataset.type === type.value) &&
      (!year.value || item.dataset.examYear === year.value) &&
      tokens.every(token => item.dataset.search.includes(token)));
    const visible = new Set(matches.slice(0, limit));
    resources.forEach(item => { item.hidden = !visible.has(item); });
    tabs.forEach(tab => {
      const active = tab.dataset.category === category;
      tab.classList.toggle('is-active', active);
      tab.setAttribute('aria-pressed', String(active));
    });
    document.getElementById('results-title').textContent = labels[category];
    count.textContent = matches.length > limit ? `${matches.length} 份资料 · 已显示 ${limit} 份` : `${matches.length} 份资料`;
    document.getElementById('library-empty').hidden = matches.length !== 0;
    more.hidden = matches.length <= limit;
    more.textContent = `显示更多资料 · 还有 ${Math.max(0, matches.length - limit)} 份`;
    if (updateUrl) {
      const query = new URLSearchParams();
      if (category !== 'all') query.set('category', category);
      if (search.value.trim()) query.set('q', search.value.trim());
      if (course.value) query.set('course', course.value);
      if (type.value) query.set('type', type.value);
      if (year.value) query.set('year', year.value);
      history.replaceState(null, '', location.pathname + (query.size ? `?${query}` : '') + location.hash);
    }
  }
  function reset() {
    category = 'all'; search.value = ''; course.value = ''; type.value = ''; year.value = ''; limit = 40; render();
  }
  tabs.forEach(tab => tab.addEventListener('click', () => { category = tab.dataset.category; limit = 40; render(); }));
  search.addEventListener('input', () => { limit = 40; render(); });
  [course, type, year].forEach(select => select.addEventListener('change', () => { limit = 40; render(); }));
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('reset', event => { event.preventDefault(); reset(); });
  document.getElementById('empty-reset').addEventListener('click', () => { reset(); search.focus(); });
  more.addEventListener('click', () => {
    const oldLimit = limit;
    limit += 40; render();
    const next = resources.filter(item => !item.hidden)[oldLimit];
    next?.querySelector('h3 a')?.focus({preventScroll: true});
  });
  document.addEventListener('keydown', event => {
    if (event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey &&
        !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName) && !document.activeElement.isContentEditable) {
      event.preventDefault(); search.focus();
    }
  });
  render(false);
  form.hidden = false;
  document.getElementById('library-controls').hidden = false;
})();
