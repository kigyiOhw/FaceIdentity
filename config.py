# 配置文件
import os

# 数据库配置
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # 请修改为您的MySQL密码
    'database': 'face_recognition_db',
    'charset': 'utf8mb4'
}

# 文件路径配置
UPLOAD_FOLDER = 'uploads'
KNOWN_FACES_FOLDER = 'known_faces'
TEMP_FOLDER = 'temp'

# 创建必要的文件夹
for folder in [UPLOAD_FOLDER, KNOWN_FACES_FOLDER, TEMP_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# 人脸识别配置
FACE_RECOGNITION_CONFIG = {
    'tolerance': 0.6,  # 人脸识别容差
    'model': 'hog',    # 使用hog模型（更快）或cnn模型（更准确）
    'upsample': 1      # 图像上采样次数
}

# Flask配置
FLASK_CONFIG = {
    'host': '127.0.0.1',
    'port': 5000,
    'debug': True
}