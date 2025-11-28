/**
 * 3D Human Body Viewer for Acupuncture and Tuina
 * 3D人体图解 - 针灸和推拿
 */

class Body3DViewer {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error('Container not found:', containerId);
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
        // Create canvas
        this.canvas = document.createElement('canvas');
        this.canvas.width = this.container.offsetWidth || 800;
        this.canvas.height = this.container.offsetHeight || 600;
        this.container.appendChild(this.canvas);

        this.ctx = this.canvas.getContext('2d');

        // Add controls
        this.addControls();

        // Initialize state
        this.rotation = { x: 0, y: 0 };
        this.zoom = 1;
        this.viewMode = 'front'; // front, back, side

        // Bind events
        this.bindEvents();

        // Start rendering
        this.render();
    }

    addControls() {
        const controlsDiv = document.createElement('div');
        controlsDiv.className = 'body-3d-controls mb-3';
        controlsDiv.innerHTML = `
            <div class="btn-group btn-group-sm" role="group">
                <button type="button" class="btn btn-outline-primary view-front">正面 | Front</button>
                <button type="button" class="btn btn-outline-primary view-back">背面 | Back</button>
                <button type="button" class="btn btn-outline-primary view-side">侧面 | Side</button>
            </div>
            <div class="btn-group btn-group-sm ms-2" role="group">
                <button type="button" class="btn btn-outline-secondary zoom-in"><i class="bi bi-zoom-in"></i></button>
                <button type="button" class="btn btn-outline-secondary zoom-out"><i class="bi bi-zoom-out"></i></button>
                <button type="button" class="btn btn-outline-secondary reset-view"><i class="bi bi-arrow-clockwise"></i></button>
            </div>
        `;
        this.container.parentElement.insertBefore(controlsDiv, this.container);

        // Bind control events
        controlsDiv.querySelector('.view-front').addEventListener('click', () => this.setView('front'));
        controlsDiv.querySelector('.view-back').addEventListener('click', () => this.setView('back'));
        controlsDiv.querySelector('.view-side').addEventListener('click', () => this.setView('side'));
        controlsDiv.querySelector('.zoom-in').addEventListener('click', () => this.adjustZoom(0.1));
        controlsDiv.querySelector('.zoom-out').addEventListener('click', () => this.adjustZoom(-0.1));
        controlsDiv.querySelector('.reset-view').addEventListener('click', () => this.resetView());
    }

    bindEvents() {
        let isDragging = false;
        let lastX, lastY;

        this.canvas.addEventListener('mousedown', (e) => {
            isDragging = true;
            lastX = e.clientX;
            lastY = e.clientY;
        });

        this.canvas.addEventListener('mousemove', (e) => {
            if (isDragging) {
                const dx = e.clientX - lastX;
                const dy = e.clientY - lastY;
                this.rotation.y += dx * 0.01;
                this.rotation.x += dy * 0.01;
                lastX = e.clientX;
                lastY = e.clientY;
                this.render();
            }
        });

        this.canvas.addEventListener('mouseup', () => {
            isDragging = false;
        });

        this.canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            this.adjustZoom(e.deltaY > 0 ? -0.05 : 0.05);
        });

        // Touch events for mobile
        this.canvas.addEventListener('touchstart', (e) => {
            if (e.touches.length === 1) {
                isDragging = true;
                lastX = e.touches[0].clientX;
                lastY = e.touches[0].clientY;
            }
        });

        this.canvas.addEventListener('touchmove', (e) => {
            if (isDragging && e.touches.length === 1) {
                const dx = e.touches[0].clientX - lastX;
                const dy = e.touches[0].clientY - lastY;
                this.rotation.y += dx * 0.01;
                this.rotation.x += dy * 0.01;
                lastX = e.touches[0].clientX;
                lastY = e.touches[0].clientY;
                this.render();
            }
        });

        this.canvas.addEventListener('touchend', () => {
            isDragging = false;
        });

        // Click to select points/areas
        this.canvas.addEventListener('click', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            this.handleClick(x, y);
        });
    }

    setView(mode) {
        this.viewMode = mode;
        if (mode === 'front') {
            this.rotation = { x: 0, y: 0 };
        } else if (mode === 'back') {
            this.rotation = { x: 0, y: Math.PI };
        } else if (mode === 'side') {
            this.rotation = { x: 0, y: Math.PI / 2 };
        }
        this.render();
    }

    adjustZoom(delta) {
        this.zoom = Math.max(0.5, Math.min(2, this.zoom + delta));
        this.render();
    }

    resetView() {
        this.rotation = { x: 0, y: 0 };
        this.zoom = 1;
        this.viewMode = 'front';
        this.render();
    }

    render() {
        const ctx = this.ctx;
        const width = this.canvas.width;
        const height = this.canvas.height;

        // Clear canvas
        ctx.clearRect(0, 0, width, height);

        // Draw background
        ctx.fillStyle = '#f8f9fa';
        ctx.fillRect(0, 0, width, height);

        // Calculate center and scale
        const centerX = width / 2;
        const centerY = height / 2;
        const scale = Math.min(width, height) * 0.35 * this.zoom;

        // Save context
        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.scale(scale, scale);

        // Draw body based on view mode
        if (this.viewMode === 'front') {
            this.drawFrontView(ctx);
        } else if (this.viewMode === 'back') {
            this.drawBackView(ctx);
        } else {
            this.drawSideView(ctx);
        }

        // Restore context
        ctx.restore();

        // Draw legend
        this.drawLegend(ctx);
    }

    drawFrontView(ctx) {
        // Draw simplified front body outline
        ctx.strokeStyle = '#2c3e50';
        ctx.lineWidth = 0.02;
        ctx.fillStyle = '#ffeaa7';

        ctx.beginPath();
        // Head
        ctx.arc(0, -1.3, 0.2, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        // Neck
        ctx.fillRect(-0.08, -1.1, 0.16, 0.15);
        ctx.strokeRect(-0.08, -1.1, 0.16, 0.15);

        // Torso
        ctx.beginPath();
        ctx.moveTo(-0.3, -0.95);
        ctx.lineTo(-0.35, -0.2);
        ctx.lineTo(-0.25, 0.3);
        ctx.lineTo(-0.15, 0.8);
        ctx.lineTo(0.15, 0.8);
        ctx.lineTo(0.25, 0.3);
        ctx.lineTo(0.35, -0.2);
        ctx.lineTo(0.3, -0.95);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        // Arms
        ctx.fillRect(-0.35, -0.8, -0.15, 0.8);
        ctx.strokeRect(-0.35, -0.8, -0.15, 0.8);
        ctx.fillRect(0.35, -0.8, 0.15, 0.8);
        ctx.strokeRect(0.35, -0.8, 0.15, 0.8);

        // Forearms
        ctx.fillRect(-0.55, 0, -0.1, 0.6);
        ctx.strokeRect(-0.55, 0, -0.1, 0.6);
        ctx.fillRect(0.55, 0, 0.1, 0.6);
        ctx.strokeRect(0.55, 0, 0.1, 0.6);

        // Legs
        ctx.fillRect(-0.15, 0.8, -0.18, 1.0);
        ctx.strokeRect(-0.15, 0.8, -0.18, 1.0);
        ctx.fillRect(0.15, 0.8, 0.18, 1.0);
        ctx.strokeRect(0.15, 0.8, 0.18, 1.0);

        // Draw acupoints if enabled
        if (this.options.showAcupoints) {
            this.drawFrontAcupoints(ctx);
        }

        // Draw selected areas if enabled
        if (this.options.showMuscles) {
            this.drawFrontMuscles(ctx);
        }
    }

    drawBackView(ctx) {
        // Draw simplified back body outline
        ctx.strokeStyle = '#2c3e50';
        ctx.lineWidth = 0.02;
        ctx.fillStyle = '#ffeaa7';

        ctx.beginPath();
        // Head (back)
        ctx.arc(0, -1.3, 0.2, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        // Neck
        ctx.fillRect(-0.08, -1.1, 0.16, 0.15);
        ctx.strokeRect(-0.08, -1.1, 0.16, 0.15);

        // Back torso
        ctx.beginPath();
        ctx.moveTo(-0.3, -0.95);
        ctx.lineTo(-0.35, -0.2);
        ctx.lineTo(-0.25, 0.3);
        ctx.lineTo(-0.15, 0.8);
        ctx.lineTo(0.15, 0.8);
        ctx.lineTo(0.25, 0.3);
        ctx.lineTo(0.35, -0.2);
        ctx.lineTo(0.3, -0.95);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        // Draw spine line
        ctx.strokeStyle = '#e74c3c';
        ctx.lineWidth = 0.015;
        ctx.beginPath();
        ctx.moveTo(0, -1.1);
        ctx.lineTo(0, 0.8);
        ctx.stroke();

        // Arms
        ctx.strokeStyle = '#2c3e50';
        ctx.lineWidth = 0.02;
        ctx.fillRect(-0.35, -0.8, -0.15, 0.8);
        ctx.strokeRect(-0.35, -0.8, -0.15, 0.8);
        ctx.fillRect(0.35, -0.8, 0.15, 0.8);
        ctx.strokeRect(0.35, -0.8, 0.15, 0.8);

        // Forearms
        ctx.fillRect(-0.55, 0, -0.1, 0.6);
        ctx.strokeRect(-0.55, 0, -0.1, 0.6);
        ctx.fillRect(0.55, 0, 0.1, 0.6);
        ctx.strokeRect(0.55, 0, 0.1, 0.6);

        // Legs
        ctx.fillRect(-0.15, 0.8, -0.18, 1.0);
        ctx.strokeRect(-0.15, 0.8, -0.18, 1.0);
        ctx.fillRect(0.15, 0.8, 0.18, 1.0);
        ctx.strokeRect(0.15, 0.8, 0.18, 1.0);

        // Draw acupoints if enabled
        if (this.options.showAcupoints) {
            this.drawBackAcupoints(ctx);
        }

        // Draw muscles if enabled
        if (this.options.showMuscles) {
            this.drawBackMuscles(ctx);
        }
    }

    drawSideView(ctx) {
        // Simplified side view
        ctx.strokeStyle = '#2c3e50';
        ctx.lineWidth = 0.02;
        ctx.fillStyle = '#ffeaa7';

        // Head
        ctx.beginPath();
        ctx.arc(0, -1.3, 0.2, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        // Side torso
        ctx.fillRect(-0.15, -1.1, 0.3, 1.9);
        ctx.strokeRect(-0.15, -1.1, 0.3, 1.9);

        // Arm
        ctx.fillRect(0.15, -0.8, 0.1, 1.4);
        ctx.strokeRect(0.15, -0.8, 0.1, 1.4);

        // Leg
        ctx.fillRect(-0.1, 0.8, 0.2, 1.0);
        ctx.strokeRect(-0.1, 0.8, 0.2, 1.0);
    }

    drawFrontAcupoints(ctx) {
        const acupoints = [
            { x: 0, y: -0.5, code: 'CV17', name: '膻中' },
            { x: 0, y: 0, code: 'CV12', name: '中脘' },
            { x: 0, y: 0.3, code: 'CV8', name: '神阙' },
            { x: 0, y: 0.5, code: 'CV4', name: '关元' },
            { x: -0.45, y: -0.1, code: 'LI4', name: '合谷' },
            { x: 0.45, y: -0.1, code: 'LI4', name: '合谷' },
            { x: -0.2, y: 1.4, code: 'ST36', name: '足三里' },
            { x: 0.2, y: 1.4, code: 'ST36', name: '足三里' },
        ];

        acupoints.forEach(point => {
            const isSelected = this.options.selectedPoints.includes(point.code);

            ctx.fillStyle = isSelected ? '#e74c3c' : '#3498db';
            ctx.beginPath();
            ctx.arc(point.x, point.y, 0.04, 0, Math.PI * 2);
            ctx.fill();

            if (isSelected) {
                ctx.strokeStyle = '#c0392b';
                ctx.lineWidth = 0.01;
                ctx.stroke();
            }

            // Label
            ctx.fillStyle = '#2c3e50';
            ctx.font = '0.08px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(point.name, point.x, point.y - 0.08);
        });
    }

    drawBackAcupoints(ctx) {
        const acupoints = [
            { x: 0, y: -0.95, code: 'GV14', name: '大椎' },
            { x: 0, y: -0.4, code: 'GV4', name: '命门' },
            { x: -0.12, y: -0.6, code: 'BL13', name: '肺俞' },
            { x: 0.12, y: -0.6, code: 'BL13', name: '肺俞' },
            { x: -0.12, y: -0.3, code: 'BL23', name: '肾俞' },
            { x: 0.12, y: -0.3, code: 'BL23', name: '肾俞' },
            { x: -0.15, y: -1.2, code: 'GB20', name: '风池' },
            { x: 0.15, y: -1.2, code: 'GB20', name: '风池' },
        ];

        acupoints.forEach(point => {
            const isSelected = this.options.selectedPoints.includes(point.code);

            ctx.fillStyle = isSelected ? '#e74c3c' : '#3498db';
            ctx.beginPath();
            ctx.arc(point.x, point.y, 0.04, 0, Math.PI * 2);
            ctx.fill();

            if (isSelected) {
                ctx.strokeStyle = '#c0392b';
                ctx.lineWidth = 0.01;
                ctx.stroke();
            }

            // Label
            ctx.fillStyle = '#2c3e50';
            ctx.font = '0.08px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(point.name, point.x, point.y - 0.08);
        });
    }

    drawFrontMuscles(ctx) {
        const areas = [
            { x: 0, y: -1.15, w: 0.16, h: 0.2, name: '颈部 | Neck', id: 'neck' },
            { x: -0.23, y: -0.7, w: 0.2, h: 0.3, name: '左肩 | L.Shoulder', id: 'left_shoulder' },
            { x: 0.23, y: -0.7, w: 0.2, h: 0.3, name: '右肩 | R.Shoulder', id: 'right_shoulder' },
            { x: 0, y: -0.3, w: 0.4, h: 0.5, name: '腹部 | Abdomen', id: 'abdomen' },
        ];

        areas.forEach(area => {
            const isSelected = this.options.selectedAreas.includes(area.id);

            ctx.fillStyle = isSelected ? 'rgba(231, 76, 60, 0.3)' : 'rgba(52, 152, 219, 0.2)';
            ctx.fillRect(area.x - area.w/2, area.y, area.w, area.h);

            if (isSelected) {
                ctx.strokeStyle = '#e74c3c';
                ctx.lineWidth = 0.02;
                ctx.strokeRect(area.x - area.w/2, area.y, area.w, area.h);
            }
        });
    }

    drawBackMuscles(ctx) {
        const areas = [
            { x: 0, y: -1.15, w: 0.16, h: 0.2, name: '颈部 | Neck', id: 'neck' },
            { x: -0.23, y: -0.7, w: 0.2, h: 0.3, name: '左肩 | L.Shoulder', id: 'left_shoulder' },
            { x: 0.23, y: -0.7, w: 0.2, h: 0.3, name: '右肩 | R.Shoulder', id: 'right_shoulder' },
            { x: 0, y: -0.5, w: 0.3, h: 0.6, name: '腰部 | Lower Back', id: 'lower_back' },
            { x: 0, y: 0.2, w: 0.25, h: 0.4, name: '臀部 | Buttocks', id: 'buttocks' },
        ];

        areas.forEach(area => {
            const isSelected = this.options.selectedAreas.includes(area.id);

            ctx.fillStyle = isSelected ? 'rgba(231, 76, 60, 0.3)' : 'rgba(52, 152, 219, 0.2)';
            ctx.fillRect(area.x - area.w/2, area.y, area.w, area.h);

            if (isSelected) {
                ctx.strokeStyle = '#e74c3c';
                ctx.lineWidth = 0.02;
                ctx.strokeRect(area.x - area.w/2, area.y, area.w, area.h);
            }
        });
    }

    drawLegend(ctx) {
        const padding = 10;
        const legendX = 10;
        const legendY = this.canvas.height - 80;

        ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
        ctx.fillRect(legendX, legendY, 200, 70);
        ctx.strokeStyle = '#ccc';
        ctx.strokeRect(legendX, legendY, 200, 70);

        ctx.fillStyle = '#2c3e50';
        ctx.font = '12px Arial';
        ctx.textAlign = 'left';

        let y = legendY + 20;

        if (this.options.showAcupoints) {
            ctx.fillStyle = '#3498db';
            ctx.beginPath();
            ctx.arc(legendX + 15, y, 5, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#2c3e50';
            ctx.fillText('穴位 | Acupoint', legendX + 30, y + 5);
            y += 20;
        }

        if (this.options.showMuscles) {
            ctx.fillStyle = 'rgba(52, 152, 219, 0.3)';
            ctx.fillRect(legendX + 10, y - 8, 15, 15);
            ctx.strokeStyle = '#3498db';
            ctx.strokeRect(legendX + 10, y - 8, 15, 15);
            ctx.fillStyle = '#2c3e50';
            ctx.fillText('治疗区域 | Treatment Area', legendX + 30, y + 5);
        }

        // Instructions
        ctx.font = '10px Arial';
        ctx.fillStyle = '#7f8c8d';
        const instrY = 20;
        ctx.textAlign = 'right';
        ctx.fillText('拖动旋转 | Drag to rotate', this.canvas.width - 10, instrY);
        ctx.fillText('滚轮缩放 | Scroll to zoom', this.canvas.width - 10, instrY + 15);
    }

    getAllAcupoints() {
        // Return all available acupoints with their data
        return [
            { code: 'LI4', name: '合谷', x: -0.45, y: -0.1, view: 'front' },
            { code: 'LI4', name: '合谷', x: -0.45, y: -0.1, view: 'back' },
            { code: 'ST36', name: '足三里', x: -0.15, y: 0.4, view: 'front' },
            { code: 'ST36', name: '足三里', x: -0.15, y: 0.4, view: 'back' },
            { code: 'LR3', name: '太冲', x: -0.12, y: 0.75, view: 'front' },
            { code: 'PC6', name: '内关', x: -0.35, y: 0.05, view: 'front' },
            { code: 'SP6', name: '三阴交', x: -0.15, y: 0.55, view: 'back' },
            { code: 'GB20', name: '风池', x: -0.12, y: -0.65, view: 'back' },
            { code: 'GV20', name: '百会', x: 0, y: -0.7, view: 'front' },
            { code: 'HT7', name: '神门', x: -0.35, y: 0.1, view: 'front' },
            { code: 'BL23', name: '肾俞', x: -0.08, y: -0.05, view: 'back' },
            { code: 'CV4', name: '关元', x: 0, y: 0.15, view: 'front' }
        ];
    }

    findAcupointAt(canvasX, canvasY) {
        // Find if click is near an acupoint
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const scale = 200 * this.zoom;

        // Get acupoints for current view
        const acupoints = this.getAllAcupoints().filter(p => p.view === this.viewMode);

        for (const point of acupoints) {
            const screenX = centerX + point.x * scale;
            const screenY = centerY + point.y * scale;

            const distance = Math.sqrt(
                Math.pow(canvasX - screenX, 2) +
                Math.pow(canvasY - screenY, 2)
            );

            // Click within 20 pixels of acupoint
            if (distance < 20) {
                return point;
            }
        }

        return null;
    }

    findAreaAt(canvasX, canvasY) {
        // Find if click is within a treatment area
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const scale = 200 * this.zoom;

        // Define treatment areas with bounding boxes
        const areas = [
            { code: 'neck', name: '颈部', x: 0, y: -0.55, width: 0.2, height: 0.15, view: 'front' },
            { code: 'neck', name: '颈部', x: 0, y: -0.55, width: 0.2, height: 0.15, view: 'back' },
            { code: 'shoulder', name: '肩部', x: -0.35, y: -0.35, width: 0.3, height: 0.2, view: 'front' },
            { code: 'shoulder', name: '肩部', x: -0.35, y: -0.35, width: 0.3, height: 0.2, view: 'back' },
            { code: 'upper_back', name: '上背部', x: 0, y: -0.2, width: 0.4, height: 0.3, view: 'back' },
            { code: 'lower_back', name: '腰部', x: 0, y: 0.05, width: 0.35, height: 0.25, view: 'back' },
            { code: 'hip', name: '臀部', x: 0, y: 0.25, width: 0.4, height: 0.2, view: 'back' },
            { code: 'leg', name: '下肢', x: -0.15, y: 0.5, width: 0.15, height: 0.4, view: 'front' },
            { code: 'leg', name: '下肢', x: -0.15, y: 0.5, width: 0.15, height: 0.4, view: 'back' },
            { code: 'arm', name: '上肢', x: -0.45, y: -0.1, width: 0.15, height: 0.35, view: 'front' },
            { code: 'arm', name: '上肢', x: -0.45, y: -0.1, width: 0.15, height: 0.35, view: 'back' }
        ];

        // Filter by current view
        const viewAreas = areas.filter(a => a.view === this.viewMode);

        for (const area of viewAreas) {
            const areaX = centerX + area.x * scale;
            const areaY = centerY + area.y * scale;
            const areaWidth = area.width * scale;
            const areaHeight = area.height * scale;

            // Check if click is within bounding box
            if (canvasX >= areaX - areaWidth / 2 &&
                canvasX <= areaX + areaWidth / 2 &&
                canvasY >= areaY - areaHeight / 2 &&
                canvasY <= areaY + areaHeight / 2) {
                return area;
            }
        }

        return null;
    }

    handleClick(x, y) {
        // Convert click coordinates to canvas coordinates
        // This is a simplified implementation
        console.log('Clicked at:', x, y);
        // You can implement point/area selection here
    }

    updateSelectedPoints(points) {
        this.options.selectedPoints = points;
        this.render();
    }

    updateSelectedAreas(areas) {
        this.options.selectedAreas = areas;
        this.render();
    }
}

// Export for use in templates
window.Body3DViewer = Body3DViewer;
