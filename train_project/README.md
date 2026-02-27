# 模型训练指南

## 1. 为什么需要源码？
你的毕设重点是**模型训练和修改**（例如添加注意力机制、修改主干网络）。
如果只用 `pip install ultralytics`，你只能训练官方标准模型。要进行“魔改”，必须拥有源码并对其进行修改。

## 2. 如何获取源码
由于检测到你的环境中没有安装 `git`，你需要手动下载源码：

1.  访问 [Ultralytics YOLOv8 GitHub 仓库](https://github.com/ultralytics/ultralytics)。
2.  点击绿色的 **Code** 按钮，选择 **Download ZIP**。
3.  下载后解压。
4.  将解压后的 `ultralytics-main` 文件夹重命名为 `ultralytics_repo`。
5.  将整个 `ultralytics_repo` 文件夹放入本项目的 `train_project` 目录下。

最终目录结构应如下：
```text
g:\work\yolo0213\v8
├── train_project/
│   ├── ultralytics_repo/  <-- 这里放你下载的源码
│   │   ├── ultralytics/
│   │   ├── ...
│   └── train.py           <-- 我为你创建的训练脚本
├── ...
```

## 3. 如何配置环境使用源码
下载好源码后，你需要以“开发模式”安装它，这样你修改源码后，训练脚本才会生效。

在终端中运行：
```bash
# 进入源码目录
cd train_project/ultralytics_repo

# 安装依赖并以编辑模式安装包
pip install -e .
```

## 4. 如何开始训练
1. 准备好你的数据集（按照 YOLO 格式，分为 images 和 labels）。
2. 修改 `train_project/train.py` 中的 `data` 参数指向你的数据集 yaml 文件。
3. 运行训练：
   ```bash
   python train_project/train.py
   ```
