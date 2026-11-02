/**
 * QuantAI Company Search & Quick-Search Controller
 * Handles query normalization, IME composition protection, and quick-action shortcuts.
 */

(function () {
  'use strict';

  var isComposing = false;
  var timer1 = null;
  var timer2 = null;

  function initSearch() {
    var form = document.getElementById('search-form');
    var input = document.getElementById('search-input');
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

    // Form submission validation
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
    });

    // Quick search shortcut buttons
    document.addEventListener('click', function (e) {
      var chip = e.target.closest('[data-quick-search]');
      if (chip) {
        e.preventDefault();
        var symbol = chip.getAttribute('data-quick-search');
        if (symbol) {
          input.value = symbol.trim();
          form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
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
