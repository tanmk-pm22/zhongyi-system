#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""保存页面HTML | Save page HTML"""

import requests

url = "http://127.0.0.1:8000/acupuncture/create/"
response = requests.get(url)

with open('acupuncture_create_page.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

print(f"✓ 页面已保存到 acupuncture_create_page.html | Page saved")
print(f"文件大小 | File size: {len(response.text)} 字符 | characters")

# 显示最后几行 | Show last few lines
lines = response.text.split('\n')
print("\n最后20行 | Last 20 lines:")
print("="*60)
for line in lines[-20:]:
    print(line)
