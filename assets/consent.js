(() => {
  'use strict';
  const TAG = 'G-XDHPQYJ5CH';
  const KEY = 'edb.analytics-consent.v1';
  const MAX_AGE = 180 * 24 * 60 * 60 * 1000;
  const script = document.currentScript;
  const root = new URL('../', script.src);
  const policy = new URL('privacy.html', root).href;
  let choice = null, tagLoaded = false, pageViewSent = false, tagNode = null, generation = 0;
  window['ga-disable-' + TAG] = true;

  function readChoice() {
    try {
      const raw = localStorage.getItem(KEY);
      if (!raw) return null;
      let data;
      try { data = JSON.parse(raw); } catch { localStorage.removeItem(KEY); return null; }
      if (!data || data.version !== 1 || !['accepted', 'rejected'].includes(data.choice) || !Number.isFinite(data.time) || data.time > Date.now() || Date.now() - data.time > MAX_AGE) { localStorage.removeItem(KEY); return null; }
      return data.choice;
    } catch { return null; }
  }
  function saveChoice(value) {
    try { localStorage.setItem(KEY, JSON.stringify({version: 1, choice: value, time: Date.now()})); return true; }
    catch { return false; }
  }
  function expireAnalyticsCookies() {
    const domains = ['', location.hostname, '.' + location.hostname.replace(/^www\./, '')];
    let cookies;
    try { cookies = document.cookie; } catch { return; }
    for (const part of cookies.split(';')) {
      const name = part.trim().split('=')[0];
      if (!/^_ga(?:_|$)/.test(name)) continue;
      for (const domain of domains) {
        try { document.cookie = name + '=; Max-Age=0; Path=/; SameSite=Lax' + (location.protocol === 'https:' ? '; Secure' : '') + (domain ? '; Domain=' + domain : ''); } catch { /* Cookie access may be blocked. */ }
      }
    }
  }
  function disableAnalytics() {
    generation++;
    window['ga-disable-' + TAG] = true;
    if (tagNode) { tagNode.remove(); tagNode = null; }
    expireAnalyticsCookies();
  }
  function initializeAnalytics() {
    if (choice !== 'accepted') return;
    window['ga-disable-' + TAG] = false;
    if (tagLoaded || tagNode) return;
    const token = ++generation;
    const node = document.createElement('script');
    node.async = true;
    node.src = 'https://www.googletagmanager.com/gtag/js?id=' + TAG;
    tagNode = node;
    node.onload = () => {
      if (choice !== 'accepted' || token !== generation) return;
      tagLoaded = true;
      window.dataLayer = window.dataLayer || [];
      window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
      window.gtag('consent', 'default', {analytics_storage:'denied', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
      window.gtag('consent', 'update', {analytics_storage:'granted', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
      window.gtag('js', new Date());
      window.gtag('config', TAG, {send_page_view:false, allow_google_signals:false, allow_ad_personalization_signals:false, page_location:location.origin + location.pathname, page_referrer:''});
      if (!pageViewSent) {
        pageViewSent = true;
        window.gtag('event', 'page_view', {send_to:TAG, page_location:location.origin + location.pathname, page_referrer:''});
      }
    };
    node.onerror = () => { if (token === generation) { tagNode = null; announce('Analytics could not load. The tools still work.'); } };
    document.head.append(node);
  }
  function announce(message) { const status = document.getElementById('edb-consent-status'); if (status) status.textContent = message; }
  function decide(value) {
    choice = value;
    const saved = saveChoice(value);
    if (value === 'accepted') initializeAnalytics(); else disableAnalytics();
    document.getElementById('edb-consent-panel').hidden = true;
    const button = document.getElementById('edb-consent-settings'); button.hidden = false; button.focus();
    announce((value === 'accepted' ? 'Analytics accepted.' : 'Analytics rejected.') + (saved ? '' : ' This browser could not save your choice; it applies only to this page.'));
  }
  function mount() {
    if (document.getElementById('edb-consent-root')) return;
    const style = document.createElement('style');
    style.textContent = '#edb-consent-root{font:16px/1.5 system-ui,sans-serif;color:#e2e8f0}#edb-consent-root [hidden]{display:none!important}#edb-consent-panel{position:fixed;z-index:2147483000;inset:auto 1rem 1rem;max-width:52rem;margin:auto;background:#0f172a;border:1px solid #818cf8;border-radius:.75rem;padding:1rem;box-shadow:0 10px 30px #0009}#edb-consent-panel p{margin:.25rem 0 .75rem}#edb-consent-actions{display:flex;flex-wrap:wrap;gap:.65rem}#edb-consent-root button{font:inherit;font-weight:600;color:#fff;background:#3730a3;border:2px solid #a5b4fc;border-radius:.5rem;padding:.55rem .9rem;cursor:pointer}#edb-consent-root button:focus-visible,#edb-consent-root a:focus-visible{outline:3px solid #facc15;outline-offset:3px}#edb-consent-root a{color:#c7d2fe;text-decoration:underline}#edb-consent-settings{position:fixed;z-index:2147483000;bottom:.75rem;left:.75rem}#edb-consent-status{position:fixed;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}';
    document.head.append(style);
    const host = document.createElement('div'); host.id = 'edb-consent-root';
    const panel = document.createElement('section'); panel.id = 'edb-consent-panel'; panel.setAttribute('aria-labelledby','edb-consent-title'); panel.setAttribute('aria-describedby','edb-consent-description');
    const title = document.createElement('h2'); title.id = 'edb-consent-title'; title.textContent = 'Analytics preferences';
    const description = document.createElement('p'); description.id = 'edb-consent-description'; description.textContent = 'We use optional Google Analytics to understand page visits. Your tool inputs stay in your browser. Choose whether to allow analytics; the tools work either way. ';
    const link = document.createElement('a'); link.href = policy; link.textContent = 'Privacy and cookies'; description.append(link);
    const actions = document.createElement('div'); actions.id = 'edb-consent-actions';
    const accept = document.createElement('button'); accept.type = 'button'; accept.id = 'edb-consent-accept'; accept.textContent = 'Accept analytics'; accept.addEventListener('click', () => decide('accepted'));
    const reject = document.createElement('button'); reject.type = 'button'; reject.id = 'edb-consent-reject'; reject.textContent = 'Reject analytics'; reject.addEventListener('click', () => decide('rejected'));
    actions.append(accept, reject); panel.append(title, description, actions);
    const settings = document.createElement('button'); settings.type = 'button'; settings.id = 'edb-consent-settings'; settings.textContent = 'Privacy settings'; settings.hidden = true; settings.addEventListener('click', () => { panel.hidden = false; settings.hidden = true; accept.focus(); });
    const status = document.createElement('p'); status.id = 'edb-consent-status'; status.setAttribute('role','status'); status.setAttribute('aria-live','polite');
    host.append(panel, settings, status); document.body.append(host);
    choice = readChoice();
    if (choice) { panel.hidden = true; settings.hidden = false; if (choice === 'accepted') initializeAnalytics(); }
  }
  window.addEventListener('storage', e => {
    if (e.key !== KEY && e.key !== null) return;
    const newChoice = readChoice();
    if (newChoice !== 'accepted') { choice = newChoice; disableAnalytics(); }
    else { choice = newChoice; initializeAnalytics(); }
    const panel = document.getElementById('edb-consent-panel'), settings = document.getElementById('edb-consent-settings');
    if (panel && settings) { panel.hidden = !!newChoice; settings.hidden = !newChoice; }
  });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, {once:true}); else mount();
})();
