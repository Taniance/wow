# movement.py

import time
from pynput.keyboard import Controller
import math

class Movement:
    def __init__(self, points, region, keyboard_controller, screen_recorder):
        self.points = points  # 目标点列表
        self.region = region  # 截屏区域
        self.keyboard = keyboard_controller
        self.screen_recorder = screen_recorder
        self.current_index = 0  # 当前目标点的索引

    def calculate_speed(self, start_point, end_point, time_diff):
        """计算人物行走速度"""
        delta_x = end_point[0] - start_point[0]
        delta_y = end_point[1] - start_point[1]
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        if time_diff == 0:
            return 0
        return distance / time_diff

    def walk_smoothly(self):
        """实现平滑行走逻辑"""
        wait_time_too_long = time.time()
        wait_time_distance = 0
        self.keyboard.press('e')  # 按住 E 键开始移动
        try:
            while self.current_index < len(self.points):
                target_point = self.points[self.current_index]
                current_point, angle = self.screen_recorder.recognize_digits_point_and_direction(self.region)

                if current_point == 0:
                    print("[警告] 无法获取当前坐标，跳过循环")
                    continue

                distance, target_angle = self.calculate_distance_and_angle(current_point, target_point)
                if time.time() - wait_time_too_long > 5 and distance == wait_time_distance:
                    print("[警告] 检测到人物卡住，尝试调整方向")
                    self.keyboard.press('space')
                    time.sleep(0.1)
                    self.keyboard.release('space')
                    time.sleep(1)
                    wait_time_too_long = time.time()
                    wait_time_distance = distance

                # 动态调整方向
                if distance > 3:
                    self.adjust_direction(distance, angle, target_angle)
                else:
                    self.current_index += 1
                    self.keyboard.release('e')
                    self.keyboard.press('e')

            print("[完成] 已到达所有目标点")
        finally:
            self.keyboard.release('e')  # 释放前进键

    def adjust_direction(self, distance, current_angle, target_angle):
        """动态调整方向"""
        if distance > 3:
            angle_diff = self.calculate_angle_difference(current_angle, target_angle)
            if abs(angle_diff) > 1:
                self.option_direction(angle_diff)

    def calculate_distance_and_angle(self, current_point, target_point):
        """计算距离和角度"""
        # 这里你可以继续使用你原有的 `calculate_distance_and_angle` 逻辑
        pass

    def calculate_angle_difference(self, current_angle, target_angle):
        """计算角度差异"""
        return (target_angle - current_angle + 180) % 360 - 180

    def option_direction(self, angle_diff):
        """调整方向"""
        # 这里是你自己的选项方向调整逻辑
        pass
