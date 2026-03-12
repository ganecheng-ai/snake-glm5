"""
高分榜模块
High Score Leaderboard Module
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class HighScoreManager:
    """高分榜管理器"""

    DEFAULT_MAX_SCORES = 10

    def __init__(self, file_path: Optional[str] = None, max_scores: int = DEFAULT_MAX_SCORES):
        """
        初始化高分榜管理器

        Args:
            file_path: 高分榜文件路径，默认为项目目录下的 highscores.json
            max_scores: 最大保存分数数量
        """
        if file_path is None:
            self.file_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'highscores.json'
            )
        else:
            self.file_path = file_path

        self.max_scores = max_scores
        self.scores: List[Dict] = []
        self._load_scores()

    def _load_scores(self):
        """从文件加载高分榜"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.scores = data.get('scores', [])
        except (json.JSONDecodeError, IOError) as e:
            self.scores = []

    def _save_scores(self):
        """保存高分榜到文件"""
        try:
            data = {
                'scores': self.scores,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            pass  # 静默处理保存失败

    def add_score(self, score: int, player_name: str = "玩家") -> int:
        """
        添加新分数

        Args:
            score: 分数
            player_name: 玩家名称

        Returns:
            int: 排名（1-based），如果未进入排行榜返回 -1
        """
        entry = {
            'score': score,
            'name': player_name,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }

        # 检查是否能进入排行榜
        if len(self.scores) >= self.max_scores:
            if score <= self.scores[-1]['score']:
                return -1

        # 插入分数
        self.scores.append(entry)
        # 按分数降序排序
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        # 保留前 max_scores 个
        self.scores = self.scores[:self.max_scores]

        # 保存
        self._save_scores()

        # 返回排名
        for i, s in enumerate(self.scores):
            if s['score'] == score and s['name'] == player_name:
                return i + 1
        return -1

    def is_high_score(self, score: int) -> bool:
        """
        检查分数是否能进入排行榜

        Args:
            score: 分数

        Returns:
            bool: 是否能进入排行榜
        """
        if len(self.scores) < self.max_scores:
            return True
        return score > self.scores[-1]['score']

    def get_rank(self, score: int) -> int:
        """
        获取分数的排名

        Args:
            score: 分数

        Returns:
            int: 排名（1-based），如果未进入排行榜返回 -1
        """
        for i, s in enumerate(self.scores):
            if score >= s['score']:
                return i + 1
        if len(self.scores) < self.max_scores:
            return len(self.scores) + 1
        return -1

    def get_top_scores(self, count: int = 10) -> List[Dict]:
        """
        获取前 N 名分数

        Args:
            count: 获取数量

        Returns:
            List[Dict]: 分数列表
        """
        return self.scores[:count]

    def get_high_score(self) -> int:
        """
        获取最高分

        Returns:
            int: 最高分，如果没有记录返回 0
        """
        if self.scores:
            return self.scores[0]['score']
        return 0

    def clear_scores(self):
        """清空高分榜"""
        self.scores = []
        self._save_scores()

    def __len__(self) -> int:
        """获取分数数量"""
        return len(self.scores)

    def __iter__(self):
        """迭代分数"""
        return iter(self.scores)


# 全局高分榜实例
_highscore_manager: Optional[HighScoreManager] = None


def get_highscore_manager() -> HighScoreManager:
    """获取高分榜管理器实例"""
    global _highscore_manager
    if _highscore_manager is None:
        _highscore_manager = HighScoreManager()
    return _highscore_manager