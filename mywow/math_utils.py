import math
import pyautogui


def calculate_distance_and_angle(point1, point2):
    """
    计算坐标2相对于坐标1的距离和角度。

    参数：
    - x1, y1: 坐标1的X和Y坐标
    - x2, y2: 坐标2的X和Y坐标

    返回：
    - distance: 坐标1和坐标2之间的距离，保留两位小数
    - angle: 坐标2相对于坐标1的角度（以正北为0度，逆时针方向），保留两位小数
    """
    # 计算ΔX和ΔY
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]

    # 计算距离
    distance = math.hypot(delta_x, delta_y)
    distance = round(distance, 2)

    # 正确计算角度
    theta_rad = math.atan2(-delta_x, -delta_y)  # 注意这里取 -delta_x 和 -delta_y
    theta_deg = math.degrees(theta_rad)

    # 将角度调整到[0°, 360°)范围内
    if theta_deg < 0:
        theta_deg += 360
    angle = round(theta_deg, 2)

    return distance, angle

def calculate_angle_difference(a1, a2):
    """
    计算两个角度之间的最小差值（-180° ~ +180°）。
    :param a1: 第一个角度
    :param a2: 第二个角度
    :return: 最小的角度差，带正负值，保留两位小数
    """
    diff = (a1 - a2 + 180) % 360 - 180
    diff = diff if diff != -180 else 180  # 确保差值为对称的最小正值
    return round(diff, 2)  # 保留两位小数

