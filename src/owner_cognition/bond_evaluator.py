import numpy as np
from datetime import datetime, timedelta
import logging

class BondEvaluator:
    def __init__(self):
        """初始化亲密关系评估器"""
        self.logger = logging.getLogger(__name__)
        self.interaction_history = []
        self.bond_score = 0.0
        
    def update_interaction(self, interaction_data):
        """
        更新交互记录
        
        Args:
            interaction_data: 交互数据字典，包含：
                - emotion: 情绪类型
                - gesture: 手势类型
                - distance: 距离
                - duration: 交互时长
        """
        timestamp = datetime.now()
        interaction_data['timestamp'] = timestamp
        
        self.interaction_history.append(interaction_data)
        
        # 保持历史记录在合理范围内
        if len(self.interaction_history) > 1000:
            self.interaction_history = self.interaction_history[-1000:]
            
    def calculate_emotion_score(self, window_minutes=60):
        """
        计算情绪得分
        
        Args:
            window_minutes: 时间窗口（分钟）
            
        Returns:
            float: 情绪得分（0-1）
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
            
        # 情绪权重
        emotion_weights = {
            'happy': 1.0,
            'surprise': 0.8,
            'neutral': 0.5,
            'sad': 0.3,
            'angry': 0.1,
            'fear': 0.1,
            'disgust': 0.1
        }
        
        # 计算加权平均
        total_weight = 0
        weighted_sum = 0
        
        for interaction in recent_interactions:
            if 'emotion' in interaction:
                emotion = interaction['emotion']
                weight = emotion_weights.get(emotion, 0.5)
                total_weight += weight
                weighted_sum += weight
                
        return weighted_sum / total_weight if total_weight > 0 else 0.0
        
    def calculate_gesture_score(self, window_minutes=60):
        """
        计算手势得分
        
        Args:
            window_minutes: 时间窗口（分钟）
            
        Returns:
            float: 手势得分（0-1）
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
            
        # 手势权重
        gesture_weights = {
            'wave': 1.0,
            'come': 0.9,
            'point': 0.7,
            'stop': 0.5,
            'none': 0.0
        }
        
        # 计算加权平均
        total_weight = 0
        weighted_sum = 0
        
        for interaction in recent_interactions:
            if 'gesture' in interaction:
                gesture = interaction['gesture']
                weight = gesture_weights.get(gesture, 0.0)
                total_weight += weight
                weighted_sum += weight
                
        return weighted_sum / total_weight if total_weight > 0 else 0.0
        
    def calculate_interaction_frequency(self, window_minutes=60):
        """
        计算交互频率
        
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
        
    def evaluate_bond(self, window_minutes=60):
        """
        评估亲密关系强度
        
        Args:
            window_minutes: 时间窗口（分钟）
            
        Returns:
            float: 亲密关系得分（0-1）
        """
        # 计算各项得分
        emotion_score = self.calculate_emotion_score(window_minutes)
        gesture_score = self.calculate_gesture_score(window_minutes)
        frequency = self.calculate_interaction_frequency(window_minutes)
        
        # 频率得分（假设每分钟5次为满分）
        frequency_score = min(1.0, frequency / 5.0)
        
        # 综合得分
        self.bond_score = (
            0.4 * emotion_score +
            0.3 * gesture_score +
            0.3 * frequency_score
        )
        
        return self.bond_score
        
    def get_bond_level(self):
        """
        获取亲密关系等级
        
        Returns:
            str: 亲密关系等级描述
        """
        if self.bond_score >= 0.8:
            return "非常亲密"
        elif self.bond_score >= 0.6:
            return "亲密"
        elif self.bond_score >= 0.4:
            return "一般"
        elif self.bond_score >= 0.2:
            return "疏远"
        else:
            return "陌生" 