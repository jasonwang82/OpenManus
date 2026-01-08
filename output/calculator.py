#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的计算器程序
支持加减乘除四则运算
"""


class Calculator:
    """计算器类，提供基本的数学运算功能"""

    @staticmethod
    def add(a, b):
        """加法运算"""
        return a + b

    @staticmethod
    def subtract(a, b):
        """减法运算"""
        return a - b

    @staticmethod
    def multiply(a, b):
        """乘法运算"""
        return a * b

    @staticmethod
    def divide(a, b):
        """除法运算"""
        if b == 0:
            raise ValueError("除数不能为零！")
        return a / b


def get_number(prompt):
    """
    获取用户输入的数字

    Args:
        prompt: 提示信息

    Returns:
        用户输入的数字（浮点数）
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("输入无效，请输入一个数字！")


def get_operator():
    """
    获取用户输入的运算符

    Returns:
        用户选择的运算符 (+, -, *, /)
    """
    while True:
        operator = input("请输入运算符 (+, -, *, /): ").strip()
        if operator in ['+', '-', '*', '/']:
            return operator
        print("无效的运算符！请重新输入。")


def main():
    """主程序"""
    print("=" * 50)
    print("欢迎使用简单计算器")
    print("=" * 50)

    calculator = Calculator()

    while True:
        print("\n" + "=" * 30)
        print("选择操作:")
        print("1. 执行计算")
        print("2. 退出程序")
        print("=" * 30)

        choice = input("请输入选择 (1/2): ").strip()

        if choice == '2':
            print("\n感谢使用计算器，再见！")
            break

        if choice != '1':
            print("无效的选择，请重新输入！")
            continue

        # 获取第一个数字
        num1 = get_number("\n请输入第一个数字: ")

        # 获取运算符
        operator = get_operator()

        # 获取第二个数字
        num2 = get_number("请输入第二个数字: ")

        # 执行计算
        try:
            result = None
            operation = ""

            if operator == '+':
                result = calculator.add(num1, num2)
                operation = "+"
            elif operator == '-':
                result = calculator.subtract(num1, num2)
                operation = "-"
            elif operator == '*':
                result = calculator.multiply(num1, num2)
                operation = "*"
            elif operator == '/':
                result = calculator.divide(num1, num2)
                operation = "/"

            # 显示结果
            print("\n" + "=" * 30)
            print(f"计算结果: {num1} {operation} {num2} = {result}")
            print("=" * 30)

        except ValueError as e:
            print(f"\n错误: {e}")
        except Exception as e:
            print(f"\n发生未知错误: {e}")


if __name__ == "__main__":
    main()
