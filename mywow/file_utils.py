import os


def read_file(file_path):
    """
    从文件中读取内容并将每一行转换为整数数组。
    :param file_path: 文件路径。
    :return: 数字列表。
    """
    try:
        with open(file_path, "r") as file:
            return [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
        return []
    except ValueError as e:
        print(f"数据解析错误: {e}")
        return []

def read_points_from_file(file_path):
    """
    从 TXT 文件中读取每行的前 6 位，解析为 (X, Y) 坐标点。
    :param file_path: TXT 文件路径。
    :return: 坐标点列表，每个点为 (X, Y)。
    """
    points = []  # 用于存储坐标点

    try:
        with open(file_path, "r") as file:
            for line in file:
                # 取每行的前 6 位，确保长度足够
                if len(line) >= 6:
                    x = int(line[:3])  # 前三位为 X 坐标
                    y = int(line[3:6])  # 后三位为 Y 坐标
                    points.append((x, y))  # 添加到列表
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except ValueError as e:
        print(f"解析坐标时出错: {e}")

    return points

def write_file(file_path, content, mode='w', encoding='utf-8'):
    """
    写入内容到文件。

    参数:
        file_path (str): 文件路径
        content (str): 要写入的内容
        mode (str): 写入模式 ('w' 为覆盖, 'a' 为追加)，默认为 'w'
        encoding (str): 文件编码，默认为 'utf-8'

    返回:
        bool: 写入是否成功

    异常:
        IOError: 如果写入过程中发生错误
    """
    try:
        # 如果文件的目录不存在，先创建目录
        dir_name = os.path.dirname(file_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # 写入文件
        with open(file_path, mode, encoding=encoding) as file:
            print(f"写入文件 写进去的是个什么东西啊？ : {content}")
            file.write(str(content))
            file.flush()
            return True
    except IOError as e:
        print(f"[错误] 写入文件失败: {file_path}, 错误信息: {e}")
        return False