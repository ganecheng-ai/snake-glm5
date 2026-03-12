"""
食物类
Food Class
"""
import math
import random
from typing import Tuple, List

from .config import GRID_WIDTH, GRID_HEIGHT, COLORS


class Food:
    """食物类"""

    def __init__(self):
        """初始化食物"""
        self.position: Tuple[int, int] = (0, 0)
        self.color = COLORS['food']
        self.animation_offset = 0

    def spawn(self, snake_body: List[Tuple[int, int]]):
        """
        在随机位置生成食物

        Args:
            snake_body: 蛇身位置列表，用于避免在蛇身上生成食物
        """
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            pos = (x, y)

            # 确保不在蛇身上
            if pos not in snake_body:
                self.position = pos
                break

    def update_animation(self):
        """更新动画效果"""
        self.animation_offset = (self.animation_offset + 1) % 10

    @property
    def pulse_scale(self) -> float:
        """
        获取脉动缩放比例

        Returns:
            float: 缩放比例 (0.8 - 1.0)
        """
        # 使用正弦波实现平滑脉动
        return 0.9 + 0.1 * math.sin(self.animation_offset * 0.628)