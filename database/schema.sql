-- 人脸识别数据库表结构
CREATE DATABASE IF NOT EXISTS face_recognition_db;
USE face_recognition_db;

-- 人员信息表
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
);

-- 人脸特征表
CREATE TABLE IF NOT EXISTS face_encodings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT NOT NULL,
    face_encoding BLOB NOT NULL,
    image_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE
);

-- 识别记录表
CREATE TABLE IF NOT EXISTS recognition_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT,
    confidence FLOAT,
    image_path VARCHAR(500),
    recognition_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE SET NULL
);