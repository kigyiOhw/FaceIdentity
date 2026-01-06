#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人脸识别系统 - 桌面版启动脚本
"""

import sys
import os

def main():
    print("=" * 50)
    print("人脸识别系统 - 桌面版")
    print("=" * 50)
    print("正在启动桌面应用程序...")
    print("=" * 50)
    
    try:
        from desktop_app import main as desktop_main
        desktop_main()
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保已安装所有依赖包")
        sys.exit(1)
    except Exception as e:
        print(f"启动应用程序时发生错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
