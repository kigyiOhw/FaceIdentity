#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Face recognition system - quick install script
"""

import os
import sys
import subprocess
import mysql.connector
from mysql.connector import Error

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 7):
        print("错误: 需要Python 3.7或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✓ Python版本检查通过: {sys.version}")
    return True

def install_requirements():
    """Install required packages"""
    print("正在安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 依赖包安装失败: {e}")
        return False

def check_mysql_connection():
    """Check MySQL connection"""
    print("检查MySQL连接...")
    try:
        from config import DATABASE_CONFIG
        
        # Try to connect to MySQL server
        connection = mysql.connector.connect(
            host=DATABASE_CONFIG['host'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            charset=DATABASE_CONFIG['charset']
        )
        
        if connection.is_connected():
            print("✓ MySQL连接成功")
            connection.close()
            return True
    except Error as e:
        print(f"✗ MySQL连接失败: {e}")
        print("请检查:")
        print("1. MySQL服务是否启动")
        print("2. 数据库配置是否正确 (config.py)")
        print("3. 用户名和密码是否正确")
        return False

def create_directories():
    """Create required directories"""
    directories = ['uploads', 'known_faces', 'temp']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ 创建目录: {directory}")

def main():
    """Main installation flow"""
    print("=" * 60)
    print("人脸识别系统 - 安装程序")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("请手动运行: pip install -r requirements.txt")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Check MySQL connection
    if not check_mysql_connection():
        print("\n请先配置MySQL数据库:")
        print("1. 启动MySQL服务")
        print("2. 修改 config.py 中的数据库配置")
        print("3. 运行 python setup_database.py 初始化数据库")
        sys.exit(1)
    
    # Initialize database
    print("\n正在初始化数据库...")
    try:
        from setup_database import create_database
        if create_database():
            print("✓ 数据库初始化完成")
        else:
            print("✗ 数据库初始化失败")
            sys.exit(1)
    except Exception as e:
        print(f"✗ 数据库初始化错误: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("安装完成！")
    print("=" * 60)
    print("启动方式:")
    print("网页版: python start_web.py")
    print("桌面版: python start_desktop.py")
    print("=" * 60)

if __name__ == '__main__':
    main()

