/**
 * Three.js Realistic 3D Human Body Viewer
 * 真实人体3D图解查看器（Three.js版本）
 *
 * Features:
 * - Full 3D human body model with realistic proportions
 * - Interactive rotation, zoom, and pan controls
 * - 3D acupoint markers with labels
 * - Anatomically accurate positioning
 * - Professional medical visualization
 *
 * Dependencies: Three.js (loaded via CDN)
 */

class Body3DViewerThreeJS {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error('容器未找到 | Container not found:', containerId);
            return;
        }

        this.options = {
            showAcupoints: options.showAcupoints || false,
            showMuscles: options.showMuscles || false,
            selectedPoints: options.selectedPoints || [],
            selectedAreas: options.selectedAreas || [],
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
            console.log('等待Three.js加载... | Waiting for Three.js to load...');
            setTimeout(() => this.initWhenReady(), 100);
            return;
        }
        this.init();
    }

    init() {
        // Create scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0xf0f4f8);

        // Create camera
        const width = this.container.clientWidth || 800;
        const height = this.container.clientHeight || 600;
        this.camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
        this.camera.position.set(0, 1.5, 5);
        this.camera.lookAt(0, 1, 0);

        // Create renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.renderer.setSize(width, height);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);

        // Add lights
        this.addLights();

        // Add controls
        this.addControls();

        // Create human body
        this.createHumanBody();

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

        // Add interaction controls UI
        this.addControlsUI();

        // Start animation loop
        this.animate();

        console.log('Three.js 真实3D人体图解已初始化 | Three.js 3D Body Viewer initialized');
    }

    addLights() {
        // Ambient light for overall illumination
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);

        // Main directional light (sunlight)
        const mainLight = new THREE.DirectionalLight(0xffffff, 0.8);
        mainLight.position.set(5, 10, 5);
        mainLight.castShadow = true;
        mainLight.shadow.camera.left = -5;
        mainLight.shadow.camera.right = 5;
        mainLight.shadow.camera.top = 5;
        mainLight.shadow.camera.bottom = -5;
        mainLight.shadow.mapSize.width = 2048;
        mainLight.shadow.mapSize.height = 2048;
        this.scene.add(mainLight);

        // Fill light from the side
        const fillLight = new THREE.DirectionalLight(0xffffff, 0.3);
        fillLight.position.set(-5, 5, 5);
        this.scene.add(fillLight);

        // Rim light from behind
        const rimLight = new THREE.DirectionalLight(0xffffff, 0.2);
        rimLight.position.set(0, 5, -5);
        this.scene.add(rimLight);

        // Hemisphere light for better color
        const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.3);
        hemiLight.position.set(0, 20, 0);
        this.scene.add(hemiLight);
    }

    addControls() {
        // OrbitControls for camera rotation
        if (typeof THREE.OrbitControls !== 'undefined') {
            this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
            this.controls.enableDamping = true;
            this.controls.dampingFactor = 0.05;
            this.controls.target.set(0, 1, 0);
            this.controls.minDistance = 2;
            this.controls.maxDistance = 10;
            this.controls.maxPolarAngle = Math.PI * 0.9;
        }
    }

    createHumanBody() {
        const bodyGroup = new THREE.Group();
        bodyGroup.name = 'humanBody';

        // Skin material - realistic skin tone
        const skinMaterial = new THREE.MeshPhongMaterial({
            color: 0xffd4a3,
            specular: 0x333333,
            shininess: 15,
            flatShading: false
        });

        const muscleMaterial = new THREE.MeshPhongMaterial({
            color: 0xcc8866,
            specular: 0x222222,
            shininess: 10,
            transparent: true,
            opacity: 0.7
        });

        // HEAD
        const headGeometry = new THREE.SphereGeometry(0.15, 32, 32);
        const head = new THREE.Mesh(headGeometry, skinMaterial);
        head.position.y = 1.75;
        head.scale.set(1, 1.1, 1);
        head.castShadow = true;
        bodyGroup.add(head);

        // NECK
        const neckGeometry = new THREE.CylinderGeometry(0.08, 0.1, 0.2, 16);
        const neck = new THREE.Mesh(neckGeometry, skinMaterial);
        neck.position.y = 1.55;
        neck.castShadow = true;
        bodyGroup.add(neck);

        // TORSO (chest and abdomen)
        const torsoGeometry = new THREE.CapsuleGeometry(0.2, 0.6, 16, 32);
        const torso = new THREE.Mesh(torsoGeometry, skinMaterial);
        torso.position.y = 1.1;
        torso.castShadow = true;
        bodyGroup.add(torso);

        // CHEST MUSCLES (if showing muscles)
        if (this.options.showMuscles || !this.options.showAcupoints) {
            const chestLeftGeometry = new THREE.SphereGeometry(0.12, 16, 16);
            const chestLeft = new THREE.Mesh(chestLeftGeometry, muscleMaterial);
            chestLeft.position.set(-0.1, 1.3, 0.15);
            chestLeft.scale.set(1, 1, 0.7);
            bodyGroup.add(chestLeft);

            const chestRight = new THREE.Mesh(chestLeftGeometry, muscleMaterial);
            chestRight.position.set(0.1, 1.3, 0.15);
            chestRight.scale.set(1, 1, 0.7);
            bodyGroup.add(chestRight);

            // ABS
            for (let i = 0; i < 3; i++) {
                const absGeometry = new THREE.BoxGeometry(0.08, 0.12, 0.06, 2, 2, 2);
                const absLeft = new THREE.Mesh(absGeometry, muscleMaterial);
                absLeft.position.set(-0.06, 1.1 - i * 0.15, 0.18);
                bodyGroup.add(absLeft);

                const absRight = new THREE.Mesh(absGeometry, muscleMaterial);
                absRight.position.set(0.06, 1.1 - i * 0.15, 0.18);
                bodyGroup.add(absRight);
            }
        }

        // PELVIS/HIPS
        const pelvisGeometry = new THREE.SphereGeometry(0.18, 16, 16);
        const pelvis = new THREE.Mesh(pelvisGeometry, skinMaterial);
        pelvis.position.y = 0.7;
        pelvis.scale.set(1, 0.6, 1);
        pelvis.castShadow = true;
        bodyGroup.add(pelvis);

        // LEFT ARM
        const armGeometry = new THREE.CapsuleGeometry(0.05, 0.5, 8, 16);
        const leftUpperArm = new THREE.Mesh(armGeometry, skinMaterial);
        leftUpperArm.position.set(-0.3, 1.3, 0);
        leftUpperArm.rotation.z = Math.PI / 8;
        leftUpperArm.castShadow = true;
        bodyGroup.add(leftUpperArm);

        const leftForearm = new THREE.Mesh(armGeometry.clone(), skinMaterial);
        leftForearm.position.set(-0.42, 0.85, 0);
        leftForearm.rotation.z = Math.PI / 6;
        leftForearm.castShadow = true;
        bodyGroup.add(leftForearm);

        // LEFT HAND
        const handGeometry = new THREE.SphereGeometry(0.06, 12, 12);
        const leftHand = new THREE.Mesh(handGeometry, skinMaterial);
        leftHand.position.set(-0.52, 0.45, 0);
        leftHand.scale.set(1, 0.7, 0.5);
        leftHand.castShadow = true;
        bodyGroup.add(leftHand);

        // RIGHT ARM
        const rightUpperArm = new THREE.Mesh(armGeometry.clone(), skinMaterial);
        rightUpperArm.position.set(0.3, 1.3, 0);
        rightUpperArm.rotation.z = -Math.PI / 8;
        rightUpperArm.castShadow = true;
        bodyGroup.add(rightUpperArm);

        const rightForearm = new THREE.Mesh(armGeometry.clone(), skinMaterial);
        rightForearm.position.set(0.42, 0.85, 0);
        rightForearm.rotation.z = -Math.PI / 6;
        rightForearm.castShadow = true;
        bodyGroup.add(rightForearm);

        // RIGHT HAND
        const rightHand = new THREE.Mesh(handGeometry.clone(), skinMaterial);
        rightHand.position.set(0.52, 0.45, 0);
        rightHand.scale.set(1, 0.7, 0.5);
        rightHand.castShadow = true;
        bodyGroup.add(rightHand);

        // LEFT LEG
        const legGeometry = new THREE.CapsuleGeometry(0.08, 0.55, 12, 16);
        const leftThigh = new THREE.Mesh(legGeometry, skinMaterial);
        leftThigh.position.set(-0.12, 0.35, 0);
        leftThigh.castShadow = true;
        bodyGroup.add(leftThigh);

        const leftCalf = new THREE.Mesh(legGeometry.clone(), skinMaterial);
        leftCalf.position.set(-0.12, -0.25, 0);
        leftCalf.scale.set(0.9, 1, 0.9);
        leftCalf.castShadow = true;
        bodyGroup.add(leftCalf);

        // LEFT FOOT
        const footGeometry = new THREE.BoxGeometry(0.1, 0.08, 0.18);
        const leftFoot = new THREE.Mesh(footGeometry, skinMaterial);
        leftFoot.position.set(-0.12, -0.6, 0.05);
        leftFoot.castShadow = true;
        bodyGroup.add(leftFoot);

        // RIGHT LEG
        const rightThigh = new THREE.Mesh(legGeometry.clone(), skinMaterial);
        rightThigh.position.set(0.12, 0.35, 0);
        rightThigh.castShadow = true;
        bodyGroup.add(rightThigh);

        const rightCalf = new THREE.Mesh(legGeometry.clone(), skinMaterial);
        rightCalf.position.set(0.12, -0.25, 0);
        rightCalf.scale.set(0.9, 1, 0.9);
        rightCalf.castShadow = true;
        bodyGroup.add(rightCalf);

        // RIGHT FOOT
        const rightFoot = new THREE.Mesh(footGeometry.clone(), skinMaterial);
        rightFoot.position.set(0.12, -0.6, 0.05);
        rightFoot.castShadow = true;
        bodyGroup.add(rightFoot);

        // Add body group to scene
        this.scene.add(bodyGroup);
        this.bodyMesh = bodyGroup;

        // Add ground plane for shadow
        const groundGeometry = new THREE.PlaneGeometry(10, 10);
        const groundMaterial = new THREE.ShadowMaterial({ opacity: 0.2 });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.position.y = -0.65;
        ground.receiveShadow = true;
        this.scene.add(ground);
    }

    addAcupoints() {
        // Define anatomically accurate acupoint positions in 3D space
        const acupoints = [
            // HEAD
            { code: 'GV20', name: '百会', position: new THREE.Vector3(0, 1.9, 0) },

            // CHEST
            { code: 'CV17', name: '膻中', position: new THREE.Vector3(0, 1.3, 0.21) },
            { code: 'CV12', name: '中脘', position: new THREE.Vector3(0, 1.0, 0.21) },

            // ABDOMEN
            { code: 'CV4', name: '关元', position: new THREE.Vector3(0, 0.75, 0.19) },

            // ARMS (left and right)
            { code: 'LI4_L', name: '合谷(左)', position: new THREE.Vector3(-0.52, 0.5, 0.05) },
            { code: 'LI4_R', name: '合谷(右)', position: new THREE.Vector3(0.52, 0.5, 0.05) },
            { code: 'PC6_L', name: '内关(左)', position: new THREE.Vector3(-0.45, 0.7, 0.05) },
            { code: 'PC6_R', name: '内关(右)', position: new THREE.Vector3(0.45, 0.7, 0.05) },
            { code: 'HT7_L', name: '神门(左)', position: new THREE.Vector3(-0.5, 0.5, -0.05) },
            { code: 'HT7_R', name: '神门(右)', position: new THREE.Vector3(0.5, 0.5, -0.05) },

            // LEGS (left and right)
            { code: 'ST36_L', name: '足三里(左)', position: new THREE.Vector3(-0.15, -0.15, 0.1) },
            { code: 'ST36_R', name: '足三里(右)', position: new THREE.Vector3(0.15, -0.15, 0.1) },
            { code: 'SP6_L', name: '三阴交(左)', position: new THREE.Vector3(-0.15, -0.4, 0.05) },
            { code: 'SP6_R', name: '三阴交(右)', position: new THREE.Vector3(0.15, -0.4, 0.05) },
            { code: 'LR3_L', name: '太冲(左)', position: new THREE.Vector3(-0.12, -0.62, 0.15) },
            { code: 'LR3_R', name: '太冲(右)', position: new THREE.Vector3(0.12, -0.62, 0.15) },

            // BACK - will be added when we rotate
            { code: 'GB20_L', name: '风池(左)', position: new THREE.Vector3(-0.08, 1.65, -0.12) },
            { code: 'GB20_R', name: '风池(右)', position: new THREE.Vector3(0.08, 1.65, -0.12) },
            { code: 'BL23_L', name: '肾俞(左)', position: new THREE.Vector3(-0.08, 0.8, -0.2) },
            { code: 'BL23_R', name: '肾俞(右)', position: new THREE.Vector3(0.08, 0.8, -0.2) },
            { code: 'BL13_L', name: '肺俞(左)', position: new THREE.Vector3(-0.08, 1.25, -0.21) },
            { code: 'BL13_R', name: '肺俞(右)', position: new THREE.Vector3(0.08, 1.25, -0.21) },
        ];

        acupoints.forEach(point => {
            const isSelected = this.options.selectedPoints.includes(point.code);
            const marker = this.createAcupointMarker(point.code, point.name, point.position, isSelected);
            this.acupointMarkers.push(marker);
            this.scene.add(marker);
        });
    }

    createAcupointMarker(code, name, position, isSelected) {
        const group = new THREE.Group();
        group.userData = { code, name, type: 'acupoint' };
        group.position.copy(position);

        // Marker sphere
        const markerGeometry = new THREE.SphereGeometry(0.025, 16, 16);
        const markerMaterial = new THREE.MeshPhongMaterial({
            color: isSelected ? 0xc0392b : 0xe74c3c,
            emissive: isSelected ? 0xc0392b : 0xe74c3c,
            emissiveIntensity: 0.3,
            shininess: 100
        });
        const marker = new THREE.Mesh(markerGeometry, markerMaterial);
        marker.castShadow = true;
        group.add(marker);

        // Glow ring
        const ringGeometry = new THREE.RingGeometry(0.025, 0.04, 16);
        const ringMaterial = new THREE.MeshBasicMaterial({
            color: isSelected ? 0xc0392b : 0xe74c3c,
            transparent: true,
            opacity: 0.4,
            side: THREE.DoubleSide
        });
        const ring = new THREE.Mesh(ringGeometry, ringMaterial);
        ring.lookAt(this.camera.position);
        group.add(ring);

        // Text label (sprite)
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = 256;
        canvas.height = 128;

        context.fillStyle = 'rgba(255, 255, 255, 0.95)';
        context.fillRect(0, 0, canvas.width, canvas.height);

        context.strokeStyle = '#2c3e50';
        context.lineWidth = 2;
        context.strokeRect(0, 0, canvas.width, canvas.height);

        context.fillStyle = '#2c3e50';
        context.font = 'bold 32px Arial';
        context.textAlign = 'center';
        context.textBaseline = 'middle';
        context.fillText(name, 128, 50);

        context.font = '24px Arial';
        context.fillStyle = '#7f8c8d';
        context.fillText(code, 128, 90);

        const texture = new THREE.CanvasTexture(canvas);
        const spriteMaterial = new THREE.SpriteMaterial({
            map: texture,
            transparent: true,
            opacity: 0
        });
        const sprite = new THREE.Sprite(spriteMaterial);
        sprite.scale.set(0.3, 0.15, 1);
        sprite.position.y = 0.08;
        sprite.userData.isLabel = true;
        group.add(sprite);

        return group;
    }

    addTreatmentAreas() {
        // Treatment areas for Tuina massage
        const areas = [
            { code: 'neck', name: '颈部 Neck', position: new THREE.Vector3(0, 1.55, 0), size: [0.25, 0.2, 0.25], color: 0x2ecc71 },
            { code: 'shoulder_L', name: '肩部(左) Shoulder', position: new THREE.Vector3(-0.25, 1.35, 0), size: [0.2, 0.2, 0.2], color: 0x3498db },
            { code: 'shoulder_R', name: '肩部(右) Shoulder', position: new THREE.Vector3(0.25, 1.35, 0), size: [0.2, 0.2, 0.2], color: 0x3498db },
            { code: 'upper_back', name: '上背部 Upper Back', position: new THREE.Vector3(0, 1.2, -0.22), size: [0.35, 0.3, 0.1], color: 0x1abc9c },
            { code: 'lower_back', name: '腰部 Lower Back', position: new THREE.Vector3(0, 0.8, -0.21), size: [0.3, 0.25, 0.1], color: 0xf39c12 },
        ];

        areas.forEach(area => {
            const isSelected = this.options.selectedAreas.includes(area.code);
            const marker = this.createAreaMarker(area.code, area.name, area.position, area.size, area.color, isSelected);
            this.areaMarkers.push(marker);
            this.scene.add(marker);
        });
    }

    createAreaMarker(code, name, position, size, color, isSelected) {
        const group = new THREE.Group();
        group.userData = { code, name, type: 'area' };
        group.position.copy(position);

        // Area box
        const geometry = new THREE.BoxGeometry(...size);
        const material = new THREE.MeshPhongMaterial({
            color: color,
            transparent: true,
            opacity: isSelected ? 0.5 : 0.3,
            emissive: color,
            emissiveIntensity: isSelected ? 0.3 : 0.1
        });
        const box = new THREE.Mesh(geometry, material);
        group.add(box);

        // Wireframe
        const wireframe = new THREE.BoxHelper(box, color);
        wireframe.material.linewidth = 2;
        group.add(wireframe);

        return group;
    }

    addControlsUI() {
        const controlsDiv = document.createElement('div');
        controlsDiv.className = 'body-3d-controls mb-3 d-flex justify-content-between align-items-center';
        controlsDiv.style.position = 'absolute';
        controlsDiv.style.top = '10px';
        controlsDiv.style.left = '10px';
        controlsDiv.style.right = '10px';
        controlsDiv.style.zIndex = '100';

        controlsDiv.innerHTML = `
            <div class="btn-group btn-group-sm" role="group">
                <button type="button" class="btn btn-primary view-front">
                    <i class="bi bi-person"></i> 正面 | Front
                </button>
                <button type="button" class="btn btn-outline-primary view-back">
                    <i class="bi bi-person-fill"></i> 背面 | Back
                </button>
                <button type="button" class="btn btn-outline-primary view-side">
                    <i class="bi bi-person-lines-fill"></i> 侧面 | Side
                </button>
            </div>
            <div class="btn-group btn-group-sm" role="group">
                <button type="button" class="btn btn-outline-secondary reset-view" title="重置视角 | Reset View">
                    <i class="bi bi-arrow-clockwise"></i> 重置 | Reset
                </button>
            </div>
        `;

        this.container.style.position = 'relative';
        this.container.appendChild(controlsDiv);

        // Bind events
        controlsDiv.querySelector('.view-front').addEventListener('click', () => this.setView('front'));
        controlsDiv.querySelector('.view-back').addEventListener('click', () => this.setView('back'));
        controlsDiv.querySelector('.view-side').addEventListener('click', () => this.setView('side'));
        controlsDiv.querySelector('.reset-view').addEventListener('click', () => this.resetView());

        this.controlsDiv = controlsDiv;
    }

    setView(mode) {
        const duration = 1000; // Animation duration in ms
        const startPosition = this.camera.position.clone();
        const startTime = Date.now();

        let targetPosition;
        switch(mode) {
            case 'front':
                targetPosition = new THREE.Vector3(0, 1.5, 5);
                break;
            case 'back':
                targetPosition = new THREE.Vector3(0, 1.5, -5);
                break;
            case 'side':
                targetPosition = new THREE.Vector3(5, 1.5, 0);
                break;
        }

        // Update button states
        this.controlsDiv.querySelectorAll('.btn-group:first-child .btn').forEach(btn => {
            btn.classList.remove('btn-primary');
            btn.classList.add('btn-outline-primary');
        });
        this.controlsDiv.querySelector(`.view-${mode}`).classList.remove('btn-outline-primary');
        this.controlsDiv.querySelector(`.view-${mode}`).classList.add('btn-primary');

        // Animate camera
        const animate = () => {
            const now = Date.now();
            const progress = Math.min((now - startTime) / duration, 1);
            const eased = this.easeInOutCubic(progress);

            this.camera.position.lerpVectors(startPosition, targetPosition, eased);
            this.camera.lookAt(0, 1, 0);

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        animate();
    }

    resetView() {
        this.setView('front');
        if (this.controls) {
            this.controls.reset();
        }
    }

    easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
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

        // Update controls
        if (this.controls) {
            this.controls.update();
        }

        // Make labels face camera
        [...this.acupointMarkers, ...this.areaMarkers].forEach(marker => {
            marker.children.forEach(child => {
                if (child instanceof THREE.Sprite || child.userData.isLabel) {
                    child.lookAt(this.camera.position);
                }
            });
        });

        // Rotate rings to face camera
        this.acupointMarkers.forEach(marker => {
            const ring = marker.children.find(child => child.geometry instanceof THREE.RingGeometry);
            if (ring) {
                ring.lookAt(this.camera.position);
            }
        });

        this.renderer.render(this.scene, this.camera);
    }

    // Public API methods
    getAllAcupoints() {
        return [
            { code: 'LI4', name: '合谷' },
            { code: 'ST36', name: '足三里' },
            { code: 'LR3', name: '太冲' },
            { code: 'PC6', name: '内关' },
            { code: 'SP6', name: '三阴交' },
            { code: 'GB20', name: '风池' },
            { code: 'GV20', name: '百会' },
            { code: 'HT7', name: '神门' },
            { code: 'BL23', name: '肾俞' },
            { code: 'CV4', name: '关元' },
            { code: 'CV17', name: '膻中' },
            { code: 'BL13', name: '肺俞' },
        ];
    }

    dispose() {
        // Clean up resources
        if (this.renderer) {
            this.renderer.dispose();
        }
        if (this.scene) {
            this.scene.traverse(object => {
                if (object.geometry) object.geometry.dispose();
                if (object.material) {
                    if (Array.isArray(object.material)) {
                        object.material.forEach(material => material.dispose());
                    } else {
                        object.material.dispose();
                    }
                }
            });
        }
    }
}

// Export for use in templates
window.Body3DViewerThreeJS = Body3DViewerThreeJS;
console.log('Three.js 真实3D人体查看器已加载 | Three.js 3D Body Viewer loaded');
