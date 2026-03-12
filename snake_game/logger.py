"""
日志系统模块
Logger Module
"""
import logging
import os
from datetime import datetime
from typing import Optional


class GameLogger:
    """游戏日志记录器"""

    _instance: Optional['GameLogger'] = None
    _initialized: bool = False

    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化日志系统"""
        if self._initialized:
            return

        self._initialized = True
        self.logger = logging.getLogger('SnakeGame')
        self.logger.setLevel(logging.DEBUG)

        # 清除已有的处理器
        self.logger.handlers.clear()

        # 创建日志目录
        self.log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(self.log_dir, exist_ok=True)

        # 日志文件路径
        self.log_file = os.path.join(
            self.log_dir,
            f'snake_game_{datetime.now().strftime("%Y%m%d")}.log'
        )

        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 文件处理器
        file_handler = logging.FileHandler(
            self.log_file,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # 控制台处理器（仅警告及以上级别）
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # 记录初始化日志
        self.info("日志系统初始化完成")
        self.info(f"日志文件路径: {self.log_file}")

    def debug(self, message: str):
        """记录调试信息"""
        self.logger.debug(message)

    def info(self, message: str):
        """记录一般信息"""
        self.logger.info(message)

    def warning(self, message: str):
        """记录警告信息"""
        self.logger.warning(message)

    def error(self, message: str):
        """记录错误信息"""
        self.logger.error(message)

    def critical(self, message: str):
        """记录严重错误"""
        self.logger.critical(message)

    def log_game_start(self, score: int = 0, speed: int = 0):
        """记录游戏开始"""
        self.info(f"游戏开始 - 初始速度: {speed}")

    def log_game_over(self, score: int, snake_length: int, high_score: int):
        """记录游戏结束"""
        self.info(
            f"游戏结束 - 得分: {score}, 蛇长度: {snake_length}, 最高分: {high_score}"
        )

    def log_food_eaten(self, score: int, position: tuple):
        """记录吃到食物"""
        self.debug(f"吃到食物 - 位置: {position}, 当前得分: {score}")

    def log_collision(self, collision_type: str, position: tuple):
        """记录碰撞事件"""
        self.info(f"碰撞事件 - 类型: {collision_type}, 位置: {position}")

    def log_direction_change(self, direction: str):
        """记录方向改变"""
        self.debug(f"方向改变: {direction}")

    def log_pause(self):
        """记录游戏暂停"""
        self.info("游戏暂停")

    def log_resume(self):
        """记录游戏恢复"""
        self.info("游戏恢复")

    def log_state_change(self, old_state: str, new_state: str):
        """记录状态变化"""
        self.debug(f"状态变化: {old_state} -> {new_state}")

    def log_error(self, error_type: str, error_msg: str):
        """记录错误"""
        self.error(f"{error_type}: {error_msg}")

    def get_log_file_path(self) -> str:
        """获取日志文件路径"""
        return self.log_file


# 全局日志实例
_logger: Optional[GameLogger] = None


def get_logger() -> GameLogger:
    """获取日志实例"""
    global _logger
    if _logger is None:
        _logger = GameLogger()
    return _logger