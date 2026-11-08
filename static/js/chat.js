/**
 * QuantAI AgentOS Chat Client
 * Connects directly to same-origin /api/agents/groq-finance-agent/runs
 * Renders assistant responses via /api/chat/render
 * Provides compact floating launcher, multiline input, empty state chips, and session continuity
 */

(function () {
  'use strict';

  var AGENT_ID = 'groq-finance-agent';
  var RUNS_URL = '/api/agents/' + AGENT_ID + '/runs';
  var RENDER_URL = '/api/chat/render';
  var SESSION_KEY = 'quantai-chat-session-id';

  var toggleBtn = document.getElementById('chat-toggle');
  var drawer = document.getElementById('chat-drawer');
  var minimizeBtn = document.getElementById('chat-minimize');
  var closeBtn = document.getElementById('chat-close');
  var form = document.getElementById('chat-form');
  var input = document.getElementById('chat-input');
  var submitBtn = document.getElementById('chat-submit');
  var messagesContainer = document.getElementById('chat-messages');
  var turnCounter = document.getElementById('chat-turn-counter');
  var connectionDot = document.getElementById('chat-connection-dot');
  var connectionText = document.getElementById('chat-connection-text');

  if (!toggleBtn || !drawer) return;

  var turnCount = 0;
  var isLoading = false;
  var sessionId = getOrCreateSessionId();

  function getOrCreateSessionId() {
    try {
      var saved = sessionStorage.getItem(SESSION_KEY);
      if (saved) return saved;
      var newId = 'session-' + Date.now() + '-' + Math.random().toString(36).slice(2, 9);
      sessionStorage.setItem(SESSION_KEY, newId);
      return newId;
    } catch (_) {
      return 'session-' + Date.now();
    }
  }

  function isDrawerOpen() {
    return drawer.classList.contains('is-open') || drawer.style.display === 'flex';
  }

  function setDrawerOpen(open) {
    if (open) {
      drawer.style.display = 'flex';
      void drawer.offsetWidth; // Force reflow
      drawer.classList.add('is-open');
      drawer.setAttribute('aria-hidden', 'false');
      toggleBtn.setAttribute('aria-expanded', 'true');
      if (input) {
        input.focus();
      }
    } else {
      drawer.classList.remove('is-open');
      drawer.setAttribute('aria-hidden', 'true');
      toggleBtn.setAttribute('aria-expanded', 'false');
      drawer.style.display = 'none';
      if (toggleBtn) {
        toggleBtn.focus();
      }
    }
  }

  function updateTurns() {
    turnCount += 1;
    if (turnCounter) {
      turnCounter.textContent = turnCount + (turnCount === 1 ? ' turn' : ' turns');
    }
  }

  function hideEmptyState() {
    var es = document.getElementById('chat-empty-state');
    if (es && es.parentNode) {
      es.parentNode.removeChild(es);
    }
  }

  function appendUserMessage(text) {
    hideEmptyState();
    var bubble = document.createElement('div');
    bubble.className = 'chat-msg chat-msg--user';
    bubble.style.cssText = 'align-self:flex-end;max-width:85%;background:var(--text);color:var(--bg);border-radius:14px;padding:10px 14px;font-size:14px;line-height:1.45;word-break:break-word;white-space:pre-wrap';
    bubble.textContent = text;
    messagesContainer.appendChild(bubble);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  function appendAssistantHtml(html) {
    var bubble = document.createElement('div');
    bubble.className = 'chat-msg chat-msg--assistant agent-markdown';
    bubble.style.cssText = 'align-self:flex-start;max-width:92%;background:var(--fill);border-radius:14px;padding:12px 14px;font-size:14px;line-height:1.5;color:var(--text);word-break:break-word';
    bubble.innerHTML = html;
    messagesContainer.appendChild(bubble);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  function appendErrorMessage(errorText) {
    var bubble = document.createElement('div');
    bubble.className = 'chat-msg chat-msg--error';
    bubble.style.cssText = 'align-self:flex-start;max-width:92%;background:var(--warnbg);border-left:3px solid var(--warn);border-radius:6px;padding:10px 12px;font-size:13px;line-height:1.4;color:var(--text)';
    bubble.textContent = errorText;
    messagesContainer.appendChild(bubble);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  function appendLoadingIndicator() {
    var indicator = document.createElement('div');
    indicator.id = 'chat-loading-indicator';
    indicator.className = 'chat-msg chat-msg--loading muted';
    indicator.style.cssText = 'align-self:flex-start;font-size:13px;padding:6px 12px;display:flex;gap:6px;align-items:center';
    indicator.innerHTML = '<span class="shimmer" style="display:inline-block;width:12px;height:12px;border-radius:50%"></span> <span>Thinking...</span>';
    messagesContainer.appendChild(indicator);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return indicator;
  }

  function removeLoadingIndicator() {
    var el = document.getElementById('chat-loading-indicator');
    if (el && el.parentNode) {
      el.parentNode.removeChild(el);
    }
  }

  function friendlyAgentError(message, status) {
    var norm = String(message || '').toLowerCase();
    if (
      status === 429 ||
      status === 503 ||
      /temporarily unavailable|rate.?limit|quota|too many requests|service unavailable|overloaded/.test(norm)
    ) {
      return 'AI analysis is temporarily unavailable. Please wait a few minutes and try again; the dashboard is ready for your next request.';
    }
    if (status && status >= 500) {
      return 'The Research Desk is temporarily unavailable. Please try again shortly.';
    }
    if (status === 401 || status === 403) {
      return 'The Research Desk is unavailable for this session. Please check the configured endpoint.';
    }
    return message || ('AgentOS request failed' + (status ? ' (' + status + ')' : '') + '.');
  }

  async function sendMessage(text) {
    var trimmed = (text || '').trim();
    if (!trimmed || isLoading) return;

    appendUserMessage(trimmed);
    updateTurns();
    if (input) {
      input.value = '';
      input.style.height = '40px';
    }

    isLoading = true;
    if (submitBtn) submitBtn.disabled = true;
    appendLoadingIndicator();

    try {
      var formPayload = new FormData();
      formPayload.append('message', trimmed);
      formPayload.append('stream', 'false');
      formPayload.append('session_id', sessionId);

      var runRes = await fetch(RUNS_URL, {
        method: 'POST',
        body: formPayload,
        headers: { Accept: 'application/json' },
      });

      var runData;
      try {
        runData = await runRes.json();
      } catch (_) {
        runData = { detail: 'Unexpected response from AgentOS.' };
      }

      removeLoadingIndicator();

      if (!runRes.ok) {
        throw new Error(friendlyAgentError(runData.detail || runData.message, runRes.status));
      }

      var rawContent = runData.content || runData.response || '';
      if (!rawContent && runData.detail) {
        throw new Error(friendlyAgentError(runData.detail, runRes.status));
      }

      // Convert agent markdown to sanitized HTML via /api/chat/render
      var renderRes = await fetch(RENDER_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ text: rawContent }),
      });

      if (!renderRes.ok) {
        var errJson = await renderRes.json().catch(function () { return {}; });
        throw new Error(errJson.detail || 'HTML rendering failed.');
      }

      var renderData = await renderRes.json();
      appendAssistantHtml(renderData.html);
    } catch (err) {
      removeLoadingIndicator();
      appendErrorMessage(err.message || 'The request could not be completed.');
    } finally {
      isLoading = false;
      if (submitBtn) submitBtn.disabled = false;
      if (input) input.focus();
    }
  }

  // Expose helper on window for external callers and inline chip handlers
  window.quantaiSendPrompt = function (prompt) {
    if (!prompt) return;
    if (!isDrawerOpen()) {
      setDrawerOpen(true);
    }
    sendMessage(prompt);
  };
  window.quantaiToggleChat = function (open) {
    if (typeof open === 'boolean') setDrawerOpen(open);
    else setDrawerOpen(!isDrawerOpen());
  };

  function updateConnectionState() {
    var isOnline = navigator.onLine !== false;
    var homeIndicator = document.getElementById('connection-indicator');
    if (homeIndicator) {
      var status = homeIndicator.getAttribute('data-status');
      if (status === 'offline' || status === 'error') {
        isOnline = false;
      }
    }
    if (connectionDot) {
      connectionDot.style.background = isOnline ? 'var(--up)' : 'var(--down)';
    }
    if (connectionText) {
      connectionText.textContent = isOnline ? 'Ready' : 'Offline';
    }
  }

  // Toggle button click (toggles drawer)
  toggleBtn.addEventListener('click', function () {
    setDrawerOpen(!isDrawerOpen());
  });

  // Minimize button click (closes drawer cleanly preserving history)
  if (minimizeBtn) {
    minimizeBtn.addEventListener('click', function () {
      setDrawerOpen(false);
    });
  }

  // Close button click
  if (closeBtn) {
    closeBtn.addEventListener('click', function () {
      setDrawerOpen(false);
    });
  }

  // Escape key closes drawer
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && isDrawerOpen()) {
      setDrawerOpen(false);
    }
  });

  // Multiline Textarea: Enter to send, Shift+Enter for newline
  if (input) {
    input.addEventListener('keydown', function (e) {
      if ((e.key === 'Enter' || e.keyCode === 13) && !e.shiftKey) {
        e.preventDefault();
        var val = input.value;
        if (val && val.trim()) {
          sendMessage(val);
        }
        return false;
      }
    });

    input.addEventListener('input', function () {
      this.style.height = 'auto';
      var scrollH = this.scrollHeight;
      var newH = Math.min(Math.max(40, scrollH), 120);
      this.style.height = newH + 'px';
    });
  }

  // Form submit button
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (input) sendMessage(input.value);
    });
  }

  // Quick contextual prompt pills (3 original prompt buttons)
  var pillsContainer = document.getElementById('chat-pills');
  if (pillsContainer) {
    pillsContainer.addEventListener('click', function (e) {
      var pill = e.target.closest('.chat-pill');
      if (pill) {
        var prompt = pill.getAttribute('data-prompt') || pill.textContent;
        if (prompt) sendMessage(prompt.trim());
      }
    });
  }

  // Empty state example prompt chips
  function bindChips() {
    var chips = document.querySelectorAll('.chat-example-chip');
    for (var i = 0; i < chips.length; i++) {
      chips[i].onclick = function (e) {
        e.preventDefault();
        var p = this.getAttribute('data-prompt') || this.textContent;
        if (p) sendMessage(p.replace(/↗/g, '').trim());
      };
    }
  }
  bindChips();

  // Monitor network status
  window.addEventListener('online', updateConnectionState);
  window.addEventListener('offline', updateConnectionState);
  updateConnectionState();
})();
