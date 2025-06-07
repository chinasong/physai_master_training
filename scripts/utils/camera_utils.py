import cv2
import yaml
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class Camera:
    def __init__(self, config_path="config/settings.yaml"):
        """Initialize camera with settings from config file."""
        self.config = self._load_config(config_path)
        self.camera = None
        self._initialize_camera()

    def _load_config(self, config_path):
        """Load camera configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config['camera']
        except Exception as e:
            logger.error(f"Failed to load camera config: {e}")
            raise

    def _initialize_camera(self):
        """Initialize camera with configured settings."""
        try:
            self.camera = cv2.VideoCapture(self.config['device_id'])
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.config['width'])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config['height'])
            self.camera.set(cv2.CAP_PROP_FPS, self.config['fps'])
            
            if not self.camera.isOpened():
                raise RuntimeError("Failed to open camera")
            
            logger.info("Camera initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            raise

    def capture_frame(self):
        """Capture a single frame from the camera."""
        if not self.camera:
            raise RuntimeError("Camera not initialized")
        
        ret, frame = self.camera.read()
        if not ret:
            raise RuntimeError("Failed to capture frame")
        
        return frame

    def release(self):
        """Release camera resources."""
        if self.camera:
            self.camera.release()
            logger.info("Camera released")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

def get_camera_stream(index=0):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise RuntimeError("Cannot open camera")
    return cap 