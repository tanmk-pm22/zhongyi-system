#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试3D人体解剖图 | Test 3D Anatomy Viewer
检查针灸和推拿模块的3D解剖图显示 | Check 3D anatomy viewer in acupuncture and tuina modules
"""

import requests
from bs4 import BeautifulSoup
import sys

def test_page(url, page_name):
    """测试页面 | Test page"""
    print(f"\n{'='*60}")
    print(f"测试 | Testing: {page_name}")
    print(f"URL: {url}")
    print(f"{'='*60}")

    try:
        response = requests.get(url, timeout=10)
        print(f"✓ 状态码 | Status Code: {response.status_code}")

        if response.status_code != 200:
            print(f"✗ 页面返回错误状态码 | Page returned error status code")
            return False

        soup = BeautifulSoup(response.content, 'html.parser')

        # 检查3D相关元素 | Check 3D related elements
        checks = {
            'Three.js库 | Three.js library': soup.find('script', src=lambda x: x and 'three' in x.lower() if x else False) or soup.find('script', string=lambda x: x and 'three' in x.lower() if x else False),
            '实时3D解剖图谱JS | RealTime 3D Atlas JS': soup.find('script', src=lambda x: x and 'realtime-3d-anatomy-atlas' in x if x else False),
            '针灸3D容器 | Acupuncture 3D container': soup.find('div', id='acupointViewer'),
            '推拿3D容器 | Tuina 3D container': soup.find('div', id='tuinaViewer'),
        }

        all_passed = True
        for check_name, element in checks.items():
            if element:
                print(f"✓ {check_name}: 找到 | Found")
            else:
                print(f"✗ {check_name}: 未找到 | Not found")
                all_passed = False

        # 检查是否有JavaScript错误 | Check for JavaScript errors
        scripts = soup.find_all('script')
        print(f"\n✓ 找到 {len(scripts)} 个脚本标签 | Found {len(scripts)} script tags")

        return all_passed

    except requests.exceptions.RequestException as e:
        print(f"✗ 请求失败 | Request failed: {e}")
        return False
    except Exception as e:
        print(f"✗ 测试出错 | Test error: {e}")
        return False

def main():
    """主函数 | Main function"""
    print("\n" + "="*60)
    print("3D人体解剖图测试 | 3D Anatomy Viewer Test")
    print("="*60)

    base_url = "http://127.0.0.1:8000"

    # 测试页面列表 | Test page list
    test_pages = [
        (f"{base_url}/acupuncture/", "针灸模块首页 | Acupuncture Home"),
        (f"{base_url}/acupuncture/create/", "新建针灸记录 | New Acupuncture Session"),
        (f"{base_url}/tuina/", "推拿模块首页 | Tuina Home"),
        (f"{base_url}/tuina/new/", "新建推拿记录 | New Tuina Session"),
    ]

    results = {}
    for url, name in test_pages:
        results[name] = test_page(url, name)

    # 总结 | Summary
    print("\n" + "="*60)
    print("测试总结 | Test Summary")
    print("="*60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for name, result in results.items():
        status = "✓ 通过 | PASSED" if result else "✗ 失败 | FAILED"
        print(f"{status}: {name}")

    print(f"\n总计 | Total: {passed}/{total} 通过 | passed")

    if passed == total:
        print("\n✓ 所有测试通过！| All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} 个测试失败 | tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
