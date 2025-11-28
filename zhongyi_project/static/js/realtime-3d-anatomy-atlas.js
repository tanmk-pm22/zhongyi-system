/**
 * Real-Time 3D Anatomy Atlas
 * 实时3D解剖图谱
 *
 * Based on professional 3D anatomy exploration systems
 * Inspired by Dr. R. Blanco Salado's 3D Anatomy Atlas
 *
 * Features:
 * - Real-time 3D interaction
 * - Layer peeling (skin → muscles → skeleton)
 * - Clickable anatomical structures
 * - Professional medical-grade rendering
 */

class RealTime3DAnatomyAtlas {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error('容器未找到 | Container not found:', containerId);
            return;
        }

        this.options = {
            mode: 'acupuncture', // 'acupuncture' or 'tuina'
            showAcupoints: true,
            showMuscles: true,
            showSkeleton: false,
            enableLayerPeeling: true,
            enableRealTimeRotation: true,
            selectedPoints: options.selectedPoints || [],
            selectedAreas: options.selectedAreas || [],
            ...options
        };

        // Current state
        this.currentLayer = 'muscles'; // 'skin', 'muscles', 'skeleton'
        this.layerOpacity = {
            skin: 1.0,
            muscles: 1.0,
            skeleton: 0.0
        };

        this.isRotating = false;
        this.rotationSpeed = 0.001;

        this.init();
    }

    init() {
        console.log('初始化实时3D解剖图谱 | Initializing Real-Time 3D Anatomy Atlas');

        if (typeof THREE === 'undefined') {
            console.error('Three.js未加载 | Three.js not loaded');
            this.showError('需要Three.js库 | Three.js library required');
            return;
        }

        this.setupUI();
        this.setupScene();
        this.setupCamera();
        this.setupLights();
        this.setupRenderer();
        this.setupControls();
        this.createAnatomicalBody();
        this.addAcupointMarkers();
        this.animate();

        console.log('✓ 实时3D解剖图谱已初始化 | Real-Time 3D Anatomy Atlas initialized');
    }

    setupUI() {
        this.container.innerHTML = `
            <div class="realtime-3d-container" style="position: relative; width: 100%; height: 700px; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 12px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.3);">

                <!-- Top Control Bar -->
                <div class="top-controls" style="position: absolute; top: 15px; left: 15px; right: 15px; z-index: 100; display: flex; justify-content: space-between; align-items: center;">
                    <div style="background: rgba(0,0,0,0.85); padding: 12px 20px; border-radius: 8px; backdrop-filter: blur(10px);">
                        <h5 style="margin: 0; color: #fff; font-size: 16px; font-weight: 600;">
                            <i class="bi bi-grid-3x3"></i> 实时3D解剖图谱 | Real-Time 3D Anatomy Atlas
                        </h5>
                    </div>

                    <div style="background: rgba(0,0,0,0.85); padding: 8px 15px; border-radius: 8px; backdrop-filter: blur(10px);">
                        <button class="btn btn-sm btn-outline-light" id="resetView" style="margin-right: 8px;">
                            <i class="bi bi-arrow-clockwise"></i> 重置视图 | Reset
                        </button>
                        <button class="btn btn-sm ${this.isRotating ? 'btn-warning' : 'btn-outline-light'}" id="toggleRotation">
                            <i class="bi bi-arrow-repeat"></i> ${this.isRotating ? '停止旋转' : '自动旋转'}
                        </button>
                    </div>
                </div>

                <!-- Layer Peeling Controls -->
                <div class="layer-controls" style="position: absolute; left: 15px; top: 80px; z-index: 100; background: rgba(0,0,0,0.85); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px); width: 280px;">
                    <h6 style="color: #fff; margin: 0 0 15px 0; font-size: 14px; font-weight: 600;">
                        <i class="bi bi-layers"></i> 图层控制 | Layer Peeling
                    </h6>

                    <!-- Skin Layer -->
                    <div class="mb-3">
                        <label style="color: #ffd7ba; font-size: 12px; display: block; margin-bottom: 5px;">
                            皮肤层 | Skin Layer
                        </label>
                        <input type="range" class="form-range" id="skinOpacity" min="0" max="100" value="100"
                               style="width: 100%;">
                        <div style="display: flex; justify-content: space-between; color: #888; font-size: 10px;">
                            <span>透明 | Transparent</span>
                            <span>不透明 | Opaque</span>
                        </div>
                    </div>

                    <!-- Muscles Layer -->
                    <div class="mb-3">
                        <label style="color: #ff6b6b; font-size: 12px; display: block; margin-bottom: 5px;">
                            肌肉层 | Muscles Layer
                        </label>
                        <input type="range" class="form-range" id="musclesOpacity" min="0" max="100" value="100">
                        <div style="display: flex; justify-content: space-between; color: #888; font-size: 10px;">
                            <span>透明 | Transparent</span>
                            <span>不透明 | Opaque</span>
                        </div>
                    </div>

                    <!-- Skeleton Layer -->
                    <div class="mb-3">
                        <label style="color: #e8d4b8; font-size: 12px; display: block; margin-bottom: 5px;">
                            骨骼层 | Skeleton Layer
                        </label>
                        <input type="range" class="form-range" id="skeletonOpacity" min="0" max="100" value="0">
                        <div style="display: flex; justify-content: space-between; color: #888; font-size: 10px;">
                            <span>隐藏 | Hidden</span>
                            <span>显示 | Visible</span>
                        </div>
                    </div>

                    <!-- Quick Presets -->
                    <div class="mt-3 pt-3" style="border-top: 1px solid rgba(255,255,255,0.1);">
                        <label style="color: #fff; font-size: 12px; display: block; margin-bottom: 8px;">
                            快速预设 | Quick Presets
                        </label>
                        <div class="btn-group-vertical" style="width: 100%;">
                            <button class="btn btn-sm btn-outline-light preset-btn" data-preset="surface">
                                <i class="bi bi-person"></i> 体表 | Surface
                            </button>
                            <button class="btn btn-sm btn-outline-light preset-btn" data-preset="muscles">
                                <i class="bi bi-heart-pulse"></i> 肌肉 | Muscles
                            </button>
                            <button class="btn btn-sm btn-outline-light preset-btn" data-preset="skeleton">
                                <i class="bi bi-person-arms-up"></i> 骨骼 | Skeleton
                            </button>
                            <button class="btn btn-sm btn-outline-light preset-btn" data-preset="xray">
                                <i class="bi bi-transparency"></i> X光 | X-Ray
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 3D Canvas -->
                <div id="canvas3d" style="width: 100%; height: 100%;"></div>

                <!-- Info Panel -->
                <div class="info-panel" style="position: absolute; bottom: 15px; left: 15px; right: 15px; background: rgba(0,0,0,0.9); padding: 15px 20px; border-radius: 8px; backdrop-filter: blur(10px); z-index: 100;">
                    <div id="anatomyInfo" style="color: #fff; font-size: 13px;">
                        <i class="bi bi-hand-index"></i>
                        <strong>交互提示 | Interaction:</strong>
                        拖动旋转 | Drag to rotate •
                        滚轮缩放 | Scroll to zoom •
                        点击选择穴位 | Click acupoints to select
                    </div>
                </div>

                <!-- Loading Indicator -->
                <div id="loadingIndicator" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #fff; text-align: center; z-index: 200;">
                    <div class="spinner-border text-light" role="status" style="width: 3rem; height: 3rem;">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div style="margin-top: 15px; font-size: 14px;">加载3D解剖模型... | Loading 3D Anatomy Model...</div>
                </div>
            </div>
        `;

        this.canvas3d = document.getElementById('canvas3d');
        this.infoPanel = document.getElementById('anatomyInfo');
        this.loadingIndicator = document.getElementById('loadingIndicator');
    }

    setupScene() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x1a1a2e);

        // Add fog for depth perception
        this.scene.fog = new THREE.Fog(0x1a1a2e, 5, 15);
    }

    setupCamera() {
        const aspect = this.canvas3d.clientWidth / this.canvas3d.clientHeight;
        this.camera = new THREE.PerspectiveCamera(50, aspect, 0.1, 1000);
        this.camera.position.set(0, 1.5, 4);
        this.camera.lookAt(0, 1, 0);
    }

    setupLights() {
        // Professional medical lighting setup

        // Key light (main light)
        const keyLight = new THREE.DirectionalLight(0xffffff, 1.5);
        keyLight.position.set(5, 8, 5);
        keyLight.castShadow = true;
        keyLight.shadow.mapSize.width = 2048;
        keyLight.shadow.mapSize.height = 2048;
        keyLight.shadow.camera.near = 0.5;
        keyLight.shadow.camera.far = 50;
        this.scene.add(keyLight);

        // Fill light
        const fillLight = new THREE.DirectionalLight(0x4a90e2, 0.6);
        fillLight.position.set(-5, 3, -5);
        this.scene.add(fillLight);

        // Back light
        const backLight = new THREE.DirectionalLight(0xffa07a, 0.4);
        backLight.position.set(0, 3, -5);
        this.scene.add(backLight);

        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404060, 0.7);
        this.scene.add(ambientLight);

        // Hemisphere light for natural ambient
        const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.5);
        hemiLight.position.set(0, 20, 0);
        this.scene.add(hemiLight);

        // Rim lights for better definition
        const rimLight1 = new THREE.SpotLight(0x00d9ff, 0.8, 20, Math.PI / 6, 0.5);
        rimLight1.position.set(-3, 5, 0);
        this.scene.add(rimLight1);

        const rimLight2 = new THREE.SpotLight(0xff6b9d, 0.8, 20, Math.PI / 6, 0.5);
        rimLight2.position.set(3, 5, 0);
        this.scene.add(rimLight2);
    }

    setupRenderer() {
        this.renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true,
            powerPreference: 'high-performance'
        });
        this.renderer.setSize(this.canvas3d.clientWidth, this.canvas3d.clientHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.renderer.outputEncoding = THREE.sRGBEncoding;
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1.2;

        this.canvas3d.appendChild(this.renderer.domElement);

        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());

        // Hide loading indicator
        setTimeout(() => {
            if (this.loadingIndicator) {
                this.loadingIndicator.style.display = 'none';
            }
        }, 500);
    }

    setupControls() {
        if (typeof THREE.OrbitControls === 'undefined') {
            console.warn('OrbitControls not available');
            return;
        }

        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.minDistance = 2;
        this.controls.maxDistance = 8;
        this.controls.target.set(0, 1, 0);
        this.controls.maxPolarAngle = Math.PI;
        this.controls.enablePan = true;
        this.controls.panSpeed = 0.5;

        // Setup UI controls
        this.setupUIControls();
    }

    setupUIControls() {
        // Layer opacity sliders
        document.getElementById('skinOpacity').addEventListener('input', (e) => {
            this.layerOpacity.skin = e.target.value / 100;
            this.updateLayerVisibility();
        });

        document.getElementById('musclesOpacity').addEventListener('input', (e) => {
            this.layerOpacity.muscles = e.target.value / 100;
            this.updateLayerVisibility();
        });

        document.getElementById('skeletonOpacity').addEventListener('input', (e) => {
            this.layerOpacity.skeleton = e.target.value / 100;
            this.updateLayerVisibility();
        });

        // Reset view button
        document.getElementById('resetView').addEventListener('click', () => {
            this.resetCamera();
        });

        // Toggle rotation button
        document.getElementById('toggleRotation').addEventListener('click', (e) => {
            this.isRotating = !this.isRotating;
            e.target.innerHTML = this.isRotating ?
                '<i class="bi bi-pause-circle"></i> 停止旋转 | Stop' :
                '<i class="bi bi-arrow-repeat"></i> 自动旋转 | Rotate';
            e.target.className = this.isRotating ?
                'btn btn-sm btn-warning' :
                'btn btn-sm btn-outline-light';
        });

        // Preset buttons
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const preset = e.currentTarget.dataset.preset;
                this.applyPreset(preset);
            });
        });

        // Click detection for acupoints
        this.renderer.domElement.addEventListener('click', (e) => {
            this.onCanvasClick(e);
        });
    }

    createAnatomicalBody() {
        this.bodyGroup = new THREE.Group();

        // Create skin layer
        this.createSkinLayer();

        // Create muscle layer
        this.createMuscleLayer();

        // Create skeleton layer
        this.createSkeletonLayer();

        this.scene.add(this.bodyGroup);
    }

    createSkinLayer() {
        const skinMaterial = new THREE.MeshStandardMaterial({
            color: 0xffd7ba,
            roughness: 0.7,
            metalness: 0.0,
            transparent: true,
            opacity: 1.0,
            side: THREE.DoubleSide
        });

        this.skinLayer = new THREE.Group();
        this.skinLayer.name = 'skinLayer';

        // Head
        const headGeo = new THREE.SphereGeometry(0.14, 48, 48);
        const head = new THREE.Mesh(headGeo, skinMaterial);
        head.position.y = 1.75;
        head.scale.set(1, 1.15, 1);
        head.castShadow = true;
        head.receiveShadow = true;
        this.skinLayer.add(head);

        // Neck
        const neckGeo = new THREE.CylinderGeometry(0.07, 0.085, 0.25, 32);
        const neck = new THREE.Mesh(neckGeo, skinMaterial);
        neck.position.y = 1.55;
        neck.castShadow = true;
        this.skinLayer.add(neck);

        // Torso
        const torsoGeo = new THREE.CapsuleGeometry(0.2, 0.7, 32, 64);
        const torso = new THREE.Mesh(torsoGeo, skinMaterial);
        torso.position.y = 1.1;
        torso.scale.set(1.2, 1, 0.7);
        torso.castShadow = true;
        this.skinLayer.add(torso);

        // Arms
        const armGeo = new THREE.CapsuleGeometry(0.04, 0.5, 16, 32);

        const leftArm = new THREE.Mesh(armGeo, skinMaterial);
        leftArm.position.set(-0.3, 1.2, 0);
        leftArm.rotation.z = Math.PI / 6;
        leftArm.castShadow = true;
        this.skinLayer.add(leftArm);

        const rightArm = new THREE.Mesh(armGeo, skinMaterial);
        rightArm.position.set(0.3, 1.2, 0);
        rightArm.rotation.z = -Math.PI / 6;
        rightArm.castShadow = true;
        this.skinLayer.add(rightArm);

        // Legs
        const legGeo = new THREE.CapsuleGeometry(0.06, 0.8, 16, 32);

        const leftLeg = new THREE.Mesh(legGeo, skinMaterial);
        leftLeg.position.set(-0.12, 0.4, 0);
        leftLeg.castShadow = true;
        this.skinLayer.add(leftLeg);

        const rightLeg = new THREE.Mesh(legGeo, skinMaterial);
        rightLeg.position.set(0.12, 0.4, 0);
        rightLeg.castShadow = true;
        this.skinLayer.add(rightLeg);

        this.bodyGroup.add(this.skinLayer);
    }

    createMuscleLayer() {
        const muscleMaterial = new THREE.MeshStandardMaterial({
            color: 0xc85555,
            roughness: 0.8,
            metalness: 0.1,
            transparent: true,
            opacity: 1.0
        });

        this.muscleLayer = new THREE.Group();
        this.muscleLayer.name = 'muscleLayer';

        // Pectoralis Major (chest muscles)
        const pectoralGeo = new THREE.SphereGeometry(0.09, 32, 32);

        const pecLeft = new THREE.Mesh(pectoralGeo, muscleMaterial);
        pecLeft.position.set(-0.09, 1.35, 0.16);
        pecLeft.scale.set(1, 1.2, 0.5);
        pecLeft.castShadow = true;
        this.muscleLayer.add(pecLeft);

        const pecRight = new THREE.Mesh(pectoralGeo, muscleMaterial);
        pecRight.position.set(0.09, 1.35, 0.16);
        pecRight.scale.set(1, 1.2, 0.5);
        pecRight.castShadow = true;
        this.muscleLayer.add(pecRight);

        // Rectus Abdominis (6-pack)
        for (let i = 0; i < 3; i++) {
            const abGeo = new THREE.BoxGeometry(0.08, 0.12, 0.04, 8, 8, 4);
            const yPos = 1.15 - i * 0.15;

            const abLeft = new THREE.Mesh(abGeo, muscleMaterial);
            abLeft.position.set(-0.06, yPos, 0.18);
            abLeft.castShadow = true;
            this.muscleLayer.add(abLeft);

            const abRight = new THREE.Mesh(abGeo, muscleMaterial);
            abRight.position.set(0.06, yPos, 0.18);
            abRight.castShadow = true;
            this.muscleLayer.add(abRight);
        }

        // Deltoids (shoulders)
        const deltoidGeo = new THREE.SphereGeometry(0.08, 32, 32);

        const deltoidLeft = new THREE.Mesh(deltoidGeo, muscleMaterial);
        deltoidLeft.position.set(-0.25, 1.4, 0);
        deltoidLeft.castShadow = true;
        this.muscleLayer.add(deltoidLeft);

        const deltoidRight = new THREE.Mesh(deltoidGeo, muscleMaterial);
        deltoidRight.position.set(0.25, 1.4, 0);
        deltoidRight.castShadow = true;
        this.muscleLayer.add(deltoidRight);

        // Quadriceps (thigh muscles)
        const quadGeo = new THREE.CylinderGeometry(0.08, 0.07, 0.4, 32);

        const quadLeft = new THREE.Mesh(quadGeo, muscleMaterial);
        quadLeft.position.set(-0.12, 0.5, 0.05);
        quadLeft.castShadow = true;
        this.muscleLayer.add(quadLeft);

        const quadRight = new THREE.Mesh(quadGeo, muscleMaterial);
        quadRight.position.set(0.12, 0.5, 0.05);
        quadRight.castShadow = true;
        this.muscleLayer.add(quadRight);

        // Initially hidden, will show when peeling skin
        this.muscleLayer.visible = true;
        this.bodyGroup.add(this.muscleLayer);
    }

    createSkeletonLayer() {
        const boneMaterial = new THREE.MeshStandardMaterial({
            color: 0xe8d4b8,
            roughness: 0.6,
            metalness: 0.2,
            transparent: true,
            opacity: 0.0
        });

        this.skeletonLayer = new THREE.Group();
        this.skeletonLayer.name = 'skeletonLayer';

        // Skull
        const skullGeo = new THREE.SphereGeometry(0.12, 32, 32);
        const skull = new THREE.Mesh(skullGeo, boneMaterial);
        skull.position.y = 1.75;
        skull.castShadow = true;
        this.skeletonLayer.add(skull);

        // Spine
        for (let i = 0; i < 12; i++) {
            const vertebraGeo = new THREE.CylinderGeometry(0.025, 0.03, 0.04, 16);
            const vertebra = new THREE.Mesh(vertebraGeo, boneMaterial);
            vertebra.position.y = 1.5 - i * 0.08;
            vertebra.castShadow = true;
            this.skeletonLayer.add(vertebra);
        }

        // Ribs
        const ribMaterial = boneMaterial.clone();
        for (let i = 0; i < 8; i++) {
            const ribGeo = new THREE.TorusGeometry(0.12, 0.008, 8, 24, Math.PI);
            const yPos = 1.4 - i * 0.06;

            const ribLeft = new THREE.Mesh(ribGeo, ribMaterial);
            ribLeft.position.set(-0.06, yPos, 0);
            ribLeft.rotation.y = -Math.PI / 2;
            ribLeft.rotation.z = -Math.PI / 12;
            this.skeletonLayer.add(ribLeft);

            const ribRight = new THREE.Mesh(ribGeo, ribMaterial);
            ribRight.position.set(0.06, yPos, 0);
            ribRight.rotation.y = Math.PI / 2;
            ribRight.rotation.z = Math.PI / 12;
            this.skeletonLayer.add(ribRight);
        }

        // Femur (thigh bones)
        const femurGeo = new THREE.CylinderGeometry(0.03, 0.025, 0.5, 16);

        const femurLeft = new THREE.Mesh(femurGeo, boneMaterial);
        femurLeft.position.set(-0.12, 0.5, 0);
        femurLeft.castShadow = true;
        this.skeletonLayer.add(femurLeft);

        const femurRight = new THREE.Mesh(femurGeo, boneMaterial);
        femurRight.position.set(0.12, 0.5, 0);
        femurRight.castShadow = true;
        this.skeletonLayer.add(femurRight);

        this.bodyGroup.add(this.skeletonLayer);
    }

    addAcupointMarkers() {
        if (this.options.mode !== 'acupuncture') return;

        this.acupointMarkers = new THREE.Group();
        this.acupointMarkers.name = 'acupointMarkers';

        // Sample acupoints with 3D positions
        const acupoints = [
            { code: 'GV20', name: '百会', position: [0, 1.89, 0], color: 0xff0000 },
            { code: 'CV17', name: '膻中', position: [0, 1.35, 0.21], color: 0xff4444 },
            { code: 'CV12', name: '中脘', position: [0, 1.1, 0.22], color: 0xff4444 },
            { code: 'CV6', name: '气海', position: [0, 0.9, 0.22], color: 0xff4444 },
            { code: 'ST36', name: '足三里', position: [-0.12, 0.35, 0.08], color: 0xffaa00 },
            { code: 'LI4', name: '合谷', position: [-0.35, 0.95, 0.05], color: 0x00aaff },
        ];

        acupoints.forEach(point => {
            const markerGeo = new THREE.SphereGeometry(0.015, 16, 16);
            const markerMat = new THREE.MeshStandardMaterial({
                color: point.color,
                emissive: point.color,
                emissiveIntensity: 0.5,
                roughness: 0.3,
                metalness: 0.7
            });

            const marker = new THREE.Mesh(markerGeo, markerMat);
            marker.position.set(...point.position);
            marker.userData = {
                code: point.code,
                name: point.name,
                type: 'acupoint'
            };

            // Add glow effect
            const glowGeo = new THREE.SphereGeometry(0.025, 16, 16);
            const glowMat = new THREE.MeshBasicMaterial({
                color: point.color,
                transparent: true,
                opacity: 0.3
            });
            const glow = new THREE.Mesh(glowGeo, glowMat);
            marker.add(glow);

            this.acupointMarkers.add(marker);
        });

        this.scene.add(this.acupointMarkers);
    }

    updateLayerVisibility() {
        if (!this.skinLayer || !this.muscleLayer || !this.skeletonLayer) return;

        // Update skin layer opacity
        this.skinLayer.children.forEach(mesh => {
            if (mesh.material) {
                mesh.material.opacity = this.layerOpacity.skin;
                mesh.material.transparent = true;
            }
        });

        // Update muscle layer opacity
        this.muscleLayer.children.forEach(mesh => {
            if (mesh.material) {
                mesh.material.opacity = this.layerOpacity.muscles;
                mesh.material.transparent = true;
            }
        });

        // Update skeleton layer opacity
        this.skeletonLayer.children.forEach(mesh => {
            if (mesh.material) {
                mesh.material.opacity = this.layerOpacity.skeleton;
                mesh.material.transparent = true;
            }
        });
    }

    applyPreset(preset) {
        const sliders = {
            skin: document.getElementById('skinOpacity'),
            muscles: document.getElementById('musclesOpacity'),
            skeleton: document.getElementById('skeletonOpacity')
        };

        switch(preset) {
            case 'surface':
                this.animateSlider(sliders.skin, 100);
                this.animateSlider(sliders.muscles, 0);
                this.animateSlider(sliders.skeleton, 0);
                break;
            case 'muscles':
                this.animateSlider(sliders.skin, 20);
                this.animateSlider(sliders.muscles, 100);
                this.animateSlider(sliders.skeleton, 0);
                break;
            case 'skeleton':
                this.animateSlider(sliders.skin, 0);
                this.animateSlider(sliders.muscles, 20);
                this.animateSlider(sliders.skeleton, 100);
                break;
            case 'xray':
                this.animateSlider(sliders.skin, 10);
                this.animateSlider(sliders.muscles, 30);
                this.animateSlider(sliders.skeleton, 80);
                break;
        }
    }

    animateSlider(slider, targetValue) {
        const currentValue = parseInt(slider.value);
        const step = (targetValue - currentValue) / 20;
        let current = currentValue;

        const interval = setInterval(() => {
            current += step;
            if ((step > 0 && current >= targetValue) || (step < 0 && current <= targetValue)) {
                current = targetValue;
                clearInterval(interval);
            }
            slider.value = Math.round(current);
            slider.dispatchEvent(new Event('input'));
        }, 20);
    }

    resetCamera() {
        this.camera.position.set(0, 1.5, 4);
        this.controls.target.set(0, 1, 0);
        this.controls.update();
    }

    onCanvasClick(event) {
        // Raycasting for click detection
        const rect = this.renderer.domElement.getBoundingClientRect();
        const mouse = new THREE.Vector2();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(mouse, this.camera);

        if (this.acupointMarkers) {
            const intersects = raycaster.intersectObjects(this.acupointMarkers.children, true);

            if (intersects.length > 0) {
                const point = intersects[0].object;
                if (point.userData && point.userData.type === 'acupoint') {
                    this.selectAcupoint(point.userData);
                }
            }
        }
    }

    selectAcupoint(pointData) {
        console.log('选择穴位 | Selected acupoint:', pointData.code, pointData.name);

        // Update info panel
        this.infoPanel.innerHTML = `
            <strong style="color: #ffd700;">${pointData.code} - ${pointData.name}</strong><br>
            <span style="color: #ccc; font-size: 12px;">点击已选择 | Acupoint selected</span>
        `;

        // Add to selected points
        if (!this.options.selectedPoints.includes(pointData.code)) {
            this.options.selectedPoints.push(pointData.code);
        }

        // Dispatch event for form integration
        this.container.dispatchEvent(new CustomEvent('pointsSelected', {
            detail: { points: this.options.selectedPoints }
        }));
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        // Auto-rotation
        if (this.isRotating && this.bodyGroup) {
            this.bodyGroup.rotation.y += this.rotationSpeed;
        }

        // Update controls
        if (this.controls) {
            this.controls.update();
        }

        // Animate acupoint markers (pulsing effect)
        if (this.acupointMarkers) {
            const time = Date.now() * 0.002;
            this.acupointMarkers.children.forEach((marker, i) => {
                const scale = 1 + Math.sin(time + i) * 0.2;
                marker.scale.set(scale, scale, scale);
            });
        }

        this.renderer.render(this.scene, this.camera);
    }

    onWindowResize() {
        const width = this.canvas3d.clientWidth;
        const height = this.canvas3d.clientHeight;

        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }

    showError(message) {
        this.container.innerHTML = `
            <div style="padding: 40px; text-align: center; color: #ff6b6b;">
                <i class="bi bi-exclamation-triangle" style="font-size: 48px;"></i>
                <h4 style="margin-top: 20px;">错误 | Error</h4>
                <p>${message}</p>
            </div>
        `;
    }

    // Public API
    getSelectedPoints() {
        return this.options.selectedPoints;
    }

    setLayerOpacity(layer, opacity) {
        this.layerOpacity[layer] = opacity;
        this.updateLayerVisibility();
    }

    dispose() {
        if (this.renderer) {
            this.renderer.dispose();
        }
        if (this.controls) {
            this.controls.dispose();
        }
    }
}

// Make available globally
window.RealTime3DAnatomyAtlas = RealTime3DAnatomyAtlas;
