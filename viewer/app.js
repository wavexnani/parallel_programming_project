// ==========================================================================
// Parallel Mandelbrot Visualizer: Multi-Core Scheduling & Color Engine
// ==========================================================================

const canvas = document.getElementById('mandelbrotCanvas');
const ctx = canvas.getContext('2d', { alpha: false });

// UI Elements: Telemetry
const zoomVal = document.getElementById('zoomVal');
const timeVal = document.getElementById('timeVal');
const fpsVal = document.getElementById('fpsVal');

// UI Elements: Sidebar Controls
const coresBadge = document.getElementById('coresBadge');
const chunkBadge = document.getElementById('chunkBadge');
const chunkSizeGroup = document.getElementById('chunkSizeGroup');
const chunkSizeSelect = document.getElementById('chunkSizeSelect');
const themeSelect = document.getElementById('themeSelect');
const calcSpeedRange = document.getElementById('calcSpeedRange');
const speedBadge = document.getElementById('speedBadge');
const coreMeters = document.getElementById('coreMeters');
const metricSpeedup = document.getElementById('metricSpeedup');
const metricEfficiency = document.getElementById('metricEfficiency');
const metricImbalance = document.getElementById('metricImbalance');

// Buttons
const modeStaticBtn = document.getElementById('modeStaticBtn');
const modeDynamicBtn = document.getElementById('modeDynamicBtn');
const viewFractalBtn = document.getElementById('viewFractalBtn');
const viewThreadMapBtn = document.getElementById('viewThreadMapBtn');
const runCalcBtn = document.getElementById('runCalcBtn');
const instantRenderBtn = document.getElementById('instantRenderBtn');
const autoZoomBtn = document.getElementById('autoZoomBtn');
const playIcon = document.getElementById('playIcon');
const playLabel = document.getElementById('playLabel');
const zoomInBtn = document.getElementById('zoomInBtn');
const zoomOutBtn = document.getElementById('zoomOutBtn');
const resetBtn = document.getElementById('resetBtn');
const presetSelect = document.getElementById('presetSelect');
const viewPpmBtn = document.getElementById('viewPpmBtn');
const ppmModal = document.getElementById('ppmModal');
const closeModalBtn = document.getElementById('closeModalBtn');
const toast = document.getElementById('toast');

// Inspector Card
const colorSwatch = document.getElementById('colorSwatch');
const hexCode = document.getElementById('hexCode');
const rgbCode = document.getElementById('rgbCode');
const hslCode = document.getElementById('hslCode');
const statusPill = document.getElementById('statusPill');
const iterVal = document.getElementById('iterVal');
const pixelVal = document.getElementById('pixelVal');
const coreOwnerVal = document.getElementById('coreOwnerVal');
const realCoord = document.getElementById('realCoord');
const imagCoord = document.getElementById('imagCoord');

// Distinct Core Palette (up to 16 cores)
const CORE_COLORS = [
  '#f43f5e', // Core 0: Rose
  '#38bdf8', // Core 1: Sky Blue
  '#10b981', // Core 2: Emerald
  '#fbbf24', // Core 3: Amber
  '#a855f7', // Core 4: Purple
  '#06b6d4', // Core 5: Cyan
  '#ec4899', // Core 6: Pink
  '#84cc16', // Core 7: Lime
  '#f97316', // Core 8: Orange
  '#6366f1', // Core 9: Indigo
  '#14b8a6', // Core 10: Teal
  '#e11d48', // Core 11: Crimson
  '#3b82f6', // Core 12: Blue
  '#8b5cf6', // Core 13: Violet
  '#d946ef', // Core 14: Fuchsia
  '#eab308'  // Core 15: Yellow
];

// Presets
const PRESETS = {
  full: { targetX: -0.75, targetY: 0.0, spanX: 3.2 },
  seahorse: { targetX: -0.743643887037, targetY: 0.131825904205, spanX: 0.005 },
  elephant: { targetX: 0.275, targetY: 0.0075, spanX: 0.04 },
  quad: { targetX: -0.16070135, targetY: 1.0375665, spanX: 0.02 },
  minibrot: { targetX: -1.768778833, targetY: -0.001738994, spanX: 0.008 },
  triple: { targetX: -0.088, targetY: 0.654, spanX: 0.03 }
};

// State
let width = 0;
let height = 0;
let centerX = -0.75;
let centerY = 0.0;
let spanX = 3.2;
let maxIter = 1000;

let numCores = 8;
let schedulingMode = 'dynamic'; // 'static' or 'dynamic'
let chunkSize = 4;
let colorTheme = 'purple';
let viewMode = 'fractal'; // 'fractal' or 'threads'
let animationSpeed = 3;

let isAutoZooming = false;
let isCalculating = false;
let calcAnimationFrame = null;

// Buffers
let iterBuffer = null;
let threadOwnerBuffer = null;
let imageData = null;

// Core Statistics
let coreStats = [];

// Setup Canvas Size
function resizeCanvas() {
  width = window.innerWidth;
  height = window.innerHeight;
  canvas.width = width;
  canvas.height = height;
  iterBuffer = new Int32Array(width * height);
  threadOwnerBuffer = new Int8Array(width * height);
  imageData = ctx.createImageData(width, height);
  instantRender();
}
window.addEventListener('resize', resizeCanvas);

// Color Interpolation
function interpolateStops(stops, t) {
  t = (t % 1.0 + 1.0) % 1.0;
  for (let i = 0; i < stops.length - 1; ++i) {
    const [p0, c0] = stops[i];
    const [p1, c1] = stops[i + 1];
    if (t >= p0 && t <= p1) {
      let localT = (t - p0) / (p1 - p0);
      localT = (1.0 - Math.cos(localT * Math.PI)) * 0.5; // Cosine ease
      return [
        Math.floor(c0[0] + (c1[0] - c0[0]) * localT),
        Math.floor(c0[1] + (c1[1] - c0[1]) * localT),
        Math.floor(c0[2] + (c1[2] - c0[2]) * localT)
      ];
    }
  }
  return stops[0][1];
}

function getPixelColor(iter, theme) {
  if (iter >= maxIter) {
    return theme === 'purple' ? [12, 2, 24] : [0, 0, 0];
  }

  if (theme === 'purple') {
    // Royal Amethyst & Pearl
    const stops = [
      [0.00, [15, 2, 32]],
      [0.12, [58, 10, 110]],
      [0.28, [115, 28, 192]],
      [0.44, [170, 88, 250]],
      [0.60, [218, 185, 255]],
      [0.78, [252, 248, 255]],
      [0.90, [228, 218, 248]],
      [1.00, [15, 2, 32]]
    ];
    return interpolateStops(stops, (iter / 42.0) % 1.0);
  } else if (theme === 'quanta') {
    // Quanta Turquoise & Gold
    const stops = [
      [0.00, [4, 12, 18]],
      [0.12, [0, 160, 215]],
      [0.24, [0, 238, 255]],
      [0.38, [242, 252, 255]],
      [0.50, [220, 168, 85]],
      [0.65, [42, 72, 58]],
      [0.82, [78, 108, 92]],
      [1.00, [4, 12, 18]]
    ];
    return interpolateStops(stops, (iter / 50.0) % 1.0);
  } else if (theme === 'electric') {
    // Classic Electric Blue & Amber
    const t = iter / 30.0;
    const r = Math.floor(128 + 127 * Math.sin(t));
    const g = Math.floor(128 + 127 * Math.sin(t + 2.094));
    const b = Math.floor(128 + 127 * Math.sin(t + 4.188));
    return [r, g, b];
  } else if (theme === 'sunset') {
    // Cosmic Sunset
    const stops = [
      [0.00, [20, 5, 20]],
      [0.20, [140, 15, 80]],
      [0.45, [230, 60, 30]],
      [0.70, [255, 180, 20]],
      [0.90, [255, 250, 180]],
      [1.00, [20, 5, 20]]
    ];
    return interpolateStops(stops, (iter / 40.0) % 1.0);
  } else if (theme === 'emerald') {
    // Cyber Emerald
    const stops = [
      [0.00, [2, 15, 10]],
      [0.25, [5, 80, 45]],
      [0.50, [16, 185, 129]],
      [0.75, [110, 231, 183]],
      [0.90, [236, 253, 245]],
      [1.00, [2, 15, 10]]
    ];
    return interpolateStops(stops, (iter / 35.0) % 1.0);
  } else {
    // Monochrome High-Contrast
    const val = Math.floor(((iter % 60) / 60.0) * 255);
    return [val, val, val];
  }
}

function hexToRgb(hex) {
  const bigint = parseInt(hex.slice(1), 16);
  return [(bigint >> 16) & 255, (bigint >> 8) & 255, bigint & 255];
}

// Compute single pixel escape iteration
function computeEscapeTime(cr, ci, maxI) {
  let zr = 0.0;
  let zi = 0.0;
  let iter = 0;
  while (zr * zr + zi * zi <= 4.0 && iter < maxI) {
    const tmp = zr * zr - zi * zi + cr;
    zi = 2.0 * zr * zi + ci;
    zr = tmp;
    iter++;
  }
  return iter;
}

// Render a single horizontal row and write to imageData
function computeRow(y, coreId) {
  const spanY = spanX * (height / width);
  const imagMin = centerY - spanY / 2.0;
  const imagMax = centerY + spanY / 2.0;
  const realMin = centerX - spanX / 2.0;
  const realMax = centerX + spanX / 2.0;

  const ci = imagMax - (y / (height - 1)) * (imagMax - imagMin);
  const realStep = (realMax - realMin) / (width - 1);
  const offset = y * width;
  const data = imageData.data;

  let rowIters = 0;
  const coreRgb = hexToRgb(CORE_COLORS[coreId % CORE_COLORS.length]);

  for (let x = 0; x < width; ++x) {
    const cr = realMin + x * realStep;
    const iter = computeEscapeTime(cr, ci, maxIter);
    iterBuffer[offset + x] = iter;
    threadOwnerBuffer[offset + x] = coreId;
    rowIters += iter;

    const pIdx = (offset + x) * 4;
    if (viewMode === 'threads') {
      // Color-coded by assigning Core
      const factor = iter >= maxIter ? 0.35 : 0.85 + 0.15 * Math.sin(iter / 10);
      data[pIdx] = Math.floor(coreRgb[0] * factor);
      data[pIdx + 1] = Math.floor(coreRgb[1] * factor);
      data[pIdx + 2] = Math.floor(coreRgb[2] * factor);
      data[pIdx + 3] = 255;
    } else {
      // Fractal Theme Color
      const [r, g, b] = getPixelColor(iter, colorTheme);
      data[pIdx] = r;
      data[pIdx + 1] = g;
      data[pIdx + 2] = b;
      data[pIdx + 3] = 255;
    }
  }

  coreStats[coreId].rows++;
  coreStats[coreId].iterations += rowIters;
}

// Build UI Meters for Cores
function updateCoreMetersUI() {
  coreMeters.innerHTML = '';
  const totalRows = height;

  coreStats.forEach(stat => {
    const row = document.createElement('div');
    row.className = 'core-row';

    const color = CORE_COLORS[stat.id % CORE_COLORS.length];
    const pct = ((stat.rows / totalRows) * 100).toFixed(1);

    row.innerHTML = `
      <div class="core-tag">
        <span class="core-color-dot" style="background: ${color};"></span>
        <span>Core #${stat.id}</span>
      </div>
      <div class="core-bar-wrap">
        <div class="core-bar-fill" style="width: ${pct}%; background: ${color};"></div>
      </div>
      <div class="core-pct">${pct}%</div>
    `;
    coreMeters.appendChild(row);
  });
}

function updateMetricsUI(elapsedMs) {
  timeVal.innerText = `${elapsedMs.toFixed(1)} ms`;

  // Calculate load imbalance: max core iterations / avg core iterations
  let maxIters = 0;
  let totalIters = 0;
  coreStats.forEach(s => {
    if (s.iterations > maxIters) maxIters = s.iterations;
    totalIters += s.iterations;
  });
  const avgIters = totalIters / numCores;
  const imbalance = avgIters > 0 ? (maxIters / avgIters).toFixed(2) : '1.00';

  metricImbalance.innerText = `${imbalance}x`;

  // Theoretical speedup estimation for visualization
  const speedupVal = (numCores / parseFloat(imbalance)).toFixed(2);
  const effVal = Math.min(100, (parseFloat(speedupVal) / numCores) * 100).toFixed(0);

  metricSpeedup.innerText = `${speedupVal}x`;
  metricEfficiency.innerText = `${effVal}%`;
}

// Instant Complete Render (without animation)
function instantRender() {
  if (isCalculating) cancelCalculation();

  coreStats = Array.from({ length: numCores }, (_, i) => ({ id: i, rows: 0, iterations: 0 }));

  const t0 = performance.now();

  if (schedulingMode === 'static') {
    const baseRows = Math.floor(height / numCores);
    const rem = height % numCores;
    for (let c = 0; c < numCores; ++c) {
      const start = c * baseRows + Math.min(c, rem);
      const count = baseRows + (c < rem ? 1 : 0);
      for (let y = start; y < start + count; ++y) {
        computeRow(y, c);
      }
    }
  } else {
    // Dynamic scheduling
    const totalChunks = Math.ceil(height / chunkSize);
    for (let chunkId = 0; chunkId < totalChunks; ++chunkId) {
      const coreId = chunkId % numCores;
      const start = chunkId * chunkSize;
      const end = Math.min(start + chunkSize, height);
      for (let y = start; y < end; ++y) {
        computeRow(y, coreId);
      }
    }
  }

  const elapsed = performance.now() - t0;
  ctx.putImageData(imageData, 0, 0);
  updateCoreMetersUI();
  updateMetricsUI(elapsed);
}

// Watch Calculation: Animated Parallel Simulation
function startAnimatedCalculation() {
  if (isCalculating) cancelCalculation();

  isCalculating = true;
  runCalcBtn.innerHTML = `<span class="icon">⏹</span><span>Stop Calculation</span>`;
  runCalcBtn.classList.add('secondary');

  coreStats = Array.from({ length: numCores }, (_, i) => ({ id: i, rows: 0, iterations: 0 }));

  // Clear canvas partially for visual effect
  ctx.fillStyle = '#070a12';
  ctx.fillRect(0, 0, width, height);
  const d = imageData.data;
  for (let i = 0; i < d.length; i += 4) {
    d[i] = 7; d[i+1] = 10; d[i+2] = 18; d[i+3] = 255;
  }

  const t0 = performance.now();

  if (schedulingMode === 'static') {
    // Static mode: each core has its own range
    const baseRows = Math.floor(height / numCores);
    const rem = height % numCores;
    const coreCursors = Array.from({ length: numCores }, (_, c) => {
      const start = c * baseRows + Math.min(c, rem);
      const count = baseRows + (c < rem ? 1 : 0);
      return { start, current: start, end: start + count };
    });

    function stepStatic() {
      if (!isCalculating) return;

      const rowsPerFrame = Math.max(1, animationSpeed * 2);
      let allDone = true;

      for (let c = 0; c < numCores; ++c) {
        const cur = coreCursors[c];
        for (let r = 0; r < rowsPerFrame && cur.current < cur.end; ++r) {
          computeRow(cur.current, c);
          cur.current++;
          allDone = false;
        }
        if (cur.current < cur.end) allDone = false;
      }

      ctx.putImageData(imageData, 0, 0);
      updateCoreMetersUI();
      updateMetricsUI(performance.now() - t0);

      if (!allDone) {
        calcAnimationFrame = requestAnimationFrame(stepStatic);
      } else {
        finishCalculation();
      }
    }
    calcAnimationFrame = requestAnimationFrame(stepStatic);

  } else {
    // Dynamic mode: shared chunk queue
    const totalChunks = Math.ceil(height / chunkSize);
    let nextChunkIdx = 0;
    const coreActiveChunks = Array.from({ length: numCores }, () => null);

    function stepDynamic() {
      if (!isCalculating) return;

      const stepsPerFrame = Math.max(1, animationSpeed);

      for (let s = 0; s < stepsPerFrame; ++s) {
        for (let c = 0; c < numCores; ++c) {
          if (coreActiveChunks[c] === null && nextChunkIdx < totalChunks) {
            const start = nextChunkIdx * chunkSize;
            const end = Math.min(start + chunkSize, height);
            coreActiveChunks[c] = { start, current: start, end };
            nextChunkIdx++;
          }

          const active = coreActiveChunks[c];
          if (active) {
            computeRow(active.current, c);
            active.current++;
            if (active.current >= active.end) {
              coreActiveChunks[c] = null;
            }
          }
        }
      }

      ctx.putImageData(imageData, 0, 0);
      updateCoreMetersUI();
      updateMetricsUI(performance.now() - t0);

      const hasActiveWork = coreActiveChunks.some(chk => chk !== null);
      if (nextChunkIdx < totalChunks || hasActiveWork) {
        calcAnimationFrame = requestAnimationFrame(stepDynamic);
      } else {
        finishCalculation();
      }
    }
    calcAnimationFrame = requestAnimationFrame(stepDynamic);
  }
}

function finishCalculation() {
  isCalculating = false;
  runCalcBtn.innerHTML = `<span class="icon">▶</span><span>Watch Calculation</span>`;
  runCalcBtn.classList.remove('secondary');
}

function cancelCalculation() {
  if (calcAnimationFrame) cancelAnimationFrame(calcAnimationFrame);
  isCalculating = false;
  runCalcBtn.innerHTML = `<span class="icon">▶</span><span>Watch Calculation</span>`;
  runCalcBtn.classList.remove('secondary');
}

// Core Selector Buttons
document.querySelectorAll('.core-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.core-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    numCores = parseInt(btn.dataset.cores);
    coresBadge.innerText = `${numCores} Cores`;
    instantRender();
  });
});

// Scheduling Mode Switch
modeStaticBtn.addEventListener('click', () => {
  modeStaticBtn.classList.add('active');
  modeDynamicBtn.classList.remove('active');
  schedulingMode = 'static';
  chunkSizeGroup.style.opacity = '0.4';
  chunkSizeGroup.style.pointerEvents = 'none';
  instantRender();
});

modeDynamicBtn.addEventListener('click', () => {
  modeDynamicBtn.classList.add('active');
  modeStaticBtn.classList.remove('active');
  schedulingMode = 'dynamic';
  chunkSizeGroup.style.opacity = '1';
  chunkSizeGroup.style.pointerEvents = 'auto';
  instantRender();
});

// Chunk Size Selector
chunkSizeSelect.addEventListener('change', (e) => {
  chunkSize = parseInt(e.target.value);
  chunkBadge.innerText = `${chunkSize} rows`;
  if (schedulingMode === 'dynamic') instantRender();
});

// Theme Selector
themeSelect.addEventListener('change', (e) => {
  colorTheme = e.target.value;
  instantRender();
});

// View Mode (Fractal vs Threads)
viewFractalBtn.addEventListener('click', () => {
  viewFractalBtn.classList.add('active');
  viewThreadMapBtn.classList.remove('active');
  viewMode = 'fractal';
  instantRender();
});

viewThreadMapBtn.addEventListener('click', () => {
  viewThreadMapBtn.classList.add('active');
  viewFractalBtn.classList.remove('active');
  viewMode = 'threads';
  instantRender();
});

// Trigger Buttons
runCalcBtn.addEventListener('click', () => {
  if (isCalculating) {
    cancelCalculation();
  } else {
    startAnimatedCalculation();
  }
});

instantRenderBtn.addEventListener('click', () => {
  instantRender();
});

// Animation Speed
calcSpeedRange.addEventListener('input', (e) => {
  animationSpeed = parseInt(e.target.value);
  const labels = ['Step', 'Slow', 'Smooth', 'Fast', 'Turbo'];
  speedBadge.innerText = labels[animationSpeed - 1];
});

// Preset Selector
presetSelect.addEventListener('change', (e) => {
  const p = PRESETS[e.target.value];
  if (p) {
    centerX = p.targetX;
    centerY = p.targetY;
    spanX = p.spanX;
    zoomVal.innerText = `${(3.2 / spanX).toFixed(1)}x`;
    instantRender();
  }
});

// Reset Button
resetBtn.addEventListener('click', () => {
  centerX = PRESETS.full.targetX;
  centerY = PRESETS.full.targetY;
  spanX = PRESETS.full.spanX;
  zoomVal.innerText = '1.0x';
  presetSelect.value = 'full';
  instantRender();
});

// Zoom In/Out
zoomInBtn.addEventListener('click', () => {
  spanX /= 1.5;
  zoomVal.innerText = `${(3.2 / spanX).toFixed(1)}x`;
  instantRender();
});

zoomOutBtn.addEventListener('click', () => {
  spanX *= 1.5;
  zoomVal.innerText = `${(3.2 / spanX).toFixed(1)}x`;
  instantRender();
});

// Auto Zoom
autoZoomBtn.addEventListener('click', () => {
  isAutoZooming = !isAutoZooming;
  if (isAutoZooming) {
    playIcon.innerText = '⏸';
    playLabel.innerText = 'Pause Auto-Zoom';
    autoZoomBtn.classList.add('active');
    loopAutoZoom();
  } else {
    playIcon.innerText = '▶';
    playLabel.innerText = 'Auto-Zoom (Video Mode)';
    autoZoomBtn.classList.remove('active');
  }
});

function loopAutoZoom() {
  if (!isAutoZooming) return;
  const target = PRESETS[presetSelect.value] || PRESETS.seahorse;
  centerX += (target.targetX - centerX) * 0.05;
  centerY += (target.targetY - centerY) * 0.05;
  spanX *= 0.98;
  zoomVal.innerText = `${(3.2 / spanX).toFixed(1)}x`;
  instantRender();
  requestAnimationFrame(loopAutoZoom);
}

// Mouse Drag & Pan
let isDragging = false;
let startDragX = 0, startDragY = 0;

canvas.addEventListener('mousedown', (e) => {
  isDragging = true;
  startDragX = e.clientX;
  startDragY = e.clientY;
});

window.addEventListener('mouseup', () => {
  isDragging = false;
});

window.addEventListener('mousemove', (e) => {
  if (isDragging) {
    const dx = e.clientX - startDragX;
    const dy = e.clientY - startDragY;
    startDragX = e.clientX;
    startDragY = e.clientY;

    const spanY = spanX * (height / width);
    centerX -= (dx / width) * spanX;
    centerY += (dy / height) * spanY;
    instantRender();
  }

  // Hover Inspector
  inspectPixel(e.clientX, e.clientY);
});

// Mouse Wheel Zoom
canvas.addEventListener('wheel', (e) => {
  e.preventDefault();
  const zoomFactor = e.deltaY < 0 ? 0.85 : 1.15;
  
  // Zoom towards cursor
  const mouseRelX = e.clientX / width;
  const mouseRelY = e.clientY / height;
  const spanY = spanX * (height / width);

  const mouseReal = (centerX - spanX / 2.0) + mouseRelX * spanX;
  const mouseImag = (centerY + spanY / 2.0) - mouseRelY * spanY;

  spanX *= zoomFactor;
  const newSpanY = spanX * (height / width);

  centerX = mouseReal - (mouseRelX - 0.5) * spanX;
  centerY = mouseImag + (mouseRelY - 0.5) * newSpanY;

  zoomVal.innerText = `${(3.2 / spanX).toFixed(1)}x`;
  instantRender();
}, { passive: false });

// Inspect Pixel Telemetry
function inspectPixel(px, py) {
  if (!iterBuffer) return;
  const x = Math.min(Math.max(0, px), width - 1);
  const y = Math.min(Math.max(0, py), height - 1);
  const idx = y * width + x;

  const iter = iterBuffer[idx];
  const coreId = threadOwnerBuffer[idx];

  const spanY = spanX * (height / width);
  const cr = (centerX - spanX / 2.0) + (x / (width - 1)) * spanX;
  const ci = (centerY + spanY / 2.0) - (y / (height - 1)) * spanY;

  // Color
  const pIdx = idx * 4;
  const r = imageData.data[pIdx];
  const g = imageData.data[pIdx + 1];
  const b = imageData.data[pIdx + 2];

  const hex = `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`.toUpperCase();

  colorSwatch.style.backgroundColor = hex;
  hexCode.innerText = hex;
  rgbCode.innerText = `rgb(${r}, ${g}, ${b})`;

  // HSL
  const rn = r / 255, gn = g / 255, bn = b / 255;
  const max = Math.max(rn, gn, bn), min = Math.min(rn, gn, bn);
  let h = 0, s = 0, l = (max + min) / 2;
  if (max !== min) {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case rn: h = (gn - bn) / d + (gn < bn ? 6 : 0); break;
      case gn: h = (bn - rn) / d + 2; break;
      case bn: h = (rn - gn) / d + 4; break;
    }
    h /= 6;
  }
  hslCode.innerText = `hsl(${Math.round(h * 360)}, ${Math.round(s * 100)}%, ${Math.round(l * 100)}%)`;

  iterVal.innerText = `${iter} / ${maxIter}`;
  pixelVal.innerText = `${x}, ${y}`;
  coreOwnerVal.innerText = `Core #${coreId}`;
  coreOwnerVal.style.color = CORE_COLORS[coreId % CORE_COLORS.length];

  if (iter >= maxIter) {
    statusPill.className = 'status-pill interior';
    statusPill.innerText = 'Interior';
  } else {
    statusPill.className = 'status-pill escaped';
    statusPill.innerText = 'Escaped';
  }

  realCoord.innerText = cr.toFixed(12);
  imagCoord.innerText = ci.toFixed(12);
}

// Copy Hex to Clipboard
hexCode.addEventListener('click', () => {
  navigator.clipboard.writeText(hexCode.innerText).then(() => {
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2000);
  });
});

// Modal view of C++ PPM/PNG output
viewPpmBtn.addEventListener('click', () => {
  ppmModal.classList.add('open');
});
closeModalBtn.addEventListener('click', () => {
  ppmModal.classList.remove('open');
});
ppmModal.addEventListener('click', (e) => {
  if (e.target === ppmModal) ppmModal.classList.remove('open');
});

// Initialize on Load
window.addEventListener('load', () => {
  resizeCanvas();
});
