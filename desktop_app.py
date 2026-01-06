# Windows desktop application
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import os
import threading
from face_recognition.face_detector import FaceDetector
from database.db_manager import DatabaseManager
from config import UPLOAD_FOLDER

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("人脸识别系统")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize face detector and database manager
        self.face_detector = FaceDetector()
        self.db_manager = DatabaseManager()
        
        # Currently selected image path
        self.current_image_path = None
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        """Create UI components"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="人脸识别系统", 
                               font=('Microsoft YaHei', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left control panel
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Image selection button
        ttk.Button(control_frame, text="选择图片", 
                  command=self.select_image).grid(row=0, column=0, pady=5, sticky=tk.W+tk.E)
        
        # Recognize button
        ttk.Button(control_frame, text="识别人脸", 
                  command=self.recognize_faces).grid(row=1, column=0, pady=5, sticky=tk.W+tk.E)
        
        # Add person button
        ttk.Button(control_frame, text="添加人员", 
                  command=self.add_person).grid(row=2, column=0, pady=5, sticky=tk.W+tk.E)
        
        # View logs button
        ttk.Button(control_frame, text="查看识别记录", 
                  command=self.view_recognition_logs).grid(row=3, column=0, pady=5, sticky=tk.W+tk.E)
        
        # Refresh database button
        ttk.Button(control_frame, text="刷新数据库", 
                  command=self.refresh_database).grid(row=4, column=0, pady=5, sticky=tk.W+tk.E)
        
        # Separator
        ttk.Separator(control_frame, orient='horizontal').grid(row=5, column=0, sticky=tk.W+tk.E, pady=10)
        
        # Status label
        self.status_label = ttk.Label(control_frame, text="就绪", 
                                     foreground="green")
        self.status_label.grid(row=6, column=0, pady=5)
        
        # Right display area
        display_frame = ttk.LabelFrame(main_frame, text="显示区域", padding="10")
        display_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(display_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Image preview tab
        self.image_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.image_frame, text="图片预览")
        
        # Image display label
        self.image_label = ttk.Label(self.image_frame, text="请选择图片", 
                                    font=('Microsoft YaHei', 12))
        self.image_label.pack(expand=True)
        
        # Recognition results tab
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="识别结果")
        
        # Recognition results text box
        self.results_text = tk.Text(self.results_frame, wrap=tk.WORD, 
                                   font=('Microsoft YaHei', 10))
        results_scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, 
                                        command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=results_scrollbar.set)
        
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Recognition logs tab
        self.logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.logs_frame, text="识别记录")
        
        # Create treeview for logs
        columns = ('时间', '姓名', '年龄', '性别', '置信度')
        self.logs_tree = ttk.Treeview(self.logs_frame, columns=columns, show='headings')
        
        # Set column headings
        for col in columns:
            self.logs_tree.heading(col, text=col)
            self.logs_tree.column(col, width=120)
        
        # Add scrollbar
        logs_scrollbar = ttk.Scrollbar(self.logs_frame, orient=tk.VERTICAL, 
                                     command=self.logs_tree.yview)
        self.logs_tree.configure(yscrollcommand=logs_scrollbar.set)
        
        self.logs_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        logs_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load recognition logs
        self.load_recognition_logs()
        
    def select_image(self):
        """Select image file"""
        file_path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.current_image_path = file_path
            self.display_image(file_path)
            self.update_status("图片已选择")
    
    def display_image(self, image_path):
        """Display image"""
        try:
            # Open image
            image = Image.open(image_path)
            
            # Calculate scale to fit the display area
            max_width = 600
            max_height = 400
            
            width, height = image.size
            scale = min(max_width/width, max_height/height, 1)
            
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            # Resize image
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Update image label
            self.image_label.configure(image=photo, text="")
            self.image_label.image = photo  # Keep reference
            
        except Exception as e:
            messagebox.showerror("错误", f"无法显示图片: {str(e)}")
    
    def recognize_faces(self):
        """Recognize faces"""
        if not self.current_image_path:
            messagebox.showwarning("警告", "请先选择图片")
            return
        
        # Run recognition in a new thread to avoid freezing the UI
        threading.Thread(target=self._recognize_faces_thread, daemon=True).start()
    
    def _recognize_faces_thread(self):
        """Face recognition thread"""
        try:
            self.update_status("正在识别人脸...")
            
            # Perform face recognition
            results = self.face_detector.recognize_faces(self.current_image_path)
            
            # 在主线程中更新界面
            self.root.after(0, self._update_recognition_results, results)
            
        except Exception as e:
            self.root.after(0, self._show_error, f"识别过程中发生错误: {str(e)}")
    
    def _update_recognition_results(self, results):
        """Update recognition results"""
        self.results_text.delete(1.0, tk.END)
        
        if not results:
            self.results_text.insert(tk.END, "未检测到人脸")
            self.update_status("未检测到人脸")
            return
        
        result_text = "识别结果:\n\n"
        
        for i, result in enumerate(results, 1):
            result_text += f"人脸 {i}:\n"
            result_text += f"  姓名: {result['name']}\n"
            
            if result['name'] != '未知':
                if result.get('age'):
                    result_text += f"  年龄: {result['age']}\n"
                if result.get('gender'):
                    result_text += f"  性别: {result['gender']}\n"
                if result.get('phone'):
                    result_text += f"  电话: {result['phone']}\n"
                if result.get('email'):
                    result_text += f"  邮箱: {result['email']}\n"
                if result.get('address'):
                    result_text += f"  地址: {result['address']}\n"
                if result.get('confidence'):
                    result_text += f"  置信度: {result['confidence']:.2f}\n"
            else:
                result_text += "  状态: 未识别的人脸\n"
            
            result_text += "\n"
        
        self.results_text.insert(tk.END, result_text)
        self.update_status(f"识别完成，检测到 {len(results)} 个人脸")
        
        # Switch to results tab
        self.notebook.select(1)
    
    def add_person(self):
        """Add person"""
        if not self.current_image_path:
            messagebox.showwarning("警告", "请先选择图片")
            return
        
        # Check if a face is detected
        try:
            face_locations, face_encodings = self.face_detector.detect_faces_in_image(self.current_image_path)
            
            if not face_encodings:
                messagebox.showerror("错误", "未检测到人脸，请选择包含人脸的图片")
                return
            
            if len(face_encodings) > 1:
                messagebox.showerror("错误", "检测到多个人脸，请选择只包含一个人脸的图片")
                return
            
        except Exception as e:
            messagebox.showerror("错误", f"检测人脸时发生错误: {str(e)}")
            return
        
        # Show person info input dialog
        self.show_person_info_dialog()
    
    def show_person_info_dialog(self):
        """Show person info input dialog"""
        dialog = PersonInfoDialog(self.root, self)
        self.root.wait_window(dialog.dialog)
    
    def add_person_to_database(self, person_info):
        """Add person to database"""
        try:
            self.update_status("正在添加人员...")
            
            # Run add operation in a new thread
            threading.Thread(target=self._add_person_thread, 
                           args=(person_info,), daemon=True).start()
            
        except Exception as e:
            self._show_error(f"添加人员时发生错误: {str(e)}")
    
    def _add_person_thread(self, person_info):
        """Add person thread"""
        try:
            success, message = self.face_detector.add_new_person(
                self.current_image_path, person_info
            )
            
            if success:
                self.root.after(0, self._show_success, message)
                self.root.after(0, self.refresh_database)
            else:
                self.root.after(0, self._show_error, message)
                
        except Exception as e:
            self.root.after(0, self._show_error, f"添加人员时发生错误: {str(e)}")
    
    def view_recognition_logs(self):
        """View recognition logs"""
        self.load_recognition_logs()
        self.notebook.select(2)  # 切换到记录标签页
    
    def load_recognition_logs(self):
        """Load recognition logs"""
        try:
            # Clear existing records
            for item in self.logs_tree.get_children():
                self.logs_tree.delete(item)
            
            # Retrieve logs
            logs = self.db_manager.get_recognition_logs(100)
            
            # Insert logs into the treeview
            for log in logs:
                self.logs_tree.insert('', 'end', values=(
                    log['recognition_time'].strftime('%Y-%m-%d %H:%M:%S'),
                    log['name'] or '未知',
                    log['age'] or '-',
                    log['gender'] or '-',
                    f"{log['confidence']:.2f}" if log['confidence'] else '-'
                ))
            
            self.update_status(f"已加载 {len(logs)} 条识别记录")
            
        except Exception as e:
            self._show_error(f"加载识别记录时发生错误: {str(e)}")
    
    def refresh_database(self):
        """Refresh database"""
        try:
            self.face_detector.load_known_faces()
            self.update_status("数据库已刷新")
        except Exception as e:
            self._show_error(f"刷新数据库时发生错误: {str(e)}")
    
    def update_status(self, message):
        """Update status label"""
        self.status_label.configure(text=message)
        self.root.update_idletasks()
    
    def _show_error(self, message):
        """Show error message"""
        messagebox.showerror("错误", message)
        self.update_status("操作失败")
    
    def _show_success(self, message):
        """Show success message"""
        messagebox.showinfo("成功", message)
        self.update_status("操作成功")


class PersonInfoDialog:
    def __init__(self, parent, app):
        self.app = app
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("添加人员信息")
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)
        
        # Make the dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create dialog components"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="人员信息", 
                               font=('Microsoft YaHei', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Form fields
        fields = [
            ('name', '姓名 *', 'text'),
            ('age', '年龄', 'number'),
            ('gender', '性别', 'combo'),
            ('phone', '电话', 'text'),
            ('email', '邮箱', 'text'),
            ('address', '地址', 'text')
        ]
        
        self.entries = {}
        
        for field, label, field_type in fields:
            frame = ttk.Frame(main_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=label, width=10).pack(side=tk.LEFT)
            
            if field_type == 'combo':
                entry = ttk.Combobox(frame, values=['', '男', '女'], state='readonly')
            elif field_type == 'number':
                entry = ttk.Entry(frame)
            else:
                entry = ttk.Entry(frame)
            
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
            self.entries[field] = entry
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="取消", 
                  command=self.dialog.destroy).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="确定", 
                  command=self.submit).pack(side=tk.RIGHT)
    
    def submit(self):
        """Submit form"""
        # Validate required fields
        if not self.entries['name'].get().strip():
            messagebox.showerror("错误", "请输入姓名")
            return
        
        # Collect data
        person_info = {
            'name': self.entries['name'].get().strip(),
            'age': self.entries['age'].get() or None,
            'gender': self.entries['gender'].get() or None,
            'phone': self.entries['phone'].get().strip() or None,
            'email': self.entries['email'].get().strip() or None,
            'address': self.entries['address'].get().strip() or None
        }
        
        # Validate age
        if person_info['age']:
            try:
                person_info['age'] = int(person_info['age'])
                if person_info['age'] < 1 or person_info['age'] > 120:
                    messagebox.showerror("错误", "年龄必须在1-120之间")
                    return
            except ValueError:
                messagebox.showerror("错误", "年龄必须是数字")
                return
        
        # Close dialog and add person
        self.dialog.destroy()
        self.app.add_person_to_database(person_info)


def main():
    """Main function"""
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
