# gacha.py
"""Gacha (抽卡) 系統  —  含效果說明

Game 破關後呼叫：
    name, img_path, effect = self.gacha_system.draw_card()
    self.apply_card_effect(effect)   # 交給 Game 處理具體數值變動

- 每張卡現在都含 `effect` 欄位，清楚描述對應影響（對 Game 屬性或參數的變動）。
- 如果只想要卡名與圖片也行：忽略第三個回傳值即可。
"""
from __future__ import annotations
import random
from typing import List, Tuple, Dict

# ===== 卡牌設定 ============================================================
# effect: 描述要改動的屬性與數值，讓上層 Game 有彈性自行處理
CARD_POOL: List[Dict] = [
    {
        "name": "藍裕棋の祝福",          # 子彈傷害↑
        "weight": 1,
        "img": "image/cards/card1.jpeg",   # ← 副檔名改成 .jpeg
        "effect": {"damage_bonus": +1}
    },
    {
        "name": "施至遠の意志",          # 射速提升
        "weight": 1,
        "img": "image/cards/card2.jpeg",   # ← 副檔名改成 .jpeg
        "effect": {"shot_delay": -10}   # 每發間隔 -10ms
    },
    {
        "name": "王學誠の怒火",          # 連射次數↑
        "weight": 1,
        "img": "image/cards/card3.jpeg",   # ← 副檔名改成 .jpeg
        "effect": {"bullets_per_second": +5}
    },
    {
        "name": "賴城諭の忍耐",          # 砲台耐久↑
        "weight": 1,
        "img": "image/cards/card4.jpeg",   # ← 副檔名改成 .jpeg
        "effect": {"cannon_hp": +1}
    },
]
TOTAL_WEIGHT = sum(c["weight"] for c in CARD_POOL)

# ==========================================================================
class GachaSystem:
    """隨機抽卡系統——回傳 (卡名, 圖檔, effect dict)"""

    def __init__(self, game):
        self.game = game

    # ------------------------------------------------------------------
    def draw_card(self) -> Tuple[str, str, Dict]:
        r = random.uniform(0, TOTAL_WEIGHT)
        acc = 0.0
        for card in CARD_POOL:
            acc += card["weight"]
            if r <= acc:
                return card["name"], card["img"], card["effect"]
        last = CARD_POOL[-1]
        return last["name"], last["img"], last["effect"]


# -------------------------- 測試 -----------------------------------------
if __name__ == "__main__":
    class _DummyGame:
        def apply_card_effect(self, eff):
            print("套用效果 →", eff)

    gs = GachaSystem(_DummyGame())
    for _ in range(4):
        print(gs.draw_card())

