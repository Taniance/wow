import time

import pyautogui

from mywow.healthMonitorThread import healthMonitorThread

if __name__ == '__main__':
    color = pyautogui.screenshot().getpixel((287, 67))
    print(f"目标颜色检测 color = {color}")

    """
    health_monitor = healthMonitorThread(
        window_title="魔兽世界",
        interval=0.1
    )
    # 启动线程
    health_monitor.start()
    # 给线程一些时间来开始监控并更新血量
    time.sleep(1)
    # 循环读取血量
    try:
        while True:
            current_blood = health_monitor.get_blood()
            print(f"实时血量：{current_blood}")
            time.sleep(0.5)  # 每隔0.5秒更新一次
    except KeyboardInterrupt:
        print("程序终止...")
        health_monitor.stop()
        health_monitor.join()  # 等待线程安全结束
    """