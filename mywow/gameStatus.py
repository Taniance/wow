import pyautogui
from paddleocr import PaddleOCR
from PIL import ImageGrab
import time

from pynput.keyboard import Controller

from mywow.screenOCR import screenOCR


class GameStatus:
    def __init__(self, region, lang='en'):
        """
        初始化 GameStatus。
        :param region: 截取的屏幕区域 (x1, y1, x2, y2)。
        :param lang: OCR 语言，默认 'en'。
        """
        self.region = region  # 截取屏幕的区域
        self.ocr = PaddleOCR(use_angle_cls=False, lang=lang)  # 初始化 OCR工具
        self.bag_region = (300, 50, 400, 150)    # 背包区域的假设位置

    def checkbag():
        keyboard = Controller()
        recorder = screenOCR()
        region_bag = (825, 817, 876, 844)
        current = 0
        text = recorder.recognize_digits(region_bag)
        # 如果未识别到文本，尝试按下键盘触发操作
        if not text:
            keyboard.press('b')
            time.sleep(0.1)
            keyboard.release('b')
            text = recorder.recognize_digits(region_bag)
        if text:
            print(f"文本内容: {text}")
            try:
                # 计算背包空余
                current = int(text.split('/')[0])
                print(f"背包还空着呢，空多少？ {current}")
            except ValueError:
                print("解析文本时出错，文本可能不符合格式 '数字/数字'")
            except IndexError:
                print("分割文本时出错，检查 OCR 返回的文本格式")
        else:
            print("未识别到有效文本")
        return current

    def get_fight_status(self):
        """
        获取人物是否在战斗状态。
        :return: 是否在战斗状态。
        """
        screenshot = ImageGrab.grab(bbox=self.fight_region)
        pixel = screenshot.getpixel((50, 50))  # 假设战斗状态图标在该位置
        # 假设战斗时状态图标是红色
        if pixel == (255, 0, 0):
            return True
        else:
            return False

    def query_game_status(self):
        """
        查询人物的血量、背包、战斗状态。
        :return: (blood_percentage, is_bag_full, is_in_fight)
        """
        blood = self.get_blood()
        is_bag_full = self.get_bag_status()
        is_in_fight = self.get_fight_status()

        return blood, is_bag_full, is_in_fight


# 使用示例
if __name__ == "__main__":
    game_status = GameStatus(region=(0, 0, 1280, 960))  # 定义屏幕区域
    blood, is_bag_full, is_in_fight = game_status.query_game_status()

    print(f"当前血量: {blood}%")
    print(f"背包是否满: {'是' if is_bag_full else '否'}")
    print(f"是否在战斗中: {'是' if is_in_fight else '否'}")
