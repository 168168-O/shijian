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
    if (themes.some(theme => theme.id === saved)) selected = saved;
  } catch (_) {
    // Keep the selected palette for this page session when storage is disabled.
  }
  root.dataset.uiTheme = selected;

  function mountSwitcher() {
    if (!document.body || document.querySelector('.ui-theme-switcher')) return;

    // Remove the inline legacy five-color switcher so users only see one palette.
    document.querySelectorAll('.themebad').forEach(element => element.remove());

    const palette = document.createElement('nav');
    palette.className = 'ui-theme-switcher';
    palette.setAttribute('aria-label', '界面主题');
    palette.title = '切换界面主题';

    const hiddenLabel = document.createElement('span');
    hiddenLabel.className = 'sr-only';
    hiddenLabel.textContent = '选择界面主题';
    palette.appendChild(hiddenLabel);

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
        try { localStorage.setItem(storageKey, selected); } catch (_) {}
        palette.querySelectorAll('button').forEach(item => {
          item.setAttribute('aria-pressed', String(item === button));
        });
      });
      palette.appendChild(button);
    });

    document.body.appendChild(palette);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mountSwitcher, { once: true });
  } else {
    mountSwitcher();
  }
})();
