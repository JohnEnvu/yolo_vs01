import sys
import cv2
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, 
    QWidget, QPushButton, QFileDialog, QStackedWidget, QListWidget, 
    QListWidgetItem, QScrollArea
)
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import QTimer, Qt, QSize
from core.detector import Detector

class GalleryWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout(self)
        
        # Title
        self.title = QLabel("图片库 (点击查看详情)")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        # List Widget for Thumbnails
        self.list_widget = QListWidget()
        self.list_widget.setIconSize(QSize(150, 150))
        self.list_widget.setViewMode(QListWidget.IconMode)
        self.list_widget.setResizeMode(QListWidget.Adjust)
        self.list_widget.setSpacing(10)
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.layout.addWidget(self.list_widget)

    def load_images(self, image_list):
        self.list_widget.clear()
        self.image_list = image_list
        self.title.setText(f"图片库 - 共 {len(image_list)} 张图片")
        
        # In a real app, use a thread for this to avoid freezing
        for path in image_list:
            item = QListWidgetItem(os.path.basename(path))
            # Lazy loading icons could be better, but for simplicity:
            # We just set the path as data and let the icon be a placeholder or load small
            # Loading all high-res images as icons is slow. 
            # Let's just set the icon from the file directly but scaled.
            
            icon = QIcon(path)
            item.setIcon(icon)
            item.setData(Qt.UserRole, path)
            self.list_widget.addItem(item)

    def on_item_clicked(self, item):
        path = item.data(Qt.UserRole)
        index = self.list_widget.row(item)
        self.main_window.show_detail_view(index)

class DetailWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout(self)
        
        # Scroll Area for Image (Zoom support)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.scroll_area.setWidget(self.image_label)
        self.layout.addWidget(self.scroll_area)

        # Controls
        self.controls_layout = QHBoxLayout()
        
        self.btn_prev = QPushButton("上一张")
        self.btn_prev.clicked.connect(self.prev_image)
        self.controls_layout.addWidget(self.btn_prev)

        self.btn_back = QPushButton("返回图库")
        self.btn_back.clicked.connect(self.go_back)
        self.controls_layout.addWidget(self.btn_back)

        self.btn_next = QPushButton("下一张")
        self.btn_next.clicked.connect(self.next_image)
        self.controls_layout.addWidget(self.btn_next)

        self.layout.addLayout(self.controls_layout)

        self.current_index = 0
        self.image_list = []

    def set_images(self, image_list, index):
        self.image_list = image_list
        self.current_index = index
        self.show_current_image()

    def show_current_image(self):
        if 0 <= self.current_index < len(self.image_list):
            path = self.image_list[self.current_index]
            self.main_window.process_and_show_image(path, self.image_label)
            self.update_buttons()

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_current_image()

    def next_image(self):
        if self.current_index < len(self.image_list) - 1:
            self.current_index += 1
            self.show_current_image()

    def go_back(self):
        self.main_window.show_gallery_view()

    def update_buttons(self):
        self.btn_prev.setEnabled(self.current_index > 0)
        self.btn_next.setEnabled(self.current_index < len(self.image_list) - 1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Construction Site Safety Detection System")
        self.setGeometry(100, 100, 1280, 720)

        # Initialize detector
        model_path = 'train_project/runs/runs/train/exp3/weights/best.onnx' 
        # Fallback logic
        import os
        pt_path = model_path.replace('.onnx', '.pt')
        if os.path.exists(pt_path):
             print(f"Switching to PT model for stability: {pt_path}")
             model_path = pt_path
        elif not os.path.exists(model_path):
             print(f"Warning: Model not found at {model_path}, using yolov8n.pt")
             model_path = 'weights/yolov8n.pt'
        
        self.detector = Detector(model_path) 

        # Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Top Toolbar
        self.toolbar_layout = QHBoxLayout()
        self.main_layout.addLayout(self.toolbar_layout)

        self.btn_camera = QPushButton("打开摄像头")
        self.btn_camera.clicked.connect(self.open_camera)
        self.toolbar_layout.addWidget(self.btn_camera)

        self.btn_file = QPushButton("打开文件 (图片/视频)")
        self.btn_file.clicked.connect(self.open_file)
        self.toolbar_layout.addWidget(self.btn_file)

        self.btn_folder = QPushButton("批量测试 (图库模式)")
        self.btn_folder.clicked.connect(self.open_folder)
        self.toolbar_layout.addWidget(self.btn_folder)
        
        self.btn_stop = QPushButton("停止/重置")
        self.btn_stop.clicked.connect(self.stop_detection)
        self.toolbar_layout.addWidget(self.btn_stop)

        # Stacked Widget for different views
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        # Page 0: Single View (Camera/Video)
        self.single_view_widget = QWidget()
        self.single_view_layout = QVBoxLayout(self.single_view_widget)
        self.video_label = QLabel("请选择输入源")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("border: 1px solid black;")
        self.single_view_layout.addWidget(self.video_label)
        self.stack.addWidget(self.single_view_widget)

        # Page 1: Gallery View
        self.gallery_view = GalleryWidget(self)
        self.stack.addWidget(self.gallery_view)

        # Page 2: Detail View
        self.detail_view = DetailWidget(self)
        self.stack.addWidget(self.detail_view)

        # Timer for Video/Camera
        self.cap = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.current_mode = None 

    def open_camera(self):
        self.stop_detection()
        self.stack.setCurrentIndex(0) # Switch to single view
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.video_label.setText("错误: 未检测到摄像头")
            return
        
        self.current_mode = 'camera'
        self.timer.start(30)
        self.video_label.setText("正在启动摄像头...")

    def open_file(self):
        self.stop_detection()
        self.stack.setCurrentIndex(0) # Switch to single view
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", 
            "Images/Videos (*.mp4 *.avi *.jpg *.png *.jpeg);;All Files (*)", options=options)
        
        if file_path:
            if file_path.lower().endswith(('.jpg', '.png', '.jpeg')):
                self.process_and_show_image(file_path, self.video_label)
            else:
                self.cap = cv2.VideoCapture(file_path)
                if self.cap.isOpened():
                    self.current_mode = 'video'
                    self.timer.start(30)

    def open_folder(self):
        self.stop_detection()
        folder_path = QFileDialog.getExistingDirectory(self, "选择图片文件夹")
        if folder_path:
            import glob
            import os
            extensions = ['*.jpg', '*.png', '*.jpeg', '*.JPG', '*.PNG', '*.JPEG']
            image_list = []
            for ext in extensions:
                image_list.extend(glob.glob(os.path.join(folder_path, ext)))
            
            if not image_list:
                self.video_label.setText("该文件夹下没有找到图片")
                self.stack.setCurrentIndex(0)
                return
            
            self.current_mode = 'folder'
            self.gallery_view.load_images(image_list)
            self.stack.setCurrentIndex(1) # Show Gallery

    def show_detail_view(self, index):
        self.stack.setCurrentIndex(2)
        self.detail_view.set_images(self.gallery_view.image_list, index)

    def show_gallery_view(self):
        self.stack.setCurrentIndex(1)

    def process_and_show_image(self, file_path, label_widget):
        frame = cv2.imread(file_path)
        if frame is not None:
            annotated_frame, _ = self.detector.detect(frame)
            # Display logic
            rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
            # Use setPixmap on the specific label
            # If label is in ScrollArea, we might not want to scale it to fit if we want zoom
            # But for basic "fit to window" or "large view", scaling is okay.
            # Let's check if the label is part of detail view
            if label_widget == self.detail_view.image_label:
                 # For detail view, set full pixmap and let scroll area handle it?
                 # Or scale to fit initially?
                 # User wants "Magnify". So default full size is good, scrollbars will appear.
                 label_widget.setPixmap(QPixmap.fromImage(qt_image))
                 label_widget.adjustSize()
            else:
                 # For single view (video label), scale to fit
                 label_widget.setPixmap(QPixmap.fromImage(qt_image).scaled(
                    label_widget.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            label_widget.setText("错误: 无法读取图片")

    def stop_detection(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        self.current_mode = None
        self.video_label.setText("已停止。请选择输入源。")
        self.video_label.clear()
        self.stack.setCurrentIndex(0)

    def update_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                annotated_frame, _ = self.detector.detect(frame)
                
                # Display on video_label (Page 0)
                rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                
                self.video_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
                    self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.stop_detection()
                self.video_label.setText("视频播放结束")

    def closeEvent(self, event):
        self.stop_detection()
        event.accept()
