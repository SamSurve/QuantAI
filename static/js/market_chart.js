/**
 * QuantAI Interactive Market Chart Controller
 * Powered by vendored Chart.js 4.x
 *
 * Implements pure client-side history slicing for 1D, 1W, 1M, 3M, 6M, 1Y, 5Y.
 * Triggering zero server requests on period tabs or crosshair movement.
 */

(function () {
  'use strict';

  const PERIOD_DAYS = {
    '1W': 7,
    '5D': 7,
    '1M': 31,
    '3M': 92,
    '6M': 184,
    'YTD': 184,
    '1Y': 366,
  };

  const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  let currentCurrency = null;

  const CURRENCY_SYMBOLS = {
    USD: '$',
    EUR: '€',
    GBP: '£',
    INR: '₹',
    JPY: '¥',
    CAD: 'CA$',
    AUD: 'A$',
    CHF: 'CHF ',
    CNY: '¥',
  };

  function formatChartPrice(value, currency, decimals) {
    const num = Number(value);
    if (!Number.isFinite(num)) return '—';
    const dec = typeof decimals === 'number' ? decimals : 2;
    const curr = currency ? String(currency).trim().toUpperCase() : null;
    const symbol = curr ? (CURRENCY_SYMBOLS[curr] || curr + ' ') : '';
    const sign = num < 0 ? '-' : '';
    const absVal = Math.abs(num);

    if (curr === 'INR') {
      return sign + symbol + absVal.toLocaleString('en-IN', {
        minimumFractionDigits: dec,
        maximumFractionDigits: dec,
      });
    }

    if (curr === 'JPY') {
      return sign + symbol + Math.round(absVal).toLocaleString('en-US');
    }

    const formatted = absVal.toLocaleString('en-US', {
      minimumFractionDigits: dec,
      maximumFractionDigits: dec,
    });
    return sign + symbol + formatted;
  }


  function formatChartDate(value) {
    const raw = String(value);
    const m = raw.match(/^(\d{4})-(\d{2})-(\d{2})/);
    if (m) {
      const monthIdx = parseInt(m[2], 10) - 1;
      const day = m[3];
      if (monthIdx >= 0 && monthIdx < 12) {
        return `${MONTHS[monthIdx]} ${day}`;
      }
    }
    return raw.slice(0, 10);
  }

  function parseTimestamp(ts) {
    if (!ts) return 0;
    const clean = String(ts).trim();
    const d = new Date(clean.length === 10 ? clean + 'T00:00:00Z' : clean);
    const time = d.getTime();
    return Number.isNaN(time) ? 0 : time;
  }

  function sliceSeries(data, period) {
    if (!data) return [];
    if (period === '1D') {
      return Array.isArray(data.intraday) && data.intraday.length ? data.intraday : data.daily || [];
    }
    const daily = data.daily || [];
    if (!daily.length) return [];
    if (period === '5Y') return daily;

    const days = PERIOD_DAYS[period];
    if (!days) return daily;

    const latest = parseTimestamp(daily[daily.length - 1].label);
    const cutoff = latest - days * 24 * 60 * 60 * 1000;
    const filtered = daily.filter(p => parseTimestamp(p.label) >= cutoff);
    return filtered.length >= 2 ? filtered : daily.slice(-Math.min(daily.length, days));
  }

  function calcPerformance(series) {
    if (!series || series.length < 2) return null;
    const values = series.map(p => Number(p.value)).filter(v => Number.isFinite(v));
    if (values.length < 2) return null;
    const first = values[0];
    const last = values[values.length - 1];
    if (first === 0 || !Number.isFinite(first) || !Number.isFinite(last)) return null;

    const low = Math.min(...values);
    const high = Math.max(...values);
    const change = ((last - first) / first) * 100;
    return { low, high, change };
  }

  function getThemeColors() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    return {
      line: isDark ? '#30d158' : '#1a9c3c',
      downLine: isDark ? '#ff453a' : '#e30000',
      fillStart: isDark ? 'rgba(48, 209, 88, 0.28)' : 'rgba(26, 156, 60, 0.22)',
      fillStop: isDark ? 'rgba(48, 209, 88, 0.0)' : 'rgba(26, 156, 60, 0.0)',
      downFillStart: isDark ? 'rgba(255, 69, 58, 0.28)' : 'rgba(227, 0, 0, 0.22)',
      downFillStop: isDark ? 'rgba(255, 69, 58, 0.0)' : 'rgba(227, 0, 0, 0.0)',
      grid: isDark ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.05)',
      tick: isDark ? '#a1a1a6' : '#6e6e73',
      tooltipBg: isDark ? '#1c1c1e' : '#1d1d1f',
      tooltipText: '#ffffff',
      tooltipMuted: '#a1a1a6',
      crosshair: isDark ? 'rgba(255, 255, 255, 0.35)' : 'rgba(0, 0, 0, 0.35)',
    };
  }

  let chartInstance = null;
  let chartData = null;
  let activePeriod = '6M';

  // Custom Chart.js vertical dashed crosshair plugin
  const crosshairPlugin = {
    id: 'verticalCrosshair',
    afterDraw(chart) {
      if (chart.tooltip && chart.tooltip.getActiveElements && chart.tooltip.getActiveElements().length) {
        const activePoint = chart.tooltip.getActiveElements()[0];
        const ctx = chart.ctx;
        const x = activePoint.element.x;
        const topY = chart.scales.y.top;
        const bottomY = chart.scales.y.bottom;

        ctx.save();
        ctx.beginPath();
        ctx.setLineDash([4, 4]);
        ctx.moveTo(x, topY);
        ctx.lineTo(x, bottomY);
        ctx.lineWidth = 1;
        ctx.strokeStyle = getThemeColors().crosshair;
        ctx.stroke();
        ctx.restore();
      }
    },
  };

  function updateChart(period) {
    if (!chartData) return;
    activePeriod = period;

    const series = sliceSeries(chartData, period);
    const canvasContainer = document.getElementById('chart-canvas-container');
    const emptyState = document.getElementById('chart-empty-state');
    const statsRow = document.getElementById('chart-stats-row');

    if (!series || series.length < 2) {
      if (canvasContainer) canvasContainer.style.display = 'none';
      if (emptyState) emptyState.style.display = 'block';
      if (statsRow) statsRow.style.display = 'none';
      return;
    }

    if (canvasContainer) canvasContainer.style.display = 'block';
    if (emptyState) emptyState.style.display = 'none';
    if (statsRow) statsRow.style.display = 'flex';

    // Update stats
    const perf = calcPerformance(series);
    const lowEl = document.getElementById('chartPeriodLow');
    const highEl = document.getElementById('chartPeriodHigh');
    const chgEl = document.getElementById('chartPeriodChange');

    if (perf) {
      if (lowEl) lowEl.textContent = formatChartPrice(perf.low, currentCurrency, 2);
      if (highEl) highEl.textContent = formatChartPrice(perf.high, currentCurrency, 2);
      if (chgEl) {
        const isPos = perf.change >= 0;
        chgEl.textContent = `${isPos ? '+' : ''}${perf.change.toFixed(2)}%`;
        chgEl.style.color = isPos ? 'var(--upt)' : 'var(--down)';
      }
    }

    // Chart.js render
    const canvas = document.getElementById('marketChartCanvas');
    if (!canvas || typeof Chart === 'undefined') return;

    const ctx = canvas.getContext('2d');
    const colors = getThemeColors();
    const isNegative = perf && perf.change < 0;

    const gradient = ctx.createLinearGradient(0, 0, 0, 280);
    if (isNegative) {
      gradient.addColorStop(0, colors.downFillStart);
      gradient.addColorStop(1, colors.downFillStop);
    } else {
      gradient.addColorStop(0, colors.fillStart);
      gradient.addColorStop(1, colors.fillStop);
    }

    const labels = series.map(p => p.label);
    const values = series.map(p => p.value);

    if (chartInstance) {
      chartInstance.data.labels = labels;
      chartInstance.data.datasets[0].data = values;
      chartInstance.data.datasets[0].borderColor = isNegative ? colors.downLine : colors.line;
      chartInstance.data.datasets[0].backgroundColor = gradient;
      chartInstance.options.scales.x.grid.color = colors.grid;
      chartInstance.options.scales.y.grid.color = colors.grid;
      chartInstance.options.scales.x.ticks.color = colors.tick;
      chartInstance.options.scales.y.ticks.color = colors.tick;
      chartInstance.update();
      return;
    }

    chartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            data: values,
            borderColor: isNegative ? colors.downLine : colors.line,
            backgroundColor: gradient,
            fill: true,
            borderWidth: 2,
            tension: 0.25,
            pointRadius: 0,
            pointHoverRadius: 6,
            pointHoverBackgroundColor: '#ffffff',
            pointHoverBorderColor: isNegative ? colors.downLine : colors.line,
            pointHoverBorderWidth: 2,
          },
        ],
      },
      plugins: [crosshairPlugin],
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        interaction: {
          intersect: false,
          mode: 'index',
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            enabled: true,
            backgroundColor: colors.tooltipBg,
            titleColor: colors.tooltipMuted,
            bodyColor: colors.tooltipText,
            padding: 10,
            cornerRadius: 10,
            displayColors: false,
            callbacks: {
              title: function (items) {
                if (!items.length) return '';
                return formatChartDate(items[0].label);
              },
              label: function (item) {
                const val = Number(item.raw);
                return formatChartPrice(val, currentCurrency, 2);
              },
            },
          },
        },
        scales: {
          x: {
            grid: { color: colors.grid, drawBorder: false },
            ticks: {
              color: colors.tick,
              maxTicksLimit: 7,
              callback: function (val, index) {
                const label = this.getLabelForValue(val);
                return formatChartDate(label);
              },
            },
          },
          y: {
            position: 'right',
            grid: { color: colors.grid, drawBorder: false },
            ticks: {
              color: colors.tick,
              callback: function (val) {
                return formatChartPrice(val, currentCurrency, 0);
              },
            },
          },
        },
      },
    });
  }

  function init() {
    const dataEl = document.getElementById('chart-data');
    if (!dataEl) return;

    try {
      const rawText = dataEl.textContent.trim();
      if (rawText && rawText !== '{}') {
        chartData = JSON.parse(rawText);
        currentCurrency = chartData.currency || null;
      }
    } catch (e) {
      console.warn('Failed to parse chart-data JSON payload', e);
    }

    // Default period from buttons or 6M
    const activeBtn = document.querySelector('.period-btn.on');
    if (activeBtn) {
      activePeriod = activeBtn.getAttribute('data-period') || '6M';
    }

    // Bind period buttons
    const buttons = document.querySelectorAll('.period-btn');
    buttons.forEach(btn => {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        buttons.forEach(b => {
          b.classList.remove('on');
          b.setAttribute('aria-selected', 'false');
        });
        btn.classList.add('on');
        btn.setAttribute('aria-selected', 'true');
        const period = btn.getAttribute('data-period');
        updateChart(period);
      });
    });

    // Theme mutation observer
    const observer = new MutationObserver(() => {
      if (chartInstance) {
        chartInstance.destroy();
        chartInstance = null;
        updateChart(activePeriod);
      }
    });
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

    if (chartData) {
      updateChart(activePeriod);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
