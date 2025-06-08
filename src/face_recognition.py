import cv2
import numpy as np
import face_recognition
import os
from pathlib import Path
import logging
from datetime import datetime

class FaceRecognition:
    def __init__(self, tolerance=0.6, min_face_size=20):
        """
        初始化人脸识别系统
        
        Args:
            tolerance (float): 人脸识别容差（越小越严格）
            min_face_size (int): 最小人脸尺寸
        """
        self.tolerance = tolerance
        self.min_face_size = min_face_size
        self.known_face_encodings = []
        self.known_face_names = []
        self.logger = logging.getLogger(__name__)
        
        # 加载已知人脸
        self._load_known_faces()
        
    def _load_known_faces(self):
        """加载已知人脸数据"""
        faces_dir = Path("data/faces")
        if not faces_dir.exists():
            self.logger.warning("No faces directory found")
            return
            
        for person_dir in faces_dir.iterdir():
            if not person_dir.is_dir():
                continue
                
            person_name = person_dir.name
            face_files = list(person_dir.glob("*.jpg"))
            
            if not face_files:
                self.logger.warning(f"No face images found for {person_name}")
                continue
                
            # 加载该人的所有面部编码
            for face_file in face_files:
                try:
                    image = face_recognition.load_image_file(str(face_file))
                    face_encodings = face_recognition.face_encodings(image)
                    
                    if face_encodings:
                        self.known_face_encodings.append(face_encodings[0])
                        self.known_face_names.append(person_name)
                except Exception as e:
                    self.logger.error(f"Error loading face {face_file}: {str(e)}")
                    
        self.logger.info(f"Loaded {len(self.known_face_names)} known faces")
        
    def detect_faces(self, frame):
        """
        检测图像中的人脸
        
        Args:
            frame: 输入图像
            
        Returns:
            list: 检测到的人脸列表
        """
        # 转换为RGB格式
        rgb_frame = frame[:, :, ::-1]
        
        # 检测人脸位置
        face_locations = face_recognition.face_locations(
            rgb_frame,
            model="hog",  # 使用HOG模型，更快但不太准确
            number_of_times_to_upsample=1
        )
        
        # 获取人脸编码
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        # 返回人脸信息
        faces = []
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            faces.append({
                'location': (top, right, bottom, left),
                'encoding': face_encoding
            })
            
        return faces
        
    def recognize_face(self, face):
        """
        识别人脸
        
        Args:
            face: 包含位置和编码的人脸信息
            
        Returns:
            str: 识别出的人名，如果未识别则返回None
        """
        if not self.known_face_encodings:
            return None
            
        # 计算与已知人脸的距离
        face_distances = face_recognition.face_distance(
            self.known_face_encodings,
            face['encoding']
        )
        
        # 找到最匹配的人脸
        best_match_index = np.argmin(face_distances)
        if face_distances[best_match_index] <= self.tolerance:
            return self.known_face_names[best_match_index]
            
        return None
        
    def add_face(self, frame, name):
        """
        添加新的人脸
        
        Args:
            frame: 包含人脸的图像
            name: 人名
            
        Returns:
            bool: 是否成功添加
        """
        try:
            # 检测人脸
            rgb_frame = frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_frame)
            
            if not face_locations:
                self.logger.warning("No face detected in the image")
                return False
                
            # 获取人脸编码
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            if not face_encodings:
                self.logger.warning("Failed to encode face")
                return False
                
            # 保存人脸图像
            face_dir = Path(f"data/faces/{name}")
            face_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            face_path = face_dir / f"{timestamp}.jpg"
            
            # 裁剪并保存人脸图像
            top, right, bottom, left = face_locations[0]
            face_image = frame[top:bottom, left:right]
            cv2.imwrite(str(face_path), face_image)
            
            # 添加到已知人脸列表
            self.known_face_encodings.append(face_encodings[0])
            self.known_face_names.append(name)
            
            self.logger.info(f"Added new face for {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding face: {str(e)}")
            return False 