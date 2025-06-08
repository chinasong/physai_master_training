import cv2
import logging

class Camera:
    def __init__(self, device_id=0, width=640, height=480, fps=30):
        """
        初始化摄像头
        
        Args:
            device_id (int): 摄像头设备ID
            width (int): 图像宽度
            height (int): 图像高度
            fps (int): 帧率
        """
        self.device_id = device_id
        self.width = width
        self.height = height
        self.fps = fps
        self.logger = logging.getLogger(__name__)
        
        # 初始化摄像头
        self.cap = cv2.VideoCapture(device_id)
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open camera {device_id}")
            
        # 设置摄像头参数
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        
        self.logger.info(f"Camera initialized: {width}x{height} @ {fps}fps")
        
    def get_frame(self):
        """
        获取一帧图像
        
        Returns:
            numpy.ndarray: 图像数据，如果失败则返回None
        """
        ret, frame = self.cap.read()
        if not ret:
            self.logger.error("Failed to capture frame")
            return None
            
        return frame
        
    def release(self):
        """释放摄像头资源"""
        if self.cap is not None:
            self.cap.release()
            self.logger.info("Camera released") 