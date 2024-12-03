import pygetwindow as gw
import win32gui
import win32con


class GetWowWindow:
    """
    用于操作 WOW 窗口的类。
    """

    def __init__(self, window_title="魔兽世界"):
        """
        初始化 GetWOW 类。
        :param window_title: 窗口标题，用于匹配 WOW 的窗口。
        """
        self.window_title = window_title
        self.hwnd = None

    def find_wow_window(self):
        """
        查找指定标题的 WOW 窗口。
        :return: 窗口句柄，如果未找到返回 None。
        """
        windows = gw.getWindowsWithTitle(self.window_title)
        if windows:
            self.hwnd = windows[0]._hWnd  # 获取第一个匹配窗口的句柄
            print(f"找到窗口：{self.window_title}")
        else:
            print(f"未找到窗口：{self.window_title}")
            self.hwnd = None
        return self.hwnd

    def set_wow_window(self, width=1280, height=960, x=0, y=0):
        """
        设置窗口的位置和大小。
        :param width: 窗口宽度，默认 1280。
        :param height: 窗口高度，默认 960。
        :param x: 窗口的左上角 X 坐标，默认 0。
        :param y: 窗口的左上角 Y 坐标，默认 0。
        """
        if self.hwnd is None:
            self.find_wow_window()

        if self.hwnd:
            # 设置窗口大小和位置
            win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOP, x, y, width, height, win32con.SWP_SHOWWINDOW)
            print(f"已设置 {self.window_title} 窗口到 ({x}, {y}), 大小为 {width}x{height}")
        else:
            print(f"无法设置窗口：{self.window_title} 未找到。")

    def get_window_bbox(self):
        """
        获取窗口的边界。
        :return: 返回窗口的 (left, top, right, bottom)，如果未找到窗口返回 None。
        """
        if self.hwnd is None:
            self.find_wow_window()

        if self.hwnd:
            rect = win32gui.GetWindowRect(self.hwnd)
            return rect
        else:
            print(f"无法获取窗口边界：{self.window_title} 未找到。")
            return None
