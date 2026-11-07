/**
 * QuantAI Application Controller
 * Startup Reveal, Reduced Motion, Toast Notifications, Keyboard Accessibility & Error Recovery
 */

(function () {
  'use strict';

  // --- 1. Startup Reveal (1.2s timing & reduced-motion support) ---
  (function () {
    var revealEl = document.getElementById('startup-reveal');
    if (!revealEl) return;

    var prefersReduced = false;
    try {
      prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    } catch (_) {}

    var duration = prefersReduced ? 0 : 1180;

    if (duration === 0) {
      revealEl.style.display = 'none';
    } else {
      setTimeout(function () {
        revealEl.style.opacity = '0';
        setTimeout(function () {
          revealEl.style.display = 'none';
        }, 250);
      }, duration);
    }
  })();

  // --- 2. Error Recovery & Reload Action ---
  document.addEventListener('click', function (e) {
    var reloadTrigger = e.target.closest('[data-action="reload-page"], #reload-page-btn, .reload-action-btn');
    if (reloadTrigger) {
      e.preventDefault();
      window.location.reload();
    }
  });

  // --- 3. Toast Notifications System ---
  function showToast(message, type, durationMs) {
    var container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.setAttribute('aria-live', 'polite');
      container.style.cssText = 'position:fixed;bottom:24px;left:24px;z-index:9990;display:flex;flex-direction:column;gap:8px;pointer-events:none';
      document.body.appendChild(container);
    }

    var toast = document.createElement('div');
    toast.className = 'toast toast--' + (type || 'info');
    toast.setAttribute('role', 'status');
    toast.style.cssText = 'pointer-events:auto;background:var(--card, #fff);color:var(--text, #111);border:1px solid var(--line, #ddd);box-shadow:0 8px 24px rgba(0,0,0,0.15);border-radius:12px;padding:12px 18px;font-size:14px;font-weight:500;display:flex;align-items:center;gap:10px;transition:opacity .2s,transform .2s;opacity:0;transform:translateY(8px)';

    if (type === 'error') {
      toast.style.borderLeft = '4px solid var(--down, #ef4444)';
    } else if (type === 'success') {
      toast.style.borderLeft = '4px solid var(--up, #10b981)';
    } else {
      toast.style.borderLeft = '4px solid var(--brand, #2563eb)';
    }

    toast.textContent = message;
    container.appendChild(toast);

    // Animate in
    requestAnimationFrame(function () {
      toast.style.opacity = '1';
      toast.style.transform = 'translateY(0)';
    });

    // Auto dismiss
    var dismissTimer = setTimeout(function () {
      dismissToast(toast);
    }, durationMs || 4000);

    toast.addEventListener('click', function () {
      clearTimeout(dismissTimer);
      dismissToast(toast);
    });
  }

  function dismissToast(toast) {
    if (!toast || !toast.parentNode) return;
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(8px)';
    setTimeout(function () {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 200);
  }

  window.showToast = showToast;

  // --- 4. Modal Dialog Focus Management & Accessibility ---
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      var openModals = document.querySelectorAll('[role="dialog"][aria-modal="true"]');
      openModals.forEach(function (dlg) {
        if (dlg.style.display !== 'none' && !dlg.hidden) {
          var closeBtn = dlg.querySelector('[aria-label*="Close"], #endpoint-close-btn, #endpoint-cancel-btn');
          if (closeBtn) closeBtn.click();
        }
      });
    }
  });
})();
