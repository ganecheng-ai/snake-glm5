# 贪吃蛇游戏配置文件
# Snake Game Configuration

# 窗口设置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "贪吃蛇"

# 颜色定义 (RGB)
COLORS = {
    'background': (26, 26, 46),
    'grid': (40, 40, 70),
    'snake_head': (0, 255, 136),
    'snake_body': (0, 200, 100),
    'food': (255, 107, 107),
    'text': (255, 255, 255),
    'game_over': (255, 80, 80),
    'menu_bg': (30, 30, 50),
    'button': (70, 130, 180),
    'button_hover': (100, 160, 210),
    'border': (60, 60, 100),
}

# 游戏设置
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 速度设置
INITIAL_SPEED = 10
SPEED_INCREMENT = 1
MAX_SPEED = 25

# 蛇的初始位置
INITIAL_SNAKE_LENGTH = 3
INITIAL_SNAKE_POSITION = (GRID_WIDTH // 2, GRID_HEIGHT // 2)

# 食物设置
FOOD_SPAWN_INTERVAL = 100  # 毫秒

# 字体设置
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 24

# 游戏状态
STATE_MENU = 0
STATE_PLAYING = 1
STATE_PAUSED = 2
STATE_GAME_OVER = 3

# 方向
DIRECTION_UP = (0, -1)
DIRECTION_DOWN = (0, 1)
DIRECTION_LEFT = (-1, 0)
DIRECTION_RIGHT = (1, 0)