#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本
用于验证基本功能
"""

def quick_test():
    """执行快速测试"""
    print("=== OpenManus 快速测试 ===")
    print(f"测试开始时间: {__import__('datetime').datetime.now()}")

    # 测试 1: 基本算术运算
    result = 2 + 2
    print(f"✓ 测试 1 - 算术运算 (2+2={result}): {'通过' if result == 4 else '失败'}")

    # 测试 2: 字符串操作
    test_str = "Hello, World!"
    print(f"✓ 测试 2 - 字符串长度 ('{test_str}' 长度为 {len(test_str)}): {'通过' if len(test_str) == 13 else '失败'}")

    # 测试 3: 列表操作
    test_list = [1, 2, 3, 4, 5]
    print(f"✓ 测试 3 - 列表求和 (sum({test_list})={sum(test_list)}): {'通过' if sum(test_list) == 15 else '失败'}")

    # 测试 4: 条件判断
    test_bool = True
    print(f"✓ 测试 4 - 条件判断 (not {test_bool} = {not test_bool}): {'通过' if not test_bool == False else '失败'}")

    print(f"测试完成时间: {__import__('datetime').datetime.now()}")
    print("=== 所有测试完成 ===")

if __name__ == "__main__":
    quick_test()
