"""
食物类
Food Class
"""
import math
import random
from typing import Tuple, List, Optional

from .config import GRID_WIDTH, GRID_HEIGHT, COLORS


class Food:
    """食物类"""

    def __init__(self):
        """初始化食物"""
        self.position: Tuple[int, int] = (0, 0)
        self._color: Optional[Tuple[int, int, int]] = None
        self._glow_color: Optional[Tuple[int, int, int]] = None
        self.animation_offset = 0

    @property
    def color(self) -> Tuple[int, int, int]:
        """获取食物颜色"""
        return self._color if self._color else COLORS['food']

    @color.setter
    def color(self, value: Tuple[int, int, int]):
        """设置食物颜色"""
        self._color = value

    @property
    def glow_color(self) -> Tuple[int, int, int]:
        """获取食物光晕颜色"""
        if self._glow_color:
            return self._glow_color
        # 默认光晕颜色比主体颜色亮一些
        base = self.color
        return (
            min(base[0] + 50, 255),
            min(base[1] + 50, 255),
            min(base[2] + 50, 255)
        )

    def set_colors(self, food_color: Tuple[int, int, int],
                   glow_color: Tuple[int, int, int] = None):
        """
        设置食物颜色

        Args:
            food_color: 食物颜色
            glow_color: 光晕颜色，为空则自动计算
        """
        self._color = food_color
        self._glow_color = glow_color

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