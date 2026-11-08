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
  let category = 'all';
  const normalize = value => value.toLocaleLowerCase('en').trim().replace(/\s+/g, ' ');
  function filter() {
    const query = normalize(search.value);
    let visible = 0;
    for (const card of cards) {
      const haystack = normalize(card.dataset.search);
      card.hidden = (category !== 'all' && card.dataset.category !== category) || !haystack.includes(query);
      if (!card.hidden) visible++;
    }
    groups.forEach(group => { group.hidden = ![...group.querySelectorAll('.tool-card')].some(card => !card.hidden); });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.categoryFilter === category)));
    select.value = category;
    document.getElementById('empty').hidden = visible !== 0;
    count.textContent = query || category !== 'all' ? `${visible} of ${cards.length} tools match` : `${cards.length} tools ready to use`;
  }
  function reset() { search.value = ''; category = 'all'; filter(); search.focus(); }
  function closeMenu(restore = false) { menu.setAttribute('aria-expanded', 'false'); nav.classList.remove('open'); if (restore) menu.focus(); }
  search.addEventListener('input', () => filter());
  document.getElementById('clearSearch').addEventListener('click', reset);
  document.getElementById('reset-results').addEventListener('click', reset);
  buttons.forEach(button => button.addEventListener('click', () => { category = button.dataset.categoryFilter; filter(); }));
  select.addEventListener('change', () => { category = select.value; filter(); });
  document.querySelectorAll('[data-category-jump]').forEach(link => link.addEventListener('click', () => { search.value = ''; category = 'all'; filter(); }));
  menu.addEventListener('click', () => { const open = menu.getAttribute('aria-expanded') !== 'true'; menu.setAttribute('aria-expanded', String(open)); nav.classList.toggle('open', open); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { event.preventDefault(); closeMenu(true); } });
  nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    if (link.hash) { search.value = ''; category = 'all'; filter(); closeMenu(); document.querySelector(link.hash)?.focus(); }
  }));
  matchMedia('(min-width:640px)').addEventListener('change', () => { const inside = nav.contains(document.activeElement); closeMenu(inside && matchMedia('(max-width:639px)').matches); });
  document.documentElement.classList.add('js');
})();
