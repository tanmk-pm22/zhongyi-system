import requests

r = requests.get('http://127.0.0.1:8000/acupuncture/create/')
print('=== 完整页面检查 | Full Page Check ===\n')
print(f'响应状态 | Response Status: {r.status_code}')
print(f'内容长度 | Content Length: {len(r.text)} chars')
print('\n=== 页面末尾200字符 | Last 200 chars ===')
print(r.text[-200:])
print('\n=== 检查关键词 | Check Keywords ===')
keywords = ['extra_js', 'Three.js', 'OrbitControls', 'enhanced', 'acupointViewer']
for kw in keywords:
    count = r.text.count(kw)
    print(f'  {kw}: {count} 次 | times')
