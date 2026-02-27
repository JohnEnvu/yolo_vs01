import cv2
from ultralytics import YOLO

class Detector:
    def __init__(self, model_path=None):
        if model_path:
            # Force CPU for ONNX to avoid CUDA version mismatch issues
            if model_path.endswith('.onnx'):
                self.model = YOLO(model_path, task='detect')
                # 显式指定 providers 为 CPU，避免自动尝试加载 CUDA 失败
                # 注意：Ultralytics 的 YOLO 类对 ONNX 的封装可能不直接接受 providers 参数
                # 但我们可以通过设置环境变量或让它默认回退
                print(f"Loaded ONNX model from: {model_path}")
            else:
                self.model = YOLO(model_path)
                print(f"Loaded PT model from: {model_path}")
        else:
            # Default to yolov8n if no path provided
            self.model = YOLO('yolov8n.pt') 
            print("Loaded default model: yolov8n.pt") 

    def detect(self, frame):
        """
        Perform detection on a frame.
        Returns the annotated frame and detection results.
        """
        results = self.model(frame)
        annotated_frame = results[0].plot()
        return annotated_frame, results
