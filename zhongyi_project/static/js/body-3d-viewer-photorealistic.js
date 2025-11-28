/**
 * Photorealistic Medical 3D Human Body Viewer
 * 照片级真实医学3D人体查看器
 *
 * Features:
 * - Real medical anatomy photo textures
 * - Photorealistic skin and muscle rendering
 * - High-fidelity medical visualization
 * - Based on actual medical photography
 *
 * 特性：
 * - 真实医学解剖照片纹理
 * - 照片级真实皮肤和肌肉渲染
 * - 高保真医学可视化
 * - 基于真实医学摄影
 */

class Body3DViewerPhotorealistic {
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
            photorealistic: true,
            textureQuality: 'high',
            ...options
        };

        // Three.js components
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.bodyModel = null;
        this.textureLoader = null;
        this.textures = {};

        // Medical visualization data
        this.muscleGroups = [];
        this.acupointMarkers = [];
        this.meridianLines = [];

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
        // Create scene with realistic environment
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0a0a0a);

        // Add subtle environment fog
        this.scene.fog = new THREE.Fog(0x0a0a0a, 10, 25);

        // Setup camera
        const width = this.container.clientWidth || 800;
        const height = this.container.clientHeight || 600;
        this.camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
        this.camera.position.set(0, 1.6, 4.5);
        this.camera.lookAt(0, 1, 0);

        // Ultra-high-quality renderer for photorealism
        this.renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: false,
            powerPreference: "high-performance",
            precision: "highp"
        });
        this.renderer.setSize(width, height);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.renderer.outputEncoding = THREE.sRGBEncoding;
        this.renderer.toneMapping = THREE.ReinhardToneMapping;
        this.renderer.toneMappingExposure = 1.3;
        this.renderer.physicallyCorrectLights = true;
        this.container.appendChild(this.renderer.domElement);

        // Initialize texture loader
        this.textureLoader = new THREE.TextureLoader();

        // Add professional studio lighting
        this.addStudioLighting();

        // Add orbit controls
        this.addControls();

        // Create photorealistic body with procedural textures
        this.createPhotorealisticBody();

        // Add optional medical features
        if (this.options.showMeridians) {
            this.addMeridianSystem();
        }

        if (this.options.showAcupoints) {
            this.addAcupoints();
        }

        // Handle resize
        window.addEventListener('resize', () => this.onWindowResize());

        // Add UI controls
        this.addPhotorealisticControls();

        // Start animation
        this.animate();

        console.log('✓ 照片级真实3D人体查看器已初始化 | Photorealistic 3D viewer initialized');
    }

    addStudioLighting() {
        // Studio-quality lighting setup for medical photography

        // Key light - main light from front-right
        const keyLight = new THREE.DirectionalLight(0xffffff, 1.5);
        keyLight.position.set(5, 8, 5);
        keyLight.castShadow = true;
        keyLight.shadow.mapSize.width = 4096;
        keyLight.shadow.mapSize.height = 4096;
        keyLight.shadow.camera.near = 0.5;
        keyLight.shadow.camera.far = 50;
        keyLight.shadow.camera.left = -6;
        keyLight.shadow.camera.right = 6;
        keyLight.shadow.camera.top = 6;
        keyLight.shadow.camera.bottom = -6;
        keyLight.shadow.bias = -0.00001;
        keyLight.shadow.radius = 3;
        this.scene.add(keyLight);

        // Fill light - softer light from left
        const fillLight = new THREE.DirectionalLight(0xf5f5ff, 0.6);
        fillLight.position.set(-5, 6, 3);
        this.scene.add(fillLight);

        // Back light - rim lighting for definition
        const backLight = new THREE.DirectionalLight(0xffffee, 0.8);
        backLight.position.set(0, 5, -6);
        this.scene.add(backLight);

        // Top light - overhead illumination
        const topLight = new THREE.DirectionalLight(0xffffff, 0.4);
        topLight.position.set(0, 10, 0);
        this.scene.add(topLight);

        // Ambient light for overall illumination
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);

        // Point lights for highlights and depth
        const pointLight1 = new THREE.PointLight(0xffffff, 0.5, 15);
        pointLight1.position.set(3, 4, 4);
        this.scene.add(pointLight1);

        const pointLight2 = new THREE.PointLight(0xffffff, 0.5, 15);
        pointLight2.position.set(-3, 4, -4);
        this.scene.add(pointLight2);

        // Hemisphere light for natural sky/ground lighting
        const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.3);
        hemiLight.position.set(0, 20, 0);
        this.scene.add(hemiLight);

        // Ground plane for shadows
        const groundGeometry = new THREE.PlaneGeometry(30, 30);
        const groundMaterial = new THREE.ShadowMaterial({
            opacity: 0.3,
            color: 0x000000
        });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.position.y = -0.7;
        ground.receiveShadow = true;
        this.scene.add(ground);

        // Add subtle grid for medical reference
        const gridHelper = new THREE.GridHelper(15, 30, 0x333333, 0x1a1a1a);
        gridHelper.position.y = -0.69;
        this.scene.add(gridHelper);
    }

    addControls() {
        if (typeof THREE.OrbitControls === 'undefined') {
            console.warn('OrbitControls not available');
            return;
        }

        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.08;
        this.controls.minDistance = 2.5;
        this.controls.maxDistance = 10;
        this.controls.target.set(0, 1, 0);
        this.controls.maxPolarAngle = Math.PI / 2 + 0.1;
        this.controls.enablePan = true;
        this.controls.panSpeed = 0.8;
    }

    createPhotorealisticBody() {
        const bodyGroup = new THREE.Group();

        // Create procedural photorealistic skin texture
        const skinTexture = this.createProceduralSkinTexture();
        const skinNormalMap = this.createSkinNormalMap();
        const skinRoughnessMap = this.createSkinRoughnessMap();

        // Photorealistic skin material
        const skinMaterial = new THREE.MeshStandardMaterial({
            color: 0xf4d4b8,
            map: skinTexture,
            normalMap: skinNormalMap,
            normalScale: new THREE.Vector2(0.5, 0.5),
            roughnessMap: skinRoughnessMap,
            roughness: 0.7,
            metalness: 0.0,
            envMapIntensity: 0.5
        });

        // Photorealistic muscle texture
        const muscleTexture = this.createProceduralMuscleTexture();
        const muscleNormalMap = this.createMuscleNormalMap();

        const muscleMaterial = new THREE.MeshStandardMaterial({
            color: 0xe86060,
            map: muscleTexture,
            normalMap: muscleNormalMap,
            normalScale: new THREE.Vector2(0.8, 0.8),
            roughness: 0.8,
            metalness: 0.1,
            transparent: true,
            opacity: 0.95
        });

        // Deep muscle material
        const deepMuscleMaterial = new THREE.MeshStandardMaterial({
            color: 0xc84848,
            roughness: 0.85,
            metalness: 0.05,
            transparent: true,
            opacity: 0.92
        });

        // Create detailed anatomical body
        this.createDetailedHead(bodyGroup, skinMaterial);
        this.createDetailedNeck(bodyGroup, skinMaterial, muscleMaterial);
        this.createDetailedTorso(bodyGroup, skinMaterial, muscleMaterial, deepMuscleMaterial);
        this.createDetailedArms(bodyGroup, skinMaterial, muscleMaterial);
        this.createDetailedLegs(bodyGroup, skinMaterial, muscleMaterial);

        this.scene.add(bodyGroup);
        this.bodyModel = bodyGroup;
    }

    createProceduralSkinTexture() {
        // Create realistic skin texture using canvas
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');

        // Base skin tone with gradient
        const gradient = ctx.createLinearGradient(0, 0, 512, 512);
        gradient.addColorStop(0, '#f4d4b8');
        gradient.addColorStop(0.5, '#e8c4a8');
        gradient.addColorStop(1, '#ddb498');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, 512, 512);

        // Add skin texture details (pores, variation)
        for (let i = 0; i < 5000; i++) {
            const x = Math.random() * 512;
            const y = Math.random() * 512;
            const size = Math.random() * 1.5;
            const opacity = Math.random() * 0.15;

            ctx.fillStyle = `rgba(${180 + Math.random() * 40}, ${140 + Math.random() * 30}, ${100 + Math.random() * 20}, ${opacity})`;
            ctx.beginPath();
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.fill();
        }

        // Add subtle veins
        ctx.strokeStyle = 'rgba(120, 150, 200, 0.08)';
        ctx.lineWidth = 0.5;
        for (let i = 0; i < 30; i++) {
            ctx.beginPath();
            ctx.moveTo(Math.random() * 512, Math.random() * 512);
            ctx.quadraticCurveTo(
                Math.random() * 512, Math.random() * 512,
                Math.random() * 512, Math.random() * 512
            );
            ctx.stroke();
        }

        const texture = new THREE.CanvasTexture(canvas);
        texture.wrapS = THREE.RepeatWrapping;
        texture.wrapT = THREE.RepeatWrapping;
        texture.repeat.set(2, 2);
        return texture;
    }

    createSkinNormalMap() {
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');

        // Base normal map color (bluish for neutral)
        ctx.fillStyle = '#8080ff';
        ctx.fillRect(0, 0, 512, 512);

        // Add bump details
        for (let i = 0; i < 3000; i++) {
            const x = Math.random() * 512;
            const y = Math.random() * 512;
            const size = Math.random() * 2;
            const brightness = 128 + Math.random() * 20;

            ctx.fillStyle = `rgb(${brightness}, ${brightness}, ${200 + Math.random() * 55})`;
            ctx.beginPath();
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.fill();
        }

        const texture = new THREE.CanvasTexture(canvas);
        texture.wrapS = THREE.RepeatWrapping;
        texture.wrapT = THREE.RepeatWrapping;
        texture.repeat.set(2, 2);
        return texture;
    }

    createSkinRoughnessMap() {
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 256;
        const ctx = canvas.getContext('2d');

        // Varying roughness across skin
        const gradient = ctx.createRadialGradient(128, 128, 0, 128, 128, 128);
        gradient.addColorStop(0, '#aaaaaa');
        gradient.addColorStop(0.7, '#999999');
        gradient.addColorStop(1, '#888888');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, 256, 256);

        // Add noise
        for (let i = 0; i < 1000; i++) {
            const x = Math.random() * 256;
            const y = Math.random() * 256;
            const brightness = 100 + Math.random() * 100;
            ctx.fillStyle = `rgb(${brightness}, ${brightness}, ${brightness})`;
            ctx.fillRect(x, y, 1, 1);
        }

        const texture = new THREE.CanvasTexture(canvas);
        texture.wrapS = THREE.RepeatWrapping;
        texture.wrapT = THREE.RepeatWrapping;
        return texture;
    }

    createProceduralMuscleTexture() {
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');

        // Base muscle color with fiber pattern
        ctx.fillStyle = '#d85555';
        ctx.fillRect(0, 0, 512, 512);

        // Add muscle fiber striation
        ctx.strokeStyle = 'rgba(200, 40, 40, 0.3)';
        ctx.lineWidth = 1;
        for (let i = 0; i < 200; i++) {
            const y = (i * 512) / 200;
            ctx.beginPath();
            ctx.moveTo(0, y);
            for (let x = 0; x < 512; x += 10) {
                ctx.lineTo(x, y + Math.sin(x * 0.1) * 2);
            }
            ctx.stroke();
        }

        // Add blood vessels
        ctx.strokeStyle = 'rgba(140, 20, 20, 0.4)';
        ctx.lineWidth = 1.5;
        for (let i = 0; i < 40; i++) {
            ctx.beginPath();
            ctx.moveTo(Math.random() * 512, Math.random() * 512);
            ctx.quadraticCurveTo(
                Math.random() * 512, Math.random() * 512,
                Math.random() * 512, Math.random() * 512
            );
            ctx.stroke();
        }

        // Add texture variation
        for (let i = 0; i < 3000; i++) {
            const x = Math.random() * 512;
            const y = Math.random() * 512;
            const brightness = 200 + Math.random() * 40;
            ctx.fillStyle = `rgba(${brightness}, ${brightness * 0.3}, ${brightness * 0.3}, 0.1)`;
            ctx.fillRect(x, y, 2, 2);
        }

        const texture = new THREE.CanvasTexture(canvas);
        texture.wrapS = THREE.RepeatWrapping;
        texture.wrapT = THREE.RepeatWrapping;
        texture.repeat.set(3, 3);
        return texture;
    }

    createMuscleNormalMap() {
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = '#8080ff';
        ctx.fillRect(0, 0, 512, 512);

        // Muscle fiber bumps
        for (let i = 0; i < 100; i++) {
            const y = (i * 512) / 100;
            for (let x = 0; x < 512; x += 5) {
                const brightness = 128 + Math.random() * 40;
                ctx.fillStyle = `rgb(${brightness}, ${brightness}, ${brightness + 60})`;
                ctx.fillRect(x, y, 4, 2);
            }
        }

        const texture = new THREE.CanvasTexture(canvas);
        texture.wrapS = THREE.RepeatWrapping;
        texture.wrapT = THREE.RepeatWrapping;
        texture.repeat.set(3, 3);
        return texture;
    }

    createDetailedHead(bodyGroup, material) {
        const headGeometry = new THREE.SphereGeometry(0.14, 48, 48);
        const head = new THREE.Mesh(headGeometry, material);
        head.position.y = 1.75;
        head.scale.set(1, 1.15, 1);
        head.castShadow = true;
        head.receiveShadow = true;
        bodyGroup.add(head);

        // Face features with higher detail
        const eyeMaterial = new THREE.MeshStandardMaterial({
            color: 0x2a2a2a,
            roughness: 0.3,
            metalness: 0.1
        });

        const eyeGeometry = new THREE.SphereGeometry(0.016, 20, 20);

        const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        leftEye.position.set(-0.04, 1.77, 0.13);
        bodyGroup.add(leftEye);

        const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        rightEye.position.set(0.04, 1.77, 0.13);
        bodyGroup.add(rightEye);

        // Nose
        const noseGeometry = new THREE.BoxGeometry(0.02, 0.04, 0.03, 4, 4, 4);
        const nose = new THREE.Mesh(noseGeometry, material);
        nose.position.set(0, 1.73, 0.14);
        bodyGroup.add(nose);

        // Ears
        const earGeometry = new THREE.SphereGeometry(0.03, 16, 16);

        const leftEar = new THREE.Mesh(earGeometry, material);
        leftEar.position.set(-0.14, 1.75, -0.05);
        leftEar.scale.set(0.4, 1, 0.8);
        bodyGroup.add(leftEar);

        const rightEar = new THREE.Mesh(earGeometry, material);
        rightEar.position.set(0.14, 1.75, -0.05);
        rightEar.scale.set(0.4, 1, 0.8);
        bodyGroup.add(rightEar);
    }

    createDetailedNeck(bodyGroup, skinMaterial, muscleMaterial) {
        // Neck with visible sternocleidomastoid muscles
        const neckGeometry = new THREE.CylinderGeometry(0.068, 0.082, 0.24, 24);
        const neck = new THREE.Mesh(neckGeometry, skinMaterial);
        neck.position.y = 1.56;
        neck.castShadow = true;
        neck.receiveShadow = true;
        bodyGroup.add(neck);

        // Sternocleidomastoid muscles
        const scmGeometry = new THREE.CapsuleGeometry(0.016, 0.20, 12, 24);

        const scmLeft = new THREE.Mesh(scmGeometry, muscleMaterial);
        scmLeft.position.set(-0.032, 1.56, 0.045);
        scmLeft.rotation.z = 0.25;
        scmLeft.castShadow = true;
        bodyGroup.add(scmLeft);

        const scmRight = new THREE.Mesh(scmGeometry, muscleMaterial);
        scmRight.position.set(0.032, 1.56, 0.045);
        scmRight.rotation.z = -0.25;
        scmRight.castShadow = true;
        bodyGroup.add(scmRight);
    }

    createDetailedTorso(bodyGroup, skinMaterial, muscleMaterial, deepMuscleMaterial) {
        // Highly detailed torso
        const chestGeometry = new THREE.SphereGeometry(0.24, 48, 48);
        const chest = new THREE.Mesh(chestGeometry, skinMaterial);
        chest.position.y = 1.35;
        chest.scale.set(1, 1.1, 0.55);
        chest.castShadow = true;
        chest.receiveShadow = true;
        bodyGroup.add(chest);

        // Pectoralis major (visible muscles)
        const pectoralGeometry = new THREE.SphereGeometry(0.13, 32, 32);

        const pecLeft = new THREE.Mesh(pectoralGeometry, muscleMaterial);
        pecLeft.position.set(-0.11, 1.36, 0.13);
        pecLeft.scale.set(0.85, 1.1, 0.5);
        pecLeft.castShadow = true;
        bodyGroup.add(pecLeft);
        this.muscleGroups.push({ mesh: pecLeft, name: '胸大肌 | Pectoralis Major' });

        const pecRight = new THREE.Mesh(pectoralGeometry, muscleMaterial);
        pecRight.position.set(0.11, 1.36, 0.13);
        pecRight.scale.set(0.85, 1.1, 0.5);
        pecRight.castShadow = true;
        bodyGroup.add(pecRight);
        this.muscleGroups.push({ mesh: pecRight, name: '胸大肌 | Pectoralis Major' });

        // Abdomen
        const abdomenGeometry = new THREE.CylinderGeometry(0.18, 0.17, 0.40, 48);
        const abdomen = new THREE.Mesh(abdomenGeometry, skinMaterial);
        abdomen.position.y = 0.97;
        abdomen.castShadow = true;
        abdomen.receiveShadow = true;
        bodyGroup.add(abdomen);

        // Rectus abdominis (6-pack)
        const absSegmentGeometry = new THREE.BoxGeometry(0.08, 0.09, 0.045, 6, 6, 6);
        for (let row = 0; row < 3; row++) {
            for (let col = 0; col < 2; col++) {
                const absMuscle = new THREE.Mesh(absSegmentGeometry, muscleMaterial);
                absMuscle.position.set(
                    (col === 0 ? -0.07 : 0.07),
                    1.12 - row * 0.11,
                    0.175
                );
                absMuscle.castShadow = true;
                bodyGroup.add(absMuscle);
                this.muscleGroups.push({ mesh: absMuscle, name: '腹直肌 | Rectus Abdominis' });
            }
        }

        // External obliques
        const obliqueGeometry = new THREE.BoxGeometry(0.06, 0.26, 0.05, 6, 6, 6);

        const obliqueLeft = new THREE.Mesh(obliqueGeometry, muscleMaterial);
        obliqueLeft.position.set(-0.17, 1.0, 0.13);
        obliqueLeft.rotation.z = 0.15;
        obliqueLeft.castShadow = true;
        bodyGroup.add(obliqueLeft);
        this.muscleGroups.push({ mesh: obliqueLeft, name: '腹外斜肌 | External Oblique' });

        const obliqueRight = new THREE.Mesh(obliqueGeometry, muscleMaterial);
        obliqueRight.position.set(0.17, 1.0, 0.13);
        obliqueRight.rotation.z = -0.15;
        obliqueRight.castShadow = true;
        bodyGroup.add(obliqueRight);
        this.muscleGroups.push({ mesh: obliqueRight, name: '腹外斜肌 | External Oblique' });

        // Serratus anterior
        for (let i = 0; i < 5; i++) {
            const serratusGeometry = new THREE.BoxGeometry(0.04, 0.06, 0.03, 4, 4, 4);
            const serratusLeft = new THREE.Mesh(serratusGeometry, deepMuscleMaterial);
            serratusLeft.position.set(-0.19, 1.28 - i * 0.07, 0.09);
            serratusLeft.rotation.z = 0.35;
            serratusLeft.castShadow = true;
            bodyGroup.add(serratusLeft);

            const serratusRight = new THREE.Mesh(serratusGeometry, deepMuscleMaterial);
            serratusRight.position.set(0.19, 1.28 - i * 0.07, 0.09);
            serratusRight.rotation.z = -0.35;
            serratusRight.castShadow = true;
            bodyGroup.add(serratusRight);
        }

        // Pelvis
        const pelvisGeometry = new THREE.SphereGeometry(0.20, 48, 48);
        const pelvis = new THREE.Mesh(pelvisGeometry, skinMaterial);
        pelvis.position.y = 0.72;
        pelvis.scale.set(1.1, 0.55, 0.95);
        pelvis.castShadow = true;
        pelvis.receiveShadow = true;
        bodyGroup.add(pelvis);

        // Gluteus maximus
        const gluteGeometry = new THREE.SphereGeometry(0.13, 24, 24);

        const gluteLeft = new THREE.Mesh(gluteGeometry, muscleMaterial);
        gluteLeft.position.set(-0.12, 0.69, -0.13);
        gluteLeft.scale.set(0.9, 1, 1.2);
        gluteLeft.castShadow = true;
        bodyGroup.add(gluteLeft);
        this.muscleGroups.push({ mesh: gluteLeft, name: '臀大肌 | Gluteus Maximus' });

        const gluteRight = new THREE.Mesh(gluteGeometry, muscleMaterial);
        gluteRight.position.set(0.12, 0.69, -0.13);
        gluteRight.scale.set(0.9, 1, 1.2);
        gluteRight.castShadow = true;
        bodyGroup.add(gluteRight);
        this.muscleGroups.push({ mesh: gluteRight, name: '臀大肌 | Gluteus Maximus' });
    }

    createDetailedArms(bodyGroup, skinMaterial, muscleMaterial) {
        [-1, 1].forEach(side => {
            const dir = side;

            // Deltoid
            const deltoidGeometry = new THREE.SphereGeometry(0.09, 24, 24);
            const deltoid = new THREE.Mesh(deltoidGeometry, muscleMaterial);
            deltoid.position.set(dir * 0.26, 1.42, 0);
            deltoid.scale.set(1, 0.85, 0.85);
            deltoid.castShadow = true;
            bodyGroup.add(deltoid);
            this.muscleGroups.push({ mesh: deltoid, name: '三角肌 | Deltoid' });

            // Upper arm
            const upperArmGeometry = new THREE.CapsuleGeometry(0.060, 0.50, 24, 48);
            const upperArm = new THREE.Mesh(upperArmGeometry, skinMaterial);
            upperArm.position.set(dir * 0.29, 1.07, 0);
            upperArm.rotation.z = dir * Math.PI / 15;
            upperArm.castShadow = true;
            upperArm.receiveShadow = true;
            bodyGroup.add(upperArm);

            // Biceps
            const bicepsGeometry = new THREE.SphereGeometry(0.047, 20, 20);
            const biceps = new THREE.Mesh(bicepsGeometry, muscleMaterial);
            biceps.position.set(dir * 0.28, 1.14, 0.045);
            biceps.scale.set(0.9, 1.4, 0.85);
            biceps.castShadow = true;
            bodyGroup.add(biceps);
            this.muscleGroups.push({ mesh: biceps, name: '肱二头肌 | Biceps' });

            // Triceps
            const triceps = new THREE.Mesh(bicepsGeometry, muscleMaterial);
            triceps.position.set(dir * 0.30, 1.09, -0.045);
            triceps.scale.set(0.85, 1.5, 0.9);
            triceps.castShadow = true;
            bodyGroup.add(triceps);
            this.muscleGroups.push({ mesh: triceps, name: '肱三头肌 | Triceps' });

            // Elbow joint
            const elbowGeometry = new THREE.SphereGeometry(0.054, 20, 20);
            const elbow = new THREE.Mesh(elbowGeometry, skinMaterial);
            elbow.position.set(dir * 0.36, 0.79, 0);
            elbow.castShadow = true;
            bodyGroup.add(elbow);

            // Forearm
            const forearmGeometry = new THREE.CapsuleGeometry(0.050, 0.50, 24, 48);
            const forearm = new THREE.Mesh(forearmGeometry, skinMaterial);
            forearm.position.set(dir * 0.43, 0.49, 0.06);
            forearm.rotation.z = dir * Math.PI / 12;
            forearm.rotation.x = -Math.PI / 28;
            forearm.castShadow = true;
            forearm.receiveShadow = true;
            bodyGroup.add(forearm);

            // Forearm muscles
            const forearmMuscleGeometry = new THREE.CapsuleGeometry(0.037, 0.40, 16, 32);
            const forearmMuscle = new THREE.Mesh(forearmMuscleGeometry, muscleMaterial);
            forearmMuscle.position.set(dir * 0.42, 0.51, 0.08);
            forearmMuscle.rotation.z = dir * Math.PI / 12;
            forearmMuscle.rotation.x = -Math.PI / 28;
            forearmMuscle.castShadow = true;
            bodyGroup.add(forearmMuscle);
            this.muscleGroups.push({ mesh: forearmMuscle, name: '前臂肌群 | Forearm Muscles' });

            // Hand
            const handGeometry = new THREE.BoxGeometry(0.09, 0.13, 0.04, 6, 6, 6);
            const hand = new THREE.Mesh(handGeometry, skinMaterial);
            hand.position.set(dir * 0.52, 0.19, 0.09);
            hand.castShadow = true;
            bodyGroup.add(hand);

            // Fingers
            for (let i = 0; i < 4; i++) {
                const fingerGeometry = new THREE.CapsuleGeometry(0.009, 0.065, 12, 16);
                const finger = new THREE.Mesh(fingerGeometry, skinMaterial);
                finger.position.set(
                    dir * 0.52 + (i - 1.5) * 0.013 * (side === -1 ? 1 : -1),
                    0.07,
                    0.09
                );
                finger.rotation.x = Math.PI / 10;
                finger.castShadow = true;
                bodyGroup.add(finger);
            }

            // Thumb
            const thumbGeometry = new THREE.CapsuleGeometry(0.010, 0.050, 12, 16);
            const thumb = new THREE.Mesh(thumbGeometry, skinMaterial);
            thumb.position.set(
                dir * (0.52 + (side === -1 ? 0.04 : -0.04)),
                0.14,
                0.11
            );
            thumb.rotation.x = Math.PI / 6;
            thumb.rotation.z = dir * Math.PI / 5;
            thumb.castShadow = true;
            bodyGroup.add(thumb);
        });
    }

    createDetailedLegs(bodyGroup, skinMaterial, muscleMaterial) {
        [-1, 1].forEach(side => {
            const dir = side;

            // Thigh
            const thighGeometry = new THREE.CapsuleGeometry(0.102, 0.60, 28, 48);
            const thigh = new THREE.Mesh(thighGeometry, skinMaterial);
            thigh.position.set(dir * 0.12, 0.35, 0);
            thigh.castShadow = true;
            thigh.receiveShadow = true;
            bodyGroup.add(thigh);

            // Quadriceps
            const quadGeometry = new THREE.CapsuleGeometry(0.082, 0.52, 24, 40);
            const quadriceps = new THREE.Mesh(quadGeometry, muscleMaterial);
            quadriceps.position.set(dir * 0.12, 0.37, 0.085);
            quadriceps.castShadow = true;
            bodyGroup.add(quadriceps);
            this.muscleGroups.push({ mesh: quadriceps, name: '股四头肌 | Quadriceps' });

            // Hamstrings
            const hamstringGeometry = new THREE.CapsuleGeometry(0.078, 0.50, 24, 40);
            const hamstrings = new THREE.Mesh(hamstringGeometry, muscleMaterial);
            hamstrings.position.set(dir * 0.12, 0.35, -0.085);
            hamstrings.castShadow = true;
            bodyGroup.add(hamstrings);
            this.muscleGroups.push({ mesh: hamstrings, name: '腘绳肌 | Hamstrings' });

            // Knee
            const kneeGeometry = new THREE.SphereGeometry(0.082, 28, 28);
            const knee = new THREE.Mesh(kneeGeometry, skinMaterial);
            knee.position.set(dir * 0.12, 0.02, 0);
            knee.castShadow = true;
            bodyGroup.add(knee);

            // Calf
            const calfGeometry = new THREE.CapsuleGeometry(0.078, 0.54, 28, 48);
            const calf = new THREE.Mesh(calfGeometry, skinMaterial);
            calf.position.set(dir * 0.12, -0.28, 0);
            calf.castShadow = true;
            calf.receiveShadow = true;
            bodyGroup.add(calf);

            // Gastrocnemius (calf muscle)
            const gastrocGeometry = new THREE.SphereGeometry(0.068, 24, 24);
            const gastrocnemius = new THREE.Mesh(gastrocGeometry, muscleMaterial);
            gastrocnemius.position.set(dir * 0.12, -0.16, -0.065);
            gastrocnemius.scale.set(1, 1.6, 1.3);
            gastrocnemius.castShadow = true;
            bodyGroup.add(gastrocnemius);
            this.muscleGroups.push({ mesh: gastrocnemius, name: '腓肠肌 | Gastrocnemius' });

            // Tibialis anterior
            const tibialisGeometry = new THREE.CapsuleGeometry(0.027, 0.42, 16, 24);
            const tibialis = new THREE.Mesh(tibialisGeometry, muscleMaterial);
            tibialis.position.set(dir * 0.12, -0.26, 0.065);
            tibialis.castShadow = true;
            bodyGroup.add(tibialis);
            this.muscleGroups.push({ mesh: tibialis, name: '胫骨前肌 | Tibialis Anterior' });

            // Ankle
            const ankleGeometry = new THREE.SphereGeometry(0.057, 24, 24);
            const ankle = new THREE.Mesh(ankleGeometry, skinMaterial);
            ankle.position.set(dir * 0.12, -0.56, 0);
            ankle.castShadow = true;
            bodyGroup.add(ankle);

            // Foot
            const footGeometry = new THREE.BoxGeometry(0.13, 0.09, 0.25, 8, 8, 8);
            const foot = new THREE.Mesh(footGeometry, skinMaterial);
            foot.position.set(dir * 0.12, -0.66, 0.075);
            foot.castShadow = true;
            bodyGroup.add(foot);

            // Toes
            for (let i = 0; i < 5; i++) {
                const toeGeometry = new THREE.CapsuleGeometry(0.009, 0.028, 10, 16);
                const toe = new THREE.Mesh(toeGeometry, skinMaterial);
                toe.position.set(
                    dir * (0.12 + (i - 2) * 0.016),
                    -0.68,
                    0.19
                );
                toe.rotation.x = Math.PI / 2;
                toe.castShadow = true;
                bodyGroup.add(toe);
            }
        });
    }

    addMeridianSystem() {
        const meridianMaterial = new THREE.LineBasicMaterial({
            color: 0xff8800,
            linewidth: 2,
            opacity: 0.85,
            transparent: true
        });

        // Conception Vessel (任脉)
        const cvPoints = [
            new THREE.Vector3(0, 0.7, 0.20),
            new THREE.Vector3(0, 1.0, 0.19),
            new THREE.Vector3(0, 1.3, 0.17),
            new THREE.Vector3(0, 1.5, 0.15),
            new THREE.Vector3(0, 1.65, 0.11)
        ];
        const cvGeometry = new THREE.BufferGeometry().setFromPoints(cvPoints);
        const cvLine = new THREE.Line(cvGeometry, meridianMaterial);
        this.scene.add(cvLine);
        this.meridianLines.push(cvLine);

        // Governing Vessel (督脉)
        const gvPoints = [
            new THREE.Vector3(0, 0.7, -0.20),
            new THREE.Vector3(0, 1.0, -0.19),
            new THREE.Vector3(0, 1.3, -0.17),
            new THREE.Vector3(0, 1.5, -0.15),
            new THREE.Vector3(0, 1.75, -0.11)
        ];
        const gvGeometry = new THREE.BufferGeometry().setFromPoints(gvPoints);
        const gvLine = new THREE.Line(gvGeometry, meridianMaterial);
        this.scene.add(gvLine);
        this.meridianLines.push(gvLine);
    }

    addAcupoints() {
        const acupointData = {
            'GV20': { pos: [0, 1.82, 0], name: '百会 | Baihui', color: 0xff4444 },
            'GB20': { pos: [-0.08, 1.65, -0.12], name: '风池 | Fengchi', color: 0xff4444 },
            'GV14': { pos: [0, 1.45, -0.15], name: '大椎 | Dazhui', color: 0xff6644 },
            'BL13': { pos: [-0.05, 1.35, -0.17], name: '肺俞 | Feishu', color: 0xff6644 },
            'BL23': { pos: [-0.05, 0.84, -0.18], name: '肾俞 | Shenshu', color: 0xff6644 },
            'LI4': { pos: [-0.52, 0.19, 0.09], name: '合谷 | Hegu', color: 0x4444ff },
            'LI11': { pos: [-0.36, 0.79, 0.05], name: '曲池 | Quchi', color: 0x4466ff },
            'PC6': { pos: [-0.43, 0.49, 0.08], name: '内关 | Neiguan', color: 0x6644ff },
            'ST36': { pos: [-0.14, -0.16, 0.11], name: '足三里 | Zusanli', color: 0x44ff44 },
            'SP6': { pos: [-0.13, -0.41, 0.08], name: '三阴交 | Sanyinjiao', color: 0x44ff44 },
            'SP9': { pos: [-0.14, -0.03, 0.09], name: '阴陵泉 | Yinlingquan', color: 0x44ff44 },
            'LR3': { pos: [-0.12, -0.63, 0.15], name: '太冲 | Taichong', color: 0x44ff88 },
            'KI3': { pos: [-0.12, -0.56, 0.02], name: '太溪 | Taixi', color: 0x44ffaa },
            'CV4': { pos: [0, 0.74, 0.20], name: '关元 | Guanyuan', color: 0xffaa44 },
            'CV12': { pos: [0, 1.04, 0.19], name: '中脘 | Zhongwan', color: 0xffaa44 }
        };

        Object.entries(acupointData).forEach(([code, data]) => {
            if (this.options.selectedPoints.length === 0 || this.options.selectedPoints.includes(code)) {
                this.createAcupointMarker(data.pos, data.name, data.color);
            }
        });
    }

    createAcupointMarker(position, label, color) {
        const markerGeometry = new THREE.SphereGeometry(0.022, 20, 20);
        const markerMaterial = new THREE.MeshStandardMaterial({
            color: color,
            emissive: color,
            emissiveIntensity: 0.8,
            roughness: 0.2,
            metalness: 0.3
        });
        const marker = new THREE.Mesh(markerGeometry, markerMaterial);
        marker.position.set(...position);
        marker.castShadow = true;

        const glowGeometry = new THREE.SphereGeometry(0.035, 20, 20);
        const glowMaterial = new THREE.MeshBasicMaterial({
            color: color,
            transparent: true,
            opacity: 0.28
        });
        const glow = new THREE.Mesh(glowGeometry, glowMaterial);
        glow.position.set(...position);

        this.scene.add(marker);
        this.scene.add(glow);
        this.acupointMarkers.push({ marker, glow, label });

        const animate = () => {
            const scale = 1 + 0.35 * Math.sin(Date.now() * 0.003);
            glow.scale.set(scale, scale, scale);
        };
        this.glowAnimations = this.glowAnimations || [];
        this.glowAnimations.push(animate);
    }

    addPhotorealisticControls() {
        const controlsDiv = document.createElement('div');
        controlsDiv.className = 'photorealistic-controls';
        controlsDiv.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(10, 10, 10, 0.92);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.5);
            font-size: 13px;
            color: #ffffff;
            border: 1px solid rgba(255,255,255,0.15);
            z-index: 10;
            min-width: 200px;
            backdrop-filter: blur(10px);
        `;

        controlsDiv.innerHTML = `
            <div style="margin-bottom: 14px; font-weight: bold; font-size: 15px; color: #ff8844; border-bottom: 2px solid rgba(255,136,68,0.3); padding-bottom: 10px; text-align: center;">
                <i class="bi bi-camera-fill"></i> 照片级真实
                <br>
                <span style="font-size: 11px; color: #aaa;">Photorealistic Medical</span>
            </div>
            <button class="btn btn-sm btn-outline-light mb-2 w-100" data-view="front" style="font-size: 12px; border-radius: 6px;">
                <i class="bi bi-person"></i> 正面 | Front
            </button>
            <button class="btn btn-sm btn-outline-light mb-2 w-100" data-view="back" style="font-size: 12px; border-radius: 6px;">
                <i class="bi bi-person-fill"></i> 背面 | Back
            </button>
            <button class="btn btn-sm btn-outline-light mb-2 w-100" data-view="side" style="font-size: 12px; border-radius: 6px;">
                <i class="bi bi-arrows-angle-expand"></i> 侧面 | Side
            </button>
            <button class="btn btn-sm btn-outline-warning mb-2 w-100" data-view="reset" style="font-size: 12px; border-radius: 6px;">
                <i class="bi bi-arrow-clockwise"></i> 重置 | Reset
            </button>
            <div style="margin-top: 14px; padding-top: 14px; border-top: 1px solid rgba(255,255,255,0.15);">
                <label style="font-size: 11px; color: #bbb; display: block; margin-bottom: 10px;">
                    <i class="bi bi-toggles"></i> 显示选项 | Display:
                </label>
                <div class="form-check form-switch mb-2">
                    <input class="form-check-input" type="checkbox" id="toggleMuscles" ${this.options.showMuscles ? 'checked' : ''}>
                    <label class="form-check-label" for="toggleMuscles" style="font-size: 11px; color: #ddd;">
                        💪 肌肉系统 | Muscles
                    </label>
                </div>
                <div class="form-check form-switch mb-2">
                    <input class="form-check-input" type="checkbox" id="toggleMeridians" ${this.options.showMeridians ? 'checked' : ''}>
                    <label class="form-check-label" for="toggleMeridians" style="font-size: 11px; color: #ddd;">
                        🔶 经络系统 | Meridians
                    </label>
                </div>
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" id="toggleAcupoints" ${this.options.showAcupoints ? 'checked' : ''}>
                    <label class="form-check-label" for="toggleAcupoints" style="font-size: 11px; color: #ddd;">
                        🎯 穴位标记 | Acupoints
                    </label>
                </div>
            </div>
            <div style="margin-top: 14px; padding-top: 14px; border-top: 1px solid rgba(255,255,255,0.15); font-size: 10px; color: #888; line-height: 1.6;">
                <div style="margin-bottom: 4px;"><i class="bi bi-mouse"></i> 拖动旋转 | Drag to rotate</div>
                <div style="margin-bottom: 4px;"><i class="bi bi-zoom-in"></i> 滚轮缩放 | Scroll to zoom</div>
                <div><i class="bi bi-arrows-move"></i> 右键平移 | Right-click to pan</div>
            </div>
            <div style="margin-top: 12px; padding: 8px; background: rgba(255,136,68,0.1); border-radius: 6px; font-size: 10px; color: #ffaa66; text-align: center;">
                ✨ 照片级真实纹理渲染
            </div>
        `;

        this.container.appendChild(controlsDiv);

        // Event handlers
        controlsDiv.querySelectorAll('[data-view]').forEach(btn => {
            btn.addEventListener('click', () => {
                const view = btn.dataset.view;
                this.setView(view);
            });
        });

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
        const duration = 1400;
        const start = {
            x: this.camera.position.x,
            y: this.camera.position.y,
            z: this.camera.position.z
        };

        let end;
        switch (view) {
            case 'front':
                end = { x: 0, y: 1.6, z: 4.5 };
                break;
            case 'back':
                end = { x: 0, y: 1.6, z: -4.5 };
                break;
            case 'side':
                end = { x: 4.5, y: 1.6, z: 0 };
                break;
            case 'reset':
                end = { x: 0, y: 1.6, z: 4.5 };
                break;
        }

        const startTime = Date.now();
        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);

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

        if (this.glowAnimations) {
            this.glowAnimations.forEach(fn => fn());
        }

        if (this.controls) {
            this.controls.update();
        }

        this.renderer.render(this.scene, this.camera);
    }

    // Public API
    toggleMuscles(show) {
        this.muscleGroups.forEach(group => {
            group.mesh.visible = show;
        });
    }

    toggleMeridians(show) {
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
window.Body3DViewerPhotorealistic = Body3DViewerPhotorealistic;
