"""
贪吃蛇游戏
Snake Game

一个使用 Pygame 开发的精美贪吃蛇游戏，支持中文界面。

使用方法:
    python -m snake_game

或者:
    from snake_game import Game
    game = Game()
    game.run()
"""

from .game import Game
from .snake import Snake
from .food import Food
from .ui import UI
from .highscore import HighScoreManager, get_highscore_manager
from .config import *

__version__ = '1.2.1'
__author__ = 'Claude Code'

__all__ = ['Game', 'Snake', 'Food', 'UI', 'HighScoreManager', 'get_highscore_manager', 'main']


def main():
    """游戏主入口"""
    game = Game()
    game.run()