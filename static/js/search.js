/**
 * QuantAI Company Search, Interactive Disambiguation & Quick-Search Controller
 * Handles query normalization, IME composition protection, candidate selection, and keyboard actions.
 */

(function () {
  'use strict';

  var isComposing = false;
  var timer1 = null;
  var timer2 = null;

  function initSearch() {
    var form = document.getElementById('search-form');
    var input = document.getElementById('search-input');
    var button = document.getElementById('search-button');
    if (!form || !input) return;

    // IME composition events
    input.addEventListener('compositionstart', function () {
      if (timer1) clearTimeout(timer1);
      if (timer2) clearTimeout(timer2);
      isComposing = true;
    });

    input.addEventListener('compositionend', function () {
      // Use double setTimeout for Safari compatibility
      timer1 = setTimeout(function () {
        timer2 = setTimeout(function () {
          isComposing = false;
        }, 0);
      }, 0);
    });

    // Prevent premature submit when completing an IME composition with Enter
    input.addEventListener('keydown', function (e) {
      if (isComposing && (e.key === 'Enter' || e.key === 'Escape')) {
        e.stopPropagation();
        if (e.key === 'Enter') {
          e.preventDefault();
        }
      }
    });

    // Form submission validation & loading feedback
    form.addEventListener('submit', function (e) {
      if (isComposing) {
        e.preventDefault();
        return;
      }
      var query = input.value.trim();
      if (!query) {
        e.preventDefault();
        input.focus();
        return;
      }
      input.value = query;

      // Provide immediate loading state
      if (button && !button.disabled) {
        button.disabled = true;
        button.style.opacity = '0.75';
        button.style.cursor = 'wait';
        var originalText = button.textContent;
        button.innerHTML = '<span style="display:inline-flex;align-items:center;gap:6px"><span style="width:12px;height:12px;border:2px solid #fff;border-top-color:transparent;border-radius:50%;display:inline-block;animation:spin 1s linear infinite"></span><span>Researching…</span></span>';
      }
    });

    // Quick search shortcut buttons & Interactive Disambiguation card selection
    document.addEventListener('click', function (e) {
      // Quick search starter chips (AAPL, MSFT, etc.)
      var chip = e.target.closest('[data-quick-search]');
      if (chip) {
        e.preventDefault();
        var symbol = chip.getAttribute('data-quick-search');
        if (symbol) {
          input.value = symbol.trim();
          if (typeof form.requestSubmit === 'function') {
            form.requestSubmit();
          } else {
            form.submit();
          }
        }
        return;
      }

      // Candidate disambiguation card or selection button click
      var disambigTarget = e.target.closest('[data-select-ticker]');
      if (disambigTarget) {
        e.preventDefault();
        var ticker = disambigTarget.getAttribute('data-select-ticker');
        if (ticker) {
          input.value = ticker.trim();
          if (typeof form.requestSubmit === 'function') {
            form.requestSubmit();
          } else {
            form.submit();
          }
        }
      }
    });

    // Accessible keyboard selection on disambiguation cards
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        var activeEl = document.activeElement;
        if (activeEl && activeEl.matches && activeEl.matches('.disambiguation-card[data-select-ticker]')) {
          e.preventDefault();
          var ticker = activeEl.getAttribute('data-select-ticker');
          if (ticker) {
            input.value = ticker.trim();
            if (typeof form.requestSubmit === 'function') {
              form.requestSubmit();
            } else {
              form.submit();
            }
          }
        }
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSearch);
  } else {
    initSearch();
  }

  window.QuantAISearch = {
    isComposing: function () {
      return isComposing;
    },
  };
})();
