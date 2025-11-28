#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from acupuncture.forms import AcupunctureSessionForm

User = get_user_model()

# Create a test context
context = {
    'form': AcupunctureSessionForm(),
    'object': None,
}

# Render template
html = render_to_string('acupuncture/acupuncturesession_form.html', context)

print('=== 模板渲染测试 | Template Rendering Test ===\n')
print(f'渲染的HTML长度 | Rendered HTML length: {len(html)} chars')
print(f'\n是否包含 extra_js | Contains extra_js: {"extra_js" in html}')
print(f'是否包含 Three.js | Contains Three.js: {"Three.js" in html}')
print(f'是否包含 enhanced | Contains enhanced: {"enhanced" in html}')
print(f'是否包含 Body3DViewerEnhanced | Contains Body3DViewerEnhanced: {"Body3DViewerEnhanced" in html}')
print(f'是否包含 acupointViewer | Contains acupointViewer: {"acupointViewer" in html}')

print('\n=== HTML末尾1000字符 | Last 1000 chars ===')
print(html[-1000:])
