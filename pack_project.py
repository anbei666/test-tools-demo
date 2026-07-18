#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Packaging Script:
Automatically bundle the project into a clean .tar.gz archive,
excluding development artifacts.
"""

import os
import tarfile
import time

# ==========================================
# 1. 基础配置
# ==========================================
PROJECT_NAME = "my-test-platform"
# 使用当前时间戳生成唯一的版本号，防止覆盖之前的包
VERSION = f"1.0.{int(time.time())}"
SOURCE_DIR = "."  # 打包当前目录
OUTPUT_FILENAME = f"{PROJECT_NAME}-{VERSION}.tar.gz"

# ==========================================
# 2. 智能过滤黑名单
# ==========================================


# ==========================================
# 2. 智能过滤黑名单 (精准修正版)
# ==========================================
def should_exclude(filename):
    """
    检查文件或文件夹是否应该被排除在压缩包之外
    """
    exclude_list = [
        ".git",            # Git 历史记录
        ".github",         # CI/CD 工作流配置
        "__pycache__",     # Python 编译缓存
        ".pytest_cache",   # Pytest 运行缓存
        ".ruff_cache",     # Ruff 检查缓存
        "venv",            # 虚拟环境文件夹 (无点)
        ".venv",           # 🌟 关键新增：你的虚拟环境文件夹 (带点)
        "env",             # 常见虚拟环境别名
        ".env",            # 本地环境变量敏感文件
        OUTPUT_FILENAME,   # 排除正在生成的压缩包自身
        "pack_project.py"  # 排除打包脚本自身
    ]
    # 拆分路径，检查是否包含黑名单中的任意项
    path_parts = filename.split(os.sep)
    for exclude in exclude_list:
        if exclude in path_parts:
            return True
    return False

# ==========================================
# 3. 执行打包逻辑
# ==========================================


def main():
    print("📦 开始本地打包流程...")
    print(f"📂 源目录: {os.path.abspath(SOURCE_DIR)}")
    print(f"🎯 目标压缩包: {OUTPUT_FILENAME}\n")

    start_time = time.time()
    file_count = 0

    # 创建并写入 tar.gz 压缩包
    with tarfile.open(OUTPUT_FILENAME, "w:gz") as tar:
        # 递归遍历当前目录
        for root, _dirs, files in os.walk(SOURCE_DIR):
            for file in files:
                # 获取相对路径，用于在压缩包内保持正确的目录结构
                full_path = os.path.relpath(
                    os.path.join(root, file), SOURCE_DIR
                )

                # 过滤黑名单文件
                if should_exclude(full_path):
                    continue

                # 将文件加入压缩包
                tar.add(os.path.join(root, file), arcname=full_path)
                file_count += 1
                print(f"  + 已添加: {full_path}")

    duration = time.time() - start_time
    file_size_mb = os.path.getsize(OUTPUT_FILENAME) / (1024 * 1024)

    print("\n🎉 打包成功!")
    print(
        f"📊 统计数据: 包含 {file_count} 个有效文件 | "
        f"大小: {file_size_mb:.2f} MB | 耗时: {duration:.2f} 秒"
    )
    print(f"📌 压缩包已存放到: {os.path.abspath(OUTPUT_FILENAME)}")


if __name__ == "__main__":
    main()
