import threading
import logging
import time
from PIL import ImageGrab
from mywow.getWowWindow import getWowWindow


class healthMonitorThread(threading.Thread):
    """
    用于监控游戏血量的线程类，支持实时获取血量。
    """
    def __init__(self, window_title="魔兽世界", interval=0.1):

        super().__init__()
        self.window_title = window_title
        # 预设像素位置（相对于窗口的位置）
        self.pixel_positions = [
            (112, 86), (124, 86), (136, 86), (148, 86), (160, 86),
            (172, 86), (184, 86), (196, 86), (208, 86), (220, 86)
        ]

        # 预设初始颜色值
        self.save_colors = [
            (0, 134, 0), (0, 137, 0), (0, 146, 0), (0, 146, 0), (0, 158, 0),
            (0, 177, 0), (0, 184, 0), (0, 187, 0), (0, 190, 0), (0, 190, 0)
        ]

        self.fight_colors = [
            (0, 145, 0), (0, 150, 0), (0, 159, 0), (0, 159, 0), (0, 172, 0),
            (0, 163, 0), (0, 168, 0), (0, 172, 0), (0, 174, 0), (0, 174, 0)
        ]
        self.interval = interval
        self.running = False
        self.blood = 0
        self.lock = threading.Lock()  # 线程安全锁
        self.wow_manager = getWowWindow(window_title=self.window_title)

    def run(self):
        """
        线程运行逻辑。
        """
        logging.info(f"启动血量监控线程：{self.window_title}")
        self.running = True
        while self.running:
            screenshot = self.capture_window()
            if screenshot:
                blood = self.check_health(screenshot)
                # 使用锁更新共享血量值
                with self.lock:
                    self.blood = blood
            time.sleep(self.interval)

    def capture_window(self):
        """
        捕获窗口截图。
        :return: 窗口截图（PIL.Image），如果窗口未找到则返回 None。
        """
        bbox = self.wow_manager.get_window_bbox()
        if bbox:
            return ImageGrab.grab(bbox)
        else:
            logging.warning("无法捕获窗口截图，窗口可能未找到。")
            return None

    def check_health(self, screenshot):
        """
        检查截图中的血量颜色匹配。
        :param screenshot: 窗口的截图。
        :return: 当前血量点数。
        """
        blood = 0
        for i, position in enumerate(self.pixel_positions):
            point_color = screenshot.getpixel(position)
            if point_color == self.save_colors[i] or point_color == self.fight_colors[i]:
                blood += 1
        return blood

    def get_blood(self):
        """
        实时获取当前血量。
        :return: 当前血量值。
        """
        with self.lock:
            return self.blood

    def stop(self):
        """
        停止线程。
        """
        logging.info("停止血量监控线程")
        self.running = False
