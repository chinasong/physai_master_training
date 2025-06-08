# PhysAI Master Training

一个简单而有效的人脸识别系统，用于让机器人识别其主人。通过摄像头采集主人人脸图像，提取特征编码，并实现实时识别。

## 项目结构
```
physai_master_training/
├── README.md                           # 项目说明：操作步骤 / 模型作用
├── requirements.txt                    # Python依赖：face_recognition, opencv-python 等
├── config/
│   └── settings.yaml                   # 参数配置文件（摄像头编号、人脸识别阈值等）
├── data/
│   ├── captured_faces/                 # 采集到的主人人脸图像
│   └── master_face_encoding.pkl        # 主人脸部特征编码（训练后生成）
├── logs/
│   └── training_log.txt                # 日志记录：识别时间戳 / 编码成功 / 错误情况
├── scripts/
│   ├── face_memory_train.py            # ✅ 采集主人人脸并保存编码
│   ├── face_recognition_live.py        # ✅ 实时识别人脸是否为主人
│   ├── voice_response.py               # （选配）识别后调用TTS语音播报："你好，主人"
│   └── utils/
│       ├── camera_utils.py             # 摄像头初始化、帧采集
│       ├── face_utils.py               # 人脸检测、人脸编码、匹配逻辑
│       └── storage_utils.py            # 文件存储、编码加载、路径管理等
```

## 功能特点
- 简单易用：只需运行脚本，按提示操作即可
- 实时识别：支持实时摄像头人脸检测和识别
- 可靠存储：自动保存人脸图像和特征编码
- 日志记录：详细记录训练和识别过程
- 语音反馈：可选配语音播报功能

## 安装依赖
```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 采集主人人脸
```bash
python scripts/face_memory_train.py
```
- 运行脚本后，正对摄像头
- 按 's' 键拍摄并保存人脸
- 按 'q' 键退出程序

### 2. 实时人脸识别
```bash
python scripts/face_recognition_live.py
```
- 启动实时识别
- 自动检测和识别主人
- 显示识别结果和置信度

### 3. 语音反馈（可选）
```bash
python scripts/voice_response.py
```
- 配置语音播报
- 自定义欢迎语

## 配置说明
编辑 `config/settings.yaml` 可调整：
- 摄像头参数（设备ID、分辨率等）
- 人脸识别阈值
- 日志级别
- 语音设置

## 日志查看
训练和识别日志保存在 `logs/training_log.txt`，包含：
- 时间戳
- 操作类型
- 识别结果
- 错误信息（如有） 