document.addEventListener('DOMContentLoaded', () => {
  // --- Navigation & Slides ---
  const navButtons = document.querySelectorAll('.nav-btn');
  const slides = document.querySelectorAll('.slide');
  const startBtn = document.getElementById('start-btn');

  function showSlide(slideId) {
    slides.forEach(slide => {
      slide.classList.remove('active');
    });
    navButtons.forEach(btn => {
      btn.classList.remove('active');
      if (btn.getAttribute('data-target') === slideId) {
        btn.classList.add('active');
      }
    });

    const activeSlide = document.getElementById(slideId);
    if (activeSlide) {
      activeSlide.classList.add('active');
    }
  }

  navButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.getAttribute('data-target');
      showSlide(target);
    });
  });

  if (startBtn) {
    startBtn.addEventListener('click', () => {
      showSlide('slide-specs');
    });
  }

  // --- Folder Explorer ---
  const folderHeaders = document.querySelectorAll('.folder-header');
  folderHeaders.forEach(header => {
    header.addEventListener('click', () => {
      const content = header.nextElementSibling;
      if (content) {
        content.classList.toggle('open');
        const icon = header.querySelector('.folder-icon');
        if (icon) {
          if (content.classList.contains('open')) {
            icon.className = 'folder-icon fas fa-folder-open';
          } else {
            icon.className = 'folder-icon fas fa-folder';
          }
        }
      }
    });
  });

  // --- Sirocco Calculator ---
  const inputs = {
    q: document.getElementById('input-q'),
    h: document.getElementById('input-h'),
    n: document.getElementById('input-n'),
    d2: document.getElementById('input-d2'),
    d1: document.getElementById('input-d1'),
    b: document.getElementById('input-b'),
    z: document.getElementById('input-z'),
    beta2: document.getElementById('input-beta2')
  };

  const outputs = {
    u2: document.getElementById('out-u2'),
    cm2: document.getElementById('out-cm2'),
    cu2: document.getElementById('out-cu2'),
    peuler: document.getElementById('out-peuler'),
    peje: document.getElementById('out-peje'),
    eta: document.getElementById('out-eta'),
    triangleSvg: document.getElementById('triangle-svg')
  };

  function calculate() {
    const q = parseFloat(inputs.q.value) || 0;
    const h = parseFloat(inputs.h.value) || 0;
    const n = parseFloat(inputs.n.value) || 0;
    const d2 = parseFloat(inputs.d2.value) || 0;
    const d1 = parseFloat(inputs.d1.value) || 0;
    const b = parseFloat(inputs.b.value) || 0;
    const z = parseInt(inputs.z.value) || 1;
    const beta2Deg = parseFloat(inputs.beta2.value) || 90;

    const rho = 1.20; // kg/m3
    const g = 9.80665;
    const t = 0.0012; // thickness 1.2 mm

    // 1. Static Pressure in Pa
    const deltaPs = h * g;

    // 2. Air Power (Useful) in kW
    const pAir = (q * deltaPs) / 1000;

    // 3. Peripheral speed U2
    const u2 = (Math.PI * d2 * n) / 60;

    // 4. Meridional speed Cm2 (with thickness blockage kb2)
    const beta2Rad = (beta2Deg * Math.PI) / 180;
    const kb2 = 1 - (z * t) / (Math.PI * d2 * Math.sin(beta2Rad));
    const cm2 = q / (Math.PI * d2 * b * (kb2 > 0 ? kb2 : 0.95));

    // 5. Wiesner slip factor
    const sigma = 1 - Math.sqrt(Math.sin(beta2Rad)) / Math.pow(z, 0.7);

    // 6. Tangential component Cu2
    const cotBeta2 = 1 / Math.tan(beta2Rad);
    const cu2 = (sigma * u2) - (cm2 * cotBeta2);

    // 7. Euler Pressure & Power
    const deltaPE = rho * u2 * cu2;
    const pEuler = (q * deltaPE) / 1000;

    // 8. Shaft Power (assume mechanical efficiency eta_m = 0.96)
    const pShaft = pEuler / 0.96;

    // 9. Static Efficiency
    const etaStatic = pShaft > 0 ? (pAir / pShaft) * 100 : 0;

    // Update outputs text
    outputs.u2.textContent = u2.toFixed(2) + ' m/s';
    outputs.cm2.textContent = cm2.toFixed(2) + ' m/s';
    outputs.cu2.textContent = cu2.toFixed(2) + ' m/s';
    outputs.peuler.textContent = (deltaPE / g).toFixed(1) + ' mmH2O';
    outputs.peje.textContent = pShaft.toFixed(2) + ' kW';
    outputs.eta.textContent = etaStatic.toFixed(1) + ' %';

    // Update status bar or colors depending on feasibility
    if (etaStatic > 90 || etaStatic < 20 || cu2 < 0) {
      outputs.eta.style.color = '#ff6b00'; // Warning color if unrealistic
    } else {
      outputs.eta.style.color = '#00f0ff'; // OK color
    }

    drawVelocityTriangle(u2, cm2, cu2, beta2Rad);
  }

  function drawVelocityTriangle(u2, cm2, cu2, beta2Rad) {
    const svg = outputs.triangleSvg;
    svg.innerHTML = ''; // Clear SVG

    // Define dimensions & scaling
    const svgWidth = svg.clientWidth || 600;
    const svgHeight = svg.clientHeight || 350;
    const padding = 50;

    // Scale calculations
    // We want the maximum speed component (usually u2 or cu2 + cm2) to fit nicely.
    const maxVal = Math.max(u2, cu2 + Math.abs(cm2 * 0.5), cm2) || 10;
    const scale = (svgWidth - 2 * padding) / maxVal;

    // Center coordinates
    const startX = padding;
    const startY = svgHeight - padding;

    // Vector ends
    const u2X = startX + u2 * scale;
    const u2Y = startY;

    const c2X = startX + cu2 * scale;
    const c2Y = startY - cm2 * scale;

    // Markers for arrowheads
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    
    const createMarker = (id, color) => {
      const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
      marker.setAttribute('id', id);
      marker.setAttribute('viewBox', '0 0 10 10');
      marker.setAttribute('refX', '8');
      marker.setAttribute('refY', '5');
      marker.setAttribute('markerWidth', '6');
      marker.setAttribute('markerHeight', '6');
      marker.setAttribute('orient', 'auto-start-reverse');
      
      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute('d', 'M 0 1 L 10 5 L 0 9 z');
      path.setAttribute('fill', color);
      marker.appendChild(path);
      return marker;
    };

    defs.appendChild(createMarker('arrow-u', '#00f0ff'));
    defs.appendChild(createMarker('arrow-c', '#ff3366'));
    defs.appendChild(createMarker('arrow-w', '#ffcc00'));
    defs.appendChild(createMarker('arrow-cm', '#00ff66'));
    svg.appendChild(defs);

    // Draw grid lines
    const grid = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    grid.setAttribute('x1', padding);
    grid.setAttribute('y1', startY);
    grid.setAttribute('x2', svgWidth - padding);
    grid.setAttribute('y2', startY);
    grid.setAttribute('stroke', '#1e293b');
    grid.setAttribute('stroke-width', '1');
    svg.appendChild(grid);

    // 1. Draw Vector U2 (Peripheral Speed - Cyan)
    drawVector(startX, startY, u2X, u2Y, '#00f0ff', 3, 'arrow-u');
    drawLabel(startX + (u2 * scale) / 2, startY + 20, 'U₂ = ' + u2.toFixed(1) + ' m/s', '#00f0ff', 'middle');

    // 2. Draw Vector C2 (Absolute Speed - Pink)
    drawVector(startX, startY, c2X, c2Y, '#ff3366', 3, 'arrow-c');
    drawLabel(startX + (cu2 * scale) / 2 - 10, startY - (cm2 * scale) / 2 - 10, 'C₂', '#ff3366', 'end');

    // 3. Draw Vector W2 (Relative Speed - Yellow)
    // Relative vector starts at U2 head and goes to C2 head
    drawVector(u2X, u2Y, c2X, c2Y, '#ffcc00', 3, 'arrow-w');
    drawLabel(u2X + ((c2X - u2X) / 2) + 15, startY - (cm2 * scale) / 2, 'W₂', '#ffcc00', 'start');

    // 4. Draw Meridional Projection Cm2 (Green, dashed)
    drawVector(c2X, startY, c2X, c2Y, '#00ff66', 1.5, 'arrow-cm', '4,4');
    drawLabel(c2X + 10, startY - (cm2 * scale) / 2, 'C_m₂ = ' + cm2.toFixed(1) + ' m/s', '#00ff66', 'start');

    // Auxiliary label for Cu2
    const auxCu2 = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    auxCu2.setAttribute('x1', startX);
    auxCu2.setAttribute('y1', startY + 30);
    auxCu2.setAttribute('x2', c2X);
    auxCu2.setAttribute('y2', startY + 30);
    auxCu2.setAttribute('stroke', '#ff3366');
    auxCu2.setAttribute('stroke-width', '1');
    auxCu2.setAttribute('stroke-dasharray', '2,2');
    svg.appendChild(auxCu2);
    
    drawLabel(startX + (cu2 * scale) / 2, startY + 45, 'C_u₂ = ' + cu2.toFixed(1) + ' m/s', '#ff3366', 'middle');
  }

  function drawVector(x1, y1, x2, y2, color, width, markerId, dashArray = '') {
    const svg = outputs.triangleSvg;
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', x1);
    line.setAttribute('y1', y1);
    line.setAttribute('x2', x2);
    line.setAttribute('y2', y2);
    line.setAttribute('stroke', color);
    line.setAttribute('stroke-width', width);
    if (markerId) {
      line.setAttribute('marker-end', `url(#${markerId})`);
    }
    if (dashArray) {
      line.setAttribute('stroke-dasharray', dashArray);
    }
    svg.appendChild(line);
  }

  function drawLabel(x, y, textStr, color, anchor) {
    const svg = outputs.triangleSvg;
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', x);
    text.setAttribute('y', y);
    text.setAttribute('fill', color);
    text.setAttribute('font-family', 'Space Grotesk, monospace');
    text.setAttribute('font-size', '12px');
    text.setAttribute('font-weight', 'bold');
    text.setAttribute('text-anchor', anchor);
    text.textContent = textStr;
    svg.appendChild(text);
  }

  // --- Add Event Listeners for Inputs ---
  Object.values(inputs).forEach(input => {
    input.addEventListener('input', calculate);
  });

  // Run initial calculation on load
  calculate();

  // Handle window resizing to redraw SVG correctly
  window.addEventListener('resize', calculate);
});
