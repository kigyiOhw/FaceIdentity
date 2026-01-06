#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Face recognition system - web starter script
"""

import os
import sys
from web_app import app

if __name__ == '__main__':
    print("=" * 50)
    print("人脸识别系统 - 网页版")
    print("=" * 50)
    print("正在启动网页服务器...")
    print("访问地址: http://127.0.0.1:5000")
    print("按 Ctrl+C 停止服务器")
    print("=" * 50)
    
    try:
        app.run(host='127.0.0.1', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动服务器时发生错误: {e}")
        sys.exit(1)
