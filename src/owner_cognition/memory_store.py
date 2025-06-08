import sqlite3
import json
from datetime import datetime
import logging
from pathlib import Path

class MemoryStore:
    def __init__(self, db_path="data/owner_memory.db"):
        """
        初始化记忆存储
        
        Args:
            db_path: 数据库文件路径
        """
        self.logger = logging.getLogger(__name__)
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化数据库
        self._init_database()
        
    def _init_database(self):
        """初始化数据库表结构"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 创建交互记录表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS interactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME NOT NULL,
                        emotion TEXT,
                        gesture TEXT,
                        distance REAL,
                        duration REAL,
                        bond_score REAL,
                        metadata TEXT
                    )
                ''')
                
                # 创建情绪历史表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS emotion_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME NOT NULL,
                        emotion TEXT NOT NULL,
                        confidence REAL NOT NULL
                    )
                ''')
                
                # 创建手势历史表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS gesture_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME NOT NULL,
                        gesture TEXT NOT NULL,
                        confidence REAL NOT NULL
                    )
                ''')
                
                # 创建距离历史表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS distance_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME NOT NULL,
                        distance REAL NOT NULL
                    )
                ''')
                
                conn.commit()
                self.logger.info("Database initialized successfully")
                
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {str(e)}")
            raise
            
    def store_interaction(self, interaction_data):
        """
        存储交互记录
        
        Args:
            interaction_data: 交互数据字典
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 准备数据
                timestamp = interaction_data.get('timestamp', datetime.now())
                emotion = interaction_data.get('emotion')
                gesture = interaction_data.get('gesture')
                distance = interaction_data.get('distance')
                duration = interaction_data.get('duration')
                bond_score = interaction_data.get('bond_score')
                metadata = json.dumps(interaction_data.get('metadata', {}))
                
                # 插入记录
                cursor.execute('''
                    INSERT INTO interactions 
                    (timestamp, emotion, gesture, distance, duration, bond_score, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (timestamp, emotion, gesture, distance, duration, bond_score, metadata))
                
                conn.commit()
                self.logger.debug(f"Stored interaction at {timestamp}")
                
        except Exception as e:
            self.logger.error(f"Failed to store interaction: {str(e)}")
            raise
            
    def store_emotion(self, emotion, confidence):
        """
        存储情绪记录
        
        Args:
            emotion: 情绪类型
            confidence: 置信度
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO emotion_history (timestamp, emotion, confidence)
                    VALUES (?, ?, ?)
                ''', (datetime.now(), emotion, confidence))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to store emotion: {str(e)}")
            raise
            
    def store_gesture(self, gesture, confidence):
        """
        存储手势记录
        
        Args:
            gesture: 手势类型
            confidence: 置信度
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO gesture_history (timestamp, gesture, confidence)
                    VALUES (?, ?, ?)
                ''', (datetime.now(), gesture, confidence))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to store gesture: {str(e)}")
            raise
            
    def store_distance(self, distance):
        """
        存储距离记录
        
        Args:
            distance: 距离值
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO distance_history (timestamp, distance)
                    VALUES (?, ?)
                ''', (datetime.now(), distance))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to store distance: {str(e)}")
            raise
            
    def get_recent_interactions(self, minutes=60):
        """
        获取最近的交互记录
        
        Args:
            minutes: 时间窗口（分钟）
            
        Returns:
            list: 交互记录列表
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM interactions
                    WHERE timestamp >= datetime('now', ?)
                    ORDER BY timestamp DESC
                ''', (f'-{minutes} minutes',))
                
                return cursor.fetchall()
                
        except Exception as e:
            self.logger.error(f"Failed to get recent interactions: {str(e)}")
            return []
            
    def get_emotion_trend(self, minutes=60):
        """
        获取情绪趋势
        
        Args:
            minutes: 时间窗口（分钟）
            
        Returns:
            dict: 情绪统计
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT emotion, COUNT(*) as count
                    FROM emotion_history
                    WHERE timestamp >= datetime('now', ?)
                    GROUP BY emotion
                ''', (f'-{minutes} minutes',))
                
                return dict(cursor.fetchall())
                
        except Exception as e:
            self.logger.error(f"Failed to get emotion trend: {str(e)}")
            return {}
            
    def get_gesture_trend(self, minutes=60):
        """
        获取手势趋势
        
        Args:
            minutes: 时间窗口（分钟）
            
        Returns:
            dict: 手势统计
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT gesture, COUNT(*) as count
                    FROM gesture_history
                    WHERE timestamp >= datetime('now', ?)
                    GROUP BY gesture
                ''', (f'-{minutes} minutes',))
                
                return dict(cursor.fetchall())
                
        except Exception as e:
            self.logger.error(f"Failed to get gesture trend: {str(e)}")
            return {}
            
    def get_distance_stats(self, minutes=60):
        """
        获取距离统计
        
        Args:
            minutes: 时间窗口（分钟）
            
        Returns:
            dict: 距离统计信息
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT 
                        AVG(distance) as avg_distance,
                        MIN(distance) as min_distance,
                        MAX(distance) as max_distance
                    FROM distance_history
                    WHERE timestamp >= datetime('now', ?)
                ''', (f'-{minutes} minutes',))
                
                row = cursor.fetchone()
                return {
                    'avg_distance': row[0],
                    'min_distance': row[1],
                    'max_distance': row[2]
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get distance stats: {str(e)}")
            return {} 