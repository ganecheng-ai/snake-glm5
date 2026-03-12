"""
贪吃蛇游戏入口
Snake Game Entry Point
"""
from .game import Game


def main():
    """游戏主入口"""
    game = Game()
    game.run()


if __name__ == '__main__':
    main()