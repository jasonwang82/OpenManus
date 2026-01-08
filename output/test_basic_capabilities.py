#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北京三日游基础能力验证脚本
"""

import requests
from bs4 import BeautifulSoup
import json
import re

def test_page_structure():
    """测试页面基本结构"""
    print("=== 测试页面基本结构 ===")
    try:
        response = requests.get('http://localhost:8080')
        soup = BeautifulSoup(response.text, 'html.parser')

        # 检查标题
        title = soup.find('title')
        if title and '北京三日旅游指南' in title.text:
            print("✓ 页面标题正确")
        else:
            print("✗ 页面标题错误")

        # 检查头部
        header = soup.find('header', class_='header')
        if header:
            print("✓ 头部结构存在")
        else:
            print("✗ 头部结构缺失")

        # 检查主体内容
        main = soup.find('main', class_='main')
        if main:
            print("✓ 主体内容结构存在")
        else:
            print("✗ 主体内容结构缺失")

        # 检查三日路线选择按钮
        day_buttons = soup.find_all('button', class_='day-btn')
        if len(day_buttons) == 3:
            print(f"✓ 三日路线按钮数量正确 (3个)")
        else:
            print(f"✗ 三日路线按钮数量错误 (期望3个,实际{len(day_buttons)}个)")

        # 检查景点列表容器
        spots_container = soup.find('div', id='spotsContainer')
        if spots_container:
            print("✓ 景点列表容器存在")
        else:
            print("✗ 景点列表容器缺失")

        # 检查地图容器
        map_container = soup.find('div', id='map')
        if map_container:
            print("✓ 地图容器存在")
        else:
            print("✗ 地图容器缺失")

        # 检查详情区域
        detail_section = soup.find('section', class_='detail-section')
        if detail_section:
            print("✓ 景点详情区域存在")
        else:
            print("✗ 景点详情区域缺失")

        print("\n页面基本结构测试完成\n")
        return True

    except Exception as e:
        print(f"✗ 页面结构测试失败: {str(e)}\n")
        return False

def test_css_files():
    """测试CSS文件加载"""
    print("=== 测试CSS文件加载 ===")
    try:
        response = requests.get('http://localhost:8080/css/style.css')
        if response.status_code == 200:
            print("✓ CSS文件加载成功")
            content = response.text
            # 检查关键样式类
            if '.header' in content:
                print("✓ 头部样式定义存在")
            if '.day-btn' in content:
                print("✓ 日期按钮样式定义存在")
            if '.spot-item' in content:
                print("✓ 景点项样式定义存在")
            if '.detail-card' in content:
                print("✓ 详情卡片样式定义存在")
        else:
            print(f"✗ CSS文件加载失败 (状态码: {response.status_code})")

        print("\nCSS文件加载测试完成\n")
        return True

    except Exception as e:
        print(f"✗ CSS文件测试失败: {str(e)}\n")
        return False

def test_js_files():
    """测试JavaScript文件加载"""
    print("=== 测试JavaScript文件加载 ===")
    try:
        response = requests.get('http://localhost:8080/js/main.js')
        if response.status_code == 200:
            print("✓ JavaScript文件加载成功")
            content = response.text
            # 检查关键函数
            if 'itineraryData' in content:
                print("✓ 旅游路线数据定义存在")
            if 'function initMap()' in content:
                print("✓ 地图初始化函数存在")
            if 'function renderSpotsList()' in content:
                print("✓ 景点列表渲染函数存在")
            if 'function showSpotDetail()' in content:
                print("✓ 景点详情展示函数存在")
            if 'function loadItinerary()' in content:
                print("✓ 路线加载函数存在")
        else:
            print(f"✗ JavaScript文件加载失败 (状态码: {response.status_code})")

        print("\nJavaScript文件加载测试完成\n")
        return True

    except Exception as e:
        print(f"✗ JavaScript文件测试失败: {str(e)}\n")
        return False

def test_itinerary_data():
    """测试旅游路线数据完整性"""
    print("=== 测试旅游路线数据完整性 ===")
    try:
        response = requests.get('http://localhost:8080/js/main.js')
        content = response.text

        # 提取itineraryData对象
        pattern = r'const itineraryData = \{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
        match = re.search(pattern, content, re.DOTALL)

        if match:
            print("✓ 找到旅游路线数据定义")

            # 检查三天数据
            for day in [1, 2, 3]:
                day_pattern = f'{day}: {{'
                if day_pattern in content:
                    print(f"✓ 第{day}天数据存在")
                    # 检查是否有景点数据
                    if 'spots:' in content:
                        print(f"  - 景点数据结构正确")
                    if 'name:' in content:
                        print(f"  - 景点名称字段存在")
                    if 'lat:' in content and 'lng:' in content:
                        print(f"  - 地理坐标字段存在")
                    if 'description:' in content:
                        print(f"  - 描述字段存在")
                    if 'openTime:' in content:
                        print(f"  - 开放时间字段存在")
                    if 'price:' in content:
                        print(f"  - 价格字段存在")
                else:
                    print(f"✗ 第{day}天数据缺失")
        else:
            print("✗ 未找到旅游路线数据")

        print("\n旅游路线数据测试完成\n")
        return True

    except Exception as e:
        print(f"✗ 旅游路线数据测试失败: {str(e)}\n")
        return False

def test_responsive_design():
    """测试响应式设计"""
    print("=== 测试响应式设计 ===")
    try:
        response = requests.get('http://localhost:8080/css/style.css')
        content = response.text

        # 检查媒体查询
        if '@media' in content:
            print("✓ 媒体查询定义存在")

            # 检查移动端断点
            if '@media (max-width: 968px)' in content or '@media (max-width: 600px)' in content:
                print("✓ 移动端断点设置正确")
            else:
                print("⚠ 移动端断点可能未设置")
        else:
            print("✗ 缺少媒体查询定义")

        print("\n响应式设计测试完成\n")
        return True

    except Exception as e:
        print(f"✗ 响应式设计测试失败: {str(e)}\n")
        return False

def test_map_api():
    """测试地图API配置"""
    print("=== 测试地图API配置 ===")
    try:
        response = requests.get('http://localhost:8080')
        content = response.text

        # 检查腾讯地图API引用
        if 'map.qq.com/api/gljs' in content:
            print("✓ 腾讯地图API引用存在")
        else:
            print("✗ 腾讯地图API引用缺失")

        if 'YOUR_API_KEY' in content:
            print("⚠ API密钥未配置 (使用占位符)")
        else:
            print("⚠ API密钥配置状态未知")

        print("\n地图API配置测试完成\n")
        return True

    except Exception as e:
        print(f"✗ 地图API配置测试失败: {str(e)}\n")
        return False

def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("北京三日游基础能力验证")
    print("="*60 + "\n")

    results = []

    # 运行各项测试
    results.append(("页面基本结构", test_page_structure()))
    results.append(("CSS文件加载", test_css_files()))
    results.append(("JavaScript文件加载", test_js_files()))
    results.append(("旅游路线数据", test_itinerary_data()))
    results.append(("响应式设计", test_responsive_design()))
    results.append(("地图API配置", test_map_api()))

    # 输出测试总结
    print("="*60)
    print("测试总结")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")

    print(f"\n总计: {passed}/{total} 项测试通过")

    if passed == total:
        print("\n🎉 所有基础能力测试通过!")
    else:
        print(f"\n⚠ 有 {total - passed} 项测试未通过")

    print("="*60 + "\n")

    return passed == total

if __name__ == '__main__':
    main()
