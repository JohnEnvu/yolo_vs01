# PyQt5 界面代码详解

## 1. 核心架构
你的界面程序本质上是一个“无限循环”，它不断地刷新屏幕来显示最新的画面。

```python
class MainWindow(QMainWindow):
    def __init__(self):
        # ... 初始化界面 ...
        
        # 核心1：定时器 (心脏)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame) # 每隔 30ms 触发一次 update_frame
```

## 2. 三种模式
我在新代码中为你设计了三种模式，通过点击不同按钮触发：

1.  **摄像头模式 (Camera Mode)**:
    *   点击 "Open Camera"。
    *   程序尝试连接 `cv2.VideoCapture(0)`。
    *   如果成功，启动定时器，每 30ms 读取一帧画面进行检测。

2.  **视频模式 (Video Mode)**:
    *   点击 "Open Image/Video" 选择 `.mp4` 文件。
    *   程序连接 `cv2.VideoCapture('文件路径')`。
    *   启动定时器，像播放电影一样一帧帧读取并检测。

3.  **图片模式 (Image Mode)**:
    *   点击 "Open Image/Video" 选择 `.jpg` 文件。
    *   程序直接读取这张图片 -> 送入模型检测 -> 显示结果。
    *   **不启动**定时器（因为图片是静止的，不需要刷新）。

## 3. 图像显示原理 (OpenCV -> PyQt)
OpenCV 读取的图片是 **BGR** 格式的数组，而 PyQt 显示需要 **RGB** 格式的图片对象。

```python
def display_frame(self, frame):
    # 1. 颜色转换: BGR (OpenCV) -> RGB (PyQt)
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 2. 创建 Qt 图片对象
    h, w, ch = rgb_image.shape
    qt_image = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)
    
    # 3. 显示在 Label 控件上
    self.video_label.setPixmap(QPixmap.fromImage(qt_image))
```

## 4. 关键控件
*   `self.video_label`: 一个巨大的文本框（QLabel），但我们把它当屏幕用，把图片贴在上面。
*   `self.timer`: 定时器，每秒钟触发约 30 次，制造“视频流畅播放”的错觉。
*   `self.detector`: 这是我们封装好的 YOLO 模型，调用 `detector.detect(frame)` 就能得到画好框的图片。
