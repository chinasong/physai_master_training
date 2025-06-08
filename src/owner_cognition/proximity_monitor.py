import numpy as np
from datetime import datetime, timedelta
import logging

class ProximityMonitor:
    def __init__(self, max_distance=5.0, min_distance=0.5):
        """
        初始化距离监控器
        
        Args:
            max_distance: 最大有效距离（米）
            min_distance: 最小安全距离（米）
        """
        self.logger = logging.getLogger(__name__)
        self.max_distance = max_distance
        self.min_distance = min_distance
        self.interaction_history = []
        self.current_distance = None
        
    def update_distance(self, distance):
        """
        更新当前距离
        
        Args:
            distance: 当前距离（米）
        """
        self.current_distance = distance
        timestamp = datetime.now()
        
        self.interaction_history.append({
            'distance': distance,
            'timestamp': timestamp
        })
        
        # 保持历史记录在合理范围内
        if len(self.interaction_history) > 1000:
            self.interaction_history = self.interaction_history[-1000:]
            
    def get_interaction_frequency(self, window_minutes=60):
        """
        获取交互频率
        
        Args:
            window_minutes: 时间窗口（分钟）
            
        Returns:
            float: 每分钟交互次数
        """
        if not self.interaction_history:
            return 0.0
            
        window_start = datetime.now() - timedelta(minutes=window_minutes)
        recent_interactions = [
            record for record in self.interaction_history
            if record['timestamp'] >= window_start
        ]
        
        if not recent_interactions:
            return 0.0
            
        return len(recent_interactions) / window_minutes
        
    def get_average_distance(self, window_minutes=60):
        """
        获取平均距离
        
        Args:
            window_minutes: 时间窗口（分钟）
            
        Returns:
            float: 平均距离（米）
        """
        if not self.interaction_history:
            return None
            
        window_start = datetime.now() - timedelta(minutes=window_minutes)
        recent_distances = [
            record['distance'] for record in self.interaction_history
            if record['timestamp'] >= window_start
        ]
        
        if not recent_distances:
            return None
            
        return np.mean(recent_distances)
        
    def is_in_interaction_range(self):
        """
        检查是否在交互范围内
        
        Returns:
            bool: 是否在有效交互范围内
        """
        if self.current_distance is None:
            return False
            
        return self.min_distance <= self.current_distance <= self.max_distance
        
    def get_proximity_score(self, window_minutes=60):
        """
        计算亲近度得分
        
        Args:
            window_minutes: 时间窗口（分钟）
            
        Returns:
            float: 亲近度得分（0-1）
        """
        if not self.interaction_history:
            return 0.0
            
        # 计算距离得分
        avg_distance = self.get_average_distance(window_minutes)
        if avg_distance is None:
            return 0.0
            
        distance_score = 1.0 - (avg_distance / self.max_distance)
        distance_score = max(0.0, min(1.0, distance_score))
        
        # 计算交互频率得分
        frequency = self.get_interaction_frequency(window_minutes)
        frequency_score = min(1.0, frequency / 10.0)  # 假设每分钟10次为满分
        
        # 综合得分
        return 0.6 * distance_score + 0.4 * frequency_score 