import cv2
import time

import keyboard
import numpy as np
from PIL import ImageGrab
from paddleocr import PaddleOCR
import threading


class screenOCR:
    """
    截屏记录工具类，动态传入参数以记录屏幕数据。
    """
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=False)  # 初始化 OCR
        self.special_trigger = False  # 用于标记特殊按键触发
        self.running = True  # 用于控制程序退出
        self.special_data = None  # 用于存储特殊按键触发时的数字

    def grab_frame(self, region):
        """
        截取屏幕的指定区域。
        :param region: 截图区域 (x1, y1, x2, y2)
        :return: 捕获的图像帧（NumPy 格式）。
        """
        screenshot = ImageGrab.grab(bbox=region)
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    def recognize_digits(self, region):
        """
        从屏幕指定区域中识别数字并取整。
        :param region: OCR 识别的区域 (x1, y1, x2, y2)
        :return: 识别到的数字文本（取整后）。
        """
        try:
            screenshot = ImageGrab.grab(bbox=region)
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            results = self.ocr.ocr(frame, cls=False)
            detected_text = ''.join([line[1][0] for line in results[0]])
            return detected_text
        except Exception as e:
            print(f"【ERROR】OCR 识别失败: {str(e)}")
            return 0


    def recognize_digits_point_and_direction(self, region):
        """
        从屏幕指定区域中识别当前坐标和面向角度。
        :param region: 截屏区域
        :return: 当前坐标（整数）和角度（整数）
        """
        try:
            screenshot = ImageGrab.grab(bbox=region)
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            results = self.ocr.ocr(frame, cls=False)
            detected_text = ''.join([line[1][0] for line in results[0]])
            digits = ''.join(filter(str.isdigit, detected_text))
            x = int(digits[:3])
            y = int(digits[3:6])
            angle = int(digits[6:])
            return (x, y), angle
        except Exception as e:
            print(f"【ERROR】OCR 识别失败: {str(e)}")
            return 0, 0


    def handle_keyboard_input(self):
        """
        监听键盘输入。
        """
        while self.running:
            if keyboard.is_pressed("g"):
                print("按下特殊键 g")
                self.special_trigger = True
            if keyboard.is_pressed("q"):
                print("退出程序")
                self.running = False
            time.sleep(0.1)  # 减少 CPU 占用

    def start_recording(self, region, output_file, record_interval):
        """
        开始截屏记录。
        :param region: 截屏区域 (x1, y1, x2, y2)
        :param output_file: 输出文件路径
        :param record_interval: 记录间隔（秒）
        """
        # 启动键盘监听线程
        threading.Thread(target=self.handle_keyboard_input, daemon=True).start()

        try:
            with open(output_file, "w") as file:
                last_record_time = time.time()
                while self.running:
                    start_time = time.time()
                    data = self.recognize_digits(region)

                    # 检测是否触发特殊按键
                    if self.special_trigger:
                        self.special_data = data
                        file.write(f"特殊坐标: {data} | 数字: {self.special_data}\n")
                        file.flush()
                        print(f"记录特殊坐标和数字: 特殊坐标={data}, 数字={self.special_data}")
                        self.special_trigger = False  # 重置触发标记

                    # 定时记录普通数据
                    current_time = time.time()
                    if current_time - last_record_time >= record_interval:
                        last_record_time = current_time
                        file.write(f"{data}\n")
                        file.flush()
                        print(f"记录普通数据: {data}")

                    # 显示捕获的屏幕内容
                    cv2.imshow("Screen Capture", self.grab_frame(region))
                    cv2.waitKey(1)
                    # 控制帧处理间隔
                    elapsed_time = time.time() - start_time
                    time.sleep(max(0, record_interval - elapsed_time))

        except KeyboardInterrupt:
            print("手动中断")
        finally:
            self.running = False  # 确保其他线程停止
            cv2.destroyAllWindows()


if __name__ == "__main__":
    # 设置截屏区域
    region = (1090, 33, 1236, 54)
    output_file = "output.txt"

    # 创建截屏记录工具类实例
    recorder = screenOCR()
    recorder.start_recording(region, output_file=output_file, record_interval=3.0)
