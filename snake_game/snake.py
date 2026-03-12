"""
贪吃蛇类
Snake Class
"""
import random
from typing import List, Tuple, Optional

from .config import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT,
    INITIAL_SNAKE_LENGTH, INITIAL_SNAKE_POSITION,
    DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT,
    COLORS
)


class Snake:
    """贪吃蛇类"""

    def __init__(self):
        """初始化蛇"""
        self.reset()

    def reset(self):
        """重置蛇到初始状态"""
        x, y = INITIAL_SNAKE_POSITION
        self.body: List[Tuple[int, int]] = [
            (x - i, y) for i in range(INITIAL_SNAKE_LENGTH)
        ]
        self.direction = DIRECTION_RIGHT
        self.next_direction = DIRECTION_RIGHT
        self.grow_pending = 0
        self.alive = True

    @property
    def head(self) -> Tuple[int, int]:
        """获取蛇头位置"""
        return self.body[0]

    def change_direction(self, new_direction: Tuple[int, int]):
        """
        改变方向（防止180度转弯）

        Args:
            new_direction: 新方向 (dx, dy)
        """
        dx, dy = new_direction
        current_dx, current_dy = self.direction

        # 防止180度转弯
        if (dx, dy) == (-current_dx, -current_dy):
            return

        self.next_direction = new_direction

    def update_direction(self):
        """更新方向"""
        self.direction = self.next_direction

    def move(self) -> bool:
        """
        移动蛇

        Returns:
            bool: 是否成功移动（未撞墙或自身）
        """
        if not self.alive:
            return False

        dx, dy = self.direction
        new_head = (self.head[0] + dx, self.head[1] + dy)

        # 检查是否撞墙
        if not self._is_valid_position(new_head):
            self.alive = False
            return False

        # 检查是否撞到自己
        if new_head in self.body:
            self.alive = False
            return False

        # 移动蛇身
        self.body.insert(0, new_head)

        # 是否需要增长
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

        return True

    def grow(self, amount: int = 1):
        """
        增加蛇的长度

        Args:
            amount: 增加的长度
        """
        self.grow_pending += amount

    def _is_valid_position(self, pos: Tuple[int, int]) -> bool:
        """
        检查位置是否有效

        Args:
            pos: 位置坐标

        Returns:
            bool: 位置是否在边界内
        """
        x, y = pos
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

    def get_body_colors(self) -> List[Tuple[int, int, int]]:
        """
        获取蛇身各部分的颜色（渐变效果）

        Returns:
            List[Tuple[int, int, int]]: 颜色列表
        """
        colors = []
        body_len = len(self.body)

        for i in range(body_len):
            # 计算渐变色
            ratio = i / max(body_len - 1, 1)

            # 从蛇头颜色渐变到蛇尾颜色
            head_color = COLORS['snake_head']
            tail_color = COLORS['snake_body']

            r = int(head_color[0] + (tail_color[0] - head_color[0]) * ratio)
            g = int(head_color[1] + (tail_color[1] - head_color[1]) * ratio)
            b = int(head_color[2] + (tail_color[2] - head_color[2]) * ratio)

            colors.append((r, g, b))

        return colors

    def __len__(self) -> int:
        """获取蛇的长度"""
        return len(self.body)

    def __contains__(self, pos: Tuple[int, int]) -> bool:
        """检查位置是否在蛇身上"""
        return pos in self.body