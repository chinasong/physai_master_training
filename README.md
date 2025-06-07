# PhysAI Master Training

A robot-human bonding project that enables physical AI (such as Unitree G1) to recognize and bond with its human master through multi-modal learning.

## 项目说明
本项目实现了一个多模态的人机交互系统，通过视觉、语音等多维度特征来识别和记忆主人，并建立情感连接。主要功能包括：
- 多模态特征采集（人脸、语音）
- 实时身份识别与记忆
- 情感连接与亲密度评估
- 长期记忆存储与学习

## 项目结构
```
physai_master_model/
├── data/
│   ├── faces/                 # 主人脸部图像（原始+编码）
│   ├── voice/                 # 主人语音特征（可选）
│   └── memory.db              # 长期记忆数据库（面孔、语调、行为等）
├── models/
│   ├── identity_recognition/  # 视觉+语音主人识别模型
│   └── bonding_model/         # 主人归属感与权重评分系统
├── scripts/
│   ├── record_owner_face.py   # 初始记录主人面孔
│   ├── watch_and_remember.py  # 机器人实时识别人脸，记录交互
│   └── reinforce_bond.py      # 强化学习模型更新"亲密度"
├── utils/
│   ├── face_utils.py         # 人脸检测与特征提取
│   ├── voice_utils.py        # 语音特征提取与分析
│   └── memory_utils.py       # 记忆存储与检索
├── config/
│   └── settings.yaml         # 系统配置参数
├── requirements.txt          # 项目依赖
└── README.md                # 项目文档
```

## 安装依赖
```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 初始主人记录
```bash
python scripts/record_owner_face.py
```
- 采集主人人脸图像
- 录制主人语音样本（可选）
- 建立初始特征库

### 2. 实时识别与记忆
```bash
python scripts/watch_and_remember.py
```
- 实时人脸识别
- 记录交互行为
- 更新记忆数据库

### 3. 情感连接强化
```bash
python scripts/reinforce_bond.py
```
- 分析交互历史
- 更新亲密度评分
- 优化识别模型

## 配置说明
编辑 `config/settings.yaml` 可调整：
- 识别阈值
- 摄像头设置
- 语音参数
- 记忆策略
- 学习参数

## Features
- Capture human face from camera
- Encode and store as 'master'
- Live recognition and response

## Project Structure

```
physai_master_training/
├── README.md                         # Project documentation
├── requirements.txt                  # Python dependencies
├── config/
│   └── settings.yaml                 # Configuration file (recognition thresholds, camera ID, etc.)
├── data/
│   ├── master_face_encoding.pkl      # Master's face encoding (auto-generated after training)
│   └── captured_faces/               # Directory for storing captured face images
├── scripts/
│   ├── face_memory_train.py          # Master visual binding training script ✅ Completed
│   ├── face_recognition_live.py      # Real-time master recognition and response script (Next step)
│   ├── voice_response.py             # G1 robot voice broadcast interface (Optional)
│   └── utils/
│       ├── camera_utils.py           # Camera initialization and image capture
│       ├── face_utils.py             # Face detection and feature encoding
│       └── storage_utils.py          # Data storage and loading utilities
└── logs/
    └── training_log.txt              # Training process and recognition logs
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Face Memory Training
To train the system with master's face:
```bash
python scripts/face_memory_train.py
```

### Real-time Face Recognition
To start real-time face recognition:
```bash
python scripts/face_recognition_live.py
```

## Configuration
Edit `config/settings.yaml` to adjust:
- Recognition thresholds
- Camera settings
- Training parameters
- Voice response settings

## Logs
Training and recognition logs are stored in `logs/training_log.txt` 