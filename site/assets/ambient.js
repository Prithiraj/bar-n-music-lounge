const canvas = document.querySelector('[data-ambient-canvas]');

if (canvas) {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  try {
    const THREE = await import('https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.min.js');

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: false, powerPreference: 'low-power' });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
    renderer.setClearColor(0x000000, 0);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 50);
    camera.position.set(0, 0.1, 5.8);

    const group = new THREE.Group();
    scene.add(group);

    const amber = new THREE.LineBasicMaterial({ color: 0xf5b342, transparent: true, opacity: 0.34 });
    const cream = new THREE.LineBasicMaterial({ color: 0xffe6b1, transparent: true, opacity: 0.18 });
    const blue = new THREE.PointsMaterial({ color: 0x7ad7ff, size: 0.035, transparent: true, opacity: 0.42, sizeAttenuation: true });

    const createWave = (z, amplitude, material, phase = 0) => {
      const points = [];
      for (let i = 0; i <= 96; i += 1) {
        const x = -3.5 + (i / 96) * 7;
        const envelope = Math.max(0, 1 - Math.abs(x) / 3.7);
        const y = Math.sin(i * 0.34 + phase) * amplitude * envelope + Math.sin(i * 0.1 + phase) * 0.08;
        points.push(new THREE.Vector3(x, y, z));
      }
      const geometry = new THREE.BufferGeometry().setFromPoints(points);
      const line = new THREE.Line(geometry, material);
      group.add(line);
      return line;
    };

    const waves = [
      createWave(0.15, 0.42, amber, 0),
      createWave(-0.18, 0.28, cream, 1.4),
      createWave(-0.5, 0.18, amber, 2.8)
    ];

    const particlePositions = [];
    for (let i = 0; i < 54; i += 1) {
      particlePositions.push(
        (Math.random() - 0.5) * 7,
        (Math.random() - 0.5) * 4.5,
        -0.8 + Math.random() * 1.8
      );
    }
    const particleGeometry = new THREE.BufferGeometry();
    particleGeometry.setAttribute('position', new THREE.Float32BufferAttribute(particlePositions, 3));
    const particles = new THREE.Points(particleGeometry, blue);
    group.add(particles);

    const resize = () => {
      const rect = canvas.getBoundingClientRect();
      const width = Math.max(1, rect.width);
      const height = Math.max(1, rect.height);
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
    };

    const observer = new ResizeObserver(resize);
    observer.observe(canvas);
    resize();

    let pointerX = 0;
    let pointerY = 0;
    const onPointerMove = (event) => {
      const rect = canvas.getBoundingClientRect();
      pointerX = ((event.clientX - rect.left) / Math.max(rect.width, 1) - 0.5) * 0.12;
      pointerY = ((event.clientY - rect.top) / Math.max(rect.height, 1) - 0.5) * 0.08;
    };

    if (!reducedMotion) {
      window.addEventListener('pointermove', onPointerMove, { passive: true });
    }

    const clock = new THREE.Clock();
    const render = () => {
      const t = clock.getElapsedTime();
      if (!reducedMotion) {
        group.rotation.y += (pointerX - group.rotation.y) * 0.035;
        group.rotation.x += (-pointerY - group.rotation.x) * 0.035;
        waves[0].position.y = Math.sin(t * 0.8) * 0.05;
        waves[1].position.y = Math.sin(t * 0.65 + 1.2) * 0.04;
        waves[2].position.y = Math.sin(t * 0.55 + 2.4) * 0.03;
        particles.rotation.z = Math.sin(t * 0.12) * 0.04;
      }
      renderer.render(scene, camera);
      if (!reducedMotion) requestAnimationFrame(render);
    };

    render();
  } catch (error) {
    canvas.hidden = true;
  }
}
