import cv2
import yaml
import logging
from pathlib import Path
from datetime import datetime

from face_recognition import FaceRecognition
from utils.camera import Camera
from utils.logger import setup_logger

def load_config():
    """加载配置文件"""
    with open('config/settings.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    # 加载配置
    config = load_config()
    
    # 设置日志
    logger = setup_logger(config['logging']['level'])
    logger.info("Starting face recognition system...")
    
    # 初始化摄像头
    camera = Camera(
        device_id=config['camera']['device_id'],
        width=config['camera']['width'],
        height=config['camera']['height'],
        fps=config['camera']['fps']
    )
    
    # 初始化人脸识别
    face_recognition = FaceRecognition(
        tolerance=config['face_recognition']['tolerance'],
        min_face_size=config['face_recognition']['min_face_size']
    )
    
    try:
        while True:
            # 获取图像
            frame = camera.get_frame()
            if frame is None:
                logger.error("Failed to capture frame")
                continue
                
            # 检测和识别人脸
            faces = face_recognition.detect_faces(frame)
            for face in faces:
                name = face_recognition.recognize_face(face)
                if name:
                    logger.info(f"Recognized: {name}")
                    
            # 显示结果
            cv2.imshow('Face Recognition', frame)
            
            # 按'q'退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        logger.info("System stopped by user")
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
    finally:
        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 