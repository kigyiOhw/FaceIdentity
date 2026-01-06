# Database management module
import mysql.connector
from mysql.connector import Error
import pickle
import numpy as np
from config import DATABASE_CONFIG

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(**DATABASE_CONFIG)
            if self.connection.is_connected():
                print("Connected to MySQL database successfully")
        except Error as e:
            print(f"Database connection error: {e}")
    
    def disconnect(self):
        """Disconnect from the database"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")
    
    def add_person(self, name, age=None, gender=None, phone=None, email=None, address=None):
        """Add new person information"""
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO persons (name, age, gender, phone, email, address)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (name, age, gender, phone, email, address)
            cursor.execute(query, values)
            self.connection.commit()
            person_id = cursor.lastrowid
            cursor.close()
            return person_id
        except Error as e:
            print(f"Error adding person info: {e}")
            return None
    
    def add_face_encoding(self, person_id, face_encoding, image_path=None):
        """Add face encoding"""
        try:
            cursor = self.connection.cursor()
            # Convert numpy array to binary data
            encoding_bytes = pickle.dumps(face_encoding)
            query = """
            INSERT INTO face_encodings (person_id, face_encoding, image_path)
            VALUES (%s, %s, %s)
            """
            values = (person_id, encoding_bytes, image_path)
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error adding face encoding: {e}")
            return False
    
    def get_all_face_encodings(self):
        """Get all face encodings"""
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT fe.id, fe.person_id, fe.face_encoding, fe.image_path,
                   p.name, p.age, p.gender, p.phone, p.email, p.address
            FROM face_encodings fe
            JOIN persons p ON fe.person_id = p.id
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            
            encodings = []
            for row in results:
                encoding_data = pickle.loads(row[2])  # Deserialize face encoding
                person_info = {
                    'encoding_id': row[0],
                    'person_id': row[1],
                    'face_encoding': encoding_data,
                    'image_path': row[3],
                    'name': row[4],
                    'age': row[5],
                    'gender': row[6],
                    'phone': row[7],
                    'email': row[8],
                    'address': row[9]
                }
                encodings.append(person_info)
            return encodings
        except Error as e:
            print(f"Error fetching face encodings: {e}")
            return []
    
    def get_person_by_id(self, person_id):
        """Get person info by ID"""
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM persons WHERE id = %s"
            cursor.execute(query, (person_id,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return {
                    'id': result[0],
                    'name': result[1],
                    'age': result[2],
                    'gender': result[3],
                    'phone': result[4],
                    'email': result[5],
                    'address': result[6],
                    'created_at': result[7],
                    'updated_at': result[8]
                }
            return None
        except Error as e:
            print(f"Error fetching person info: {e}")
            return None
    
    def add_recognition_log(self, person_id, confidence, image_path):
        """Add recognition log"""
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO recognition_logs (person_id, confidence, image_path)
            VALUES (%s, %s, %s)
            """
            values = (person_id, confidence, image_path)
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error adding recognition log: {e}")
            return False
    
    def get_recognition_logs(self, limit=50):
        """Get recognition logs"""
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT rl.id, rl.person_id, rl.confidence, rl.image_path, rl.recognition_time,
                   p.name, p.age, p.gender
            FROM recognition_logs rl
            LEFT JOIN persons p ON rl.person_id = p.id
            ORDER BY rl.recognition_time DESC
            LIMIT %s
            """
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            cursor.close()
            
            logs = []
            for row in results:
                log = {
                    'id': row[0],
                    'person_id': row[1],
                    'confidence': row[2],
                    'image_path': row[3],
                    'recognition_time': row[4],
                    'name': row[5],
                    'age': row[6],
                    'gender': row[7]
                }
                logs.append(log)
            return logs
        except Error as e:
            print(f"Error fetching recognition logs: {e}")
            return []
    
    def update_person(self, person_id, **kwargs):
        """Update person information"""
        try:
            cursor = self.connection.cursor()
            set_clauses = []
            values = []
            
            for key, value in kwargs.items():
                if value is not None:
                    set_clauses.append(f"{key} = %s")
                    values.append(value)
            
            if set_clauses:
                values.append(person_id)
                query = f"UPDATE persons SET {', '.join(set_clauses)} WHERE id = %s"
                cursor.execute(query, values)
                self.connection.commit()
                cursor.close()
                return True
            return False
        except Error as e:
            print(f"Error updating person info: {e}")
            return False
    
    def delete_person(self, person_id):
        """Delete person information (cascade delete face encodings)"""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM persons WHERE id = %s"
            cursor.execute(query, (person_id,))
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error deleting person info: {e}")
            return False
