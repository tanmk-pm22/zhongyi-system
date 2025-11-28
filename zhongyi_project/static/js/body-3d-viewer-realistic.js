/**
 * Realistic 3D Human Body Viewer for Acupuncture and Tuina
 * 真实人体3D图解 - 针灸和推拿
 *
 * Features:
 * - Realistic human body SVG graphics
 * - Anatomically accurate proportions
 * - High-quality acupoint and treatment area markers
 * - Professional medical visualization
 */

class Body3DViewerRealistic {
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

        this.init();
    }

    init() {
        // Create SVG container
        this.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        this.svg.setAttribute('width', '100%');
        this.svg.setAttribute('height', '100%');
        this.svg.setAttribute('viewBox', '0 0 400 600');
        this.svg.style.background = 'linear-gradient(to bottom, #f0f4f8, #e8f0f7)';
        this.container.appendChild(this.svg);

        // Add controls
        this.addControls();

        // Initialize state
        this.viewMode = 'front';
        this.zoom = 1;

        // Bind events
        this.bindEvents();

        // Render
        this.render();

        console.log('真实人体3D图解已初始化 | Realistic 3D Body Viewer initialized');
    }

    addControls() {
        const controlsDiv = document.createElement('div');
        controlsDiv.className = 'body-3d-controls mb-3 d-flex justify-content-between align-items-center';
        controlsDiv.innerHTML = `
            <div class="btn-group btn-group-sm" role="group">
                <button type="button" class="btn btn-primary view-front active">
                    <i class="bi bi-person"></i> 正面 | Front
                </button>
                <button type="button" class="btn btn-outline-primary view-back">
                    <i class="bi bi-person-fill"></i> 背面 | Back
                </button>
            </div>
            <div class="btn-group btn-group-sm" role="group">
                <button type="button" class="btn btn-outline-secondary zoom-in" title="放大 | Zoom In">
                    <i class="bi bi-zoom-in"></i>
                </button>
                <button type="button" class="btn btn-outline-secondary zoom-out" title="缩小 | Zoom Out">
                    <i class="bi bi-zoom-out"></i>
                </button>
                <button type="button" class="btn btn-outline-secondary reset-view" title="重置 | Reset">
                    <i class="bi bi-arrow-clockwise"></i>
                </button>
            </div>
        `;
        this.container.parentElement.insertBefore(controlsDiv, this.container);

        // Bind control events
        controlsDiv.querySelector('.view-front').addEventListener('click', () => this.setView('front'));
        controlsDiv.querySelector('.view-back').addEventListener('click', () => this.setView('back'));
        controlsDiv.querySelector('.zoom-in').addEventListener('click', () => this.adjustZoom(0.2));
        controlsDiv.querySelector('.zoom-out').addEventListener('click', () => this.adjustZoom(-0.2));
        controlsDiv.querySelector('.reset-view').addEventListener('click', () => this.resetView());

        this.controlsDiv = controlsDiv;
    }

    bindEvents() {
        // Click events for acupoint/area selection
        this.svg.addEventListener('click', (e) => {
            if (e.target.classList.contains('acupoint') || e.target.classList.contains('treatment-area')) {
                const code = e.target.getAttribute('data-code');
                const name = e.target.getAttribute('data-name');

                if (this.options.showAcupoints) {
                    this.toggleAcupoint(code, name);
                } else if (this.options.showMuscles) {
                    this.toggleArea(code, name);
                }
            }
        });

        // Mouse wheel for zoom
        this.container.addEventListener('wheel', (e) => {
            e.preventDefault();
            const delta = e.deltaY > 0 ? -0.1 : 0.1;
            this.adjustZoom(delta);
        });
    }

    setView(mode) {
        this.viewMode = mode;

        // Update button states
        this.controlsDiv.querySelectorAll('.btn-group:first-child .btn').forEach(btn => {
            btn.classList.remove('active', 'btn-primary');
            btn.classList.add('btn-outline-primary');
        });

        const activeBtn = this.controlsDiv.querySelector(`.view-${mode}`);
        if (activeBtn) {
            activeBtn.classList.remove('btn-outline-primary');
            activeBtn.classList.add('btn-primary', 'active');
        }

        this.render();
    }

    adjustZoom(delta) {
        this.zoom = Math.max(0.5, Math.min(2, this.zoom + delta));
        const baseViewBox = '0 0 400 600';
        const [x, y, w, h] = baseViewBox.split(' ').map(Number);
        const newW = w / this.zoom;
        const newH = h / this.zoom;
        const newX = x + (w - newW) / 2;
        const newY = y + (h - newH) / 2;
        this.svg.setAttribute('viewBox', `${newX} ${newY} ${newW} ${newH}`);
    }

    resetView() {
        this.zoom = 1;
        this.svg.setAttribute('viewBox', '0 0 400 600');
        this.setView('front');
    }

    render() {
        // Clear SVG
        while (this.svg.firstChild) {
            this.svg.removeChild(this.svg.firstChild);
        }

        // Add defs for gradients and filters
        this.addDefs();

        // Draw body based on view
        if (this.viewMode === 'front') {
            this.drawFrontBody();
        } else {
            this.drawBackBody();
        }

        // Draw legend
        this.drawLegend();
    }

    addDefs() {
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');

        // Skin gradient
        const skinGradient = `
            <linearGradient id="skinGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#ffd4a3;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#ffcb9a;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#f4c097;stop-opacity:1" />
            </linearGradient>
        `;

        // Shadow filter
        const shadowFilter = `
            <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
                <feOffset dx="2" dy="2" result="offsetblur"/>
                <feComponentTransfer>
                    <feFuncA type="linear" slope="0.3"/>
                </feComponentTransfer>
                <feMerge>
                    <feMergeNode/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
        `;

        // Muscle shading
        const muscleGradient = `
            <radialGradient id="muscleGradient">
                <stop offset="0%" style="stop-color:#d89b7b;stop-opacity:0.8" />
                <stop offset="100%" style="stop-color:#cc8866;stop-opacity:0.6" />
            </radialGradient>
        `;

        defs.innerHTML = skinGradient + shadowFilter + muscleGradient;
        this.svg.appendChild(defs);
    }

    drawFrontBody() {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('id', 'frontBody');

        // Head
        const head = this.createEllipse(200, 60, 35, 45, 'url(#skinGradient)', '#8b7355');
        head.setAttribute('filter', 'url(#shadow)');
        g.appendChild(head);

        // Face features
        const leftEye = this.createEllipse(185, 55, 4, 6, '#2c3e50', 'none');
        const rightEye = this.createEllipse(215, 55, 4, 6, '#2c3e50', 'none');
        g.appendChild(leftEye);
        g.appendChild(rightEye);

        // Neck
        const neck = this.createRect(185, 105, 30, 35, 'url(#skinGradient)', '#8b7355');
        neck.setAttribute('filter', 'url(#shadow)');
        g.appendChild(neck);

        // Torso - realistic shape
        const torsoPath = `
            M 175 140
            Q 160 160, 155 200
            Q 152 250, 160 300
            Q 165 320, 175 340
            L 225 340
            Q 235 320, 240 300
            Q 248 250, 245 200
            Q 240 160, 225 140
            Z
        `;
        const torso = this.createPath(torsoPath, 'url(#skinGradient)', '#8b7355', 2);
        torso.setAttribute('filter', 'url(#shadow)');
        g.appendChild(torso);

        // Chest muscles (if showing muscles)
        if (this.options.showMuscles || !this.options.showAcupoints) {
            const chestLeft = this.createEllipse(180, 180, 25, 35, 'url(#muscleGradient)', 'none', 0.6);
            const chestRight = this.createEllipse(220, 180, 25, 35, 'url(#muscleGradient)', 'none', 0.6);
            g.appendChild(chestLeft);
            g.appendChild(chestRight);

            // Abs
            for (let i = 0; i < 3; i++) {
                const absLeft = this.createRect(180, 220 + i * 30, 15, 25, 'url(#muscleGradient)', 'none', 5);
                absLeft.style.opacity = '0.4';
                const absRight = this.createRect(205, 220 + i * 30, 15, 25, 'url(#muscleGradient)', 'none', 5);
                absRight.style.opacity = '0.4';
                g.appendChild(absLeft);
                g.appendChild(absRight);
            }
        }

        // Left arm
        const leftArm = this.createPath(`
            M 155 160
            Q 130 180, 120 220
            Q 115 260, 110 300
            L 125 305
            Q 130 265, 135 225
            Q 145 185, 170 165
            Z
        `, 'url(#skinGradient)', '#8b7355', 2);
        leftArm.setAttribute('filter', 'url(#shadow)');
        g.appendChild(leftArm);

        // Right arm
        const rightArm = this.createPath(`
            M 245 160
            Q 270 180, 280 220
            Q 285 260, 290 300
            L 275 305
            Q 270 265, 265 225
            Q 255 185, 230 165
            Z
        `, 'url(#skinGradient)', '#8b7355', 2);
        rightArm.setAttribute('filter', 'url(#shadow)');
        g.appendChild(rightArm);

        // Left leg
        const leftLeg = this.createPath(`
            M 175 340
            Q 173 380, 170 420
            Q 168 460, 165 500
            Q 163 540, 160 580
            L 180 580
            Q 183 540, 185 500
            Q 187 460, 190 420
            Q 192 380, 195 340
            Z
        `, 'url(#skinGradient)', '#8b7355', 2);
        leftLeg.setAttribute('filter', 'url(#shadow)');
        g.appendChild(leftLeg);

        // Right leg
        const rightLeg = this.createPath(`
            M 225 340
            Q 223 380, 220 420
            Q 218 460, 215 500
            Q 213 540, 210 580
            L 230 580
            Q 233 540, 235 500
            Q 237 460, 240 420
            Q 242 380, 245 340
            Z
        `, 'url(#skinGradient)', '#8b7355', 2);
        rightLeg.setAttribute('filter', 'url(#shadow)');
        g.appendChild(rightLeg);

        this.svg.appendChild(g);

        // Add acupoints or treatment areas
        if (this.options.showAcupoints) {
            this.drawFrontAcupoints();
        }
        if (this.options.showMuscles) {
            this.drawFrontTreatmentAreas();
        }
    }

    drawBackBody() {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('id', 'backBody');

        // Head (back)
        const head = this.createEllipse(200, 60, 35, 45, 'url(#skinGradient)', '#8b7355');
        head.setAttribute('filter', 'url(#shadow)');
        g.appendChild(head);

        // Hair
        const hair = this.createEllipse(200, 45, 38, 30, '#2c3e50', 'none');
        g.appendChild(hair);

        // Neck
        const neck = this.createRect(185, 105, 30, 35, 'url(#skinGradient)', '#8b7355');
        neck.setAttribute('filter', 'url(#shadow)');
        g.appendChild(neck);

        // Back torso
        const torsoPath = `
            M 175 140
            Q 160 160, 155 200
            Q 152 250, 160 300
            Q 165 320, 175 340
            L 225 340
            Q 235 320, 240 300
            Q 248 250, 245 200
            Q 240 160, 225 140
            Z
        `;
        const torso = this.createPath(torsoPath, 'url(#skinGradient)', '#8b7355', 2);
        torso.setAttribute('filter', 'url(#shadow)');
        g.appendChild(torso);

        // Spine line
        const spine = this.createLine(200, 140, 200, 340, '#8b7355', 2, 0.5);
        g.appendChild(spine);

        // Back muscles
        if (this.options.showMuscles || !this.options.showAcupoints) {
            // Trapezius
            const trapLeft = this.createPath(`
                M 180 145
                Q 165 155, 160 175
                Q 175 185, 190 180
                Z
            `, 'url(#muscleGradient)', 'none');
            trapLeft.style.opacity = '0.5';
            g.appendChild(trapLeft);

            const trapRight = this.createPath(`
                M 220 145
                Q 235 155, 240 175
                Q 225 185, 210 180
                Z
            `, 'url(#muscleGradient)', 'none');
            trapRight.style.opacity = '0.5';
            g.appendChild(trapRight);

            // Latissimus dorsi
            const latLeft = this.createPath(`
                M 165 200
                Q 158 230, 160 260
                Q 170 250, 180 240
                Q 185 220, 180 200
                Z
            `, 'url(#muscleGradient)', 'none');
            latLeft.style.opacity = '0.5';
            g.appendChild(latLeft);

            const latRight = this.createPath(`
                M 235 200
                Q 242 230, 240 260
                Q 230 250, 220 240
                Q 215 220, 220 200
                Z
            `, 'url(#muscleGradient)', 'none');
            latRight.style.opacity = '0.5';
            g.appendChild(latRight);

            // Lower back
            const lowerBack = this.createEllipse(200, 290, 35, 40, 'url(#muscleGradient)', 'none');
            lowerBack.style.opacity = '0.4';
            g.appendChild(lowerBack);
        }

        // Arms (back view)
        const leftArm = this.createPath(`
            M 155 160
            Q 130 180, 120 220
            Q 115 260, 110 300
            L 125 305
            Q 130 265, 135 225
            Q 145 185, 170 165
            Z
        `, 'url(#skinGradient)', '#8b7355', 2);
        leftArm.setAttribute('filter', 'url(#shadow)');
        g.appendChild(leftArm);

        const rightArm = this.createPath(`
            M 245 160
            Q 270 180, 280 220
            Q 285 260, 290 300
            L 275 305
            Q 270 265, 265 225
            Q 255 185, 230 165
            Z
        `, 'url(#skinGradient)', '#8b7355', 2);
        rightArm.setAttribute('filter', 'url(#shadow)');
        g.appendChild(rightArm);

        // Legs (same as front)
        const leftLeg = this.createPath(`
            M 175 340
            Q 173 380, 170 420
            Q 168 460, 165 500
            Q 163 540, 160 580
            L 180 580
            Q 183 540, 185 500
            Q 187 460, 190 420
            Q 192 380, 195 340
            Z
        `, 'url(#skinGradient)', '#8b7355', 2);
        leftLeg.setAttribute('filter', 'url(#shadow)');
        g.appendChild(leftLeg);

        const rightLeg = this.createPath(`
            M 225 340
            Q 223 380, 220 420
            Q 218 460, 215 500
            Q 213 540, 210 580
            L 230 580
            Q 233 540, 235 500
            Q 237 460, 240 420
            Q 242 380, 245 340
            Z
        `, 'url(#skinGradient)', '#8b7355', 2);
        rightLeg.setAttribute('filter', 'url(#shadow)');
        g.appendChild(rightLeg);

        this.svg.appendChild(g);

        // Add acupoints or treatment areas
        if (this.options.showAcupoints) {
            this.drawBackAcupoints();
        }
        if (this.options.showMuscles) {
            this.drawBackTreatmentAreas();
        }
    }

    drawFrontAcupoints() {
        const acupoints = [
            { x: 200, y: 40, code: 'GV20', name: '百会', desc: 'Baihui' },
            { x: 110, y: 280, code: 'LI4', name: '合谷', desc: 'Hegu' },
            { x: 290, y: 280, code: 'LI4', name: '合谷', desc: 'Hegu' },
            { x: 200, y: 175, code: 'CV17', name: '膻中', desc: 'Danzhong' },
            { x: 200, y: 270, code: 'CV4', name: '关元', desc: 'Guanyuan' },
            { x: 115, y: 290, code: 'PC6', name: '内关', desc: 'Neiguan' },
            { x: 285, y: 290, code: 'PC6', name: '内关', desc: 'Neiguan' },
            { x: 120, y: 295, code: 'HT7', name: '神门', desc: 'Shenmen' },
            { x: 280, y: 295, code: 'HT7', name: '神门', desc: 'Shenmen' },
            { x: 170, y: 450, code: 'ST36', name: '足三里', desc: 'Zusanli' },
            { x: 230, y: 450, code: 'ST36', name: '足三里', desc: 'Zusanli' },
            { x: 170, y: 550, code: 'LR3', name: '太冲', desc: 'Taichong' },
            { x: 230, y: 550, code: 'LR3', name: '太冲', desc: 'Taichong' },
        ];

        acupoints.forEach(point => {
            const isSelected = this.options.selectedPoints.includes(point.code);
            const g = this.createAcupointMarker(point.x, point.y, point.code, point.name, point.desc, isSelected);
            this.svg.appendChild(g);
        });
    }

    drawBackAcupoints() {
        const acupoints = [
            { x: 185, y: 70, code: 'GB20', name: '风池', desc: 'Fengchi' },
            { x: 215, y: 70, code: 'GB20', name: '风池', desc: 'Fengchi' },
            { x: 185, y: 250, code: 'BL23', name: '肾俞', desc: 'Shenshu' },
            { x: 215, y: 250, code: 'BL23', name: '肾俞', desc: 'Shenshu' },
            { x: 170, y: 490, code: 'SP6', name: '三阴交', desc: 'Sanyinjiao' },
            { x: 230, y: 490, code: 'SP6', name: '三阴交', desc: 'Sanyinjiao' },
            { x: 170, y: 180, code: 'BL13', name: '肺俞', desc: 'Feishu' },
            { x: 230, y: 180, code: 'BL13', name: '肺俞', desc: 'Feishu' },
        ];

        acupoints.forEach(point => {
            const isSelected = this.options.selectedPoints.includes(point.code);
            const g = this.createAcupointMarker(point.x, point.y, point.code, point.name, point.desc, isSelected);
            this.svg.appendChild(g);
        });
    }

    drawFrontTreatmentAreas() {
        const areas = [
            { x: 200, y: 120, w: 50, h: 35, code: 'neck', name: '颈部 Neck', color: '#2ecc71' },
            { x: 140, y: 170, w: 45, h: 50, code: 'shoulder', name: '肩部 Shoulder', color: '#3498db' },
            { x: 260, y: 170, w: 45, h: 50, code: 'shoulder', name: '肩部 Shoulder', color: '#3498db' },
            { x: 125, y: 240, w: 30, h: 60, code: 'arm', name: '上肢 Arm', color: '#9b59b6' },
            { x: 275, y: 240, w: 30, h: 60, code: 'arm', name: '上肢 Arm', color: '#9b59b6' },
            { x: 175, y: 400, w: 25, h: 100, code: 'leg', name: '下肢 Leg', color: '#e67e22' },
            { x: 225, y: 400, w: 25, h: 100, code: 'leg', name: '下肢 Leg', color: '#e67e22' },
        ];

        areas.forEach(area => {
            const isSelected = this.options.selectedAreas.includes(area.code);
            const g = this.createTreatmentArea(area.x, area.y, area.w, area.h, area.code, area.name, area.color, isSelected);
            this.svg.appendChild(g);
        });
    }

    drawBackTreatmentAreas() {
        const areas = [
            { x: 200, y: 120, w: 50, h: 35, code: 'neck', name: '颈部 Neck', color: '#2ecc71' },
            { x: 140, y: 170, w: 45, h: 50, code: 'shoulder', name: '肩部 Shoulder', color: '#3498db' },
            { x: 260, y: 170, w: 45, h: 50, code: 'shoulder', name: '肩部 Shoulder', color: '#3498db' },
            { x: 200, y: 210, w: 60, h: 55, code: 'upper_back', name: '上背部 Upper Back', color: '#1abc9c' },
            { x: 200, y: 280, w: 55, h: 50, code: 'lower_back', name: '腰部 Lower Back', color: '#f39c12' },
            { x: 200, y: 330, w: 60, h: 30, code: 'hip', name: '臀部 Hip', color: '#e74c3c' },
            { x: 175, y: 400, w: 25, h: 100, code: 'leg', name: '下肢 Leg', color: '#e67e22' },
            { x: 225, y: 400, w: 25, h: 100, code: 'leg', name: '下肢 Leg', color: '#e67e22' },
        ];

        areas.forEach(area => {
            const isSelected = this.options.selectedAreas.includes(area.code);
            const g = this.createTreatmentArea(area.x, area.y, area.w, area.h, area.code, area.name, area.color, isSelected);
            this.svg.appendChild(g);
        });
    }

    createAcupointMarker(x, y, code, name, desc, isSelected) {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('class', 'acupoint-group');
        g.style.cursor = 'pointer';

        // Outer glow
        const glow = this.createCircle(x, y, 10, isSelected ? '#c0392b' : '#e74c3c', 'none', 0.3);
        g.appendChild(glow);

        // Main marker
        const marker = this.createCircle(x, y, 6, isSelected ? '#c0392b' : '#e74c3c', '#fff', 1, 2);
        marker.setAttribute('class', 'acupoint');
        marker.setAttribute('data-code', code);
        marker.setAttribute('data-name', name);
        g.appendChild(marker);

        // Label background
        const labelBg = this.createRect(x - 25, y - 30, 50, 20, 'rgba(255,255,255,0.95)', '#2c3e50', 3);
        labelBg.style.display = 'none';
        labelBg.setAttribute('class', 'acupoint-label-bg');
        g.appendChild(labelBg);

        // Label text
        const label = this.createText(x, y - 20, `${name}`, '#2c3e50', '11px', 'bold');
        label.style.display = 'none';
        label.setAttribute('class', 'acupoint-label');
        g.appendChild(label);

        const labelCode = this.createText(x, y - 8, code, '#7f8c8d', '9px');
        labelCode.style.display = 'none';
        labelCode.setAttribute('class', 'acupoint-label');
        g.appendChild(labelCode);

        // Hover effects
        g.addEventListener('mouseenter', () => {
            labelBg.style.display = 'block';
            label.style.display = 'block';
            labelCode.style.display = 'block';
            marker.setAttribute('r', '8');
        });

        g.addEventListener('mouseleave', () => {
            labelBg.style.display = 'none';
            label.style.display = 'none';
            labelCode.style.display = 'none';
            marker.setAttribute('r', '6');
        });

        return g;
    }

    createTreatmentArea(x, y, w, h, code, name, color, isSelected) {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('class', 'treatment-area-group');
        g.style.cursor = 'pointer';

        // Area rectangle
        const area = this.createRect(
            x - w/2, y - h/2, w, h,
            isSelected ? `${color}88` : `${color}33`,
            isSelected ? color : `${color}66`,
            8, 2
        );
        area.setAttribute('class', 'treatment-area');
        area.setAttribute('data-code', code);
        area.setAttribute('data-name', name);
        g.appendChild(area);

        // Label
        const label = this.createText(x, y + 5, name, '#2c3e50', '11px', 'bold');
        label.style.display = 'none';
        label.setAttribute('class', 'area-label');
        g.appendChild(label);

        // Hover effects
        g.addEventListener('mouseenter', () => {
            label.style.display = 'block';
            area.style.opacity = '0.8';
        });

        g.addEventListener('mouseleave', () => {
            label.style.display = 'none';
            area.style.opacity = isSelected ? '0.6' : '0.4';
        });

        return g;
    }

    drawLegend() {
        const legend = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        legend.setAttribute('id', 'legend');

        // Legend background
        const bg = this.createRect(10, 520, 180, 70, 'rgba(255,255,255,0.95)', '#ddd', 5, 1);
        legend.appendChild(bg);

        // Title
        const title = this.createText(100, 540, '图例 | Legend', '#2c3e50', '12px', 'bold');
        legend.appendChild(title);

        if (this.options.showAcupoints) {
            const dot = this.createCircle(25, 560, 5, '#e74c3c', '#fff', 1, 1);
            legend.appendChild(dot);
            const text = this.createText(45, 563, '穴位 | Acupoint', '#2c3e50', '10px');
            legend.appendChild(text);
        }

        if (this.options.showMuscles) {
            const rect = this.createRect(20, 555, 10, 10, '#2ecc7166', '#2ecc71', 2, 1);
            legend.appendChild(rect);
            const text = this.createText(45, 563, '治疗区域 | Treatment Area', '#2c3e50', '10px');
            legend.appendChild(text);
        }

        // Instructions
        const instr1 = this.createText(100, 578, '点击选择 | Click to select', '#7f8c8d', '9px');
        legend.appendChild(instr1);

        this.svg.appendChild(legend);
    }

    // Helper methods to create SVG elements
    createCircle(cx, cy, r, fill, stroke, opacity = 1, strokeWidth = 0) {
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', cx);
        circle.setAttribute('cy', cy);
        circle.setAttribute('r', r);
        circle.setAttribute('fill', fill);
        if (stroke !== 'none') circle.setAttribute('stroke', stroke);
        if (strokeWidth > 0) circle.setAttribute('stroke-width', strokeWidth);
        circle.style.opacity = opacity;
        return circle;
    }

    createEllipse(cx, cy, rx, ry, fill, stroke, opacity = 1) {
        const ellipse = document.createElementNS('http://www.w3.org/2000/svg', 'ellipse');
        ellipse.setAttribute('cx', cx);
        ellipse.setAttribute('cy', cy);
        ellipse.setAttribute('rx', rx);
        ellipse.setAttribute('ry', ry);
        ellipse.setAttribute('fill', fill);
        if (stroke !== 'none') ellipse.setAttribute('stroke', stroke);
        ellipse.setAttribute('stroke-width', '2');
        if (opacity < 1) ellipse.style.opacity = opacity;
        return ellipse;
    }

    createRect(x, y, width, height, fill, stroke, rx = 0, strokeWidth = 1) {
        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('x', x);
        rect.setAttribute('y', y);
        rect.setAttribute('width', width);
        rect.setAttribute('height', height);
        rect.setAttribute('fill', fill);
        if (stroke) rect.setAttribute('stroke', stroke);
        if (strokeWidth > 0) rect.setAttribute('stroke-width', strokeWidth);
        if (rx > 0) rect.setAttribute('rx', rx);
        return rect;
    }

    createPath(d, fill, stroke, strokeWidth = 1) {
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', d);
        path.setAttribute('fill', fill);
        if (stroke !== 'none') path.setAttribute('stroke', stroke);
        path.setAttribute('stroke-width', strokeWidth);
        return path;
    }

    createLine(x1, y1, x2, y2, stroke, strokeWidth, opacity = 1) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x1);
        line.setAttribute('y1', y1);
        line.setAttribute('x2', x2);
        line.setAttribute('y2', y2);
        line.setAttribute('stroke', stroke);
        line.setAttribute('stroke-width', strokeWidth);
        line.style.opacity = opacity;
        return line;
    }

    createText(x, y, content, fill, fontSize, fontWeight = 'normal') {
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', x);
        text.setAttribute('y', y);
        text.setAttribute('fill', fill);
        text.setAttribute('font-size', fontSize);
        text.setAttribute('font-weight', fontWeight);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('font-family', 'Arial, sans-serif');
        text.textContent = content;
        return text;
    }

    // Interaction methods
    toggleAcupoint(code, name) {
        const index = this.options.selectedPoints.indexOf(code);
        if (index > -1) {
            this.options.selectedPoints.splice(index, 1);
        } else {
            this.options.selectedPoints.push(code);
        }
        this.render();

        // Trigger custom event
        const event = new CustomEvent('acupointSelected', {
            detail: { code, name, selected: index === -1 }
        });
        this.container.dispatchEvent(event);
    }

    toggleArea(code, name) {
        const index = this.options.selectedAreas.indexOf(code);
        if (index > -1) {
            this.options.selectedAreas.splice(index, 1);
        } else {
            this.options.selectedAreas.push(code);
        }
        this.render();

        // Trigger custom event
        const event = new CustomEvent('areaSelected', {
            detail: { code, name, selected: index === -1 }
        });
        this.container.dispatchEvent(event);
    }

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

    findAcupointAt(x, y) {
        // This is handled by click events on SVG elements
        return null;
    }

    findAreaAt(x, y) {
        // This is handled by click events on SVG elements
        return null;
    }

    draw() {
        this.render();
    }
}

// Export for use in templates
window.Body3DViewer = Body3DViewerRealistic;
console.log('真实人体3D图解已加载 | Realistic 3D Body Viewer loaded');
