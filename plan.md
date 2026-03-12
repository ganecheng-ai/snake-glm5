# 贪吃蛇游戏开发计划

## 项目概述
使用 Python + Pygame 开发一个精美的贪吃蛇游戏，支持简体中文界面。

## 技术栈
- **语言**: Python 3.10+
- **游戏框架**: Pygame
- **构建工具**: PyInstaller (打包为可执行文件)

## 开发阶段

### 第一阶段：核心游戏功能 ✅
- [x] 创建项目结构
- [x] 游戏主循环
- [x] 蛇的移动与控制
- [x] 食物生成与碰撞检测
- [x] 分数系统
- [x] 游戏结束逻辑

### 第二阶段：界面美化 ✅
- [x] 精美的视觉效果
- [x] 渐变色彩蛇身
- [x] 动画效果（食物脉动）
- [x] 中文界面支持

### 第三阶段：用户体验优化 ✅
- [x] 开始菜单
- [x] 暂停功能
- [x] 游戏设置（config.py）
- [ ] 音效支持（可选）

### 第四阶段：发布与部署 ✅
- [x] 单元测试（18个测试用例全部通过）
- [x] GitHub Actions CI/CD
- [x] 多平台构建 (Windows/Linux/macOS)
- [x] 自动发布 Release

## 文件结构
```
snake-glm5/
├── snake_game/          # 游戏主模块
│   ├── __init__.py
│   ├── main.py          # 游戏入口
│   ├── game.py          # 游戏逻辑
│   ├── snake.py         # 蛇类
│   ├── food.py          # 食物类
│   ├── ui.py            # 界面渲染
│   └── config.py        # 配置文件
├── tests/               # 测试目录
│   ├── __init__.py
│   └── test_game.py
├── .github/
│   └── workflows/
│       └── release.yml  # 发布工作流
├── requirements.txt     # 依赖文件
├── setup.py            # 安装配置
├── plan.md             # 开发计划
├── README.md           # 项目说明
├── run_game.py         # 启动脚本
├── .gitignore          # Git忽略配置
└── LICENSE             # 许可证
```

## 版本规划
- **v1.0.0**: 基础游戏功能 + 中文界面 ✅
- **v1.1.0**: 音效 + 设置菜单（计划中）
- **v1.2.0**: 高分榜 + 皮肤系统（计划中）

## 当前状态
✅ v1.0.1 已发布！[下载地址](https://github.com/ganecheng-ai/snake-glm5/releases/tag/v1.0.1)

### v1.0.1 更新内容
- 修复 GitHub Actions 发布工作流权限问题
- 成功发布 Windows/Linux/macOS 三个平台的构建产物