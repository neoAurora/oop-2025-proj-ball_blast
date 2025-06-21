# gacha.py
"""Gacha (抽卡) 系統 - 含金幣消耗與效果說明"""
from __future__ import annotations
import random
from typing import List, Tuple, Dict

# 卡牌設定 - 新增稀有度分級
CARD_POOL: List[Dict] = [
    {
        "name": "TOYZ(R)", 
        "weight": 16,
        "img": "image/cards/card0.jpg",
        "effect": {"cannon_speed+4"},
        "rarity": "R"
    },
    {
        "name": "一步都沒有退(R)",
        "weight": 15,
        "img": "image/cards/card1.jpg",
        "effect": {"damage+1, bullet_per_second-5"},
        "rarity": "R"
    },
    {
        "name": "咻碰阿罵(R)",
        "weight": 16,
        "img": "image/cards/card2.jpg",
        "effect": {"crit_damage+25%"},
        "rarity": "R"
    },
    {
        "name": "張家檸檬綠茶(R)",
        "weight": 16,
        "img": "image/cards/card3.jpg",
        "effect": {"coins*0.25"},
        "rarity": "R"
    },
    {
        "name": "杰哥的麵包(R)", 
        "weight": 16,
        "img": "image/cards/card4.png",
        "effect": {"crit_rate+15%"},
        "rarity": "R"
    },
    {
        "name": "114514(SR)", 
        "weight": 5,
        "img": "image/cards/card5.jpg",
        "effect": {"damage+3"},
        "rarity": "SR"
    },
    {
        "name": "MVP(SR)", 
        "weight": 5,
        "img": "image/cards/card6.jpg",
        "effect": {"bullet_per_second+10, coins-500"},
        "rarity": "SR"
    },
    {
        "name": "圓神啟動(SR)", 
        "weight": 5,
        "img": "image/cards/card7.jpg",
        "effect": {"crit_rate+50%, crit_damage+75%"},
        "rarity": "SR"
    },
    {
        "name": "最強(SSR)", 
        "weight": 2,
        "img": "image/cards/card8.jpg",
        "effect": {"bullet_rows+1"},
        "rarity": "SSR"
    },
    {
        "name": "oop之神(UR)", 
        "weight": 1,
        "img": "image/cards/card9.jpg",
        "effect": {"???"},
        "rarity": "UR"
    }
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
        self.game.apply_card_effect(name)
        

        return name, img_path, effect, rarity
    
    def draw_card_for_free(self):
        """免費抽卡（不扣金幣）"""
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

        self.game.apply_card_effect(name)
        return name, img_path, effect, rarity
