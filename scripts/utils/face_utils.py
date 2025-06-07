"""
使用 face_recognition 进行编码提取。
提供人脸检测和特征编码的核心功能。
"""

import cv2
import numpy as np
import face_recognition
import logging
import yaml
from pathlib import Path

logger = logging.getLogger(__name__)

class FaceDetector:
    def __init__(self, config_path="config/settings.yaml"):
        """Initialize face detector with settings from config file."""
        self.config = self._load_config(config_path)
        self.face_recognition_config = self.config['face_recognition']

    def _load_config(self, config_path):
        """Load face recognition configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            logger.error(f"Failed to load face recognition config: {e}")
            raise

    def detect_faces(self, frame):
        """Detect faces in the given frame."""
        # Convert BGR to RGB
        rgb_frame = frame[:, :, ::-1]
        
        # Detect face locations
        face_locations = face_recognition.face_locations(
            rgb_frame,
            model=self.config['training']['face_encoding_model']
        )
        
        return face_locations

    def encode_face(self, frame):
        """Encode face features from the given frame."""
        rgb = frame[:, :, ::-1]  # BGR to RGB
        face_locations = face_recognition.face_locations(rgb)
        if not face_locations:
            return None
        return face_recognition.face_encodings(rgb, face_locations)[0]  # assume first

    def compare_faces(self, known_encoding, face_encoding):
        """Compare a known face encoding with a detected face encoding."""
        if face_encoding is None:
            return False
            
        # Compare faces using the configured tolerance
        matches = face_recognition.compare_faces(
            [known_encoding],
            face_encoding,
            tolerance=self.face_recognition_config['tolerance']
        )
        
        return matches[0]

    def draw_face_box(self, frame, face_location, label=None):
        """Draw a box around the detected face with optional label."""
        top, right, bottom, left = face_location
        
        # Draw rectangle
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        
        # Add label if provided
        if label:
            cv2.putText(
                frame,
                label,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (0, 255, 0),
                2
            )
        
        return frame 