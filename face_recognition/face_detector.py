# Core face recognition module
import face_recognition
import cv2
import numpy as np
from PIL import Image
import os
from config import FACE_RECOGNITION_CONFIG
from database.db_manager import DatabaseManager

class FaceDetector:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_info = []
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load known faces from the database"""
        try:
            face_data = self.db_manager.get_all_face_encodings()
            self.known_face_encodings = []
            self.known_face_names = []
            self.known_face_info = []
            
            for data in face_data:
                self.known_face_encodings.append(data['face_encoding'])
                self.known_face_names.append(data['name'])
                self.known_face_info.append({
                    'person_id': data['person_id'],
                    'name': data['name'],
                    'age': data['age'],
                    'gender': data['gender'],
                    'phone': data['phone'],
                    'email': data['email'],
                    'address': data['address']
                })
            print(f"Loaded {len(self.known_face_encodings)} known faces")
        except Exception as e:
            print(f"Error loading known faces: {e}")
    
    def detect_faces_in_image(self, image_path):
        """Detect faces in an image"""
        try:
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Detect face locations
            face_locations = face_recognition.face_locations(
                image, 
                model=FACE_RECOGNITION_CONFIG['model'],
                number_of_times_to_upsample=FACE_RECOGNITION_CONFIG['upsample']
            )
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            return face_locations, face_encodings
        except Exception as e:
            print(f"Face detection error: {e}")
            return [], []
    
    def recognize_faces(self, image_path):
        """Recognize faces and return results"""
        try:
            face_locations, face_encodings = self.detect_faces_in_image(image_path)
            
            if not face_encodings:
                return []
            
            results = []
            
            for i, face_encoding in enumerate(face_encodings):
                # Compare with known faces
                matches = face_recognition.compare_faces(
                    self.known_face_encodings, 
                    face_encoding, 
                    tolerance=FACE_RECOGNITION_CONFIG['tolerance']
                )
                
                face_distances = face_recognition.face_distance(
                    self.known_face_encodings, 
                    face_encoding
                )
                
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    # Found matching face
                    confidence = 1 - face_distances[best_match_index]
                    person_info = self.known_face_info[best_match_index].copy()
                    person_info['confidence'] = confidence
                    person_info['face_location'] = face_locations[i]
                    
                    # Record recognition log
                    self.db_manager.add_recognition_log(
                        person_info['person_id'], 
                        confidence, 
                        image_path
                    )
                    
                    results.append(person_info)
                else:
                    # Unrecognized face
                    results.append({
                        'name': '未知',
                        'confidence': 0,
                        'face_location': face_locations[i],
                        'person_id': None
                    })
            
            return results
        except Exception as e:
            print(f"Face recognition error: {e}")
            return []
    
    def add_new_person(self, image_path, person_info):
        """Add a new person and their face information"""
        try:
            # Detect faces
            face_locations, face_encodings = self.detect_faces_in_image(image_path)
            
            if not face_encodings:
                return False, "未检测到人脸"
            
            if len(face_encodings) > 1:
                return False, "图像中包含多个人脸，请上传只包含一个人脸的照片"
            
            # Add person info to the database
            person_id = self.db_manager.add_person(
                name=person_info['name'],
                age=person_info.get('age'),
                gender=person_info.get('gender'),
                phone=person_info.get('phone'),
                email=person_info.get('email'),
                address=person_info.get('address')
            )
            
            if not person_id:
                return False, "添加人员信息失败"
            
            # Add face encoding
            success = self.db_manager.add_face_encoding(
                person_id, 
                face_encodings[0], 
                image_path
            )
            
            if success:
                # Reload known faces
                self.load_known_faces()
                return True, f"成功添加人员: {person_info['name']}"
            else:
                return False, "添加人脸编码失败"
                
        except Exception as e:
            print(f"Error adding new person: {e}")
            return False, f"添加失败: {str(e)}"
    
    def get_face_encoding_from_image(self, image_path):
        """Extract face encoding from an image"""
        try:
            face_locations, face_encodings = self.detect_faces_in_image(image_path)
            
            if not face_encodings:
                return None, "未检测到人脸"
            
            if len(face_encodings) > 1:
                return None, "图像中包含多个人脸"
            
            return face_encodings[0], "成功"
        except Exception as e:
            return None, f"Error extracting face encoding: {str(e)}"
    
    def draw_face_boxes(self, image_path, results, output_path=None):
        """Draw face boxes and labels on an image"""
        try:
            # Load image
            image = cv2.imread(image_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            for result in results:
                if 'face_location' in result:
                    top, right, bottom, left = result['face_location']
                    
                    # Draw face box
                    color = (0, 255, 0) if result['name'] != '未知' else (0, 0, 255)
                    cv2.rectangle(image_rgb, (left, top), (right, bottom), color, 2)
                    
                    # Add label
                    label = f"{result['name']}"
                    if 'confidence' in result and result['confidence'] > 0:
                        label += f" ({result['confidence']:.2f})"
                    
                    cv2.putText(image_rgb, label, (left, top - 10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            
            if output_path:
                cv2.imwrite(output_path, cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))
            
            return image_rgb
        except Exception as e:
            print(f"Error drawing face boxes: {e}")
            return None
