import time

from PIL import ImageGrab
import cv2
import numpy as np
from pynput.keyboard import Controller
from paddleocr import PaddleOCR

from mywow.screenOCR import screenOCR


def find_image_in_region(region, small_image_path, threshold=0.8):
    """
    在指定屏幕区域内查找小图。

    参数:
        region (tuple): 截屏区域 (x1, y1, x2, y2)。
        small_image_path (str): 小图的文件路径。
        threshold (float): 匹配的相似度阈值，默认为0.8。

    返回:
        bool: 是否找到匹配。
        list: 匹配位置的左上角坐标列表 [(x1, y1), (x2, y2), ...]。
    """
    # 截取屏幕指定区域
    screenshot = ImageGrab.grab(bbox=region)

    # 将 PIL 图像转换为 OpenCV 格式
    large_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 读取小图
    small_image = cv2.imread(small_image_path)

    # 检查图像是否加载成功
    if large_image is None or small_image is None:
        raise ValueError("加载图像失败，请检查路径或截图区域")

    # 转为灰度图（模板匹配需要灰度图）
    large_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
    small_gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)

    # 模板匹配
    result = cv2.matchTemplate(large_gray, small_gray, cv2.TM_CCOEFF_NORMED)

    # 获取匹配位置
    locations = np.where(result >= threshold)

    # 获取小图的宽度和高度
    h, w = small_gray.shape

    # 保存匹配位置
    match_points = []
    for pt in zip(*locations[::-1]):  # 转换为 (x, y)
        match_points.append(pt)

    # 返回是否找到匹配以及匹配位置
    return len(match_points) > 0, match_points


if __name__ == "__main__":
    keyboard = Controller()
    recorder = screenOCR()
    region_bag = (825, 817, 876, 844)
    # region_blood = (105, 79, 228, 91)
    current = 0
    while True:
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

    #    write_file("images\\die_point.txt", 5678910)

