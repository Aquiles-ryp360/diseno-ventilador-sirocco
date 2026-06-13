(function () {
  "use strict";
  const data = window.SIROCCO_DATA;
  const canvas = document.getElementById("canvas3d");
  const viewport = document.getElementById("viewport");
  const info = document.getElementById("componentInfo");
  if (!window.THREE || !data) {
    info.textContent = "No se pudo cargar el modelo. Mantenga todas las carpetas juntas.";
    return;
  }

  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x07111f, 0.00032);
  const camera = new THREE.PerspectiveCamera(42, 1, 1, 8000);
  camera.position.set(1850, -2250, 1350);

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.07;
  controls.target.set(120, 0, 0);
  controls.minDistance = 450;
  controls.maxDistance = 4500;

  scene.add(new THREE.HemisphereLight(0xbce7ff, 0x162333, 1.25));
  const key = new THREE.DirectionalLight(0xffffff, 1.2);
  key.position.set(-800, -900, 1700); key.castShadow = true; scene.add(key);
  const rim = new THREE.DirectionalLight(0x31cbe0, 0.85);
  rim.position.set(1200, 900, 600); scene.add(rim);
  const warm = new THREE.PointLight(0xff9d48, 0.7, 2500);
  warm.position.set(500, -500, -500); scene.add(warm);

  const grid = new THREE.GridHelper(3000, 30, 0x284b63, 0x142b3c);
  grid.rotation.x = Math.PI / 2; grid.position.z = -410; scene.add(grid);
  const axes = new THREE.AxesHelper(360); axes.position.set(-850, -560, -390); scene.add(axes);

  const root = new THREE.Group(); scene.add(root);
  const rotor = new THREE.Group(); rotor.name = "Rodete completo"; root.add(rotor);
  const volute = new THREE.Group(); volute.name = "Voluta"; root.add(volute);
  const flow = new THREE.Group(); flow.name = "Trayectoria del aire"; root.add(flow);

  const matBlade = new THREE.MeshStandardMaterial({ color: 0x197bc2, metalness: .55, roughness: .28, side: THREE.DoubleSide });
  const matRing = new THREE.MeshStandardMaterial({ color: 0x35a5df, metalness: .55, roughness: .24, side: THREE.DoubleSide });
  const matDisk = new THREE.MeshStandardMaterial({ color: 0x29475d, metalness: .7, roughness: .3, side: THREE.DoubleSide });
  const matSteel = new THREE.MeshStandardMaterial({ color: 0xa7b5c2, metalness: .9, roughness: .2 });
  const matPulley = new THREE.MeshStandardMaterial({ color: 0xe97823, metalness: .5, roughness: .35 });
  const matVolute = new THREE.MeshPhysicalMaterial({ color: 0x21a6bd, transparent: true, opacity: .24, roughness: .2, metalness: .1, side: THREE.DoubleSide, depthWrite: false });
  const matVoluteEdge = new THREE.LineBasicMaterial({ color: 0x74e9f5, transparent: true, opacity: .55 });

  function component(mesh, name) { mesh.userData.label = name; mesh.castShadow = true; mesh.receiveShadow = true; return mesh; }
  function axialCylinder(r, length, material, z, name, radial) {
    const mesh = component(new THREE.Mesh(new THREE.CylinderGeometry(r, r, length, radial || 72), material), name);
    mesh.rotation.x = Math.PI / 2; mesh.position.z = z || 0; return mesh;
  }
  function annularShape(rOut, rIn) {
    const s = new THREE.Shape(); s.absarc(0, 0, rOut, 0, Math.PI * 2, false);
    const h = new THREE.Path(); h.absarc(0, 0, rIn, 0, Math.PI * 2, true); s.holes.push(h); return s;
  }
  function extruded(shape, depth, material, name) {
    const g = new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: false, curveSegments: 72, steps: 1 });
    g.translate(0, 0, -depth / 2); g.computeVertexNormals(); return component(new THREE.Mesh(g, material), name);
  }

  const bladeShape = new THREE.Shape();
  data.geometria.contorno_alabe_mm.forEach((p, i) => i ? bladeShape.lineTo(p[0], p[1]) : bladeShape.moveTo(p[0], p[1]));
  bladeShape.closePath();
  const bladeGeometry = new THREE.ExtrudeGeometry(bladeShape, { depth: data.dimensiones.ancho_rodete_mm, bevelEnabled: false, steps: 1 });
  bladeGeometry.translate(0, 0, -data.dimensiones.ancho_rodete_mm / 2); bladeGeometry.computeVertexNormals();
  const bladeGroup = new THREE.Group(); bladeGroup.name = "48 álabes curvados hacia adelante"; rotor.add(bladeGroup);
  for (let i = 0; i < data.dimensiones.numero_alabes; i++) {
    const blade = component(new THREE.Mesh(bladeGeometry, matBlade), "Álabe " + (i + 1));
    blade.rotation.z = i * Math.PI * 2 / data.dimensiones.numero_alabes; blade.castShadow = true; bladeGroup.add(blade);
  }
  rotor.add(extruded(annularShape(300, 255), 2, matRing, "Anillo de entrada izquierdo")).position.z = -116;
  const rightRing = extruded(annularShape(300, 255), 2, matRing, "Anillo de entrada derecho"); rightRing.position.z = 116; rotor.add(rightRing);
  rotor.add(extruded(annularShape(300, 40), 3, matDisk, "Disco central"));
  rotor.add(extruded(annularShape(40, 17.5), 80, matDisk, "Cubo"));
  rotor.add(axialCylinder(17.5, 720, matSteel, 0, "Eje Ø35 mm"));
  const pulley = extruded(annularShape(100, 18), 40, matPulley, "Polea Ø200 mm"); pulley.position.z = 265; rotor.add(pulley);

  const spiral = data.geometria.espiral_voluta_mm;
  const r0 = data.dimensiones.D2_mm / 2 + data.dimensiones.holgura_lengua_mm;
  const rFinal = data.dimensiones.radio_final_voluta_mm;
  const voluteShape = new THREE.Shape();
  spiral.forEach((p, i) => i ? voluteShape.lineTo(p[0], p[1]) : voluteShape.moveTo(p[0], p[1]));
  voluteShape.lineTo(rFinal, 500); voluteShape.lineTo(r0, 500); voluteShape.lineTo(r0, 0); voluteShape.closePath();
  const eye = new THREE.Path(); eye.absarc(0, 0, r0 - 6, 0, Math.PI * 2, true); voluteShape.holes.push(eye);
  const voluteMesh = extruded(voluteShape, data.dimensiones.ancho_voluta_mm, matVolute, "Carcasa espiral y descarga"); volute.add(voluteMesh);
  const edge = new THREE.LineSegments(new THREE.EdgesGeometry(voluteMesh.geometry, 18), matVoluteEdge); edge.userData.label = "Contorno de voluta"; volute.add(edge);

  const bearingMat = new THREE.MeshStandardMaterial({ color: 0x4b5964, metalness: .6, roughness: .4 });
  [-225, 225].forEach((z, i) => {
    const housing = component(new THREE.Mesh(new THREE.BoxGeometry(150, 220, 75), bearingMat), "Soporte de rodamiento " + (i + 1));
    housing.position.set(0, -118, z); rotor.add(housing);
    rotor.add(axialCylinder(48, 76, matSteel, z, "Rodamiento Ø35 mm"));
  });

  const inletMat = new THREE.MeshBasicMaterial({ color: 0x47d8ff, transparent: true, opacity: .8 });
  const outletMat = new THREE.MeshBasicMaterial({ color: 0xffb347, transparent: true, opacity: .85 });
  const arrow1 = new THREE.ArrowHelper(new THREE.Vector3(0, 0, 1), new THREE.Vector3(0, 0, -520), 290, 0x47d8ff, 45, 24);
  const arrow2 = new THREE.ArrowHelper(new THREE.Vector3(0, 0, -1), new THREE.Vector3(0, 0, 520), 290, 0x47d8ff, 45, 24);
  const arrow3 = new THREE.ArrowHelper(new THREE.Vector3(0, 1, 0), new THREE.Vector3((r0 + rFinal) / 2, 420, 0), 280, 0xffa53a, 55, 28);
  [arrow1, arrow2, arrow3].forEach(a => { a.userData.label = "Dirección del aire"; flow.add(a); });
  const particles = [];
  for (let i = 0; i < 24; i++) {
    const m = new THREE.Mesh(new THREE.SphereGeometry(7, 10, 8), i < 16 ? inletMat : outletMat);
    m.userData.phase = i / 24; flow.add(m); particles.push(m);
  }

  function setCamera(position, target) {
    camera.position.set(position[0], position[1], position[2]); controls.target.set(target[0], target[1], target[2]); controls.update();
  }
  const views = {
    iso: [[1850, -2250, 1350], [120, 0, 0]],
    front: [[0, 0, 2800], [100, 80, 0]],
    side: [[2800, 0, 180], [150, 0, 0]],
    top: [[0, -2800, 80], [120, 0, 0]]
  };
  document.querySelectorAll("[data-view]").forEach(btn => btn.addEventListener("click", () => {
    document.querySelectorAll("[data-view]").forEach(b => b.classList.remove("active")); btn.classList.add("active"); setCamera(...views[btn.dataset.view]);
  }));

  function bindCheck(id, object) { document.getElementById(id).addEventListener("change", e => object.visible = e.target.checked); }
  bindCheck("showRotor", rotor); bindCheck("showVolute", volute); bindCheck("showFlow", flow);
  document.getElementById("showGrid").addEventListener("change", e => { grid.visible = axes.visible = e.target.checked; });
  document.getElementById("opacity").addEventListener("input", e => { matVolute.opacity = Number(e.target.value) / 100; document.getElementById("opacityValue").textContent = e.target.value + "%"; });
  document.getElementById("speed").addEventListener("input", e => document.getElementById("speedValue").textContent = e.target.value + "%");
  document.getElementById("explode").addEventListener("input", e => { const v = Number(e.target.value) / 100; rotor.position.z = -360 * v; volute.position.z = 130 * v; flow.position.z = 70 * v; document.getElementById("explodeValue").textContent = e.target.value + "%"; });
  document.getElementById("resetView").addEventListener("click", () => { setCamera(...views.iso); controls.reset(); });
  document.getElementById("fullscreen").addEventListener("click", () => viewport.requestFullscreen && viewport.requestFullscreen());
  document.getElementById("screenshot").addEventListener("click", () => { renderer.render(scene, camera); const a = document.createElement("a"); a.download = "ventilador_sirocco_3d.png"; a.href = renderer.domElement.toDataURL("image/png"); a.click(); });

  const reportMode = new URLSearchParams(window.location.search).get("report");
  if (reportMode === "rotor") {
    volute.visible = false; flow.visible = false; grid.visible = axes.visible = false;
    document.querySelector(".panel").style.display = "none";
    document.getElementById("app").style.gridTemplateColumns = "1fr";
    setCamera([900, -1180, 760], [0, 0, 0]);
  } else if (reportMode === "assembly") {
    flow.visible = false; grid.visible = axes.visible = false; matVolute.opacity = .16;
    document.querySelector(".panel").style.display = "none";
    document.getElementById("app").style.gridTemplateColumns = "1fr";
    setCamera([1750, -2100, 1250], [130, 0, 0]);
  }

  const raycaster = new THREE.Raycaster(); const mouse = new THREE.Vector2(); let selected = null;
  renderer.domElement.addEventListener("pointerdown", event => {
    const rect = renderer.domElement.getBoundingClientRect(); mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1; mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(mouse, camera); const hits = raycaster.intersectObjects(root.children, true);
    if (selected && selected.material && selected.material.emissive) selected.material.emissive.setHex(selected.userData.oldEmissive || 0);
    selected = hits.find(h => h.object.userData.label)?.object || null;
    if (selected) { info.textContent = selected.userData.label; if (selected.material && selected.material.emissive) { selected.userData.oldEmissive = selected.material.emissive.getHex(); selected.material.emissive.setHex(0x16465d); } }
  });

  function resize() { const w = viewport.clientWidth, h = viewport.clientHeight; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); }
  window.addEventListener("resize", resize); resize();
  const clock = new THREE.Clock();
  function animate() {
    requestAnimationFrame(animate); const dt = Math.min(clock.getDelta(), .04); const t = clock.elapsedTime;
    if (document.getElementById("spinRotor").checked) rotor.rotation.z -= dt * Number(document.getElementById("speed").value) * .012;
    particles.forEach((p, i) => {
      const phase = (p.userData.phase + t * .08) % 1;
      if (phase < .36) { const side = i % 2 ? 1 : -1; p.position.set(35 * Math.sin(i), 35 * Math.cos(i), side * (520 - phase / .36 * 390)); }
      else if (phase < .72) { const q = (phase - .36) / .36, a = i * 1.7; p.position.set((55 + 260*q)*Math.cos(a), (55 + 260*q)*Math.sin(a), 25*Math.sin(i)); }
      else { const q = (phase - .72) / .28; p.position.set(r0 + (rFinal-r0)*.72, 160 + 560*q, 35*Math.sin(i)); }
    });
    controls.update(); renderer.render(scene, camera);
  }
  animate();
})();
