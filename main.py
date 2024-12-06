# main.py
import time

from mywow.getWowWindow import getWowWindow
from mywow.healthMonitorThread import healthMonitorThread
from mywow.screenOCR import screenOCR

def main():
    wow_manager = getWowWindow("魔兽世界")
    wow_manager.set_wow_window()
    health_monitor = healthMonitorThread(
        window_title="魔兽世界",
        interval=0.1
    )
    # 启动线程
    health_monitor.start()
    # 给线程一些时间来开始监控并更新血量
    current_blood = health_monitor.get_blood()
    print(f"实时血量：{current_blood}")
    region_bag = (825, 817, 876, 844)
    screen = screenOCR()
    text = screen.recognize_digits(region_bag)
    print(f"实时背包：{text}")


if __name__ == "__main__":
    # main()



