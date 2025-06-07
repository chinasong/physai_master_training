"""
负责保存与读取编码文件。
提供人脸编码数据的持久化存储功能。
"""

import pickle
import cv2
import logging
import yaml
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class StorageManager:
    def __init__(self, config_path="config/settings.yaml"):
        """Initialize storage manager with settings from config file."""
        self.config = self._load_config(config_path)
        self._setup_directories()

    def _load_config(self, config_path):
        """Load storage configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            logger.error(f"Failed to load storage config: {e}")
            raise

    def _setup_directories(self):
        """Create necessary directories if they don't exist."""
        # Create data directory
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Create captured faces directory
        self.faces_dir = self.data_dir / "captured_faces"
        self.faces_dir.mkdir(exist_ok=True)
        
        # Create logs directory
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)

    def save_face_encoding(self, encoding, filename="master_face_encoding.pkl"):
        """Save face encoding to file."""
        try:
            filepath = self.data_dir / filename
            with open(filepath, 'wb') as f:
                pickle.dump(encoding, f)
            logger.info(f"Face encoding saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save face encoding: {e}")
            raise

    def load_face_encoding(self, filename="master_face_encoding.pkl"):
        """Load face encoding from file."""
        try:
            filepath = self.data_dir / filename
            if not filepath.exists():
                logger.warning(f"No face encoding found at {filepath}")
                return None
                
            with open(filepath, 'rb') as f:
                encoding = pickle.load(f)
            logger.info(f"Face encoding loaded from {filepath}")
            return encoding
        except Exception as e:
            logger.error(f"Failed to load face encoding: {e}")
            raise

    def save_face_image(self, frame, face_location):
        """Save captured face image."""
        if not self.config['logging']['save_images']:
            return
            
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"face_{timestamp}.jpg"
            filepath = self.faces_dir / filename
            
            # Extract face region
            top, right, bottom, left = face_location
            face_image = frame[top:bottom, left:right]
            
            # Save image
            cv2.imwrite(str(filepath), face_image)
            logger.info(f"Face image saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save face image: {e}")
            raise

    def log_training(self, message):
        """Log training message to file."""
        try:
            log_file = self.logs_dir / "training_log.txt"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_file, 'a') as f:
                f.write(f"[{timestamp}] {message}\n")
        except Exception as e:
            logger.error(f"Failed to write to training log: {e}")
            raise

def save_encoding(filepath, encoding):
    with open(filepath, 'wb') as f:
        pickle.dump(encoding, f)

def load_encoding(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f) 