# targeting.py

import pyautogui

class Targeting:
    def __init__(self, screen_recorder):
        self.screen_recorder = screen_recorder

    def get_target_color(self):
        """获取目标颜色"""
        color = pyautogui.screenshot().getpixel((290, 67))
        return color
