/**
 * Enhanced Three.js 3D Human Body Viewer
 * ž:HžºS3Dþãåh
 *
 * Features:
 * - Ultra-realistic 3D human body model
 * - Smooth shading and realistic materials
 * - Advanced lighting system
 * - Interactive rotation, zoom, and pan
 * - Professional medical visualization
 * - Better proportions and anatomy
 *
 * Dependencies: Three.js r160+ (loaded via CDN)
 */

class Body3DViewerEnhanced {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error('¹h*~0 | Container not found:', containerId);
            return;
        }

        this.options = {
            showAcupoints: options.showAcupoints || false,
            showMuscles: options.showMuscles || false,
            selectedPoints: options.selectedPoints || [],
            selectedAreas: options.selectedAreas || [],
            enableShadows: true,
            highQuality: true,
            ...options
        };

        // Initialize Three.js components
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.bodyMesh = null;
        this.acupointMarkers = [];
        this.areaMarkers = [];

        // Wait for Three.js to load
        this.initWhenReady();
    }

    initWhenReady() {
        if (typeof THREE === 'undefined') {
            console.log('I…Three.js }... | Waiting for Three.js to load...');
            setTimeout(() => this.initWhenReady(), 100);
            return;
        }
        this.init();
    }

    init() {
        // Create scene with fog for depth
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0xf5f7fa);
        this.scene.fog = new THREE.Fog(0xf5f7fa, 5, 15);

        // Create camera
        const width = this.container.clientWidth || 800;
        const height = this.container.clientHeight || 600;
        this.camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
        this.camera.position.set(0, 1.6, 4);
        this.camera.lookAt(0, 1, 0);

        // Create high-quality renderer
        this.renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true,
            powerPreference: "high-performance"
        });
        this.renderer.setSize(width, height);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.shadowMap.enabled = this.options.enableShadows;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.renderer.outputEncoding = THREE.sRGBEncoding;
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1.2;
        this.container.appendChild(this.renderer.domElement);

        // Add advanced lights
        this.addLights();

        // Add orbit controls
        this.addControls();

        // Create enhanced human body
        this.createEnhancedHumanBody();

        // Add acupoints if enabled
        if (this.options.showAcupoints) {
            this.addAcupoints();
        }

        // Add treatment areas if enabled
        if (this.options.showMuscles) {
            this.addTreatmentAreas();
        }

        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());

        // Add UI controls
        this.addControlsUI();

        // Start animation loop
        this.animate();

        console.log(' ž:H3DºSåhËŒ | Enhanced 3D Body Viewer initialized');
    }

    addLights() {
        // Ambient light for overall illumination
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        this.scene.add(ambientLight);

        // Main directional light (key light)
        const mainLight = new THREE.DirectionalLight(0xffffff, 0.8);
        mainLight.position.set(5, 10, 5);
        mainLight.castShadow = true;
        mainLight.shadow.mapSize.width = 2048;
        mainLight.shadow.mapSize.height = 2048;
        mainLight.shadow.camera.near = 0.5;
        mainLight.shadow.camera.far = 50;
        mainLight.shadow.camera.left = -5;
        mainLight.shadow.camera.right = 5;
        mainLight.shadow.camera.top = 5;
        mainLight.shadow.camera.bottom = -5;
        mainLight.shadow.bias = -0.0001;
        this.scene.add(mainLight);

        // Fill light (softer, from opposite side)
        const fillLight = new THREE.DirectionalLight(0xffffff, 0.3);
        fillLight.position.set(-5, 5, -5);
        this.scene.add(fillLight);

        // Back light for rim lighting effect
        const backLight = new THREE.DirectionalLight(0xffffff, 0.4);
        backLight.position.set(0, 5, -5);
        this.scene.add(backLight);

        // Hemisphere light for natural sky/ground lighting
        const hemiLight = new THREE.HemisphereLight(0xffffff, 0x8d8d8d, 0.2);
        hemiLight.position.set(0, 20, 0);
        this.scene.add(hemiLight);

        // Add ground plane for shadows
        if (this.options.enableShadows) {
            const groundGeometry = new THREE.PlaneGeometry(10, 10);
            const groundMaterial = new THREE.ShadowMaterial({ opacity: 0.1 });
            const ground = new THREE.Mesh(groundGeometry, groundMaterial);
            ground.rotation.x = -Math.PI / 2;
            ground.position.y = -0.7;
            ground.receiveShadow = true;
            this.scene.add(ground);
        }
    }

    addControls() {
        if (typeof THREE.OrbitControls === 'undefined') {
            console.warn('OrbitControls not available');
            return;
        }

        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.minDistance = 2;
        this.controls.maxDistance = 10;
        this.controls.target.set(0, 1, 0);
        this.controls.enablePan = true;
        this.controls.panSpeed = 0.5;
        this.controls.rotateSpeed = 0.5;
    }

    createEnhancedHumanBody() {
        const bodyGroup = new THREE.Group();

        // Create realistic skin material with subsurface scattering effect
        const skinMaterial = new THREE.MeshStandardMaterial({
            color: 0xffd7ba,
            roughness: 0.6,
            metalness: 0.0,
            emissive: 0x000000,
            flatShading: false
        });

        // Muscle material (slightly redder)
        const muscleMaterial = new THREE.MeshStandardMaterial({
            color: 0xffb3a0,
            roughness: 0.7,
            metalness: 0.0,
            transparent: true,
            opacity: 0.85
        });

        // HEAD with better proportions
        const headGeometry = new THREE.SphereGeometry(0.14, 32, 32);
        const head = new THREE.Mesh(headGeometry, skinMaterial);
        head.position.y = 1.75;
        head.scale.set(1, 1.15, 1);
        head.castShadow = true;
        head.receiveShadow = true;
        bodyGroup.add(head);

        // NECK (more realistic)
        const neckGeometry = new THREE.CylinderGeometry(0.07, 0.08, 0.2, 16);
        const neck = new THREE.Mesh(neckGeometry, skinMaterial);
        neck.position.y = 1.58;
        neck.castShadow = true;
        neck.receiveShadow = true;
        bodyGroup.add(neck);

        // TORSO - Upper (chest area)
        const chestGeometry = new THREE.SphereGeometry(0.22, 32, 32);
        const chest = new THREE.Mesh(chestGeometry, skinMaterial);
        chest.position.y = 1.35;
        chest.scale.set(1, 1.2, 0.6);
        chest.castShadow = true;
        chest.receiveShadow = true;
        bodyGroup.add(chest);

        // TORSO - Middle (abdomen)
        const abdomenGeometry = new THREE.CylinderGeometry(0.18, 0.17, 0.35, 32);
        const abdomen = new THREE.Mesh(abdomenGeometry, skinMaterial);
        abdomen.position.y = 1.0;
        abdomen.castShadow = true;
        abdomen.receiveShadow = true;
        bodyGroup.add(abdomen);

        // Show muscle definition if enabled
        if (this.options.showMuscles) {
            // Chest muscles (pectorals)
            const pectoralGeometry = new THREE.SphereGeometry(0.12, 16, 16);

            const pectoralLeft = new THREE.Mesh(pectoralGeometry, muscleMaterial);
            pectoralLeft.position.set(-0.1, 1.35, 0.15);
            pectoralLeft.scale.set(0.8, 1, 0.6);
            bodyGroup.add(pectoralLeft);

            const pectoralRight = new THREE.Mesh(pectoralGeometry, muscleMaterial);
            pectoralRight.position.set(0.1, 1.35, 0.15);
            pectoralRight.scale.set(0.8, 1, 0.6);
            bodyGroup.add(pectoralRight);

            // Abdominal muscles (6-pack)
            const absSegmentGeometry = new THREE.BoxGeometry(0.08, 0.1, 0.05, 4, 4, 4);
            for (let row = 0; row < 3; row++) {
                for (let col = 0; col < 2; col++) {
                    const absMuscle = new THREE.Mesh(absSegmentGeometry, muscleMaterial);
                    absMuscle.position.set(
                        (col === 0 ? -0.07 : 0.07),
                        1.15 - row * 0.12,
                        0.17
                    );
                    bodyGroup.add(absMuscle);
                }
            }
        }

        // PELVIS/HIPS
        const pelvisGeometry = new THREE.SphereGeometry(0.19, 32, 32);
        const pelvis = new THREE.Mesh(pelvisGeometry, skinMaterial);
        pelvis.position.y = 0.75;
        pelvis.scale.set(1.1, 0.6, 0.95);
        pelvis.castShadow = true;
        pelvis.receiveShadow = true;
        bodyGroup.add(pelvis);

        // ARMS (with better anatomy)
        this.createArm(bodyGroup, skinMaterial, -1); // Left arm
        this.createArm(bodyGroup, skinMaterial, 1);  // Right arm

        // LEGS (with better anatomy)
        this.createLeg(bodyGroup, skinMaterial, -1); // Left leg
        this.createLeg(bodyGroup, skinMaterial, 1);  // Right leg

        // Add to scene
        this.scene.add(bodyGroup);
        this.bodyMesh = bodyGroup;

        console.log(' ž:HºS!‹úŒ | Enhanced body model created');
    }

    createArm(bodyGroup, material, side) {
        const dir = side; // -1 for left, 1 for right

        // Shoulder
        const shoulderGeometry = new THREE.SphereGeometry(0.08, 16, 16);
        const shoulder = new THREE.Mesh(shoulderGeometry, material);
        shoulder.position.set(dir * 0.25, 1.4, 0);
        shoulder.castShadow = true;
        bodyGroup.add(shoulder);

        // Upper arm
        const upperArmGeometry = new THREE.CapsuleGeometry(0.055, 0.45, 16, 32);
        const upperArm = new THREE.Mesh(upperArmGeometry, material);
        upperArm.position.set(dir * 0.28, 1.1, 0);
        upperArm.rotation.z = dir * Math.PI / 12;
        upperArm.castShadow = true;
        bodyGroup.add(upperArm);

        // Elbow
        const elbowGeometry = new THREE.SphereGeometry(0.05, 16, 16);
        const elbow = new THREE.Mesh(elbowGeometry, material);
        elbow.position.set(dir * 0.35, 0.82, 0);
        elbow.castShadow = true;
        bodyGroup.add(elbow);

        // Forearm
        const forearmGeometry = new THREE.CapsuleGeometry(0.045, 0.45, 16, 32);
        const forearm = new THREE.Mesh(forearmGeometry, material);
        forearm.position.set(dir * 0.42, 0.52, 0.05);
        forearm.rotation.z = dir * Math.PI / 10;
        forearm.rotation.x = -Math.PI / 20;
        forearm.castShadow = true;
        bodyGroup.add(forearm);

        // Hand
        const handGeometry = new THREE.BoxGeometry(0.08, 0.12, 0.04, 4, 4, 4);
        const hand = new THREE.Mesh(handGeometry, material);
        hand.position.set(dir * 0.5, 0.22, 0.08);
        hand.scale.set(1, 1, 1);
        hand.castShadow = true;
        bodyGroup.add(hand);
    }

    createLeg(bodyGroup, material, side) {
        const dir = side; // -1 for left, 1 for right

        // Thigh
        const thighGeometry = new THREE.CapsuleGeometry(0.09, 0.55, 16, 32);
        const thigh = new THREE.Mesh(thighGeometry, material);
        thigh.position.set(dir * 0.12, 0.38, 0);
        thigh.castShadow = true;
        bodyGroup.add(thigh);

        // Knee
        const kneeGeometry = new THREE.SphereGeometry(0.07, 16, 16);
        const knee = new THREE.Mesh(kneeGeometry, material);
        knee.position.set(dir * 0.12, 0.05, 0);
        knee.castShadow = true;
        bodyGroup.add(knee);

        // Calf
        const calfGeometry = new THREE.CapsuleGeometry(0.07, 0.5, 16, 32);
        const calf = new THREE.Mesh(calfGeometry, material);
        calf.position.set(dir * 0.12, -0.25, 0);
        calf.castShadow = true;
        bodyGroup.add(calf);

        // Ankle
        const ankleGeometry = new THREE.SphereGeometry(0.05, 16, 16);
        const ankle = new THREE.Mesh(ankleGeometry, material);
        ankle.position.set(dir * 0.12, -0.53, 0);
        ankle.castShadow = true;
        bodyGroup.add(ankle);

        // Foot
        const footGeometry = new THREE.BoxGeometry(0.12, 0.08, 0.22, 4, 4, 4);
        const foot = new THREE.Mesh(footGeometry, material);
        foot.position.set(dir * 0.12, -0.63, 0.06);
        foot.castShadow = true;
        bodyGroup.add(foot);
    }

    addAcupoints() {
        // Common acupoint positions for acupuncture
        const acupointData = {
            'GV20': { pos: [0, 1.82, 0], name: '~ | Baihui', color: 0xff4444 },
            'GB20': { pos: [-0.08, 1.65, -0.1], name: 'Î` | Fengchi', color: 0xff4444 },
            'LI4': { pos: [-0.5, 0.22, 0.08], name: '7 | Hegu', color: 0x4444ff },
            'PC6': { pos: [-0.42, 0.52, 0.07], name: '…s | Neiguan', color: 0x4444ff },
            'ST36': { pos: [-0.13, -0.15, 0.12], name: '³	Ì | Zusanli', color: 0x44ff44 },
            'SP6': { pos: [-0.13, -0.38, 0.06], name: '	4¤ | Sanyinjiao', color: 0x44ff44 },
            'LR3': { pos: [-0.12, -0.6, 0.12], name: '*² | Taichong', color: 0x44ff44 },
            'HT7': { pos: [-0.48, 0.24, 0.06], name: '^è | Shenmen', color: 0xff44ff },
        };

        Object.entries(acupointData).forEach(([code, data]) => {
            if (this.options.selectedPoints.includes(code)) {
                this.createAcupointMarker(data.pos, data.name, data.color);
            }
        });
    }

    createAcupointMarker(position, label, color) {
        // Glowing sphere for acupoint
        const markerGeometry = new THREE.SphereGeometry(0.025, 16, 16);
        const markerMaterial = new THREE.MeshStandardMaterial({
            color: color,
            emissive: color,
            emissiveIntensity: 0.5,
            roughness: 0.3,
            metalness: 0.2
        });
        const marker = new THREE.Mesh(markerGeometry, markerMaterial);
        marker.position.set(...position);
        marker.castShadow = true;

        // Add glow effect
        const glowGeometry = new THREE.SphereGeometry(0.035, 16, 16);
        const glowMaterial = new THREE.MeshBasicMaterial({
            color: color,
            transparent: true,
            opacity: 0.3
        });
        const glow = new THREE.Mesh(glowGeometry, glowMaterial);
        glow.position.set(...position);

        this.scene.add(marker);
        this.scene.add(glow);
        this.acupointMarkers.push({ marker, glow, label });

        // Animate glow
        const animate = () => {
            glow.scale.set(
                1 + 0.2 * Math.sin(Date.now() * 0.003),
                1 + 0.2 * Math.sin(Date.now() * 0.003),
                1 + 0.2 * Math.sin(Date.now() * 0.003)
            );
        };
        this.glowAnimations = this.glowAnimations || [];
        this.glowAnimations.push(animate);
    }

    addTreatmentAreas() {
        // Common treatment areas for tuina/massage
        const areaData = {
            'neck': { pos: [0, 1.58, -0.08], size: [0.2, 0.15, 0.1], name: 'ˆè | Neck', color: 0x4488ff },
            'shoulder-left': { pos: [-0.25, 1.4, 0], size: [0.15, 0.15, 0.15], name: 'æ© | Left Shoulder', color: 0xff8844 },
            'shoulder-right': { pos: [0.25, 1.4, 0], size: [0.15, 0.15, 0.15], name: 'ó© | Right Shoulder', color: 0xff8844 },
            'lower-back': { pos: [0, 0.85, -0.15], size: [0.3, 0.25, 0.1], name: 'Ìè | Lower Back', color: 0x44ff88 },
        };

        Object.entries(areaData).forEach(([code, data]) => {
            if (this.options.selectedAreas.includes(code)) {
                this.createTreatmentArea(data.pos, data.size, data.name, data.color);
            }
        });
    }

    createTreatmentArea(position, size, label, color) {
        const areaGeometry = new THREE.BoxGeometry(...size, 4, 4, 4);
        const areaMaterial = new THREE.MeshStandardMaterial({
            color: color,
            transparent: true,
            opacity: 0.3,
            roughness: 0.5,
            metalness: 0.1
        });
        const area = new THREE.Mesh(areaGeometry, areaMaterial);
        area.position.set(...position);

        this.scene.add(area);
        this.areaMarkers.push({ area, label });
    }

    addControlsUI() {
        const controlsDiv = document.createElement('div');
        controlsDiv.className = 'body-3d-controls';
        controlsDiv.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(255, 255, 255, 0.95);
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            font-size: 13px;
            z-index: 10;
        `;

        controlsDiv.innerHTML = `
            <div style="margin-bottom: 10px; font-weight: bold; color: #333;">
                ÆÒ§6 | View Controls
            </div>
            <button class="btn btn-sm btn-outline-primary mb-1 w-100" data-view="front">
                cb | Front
            </button>
            <button class="btn btn-sm btn-outline-primary mb-1 w-100" data-view="back">
                Ìb | Back
            </button>
            <button class="btn btn-sm btn-outline-primary mb-1 w-100" data-view="side">
                §b | Side
            </button>
            <button class="btn btn-sm btn-outline-secondary w-100" data-view="reset">
                Ín | Reset
            </button>
            <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #ddd; font-size: 11px; color: #666;">
                =± Ö¨Ël | Drag to rotate<br>
                = Ún)> | Scroll to zoom
            </div>
        `;

        this.container.appendChild(controlsDiv);

        // Add click handlers
        controlsDiv.querySelectorAll('[data-view]').forEach(btn => {
            btn.addEventListener('click', () => {
                const view = btn.dataset.view;
                this.setView(view);
            });
        });
    }

    setView(view) {
        const duration = 1000;
        const start = {
            x: this.camera.position.x,
            y: this.camera.position.y,
            z: this.camera.position.z
        };

        let end;
        switch (view) {
            case 'front':
                end = { x: 0, y: 1.6, z: 4 };
                break;
            case 'back':
                end = { x: 0, y: 1.6, z: -4 };
                break;
            case 'side':
                end = { x: 4, y: 1.6, z: 0 };
                break;
            case 'reset':
                end = { x: 0, y: 1.6, z: 4 };
                break;
        }

        const startTime = Date.now();
        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = progress < 0.5
                ? 2 * progress * progress
                : -1 + (4 - 2 * progress) * progress;

            this.camera.position.x = start.x + (end.x - start.x) * eased;
            this.camera.position.y = start.y + (end.y - start.y) * eased;
            this.camera.position.z = start.z + (end.z - start.z) * eased;
            this.camera.lookAt(0, 1, 0);

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        animate();
    }

    onWindowResize() {
        const width = this.container.clientWidth;
        const height = this.container.clientHeight;

        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        // Animate glowing markers
        if (this.glowAnimations) {
            this.glowAnimations.forEach(fn => fn());
        }

        // Update controls
        if (this.controls) {
            this.controls.update();
        }

        // Render scene
        this.renderer.render(this.scene, this.camera);
    }

    // Public API methods
    selectAcupoint(code) {
        if (!this.options.selectedPoints.includes(code)) {
            this.options.selectedPoints.push(code);
            this.clearMarkers();
            this.addAcupoints();
        }
    }

    deselectAcupoint(code) {
        const index = this.options.selectedPoints.indexOf(code);
        if (index > -1) {
            this.options.selectedPoints.splice(index, 1);
            this.clearMarkers();
            this.addAcupoints();
        }
    }

    selectArea(code) {
        if (!this.options.selectedAreas.includes(code)) {
            this.options.selectedAreas.push(code);
            this.clearAreas();
            this.addTreatmentAreas();
        }
    }

    clearMarkers() {
        this.acupointMarkers.forEach(({ marker, glow }) => {
            this.scene.remove(marker);
            this.scene.remove(glow);
        });
        this.acupointMarkers = [];
        this.glowAnimations = [];
    }

    clearAreas() {
        this.areaMarkers.forEach(({ area }) => {
            this.scene.remove(area);
        });
        this.areaMarkers = [];
    }
}

// Make available globally
window.Body3DViewerEnhanced = Body3DViewerEnhanced;
