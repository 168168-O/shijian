(() => {
  'use strict';

  const storageKey = 'shijian.ui-theme.v1';
  const themes = [
    { id: 'midnight', label: '午夜星云' },
    { id: 'pearl', label: '冰晶珍珠' },
    { id: 'jade', label: '翡翠深海' },
    { id: 'rose', label: '玫瑰暮色' }
  ];

  const root = document.documentElement;
  let selected = 'midnight';

  try {
    const saved = localStorage.getItem(storageKey);
    if (themes.some(x => x.id === saved)) selected = saved;
  } catch (_) {
    // Session-only fallback if storage is unavailable.
  }

  root.dataset.uiTheme = selected;

  function mountSwitcher() {
    if (document.querySelector('.ui-theme-switcher')) return;

    const nav = document.createElement('nav');
    nav.className = 'ui-theme-switcher';
    nav.setAttribute('aria-label', '界面主题');
    nav.title = '切换界面主题';

    const sr = document.createElement('span');
    sr.className = 'sr-only';
    sr.textContent = '选择界面主题';
    nav.appendChild(sr);

    themes.forEach(theme => {
      const button = document.createElement('button');
      button.type = 'button';
      button.dataset.theme = theme.id;
      button.title = theme.label;
      button.setAttribute('aria-label', `切换到${theme.label}`);
      button.setAttribute('aria-pressed', String(theme.id === selected));

      button.addEventListener('click', () => {
        selected = theme.id;
        root.dataset.uiTheme = selected;
        try {
          localStorage.setItem(storageKey, selected);
        } catch (_) {}

        nav.querySelectorAll('button').forEach(item => {
          item.setAttribute('aria-pressed', String(item === button));
        });
      });

      nav.appendChild(button);
    });

    document.body.appendChild(nav);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mountSwitcher, { once: true });
  } else {
    mountSwitcher();
  }
})();
