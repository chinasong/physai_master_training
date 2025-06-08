#!/usr/bin/env python3
import sys
import logging
from pathlib import Path
import numpy as np
from datetime import datetime, timedelta
import json

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.owner_cognition.memory_store import MemoryStore
from src.owner_cognition.bond_evaluator import BondEvaluator

class BondReinforcement:
    def __init__(self, db_path="data/owner_memory.db"):
        """
        初始化亲密关系强化系统
        
        Args:
            db_path: 数据库文件路径
        """
        self.logger = logging.getLogger(__name__)
        self.memory_store = MemoryStore(db_path)
        self.bond_evaluator = BondEvaluator()
        
        # 权重配置
        self.weights = {
            'emotion': 0.4,
            'gesture': 0.3,
            'frequency': 0.3
        }
        
        # 学习率
        self.learning_rate = 0.01
        
    def analyze_historical_data(self, days=7):
        """
        分析历史数据
        
        Args:
            days: 分析的天数
            
        Returns:
            dict: 分析结果
        """
        try:
            # 获取情绪趋势
            emotion_trend = self.memory_store.get_emotion_trend(minutes=days*24*60)
            
            # 获取手势趋势
            gesture_trend = self.memory_store.get_gesture_trend(minutes=days*24*60)
            
            # 获取距离统计
            distance_stats = self.memory_store.get_distance_stats(minutes=days*24*60)
            
            # 获取交互记录
            interactions = self.memory_store.get_recent_interactions(minutes=days*24*60)
            
            return {
                'emotion_trend': emotion_trend,
                'gesture_trend': gesture_trend,
                'distance_stats': distance_stats,
                'interaction_count': len(interactions)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to analyze historical data: {str(e)}")
            return {}
            
    def calculate_reward(self, analysis_data):
        """
        计算奖励值
        
        Args:
            analysis_data: 分析数据
            
        Returns:
            float: 奖励值
        """
        try:
            reward = 0.0
            
            # 情绪奖励
            emotion_trend = analysis_data.get('emotion_trend', {})
            positive_emotions = emotion_trend.get('happy', 0) + emotion_trend.get('surprise', 0)
            negative_emotions = emotion_trend.get('angry', 0) + emotion_trend.get('sad', 0)
            total_emotions = sum(emotion_trend.values()) or 1
            
            emotion_reward = (positive_emotions - negative_emotions) / total_emotions
            
            # 手势奖励
            gesture_trend = analysis_data.get('gesture_trend', {})
            positive_gestures = gesture_trend.get('wave', 0) + gesture_trend.get('come', 0)
            total_gestures = sum(gesture_trend.values()) or 1
            
            gesture_reward = positive_gestures / total_gestures
            
            # 交互频率奖励
            interaction_count = analysis_data.get('interaction_count', 0)
            frequency_reward = min(1.0, interaction_count / (7 * 24 * 60))  # 假设每天60次交互为满分
            
            # 计算总奖励
            reward = (
                self.weights['emotion'] * emotion_reward +
                self.weights['gesture'] * gesture_reward +
                self.weights['frequency'] * frequency_reward
            )
            
            return reward
            
        except Exception as e:
            self.logger.error(f"Failed to calculate reward: {str(e)}")
            return 0.0
            
    def update_weights(self, reward):
        """
        更新权重
        
        Args:
            reward: 奖励值
        """
        try:
            # 根据奖励值调整权重
            if reward > 0.7:  # 高奖励
                # 增加当前权重
                for key in self.weights:
                    self.weights[key] *= (1 + self.learning_rate)
            elif reward < 0.3:  # 低奖励
                # 减少当前权重
                for key in self.weights:
                    self.weights[key] *= (1 - self.learning_rate)
                    
            # 归一化权重
            total = sum(self.weights.values())
            for key in self.weights:
                self.weights[key] /= total
                
            self.logger.info(f"Updated weights: {self.weights}")
            
        except Exception as e:
            self.logger.error(f"Failed to update weights: {str(e)}")
            
    def save_weights(self, file_path="config/bond_weights.json"):
        """
        保存权重配置
        
        Args:
            file_path: 配置文件路径
        """
        try:
            weights_data = {
                'weights': self.weights,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(file_path, 'w') as f:
                json.dump(weights_data, f, indent=4)
                
            self.logger.info(f"Saved weights to {file_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save weights: {str(e)}")
            
    def load_weights(self, file_path="config/bond_weights.json"):
        """
        加载权重配置
        
        Args:
            file_path: 配置文件路径
        """
        try:
            with open(file_path, 'r') as f:
                weights_data = json.load(f)
                
            self.weights = weights_data['weights']
            self.logger.info(f"Loaded weights from {file_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to load weights: {str(e)}")
            
    def run_reinforcement(self, days=7):
        """
        运行强化学习过程
        
        Args:
            days: 分析的天数
        """
        try:
            # 分析历史数据
            analysis_data = self.analyze_historical_data(days)
            
            # 计算奖励
            reward = self.calculate_reward(analysis_data)
            self.logger.info(f"Calculated reward: {reward:.3f}")
            
            # 更新权重
            self.update_weights(reward)
            
            # 保存更新后的权重
            self.save_weights()
            
            return reward
            
        except Exception as e:
            self.logger.error(f"Failed to run reinforcement: {str(e)}")
            return 0.0

def main():
    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建强化学习系统
    reinforcement = BondReinforcement()
    
    # 运行强化学习
    reward = reinforcement.run_reinforcement()
    
    # 输出结果
    print(f"\nReinforcement Learning Results:")
    print(f"Final Reward: {reward:.3f}")
    print(f"Updated Weights:")
    for key, value in reinforcement.weights.items():
        print(f"  {key}: {value:.3f}")

if __name__ == "__main__":
    main() 