"""
皮肤系统模块
Skin System Module
"""
import os
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

from .logger import get_logger


@dataclass
class SkinTheme:
    """皮肤主题"""
    name: str
    display_name: str
    snake_head: Tuple[int, int, int]
    snake_body: Tuple[int, int, int]
    food: Tuple[int, int, int]
    food_glow: Tuple[int, int, int]
    description: str = ""

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'name': self.name,
            'display_name': self.display_name,
            'snake_head': list(self.snake_head),
            'snake_body': list(self.snake_body),
            'food': list(self.food),
            'food_glow': list(self.food_glow),
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'SkinTheme':
        """从字典创建"""
        return cls(
            name=data['name'],
            display_name=data['display_name'],
            snake_head=tuple(data['snake_head']),
            snake_body=tuple(data['snake_body']),
            food=tuple(data['food']),
            food_glow=tuple(data['food_glow']),
            description=data.get('description', '')
        )


# 预定义皮肤主题
BUILTIN_SKINS: List[SkinTheme] = [
    SkinTheme(
        name='classic',
        display_name='经典绿',
        snake_head=(0, 255, 136),
        snake_body=(0, 200, 100),
        food=(255, 107, 107),
        food_glow=(255, 157, 157),
        description='经典绿色蛇身，红色食物'
    ),
    SkinTheme(
        name='ocean',
        display_name='海洋蓝',
        snake_head=(0, 191, 255),
        snake_body=(30, 144, 255),
        food=(255, 215, 0),
        food_glow=(255, 235, 100),
        description='蓝色蛇身，金色食物'
    ),
    SkinTheme(
        name='purple',
        display_name='梦幻紫',
        snake_head=(186, 85, 211),
        snake_body=(148, 0, 211),
        food=(255, 20, 147),
        food_glow=(255, 100, 180),
        description='紫色蛇身，粉色食物'
    ),
    SkinTheme(
        name='golden',
        display_name='金色辉煌',
        snake_head=(255, 215, 0),
        snake_body=(218, 165, 32),
        food=(220, 20, 60),
        food_glow=(255, 80, 100),
        description='金色蛇身，深红食物'
    ),
    SkinTheme(
        name='fire',
        display_name='火焰红',
        snake_head=(255, 69, 0),
        snake_body=(255, 140, 0),
        food=(50, 205, 50),
        food_glow=(100, 255, 100),
        description='橙红蛇身，绿色食物'
    ),
    SkinTheme(
        name='neon',
        display_name='霓虹夜',
        snake_head=(0, 255, 255),
        snake_body=(255, 0, 255),
        food=(255, 255, 0),
        food_glow=(200, 200, 50),
        description='青色蛇头，紫色蛇身，黄色食物'
    ),
    SkinTheme(
        name='forest',
        display_name='森林绿',
        snake_head=(34, 139, 34),
        snake_body=(0, 100, 0),
        food=(255, 165, 0),
        food_glow=(255, 200, 100),
        description='深绿蛇身，橙色食物'
    ),
    SkinTheme(
        name='ice',
        display_name='冰晶蓝',
        snake_head=(173, 216, 230),
        snake_body=(135, 206, 250),
        food=(255, 99, 71),
        food_glow=(255, 150, 130),
        description='冰蓝蛇身，番茄红食物'
    ),
]


class SkinManager:
    """皮肤管理器"""

    DEFAULT_SKIN = 'classic'

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化皮肤管理器

        Args:
            config_path: 配置文件路径
        """
        self.logger = get_logger()
        self.skins: Dict[str, SkinTheme] = {}
        self._load_builtin_skins()
        self.current_skin_name = self.DEFAULT_SKIN

        if config_path is None:
            self.config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'skin_config.json'
            )
        else:
            self.config_path = config_path

        self._load_config()

    def _load_builtin_skins(self):
        """加载内置皮肤"""
        for skin in BUILTIN_SKINS:
            self.skins[skin.name] = skin
        self.logger.debug(f"已加载 {len(self.skins)} 个内置皮肤")

    def _load_config(self):
        """加载配置"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    skin_name = data.get('current_skin', self.DEFAULT_SKIN)
                    if skin_name in self.skins:
                        self.current_skin_name = skin_name
                        self.logger.info(f"加载皮肤配置: {skin_name}")
        except (json.JSONDecodeError, IOError) as e:
            self.logger.warning(f"加载皮肤配置失败: {e}")

    def _save_config(self):
        """保存配置"""
        try:
            data = {
                'current_skin': self.current_skin_name
            }
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.debug(f"保存皮肤配置: {self.current_skin_name}")
        except IOError as e:
            self.logger.warning(f"保存皮肤配置失败: {e}")

    def get_skin(self, name: Optional[str] = None) -> SkinTheme:
        """
        获取皮肤主题

        Args:
            name: 皮肤名称，为空则返回当前皮肤

        Returns:
            SkinTheme: 皮肤主题
        """
        if name is None:
            name = self.current_skin_name
        return self.skins.get(name, self.skins[self.DEFAULT_SKIN])

    def set_skin(self, name: str) -> bool:
        """
        设置当前皮肤

        Args:
            name: 皮肤名称

        Returns:
            bool: 是否设置成功
        """
        if name in self.skins:
            old_skin = self.current_skin_name
            self.current_skin_name = name
            self._save_config()
            self.logger.info(f"切换皮肤: {old_skin} -> {name}")
            return True
        self.logger.warning(f"皮肤不存在: {name}")
        return False

    def get_all_skins(self) -> List[SkinTheme]:
        """
        获取所有皮肤

        Returns:
            List[SkinTheme]: 皮肤列表
        """
        return list(self.skins.values())

    def get_skin_names(self) -> List[str]:
        """
        获取所有皮肤名称

        Returns:
            List[str]: 皮肤名称列表
        """
        return list(self.skins.keys())

    def get_current_skin_name(self) -> str:
        """获取当前皮肤名称"""
        return self.current_skin_name

    def __len__(self) -> int:
        """获取皮肤数量"""
        return len(self.skins)

    def __contains__(self, name: str) -> bool:
        """检查皮肤是否存在"""
        return name in self.skins


# 全局皮肤管理器实例
_skin_manager: Optional[SkinManager] = None


def get_skin_manager() -> SkinManager:
    """获取皮肤管理器实例"""
    global _skin_manager
    if _skin_manager is None:
        _skin_manager = SkinManager()
    return _skin_manager