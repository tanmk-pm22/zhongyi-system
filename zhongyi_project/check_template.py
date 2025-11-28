# 检查模板文件
template_path = 'templates/acupuncture/acupuncturesession_form.html'
with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

print('=== 模板文件检查 | Template File Check ===\n')
print(f'文件大小 | File Size: {len(content)} chars')
print(f'\n是否包含 extra_js | Contains extra_js: {"extra_js" in content}')
print(f'是否包含 Three.js | Contains Three.js: {"Three.js" in content}')
print(f'是否包含 enhanced | Contains enhanced: {"enhanced" in content}')

print('\n=== 文件末尾500字符 | Last 500 chars ===')
print(content[-500:])
