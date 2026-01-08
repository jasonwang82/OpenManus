#!/usr/bin/env python3
"""
验证北京三日游基础能力的测试脚本
"""

import asyncio
from playwright.async_api import async_playwright
import json


async def test_beijing_trip():
    """测试北京三日游的所有功能"""
    print("=" * 80)
    print("开始验证北京三日游基础能力")
    print("=" * 80)

    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()

        try:
            # 1. 访问页面
            print("\n[1/8] 正在访问页面...")
            await page.goto('http://localhost:8000/index.html')
            await page.wait_for_load_state('networkidle')

            # 检查页面标题
            title = await page.title()
            print(f"✓ 页面标题: {title}")
            assert "北京" in title and "旅游" in title, "页面标题不正确"

            # 检查主标题
            h1 = await page.text_content('.title')
            print(f"✓ 主标题: {h1}")
            assert "北京三日旅游指南" in h1, "主标题不正确"

            # 2. 验证三天路线按钮存在
            print("\n[2/8] 验证三天路线按钮...")
            buttons = await page.query_selector_all('.day-btn')
            print(f"✓ 找到 {len(buttons)} 个天按钮")
            assert len(buttons) == 3, "应该有3个天按钮"

            button_texts = [await btn.text_content() for btn in buttons]
            print(f"✓ 按钮文本: {button_texts}")
            assert "第一天" in button_texts[0], "第一个按钮文本不正确"
            assert "第二天" in button_texts[1], "第二个按钮文本不正确"
            assert "第三天" in button_texts[2], "第三个按钮文本不正确"

            # 3. 验证第一天景点列表
            print("\n[3/8] 验证第一天景点列表...")
            spots = await page.query_selector_all('.spot-item')
            print(f"✓ 找到 {len(spots)} 个景点")

            # 获取景点名称
            spot_names = []
            for spot in spots:
                name = await spot.query_selector('.spot-name')
                if name:
                    text = await name.text_content()
                    spot_names.append(text.strip())
            print(f"✓ 景点列表: {spot_names}")

            # 验证第一天的景点
            expected_day1 = ["天安门广场", "故宫博物院", "景山公园"]
            for expected in expected_day1:
                found = any(expected in name for name in spot_names)
                print(f"  {'✓' if found else '✗'} {expected}")
                assert found, f"未找到景点: {expected}"

            # 4. 测试点击第一个景点
            print("\n[4/8] 测试点击第一个景点...")
            first_spot = spots[0]
            await first_spot.click()
            await page.wait_for_timeout(1000)

            # 验证详情弹窗出现
            detail_section = await page.query_selector('#detailSection')
            detail_visible = await detail_section.is_visible() if detail_section else False
            print(f"✓ 详情弹窗显示: {detail_visible}")
            assert detail_visible, "点击景点后详情弹窗未显示"

            # 验证详情内容
            detail_title = await page.text_content('#detailTitle')
            print(f"✓ 详情标题: {detail_title}")
            assert detail_title, "详情标题为空"

            detail_desc = await page.text_content('#detailDescription')
            print(f"✓ 详情描述: {detail_desc[:50]}...")  # 只显示前50个字符
            assert detail_desc, "详情描述为空"

            # 验证元数据
            open_time = await page.text_content('#detailOpenTime')
            price = await page.text_content('#detailPrice')
            duration = await page.text_content('#detailDuration')
            print(f"✓ 开放时间: {open_time}")
            print(f"✓ 门票价格: {price}")
            print(f"✓ 游览时长: {duration}")

            # 5. 测试关闭详情弹窗
            print("\n[5/8] 测试关闭详情弹窗...")
            close_btn = await page.query_selector('#closeDetail')
            await close_btn.click()
            await page.wait_for_timeout(500)

            detail_visible = await detail_section.is_visible()
            print(f"✓ 详情弹窗已关闭: {not detail_visible}")
            assert not detail_visible, "详情弹窗未能正确关闭"

            # 6. 测试切换到第二天
            print("\n[6/8] 测试切换到第二天...")
            day2_button = buttons[1]
            await day2_button.click()
            await page.wait_for_timeout(1000)

            # 获取第二天的景点
            spots_day2 = await page.query_selector_all('.spot-item')
            print(f"✓ 第二天景点数量: {len(spots_day2)}")

            # 获取第二天景点名称
            spot_names_day2 = []
            for spot in spots_day2:
                name = await spot.query_selector('.spot-name')
                if name:
                    text = await name.text_content()
                    spot_names_day2.append(text.strip())
            print(f"✓ 第二天景点列表: {spot_names_day2}")

            # 验证第二天的景点
            expected_day2 = ["八达岭长城", "慕田峪长城", "明十三陵"]
            for expected in expected_day2:
                found = any(expected in name for name in spot_names_day2)
                print(f"  {'✓' if found else '✗'} {expected}")
                assert found, f"未找到第二天景点: {expected}"

            # 7. 测试切换到第三天
            print("\n[7/8] 测试切换到第三天...")
            day3_button = buttons[2]
            await day3_button.click()
            await page.wait_for_timeout(1000)

            # 获取第三天的景点
            spots_day3 = await page.query_selector_all('.spot-item')
            print(f"✓ 第三天景点数量: {len(spots_day3)}")

            # 获取第三天景点名称
            spot_names_day3 = []
            for spot in spots_day3:
                name = await spot.query_selector('.spot-name')
                if name:
                    text = await name.text_content()
                    spot_names_day3.append(text.strip())
            print(f"✓ 第三天景点列表: {spot_names_day3}")

            # 验证第三天的景点
            expected_day3 = ["颐和园", "圆明园", "天坛"]
            for expected in expected_day3:
                found = any(expected in name for name in spot_names_day3)
                print(f"  {'✓' if found else '✗'} {expected}")
                assert found, f"未找到第三天景点: {expected}"

            # 8. 测试第三天点击景点
            print("\n[8/8] 测试第三天景点详情...")
            third_day_spot = spots_day3[0]
            await third_day_spot.click()
            await page.wait_for_timeout(1000)

            detail_title_day3 = await page.text_content('#detailTitle')
            print(f"✓ 第三天详情标题: {detail_title_day3}")
            assert detail_title_day3, "第三天详情标题为空"

            # 验证页面结构
            print("\n" + "=" * 80)
            print("✅ 所有测试通过！")
            print("=" * 80)

            # 生成测试报告
            report = {
                "status": "success",
                "tests": [
                    {"name": "页面加载", "status": "passed"},
                    {"name": "三天路线按钮", "status": "passed"},
                    {"name": "第一天景点", "status": "passed", "count": len(spots)},
                    {"name": "景点详情显示", "status": "passed"},
                    {"name": "关闭详情弹窗", "status": "passed"},
                    {"name": "第二天切换", "status": "passed", "count": len(spots_day2)},
                    {"name": "第三天切换", "status": "passed", "count": len(spots_day3)},
                    {"name": "详情内容验证", "status": "passed"}
                ],
                "summary": {
                    "total": 8,
                    "passed": 8,
                    "failed": 0
                }
            }

            # 截图保存
            screenshot_path = "/Users/jasonwang/workspace/OpenManus/output/test_screenshot.png"
            await page.screenshot(path=screenshot_path)
            print(f"\n📸 截图已保存: {screenshot_path}")

            return report

        except AssertionError as e:
            print(f"\n❌ 测试失败: {e}")
            raise
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            import traceback
            traceback.print_exc()
            raise
        finally:
            # 保持浏览器打开5秒以便观察
            print("\n浏览器将保持5秒以便观察...")
            await page.wait_for_timeout(5000)
            await browser.close()


async def main():
    """主函数"""
    try:
        report = await test_beijing_trip()

        # 保存测试报告
        report_path = "/Users/jasonwang/workspace/OpenManus/output/test_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📋 测试报告已保存: {report_path}")

    except Exception as e:
        print(f"\n❌ 测试过程出现异常: {e}")


if __name__ == "__main__":
    asyncio.run(main())
