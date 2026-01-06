# 人脸识别系统

一个基于Python的人脸识别系统，支持网页端和Windows桌面端，使用MySQL数据库存储人员信息。

## 功能特性

- 🎭 **人脸识别**: 自动检测和识别人脸
- 👤 **人员管理**: 添加、编辑、删除人员信息
- 📊 **数据存储**: 使用MySQL数据库存储人员信息和识别记录
- 🌐 **网页界面**: 现代化的Web界面，支持拖拽上传
- 🖥️ **桌面程序**: Windows桌面应用程序
- 📝 **识别记录**: 查看历史识别记录
- 🔍 **未知人脸**: 对未识别的人脸可以手动添加信息

## 系统要求

- Python 3.7+
- MySQL 5.7+
- Windows 10/11 (桌面版)

## 安装步骤

### 1. 克隆项目
```bash
git clone <repository-url>
cd face-data
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置数据库

1. 安装并启动MySQL服务
2. 创建数据库：
```sql
CREATE DATABASE face_recognition_db;
```
3. 导入数据库结构：
```bash
mysql -u root -p face_recognition_db < database/schema.sql
```

### 4. 配置数据库连接

编辑 `config.py` 文件，修改数据库配置：
```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # 修改为您的MySQL密码
    'database': 'face_recognition_db',
    'charset': 'utf8mb4'
}
```

## 使用方法

### 网页版

1. 启动网页服务器：
```bash
python start_web.py
```

2. 打开浏览器访问：http://127.0.0.1:5000

3. 功能说明：
   - **人脸识别**: 上传图片进行人脸识别
   - **添加人员**: 上传图片并填写人员信息
   - **识别记录**: 查看历史识别记录

### 桌面版

1. 启动桌面应用程序：
```bash
python start_desktop.py
```

2. 功能说明：
   - 选择图片进行人脸识别
   - 添加新人员到数据库
   - 查看识别记录
   - 管理人员信息

## 项目结构

```
face-data/
├── config.py                 # 配置文件
├── requirements.txt          # 依赖包列表
├── start_web.py             # 网页版启动脚本
├── start_desktop.py         # 桌面版启动脚本
├── web_app.py               # Flask网页应用
├── desktop_app.py           # 桌面应用程序
├── database/
│   ├── schema.sql           # 数据库结构
│   └── db_manager.py        # 数据库操作
├── face_recognition/
│   └── face_detector.py     # 人脸识别核心
├── templates/
│   └── index.html           # 网页模板
├── uploads/                 # 上传文件目录
├── known_faces/             # 已知人脸目录
└── temp/                    # 临时文件目录
```

## 数据库表结构

### persons (人员信息表)
- id: 主键
- name: 姓名
- age: 年龄
- gender: 性别
- phone: 电话
- email: 邮箱
- address: 地址
- created_at: 创建时间
- updated_at: 更新时间

### face_encodings (人脸特征表)
- id: 主键
- person_id: 人员ID (外键)
- face_encoding: 人脸编码 (BLOB)
- image_path: 图片路径
- created_at: 创建时间

### recognition_logs (识别记录表)
- id: 主键
- person_id: 人员ID (外键)
- confidence: 识别置信度
- image_path: 图片路径
- recognition_time: 识别时间

## 技术栈

- **后端**: Python, Flask
- **前端**: HTML, CSS, JavaScript
- **桌面**: Tkinter
- **数据库**: MySQL
- **人脸识别**: face_recognition, OpenCV
- **图像处理**: Pillow

## 注意事项

1. **首次使用**: 需要先添加人员信息到数据库，系统才能进行识别
2. **图片要求**: 建议使用清晰的人脸照片，避免模糊或侧脸
3. **性能优化**: 大量人脸数据时，建议定期清理临时文件
4. **安全考虑**: 生产环境请修改默认配置，加强安全措施

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查MySQL服务是否启动
   - 验证数据库配置信息
   - 确认数据库用户权限

2. **人脸识别失败**
   - 检查图片是否包含清晰的人脸
   - 确认face_recognition库安装正确
   - 检查系统内存是否充足

3. **网页无法访问**
   - 检查端口5000是否被占用
   - 确认防火墙设置
   - 查看控制台错误信息

### 日志查看

- 网页版: 查看控制台输出
- 桌面版: 查看应用程序日志

## 开发说明

### 添加新功能

1. 修改 `face_recognition/face_detector.py` 添加识别算法
2. 更新 `database/db_manager.py` 添加数据库操作
3. 修改前端界面或桌面界面

### 自定义配置

编辑 `config.py` 文件可以修改：
- 数据库连接参数
- 文件存储路径
- 人脸识别参数
- Flask服务器配置

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- 发送邮件至项目维护者
