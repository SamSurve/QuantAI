/**
 * QuantAI Persistent Three-Mode Theme System
 * Supports Light, Dark, and System modes with instant client-side updates.
 * Key: quantai-theme in localStorage.
 * No server requests, no page reload.
 */

(function () {
  'use strict';

  var STORAGE_KEY = 'quantai-theme';
  var media = window.matchMedia('(prefers-color-scheme: dark)');

  function getStoredTheme() {
    try {
      var val = localStorage.getItem(STORAGE_KEY);
      if (val === 'light' || val === 'dark' || val === 'system') {
        return val;
      }
    } catch (_) {}
    return 'system';
  }

  function resolveTheme(preference) {
    if (preference === 'dark') return 'dark';
    if (preference === 'light') return 'light';
    return media.matches ? 'dark' : 'light';
  }

  function applyTheme(preference) {
    var resolved = resolveTheme(preference);

    document.documentElement.classList.toggle('dark', resolved === 'dark');
    document.documentElement.dataset.theme = resolved;
    document.documentElement.style.colorScheme = resolved;

    try {
      localStorage.setItem(STORAGE_KEY, preference);
    } catch (_) {}

    var buttons = document.querySelectorAll('[data-theme-value]');
    for (var i = 0; i < buttons.length; i++) {
      var btn = buttons[i];
      var isCurrent = btn.dataset.themeValue === preference;
      btn.classList.toggle('on', isCurrent);
      btn.setAttribute('aria-pressed', isCurrent ? 'true' : 'false');
    }
  }

  // Listen for OS theme preference changes when in 'system' mode
  try {
    media.addEventListener('change', function () {
      if (getStoredTheme() === 'system') {
        applyTheme('system');
      }
    });
  } catch (_) {
    // Legacy Safari fallback
    if (typeof media.addListener === 'function') {
      media.addListener(function () {
        if (getStoredTheme() === 'system') {
          applyTheme('system');
        }
      });
    }
  }

  // Click delegation for theme buttons
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-theme-value]');
    if (btn) {
      e.preventDefault();
      var selected = btn.dataset.themeValue;
      if (selected === 'light' || selected === 'dark' || selected === 'system') {
        applyTheme(selected);
      }
    }
  });

  // Initialize UI state on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      applyTheme(getStoredTheme());
    });
  } else {
    applyTheme(getStoredTheme());
  }

  window.QuantAITheme = {
    getTheme: getStoredTheme,
    setTheme: applyTheme,
    resolveTheme: resolveTheme,
  };
})();
