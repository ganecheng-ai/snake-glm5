"""
贪吃蛇游戏测试
Snake Game Tests
"""
import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from snake_game.snake import Snake
from snake_game.food import Food
from snake_game.config import (
    GRID_WIDTH, GRID_HEIGHT,
    DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT,
    INITIAL_SNAKE_LENGTH
)


class TestSnake(unittest.TestCase):
    """蛇类测试"""

    def setUp(self):
        """测试前准备"""
        self.snake = Snake()

    def test_initial_length(self):
        """测试初始长度"""
        self.assertEqual(len(self.snake), INITIAL_SNAKE_LENGTH)

    def test_initial_direction(self):
        """测试初始方向"""
        self.assertEqual(self.snake.direction, DIRECTION_RIGHT)

    def test_initial_alive(self):
        """测试初始存活状态"""
        self.assertTrue(self.snake.alive)

    def test_move(self):
        """测试移动"""
        initial_head = self.snake.head
        self.assertTrue(self.snake.move())
        # 蛇头应该向右移动一格
        expected_head = (initial_head[0] + 1, initial_head[1])
        self.assertEqual(self.snake.head, expected_head)

    def test_change_direction(self):
        """测试改变方向"""
        self.snake.change_direction(DIRECTION_UP)
        self.snake.update_direction()
        self.assertEqual(self.snake.direction, DIRECTION_UP)

    def test_no_180_turn(self):
        """测试不能180度转弯"""
        self.snake.direction = DIRECTION_RIGHT
        self.snake.change_direction(DIRECTION_LEFT)
        self.snake.update_direction()
        # 方向不应该改变
        self.assertEqual(self.snake.direction, DIRECTION_RIGHT)

    def test_grow(self):
        """测试增长"""
        initial_length = len(self.snake)
        self.snake.grow()
        self.snake.move()
        self.assertEqual(len(self.snake), initial_length + 1)

    def test_wall_collision(self):
        """测试撞墙"""
        # 将蛇移到右边界
        while self.snake.head[0] < GRID_WIDTH - 1:
            self.snake.move()

        # 下一次移动应该撞墙
        self.assertFalse(self.snake.move())
        self.assertFalse(self.snake.alive)

    def test_self_collision(self):
        """测试撞自己"""
        # 构造一个会撞到自己的情况
        self.snake.body = [(5, 5), (5, 4), (5, 3), (6, 3), (6, 4)]
        self.snake.direction = DIRECTION_UP
        self.snake.next_direction = DIRECTION_UP
        self.snake.move()
        # 现在蛇头在 (5, 4)，下一次向左移动会撞到自己
        self.snake.change_direction(DIRECTION_LEFT)
        self.snake.move()
        self.snake.change_direction(DIRECTION_DOWN)
        self.snake.move()
        self.snake.change_direction(DIRECTION_RIGHT)
        result = self.snake.move()
        # 可能会撞到自己或撞墙
        self.assertFalse(self.snake.alive)

    def test_reset(self):
        """测试重置"""
        # 先改变蛇的状态
        self.snake.move()
        self.snake.move()
        self.snake.grow(3)

        # 重置
        self.snake.reset()

        # 检查是否恢复初始状态
        self.assertEqual(len(self.snake), INITIAL_SNAKE_LENGTH)
        self.assertTrue(self.snake.alive)

    def test_body_colors(self):
        """测试蛇身颜色"""
        colors = self.snake.get_body_colors()
        self.assertEqual(len(colors), len(self.snake))
        # 蛇头颜色应该更亮
        head_color = colors[0]
        tail_color = colors[-1]
        # 蛇头的绿色分量应该更大
        self.assertGreater(head_color[1], tail_color[1])


class TestFood(unittest.TestCase):
    """食物类测试"""

    def setUp(self):
        """测试前准备"""
        self.food = Food()

    def test_spawn_in_bounds(self):
        """测试食物在边界内生成"""
        snake_body = [(5, 5)]
        for _ in range(100):  # 测试多次生成
            self.food.spawn(snake_body)
            x, y = self.food.position
            self.assertGreaterEqual(x, 0)
            self.assertLess(x, GRID_WIDTH)
            self.assertGreaterEqual(y, 0)
            self.assertLess(y, GRID_HEIGHT)

    def test_spawn_not_on_snake(self):
        """测试食物不会生成在蛇身上"""
        snake_body = [(x, 5) for x in range(10)]
        for _ in range(100):  # 测试多次生成
            self.food.spawn(snake_body)
            self.assertNotIn(self.food.position, snake_body)

    def test_pulse_scale(self):
        """测试脉动缩放"""
        scale = self.food.pulse_scale
        self.assertGreaterEqual(scale, 0.8)
        self.assertLessEqual(scale, 1.0)

    def test_animation_update(self):
        """测试动画更新"""
        initial_offset = self.food.animation_offset
        self.food.update_animation()
        self.assertEqual(
            self.food.animation_offset,
            (initial_offset + 1) % 10
        )


class TestConfig(unittest.TestCase):
    """配置测试"""

    def test_grid_dimensions(self):
        """测试网格尺寸"""
        from snake_game.config import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE

        # 确保窗口尺寸是网格大小的整数倍
        self.assertEqual(WINDOW_WIDTH % GRID_SIZE, 0)
        self.assertEqual(WINDOW_HEIGHT % GRID_SIZE, 0)

    def test_speed_limits(self):
        """测试速度限制"""
        from snake_game.config import INITIAL_SPEED, MAX_SPEED

        self.assertGreater(INITIAL_SPEED, 0)
        self.assertGreater(MAX_SPEED, INITIAL_SPEED)

    def test_directions(self):
        """测试方向向量"""
        # 方向向量应该是单位向量
        for direction in [DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT]:
            dx, dy = direction
            self.assertEqual(abs(dx) + abs(dy), 1)


if __name__ == '__main__':
    unittest.main()