"""
贪吃蛇游戏主逻辑
Snake Game Main Logic
"""
import sys
from typing import Optional

import pygame

from .config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    INITIAL_SPEED, SPEED_INCREMENT, MAX_SPEED,
    STATE_MENU, STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER,
    DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT,
    STATE_NAMES, GRID_WIDTH, GRID_HEIGHT
)
from .snake import Snake
from .food import Food
from .ui import UI
from .logger import get_logger


class Game:
    """贪吃蛇游戏类"""

    def __init__(self):
        """初始化游戏"""
        # 初始化日志系统
        self.logger = get_logger()
        self.logger.info("正在初始化游戏...")

        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)

        # 创建窗口
        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.logger.info(f"窗口创建成功: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        # 游戏组件
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.ui = UI(self.screen)

        # 游戏状态
        self.state = STATE_MENU
        self.score = 0
        self.speed = INITIAL_SPEED
        self.high_score = 0

        # 计时器
        self.last_move_time = 0

        # 音效（可选）
        self.sound_enabled = False
        self._init_sounds()

        self.logger.info("游戏初始化完成")

    def _init_sounds(self):
        """初始化音效"""
        try:
            pygame.mixer.init()
            self.sound_enabled = True
            self.logger.info("音效系统初始化成功")
        except Exception as e:
            self.sound_enabled = False
            self.logger.warning(f"音效系统初始化失败: {e}")

    def reset(self):
        """重置游戏状态"""
        self.logger.info("重置游戏状态")
        self.snake.reset()
        self.food.spawn(self.snake.body)
        self.score = 0
        self.speed = INITIAL_SPEED
        old_state = self.state
        self.state = STATE_PLAYING
        self.last_move_time = pygame.time.get_ticks()
        self.logger.log_state_change(STATE_NAMES.get(old_state, str(old_state)), '游戏中')
        self.logger.log_game_start(self.score, self.speed)

    def handle_events(self) -> bool:
        """
        处理输入事件

        Returns:
            bool: 游戏是否继续运行
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.logger.info("用户请求退出游戏")
                return False

            if event.type == pygame.KEYDOWN:
                # 菜单状态
                if self.state == STATE_MENU:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.reset()
                    elif event.key == pygame.K_q:
                        self.logger.info("用户在菜单界面按Q退出")
                        return False

                # 游戏中状态
                elif self.state == STATE_PLAYING:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.snake.change_direction(DIRECTION_UP)
                        self.logger.log_direction_change('上')
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.snake.change_direction(DIRECTION_DOWN)
                        self.logger.log_direction_change('下')
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.snake.change_direction(DIRECTION_LEFT)
                        self.logger.log_direction_change('左')
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.snake.change_direction(DIRECTION_RIGHT)
                        self.logger.log_direction_change('右')
                    elif event.key == pygame.K_ESCAPE:
                        self.state = STATE_PAUSED
                        self.logger.log_pause()
                    elif event.key == pygame.K_q:
                        self.logger.info("用户在游戏中按Q退出")
                        return False

                # 暂停状态
                elif self.state == STATE_PAUSED:
                    if event.key == pygame.K_ESCAPE:
                        self.state = STATE_PLAYING
                        self.last_move_time = pygame.time.get_ticks()
                        self.logger.log_resume()

                # 游戏结束状态
                elif self.state == STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_q:
                        self.logger.info("用户在游戏结束界面按Q退出")
                        return False

        return True

    def update(self):
        """更新游戏状态"""
        if self.state != STATE_PLAYING:
            return

        # 检查是否到移动时间
        current_time = pygame.time.get_ticks()
        move_interval = 1000 // self.speed

        if current_time - self.last_move_time < move_interval:
            return

        self.last_move_time = current_time

        # 更新蛇的方向
        self.snake.update_direction()

        # 移动蛇
        if not self.snake.move():
            # 检查碰撞类型
            head = self.snake.head
            dx, dy = self.snake.direction
            new_head = (head[0] + dx, head[1] + dy)

            # 判断是撞墙还是撞自己
            x, y = new_head
            if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
                self.logger.log_collision('撞墙', new_head)
            else:
                self.logger.log_collision('撞自己', new_head)

            self.state = STATE_GAME_OVER
            if self.score > self.high_score:
                self.high_score = self.score
                self.logger.info(f"新最高分: {self.high_score}")
            self.logger.log_game_over(self.score, len(self.snake), self.high_score)
            return

        # 检查是否吃到食物
        if self.snake.head == self.food.position:
            self.snake.grow()
            self.score += 10
            self.logger.log_food_eaten(self.score, self.food.position)
            self.food.spawn(self.snake.body)

            # 增加速度
            if self.speed < MAX_SPEED:
                self.speed += SPEED_INCREMENT
                self.logger.debug(f"速度增加至: {self.speed}")

    def render(self):
        """渲染游戏画面"""
        # 绘制背景
        self.ui.draw_background()
        self.ui.draw_border()

        # 绘制食物
        self.food.update_animation()
        self.ui.draw_food(
            self.food.position,
            self.food.pulse_scale
        )

        # 绘制蛇
        self.ui.draw_snake(
            self.snake.body,
            self.snake.get_body_colors()
        )

        # 绘制分数
        self.ui.draw_score(self.score)

        # 绘制界面
        if self.state == STATE_MENU:
            self.ui.draw_menu()
        elif self.state == STATE_PAUSED:
            self.ui.draw_pause()
        elif self.state == STATE_GAME_OVER:
            self.ui.draw_game_over(self.score)

        # 更新显示
        pygame.display.flip()

    def run(self):
        """运行游戏主循环"""
        running = True
        self.logger.info("游戏主循环开始")

        while running:
            running = self.handle_events()
            self.update()
            self.render()

            # 控制帧率
            self.clock.tick(60)

        self.logger.info("游戏退出")
        pygame.quit()
        sys.exit()

    def get_state_info(self) -> dict:
        """
        获取游戏状态信息

        Returns:
            dict: 游戏状态信息
        """
        return {
            'state': self.state,
            'score': self.score,
            'high_score': self.high_score,
            'speed': self.speed,
            'snake_length': len(self.snake),
            'snake_alive': self.snake.alive
        }