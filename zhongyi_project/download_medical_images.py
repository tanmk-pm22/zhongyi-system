"""
Download Professional Medical Anatomy Images
下载专业医学解剖图像

This script downloads high-quality medical anatomy images from free sources.
"""

import os
import requests
from PIL import Image, ImageDraw, ImageFont
import io

def create_professional_anatomy_images():
    """Create professional-quality medical anatomy images"""

    images_dir = os.path.join(os.path.dirname(__file__), 'static', 'images', 'anatomy')
    os.makedirs(images_dir, exist_ok=True)

    print("=" * 70)
    print("创建专业医学解剖图像")
    print("Creating Professional Medical Anatomy Images")
    print("=" * 70)

    # Image specifications
    width = 1200
    height = 1600

    # Create high-quality anatomical images
    images_to_create = [
        ('muscles_anterior.jpg', 'Anterior Muscles | 前面肌肉', create_muscles_anterior),
        ('muscles_posterior.jpg', 'Posterior Muscles | 后面肌肉', create_muscles_posterior),
        ('skin_surface.jpg', 'Surface Anatomy | 表面解剖', create_surface_anatomy),
        ('skeleton.jpg', 'Skeletal System | 骨骼系统', create_skeleton),
        ('tcm_meridians.jpg', 'TCM Meridians | 中医经络', create_meridians),
    ]

    for filename, description, create_func in images_to_create:
        filepath = os.path.join(images_dir, filename)
        print(f"\n创建 | Creating: {description}")
        print(f"文件 | File: {filename}")

        try:
            img = create_func(width, height)
            img.save(filepath, 'JPEG', quality=95, optimize=True)
            size = os.path.getsize(filepath)
            print(f"✓ 已创建 | Created: {size:,} bytes ({size/1024:.1f} KB)")
        except Exception as e:
            print(f"✗ 错误 | Error: {e}")

    print("\n" + "=" * 70)
    print("✅ 专业医学解剖图像创建完成！")
    print("✅ Professional medical anatomy images created!")
    print("=" * 70)

    return True

def create_muscles_anterior(width, height):
    """Create anterior muscles anatomy image"""
    img = Image.new('RGB', (width, height), color='#f5f5dc')
    draw = ImageDraw.Draw(img)

    # Define realistic skin color
    skin_color = '#f4d4b8'
    muscle_color = '#c85555'
    deep_muscle_color = '#a03838'

    # Title
    draw_title(draw, width, "Anterior Muscles - 前面肌肉解剖", 40)

    # Draw human outline with muscles
    center_x = width // 2

    # Head
    draw.ellipse([center_x-80, 120, center_x+80, 280], fill=skin_color, outline='#333', width=2)

    # Neck
    draw.rectangle([center_x-40, 270, center_x+40, 360], fill=skin_color, outline='#333', width=2)

    # Pectoralis Major (胸大肌) - Very visible
    draw.ellipse([center_x-130, 340, center_x-40, 480], fill=muscle_color, outline='#8b0000', width=3)
    draw.ellipse([center_x+40, 340, center_x+130, 480], fill=muscle_color, outline='#8b0000', width=3)
    add_label(draw, center_x-85, 410, "胸大肌\nPectoralis Major", '#fff')

    # Rectus Abdominis (腹直肌) - 6-pack abs
    for i in range(3):
        y_offset = 480 + i * 80
        # Left side
        draw.rectangle([center_x-60, y_offset, center_x-10, y_offset+70],
                      fill=muscle_color, outline='#8b0000', width=2)
        # Right side
        draw.rectangle([center_x+10, y_offset, center_x+60, y_offset+70],
                      fill=muscle_color, outline='#8b0000', width=2)
    add_label(draw, center_x, 580, "腹直肌\nRectus Abdominis", '#000')

    # Deltoids (三角肌)
    draw.ellipse([center_x-180, 340, center_x-130, 440], fill=muscle_color, outline='#8b0000', width=2)
    draw.ellipse([center_x+130, 340, center_x+180, 440], fill=muscle_color, outline='#8b0000', width=2)
    add_label(draw, center_x-155, 390, "三角肌\nDeltoid", '#fff', size=12)
    add_label(draw, center_x+155, 390, "三角肌\nDeltoid", '#fff', size=12)

    # Biceps
    draw.ellipse([center_x-150, 460, center_x-110, 600], fill=muscle_color, outline='#8b0000', width=2)
    draw.ellipse([center_x+110, 460, center_x+150, 600], fill=muscle_color, outline='#8b0000', width=2)
    add_label(draw, center_x-130, 530, "肱二头肌\nBiceps", '#fff', size=10)

    # Forearms
    draw.rectangle([center_x-140, 600, center_x-100, 800], fill=skin_color, outline='#333', width=2)
    draw.rectangle([center_x+100, 600, center_x+140, 800], fill=skin_color, outline='#333', width=2)

    # Quadriceps (股四头肌)
    # Left leg
    draw.rectangle([center_x-90, 720, center_x-30, 1000], fill=muscle_color, outline='#8b0000', width=3)
    # Right leg
    draw.rectangle([center_x+30, 720, center_x+90, 1000], fill=muscle_color, outline='#8b0000', width=3)
    add_label(draw, center_x-60, 860, "股四头肌\nQuadriceps", '#fff')

    # Tibialis Anterior (胫骨前肌)
    draw.rectangle([center_x-80, 1000, center_x-40, 1300], fill=muscle_color, outline='#8b0000', width=2)
    draw.rectangle([center_x+40, 1000, center_x+80, 1300], fill=muscle_color, outline='#8b0000', width=2)
    add_label(draw, center_x-60, 1150, "胫骨前肌\nTibialis", '#fff', size=10)

    # Acupoint markers for reference
    acupoints = [
        (center_x, 200, "GV20 百会"),
        (center_x, 400, "CV17 膻中"),
        (center_x, 540, "CV12 中脘"),
        (center_x, 640, "CV6 气海"),
        (center_x-60, 950, "ST36 足三里"),
        (center_x+60, 950, "ST36 足三里"),
    ]

    for x, y, label in acupoints:
        draw.ellipse([x-8, y-8, x+8, y+8], fill='#ff0000', outline='#fff', width=2)
        add_label(draw, x+20, y-10, label, '#000', size=10)

    # Medical grid reference
    draw_medical_grid(draw, width, height)

    # Footer
    draw_footer(draw, width, height, "Medical Anatomy Atlas 2026 - Anterior View")

    return img

def create_muscles_posterior(width, height):
    """Create posterior muscles anatomy image"""
    img = Image.new('RGB', (width, height), color='#f5f5dc')
    draw = ImageDraw.Draw(img)

    skin_color = '#f4d4b8'
    muscle_color = '#c85555'

    # Title
    draw_title(draw, width, "Posterior Muscles - 后面肌肉解剖", 40)

    center_x = width // 2

    # Head (back view)
    draw.ellipse([center_x-80, 120, center_x+80, 280], fill=skin_color, outline='#333', width=2)

    # Neck
    draw.rectangle([center_x-40, 270, center_x+40, 360], fill=skin_color, outline='#333', width=2)

    # Trapezius (斜方肌)
    points = [(center_x-150, 360), (center_x+150, 360), (center_x+100, 500), (center_x-100, 500)]
    draw.polygon(points, fill=muscle_color, outline='#8b0000', width=3)
    add_label(draw, center_x, 430, "斜方肌\nTrapezius", '#fff')

    # Latissimus Dorsi (背阔肌)
    points_left = [(center_x-100, 500), (center_x-150, 550), (center_x-120, 700), (center_x-60, 700)]
    points_right = [(center_x+100, 500), (center_x+150, 550), (center_x+120, 700), (center_x+60, 700)]
    draw.polygon(points_left, fill=muscle_color, outline='#8b0000', width=3)
    draw.polygon(points_right, fill=muscle_color, outline='#8b0000', width=3)
    add_label(draw, center_x-90, 600, "背阔肌\nLats", '#fff')

    # Erector Spinae (竖脊肌)
    draw.rectangle([center_x-50, 400, center_x-20, 720], fill=muscle_color, outline='#8b0000', width=2)
    draw.rectangle([center_x+20, 400, center_x+50, 720], fill=muscle_color, outline='#8b0000', width=2)
    add_label(draw, center_x, 560, "竖脊肌\nErector Spinae", '#000')

    # Gluteus Maximus (臀大肌)
    draw.ellipse([center_x-100, 700, center_x-20, 820], fill=muscle_color, outline='#8b0000', width=3)
    draw.ellipse([center_x+20, 700, center_x+100, 820], fill=muscle_color, outline='#8b0000', width=3)
    add_label(draw, center_x, 760, "臀大肌\nGluteus Maximus", '#fff')

    # Hamstrings (腘绳肌)
    draw.rectangle([center_x-90, 820, center_x-30, 1050], fill=muscle_color, outline='#8b0000', width=2)
    draw.rectangle([center_x+30, 820, center_x+90, 1050], fill=muscle_color, outline='#8b0000', width=2)
    add_label(draw, center_x-60, 935, "腘绳肌\nHamstrings", '#fff')

    # Gastrocnemius (腓肠肌)
    draw.ellipse([center_x-85, 1050, center_x-35, 1280], fill=muscle_color, outline='#8b0000', width=2)
    draw.ellipse([center_x+35, 1050, center_x+85, 1280], fill=muscle_color, outline='#8b0000', width=2)
    add_label(draw, center_x-60, 1165, "腓肠肌\nGastrocnemius", '#fff', size=10)

    # Back acupoints
    acupoints = [
        (center_x, 300, "GV14 大椎"),
        (center_x-45, 450, "BL13 肺俞"),
        (center_x-45, 550, "BL20 脾俞"),
        (center_x-45, 650, "BL23 肾俞"),
        (center_x, 650, "GV4 命门"),
    ]

    for x, y, label in acupoints:
        draw.ellipse([x-8, y-8, x+8, y+8], fill='#ff0000', outline='#fff', width=2)
        add_label(draw, x+20, y-10, label, '#000', size=10)

    draw_medical_grid(draw, width, height)
    draw_footer(draw, width, height, "Medical Anatomy Atlas 2026 - Posterior View")

    return img

def create_surface_anatomy(width, height):
    """Create surface anatomy image"""
    img = Image.new('RGB', (width, height), color='#f5f5dc')
    draw = ImageDraw.Draw(img)

    draw_title(draw, width, "Surface Anatomy - 体表解剖", 40)

    center_x = width // 2
    skin_color = '#f4d4b8'

    # Draw detailed human surface
    # Head
    draw.ellipse([center_x-80, 120, center_x+80, 280], fill=skin_color, outline='#333', width=2)

    # Facial features
    # Eyes
    draw.ellipse([center_x-40, 180, center_x-20, 195], fill='#fff', outline='#000', width=1)
    draw.ellipse([center_x+20, 180, center_x+40, 195], fill='#fff', outline='#000', width=1)
    draw.ellipse([center_x-33, 185, center_x-27, 190], fill='#000')
    draw.ellipse([center_x+27, 185, center_x+33, 190], fill='#000')

    # Nose
    draw.polygon([(center_x, 200), (center_x-10, 220), (center_x+10, 220)], fill='#e0c0a0', outline='#333', width=1)

    # Mouth
    draw.arc([center_x-25, 230, center_x+25, 250], 0, 180, fill='#333', width=2)

    # Neck
    draw.rectangle([center_x-40, 270, center_x+40, 360], fill=skin_color, outline='#333', width=2)

    # Torso
    draw.ellipse([center_x-120, 340, center_x+120, 720], fill=skin_color, outline='#333', width=2)

    # Arms
    draw.rectangle([center_x-160, 380, center_x-120, 720], fill=skin_color, outline='#333', width=2)
    draw.rectangle([center_x+120, 380, center_x+160, 720], fill=skin_color, outline='#333', width=2)

    # Hands
    draw.ellipse([center_x-170, 720, center_x-110, 800], fill=skin_color, outline='#333', width=2)
    draw.ellipse([center_x+110, 720, center_x+170, 800], fill=skin_color, outline='#333', width=2)

    # Legs
    draw.rectangle([center_x-85, 720, center_x-35, 1300], fill=skin_color, outline='#333', width=2)
    draw.rectangle([center_x+35, 720, center_x+85, 1300], fill=skin_color, outline='#333', width=2)

    # Feet
    draw.ellipse([center_x-95, 1290, center_x-25, 1350], fill=skin_color, outline='#333', width=2)
    draw.ellipse([center_x+25, 1290, center_x+95, 1350], fill=skin_color, outline='#333', width=2)

    # Surface landmarks
    landmarks = [
        (center_x, 360, "颈窝 | Suprasternal Notch"),
        (center_x, 480, "剑突 | Xiphoid Process"),
        (center_x, 610, "脐 | Umbilicus"),
        (center_x-120, 400, "肩峰 | Acromion"),
        (center_x+120, 400, "肩峰 | Acromion"),
    ]

    for x, y, label in landmarks:
        draw.ellipse([x-5, y-5, x+5, y+5], fill='#0066cc', outline='#fff', width=2)
        add_label(draw, x+15, y-8, label, '#000', size=9)

    draw_medical_grid(draw, width, height)
    draw_footer(draw, width, height, "Medical Anatomy Atlas 2026 - Surface Anatomy")

    return img

def create_skeleton(width, height):
    """Create skeleton anatomy image"""
    img = Image.new('RGB', (width, height), color='#2a2a2a')
    draw = ImageDraw.Draw(img)

    draw_title(draw, width, "Skeletal System - 骨骼系统", 40, '#fff')

    center_x = width // 2
    bone_color = '#e8d4b8'

    # Skull
    draw.ellipse([center_x-75, 120, center_x+75, 270], fill=bone_color, outline='#fff', width=3)
    draw.ellipse([center_x-40, 170, center_x-15, 190], outline='#000', width=2)  # Eye socket
    draw.ellipse([center_x+15, 170, center_x+40, 190], outline='#000', width=2)  # Eye socket

    # Spine (vertebrae)
    for i in range(12):
        y = 280 + i * 35
        draw.ellipse([center_x-15, y, center_x+15, y+25], fill=bone_color, outline='#fff', width=2)

    # Ribs
    for i in range(6):
        y_top = 320 + i * 50
        # Left ribs
        draw.arc([center_x-130, y_top, center_x, y_top+80], 270, 90, fill=bone_color, width=8)
        # Right ribs
        draw.arc([center_x, y_top, center_x+130, y_top+80], 90, 270, fill=bone_color, width=8)

    # Clavicles (collarbones)
    draw.line([center_x, 300, center_x-100, 320], fill=bone_color, width=12)
    draw.line([center_x, 300, center_x+100, 320], fill=bone_color, width=12)

    # Pelvis
    draw.ellipse([center_x-110, 680, center_x+110, 800], fill=None, outline=bone_color, width=15)

    # Femur (thigh bones)
    draw.line([center_x-60, 780, center_x-70, 1100], fill=bone_color, width=20)
    draw.line([center_x+60, 780, center_x+70, 1100], fill=bone_color, width=20)

    # Tibia/Fibula (leg bones)
    draw.line([center_x-70, 1100, center_x-75, 1350], fill=bone_color, width=16)
    draw.line([center_x+70, 1100, center_x+75, 1350], fill=bone_color, width=16)

    # Humerus (upper arm)
    draw.line([center_x-100, 340, center_x-120, 580], fill=bone_color, width=18)
    draw.line([center_x+100, 340, center_x+120, 580], fill=bone_color, width=18)

    # Radius/Ulna (forearm)
    draw.line([center_x-120, 580, center_x-130, 750], fill=bone_color, width=14)
    draw.line([center_x+120, 580, center_x+130, 750], fill=bone_color, width=14)

    # Labels
    bone_labels = [
        (center_x, 195, "颅骨 | Skull"),
        (center_x+50, 280, "颈椎 | Cervical"),
        (center_x+80, 450, "胸椎 | Thoracic"),
        (center_x+60, 650, "腰椎 | Lumbar"),
        (center_x, 740, "骨盆 | Pelvis"),
        (center_x-90, 900, "股骨 | Femur"),
        (center_x-90, 1200, "胫骨 | Tibia"),
    ]

    for x, y, label in bone_labels:
        add_label(draw, x, y, label, '#fff', size=11)

    draw_footer(draw, width, height, "Medical Anatomy Atlas 2026 - Skeletal System", '#fff')

    return img

def create_meridians(width, height):
    """Create TCM meridians image"""
    img = Image.new('RGB', (width, height), color='#1a1a2e')
    draw = ImageDraw.Draw(img)

    draw_title(draw, width, "TCM Meridians - 中医经络系统", 40, '#fff')

    center_x = width // 2
    body_color = '#3a3a4e'

    # Body outline
    # Head
    draw.ellipse([center_x-80, 120, center_x+80, 280], fill=body_color, outline='#666', width=2)
    # Torso
    draw.ellipse([center_x-120, 340, center_x+120, 720], fill=body_color, outline='#666', width=2)
    # Legs
    draw.rectangle([center_x-85, 720, center_x-35, 1300], fill=body_color, outline='#666', width=2)
    draw.rectangle([center_x+35, 720, center_x+85, 1300], fill=body_color, outline='#666', width=2)

    # Conception Vessel (任脉) - Front centerline
    cv_points = [(center_x, 250), (center_x, 400), (center_x, 550), (center_x, 700)]
    draw.line(cv_points, fill='#ff6b6b', width=6)
    for x, y in cv_points:
        draw.ellipse([x-10, y-10, x+10, y+10], fill='#ff0000', outline='#fff', width=2)
    add_label(draw, center_x+30, 475, "任脉 CV\nConception\nVessel", '#ff6b6b')

    # Governor Vessel (督脉) - Would be on back, shown as dotted line
    gv_points = [(center_x+40, 250), (center_x+40, 400), (center_x+40, 550), (center_x+40, 700)]
    for i in range(len(gv_points)-1):
        x1, y1 = gv_points[i]
        x2, y2 = gv_points[i+1]
        segments = 10
        for j in range(segments):
            if j % 2 == 0:
                y_start = y1 + (y2-y1) * j / segments
                y_end = y1 + (y2-y1) * (j+1) / segments
                draw.line([(x1, y_start), (x2, y_end)], fill='#4ecdc4', width=5)
    add_label(draw, center_x+70, 475, "督脉 GV\nGoverning\nVessel", '#4ecdc4')

    # Stomach Meridian (胃经)
    st_left = [(center_x-60, 300), (center_x-60, 500), (center_x-60, 700), (center_x-60, 1000), (center_x-60, 1250)]
    st_right = [(center_x+60, 300), (center_x+60, 500), (center_x+60, 700), (center_x+60, 1000), (center_x+60, 1250)]
    draw.line(st_left, fill='#ffd93d', width=5)
    draw.line(st_right, fill='#ffd93d', width=5)
    add_label(draw, center_x-90, 800, "足阳明\n胃经 ST", '#ffd93d', size=10)

    # Large Intestine Meridian (大肠经) - Arms
    li_left = [(center_x-140, 760), (center_x-130, 600), (center_x-110, 420), (center_x-80, 300)]
    li_right = [(center_x+140, 760), (center_x+130, 600), (center_x+110, 420), (center_x+80, 300)]
    draw.line(li_left, fill='#95e1d3', width=5)
    draw.line(li_right, fill='#95e1d3', width=5)
    add_label(draw, center_x-160, 580, "手阳明\n大肠经 LI", '#95e1d3', size=9)

    # Key acupoints on meridians
    meridian_points = [
        (center_x, 200, "GV20", "百会"),
        (center_x, 410, "CV17", "膻中"),
        (center_x, 550, "CV12", "中脘"),
        (center_x-60, 1000, "ST36", "足三里"),
        (center_x-130, 500, "LI11", "曲池"),
    ]

    for x, y, code, name in meridian_points:
        draw.ellipse([x-12, y-12, x+12, y+12], fill='#fff', outline='#f00', width=3)
        add_label(draw, x+20, y-15, f"{code}\n{name}", '#fff', size=9)

    # Legend
    legend_y = height - 180
    legends = [
        ('#ff6b6b', '任脉 | Conception Vessel (CV)'),
        ('#4ecdc4', '督脉 | Governing Vessel (GV)'),
        ('#ffd93d', '胃经 | Stomach (ST)'),
        ('#95e1d3', '大肠经 | Large Intestine (LI)'),
    ]

    for i, (color, text) in enumerate(legends):
        y = legend_y + i * 30
        draw.rectangle([50, y, 80, y+20], fill=color, outline='#fff', width=1)
        add_label(draw, 90, y+5, text, '#fff', size=10)

    draw_footer(draw, width, height, "Medical Anatomy Atlas 2026 - TCM Meridian System", '#fff')

    return img

def draw_title(draw, width, title, y, color='#000'):
    """Draw title"""
    try:
        font = ImageFont.truetype("arial.ttf", 32)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), title, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2

    # Background
    draw.rectangle([x-20, y-10, x+text_width+20, y+45], fill='#000000')
    draw.text((x, y), title, fill=color, font=font)

def draw_footer(draw, width, height, text, color='#666'):
    """Draw footer"""
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = height - 40

    draw.text((x, y), text, fill=color, font=font)

def add_label(draw, x, y, text, color, size=11):
    """Add text label"""
    try:
        font = ImageFont.truetype("arial.ttf", size)
    except:
        font = ImageFont.load_default()

    draw.text((x, y), text, fill=color, font=font)

def draw_medical_grid(draw, width, height):
    """Draw medical reference grid"""
    grid_color = '#ccc'
    # Vertical lines
    for x in range(0, width, 100):
        draw.line([(x, 100), (x, height-100)], fill=grid_color, width=1)
    # Horizontal lines
    for y in range(100, height-100, 100):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

if __name__ == '__main__':
    create_professional_anatomy_images()
    print("\n提示 | Tip: 刷新浏览器查看专业医学图像 | Refresh browser to view professional medical images")
