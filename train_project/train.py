import os
from ultralytics import YOLO

if __name__ == '__main__':
    # 获取当前脚本所在目录，确保路径在不同环境下都能正确解析
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Load a model
    # 使用相对路径构建绝对路径，兼容 Win 和 Docker
    model_path = os.path.join(current_dir, "..", "weights", "yolov8n.pt")
    model = YOLO(model_path)  

    # 2. Train the model
    data_config = os.path.join(current_dir, "..", "external", "construction-ppe.yaml")
    
    results = model.train(
        data=data_config,      # 你的数据集配置文件路径
        epochs=300,            # 训练轮数
        imgsz=640,             # 图像尺寸
        batch=-1,              # 自动检测显存允许的最大 batch
        device=0,              # 使用 0 号显卡
        project=os.path.join(current_dir, "..", "runs/train"), 
        name="exp_docker_compatible",
        workers=8,             # 数据加载进程数
        patience=50, 
        save=True,
        cache=True,
    )

    # 3. Validation
    metrics = model.val()  # evaluate model performance on the validation set

    # 4. Export the model
    success = model.export(format="onnx")  # export the model to ONNX format
