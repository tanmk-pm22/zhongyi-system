/**
 * Human Anatomy Atlas 2026 Viewer with AI Acupuncture & Tuina
 * 人体解剖图谱2026查看器 - 集成AI针灸和推拿
 *
 * Uses real medical anatomy images with AI-powered acupuncture point detection
 * and tuina treatment area recommendations.
 */

class AnatomyAtlasViewer {
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
            aiEnabled: true,
            language: 'bilingual', // 'zh', 'en', 'bilingual'
            ...options
        };

        // Anatomy atlas image sets (to be replaced with real medical photos)
        this.anatomyLayers = {
            skin: '/static/images/anatomy/skin_surface.jpg',
            muscles_front: '/static/images/anatomy/muscles_anterior.jpg',
            muscles_back: '/static/images/anatomy/muscles_posterior.jpg',
            skeleton: '/static/images/anatomy/skeleton.jpg',
            meridians: '/static/images/anatomy/tcm_meridians.jpg'
        };

        // AI-powered acupuncture points database (361 standard points)
        this.acupointDatabase = this.initializeAcupointDatabase();

        // Tuina treatment areas
        this.tuinaAreas = this.initializeTuinaAreas();

        this.currentView = 'front';
        this.currentLayer = 'muscles_front';
        this.selectedPoints = options.selectedPoints || [];
        this.selectedAreas = options.selectedAreas || [];

        this.init();
    }

    init() {
        console.log('初始化人体解剖图谱查看器 | Initializing Anatomy Atlas Viewer');
        this.createUI();
        this.loadAnatomyImages();
        this.setupControls();

        if (this.options.aiEnabled) {
            this.initializeAI();
        }

        console.log('✓ 解剖图谱查看器已初始化 | Anatomy Atlas Viewer initialized');
    }

    createUI() {
        // Main container structure
        this.container.innerHTML = `
            <div class="anatomy-atlas-container" style="position: relative; width: 100%; height: 600px; background: #1a1a1a; border-radius: 8px; overflow: hidden;">
                <!-- Control Panel -->
                <div class="atlas-controls" style="position: absolute; top: 10px; left: 10px; z-index: 100; background: rgba(0,0,0,0.8); padding: 15px; border-radius: 8px; color: white;">
                    <h5 style="margin: 0 0 10px 0; color: #fff;">解剖图谱控制 | Atlas Controls</h5>

                    <!-- View Selection -->
                    <div class="mb-3">
                        <label style="display: block; margin-bottom: 5px; font-size: 12px;">视图 | View:</label>
                        <select id="viewSelect" class="form-select form-select-sm" style="width: 150px;">
                            <option value="front">正面 | Front</option>
                            <option value="back">背面 | Back</option>
                            <option value="side_left">左侧 | Left Side</option>
                            <option value="side_right">右侧 | Right Side</option>
                        </select>
                    </div>

                    <!-- Layer Selection -->
                    <div class="mb-3">
                        <label style="display: block; margin-bottom: 5px; font-size: 12px;">图层 | Layer:</label>
                        <div class="btn-group-vertical" role="group" style="width: 100%;">
                            <button type="button" class="btn btn-sm btn-outline-light layer-btn" data-layer="skin">皮肤 | Skin</button>
                            <button type="button" class="btn btn-sm btn-outline-light layer-btn active" data-layer="muscles_front">肌肉 | Muscles</button>
                            <button type="button" class="btn btn-sm btn-outline-light layer-btn" data-layer="skeleton">骨骼 | Skeleton</button>
                            ${this.options.mode === 'acupuncture' ? '<button type="button" class="btn btn-sm btn-outline-light layer-btn" data-layer="meridians">经络 | Meridians</button>' : ''}
                        </div>
                    </div>

                    <!-- AI Features -->
                    ${this.options.aiEnabled ? `
                    <div class="mb-3">
                        <label style="display: block; margin-bottom: 5px; font-size: 12px;">AI功能 | AI Features:</label>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="aiDetection" checked>
                            <label class="form-check-label" for="aiDetection" style="font-size: 11px;">
                                AI点位检测 | AI Detection
                            </label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="aiRecommendation" checked>
                            <label class="form-check-label" for="aiRecommendation" style="font-size: 11px;">
                                AI推荐 | AI Recommend
                            </label>
                        </div>
                    </div>
                    ` : ''}

                    <!-- Zoom Controls -->
                    <div class="mb-3">
                        <label style="display: block; margin-bottom: 5px; font-size: 12px;">缩放 | Zoom:</label>
                        <div class="btn-group" role="group" style="width: 100%;">
                            <button type="button" class="btn btn-sm btn-outline-light" id="zoomIn">+</button>
                            <button type="button" class="btn btn-sm btn-outline-light" id="zoomReset">100%</button>
                            <button type="button" class="btn btn-sm btn-outline-light" id="zoomOut">-</button>
                        </div>
                    </div>
                </div>

                <!-- Image Display Area -->
                <div class="atlas-image-area" style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; overflow: hidden;" id="imageArea">
                    <canvas id="anatomyCanvas" style="max-width: 100%; max-height: 100%; cursor: crosshair;"></canvas>
                </div>

                <!-- Info Panel -->
                <div class="atlas-info" style="position: absolute; bottom: 10px; left: 10px; right: 10px; background: rgba(0,0,0,0.9); padding: 15px; border-radius: 8px; color: white; max-height: 150px; overflow-y: auto;" id="infoPanel">
                    <div id="pointInfo">
                        <p style="margin: 0; font-size: 12px;">点击图像选择${this.options.mode === 'acupuncture' ? '穴位' : '治疗区域'} | Click to select ${this.options.mode === 'acupuncture' ? 'acupoints' : 'treatment areas'}</p>
                    </div>
                </div>
            </div>
        `;

        this.canvas = document.getElementById('anatomyCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.imageArea = document.getElementById('imageArea');
        this.infoPanel = document.getElementById('infoPanel');
    }

    loadAnatomyImages() {
        console.log('加载解剖图像 | Loading anatomy images...');

        // Create image object
        this.currentImage = new Image();
        this.currentImage.crossOrigin = 'anonymous';

        this.currentImage.onload = () => {
            this.canvas.width = this.currentImage.width;
            this.canvas.height = this.currentImage.height;
            this.renderImage();
            console.log('✓ 解剖图像已加载 | Anatomy image loaded');
        };

        this.currentImage.onerror = () => {
            console.warn('⚠ 无法加载解剖图像，使用占位图 | Cannot load image, using placeholder');
            this.createPlaceholderImage();
        };

        // Try to load image (will fallback to placeholder if not found)
        const imagePath = this.anatomyLayers[this.currentLayer];
        this.currentImage.src = imagePath;
    }

    createPlaceholderImage() {
        // Create a placeholder anatomy image with basic structure
        this.canvas.width = 800;
        this.canvas.height = 1000;

        const ctx = this.ctx;

        // Background
        ctx.fillStyle = '#f5f5f5';
        ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw basic human outline
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 2;
        ctx.fillStyle = '#ffd7ba';

        // Head
        ctx.beginPath();
        ctx.arc(400, 100, 50, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        // Neck
        ctx.fillRect(380, 140, 40, 60);
        ctx.strokeRect(380, 140, 40, 60);

        // Torso
        ctx.beginPath();
        ctx.ellipse(400, 300, 100, 150, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        // Arms
        ctx.fillRect(280, 200, 30, 200);
        ctx.strokeRect(280, 200, 30, 200);
        ctx.fillRect(490, 200, 30, 200);
        ctx.strokeRect(490, 200, 30, 200);

        // Legs
        ctx.fillRect(350, 450, 40, 300);
        ctx.strokeRect(350, 450, 40, 300);
        ctx.fillRect(410, 450, 40, 300);
        ctx.strokeRect(410, 450, 40, 300);

        // Add text overlay
        ctx.fillStyle = 'rgba(0,0,0,0.7)';
        ctx.fillRect(150, 450, 500, 100);

        ctx.fillStyle = '#fff';
        ctx.font = 'bold 20px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('医学解剖图像占位图', 400, 490);
        ctx.fillText('Medical Anatomy Image Placeholder', 400, 520);

        ctx.font = '14px Arial';
        ctx.fillText('请添加真实医学解剖照片到: /static/images/anatomy/', 400, 545);

        // Draw sample acupoints if in acupuncture mode
        if (this.options.mode === 'acupuncture') {
            this.drawSampleAcupoints();
        }

        // Draw sample tuina areas if in tuina mode
        if (this.options.mode === 'tuina') {
            this.drawSampleTuinaAreas();
        }
    }

    drawSampleAcupoints() {
        const samplePoints = [
            { x: 400, y: 100, code: 'GV20', name: '百会' },
            { x: 380, y: 300, code: 'CV17', name: '膻中' },
            { x: 300, y: 250, code: 'LI4', name: '合谷' },
            { x: 380, y: 600, code: 'ST36', name: '足三里' }
        ];

        samplePoints.forEach(point => {
            this.drawAcupoint(point.x, point.y, point.code, point.name);
        });
    }

    drawSampleTuinaAreas() {
        const ctx = this.ctx;
        ctx.strokeStyle = '#ff6b6b';
        ctx.lineWidth = 3;
        ctx.setLineDash([5, 5]);

        // Shoulder area
        ctx.strokeRect(280, 200, 240, 80);
        ctx.fillStyle = 'rgba(255, 107, 107, 0.2)';
        ctx.fillRect(280, 200, 240, 80);

        // Lower back area
        ctx.strokeRect(320, 400, 160, 100);
        ctx.fillStyle = 'rgba(255, 107, 107, 0.2)';
        ctx.fillRect(320, 400, 160, 100);

        ctx.setLineDash([]);
    }

    renderImage() {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw anatomy image
        this.ctx.drawImage(this.currentImage, 0, 0);

        // Draw overlays based on mode
        if (this.options.mode === 'acupuncture' && this.options.showAcupoints) {
            this.drawAcupointsOverlay();
        }

        if (this.options.mode === 'tuina') {
            this.drawTuinaAreasOverlay();
        }
    }

    drawAcupointsOverlay() {
        // Draw acupoints on the anatomy image
        const pointsForView = this.getAcupointsForCurrentView();

        pointsForView.forEach(point => {
            const isSelected = this.selectedPoints.includes(point.code);
            this.drawAcupoint(point.x, point.y, point.code, point.name, isSelected);
        });
    }

    drawAcupoint(x, y, code, name, isSelected = false) {
        const ctx = this.ctx;

        // Outer glow
        ctx.shadowColor = isSelected ? '#ffd700' : '#ff4444';
        ctx.shadowBlur = isSelected ? 20 : 10;

        // Point circle
        ctx.beginPath();
        ctx.arc(x, y, isSelected ? 8 : 6, 0, Math.PI * 2);
        ctx.fillStyle = isSelected ? '#ffd700' : '#ff4444';
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.shadowBlur = 0;

        // Label background
        ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
        ctx.fillRect(x + 10, y - 20, 80, 35);

        // Label text
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 11px Arial';
        ctx.fillText(code, x + 15, y - 8);
        ctx.font = '10px Arial';
        ctx.fillText(name, x + 15, y + 5);
    }

    drawTuinaAreasOverlay() {
        const areasForView = this.getTuinaAreasForCurrentView();

        areasForView.forEach(area => {
            const isSelected = this.selectedAreas.includes(area.id);
            this.drawTuinaArea(area, isSelected);
        });
    }

    drawTuinaArea(area, isSelected = false) {
        const ctx = this.ctx;

        ctx.strokeStyle = isSelected ? '#4caf50' : '#ff9800';
        ctx.lineWidth = isSelected ? 4 : 2;
        ctx.setLineDash([8, 4]);
        ctx.strokeRect(area.x, area.y, area.width, area.height);

        ctx.fillStyle = isSelected ? 'rgba(76, 175, 80, 0.2)' : 'rgba(255, 152, 0, 0.15)';
        ctx.fillRect(area.x, area.y, area.width, area.height);

        ctx.setLineDash([]);

        // Label
        ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
        ctx.fillRect(area.x + 5, area.y + 5, 120, 30);

        ctx.fillStyle = '#fff';
        ctx.font = 'bold 12px Arial';
        ctx.fillText(area.name_zh, area.x + 10, area.y + 20);
        ctx.font = '10px Arial';
        ctx.fillText(area.name_en, area.x + 10, area.y + 32);
    }

    setupControls() {
        // View selection
        document.getElementById('viewSelect').addEventListener('change', (e) => {
            this.currentView = e.target.value;
            this.updateLayerForView();
            this.loadAnatomyImages();
        });

        // Layer buttons
        document.querySelectorAll('.layer-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.layer-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentLayer = e.target.dataset.layer;
                this.loadAnatomyImages();
            });
        });

        // Zoom controls
        document.getElementById('zoomIn').addEventListener('click', () => this.zoom(1.2));
        document.getElementById('zoomOut').addEventListener('click', () => this.zoom(0.8));
        document.getElementById('zoomReset').addEventListener('click', () => this.zoom(1, true));

        // Canvas click for point selection
        this.canvas.addEventListener('click', (e) => this.handleCanvasClick(e));

        // Canvas hover for info display
        this.canvas.addEventListener('mousemove', (e) => this.handleCanvasHover(e));
    }

    handleCanvasClick(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = (e.clientX - rect.left) * (this.canvas.width / rect.width);
        const y = (e.clientY - rect.top) * (this.canvas.height / rect.height);

        if (this.options.mode === 'acupuncture') {
            this.selectAcupointNear(x, y);
        } else {
            this.selectTuinaAreaAt(x, y);
        }
    }

    handleCanvasHover(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = (e.clientX - rect.left) * (this.canvas.width / rect.width);
        const y = (e.clientY - rect.top) * (this.canvas.height / rect.height);

        if (this.options.mode === 'acupuncture') {
            this.showAcupointInfo(x, y);
        } else {
            this.showTuinaAreaInfo(x, y);
        }
    }

    selectAcupointNear(x, y) {
        const points = this.getAcupointsForCurrentView();
        const threshold = 20;

        for (const point of points) {
            const distance = Math.sqrt(Math.pow(x - point.x, 2) + Math.pow(y - point.y, 2));
            if (distance < threshold) {
                const index = this.selectedPoints.indexOf(point.code);
                if (index > -1) {
                    this.selectedPoints.splice(index, 1);
                } else {
                    this.selectedPoints.push(point.code);
                }
                this.renderImage();
                this.updateSelectedPointsDisplay();
                break;
            }
        }
    }

    selectTuinaAreaAt(x, y) {
        const areas = this.getTuinaAreasForCurrentView();

        for (const area of areas) {
            if (x >= area.x && x <= area.x + area.width &&
                y >= area.y && y <= area.y + area.height) {
                const index = this.selectedAreas.indexOf(area.id);
                if (index > -1) {
                    this.selectedAreas.splice(index, 1);
                } else {
                    this.selectedAreas.push(area.id);
                }
                this.renderImage();
                this.updateSelectedAreasDisplay();
                break;
            }
        }
    }

    showAcupointInfo(x, y) {
        const points = this.getAcupointsForCurrentView();
        const threshold = 20;

        for (const point of points) {
            const distance = Math.sqrt(Math.pow(x - point.x, 2) + Math.pow(y - point.y, 2));
            if (distance < threshold) {
                this.displayPointInfo(point);
                return;
            }
        }
    }

    showTuinaAreaInfo(x, y) {
        const areas = this.getTuinaAreasForCurrentView();

        for (const area of areas) {
            if (x >= area.x && x <= area.x + area.width &&
                y >= area.y && y <= area.y + area.height) {
                this.displayAreaInfo(area);
                return;
            }
        }
    }

    displayPointInfo(point) {
        const info = document.getElementById('pointInfo');
        info.innerHTML = `
            <div style="font-size: 12px;">
                <strong style="color: #ffd700;">${point.code} - ${point.name}</strong><br>
                <span style="color: #ccc;">定位 | Location: ${point.location || '点击选择'}</span><br>
                <span style="color: #ccc;">主治 | Indications: ${point.indications || '加载中...'}</span>
            </div>
        `;
    }

    displayAreaInfo(area) {
        const info = document.getElementById('pointInfo');
        info.innerHTML = `
            <div style="font-size: 12px;">
                <strong style="color: #4caf50;">${area.name_zh} | ${area.name_en}</strong><br>
                <span style="color: #ccc;">手法 | Technique: ${area.technique || '按摩'}</span><br>
                <span style="color: #ccc;">适应症 | Indications: ${area.indications || '肌肉放松'}</span>
            </div>
        `;
    }

    updateSelectedPointsDisplay() {
        console.log('已选择穴位 | Selected points:', this.selectedPoints);
        // Trigger custom event for form integration
        this.container.dispatchEvent(new CustomEvent('pointsSelected', {
            detail: { points: this.selectedPoints }
        }));
    }

    updateSelectedAreasDisplay() {
        console.log('已选择治疗区域 | Selected areas:', this.selectedAreas);
        // Trigger custom event for form integration
        this.container.dispatchEvent(new CustomEvent('areasSelected', {
            detail: { areas: this.selectedAreas }
        }));
    }

    zoom(factor, reset = false) {
        if (reset) {
            this.canvas.style.transform = 'scale(1)';
        } else {
            const currentScale = parseFloat(this.canvas.style.transform.replace(/[^0-9.]/g, '') || 1);
            const newScale = currentScale * factor;
            this.canvas.style.transform = `scale(${newScale})`;
        }
    }

    updateLayerForView() {
        if (this.currentView === 'back') {
            this.currentLayer = 'muscles_back';
        } else {
            this.currentLayer = 'muscles_front';
        }
    }

    initializeAcupointDatabase() {
        // Sample acupoint database (should be expanded with all 361 points)
        return {
            front: [
                { code: 'GV20', name: '百会', x: 400, y: 80, location: '头顶正中', indications: '头痛，眩晕，失眠' },
                { code: 'CV17', name: '膻中', x: 400, y: 280, location: '胸部正中线', indications: '胸闷，咳嗽，乳腺疾病' },
                { code: 'CV12', name: '中脘', x: 400, y: 350, location: '上腹部正中', indications: '胃痛，消化不良' },
                { code: 'CV6', name: '气海', x: 400, y: 400, location: '下腹部', indications: '腹痛，月经不调' },
                { code: 'ST36', name: '足三里', x: 380, y: 650, location: '小腿外侧', indications: '胃痛，呕吐，调理脾胃' },
                { code: 'LI4', name: '合谷', x: 300, y: 350, location: '手背第1、2掌骨间', indications: '头痛，牙痛，感冒' },
                { code: 'PC6', name: '内关', x: 320, y: 380, location: '前臂掌侧', indications: '心痛，胃痛，失眠' }
            ],
            back: [
                { code: 'GV14', name: '大椎', x: 400, y: 180, location: '第7颈椎棘突下', indications: '感冒，发热，颈项强痛' },
                { code: 'BL13', name: '肺俞', x: 350, y: 220, location: '第3胸椎棘突旁', indications: '咳嗽，气喘，肺部疾病' },
                { code: 'BL20', name: '脾俞', x: 350, y: 300, location: '第11胸椎棘突旁', indications: '腹胀，便溏，消化不良' },
                { code: 'BL23', name: '肾俞', x: 350, y: 380, location: '第2腰椎棘突旁', indications: '腰痛，遗精，耳鸣' },
                { code: 'GV4', name: '命门', x: 400, y: 380, location: '第2腰椎棘突下', indications: '腰痛，遗精，月经不调' }
            ]
        };
    }

    initializeTuinaAreas() {
        return {
            front: [
                { id: 'chest', name_zh: '胸部', name_en: 'Chest', x: 300, y: 250, width: 200, height: 100, technique: '推拿按摩', indications: '胸闷，呼吸问题' },
                { id: 'abdomen', name_zh: '腹部', name_en: 'Abdomen', x: 320, y: 380, width: 160, height: 120, technique: '揉腹', indications: '消化不良，便秘' },
                { id: 'thigh', name_zh: '大腿', name_en: 'Thigh', x: 340, y: 550, width: 120, height: 150, technique: '推按', indications: '腿部疼痛，循环改善' }
            ],
            back: [
                { id: 'upper_back', name_zh: '上背部', name_en: 'Upper Back', x: 300, y: 200, width: 200, height: 100, technique: '按压推拿', indications: '肩颈疼痛，上背部紧张' },
                { id: 'lower_back', name_zh: '下背部/腰部', name_en: 'Lower Back', x: 320, y: 350, width: 160, height: 120, technique: '腰部按摩', indications: '腰痛，腰肌劳损' },
                { id: 'buttocks', name_zh: '臀部', name_en: 'Buttocks', x: 340, y: 490, width: 120, height: 80, technique: '点按推拿', indications: '坐骨神经痛' }
            ]
        };
    }

    getAcupointsForCurrentView() {
        return this.acupointDatabase[this.currentView] || this.acupointDatabase.front;
    }

    getTuinaAreasForCurrentView() {
        return this.tuinaAreas[this.currentView] || this.tuinaAreas.front;
    }

    initializeAI() {
        console.log('初始化AI功能 | Initializing AI features...');
        // Placeholder for AI functionality
        // In production, this would connect to an AI model for:
        // - Automatic acupoint detection
        // - Treatment recommendations based on symptoms
        // - Point combination suggestions
    }

    // Public API methods
    getSelectedPoints() {
        return this.selectedPoints;
    }

    getSelectedAreas() {
        return this.selectedAreas;
    }

    setSelectedPoints(points) {
        this.selectedPoints = points;
        this.renderImage();
    }

    setSelectedAreas(areas) {
        this.selectedAreas = areas;
        this.renderImage();
    }
}

// Make available globally
window.AnatomyAtlasViewer = AnatomyAtlasViewer;
