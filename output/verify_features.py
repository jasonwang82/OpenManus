#!/usr/bin/env python3
"""
验证北京三日游网页功能的脚本
"""
import json
import re
import requests
from bs4 import BeautifulSoup

def check_html_structure():
    """检查HTML结构"""
    print("=" * 60)
    print("1. 检查HTML结构")
    print("=" * 60)

    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 检查关键元素
    checks = {
        "标题": '<title>北京三日旅游指南</title>',
        "腾讯地图API": 'map.qq.com/api/gljs',
        "三日路线按钮": 'data-day="1"',  # 检查第一天按钮
        "景点列表容器": 'id="spotsContainer"',
        "地图容器": 'id="map"',
        "景点详情区域": 'id="detailSection"',
    }

    for name, pattern in checks.items():
        if pattern in html_content:
            print(f"✓ {name} - 存在")
        else:
            print(f"✗ {name} - 缺失")

    print()

def check_javascript_data():
    """检查JavaScript中的数据"""
    print("=" * 60)
    print("2. 检查JavaScript数据结构")
    print("=" * 60)

    with open('js/main.js', 'r', encoding='utf-8') as f:
        js_content = f.read()

    # 提取itineraryData对象
    data_match = re.search(r'const itineraryData = \{([\s\S]*?)\};', js_content)
    if data_match:
        print("✓ itineraryData 数据结构存在")

        # 检查三天的数据
        for day in [1, 2, 3]:
            if f'{day}:' in data_match.group(0):
                print(f"✓ 第{day}天数据存在")
                # 检查景点数量
                day_pattern = rf'{day}:\s*\{{[\s\S]*?title:.*?spots:'
                day_match = re.search(day_pattern, js_content)
                if day_match:
                    # 计算该天的景点数量
                    spots_count = js_content.count('name:', data_match.start(), data_match.end())
                    print(f"  - 第{day}天包含景点")
    else:
        print("✗ itineraryData 数据结构不存在")

    print()

def check_css_styles():
    """检查CSS样式"""
    print("=" * 60)
    print("3. 检查CSS样式")
    print("=" * 60)

    with open('css/style.css', 'r', encoding='utf-8') as f:
        css_content = f.read()

    styles_to_check = [
        ".day-btn",
        ".spot-item",
        "#map",
        ".detail-card",
        ".header",
    ]

    for style in styles_to_check:
        if style in css_content:
            print(f"✓ {style} 样式存在")
        else:
            print(f"✗ {style} 样式缺失")

    print()

def test_functionality():
    """测试功能点"""
    print("=" * 60)
    print("4. 功能点验证")
    print("=" * 60)

    with open('js/main.js', 'r', encoding='utf-8') as f:
        js_content = f.read()

    functions = {
        "地图初始化": "function initMap()",
        "加载路线": "function loadItinerary(day)",
        "渲染景点列表": "function renderSpotsList(spots)",
        "显示景点详情": "function showSpotDetail(spot)",
        "清除地图标记": "function clearMarkers()",
        "添加景点标记": "function addMarkers(spots)",
        "高亮景点项": "function highlightSpotItem(index)",
        "地图定位到景点": "function centerMapOnSpot(spot)",
    }

    for name, pattern in functions.items():
        if pattern in js_content:
            print(f"✓ {name} 功能已实现")
        else:
            print(f"✗ {name} 功能缺失")

    print()

def check_day1_data():
    """检查第一天的具体数据"""
    print("=" * 60)
    print("5. 第一天数据详情")
    print("=" * 60)

    with open('js/main.js', 'r', encoding='utf-8') as f:
        js_content = f.read()

    # 提取第一天的数据
    day1_pattern = r'1:\s*\{[\s\S]*?title:\s*"([^"]+)"[\s\S]*?spots:\s*\[([\s\S]*?)\]'
    day1_match = re.search(day1_pattern, js_content)

    if day1_match:
        title = day1_match.group(1)
        spots_section = day1_match.group(2)

        print(f"第一天主题: {title}")

        # 提取景点
        spot_pattern = r'\{\s*name:\s*"([^"]+)"[\s\S]*?lat:\s*([\d.]+)[\s\S]*?lng:\s*([\d.]+)[\s\S]*?description:\s*"([^"]+)"'
        spots = re.findall(spot_pattern, spots_section)

        print(f"景点数量: {len(spots)}")
        for i, (name, lat, lng, desc) in enumerate(spots, 1):
            print(f"  {i}. {name}")
            print(f"     坐标: ({lat}, {lng})")
            print(f"     描述: {desc[:30]}...")
    else:
        print("✗ 无法提取第一天数据")

    print()

def check_api_key():
    """检查腾讯地图API密钥"""
    print("=" * 60)
    print("6. API密钥检查")
    print("=" * 60)

    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    if 'YOUR_API_KEY' in html_content:
        print("⚠ 警告: 腾讯地图API密钥未配置（使用占位符 YOUR_API_KEY）")
        print("  地图可能无法正常显示，需要替换为有效的API密钥")
    else:
        print("✓ API密钥已配置")

    print()

def main():
    """主函数"""
    print("\n")
    print("█" * 60)
    print("█" + " " * 58 + "█")
    print("█  北京三日游网页功能验证报告                  █")
    print("█" + " " * 58 + "█")
    print("█" * 60)
    print("\n")

    try:
        check_html_structure()
        check_javascript_data()
        check_css_styles()
        test_functionality()
        check_day1_data()
        check_api_key()

        print("=" * 60)
        print("验证完成！")
        print("=" * 60)

    except FileNotFoundError as e:
        print(f"错误: 文件不存在 - {e}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main()
