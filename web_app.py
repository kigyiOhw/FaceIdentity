# Flask web application
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
from face_recognition.face_detector import FaceDetector
from database.db_manager import DatabaseManager
from config import UPLOAD_FOLDER, FLASK_CONFIG

app = Flask(__name__)
CORS(app)

# Configure file uploads
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize face detector and database manager
face_detector = FaceDetector()
db_manager = DatabaseManager()

@app.route('/')
def index():
    """Home"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload image and recognize faces"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # Recognize faces
            results = face_detector.recognize_faces(filepath)
            
            return jsonify({
                'success': True,
                'results': results,
                'image_path': filepath
            })
        else:
            return jsonify({'error': '不支持的文件类型'}), 400
    
    except Exception as e:
        return jsonify({'error': f'处理文件时出错: {str(e)}'}), 500

@app.route('/add_person', methods=['POST'])
def add_person():
    """Add new person"""
    try:
        data = request.get_json()
        
        if 'file' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400
        
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Save file
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # Add person info
            success, message = face_detector.add_new_person(filepath, data)
            
            if success:
                return jsonify({'success': True, 'message': message})
            else:
                return jsonify({'error': message}), 400
        else:
            return jsonify({'error': '不支持的文件类型'}), 400
    
    except Exception as e:
        return jsonify({'error': f'添加人员时出错: {str(e)}'}), 500

@app.route('/persons', methods=['GET'])
def get_persons():
    """Get list of all persons"""
    try:
        # TODO: implement retrieval of person list
        # Return empty list for now
        return jsonify({'persons': []})
    except Exception as e:
        return jsonify({'error': f'获取人员列表时出错: {str(e)}'}), 500

@app.route('/recognition_logs', methods=['GET'])
def get_recognition_logs():
    """获取识别记录"""
    try:
        limit = request.args.get('limit', 50, type=int)
        logs = db_manager.get_recognition_logs(limit)
        return jsonify({'logs': logs})
    except Exception as e:
        return jsonify({'error': f'获取识别记录时出错: {str(e)}'}), 500

@app.route('/delete_person/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    """删除人员"""
    try:
        success = db_manager.delete_person(person_id)
        if success:
            # 重新加载已知人脸
            face_detector.load_known_faces()
            return jsonify({'success': True, 'message': '删除成功'})
        else:
            return jsonify({'error': '删除失败'}), 500
    except Exception as e:
        return jsonify({'error': f'删除人员时出错: {str(e)}'}), 500

@app.route('/update_person/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    """更新人员信息"""
    try:
        data = request.get_json()
        success = db_manager.update_person(person_id, **data)
        
        if success:
            # 重新加载已知人脸
            face_detector.load_known_faces()
            return jsonify({'success': True, 'message': '更新成功'})
        else:
            return jsonify({'error': '更新失败'}), 500
    except Exception as e:
        return jsonify({'error': f'更新人员信息时出错: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(
        host=FLASK_CONFIG['host'],
        port=FLASK_CONFIG['port'],
        debug=FLASK_CONFIG['debug']
    )
