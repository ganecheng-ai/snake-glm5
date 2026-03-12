# 贪吃蛇游戏 (Snake Game)

一个使用 Python + Pygame 开发的精美贪吃蛇游戏，支持简体中文界面。

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.5%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 功能特点

- 🎮 经典贪吃蛇玩法
- 🎨 精美的视觉效果
  - 渐变色蛇身
  - 脉动动画食物
  - 网格背景
- 🇨🇳 完整的中文界面支持
- ⚡ 平滑的游戏体验
- 🎯 分数系统
- 📊 速度递增难度
- 📝 日志系统（方便问题定位）

## 游戏截图

游戏界面包含：
- 主菜单界面
- 游戏进行界面
- 暂停界面
- 游戏结束界面

## 安装

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/ganecheng-ai/snake-glm5.git
cd snake-glm5

# 安装依赖
pip install -r requirements.txt

# 运行游戏
python -m snake_game
```

### 或直接运行

```bash
python run_game.py
```

## 游戏操作

| 按键 | 功能 |
|------|------|
| ↑ / W | 向上移动 |
| ↓ / S | 向下移动 |
| ← / A | 向左移动 |
| → / D | 向右移动 |
| ESC | 暂停/继续游戏 |
| 空格 / 回车 | 开始游戏 |
| R | 重新开始（游戏结束后） |
| Q | 退出游戏 |

## 游戏规则

1. 使用方向键控制蛇的移动方向
2. 吃到食物（红色圆点）可以增加蛇的长度和分数
3. 每吃一个食物得 10 分
4. 蛇的移动速度会随着分数增加而加快
5. 撞到墙壁或自己的身体会导致游戏结束

## 项目结构

```
snake-glm5/
├── snake_game/           # 游戏主模块
│   ├── __init__.py       # 模块初始化
│   ├── config.py         # 游戏配置
│   ├── game.py           # 游戏主逻辑
│   ├── snake.py          # 蛇类
│   ├── food.py           # 食物类
│   ├── ui.py             # 界面渲染
│   ├── logger.py         # 日志系统
│   └── main.py           # 游戏入口
├── logs/                 # 日志目录（自动生成）
├── tests/                # 测试目录
│   ├── __init__.py
│   └── test_game.py      # 单元测试
├── .github/
│   └── workflows/
│       └── release.yml   # 发布工作流
├── plan.md               # 开发计划
├── README.md             # 项目说明
├── requirements.txt      # 依赖文件
├── setup.py              # 安装配置
├── run_game.py           # 启动脚本
└── LICENSE               # 许可证
```

## 开发

### 运行测试

```bash
python -m pytest tests/ -v
# 或
python -m unittest discover tests/
```

### 代码规范

- 使用 Python 3.10+ 语法特性
- 遵循 PEP 8 编码规范
- 使用类型注解
- 保持代码简洁清晰

## 发布版本

本项目使用 GitHub Actions 自动构建和发布。

支持的平台：
- **Windows**: `.zip` 压缩包
- **Linux**: `.tar.gz` 压缩包
- **macOS**: `.tar.gz` 压缩包

每次发布新版本（创建 `v*` 标签）时，会自动：
1. 运行单元测试
2. 在三个平台上构建
3. 生成 SHA256 校验文件
4. 创建 GitHub Release

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 致谢

- [Pygame](https://www.pygame.org/) - Python 游戏开发库
- [Claude Code](https://claude.com/) - AI 辅助开发