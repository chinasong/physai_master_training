"""
采集并保存"主人"的脸部编码。
通过摄像头实时捕获人脸图像，提取特征编码并保存到文件中。
使用方法：
1. 运行脚本
2. 正对摄像头
3. 按 's' 键拍摄并保存
4. 按 'q' 键退出
"""

import cv2
import yaml
import os
from utils.camera_utils import get_camera_stream
from utils.face_utils import encode_face
from utils.storage_utils import save_encoding

config = yaml.safe_load(open("config/settings.yaml"))
camera = get_camera_stream(config['camera_index'])

print("📷 请正对摄像头，准备拍摄主人面孔。按 's' 拍摄，'q' 退出。")

while True:
    ret, frame = camera.read()
    if not ret:
        continue
    cv2.imshow("Master Face Capture", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        encoding = encode_face(frame)
        if encoding is not None:
            os.makedirs("data", exist_ok=True)
            save_encoding(config['encoding_output_path'], encoding)
            print("✅ 主人脸部编码已保存！")
            break
        else:
            print("⚠️ 未检测到人脸，请重试。")
    elif key == ord('q'):
        print("❌ 退出采集")
        break

camera.release()
cv2.destroyAllWindows() 