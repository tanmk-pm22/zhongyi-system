/**
 * Anatomical 3D Human Body Viewer - Medical Grade
 * 医学级解剖3D人体查看器
 *
 * Features:
 * - Realistic male anatomical model
 * - Muscle system visualization
 * - Skeletal landmarks
 * - Meridian system (TCM)
 * - Professional medical-grade rendering
 *
 * 功能：
 * - 真实男性解剖模型
 * - 肌肉系统可视化
 * - 骨骼标记
 * - 经络系统（中医）
 * - 专业医学级渲染
 */

class Body3DViewerAnatomical {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error('容器未找到 | Container not found:', containerId);
            return;
        }

        this.options = {
            showAcupoints: options.showAcupoints || false,
            showMuscles: options.showMuscles || false,
            showSkeleton: options.showSkeleton || false,
            showMeridians: options.showMeridians || false,
            selectedPoints: options.selectedPoints || [],
            selectedAreas: options.selectedAreas || [],
            anatomicalView: true,
            ...options
        };

        // Initialize Three.js components
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.bodyModel = null;
        this.muscleGroups = [];
        this.skeletonMarkers = [];
        this.meridianLines = [];
        this.acupointMarkers = [];

        // Wait for Three.js to load
        this.initWhenReady();
    }

    initWhenReady() {
        if (typeof THREE === 'undefined') {
            console.log('等待Three.js加载... | Waiting for Three.js...');
            setTimeout(() => this.initWhenReady(), 100);
            return;
        }
        this.init();
    }

    init() {
        // Create scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x1a1a2e);
        this.scene.fog = new THREE.Fog(0x1a1a2e, 8, 20);

        // Create camera
        const width = this.container.clientWidth || 800;
        const height = this.container.clientHeight || 600;
        this.camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
        this.camera.position.set(0, 1.6, 5);
        this.camera.lookAt(0, 1, 0);

        // Create ultra-high-quality renderer
        this.renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true,
            powerPreference: "high-performance",
            precision: "highp",
            logarithmicDepthBuffer: true
        });
        this.renderer.setSize(width, height);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.renderer.shadowMap.autoUpdate = true;
        this.renderer.outputEncoding = THREE.sRGBEncoding;
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1.1;
        this.renderer.physicallyCorrectLights = true;
        this.container.appendChild(this.renderer.domElement);

        // Add professional lighting
        this.addProfessionalLighting();

        // Add controls
        this.addControls();

        // Create anatomical human body
        this.createAnatomicalBody();

        // Add optional systems
        if (this.options.showMeridians) {
            this.addMeridianSystem();
        }

        if (this.options.showAcupoints) {
            this.addAcupoints();
        }

        if (this.options.showMuscles) {
            this.highlightMuscleGroups();
        }

        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());

        // Add UI controls
        this.addAnatomicalControls();

        // Start animation
        this.animate();

        console.log('✓ 医学级解剖3D查看器初始化完成 | Medical-grade anatomical viewer initialized');
    }

    addProfessionalLighting() {
        // Enhanced ambient light
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        this.scene.add(ambientLight);

        // Key light (main directional light) - warmer tone
        const keyLight = new THREE.DirectionalLight(0xfff5e6, 1.2);
        keyLight.position.set(5, 10, 5);
        keyLight.castShadow = true;
        keyLight.shadow.mapSize.width = 4096;  // Higher resolution shadows
        keyLight.shadow.mapSize.height = 4096;
        keyLight.shadow.camera.near = 0.5;
        keyLight.shadow.camera.far = 50;
        keyLight.shadow.camera.left = -5;
        keyLight.shadow.camera.right = 5;
        keyLight.shadow.camera.top = 5;
        keyLight.shadow.camera.bottom = -5;
        keyLight.shadow.bias = -0.00005;
        keyLight.shadow.radius = 2;  // Softer shadows
        this.scene.add(keyLight);

        // Fill light (cooler tone for contrast)
        const fillLight = new THREE.DirectionalLight(0xe6f0ff, 0.5);
        fillLight.position.set(-5, 6, -5);
        this.scene.add(fillLight);

        // Back/Rim light (stronger for definition)
        const rimLight = new THREE.DirectionalLight(0xb8d4ff, 0.8);
        rimLight.position.set(0, 6, -6);
        this.scene.add(rimLight);

        // Additional side lights for better muscle definition
        const sideLight1 = new THREE.DirectionalLight(0xfff8f0, 0.3);
        sideLight1.position.set(8, 3, 0);
        this.scene.add(sideLight1);

        const sideLight2 = new THREE.DirectionalLight(0xfff8f0, 0.3);
        sideLight2.position.set(-8, 3, 0);
        this.scene.add(sideLight2);

        // Point lights for depth and highlights
        const pointLight1 = new THREE.PointLight(0xffffff, 0.4, 12);
        pointLight1.position.set(2, 4, 3);
        this.scene.add(pointLight1);

        const pointLight2 = new THREE.PointLight(0xffffff, 0.4, 12);
        pointLight2.position.set(-2, 4, -3);
        this.scene.add(pointLight2);

        // Spot light from above for dramatic effect
        const spotLight = new THREE.SpotLight(0xffffff, 0.5);
        spotLight.position.set(0, 12, 0);
        spotLight.angle = Math.PI / 6;
        spotLight.penumbra = 0.3;
        spotLight.decay = 2;
        spotLight.distance = 20;
        this.scene.add(spotLight);

        // Ground plane for shadows
        const groundGeometry = new THREE.PlaneGeometry(20, 20);
        const groundMaterial = new THREE.ShadowMaterial({ opacity: 0.2 });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.position.y = -0.7;
        ground.receiveShadow = true;
        this.scene.add(ground);

        // Add subtle grid for reference
        const gridHelper = new THREE.GridHelper(10, 20, 0x444444, 0x222222);
        gridHelper.position.y = -0.7;
        this.scene.add(gridHelper);
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
        this.controls.maxDistance = 12;
        this.controls.target.set(0, 1, 0);
        this.controls.maxPolarAngle = Math.PI / 2 + 0.1;
    }

    createAnatomicalBody() {
        const bodyGroup = new THREE.Group();

        // Ultra-realistic skin material with subsurface scattering simulation
        const skinMaterial = new THREE.MeshStandardMaterial({
            color: 0xe0b090,
            roughness: 0.65,
            metalness: 0.0,
            side: THREE.DoubleSide,
            emissive: 0x2a1810,
            emissiveIntensity: 0.05
        });

        // Enhanced muscle material with better color
        const muscleMaterial = new THREE.MeshStandardMaterial({
            color: 0xd85050,
            roughness: 0.75,
            metalness: 0.05,
            transparent: true,
            opacity: 0.92,
            emissive: 0x3a0a0a,
            emissiveIntensity: 0.1
        });

        // Deep muscle material with darker tone
        const deepMuscleMaterial = new THREE.MeshStandardMaterial({
            color: 0xb84040,
            roughness: 0.8,
            metalness: 0.0,
            transparent: true,
            opacity: 0.88,
            emissive: 0x2a0000,
            emissiveIntensity: 0.08
        });

        // HEAD - More detailed
        const headGeometry = new THREE.SphereGeometry(0.14, 32, 32);
        const head = new THREE.Mesh(headGeometry, skinMaterial);
        head.position.y = 1.75;
        head.scale.set(1, 1.15, 1);
        head.castShadow = true;
        head.receiveShadow = true;
        bodyGroup.add(head);

        // Face features
        const eyeGeometry = new THREE.SphereGeometry(0.015, 16, 16);
        const eyeMaterial = new THREE.MeshStandardMaterial({ color: 0x2a2a2a });

        const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        leftEye.position.set(-0.04, 1.77, 0.13);
        bodyGroup.add(leftEye);

        const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        rightEye.position.set(0.04, 1.77, 0.13);
        bodyGroup.add(rightEye);

        // NECK with muscle detail
        const neckGeometry = new THREE.CylinderGeometry(0.065, 0.08, 0.22, 16);
        const neck = new THREE.Mesh(neckGeometry, skinMaterial);
        neck.position.y = 1.57;
        neck.castShadow = true;
        neck.receiveShadow = true;
        bodyGroup.add(neck);

        // Sternocleidomastoid muscles (visible neck muscles)
        const scmGeometry = new THREE.CylinderGeometry(0.015, 0.02, 0.18, 8);
        const scmLeft = new THREE.Mesh(scmGeometry, muscleMaterial);
        scmLeft.position.set(-0.03, 1.57, 0.04);
        scmLeft.rotation.z = 0.2;
        bodyGroup.add(scmLeft);

        const scmRight = new THREE.Mesh(scmGeometry, muscleMaterial);
        scmRight.position.set(0.03, 1.57, 0.04);
        scmRight.rotation.z = -0.2;
        bodyGroup.add(scmRight);

        // TORSO with detailed muscle groups
        this.createDetailedTorso(bodyGroup, skinMaterial, muscleMaterial, deepMuscleMaterial);

        // ARMS with muscle definition
        this.createAnatomicalArm(bodyGroup, skinMaterial, muscleMaterial, -1);
        this.createAnatomicalArm(bodyGroup, skinMaterial, muscleMaterial, 1);

        // LEGS with muscle definition
        this.createAnatomicalLeg(bodyGroup, skinMaterial, muscleMaterial, -1);
        this.createAnatomicalLeg(bodyGroup, skinMaterial, muscleMaterial, 1);

        this.scene.add(bodyGroup);
        this.bodyModel = bodyGroup;
    }

    createDetailedTorso(bodyGroup, skinMaterial, muscleMaterial, deepMuscleMaterial) {
        // Chest/Thorax
        const chestGeometry = new THREE.SphereGeometry(0.24, 32, 32);
        const chest = new THREE.Mesh(chestGeometry, skinMaterial);
        chest.position.y = 1.35;
        chest.scale.set(1, 1.1, 0.55);
        chest.castShadow = true;
        chest.receiveShadow = true;
        bodyGroup.add(chest);

        // Pectoralis major muscles
        const pectoralGeometry = new THREE.SphereGeometry(0.13, 24, 24);

        const pecLeft = new THREE.Mesh(pectoralGeometry, muscleMaterial);
        pecLeft.position.set(-0.11, 1.36, 0.12);
        pecLeft.scale.set(0.85, 1.1, 0.5);
        pecLeft.castShadow = true;
        bodyGroup.add(pecLeft);

        const pecRight = new THREE.Mesh(pectoralGeometry, muscleMaterial);
        pecRight.position.set(0.11, 1.36, 0.12);
        pecRight.scale.set(0.85, 1.1, 0.5);
        pecRight.castShadow = true;
        bodyGroup.add(pecRight);

        // Abdomen
        const abdomenGeometry = new THREE.CylinderGeometry(0.18, 0.17, 0.38, 32);
        const abdomen = new THREE.Mesh(abdomenGeometry, skinMaterial);
        abdomen.position.y = 0.98;
        abdomen.castShadow = true;
        abdomen.receiveShadow = true;
        bodyGroup.add(abdomen);

        // Rectus abdominis (6-pack muscles)
        const absWidth = 0.08;
        const absHeight = 0.09;
        const absDepth = 0.04;

        for (let row = 0; row < 3; row++) {
            for (let col = 0; col < 2; col++) {
                const absGeometry = new THREE.BoxGeometry(absWidth, absHeight, absDepth, 4, 4, 4);
                const absMuscle = new THREE.Mesh(absGeometry, muscleMaterial);
                absMuscle.position.set(
                    (col === 0 ? -0.07 : 0.07),
                    1.12 - row * 0.11,
                    0.17
                );
                absMuscle.castShadow = true;
                bodyGroup.add(absMuscle);
                this.muscleGroups.push({ mesh: absMuscle, name: '腹直肌 | Rectus Abdominis' });
            }
        }

        // External obliques
        const obliqueGeometry = new THREE.BoxGeometry(0.06, 0.25, 0.05, 4, 4, 4);

        const obliqueLeft = new THREE.Mesh(obliqueGeometry, muscleMaterial);
        obliqueLeft.position.set(-0.17, 1.0, 0.12);
        obliqueLeft.rotation.z = 0.15;
        bodyGroup.add(obliqueLeft);
        this.muscleGroups.push({ mesh: obliqueLeft, name: '腹外斜肌 | External Oblique' });

        const obliqueRight = new THREE.Mesh(obliqueGeometry, muscleMaterial);
        obliqueRight.position.set(0.17, 1.0, 0.12);
        obliqueRight.rotation.z = -0.15;
        bodyGroup.add(obliqueRight);
        this.muscleGroups.push({ mesh: obliqueRight, name: '腹外斜肌 | External Oblique' });

        // Serratus anterior (rib muscles)
        for (let i = 0; i < 4; i++) {
            const serratusGeometry = new THREE.BoxGeometry(0.04, 0.06, 0.03, 2, 2, 2);
            const serratusLeft = new THREE.Mesh(serratusGeometry, deepMuscleMaterial);
            serratusLeft.position.set(-0.18, 1.25 - i * 0.08, 0.08);
            serratusLeft.rotation.z = 0.3;
            bodyGroup.add(serratusLeft);

            const serratusRight = new THREE.Mesh(serratusGeometry, deepMuscleMaterial);
            serratusRight.position.set(0.18, 1.25 - i * 0.08, 0.08);
            serratusRight.rotation.z = -0.3;
            bodyGroup.add(serratusRight);
        }

        // Pelvis
        const pelvisGeometry = new THREE.SphereGeometry(0.20, 32, 32);
        const pelvis = new THREE.Mesh(pelvisGeometry, skinMaterial);
        pelvis.position.y = 0.73;
        pelvis.scale.set(1.1, 0.55, 0.95);
        pelvis.castShadow = true;
        pelvis.receiveShadow = true;
        bodyGroup.add(pelvis);

        // Gluteus muscles
        const gluteGeometry = new THREE.SphereGeometry(0.12, 16, 16);

        const gluteLeft = new THREE.Mesh(gluteGeometry, muscleMaterial);
        gluteLeft.position.set(-0.12, 0.7, -0.12);
        gluteLeft.scale.set(0.9, 1, 1.2);
        bodyGroup.add(gluteLeft);
        this.muscleGroups.push({ mesh: gluteLeft, name: '臀大肌 | Gluteus Maximus' });

        const gluteRight = new THREE.Mesh(gluteGeometry, muscleMaterial);
        gluteRight.position.set(0.12, 0.7, -0.12);
        gluteRight.scale.set(0.9, 1, 1.2);
        bodyGroup.add(gluteRight);
        this.muscleGroups.push({ mesh: gluteRight, name: '臀大肌 | Gluteus Maximus' });
    }

    createAnatomicalArm(bodyGroup, skinMaterial, muscleMaterial, side) {
        const dir = side; // -1 for left, 1 for right

        // Deltoid (shoulder muscle)
        const deltoidGeometry = new THREE.SphereGeometry(0.09, 16, 16);
        const deltoid = new THREE.Mesh(deltoidGeometry, muscleMaterial);
        deltoid.position.set(dir * 0.26, 1.42, 0);
        deltoid.scale.set(1, 0.85, 0.85);
        deltoid.castShadow = true;
        bodyGroup.add(deltoid);
        this.muscleGroups.push({ mesh: deltoid, name: '三角肌 | Deltoid' });

        // Upper arm with biceps/triceps
        const upperArmBase = new THREE.CapsuleGeometry(0.058, 0.48, 16, 32);
        const upperArm = new THREE.Mesh(upperArmBase, skinMaterial);
        upperArm.position.set(dir * 0.29, 1.08, 0);
        upperArm.rotation.z = dir * Math.PI / 14;
        upperArm.castShadow = true;
        bodyGroup.add(upperArm);

        // Biceps
        const bicepsGeometry = new THREE.SphereGeometry(0.045, 12, 12);
        const biceps = new THREE.Mesh(bicepsGeometry, muscleMaterial);
        biceps.position.set(dir * 0.28, 1.15, 0.04);
        biceps.scale.set(0.9, 1.3, 0.85);
        biceps.castShadow = true;
        bodyGroup.add(biceps);
        this.muscleGroups.push({ mesh: biceps, name: '肱二头肌 | Biceps Brachii' });

        // Triceps
        const triceps = new THREE.Mesh(bicepsGeometry, muscleMaterial);
        triceps.position.set(dir * 0.30, 1.10, -0.04);
        triceps.scale.set(0.85, 1.4, 0.9);
        triceps.castShadow = true;
        bodyGroup.add(triceps);
        this.muscleGroups.push({ mesh: triceps, name: '肱三头肌 | Triceps Brachii' });

        // Elbow
        const elbowGeometry = new THREE.SphereGeometry(0.052, 16, 16);
        const elbow = new THREE.Mesh(elbowGeometry, skinMaterial);
        elbow.position.set(dir * 0.36, 0.80, 0);
        elbow.castShadow = true;
        bodyGroup.add(elbow);

        // Forearm with muscle definition
        const forearmGeometry = new THREE.CapsuleGeometry(0.048, 0.48, 16, 32);
        const forearm = new THREE.Mesh(forearmGeometry, skinMaterial);
        forearm.position.set(dir * 0.43, 0.50, 0.06);
        forearm.rotation.z = dir * Math.PI / 11;
        forearm.rotation.x = -Math.PI / 25;
        forearm.castShadow = true;
        bodyGroup.add(forearm);

        // Forearm flexors
        const forearmMuscleGeometry = new THREE.CapsuleGeometry(0.035, 0.38, 12, 24);
        const forearmFlexors = new THREE.Mesh(forearmMuscleGeometry, muscleMaterial);
        forearmFlexors.position.set(dir * 0.42, 0.52, 0.08);
        forearmFlexors.rotation.z = dir * Math.PI / 11;
        forearmFlexors.rotation.x = -Math.PI / 25;
        bodyGroup.add(forearmFlexors);
        this.muscleGroups.push({ mesh: forearmFlexors, name: '前臂屈肌 | Forearm Flexors' });

        // Hand
        const handGeometry = new THREE.BoxGeometry(0.09, 0.13, 0.04, 4, 4, 4);
        const hand = new THREE.Mesh(handGeometry, skinMaterial);
        hand.position.set(dir * 0.52, 0.20, 0.09);
        hand.castShadow = true;
        bodyGroup.add(hand);

        // Fingers (simplified)
        for (let i = 0; i < 4; i++) {
            const fingerGeometry = new THREE.CapsuleGeometry(0.008, 0.06, 8, 16);
            const finger = new THREE.Mesh(fingerGeometry, skinMaterial);
            finger.position.set(
                dir * 0.52 + (i - 1.5) * 0.012 * (side === -1 ? 1 : -1),
                0.08,
                0.09
            );
            finger.rotation.x = Math.PI / 12;
            bodyGroup.add(finger);
        }
    }

    createAnatomicalLeg(bodyGroup, skinMaterial, muscleMaterial, side) {
        const dir = side; // -1 for left, 1 for right

        // Thigh with muscle groups
        const thighGeometry = new THREE.CapsuleGeometry(0.10, 0.58, 20, 32);
        const thigh = new THREE.Mesh(thighGeometry, skinMaterial);
        thigh.position.set(dir * 0.12, 0.36, 0);
        thigh.castShadow = true;
        thigh.receiveShadow = true;
        bodyGroup.add(thigh);

        // Quadriceps femoris (front thigh)
        const quadGeometry = new THREE.CapsuleGeometry(0.08, 0.50, 16, 24);
        const quadriceps = new THREE.Mesh(quadGeometry, muscleMaterial);
        quadriceps.position.set(dir * 0.12, 0.38, 0.08);
        quadriceps.castShadow = true;
        bodyGroup.add(quadriceps);
        this.muscleGroups.push({ mesh: quadriceps, name: '股四头肌 | Quadriceps Femoris' });

        // Hamstrings (back thigh)
        const hamstringGeometry = new THREE.CapsuleGeometry(0.075, 0.48, 16, 24);
        const hamstrings = new THREE.Mesh(hamstringGeometry, muscleMaterial);
        hamstrings.position.set(dir * 0.12, 0.36, -0.08);
        hamstrings.castShadow = true;
        bodyGroup.add(hamstrings);
        this.muscleGroups.push({ mesh: hamstrings, name: '腘绳肌 | Hamstrings' });

        // Knee
        const kneeGeometry = new THREE.SphereGeometry(0.08, 20, 20);
        const knee = new THREE.Mesh(kneeGeometry, skinMaterial);
        knee.position.set(dir * 0.12, 0.03, 0);
        knee.castShadow = true;
        bodyGroup.add(knee);

        // Calf/Lower leg with muscles
        const calfGeometry = new THREE.CapsuleGeometry(0.075, 0.52, 20, 32);
        const calf = new THREE.Mesh(calfGeometry, skinMaterial);
        calf.position.set(dir * 0.12, -0.27, 0);
        calf.castShadow = true;
        bodyGroup.add(calf);

        // Gastrocnemius (calf muscle)
        const gastrocGeometry = new THREE.SphereGeometry(0.065, 16, 16);
        const gastrocnemius = new THREE.Mesh(gastrocGeometry, muscleMaterial);
        gastrocnemius.position.set(dir * 0.12, -0.15, -0.06);
        gastrocnemius.scale.set(1, 1.5, 1.2);
        gastrocnemius.castShadow = true;
        bodyGroup.add(gastrocnemius);
        this.muscleGroups.push({ mesh: gastrocnemius, name: '腓肠肌 | Gastrocnemius' });

        // Tibialis anterior (shin muscle)
        const tibialisGeometry = new THREE.CapsuleGeometry(0.025, 0.40, 12, 20);
        const tibialis = new THREE.Mesh(tibialisGeometry, muscleMaterial);
        tibialis.position.set(dir * 0.12, -0.25, 0.06);
        bodyGroup.add(tibialis);
        this.muscleGroups.push({ mesh: tibialis, name: '胫骨前肌 | Tibialis Anterior' });

        // Ankle
        const ankleGeometry = new THREE.SphereGeometry(0.055, 16, 16);
        const ankle = new THREE.Mesh(ankleGeometry, skinMaterial);
        ankle.position.set(dir * 0.12, -0.55, 0);
        ankle.castShadow = true;
        bodyGroup.add(ankle);

        // Foot
        const footGeometry = new THREE.BoxGeometry(0.13, 0.09, 0.24, 4, 4, 4);
        const foot = new THREE.Mesh(footGeometry, skinMaterial);
        foot.position.set(dir * 0.12, -0.65, 0.07);
        foot.castShadow = true;
        bodyGroup.add(foot);

        // Toes
        for (let i = 0; i < 5; i++) {
            const toeGeometry = new THREE.CapsuleGeometry(0.008, 0.025, 6, 12);
            const toe = new THREE.Mesh(toeGeometry, skinMaterial);
            toe.position.set(
                dir * (0.12 + (i - 2) * 0.015),
                -0.67,
                0.18
            );
            toe.rotation.x = Math.PI / 2;
            bodyGroup.add(toe);
        }
    }

    addMeridianSystem() {
        // 创建经络线条 | Create meridian lines
        const meridianMaterial = new THREE.LineBasicMaterial({
            color: 0xff6600,
            linewidth: 2,
            opacity: 0.8,
            transparent: true
        });

        // 任脉 | Conception Vessel (前正中线)
        const cvPoints = [
            new THREE.Vector3(0, 0.7, 0.19),
            new THREE.Vector3(0, 1.0, 0.18),
            new THREE.Vector3(0, 1.3, 0.16),
            new THREE.Vector3(0, 1.5, 0.14),
            new THREE.Vector3(0, 1.65, 0.10)
        ];
        const cvGeometry = new THREE.BufferGeometry().setFromPoints(cvPoints);
        const cvLine = new THREE.Line(cvGeometry, meridianMaterial);
        this.scene.add(cvLine);
        this.meridianLines.push(cvLine);

        // 督脉 | Governing Vessel (后正中线)
        const gvPoints = [
            new THREE.Vector3(0, 0.7, -0.19),
            new THREE.Vector3(0, 1.0, -0.18),
            new THREE.Vector3(0, 1.3, -0.16),
            new THREE.Vector3(0, 1.5, -0.14),
            new THREE.Vector3(0, 1.75, -0.10)
        ];
        const gvGeometry = new THREE.BufferGeometry().setFromPoints(gvPoints);
        const gvLine = new THREE.Line(gvGeometry, meridianMaterial);
        this.scene.add(gvLine);
        this.meridianLines.push(gvLine);
    }

    addAcupoints() {
        // 常用穴位数据 | Common acupoint data
        const acupointData = {
            'GV20': { pos: [0, 1.82, 0], name: '百会 | Baihui', color: 0xff4444 },
            'GB20': { pos: [-0.08, 1.65, -0.12], name: '风池 | Fengchi', color: 0xff4444 },
            'GV14': { pos: [0, 1.45, -0.14], name: '大椎 | Dazhui', color: 0xff4444 },
            'BL13': { pos: [-0.05, 1.35, -0.16], name: '肺俞 | Feishu', color: 0xff6644 },
            'BL23': { pos: [-0.05, 0.85, -0.17], name: '肾俞 | Shenshu', color: 0xff6644 },
            'LI4': { pos: [-0.52, 0.20, 0.09], name: '合谷 | Hegu', color: 0x4444ff },
            'LI11': { pos: [-0.36, 0.80, 0.05], name: '曲池 | Quchi', color: 0x4466ff },
            'PC6': { pos: [-0.43, 0.52, 0.08], name: '内关 | Neiguan', color: 0x6644ff },
            'ST36': { pos: [-0.14, -0.15, 0.10], name: '足三里 | Zusanli', color: 0x44ff44 },
            'SP6': { pos: [-0.13, -0.40, 0.08], name: '三阴交 | Sanyinjiao', color: 0x44ff44 },
            'SP9': { pos: [-0.14, -0.02, 0.08], name: '阴陵泉 | Yinlingquan', color: 0x44ff44 },
            'LR3': { pos: [-0.12, -0.62, 0.14], name: '太冲 | Taichong', color: 0x44ff88 },
            'KI3': { pos: [-0.12, -0.55, 0.02], name: '太溪 | Taixi', color: 0x44ffaa },
            'CV4': { pos: [0, 0.75, 0.19], name: '关元 | Guanyuan', color: 0xffaa44 },
            'CV12': { pos: [0, 1.05, 0.18], name: '中脘 | Zhongwan', color: 0xffaa44 }
        };

        Object.entries(acupointData).forEach(([code, data]) => {
            if (this.options.selectedPoints.length === 0 || this.options.selectedPoints.includes(code)) {
                this.createAcupointMarker(data.pos, data.name, data.color);
            }
        });
    }

    createAcupointMarker(position, label, color) {
        // 发光穴位标记 | Glowing acupoint marker
        const markerGeometry = new THREE.SphereGeometry(0.02, 16, 16);
        const markerMaterial = new THREE.MeshStandardMaterial({
            color: color,
            emissive: color,
            emissiveIntensity: 0.7,
            roughness: 0.2,
            metalness: 0.3
        });
        const marker = new THREE.Mesh(markerGeometry, markerMaterial);
        marker.position.set(...position);
        marker.castShadow = true;

        // 外层光晕 | Outer glow
        const glowGeometry = new THREE.SphereGeometry(0.032, 16, 16);
        const glowMaterial = new THREE.MeshBasicMaterial({
            color: color,
            transparent: true,
            opacity: 0.25
        });
        const glow = new THREE.Mesh(glowGeometry, glowMaterial);
        glow.position.set(...position);

        this.scene.add(marker);
        this.scene.add(glow);
        this.acupointMarkers.push({ marker, glow, label });

        // 动画效果 | Animation effect
        const animate = () => {
            const scale = 1 + 0.3 * Math.sin(Date.now() * 0.003);
            glow.scale.set(scale, scale, scale);
        };
        this.glowAnimations = this.glowAnimations || [];
        this.glowAnimations.push(animate);
    }

    highlightMuscleGroups() {
        // 高亮显示肌肉组 | Highlight muscle groups
        this.muscleGroups.forEach(group => {
            group.mesh.material.opacity = 1.0;
            group.mesh.material.emissive = new THREE.Color(0x331111);
            group.mesh.material.emissiveIntensity = 0.2;
        });
    }

    addAnatomicalControls() {
        const controlsDiv = document.createElement('div');
        controlsDiv.className = 'anatomical-controls';
        controlsDiv.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(20, 20, 40, 0.95);
            padding: 18px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            font-size: 13px;
            color: #ffffff;
            border: 1px solid rgba(255,255,255,0.1);
            z-index: 10;
            min-width: 180px;
        `;

        controlsDiv.innerHTML = `
            <div style="margin-bottom: 12px; font-weight: bold; font-size: 14px; color: #4da6ff; border-bottom: 1px solid rgba(77,166,255,0.3); padding-bottom: 8px;">
                <i class="bi bi-gear"></i> 解剖控制 | Anatomical Controls
            </div>
            <button class="btn btn-sm btn-outline-light mb-2 w-100" data-view="front" style="font-size: 12px;">
                <i class="bi bi-person"></i> 正面 | Front
            </button>
            <button class="btn btn-sm btn-outline-light mb-2 w-100" data-view="back" style="font-size: 12px;">
                <i class="bi bi-person-fill"></i> 背面 | Back
            </button>
            <button class="btn btn-sm btn-outline-light mb-2 w-100" data-view="side" style="font-size: 12px;">
                <i class="bi bi-person-bounding-box"></i> 侧面 | Side
            </button>
            <button class="btn btn-sm btn-outline-secondary mb-2 w-100" data-view="reset" style="font-size: 12px;">
                <i class="bi bi-arrow-clockwise"></i> 重置 | Reset
            </button>
            <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.1);">
                <label style="font-size: 11px; color: #aaaaaa; display: block; margin-bottom: 8px;">
                    显示选项 | Display Options:
                </label>
                <div class="form-check form-switch mb-2">
                    <input class="form-check-input" type="checkbox" id="toggleMuscles" ${this.options.showMuscles ? 'checked' : ''}>
                    <label class="form-check-label" for="toggleMuscles" style="font-size: 11px; color: #dddddd;">
                        肌肉系统 | Muscles
                    </label>
                </div>
                <div class="form-check form-switch mb-2">
                    <input class="form-check-input" type="checkbox" id="toggleMeridians" ${this.options.showMeridians ? 'checked' : ''}>
                    <label class="form-check-label" for="toggleMeridians" style="font-size: 11px; color: #dddddd;">
                        经络系统 | Meridians
                    </label>
                </div>
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" id="toggleAcupoints" ${this.options.showAcupoints ? 'checked' : ''}>
                    <label class="form-check-label" for="toggleAcupoints" style="font-size: 11px; color: #dddddd;">
                        穴位标记 | Acupoints
                    </label>
                </div>
            </div>
            <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 10px; color: #888888;">
                <i class="bi bi-mouse"></i> 拖动旋转 | Drag to rotate<br>
                <i class="bi bi-zoom-in"></i> 滚轮缩放 | Scroll to zoom
            </div>
        `;

        this.container.appendChild(controlsDiv);

        // Add event handlers
        controlsDiv.querySelectorAll('[data-view]').forEach(btn => {
            btn.addEventListener('click', () => {
                const view = btn.dataset.view;
                this.setView(view);
            });
        });

        // Toggle controls
        document.getElementById('toggleMuscles')?.addEventListener('change', (e) => {
            this.muscleGroups.forEach(group => {
                group.mesh.visible = e.target.checked;
            });
        });

        document.getElementById('toggleMeridians')?.addEventListener('change', (e) => {
            this.meridianLines.forEach(line => {
                line.visible = e.target.checked;
            });
        });

        document.getElementById('toggleAcupoints')?.addEventListener('change', (e) => {
            this.acupointMarkers.forEach(({ marker, glow }) => {
                marker.visible = e.target.checked;
                glow.visible = e.target.checked;
            });
        });
    }

    setView(view) {
        const duration = 1200;
        const start = {
            x: this.camera.position.x,
            y: this.camera.position.y,
            z: this.camera.position.z
        };

        let end;
        switch (view) {
            case 'front':
                end = { x: 0, y: 1.6, z: 5 };
                break;
            case 'back':
                end = { x: 0, y: 1.6, z: -5 };
                break;
            case 'side':
                end = { x: 5, y: 1.6, z: 0 };
                break;
            case 'reset':
                end = { x: 0, y: 1.6, z: 5 };
                break;
        }

        const startTime = Date.now();
        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic

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

        // Rotate body slightly for presentation (optional)
        if (this.bodyModel && this.options.autoRotate) {
            this.bodyModel.rotation.y += 0.001;
        }

        // Update controls
        if (this.controls) {
            this.controls.update();
        }

        // Render
        this.renderer.render(this.scene, this.camera);
    }

    // Public API
    toggleMuscleSystem(show) {
        this.muscleGroups.forEach(group => {
            group.mesh.visible = show;
        });
    }

    toggleMeridianSystem(show) {
        this.meridianLines.forEach(line => {
            line.visible = show;
        });
    }

    toggleAcupoints(show) {
        this.acupointMarkers.forEach(({ marker, glow }) => {
            marker.visible = show;
            glow.visible = show;
        });
    }
}

// Make available globally
window.Body3DViewerAnatomical = Body3DViewerAnatomical;
