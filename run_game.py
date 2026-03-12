#!/usr/bin/env python
"""
贪吃蛇游戏启动脚本
Snake Game Launcher
"""
import sys
import os

# 确保可以找到 snake_game 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from snake_game import main

if __name__ == '__main__':
    main()