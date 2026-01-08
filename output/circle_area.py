"""
计算圆面积的模块

该模块提供了一个计算圆面积的函数，使用数学公式：面积 = π × 半径²
"""

import math


def circle_area(radius):
    """
    计算圆的面积

    参数:
        radius (float): 圆的半径，必须是非负数

    返回:
        float: 圆的面积

    异常:
        ValueError: 当半径为负数时抛出
        TypeError: 当半径不是数字时抛出

    示例:
        >>> circle_area(5)
        78.53981633974483
        >>> circle_area(0)
        0.0
    """
    # 验证输入类型
    if not isinstance(radius, (int, float)):
        raise TypeError("半径必须是数字类型")

    # 验证半径值
    if radius < 0:
        raise ValueError("半径不能为负数")

    # 计算圆的面积
    area = math.pi * radius ** 2

    return area


def main():
    """
    主函数，用于演示circle_area函数的使用
    """
    # 示例：计算不同半径的圆面积
    test_radii = [0, 1, 2, 5, 10]

    print("圆面积计算器")
    print("=" * 40)

    for radius in test_radii:
        area = circle_area(radius)
        print(f"半径: {radius:4d} -> 面积: {area:10.2f}")

    # 示例：用户交互式计算
    print("\n" + "=" * 40)
    print("您可以输入半径来计算圆的面积（输入q退出）")

    while True:
        user_input = input("\n请输入圆的半径: ")

        if user_input.lower() == 'q':
            print("感谢使用！")
            break

        try:
            radius = float(user_input)
            area = circle_area(radius)
            print(f"半径为 {radius} 的圆面积是: {area:.4f}")
        except ValueError as e:
            print(f"错误: {e}")
        except TypeError as e:
            print(f"错误: {e}")


if __name__ == "__main__":
    main()
