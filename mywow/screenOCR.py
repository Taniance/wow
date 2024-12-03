import cv2
import numpy as np
from paddleocr import PaddleOCR
from PIL import ImageGrab
import time


class ScreenOCR:
    """
    屏幕 OCR 识别工具，优化版。
    """

    def __init__(self, region, lang='en', use_angle_cls=True, debug=False):
        """
        初始化 ScreenOCR。
        :param region: 屏幕区域 (x1, y1, x2, y2)。
        :param lang: OCR 语言，默认 'en'。
        :param use_angle_cls: 是否启用角度分类器（有助于识别旋转的文字）。
        :param debug: 是否开启调试模式。
        """
        self.region = region  # 截取屏幕的区域
        self.ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang)  # 初始化 OCR
        self.debug = debug  # 开启调试模式
        self.retry_limit = 3  # OCR失败后的重试次数

    def recognize_digits(self):
        """
        从屏幕指定区域中识别数字并取整。
        :return: 识别到的数字文本（取整后）。
        """
        try:
            # 捕获屏幕区域
            screenshot = ImageGrab.grab(bbox=self.region)
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            if self.debug:
                print(f"【DEBUG】捕获图像尺寸: {frame.shape}")
                cv2.imwrite("temp_screen_debug.jpg", frame)

            # OCR 识别
            results = self.ocr.ocr(frame, cls=False)

            if not results:
                print("【ERROR】OCR识别结果为空，尝试重新识别")
                return (0, 0), 0  # 返回默认值

            # 提取识别的文本并尝试将其转换为整数
            detected_text = ''.join([line[1][0] for line in results[0]])
            if self.debug:
                print(f"【DEBUG】OCR 识别结果: {detected_text}")

            # 提取其中的数字并取整（如果不是数字则跳过）
            cleaned = ''.join(filter(str.isdigit, detected_text))  # 只保留数字部分

            if len(cleaned) < 9:
                print(f"【ERROR】OCR识别结果不完整：{cleaned}")
                return (0, 0), 0  # 返回默认值

            # 假设坐标是前三个数字和后四个数字
            x = int(cleaned[:3])
            y = int(cleaned[3:6])
            angle = int(cleaned[6:])

            if self.debug:
                print(f"【DEBUG】去符号后的结果: {x}:{y}={angle}")

            return (x, y), angle

        except Exception as e:
            print(f"【ERROR】OCR 识别失败: {str(e)}")
            return (0, 0), 0

    def capture_screen(self):
        """
        捕获指定区域的屏幕，并返回图像。
        """
        try:
            screenshot = ImageGrab.grab(bbox=self.region)
            frame = np.array(screenshot)
            return frame
        except Exception as e:
            print(f"【ERROR】屏幕捕获失败: {str(e)}")
            return None

    def retry_recognition(self, retries=3):
        """
        如果OCR识别失败，进行重试。
        :param retries: 最大重试次数。
        :return: 识别结果。
        """
        for attempt in range(retries):
            result = self.recognize_digits()
            if result != ((0, 0), 0):  # 正确的语法
                return result

            print(f"【INFO】第{attempt + 1}次尝试OCR识别失败，重试中...")
            time.sleep(1)  # 等待1秒后重试
        print("【ERROR】所有重试失败，返回默认值")
        return (0, 0), 0
