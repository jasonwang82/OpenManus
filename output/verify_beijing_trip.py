#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证北京三日游基础能力的测试脚本
"""
import json
import re
from pathlib import Path

def verify_html_structure():
    """验证 HTML 结构是否完整"""
    print("=" * 60)
    print("1. 验证 HTML 结构")
    print("=" * 60)

    html_path = Path(__file__).parent / "index.html"
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    checks = [
        ("DOCTYPE 声明", r"<!DOCTYPE html>", True),
        ("中文语言设置", r'lang="zh-CN"', True),
        ("标题元素", r"<title>北京三日旅游指南</title>", True),
        ("CSS 样式表", r'<link rel="stylesheet" href="css/style.css">', True),
        ("JavaScript 文件", r'<script src="js/main.js"></script>', True),
        ("腾讯地图 API", r'map.qq.com/api/gljs', True),
        ("头部区域", r'<header class="header">', True),
        ("三日路线选择", r'<section class="itinerary-section">', True),
        ("景点信息展示", r'<section class="spots-section">', True),
        ("景点详情", r'<section class="detail-section"', True),
        ("页脚", r'<footer class="footer">', True),
    ]

    results = []
    for name, pattern, expected in checks:
        match = re.search(pattern, html_content)
        found = match is not None
        status = "✅ 通过" if found == expected else "❌ 失败"
        results.append((name, status))
        print(f"  {name}: {status}")

    passed = sum(1 for _, status in results if "✅" in status)
    total = len(results)
    print(f"\n结果: {passed}/{total} 项检查通过")
    print()

    return all("✅" in status for _, status in results)

def verify_javascript_data():
    """验证 JavaScript 数据结构"""
    print("=" * 60)
    print("2. 验证 JavaScript 数据结构")
    print("=" * 60)

    js_path = Path(__file__).parent / "js" / "main.js"
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()

    checks = [
        ("三日路线数据", r"const itineraryData = \{", True),
        ("第一天数据", r"1:\s*\{", True),
        ("第二天数据", r"2:\s*\{", True),
        ("第三天数据", r"3:\s*\{", True),
        ("景点数组", r"spots:\s*\[", True),
        ("景点名称", r"name:", True),
        ("经纬度", r"lat:.*?lng:", True),
        ("景点描述", r"description:", True),
        ("开放时间", r"openTime:", True),
        ("门票价格", r"price:", True),
        ("游览时长", r"duration:", True),
        ("地图初始化函数", r"function initMap\(\)", True),
        ("添加标记函数", r"function addMarkers", True),
        ("显示景点列表", r"function renderSpotsList", True),
        ("显示景点详情", r"function showSpotDetail", True),
        ("加载路线函数", r"function loadItinerary", True),
        ("页面初始化函数", r"function initPage\(\)", True),
    ]

    results = []
    for name, pattern, expected in checks:
        match = re.search(pattern, js_content)
        found = match is not None
        status = "✅ 通过" if found == expected else "❌ 失败"
        results.append((name, status))
        print(f"  {name}: {status}")

    passed = sum(1 for _, status in results if "✅" in status)
    total = len(results)
    print(f"\n结果: {passed}/{total} 项检查通过")
    print()

    return all("✅" in status for _, status in results)

def verify_css_styles():
    """验证 CSS 样式"""
    print("=" * 60)
    print("3. 验证 CSS 样式")
    print("=" * 60)

    css_path = Path(__file__).parent / "css" / "style.css"
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()

    checks = [
        ("全局样式", r"\*\s*\{", True),
        ("头部样式", r"\.header\s*\{", True),
        ("标题样式", r"\.title\s*\{", True),
        ("按钮样式", r"\.day-btn\s*\{", True),
        ("景点列表", r"\.spots-list\s*\{", True),
        ("景点项", r"\.spot-item\s*\{", True),
        ("地图容器", r"\.map-container\s*\{", True),
        ("详情卡片", r"\.detail-card\s*\{", True),
        ("页脚样式", r"\.footer\s*\{", True),
        ("响应式设计", r"@media.*max-width", True),
    ]

    results = []
    for name, pattern, expected in checks:
        match = re.search(pattern, css_content)
        found = match is not None
        status = "✅ 通过" if found == expected else "❌ 失败"
        results.append((name, status))
        print(f"  {name}: {status}")

    passed = sum(1 for _, status in results if "✅" in status)
    total = len(results)
    print(f"\n结果: {passed}/{total} 项检查通过")
    print()

    return all("✅" in status for _, status in results)

def verify_itinerary_content():
    """验证旅游路线内容"""
    print("=" * 60)
    print("4. 验证旅游路线内容")
    print("=" * 60)

    js_path = Path(__file__).parent / "js" / "main.js"
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()

    # 第一天景点
    day1_spots = ["天安门广场", "故宫博物院", "景山公园"]
    # 第二天景点
    day2_spots = ["八达岭长城", "慕田峪长城", "明十三陵"]
    # 第三天景点
    day3_spots = ["颐和园", "圆明园遗址公园", "天坛公园"]

    all_spots = {
        "第一天": day1_spots,
        "第二天": day2_spots,
        "第三天": day3_spots
    }

    results = []
    for day, spots in all_spots.items():
        print(f"\n{day}景点:")
        for spot in spots:
            found = spot in js_content
            status = "✅ 通过" if found else "❌ 失败"
            results.append((day, spot, status))
            print(f"  {spot}: {status}")

    passed = sum(1 for _, _, status in results if "✅" in status)
    total = len(results)
    print(f"\n结果: {passed}/{total} 项检查通过")
    print()

    return all("✅" in status for _, _, status in results)

def verify_file_structure():
    """验证文件结构"""
    print("=" * 60)
    print("5. 验证文件结构")
    print("=" * 60)

    output_dir = Path(__file__).parent

    required_files = [
        ("index.html", "主页面"),
        ("js/main.js", "JavaScript 文件"),
        ("css/style.css", "样式表文件"),
    ]

    required_dirs = [
        ("css", "样式目录"),
        ("js", "脚本目录"),
    ]

    results = []
    print("\n必需文件:")
    for filename, description in required_files:
        file_path = output_dir / filename
        exists = file_path.exists()
        status = "✅ 通过" if exists else "❌ 失败"
        results.append((filename, status))
        print(f"  {filename} ({description}): {status}")

    print("\n必需目录:")
    for dirname, description in required_dirs:
        dir_path = output_dir / dirname
        exists = dir_path.exists() and dir_path.is_dir()
        status = "✅ 通过" if exists else "❌ 失败"
        results.append((dirname, status))
        print(f"  {dirname} ({description}): {status}")

    passed = sum(1 for _, status in results if "✅" in status)
    total = len(results)
    print(f"\n结果: {passed}/{total} 项检查通过")
    print()

    return all("✅" in status for _, status in results)

def verify_interactive_features():
    """验证交互功能"""
    print("=" * 60)
    print("6. 验证交互功能")
    print("=" * 60)

    js_path = Path(__file__).parent / "js" / "main.js"
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()

    checks = [
        ("日期切换按钮事件", r"dayButtons\.forEach.*addEventListener.*click", True),
        ("景点点击事件", r"item\.addEventListener.*click", True),
        ("详情关闭按钮", r"closeDetailBtn\.addEventListener", True),
        ("地图标记点击", r"marker\.on\('click'", True),
        ("地图视野调整", r"map\.fitBounds", True),
        ("地图中心定位", r"map\.setCenter", True),
        ("景点高亮", r"highlightSpotItem", True),
        ("清除标记", r"clearMarkers", True),
    ]

    results = []
    for name, pattern, expected in checks:
        match = re.search(pattern, js_content)
        found = match is not None
        status = "✅ 通过" if found == expected else "❌ 失败"
        results.append((name, status))
        print(f"  {name}: {status}")

    passed = sum(1 for _, status in results if "✅" in status)
    total = len(results)
    print(f"\n结果: {passed}/{total} 项检查通过")
    print()

    return all("✅" in status for _, status in results)

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("北京三日游基础能力验证")
    print("=" * 60 + "\n")

    results = {}

    # 运行所有验证
    results["HTML 结构"] = verify_html_structure()
    results["JavaScript 数据结构"] = verify_javascript_data()
    results["CSS 样式"] = verify_css_styles()
    results["旅游路线内容"] = verify_itinerary_content()
    results["文件结构"] = verify_file_structure()
    results["交互功能"] = verify_interactive_features()

    # 生成总结报告
    print("=" * 60)
    print("验证总结")
    print("=" * 60)

    total_passed = sum(1 for result in results.values() if result)
    total = len(results)

    for category, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{category}: {status}")

    print(f"\n总计: {total_passed}/{total} 个验证项通过")

    if total_passed == total:
        print("\n🎉 所有基础能力验证通过！北京三日游应用已准备就绪。")
        print("\n要查看应用，请在浏览器中访问: http://localhost:8888/index.html")
    else:
        print("\n⚠️  部分验证项未通过，请检查相关功能。")

    print("\n" + "=" * 60)

    return total_passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
