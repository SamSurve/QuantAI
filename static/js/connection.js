/**
 * QuantAI Connection Health, Endpoint Settings & Recent Activity Tracker
 *
 * Strict SSRF boundary:
 * - analysts-ledger-agentos-url is stored ONLY in browser localStorage.
 * - Used strictly by browser JavaScript for client-side health checks and AgentOS runs.
 * - Python server research remains completely in-process.
 */

(function () {
  'use strict';

  var STORAGE_KEY = 'analysts-ledger-agentos-url';
  var ACTIVITY_KEY = 'analysts-ledger-activity';
  var DEFAULT_API_URL = '/api';

  var indicator = document.getElementById('connection-indicator');
  var statusText = document.getElementById('connection-status-text');
  var dot = document.getElementById('connection-dot');
  var refreshBtn = document.getElementById('connection-refresh-btn');
  var settingsBtn = document.getElementById('connection-settings-btn');
  var dialog = document.getElementById('endpoint-settings-dialog');
  var urlInput = document.getElementById('endpoint-url-input');
  var cancelBtn = document.getElementById('endpoint-cancel-btn');
  var closeBtn = document.getElementById('endpoint-close-btn');
  var saveBtn = document.getElementById('endpoint-save-btn');
  var activityList = document.getElementById('recent-activity-list');

  function normalizeApiUrl(value) {
    if (!value) return DEFAULT_API_URL;
    var trimmed = String(value).trim().replace(/\/+$/, '');
    if (!trimmed || trimmed === '/agentos') return DEFAULT_API_URL;
    return trimmed;
  }

  function getAgentosUrl() {
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      return normalizeApiUrl(saved || DEFAULT_API_URL);
    } catch (_) {
      return DEFAULT_API_URL;
    }
  }

  function saveAgentosUrl(value) {
    var normalized = normalizeApiUrl(value);
    try {
      localStorage.setItem(STORAGE_KEY, normalized);
    } catch (_) {}
    return normalized;
  }

  function setConnectionStatus(status) {
    if (!indicator) return;
    var norm = String(status || '').toLowerCase();
    indicator.setAttribute('data-status', norm);

    if (norm === 'ready') {
      if (statusText) statusText.textContent = 'Ready';
      if (dot) dot.style.background = 'var(--up, #10b981)';
    } else if (norm === 'checking') {
      if (statusText) statusText.textContent = 'Checking';
      if (dot) dot.style.background = 'var(--warn, #f59e0b)';
    } else {
      if (statusText) statusText.textContent = 'Offline';
      if (dot) dot.style.background = 'var(--down, #ef4444)';
    }
  }

  async function verifyConnection(apiUrl) {
    var targetUrl = apiUrl || getAgentosUrl();
    setConnectionStatus('checking');

    try {
      var res = await fetch(targetUrl + '/agents', {
        headers: { Accept: 'application/json' },
      });
      if (res.ok) {
        setConnectionStatus('ready');
      } else {
        setConnectionStatus('offline');
      }
    } catch (_) {
      setConnectionStatus('offline');
    }
  }

  function openSettingsDialog() {
    if (!dialog) return;
    if (urlInput) urlInput.value = getAgentosUrl();
    dialog.style.display = 'grid';
    dialog.setAttribute('aria-hidden', 'false');
    if (urlInput) urlInput.focus();
  }

  function closeSettingsDialog() {
    if (!dialog) return;
    dialog.style.display = 'none';
    dialog.setAttribute('aria-hidden', 'true');
    if (settingsBtn) settingsBtn.focus();
  }

  // Activity Tracker
  function getRecentActivity() {
    try {
      var raw = sessionStorage.getItem(ACTIVITY_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (_) {
      return [];
    }
  }

  function saveRecentActivity(list) {
    try {
      sessionStorage.setItem(ACTIVITY_KEY, JSON.stringify(list));
    } catch (_) {}
  }

  function renderActivityList(items) {
    if (!activityList) return;
    if (!items || items.length === 0) {
      activityList.innerHTML = '<li id="recent-activity-empty"><p class="muted" style="font-size:13px;line-height:1.4;margin:0">Research activity appears after a returned request.</p></li>';
      return;
    }

    var html = '';
    for (var i = 0; i < Math.min(items.length, 5); i++) {
      var it = items[i];
      var conf = it.confidence ? ' · ' + it.confidence : '';
      html += '<li style="border-bottom:1px solid var(--line);padding-bottom:8px">' +
        '<p style="font-size:14px;font-weight:600;color:var(--text);margin:0">' + (it.query || '') + '</p>' +
        '<p class="muted" style="font-size:12px;margin:2px 0 0">' + (it.type || 'Research') + ' · ' + (it.status || 'completed') + conf + '</p>' +
        '</li>';
    }
    activityList.innerHTML = html;
  }

  function recordActivity(query, mode, status, confidence) {
    var current = getRecentActivity();
    var q = (query || '').trim();
    if (!q) return;

    // Deduplicate consecutive identical submissions
    if (current.length > 0 && current[0].query && current[0].query.toLowerCase() === q.toLowerCase()) {
      current[0].status = status || current[0].status || 'completed';
      current[0].confidence = confidence || current[0].confidence || 'high';
      saveRecentActivity(current);
      renderActivityList(current);
      return;
    }

    var newItem = {
      id: 'act-' + Date.now(),
      query: q,
      type: (mode || 'Market Intelligence').replace('_', ' '),
      status: status || 'completed',
      confidence: confidence || 'high',
    };
    var updated = [newItem].concat(current).slice(0, 5);
    saveRecentActivity(updated);
    renderActivityList(updated);
  }

  // Expose global methods for page integration
  window.QuantAIConnection = {
    verifyConnection: verifyConnection,
    getAgentosUrl: getAgentosUrl,
    saveAgentosUrl: saveAgentosUrl,
    recordActivity: recordActivity,
    getRecentActivity: getRecentActivity,
  };

  // Event Listeners
  if (refreshBtn) {
    refreshBtn.addEventListener('click', function () {
      verifyConnection();
    });
  }

  if (settingsBtn) {
    settingsBtn.addEventListener('click', function () {
      openSettingsDialog();
    });
  }

  if (cancelBtn) {
    cancelBtn.addEventListener('click', closeSettingsDialog);
  }

  if (closeBtn) {
    closeBtn.addEventListener('click', closeSettingsDialog);
  }

  if (saveBtn) {
    saveBtn.addEventListener('click', function () {
      if (urlInput) {
        var saved = saveAgentosUrl(urlInput.value);
        closeSettingsDialog();
        verifyConnection(saved);
      }
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && dialog && dialog.style.display !== 'none') {
      closeSettingsDialog();
    }
  });

  // Track search queries submitted in search-form
  var searchForm = document.getElementById('search-form');
  if (searchForm) {
    searchForm.addEventListener('submit', function () {
      var searchInput = document.getElementById('search-input');
      if (searchInput && searchInput.value.trim()) {
        recordActivity(searchInput.value.trim(), 'Market Intelligence', 'completed', 'high');
      }
    });
  }

  // Initial setup
  renderActivityList(getRecentActivity());
  verifyConnection();
})();
