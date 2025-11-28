#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查页面源代码 | Check page source"""

import requests

url = "http://127.0.0.1:8000/acupuncture/create/"
response = requests.get(url)

print(f"状态码 | Status: {response.status_code}")
print("\n" + "="*60)
print("搜索关键词 | Searching for keywords:")
print("="*60)

keywords = [
    "three",
    "Three.js",
    "acupointViewer",
    "realtime-3d-anatomy-atlas",
    "extra_js",
]

html = response.text
for keyword in keywords:
    if keyword.lower() in html.lower():
        print(f"✓ 找到 | Found: {keyword}")
        # 显示匹配的行 | Show matching lines
        lines = html.split('\n')
        for i, line in enumerate(lines):
            if keyword.lower() in line.lower():
                print(f"  行 {i+1}: {line.strip()[:100]}")
    else:
        print(f"✗ 未找到 | Not found: {keyword}")

print("\n" + "="*60)
print("查找 <div id= 标签 | Looking for <div id= tags:")
print("="*60)
import re
div_ids = re.findall(r'<div[^>]*id=["\']([^"\']+)["\']', html)
print("找到的DIV IDs | Found DIV IDs:")
for div_id in div_ids[:20]:  # Show first 20
    print(f"  - {div_id}")
