# main.py

from walksmoothfight import Walksmoothfight

def main():
    points = [(100, 200), (300, 400), (500, 600)]  # 示例目标点
    region = (1090, 33, 1266, 54)  # 截图区域
    walksmoothfight = Walksmoothfight(points, region)
    walksmoothfight.execute()

if __name__ == "__main__":
    main()
