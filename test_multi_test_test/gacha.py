# gacha.py
"""Gacha (抽卡) 系統 - 含金幣消耗與效果說明"""
from __future__ import annotations
import random
from typing import List, Tuple, Dict

# 卡牌設定 - 新增稀有度分級
CARD_POOL: List[Dict] = [
    # 普通卡 (70% 機率)
    {
        "name": "藍裕棋の祝福", 
        "weight": 7,
        "img": "image/cards/card1.jpeg",
        "effect": {"damage_bonus": +1},
        "rarity": "普通"
    },
    {
        "name": "施至遠の意志",
        "weight": 7,
        "img": "image/cards/card2.jpeg",
        "effect": {"shot_delay": -10},
        "rarity": "普通"
    },
    # 稀有卡 (25% 機率)
    {
        "name": "王學誠の怒火",
        "weight": 2.5,
        "img": "image/cards/card3.jpeg",
        "effect": {"bullets_per_second": +5},
        "rarity": "稀有"
    },
    # 傳說卡 (5% 機率)
    {
        "name": "賴城諭の忍耐",
        "weight": 0.5,
        "img": "image/cards/card4.jpeg",
        "effect": {"cannon_hp": +2, "damage_bonus": +1},
        "rarity": "傳說"
    },
]
TOTAL_WEIGHT = sum(c["weight"] for c in CARD_POOL)

class GachaSystem:
    """隨機抽卡系統 - 含金幣消耗"""
    
    COST_PER_DRAW = 100  # 每次抽卡消耗100金幣
    
    def __init__(self, game):
        self.game = game
    
    def can_draw(self) -> bool:
        """檢查是否有足夠金幣抽卡"""
        return self.game.coins >= self.COST_PER_DRAW
    
    def draw_card(self):
        if not self.can_draw():
            return None

        self.game.coins -= 100

        # 抽卡機率
        r = random.uniform(0, TOTAL_WEIGHT)
        acc = 0
        for card in CARD_POOL:
            acc += card["weight"]
            if r <= acc:
                selected = card
                break
        else:
            selected = CARD_POOL[-1]

        name = selected["name"]
        img_path = selected["img"]
        effect = selected["effect"]
        rarity = selected["rarity"]

        # ⚠️ 不在這裡播動畫，交給主程式處理
        self.game.apply_card_effect(effect)

        return name, img_path, effect, rarity
