import requests

r = requests.get('http://127.0.0.1:8000/acupuncture/create/')
print('=== 针灸页面 HTML检查 | Acupuncture Page HTML Check ===\n')
lines = r.text.split('\n')
for i, line in enumerate(lines, 1):
    if 'body-3d-viewer' in line.lower() or 'body3dviewer' in line.lower():
        print(f'第{i}行 | Line {i}:')
        print(f'  {line.strip()[:200]}')
        print()
