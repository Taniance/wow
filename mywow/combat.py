# combat.py

import time
from pynput.keyboard import Controller, Key
import pyautogui

class Combat:
    def __init__(self, keyboard_controller, screen_recorder):
        self.keyboard = keyboard_controller
        self.screen_recorder = screen_recorder

    def detect_monster(self):
        """检测是否有怪物"""
        self.keyboard.press(Key.tab)
        time.sleep(0.01)
        self.keyboard.release(Key.tab)
        time.sleep(0.5)

        color = pyautogui.screenshot().getpixel((290, 67))
        if color == (201, 199, 0):  # 黄色表示怪物存在
            return True
        return False

    def fight(self):
        """战斗逻辑"""
        print("[战斗] 开始战斗")
        self.keyboard.release('e')  # 停止移动
        self.attack_monster()

    def attack_monster(self):
        """攻击怪物逻辑"""
        while True:
            no_blood = pyautogui.screenshot().getpixel((287, 85))
            if no_blood != (0, 160, 0):  # 目标死亡
                print("目标已死亡")
                break
            self.keyboard.press('2')
            time.sleep(0.01)
            self.keyboard.release('2')
            time.sleep(0.5)
            self.keyboard.press('3')
            time.sleep(0.01)
            self.keyboard.release('3')
            time.sleep(0.5)
            self.keyboard.press('g')
            time.sleep(0.01)
            self.keyboard.release('g')
