import os
import tiktoken
from common.contants import LOGGER


def file_line_size(file_path):
    # 获取文件大小（字节）
    file_size = os.path.getsize(file_path)

    # 获取文件行数
    with open(file_path, 'r', encoding='utf-8') as f:
        line_count = sum(1 for _ in f)

    LOGGER.info(f"文件大小：{file_size} 字节")
    LOGGER.info(f"文件行数：{line_count} 行")

    if line_count < 255:
        return True

    return False


def analyze_md_files(folder_path):
    file_name_list = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.md'):
            file_path = os.path.join(folder_path, filename)

            # 获取文件大小（字节）
            file_size = os.path.getsize(file_path)

            # 计算行数
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            encoding = tiktoken.get_encoding("cl100k_base")
            tokens = encoding.encode(text)
            LOGGER.info(f"文件: {filename}")
            LOGGER.info(f"  大小: {file_size} 字节")
            LOGGER.info(f"  token数: {len(tokens)} ")
            if len(tokens) < 60000:
                file_name_list.append(filename)

    return file_name_list
