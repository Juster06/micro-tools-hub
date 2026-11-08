(() => {
  'use strict';
  const search = document.getElementById('toolSearch');
  const select = document.getElementById('category-select');
  const cards = [...document.querySelectorAll('#toolGrid .tool-card')];
  const groups = [...document.querySelectorAll('[data-group]')];
  const buttons = [...document.querySelectorAll('[data-category-filter]')];
  const count = document.getElementById('resultCount');
  const menu = document.getElementById('menu');
  const nav = document.getElementById('site-nav');
  let category = 'all', announcement;
  const normalize = value => value.toLocaleLowerCase('en').trim().replace(/\s+/g, ' ');
  function filter(immediate = false) {
    const terms = normalize(search.value).split(' ').filter(Boolean);
    let visible = 0;
    for (const card of cards) {
      const haystack = normalize(card.dataset.search);
      card.hidden = (category !== 'all' && card.dataset.category !== category) || !terms.every(term => haystack.includes(term));
      if (!card.hidden) visible++;
    }
    groups.forEach(group => { group.hidden = ![...group.querySelectorAll('.tool-card')].some(card => !card.hidden); });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.categoryFilter === category)));
    select.value = category;
    document.getElementById('empty').hidden = visible !== 0;
    clearTimeout(announcement);
    const announce = () => { count.textContent = terms.length || category !== 'all' ? `${visible} of ${cards.length} tools match` : `${cards.length} tools ready to use`; };
    if (immediate) announce(); else announcement = setTimeout(announce, 150);
  }
  function reset() { search.value = ''; category = 'all'; filter(true); search.focus(); }
  function closeMenu(restore = false) { menu.setAttribute('aria-expanded', 'false'); nav.classList.remove('open'); if (restore) menu.focus(); }
  search.addEventListener('input', () => filter());
  document.getElementById('clear-search').addEventListener('click', reset);
  document.getElementById('reset-results').addEventListener('click', reset);
  buttons.forEach(button => button.addEventListener('click', () => { category = button.dataset.categoryFilter; filter(true); }));
  select.addEventListener('change', () => { category = select.value; filter(true); });
  document.querySelectorAll('[data-category-jump]').forEach(link => link.addEventListener('click', () => { search.value = ''; category = 'all'; filter(true); }));
  menu.addEventListener('click', () => { const open = menu.getAttribute('aria-expanded') !== 'true'; menu.setAttribute('aria-expanded', String(open)); nav.classList.toggle('open', open); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { event.preventDefault(); closeMenu(true); } });
  nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    if (link.hash) { search.value = ''; category = 'all'; filter(true); closeMenu(); document.querySelector(link.hash)?.focus(); }
  }));
  matchMedia('(min-width:640px)').addEventListener('change', () => { const inside = nav.contains(document.activeElement); closeMenu(inside && matchMedia('(max-width:639px)').matches); });
  document.documentElement.classList.add('js');
})();
