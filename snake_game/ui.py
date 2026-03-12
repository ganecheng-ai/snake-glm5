"""
用户界面渲染
User Interface Rendering
"""
import os
from typing import Tuple, Optional

import pygame

from .config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE,
    COLORS, FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL,
    STATE_MENU, STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER
)


class UI:
    """用户界面类"""

    def __init__(self, screen: pygame.Surface):
        """
        初始化界面

        Args:
            screen: Pygame屏幕对象
        """
        self.screen = screen
        self.fonts = self._load_fonts()
        self.animation_frame = 0

    def _load_fonts(self) -> dict:
        """
        加载字体

        Returns:
            dict: 字体字典
        """
        fonts = {}

        # 尝试加载中文字体
        chinese_fonts = [
            # Linux常见中文字体
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
            # Windows中文字体
            'C:/Windows/Fonts/msyh.ttc',
            'C:/Windows/Fonts/simhei.ttf',
            'C:/Windows/Fonts/simsun.ttc',
            # macOS中文字体
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/STHeiti Light.ttc',
            '/System/Library/Fonts/Hiragino Sans GB.ttc',
        ]

        font_path = None
        for path in chinese_fonts:
            if os.path.exists(path):
                font_path = path
                break

        try:
            if font_path:
                fonts['large'] = pygame.font.Font(font_path, FONT_SIZE_LARGE)
                fonts['medium'] = pygame.font.Font(font_path, FONT_SIZE_MEDIUM)
                fonts['small'] = pygame.font.Font(font_path, FONT_SIZE_SMALL)
            else:
                # 使用系统默认字体
                fonts['large'] = pygame.font.SysFont('sans', FONT_SIZE_LARGE)
                fonts['medium'] = pygame.font.SysFont('sans', FONT_SIZE_MEDIUM)
                fonts['small'] = pygame.font.SysFont('sans', FONT_SIZE_SMALL)
        except Exception:
            # 最后的备选方案
            fonts['large'] = pygame.font.Font(None, FONT_SIZE_LARGE)
            fonts['medium'] = pygame.font.Font(None, FONT_SIZE_MEDIUM)
            fonts['small'] = pygame.font.Font(None, FONT_SIZE_SMALL)

        return fonts

    def draw_background(self):
        """绘制背景"""
        self.screen.fill(COLORS['background'])

        # 绘制网格
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(
                self.screen,
                COLORS['grid'],
                (x, 0),
                (x, WINDOW_HEIGHT)
            )
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(
                self.screen,
                COLORS['grid'],
                (0, y),
                (WINDOW_WIDTH, y)
            )

    def draw_snake(self, body: list, colors: list):
        """
        绘制蛇

        Args:
            body: 蛇身坐标列表
            colors: 蛇身颜色列表
        """
        for i, (pos, color) in enumerate(zip(body, colors)):
            x, y = pos
            rect = pygame.Rect(
                x * GRID_SIZE + 1,
                y * GRID_SIZE + 1,
                GRID_SIZE - 2,
                GRID_SIZE - 2
            )

            # 蛇头绘制特殊效果
            if i == 0:
                # 绘制圆角矩形作为蛇头
                pygame.draw.rect(
                    self.screen,
                    color,
                    rect,
                    border_radius=5
                )
                # 绘制眼睛
                self._draw_eyes(rect)
            else:
                # 蛇身绘制圆角矩形
                pygame.draw.rect(
                    self.screen,
                    color,
                    rect,
                    border_radius=3
                )

    def _draw_eyes(self, head_rect: pygame.Rect):
        """
        绘制蛇的眼睛

        Args:
            head_rect: 蛇头矩形
        """
        eye_size = 4
        eye_color = (255, 255, 255)
        pupil_color = (0, 0, 0)

        # 左眼
        left_eye_pos = (
            head_rect.left + 5,
            head_rect.top + 5
        )
        pygame.draw.circle(
            self.screen,
            eye_color,
            left_eye_pos,
            eye_size
        )
        pygame.draw.circle(
            self.screen,
            pupil_color,
            left_eye_pos,
            eye_size // 2
        )

        # 右眼
        right_eye_pos = (
            head_rect.right - 5,
            head_rect.top + 5
        )
        pygame.draw.circle(
            self.screen,
            eye_color,
            right_eye_pos,
            eye_size
        )
        pygame.draw.circle(
            self.screen,
            pupil_color,
            right_eye_pos,
            eye_size // 2
        )

    def draw_food(self, position: Tuple[int, int], pulse_scale: float):
        """
        绘制食物

        Args:
            position: 食物位置
            pulse_scale: 脉动缩放比例
        """
        x, y = position
        center_x = x * GRID_SIZE + GRID_SIZE // 2
        center_y = y * GRID_SIZE + GRID_SIZE // 2

        # 基础半径
        base_radius = GRID_SIZE // 2 - 2

        # 应用脉动效果
        radius = int(base_radius * pulse_scale)

        # 绘制外圈光晕
        glow_color = (
            min(COLORS['food'][0] + 50, 255),
            min(COLORS['food'][1] + 50, 255),
            min(COLORS['food'][2] + 50, 255)
        )
        pygame.draw.circle(
            self.screen,
            glow_color,
            (center_x, center_y),
            radius + 3
        )

        # 绘制主体
        pygame.draw.circle(
            self.screen,
            COLORS['food'],
            (center_x, center_y),
            radius
        )

        # 绘制高光
        highlight_pos = (
            center_x - radius // 3,
            center_y - radius // 3
        )
        pygame.draw.circle(
            self.screen,
            (255, 200, 200),
            highlight_pos,
            radius // 3
        )

    def draw_score(self, score: int):
        """
        绘制分数

        Args:
            score: 当前分数
        """
        score_text = f"分数: {score}"
        text_surface = self.fonts['medium'].render(
            score_text,
            True,
            COLORS['text']
        )
        self.screen.blit(text_surface, (20, 15))

    def draw_menu(self):
        """绘制主菜单"""
        # 半透明背景
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(COLORS['menu_bg'])
        self.screen.blit(overlay, (0, 0))

        # 标题
        title = self.fonts['large'].render(
            "贪吃蛇",
            True,
            COLORS['snake_head']
        )
        title_rect = title.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)
        )
        self.screen.blit(title, title_rect)

        # 开始提示（闪烁效果）
        self.animation_frame += 1
        if (self.animation_frame // 30) % 2 == 0:
            start_text = self.fonts['medium'].render(
                "按 空格键 或 回车键 开始游戏",
                True,
                COLORS['text']
            )
            start_rect = start_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            )
            self.screen.blit(start_text, start_rect)

        # 操作说明
        instructions = [
            "操作说明:",
            "↑ ↓ ← → 或 W A S D 控制方向",
            "ESC 暂停游戏",
            "Q 退出游戏"
        ]

        for i, text in enumerate(instructions):
            inst_surface = self.fonts['small'].render(
                text,
                True,
                COLORS['text']
            )
            inst_rect = inst_surface.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 2 // 3 + i * 30)
            )
            self.screen.blit(inst_surface, inst_rect)

    def draw_pause(self):
        """绘制暂停界面"""
        # 半透明背景
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(COLORS['menu_bg'])
        self.screen.blit(overlay, (0, 0))

        # 暂停文字
        pause_text = self.fonts['large'].render(
            "游戏暂停",
            True,
            COLORS['text']
        )
        pause_rect = pause_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)
        )
        self.screen.blit(pause_text, pause_rect)

        # 继续提示
        continue_text = self.fonts['medium'].render(
            "按 ESC 继续游戏",
            True,
            COLORS['text']
        )
        continue_rect = continue_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30)
        )
        self.screen.blit(continue_text, continue_rect)

    def draw_game_over(self, score: int):
        """
        绘制游戏结束界面

        Args:
            score: 最终分数
        """
        # 半透明背景
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(COLORS['menu_bg'])
        self.screen.blit(overlay, (0, 0))

        # 游戏结束文字
        game_over_text = self.fonts['large'].render(
            "游戏结束",
            True,
            COLORS['game_over']
        )
        game_over_rect = game_over_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)
        )
        self.screen.blit(game_over_text, game_over_rect)

        # 最终分数
        final_score = self.fonts['medium'].render(
            f"最终分数: {score}",
            True,
            COLORS['text']
        )
        final_score_rect = final_score.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        self.screen.blit(final_score, final_score_rect)

        # 重新开始提示
        restart_text = self.fonts['medium'].render(
            "按 R 重新开始  |  按 Q 退出",
            True,
            COLORS['text']
        )
        restart_rect = restart_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 2 // 3)
        )
        self.screen.blit(restart_text, restart_rect)

    def draw_border(self):
        """绘制游戏边界"""
        pygame.draw.rect(
            self.screen,
            COLORS['border'],
            (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
            2
        )