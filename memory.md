# 项目记忆：施工现场安全防护装备检测系统

## 项目概览
- **目标**：开发一个基于 YOLO 的复杂施工现场实时安全防护装备检测系统。
- **核心指标**：
  - 检测目标：安全帽 (helmet)、反光衣 (vest) 等。
  - 精度要求：自建数据集上 mAP@0.5 >= 85%。
  - 实时性：处理速度 >= 30 FPS。
  - 软件功能：包含 GUI 界面、报警功能和统计分析的原型系统。
- **技术栈**：
  - **语言**：Python 3.9 (Conda 环境: `yolo_env`)
  - **模型**：YOLOv8 (源码集成方式) + PyTorch
  - **界面**：PyQt5 (桌面应用程序)
  - **视觉库**：OpenCV
  - **数据库**：SQLite
- **当前状态**：
  - Conda 环境 `yolo_env` 已成功配置并验证。
  - YOLOv8 源码已以编辑模式 (`pip install -e .`) 安装到 `train_project/ultralytics_repo`。
  - 项目目录结构和基础 GUI 代码已就绪。
  - 环境配置指南和数据准备指南文档已创建。
  - **更新 (2026-02-23)**：
    - 数据集配置已完成 (`external/construction-ppe.yaml`)，采用绝对路径确保稳定性。
    - 训练脚本 `train_project/train.py` 已配置，使用预训练权重 `yolov8n.pt`。
    - 项目结构文档 `docs/project_structure.md` 已生成，明确了“上位机”、“训练”、“数据”、“环境”四大板块。
    - 发现环境问题：`torch` 存在 DLL 初始化失败错误，建议用户重装。
    - **最新进展**：
      - 训练成功：已完成 100 轮训练 (Early Stopping 触发)，模型收敛。
      - 模型部署：因 Windows ONNX Runtime 环境兼容性问题，**回退使用 `.pt` 原生模型**，确保稳定性。
      - UI 重构：上位机界面已全面升级，支持 **图库视图 (Gallery View)** 和 **详情视图 (Detail View)**，实现类似 Windows 资源管理器的图片浏览体验。

## 会话历史
- **2026-02-20**:
  - 用户请求项目架构和技术栈建议。
  - **决策**：采用以 Python 为核心的桌面应用架构 (PyQt5 + OpenCV + YOLOv8)。
  - 创建项目结构：`core/`, `ui/`, `data/`, `weights/`, `utils/`。
  - 创建初始文件：`requirements.txt`, `main.py`, `ui/main_window.py`, `core/detector.py`。
- **2026-02-23**:
  - **环境搭建**：
    - 创建 `environment.yml` 并配置 Conda 环境 `yolo_env`。
    - 将 YOLOv8 源码集成到 `train_project/ultralytics_repo`。
    - 解决 PowerShell `conda activate` 报错问题（更新执行策略 `Set-ExecutionPolicy RemoteSigned`）。
    - 验证 YOLOv8 运行在本地源码模式（可编辑模式）。
  - **文档编写**：
    - 创建 `docs/环境配置指南.md`。
    - 创建 `docs/数据准备指南.md`。
    - **新增**：创建 `docs/project_structure.md` (项目结构与功能说明文档)。
    - **新增**：创建 `docs/py/pyqt_explanation.md` (PyQt 代码解释文档)。
  - **代码更新**：
    - 创建 `train_project/train.py` 训练脚本模板。
    - 增强 `ui/main_window.py`：
        - 添加摄像头连接错误处理。
        - **新增**：支持图片/视频文件输入模式（解决无摄像头测试问题）。
        - **新增**：界面添加功能按钮（打开摄像头、打开文件、停止）。
    - **配置更新**：
        - 更新 `external/construction-ppe.yaml`：修正路径为绝对路径，同步数据集类别。
        - 验证环境发现 `torch` DLL 错误，建议用户重装。
  - **训练与部署 (最新)**：
    - **训练优化**：针对 12GB 显存优化训练参数 (`batch=16`, `workers=8`, `cache=True`)。
    - **模型选择**：虽然导出了 ONNX，但因环境兼容性问题 (CUDA/cuDNN 版本不匹配)，决定**优先使用 `.pt` 模型**，并在代码中实现了自动降级/回退逻辑。
    - **UI 交互升级**：
      - **批量测试**：放弃自动播放，改为 **缩略图列表 (Gallery)** + **详情页 (Detail)** 模式。
      - **功能增强**：实现图片缩放、上一张/下一张导航、全中文界面。
      - **逻辑修复**：修复了批量测试时模式被重置为单张模式的 Bug。
    - **知识点澄清**：解释了训练集/验证集/测试集的区别，建议用户使用 `images/test` 进行批量测试以验证泛化能力。

## 开发计划
1.  **环境与项目结构** (已完成)：Python 3.9, Conda, 源码集成, 核心功能地图。
2.  **数据集准备** (已完成)：
    - 数据集下载与解压 (已完成)。
    - 配置文件 `construction-ppe.yaml` (已完成)。
3.  **模型训练 (核心)** (已完成第一阶段)：
    - 完成基线模型训练 (YOLOv8n)。
    - **下一步**：分析训练结果 (mAP, loss)，考虑是否需要改进模型结构（注意力机制等）。
4.  **应用开发** (进行中)：
    - 构建 PyQt5 界面 (已完成基础 + 图库视图)。
    - **下一步**：实现视频流实时检测与报警功能。
5.  **集成与测试**：结合模型与 UI，测试性能。

## 关键决策
- 使用 **PyQt5** 开发用户界面。
- 使用 **SQLite** 存储数据。
- 聚焦 **YOLOv8** 作为基础模型。
- **源码集成**：将 YOLOv8 源码集成到 `train_project/ultralytics_repo` 并通过 `pip install -e .` 安装，以便直接修改模型架构（毕设创新点必需）。
- **环境管理**：使用 Conda 环境 `yolo_env` (Python 3.9) 确保稳定性和隔离性。
- **第三方资源管理**：将数据集和 yaml 配置统一放置在 `external/` 目录下，保持项目主目录整洁。
- **训练验证策略**：提供快速验证脚本（已执行并发现问题），建议优先修复环境问题再进行全量训练。
- **模型部署策略**：优先使用 PyTorch 原生 `.pt` 模型，避免 ONNX Runtime 在 Windows 上的环境配置陷阱。
- **UI 设计原则**：采用“图库+详情”的交互模式替代简单的自动播放，提升用户查看测试结果的便捷性和专业度。
