# PyQt5 开发指南与项目结构说明

## 1. PyQt5 简介
PyQt5 是 Python 的一套 GUI (图形用户界面) 库，基于强大的 Qt5 框架。它允许开发者使用 Python 语言快速构建跨平台的桌面应用程序。
- **核心优势**：
  - **组件丰富**：提供按钮、标签、文本框、表格等所有常见控件。
  - **信号与槽机制**：独特的事件处理机制，解耦逻辑与界面。
  - **跨平台**：一次编写，可在 Windows、Linux、macOS 上运行。
  - **易于扩展**：支持 CSS 样式表 (QSS) 美化界面。

## 2. 本项目结构解析

为了保持代码整洁和易于维护，我们采用了**模块化**的设计思想，将界面逻辑、业务逻辑和入口文件分离。

```text
g:\work\yolo0213\v8
├── main.py            # 【入口】程序的启动文件
├── core/              # 【核心业务】存放 YOLO 模型推理逻辑
│   └── detector.py    # 封装后的检测器类，负责调用 YOLOv8
├── ui/                # 【界面逻辑】存放 PyQt5 界面相关代码
│   └── main_window.py # 主窗口类，负责显示画面、响应按钮
├── data/              # 【数据】存放图片、视频或数据库文件
├── weights/           # 【模型】存放训练好的 .pt 权重文件
└── requirements.txt   # 【依赖】项目所需的 Python 库列表
```

### 2.1 各文件详细作用

#### `main.py` (入口)
- **作用**：程序的起点。它的唯一职责是初始化 PyQt 的 `QApplication` 对象，创建并显示 `MainWindow`，然后启动事件循环。
- **关键代码**：
  ```python
  app = QApplication(sys.argv)  # 创建应用程序对象
  window = MainWindow()         # 实例化主窗口
  window.show()                 # 显示窗口
  sys.exit(app.exec_())         # 进入事件循环，直到窗口关闭
  ```

#### `ui/main_window.py` (主界面)
- **作用**：定义窗口长什么样（按钮在哪、视频在哪显示），以及用户点击按钮后发生什么（信号与槽）。
- **核心组件**：
  - `QMainWindow`: 主窗口基类。
  - `QLabel`: 用于显示视频帧（我们将 OpenCV 读取的图片转换后贴在这个标签上）。
  - `QPushButton`: 控制检测开始/停止的按钮。
  - `QTimer`: 定时器，用于定期（如每 30ms）触发一次“读取摄像头 -> 检测 -> 显示”的流程。

#### `core/detector.py` (检测逻辑)
- **作用**：将深度学习模型封装成一个简单的工具类，界面代码不需要知道 YOLO 是怎么工作的，只需要调用 `detect(image)` 方法即可。
- **核心方法**：
  - `__init__`: 加载模型（默认 `yolov8n.pt`）。
  - `detect(frame)`: 接收一张图片，返回画了框的图片和检测结果数据。

## 3. 常用 PyQt5 组件与概念

### 3.1 信号与槽 (Signals & Slots)
这是 Qt 最核心的通信机制。
- **信号 (Signal)**：当某个事件发生时（如按钮被点击），组件会发出一个信号。
- **槽 (Slot)**：这是一个函数，用于响应信号。
- **连接方式**：
  ```python
  # 当 start_button 被点击 (clicked) 时，执行 toggle_detection 函数
  self.start_button.clicked.connect(self.toggle_detection)
  
  # 当定时器时间到 (timeout) 时，执行 update_frame 函数
  self.timer.timeout.connect(self.update_frame)
  ```

### 3.2 图像显示流程 (OpenCV -> PyQt)
OpenCV 读取的图片格式是 `BGR`，而 PyQt 显示需要 `RGB` 格式，且需要转换为 `QImage` 对象。
1. **读取**：`ret, frame = cap.read()` (OpenCV, BGR 格式)
2. **转换颜色**：`rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)`
3. **转换为 QImage**：
   ```python
   h, w, ch = rgb_image.shape
   bytes_per_line = ch * w
   qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
   ```
4. **显示**：`label.setPixmap(QPixmap.fromImage(qt_image))`

### 3.3 布局管理 (Layouts)
不要使用绝对坐标（x=100, y=200），而是使用布局管理器，这样窗口缩放时组件会自动调整。
- `QVBoxLayout`: 垂直布局（从上到下排列）。
- `QHBoxLayout`: 水平布局（从左到右排列）。
- `QGridLayout`: 网格布局（像 Excel 表格一样排列）。

## 4. 如何开发与修改

### 场景一：我想修改界面，加一个“保存截图”的按钮
1. 打开 `ui/main_window.py`。
2. 在 `__init__` 方法中创建一个新按钮：
   ```python
   self.save_btn = QPushButton("截图", self)
   self.layout.addWidget(self.save_btn)  # 添加到布局中
   ```
3. 定义一个函数（槽）来处理点击：
   ```python
   def save_screenshot(self):
       # 保存当前帧逻辑...
       print("截图已保存")
   ```
4. 连接信号与槽：
   ```python
   self.save_btn.clicked.connect(self.save_screenshot)
   ```

### 场景二：我想换成训练好的安全帽检测模型
1. 将训练好的权重文件（如 `best.pt`）放入 `weights/` 文件夹。
2. 修改 `ui/main_window.py` 中的初始化代码：
   ```python
   # 修改前
   self.detector = Detector() 
   
   # 修改后 (假设权重文件在 weights/best.pt)
   self.detector = Detector(model_path='weights/best.pt')
   ```

### 场景三：程序运行卡顿怎么办？
当前方案是在主线程（UI 线程）中进行模型推理，如果模型很大（如 YOLOv8x），界面会卡死。
- **解决方案**：使用 `QThread` 将检测任务放到后台线程执行，检测完成后通过信号将结果发回主线程显示。这是进阶用法，后续可视情况优化。

## 5. 环境配置与运行
确保已安装依赖：
```bash
pip install -r requirements.txt
```
运行项目：
```bash
python main.py
```
