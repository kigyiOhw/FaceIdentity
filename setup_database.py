#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database initialization script
"""

import mysql.connector
from mysql.connector import Error
from config import DATABASE_CONFIG

def create_database():
    """Create database and tables"""
    try:
        # Connect to MySQL server (without specifying a database)
        connection = mysql.connector.connect(
            host=DATABASE_CONFIG['host'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            charset=DATABASE_CONFIG['charset']
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_CONFIG['database']}")
            print(f"数据库 {DATABASE_CONFIG['database']} 创建成功")
            
            # Use the database
            cursor.execute(f"USE {DATABASE_CONFIG['database']}")
            
            # Create persons table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS persons (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INT,
                    gender VARCHAR(10),
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            print("Persons table created successfully")
            
            # Create face encodings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS face_encodings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    person_id INT NOT NULL,
                    face_encoding BLOB NOT NULL,
                    image_path VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE
                )
            """)
            print("Face encodings table created successfully")
            
            # Create recognition logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recognition_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    person_id INT,
                    confidence FLOAT,
                    image_path VARCHAR(500),
                    recognition_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE SET NULL
                )
            """)
            print("Recognition logs table created successfully")
            
            cursor.close()
            connection.close()
            print("Database initialization complete!")
            
    except Error as e:
        print(f"Database initialization failed: {e}")
        return False
    
    return True

def test_connection():
    """Test database connection"""
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        if connection.is_connected():
            print("Database connection test successful!")
            connection.close()
            return True
    except Error as e:
        print(f"Database connection test failed: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("人脸识别系统 - 数据库初始化")
    print("=" * 50)
    
    # Test connection
    if test_connection():
        print("Database connection OK, starting initialization...")
        if create_database():
            print("Database initialized successfully!")
        else:
            print("Database initialization failed!")
    else:
        print("Please check database configuration and MySQL service status")
        print("Config file: config.py")
        print("Ensure MySQL service is running")
